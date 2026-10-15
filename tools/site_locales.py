"""Generate Spanish static routes and bilingual navigation without runtime dependencies."""
from __future__ import annotations
import html
import hashlib
import json
import re
from pathlib import Path

class LocaleError(Exception):
    pass


ROOT = Path(__file__).resolve().parents[1]


def spanish(record):
    if isinstance(record, list):
        return [spanish(item) for item in record]
    if not isinstance(record, dict):
        return record
    return {key: spanish(record.get(key + '_es', value)) for key, value in record.items() if not key.endswith('_es')}


def collect_pairs(record, pairs):
    if isinstance(record, list):
        for item in record:
            collect_pairs(item, pairs)
    elif isinstance(record, dict):
        for key, value in record.items():
            if key.endswith('_es') and key != 'title_es' and isinstance(value, str) and isinstance(record.get(key[:-3]), str):
                pairs[record[key[:-3]]] = value
            else:
                collect_pairs(value, pairs)


def translate_text(text, pairs):
    decoded = html.unescape(text)
    core = decoded.strip()
    if core in pairs:
        return decoded[:len(decoded)-len(decoded.lstrip())] + html.escape(pairs[core], quote=False) + decoded[len(decoded.rstrip()):]
    for kind in ('Journal article', 'Working paper', 'Book', 'Book chapter', 'Policy brief', 'Other'):
        if core.startswith(kind + ' · '):
            return html.escape(pairs.get(kind, kind) + core[len(kind):])
    # Titles, year labels and breadcrumbs combine short interface strings.
    if ' | UP Economics Research Center' in core:
        title = core.removesuffix(' | UP Economics Research Center')
        return html.escape(pairs.get(title, title) + ' | Centro de Investigación Económica UP')
    if core.startswith('/') and core[1:].strip() in pairs:
        return '/ ' + html.escape(pairs[core[1:].strip()])
    if core.startswith('Showing ') and core.endswith(' verified publications'):
        return 'Mostrando ' + core.split()[1] + ' publicaciones verificadas'
    return text


def localize_markup(source, pairs):
    # Translate text/accessible labels while leaving inline scripts and styles intact.
    blocks = re.split(r'(<script\b.*?</script>|<style\b.*?</style>)', source, flags=re.S | re.I)
    for index in range(0, len(blocks), 2):
        value = re.sub(r'(?<=>)([^<>]+)(?=<)', lambda m: translate_text(m[1], pairs), blocks[index])
        value = re.sub(r'\b(alt|aria-label|placeholder|title)="([^"]*)"', lambda m: m[1] + '="' + html.escape(pairs.get(html.unescape(m[2]), html.unescape(m[2])), quote=True) + '"', value)
        value = re.sub(r'\bhref="([^"]*)"', lambda m: 'href="' + spanish_url(m[1]) + '"', value)
        blocks[index] = value
    return ''.join(blocks).replace('<html lang="en">', '<html lang="es">')


def spanish_url(url):
    if url.startswith('/es/') or url.startswith('#'):
        return url
    if url.startswith('/') and not url.startswith('//') and not url.startswith(('/design/', '/admin/')):
        if url == '/' or url.startswith('/#') or url.startswith('/?') or '.html' in url or url.startswith('/publications/'):
            return '/es' + url
    if re.match(r'^[a-z-]+\.html(?:[?#]|$)', url):
        return '/es/' + url
    return url


def language_switch(english_url, language):
    def link(code, label, url):
        current = ' aria-current="true"' if language == code else ''
        return f'<a href="{url}" lang="{code}" hreflang="{code}" data-language="{code}"{current}>{label}</a>'
    return '<div class="language-switch" role="navigation" aria-label="' + ('Idioma' if language == 'es' else 'Language') + '">' + link('en', 'EN', english_url) + '<span aria-hidden="true">/</span>' + link('es', 'ES', '/es' + english_url) + '</div>'


def emphasize_center_name(source):
    # Apply the visual name treatment only to rendered text, never metadata or attributes.
    blocks = re.split(r'(<head\b.*?</head>|<script\b.*?</script>|<style\b.*?</style>)', source, flags=re.S | re.I)
    for index in range(0, len(blocks), 2):
        blocks[index] = re.sub(
            r'(?<=>)([^<>]+)(?=<)',
            lambda match: match[1].replace('UP Economics Research Center', '<strong class="center-name-emphasis">UP Economics</strong> Research Center'),
            blocks[index],
        )
    return ''.join(blocks)


