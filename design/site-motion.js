(() => {
  const preference = matchMedia('(prefers-reduced-motion: reduce)');
  if (!('IntersectionObserver' in window) || !Element.prototype.animate) return;

  const selector = '.research-index > .research-row, .home-section .section-intro, .output-layout > div:first-child, .output-link, .people-list .person, .publication-list > .publication, .media-list > .publication, .source-area-page .split-label, .source-area-page .project-card, .source-area-page .reference-paper, .seminar-overview, .seminar-agenda > section, .seminar-proposals';
  const pending = new Set();
  const animations = new Map();
  const settle = element => {
    pending.delete(element);
    observer.unobserve(element);
    animations.get(element)?.cancel();
    animations.delete(element);
    element.dataset.motionReady = 'done';
  };
  const reveal = element => {
    pending.delete(element);
    observer.unobserve(element);
    element.dataset.motionReady = 'done';
    // Base content is always visible. Animate only after it enters the viewport;
    // no hidden styles, layout changes or persistent transforms are required.
    if (preference.matches || element.contains(document.activeElement)) return;
    const siblings = [...element.parentElement.children].filter(sibling => sibling.matches(selector));
    const delay = (Math.max(0, siblings.indexOf(element)) % 3) * 45;
    const animation = element.animate([
      {transform: 'translateY(12px)', opacity: 0.86},
      {transform: 'translateY(0)', opacity: 1},
    ], {duration: 440, delay, easing: 'cubic-bezier(.22,.68,.2,1)', fill: 'backwards'});
    animations.set(element, animation);
    animation.onfinish = () => animations.delete(element);
  };
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => { if (entry.isIntersecting) reveal(entry.target); });
  }, {threshold: 0, rootMargin: '0px 0px -24px 0px'});
  const register = root => {
    if (preference.matches) return;
    root.querySelectorAll(selector).forEach(element => {
      if (element.dataset.motionReady) return;
      // Preserve direct anchor landings without animating the linked section.
      const anchor = location.hash && document.getElementById(location.hash.slice(1));
      if (anchor && (element === anchor || element.contains(anchor) || anchor.contains(element))) {
        element.dataset.motionReady = 'done';
        return;
      }
      element.dataset.motionReady = 'pending';
      pending.add(element);
      observer.observe(element);
    });
  };
  register(document);
  const main = document.getElementById('main-content');
  if (main) new MutationObserver(() => register(main)).observe(main, {childList: true, subtree: true});
  document.addEventListener('focusin', event => {
    // Focusing a child immediately settles its moving ancestors too.
    for (let element = event.target; element; element = element.parentElement) {
      if (element.dataset.motionReady) settle(element);
    }
  });
  preference.addEventListener('change', () => {
    if (preference.matches) {
      [...pending, ...animations.keys()].forEach(settle);
      observer.disconnect();
    } else register(document);
  });
})();
