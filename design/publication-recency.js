(() => {
  const day = value => {
    if (!/^\d{4}-\d{2}-\d{2}$/.test(value || '')) return NaN;
    const ms = Date.parse(`${value}T00:00:00Z`);
    return Number.isFinite(ms) && new Date(ms).toISOString().slice(0, 10) === value ? ms : NaN;
  };
  const refresh = (root = document) => {
    const now = new Date();
    const today = Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate());
    root.querySelectorAll('[data-publication-date]').forEach(badge => {
      let source = false;
      try { const url = new URL(badge.dataset.publicationDateSource); source = url.protocol === 'https:' && !url.username && !url.password; } catch {}
      const age = (today - day(badge.dataset.publicationDate)) / 86400000;
      badge.hidden = !(source && age >= 0 && age < 90);
      badge.textContent = document.documentElement.lang === 'es' ? 'Nueva' : 'New';
    });
  };
  window.PublicationRecency = {refresh};
  refresh();
  // Expire badges in open tabs too, without requiring a new static build.
  setInterval(() => refresh(), 60000);
  document.addEventListener('visibilitychange', () => { if (!document.hidden) refresh(); });
})();
