# Brand, typography and interface review — 26 October 2026

The user rejected the overly wide/heavy home title and header, asked to check buttons against the manual, and specifically requested review of brand architecture, oak textures and illustration guidance. This supersedes the first local typography preview; nothing in this round has been published.

## Evidence and interpretation

- Current brand site: https://www.up.edu.mx/marca-institucional/marca/ shows Panamericana and Seravek. Its FAQs specify Panamericana as primary. The older 243-page PDF linked through the official guide calls the primary type Laurentian (pages 30–31). Use the supplied Panamericana files, not a downloaded substitute.
- Full manual: https://www.dropbox.com/scl/fi/93odkq4ud55rmgt7b14zk/UP_Manual-de-marca.pdf?rlkey=qi09kpm6xlavsr7l63adyrs8a&dl=0. Institutional mark and incorrect uses are on pages 60–75; preserve official proportions and avoid noninstitutional symbols. Existing site name text is navigation identification, not an approved new institutional lockup. No formal Center logo or Communication Committee approval is claimed.
- The reviewed guide/manual give no web-button geometry or state specification. The use of regular Seravek labels, existing accessible control sizes/focus states and restrained presentation is this site's implementation, not a mandatory manual component.
- Official current color reference https://www.up.edu.mx/marca-institucional/ gives university wine #7A1A37 and gold #B9975B; shared tokens now use those values.
- https://www.up.edu.mx/instrucciones-de-instalacion/ recommends WOFF/WOFF2 for the web. Locally generated WOFF2 files retain all glyphs and original advance metrics, and originals remain. FontTools/Brotli were authoring utilities under /tmp only, not production dependencies. User-confirmed Seravek web authorization remains recorded separately from the desktop license.

## Diagnosis and changes

Chrome confirmed both supplied families loaded, h1 font-stretch 100% and no scale transform. The inherited October 16 blanket weight rule forced the home title and slogan to Bold. The supplied Panamericana Bold is materially wider than Regular at the same size; applying the old sans-serif bold treatment made the change look stretched. The initial broad weight mapping also made controls too heavy. This was a styling failure, not a wrong font filename.

The home title and slogan now use real Regular faces. Remaining emphasis uses real Medium/Semibold where appropriate, all 18 CSS weights match font metadata, and synthetic bold/italic is disabled. Navigation identification uses simple Seravek Regular text; the decorative square is removed from source templates. Buttons, action links and menu labels use Seravek Regular; focus behavior and touch target sizing remain. The supplied original files are unmodified; WOFF2 derivatives have matching glyph order and metrics.

The invented E favicon and old icons are retained only under internal `docs/legacy-brand-icons/`, excluded from public build. Public icon tags reference unaltered UP site PNGs; source URLs and hashes are in `institutional-brand-assets-2026-10-26.json`. No emblem was recreated, recolored or attached to a new Center lockup.

No new oak pattern or decoration is added. Active area imagery is photographic; unused legacy sketch assets are not restored. The supplied glasses illustration, extended with AI at the user's express request, remains the existing editorial exception. This does not constitute general approval to replace research photographs with illustrations. Formal identity assets/lockups for the Center must be supplied through the institution's approved branding process rather than designed ad hoc.

## Validation

Bilingual build and syntax/path inspection; Chrome review of the home title, header, slogan, buttons and mobile menu. Regular face/actual file weights checked; WOFF2 glyph and advance metrics checked against originals; responsive overflow, keyboard focus and controls inspected before completion. No test suite run per AGENTS.md. Local preview http://localhost:8790/; no production publication.

## Complete-manual and CSS cascade follow-up

The complete 243-page text was reviewed, including the final graphic/layout chapters, with relevant pages rendered for visual inspection. Additional references: 19–28 photography; 210–212 whitespace/grid; 213 graphic heads (Semibold, uppercase, 85% leading, tracking notation 10 and auto kerning); 214 highlights (Semibold/Bold, lowercase, tracking notation -5); 217 body Light allowed only when legible; 230 Seravek subheads; 236–239 editorial layouts, including web content explicitly on 239; 241 incorrect layouts. These graphic recipes can apply to web content, so they must not be dismissed as print-only. The site's title-case Regular headlines and comfortable leading are editorial web adaptations for local review, not a claim of literal compliance with every graphic recipe. No explicit button/tag radius or interaction-state specification was found. The illustration caution comes from the current website and project editorial policy, not a general ban in the older PDF.

The user identified home area links still looking bold. Legacy per-selector weight600 rules defeated generic Regular declarations across directories, topic links, filters, labels, badges, archive buttons, profile actions, search and footer labels. All legacy text weight declarations were removed from the shared CSS, preserving the 18 font-face descriptors. A single final weight system now defines Regular400 for ordinary UI, text and headings, and real Medium/Semibold600 only for semantic emphasis and selected states. Panamericana serves h1/h2; Seravek serves subheads h3–h6 as well as body/UI. Area/card names in strong elements explicitly use Regular; heading strong spans inherit their heading weight. No new button/tag shapes, tracking recipes or identities are invented.

Browser inspection after this correction covered 32 views: Home, Research, People, Publications, Health, a publication detail, Seminars and Privacy, EN/ES at 1440/390px. 1,224 selected UI/heading elements were inspected: no unexpected Medium weights in the reviewed controls/headings and no horizontal overflow. Semantic UP-author emphasis and selected language/pagination intentionally retain600. Source/font-face weight checks and the bilingual build remain required; no test suite was run.

## Requested next logo discussion

The user asks how a redesigned Center logo should work and whether the hero's Universidad Panamericana eyebrow is prescribed. The manual explicitly includes centers among first-level product descriptors (p196: Regular, black; schools/faculties/departments are the second level, Semibold in university wine). This is a basis for a proposal, not automatic institutional classification/approval of a new Center lockup. Recommend an unaltered official UP identity asset with a separate Center descriptor, preserving proportions and clear space; any formal lockup should use an approved institutional file. The plain hero eyebrow is editorial copy, not a mandated logo treatment. Once the official university identity is present in the header, omitting its repeated hero label is the proposed editorial simplification. No new logo implementation has been applied in this discussion.

## Superseding logo direction

The user subsequently requested a more distinctive Center design, explicitly removed the oak, and supplied a stacked-wordmark reference to create the Center's own typographic mark. The local proposal now follows that request; earlier oak-based signature recommendations above are historical. See `center-logo-proposal-2026-10-26.md`. Typography, button/tag weight corrections and the rest of this review remain.

## Release decision

The user authorized push to production after the final Seravek Medium two-line identity refinement (30px/26px, school below without rule). Earlier local-only status and identity proposals above describe the review history; the current implementation and authorization are in center-logo-proposal-2026-10-26.md. No formal institutional certification is claimed.
