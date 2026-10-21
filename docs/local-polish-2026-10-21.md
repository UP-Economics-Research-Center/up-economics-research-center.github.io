# Local production-polish fixes — 21 October 2026

Status: implemented locally, uncommitted and unpushed. Production is unchanged.

The changes use the existing clean release worktree at `.worktrees/site-release-2026-10-19`, based on `b2ce51fd0e44a039ddf3cf301dc5d3f18f779191`. Its baseline source tree matches the audited production revision. The older, modified root checkout was not used for presentation changes.

## Changes

- A08: stack all archive filter fields at widths up to 600px; native selects, labels, URL state and keyboard operation remain in place.
- A09: when the published archive contains no Policy Briefs, show a truthful bilingual explanation. Keep generic guidance for other empty filters and the existing Clear filters control.
- A11: describe currently published research in the publication search suggestion, without advertising hidden working papers.
- A16: add bilingual page descriptions to Home, Research, People, Publications, Seminars and Media; add correct production canonical URLs, including public identities for legacy design routes. Preserve publication-detail descriptions. Legal/credit pages receive their own existing summaries rather than inheriting Research copy. The query-driven research-area route is excluded from generic canonical generation so distinct areas are not collapsed to one URL.
- A17: repair Isabel Ruiz's incomplete English sentence without adding factual claims; Spanish copy is unchanged.
- A18: translate the generated video action to “Reproducir” for the actual editorial video title.
- A19: use a visible date separator and localized readable Media dates, retaining `datetime`; the undated podcast remains undated.
- Related metadata correction: retain distinct English/Spanish article alternate links. The old broad URL replacement changed the English alternate on Spanish article pages to Spanish.

Review/approval notes, legal draft status, media permission records, publication visibility, real assets, approved composition and account permissions were preserved. No dependencies, public API or CMS fields were added.

## Verification

The static build completed with 53 search records, 21 publication pages and 14 people. JavaScript syntax and diff whitespace checks passed. No test suite ran, following project instructions.

Manual local browser checks covered the archive in EN/ES at 320, 390, 1024 and 1440px, with no horizontal document overflow. Year/type controls were full-width on narrow screens (241px at 320px; 303px at 390px, allowing for scrollbar and layout padding). The screenshot confirmed complete Spanish year/type selections.

Keyboard language switching preserved the Policy Brief state. Clear filters restored 21 records and removed the empty explanation. Changing from a generic no-results search to Policy Brief updated the explanation. The Spanish Home accessible name read “Reproducir Reinventamos la Economía | Universidad Panamericana”; no video iframe existed before activation. Both profile languages, the corrected search suggestion and Media dates (“March 10, 2026” / “10 de marzo de 2026”) were read back in the browser.

Generated head markup was inspected for main pages, legal/credit pages and a representative article in both languages: one page description, one correct canonical URL, and distinct article alternate-language routes. Native 200% zoom, activated reduced motion and screen-reader review remain outside this verification.

## Preview

From this worktree:

```sh
python3 tools/build_site.py
python3 -m http.server 8792 --bind 127.0.0.1 --directory _site
```

Open <http://127.0.0.1:8792/es/publications.html?lang=es&type=Policy+brief> to review the changed mobile controls and empty state. Canonical URLs intentionally identify the production domain, even in a local preview.

Institutional approvals, access/recovery setup, Figma cleanup and security-report storage recovery remain separate outstanding work. Nothing in this local patch approves or publishes those items.

## Approved motion and underline refinement

The user approved a restrained local motion pass, then requested a review of underlines. Section/card entrances now use 12px movement over 440ms, with 0/45/90ms sibling staggering. They run once on entry and leave normal visible content as the base state. Keyboard focus cancels movement on the focused element's ancestors; direct anchor landings are preserved. Unsupported animation/observer APIs fall back to static content. Reduced-motion preference disables registration and cancels active entrances if changed while the page is open.

Home arrival timing is coordinated, menu/search opening uses a 180ms transition, and desktop buttons and gallery images have small hover/press feedback. Existing colors and crops remain the presentation baseline. People and Seminars now omit section navigation entirely, following the final user decision.

Underline rule: content links retain underlines (publication titles, linked researcher names, profile/publisher links, email, references, credits and search results). Navigation, language switches, wordmarks, breadcrumbs, section links, gallery cards, topic selectors and button-style actions omit them. Gallery title and topic hover rules were made consistent; keyboard focus remains visible. The fallback search description now also uses the corrected published-research wording.

Additional manual browser evidence: the gallery progressed from six entered/three pending cards to nine entered/zero pending; all nine settled to opacity 1 and no transform. No local-origin error was present in the bounded captured console excerpt. Desktop keyboard navigation focused the seminar target below the sticky strip; Spanish mobile selection focused the proposal heading at 266px, below the navigation ending at 218px. Menu/search used the expected opening animation; Escape closed each and returned focus to its trigger. Rendered underline categories matched the intended rule on Home, Research, People, Publications, Media and Privacy. Native reduced-motion activation remains unverified in this browser; source safeguards were inspected. The build and changed JavaScript syntax checks passed; no tests, commits, pushes or deployment ran.

## Section navigation removed and official legal references

The final user decision removes section controls completely from People and Seminars. Static menus, their controller and generated script inclusion are removed. The content retains its headings and section IDs, in the normal reading flow, with no sidebar column or floating button.

Home actions now use two equal columns above 480px, including Spanish labels; narrower phones stack the actions. Labels can wrap within each button without causing horizontal overflow.

The missing-public-full-text sentence is omitted when no download exists; actual article/download actions remain. The public draft/pending banner is removed. Privacy and Terms now reference the official UP publications in the selected language, rather than displaying locally authored policy drafts or transplanting unrelated provisions. Storage/rights pages retain factual site information; public review instructions and obsolete hosting/portrait descriptions were corrected. Internal review status remains draft with no invented reviewer/date. Earlier authored records are archived in `docs/legal-drafts-before-official-links-2026-10-21.json`; the source discrepancy is recorded in `docs/official-legal-sources-2026-10-21.md`.

The legal-link CMS block now supports an optional English URL (`url_en`), falling back to the main URL when absent or empty. README guidance is updated. The generated 86 HTML files contain zero copies of either missing-full-text message or either public draft banner. English/Spanish Privacy and Terms contain the matching official UP URLs. The CMS YAML parses, the static build reports 53 search records/21 publication pages/14 people, and JavaScript syntax/diff whitespace checks pass. No tests, commits, pushes, approval or deployment ran.
