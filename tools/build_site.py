#!/usr/bin/env python3
"""Build the GitHub Pages artifact from approved editorial JSON records."""
from __future__ import annotations

import html
import json
import re
import shutil
import sys
import tempfile
from datetime import date
from pathlib import Path
from urllib.parse import quote, urlparse

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "_site"
CONTENT = ROOT / "content"
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
YOUTUBE_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")
DOI_RE = re.compile(r"^10\.\d{4,9}/\S+$")
COLLECTIONS = {
    "people": "people",
    "research_areas": "research-areas",
    "publications": "publications",
    "news": "news",
    "seminars": "seminars",
}


class BuildError(Exception):
    pass


def fail(path: Path, field: str, message: str) -> None:
    raise BuildError(f"{path.relative_to(ROOT)}: field '{field}': {message}")


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise BuildError(f"{path.relative_to(ROOT)}: invalid JSON: {exc}") from exc


def load_records(dirname: str) -> list[tuple[Path, dict]]:
    folder = CONTENT / dirname
    rows = []
    if not folder.exists():
        return rows
    for path in sorted(folder.glob("*.json")):
        value = load_json(path)
        if not isinstance(value, dict):
            fail(path, "record", "expected a JSON object")
        rows.append((path, value))
    return rows


def require_text(path: Path, record: dict, key: str) -> str:
    value = record.get(key)
    if not isinstance(value, str) or not value.strip():
        fail(path, key, "a non-empty value is required for published records")
    return value.strip()


def optional_text(path: Path, record: dict, key: str, default="") -> str:
    value = record.get(key, default)
    if value is None:
        return default
    if not isinstance(value, str):
        fail(path, key, "must be text")
    return value.strip()


def validate_url(path: Path, key: str, value: str, *, optional=False) -> str:
    if value is None:
        value = ""
    if not isinstance(value, str):
        fail(path, key, "must be text")
    value = value.strip()
    if not value and optional:
        return ""
    if not value:
        fail(path, key, "a verified URL is required")
    parsed = urlparse(value)
    if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password:
        fail(path, key, "use a valid https URL")
    return value


def local_asset(path: Path, key: str, value: str, *, optional=False) -> str:
    if value is None:
        value = ""
    if not isinstance(value, str):
        fail(path, key, "must be a local path or URL")
    value = value.strip()
    if not value and optional:
        return ""
    if not value:
        fail(path, key, "a local path or https URL is required")
    parsed = urlparse(value)
    if parsed.scheme:
        return validate_url(path, key, value)
    clean = value.lstrip("/")
    if not clean or ".." in Path(clean).parts:
        fail(path, key, "path must stay inside the repository")
    asset = (ROOT / clean).resolve()
    if ROOT.resolve() not in asset.parents or not asset.is_file():
        fail(path, key, f"local file does not exist: {value}")
    return "/" + clean


def validate_common(rows: list[tuple[Path, dict]], collection: str) -> list[dict]:
    visible = []
    seen = set()
    for path, record in rows:
        if not isinstance(record.get("published", False), bool):
            fail(path, "published", "must be true or false")
        if not record.get("published", False):
            continue
        slug = require_text(path, record, "slug")
        if not SLUG_RE.fullmatch(slug):
            fail(path, "slug", "use lowercase letters, numbers, and single hyphens")
        if slug in seen:
            fail(path, "slug", f"duplicate {collection} slug '{slug}'")
        seen.add(slug)
        record = dict(record)
        record["_path"] = path
        visible.append(record)
    return visible


