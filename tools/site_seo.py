"""Static research routes, search metadata and crawl discovery. No network at build time."""
from __future__ import annotations
import html
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlsplit
from xml.etree import ElementTree as ET
from site_locales import spanish, language_switch

ROOT = Path(__file__).resolve().parents[1]
e = html.escape


def paragraphs(text, cls=''):
    attr = f' class="{cls}"' if cls else ''
    return ''.join(f'<p{attr}>{e(p)}</p>' for p in re.split(r'\n\s*\n', text) if p)


def area_main(area, people, publications, language, image_html, render_authors, recency_badge):
    """Use the same classes, assets and record selection as the legacy area renderer."""
    prefix = '/es' if language == 'es' else ''
    ui = json.loads((ROOT / 'content/settings/interface-es.json').read_text())
    def t(text):
        return ui.get(text, text) if prefix else text
    def a(url, text, cls=''):
        return f'<a href="{e(url, quote=True)}" class="{cls}">{e(text)}</a>'
    def photo(record, cls):
        markup = image_html(record, cls)
        attrs = ''
        if record.get('image_fit') == 'contain':
            attrs += ' data-image-fit="contain"'
        if record.get('image_focus') in ('top', 'center', 'bottom'):
            attrs += f' style="object-position:center {record["image_focus"]}"'
        return markup.replace('<img ', '<img' + attrs + ' ', 1)
    reference = area.get('layout') == 'original-reference'
    image = area if area.get('image') else area.get('banner', {})
    visual = ''
    if image.get('image'):
        if reference:
            visual = f'<figure class="area-presentation-image motion-frame" data-area="{e(area["slug"])}">' + photo(image, 'source-area-banner').replace('loading="lazy"', 'loading="eager"') + '</figure>'
        else:
            visual = f'<figure class="feature-area-visual research-art" data-area="{e(area["slug"])}">' + photo(image, 'research-photo') + '</figure>'
    summary = '<div class="feature-area-copy"><div id="area-summary" class="area-description">' + paragraphs(area['summary']) + paragraphs(area.get('overview', '')) + '</div></div>'
    intro = visual + summary if reference else summary + visual
    hero = (f'<section class="feature-area" id="area-hero"><div class="area-heading"><div class="crumb" role="navigation" aria-label="{t("Breadcrumb")}">'
            + a(prefix + '/', t('Home')) + ' / ' + a(prefix + '/research.html', t('Research')) + ' / ' + e(area['name'])
            + '</div><div class="eyebrow">' + t('Research area') + '</div><h1 id="area-title">' + e(area['name']) + '</h1></div><div class="area-intro">' + intro + '</div></section>')
    projects = ''
    for project in area['projects']:
        heading = a(project['url'], project['title']) if project.get('url') else e(project['title'])
        notes = ''
        for text in re.split(r'\n\s*\n', project.get('researcher_note', '')):
            if not text:
                continue
            match = re.match(r'^((?:UP Researchers?:|Investigador(?:es)? UP:)\s*)([\s\S]*)$', text)
            value = e(text)
            if match:
                names = [name.strip() for name in match[2].split('\n') if name.strip()]
                conjunction = ' y ' if prefix else ' and '
                group = ', '.join(names[:-1]) + conjunction + names[-1] if len(names) > 1 else names[0] if names else ''
                value = e(match[1]) + '<strong>' + e(group) + '</strong>'
            notes += '<p class="pub-authors">' + value + '</p>'
        media = ''
        if project.get('image'):
            img = photo(project, 'project-photo')
            if project.get('url'):
                img = f'<a href="{e(project["url"])}" aria-label="{e(project["title"])}">{img}</a>'
            media = '<figure class="project-media">' + img + '</figure>'
        projects += '<article class="publication project-card' + (' has-image' if media else '') + '"><div class="project-copy"><h3 class="pub-title">' + heading + '</h3><div class="project-description">' + paragraphs(project['summary']) + '</div><div class="project-researchers">' + notes + '</div></div>' + media + '</article>'
    if not projects:
        projects = '<p class="note">' + t('No current projects are listed for this area.') + '</p>'
    if reference and area.get('reference_team'):
        index = {person['slug']: person for person in people}
        members = [index[item['person_id']] for item in area['reference_team'] if item['person_id'] in index]
    else:
        members = [person for person in people if area['slug'] in person['research_areas']]
    team = ''
    for person in members:
        portrait = ''
        if person.get('portrait'):
            crop = person.get('portrait_crop')
            style = ''
            if crop:
                style = f' style="--crop-width:{10000 / crop["width"]:.4f}%;--crop-height:{10000 / crop["height"]:.4f}%;--crop-left:{-100 * crop["left"] / crop["width"]:.4f}%;--crop-top:{-100 * crop["top"] / crop["height"]:.4f}%"'
            classes = 'area-portrait' + (' reference-portrait' if person.get('reference_portrait') else '') + (' portrait-frame' if crop else '')
            portrait = f'<div class="{classes}"{style}><img src="{e(person["portrait"])}" alt="" width="240" height="300" loading="lazy"></div>'
        team += f'<a class="area-person" href="{prefix}/people.html#{e(person["slug"])}">{portrait}<span><strong>{e(person.get("display_name") or person["name"])}</strong><small>{t("View profile →")}</small></span></a>'
    if not team:
        team = '<p class="note">' + t('No published researcher profiles are linked to this area yet.') + '</p>'
    related = sorted([pub for pub in publications if area['slug'] in pub['topics']], key=lambda pub: (-pub['year'], pub['title']))
    papers = ''
    for pub in related:
        feature = next((item for item in area.get('publication_features', []) if item['publication'] == pub['slug']), {}) if reference else {}
        description = feature.get('description') or pub['abstract'] if reference else ''
        href = pub.get('canonical_url') or pub.get('pdf_url') or pub.get('pdf') or ''
        title = (f'<a href="{e(href, quote=True)}" lang="{pub["title_language"]}" translate="no">{e(pub["title"])}</a>'
                 if href else f'<span lang="{pub["title_language"]}" translate="no">{e(pub["title"])}</span>')
        img = photo({**pub, 'image_alt': ''}, 'paper-photo')
        preview = ''
        if img:
            preview = (f'<a class="paper-image" href="{e(href, quote=True)}" aria-label="{e(pub["title"])}" lang="{pub["title_language"]}" translate="no">{img}</a>'
                       if href else '<div class="paper-image">' + img + '</div>')
        authors = render_authors(pub).replace('href="/people.html', f'href="{prefix}/people.html')
        if prefix:
            for en in ('UP researchers:', 'UP researcher:', 'with'):
                authors = authors.replace('>' + en + '<', '>' + t(en) + '<')
        media = ''.join(a(item['url'], item['label']) for item in feature.get('media_links', []))
        brief = a(prefix + '/publications/' + pub['policy_brief']['slug'] + '/', t('Policy brief →'), 'text-link') if pub.get('policy_brief') else ''
        body = '<div class="paper-heading">' + recency_badge(pub).replace('>New<', '>' + t('New') + '<') + '<h3 class="pub-title">' + title + '</h3></div>'
        if description:
            body += '<div class="paper-description">' + paragraphs(description, 'reference-description') + '</div>'
        body += '<div class="paper-details"><p class="pub-authors">' + authors + '</p><p class="pub-venue">' + e(pub['venue'] or t(pub['type'])) + ' · ' + str(pub['year']) + '</p><div class="reference-media-links">' + media + '</div>' + brief + '</div>'
        action = a(href, t('Read paper ↗' if pub['type'] == 'Journal article' else 'View publication ↗'), 'text-link') if href else ''
        papers += '<article class="publication paper-row' + (' has-image' if img else '') + (' reference-paper' if description else '') + '">' + preview + '<div class="paper-copy">' + body + action + '</div></article>'
    if not papers:
        papers = '<p class="note">' + t('No verified publications are linked to this area yet.') + '</p>'
    def block(key, heading, content, cls=''):
        return f'<div class="split-label" id="{key}"><h2>{t(heading)}</h2></div><div id="' + {'team':'area-team','projects':'project-list','outputs':'outputs-list'}[key] + f'" class="{cls}">{content}</div>'
    team_block = block('team', 'Team' if reference else 'People behind this work', team, 'area-team')
    project_block = block('projects', 'Current Projects' if reference else 'Ongoing research', projects)
    outputs_heading = 'Journal Publications' if reference and not any(pub['type'] != 'Journal article' for pub in related) else 'Publications'
    output_block = block('outputs', outputs_heading, papers)
    aside = '<aside class="side-index">' + ''.join(a('#' + key, t(label)) for key,label in [('projects','Projects'),('team','Researchers'),('outputs','Publications')]) + '</aside>'
    content = team_block + project_block + output_block if reference else project_block + team_block + output_block
    return '<main id="main-content" tabindex="-1">' + hero + '<section class="section"><div class="wrap area-content">' + aside + '<div class="area-main">' + content + '</div></div></section></main>'


