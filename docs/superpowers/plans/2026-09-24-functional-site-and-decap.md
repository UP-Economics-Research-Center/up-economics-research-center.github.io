# Functional Site and Decap CMS Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the existing organization-root website navigable and searchable, publish verified publication details, and enable invited editors to propose reviewed content changes through Decap CMS.

**Architecture:** Keep `index.html`, existing `design/*.html`, shared CSS, scripts, and local media as the presentation source of truth. Add structured approved content and a dependency-free Python build that generates `_site/` with the existing site, publication detail routes, and a local search index; GitHub Actions publishes `_site/` to Pages. Decap edits the structured records on review branches through GitHub OAuth backed by a separately configured Cloudflare Worker.

**Tech Stack:** Existing HTML/CSS/vanilla JavaScript; Python 3 standard library for static content validation/build; Decap CMS; GitHub Actions and Pages; Cloudflare Worker for OAuth.

**Spec:** `docs/superpowers/specs/2026-09-24-decap-cms-design.md`

## Global Constraints

- Preserve the current HTML and shared CSS as presentation source of truth, along with existing local media and responsive/accessibility behavior.
- Use GitHub Pages with GitHub Actions. Do not use `docs/` as the Pages source.
- Use Decap CMS and GitHub authentication for invited repository collaborators. Other contributors may submit GitHub pull requests for review.
- Do not publish demo, unverified, or unsupported content as fact. The six `[Demo]` publication records currently embedded in `design/publications.html` are illustrative and must not appear in the public list, search index, or generated detail pages.
- Do not commit OAuth secrets, tokens, or other credentials.
- Keep the organization root URL: `https://up-economics-research-center.github.io/` and repository `UP-Economics-Research-Center/up-economics-research-center.github.io`.
- Preserve the homepage's muted autoplay video and reduced-motion behavior.
- No automated test files or test suites are added or run; perform focused source/configuration and path inspections as requested by project guidance.

## Review Focus

- Empty or malformed content records must produce a clear build error and must not leak drafts into public output.
- Accented, mixed-case, multi-term, and unmatched search queries must keep useful, accessible outcomes.
- Missing publication abstracts or download files must not be invented or rendered as broken buttons.
- Internal links and section anchors must resolve from both `/` and `/design/` routes on the organization root domain.
- Missing OAuth configuration or repository access must explain the required owner/editor action without exposing a secret.

---

### Task 1: Define structured editorial records and Decap collections

**Files:**
- Create: `content/settings/site.json`
- Create: `content/people/` records mapped from existing currently approved public content
- Create: `content/research-areas/` records mapped from existing currently approved public content
- Create: `content/publications/` (empty of public records until verified records are supplied)
- Create: `content/news/` and `content/seminars/` records only for existing verified content
- Create: `admin/index.html`
- Create: `admin/config.yml`
- Create/update: `.gitignore` for `_site/`
- Reference: `design/research-people-data.json`, `design/publications.html`, `design/news.html`, `design/seminars.html`

**Interfaces:**
- Produces stable IDs/slugs and named fields that Tasks 2–4 consume.
- Publication records use: `slug`, `title`, ordered `authors`, `abstract`, `year`, `type`, `venue`, optional `doi`, `canonical_url`, optional `pdf`, `topics`, `source_url`, `verified_on`, and `published`.
- Person and area records keep relationship IDs instead of duplicating titles or URLs.

- [ ] Inspect each existing record and preserve only currently approved content; do not convert `[Demo]` publications or unconfirmed events into published records.
- [ ] Create Decap collections matching the spec with explicit user-facing labels, required fields, repeatable authors/topics, media paths, draft/published state, and validation hints.
- [ ] Configure Decap GitHub backend for `UP-Economics-Research-Center/up-economics-research-center.github.io`, branch `main`, editorial workflow enabled, local media under `design/assets/uploads`, and no Open Authoring.
- [ ] Keep OAuth credentials out of `admin/config.yml`; leave only documented public Worker URL/client ID configuration placeholders.
- [ ] Inspect YAML and JSON syntax with available standard-library parsers and inspect each configured media/content path.

### Task 2: Build the static site artifact and content validation

