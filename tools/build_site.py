#!/usr/bin/env python3
"""Build the GitHub Pages artifact from approved editorial JSON records."""
from __future__ import annotations

import html
import json
import re
import shutil
import sys
import tempfile
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.parse import quote, urlparse
from site_locales import generate_languages, LocaleError
from media_dimensions import image_dimensions

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
    "media": "media",
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


def validate_day(path, key, value):
    if not value:
        return
    try:
        if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            raise ValueError()
        parsed = date.fromisoformat(value)
        if parsed > datetime.now(timezone.utc).date():
            raise ValueError()
    except ValueError:
        fail(path, key, "use a real YYYY-MM-DD date, not in the future")


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
        row["display_name"] = optional_text(path, row, "display_name") or row["name"]
        require_text(path, row, "role")
        require_text(path, row, "bio")
        row["source_url"] = validate_url(path, "source_url", row.get("source_url", ""), optional=True)
        require_text(path, row, "verified_on")
        row["portrait"] = local_asset(path, "portrait", row.get("portrait", ""), optional=True) if row.get("portrait") else ""
        crop = row.get("portrait_crop")
        if crop:
            if not isinstance(crop, dict):
                fail(path, "portrait_crop", "expected a crop rectangle in percentages")
            for key in ("left", "top", "width", "height"):
                value = crop.get(key)
                if isinstance(value, bool) or not isinstance(value, (int, float)) or not 0 <= value <= 100:
                    fail(path, "portrait_crop", "use percentages between 0 and 100")
            if crop["width"] <= 0 or crop["height"] <= 0 or crop["left"] + crop["width"] > 100.01 or crop["top"] + crop["height"] > 100.01:
                fail(path, "portrait_crop", "the crop must fit inside the original photograph")
        row["canonical_url"] = validate_url(path, "canonical_url", row.get("canonical_url", ""), optional=True)
        row["personal_website"] = validate_url(path, "personal_website", row.get("personal_website", ""), optional=True)
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
        require_text(path, row, "overview")
        row["source_url"] = validate_url(path, "source_url", row.get("source_url", ""), optional=True)
        require_text(path, row, "verified_on")
        projects = row.get("projects", [])
        if not isinstance(projects, list):
            fail(path, "projects", "expected a list of project records")
        for project in projects:
            if not isinstance(project, dict):
                fail(path, "projects", "each project must be an object")
            for key in ("title", "summary"):
                if not isinstance(project.get(key), str) or not project[key].strip():
                    fail(path, "projects", f"each project needs a non-empty {key}")
            project["image_fit"] = project.get("image_fit") or "cover"
            if project["image_fit"] not in ("cover", "contain"):
                fail(path, "projects.image_fit", "choose cover for photographs or contain for complete diagrams")
            project["image_focus"] = project.get("image_focus") or "center"
            if project["image_focus"] not in ("top", "center", "bottom"):
                fail(path, "projects.image_focus", "choose top, center or bottom")
            researchers = project.get("researchers", [])
            if not isinstance(researchers, list) or not all(isinstance(item, str) and item.strip() for item in researchers):
                fail(path, "projects", "researchers must be a list of names")
        row["projects"] = projects
        members = row.get("people", [])
        if not isinstance(members, list) or not all(isinstance(item, str) for item in members):
            fail(path, "people", "expected a list of researcher slugs")
        missing = [item for item in members if item not in people]
        if missing:
            fail(path, "people", "unknown or unpublished researcher ID(s): " + ", ".join(missing))
        row["people"] = members

    types = {"Journal article", "Working paper", "Book", "Book chapter", "Policy brief", "Conference paper", "Case study", "Other"}
    for row in data["publications"]:
        path = row.pop("_path")
        for key in ("title", "abstract", "type", "verified_on"):
            require_text(path, row, key)
        row["source_url"] = validate_url(path, "source_url", row.get("source_url", ""), optional=True)
        row["title_language"] = row.get("title_language", "en")
        if row["title_language"] not in ("en", "es"):
            fail(path, "title_language", "choose en (English) or es (Spanish) for the original title")
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
        validate_day(path, "publication_date", row.get("publication_date", ""))
        row["publication_date_source_url"] = validate_url(path, "publication_date_source_url", row.get("publication_date_source_url", ""), optional=True)
        row["isbn"] = optional_text(path, row, "isbn")

    for collection in ("news", "seminars"):
        for row in data[collection]:
            path = row.pop("_path")
            required = ("title", "summary", "verified_on") if collection == "news" else ("title", "series", "speaker", "date", "timezone", "description", "verified_on")
            for key in required:
                require_text(path, row, key)
            row["source_url"] = validate_url(path, "source_url", row.get("source_url", ""), optional=True)
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

    for row in data["media"]:
        path = row.pop("_path")
        for key in ("title", "title_es", "summary", "summary_es", "type", "outlet", "verified_on"):
            require_text(path, row, key)
        if row["type"] not in {"Blog", "Podcast", "Article", "Interview", "Video", "Other"}:
            fail(path, "type", "choose a supported media type")
        for key in ("canonical_url", "source_url"):
            row[key] = validate_url(path, key, row.get(key, ""))
        validate_day(path, "date", row.get("date", ""))
        authors = row.get("authors", [])
        if not isinstance(authors, list) or not all(isinstance(name, str) and name.strip() for name in authors):
            fail(path, "authors", "use a list of verified author names")
        if row.get("person_id") and row["person_id"] not in people:
            fail(path, "person_id", "choose a published researcher")
        if row.get("publication_id") and row["publication_id"] not in {p["slug"] for p in data["publications"]}:
            fail(path, "publication_id", "choose a published publication")
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


