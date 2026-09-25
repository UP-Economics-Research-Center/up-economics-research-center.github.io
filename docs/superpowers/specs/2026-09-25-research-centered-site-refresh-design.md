# Research-Centered Site Refresh — Design

**Date:** 2026-09-25  
**Status:** Proposed; conversation design approved, awaiting written-spec review  
**Repository:** `UP-Economics-Research-Center/up-economics-research-center.github.io`

## Goal

Refocus the public UP Economics Research Center site around its people and research, with accurate researcher profiles, accessible conceptual artwork for research areas, and working links from every paper card to complete publication details.

## Agreed direction

- Keep the current GitHub Pages static site, its HTML/CSS design, and Decap CMS. The site continues to publish at the organization root URL.
- Keep Research, People, About, and a direct Contact action in the visitor-facing navigation. The wordmark links home; Contact targets the existing `about.html#contact` section.
- Remove the general Publications directory while retaining each paper’s individual details page. Research-area cards link directly to those pages. An old `/publications.html` URL redirects to the Research area index so existing links have a useful destination.
- Keep News and Seminars out of the public site, search, and CMS for now. Leave the internal Google Sites seminar portal and existing source records untouched; do not migrate or expose its content.
- Preserve existing site assets and the responsive design. Add only assets selected for this approved direction.
- Replace the home-page video with the Center-approved YouTube video `https://www.youtube.com/watch?v=ISvo7S30of4`, keeping muted autoplay and the existing reduced-motion fallback.

## People

- Match the current Center source page’s eleven listed people and copy each individual research biography from that page, preserving its person-specific meaning and factual detail. Make no unsupported additions.
- Order lead researchers as Akito Kamei, Esteban Colla de Robertis, Eugenio Gómez Alatorre, Maria Jose Favela, and Arnulfo Rodríguez Hernández. Add an explicit numeric display-order field to the CMS so the directory does not depend on filenames.
- Use the public name `Maria Jose Favela` as previously corrected by the Center. Do not show the nickname “Majo” as her directory name.
- Keep `content/people/sergio.json` as an unpublished draft; do not render a Sergio card because he is not on the current Center source page.
- Use a person’s current canonical profile URL when available. Use the official Universidad Panamericana page for Esteban, as selected by the Center. The existing People source points to Eugenio’s personal site at `https://eugeniogomeza.github.io/eugeniogomez/`; verify that this is still his preferred current link before publication.
- Do not show Esteban’s outdated portrait. Check the provided Drive item for a current individual portrait; if it does not contain one, leave the portrait out until a current approved image is supplied. Retain all other existing image assets unless a verified replacement is approved.

## Research and publications

- The Research hub becomes a responsive set of nine area cards. Each area page presents the same area illustration at a larger size, followed by its current summary, projects, researchers, and linked papers.
- Show every paper within its linked research area(s). Link each paper card to its existing generated detail route, which contains the complete abstract, complete author byline, verified metadata, and available canonical/download links.
- Preserve the publication’s exact complete author list and official order on its detail page. In research-area cards, put identified UP researcher(s) first; follow them with “with” and the remaining authors in their official relative order. Determine Center researchers by stable `person_id` associations, not name guessing. If a paper has no linked current UP researcher, retain its complete source author order without inventing a Center affiliation.
- Associate all existing publication author records with current Center people through CMS relations where applicable. Leave outside collaborators as authors without a Center person relation.

## Visual direction

- Create nine locally stored, original SVG line illustrations, one for each research area. The drawings should feel like refined architectural concept sketches: thin, precise but expressive lines, distinct motifs, open negative space, and no large filled shapes.
- Use the existing palette: ink `#242126`, wine `#8A1538`, warm paper `#F7F5F2`, and sparing gold `#BA9357`. Keep the SVG backgrounds transparent so they sit naturally in the existing pages.
- Use each drawing as a decorative area marker on the Research hub and a larger editorial illustration on its area page. Area titles and descriptions remain visible text; decorative SVGs use empty alternative text.
- Add a favicon set based on a geometric ivory `E` on a wine square, echoing the current wordmark accent. Deliver a root-level SVG, an `.ico` fallback, and a 180px Apple touch PNG from the same artwork. Include root-relative icon links on the public page sources, the CMS entry page, and publication detail template; copy the icon assets into the static build. Do not use the rejected book-and-arch concept asset.
- Add a Home-page research highlight using the provided people/article image and the existing record `gender-education-farm-succession-western-parana`. The image and call to action link to that paper’s internal details page. Store the image in the project and provide CMS fields for image, alternative text, credit/source, and a relation to the publication record.
- Keep the people/article image separate from the conceptual area illustrations. Confirm image identity, resolution, share access, and reuse permission before putting it in the public build. If the Drive file is not accessible to the editor or is not suitable, request an accessible approved file before publishing the highlight.

