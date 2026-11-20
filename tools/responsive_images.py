"""Use pre-generated image derivatives without adding production dependencies."""
from functools import lru_cache
import hashlib
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "design/assets/responsive/manifest.json"


@lru_cache(maxsize=1)
def manifest():
    return json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}


@lru_cache(maxsize=None)
def variants(source):
    row = manifest().get("/" + source.lstrip("/"))
    if not row:
        return []
    original = ROOT / source.lstrip("/")
    if not original.is_file() or hashlib.sha256(original.read_bytes()).hexdigest() != row["sha256"]:
        return []
    return [item for item in row["variants"] if (ROOT / item["src"].lstrip("/")).is_file()]


def image_source(source, sizes):
    """Fall back to the CMS original when derivatives are absent or stale."""
    options = variants(source)
    if not options:
        return 'src="' + html.escape(source, quote=True) + '"'
    srcset = ", ".join(item["src"] + " " + str(item["width"]) + "w" for item in options)
    return ('src="' + html.escape(options[-1]["src"], quote=True) + '" srcset="'
            + html.escape(srcset, quote=True) + '" sizes="' + html.escape(sizes, quote=True) + '"')


def portrait_source(person, frame_width):
    crop = person.get("portrait_crop")
    width = frame_width * 100 / crop["width"] if crop else frame_width
    return image_source(person["portrait"], f"{width:.2f}px")
