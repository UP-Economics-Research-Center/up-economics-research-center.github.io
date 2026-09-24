# UP Economics Research Center site and CMS design

**Date:** 2026-09-24  
**Status:** Proposed for review

## Goal

Turn the current static site into a reliable, editable research center website without changing its approved visual direction. Visitors must be able to follow navigation, search useful site content, filter publications, and open a publication detail page with verified metadata and paper links. Invited editors use Decap CMS with GitHub sign-in; a maintainer reviews changes before they reach the live site.

## Agreed constraints

- Keep the organization root URL: <https://up-economics-research-center.github.io/> and the repository `UP-Economics-Research-Center/up-economics-research-center.github.io`.
- Preserve the current HTML and shared CSS as presentation source of truth, along with existing local media and responsive/accessibility behavior.
- Use GitHub Pages with GitHub Actions. Do not use `docs/` as the Pages source.
- Use Decap CMS and GitHub authentication for invited repository collaborators. Other contributors may submit GitHub pull requests for review.
- Do not publish demo, unverified, or unsupported content as fact. The six `[Demo]` publication records currently embedded in `design/publications.html` are illustrative and must not appear in the public list, search index, or generated detail pages.
- Do not commit OAuth secrets, tokens, or other credentials.

## Approaches considered

1. **Keep all content embedded in HTML.** Lowest initial effort, but editors must change code and the search index and publication details will drift.
2. **Use Decap content records and generate static pages. Recommended.** Editors work with named fields, while a small dependency-free build step produces fast, crawlable static pages and a shared search index for GitHub Pages.
3. **Move to a server-rendered CMS or hosted publishing platform.** This adds hosting and migration costs and is unnecessary for the agreed static site and review workflow.

## Architecture

The site remains a static GitHub Pages publication built from the root repository source by GitHub Actions. Existing HTML and `design/site-concept.css` remain the visual source of truth. A dependency-free Python build step reads structured files under `content/`, validates references and publication approval state, and creates the Pages artifact in a temporary build directory. The step retains the current page templates and local design assets, produces approved publication detail pages, and writes a search index from the approved public content. GitHub Actions uploads that artifact to Pages.

Decap CMS lives under `/admin/`. Its GitHub backend targets `UP-Economics-Research-Center/up-economics-research-center.github.io` on `main`, with editorial workflow enabled. A small Cloudflare Worker supplies the OAuth authorization and callback Decap requires; GitHub Pages does not provide server-side authentication. The Worker holds OAuth credentials as secrets. Repository configuration contains only the public client ID and Worker endpoint.

The current homepage's muted autoplay video remains. Existing pages and media stay locally referenced where possible. Site-wide navigation, footer links, research-area links, people profile anchors, homepage calls to action, and publication filters must resolve to a real page, valid section anchor, or valid external destination. External destinations open only when appropriate and are labelled accessibly.

## Public routes and navigation

- Keep the organization homepage at `/`.
- Keep the current section routes under `/design/` during this iteration so existing linked paths remain stable.
- Treat `design/homepage-concept.html` as the current source page for homepage presentation; keep `index.html` aligned with it or make it the canonical homepage template during the build.
- Add publication detail pages at `/publications/<slug>/index.html`. Publication-list links point to these stable slugs. A detail page includes a clear return link to Publications and working links to the DOI, publisher, or approved downloadable file.
- Validate internal links and anchors against the built route set. Keep only verified external links in approved content. Do not use `href="#"` as a placeholder action.
- Preserve useful existing query links such as publication type filters and research area filters. Invalid or empty filter values fall back to the unfiltered page without a broken state.

## Search and publications

The existing global search index currently contains only hard-coded section and research-area entries. Replace this limited list with a generated, local search index containing approved public records from:

- Site pages and research areas.
- People profiles and research topics.
- Publications, including title, authors, abstract, year, venue, and topics.
- Approved news and seminars.

Search remains client-side and dependency-free. Normalize case and diacritics, support combined terms, show a useful no-results state, preserve keyboard operation and screen-reader status announcements, and link results to the relevant page or publication detail. If JavaScript or the index is unavailable, the site navigation and publication list remain usable; search reports a clear unavailable state.

The Publications page supports text, topic, year, and type filters, reflects shareable filter state in the URL, and displays a meaningful empty state when there are no approved matching records. Clicking a publication opens its detail page with:

- Title, author list in editorial order, year, publication type, venue or working-paper series.
- Abstract and research topics.
- DOI, publisher/canonical source, and downloadable PDF or other approved paper file when supplied.
- Optional citation and related researchers/areas only when verified.
- A clear indication when the full text is available externally or no download has been supplied.

No abstract, author, citation, DOI, or download is inferred or fabricated. If no verified records are provided at rollout, the public publication page shows its reviewed empty state and the demo records remain excluded.

## Decap collections and fields

Content is stored in explicit JSON or Markdown records under `content/`. Stable IDs and slugs keep links between people, research areas, publications, news, and seminars.

