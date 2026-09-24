# Econ Site

Visual website mock for the **Economics Research Center, Universidad Panamericana**, with a planned visual editing workflow for economists and other non-technical editors.

## What is here

- `design/` contains the current HTML pages, shared CSS, scripts, and original media assets.
- `docs/` contains design decisions and prior migration research.
- `admin/` and `content/` will hold the visual CMS interface and editable records.

Open `index.html` in a browser to view the homepage mock. GitHub Pages serves this file at the site root; the remaining page templates and assets stay in `design/`. The mock is currently a static local prototype; CMS publishing and editor login require a Git hosting and deployment setup.

## Editing approach

The project is being prepared for **Decap CMS**, a browser-based editor with simple fields and repeatable content blocks. Editors will use a preview, fill in familiar fields, and save changes; they will not need to edit HTML or CSS. The current design and assets remain the presentation layer.

Content should be organized as:

- Pages: Home, Research, People, Publications, Seminars, News, and About.
- Repeatable records: people, research areas, publications, seminars, and news items.
- Media: locally stored images and files with their source/permission details retained.

## Local preview

Open `design/homepage-concept.html` directly in a browser. Some browser features may work more reliably when served locally. From the repository root, run:

```sh
python3 -m http.server 8000
```

Then visit `http://localhost:8000/`.

## CMS and publishing status

The CMS editor becomes usable after the repository is hosted on GitHub and connected to a supported deployment/authentication setup. Keep the site in draft until the Center owner verifies biographies, affiliations, image permissions, contact details, public audience, and domain. Existing media and content approval notes are in `design/`.

## Editorial guidance

- Do not publish demo examples or unverified facts as final content.
- Keep dates and citations current and link each item to its canonical source or destination.
- Preserve the shared design system in `design/site-concept.css`; editors should change content, not page styling.
- See `AGENTS.md` for project-wide editing rules.
