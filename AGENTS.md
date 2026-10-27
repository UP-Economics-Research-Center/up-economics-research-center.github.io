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