def validate_records(raw: dict[str, list[tuple[Path, dict]]]) -> dict[str, list[dict]]:
    data = {key: validate_common(raw[key], key) for key in COLLECTIONS}
    areas = {row["slug"] for row in data["research_areas"]}
    people = {row["slug"] for row in data["people"]}

    for row in data["people"]:
        path = row.pop("_path")
        require_text(path, row, "name")
        require_text(path, row, "role")
        require_text(path, row, "bio")
        validate_url(path, "source_url", row.get("source_url", ""))
        require_text(path, row, "verified_on")
        row["portrait"] = local_asset(path, "portrait", row.get("portrait", ""), optional=True) if row.get("portrait") else ""
        row["canonical_url"] = validate_url(path, "canonical_url", row.get("canonical_url", ""), optional=True)
        topics = row.get("research_areas", [])
        if not isinstance(topics, list) or not all(isinstance(item, str) for item in topics):
            fail(path, "research_areas", "expected a list of area slugs")
        missing = [item for item in topics if item not in areas]
        if missing:
            fail(path, "research_areas", "unknown or unpublished area ID(s): " + ", ".join(missing))

    for row in data["research_areas"]:
        path = row.pop("_path")
        require_text(path, row, "name")
        require_text(path, row, "summary")
        validate_url(path, "source_url", row.get("source_url", ""))
        require_text(path, row, "verified_on")
        members = row.get("people", [])
        if not isinstance(members, list) or not all(isinstance(item, str) for item in members):
            fail(path, "people", "expected a list of researcher slugs")
        missing = [item for item in members if item not in people]
        if missing:
            fail(path, "people", "unknown or unpublished researcher ID(s): " + ", ".join(missing))
        row["people"] = members

    types = {"Journal article", "Working paper", "Book", "Book chapter", "Policy brief", "Other"}
    for row in data["publications"]:
        path = row.pop("_path")
        for key in ("title", "abstract", "type", "source_url", "verified_on"):
            require_text(path, row, key)
        validate_url(path, "source_url", row["source_url"])
        if row["type"] not in types:
            fail(path, "type", "choose a supported publication type")
        try:
            year = int(row.get("year"))
        except (TypeError, ValueError):
            fail(path, "year", "must be an integer year")
        if not 1900 <= year <= 2100:
            fail(path, "year", "must be between 1900 and 2100")
        row["year"] = year
        authors = row.get("authors")
        if not isinstance(authors, list) or not authors:
            fail(path, "authors", "add at least one verified author")
        for idx, author in enumerate(authors):
            if isinstance(author, str):
                if not author.strip():
                    fail(path, f"authors[{idx}]", "author name cannot be empty")
            elif isinstance(author, dict) and isinstance(author.get("name"), str) and author["name"].strip():
                person_id = author.get("person_id", "")
                if person_id and (not isinstance(person_id, str) or person_id not in people):
                    fail(path, f"authors[{idx}].person_id", f"unknown or unpublished researcher '{person_id}'")
            else:
                fail(path, f"authors[{idx}]", "expected a name or an author object with a name")
        doi = str(row.get("doi") or "").strip()
        if doi and not DOI_RE.fullmatch(doi):
            fail(path, "doi", "enter a DOI such as 10.1234/example")
        canonical = validate_url(path, "canonical_url", row.get("canonical_url", ""), optional=True)
        row["canonical_url"] = canonical or ("https://doi.org/" + doi if doi else "")
        pdf = str(row.get("pdf") or "").strip()
        pdf_url = str(row.get("pdf_url") or "").strip()
        if pdf and pdf_url:
            fail(path, "pdf", "provide either a local PDF or an external PDF URL, not both")
        row["pdf"] = local_asset(path, "pdf", pdf, optional=True) if pdf else ""
        row["pdf_url"] = validate_url(path, "pdf_url", pdf_url, optional=True) if pdf_url else ""
        topics = row.get("topics", [])
        if not isinstance(topics, list):
            fail(path, "topics", "expected a list of research-area slugs")
        missing = [item for item in topics if item not in areas]
        if missing:
            fail(path, "topics", "unknown or unpublished area ID(s): " + ", ".join(missing))
        row["topics"] = topics
        row["venue"] = optional_text(path, row, "venue")

    for collection in ("news", "seminars"):
        for row in data[collection]:
            path = row.pop("_path")
            required = ("title", "summary", "source_url", "verified_on") if collection == "news" else ("title", "series", "speaker", "date", "timezone", "description", "source_url", "verified_on")
            for key in required:
                require_text(path, row, key)
            validate_url(path, "source_url", row["source_url"])
            for key in (("canonical_url",) if collection == "news" else ("event_url", "recording_url")):
                row[key] = validate_url(path, key, row.get(key, ""), optional=True)
            try:
                date.fromisoformat(str(row["date"])[:10])
            except ValueError:
                fail(path, "date", "use an ISO date or date-time")
            if collection == "news":
                row["category"] = optional_text(path, row, "category", "Announcement") or "Announcement"
                row["body"] = optional_text(path, row, "body")
            else:
                row["location"] = optional_text(path, row, "location")
                if row["series"] not in {"General Research Seminar", "Student Research Seminar", "Other"}:
                    fail(path, "series", "choose a supported seminar series")

    return data