def image_html(record: dict, cls: str = "research-photo") -> str:
    if not record.get("image"):
        return ""
    size = image_dimensions(str(ROOT / record["image"].lstrip("/")))
    dimensions = f' width="{size[0]}" height="{size[1]}"' if size else ""
    responsive = ""
    if "/area-photography/" in record["image"] and size:
        source = Path(record["image"])
        variants = [(source.with_name(source.stem + f"-{width}.webp").as_posix(), width) for width in (480, 960) if width < size[0]]
        variants.append((record["image"], size[0]))
        responsive = ' srcset="' + ', '.join(e(url) + ' ' + str(width) + 'w' for url, width in variants) + '" sizes="(max-width:700px) calc(100vw - 40px), (max-width:1000px) 46vw, 640px"'
    return f'<img class="{cls}" src="{e(record["image"])}" alt="{e(record.get("image_alt", ""))}"{dimensions}{responsive} loading="lazy">'


def render_area(area: dict, index: int, *, home=False) -> str:
    href = f'/research-area.html?area={quote(area["slug"], safe="-")}'
    if home:
        return f'<a class="topic-link" href="{e(href)}"><span>{e(area["name"])}</span><span aria-hidden="true">→</span></a>'
    visual = area if area.get("image") else (area.get("banner") or area)
    art = f'<span class="research-art" data-area="{e(area["slug"])}">{image_html(visual)}</span>'
    return f'<a class="research-row" href="{e(href)}">{art}<strong>{e(area["name"])}</strong><span class="arrow" aria-hidden="true">→</span></a>'


def render_person(person: dict, areas: dict[str, dict], publication_authors: set[str]) -> str:
    portrait = f'<img class="person-portrait" src="{e(person["portrait"])}" alt="{e(person.get("portrait_alt") or person["name"])}" width="240" height="300" loading="lazy">' if person.get("portrait") else ""
    if portrait and person.get("portrait_crop"):
        crop = person["portrait_crop"]
        style = f'--crop-width:{10000 / crop["width"]:.4f}%;--crop-height:{10000 / crop["height"]:.4f}%;--crop-left:{-100 * crop["left"] / crop["width"]:.4f}%;--crop-top:{-100 * crop["top"] / crop["height"]:.4f}%'
        portrait = f'<div class="portrait-frame" style="{style}">{portrait}</div>'
    topics = [area for key, area in areas.items() if key in person.get("research_areas", [])]
    topic_html = ""
    if topics:
        links = "".join(f'<li><a href="/research-area.html?area={quote(area["slug"], safe="-")}">{e(area["name"])} <span aria-hidden="true">→</span></a></li>' for area in topics)
        topic_html = f'<div class="person-topics"><span class="person-topics-label">Research areas</span><ul>{links}</ul></div>'
    profile = external_anchor(person.get("personal_website", ""), "Personal website", "profile-link")
    if person.get("canonical_url") and person["canonical_url"] != person.get("personal_website"):
        profile += external_anchor(person["canonical_url"], "Research profile", "profile-link")
    if person["slug"] in publication_authors:
        profile += f'<a class="profile-link" href="/publications.html?author={quote(person["slug"], safe="-")}">View publications</a>'
    return f'<article class="person" id="{e(person["slug"])}"><h3 class="person-name">{e(person["display_name"])}</h3><div class="person-visual">{portrait}{topic_html}</div><div class="person-copy"><p class="person-bio">{e(person["bio"])}</p>{profile}</div></article>'


