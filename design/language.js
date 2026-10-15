/* A complete static page exists in each language; navigation works without storage. */
(() => {
  const language = document.documentElement.lang === 'es' ? 'es' : 'en';
  const prefix = language === 'es' ? '/es' : '';
  const url = new URL(location.href);
  const explicit = url.searchParams.get('lang');
  let preferred = null;
  try {
    if (explicit === 'en' || explicit === 'es') localStorage.setItem('up-language', explicit);
    preferred = explicit || localStorage.getItem('up-language');
  } catch { preferred = explicit; }
  if ((preferred === 'en' || preferred === 'es') && preferred !== language) {
    url.pathname = preferred === 'es' ? '/es' + url.pathname : url.pathname.replace(/^\/es(?=\/)/, '');
    location.replace(url.href);
  }
  window.SiteLanguage = {
    language, prefix,
    t: text => language === 'es' ? (window.UP_TRANSLATIONS?.[text] || text) : text,
  };
  document.addEventListener('DOMContentLoaded', () => {
    const links = [...document.querySelectorAll('[data-language]')];
    const refresh = link => {
      const target = new URL(link.href);
      target.search = location.search;
      target.searchParams.set('lang', link.dataset.language);
      target.hash = location.hash;
      link.href = target.href;
    };
    const refreshAll = () => links.forEach(refresh);
    links.forEach(link => {
      refresh(link);
      link.addEventListener('pointerdown', () => refresh(link));
      link.addEventListener('focus', () => refresh(link));
      link.addEventListener('click', () => {
        refresh(link);
        try { localStorage.setItem('up-language', link.dataset.language); } catch { /* URL selects the language. */ }
      });
    });
    window.addEventListener('hashchange', refreshAll);
    window.addEventListener('popstate', refreshAll);
    window.addEventListener('up:urlchange', refreshAll);
  });
})();
