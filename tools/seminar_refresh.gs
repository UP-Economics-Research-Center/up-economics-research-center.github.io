/**
 * Private, standalone Google Apps Script. See docs/seminar-refresh-setup.md.
 * Never paste credentials into this file or deploy this project as a web app.
 */
const SEMINAR_WORKBOOK = '10-ZeGcNtUeQB5wXC0-f6FYuosoiduBeAyMvPtvR1KzI';
const SEMINAR_REPOSITORY = 'UP-Economics-Research-Center/up-economics-research-center.github.io';

function base64Url_(value) {
  return Utilities.base64EncodeWebSafe(value).replace(/=+$/, '');
}

function githubPost_(path, token, body, expectedStatus) {
  const response = UrlFetchApp.fetch('https://api.github.com' + path, {
    method: 'post',
    contentType: 'application/json',
    headers: {
      Authorization: 'Bearer ' + token,
      Accept: 'application/vnd.github+json',
      'X-GitHub-Api-Version': '2022-11-28',
    },
    payload: JSON.stringify(body),
    muteHttpExceptions: true,
  });
  if (response.getResponseCode() !== expectedStatus) {
    // Never include response bodies, tokens, JWTs or key material in errors.
    throw new Error('GitHub rejected ' + path + ' (HTTP ' + response.getResponseCode()
      + '). Check the private app credentials, installation and Actions write permission.');
  }
  return response;
}

function githubAppToken_(properties) {
  const clientId = properties.getProperty('GITHUB_APP_CLIENT_ID');
  const installationId = properties.getProperty('GITHUB_APP_INSTALLATION_ID');
  const encodedKey = properties.getProperty('GITHUB_APP_PRIVATE_KEY_BASE64');
  if (!clientId || !installationId || !encodedKey) {
    throw new Error('Set GITHUB_APP_CLIENT_ID, GITHUB_APP_INSTALLATION_ID and '
      + 'GITHUB_APP_PRIVATE_KEY_BASE64 in the private Script Properties.');
  }
  if (!/^\d+$/.test(installationId)) throw new Error('Invalid GitHub App installation ID.');
  const keyBody = encodedKey.replace(/\s/g, '');
  if (!/^[A-Za-z0-9+/]+={0,2}$/.test(keyBody)) {
    throw new Error('Private key must be base64-encoded PKCS#8 DER; see the setup guide.');
  }
  const key = '-----BEGIN PRIVATE KEY-----\n' + keyBody.match(/.{1,64}/g).join('\n')
    + '\n-----END PRIVATE KEY-----';
  const now = Math.floor(Date.now() / 1000);
  const unsigned = base64Url_(JSON.stringify({ alg: 'RS256', typ: 'JWT' })) + '.'
    + base64Url_(JSON.stringify({ iat: now - 60, exp: now + 540, iss: clientId }));
  let signature;
  try {
    signature = Utilities.computeRsaSha256Signature(unsigned, key);
  } catch {
    throw new Error('Cannot sign with the private GitHub App key; check the PKCS#8 conversion.');
  }
  const jwt = unsigned + '.' + base64Url_(signature);
  const response = githubPost_('/app/installations/' + installationId + '/access_tokens', jwt, {
    repositories: [SEMINAR_REPOSITORY.split('/')[1]],
    permissions: { actions: 'write' },
  }, 201);
  const installation = JSON.parse(response.getContentText());
  if (typeof installation.token !== 'string' || !installation.token
      || installation.permissions?.actions !== 'write'
      || installation.repositories?.length !== 1
      || installation.repositories[0].full_name !== SEMINAR_REPOSITORY) {
    throw new Error('GitHub App token must grant Actions write access to the website repository only.');
  }
  // Mint a short-lived token on each request; never persist it or use a personal-token fallback.
  return installation.token;
}

function requestSeminarRefresh() {
  const properties = PropertiesService.getScriptProperties();
  const lock = LockService.getScriptLock();
  if (!lock.tryLock(1000)) return;
  try {
    // Coalesce a burst of cell edits; the timer also catches imports and API edits.
    const previous = Number(properties.getProperty('LAST_REQUESTED_AT') || 0);
    if (Date.now() - previous < 60000) return;
    const token = githubAppToken_(properties);
    githubPost_('/repos/' + SEMINAR_REPOSITORY + '/actions/workflows/pages.yml/dispatches',
      token, { ref: 'main' }, 204);
    properties.setProperty('LAST_REQUESTED_AT', String(Date.now()));
  } finally {
    lock.releaseLock();
  }
}

function refreshSeminarsOnEdit(event) {
  if (event && event.range.getSheet().getName() === 'Archivo') requestSeminarRefresh();
}

function installSeminarRefresh() {
  // Verify access before installing triggers. Re-running setup replaces only ours.
  requestSeminarRefresh();
  const handlers = ['requestSeminarRefresh', 'refreshSeminarsOnEdit'];
  for (const trigger of ScriptApp.getProjectTriggers()) {
    if (handlers.includes(trigger.getHandlerFunction())) ScriptApp.deleteTrigger(trigger);
  }
  ScriptApp.newTrigger('refreshSeminarsOnEdit').forSpreadsheet(SEMINAR_WORKBOOK).onEdit().create();
  ScriptApp.newTrigger('requestSeminarRefresh').timeBased().everyMinutes(30).create();
}
