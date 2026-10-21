"""Generate Spanish static routes and bilingual navigation without runtime dependencies."""
from __future__ import annotations
import html
import hashlib
import json
import re
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

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
        return html.escape(pairs.get(title, title) + ' | ' + pairs.get('UP Economics Research Center', 'UP Economics Research Center'))
    if core.startswith('/') and core[1:].strip() in pairs:
        return '/ ' + html.escape(pairs[core[1:].strip()])
    if core.startswith('Showing ') and core.endswith(' verified publications'):
        return 'Mostrando ' + core.split()[1] + ' publicaciones verificadas'
    return text


def localize_markup(source, pairs):
    # Translate text/accessible labels while leaving inline scripts and styles intact.
    blocks = re.split(r'(<script\b.*?</script>|<style\b.*?</style>)', source, flags=re.S | re.I)
    for index in range(0, len(blocks), 2):
        # Original publication titles and their image-link names retain their language.
        # Restore before normalizing links so their destinations still use Spanish routes.
        original_titles = []
        def preserve_title(match):
            original_titles.append(match[0])
            return f'__ORIGINAL_PUBLICATION_TITLE_{len(original_titles) - 1}__'
        value = re.sub(r'<(a|h1)\b(?=[^>]*\blang="(?:en|es)")(?=[^>]*\btranslate="no")[^>]*>.*?</\1>', preserve_title, blocks[index], flags=re.S)
        value = re.sub(r'(?<=>)([^<>]+)(?=<)', lambda m: translate_text(m[1], pairs), value)
        value = re.sub(r'\b(alt|aria-label|placeholder|title)="([^"]*)"', lambda m: m[1] + '="' + html.escape(pairs.get(html.unescape(m[2]), html.unescape(m[2])), quote=True) + '"', value)
        value = re.sub(r'(<meta name="description" content=")([^"]*)(">)', lambda m: m[1] + html.escape(pairs.get(html.unescape(m[2]), html.unescape(m[2])), quote=True) + m[3], value)
        for number, title_markup in enumerate(original_titles):
            value = value.replace(f'__ORIGINAL_PUBLICATION_TITLE_{number}__', title_markup)
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
            lambda match: match[1].replace('UP Economics Research Center', '<strong class="center-name-emphasis">UP Economics Research Center</strong>').replace('Centro de Investigación Económica UP', '<strong class="center-name-emphasis">Centro de Investigación Económica UP</strong>'),
            blocks[index],
        )
    return ''.join(blocks)


def decorate(source, english_url, language):
    # Legacy design URLs share the public page's canonical identity.
    canonical_path = english_url.removeprefix('/design') if english_url.startswith('/design/') else english_url
    if canonical_path == '/homepage-concept.html':
        canonical_path = '/'
    canonical_url = 'https://up-economics-research-center.github.io' + ('/es' if language == 'es' else '') + canonical_path
    source = re.sub(r'<link rel="canonical"[^>]*>', '', source)
    # Area identity lives in ?area=; do not collapse distinct areas to one
    # generic canonical URL before their directory content has loaded.
    if canonical_path != '/research-area.html':
        source = source.replace('</head>', '<link rel="canonical" href="' + canonical_url + '"></head>')
    switch = language_switch(english_url, language)
    # Keep language, search and menu in one predictable utility group.
    source = source.replace('<div class="mobile-controls">', '<div class="nav-utilities">' + switch + '<div class="mobile-controls">', 1)
    source = re.sub(r'(<div class="nav-tools">.*?</button>\s*</div>)', r'\1</div>', source, count=1, flags=re.S)
    scripts = '<script>document.documentElement.dataset.presentation = "gallery";</script><script src="/design/site-motion.js" defer></script><script src="/design/publication-recency.js" defer></script><script src="/design/language-strings.js"></script><script src="/design/language.js"></script>'
    source = source.replace('</head>', f'<link rel="alternate" hreflang="en" href="https://up-economics-research-center.github.io{english_url}"><link rel="alternate" hreflang="es" href="https://up-economics-research-center.github.io/es{english_url}">{scripts}</head>')
    source = source.replace('</head>', '<link rel="icon" type="image/svg+xml" href="/favicon.svg"><link rel="icon" href="/favicon.ico" sizes="any"><link rel="apple-touch-icon" href="/apple-touch-icon.png"></head>')
    return emphasize_center_name(source)