- **Site settings:** site label, homepage introduction, footer attribution, verified public contact details, and campus video ID/caption.
- **People:** stable ID, name, role, biography, portrait path and alt text, profile slug, research-area IDs, canonical/source URL, verification date, and publication approval.
- **Research areas:** stable ID, name, summary, associated people IDs, canonical/source URL, verification date, and publication approval.
- **Publications:** stable slug, title, ordered/repeatable authors, abstract, year, type, venue/series, DOI, publisher/canonical URL, optional local PDF path or approved download URL, topic IDs, source URL, verification date, and publication approval.
- **Seminars:** stable ID, series, title, speaker, date and time with time zone, description, location or registration/recording URL, source URL, and publication approval. Unconfirmed events are drafts.
- **News:** stable ID, title, date, summary, body, canonical URL, source URL, and publication approval.
- **About-page copy:** approved scope, affiliation, collaboration text, and verified public contact.

Fields use plain language, required-field guidance, repeatable lists for authors and related topics, and validation for dates, slugs, and links. Editors do not edit HTML or CSS. Records lacking required verified facts stay drafts and are not emitted into the public build.

## Review, publication, and access

1. A named editor with repository access signs into `/admin/` through GitHub and edits a content record.
2. Decap saves the work to an editorial branch and opens a pull request; it does not publish directly to `main`.
3. A maintainer checks the rendered preview, factual sources, link destinations, image permission/alt text, and changed records, then approves and merges.
4. GitHub Actions validates content references and builds the static artifact. Draft or unapproved records are excluded. Invalid required data or broken internal references fail the build with a file/field error rather than silently producing incomplete pages.
5. A successful Pages deployment updates the public site. A failed build leaves the previous deployment in place.

Do not enable Decap Open Authoring in v1. Anyone without repository write access cannot edit through the CMS; they can submit a pull request from GitHub for maintainer review. Protect `main` with pull-request review where the organization plan permits. If that rule is unavailable, only named maintainers merge content PRs and the README documents that manual review step.

The admin page explains sign-in failures, missing repository access, and how to request access in plain language. CMS controls are labelled, keyboard-operable, and usable with assistive technology. Public pages keep semantic headings and image alternatives. The existing responsive and reduced-motion behavior is preserved.

## Rollout prerequisites

1. Add Decap admin files/configuration, content collections, approved content records, build step, and Pages workflow integration while retaining the current visual templates.
2. Map only verified and currently approved public material. Exclude all demo publications and unconfirmed events.
3. Have the organization owner create a GitHub OAuth App, deploy the OAuth Worker, store its client secret in Cloudflare, and configure the public Worker address/client ID in Decap.
4. Invite editors to the repository at the minimum role that permits Decap editing, and have each editor authorize the GitHub app.
5. Configure review protection for `main` if available on the organization plan.
6. Verify a draft-to-PR-to-review-to-merge flow, a successful Pages deployment, search/navigation/publication routes, and that no secret enters the repository or deployed artifact.

The organization owner must provide/configure the Cloudflare account and OAuth application. Credentials are never requested in chat or committed to the repository.

## README guidance

The README must clearly distinguish installed features from pending owner configuration. It should explain in plain language how invited editors sign in, select and edit a collection, check a preview, submit work for review, and know when a change is published. It must explain the pull-request workflow for outside contributors, how to provide verified publication abstracts and paper links, and the remaining OAuth Worker setup. Do not tell editors to sign into a CMS before `/admin/` is deployed.

## Out of scope

- Redesigning the approved visual identity, replacing original local media, or removing the requested muted autoplay homepage video.
- Publishing the illustrative `[Demo]` records or inventing missing paper metadata.
- Using Clerk as a drop-in Decap GitHub backend; it would require a separate custom authorization and GitHub-writing service.
- Moving the public site away from GitHub Pages or making `docs/` its Pages source.
- Publishing user-submitted content without maintainer review.

## Acceptance criteria

- The root homepage and all existing navigation/CTA/internal links resolve correctly on the organization-root GitHub Pages domain, including mobile navigation and valid section anchors.
- Global search finds approved people, areas, publications, news, seminars, and pages by relevant words; combined queries, accents, empty queries, and no-match queries have usable outcomes.
- Publications can be filtered by text, topic, year, and type with shareable URL state. Each approved result opens a stable detail page with its verified abstract, authors, metadata, and supplied canonical/download links.
- Demo publications, unapproved records, and unconfirmed items are absent from public pages and search.
- An invited collaborator can use Decap to create a review pull request; no CMS save directly deploys to the public branch.
- Merged approved changes trigger GitHub Actions Pages deployment; build/content errors are reported clearly.
- Existing visual direction, local assets, responsive layout, accessible labels/keyboard use, and reduced-motion behavior are retained.
- No OAuth secret, access token, or other credential appears in version control, CMS client configuration, or the Pages artifact.
- README accurately describes the working editor flow and names any setup still owned by the organization administrator.
