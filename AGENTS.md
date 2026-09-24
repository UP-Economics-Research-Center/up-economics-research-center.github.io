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
