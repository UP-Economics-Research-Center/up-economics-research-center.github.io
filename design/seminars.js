/* Static HTML is complete. Keep its calendar grouping current in Mexico City. */
(() => {
  const upcoming = document.getElementById('seminar-upcoming-list');
  const archive = document.getElementById('seminar-archive-list');
  if (!upcoming || !archive) return;
  const records = [...document.querySelectorAll('.seminar-record[data-event-date]')];
  const clock = new Intl.DateTimeFormat('en-US', {
    timeZone: 'America/Mexico_City', year: 'numeric', month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit', second: '2-digit', hourCycle: 'h23',
  });
  const locale = document.documentElement.lang === 'es' ? 'es-MX' : 'en-US';
  const dateLabel = new Intl.DateTimeFormat(locale, {
    timeZone: 'UTC', year: 'numeric', month: 'long', day: 'numeric',
  });
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
      for (const [list, items] of [[upcoming, next], [archive, past]]) {
        const empty = list.querySelector('[data-seminar-empty]');
        items.forEach(item => list.insertBefore(item, empty));
        empty.hidden = items.length > 0;
      }
      for (const label of document.querySelectorAll('[data-seminar-day]')) {
        label.textContent = dateLabel.format(new Date(label.dateTime + 'T12:00:00Z'));
      }
      groupedDay = today;
    }
    // Wake just after midnight; recheck at least once a minute for clock changes.
    const remaining = (86400 - (+parts.hour * 3600 + +parts.minute * 60 + +parts.second)) * 1000 - now.getMilliseconds();
    timer = setTimeout(refresh, Math.min(60000, remaining + 50));
  }
  refresh();
  document.addEventListener('visibilitychange', () => { if (!document.hidden) refresh(); });
  window.addEventListener('pageshow', refresh);
  window.addEventListener('focus', refresh);
})();
