# Google Sheets seminar schedule — 4 November 2026

## Scope and implementation

Implementation checkout: `.worktrees/sheets-seminars-2026-11-04`, branch `codex/sheets-seminars`, released baseline `4bc28f2` (PR #42). Original checkout and pending changes preserved.

The [Seminario sheet](https://docs.google.com/spreadsheets/d/10-ZeGcNtUeQB5wXC0-f6FYuosoiduBeAyMvPtvR1KzI/edit?gid=1187319866#gid=1187319866) is the editing source. Keep the existing approved HTML/CSS, proposal form and bilingual navigation. Add Event date (`YYYY-MM-DD`) and Show on website (native checkbox) columns without replacing existing content. Checked named sessions with exact dates authorize publication without another site review. Available slots and tentative dates stay unchecked.

Initial sessions: November 27, 2026 (the two-part José Miguel Montoya / workshop agenda, one event); January 29, 2027 (Sandro Navarro-Castañeda de Universidad de Pieura, original spelling); February 26, 2027 (Sergio Rodríguez García). Preserve titles and supplied duration text; do not infer affiliations, start times or links. The three unassociated paper titles remain excluded.

The public CSV is imported during scheduled, pushed and manual deployments. JSON and HTML are generated locally; imports never change CMS records or create automatic commits. The separate `/seminars-sheet.json` contains deterministic IDs, event dates, original agenda, optional duration and the last successful refresh timestamp. The existing `/seminars.json` stays CMS-managed. A failed import recovers only from a validated feed from the last successful deployment; first activation fails closed if none exists. Actions warnings and its job summary expose recovery. A deliberately empty schedule is valid. The approximate hourly refresh may be delayed by GitHub Actions.

Upcoming sessions sort nearest first; archived sessions newest first. Build and browser use Mexico City calendar days, including all of today in upcoming. The browser regroups on open, midnight, visibility return, page restore and focus; no JavaScript visitors receive the last build's grouping. Original session text stays unchanged in both languages. Only interface labels and date formatting are translated. The full schedule link opens the supplied sheet.

## Sheet access and initial activation

Read verified through the connector: spreadsheet `10-ZeGcNtUeQB5wXC0-f6FYuosoiduBeAyMvPtvR1KzI`, tab `Seminario`, sheet ID `1187319866`, grid 997 × 26. Existing headers are B2 `Fecha`, C2 `Tema`; optional duration is D. Rows 3–5 contain the named sessions; rows 6–9 are available slots, with June's date tentative. Public CSV download succeeded without a Google sign-in.

**Sheet editing is blocked:** the Sheets API returned HTTP 403, `The caller does not have permission`. The connected Drive account is the personal account; the user confirmed that the sheet is shared with the UP account. Browser access is unavailable in this session. No cells were changed. This is an actual Google permission denial, not a request for publication approval.

Required owner change (or connect an account with edit access):

| Cells | Value |
| --- | --- |
| G2 | Event date |
| H2 | Show on website |
| G3 | 2026-11-27 |
| G4 | 2027-01-29 |
| G5 | 2027-02-26 |
| H3:H5 | Checked |
| H6:H997 | Unchecked |
| I2 | Modalidad |
| J2 | Salón / auditorio |
| K2 | Enlace de conexión |

Format G as plain text and H3:H997 as native checkboxes. Preserve B:F. The original CSV has neither new header, so a real first deployment is intentionally blocked. Do not deploy the preview feed or bypass this gate. Re-fetch the real sheet and confirm these controls before release.

For I3:I997, use a dropdown with Presencial, En línea, Híbrida and Por confirmar. J contains the room or auditorium, optionally including building/campus; K contains the public attendee HTTPS link. Leave I:K blank for existing sessions until someone confirms their participation details. These fields are optional, so old valid feeds still recover correctly. The website shows translated format labels, a physical venue for in-person/hybrid sessions, and an online-access link for online/hybrid sessions. Unknown details show Por confirmar / To be confirmed. Session IDs do not change when participation details change. Conflicting room/format combinations or invalid online links reject a checked row's refresh instead of publishing misleading information.

The user identified `0251520@up.edu.mx` as the intended editing account and reported reconnecting it. Subsequent connector profile reads still returned the personal account. Writing an email in the conversation does not provide an account-selection parameter to the Sheets tool. Account switching remains an external connection issue; no participation details or other cells have been written to the real sheet.

Final real-network import attempt confirmed the gate: the CSV was rejected for missing `Event date`, and the deployed fallback returned HTTP 404. The importer exited 1 without creating a feed at its requested temporary destination. The existing production site was not changed.

## Verification

No test suites were run, per project instructions. Python compilation, JavaScript syntax and workflow YAML inspection completed. A static build from a temporary preview CSV (the real public rows plus exactly the authorized G–H changes) produced 57 search records, 21 publication pages and 15 people. The preview is ignored and is **not evidence that the sheet itself was updated**.

Inspected JSON and EN/ES HTML: all three dates and original agenda text, November as one event, original Pieura spelling, optional durations, full schedule link, independent proposal URL, unchanged CMS feed and local script paths. Exact Spanish date labels and full schedule label checked. Manual scenario inspection: today remains upcoming; previous days archive newest first; December/January sorting; all unchecked gives a valid empty schedule; unchecked incomplete/tentative rows are excluded; checked impossible/non-ISO dates and checked tentative available slots reject the refresh; fallback retains the feed and timestamp exactly; no valid fallback blocks initial activation.

Inspected rendered layouts: [English desktop](seminar-sheet-2026-11-04/desktop-en.png), [Spanish desktop](seminar-sheet-2026-11-04/desktop-es.png), [Spanish mobile at 390px](seminar-sheet-2026-11-04/mobile-es.png), and [English mobile at 320px](seminar-sheet-2026-11-04/mobile-en-320.png). No clipping or horizontal overflow visible; shared navigation, typography, original logo and proposal form retained. The existing analytics consent panel is present in these fresh-browser captures.

Simulated browser time immediately before and after Mexico City midnight: November 27 moved from upcoming to past automatically; January and February remained upcoming. Before: upcoming `[2026-11-27, 2027-01-29, 2027-02-26]`, past `[]`. After: upcoming `[2027-01-29, 2027-02-26]`, past `[2026-11-27]`. This inspection used only local generated pages; no live browser account or Google Sheet was modified.

Independent read-only code review found one important recovery issue: an incomplete HTTP response could be accepted as a partial CSV, or a chunked-read exception could bypass recovery. Fixed by checking the advertised Content-Length against received bytes and converting HTTP client exceptions into import errors. Manual localhost response inspection accepted a complete three-session CSV, rejected a short Content-Length response as incomplete, and rejected truncated chunked data as `IncompleteRead`. Both failures now enter the same validated deployed-feed recovery path. No critical or minor findings remained in that review. The reviewer did not independently verify Google permissions, production CSV contents, Actions execution or live browser behavior; the evidence above comes from this implementation session. Actual Actions execution and deployment remain unverified until the owner completes sheet setup and authorizes release.

No push, merge or deployment is part of this local implementation.

## Participation fields verification

Python compilation, the static build and diff whitespace inspection completed after adding the participation fields. Manual local scenario inspection covered Presencial with an auditorium, En línea with an HTTPS link, Híbrida with both, and blank details. EN/ES labels and the original room text were inspected. An unknown mode, a room attached to an online-only event and a non-HTTPS connection link were rejected. The prior valid feed without participation fields was accepted. Illustrative room names and example.org links were used only in temporary local inspection data; none were added to the actual sheet or a committed/public feed. Rendered the illustrative participation view at 1440px desktop and 390px mobile; labels, long auditorium text and online links remained readable without visible clipping. The illustrative page was removed by the final static rebuild. No test suite was run.
