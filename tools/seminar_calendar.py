"""Google Calendar links from confirmed sheet data; no accounts or mail service."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from urllib.parse import urlencode

from seminar_sheet import TIMEZONE

SITE_URL = "https://up-economics-research-center.github.io"


def seminar_text(item: dict, field: str, language: str):
    other = "en" if language == "es" else "es"
    return (item.get(field + "_" + language), language) if item.get(field + "_" + language) else (item.get(field + "_" + other, ""), other)


def calendar_event(day: str, item: dict, language: str):
    # Never turn an unconfirmed time into midnight or guess an ending.
    if not item.get("time") or not item.get("duration"):
        return None
    start = datetime.fromisoformat(day + "T" + item["time"]).replace(tzinfo=ZoneInfo(TIMEZONE))
    end = start + timedelta(minutes=item["duration"])
    prefix = "/es" if language == "es" else ""
    url = f'{SITE_URL}{prefix}/seminars.html#{item["id"]}'
    title = seminar_text(item, "title", language)[0] or item.get("speaker", "")
    labels = (
        {"speaker": "Ponente", "institution": "Institución", "online_url": "Acceso en línea",
         "rsvp_url": "Inscripción", "material_url": "Material"}
        if language == "es" else
        {"speaker": "Speaker", "institution": "Institution", "online_url": "Join online",
         "rsvp_url": "Registration", "material_url": "Material"}
    )
    details = [f'{label}: {item[key]}' for key, label in labels.items() if item.get(key)]
    for field in ("description", "details"):
        value = seminar_text(item, field, language)[0]
        if value:
            details.append(value)
    details.append(
        "Esta copia no se actualiza automáticamente. Consulta los cambios en:"
        if language == "es" else
        "This copy does not update automatically. Check for changes at:"
    )
    details.append(url)
    return {
        "title": title,
        "start": start.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
        "end": end.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
        "location": " · ".join(item[key] for key in ("location", "campus") if item.get(key)),
        "description": "\n\n".join(details),
        "url": url,
    }


def google_calendar_url(event: dict) -> str:
    return "https://calendar.google.com/calendar/render?" + urlencode({
        "action": "TEMPLATE",
        "text": event["title"],
        "dates": event["start"] + "/" + event["end"],
        "ctz": TIMEZONE,
        "details": event["description"],
        "location": event["location"],
    })
