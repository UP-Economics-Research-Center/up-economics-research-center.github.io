# Institutional typography — 26 October 2026

User request: implement the supplied fonts and organize them following https://www.up.edu.mx/marca-institucional/.

Reference review: the official brand page displays Panamericana and Seravek specimens. Its FAQs specify Panamericana as the primary institutional family for headings and descriptive text. For this website, Panamericana is assigned to content headings; Seravek is assigned to paragraphs, plain-text navigation identification and controls. This is typography integration into the approved layout.

Original upload directories were moved into `design/assets/fonts/panamericana/` and `design/assets/fonts/seravek/`; original bytes, names and license retained. Inventory/SHA-256 recorded separately. All 18 static WOFF2 faces registered locally with real OS/2 weights and italic styles, including Seravek Medium at 600. Legacy variable-font weights are mapped to supplied weights. Font display uses swap and system fallbacks; no remote font hosting or new build dependency. CMS content previews use the shared CSS. Existing raster publication cards and images are preserved.

The supplied Seravek desktop agreement restricts web linking, so the user was asked specifically about institutional web authorization and replied “Sí, tenemos autorización web”. That confirmation is the recorded authorization; the desktop agreement is not represented as a web grant. No open-license assertion.

Validation: bilingual static build succeeded. Local Chrome review confirmed Panamericana computed family on headings, Seravek on body, with no horizontal overflow on desktop Home/Health/Publications and Spanish People; mobile Home, Health, Spanish People and Publications also checked at 390px without horizontal overflow. Final checks and browser evidence are recorded in the working session. No test suite run per AGENTS.md. Source/reference files and existing unpublished local work preserved.

Implementation branch: `codex/institutional-fonts-2026-10-26`, active integration worktree `.worktrees/pending4-production-2026-10-26`. Local preview: http://localhost:8790/. The user subsequently authorized production publication of this implementation and the final Center identity; see center-logo-proposal-2026-10-26.md.

Follow-up corrections requested by the user: remove inherited all-bold styling, keep primary heading/slogan at Regular, simplify controls, remove the site-created square/E icon, and review brand architecture/imagery. See `brand-interface-review-2026-10-26.md` for the current decision.