def render_people(people: list[dict], areas: dict[str, dict], publications: list[dict]) -> str:
    publication_authors = {author["person_id"] for pub in publications for author in pub["authors"] if isinstance(author, dict) and author.get("person_id")}
    groups = [("lead-researchers", "Lead researchers", [p for p in people if p["role"] == "Lead researcher"]),
              ("research-professionals", "Research professionals", [p for p in people if p["role"] == "Research professional"]),
              ("other-researchers", "Researchers", [p for p in people if p["role"] not in {"Lead researcher", "Research professional"}])]
    return "".join(f'<div class="people-group" id="{slug}"><h2>{title}</h2><div class="people-list">' + "".join(render_person(person, areas, publication_authors) for person in members) + '</div></div>' for slug, title, members in groups if members)


def render_authors(pub: dict) -> str:
    up = [a for a in pub["authors"] if isinstance(a, dict) and a.get("person_id")]
    others = [a for a in pub["authors"] if not (isinstance(a, dict) and a.get("person_id"))]
    def names(authors):
        return ", ".join(
            f'<a href="/people.html#{quote(a["person_id"], safe="-")}">{e(a["name"])}</a>'
            if isinstance(a, dict) and a.get("person_id")
            else e(a if isinstance(a, str) else a["name"])
            for a in authors
        )
    if not up:
        return names(others)
    label = "UP researcher:" if len(up) == 1 else "UP researchers:"
    result = f'<span class="author-group-label">{label}</span> ' + names(up)
    if others:
        result += '<br><span class="coauthor-prefix">with</span> ' + names(others)
    return result


def recency_badge(pub):
    if not pub.get("publication_date") or not pub.get("publication_date_source_url"):
        return ""
    return f'<span class="publication-new" data-publication-date="{e(pub["publication_date"])}" data-publication-date-source="{e(pub["publication_date_source_url"])}" hidden>New</span>'


def render_media(item, people):
    day = f'<time datetime="{e(item["date"])}">{e(item["date"])}</time>' if item.get("date") else ""
    authors = f'<p>{e(", ".join(item.get("authors", [])))}</p>' if item.get("authors") else ""
    related = f'<a href="/publications/{e(item["publication_id"])}/">Related publication</a>' if item.get("publication_id") else ""
    person = f'<a href="/people.html#{e(item["person_id"])}">{e(people[item["person_id"]]["display_name"])}</a>' if item.get("person_id") else ""
    return f'<article class="publication" id="{e(item["slug"])}"><p class="pub-venue">{e(item["outlet"])} · {e(item["type"])} {day}</p><h2 class="pub-title"><a href="{e(item["canonical_url"])}">{e(item["title"])}</a></h2>{authors}<p>{e(item["summary"])}</p><div class="reference-media-links">{person}{related}</div></article>'


def render_policy_brief_panel(brief: dict | None) -> str:
    if not brief:
        return ""
    url = '/publications/' + quote(brief["slug"], safe="-") + '/'
    pdf = brief.get("pdf") or brief.get("pdf_url")
    download = external_anchor(pdf, "Download policy brief (PDF)") if pdf else ""
    return (f'<aside class="policy-brief-panel" aria-labelledby="policy-brief-heading"><p class="eyebrow">Policy brief</p>'
            f'<h2 id="policy-brief-heading"><a href="{e(url)}" lang="{brief["title_language"]}" translate="no">{e(brief["title"])}</a></h2>'
            f'<p>{brief["year"]}</p><a class="text-link" href="{e(url)}">Read policy brief →</a>{download}</aside>')