**Files:**
- Create: `tools/build_site.py`
- Create: `templates/publication-detail.html`
- Create: `content/search-pages.json` or an equivalent explicit static page metadata source
- Modify: `.github/workflows/pages.yml`
- Modify: `.gitignore`
- Reference: `index.html`, `design/*.html`, `design/site-concept.css`, `design/assets/`

**Interfaces:**
- `build_site.py` reads `content/` and outputs the complete deployable site to `_site/`.
- Build validation rejects duplicate slugs, missing required fields, invalid local file paths, broken content references, malformed publication URLs, or invalid year/date fields with source filename and field in its error message.
- Only records with `published: true` are copied to the public output or search index.
- Pages workflow installs no runtime dependency and uploads `_site/` rather than `.`.

- [ ] Add a small build entry point using only Python standard library modules (`json`, `pathlib`, `shutil`, `html`, `urllib.parse`, `sys`).
- [ ] Copy existing homepage and design pages/assets into `_site/` without changing presentation CSS or media; make the current root `index.html` the canonical generated homepage and keep its navigation prefixed correctly for `/design/` destinations.
- [ ] Validate stable IDs, local paths, allowed link schemes (`https`, `mailto`, `tel`, and site-relative), required fields, and references before writing any artifact.
- [ ] Render published people, research areas, publications, news, seminars, site settings, and About-page values into marked slots in their existing HTML templates; render an accessible empty state when an approved collection has no records. Keep template structure/CSS in the existing HTML/CSS and escape every inserted value.
- [ ] Generate `/publications/<slug>/index.html` from the publication template for each published publication, HTML-escaping all text and attributes.
- [ ] Generate `/people.json`, `/research-areas.json`, `/publications.json`, `/news.json`, and `/seminars.json` only where page scripts need structured records; each must contain published records only.
- [ ] Write a compact `_site/search-index.json` containing approved page, area, person, publication, seminar, and news fields with their correct root-relative route.
- [ ] Update `.github/workflows/pages.yml` to run the builder, then upload `_site/`; retain `configure-pages`, `deploy-pages`, permissions, `main` trigger, and concurrency.
- [ ] Inspect the build output paths and workflow YAML manually. Confirm source files and `docs/` are not copied as the Pages source except where expressly linked public docs are required.

### Task 3: Make global navigation and search content-aware

**Files:**
- Modify: `design/mobile-navigation.js`
- Modify: `index.html` and the shared search markup in `design/*.html` only where IDs/labels or search status need correction
- Modify: `design/site-concept.css` only for accessible search result/unavailable states if missing
- Produced input: `_site/search-index.json` from Task 2

**Interfaces:**
- Browser search reads `/search-index.json` relative to the domain root and matches records with `name`, `description`, `keywords`, `url`, and `group` fields.
- Search normalizes case and diacritics, matches every query term across indexed fields, and only creates result elements with DOM text APIs (never injects record text as HTML).

- [ ] Preserve the current open/close, Escape, focus restoration, clear button, mobile menu interaction, and no-query suggested links.
- [ ] Load the generated index once; show an announced, plain-language unavailable message if it cannot be fetched.
- [ ] Add approved people, areas, publications, news, and seminars to matches; make every result link to a real route or person anchor.
- [ ] Ensure no results include a short actionable hint and the status is announced via the existing live region.
- [ ] Inspect URL paths from root and `design/` pages; use root-relative URLs for generated routes and valid fragments for existing pages.

### Task 4: Connect publications list, filters, and detail pages

**Files:**
- Modify: `design/publications.html`
- Modify: `templates/publication-detail.html`
- Modify: `design/site-concept.css` only for new detail/empty-state components if needed
- Input records: `content/publications/*.json`
- Generated route: `/publications/<slug>/index.html`

**Interfaces:**
- The list consumes published publication records via generated `/publications.json` or an equivalent generated list data file.
- Query parameters `q`, `topic`, `year`, and `type` initialize filters and update the URL with `history.replaceState` without reloading.
- Each list row links to `/publications/<slug>/`; detail pages include title, authors, abstract, date/type/venue, topics, canonical source, and optional PDF.