def clean_description(value):
    value = re.sub(r'\s+', ' ', value).strip()
    return value if len(value) <= 190 else value[:187].rsplit(' ', 1)[0] + '…'


def build_not_found(site, base):
    """GitHub Pages serves the root file at missing URLs, including nested ones."""
    main = (ROOT / 'templates/not-found.html').read_text(encoding='utf-8')
    for language, prefix in [('en', ''), ('es', '/es')]:
        shell = (site / prefix.lstrip('/') / 'research.html').read_text(encoding='utf-8')
        shell = shell.replace('<html ', '<html data-error-page="404" ', 1)
        shell = re.sub(r'<main\b.*?</main>', lambda _: main, shell, flags=re.S)
        title = 'Página no encontrada' if prefix else 'Page not found'
        shell = re.sub(r'<title>.*?</title>', f'<title>404 · {title} | UP Economics Research Center</title>', shell)
        shell = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="404 · {title}. Page not found / Página no encontrada.">', shell)
        shell = re.sub(r'<div class="language-switch".*?</div>', lambda _: language_switch('/404.html', language), shell, flags=re.S)
        shell = shell.replace('class="active" aria-current="page"', 'class=""')
        # Absolute destinations and assets work from any missing nested URL.
        shell = re.sub(r'(href|src)="(/[^"<>]*)"', lambda m: m[1] + '="' + base + m[2] + '"', shell)
        (site / prefix.lstrip('/') / '404.html').write_text(shell, encoding='utf-8')


