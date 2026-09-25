# Research-Centered Site Refresh Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refocus the organization-root site around its researchers and research, with accurate profiles, nine conceptual area illustrations, discoverable paper details, a refreshed home page, Contact information, and consistent site icons.

**Architecture:** Keep the current HTML/CSS, Python static builder, Decap content files, and GitHub Pages workflow. Extend the structured records and builder to render ordered people, area cards, area-specific SVGs, individual publication pages, the home research feature, current UP video, and shared favicons. Keep the seminar portal internal and omit retired sections from the public artifact.

**Tech Stack:** HTML, CSS, vanilla JavaScript, hand-authored SVG, Python 3 standard library, Decap CMS, GitHub Pages Actions.

**Spec:** `docs/superpowers/specs/2026-09-25-research-centered-site-refresh-design.md`

## Global Constraints

- Keep `https://up-economics-research-center.github.io/` as the public site root.
- Use the approved English source descriptions and names; do not add unsupported biography, project, paper, or contact claims.
- Preserve official complete author order on individual paper pages. Use `person_id` relationships to prioritize UP authors only in research-area cards.
- Keep the publications CMS collection and individual `/publications/<slug>/` routes; remove the general listing from public navigation/output.
- Keep News and Seminars source records and files, but remove their CMS collections, feeds, search results, and public routes. Do not change the internal seminar portal.
- Preserve any already-approved About copy and fields. Publish Contact independently without setting an unpublished About section to published or exposing unverified About text.
- Keep Decap direct publishing and `open_authoring: false`; do not change OAuth, branch protection, or permissions.
- Keep image and illustration assets local. Use the supplied Drive image only after confirming the file is accessible and matches the requested people/article feature.
- Do not display Esteban’s outdated portrait. If no current approved portrait is in the Drive item, leave his portrait absent.
- Keep the campus player muted with autoplay on the normal motion path, controls and inline playback, and click-to-play for reduced-motion preference.
- Add no dependencies, test files, or automated test suites. Use build, syntax, path, and manual visual checks only.
- Do not commit secrets or files outside the project.

## Review Focus

- **Author affiliation and order:** An external coauthor must never be promoted to UP or removed from the official byline. Manual check in Task 2 compares a paper with a non-first UP author and its detail-page citation.
- **Stale or inaccessible media:** The home feature, Esteban portrait, and campus poster must use the intended approved files. Manual check in Tasks 1 and 5 verifies image identity, alt text, reuse permission, and local file paths; omit a portrait or feature if its asset is unavailable. Do not invent a video caption, title, or poster when the video cannot be verified.
- **Retired routes and search:** Old nav links, feeds, or search entries must not lead to News, Seminars, or a publication directory. Manual artifact inspection in Tasks 3 and 7 checks generated paths and links.
- **Responsive and accessible artwork:** The sketches must not replace readable area names or overflow narrow screens. Manual checks in Task 4 inspect 390px, 768px, and desktop widths and verify decorative images have empty alt text.
- **Icon paths from nested routes:** Favicon links must work from root pages, `/admin/`, and nested publication details. Manual checks in Tasks 6 and 7 inspect every icon URL in the built artifact.

---

### Task 1: Refresh People records and directory order

**Files:**
- Modify: `admin/config.yml`
- Modify: `content/people/*.json`
- Modify: `tools/build_site.py`
- Reference: current Center source page and selected official profile URLs in the design spec

**Interfaces:**
- Consumes: person JSON records with `name`, `role`, `bio`, `portrait`, `canonical_url`, and publication state.
- Produces: ordered People output from `render_people(people, areas)`, sorted by each record’s numeric `display_order`.

- [ ] Copy each of the eleven listed researchers’ individual research descriptions from the current Center source page into that person’s record; keep Maria Jose Favela’s approved display name exactly `Maria Jose Favela`.
- [ ] Add a required numeric `display_order` field to the Decap people collection and assign lead order Akito `10`, Esteban `20`, Eugenio `30`, Maria Jose `40`, Arnulfo `50`; order research professionals as José Miguel `60`, Marytell `70`, Juan Álvaro `80`, Andrea `90`, Joshua `100`, Luciano `110`.
- [ ] Update `render_people()` to sort by `display_order` before grouping, and render the canonical profile link from the CMS field.
- [ ] Set Esteban’s canonical URL to the selected official UP profile. Confirm Eugenio’s candidate personal URL from the existing People source is still preferred; set the confirmed URL in his record.
- [ ] Inspect the supplied Drive item for a current Esteban portrait. Use it only if it is clearly his current approved portrait; otherwise set his portrait empty so no old image appears.
- [ ] Keep `content/people/sergio.json` unpublished and confirm no Sergio card is generated.
- [ ] Build the site and manually inspect the resulting People order, bios, profile links, portrait alt text, and missing-portrait behavior.
- [ ] Commit the People records, schema, and renderer together.