def e(value) -> str:
    return html.escape(str(value or ""), quote=True)


def iso_day(value: str) -> str:
    return str(value)[:10]


def format_date(value: str) -> str:
    try:
        return date.fromisoformat(iso_day(value)).strftime("%B %d, %Y")
    except ValueError:
        return iso_day(value)


def external_anchor(url: str, text: str, cls="text-link") -> str:
    if not url:
        return ""
    return f'<a class="{cls}" href="{e(url)}" target="_blank" rel="noopener noreferrer">{e(text)} ↗</a>'


def render_area(area: dict, index: int, *, home=False) -> str:
    slug = quote(area["slug"], safe="-")
    href = ("/" if home else "") + f"research-area.html?area={slug}"
    if home:
        return f'<a class="topic-link" href="{e(href)}"><span>{e(area["name"])}</span><span aria-hidden="true">→</span></a>'
    return f'<a class="research-row" href="{e(href)}"><span class="num">{index:02d}</span><strong>{e(area["name"])}</strong><span class="arrow" aria-hidden="true">→</span></a>'


def render_person(person: dict, areas: dict[str, dict]) -> str:
    portrait = f'<img class="person-portrait" src="{e(person["portrait"])}" alt="{e(person.get("portrait_alt") or person["name"])}" width="110" height="138" loading="lazy">' if person.get("portrait") else ""
    topics = [areas[key] for key in person.get("research_areas", [])]
    topic_html = ""
    if topics:
        links = "".join(f'<li><a href="research-area.html?area={quote(area["slug"], safe="-")}">{e(area["name"])} <span aria-hidden="true">→</span></a></li>' for area in topics)
        topic_html = f'<div class="person-topics"><span class="person-topics-label">Research areas</span><ul>{links}</ul></div>'
    profile = external_anchor(person.get("canonical_url", ""), "Research profile", "profile-link")
    bio = f'<p class="person-bio">{e(person["bio"])}</p>'
    return f'<article class="person" id="{e(person["slug"])}">{portrait}<div><h3>{e(person["name"])}</h3><p class="eyebrow">{e(person["role"])}</p>{bio}{topic_html}{profile}</div></article>'


def render_people(people: list[dict], areas: dict[str, dict]) -> str:
    groups = [
        ("lead-researchers", "Lead researchers", [p for p in people if p["role"] == "Lead researcher"]),
        ("research-professionals", "Research professionals", [p for p in people if p["role"] == "Research professional"]),
        ("other-researchers", "Researchers", [p for p in people if p["role"] not in {"Lead researcher", "Research professional"}]),
    ]
    blocks = []
    for slug, title, members in groups:
        if not members and slug == "other-researchers":
            continue
        cards = "".join(render_person(person, areas) for person in members) or '<p class="note">Profiles will appear here after their details are verified.</p>'
        blocks.append(f'<div class="people-group" id="{slug}"><div class="eyebrow">Research team</div><h2>{e(title)}</h2><div class="people-list">{cards}</div></div>')
    return "".join(blocks)


