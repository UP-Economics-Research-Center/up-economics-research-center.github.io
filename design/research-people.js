function formatAreaByline(authors) {
  const source = Array.isArray(authors) ? authors : [];
  const linkedPeople = [];
  const collaborators = [];
  for (const author of source) {
    const name = typeof author === 'string' ? author : (author && author.name) || '';
    if (!name) continue;
    if (author && typeof author === 'object' && author.person_id) linkedPeople.push(name);
    else collaborators.push(name);
  }
  if (!linkedPeople.length) return source.map(author => typeof author === 'string' ? author : author.name).join(', ');
  return linkedPeople.join(', ') + (collaborators.length ? ` with ${collaborators.join(', ')}` : '');
}

(async () => {
  const params = new URLSearchParams(location.search);
  const requested = params.get('area') || '';
  const title = document.getElementById('area-title');
  const kicker = document.getElementById('area-kicker');
  const artwork = document.getElementById('area-illustration');
  const crumb = document.getElementById('area-crumb');
  const question = document.getElementById('area-question');
  const summary = document.getElementById('area-summary');
  const description = document.getElementById('area-description');
  const projectsHost = document.getElementById('project-list');
  const team = document.getElementById('area-team');
  const outputs = document.getElementById('outputs-list');
  if (!title || !team || !outputs) return;

  const setNote = (host, message) => {
    const note = document.createElement('p');
    note.className = 'note';
    note.textContent = message;
    host.replaceChildren(note);
  };
  const makeLink = (href, label, className = '') => {
    const link = document.createElement('a');
    link.href = href;
    link.className = className;
    link.textContent = label;
    return link;
  };

  try {
    const [areaResponse, peopleResponse, publicationResponse] = await Promise.all([
      fetch('/research-areas.json'), fetch('/people.json'), fetch('/publications.json'),
    ]);
    if (![areaResponse, peopleResponse, publicationResponse].every(response => response.ok)) {
      throw new Error('The research directory could not be loaded.');
    }
    const [areas, people, publications] = await Promise.all([
      areaResponse.json(), peopleResponse.json(), publicationResponse.json(),
    ]);
    const index = areas.findIndex(area => area.slug === requested);
    const area = areas[index];
    if (!area) {
      title.textContent = 'Research area unavailable';
      if (description) description.textContent = 'Choose a published research area from the Research page.';
      setNote(team, 'No published researchers are listed for this area.');
      setNote(outputs, 'No published papers are listed for this area.');
      return;
    }

    title.textContent = area.name;
    if (artwork && area.illustration) artwork.src = area.illustration;
    else if (artwork && artwork.parentElement) artwork.parentElement.hidden = true;
    if (crumb) crumb.textContent = area.name;
    if (question) question.textContent = `${area.name}: research focus`;
    const areaNumber = String(index + 1).padStart(2, '0');
    if (kicker) kicker.textContent = `Research area ${areaNumber}`;
    if (summary) summary.textContent = area.summary;
    if (description) description.textContent = area.overview || area.summary;

    const projects = area.projects || [];
    if (projectsHost) {
      if (!projects.length) setNote(projectsHost, 'No current projects are listed for this area.');
      else projectsHost.replaceChildren(...projects.map(project => {
        const article = document.createElement('article');
        article.className = 'publication project-card';
        const text = document.createElement('div');
        const heading = document.createElement('h3');
        heading.className = 'pub-title';
        heading.textContent = project.title;
        const detail = document.createElement('p');
        detail.textContent = project.summary;
        text.append(heading, detail);
        if (project.researchers && project.researchers.length) {
          const names = document.createElement('p');
          names.className = 'pub-authors';
          names.textContent = project.researchers.join(', ');
          text.append(names);
        }
        article.append(text);
        return article;
      }));
    }

    const members = people.filter(person => (person.research_areas || []).includes(area.slug));
    if (!members.length) {
      setNote(team, 'No published researcher profiles are linked to this area yet.');
    } else {
      team.replaceChildren(...members.map(person => {
        const link = document.createElement('a');
        link.href = `people.html#${encodeURIComponent(person.slug)}`;
        link.className = 'area-person';
        if (person.portrait) {
          const img = document.createElement('img');
          img.src = person.portrait;
          img.alt = '';
          img.width = 64;
          img.height = 80;
          img.loading = 'lazy';
          link.append(img);
        }
        const text = document.createElement('span');
        const name = document.createElement('strong');
        const detail = document.createElement('small');
        name.textContent = person.name;
        detail.textContent = 'View profile →';
        text.append(name, detail);
        link.append(text);
        return link;
      }));
    }

    const related = publications
      .filter(publication => (publication.topics || []).includes(area.slug))
      .sort((a, b) => Number(b.year) - Number(a.year) || a.title.localeCompare(b.title));
    if (!related.length) {
      setNote(outputs, 'No verified publications are linked to this area yet.');
    } else {
      outputs.replaceChildren(...related.map(publication => {
        const article = document.createElement('article');
        article.className = 'publication';
        const year = document.createElement('div');
        year.className = 'pub-year';
        year.textContent = String(publication.year);
        const text = document.createElement('div');
        const heading = document.createElement('h3');
        heading.className = 'pub-title';
        heading.append(makeLink(`/publications/${encodeURIComponent(publication.slug)}/`, publication.title));
        const authors = document.createElement('p');
        authors.className = 'pub-authors';
        authors.textContent = formatAreaByline(publication.authors);
        text.append(heading, authors);
        article.append(year, text);
        return article;
      }));
    }
  } catch {
    title.textContent = 'Research area';
    setNote(team, 'The research directory is temporarily unavailable. Browse all research areas or try again later.');
    setNote(outputs, 'The publication directory is temporarily unavailable.');
  }
})();