def generate_languages(site: Path, data, settings, about):
    style_version = hashlib.sha256((site / 'design/site-concept.css').read_bytes()).hexdigest()[:12]
    ui = json.loads((ROOT / 'content/settings/interface-es.json').read_text())
    legal = json.loads((ROOT / 'content/settings/legal.json').read_text())
    def expand_legal(value):
        if isinstance(value, str):
            for field in ('contact_name', 'contact_email', 'official_privacy_url'):
                value = value.replace('{{' + field + '}}', legal[field])
            return value
        if isinstance(value, list):
            return [expand_legal(item) for item in value]
        if isinstance(value, dict):
            return {key: expand_legal(item) for key, item in value.items()}
        return value
    legal['pages'] = expand_legal(legal['pages'])
    for page in legal['pages']:
        if page['slug'] not in {'privacy', 'terms', 'cookies', 'rights'}:
            raise LocaleError('Legal pages must use an existing legal route.')
        for section in page['sections']:
            for item in section.get('links', []):
                for url in (item['url'], item.get('url_en') or item['url']):
                    parsed = urlsplit(url)
                    valid = (url.startswith('/') and not url.startswith('//')) or (parsed.scheme == 'https' and bool(parsed.netloc)) or (parsed.scheme == 'mailto' and bool(parsed.path) and '@' in parsed.path)
                    if not valid or any(ord(char) < 32 for char in url):
                        raise LocaleError('Legal links must use HTTPS, a local route, or an email address.')

    if legal['review_status'] == 'approved' and not (legal.get('reviewed_by') and legal.get('reviewed_on')):
        raise LocaleError('Legal approval needs a reviewer and review date.')
    pairs = dict(ui)
    # The title is editorial content, so translate the action rather than matching
    # a single hard-coded title in the interface dictionary.
    if settings.get('campus_video_title'):
        pairs['Play ' + settings['campus_video_title']] = 'Reproducir ' + settings['campus_video_title']
    months_es = ('enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre')
    for item in data['media']:
        if item.get('date'):
            day = date.fromisoformat(item['date'][:10])
            pairs[day.strftime('%B %d, %Y')] = f'{day.day} de {months_es[day.month - 1]} de {day.year}'
    collect_pairs(legal, pairs)
    for page in legal["pages"]:
        pairs[page["title"]] = page["title_es"]
    for records in [*data.values(), settings, about]:
        collect_pairs(records, pairs)
    for row in data['media']:
        pairs[row['title']] = row['title_es']
    # Essential public fields must have actual translations before shipping a Spanish route.
    requirements = {'people': ('bio',), 'research_areas': ('name', 'summary', 'overview'), 'publications': ('abstract',), 'news': ('title', 'summary', 'body'), 'seminars': ('title', 'description'), 'media': ('title', 'summary')}
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
    # The directory feeds must change URLs with their content, just like CSS and JS.
    # Otherwise a newly deployed area page can display cached publication images/names.
    directory_version = hashlib.sha256(b''.join(
        (site / (name + '.json')).read_bytes()
        for name in ('people', 'research-areas', 'publications')
    )).hexdigest()[:12]
    (site / 'design/language-strings.js').write_text('window.UP_DIRECTORY_VERSION = ' + json.dumps(directory_version) + ';\nwindow.UP_PUBLIC_SECTIONS = ' + json.dumps(visible_sections) + ';\nwindow.UP_TRANSLATIONS = ' + json.dumps(ui, ensure_ascii=False).replace('<', '\\u003c') + ';\n')
    for name in ('people', 'research-areas', 'publications', 'news', 'seminars', 'media'):
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
    # Credit only media used in this build, and describe its actual display treatment.
    catalog = {row['path']: row for row in json.loads((ROOT / 'design/assets/research/photo-sources.json').read_text())}
    credits = {}
    def credit(record, title, kind, treatment, title_es=None):
        path = record.get('image')
        if not path or path in credits:
            return
        source = catalog.get(path, {})
        credits[path] = {
            'title': title,
            'title_es': title_es or title,
            'creator': record.get('image_credit') or source.get('creator', ''),
            'source': record.get('image_source_url') or source.get('source_url') or path,
            'license': record.get('image_license') or source.get('license', ''),
            'license_url': record.get('image_license_url') or source.get('license_url', ''),
            'kind': kind,
            'treatment': treatment,
        }
    publications = {row['slug']: row for row in data['publications']}
    for pub in data['publications']:
        kind = 'Book cover' if pub['type'] == 'Book' else 'Article first page' if '/assets/publications/' in pub.get('image', '') else 'Journal-page capture'
        credit(pub, pub['title'], kind, 'Displayed complete, without cropping or color filters.')
    for area in data['research_areas']:
        credit(area, area['name'], 'Research area image', 'Resized and cropped to fill the display frame; original source linked. No color filters.', area['name_es'])
        if area.get('banner'):
            credit(area['banner'], area['name'], 'Cover image', 'Resized and cropped to fill the display frame; original source linked. No color filters.', area['name_es'])
        for project in area.get('projects', []):
            credit(project, project['title'], 'Project image', 'Displayed complete, without cropping or color filters.' if project.get('image_fit') == 'contain' else 'Resized and cropped to match adjacent text; no color filters.', project['title_es'])
        for feature in area.get('publication_features', []):
            if feature['publication'] in publications:
                credit(feature, publications[feature['publication']]['title'], 'Journal-page capture', 'Displayed complete, without cropping or color filters.')
    items = ''
    for row in credits.values():
        license_link = ''
        if row['license_url']:
            license_link = '<p><a href="' + html.escape(row['license_url'], quote=True) + '">' + html.escape(row['license'] or 'License') + '</a></p>'
        items += ('<article class="photo-source"><div class="eyebrow">' + html.escape(row['kind']) + '</div><h2>' + html.escape(row['title']) + '</h2><p>' + html.escape(row['creator']) + '</p><p><a href="' + html.escape(row['source'], quote=True) + '">Image source</a></p>' + license_link + '<p>' + html.escape(row['treatment']) + '</p></article>')
    credit_page = (site / 'research.html').read_text()
    credit_page = re.sub(r'<main.*?</main>', '<main id="main-content" tabindex="-1"><section class="section"><div class="wrap"><h1>Image credits</h1>' + items + '</div></section></main>', credit_page, flags=re.S)
    credit_page = re.sub(r'<title>.*?</title>', '<title>Image credits | UP Economics Research Center</title>', credit_page)
    credit_page = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Sources and credits for images used on the Center’s website.">', credit_page)
    (site / 'photo-credits.html').write_text(credit_page)
    # Render legal bodies from their actual language record, including any paragraph count.
    def legal_main(page, language):
        suffix = '_es' if language == 'es' else ''
        home_label = 'Inicio' if language == 'es' else 'Home'
        version_label = 'Versión' if language == 'es' else 'Version'
        body = ''
        for section in page['sections']:
            paragraphs = ''.join('<p>' + html.escape(text) + '</p>' for text in re.split(r'\n\s*\n', section['body' + suffix]) if text)
            links = ''
            for item in section.get('links', []):
                url = spanish_url(item['url']) if language == 'es' else (item.get('url_en') or item['url'])
                links += '<p><a href="' + html.escape(url, quote=True) + '">' + html.escape(item['label' + suffix]) + '</a></p>'
            body += '<section><h2>' + html.escape(section['heading' + suffix]) + '</h2>' + paragraphs + links + '</section>'
        home_url = '/es/' if language == 'es' else '/'
        title = html.escape(page['title' + suffix])
        version = '' if page['slug'] in {'privacy', 'terms'} else '<p class="legal-version">' + version_label + ': ' + html.escape(legal['version']) + '</p>'
        return '<main id="main-content" class="legal-page" tabindex="-1"><section class="page-hero"><div class="wrap"><div class="crumb"><a href="' + home_url + '">' + home_label + '</a> / ' + title + '</div><h1>' + title + '</h1><p>' + html.escape(page['summary' + suffix]) + '</p></div></section><div class="wrap legal-content">' + body + version + '</div></main>'

    template = (site / 'research.html').read_text()
    legal_routes = {page['slug'] + '.html': page for page in legal['pages']}
    for route, page in legal_routes.items():
        markup = re.sub(r'<main.*?</main>', lambda m: legal_main(page, 'en'), template, flags=re.S)
        markup = re.sub(r'<title>.*?</title>', '<title>' + html.escape(page['title']) + ' | UP Economics Research Center</title>', markup)
        markup = re.sub(r'<meta name="description" content="[^"]*">', lambda m: '<meta name="description" content="' + html.escape(page['summary'], quote=True) + '">', markup)
        markup = markup.replace('class="active" aria-current="page"', 'class=""')
        (site / route).write_text(markup)
    pairs['Draft for institutional review. Not yet approved by Universidad Panamericana.'] = 'Borrador para revisión institucional. Aún no aprobado por la Universidad Panamericana.'
    pairs['Version: ' + legal['version']] = 'Versión: ' + legal['version']
    for en, es in [('Privacy notice','Aviso de privacidad'),('Terms of use','Términos de uso'),('Storage and external services','Almacenamiento y servicios externos'),('Copyright and attribution','Derechos de autor y atribución'),('Legal information','Información legal')]:
        pairs[en] = es
    paths = [site / 'index.html' , *site.glob('*.html'), *site.glob('publications/*/index.html'), *site.glob('design/*.html')]
    for path in dict.fromkeys(paths):
        rel = path.relative_to(site).as_posix()
        english_url = '/' if rel == 'index.html' else '/' + rel.removesuffix('index.html') if rel.startswith('publications/') else '/' + rel
        source = path.read_text().replace('<b>At the Center</b>', '<b>At the Center</b><a href="/media.html">Media</a>').replace('</footer>', '<nav class="wrap legal-footer" aria-label="Legal information"><a href="/privacy.html">Privacy notice</a><a href="/terms.html">Terms of use</a><a href="/cookies.html">Storage and external services</a><a href="/rights.html">Copyright and attribution</a><a href="/photo-credits.html">Image credits</a></nav></footer>')
        footer = ('<div class="footer-bottom"><span>' + html.escape(settings['university']) + ' · ' + html.escape(settings['center_name']) + '</span><span>' + html.escape(settings.get('footer_note', '')) + '</span></div>')
        source = re.sub(r'<div class="footer-bottom">.*?</div>', lambda match: footer, source, flags=re.S)
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
        if rel == 'photo-credits.html':
            for row in credits.values():
                translated = translated.replace('<h2>' + html.escape(row['title']) + '</h2>', '<h2>' + html.escape(row['title_es']) + '</h2>')
        translated = localize_markup(translated, pairs)
        if rel in legal_routes:
            translated = re.sub(r'<main.*?</main>', lambda m: legal_main(legal_routes[rel], 'es'), translated, flags=re.S)
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
