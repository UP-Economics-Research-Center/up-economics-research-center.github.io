(function () {
  if (!window.CMS || !window.createClass || !window.h) return;
  CMS.registerPreviewStyle('/design/site-concept.css');

  function field(entry, name) {
    var value = entry.getIn(['data', name]);
    if (value && typeof value.toJS === 'function') value = value.toJS();
    return value == null ? '' : value;
  }
  function Preview(props, kind) {
    var entry = props.entry;
    var title = field(entry, 'title') || field(entry, 'display_name') || field(entry, 'name') || field(entry, 'center_name') || 'Content preview';
    var blocks = [];
    function line(label, value) {
      if (Array.isArray(value)) value = value.map(function (item) { return typeof item === 'string' ? item : (item.name || ''); }).filter(Boolean).join(', ');
      if (value) blocks.push(h('p', { key: label, style: { whiteSpace: 'pre-line' } }, h('strong', {}, label + ': '), String(value)));
    }
    function bilingual(label, name) {
      line(label + ' — English', field(entry, name));
      line(label + ' — Español', field(entry, name + '_es'));
      if (field(entry, name) && !field(entry, name + '_es')) line('Missing Spanish: ' + label, 'Complete the Spanish field before requesting approval.');
    }
    function image(label, source, alt) {
      if (!source) return;
      var asset = props.getAsset ? String(props.getAsset(source)) : source;
      blocks.push(h('figure', { key: label, style: { margin: '1rem 0' } },
        h('img', { src: asset, alt: alt || label, style: { display: 'block', maxWidth: '200px', maxHeight: '260px', width: 'auto', height: 'auto', objectFit: 'contain' } }),
        h('figcaption', {}, label)));
    }
    if (kind === 'media') {
      bilingual('Title', 'title'); bilingual('Summary', 'summary');
      line('Type', field(entry, 'type')); line('Outlet', field(entry, 'outlet'));
      line('Date (only if verified)', field(entry, 'date')); line('URL', field(entry, 'canonical_url'));
      line('Researcher', field(entry, 'person_id')); line('Publication', field(entry, 'publication_id'));
    } else if (kind === 'publications') {
      line('Title (original language)', field(entry, 'title'));
      line('Authors (citation order)', field(entry, 'authors'));
      line('Exact publication date', field(entry, 'publication_date')); line('Date source', field(entry, 'publication_date_source_url')); line('ISBN', field(entry, 'isbn'));
      line('Year', field(entry, 'year')); line('Type', field(entry, 'type')); line('Journal / publisher', field(entry, 'venue'));
      var rights = field(entry, 'image_rights_status') || 'pending';
      line('Image reuse status', rights); line('Rights evidence', field(entry, 'image_rights_url'));
      if (rights !== 'pending') image('Article thumbnail', field(entry, 'image'), field(entry, 'image_alt'));
      else line('Publication preview', 'Bibliographic reference; image permission pending or image unavailable.');
      line('Companion policy brief', field(entry, 'policy_brief_id'));
      bilingual('Abstract', 'abstract'); line('Research areas', field(entry, 'topics'));
      line('DOI', field(entry, 'doi')); line('Article URL', field(entry, 'canonical_url')); line('PDF', field(entry, 'pdf') || field(entry, 'pdf_url'));
    } else if (kind === 'people') {
      image('Portrait', field(entry, 'portrait'), field(entry, 'portrait_alt'));
      line('Complete name', field(entry, 'name')); line('Public name', field(entry, 'display_name')); line('Role', field(entry, 'role')); line('Display order', field(entry, 'display_order'));
      bilingual('Biography', 'bio'); line('Research areas', field(entry, 'research_areas'));
      line('Personal website', field(entry, 'personal_website')); line('Official profile', field(entry, 'canonical_url'));
    } else if (kind === 'research_areas') {
      bilingual('Area name', 'name'); bilingual('Introduction', 'summary'); bilingual('Overview', 'overview');
      image('Area thumbnail', field(entry, 'image'), field(entry, 'image_alt'));
      var banner = field(entry, 'banner');
      if (banner) image('Cover photograph', banner.image, banner.image_alt);
      (field(entry, 'projects') || []).forEach(function (project, index) {
        var label = 'Project ' + (index + 1);
        line(label + ' — English', project.title); line(label + ' — Español', project.title_es);
        line(label + ' description — English', project.summary); line(label + ' description — Español', project.summary_es);
        line(label + ' researchers', project.researcher_note); line(label + ' investigadores', project.researcher_note_es);
        image(label + ' image', project.image, project.image_alt);
        if (project.image) line(label + ' image display', project.image_fit === 'contain' ? 'Complete diagram / Gráfico completo' : 'Photograph — match text height / Fotografía — altura del texto');
        if (project.image) line(label + ' photo focus', project.image_focus || 'center');
        if (!project.image) line(label + ' layout', 'Full-width text; no image space is reserved.');
      });
      (field(entry, 'publication_features') || []).forEach(function (item, index) {
        var label = 'Featured publication ' + (index + 1);
        line(label, item.publication); image(label + ' thumbnail', item.image, item.image_alt);
        line(label + ' — English', item.description); line(label + ' — Español', item.description_es);
      });
      line('Team override', field(entry, 'reference_team').map ? field(entry, 'reference_team').map(function (item) { return item.person_id; }) : '');
      line('Team selection', 'An empty team override uses the researcher directory’s area assignments.');
    } else if (kind === 'news') {
      bilingual('Title', 'title'); line('Date', field(entry, 'date')); line('Category', field(entry, 'category'));
      bilingual('Summary', 'summary'); bilingual('Story', 'body');
    } else if (kind === 'seminars') {
      bilingual('Title', 'title'); line('Speaker', field(entry, 'speaker')); line('Date and time', field(entry, 'date')); line('Time zone', field(entry, 'timezone'));
      bilingual('Description', 'description'); line('Location', field(entry, 'location')); line('Event URL', field(entry, 'event_url'));
    } else if (kind === 'about') {
      bilingual('Center scope', 'scope'); bilingual('Scope heading', 'research_scope'); bilingual('Affiliation', 'affiliation'); bilingual('Collaboration', 'collaboration');
      bilingual('Contact introduction', 'contact_intro'); line('Contact email', field(entry, 'contact_email')); line('Postal address', field(entry, 'address'));
      bilingual('Seminar introduction', 'seminar_description'); bilingual('Seminar schedule', 'seminar_schedule'); bilingual('Session confirmation', 'seminar_schedule_note');
      line('Proposal form URL', field(entry, 'seminar_form_url'));
      (field(entry, 'seminar_proposals') || []).forEach(function (item, index) {
        line('Proposal ' + (index + 1) + ' — English', item.label + ': ' + item.description);
        line('Proposal ' + (index + 1) + ' — Español', item.label_es + ': ' + item.description_es);
      });
      bilingual('Editorial note (appears publicly)', 'editorial_note');
    } else {
      bilingual('Center name (do not translate)', 'center_name'); line('University', field(entry, 'university'));
      bilingual('Home heading', 'hero_heading'); bilingual('Home introduction', 'hero_summary'); bilingual('Video caption', 'campus_video_caption');
      line('News visible', String(field(entry, 'show_news'))); line('Seminars visible', String(field(entry, 'show_seminars')));
      line('Working papers visible', String(field(entry, 'show_working_papers'))); line('Policy briefs visible', String(field(entry, 'show_policy_briefs')));
    }
    line('Reference URL', field(entry, 'source_url'));
    var visibility = kind === 'site' ? 'Site settings take effect after approval, publication and a successful deployment.' :
      field(entry, 'published') ? 'Included on the website after approval and publication. Saving a draft does not change the live version.' :
      'Excluded from the public website after publication. This visibility switch is separate from review approval.';
    return h('main', { className: 'wrap', style: { maxWidth: '52rem', margin: '2rem auto', padding: '1.5rem', background: '#fff' } },
      h('div', { className: 'eyebrow' }, 'Content review preview'), h('h1', {}, title),
      h('p', { className: 'note' }, 'Review the text and images below. This is a content preview; the full page layout is available in the built site preview.'),
      h('div', {}, blocks.length ? blocks : [h('p', { key: 'empty' }, 'Add details to see them here.')]),
      h('p', { className: 'note' }, visibility));
  }
  ['media', 'site', 'about', 'people', 'research_areas', 'publications', 'news', 'seminars'].forEach(function (collection) {
    var template = createClass({ render: function () { return Preview(this.props, collection); } });
    CMS.registerPreviewTemplate(collection, template);
  });
})();
