/* Optional, consent-gated traffic measurement. No provider code loads before acceptance. */
(() => {
  const config = document.currentScript;
  const token = config?.dataset.analyticsToken;
  const productionHost = config?.dataset.siteHost;
  if (!token || !/^[a-f0-9]{32}$/i.test(token)) return;
  const es = document.documentElement.lang === 'es';
  const text = (en, spanish) => es ? spanish : en;
  const storageKey = 'up-analytics-consent-v1';
  const lifetime = 180 * 24 * 60 * 60 * 1000;
  let loaded = false;
  let choice = null;
  try {
    const saved = JSON.parse(localStorage.getItem(storageKey));
    if (saved && ['accepted', 'rejected'].includes(saved.choice) && typeof saved.at === 'number' && saved.at <= Date.now() && Date.now() - saved.at < lifetime) choice = saved.choice;
  } catch { /* Storage is optional. A fresh choice applies to this page. */ }
  const privacySignal = navigator.globalPrivacyControl === true || navigator.doNotTrack === '1';
  const load = () => {
    if (loaded || location.hostname !== productionHost || privacySignal) return;
    loaded = true;
    const beacon = document.createElement('script');
    beacon.src = 'https://static.cloudflareinsights.com/beacon.min.js';
    beacon.type = 'module';
    beacon.dataset.cfBeacon = JSON.stringify({token, spa: false});
    document.head.append(beacon);
  };
  const button = (label, action) => {
    const element = document.createElement('button');
    element.type = 'button'; element.textContent = label;
    element.addEventListener('click', action);
    return element;
  };
  const panel = document.createElement('dialog');
  panel.className = 'privacy-preferences';
  panel.setAttribute('aria-labelledby', 'privacy-preferences-title');
  const title = document.createElement('h2');
  title.id = 'privacy-preferences-title';
  title.textContent = text('Privacy preferences', 'Preferencias de privacidad');
  const description = document.createElement('p');
  description.textContent = text('Allow optional Cloudflare Web Analytics to measure visits and page performance? It uses no analytics cookies or advertising profiles. Your language preference works either way.', '¿Permites Cloudflare Web Analytics para medir visitas y rendimiento de las páginas? No utiliza cookies de analítica ni perfiles publicitarios. Tu preferencia de idioma funciona con cualquier opción.');
  const status = document.createElement('p');
  status.className = 'note'; status.setAttribute('role', 'status');
  const details = document.createElement('a');
  details.href = (es ? '/es' : '') + '/cookies.html';
  details.textContent = text('Read about storage and external services', 'Consulta el almacenamiento y los servicios externos');
  const actions = document.createElement('div');
  actions.className = 'privacy-actions';
  const banner = document.createElement('aside');
  banner.className = 'privacy-banner';
  banner.setAttribute('aria-label', text('Optional analytics', 'Analítica opcional'));
  const update = () => {
    status.textContent = privacySignal ? text('Your browser’s privacy signal prevents analytics from loading.', 'La señal de privacidad de tu navegador impide cargar la analítica.') : text('Current choice: ', 'Elección actual: ') + (choice === 'accepted' ? text('allowed', 'permitida') : choice === 'rejected' ? text('declined', 'rechazada') : text('not selected', 'sin seleccionar'));
  };
  const save = value => {
    choice = value;
    try { localStorage.setItem(storageKey, JSON.stringify({choice: value, at: Date.now()})); } catch { /* Do not require storage to refuse tracking. */ }
    banner.remove(); update();
    panel.close();
    if (value === 'accepted') load();
    else if (loaded) location.reload(); // Ends the provider's existing page listeners.
  };
  const acceptLabel = text('Accept analytics', 'Aceptar analítica');
  const rejectLabel = text('Reject analytics', 'Rechazar analítica');
  const accept = button(acceptLabel, () => save('accepted'));
  accept.disabled = privacySignal;
  actions.append(accept, button(rejectLabel, () => save('rejected')), button(text('Close', 'Cerrar'), () => panel.close()));
  panel.append(title, description, status, details, actions);
  document.body.append(panel);
  const open = () => {update(); panel.showModal();};
  const manage = button(text('Privacy preferences', 'Preferencias de privacidad'), open);
  manage.className = 'privacy-manage';
  (document.querySelector('.legal-footer') || document.querySelector('footer') || document.body).append(manage);
  if (!choice && !privacySignal) {
    const message = document.createElement('p');
    message.textContent = text('May we measure visits and page performance with optional Cloudflare analytics?', '¿Podemos medir las visitas y el rendimiento con analítica opcional de Cloudflare?');
    const options = document.createElement('div'); options.className = 'privacy-actions';
    options.append(button(acceptLabel, () => save('accepted')), button(rejectLabel, () => save('rejected')), button(text('Preferences', 'Preferencias'), open));
    banner.append(message, options); document.body.append(banner);
  }
  if (choice === 'accepted') load();
})();
