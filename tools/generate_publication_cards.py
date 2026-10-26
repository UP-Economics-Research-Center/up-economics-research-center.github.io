#!/usr/bin/env python3
"""Generate original citation cards from CMS records; Pillow is authoring-only.

No publisher cover, logo, article screenshot, or generated factual text is used.
The static website build consumes the saved PNGs and does not import Pillow.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "design/assets/publications/bibliographic-cards"
REGISTER = ROOT / "docs/publication-card-assets-2026-10-26.json"
WIDTH, HEIGHT, LEFT, RIGHT = 1024, 1536, 54, 970
WINE = "#720b21"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

PUBLISHERS = {
    "Business and Society Review": "Wiley",
    "Journal of International Development": "Wiley",
    "International Journal of Educational Development": "Elsevier",
    "Land Use Policy": "Elsevier",
    "Food Policy": "Elsevier",
    "Regional Science Policy & Practice": "Wiley / Elsevier",
    "Computational Economics": "Springer Nature",
    "Economic Theory": "Springer Nature",
    "Reproductive Health": "BMC / Springer Nature",
    "Management Research: Journal of the Iberoamerican Academy of Management": "Emerald Publishing",
    "Emerald Emerging Markets Case Studies": "Emerald Publishing",
    "The Journal of Development Studies": "Taylor & Francis",
    "Academy of Management Global Proceedings, Mexico": "Academy of Management",
    "The World Bank Economic Review": "Oxford University Press",
    "Journal of Management and Financial Sciences": "SGH Warsaw School of Economics",
    "PLOS One": "PLOS",
    "PLOS Water": "PLOS",
    "PLOS Global Public Health": "PLOS",
}


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, face, max_width=RIGHT - LEFT):
    lines, line = [], ""
    for word in text.split():
        if face.getlength(word) > max_width:
            if line:
                lines.append(line)
                line = ""
            chunk = ""
            for char in word:
                if chunk and face.getlength(chunk + char) > max_width:
                    lines.append(chunk)
                    chunk = char
                else:
                    chunk += char
            line = chunk
        elif line and face.getlength(line + " " + word) > max_width:
            lines.append(line)
            line = word
        else:
            line = (line + " " + word).strip()
    if line:
        lines.append(line)
    return lines


def draw_lines(draw, lines, face, y, leading, color="#111111"):
    for line in lines:
        draw.text((LEFT, y), line, font=face, fill=color, anchor="lt")
        y += leading
    return y


def create_card(pub):
    image = Image.new("RGB", (WIDTH, HEIGHT), "#ffffff")
    draw = ImageDraw.Draw(image)
    proceedings = pub["venue"].startswith("Academy of Management")
    label = "PROCEEDINGS" if proceedings else "JOURNAL"
    draw.text((LEFT, 65), label, font=font(SANS, 24), fill=WINE)
    for size in range(64, 31, -1):
        journal_font = font(SERIF_BOLD, size)
        journal_lines = wrap(pub["venue"], journal_font)
        if len(journal_lines) <= 2:
            break
    y = draw_lines(draw, journal_lines, journal_font, 111, size * 1.12, WINE)
    rule_y = y + 24
    draw.line((LEFT, rule_y, RIGHT, rule_y), fill=WINE, width=2)
    title_y = rule_y + 42
    names = [a["name"] if isinstance(a, dict) else a for a in pub["authors"]]
    for title_size in range(86, 37, -1):
        author_size = max(25, min(37, int(title_size * .48)))
        title_font, author_font = font(SERIF_BOLD, title_size), font(SANS, author_size)
        title_lines = wrap(pub["title"], title_font)
        author_lines = [line for name in names for line in wrap(name, author_font)]
        total = len(title_lines) * title_size * 1.10 + 38 + len(author_lines) * author_size * 1.25
        if title_y + total <= 1033:
            break
    if title_y + total > 1033:
        raise ValueError("Citation does not fit card: " + pub["slug"])
    y = draw_lines(draw, title_lines, title_font, title_y, title_size * 1.10)
    y = draw_lines(draw, author_lines, author_font, y + 38, author_size * 1.25)

    draw.text((LEFT, 1072), "PUBLISHER", font=font(SANS, 23), fill=WINE)
    publisher = PUBLISHERS[pub["venue"]]
    publisher_size = 49
    while font(SERIF, publisher_size).getlength(publisher) > RIGHT - LEFT:
        publisher_size -= 1
    draw.text((LEFT, 1110), publisher, font=font(SERIF, publisher_size), fill="#111111")
    draw.text((LEFT, 1173), str(pub["year"]), font=font(SANS, 32), fill="#111111")
    draw.line((LEFT, 1234, RIGHT, 1234), fill=WINE, width=2)
    doi = pub.get("doi", "")
    draw.text((LEFT, 1261), "DOI:" if doi else "REFERENCE:", font=font(SANS, 25), fill=WINE)
    value = doi or "Mexico 2020 · Conference proceedings"
    start = LEFT + (93 if doi else 180)
    value_size = 28
    while font(SANS, value_size).getlength(value) > RIGHT - start:
        value_size -= 1
    draw.text((start, 1261), value, font=font(SANS, value_size), fill="#111111")
    draw.text((LEFT, 1320), "SUGGESTED CITATION", font=font(SANS, 22), fill=WINE)
    citation = "; ".join(names) + f" ({pub['year']}). {pub['title']}. {pub['venue']}."
    if doi:
        citation += " https://doi.org/" + doi
    for citation_size in range(25, 13, -1):
        citation_font = font(SANS, citation_size)
        citation_lines = wrap(citation, citation_font)
        if 1357 + len(citation_lines) * citation_size * 1.26 <= 1480:
            break
    end = draw_lines(draw, citation_lines, citation_font, 1357, citation_size * 1.26)
    if end > 1480:
        raise ValueError("Citation footer does not fit: " + pub["slug"])
    draw.text((LEFT, 1503), "UP ERC · Bibliographic card / Ficha bibliográfica", font=font(SANS, 18), fill="#666666")
    path = OUTPUT / (pub["slug"] + ".png")
    image.save(path, optimize=True)
    return {
        "image": "/" + path.relative_to(ROOT).as_posix(),
        "image_is_thematic": False,
        "image_is_bibliographic": True,
        "image_alt": f"Center-created bibliographic card: {pub['title']}. {pub['venue']}, {pub['year']}.",
        "image_alt_es": f"Ficha bibliográfica creada por el Centro: {pub['title']}. {pub['venue']}, {pub['year']}.",
        "image_credit": "UP Economics Research Center · Original bibliographic design; not publisher artwork",
        "image_credit_es": "Centro de Investigación Económica UP · Diseño bibliográfico propio; no es una portada editorial",
        "image_source_url": pub.get("canonical_url") or pub["source_url"],
        "image_license": "Original Center-created bibliographic card, requested by the user; journal cover rights remain unconfirmed",
        "image_license_es": "Ficha bibliográfica propia del Centro solicitada por el usuario; los derechos de las portadas siguen sin confirmar",
        "image_license_url": "",
        "image_rights_status": "original",
        "image_rights_url": "",
    }, {"title_font_size": title_size, "author_font_size": author_size, "citation_font_size": citation_size, "title_lines": title_lines, "authors": names, "citation": citation, "last_author_bottom": round(y), "publisher": publisher}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Update the CMS image fields after generating the cards")
    args = parser.parse_args()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    prior = json.loads(REGISTER.read_text()) if REGISTER.exists() else {"publications": {}, "area_features": {}}
    manifest = {"created_on": "2026-10-26", "method": "Deterministic typography using Pillow; no generative image model, publisher images or logos", "reference": "User-supplied WBER bibliographic card", "scope": "All published Journal article records, including the existing conference-proceedings record", "publications": prior["publications"], "area_features": prior["area_features"]}
    cards = {}
    for path in sorted((ROOT / "content/publications").glob("*.json")):
        pub = json.loads(path.read_text())
        if not pub.get("published") or pub["type"] != "Journal article":
            continue
        card, layout = create_card(pub)
        previous = manifest["publications"].get(pub["slug"], {}).get("previous_image", {k: v for k, v in pub.items() if k.startswith("image")})
        manifest["publications"][pub["slug"]] = {"previous_image": previous, "card": card, "layout": layout, "metadata_source": pub.get("canonical_url") or pub["source_url"]}
        cards[pub["slug"]] = card
        if args.apply:
            pub.update(card)
            path.write_text(json.dumps(pub, ensure_ascii=False, indent=2) + "\n")
    if args.apply:
        for path in sorted((ROOT / "content/research-areas").glob("*.json")):
            area = json.loads(path.read_text())
            for feature in area.get("publication_features", []):
                slug = feature["publication"]
                if slug not in cards:
                    continue
                key = area["slug"] + ":" + slug
                manifest["area_features"].setdefault(key, {k: v for k, v in feature.items() if k.startswith("image")})
                feature.update(cards[slug])
            path.write_text(json.dumps(area, ensure_ascii=False, indent=2) + "\n")
    REGISTER.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print(f"Generated {len(cards)} original bibliographic cards in {OUTPUT.relative_to(ROOT)}; CMS references {'updated' if args.apply else 'unchanged'}.")


if __name__ == "__main__":
    main()