### Task 2: Link UP authors and format area-card bylines

**Files:**
- Modify: `admin/config.yml`
- Modify: `content/publications/*.json`
- Modify: `design/research-people.js`
- Reference: `templates/publication-detail.html`, `tools/build_site.py`

**Interfaces:**
- Consumes: publication authors as ordered objects `{name, person_id?}`; current Center authors use a valid People slug and outside coauthors omit `person_id`.
- Produces: `formatAreaByline(authors) -> string` for area cards; generated publication detail pages continue to render `authors` in original citation order.

- [ ] Change the nested author “Center researcher” field in Decap to a relation to the `people` collection, with person slug as its value.
- [ ] Add `person_id` only to publication author entries that match a current Center person; retain every author and the exact current sequence in each record.
- [ ] Implement `formatAreaByline(authors)` in `design/research-people.js`: put linked UP authors first in their source-relative order, append ` with ` and remaining coauthors in source-relative order, and show the complete source order unchanged when there is no linked UP author.
- [ ] Use the formatter for paper cards on area pages; do not use it in `templates/publication-detail.html` or the full publication citation.
- [ ] Build the site and inspect a paper where the UP researcher is not first in the official byline, a paper with only UP authors, and one paper detail page. Confirm the detail page preserves the full official order.
- [ ] Commit author relations and rendering together.

### Task 3: Simplify public navigation and publish Contact separately

**Files:**
- Modify: `index.html`
- Modify: `design/homepage-concept.html`, `design/research.html`, `design/research-area.html`, `design/people.html`, `design/about.html`, `design/publications.html`, `design/news.html`, `design/seminars.html`
- Modify: `templates/publication-detail.html`
- Modify: `admin/config.yml`, `content/settings/about.json`, `content/search-pages.json`, `tools/build_site.py`
- Preserve: `content/news/`, `content/seminars/`, and source HTML files

**Interfaces:**
- Consumes: approved current records plus `contact_published`, `contact_email`, and `contact_address` in `content/settings/about.json`.
- Produces: primary navigation with Research, People, About, and Contact; `/publications.html` redirects to `/research.html#areas`; paper details remain at `/publications/<slug>/`.

- [ ] Remove Publications, News, and Seminars links from desktop navigation, mobile navigation, and footers on all maintained source pages; keep Home linked through the wordmark and Contact pointed to `about.html#contact`.
- [ ] Remove News and Seminars collections from Decap and omit their pages, scripts, feeds, and search records from `tools/build_site.py`; leave their tracked source files and content folders untouched.
- [ ] Retain the Decap Publications collection and individual publication detail generation; stop generating the publication directory and emit a simple legacy redirect from `/publications.html` to `/research.html#areas`.
- [ ] Remove the obsolete publication directory entry from `content/search-pages.json`; retain one search result per published paper pointing to its detail route.
- [ ] Add `contact_published` and `contact_address` to the About CMS fields. Set Contact to published with the email and address from the original Center page while preserving the current About publication setting and all approved About copy. Leave the broader About content unpublished only if it is currently unpublished; do not overwrite approved content.
- [ ] Update `render_about()` and build validation so published Contact renders independently of the About-copy `published` flag; preserve existing About content/settings and validate email, address, and source metadata before output.
- [ ] Build and inspect root and mobile nav, footer, contact mailto/address, legacy redirect, and the absence of public News/Seminars pages and feeds.
- [ ] Commit navigation, route generation, Contact content, and CMS schema together.

### Task 4: Add research-area sketches and image-led layouts