def render_publication_card(pub: dict, area_names: dict[str, str]) -> str:
    authors = ", ".join(a if isinstance(a, str) else a["name"] for a in pub["authors"])
    topics = "".join(f'<span class="tag">{e(area_names[key])}</span>' for key in pub["topics"])
    return (f'<article class="publication" data-title="{e(pub["title"])}" data-authors="{e(authors)}" data-year="{pub["year"]}" data-type="{e(pub["type"])}" data-topics="{e(" ".join(pub["topics"]))}">'
            f'<div class="pub-year">{pub["year"]}</div><div><h3 class="pub-title"><a href="/publications/{quote(pub["slug"], safe="-")}/">{e(pub["title"])}</a></h3><p class="pub-authors">{e(authors)}</p>'
            f'<div class="pub-venue">{e(pub["type"])}{(" · " + e(pub["venue"])) if pub["venue"] else ""}</div><div class="pub-tags">{topics}</div></div>'
            f'<div class="pub-actions"><a class="text-link" href="/publications/{quote(pub["slug"], safe="-")}/">Abstract and details →</a></div></article>')


def render_news(item: dict) -> str:
    link = external_anchor(item.get("canonical_url", ""), "Read announcement")
    summary = f'<p>{e(item["summary"])}</p>'
    body = "".join(f'<p class="news-body">{e(line)}</p>' for line in item.get("body", "").splitlines() if line.strip())
    body_link = link or ""
    return (f'<article class="publication news-record" id="{e(item["slug"])}" data-year="{e(iso_day(item["date"])[:4])}" data-category="{e(item["category"])}" data-search="{e(item["title"] + " " + item["summary"] + " " + item["body"])}">'
            f'<div class="pub-year">{e(iso_day(item["date"])[:4])}</div><div><div class="eyebrow">{e(item["category"])} · {e(format_date(item["date"]))}</div><h3 class="pub-title">{e(item["title"])}</h3>{summary}{body}</div><div class="pub-actions">{body_link}</div></article>')


def render_seminar(item: dict, archived=False) -> str:
    event_date = f'{format_date(item["date"])} · {e(str(item["date"])[11:16]) if "T" in str(item["date"]) else ""} {e(item["timezone"])}'.strip()
    links = " ".join(x for x in (external_anchor(item.get("event_url", ""), "Event details"), external_anchor(item.get("recording_url", ""), "Watch recording")) if x)
    summary = f'{e(item["speaker"])} · {e(item["description"])}'
    if item.get("location"):
        summary += f' · {e(item["location"])}'
    return f'<article class="event-line seminar-record" id="{e(item["slug"])}"><div class="event-date">{event_date}</div><div><h3>{e(item["title"])}</h3><p>{summary}</p></div><div>{links}</div></article>'


def render_about(settings: dict) -> str:
    if not settings.get("published"):
        return '<div><div class="eyebrow">Research scope</div><h2>About information is under review.</h2><p class="note">Approved Center scope and collaboration details will appear here when provided.</p></div><aside><div class="split-label" id="contact"><div class="eyebrow">Contact</div><h2>Get in touch</h2></div><p class="note">A public contact will be added after it is verified.</p></aside>'
    about_text = settings.get("scope", "")
    research = settings.get("research_scope", "")
    collaboration = settings.get("collaboration", "")
    source = external_anchor(settings.get("source_url", ""), "Source")
    contact = optional_text(CONTENT / "settings/about.json", settings, "contact_email")
    contact_html = f'<p>For research, seminar, or collaboration enquiries:</p><a class="text-link" href="mailto:{e(contact)}">{e(contact)} →</a>' if contact else '<p class="note">A public contact will be added after it is verified.</p>'
    return f'<div><div class="eyebrow">Research scope</div><h2>{e(research) if research else "About the Center"}</h2><p>{e(about_text)}</p><div class="split-label"><div class="eyebrow">Collaboration</div><h2>Work with the Center</h2></div><p>{e(collaboration)}</p>{source}</div><aside><div class="split-label" id="contact"><div class="eyebrow">Contact</div><h2>Get in touch</h2></div>{contact_html}</aside>'



