(() => {
  const {t = value => value} = window.SiteLanguage || {};
  const original = document.querySelector('.people-jump, .seminar-tabs');
  if (!original) return;
  const links = Array.from(original.querySelectorAll('a[href^="#"]'));
  const sections = links.map(link => document.getElementById(link.hash.slice(1))).filter(Boolean);
  if (!links.length || !sections.length) return;
  const nav = document.createElement('nav'); nav.className = 'section-navigation';
  nav.setAttribute('aria-label', t('In this section'));
  const caption = document.createElement('span'); caption.className = 'section-navigation-label'; caption.textContent = t('In this section');
  const track = document.createElement('div'); track.className = 'section-navigation-track';
  links.forEach(link => {link.textContent = link.textContent.replace(/\s*↓\s*$/, ''); track.append(link);});
  const label = document.createElement('label'); label.className = 'section-navigation-mobile'; label.textContent = t('Jump to section');
  const select = document.createElement('select');
  links.forEach(link => {const option = document.createElement('option'); option.value = link.hash; option.textContent = link.textContent; select.append(option);});
  label.append(select); nav.append(caption,track,label); original.replaceWith(nav);
  const headerHeight = () => {
    const header = document.querySelector('header');
    return header && ['sticky','fixed'].includes(getComputedStyle(header).position) ? header.getBoundingClientRect().height : 0;
  };
  const positionBar = () => nav.style.setProperty('--section-nav-top', `${headerHeight()}px`);
  positionBar(); addEventListener('resize', positionBar);

  const activate = id => {
    links.forEach(link => {if (link.hash === '#' + id) link.setAttribute('aria-current','location'); else link.removeAttribute('aria-current');});
    select.value = '#' + id;
  };
  const first = sections.find(section => '#' + section.id === location.hash) || sections[0]; activate(first.id);
  const moveTo = hash => {
    const section = document.getElementById(hash.slice(1)); if (!section) return;
    activate(section.id); history.replaceState(null,'',hash);
    const rootPadding = parseFloat(getComputedStyle(document.documentElement).scrollPaddingTop) || 0;
    section.style.scrollMarginTop = `${Math.max(0, headerHeight() + nav.offsetHeight + 24 - rootPadding)}px`;
    section.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth',block:'start'});
    const heading = section.querySelector('h2,h3') || section; heading.setAttribute('tabindex','-1'); heading.focus({preventScroll:true});
  };
  track.addEventListener('click', event => {const link=event.target.closest('a');if(link){event.preventDefault();moveTo(link.hash);}});
  select.addEventListener('change', () => moveTo(select.value));
  let queued = false;
  const sync = () => {
    queued = false;
    const threshold = headerHeight() + nav.offsetHeight + 48;
    const atBottom = scrollY + innerHeight >= document.documentElement.scrollHeight - 3;
    const current = atBottom ? sections.at(-1) : sections.filter(section => section.getBoundingClientRect().top <= threshold).at(-1);
    if (current) activate(current.id);
  };
  document.addEventListener('scroll',()=>{if(!queued){queued=true;requestAnimationFrame(sync);}},{passive:true});
})();
