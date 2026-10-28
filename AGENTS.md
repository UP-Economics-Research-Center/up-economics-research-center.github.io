# Project guidance

## Purpose
This repository contains the visual mock and assets for the UP Economics Research Center website. Preserve the approved visual direction and existing assets unless the user asks for a redesign.

## Editing principles
- Keep the existing HTML and shared CSS as the source of truth for presentation.
- Make content editable through clear, named CMS fields and repeatable blocks suitable for non-technical editors.
- Do not publish sample, unverified, or demo content as fact. Preserve existing review/approval notes.
- Keep all assets locally referenced where possible; do not replace real media with generated imagery.
- Maintain responsive layouts, accessible labels, keyboard operation, and reduced-motion behavior.
- Explain any CMS workflow in plain language for economists and other non-technical editors.

## Project structure
- `design/`: current mock, shared styles, scripts, source media, and migration materials.
- `docs/`: design decisions and implementation plans.
- `admin/`: visual CMS configuration and editorial entry point.
- `content/`: CMS-managed content records.

## Changes and checks
- Avoid adding dependencies unless they are needed for the chosen hosting or CMS workflow.
- Do not run tests unless asked. For content/config changes, inspect paths and configuration syntax where feasible.
- Keep README instructions current when editor workflows or setup change.

## Design references and editorial review
- Consult `docs/design-references.md` for the design resources supplied by the team.
- Consult `docs/editorial-review-2026-10-15.md` for the latest review decisions and unresolved questions. Preserve the distinction between agreed direction and pending details.

## Latest approved editorial decisions — 26 October 2026
- Land tenure security and agrarian investments in the Peruvian Highlands belongs only to Agricultural Economics. Do not restore its Political Economy topic.
- The Health glasses project uses the supplied classroom/eyeglasses illustration, extended horizontally with AI at the user's express request. Retain the original and edited local files, disclose the extension in image credits, and use the existing project photo sizing (`image_fit: cover`). This is a specific authorization for this asset, not a general change to the image policy.
- In project researcher notes, lines starting with `with` / `con` identify external collaborators; keep them separate from the UP names and never prepend `and` / `y` to those lines.
- The home video uses the licensed international-trade port photograph as an illustrative thumbnail. Keep the video ID and include its photo attribution in the credit page.
- Release details and validation: `docs/health-editorial-release-2026-10-26.md`. Preserve unrelated local documentation and correspondence artifacts.

## Institutional typography — 26 October 2026
- Use the supplied local Panamericana family for content headings, and Seravek for body copy, plain-text navigation identification and controls. See `design/assets/fonts/README.md` and the UP brand reference in `docs/design-references.md`.
- Preserve the original TTF/OTF files, real weights and italics; Seravek Medium is weight 600. Do not restore Manrope or Ubuntu as the active site family.
- The user explicitly confirmed Seravek web authorization. Retain that decision separately from the supplied desktop agreement; no open-license claim or authorization for other projects is implied.
- Keep CSS as the source of truth, use local paths with `font-display: swap`, and verify heading wrapping/navigation in EN/ES on desktop and mobile after typography changes. No tests unless requested.

## Current typography and Center identity — 26 October 2026
- Use Regular for ordinary buttons, tags, filters, directory names and subheadings; meaningful semantic emphasis/selected states may use Medium/Semibold. Keep weight rules centralized. h1/h2 use Panamericana; h3–h6 and UI use Seravek. Do not restore blanket bold lists.
- The user authorized publication of the final oak-free typographic logo. Use live Seravek Medium (600) in two lines: UP Economics 30px and Research Center 26px on desktop, with proportional mobile sizing. Different line sizes explicitly supersede earlier equal-size requirements.
- Name is ink #242126; the smaller school affiliation is wine #7A1A37, without a decorative rule. Keep its bilingual CMS fields. No oak, boxes, detached monograms, or split Economics spelling in the signature. Do not restore earlier rejected drafts.
- SVG/PNG exports and UP icons are in design/assets/brand/center/. Source HTML/shared CSS controls header/footer presentation. Preserve the original institutional files and old drafts as historical references.
- Hero university eyebrow stays removed. Existing licensed photographs and the expressly approved glasses illustration remain.
- Official current wine #7A1A37 and gold #B9975B. The reviewed manual does not define a web button/tag component library. The site’s title-case/Regular layout is an editorial adaptation.
- Website publication approval does not certify a formal institutional logo. See docs/center-logo-proposal-2026-10-26.md and docs/brand-interface-review-2026-10-26.md. Preserve unrelated journal-cover review and correspondence artifacts.

## Temporary institutional identity — 28 October 2026
- Use the original red PNG supplied by Institutional Communications in header/footer, both languages. Preserve its pixels, colour and proportions; the CSS frame removes only the transparent canvas for display. White original retained unused.
- This supersedes the self-designed live Seravek Center mark and its icon links. Do not regenerate or restore them as the active identity. Only English artwork was supplied; do not invent a translated graphic.
- Institutional architecture remains pending Council approval in December. Source and hashes: docs/institutional-wordmark-2026-10-28.json.

## Signature scale and shared colour — 28 October 2026
- Remove the school affiliation below the supplied logo in both languages. No signature-affiliation CMS fields remain.
- Use the PNG's exact opaque artwork red #8D1838 for the website's primary accents, including buttons, links, focus and frames. Dark hover #71132D is derived from that red. This supersedes #7A1A37 as the active website accent; do not recolour source media.
- Header logo width: 240px desktop, 210px mobile, constrained to available space; footer 280px/240px. Keep proportions and original image bytes.