def build_llms(site, base, routes):
    """Index canonical public research pages; reuse visibility decisions from SEO."""
    lines = ['# UP Economics Research Center', '',
             '> Public economic research at Universidad Panamericana, in English and Spanish.', '',
             'This optional index links to the public website. Publication titles retain their original language.',
             'Editorial review notes on linked pages still apply. This file does not grant reuse rights.', '',
             f'Sitemap: {base}/sitemap.xml', '']
    for prefix, label in [('', 'English'), ('/es', 'Español')]:
        localized = [route for route in sorted(set(routes)) if route.startswith('/es/') == bool(prefix)]
        groups = [('Overview', lambda route: route in ('/', '/research.html', '/people.html', '/publications.html', '/seminars.html', '/news.html', '/media.html')),
                  ('Research areas', lambda route: route.startswith('/research/')),
                  ('Publications', lambda route: route.startswith('/publications/'))]
        for group, include in groups:
            selected = [route for route in localized if include(route.removeprefix(prefix) if prefix else route)]
            if not selected:
                continue
            lines += [f'## {label} — {group}', '']
            for route in selected:
                path = site / route.lstrip('/')
                if route.endswith('/'):
                    path /= 'index.html'
                markup = path.read_text(encoding='utf-8')
                title = html.unescape(re.search(r'<title>(.*?)</title>', markup, re.S)[1]).split(' | ')[0]
                title = re.sub(r'\s+', ' ', title).replace('[', r'\[').replace(']', r'\]')
                lines.append(f'- [{title}]({base}{route})')
            lines.append('')
    (site / 'llms.txt').write_text('\n'.join(lines), encoding='utf-8')