def render_publication_card(pub: dict, area_names: dict[str, str]) -> str:
    authors = ", ".join(a if isinstance(a, str) else a["name"] for a in pub["authors"])
    url = f'/publications/{quote(pub["slug"], safe="-")}/'
    language = pub["title_language"]
    person_ids = " ".join(dict.fromkeys(author["person_id"] for author in pub["authors"] if isinstance(author, dict) and author.get("person_id")))
    photo = f'<a class="paper-image" href="{e(url)}" lang="{language}" translate="no" aria-label="{e(pub["title"])}">{image_html({**pub, "image_alt": ""}, "paper-photo")}</a>' if pub.get("image") else ""
    brief_link = f'<a class="text-link" href="/publications/{e(pub["policy_brief"]["slug"])}/">Policy brief →</a>' if pub.get("policy_brief") else ""
    venue = pub["venue"] or pub["type"]
    return (f'<article class="publication paper-row {"has-image" if photo else ""}" data-title="{e(pub["title"])}" data-authors="{e(authors)}" data-person-ids="{e(person_ids)}" data-year="{pub["year"]}" data-type="{e(pub["type"])}" data-topics="{e(" ".join(pub["topics"]))}">'
            f'{photo}<div>{recency_badge(pub)}<h2 class="pub-title"><a lang="{language}" translate="no" href="{e(url)}">{e(pub["title"])}</a></h2><p class="pub-authors" translate="no">{render_authors(pub)}</p>'
            f'<div class="pub-venue"><span>{e(venue)}</span> · {pub["year"]}</div></div>'
            f'<div class="pub-actions"><a class="text-link" href="/publications/{quote(pub["slug"], safe="-")}/">Abstract and details →</a>{brief_link}</div></article>')


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


def render_seminar_information(settings: dict) -> str:
    description = f'<p>{e(settings["seminar_description"])}</p>' if settings.get("seminar_description") else ""
    schedule = "".join(f'<p>{e(settings[field])}</p>' for field in ("seminar_schedule", "seminar_schedule_note") if settings.get(field))
    return f'<div class="seminar-overview"><div>{description}</div><aside class="seminar-schedule"><h3>Format and schedule</h3>{schedule}</aside></div>'


def render_seminar_proposals(settings: dict) -> str:
    items = "".join(f'<li><h3>{e(item["label"])}</h3><p>{e(item["description"])}</p></li>' for item in settings.get("seminar_proposals", []))
    form = external_anchor(settings.get("seminar_form_url", ""), "Submit a proposal", "button")
    note = f'<p class="note">{e(settings["seminar_form_note"])}</p>' if settings.get("seminar_form_note") else ""
    return f'<div class="seminar-proposal-heading"><h2>Propose a session</h2>{form}</div><div class="seminar-proposal-action">{note}</div><ul class="seminar-proposal-types">{items}</ul>'


def render_scope(settings: dict) -> str:
    if not settings.get("published"):
        return '<p class="note">About information is under review.</p>'
    heading = f'<h2>{e(settings["research_scope"])}</h2>' if settings.get("research_scope") else ""
    return f'<div class="eyebrow">Research scope</div>{heading}<p>{e(settings.get("scope", ""))}</p><p>{e(settings.get("affiliation", ""))}</p>'


