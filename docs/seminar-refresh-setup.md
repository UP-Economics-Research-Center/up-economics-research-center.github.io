# Reliable seminar refresh trigger

The importer no longer reads the hidden spreadsheet IDs. That fix is independent
of scheduling. GitHub's native schedule remains a backup, not a delivery promise.

For unattended refresh without relying on a running computer, use the supplied
**private, standalone Google Apps Script**. It requests a deployment when someone
edits **Archivo**, with a 30-minute Google timer as a safety net for edits made by
imports/APIs and bursts of edits. GitHub still performs validation and publication;
no website credentials go into the workbook or the public site.

## One-time owner setup

1. In GitHub, create a **fine-grained personal access token**, owned by an
   institutional maintainer and limited to **this repository only**, with
   **Actions: Read and write** (and the automatically required metadata access).
   Complete organization approval if required. Set an appropriate expiry and a
   renewal reminder. Do not reuse a broad personal token.
2. Open <https://script.google.com/> using the institutional Google account that
   can edit the workbook. Create a **standalone project**, not a script shared with
   everyone who can view the public workbook.
3. Copy [`tools/seminar_refresh.gs`](../tools/seminar_refresh.gs) into its editor.
   Do not deploy it as a web app or make the project public.
4. In **Project Settings → Script Properties**, add `GITHUB_ACTIONS_TOKEN`.
   Paste the token there, never in the code, workbook cells, GitHub repository,
   screenshots or chat.
5. Run **installSeminarRefresh** once and authorize spreadsheet, trigger and
   external-request access. This requests an initial deployment and installs the
   edit trigger and timer. Re-running it replaces only this script's own triggers.
6. In GitHub Actions, verify a new **workflow_dispatch** run on **main**, a
   **fresh** Seminar schedule summary and successful Pages deployment. Confirm
   `/seminars-sheet.json` and both website languages reflect the workbook.
7. Set both Apps Script triggers' failure notifications to **Notify me immediately**.
   If a token expires or
   is revoked, renew the Script Property and run **requestSeminarRefresh** again.

After setup, editors only change **Archivo**, keep **Publicar** checked for
approved presentations and reload the website after deployment. Edits within one
minute are coalesced; the timer catches any change missed by that short window.
Invalid published content still retains the previous valid schedule and requires
correcting the row reported in Actions. Do not uncheck unrelated presentations.

## Operational limits and ownership

- This removes dependence on GitHub's *scheduled-event delivery*, not on GitHub
  deployment availability, Google availability or account authorization.
- Google triggers are best-effort too; neither provider guarantees instantaneous
  updates. GitHub queue time and deployment time still apply.
- Install triggers under the institutional maintainer's account. Triggers belong
  to their creator; a departing maintainer must transfer setup to a successor.
- To stop this integration, delete its two triggers and revoke its scoped token.
- **Activation — 24 November 2026 (UTC):** the institutional account owns the
  private “UP ERC seminar refresh” project. Its edit trigger and 30-minute timer
  are installed. A repository-scoped Actions read/write token is stored only in
  private Script Properties; metadata is its only other permission. It expires
  **24 November 2027**, the organization’s maximum permitted lifetime.
- The first Google-script dispatch reached GitHub successfully (run
  `45330296764`), exposing a separate Pages artifact-indexing failure. Deployment
  actions and an explicit artifact-readiness gate address that failure; completed
  deployment verification is recorded in the activation release notes.
- Renew the scoped token before **24 November 2027** and replace the private
  property. No service or token can be promised to work forever without maintenance.
