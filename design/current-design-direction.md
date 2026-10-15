> **Current approved direction — 2026-09-25:** The public site is GitHub Pages at the organization root. Home features the new Universidad Panamericana film “Reinventamos la Economía” with muted autoplay, followed by a featured research item when an approved image is available. Research and People are the public focus; News and Seminars stay internal. Nine hand-drawn area sketches, the Manrope wordmark, shared responsive styles, and the wine-square `E` favicon are current. Individual publication detail pages stay available from research areas/search. Earlier mock descriptions below are historical notes where they differ from this direction.

# Current visual direction

This revision replaces the previous ticker, large 09 panel, blue-dominant backgrounds, serif headlines, and very small typography.

- Burgundy is the primary color. Warm white and neutral text carry the rest of the pages; gold is a minor accent.
- Home opens with the Center name, a short factual description, and a panoramic concept photograph below the text.
- The research directory uses open rows and generous spacing. Publications have a quieter reading layout. Seminars occupy a warm sand section with charcoal text and burgundy actions. Interior page titles use charcoal; the home title retains burgundy.
- Body copy is 18–20px; controls are normally 16px; dates and secondary metadata are 14–16px. The compact institutional wordmark is the only smaller text treatment.
- Motion is limited to a short initial entrance and subtle link/button feedback. No marquee, continuous image drift, or hidden scroll-dependent content. Reduced-motion preferences are respected.
- The shared stylesheet applies to every page. News and publication example records remain marked as demo. Existing unverified personnel data and the generated photograph still need replacement or confirmation before launch.

Open homepage-concept.html for the current visual mock. The mock remains local HTML, not a published Google Site.

## Mobile refinement

All eight pages now share an expandable mobile menu and search control below 1050px. Navigation supports Escape, outside-click dismissal, current-page indication, and native keyboard interaction. At phone widths, filters and search forms use one column, record lists stack, long names wrap, and touch controls are at least 44px high. Text inputs stay at 16px or above. Home title size and photo crop adapt to narrow screens. The former horizontal navigation strip is removed.

Markup and local references were checked. Visual browser validation remains unavailable because the integrated browser blocks local-file previews; device rendering has not been visually verified.

## Logo proposal and palette refinement

The proposed Center mark combines an open book with an architectural arch in burgundy. This is a design exploration, not an approved university identity. The generated PNG is used alongside live text in all eight headers, with a smaller mark on mobile. The original UP seal is not reproduced or replaced in institutional materials.

Section backgrounds alternate warm white, white, and sand. Burgundy remains on the home title, logo, primary actions, and navigation accents.

Logo asset: assets/erc-logo-concept.png. Generated using the built-in image generation tool.

Generation prompt:

Use case: logo-brand. Create a single polished logo symbol for the Economics Research Center at Universidad Panamericana. Symbol only, NO text or letters. Design a distinctive minimalist abstract open book whose three parallel horizontal editorial strokes subtly turn into an open architectural arch / exchange of ideas. Restrained academic identity, excellent optical balance, crisp geometric flat vector-like shapes, strong recognition at 40px. One solid burgundy ink #8A1538 only. Truly transparent background. Square canvas, symbol fills about 85 percent of canvas with equal margins. No gradients, no shadows, no mockup, no texture, no crest, no shield, no graph arrow, no currency signs. This is a proposed research center identity, not an official university seal. Aim for timeless contemporary editorial design.

## Revised typographic identity

The book-and-arch proposal was rejected. All eight headers now use a live-text wordmark in locally hosted Ubuntu Medium: Economics / Research Center, with a small burgundy square and a separate university attribution. The older PNG is retained only as an unused exploration. Typography scales down for mobile. Neutral section backgrounds from the previous revision remain.

## Current typography after detailed UI audit

Manrope replaces Ubuntu and the small Arial university line. The current wordmark combines an extra-bold Economics line with a medium Research Center line and a 14px university attribution (12px on mobile). Navigation is 16px; footer links are 18px desktop / 17px mobile and footer secondary text is 15px. Section headings combine regular/medium and bold weights with restrained burgundy accents.

Eight-page structural, local-link, contrast and DOM-stub behavior checks passed. Browser rendering remains unverified. See ui-ux-audit-2026-09-24.md for page-by-page findings and limits.

## Hero color adjustment

The home title now uses charcoal, retaining its bold/medium weight contrast. The secondary hero action is charcoal at rest. Burgundy is reserved for the primary button and university eyebrow in the hero.

## Search refinement

All pages share a labeled search panel with close/clear controls, quick links, debounced live results, relevance ordering and useful no-match suggestions. Escape returns focus to the opener; outside click dismisses the panel. Results are standard keyboard-accessible links. Search covers sections and research areas. Phone results stack in one column.

## Real media revision

Home now uses a click-to-play existing UP campus film instead of generated photography. People uses twelve source-backed entries and eight real portraits; four unavailable portraits retain initials. Media remains concentrated on Home and People, with future documentary imagery reserved for real project, event and news records. See media-direction.md and assets/media-sources.json.

## Completed people imagery and topic links

All twelve portraits are now present. Mini biographies accompany the profiles, with research-area links and reciprocal team links on all nine area views. Maria Jose Favela’s related topics are distinguished from documented team membership.