def render_about(settings: dict) -> str:
    if not settings.get("published"):
        return '<p class="note">About information is under review.</p>'
    address = "<br>".join(e(line) for line in settings.get("address", "").splitlines())
    note = f'<p class="note">{e(settings["editorial_note"])}</p>' if settings.get("editorial_note") else ""
    return (f'<div><div class="eyebrow">Collaboration</div><h2>Work with the Center</h2><p>{e(settings["collaboration"])}</p></div>'
            f'<aside id="contact"><div class="eyebrow">Contact</div><h2>Get in touch</h2><p>{e(settings.get("contact_intro", ""))}</p>'
            f'<a class="text-link" href="mailto:{e(settings.get("contact_email", ""))}">{e(settings.get("contact_email", ""))} →</a><address>{address}</address>{note}</aside>')


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
        for key in ("scope", "collaboration", "verified_on"):
            require_text(CONTENT / "settings/about.json", about_settings, key)
        about_settings["source_url"] = validate_url(CONTENT / "settings/about.json", "source_url", about_settings.get("source_url", ""), optional=True)
        contact_email = optional_text(CONTENT / "settings/about.json", about_settings, "contact_email")
        if contact_email and not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", contact_email):
            fail(CONTENT / "settings/about.json", "contact_email", "must be a valid public email address")
    raw = {key: load_records(folder) for key, folder in COLLECTIONS.items()}
    if site_settings.get("show_seminars", False):
        path = CONTENT / "settings/about.json"
        for field in ("seminar_description", "seminar_schedule", "seminar_schedule_note"):
            require_text(path, about_settings, field)
            require_text(path, about_settings, field + "_es")
        for field in ("seminar_form_url", "seminar_source_url"):
            about_settings[field] = validate_url(path, field, about_settings.get(field, ""))
        proposals = about_settings.get("seminar_proposals", [])
        if not isinstance(proposals, list) or not all(isinstance(item, dict) for item in proposals):
            fail(path, "seminar_proposals", "expected a list of proposal types")
        for item in proposals:
            for field in ("label", "label_es", "description", "description_es"):
                require_text(path, item, field)
    data = validate_records(raw)
    for collection in ("research_areas", "people"):
        for row in data[collection]:
            value = row.get("display_order", 999)
            if not isinstance(value, int) or isinstance(value, bool) or value < 1:
                fail(CONTENT / COLLECTIONS[collection] / (row["slug"] + ".json"), "display_order", "must be a positive integer")
        data[collection].sort(key=lambda row: (row.get("display_order", 999), row["name"]))
    for collection in ("research_areas", "publications"):
        for row in data[collection]:
            path = CONTENT / COLLECTIONS[collection] / (row["slug"] + ".json")
            row["image"] = local_asset(path, "image", row.get("image", ""), optional=True)
            for field in ("image_source_url", "image_license_url"):
                row[field] = validate_url(path, field, row.get(field, ""), optional=True)
            if row["image"]:
                require_text(path, row, "image_alt")
                require_text(path, row, "image_alt_es")
                require_text(path, row, "image_credit")
            if collection == "publications":
                status = row.get("image_rights_status") or "pending"
                if status not in ("pending", "licensed", "permission-confirmed"):
                    fail(path, "image_rights_status", "choose pending, licensed or permission-confirmed")
                row["image_rights_status"] = status
                row["image_rights_url"] = validate_url(path, "image_rights_url", row.get("image_rights_url", ""), optional=True)
                if row["image"] and status != "pending":
                    require_text(path, row, "image_rights_url")
                    if status == "licensed":
                        require_text(path, row, "image_license_url")
                        require_text(path, row, "image_license")
                elif row["image"]:
                    row["_withheld_image"] = row["image"]
                    row["image"] = ""
            if collection == "research_areas":
                for project in row["projects"]:
                    project["image"] = local_asset(path, "projects.image", project.get("image", ""), optional=True)
                    project["url"] = validate_url(path, "projects.url", project.get("url", ""), optional=True)
                    for field in ("image_source_url", "image_license_url"):
                        project[field] = validate_url(path, "projects." + field, project.get(field, ""), optional=True)
                    if project["image"]:
                        require_text(path, project, "image_alt_es")
                        require_text(path, project, "image_alt")
                        require_text(path, project, "image_credit")
                layout = row.get("layout", "standard")
                if layout not in {"standard", "original-reference"}:
                    fail(path, "layout", "choose standard or original-reference")
                if layout == "original-reference":
                    banner = row.get("banner")
                    team = row.get("reference_team", [])
                    features = row.get("publication_features", [])
                    if not isinstance(banner, dict) or not isinstance(team, list) or not isinstance(features, list):
                        fail(path, "layout", "the original layout needs a banner, team list and publication features list")
                    for member in team:
                        if not isinstance(member, dict) or member.get("person_id") not in {person["slug"] for person in data["people"]}:
                            fail(path, "reference_team", "choose a published researcher")
                    # Legacy area photographs remain in source history; public team data is people IDs only.
                    row["reference_team"] = [{"person_id": member["person_id"]} for member in team]
                    for feature in features:
                        if not isinstance(feature, dict) or feature.get("publication") not in {pub["slug"] for pub in data["publications"]}:
                            fail(path, "publication_features", "choose an approved publication")
                        require_text(path, feature, "description")
                        require_text(path, feature, "description_es")
                        links = feature.get("media_links", [])
                        if not isinstance(links, list) or not all(isinstance(item, dict) for item in links):
                            fail(path, "media_links", "expected a list of labeled links")
                        for item in links:
                            require_text(path, item, "label")
                            require_text(path, item, "label_es")
                            item["url"] = validate_url(path, "media_links.url", item.get("url", ""))
                    for record in [banner]:
                        record["image"] = local_asset(path, "reference image", record.get("image", ""))
                        for field in ("image_alt", "image_alt_es", "image_credit"):
                            require_text(path, record, field)
                        record["image_source_url"] = validate_url(path, "image_source_url", record.get("image_source_url", ""))
    # Publication records own the verified first page; area descriptions cannot override it.
    for area in data["research_areas"]:
        for feature in area.get("publication_features", []):
            for field in list(feature):
                if field.startswith("image"):
                    feature.pop(field)

    def add_image_dimensions(value):
        if isinstance(value, list):
            for item in value:
                add_image_dimensions(item)
        elif isinstance(value, dict):
            if value.get("image"):
                size = image_dimensions(str(ROOT / value["image"].lstrip("/")))
                if size:
                    value["image_width"], value["image_height"] = size
            for item in list(value.values()):
                if isinstance(item, (dict, list)):
                    add_image_dimensions(item)
    add_image_dimensions(data)

    # Visibility is editorial, separate from each record's approval status.
    for flag in ("show_working_papers", "show_policy_briefs"):
        if not isinstance(site_settings.get(flag, True), bool):
            fail(CONTENT / "settings/site.json", flag, "must be true or false")
    approved_publications = {pub["slug"]: pub for pub in data["publications"]}
    hidden_types = {kind for kind, flag in (("Working paper", "show_working_papers"), ("Policy brief", "show_policy_briefs")) if not site_settings.get(flag, True)}
    data["publications"] = sorted(
        (pub for pub in data["publications"] if pub["type"] not in hidden_types),
        key=lambda pub: (-pub["year"], pub["title"].casefold()),
    )
    publication_index = {pub["slug"]: pub for pub in data["publications"]}
    for pub in data["publications"]:
        path = CONTENT / "publications" / (pub["slug"] + ".json")
        brief_id = optional_text(path, pub, "policy_brief_id")
        pub["policy_brief_id"] = brief_id
        brief = approved_publications.get(brief_id) if brief_id else None
        if brief_id and (not brief or brief["type"] != "Policy brief" or brief_id == pub["slug"]):
            fail(path, "policy_brief_id", "choose another published Policy brief")
        if brief and brief_id in publication_index:
            pub["policy_brief"] = {key: brief.get(key, "") for key in ("slug", "title", "title_language", "year", "pdf", "pdf_url")}
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
            "media.html", "section-navigation.js", "site-motion.js", "publication-recency.js", "campus-video.js", "language.js", "mobile-navigation.js", "research-people.js", "publications.js", "news.js", "site-concept.css",
        )
        for relative in public_files:
            shutil.copy2(ROOT / "design" / relative, public_design / relative)
        shutil.copytree(ROOT / "design" / "assets", public_design / "assets",
                         ignore=shutil.ignore_patterns("media-sources.json", "juan-alvaro-source-2022.jpg"))
        # Retain source assets; omit withheld thumbnails unless another active record uses the file.
        active_media = {row.get("image") for row in data["publications"] + data["research_areas"]}
        active_media.update(person.get("portrait") for person in data["people"])
        active_media.update(project.get("image") for area in data["research_areas"] for project in area["projects"])
        active_media.update(area.get("banner", {}).get("image") for area in data["research_areas"])
        active_media.update("/" + str(site_settings.get(key, "")).lstrip("/") for key in ("featured_image", "campus_video_poster"))
        # Include unpublished/hidden records: changing visibility must not expose a pending asset.
        for _, pub in raw["publications"]:
            image = pub.get("image", "")
            if not isinstance(image, str) or pub.get("image_rights_status") in ("licensed", "permission-confirmed"):
                continue
            clean = image.strip().lstrip("/")
            if not clean or urlparse(image).scheme or ".." in Path(clean).parts:
                continue
            asset = (site / clean).resolve()
            if site.resolve() in asset.parents and "/" + clean not in active_media:
                asset.unlink(missing_ok=True)
        shutil.copytree(ROOT / "admin", site / "admin")
        for icon in ("favicon.svg", "favicon.ico", "apple-touch-icon.png"):
            shutil.copy2(ROOT / icon, site / icon)

        # Static pages are the canonical templates; each record collection replaces only its marked content slot.
        replacements = {
            "index.html": {"home_heading": e(site_settings.get("hero_heading", "")) or None,
                            "home_summary": e(site_settings.get("hero_summary", "")).replace("UPward", '<span class="up-emphasis">UP</span>ward') or None,
                            "homepage_areas": "".join(render_area(a, i, home=True) for i, a in enumerate(data["research_areas"], 1)) or '<p class="note">Verified research areas will appear here.</p>',
                            "video_caption": e(site_settings.get("campus_video_caption", "")) or None,
                            "home_scope": render_scope(about_settings),
                            "home_contact": render_about(about_settings)},
            "design/homepage-concept.html": {"home_heading": e(site_settings.get("hero_heading", "")) or None,
                            "home_summary": e(site_settings.get("hero_summary", "")).replace("UPward", '<span class="up-emphasis">UP</span>ward') or None,
                            "homepage_areas": "".join(render_area(a, i, home=True) for i, a in enumerate(data["research_areas"], 1)) or '<p class="note">Verified research areas will appear here.</p>',
                            "video_caption": e(site_settings.get("campus_video_caption", "")) or None,
                            "home_scope": render_scope(about_settings),
                            "home_contact": render_about(about_settings)},
            "design/research.html": {"research_areas": "".join(render_area(a, i) for i, a in enumerate(data["research_areas"], 1)) or '<p class="note">Verified research areas will appear here.</p>'},
            "design/media.html": {"media_list": "".join(render_media(item, {p["slug"]: p for p in data["people"]}) for item in data["media"])},
            "design/people.html": {"people_directory": render_people(data["people"], areas_by_id, data["publications"])},
            "design/publications.html": {"publication_list": "".join(render_publication_card(pub, area_names) for pub in data["publications"]) or '<p class="empty-state">No verified publications have been added yet.</p>'},
            "design/news.html": {"news_list": "".join(render_news(item) for item in data["news"]) or '<p class="empty-state">No approved announcements have been added yet.</p>'},
            "design/seminars.html": {"seminar_information": render_seminar_information(about_settings),
                                      "seminar_proposals": render_seminar_proposals(about_settings),
                                      "seminar_upcoming": "".join(render_seminar(item) for item in data["seminars"] if iso_day(item["date"]) >= date.today().isoformat()) or '<p class="note">Confirmed upcoming seminars will appear here.</p>',
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
                if "Working paper" in hidden_types:
                    source = re.sub(r'<a class="output-link" href="publications\.html\?type=Working%20paper">.*?</a>', '', source, flags=re.S)
                source = re.sub(r'data-video-id="[^"]*"', f'data-video-id="{e(site_settings["campus_video_id"])}"', source, count=1)
                source = re.sub(r'<img src="(?:design/)?assets/[^"]+" alt="[^"]*" width="\d+" height="\d+"', f'<img src="{e(site_settings["campus_video_poster"])}" alt="{e(site_settings["campus_video_poster_alt"])}" width="480" height="360"', source, count=1)
                source = re.sub(r'href="https://www\.youtube\.com/watch\?v=[A-Za-z0-9_-]{11}"', f'href="https://www.youtube.com/watch?v={e(site_settings["campus_video_id"])}"', source, count=1)
                source = re.sub(
                    r'(<button[^>]*class="film-play"[^>]*>.*?<strong>)[^<]+(</strong>)',
                    lambda match: match.group(1) + e(site_settings["campus_video_title"]) + match.group(2),
                    source, count=1, flags=re.S,
                )
                source = re.sub(r'aria-label="Play [^"]*"', f'aria-label="Play {e(site_settings["campus_video_title"])}"', source, count=1)
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
                topics = [area["slug"] for area in data["research_areas"] if any(area["slug"] in pub["topics"] for pub in data["publications"])]
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
        route_pages = ("about", "news", "people", "publications", "research-area", "research", "seminars", "media")
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
        for name, value in (("media.json", data["media"]), ("people.json", people_feed), ("research-areas.json", area_feed), ("publications.json", publication_feed), ("news.json", news_feed), ("seminars.json", seminar_feed)):
            write_json(site / name, value)

        search = list(pages)
        search.append(page_entry("Media", "Media", "BOLD blog podcast", "/media.html", "Media"))
        for item in data["media"]:
            search.append(page_entry(item["title"], item["summary"], item["outlet"] + " " + item["type"], '/media.html#' + item["slug"], "Media"))
        for person in data["people"]:
            search.append(page_entry(person["display_name"], person["bio"], person["name"] + " " + " ".join(person.get("research_areas", [])), f'/people.html#{quote(person["slug"], safe="-")}', "People"))
        for area in data["research_areas"]:
            search.append(page_entry(area["name"], area["summary"] + " " + area.get("overview", "") + " " + " ".join(p["title"] + " " + p["summary"] for p in area.get("projects", [])), area["slug"], f'/research-area.html?area={quote(area["slug"], safe="-")}', "Research area"))
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
            author_html = render_authors(pub)
            topic_html = "".join(f'<a class="tag" href="/research-area.html?area={quote(key, safe="-")}">{e(area_names[key])}</a>' for key in pub["topics"])
            canonical_link = external_anchor(pub.get("canonical_url", ""), "View book" if pub["type"] == "Book" else "View article", "button")
            pdf_url = pub.get("pdf") or pub.get("pdf_url")
            download_link = external_anchor(pdf_url, "Download paper (PDF)") if pdf_url else ""
            if not download_link:
                download_link = '<p class="note">A public full-text link has not been supplied.</p>'
            meta = " ".join([pub["type"], str(pub["year"]), pub["venue"], pub["abstract"]]).strip()[:250]
            replacements = {
                "__POLICY_BRIEF_LAYOUT__": " has-policy-brief" if pub.get("policy_brief") else "",
                "__POLICY_BRIEF__": render_policy_brief_panel(publication_index.get(pub.get("policy_brief_id", ""))),
                "__NEW__": recency_badge(pub), "__ISBN__": f'<p>ISBN {e(pub["isbn"])}</p>' if pub.get("isbn") else "",
                "__TITLE__": e(pub["title"]), "__TITLE_LANGUAGE__": pub["title_language"], "__YEAR__": str(pub["year"]), "__TYPE__": e(pub["type"]),
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

        # Paused sections stay editable in source, but emit no public pages or feeds.
        public_data = dict(data)
        for section in ("news", "seminars"):
            if site_settings.get("show_" + section, False):
                continue
            public_data[section] = []
            for relative in (f"{section}.html", f"design/{section}.html", f"{section}.json"):
                (site / relative).unlink(missing_ok=True)
            for page in site.rglob("*.html"):
                if "admin" in page.relative_to(site).parts:
                    continue
                source = page.read_text(encoding="utf-8")
                source = re.sub(r'<a\b[^>]*href="(?:[^"<>]*/)?' + section + r'\.html(?:[?#][^"]*)?"[^>]*>.*?</a>', "", source, flags=re.S)
                block = "home-note" if section == "news" else "home-seminars"
                source = re.sub(r'<section class="' + block + r'"[^>]*>.*?</section>', "", source, flags=re.S)
                page.write_text(source, encoding="utf-8")
        for page in site.rglob("*.html"):
            if "admin" in page.relative_to(site).parts:
                continue
            source = page.read_text(encoding="utf-8")
            if not site_settings.get("show_news", False) and not site_settings.get("show_seminars", False):
                source = source.replace("Find people, papers, research areas, seminars, and news.", "Find people, papers, and research areas.")
                source = source.replace("Try education, working papers, or seminars", "Try education, development, or working papers")
            elif not site_settings.get("show_news", False):
                source = source.replace("Find people, papers, research areas, seminars, and news.", "Find people, papers, research areas, and seminars.")
            if not site_settings.get("show_working_papers", True):
                source = source.replace("Try education, working papers, or seminars", "Try education, publications, or seminars")
                source = re.sub(r'<a class="output-link" href="[^"<>]*publications\.html\?type=Working%20paper">.*?</a>', "", source, flags=re.S)
                source = source.replace("Explore academic publications and work in progress by the Center’s researchers.", "Explore academic publications by the Center’s researchers.")
            page.write_text(source, encoding="utf-8")
        search = [row for row in search if not any(not site_settings.get("show_" + section, False) and re.search(r"/" + section + r"\.html(?:[?#]|$)", row["url"]) for section in ("news", "seminars"))]
        write_json(site / "search-index.json", search)
        generate_languages(site, public_data, site_settings, about_settings)

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
    except (BuildError, LocaleError) as exc:
        print(f"Site build error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
