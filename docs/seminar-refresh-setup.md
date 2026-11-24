# Reliable seminar refresh trigger

The importer no longer reads the hidden spreadsheet IDs. That fix is independent
of scheduling. GitHub's native schedule remains a backup, not a delivery promise.

The **private, standalone Google Apps Script** requests deployment when someone
edits **Archivo**, with a 30-minute Google timer as a safety net for imports/API
edits and bursts of edits. GitHub still validates and publishes the site.

## Current status — 24 November 2026 (UTC)

- Both triggers are installed under the institutional Google account; failure
  notifications are **Notify me immediately**.
- The live script still uses the private `GITHUB_ACTIONS_TOKEN` personal token.
  It expires **24 November 2027** under the organization's 366-day maximum.
- The owner authorized migration to a GitHub App rather than weakening that policy.
- **UP ERC Seminar Refresh** (`up-erc-seminar-refresh`, app ID `5905208`) is
  registered under UP-Economics-Research-Center and installed as `185404009` on
  **only this repository**. Its only permissions are Actions read/write and
  mandatory metadata read. Webhooks and user authorization are disabled.
- The new source is prepared, but the app credentials and source have **not yet
  been connected to the live script**. Chrome reported an extension popup blocking
  the private settings page, including after user handoff. Do not claim app-based
  refresh is active until cutover and deployment verification succeed.
- Earlier personal-token activation and successful publication are recorded in
  [the activation notes](seminar-refresh-activation-2026-11-24.md).

## GitHub App credentials

For a new installation, register an organization-owned, private GitHub App with
**Actions: Read and write** only. Install it on this website repository only.
Do not request Contents, administration, organization or user permissions.
No webhook, callback URL, OAuth client secret or public web app is needed.

Keep the standalone Google project private. In **Project Settings → Script
Properties**, configure:

| Property | Value |
| --- | --- |
| `GITHUB_APP_CLIENT_ID` | The app's client ID from its GitHub settings. |
| `GITHUB_APP_INSTALLATION_ID` | The numeric installation ID from the installation settings URL. |
| `GITHUB_APP_PRIVATE_KEY_BASE64` | Base64-encoded, unencrypted **PKCS#8 DER** signing key, as one line. |

Generate a private key from the app's **Credentials** page. GitHub's downloaded
PEM needs a one-time format conversion for Apps Script's RSA signing utility:

```sh
umask 077
openssl pkcs8 -topk8 -nocrypt -in github-app.private-key.pem -outform DER \
  | openssl base64 -A > private-key-base64.txt
```

Protect both files with owner-only permissions. Transfer the converted value
directly into the private Script Property; never put it in source, workbook cells,
screenshots, chat or deployment logs. Store local migration material only in an
ignored, owner-private directory, not alongside publishable site assets.

## Cut over the existing private script

1. Leave the working personal token in place until verification succeeds. Add all
   three app properties before replacing the running script.
2. Copy the complete [`tools/seminar_refresh.gs`](../tools/seminar_refresh.gs) into
   the existing **UP ERC seminar refresh** project's editor and save. Do not deploy
   a web app or change project sharing.
3. Keep the existing edit/timer triggers: they already invoke the current source.
   Run **requestSeminarRefresh**, not the installer, for this migration. Re-running
   the installer would replace the triggers and reset their notification settings.
4. Confirm a new GitHub **workflow_dispatch** run on **main**, started by the app's
   bot identity, with a **fresh** import and successful Pages deployment. Read back
   `/seminars-sheet.json` and both languages against the checked source rows.
5. Only after success, revoke the old **UP ERC seminar refresh** personal token
   in GitHub and remove `GITHUB_ACTIONS_TOKEN` from private Script Properties.
   Do not revoke unrelated credentials.
6. Verify another app-triggered deployment after retirement of the personal token,
   then update README's activation status and record the successful run URLs.

The new source signs a short-lived app JWT and exchanges it for an installation
token restricted to this one repository and Actions write access. It obtains a
fresh token for every request, keeps it only in memory, and never falls back to a
personal token. There is no annual personal-token renewal after verified cutover.

For a completely new Google project, run **installSeminarRefresh** once after
setting the three app properties, authorize Google access, and set **both**
trigger failure notifications to **Notify me immediately**.

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
- Before cutover, renew the personal token before **24 November 2027** if migration
  has not completed. Pushing new source does not change the separate Google project.
- After cutover, the app key remains a sensitive, long-lived credential. Rotate it
  if compromised, revoked or affected by an ownership transition. App installation
  tokens expire after about an hour and are renewed automatically.
- To stop app-based refresh, remove its two Google triggers and suspend/uninstall
  only this app installation. Revoke its signing key when it is no longer needed.
- No service or key can be promised to work forever without maintenance.
