/**
 * Private, standalone Google Apps Script. See docs/seminar-refresh-setup.md.
 * Never paste credentials into this file or deploy this project as a web app.
 */
const SEMINAR_WORKBOOK = '10-ZeGcNtUeQB5wXC0-f6FYuosoiduBeAyMvPtvR1KzI';
const SEMINAR_DISPATCH = 'https://api.github.com/repos/UP-Economics-Research-Center/up-economics-research-center.github.io/actions/workflows/pages.yml/dispatches';

function requestSeminarRefresh() {
  const properties = PropertiesService.getScriptProperties();
  const token = properties.getProperty('GITHUB_ACTIONS_TOKEN');
  if (!token) throw new Error('Set GITHUB_ACTIONS_TOKEN in this private project’s Script Properties.');
  const lock = LockService.getScriptLock();
  if (!lock.tryLock(1000)) return;
  try {
    // Coalesce a burst of cell edits; the timer also catches imports and API edits.
    const previous = Number(properties.getProperty('LAST_REQUESTED_AT') || 0);
    if (Date.now() - previous < 60000) return;
    const response = UrlFetchApp.fetch(SEMINAR_DISPATCH, {
      method: 'post',
      contentType: 'application/json',
      headers: {
        Authorization: 'Bearer ' + token,
        Accept: 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
      },
      payload: JSON.stringify({ ref: 'main' }),
      muteHttpExceptions: true,
    });
    if (response.getResponseCode() !== 204) {
      throw new Error('GitHub rejected the seminar refresh (HTTP ' + response.getResponseCode()
        + '). Check token expiry, repository access and Actions write permission.');
    }
    properties.setProperty('LAST_REQUESTED_AT', String(Date.now()));
  } finally {
    lock.releaseLock();
  }
}

function refreshSeminarsOnEdit(event) {
  if (event && event.range.getSheet().getName() === 'Archivo') requestSeminarRefresh();
}

function installSeminarRefresh() {
  // Verify access before installing triggers. Re-running setup replaces only ours.
  requestSeminarRefresh();
  const handlers = ['requestSeminarRefresh', 'refreshSeminarsOnEdit'];
  for (const trigger of ScriptApp.getProjectTriggers()) {
    if (handlers.includes(trigger.getHandlerFunction())) ScriptApp.deleteTrigger(trigger);
  }
  ScriptApp.newTrigger('refreshSeminarsOnEdit').forSpreadsheet(SEMINAR_WORKBOOK).onEdit().create();
  ScriptApp.newTrigger('requestSeminarRefresh').timeBased().everyMinutes(30).create();
}