def apply_seo(site, data, settings, image_html, render_authors, recency_badge):
    config = json.loads((ROOT / 'content/settings/discovery.json').read_text())
    base = config['site_url'].rstrip('/')
    parsed = urlsplit(base)
    if parsed.scheme != 'https' or not parsed.netloc or parsed.path or parsed.query or parsed.fragment:
        raise ValueError('Discovery site_url must be an HTTPS origin without a path.')
    for field in ('google_site_verification', 'bing_site_verification'):
        if config.get(field) and not re.fullmatch(r'[A-Za-z0-9_-]{8,256}', config[field]):
            raise ValueError('Invalid ' + field + ' token.')
    analytics = config.get('cloudflare_analytics_token', '')
    if analytics and not re.fullmatch(r'[a-fA-F0-9]{32}', analytics):
        raise ValueError('Cloudflare Web Analytics token must contain 32 hexadecimal characters.')
    share = config['share_image']
    if not share.startswith('/design/assets/') or '..' in share or not (site / share.lstrip('/')).is_file():
        raise ValueError('Sharing image must be an existing local public asset.')
    build_not_found(site, base)
    # Static area pages reuse the fully localized page shell and approved records.
    for language in ('en', 'es'):
        prefix = '/es' if language == 'es' else ''
        records = spanish(data) if prefix else data
        template = (site / (prefix.lstrip('/') + '/research-area.html').lstrip('/')).read_text()
        for area in records['research_areas']:
            markup = re.sub(r'<main\b.*?</main>', lambda _: area_main(area, records['people'], records['publications'], language, image_html, render_authors, recency_badge), template, flags=re.S)
            if area.get('layout') == 'original-reference':
                markup = markup.replace('<body>', '<body class="source-area-page">')
            markup = re.sub(r'<script\b[^>]*src="[^"]*research-people\.js[^"<>]*"[^>]*></script>', '', markup)
            for lang, lang_prefix in [('en',''),('es','/es')]:
                markup = re.sub(r'<a\b(?=[^>]*data-language="' + lang + '")[^>]*>', lambda m: re.sub(r'href="[^"]*"', 'href="' + lang_prefix + '/research/' + area['slug'] + '/"', m[0]), markup)
            markup = re.sub(r'<title>.*?</title>', lambda _: '<title>' + e(area['name']) + ' | UP Economics Research Center</title>', markup)
            markup = markup.replace('</head>', '<meta name="description" content="' + e(clean_description(area['summary']), quote=True) + '"></head>')
            target = site / prefix.lstrip('/') / 'research' / area['slug'] / 'index.html'
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(markup)
    def migrate(value):
        return re.sub(r'(?:(?:/design)?/)?research-area\.html\?area=([a-z0-9-]+)', lambda m: '/research/' + m[1] + '/', value)
    canonical_routes = []
    area_by_slug = {area['slug']: area for area in data['research_areas']}
    pub_by_slug = {pub['slug']: pub for pub in data['publications']}
    for path in site.rglob('*.html'):
        rel = path.relative_to(site).as_posix()
        markup = path.read_text()
        if rel.startswith('admin/'):
            markup = markup.replace('</head>', '<meta name="robots" content="noindex"></head>')
            path.write_text(markup)
            continue
        markup = migrate(markup)
        es = rel.startswith('es/')
        prefix = '/es' if es else ''
        route = '/' + rel.removesuffix('index.html') if rel.endswith('index.html') else '/' + rel
        english = route.removeprefix('/es') if es else route
        public_english = english.removeprefix('/design') if english.startswith('/design/') else english
        if public_english == '/homepage-concept.html':
            public_english = '/'
        canonical = base + prefix + public_english
        excluded = '/design/' in route or public_english in ('/about.html', '/research-area.html', '/404.html')
        if not excluded:
            canonical_routes.append(route)
        markup = re.sub(r'<link\b(?=[^>]*rel="(?:canonical|alternate)")[^>]*>', '', markup)
        meta = f'<link rel="canonical" href="{canonical}">' + ''.join(f'<link rel="alternate" hreflang="{lang}" href="{base + pre + public_english}">' for lang,pre in [('en',''),('es','/es'),('x-default','')])
        if public_english in ('/research-area.html', '/404.html'):
            meta = '<meta name="robots" content="noindex">'
        if public_english == '/':
            title = ('Investigación económica en México' if es else 'Economic research in Mexico') + ' | UP Economics Research Center'
            markup = re.sub(r'<title>.*?</title>', lambda _: '<title>' + e(title) + '</title>', markup)
        title_match = re.search(r'<title>(.*?)</title>', markup, re.S)
        title = html.unescape(re.sub('<[^>]+>', '', title_match[1])) if title_match else settings['center_name']
        desc_match = re.search(r'<meta name="description" content="([^"]*)"', markup)
        description = html.unescape(desc_match[1]) if desc_match else (settings['hero_summary_es'] if es else settings['hero_summary'])
        description = clean_description(description)
        if desc_match:
            markup = re.sub(r'<meta name="description" content="[^"]*">', lambda _: '<meta name="description" content="' + e(description, quote=True) + '">', markup)
        else:
            meta += '<meta name="description" content="' + e(description, quote=True) + '">'
        record = None
        image = share
        kind = 'WebPage'
        if public_english.startswith('/research/'):
            record = area_by_slug.get(public_english.split('/')[2])
            if record:
                image = record.get('image') or share
        if public_english.startswith('/publications/'):
            record = pub_by_slug.get(public_english.split('/')[2])
            if record:
                image = record.get('image') or share
                kind = {'Journal article':'ScholarlyArticle','Book':'Book','Book chapter':'Chapter'}.get(record['type'], 'CreativeWork')
        for key,value in [('og:title',title),('og:description',description),('og:url',canonical),('og:type','article' if kind in ('ScholarlyArticle','CreativeWork') else 'website'),('og:site_name',settings['center_name']),('og:locale','es_MX' if es else 'en_US'),('og:locale:alternate','en_US' if es else 'es_MX'),('og:image',base + image)]:
            meta += f'<meta property="{key}" content="{e(value, quote=True)}">'
        meta += '<meta name="twitter:card" content="summary_large_image">'
        for key,value in [('title',title),('description',description),('image',base+image)]:
            meta += f'<meta name="twitter:{key}" content="{e(value, quote=True)}">'
        schema = {'@context':'https://schema.org','@type':kind,'@id':canonical + '#content','url':canonical,'name':title.split(' | ')[0],'description':description,'inLanguage':'es' if es else 'en','isPartOf':{'@id':base + '/#website'}}
        if kind != 'WebPage' and record:
            schema.update(name=record['title'], author=[{'@type':'Person','name':author if isinstance(author,str) else author['name']} for author in record['authors']])
            schema['inLanguage'] = record['title_language']
            meta += '<meta name="citation_title" content="' + e(record['title'], quote=True) + '">'
            for author in record['authors']:
                meta += '<meta name="citation_author" content="' + e(author if isinstance(author,str) else author['name'], quote=True) + '">'
            meta += '<meta name="citation_publication_date" content="' + str(record['year']) + '">'
            if record['type'] == 'Journal article' and record.get('venue'):
                meta += '<meta name="citation_journal_title" content="' + e(record['venue'], quote=True) + '">'
            if record.get('doi'):
                meta += '<meta name="citation_doi" content="' + e(record['doi'], quote=True) + '">'
                schema['identifier'] = 'https://doi.org/' + record['doi']
            if record.get('canonical_url'):
                schema['sameAs'] = record['canonical_url']
            if record.get('publication_date'):
                schema['datePublished'] = record['publication_date']
        graph = [schema]
        if public_english == '/':
            graph += [{'@type':'Organization','@id':base + '/#organization','name':settings['center_name'],'url':base + '/','parentOrganization':{'@type':'EducationalOrganization','name':settings['university'],'url':'https://www.up.edu.mx/'}}, {'@type':'WebSite','@id':base + '/#website','name':settings['center_name'],'url':base + '/','inLanguage':['en','es'],'publisher':{'@id':base + '/#organization'}}]
        meta += '<script type="application/ld+json">' + json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False).replace('<','\\u003c') + '</script>'
        for field,name in [('google_site_verification','google-site-verification'),('bing_site_verification','msvalidate.01')]:
            if config.get(field):
                meta += f'<meta name="{name}" content="{e(config[field], quote=True)}">'
        if analytics and not excluded:
            privacy_version = hashlib.sha256((site / 'design/privacy-preferences.js').read_bytes()).hexdigest()[:12]
            meta += f'<script src="/design/privacy-preferences.js?v={privacy_version}" data-analytics-token="{analytics}" data-site-host="{parsed.hostname}" defer></script>'
        markup = markup.replace('</head>', meta + '</head>')
        path.write_text(markup)
    # Update all site-search destinations too; do not change editorial source IDs.
    for prefix in ('', 'es/'):
        path = site / (prefix + 'search-index.json')
        path.write_text(migrate(path.read_text()))
    ns = 'http://www.sitemaps.org/schemas/sitemap/0.9'
    xhtml = 'http://www.w3.org/1999/xhtml'
    ET.register_namespace('', ns)
    ET.register_namespace('xhtml', xhtml)
    root = ET.Element('{' + ns + '}urlset')
    for route in sorted(set(canonical_routes)):
        entry = ET.SubElement(root, '{' + ns + '}url')
        ET.SubElement(entry, '{' + ns + '}loc').text = base + route
        english = route.removeprefix('/es') if route.startswith('/es/') else route
        for lang,pre in [('en',''),('es','/es'),('x-default','')]:
            ET.SubElement(entry, '{' + xhtml + '}link', rel='alternate', hreflang=lang, href=base + pre + english)
    ET.ElementTree(root).write(site / 'sitemap.xml', encoding='utf-8', xml_declaration=True)
    (site / 'robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: ' + base + '/sitemap.xml\n')
    build_llms(site, base, canonical_routes)
