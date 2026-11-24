# Automatic seminar refresh activation — 24 November 2026 (UTC)

## Active configuration

- Created the private standalone Google Apps Script project **UP ERC seminar
  refresh** under the previously approved institutional Google editing account.
- Saved exactly `tools/seminar_refresh.gs`; no token is embedded in the code.
- The owner confirmed GitHub access and supplied a new fine-grained token directly
  to the private `GITHUB_ACTIONS_TOKEN` Script Property. Its resource owner is
  UP-Economics-Research-Center, its sole repository is the website, and its only
  permissions are Actions read/write plus mandatory metadata read.
- Verified token expiry in GitHub: **24 November 2027**. Renewal remains an owner
  maintenance requirement; do not describe this token as permanent.
- Ran `installSeminarRefresh` successfully at 2026-11-24T05:00:46–49Z.
- Read back both installed triggers: `refreshSeminarsOnEdit` is a spreadsheet
  **On edit** trigger, and `requestSeminarRefresh` is **Every 30 minutes**.
- Changed both triggers' failure notifications from daily to **immediately**.

No source spreadsheet cells, publication checkboxes, translations or times were
changed to activate the integration. Script/trigger ownership is private; sharing
the public workbook does not share this standalone script's properties.

## Additional deployment failure discovered

The Google script successfully dispatched workflow run
[45330296764](https://github.com/UP-Economics-Research-Center/up-economics-research-center.github.io/actions/runs/45330296764).
Its importer and build succeeded. Upload finalized artifact `14891946079` at
05:01:07.276Z; deployment's immediate lookup reported zero artifacts at
05:01:07.807Z. A subsequent API read found the correct, unexpired `github-pages`
artifact attached to the same run. Thus a successful import/dispatch alone was
not sufficient evidence of successful website publication.

Remediation:

- Update the Pages pipeline's official actions to their maintained Node 24
  versions; use `deploy-pages@v5.0.1`.
- Add an explicit, bounded readiness gate for the **exact ID returned by this
  run's upload**, with narrowly scoped Actions read permission.
- If the artifact does not appear in this run's artifact list within two minutes,
  fail visibly without attempting publication. Do not add an arbitrary fixed
  sleep or redeploy an artifact from another run.
- Retain validated seminar-feed recovery and its final failed-import signal.

## Verification

Python AST, workflow YAML and whitespace inspection are performed before release.
No tests run, per project instructions. Verification of the new pipeline and a
fresh Google-script dispatch is recorded in the release PR and live public feed,
not inferred from script installation or source-code presence alone.
