(async () => {
  const {t, prefix} = window.SiteLanguage || {t: value => value, prefix: ''};
  const requested = new URLSearchParams(location.search).get('area');
  const title = document.getElementById('area-title');
  const team = document.getElementById('area-team');
  const outputs = document.getElementById('outputs-list');
  if (!title || !team || !outputs) return;
  const node = (tag, text = '', cls = '') => {
    const element = document.createElement(tag);
    element.textContent = text;
    if (cls) element.className = cls;
    return element;
  };
  const link = (url, text, cls = '') => {
    const element = node('a', text, cls);
    element.href = url;
    return element;
  };
  const note = (host, text) => host?.replaceChildren(node('p', t(text), 'note'));
  const photo = (record, cls) => {
    if (!record.image) return null;
    const img = node('img', '', cls);
    img.src = record.image;
    img.alt = record.image_alt || '';
    img.width = 160;
    img.height = 110;
    img.loading = 'lazy';
    return img;
  };
  const credit = record => {
    const caption = node('p', '', 'photo-credit');
    if (record.image_source_url) caption.append(link(record.image_source_url, record.image_credit || 'Wikimedia Commons'));
    else caption.textContent = record.image_credit || '';
    if (record.image_license_url) caption.append(' · ', link(record.image_license_url, t('License')));
    return caption;
  };
  try {
    const responses = await Promise.all(['research-areas', 'people', 'publications'].map(name => fetch(`${prefix}/${name}.json`)));
    if (!responses.every(response => response.ok)) throw new Error('Directory unavailable');
    const [areas, people, publications] = await Promise.all(responses.map(response => response.json()));
    const index = areas.findIndex(area => area.slug === requested);
    const area = areas[index];
    if (!area) {
      title.textContent = t('Research area unavailable');
      document.getElementById('area-summary').textContent = t('Choose a published research area from the Research page.');
      note(team, 'No published researchers are listed for this area.');
      note(outputs, 'No published papers are listed for this area.');
      note(document.getElementById('project-list'), 'No current projects are listed for this area.');
      return;
    }
    title.textContent = area.name;
    document.title = `${area.name} | ${languageName()}`;
    document.getElementById('area-crumb').textContent = area.name;
    document.getElementById('area-kicker').textContent = t('Research area');
    document.getElementById('area-summary').replaceChildren(
      ...[area.summary, area.overview].filter(Boolean).flatMap(text => text.split(/\n\s*\n/)).map(text => node('p', text))
    );
    const hero = document.getElementById('area-image');
    if (hero && area.image) {
      hero.closest('.research-art').dataset.area = area.slug;
      hero.src = area.image;
      hero.alt = area.image_alt || '';
      hero.hidden = false;
      const caption = document.getElementById('area-image-credit');
      caption.replaceChildren(credit(area));
      caption.hidden = false;
    }
    const host = document.getElementById('project-list');
    if (!area.projects.length) note(host, 'No current projects are listed for this area.');
    else host.replaceChildren(...area.projects.map(project => {
      const article = node('article', '', 'publication project-card');
      const img = photo(project, 'project-photo');
      if (img) {
        if (project.url) {const anchor = link(project.url, ''); anchor.append(img); article.append(anchor);}
        else article.append(img);
      }
      const heading = node('h3', '', 'pub-title');
      heading.append(project.url ? link(project.url, project.title) : project.title);
      article.append(heading, ...project.summary.split(/\n\s*\n/).map(text => node('p', text)));
      if (project.researcher_note) article.append(node('p', project.researcher_note, 'pub-authors'));
      if (img) article.append(credit(project));
      return article;
    }));
    const members = people.filter(person => person.research_areas.includes(area.slug));
    if (!members.length) note(team, 'No published researcher profiles are linked to this area yet.');
    else team.replaceChildren(...members.map(person => {
      const anchor = link(`${prefix}/people.html#${encodeURIComponent(person.slug)}`, '', 'area-person');
      if (person.portrait) {
        const img = node('img'); img.src = person.portrait; img.alt = ''; img.width = 96; img.height = 120; img.loading = 'lazy'; anchor.append(img);
      }
      const text = node('span'); text.append(node('strong', person.name), node('small', t('View profile →'))); anchor.append(text); return anchor;
    }));
    const related = publications.filter(pub => pub.topics.includes(area.slug));
    if (!related.length) note(outputs, 'No verified publications are linked to this area yet.');
    else outputs.replaceChildren(...related.map(pub => {
      const article = node('article', '', 'publication paper-row');
      const href = pub.canonical_url || pub.pdf || pub.pdf_url || `${prefix}/publications/${encodeURIComponent(pub.slug)}/`;
      const img = photo(pub, 'paper-photo');
      if (img) {const anchor = link(href, '', 'paper-image');anchor.setAttribute('aria-label', pub.title);anchor.append(img);article.append(anchor);article.classList.add('has-image');}
      const text = node('div'); const heading = node('h3', '', 'pub-title');heading.append(link(href, pub.title));
      const authors = node('p', '', 'pub-authors');
      pub.authors.forEach((author, index) => {
        if (index) authors.append(', ');
        if (typeof author === 'object' && author.person_id) authors.append(link(`${prefix}/people.html#${encodeURIComponent(author.person_id)}`, author.name));
        else authors.append(typeof author === 'string' ? author : author.name);
      });
      const venue = pub.venue || t(pub.type);
      text.append(heading, authors, node('p', `${venue} · ${pub.year}`, 'pub-venue'));
      if (img) text.append(credit(pub));
      article.append(text, link(`${prefix}/publications/${encodeURIComponent(pub.slug)}/`, t('Abstract and details →'), 'text-link'));
      return article;
    }));
  } catch {
    title.textContent = t('Research area');
    note(team, 'The research directory is temporarily unavailable. Browse all research areas or try again later.');
    note(outputs, 'The publication directory is temporarily unavailable.');
  }
  function languageName() {return prefix ? 'Centro de Investigación Económica UP' : 'UP Economics Research Center';}
})();
