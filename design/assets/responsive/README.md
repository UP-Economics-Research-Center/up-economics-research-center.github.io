# Responsive delivery copies

These WebP files are smaller delivery copies of existing approved portraits,
research-area images and project photographs. They do not introduce new imagery
or permissions. Original files, provenance and editorial framing remain the
source of truth; the original institutional wordmark is never processed.

Regenerate from the repository root after changing a source photograph:

```sh
python3 tools/generate_responsive_images.py
python3 tools/build_site.py
```

Generation uses Pillow, already required by the authoring-only publication-card
generator. The production build needs only Python's standard library and the
committed copies. It checks the original's SHA-256 against `manifest.json` and
falls back to that original if copies are missing or outdated. Editors can still
publish a new photograph through the CMS without running an image tool.

Copies keep the whole source composition and its orientation, without cropping
or colour filters. Existing CSS and `portrait_crop` still control the displayed
framing. Widths are 480, 960 and 1440 pixels, without upscaling. Sources smaller
than 150 kB and complete project diagrams remain unchanged.
