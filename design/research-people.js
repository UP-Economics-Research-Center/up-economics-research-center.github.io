/* Compatibility for inbound links predating the static research routes. */
(async () => {
  const {t, prefix} = window.SiteLanguage || {t: value => value, prefix: ''};
  const title = document.getElementById('area-title');
  const summary = document.getElementById('area-summary');
  if (!title || !summary) return;
  const requested = new URLSearchParams(location.search).get('area');
  try {
    const version = window.UP_DIRECTORY_VERSION;
    const response = await fetch(`${prefix}/research-areas.json${version ? '?v=' + encodeURIComponent(version) : ''}`);
    if (!response.ok) throw new Error('Directory unavailable');
    const areas = await response.json();
    const area = areas.find(record => record.slug === requested);
    if (area) {
      const target = new URL(`${prefix}/research/${area.slug}/`, location.origin);
      target.search = location.search;
      target.searchParams.delete('area');
      target.hash = location.hash;
      location.replace(target.href);
      return;
    }
    title.textContent = t('Research');
    const list = document.createElement('ul');
    areas.forEach(record => {
      const item = document.createElement('li');
      const link = document.createElement('a');
      link.href = `${prefix}/research/${record.slug}/`;
      link.textContent = record.name;
      item.append(link); list.append(item);
    });
    summary.append(list);
  } catch {
    title.textContent = t('Research area');
    summary.textContent = t('The research directory is temporarily unavailable. Browse all research areas or try again later.');
  }
})();
