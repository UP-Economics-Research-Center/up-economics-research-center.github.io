# UI and UX audit — 24 September 2026

## Scope and evidence
Reviewed all eight HTML pages, the shared stylesheet, shared navigation/search script, inline archive scripts, local assets, and font licensing.
Applied corrections directly to the mock. This is a source and behavior audit, not a complete accessibility conformance assessment.

## Shared corrections
- Replaced Ubuntu and tiny Arial university attribution with locally hosted Manrope variable (200–800). The university name is in title case: 14px desktop / 12px mobile.
- Brand: Economics 27px/800; Research Center 22px/500. Mobile uses 23px/19px, or 21px/17px on the narrowest breakpoint. The university name can wrap instead of shrinking.
- Navigation and search: 16px/600. Expanded mobile navigation starts at 1180px to make room for readable desktop navigation.
- Footer: brand 32px/27px, university 17px, navigation 18px, secondary information 15px. Phone brand 29px/24px, university 16px, links 17px.
- Headings combine medium and extra-bold weights; body prose stays regular. Burgundy highlights actions and selected words. Warm neutral surfaces retained.
- Made input and menu borders darker; focus rings use dark burgundy. Consistent control heights, corner radii, hover and keyboard-focus behavior.
- Added a keyboard skip link, a focusable main landmark, linked breadcrumbs, and a single h1 on every page.
- Headers and footers are identical across all pages except navigation current-page state.
- Internal navigation uses a right arrow instead of an external-link arrow.
- Centralized section search; added research-area matches, empty-query guidance and DOM-based result construction.

## Page-by-page review

| Page | Issues corrected | Remaining content dependency |
|---|---|---|
| Home | Stronger heading weight hierarchy, emphasized research description, shared larger brand/footer, consistent internal-link arrows | Concept photograph needs approved replacement |
| Research | Linked breadcrumb, consistent topic names, clearer row weight and navigation | Topic naming should be approved by Center |
| Research area | Replaced h2 hero with h1; dynamic document title; invalid route now falls back to area 01; removed editing instructions from public-facing copy; added useful directory links | Projects, affiliations and publications are not migrated |
| People | Numbered avatar badges replaced with initials; larger role text; consistent name weights; concise pending-profile copy | Names, roles and full profiles require confirmation |
| Publications | Visible filter labels, semantic submit form, announced result count, working year shortcuts; removed fictitious pagination and dead View record links | Six demo records remain; real files and metadata are pending |
| Seminars | Unified series headings, removed visual number blocks, clearer student-series separation, concise archive copy | Dates, speakers and historical materials not supplied |
| News | Added clear filters, live result count, form submission, working year shortcuts, accurate Related section link labels | Three demo updates remain |
| About | Linked Research/People in prose, corrected contact-section alignment, shared typography | Public contact and institutional description require confirmation |

## Contrast measurements
Calculated using the WCAG sRGB relative-luminance formula from declared CSS colors.

| Pair | Ratio |
|---|---:|
| Burgundy #8A1538 / white | 9.35:1 |
| Muted #69636A / ivory #F7F5F2 | 5.37:1 |
| Muted #69636A / footer #F3EFED | 5.11:1 |
| Seminar text #615A57 / sand #EEE7DC | 5.50:1 |
| Control border #84777D / white | 4.27:1 |
| Focus #63112C / ivory | 11.72:1 |
| Focus #63112C / sand | 10.38:1 |

These measured text pairs exceed the 4.5:1 normal-text threshold. Measured control/focus pairs exceed 3:1. This does not certify all possible rendered states.

## Checks run
- HTMLParser audit: balanced tags, one h1 per page, unique IDs, labeled controls, local file and fragment references.
- 251 local/page/asset references inspected across the eight pages; no missing local target or referenced fragment found.
- node --check: every inline script and shared navigation script.
- Node VM with DOM stubs: publication preset/reset/search-empty/year filtering; news result count/reset/search-empty/year filtering; valid and invalid area routes; research-area search and empty query.
- Exact header/footer comparison after normalizing current-page state.
- All of these checks passed.

## Verification limits and remaining work
Browser rendering is unavailable because the integrated browser blocks local-file previews. No screenshots, real-device layout checks, browser keyboard walkthrough, zoom/reflow check, or screen-reader check was completed. DOM-stub behavior checks do not prove real-browser behavior.
Search covers sections and research areas, not a full-text research repository.
Google Sites parity for typography, filtering and custom interactions remains to be resolved before publishing.
Unverified/demo records are still marked as such. No new research claims, publications, biographies or dates were invented.

## References
- Manrope font and license: https://github.com/google/fonts/tree/main/ofl/manrope
- Text contrast: https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
- UI contrast: https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html
