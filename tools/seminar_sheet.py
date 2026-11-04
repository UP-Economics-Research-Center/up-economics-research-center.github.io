#!/usr/bin/env python3
"""Import explicitly published seminar rows; never write CMS records or commit data."""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import re
import sys
from datetime import date, datetime, timezone
from http.client import HTTPException
from pathlib import Path
from urllib.error import URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "content/settings/seminar-sheet.json"
FEED = ROOT / ".seminar-import/feed.json"
TIMEZONE = "America/Mexico_City"
MAX_BYTES = 2_000_000
PLACEHOLDER = re.compile(r"^(espacio disponible|available(?: slot)?|tbd|por confirmar|tentative|tentativo)\b", re.I)
FORMATS = {"": "", "por confirmar": "", "presencial": "in_person", "en línea": "online", "híbrida": "hybrid"}


class SheetError(ValueError):
    pass


def settings():
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    for key in ("csv_url", "schedule_url", "deployed_feed_url"):
        parsed = urlsplit(config[key])
        if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password:
            raise SheetError(f"{key} must be an HTTPS URL")
    return config


def read_url(url):
    request = Request(url, headers={"User-Agent": "UP-ERC-seminar-schedule/1.0", "Cache-Control": "no-cache"})
    try:
        with urlopen(request, timeout=30) as response:
            advertised = response.headers.get("Content-Length")
            expected = int(advertised) if advertised is not None else None
            if expected is not None and (expected < 0 or expected > MAX_BYTES):
                raise SheetError("response exceeds the schedule size limit or has an invalid length")
            raw = response.read(MAX_BYTES + 1)
            if len(raw) > MAX_BYTES:
                raise SheetError("response exceeds the schedule size limit")
            if expected is not None and len(raw) != expected:
                raise SheetError("incomplete schedule response")
            return raw.decode("utf-8-sig")
    except HTTPException as exc:
        raise SheetError(f"incomplete or invalid HTTP response: {type(exc).__name__}") from exc


def valid_day(value):
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise SheetError("Fecha must use YYYY-MM-DD")
    try:
        date.fromisoformat(value)
    except ValueError as exc:
        raise SheetError(f"invalid Fecha: {value}") from exc
    return value


def validate_https(value, label):
    if not isinstance(value, str):
        raise SheetError(f"{label} must be text")
    if not value:
        return
    try:
        parsed = urlsplit(value)
        parsed.port
        valid = parsed.scheme == "https" and parsed.hostname and not parsed.username and not parsed.password
    except ValueError:
        valid = False
    if not valid or any(char.isspace() or ord(char) < 32 for char in value):
        raise SheetError(f"{label} must be a valid HTTPS URL")


def validate_presentation(item):
    if not isinstance(item, dict):
        raise SheetError("invalid presentation")
    fields = ("speaker", "institution", "title_es", "title_en", "description_es", "description_en",
              "details_es", "details_en", "location", "campus", "time")
    for key in fields:
        if key in item and not isinstance(item[key], str):
            raise SheetError(f"{key} must be text")
    if not any(item.get(key, "").strip() for key in ("speaker", "title_es", "title_en")):
        raise SheetError("a published presentation needs a speaker or title")
    if not item.get("speaker") and any(PLACEHOLDER.search(item.get(key, "")) for key in ("title_es", "title_en")):
        raise SheetError("available slots cannot be published")
    mode = item.get("format", "")
    if not isinstance(mode, str) or mode not in {"", "in_person", "online", "hybrid"}:
        raise SheetError("invalid presentation format")
    if item.get("time") and not re.fullmatch(r"(?:[01]\d|2[0-3]):[0-5]\d", item["time"]):
        raise SheetError("Hora (CDMX) must use HH:MM in 24-hour format")
    if "duration" in item and (type(item["duration"]) is not int or not 1 <= item["duration"] <= 1440):
        raise SheetError("Duración (min) must be an integer from 1 to 1440")
    for key in ("online_url", "rsvp_url", "material_url"):
        validate_https(item.get(key, ""), key)


def presentation_id(parent, item):
    identity = "\n".join((parent, item.get("speaker", ""), item.get("title_es") or item.get("title_en", ""), item.get("time", "")))
    return "talk-" + hashlib.sha256(identity.encode("utf-8")).hexdigest()[:20]


