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
    var title = field(entry, 'title') || field(entry, 'name') || field(entry, 'center_name') || 'Content preview';
    var blocks = [];
    function line(label, value) {
      if (Array.isArray(value)) value = value.map(function (item) { return typeof item === 'string' ? item : (item.name || ''); }).filter(Boolean).join(', ');
      if (value) blocks.push(h('p', { key: label }, h('strong', {}, label + ': '), String(value)));
    }
    if (kind === 'publications') {
      line('Authors', field(entry, 'authors')); line('Year', field(entry, 'year')); line('Type', field(entry, 'type')); line('Venue', field(entry, 'venue')); line('Abstract', field(entry, 'abstract')); line('Topics', field(entry, 'topics')); line('DOI', field(entry, 'doi')); line('PDF', field(entry, 'pdf') || field(entry, 'pdf_url')); line('Reference URL (optional)', field(entry, 'source_url'));
    } else if (kind === 'people') {
      line('Role', field(entry, 'role')); line('Biography', field(entry, 'bio')); line('Research areas', field(entry, 'research_areas')); line('Official profile', field(entry, 'canonical_url')); line('Reference URL (optional)', field(entry, 'source_url'));
    } else if (kind === 'research_areas') {
      line('Research focus', field(entry, 'summary')); line('Researchers', field(entry, 'people')); line('Official page', field(entry, 'canonical_url')); line('Reference URL (optional)', field(entry, 'source_url'));
    } else if (kind === 'news') {
      line('Date', field(entry, 'date')); line('Category', field(entry, 'category')); line('Summary', field(entry, 'summary')); line('Story', field(entry, 'body')); line('Canonical page', field(entry, 'canonical_url')); line('Reference URL (optional)', field(entry, 'source_url'));
    } else if (kind === 'seminars') {
      line('Series', field(entry, 'series')); line('Speaker', field(entry, 'speaker')); line('Date and time', field(entry, 'date')); line('Time zone', field(entry, 'timezone')); line('Description', field(entry, 'description')); line('Location', field(entry, 'location')); line('Registration', field(entry, 'event_url')); line('Reference URL (optional)', field(entry, 'source_url'));
    } else if (kind === 'about') {
      line('Research scope', field(entry, 'research_scope')); line('About the Center', field(entry, 'scope')); line('Collaboration', field(entry, 'collaboration')); line('Public contact', field(entry, 'contact_email')); line('Reference URL (optional)', field(entry, 'source_url'));
    } else {
      line('University', field(entry, 'university')); line('Introduction', field(entry, 'hero_summary')); line('Campus video', field(entry, 'campus_video_caption'));
    }
    return h('main', { className: 'wrap', style: { maxWidth: '52rem', margin: '2rem auto', padding: '1.5rem', background: '#fff' } },
      h('div', { className: 'eyebrow' }, 'Content preview'),
      h('h1', {}, title),
      h('div', {}, blocks.length ? blocks : [h('p', { key: 'empty' }, 'Add details to see them in this preview.')]),
      h('p', { className: 'note' }, field(entry, 'published') ? 'Marked for publication; a maintainer still reviews and merges the change.' : 'Draft only; this record will not appear on the public site.')
    );
  }
  ['site', 'about', 'people', 'research_areas', 'publications', 'news', 'seminars'].forEach(function (collection) {
    var template = createClass({ render: function () { return Preview(this.props, collection); } });
    CMS.registerPreviewTemplate(collection, template);
  });
})();