**Files:**
- Create: `design/assets/research-areas/education-and-human-capital.svg`
- Create: `design/assets/research-areas/digital-and-business-economics.svg`
- Create: `design/assets/research-areas/political-economy.svg`
- Create: `design/assets/research-areas/macroeconomics.svg`
- Create: `design/assets/research-areas/development-economics.svg`
- Create: `design/assets/research-areas/health-water-sanitation.svg`
- Create: `design/assets/research-areas/agricultural-economics.svg`
- Create: `design/assets/research-areas/environmental-economics.svg`
- Create: `design/assets/research-areas/economic-demography.svg`
- Modify: `design/research.html`, `design/research-area.html`, `design/research-people.js`, `design/site-concept.css`, `tools/build_site.py`

**Interfaces:**
- Consumes: each published area’s stable `slug`, name, summary, overview, projects, team, and related papers.
- Produces: area feed entries with an optional local `illustration` path; Research hub cards and area detail heroes render that illustration decoratively, with visible text carrying the area meaning.

- [ ] Draw nine distinct transparent-background SVGs with `viewBox="0 0 640 400"`, fine ink lines, limited wine and gold accents, and no embedded text. Use the approved motifs: book/steps; digital windows/nodes; civic columns/decision network; skyline/economic cycle; connected paths to services; water and pipes; agricultural terraces; climate/wind contours; population paths.
- [ ] Add a slug-to-local-file illustration map in `tools/build_site.py`; include an illustration URL in area feed records only when the mapped file exists.
- [ ] Update `render_area()` and `design/research.html` to render nine responsive image-led cards with the existing area number, title, and summary.
- [ ] Replace the hidden number-only visual in `design/research-area.html` with the selected area sketch and bind the area illustration from the feed in `design/research-people.js`.
- [ ] Add responsive CSS for the card grid and large area visual; keep the existing warm paper, ink, wine, and restrained gold palette.
- [ ] Mark illustrations decorative with empty alt text and preserve visible headings, summaries, and keyboard-accessible links.
- [ ] Build and manually view all nine hub cards and area details at 390px, 768px, and 1440px; inspect for broken images, clipping, and text overflow.
- [ ] Commit the illustrations, layout, and rendering map together.

### Task 5: Feature the supplied paper and replace the campus video

**Files:**
- Modify: `index.html`, `design/homepage-concept.html`, `design/site-concept.css`, `design/campus-video.js`, `tools/build_site.py`, `admin/config.yml`, `content/settings/site.json`, `design/assets/media-sources.json`
- Create or replace: approved local feature image and campus-video poster under `design/assets/`

**Interfaces:**
- Consumes: `featured_publication_slug`, `featured_image`, image alt/credit/source, `campus_video_id`, `campus_video_caption`, `campus_video_poster`, and poster alt text from `content/settings/site.json`.
- Produces: a Home research-highlight card linked to `/publications/<slug>/` and a video player whose embed, poster, caption, alt text, and YouTube link all use the approved video ID `ISvo7S30of4`.

- [ ] Add Decap fields for the featured image, alternative text, image credit/source, and a relation to `publications`; add video-poster image and alternative-text fields alongside the existing video ID and caption.
- [ ] Verify the Drive file’s identity and access, download the supplied people/article image into the project, and record its source. If the file cannot be retrieved or is not the intended people/article image, stop this feature step and request an accessible approved file while continuing independent tasks.
- [ ] Set the featured relation to `gender-education-farm-succession-western-parana`. Validate that the record exists and is published before generating the feature; make the image and action link to its internal paper detail route.
- [ ] Verify YouTube ID `ISvo7S30of4` against the Center-approved film, retrieve and save its matching thumbnail, and update its accessible description, visible caption, and media source entry. If the ID or thumbnail cannot be verified, leave the old film out of the new player, pause publication of the video change, and request an accessible approved thumbnail/details; do not substitute a guessed title, caption, or poster.
- [ ] Set `campus_video_id` to `ISvo7S30of4` and update the generated `Watch on YouTube` link from the same setting so the link cannot stay on the old video.
- [ ] Update `tools/build_site.py` to validate the featured paper relation and local feature/poster assets and render their alt text safely.
- [ ] Preserve `autoplay=1`, `mute=1`, `playsinline=1`, and visible controls in `design/campus-video.js`; preserve click-to-play when reduced motion is requested and use a generic iframe title that does not claim the old film title.
- [ ] Build and manually confirm the feature links to the correct paper; verify in a browser that the video is muted and autoplaying under normal motion preference, and waits for user action under reduced-motion preference.
- [ ] Commit the Home feature, video settings, poster, and source metadata together.

