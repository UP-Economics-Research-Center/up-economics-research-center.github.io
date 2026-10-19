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
    if (record.image_width && record.image_height) {
      img.width = record.image_width;
      img.height = record.image_height;
    }
    if (record.image.includes('/area-photography/') && record.image_width) {
      const variants = [480,960].filter(width => width < record.image_width).map(width => `${record.image.replace('.webp', `-${width}.webp`)} ${width}w`);
      variants.push(`${record.image} ${record.image_width}w`);
      img.srcset = variants.join(', ');
      img.sizes = '(max-width:700px) calc(100vw - 40px), (max-width:1000px) 46vw, 640px';
    }
    img.loading = 'lazy';
    if (record.image_fit === 'contain') img.dataset.imageFit = 'contain';
    return img;
  };
  const credit = () => {
    const caption = node('p', '', 'photo-credit');
    caption.append(link(`${prefix}/photo-credits.html`, t('Image credit')));
    return caption;
  };
  const researcherNote = text => {
    const paragraph = node('p', '', 'pub-authors');
    // Preserve the source names verbatim; only the explicit UP attribution is emphasized.
    const match = text.match(/^((?:UP Researchers?:|Investigador(?:es)? UP:)\s*)([\s\S]*?)(?=\n[ \t]*(?:with|con)\b|$)/i);
    if (match) {
      const names = match[2].split(/\n/).map(name => name.trim()).filter(Boolean);
      const conjunction = document.documentElement.lang === 'es' ? ' y ' : ' and ';
      const group = names.length > 1 ? names.slice(0, -1).join(', ') + conjunction + names.at(-1) : names[0] || '';
      paragraph.append(match[1], node('strong', group), text.slice(match[0].length));
    } else paragraph.textContent = text;
    return paragraph;
  };
  try {
    const version = window.UP_DIRECTORY_VERSION;
    const directoryQuery = version ? `?v=${encodeURIComponent(version)}` : '';
    const responses = await Promise.all(['research-areas', 'people', 'publications'].map(name => fetch(`${prefix}/${name}.json${directoryQuery}`)));
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
    const referenceLayout = area.layout === 'original-reference';
    let banner = null;
    if (referenceLayout) {
      document.body.classList.add('source-area-page');
      banner = photo(area.image ? area : (area.banner || {}), 'source-area-banner');
      if (banner) {
        banner.loading = 'eager';
        banner.dataset.area = area.slug;
      }
      const teamHeading = document.getElementById('team');
      teamHeading.querySelector('h2').textContent = t('Team');
      document.getElementById('projects').querySelector('h2').textContent = t('Current Projects');
      document.getElementById('outputs').querySelector('h2').textContent = t('Journal Publications');
      team.parentElement.prepend(teamHeading, team);
    }
    document.getElementById('area-summary').replaceChildren(
      ...[area.summary, area.overview].filter(Boolean).flatMap(text => text.split(/\n\s*\n/)).map(text => node('p', text))
    );
    if (banner) {
      const frame = node('figure', '', 'area-presentation-image motion-frame');
      frame.dataset.area = area.slug;
      frame.append(banner);
      document.querySelector('.area-intro').prepend(frame);
    }
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
      const copy = node('div', '', 'project-copy');
      const heading = node('h3', '', 'pub-title');
      heading.append(project.url ? link(project.url, project.title) : project.title);
      copy.append(heading, ...project.summary.split(/\n\s*\n/).map(text => node('p', text)));
      if (project.researcher_note) copy.append(...project.researcher_note.split(/\n\s*\n/).map(text => researcherNote(text)));
      article.append(copy);
      const img = photo(project, 'project-photo');
      if (img) {
        article.classList.add('has-image');
        const media = node('figure', '', 'project-media');
        if (project.url) {
          const anchor = link(project.url, '');
          anchor.setAttribute('aria-label', project.title);
          anchor.append(img);
          media.append(anchor);
        } else media.append(img);
        const caption = node('figcaption');
        caption.append(credit(project));
        media.append(caption);
        article.append(media);
      }
      return article;
    }));
    const members = referenceLayout && area.reference_team?.length ? (area.reference_team || []).map(item => {
      const person = people.find(person => person.slug === item.person_id);
      return person || null; // People is the single source for the portrait and its crop.
    }).filter(Boolean) : people.filter(person => person.research_areas.includes(area.slug));
    if (!members.length) note(team, 'No published researcher profiles are linked to this area yet.');
    else team.replaceChildren(...members.map(person => {
      const anchor = link(`${prefix}/people.html#${encodeURIComponent(person.slug)}`, '', 'area-person');
      if (person.portrait) {
        const frame = node('div', '', 'area-portrait' + (person.reference_portrait ? ' reference-portrait' : ''));
        const img = node('img'); img.src = person.portrait; img.alt = ''; img.width = 240; img.height = 300; img.loading = 'lazy';
        if (person.portrait_crop) {
          const crop = person.portrait_crop;
          frame.classList.add('portrait-frame');
          frame.style.setProperty('--crop-width', `${10000 / crop.width}%`);
          frame.style.setProperty('--crop-height', `${10000 / crop.height}%`);
          frame.style.setProperty('--crop-left', `${-100 * crop.left / crop.width}%`);
          frame.style.setProperty('--crop-top', `${-100 * crop.top / crop.height}%`);
        }
        frame.append(img);
        anchor.append(frame);
      }
      const text = node('span'); text.append(node('strong', person.display_name || person.name), node('small', t('View profile →'))); anchor.append(text); return anchor;
    }));
    const related = publications.filter(pub => pub.topics.includes(area.slug)).sort((a, b) => b.year - a.year || a.title.localeCompare(b.title));
    if (related.some(pub => pub.type !== 'Journal article')) document.querySelector('#outputs h2').textContent = t('Publications');
    if (!related.length) note(outputs, 'No verified publications are linked to this area yet.');
    else outputs.replaceChildren(...related.map(pub => {
      const feature = referenceLayout ? (area.publication_features || []).find(item => item.publication === pub.slug) : null;
      const description = referenceLayout ? (feature?.description || pub.abstract) : '';
      const article = node('article', '', 'publication paper-row');
      const href = `${prefix}/publications/${encodeURIComponent(pub.slug)}/`;
      const img = photo(pub, 'paper-photo'); // One verified document thumbnail, shared with Publications.
      const titleLanguage = pub.title_language === 'es' ? 'es' : 'en';
      if (img) {const anchor = link(href, '', 'paper-image');anchor.lang = titleLanguage;anchor.translate = false;anchor.setAttribute('aria-label', pub.title);img.alt = '';anchor.append(img);article.append(anchor);article.classList.add('has-image');}
      const text = node('div'); const heading = node('h3', '', 'pub-title');
      const titleLink = link(href, pub.title);titleLink.lang = titleLanguage;titleLink.translate = false;heading.append(titleLink);
      const authors = node('p', '', 'pub-authors');
      const up = pub.authors.filter(author => typeof author === 'object' && author.person_id);
      const others = pub.authors.filter(author => !(typeof author === 'object' && author.person_id));
      const appendNames = group => group.forEach((author, index) => {
        if (index) authors.append(', ');
        if (typeof author === 'object' && author.person_id) authors.append(link(`${prefix}/people.html#${encodeURIComponent(author.person_id)}`, author.name));
        else authors.append(typeof author === 'string' ? author : author.name);
      });
      if (up.length) {
        authors.append(t(up.length === 1 ? 'UP researcher:' : 'UP researchers:') + ' ');
        appendNames(up);
        if (others.length) authors.append(node('br'), t('with') + ' ');
      }
      appendNames(others);
      const venue = pub.venue || t(pub.type);
      text.append(heading);
      if (pub.publication_date && pub.publication_date_source_url) {
        const badge = node('span', t('New'), 'publication-new');
        badge.dataset.publicationDate = pub.publication_date;
        badge.dataset.publicationDateSource = pub.publication_date_source_url;
        badge.hidden = true;
        text.prepend(badge);
      }
      if (description) {
        article.classList.add('reference-paper');
        text.append(...description.split(/\n\s*\n/).map(paragraph => node('p', paragraph, 'reference-description')));
      }
      text.append(authors, node('p', `${venue} · ${pub.year}`, 'pub-venue'));
      if (feature?.media_links?.length) {
        const media = node('div', '', 'reference-media-links');
        feature.media_links.forEach(item => media.append(link(item.url, item.label)));
        text.append(media);
      }
      if (img) text.append(credit(feature || pub));
      article.append(text, link(`${prefix}/publications/${encodeURIComponent(pub.slug)}/`, t('Abstract and details →'), 'text-link'));
      return article;
    }));
    window.PublicationRecency?.refresh(outputs);
  } catch {
    title.textContent = t('Research area');
    note(team, 'The research directory is temporarily unavailable. Browse all research areas or try again later.');
    note(outputs, 'The publication directory is temporarily unavailable.');
  }
  function languageName() {return 'UP Economics Research Center';}
})();
