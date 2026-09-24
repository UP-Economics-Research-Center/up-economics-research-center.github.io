const encoder = new TextEncoder();
const STATE_COOKIE = 'decap_oauth_state';
const STATE_TTL_MS = 10 * 60 * 1000;

function base64url(bytes) {
  let binary = '';
  for (const byte of bytes) binary += String.fromCharCode(byte);
  return btoa(binary).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

async function sign(value, secret) {
  const key = await crypto.subtle.importKey(
    'raw', encoder.encode(secret), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign'],
  );
  const signature = await crypto.subtle.sign('HMAC', key, encoder.encode(value));
  return base64url(new Uint8Array(signature));
}

async function makeState(secret) {
  const nonce = base64url(crypto.getRandomValues(new Uint8Array(24)));
  const expires = String(Date.now() + STATE_TTL_MS);
  const payload = `${nonce}.${expires}`;
  return `${payload}.${await sign(payload, secret)}`;
}

async function validState(state, secret) {
  if (!state || state.length > 256) return false;
  const parts = state.split('.');
  if (parts.length !== 3 || !/^\d+$/.test(parts[1]) || Number(parts[1]) < Date.now()) return false;
  return (await sign(`${parts[0]}.${parts[1]}`, secret)) === parts[2];
}

function page(origin, payload, success = true) {
  const outcome = success ? 'success' : 'error';
  const message = `authorization:github:${outcome}:${JSON.stringify(payload)}`;
  const html = `<!doctype html><meta charset="utf-8"><title>GitHub sign-in</title>
<script>
if (window.opener) {
  window.opener.postMessage(${JSON.stringify(message)}, ${JSON.stringify(origin)});
  window.close();
} else {
  document.body.textContent = 'Return to the Decap editor to continue.';
}
</script>`;
  return new Response(html, {
    headers: {
      'content-type': 'text/html; charset=utf-8',
      'cache-control': 'no-store',
      'x-content-type-options': 'nosniff',
      'content-security-policy': "default-src 'none'; script-src 'unsafe-inline'; base-uri 'none'; frame-ancestors 'none'",
      'set-cookie': `${STATE_COOKIE}=; HttpOnly; Secure; SameSite=Lax; Max-Age=0; Path=/callback`,
    },
  });
}

function stateCookie(request) {
  const cookie = (request.headers.get('cookie') || '').split(';')
    .map((part) => part.trim())
    .find((part) => part.startsWith(`${STATE_COOKIE}=`));
  return cookie ? cookie.slice(STATE_COOKIE.length + 1) : '';
}

function configured(env) {
  return Boolean(env.SITE_ORIGIN && env.GITHUB_CLIENT_ID && env.GITHUB_CLIENT_SECRET && env.STATE_SIGNING_SECRET);
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (!configured(env)) return new Response('Owner setup is incomplete.', { status: 503 });

    if (url.pathname === '/auth' && request.method === 'GET') {
      if (url.searchParams.get('provider') !== 'github') {
        return new Response('Unsupported provider.', { status: 400 });
      }
      const state = await makeState(env.STATE_SIGNING_SECRET);
      const authorize = new URL('https://github.com/login/oauth/authorize');
      authorize.searchParams.set('client_id', env.GITHUB_CLIENT_ID);
      authorize.searchParams.set('scope', 'public_repo');
      authorize.searchParams.set('state', state);
      return new Response(null, {
        status: 302,
        headers: {
          location: authorize.toString(),
          'cache-control': 'no-store',
          'set-cookie': `${STATE_COOKIE}=${state}; HttpOnly; Secure; SameSite=Lax; Max-Age=600; Path=/callback`,
        },
      });
    }

    if (url.pathname === '/callback' && request.method === 'GET') {
      const state = url.searchParams.get('state') || '';
      if (stateCookie(request) !== state || !(await validState(state, env.STATE_SIGNING_SECRET))) {
        return page(env.SITE_ORIGIN, { message: 'Invalid or expired sign-in state.' }, false);
      }
      if (url.searchParams.has('error')) {
        return page(env.SITE_ORIGIN, { message: 'GitHub sign-in was not completed.' }, false);
      }
      const code = url.searchParams.get('code');
      if (!code) {
        return page(env.SITE_ORIGIN, { message: 'GitHub did not return an authorization code.' }, false);
      }

      const tokenResponse = await fetch('https://github.com/login/oauth/access_token', {
        method: 'POST',
        headers: { accept: 'application/json', 'content-type': 'application/json' },
        body: JSON.stringify({
          client_id: env.GITHUB_CLIENT_ID,
          client_secret: env.GITHUB_CLIENT_SECRET,
          code,
        }),
      });
      if (!tokenResponse.ok) {
        return page(env.SITE_ORIGIN, { message: 'GitHub token exchange failed.' }, false);
      }
      const tokenData = await tokenResponse.json();
      if (!tokenData.access_token) {
        return page(env.SITE_ORIGIN, { message: 'GitHub did not grant access.' }, false);
      }
      return page(env.SITE_ORIGIN, { token: tokenData.access_token, provider: 'github' });
    }

    return new Response('Not found.', { status: 404, headers: { 'cache-control': 'no-store' } });
  },
};