### Task 6: Add and wire a consistent favicon set

**Files:**
- Create: `favicon.svg`, `favicon.ico`, `apple-touch-icon.png`
- Modify: `index.html`, public `design/*.html` page heads, `admin/index.html`, `templates/publication-detail.html`, `tools/build_site.py`
- Preserve: `design/assets/erc-logo-concept.png` as an unused rejected exploration

**Interfaces:**
- Consumes: one geometric ivory `E` on a wine square, matching the approved design.
- Produces: root-relative favicon links on public routes, Decap, and nested publication details; icon assets copied to `_site/` root.

- [ ] Create `favicon.svg` as the crisp master artwork, with the approved geometric `E` and the current wine color `#8A1538`.
- [ ] Export `favicon.ico` and a 180×180 `apple-touch-icon.png` from the same master using an installed image conversion tool; add no dependency.
- [ ] Replace the rejected `erc-logo-concept.png` favicon link in `admin/index.html` and add SVG, ICO, and Apple icon links to maintained public page heads and `templates/publication-detail.html` using root-relative paths.
- [ ] Update `tools/build_site.py` to copy all three root icons into `_site/`.
- [ ] Build and inspect icon links and output files from `/`, `/people.html`, `/admin/`, and one nested publication detail route; confirm no page references the rejected logo as a favicon.
- [ ] Commit favicon source, exports, page links, and build-copy behavior together.

### Task 7: Update editor documentation and inspect the integrated build

**Files:**
- Modify: `README.md`, `content/README.md`, `design/current-design-direction.md`, `design/google-sites-build-map.md`
- Inspect: `admin/config.yml`, `.github/workflows/pages.yml`, generated `_site/`

**Interfaces:**
- Consumes: final CMS fields and routes from Tasks 1–6.
- Produces: current, plain-language editor instructions and a complete, manually reviewed `_site/` build.

- [ ] Update README editor instructions for People order, profile links, paper relation/author handling, area illustrations, Home highlight/video poster, Contact, and the direct publish-to-main workflow.
- [ ] Mark the Google Sites migration map as historical and link it to the active GitHub Pages architecture; leave its source material intact.
- [ ] Run `python3 tools/build_site.py` and inspect the output summary; confirm all 26 current paper detail routes and eleven public People profiles are emitted.
- [ ] Run `git diff --check` and `node --check design/research-people.js`; inspect any output before continuing.
- [ ] Inspect `_site/` for the expected root pages, all nine area illustration files, all favicon files, and the `/publications.html` redirect; confirm it contains no `news.html`, `seminars.html`, `news.json`, `seminars.json`, or publication-list page.
- [ ] Serve `_site/` locally and manually check Home, Research, People, About/Contact, one area detail, one paper detail, `/admin/`, desktop and mobile widths, keyboard navigation, search results, and video reduced-motion behavior.
- [ ] Review the final diff for only approved project files and commit documentation and integrated cleanup.

### Task 8: Publish the verified site and check GitHub Pages

**Files:**
- Publish: verified commits on the implementation branch to `main` using the already-authorized direct-publish workflow
- Inspect: GitHub Actions Pages run and live root site

**Interfaces:**
- Consumes: a clean, verified `_site/` build from Task 7.
- Produces: successful Pages deployment with live video ID, favicon assets, Research area cards, People directory, and individual paper routes.

- [ ] Confirm the implementation branch is based on the approved design/spec branch and the working tree is clean.
- [ ] Push the verified implementation to `main`; do not alter repository protection, OAuth, or organization permissions.
- [ ] Wait for the GitHub Pages Actions workflow to complete successfully.
- [ ] Request the homepage, one research page, one People page, one nested publication detail, `/admin/`, `/favicon.svg`, `/favicon.ico`, and `/apple-touch-icon.png`; confirm the expected pages and assets load.
- [ ] Confirm the live Home embeds verified video ID `ISvo7S30of4`, its matching poster and YouTube link use the same ID. Report any remaining Drive/image access issue explicitly.
- [ ] Record the live site URL, successful workflow run, and any remaining editor-provided media item needed.
