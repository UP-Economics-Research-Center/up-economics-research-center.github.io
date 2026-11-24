# Seminar refresh: GitHub App migration — 24 November 2026

## Completed private-account configuration

- Organization-owned, private app: **UP ERC Seminar Refresh**, slug
  `up-erc-seminar-refresh`, app ID `5905208`.
- Installation `185404009` is restricted to
  `UP-Economics-Research-Center/up-economics-research-center.github.io`.
- Permissions are Actions read/write and mandatory metadata read only. No
  webhook, user OAuth, Contents write, administration or organization permission.
- The existing private institutional Google project now stores
  `GITHUB_APP_CLIENT_ID`, `GITHUB_APP_INSTALLATION_ID` and
  `GITHUB_APP_PRIVATE_KEY_BASE64`. The key was transferred directly from an
  owner-private file to private Script Properties; it was never placed in source,
  chat, tool arguments or deployment logs.
- Running script SHA-256:
  `c72e326cce6b066702c6b65ddd082967ee9e3e1eeebe45e278a07e285d52857d`,
  matching the committed `tools/seminar_refresh.gs`.
- The existing edit trigger, 30-minute timer and immediate script-failure
  notifications were preserved; the installer was not re-run.

The script signs an RS256 app JWT with clock-skew allowance, exchanges it for a
token restricted again to this repository and Actions write, and holds that token
only in memory. It mints a fresh token on every request, with no personal-token
fallback or persisted installation-token cache. No annual personal-token renewal
is needed; the long-lived app signing key still requires secure custody.

## Verified publication and retirement

1. [Run 45412836186](https://github.com/UP-Economics-Research-Center/up-economics-research-center.github.io/actions/runs/45412836186)
   was dispatched at **2026-11-24T14:19:40Z** by
   **`up-erc-seminar-refresh[bot]`** and completed successfully.
2. Deleted only the former **UP ERC seminar refresh** fine-grained personal token.
   GitHub then showed no fine-grained personal tokens for that account. Unrelated
   classic credentials and the organization-wide 366-day policy were unchanged.
3. Removed the old `GITHUB_ACTIONS_TOKEN` Script Property and saved the remaining
   app properties and refresh timestamp.
4. [Run 45413277751](https://github.com/UP-Economics-Research-Center/up-economics-research-center.github.io/actions/runs/45413277751)
   was dispatched at **2026-11-24T14:22:01Z** by the same app bot and succeeded
   after the personal token had been retired.

No spreadsheet cells, publication checkboxes, factual content or translations
were changed to exercise the integration. These were real refresh requests, not
artificial source edits. No automated tests ran, per project instructions.

## Follow-up: remove a remaining artifact-name lookup race

Review of an earlier native-timer run,
[45408507800](https://github.com/UP-Economics-Research-Center/up-economics-research-center.github.io/actions/runs/45408507800),
showed a successful fresh import and uploaded artifact, with REST readiness
confirmed at 13:56:05.295Z, followed by the deploy action's separate artifact-name
lookup reporting zero artifacts at 13:56:05.672Z. The earlier readiness gate and
action upgrade therefore did not fully eliminate that intermittent failure.

`tools/deploy_pages.py` removes the second lookup. It validates the exact upload
ID, name, expiry and owning workflow run, then calls GitHub's Pages deployment API
with that ID and the current Actions OIDC identity. It monitors the resulting
deployment, fails on terminal errors, and cancels unfinished publication on
timeout/interruption. API response bodies and OIDC tokens are not logged. No
dependency or extra permission was added.

Production verification of this follow-up is recorded in the release PR and live
feed after publication; the two app-authentication runs above predate that
deployment-helper change.