def replace_select_options(source: str, element_id: str, default_label: str, options: list[tuple[str, str]]) -> str:
    pattern = re.compile(r'(<select\b[^>]*\bid="' + re.escape(element_id) + r'"[^>]*>).*?(</select>)', re.S)
    found = pattern.search(source)
    if not found:
        raise BuildError(f"missing filter select #{element_id}")
    html_options = f'<option value="">{e(default_label)}</option>' + "".join(
        f'<option value="{e(value)}">{e(label)}</option>' for value, label in options
    )
    return source[:found.start()] + found.group(1) + html_options + found.group(2) + source[found.end():]


def replace_archive(source: str, aria_label: str, action: str, years: list[str], empty_note: str) -> str:
    pattern = re.compile(r'(<div class="archive-links" aria-label="' + re.escape(aria_label) + r'">).*?(</div>)', re.S)
    found = pattern.search(source)
    if not found:
        raise BuildError(f"missing archive list '{aria_label}'")
    content = "".join(f'<button type="button" onclick="{action}(\'{e(year)}\')">{e(year)}</button>' for year in years)
    content = content or f'<span class="note">{e(empty_note)}</span>'
    return source[:found.start()] + found.group(1) + content + found.group(2) + source[found.end():]

def replace_slot(source: str, name: str, value: str, path: Path) -> str:
    start = f"<!-- CMS_SLOT:{name}:START -->"
    end = f"<!-- CMS_SLOT:{name}:END -->"
    if source.count(start) != 1 or source.count(end) != 1:
        raise BuildError(f"{path.relative_to(ROOT)}: expected one balanced CMS slot '{name}'")
    return source.replace(start + source.split(start, 1)[1].split(end, 1)[0] + end, start + value + end, 1)


def minify_slots(remove_comments: str) -> str:
    return re.sub(r"<!-- CMS_SLOT:[a-z_]+:(?:START|END) -->", "", remove_comments)


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")


def page_entry(name: str, description: str, keywords: str, url: str, group: str) -> dict:
    return {"name": name, "description": description, "keywords": keywords, "url": url, "group": group}