## Contact and CMS

- Move the original Center contact email and institutional address into the public Contact area on the new site. Make Contact reachable from the primary navigation and retain a contact link in the footer.
- Extend the existing Decap schema for people ordering, the Home research highlight, and campus video poster/alternative text. Use a relation field to select an existing publication so the feature cannot point to a guessed URL.
- Set the campus video ID to `ISvo7S30of4`. Update its local poster, alternative text, caption, accessible iframe title, and “Watch on YouTube” link to match the new film. Add CMS fields for the local poster and its alternative text so later video updates can keep the thumbnail accurate. Keep the CMS video ID, caption, and poster synchronized with the generated embed/link.
- Configure publication author relations so the build can distinguish Center people from external coauthors and format area-card bylines consistently while retaining the official full author metadata.
- Remove News and Seminars from Decap for this public-site period. Do not delete any existing content/source files as part of this change.
- Update README editor instructions to describe the current, simpler Research/People/About workflow, the direct-publishing behavior already configured, image accessibility/source requirements, and how papers are reached through research areas.

## Implementation boundaries

- Keep the HTML and shared CSS as the presentation source of truth. Update generated navigation consistently on the canonical pages and their design-source counterparts.
- Keep the video muted, inline, and set to autoplay on the normal motion path. Preserve the current click-to-play behavior when reduced motion is requested, as well as visible player controls. Use the new film’s thumbnail as the local poster.
- Keep generated publication detail routes under `/publications/<slug>/`; do not generate or index the old publication listing. Keep the legacy `/publications.html` location as a redirect only.
- Exclude News and Seminars pages, data feeds, CMS collections, and search records from the public build. Preserve the original source files and the separate internal seminar portal.
- No replacement of current media with generated photographs. The nine requested conceptual SVG sketches are new custom illustrations; the user-provided feature photograph remains authentic source media.
- No new runtime dependency, test suite, or automated test files. Perform a focused static build and manual checks for content paths, route links, author rendering, accessibility, and mobile layout when implementing.
- The implementation must not publish OAuth secrets or other non-project files.

## Acceptance criteria

1. The public navigation and footer contain no News, Seminars, or Publications directory link. Contact is easy to reach; Home is reachable by the wordmark.
2. The internal seminar portal remains unchanged and no seminar/news content or feed is emitted in the public artifact.
3. All eleven source-listed researcher profiles use the approved names, distinct source-backed biographies, functional profile links where available, and the requested lead-researcher order. Sergio remains unpublished.
4. Esteban’s old portrait is absent. A new portrait is used only if the supplied image is identified as current and approved.
5. Nine distinct local SVG sketches appear on the Research hub and at larger size on their corresponding detail pages, with the agreed palette and accessible decorative treatment.
6. Home contains the approved research highlight image linked to the existing farm-succession paper detail route; the paper itself retains a complete source-author byline.
7. All published papers remain reachable from their research areas; cards prioritize linked UP researchers and use “with” for remaining coauthors, while details preserve the full official author order.
8. An old `/publications.html` visit redirects to the Research index without breaking any individual paper detail URL.
9. The About/Contact page presents the original approved email and address, and Decap exposes the agreed editorial fields without exposing private content.
10. The new video ID, embedded player, muted autoplay settings, reduced-motion fallback, title, poster, caption, and direct YouTube link all refer to the approved video; Decap exposes the poster and alternative text with the video ID.
11. The favicon appears consistently on the home page, section pages, CMS, and generated paper detail routes, including on mobile browser tabs/home screens.
12. Manual review confirms page paths, internal links, keyboard navigation, mobile rendering, and the static build output. No automated tests are added or run.

## Sources and remaining content check

- Current Center people, research descriptions, and original contact information: <https://sites.google.com/view/akitokamei/up-economics-research>
- Esteban’s selected official UP profile: <https://www.up.edu.mx/en/investigacion/esteban-colla-de-robertis/>
- Eugenio’s personal profile candidate in the existing People source: <https://eugeniogomeza.github.io/eugeniogomez/>. Confirm it remains the preferred current link before publication.
- Feature image: user-provided Drive item `<https://drive.google.com/open?id=1t8vYzwhCzM3XeRZ7G-gd92lqcpBp8FdA&usp=drive_fs>`. Its contents were not accessible to the current web inspection tool; image identity and reuse permission remain to be checked before publication.
- Home video selected by the Center: <https://www.youtube.com/watch?v=ISvo7S30of4>. YouTube page metadata could not be fetched during planning; verify its title and retrieve its matching thumbnail when implementing.
- Internal seminar portal: <https://sites.google.com/up.edu.mx/up-econresearchcenter-portal/seminar>. It remains internal and is not part of this migration.
