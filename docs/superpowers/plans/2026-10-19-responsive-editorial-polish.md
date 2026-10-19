# Responsive and editorial polish implementation plan

**Goal:** Resolve the complete design evaluation findings, update PR #19, and merge after successful checks as authorized by the user.

**Architecture:** Keep the existing shared CSS, static generator, localized HTML and publication filter. Preserve original assets, complete content, desktop ordering, and pending editorial/CMS approval notes. No dependencies or tests per project guidance; use build, syntax and browser inspection.

**Approved scope:** Fix People at tablet widths; correct the home publication category destination label; avoid broken words in mobile research cards; simplify publication breadcrumbs and mobile title scale; enlarge language targets; correct publication heading levels and title language metadata; add researcher-to-publications navigation using verified author IDs.

- [x] Update responsive CSS and home category label. Inspect People at 320/768/1024/desktop and long Research names in EN/ES.
- [x] Update publication markup, CMS title-language field, and researcher publication links/filter using exact author IDs. Inspect localized links, long titles, heading hierarchy and clear/reset behavior.
- [x] Build, inspect syntax/configuration and review the diff. Check representative desktop/mobile pages, preserve original media and unrelated untracked portraits.
- [x] Prepare the complete patch and PR #19 description for the authorized commit, push and merge. Confirm the review build before merging and verify deployment; GitHub records the final integration outcome.