def parse_csv(text, config):
    try:
        rows = list(csv.reader(io.StringIO(text, newline=""), strict=True))
    except csv.Error as exc:
        raise SheetError(f"invalid CSV: {exc}") from exc
    names = tuple(config["columns"].values())
    candidates = [index for index, row in enumerate(rows[:10])
                  if all([field.strip() for field in row].count(name) == 1 for name in names)]
    if len(candidates) != 1:
        raise SheetError("expected one complete schedule header within the first 10 rows")
    header_index = candidates[0]
    headers = [field.strip() for field in rows[header_index]]
    columns = {}
    for key, name in config["columns"].items():
        if headers.count(name) != 1:
            raise SheetError(f"expected exactly one {name!r} column on row {header_index + 1}")
        columns[key] = headers.index(name)
    entries = []
    identities_by_day = {}
    # Unpublished rows still own their existing session identity. Replacing a
    # presentation must not change the date's anchor when the old row is unchecked.
    for values in rows[header_index + 1:]:
        day = values[columns["date"]].strip() if len(values) > columns["date"] else ""
        source_id = values[columns["session_id"]].strip() if len(values) > columns["session_id"] else ""
        if not source_id or not re.fullmatch(r"sheet-(?:[a-f0-9]{20}|day-\d{4}-\d{2}-\d{2})", source_id):
            continue
        try:
            valid_day(day)
        except SheetError:
            continue
        identities_by_day.setdefault(day, set()).add(source_id)
    for number, values in enumerate(rows[header_index + 1:], header_index + 2):
        def cell(key):
            index = columns[key]
            return values[index].strip() if index < len(values) else ""
        published = cell("published").upper()
        if published in ("", "FALSE"):
            continue
        if published != "TRUE":
            raise SheetError(f"row {number}: Publicar must be a checkbox")
        try:
            day = valid_day(cell("date"))
            item = {key: cell(key) for key in columns if key not in {"published", "date", "session_id", "duration", "format"} and cell(key)}
            mode = cell("format").casefold()
            if mode not in FORMATS:
                raise SheetError("Modalidad must be Presencial, En línea, Híbrida or Por confirmar")
            if FORMATS[mode]:
                item["format"] = FORMATS[mode]
            if cell("duration"):
                if not re.fullmatch(r"[0-9]+", cell("duration")):
                    raise SheetError("Duración (min) must be an integer")
                item["duration"] = int(cell("duration"))
            validate_presentation(item)
            source_id = cell("session_id")
            if source_id:
                if not re.fullmatch(r"sheet-(?:[a-f0-9]{20}|day-\d{4}-\d{2}-\d{2})", source_id):
                    raise SheetError("invalid ID de sesión")
            entries.append((day, item))
        except SheetError as exc:
            raise SheetError(f"row {number}: {exc}") from exc
    sessions = {}
    for day, item in entries:
        existing_ids = identities_by_day.get(day, set())
        if len(existing_ids) > 1:
            raise SheetError("presentations on the same date must share ID de sesión")
        identifier = next(iter(existing_ids), "sheet-day-" + day)
        if identifier in sessions and sessions[identifier]["date"] != day:
            raise SheetError("one ID de sesión cannot refer to different dates")
        parent = sessions.setdefault(identifier, {"id": identifier, "date": day, "presentations": []})
        item["id"] = presentation_id(identifier, item)
        if any(existing["id"] == item["id"] for existing in parent["presentations"]):
            raise SheetError("duplicate presentation; give repeated talks their actual start times")
        parent["presentations"].append(item)
    for parent in sessions.values():
        parent["presentations"].sort(key=lambda item: item.get("time") or "99:99")
    return {
        "schema_version": 2,
        "source_url": config["schedule_url"],
        "csv_url": config["csv_url"],
        "timezone": TIMEZONE,
        "last_successful_refresh": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "sessions": sorted(sessions.values(), key=lambda item: (item["date"], item["id"])),
    }


