(async () => {
  const note = document.getElementById('setup-note');
  try {
    const response = await fetch('./config.yml', { cache: 'no-store' });
    const config = response.ok ? await response.text() : '';
    if (!config || config.includes('REPLACE_WITH_CLOUDFLARE_WORKER')) note.hidden = false;
  } catch {
    note.hidden = false;
  }
})();