- [ ] Remove the inline `demoPubs` dataset and its fictional records from public output; retain the current filter layout and visual styling.
- [ ] Generate a public publication data file from published records and have the list render rows using safe DOM APIs.
- [ ] Preserve search by text, topic, year, and type; populate year/type/topic options from available approved records, apply URL parameters on page load, and keep links to filtered views shareable.
- [ ] Add an explicit empty state for no published papers and for filters with no matches; do not show dead `#` links or a download control when no paper file exists.
- [ ] Render detail pages with an ordered author list, full abstract, verified metadata, topic links, DOI/canonical external link, and only a supplied approved download path/URL.
- [ ] Include a working “All publications” return link and sensible page title/description metadata.

### Task 5: Repair and preserve site links and static routes

**Files:**
- Modify only affected links in: `index.html`, `design/homepage-concept.html`, `design/research.html`, `design/people.html`, `design/research-area.html`, `design/publications.html`, `design/seminars.html`, `design/news.html`, `design/about.html`
- Modify: `design/research-people.js` and corresponding data records only if a real profile anchor/path is broken
- Reference generated paths from Tasks 2–4

- [ ] Inventory all local `href`, `src`, form actions, and fragment links in the maintained pages; exclude intentionally external links, `mailto:`, and valid query routes from local-file checks.
- [ ] Correct dead links, placeholder `href="#"` actions, incorrect root-vs-`/design/` paths, and missing anchors while retaining existing link text and visual direction.
- [ ] Preserve `research-area.html?area=...`, people profile anchors, publication type filters, seminar section anchors, and contact links.
- [ ] Inspect YouTube player markup and reduced-motion code to ensure the current muted autoplay experience and user-operated fallback remain.

### Task 6: Add the GitHub OAuth Worker and Decap editor guidance

**Files:**
- Create: `oauth-worker/src/index.js` (or the smallest maintainable Worker entry point)
- Create: `oauth-worker/wrangler.toml` without secrets
- Create: `oauth-worker/README.md`
- Modify: `README.md`
- Reference: `admin/config.yml`, organization OAuth App settings, Cloudflare Worker secrets

**Interfaces:**
- Worker endpoints implement the authorization redirect and OAuth callback expected by the pinned Decap CMS version.
- GitHub client secret is read only from Cloudflare Worker secret binding; never from repository variables embedded into the artifact.
- README separates steps an invited editor can do from owner-only OAuth/Cloudflare setup.

- [ ] Pin an official Decap CMS release and consult its official backend-authentication documentation for the exact OAuth message/callback protocol before implementing the Worker.
- [ ] Implement narrowly scoped OAuth state validation, redirect validation against the configured Pages origin, provider error handling, and the Decap callback response; keep client ID public and client secret in an external Worker secret.
- [ ] Document Worker deployment, GitHub OAuth App callback URL, secret binding, allowed site origin, CMS public URL/client ID configuration, and credential rotation without including example secrets.
- [ ] Rewrite the README editor guide so it never implies `/admin/` is usable before owner setup is complete; explain GitHub sign-in, collections, preview, PR review, merge/deploy timing, outside PR proposals, verified paper metadata, and troubleshooting in plain language.
- [ ] Document that OAuth Worker deployment, OAuth App setup, invited collaborator access, and branch review protection are owner-side setup still required unless those steps are actually completed.

### Task 7: Review the integrated publication workflow and deployment configuration

**Files:**
- Inspect: `.github/workflows/pages.yml`, `admin/config.yml`, `oauth-worker/README.md`, `README.md`
- Inspect generated artifact: `_site/`
- No new automated test files or test suite runs

- [ ] Manually inspect one built homepage route, a `/design/` route, the publications empty state, and one detail page built from a verified record if the Center has supplied one.
- [ ] Manually inspect search result routes for each content type, accented and multi-term matching, no-result behavior, and unavailable-index message.
- [ ] Inspect internal route/fragment inventory against `_site/`; confirm list/detail, area, person, news, seminar, and contact links land correctly.
- [ ] Review responsive/accessibility attributes touched by changes: labels, headings, live region, keyboard search controls, image alt text, reduced-motion behavior, and focus restoration.
- [ ] Confirm no `[Demo]` records, OAuth secret, token, or owner credential is in `_site/` or tracked configuration.
- [ ] If Cloudflare/GitHub owner configuration is available, perform a manual CMS draft → PR → maintainer merge → Pages deployment walkthrough. Otherwise report the exact owner setup items remaining and do not claim CMS authentication is live.
- [ ] Review Git diff for unrelated changes and commit the completed integrated work in coherent commits.
