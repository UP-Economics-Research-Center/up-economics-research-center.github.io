#!/usr/bin/env python3
"""Generate reviewed-image delivery copies; keep every original untouched.

Authoring only: requires the Pillow already used for publication-card generation.
The static production build does not import Pillow.
"""
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "design/assets/responsive"


def main():
    sources = set()
    for path in sorted((ROOT / "content/people").glob("*.json")):
        row = json.loads(path.read_text())
        if row.get("published") and row.get("portrait"):
            sources.add(row["portrait"])
    for path in sorted((ROOT / "content/research-areas").glob("*.json")):
        row = json.loads(path.read_text())
        if not row.get("published"):
            continue
        records = [row if row.get("image") else row.get("banner", {}), *row.get("projects", [])]
        sources.update(record["image"] for record in records if record.get("image") and record.get("image_fit") != "contain")
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for source in sorted(sources):
        path = ROOT / source.lstrip("/")
        if path.stat().st_size < 150_000:
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        with Image.open(path) as original:
            image = ImageOps.exif_transpose(original)
            if image.mode not in ("RGB", "RGBA"):
                image = image.convert("RGBA" if "transparency" in image.info else "RGB")
            widths = sorted({min(width, image.width) for width in (480, 960, 1440)})
            options = []
            for width in widths:
                target = OUT / f"{path.stem}-{digest[:12]}-{width}.webp"
                resized = image.resize((width, round(image.height * width / image.width)), Image.Resampling.LANCZOS)
                resized.save(target, "WEBP", quality=88, method=6, icc_profile=original.info.get("icc_profile", b""))
                options.append({"src": "/" + target.relative_to(ROOT).as_posix(), "width": width, "height": resized.height})
            manifest["/" + source.lstrip("/")] = {"sha256": digest, "variants": options}
    (OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print(f"Generated derivatives for {len(manifest)} approved source images; originals unchanged.")


if __name__ == "__main__":
    main()