def validate_feed(feed, config):
    if not isinstance(feed, dict) or feed.get("schema_version") != 2 or feed.get("timezone") != TIMEZONE:
        raise SheetError("unsupported seminar feed")
    if feed.get("csv_url") != config["csv_url"] or feed.get("source_url") != config["schedule_url"]:
        raise SheetError("feed belongs to a different schedule")
    try:
        refreshed = datetime.fromisoformat(feed["last_successful_refresh"])
        if refreshed.tzinfo is None or refreshed > datetime.now(timezone.utc):
            raise ValueError()
    except (KeyError, TypeError, ValueError) as exc:
        raise SheetError("invalid last successful refresh timestamp") from exc
    if not isinstance(feed.get("sessions"), list):
        raise SheetError("feed must contain a sessions list (which may be empty)")
    seen = set()
    seen_days = set()
    for item in feed["sessions"]:
        if not isinstance(item, dict):
            raise SheetError("invalid session record")
        day = valid_day(item.get("date"))
        identifier = item.get("id")
        if not isinstance(identifier, str) or not re.fullmatch(r"sheet-(?:[a-f0-9]{20}|day-\d{4}-\d{2}-\d{2})", identifier) or identifier in seen or day in seen_days:
            raise SheetError("invalid or duplicate session ID/date")
        seen.add(identifier)
        seen_days.add(day)
        presentations = item.get("presentations")
        if not isinstance(presentations, list) or not presentations:
            raise SheetError("session needs at least one presentation")
        for presentation in presentations:
            validate_presentation(presentation)
            child_id = presentation_id(identifier, presentation)
            if presentation.get("id") != child_id or child_id in seen:
                raise SheetError("invalid or duplicate presentation ID")
            seen.add(child_id)
    return feed


def load_feed(path=FEED):
    try:
        return validate_feed(json.loads(path.read_text(encoding="utf-8")), settings())
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise SheetError(f"No valid seminar feed at {path}; run python3 tools/seminar_sheet.py before building: {exc}") from exc


def mexico_day():
    return datetime.now(ZoneInfo(TIMEZONE)).date().isoformat()


def split_sessions(sessions, today=None):
    today = today or mexico_day()
    upcoming = sorted((item for item in sessions if item["date"][:10] >= today), key=lambda item: (item["date"][:10], item.get("id", item.get("slug", ""))))
    past = sorted((item for item in sessions if item["date"][:10] < today), key=lambda item: (item["date"][:10], item.get("id", item.get("slug", ""))), reverse=True)
    return upcoming, past


def report(message, level="warning"):
    # Escape Actions command payloads: spreadsheet values must not create workflow commands.
    safe = message.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
    print(f"::{level}::{safe}" if os.environ.get("GITHUB_ACTIONS") else f"{level}: {message}", file=sys.stderr)


def refresh(output, csv_file=None, fallback_file=None):
    config = settings()
    try:
        text = csv_file.read_text(encoding="utf-8-sig") if csv_file else read_url(config["csv_url"])
        feed = validate_feed(parse_csv(text, config), config)
        status = "Refreshed seminar schedule from Google Sheets."
    except (OSError, URLError, ValueError, KeyError, TypeError) as exc:
        report(f"Seminar refresh failed: {exc}. Trying the last successfully deployed feed.")
        try:
            raw = fallback_file.read_text(encoding="utf-8") if fallback_file else read_url(config["deployed_feed_url"])
            feed = validate_feed(json.loads(raw), config)
        except (OSError, URLError, ValueError, KeyError, TypeError) as fallback_exc:
            raise SheetError(f"Initial activation blocked: no valid deployed seminar feed. {fallback_exc}") from fallback_exc
        status = "Using last successfully deployed seminar feed (refresh failed); retained timestamp: " + feed["last_successful_refresh"]
        report(status)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(".tmp")
    temporary.write_text(json.dumps(feed, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(output)
    print(status)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as summary:
            summary.write("\n### Seminar schedule\n\n" + status + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=FEED)
    parser.add_argument("--csv-file", type=Path, help="Inspect an already downloaded CSV without a network fetch")
    parser.add_argument("--fallback-file", type=Path, help="Inspect recovery using a previously deployed feed")
    args = parser.parse_args()
    try:
        refresh(args.output, args.csv_file, args.fallback_file)
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        report(str(exc), "error")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
