# Bilingual editorial refresh implementation plan

**Goal:** Implement the editorial agreements recorded in `docs/editorial-review-2026-10-15.md`.
**Architecture:** Keep the current static Python build, HTML/CSS sources and Decap CMS. Store English text and named Spanish companion fields in the same records. Generate a complete `/es/` version alongside English routes, with an accessible EN/ES switch that preserves page/query/hash and remembers an explicit selection.
**Execution:** Inline in this chat, as authorized by the user on 2026-10-15. No tests, new runtime framework, deployment, or push. Build and manually inspect the resulting artifact.

## Tasks
- [x] Import exact source descriptions and ongoing research from Akito's nine linked pages. Preserve paragraphs and provenance. Add faithful Spanish text, source-backed area relations, agreed names, biographies, ordering, and contact information. Flag ambiguous person assignments for the user.
- [x] Extend existing build rendering and CMS fields for bilingual text, area order, optional image/credit/link fields. Produce local Spanish routes and localized content/search feeds, preserving original paper titles and author order. Reject invalid paths and missing Spanish public text.
- [x] Update source HTML/CSS: hero slogan, full UP wordmark, home scope/seminar/collaboration/contact, larger portraits with areas beneath, optional small paper photos, journal/year metadata, photographic research areas. Keep the existing video and reduced-motion behavior.
- [x] Add EN/ES navigation with persistent selection and language-aware dynamic research, publication filters and search. Redirect legacy About routes to home contact.
- [x] Update README and content workflow. Build, inspect generated paths, JS/config syntax and responsive browser views; repair discovered issues. Record inaccessible or unapproved image material and unresolved editorial choices.

## Review focus
- Missing optional images collapse their column without empty placeholders.
- EN/ES switching preserves the current research area, filters and anchors; unavailable storage does not block navigation.
- Paper titles and names retain original wording in Spanish; full text/links remain available.
- Original area descriptions are not abridged and projects are not duplicated or confused with publications.
- About content and editorial review notes survive relocation; unverified content stays unpublished.

## Completion record

Implemented inline. Static build succeeds with 51 search entries per language, 24 publication details per language and 11 published profiles. Reviewed desktop and 390px mobile views, EN/ES navigation and publication filters in the browser. Syntax/config/path inspection found no missing local HTML resources; all nine source area descriptions match their transcriptions. No test suite was run, and no commit, push or deployment was performed.

Majo: Development Economics, confirmed by user. Sergio: areas pending and original draft status retained. Drive image: connector returned file not found; optional paper-photo blocks remain hidden until approved material is available. All nine area photographs have recorded public-domain or Creative Commons license metadata and public attribution.
