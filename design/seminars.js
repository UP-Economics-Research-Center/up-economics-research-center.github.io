/* Complete static HTML, live Mexico City grouping and a local seminar archive. */
(() => {
  const upcoming = document.getElementById('seminar-upcoming-list');
  const archive = document.getElementById('seminar-archive-list');
  if (!upcoming || !archive) return;
  const records = [...document.querySelectorAll('.seminar-record[data-event-date]')];
  const language = document.documentElement.lang === 'es' ? 'es' : 'en';
  const clock = new Intl.DateTimeFormat('en-US', {
    timeZone: 'America/Mexico_City', year: 'numeric', month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit', second: '2-digit', hourCycle: 'h23',
  });
  const dateLabel = new Intl.DateTimeFormat(language === 'es' ? 'es-MX' : 'en-US', {
    timeZone: 'UTC', year: 'numeric', month: 'long', day: 'numeric',
  });

  function createArchiveBrowser() {
    const form = document.getElementById('seminar-archive-form');
    const query = document.getElementById('seminar-archive-query');
    const year = document.getElementById('seminar-archive-year');
    const count = document.getElementById('seminar-archive-count');
    const noResults = document.getElementById('seminar-archive-no-results');
    const pages = document.getElementById('seminar-archive-pages');
    const previous = document.getElementById('seminar-archive-previous');
    const next = document.getElementById('seminar-archive-next');
    const pageLabel = document.getElementById('seminar-archive-page');
    if (!form || !query || !year || !count || !noResults || !pages || !previous || !next || !pageLabel) return () => {};
    const pageSize = 6;
    const normalize = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
    const searchable = new Map(records.map(row => [row, normalize((row.dataset.search || '') + ' ' + row.textContent)]));
    let past = [];
    let page = 1;
    function readLocation() {
      const params = new URL(location.href).searchParams;
      query.value = (params.get('archive_q') || '').slice(0, 200);
      page = Math.max(1, parseInt(params.get('archive_page'), 10) || 1);
      return params.get('archive_year') || '';
    }
    let selectedYear = readLocation();
    function saveLocation(clearAnchor = false) {
      const url = new URL(location.href);
      for (const [key, value] of [['archive_q', query.value.trim()], ['archive_year', year.value], ['archive_page', page > 1 ? String(page) : '']]) {
        if (value) url.searchParams.set(key, value); else url.searchParams.delete(key);
      }
      if (clearAnchor) {
        let target;
        try { target = document.getElementById(decodeURIComponent(url.hash.slice(1))); } catch { /* Keep unrelated malformed hashes harmless. */ }
        if (target?.closest('.seminar-record')) url.hash = 'archive';
      }
      if (url.href !== location.href) history.replaceState(history.state, '', url.href);
    }
    function matches() {
      const terms = normalize(query.value.trim()).split(/\s+/).filter(Boolean);
      return past.filter(row => (!year.value || row.dataset.eventDate.startsWith(year.value)) && terms.every(term => searchable.get(row).includes(term)));
    }
    function apply(clearAnchor = false) {
      const found = matches();
      const pageCount = Math.max(1, Math.ceil(found.length / pageSize));
      page = Math.min(page, pageCount);
      const visible = new Set(found.slice((page - 1) * pageSize, page * pageSize));
      past.forEach(row => { row.hidden = !visible.has(row); });
      noResults.hidden = past.length === 0 || found.length > 0;
      pages.hidden = pageCount <= 1;
      previous.disabled = page <= 1;
      next.disabled = page >= pageCount;
      pageLabel.textContent = language === 'es' ? `Página ${page} de ${pageCount}` : `Page ${page} of ${pageCount}`;
      count.textContent = language === 'es'
        ? `${found.length} seminario${found.length === 1 ? '' : 's'} encontrado${found.length === 1 ? '' : 's'}`
        : `${found.length} seminar${found.length === 1 ? '' : 's'} found`;
      saveLocation(clearAnchor);
    }
    function revealHash() {
      let id;
      try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
      const target = id && document.getElementById(id);
      const row = target && target.closest('.seminar-record');
      if (!row || !past.includes(row) || !row.hidden) return;
      if (!matches().includes(row)) { query.value = ''; year.value = ''; selectedYear = ''; }
      page = Math.floor(matches().indexOf(row) / pageSize) + 1;
      apply();
      target.scrollIntoView({ block: 'start' });
    }
    function filter() { selectedYear = year.value; page = 1; apply(true); }
    form.addEventListener('submit', event => { event.preventDefault(); filter(); });
    form.addEventListener('reset', event => { event.preventDefault(); query.value = ''; year.value = ''; filter(); });
    query.addEventListener('input', filter);
    year.addEventListener('change', filter);
    function navigate(change) {
      page += change;
      apply(true);
      document.getElementById('seminar-archive-heading')?.focus();
    }
    previous.addEventListener('click', () => navigate(-1));
    next.addEventListener('click', () => navigate(1));
    window.addEventListener('hashchange', revealHash);
    window.addEventListener('popstate', () => { selectedYear = readLocation(); year.value = selectedYear; apply(); revealHash(); });
    document.querySelector('[data-seminar-archive-tools]').hidden = false;
    return items => {
      past = items;
      const keepYear = year.value || selectedYear;
      const years = [...new Set(past.map(row => row.dataset.eventDate.slice(0, 4)))].sort().reverse();
      while (year.options.length > 1) year.remove(1);
      years.forEach(value => { const option = document.createElement('option'); option.value = value; option.textContent = value; year.append(option); });
      year.value = years.includes(keepYear) ? keepYear : '';
      selectedYear = year.value;
      apply();
      revealHash();
    };
  }

  const updateArchive = createArchiveBrowser();
  let groupedDay;
  let timer;
  function refresh() {
    clearTimeout(timer);
    const now = new Date();
    const parts = Object.fromEntries(clock.formatToParts(now).map(part => [part.type, part.value]));
    const today = `${parts.year}-${parts.month}-${parts.day}`;
    if (today !== groupedDay) {
      const byDate = (a, b) => a.dataset.eventDate.localeCompare(b.dataset.eventDate) || a.id.localeCompare(b.id);
      const next = records.filter(row => row.dataset.eventDate >= today).sort(byDate);
      const past = records.filter(row => row.dataset.eventDate < today).sort((a, b) => byDate(b, a));
      records.forEach(row => { row.hidden = false; });
      for (const [list, items] of [[upcoming, next], [archive, past]]) {
        const empty = list.querySelector('[data-seminar-empty]');
        items.forEach(item => list.insertBefore(item, empty));
        empty.hidden = items.length > 0;
      }
      for (const label of document.querySelectorAll('[data-seminar-day]')) {
        label.textContent = dateLabel.format(new Date(label.dateTime + 'T12:00:00Z'));
      }
      groupedDay = today;
      updateArchive(past);
    }
    const remaining = (86400 - (+parts.hour * 3600 + +parts.minute * 60 + +parts.second)) * 1000 - now.getMilliseconds();
    timer = setTimeout(refresh, Math.min(60000, remaining + 50));
  }
  refresh();
  document.addEventListener('visibilitychange', () => { if (!document.hidden) refresh(); });
  window.addEventListener('pageshow', refresh);
  window.addEventListener('focus', refresh);
})();
