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
        raise SheetError("Event date must use YYYY-MM-DD")
    try:
        date.fromisoformat(value)
    except ValueError as exc:
        raise SheetError(f"invalid Event date: {value}") from exc
    return value


def session_id(day, agenda):
    # Deterministic across builds and spreadsheet reordering, independent of row numbers.
    digest = hashlib.sha256((day + "\n" + agenda).encode("utf-8")).hexdigest()[:20]
    return "sheet-" + digest


def validate_participation(item):
    mode = item.get("format", "")
    if not isinstance(mode, str) or mode not in {"", "in_person", "online", "hybrid"}:
        raise SheetError("invalid session format")
    for key in ("location", "online_url"):
        if key in item and not isinstance(item[key], str):
            raise SheetError(f"{key} must be text")
    if item.get("location") and mode not in {"in_person", "hybrid"}:
        raise SheetError("Salón / auditorio requires Presencial or Híbrida")
    if item.get("online_url"):
        if mode not in {"online", "hybrid"}:
            raise SheetError("Enlace de conexión requires En línea or Híbrida")
        url = item["online_url"]
        parsed = urlsplit(url)
        if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password or any(char.isspace() or ord(char) < 32 for char in url):
            raise SheetError("Enlace de conexión must be a valid HTTPS URL")


def parse_csv(text, config):
    try:
        rows = list(csv.reader(io.StringIO(text, newline=""), strict=True))
    except csv.Error as exc:
        raise SheetError(f"invalid CSV: {exc}") from exc
    header_index = config["header_row"] - 1
    if len(rows) <= header_index:
        raise SheetError("missing schedule header row")
    headers = [field.strip() for field in rows[header_index]]
    required = (config["agenda_header"], config["original_date_header"], "Event date", "Show on website")
    for name in required:
        if headers.count(name) != 1:
            raise SheetError(f"expected exactly one {name!r} column on row {header_index + 1}")
    columns = {name: headers.index(name) for name in required}
    participation_columns = {}
    for key in ("format", "location", "online_url"):
        header = config[key + "_header"]
        if headers.count(header) > 1:
            raise SheetError(f"duplicate {header!r} column")
        if header in headers:
            participation_columns[key] = headers.index(header)
    duration_index = 0
    for letter in config["duration_column"]:
        duration_index = duration_index * 26 + ord(letter) - ord("A") + 1
    duration_index -= 1
    sessions = []
    seen = set()
    for number, values in enumerate(rows[header_index + 1:], header_index + 2):
        def cell(index):
            return values[index].strip() if index < len(values) else ""
        published = cell(columns["Show on website"]).upper()
        if published in ("", "FALSE"):
            continue
        if published != "TRUE":
            raise SheetError(f"row {number}: Show on website must be a checkbox (TRUE/FALSE)")
        agenda = cell(columns[config["agenda_header"]])
        original_date = cell(columns[config["original_date_header"]])
        if not agenda or PLACEHOLDER.search(agenda) or "?" in original_date or re.search(r"tentativ|por confirmar|tbd", original_date, re.I):
            raise SheetError(f"row {number}: checked row needs a named, confirmed session")
        try:
            day = valid_day(cell(columns["Event date"]))
        except SheetError as exc:
            raise SheetError(f"row {number}: {exc}") from exc
        identifier = session_id(day, agenda)
        if identifier in seen:
            raise SheetError(f"row {number}: duplicate session")
        seen.add(identifier)
        item = {"id": identifier, "date": day, "title": agenda.splitlines()[0], "agenda": agenda}
        duration = cell(duration_index)
        if duration:
            item["duration"] = duration
        for key, index in participation_columns.items():
            value = cell(index)
            if key == "format":
                if value.casefold() not in FORMATS:
                    raise SheetError(f"row {number}: Modalidad must be Presencial, En línea, Híbrida or Por confirmar")
                value = FORMATS[value.casefold()]
            if value:
                item[key] = value
        try:
            validate_participation(item)
        except SheetError as exc:
            raise SheetError(f"row {number}: {exc}") from exc
        sessions.append(item)
    return {
        "schema_version": 1,
        "source_url": config["schedule_url"],
        "csv_url": config["csv_url"],
        "timezone": TIMEZONE,
        "last_successful_refresh": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "sessions": sorted(sessions, key=lambda item: (item["date"], item["id"])),
    }


def validate_feed(feed, config):
    if not isinstance(feed, dict) or feed.get("schema_version") != 1 or feed.get("timezone") != TIMEZONE:
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
    for item in feed["sessions"]:
        if not isinstance(item, dict):
            raise SheetError("invalid session record")
        day = valid_day(item.get("date"))
        for key in ("title", "agenda"):
            if not isinstance(item.get(key), str) or not item[key].strip():
                raise SheetError(f"session needs {key}")
        if PLACEHOLDER.search(item["agenda"]) or item["title"] != item["agenda"].splitlines()[0]:
            raise SheetError("feed contains an unnamed or inconsistent session")
        if "duration" in item and not isinstance(item["duration"], str):
            raise SheetError("duration must be text")
        validate_participation(item)
        identifier = session_id(day, item["agenda"])
        if item.get("id") != identifier or identifier in seen:
            raise SheetError("invalid or duplicate session ID")
        seen.add(identifier)
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
