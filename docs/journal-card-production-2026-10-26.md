# Journal-card production release — 26 October 2026

The user approved the local presentation and explicitly requested production publication. This release replaces the images for all 20 published Journal article records with original Center bibliographic cards. It also removes the master’s-student invitation from the Health glasses project in both languages and uses the existing Team selection to omit Joy’s photo card there. Joy’s People profile, Health affiliation and glasses-project credit remain.

The card design follows the supplied white, black and wine reference. Title, journal, complete author names, year and DOI come from the existing records. No citation metadata was changed. The conference contribution is labeled Proceedings. No publisher logos or cover artwork were reused, and cards identify themselves as Center bibliographic cards. The new `original` image-rights state and CMS field distinguish this design from third-party permission. Real journal-cover permissions remain unconfirmed.

Previous images remain in the repository. The [asset register](publication-card-assets-2026-10-26.json) preserves the prior image fields and exact card layout/text for each publication. The script `tools/generate_publication_cards.py --apply` regenerates images after citation edits. Pillow and fonts are needed only in the authoring environment; the deployment build consumes saved PNGs with no added dependency.

## Verification

- Static build succeeded: 54 search records, 21 public publication pages, 15 People profiles.
- Both language publication feeds and archives use all 20 expected cards with original-design status.
- All local rendered image paths exist; no email artifacts or correspondence are copied into the public build.
- Health changes and retained Joy profile/project credit inspected in EN/ES.
- Publication non-image metadata compared to production baseline with no changes.
- Python AST, content JSON, CMS YAML and git diff syntax inspected.
- Tests were not run, per AGENTS.md. No automated browser screenshot or visual acceptance is claimed because saved browser permission denied localhost access. The generated card images were inspected directly, and the user approved the local presentation before requesting this release.

Private email drafts and sent-message receipts stay local and are excluded from this commit. Earlier local editorial and rights-review notes are preserved separately. No email is sent by the production build.