def decorate(source, english_url, language):
    switch = language_switch(english_url, language)
    # Put the switch beside mobile controls so it is available at every viewport.
    source = source.replace('<div class="mobile-controls">', switch + '<div class="mobile-controls">', 1)
    scripts = '<script src="/design/language-strings.js"></script><script src="/design/language.js"></script>'
    source = source.replace('</head>', f'<link rel="alternate" hreflang="en" href="https://up-economics-research-center.github.io{english_url}"><link rel="alternate" hreflang="es" href="https://up-economics-research-center.github.io/es{english_url}">{scripts}</head>')
    if language == 'es':
        source = source.replace('https://up-economics-research-center.github.io/publications/', 'https://up-economics-research-center.github.io/es/publications/')
    source = source.replace('</head>', '<link rel="icon" type="image/svg+xml" href="/favicon.svg"><link rel="icon" href="/favicon.ico" sizes="any"><link rel="apple-touch-icon" href="/apple-touch-icon.png"></head>')
    return emphasize_center_name(source)


def generate_languages(site: Path, data, settings, about):
    style_version = hashlib.sha256((site / 'design/site-concept.css').read_bytes()).hexdigest()[:12]
    ui = json.loads((ROOT / 'content/settings/interface-es.json').read_text())
    pairs = dict(ui)
    for records in [*data.values(), settings, about]:
        collect_pairs(records, pairs)
    # Essential public fields must have actual translations before shipping a Spanish route.
    requirements = {'people': ('bio',), 'research_areas': ('name', 'summary', 'overview'), 'publications': ('abstract',), 'news': ('title', 'summary', 'body'), 'seminars': ('title', 'description')}
    for collection, fields in requirements.items():
        for row in data[collection]:
            for field in fields:
                if row.get(field) and not row.get(field + '_es'):
                    raise LocaleError(f'{collection}/{row["slug"]}: missing {field}_es')
            for project in row.get('projects', []):
                if not project.get('title_es') or not project.get('summary_es'):
                    raise LocaleError(f'{row["slug"]}: project needs Spanish title and summary')
    for label, record, fields in [('site settings', settings, ('center_name', 'hero_heading', 'hero_summary', 'campus_video_caption', 'footer_note')), ('home scope/contact', about, ('scope', 'research_scope', 'collaboration', 'contact_intro', 'affiliation', 'editorial_note'))]:
        if label == 'home scope/contact' and not record.get('published'):
            continue
        for field in fields:
            if record.get(field) and not record.get(field + '_es'):
                raise LocaleError(f'{label}: missing {field}_es')
    visible_sections = {name: bool(settings.get('show_' + name, False)) for name in ('news', 'seminars')}
    (site / 'design/language-strings.js').write_text('window.UP_PUBLIC_SECTIONS = ' + json.dumps(visible_sections) + ';\nwindow.UP_TRANSLATIONS = ' + json.dumps(ui, ensure_ascii=False).replace('<', '\\u003c') + ';\n')
    for name in ('people', 'research-areas', 'publications', 'news', 'seminars'):
        file = site / (name + '.json')
        if not file.exists():
            continue
        target = site / 'es' / file.name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(spanish(json.loads(file.read_text())), ensure_ascii=False) + '\n')
    search = json.loads((site / 'search-index.json').read_text())
    es_data = {key: spanish(value) for key, value in data.items()}
    for row in search:
        row.update(name=pairs.get(row['name'], row['name']), description=pairs.get(row['description'], row['description']), url=spanish_url(row['url']), group=pairs.get(row['group'], row['group']))
        for person in es_data['people']:
            if row['url'].endswith('/people.html#' + person['slug']):
                row['description'] = person['bio']
        for area in es_data['research_areas']:
            if row['url'].endswith('?area=' + area['slug']):
                row['description'] = area['summary'] + ' ' + area['overview'] + ' ' + ' '.join(p['title'] + ' ' + p['summary'] for p in area['projects'])
        for pub in es_data['publications']:
            if row['url'].endswith('/publications/' + pub['slug'] + '/'):
                row['name'], row['description'] = pub['title'], pub['abstract']
    (site / 'es/search-index.json').write_text(json.dumps(search, ensure_ascii=False) + '\n')
    # Attribution is reachable from every page, including small research thumbnails.
    credits = json.loads((ROOT / 'design/assets/research/photo-sources.json').read_text())
    seen_images = {row.get('path') for row in credits}
    for record in [*data['research_areas'], *data['publications'], *(p for a in data['research_areas'] for p in a['projects'])]:
        if record.get('image') and record['image'] not in seen_images:
            seen_images.add(record['image'])
            credits.append({'slug': record.get('name', record.get('title', '')), 'creator': record['image_credit'], 'license': '', 'source_url': record.get('image_source_url') or record.get('image_license_url') or record['image']})
    items = ''.join('<article class="photo-source"><h2>' + html.escape(next((a['name'] for a in data['research_areas'] if a['slug'] == row.get('slug')), row.get('slug', ''))) + '</h2><p>' + html.escape(row.get('creator', '')) + ' · ' + html.escape(row.get('license', '')) + '</p><p><a href="' + html.escape(row['source_url'], quote=True) + '">Original photograph and license</a></p><p>Displayed with cropping, edge fading and color treatment.</p></article>' for row in credits if row.get('source_url'))
    credit_page = (site / 'research.html').read_text()
    credit_page = re.sub(r'<main.*?</main>', '<main id="main-content" tabindex="-1"><section class="section"><div class="wrap"><h1>Photo credits</h1>' + items + '</div></section></main>', credit_page, flags=re.S)
    credit_page = re.sub(r'<title>.*?</title>', '<title>Photo credits | UP Economics Research Center</title>', credit_page)
    (site / 'photo-credits.html').write_text(credit_page)
    paths = [site / 'index.html' , *site.glob('*.html'), *site.glob('publications/*/index.html'), *site.glob('design/*.html')]
    for path in dict.fromkeys(paths):
        rel = path.relative_to(site).as_posix()
        english_url = '/' if rel == 'index.html' else '/' + rel.removesuffix('index.html') if rel.startswith('publications/') else '/' + rel
        source = path.read_text().replace('</footer>', '<p class="wrap photo-credit"><a href="/photo-credits.html">Photo credits</a></p></footer>')
        source = re.sub(r'<a class="nav-cta"[^>]*>Contact</a>', '', source)
        source = re.sub(r'(src|href)="(?:/|design/)?(assets/[^"]+)"', r'\1="/design/\2"', source)
        source = re.sub(r'(src|href)="(?:design/)?(site-concept\.css|campus-video\.js|language\.js|mobile-navigation\.js|research-people\.js|publications\.js|news\.js)"', r'\1="/design/\2"', source)
        # Normalize visitor links to canonical routes even in the design previews.
        source = re.sub(r'href="(?:/design/|design/)?([a-z-]+\.html)([?#][^"]*)?"', lambda m: 'href="' + ('/' if m[1] == 'homepage-concept.html' else '/' + m[1]) + (m[2] or '') + '"', source)
        if rel.endswith('about.html'):
            source = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=/#contact"><title>Contact | UP Economics Research Center</title></head><body><a href="/#contact">Contact</a></body></html>'
        source = source.replace('href="/design/site-concept.css"', f'href="/design/site-concept.css?v={style_version}"')
        translated = source.replace('Generating empirical evidence to move society <span class="up-emphasis">UP</span>ward', html.escape(settings['hero_summary_es']))
        translated = translated.replace('<h2>Research<br><strong>seminars.</strong></h2>', '<h2>Seminarios<br><strong>de investigación.</strong></h2>')
        translated = localize_markup(translated, pairs)
        if rel.startswith('publications/'):
            pub = next(row for row in data['publications'] if row['slug'] == path.parent.name)
            translated = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="' + html.escape(pub['abstract_es'][:250], quote=True) + '">', translated)
        translated = translated.replace('content="0;url=/#contact"', 'content="0;url=/es/#contact"')
        target = site / 'es' / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        def version_scripts(markup):
            return re.sub(r'src="(/design/[^"?]+\.js)"', lambda m: 'src="' + m[1] + '?v=' + hashlib.sha256((site / m[1].lstrip('/')).read_bytes()).hexdigest()[:12] + '"', markup)
        target.write_text(version_scripts(decorate(translated, english_url, 'es')))
        path.write_text(version_scripts(decorate(source, english_url, 'en')))