def build() -> None:
    site_settings = load_json(CONTENT / "settings/site.json")
    if not isinstance(site_settings, dict):
        fail(CONTENT / "settings/site.json", "record", "expected a JSON object")
    about_settings = load_json(CONTENT / "settings/about.json")
    if not isinstance(about_settings, dict):
        fail(CONTENT / "settings/about.json", "record", "expected a JSON object")
    if not isinstance(about_settings.get("published", False), bool):
        fail(CONTENT / "settings/about.json", "published", "must be true or false")
    for key in ("center_name", "university", "campus_video_caption"):
        require_text(CONTENT / "settings/site.json", site_settings, key)
    video_id = require_text(CONTENT / "settings/site.json", site_settings, "campus_video_id")
    if not YOUTUBE_ID_RE.fullmatch(video_id):
        fail(CONTENT / "settings/site.json", "campus_video_id", "must be a valid 11-character YouTube ID")
    if about_settings.get("published"):
        for key in ("scope", "research_scope", "collaboration", "source_url", "verified_on"):
            require_text(CONTENT / "settings/about.json", about_settings, key)
        validate_url(CONTENT / "settings/about.json", "source_url", about_settings.get("source_url", ""))
        contact_email = optional_text(CONTENT / "settings/about.json", about_settings, "contact_email")
        if contact_email and not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", contact_email):
            fail(CONTENT / "settings/about.json", "contact_email", "must be a valid public email address")
    raw = {key: load_records(folder) for key, folder in COLLECTIONS.items()}
    data = validate_records(raw)
    areas_by_id = {area["slug"]: area for area in data["research_areas"]}
    area_names = {key: value["name"] for key, value in areas_by_id.items()}

    pages = load_json(CONTENT / "search-pages.json")
    if not isinstance(pages, list) or not all(isinstance(row, dict) for row in pages):
        fail(CONTENT / "search-pages.json", "records", "expected a list of page records")
    for row in pages:
        for key in ("name", "description", "keywords", "url", "group"):
            if not isinstance(row.get(key), str) or not row[key].strip():
                fail(CONTENT / "search-pages.json", key, "a non-empty value is required")
        if not row["url"].startswith("/"):
            fail(CONTENT / "search-pages.json", "url", "use an organization-root path")

    temp_root = Path(tempfile.mkdtemp(prefix=".pages-build-", dir=ROOT))
    site = temp_root / "site"
    site.mkdir(parents=True)
    try:
        shutil.copy2(ROOT / "index.html", site / "index.html")
        public_design = site / "design"
        public_design.mkdir()
        public_files = (
            "about.html", "homepage-concept.html", "news.html", "people.html",
            "publications.html", "research-area.html", "research.html", "seminars.html",
            "campus-video.js", "mobile-navigation.js", "research-people.js", "publications.js", "news.js", "site-concept.css",
        )
        for relative in public_files:
            shutil.copy2(ROOT / "design" / relative, public_design / relative)
        shutil.copytree(ROOT / "design" / "assets", public_design / "assets",
                         ignore=shutil.ignore_patterns("media-sources.json"))
        shutil.copytree(ROOT / "admin", site / "admin")

        # Static pages are the canonical templates; each record collection replaces only its marked content slot.
        replacements = {
            "index.html": {"home_heading": e(site_settings.get("hero_heading", "")) or None,
                            "home_summary": e(site_settings.get("hero_summary", "")) or None,
                            "homepage_areas": "".join(render_area(a, i, home=True) for i, a in enumerate(data["research_areas"], 1)) or '<p class="note">Verified research areas will appear here.</p>',
                            "video_caption": e(site_settings.get("campus_video_caption", "")) or None},
            "design/homepage-concept.html": {"home_heading": e(site_settings.get("hero_heading", "")) or None,
                            "home_summary": e(site_settings.get("hero_summary", "")) or None,
                            "homepage_areas": "".join(render_area(a, i, home=True) for i, a in enumerate(data["research_areas"], 1)) or '<p class="note">Verified research areas will appear here.</p>',
                            "video_caption": e(site_settings.get("campus_video_caption", "")) or None},
            "design/research.html": {"research_areas": "".join(render_area(a, i) for i, a in enumerate(data["research_areas"], 1)) or '<p class="note">Verified research areas will appear here.</p>'},
            "design/people.html": {"people_directory": render_people(data["people"], areas_by_id)},
            "design/publications.html": {"publication_list": "".join(render_publication_card(pub, area_names) for pub in data["publications"]) or '<p class="empty-state">No verified publications have been added yet.</p>'},
            "design/news.html": {"news_list": "".join(render_news(item) for item in data["news"]) or '<p class="empty-state">No approved announcements have been added yet.</p>'},
            "design/seminars.html": {"seminar_upcoming": "".join(render_seminar(item) for item in data["seminars"] if iso_day(item["date"]) >= date.today().isoformat()) or '<p class="note">Confirmed upcoming seminars will appear here.</p>',
                                      "seminar_archive": "".join(render_seminar(item, archived=True) for item in data["seminars"] if iso_day(item["date"]) < date.today().isoformat()) or '<p class="note">Confirmed past seminars will appear here.</p>'},
            "design/about.html": {"about_content": render_about(about_settings)},
        }
        for relpath, slots in replacements.items():
            path = site / relpath
            source = path.read_text(encoding="utf-8")
            for name, value in slots.items():
                if value is not None:
                    source = replace_slot(source, name, value, ROOT / relpath)
                else:
                    # Blank settings preserve the currently approved template copy.
                    source = replace_slot(source, name, source.split(f"<!-- CMS_SLOT:{name}:START -->", 1)[1].split(f"<!-- CMS_SLOT:{name}:END -->", 1)[0], ROOT / relpath)
            source = minify_slots(source)
            if relpath in {"index.html", "design/homepage-concept.html"}:
                source = re.sub(r'data-video-id="[^"]*"', f'data-video-id="{e(site_settings["campus_video_id"])}"', source, count=1)
            source = source.replace("UP Economics Research Center", e(site_settings.get("center_name", "UP Economics Research Center")))
            source = source.replace("Universidad Panamericana", e(site_settings.get("university", "Universidad Panamericana")))
            source = source.replace("Design preview · Illustrative content", e(site_settings.get("footer_note", "Design preview · Illustrative content")))
            path.write_text(source, encoding="utf-8")

        # Remove every fictional inline dataset from public output, retaining external shared scripts.
        for relpath, marker in (("design/publications.html", "demoPubs"), ("design/news.html", "const updates=")):
            path = site / relpath
            source = path.read_text(encoding="utf-8")
            source, count = re.subn(r"<script>(?:(?!</script>).)*" + re.escape(marker) + r"(?:(?!</script>).)*</script>", "", source, count=1, flags=re.S)
            if count != 1:
                raise BuildError(f"{relpath}: expected to remove the illustrative inline script containing {marker}")
            if relpath == "design/publications.html":
                source = re.sub(r"<p class=\"note\">Interface demonstration only:.*?</p>", "", source, count=1)
            else:
                source = re.sub(r"<p class=\"note\">Illustrative announcement records for interface review only\..*?</p>", "", source, count=1)
            if relpath == "design/publications.html":
                years = sorted({str(pub["year"]) for pub in data["publications"]}, reverse=True)
                topics = sorted({key for pub in data["publications"] for key in pub["topics"]})
                types = sorted({pub["type"] for pub in data["publications"]})
                source = replace_select_options(source, "pub-topic", "All topics", [(key, area_names[key]) for key in topics])
                source = replace_select_options(source, "pub-year", "All years", [(year, year) for year in years])
                source = replace_select_options(source, "pub-type", "All types", [(kind, kind) for kind in types])
                source = source.replace("Showing 6 illustrative records", f"Showing {len(data['publications'])} verified publications", 1)
                source = replace_archive(source, "Publication years", "browsePubYear", years, "Verified publication years will appear here.") if 'Publication years' in source else source
            else:
                years = sorted({iso_day(item["date"])[:4] for item in data["news"]}, reverse=True)
                categories = sorted({item["category"] for item in data["news"]})
                source = replace_select_options(source, "news-year", "All years", [(year, year) for year in years])
                source = replace_select_options(source, "news-type", "All updates", [(category, category) for category in categories])
                source = source.replace('aria-label="News years"', 'aria-label="News years"', 1)
                source = replace_archive(source, "News years", "browseNewsYear", years, "Approved news years will appear here.")
            path.write_text(source, encoding="utf-8")

        # Publish visitor-facing section pages at the repository root. Keep
        # styles, scripts, and media in design/ as implementation assets.
        route_pages = ("about", "news", "people", "publications", "research-area", "research", "seminars")
        for name in route_pages:
            source = (site / "design" / f"{name}.html").read_text(encoding="utf-8")
            source = source.replace('href="site-concept.css"', 'href="/design/site-concept.css"')
            source = source.replace('href="homepage-concept.html"', 'href="/"')
            source = re.sub(r'(src|href)="(campus-video|mobile-navigation|research-people|publications|news)\.js"', r'\1="/design/\2.js"', source)
            source = source.replace('src="assets/', 'src="/design/assets/')
            (site / f"{name}.html").write_text(source, encoding="utf-8")

        # Point homepage navigation at the new canonical section URLs.
        home_path = site / "index.html"
        home_source = home_path.read_text(encoding="utf-8")
        home_source = re.sub(r'href="design/([a-z-]+\.html(?:#[^"]*)?)"', r'href="\1"', home_source)
        home_path.write_text(home_source, encoding="utf-8")

        # Use approved content only in generated search and content feeds.
        people_feed = [{k: v for k, v in row.items() if not k.startswith("_")} for row in data["people"]]
        area_feed = [{k: v for k, v in row.items() if not k.startswith("_")} for row in data["research_areas"]]
        publication_feed = [{k: v for k, v in row.items() if not k.startswith("_")} for row in data["publications"]]
        news_feed = [{k: v for k, v in row.items() if not k.startswith("_")} for row in data["news"]]
        seminar_feed = [{k: v for k, v in row.items() if not k.startswith("_")} for row in data["seminars"]]
        for name, value in (("people.json", people_feed), ("research-areas.json", area_feed), ("publications.json", publication_feed), ("news.json", news_feed), ("seminars.json", seminar_feed)):
            write_json(site / name, value)

        search = list(pages)
        for person in data["people"]:
            search.append(page_entry(person["name"], person["bio"], " ".join(person.get("research_areas", [])), f'/people.html#{quote(person["slug"], safe="-")}', "People"))
        for area in data["research_areas"]:
            search.append(page_entry(area["name"], area["summary"], area["slug"], f'/research-area.html?area={quote(area["slug"], safe="-")}', "Research area"))
        for pub in data["publications"]:
            authors = ", ".join(a if isinstance(a, str) else a["name"] for a in pub["authors"])
            desc = pub["abstract"]
            search.append(page_entry(pub["title"], desc, f'{authors} {pub["year"]} {pub["type"]} {pub["venue"]} ' + " ".join(pub["topics"]), f'/publications/{quote(pub["slug"], safe="-")}/', "Publication"))
        for item in data["news"]:
            search.append(page_entry(item["title"], item["summary"], item.get("category", "News"), f'/news.html#{quote(item["slug"], safe="-")}', "News"))
        for item in data["seminars"]:
            search.append(page_entry(item["title"], item["description"], f'{item["speaker"]} {item["series"]} {item["date"]}', f'/seminars.html#{quote(item["slug"], safe="-")}', "Seminar"))
        write_json(site / "search-index.json", search)

        template_path = ROOT / "templates/publication-detail.html"
        template = template_path.read_text(encoding="utf-8")
        for pub in data["publications"]:
            author_html = ", ".join(e(a if isinstance(a, str) else a["name"]) for a in pub["authors"])
            topic_html = "".join(f'<a class="tag" href="/research-area.html?area={quote(key, safe="-")}">{e(area_names[key])}</a>' for key in pub["topics"])
            canonical_link = external_anchor(pub.get("canonical_url", ""), "View publisher page")
            pdf_url = pub.get("pdf") or pub.get("pdf_url")
            download_link = external_anchor(pdf_url, "Download paper (PDF)") if pdf_url else ""
            if not download_link:
                download_link = '<p class="note">A public full-text link has not been supplied.</p>'
            meta = " ".join([pub["type"], str(pub["year"]), pub["venue"], pub["abstract"]]).strip()[:250]
            replacements = {
                "__TITLE__": e(pub["title"]), "__YEAR__": str(pub["year"]), "__TYPE__": e(pub["type"]),
                "__VENUE__": e(pub["venue"]), "__AUTHORS__": author_html, "__ABSTRACT__": e(pub["abstract"]),
                "__TOPICS__": topic_html, "__CANONICAL_LINK__": canonical_link, "__DOWNLOAD_LINK__": download_link,
                "__META_DESCRIPTION__": e(meta), "__SLUG__": quote(pub["slug"], safe="-"),
            }
            output = template
            for token, value in replacements.items():
                output = output.replace(token, value)
            route = site / "publications" / pub["slug"] / "index.html"
            route.parent.mkdir(parents=True, exist_ok=True)
            route.write_text(output, encoding="utf-8")

        # Write metadata fields that remain public; source and validation-only values are not emitted as HTML.
        if OUT.exists():
            shutil.rmtree(OUT)
        shutil.move(str(site), str(OUT))
        print(f"Built {len(search)} search records, {len(data['publications'])} publication pages, and {len(data['people'])} people in {OUT.relative_to(ROOT)}/")
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)


def main() -> int:
    try:
        build()
        return 0
    except BuildError as exc:
        print(f"Site build error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
