(() => {
  const preference = matchMedia('(prefers-reduced-motion: reduce)');
  if (!('IntersectionObserver' in window) || preference.matches) return;
  const selector = '.research-index, .home-section .section-intro, .output-layout, .people-list .person, .publication-list > .publication, .media-list > .publication, .source-area-page .split-label, .source-area-page .project-card, .seminar-overview, .seminar-agenda > section, .seminar-proposals';
  const active = new Set();
  const reveal = element => { element.classList.remove('motion-pending'); active.delete(element); };
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) { reveal(entry.target); observer.unobserve(entry.target); }
    });
  }, {threshold: 0.04, rootMargin: '0px 0px 36px 0px'});
  const register = root => {
    if (preference.matches) return;
    root.querySelectorAll(selector).forEach(element => {
    if (element.dataset.motionReady) return;
    element.dataset.motionReady = 'true';
    // Never hide content: movement is a short positional transition only.
    if (element.getBoundingClientRect().top > innerHeight) {
      element.classList.add('motion-pending'); active.add(element); observer.observe(element);
    }
    });
  };
  register(document);
  const dynamic = document.getElementById('main-content');
  if (dynamic) new MutationObserver(() => register(dynamic)).observe(dynamic, {childList: true, subtree: true});
  document.addEventListener('focusin', event => {
    const host = event.target.closest('[data-motion-ready]'); if (host) reveal(host);
  });
  preference.addEventListener('change', () => { if (preference.matches) { active.forEach(reveal); observer.disconnect(); } });
})();
