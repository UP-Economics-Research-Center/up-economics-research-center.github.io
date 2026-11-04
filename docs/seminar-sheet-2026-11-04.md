# Google Sheets seminar schedule — 4 November 2026

## Current state — structured bilingual schedule

The current editing source is [Archivo](https://docs.google.com/spreadsheets/d/10-ZeGcNtUeQB5wXC0-f6FYuosoiduBeAyMvPtvR1KzI/edit#gid=2026110401), gid 2026110401. [Seminario](https://docs.google.com/spreadsheets/d/10-ZeGcNtUeQB5wXC0-f6FYuosoiduBeAyMvPtvR1KzI/edit#gid=1187319866) keeps the original public link and is now an upcoming-only formula view. Guía de edición is gid 2026110402; the hidden complete original backup is gid 2026110403. The current README describes the final schema/workflow; earlier sections below record the superseded prototype and access history.

There is one native date column and one optional native time column (CDMX). One source row represents one presentation; the importer groups checked rows sharing a date into a session. November has two presentations in one session, January one, February one. Each presentation has separate speaker, institution, ES/EN title/description/details, integer duration, format, room, campus, Zoom, RSVP and material fields. Existing session IDs are preserved, including when an old presentation is unchecked and replaced on the same date. Dates, times, durations, dropdowns and HTTPS links have native validation through row 997. No missing start times, locations, workshop speaker, paper title or URL was inferred.

The original duplicate date field was removed. Undated available slots and their original unconfirmed date references remain unchecked in Archivo. Description cells remain empty until source descriptions are supplied. The provided thesis/workshop titles have faithful English translations in their own columns, following the user's later request for bilingual text fields. Universidad de Pieura is preserved exactly. Zoom, RSVP and material are independent and each is visible only when filled. Missing translations fall back to original-language text; descriptions/details display an original-language notice.

The user selected hourly refresh plus manual refresh, and Swiss styling for the spreadsheet only. Native sheet styling uses Arial, a black/white grid, light alternate rows, restrained red group labels, fixed header rows/first three columns, column widths and wrapped text. Archivo has a filter. Formula output and session IDs have edit warnings; the ID column is hidden. Google Sheets autoRecalc is HOUR, and Seminario uses a native FILTER/SORT on dates >= TODAY() in America/Mexico_City. The real formula output was read back: four presentation rows, including both November rows. Past and undated rows remain in Archivo. No Apps Script, GitHub credential in the sheet, or per-edit webhook was added.

The real public Archivo CSV import and static build succeed: 3 sessions, 4 presentations, 58 search records, 21 publication pages, 15 people. EN/ES headings/search records use their respective title columns. Manual scenario inspections covered same-day/end-of-day/year-boundary grouping, time ordering, empty schedules, invalid date/time/duration/RSVP, inconsistent IDs, bilingual descriptions, original-language fallback, independent Zoom/RSVP/material links and unchanged fallback timestamps. An independent read-only code review found a parent-ID edge case (an unchecked original talk could lose its stored session ID) and a shared-name language-attribute issue. Both were corrected and inspected. No test suites were run.

Current web layout captures: [English desktop](seminar-sheet-2026-11-04/structured-en-1440.png) and [Spanish mobile](seminar-sheet-2026-11-04/structured-es-390.png). Spreadsheet native rendering was unavailable because the browser access host is unavailable and artifact_tool is not installed; native values, formula results, styles, dimensions and validation metadata were inspected instead. A native Table API attempt returned an internal error without applying changes; a filtered, banded native cell grid was used successfully. The original data backup was created before rewriting the view.

The user subsequently authorized publication and activation of this complete revision. The main-branch deployment workflow imports Archivo on hourly and manual builds; Guía de edición links to manual Actions refresh for maintainers. Deployment results are recorded in the release pull request and GitHub Actions. [GitHub documents possible scheduled-run delays and disabling schedules after 60 inactive days](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule). Imported feed JSON remains ignored and uncommitted.

## Historical prototype and implementation record

## Scope and implementation

Implementation checkout: `.worktrees/sheets-seminars-2026-11-04`, branch `codex/sheets-seminars`, released baseline `4bc28f2` (PR #42). Original checkout and pending changes preserved.

The [Seminario sheet](https://docs.google.com/spreadsheets/d/10-ZeGcNtUeQB5wXC0-f6FYuosoiduBeAyMvPtvR1KzI/edit?gid=1187319866#gid=1187319866) is the editing source. Keep the existing approved HTML/CSS, proposal form and bilingual navigation. Add Event date (`YYYY-MM-DD`) and Show on website (native checkbox) columns without replacing existing content. Checked named sessions with exact dates authorize publication without another site review. Available slots and tentative dates stay unchecked.

Initial sessions: November 27, 2026 (the two-part José Miguel Montoya / workshop agenda, one event); January 29, 2027 (Sandro Navarro-Castañeda de Universidad de Pieura, original spelling); February 26, 2027 (Sergio Rodríguez García). Preserve titles and supplied duration text; do not infer affiliations, start times or links. The three unassociated paper titles remain excluded.

The public CSV is imported during scheduled, pushed and manual deployments. JSON and HTML are generated locally; imports never change CMS records or create automatic commits. The separate `/seminars-sheet.json` contains deterministic IDs, event dates, original agenda, optional duration and the last successful refresh timestamp. The existing `/seminars.json` stays CMS-managed. A failed import recovers only from a validated feed from the last successful deployment; first activation fails closed if none exists. Actions warnings and its job summary expose recovery. A deliberately empty schedule is valid. The approximate hourly refresh may be delayed by GitHub Actions.

Upcoming sessions sort nearest first; archived sessions newest first. Build and browser use Mexico City calendar days, including all of today in upcoming. The browser regroups on open, midnight, visibility return, page restore and focus; no JavaScript visitors receive the last build's grouping. Original session text stays unchanged in both languages. Only interface labels and date formatting are translated. The full schedule link opens the supplied sheet.

## Sheet access and initial activation

Read verified through the connector: spreadsheet `10-ZeGcNtUeQB5wXC0-f6FYuosoiduBeAyMvPtvR1KzI`, tab `Seminario`, sheet ID `1187319866`, grid 997 × 26. Existing headers are B2 `Fecha`, C2 `Tema`; optional duration is D. Rows 3–5 contain the named sessions; rows 6–9 are available slots, with June's date tentative. Public CSV download succeeded without a Google sign-in.

**Initial editing blocker (resolved):** the personal account received HTTP 403, `The caller does not have permission`. After the user connected the UP account, the tool exposed explicit account selection. Selecting the UP connection returned `0251520@up.edu.mx` and the authorized sheet update succeeded. Browser access remains unavailable; sheet verification used native values, formatting and validation metadata.

Applied and verified sheet configuration:

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

G3:G997 is formatted as plain text, H3:H997 has native checkboxes, and I3:I997 has the modality dropdown. G3:G5 contain the approved dates and H3:H5 are checked; available slots are unchecked. The original B2:F12 values, formatting and chip metadata were compared before/after and are unchanged. Header notes explain publication authorization and how to fill participation fields. New columns have explicit widths and wrapped text. Native validation was also read back at row 997. Do not deploy preview feeds; the real CSV now supplies the generated feed.

I3:I997 has a dropdown with Presencial, En línea, Híbrida and Por confirmar. J contains the room or auditorium, optionally including building/campus; K contains the public attendee HTTPS link. Leave I:K blank for existing sessions until someone confirms their participation details. These fields are optional, so old valid feeds still recover correctly. The website shows translated format labels, a physical venue for in-person/hybrid sessions, and an online-access link for online/hybrid sessions. Unknown details show Por confirmar / To be confirmed. Session IDs do not change when participation details change. Conflicting room/format combinations or invalid online links reject a checked row's refresh instead of publishing misleading information.

The user identified `0251520@up.edu.mx` as the intended editing account. Earlier tool schemas did not expose account selection and continued returning the personal account. On retry, the tool schemas listed both accounts and accepted a connection selector; all final reads and the write used the verified UP account. No modality, physical venue or meeting link was invented for the three existing sessions.

The earlier real-network attempt correctly blocked activation for a missing `Event date` header and a 404 deployed fallback. After the authorized sheet edit, `python3 tools/seminar_sheet.py` imported the real public CSV successfully, and `python3 tools/build_site.py` succeeded with 57 search records, 21 publication pages and 15 people. The feed contains exactly the three approved dates; November has two agenda lines in one session. EN/ES output includes the three sessions and pending modality labels, with no available slots published. CMS records remain separate. Last successful real refresh: `2026-11-04T17:11:44+00:00`. Imported JSON remains ignored and uncommitted. The production website was not changed.

## Verification

No test suites were run, per project instructions. Python compilation, JavaScript syntax and workflow YAML inspection completed. A static build from a temporary preview CSV (the real public rows plus exactly the authorized G–H changes) produced 57 search records, 21 publication pages and 15 people. The preview is ignored and is **not evidence that the sheet itself was updated**.

Inspected JSON and EN/ES HTML: all three dates and original agenda text, November as one event, original Pieura spelling, optional durations, full schedule link, independent proposal URL, unchanged CMS feed and local script paths. Exact Spanish date labels and full schedule label checked. Manual scenario inspection: today remains upcoming; previous days archive newest first; December/January sorting; all unchecked gives a valid empty schedule; unchecked incomplete/tentative rows are excluded; checked impossible/non-ISO dates and checked tentative available slots reject the refresh; fallback retains the feed and timestamp exactly; no valid fallback blocks initial activation.

Inspected rendered layouts: [English desktop](seminar-sheet-2026-11-04/desktop-en.png), [Spanish desktop](seminar-sheet-2026-11-04/desktop-es.png), [Spanish mobile at 390px](seminar-sheet-2026-11-04/mobile-es.png), and [English mobile at 320px](seminar-sheet-2026-11-04/mobile-en-320.png). No clipping or horizontal overflow visible; shared navigation, typography, original logo and proposal form retained. The existing analytics consent panel is present in these fresh-browser captures.

Simulated browser time immediately before and after Mexico City midnight: November 27 moved from upcoming to past automatically; January and February remained upcoming. Before: upcoming `[2026-11-27, 2027-01-29, 2027-02-26]`, past `[]`. After: upcoming `[2027-01-29, 2027-02-26]`, past `[2026-11-27]`. This inspection used only local generated pages; no live browser account or Google Sheet was modified.

Independent read-only code review found one important recovery issue: an incomplete HTTP response could be accepted as a partial CSV, or a chunked-read exception could bypass recovery. Fixed by checking the advertised Content-Length against received bytes and converting HTTP client exceptions into import errors. Manual localhost response inspection accepted a complete three-session CSV, rejected a short Content-Length response as incomplete, and rejected truncated chunked data as `IncompleteRead`. Both failures now enter the same validated deployed-feed recovery path. No critical or minor findings remained in that review. The reviewer did not independently verify Google permissions, production CSV contents, Actions execution or live browser behavior; the evidence above comes from this implementation session. Sheet setup and real CSV import are now verified; actual Actions execution and deployment remain unverified until an authorized release.

No push, merge or deployment is part of this local implementation.

## Participation fields verification

Python compilation, the static build and diff whitespace inspection completed after adding the participation fields. Manual local scenario inspection covered Presencial with an auditorium, En línea with an HTTPS link, Híbrida with both, and blank details. EN/ES labels and the original room text were inspected. An unknown mode, a room attached to an online-only event and a non-HTTPS connection link were rejected. The prior valid feed without participation fields was accepted. Illustrative room names and example.org links were used only in temporary local inspection data; none were added to the actual sheet or a committed feed; the locally generated public feed now comes from the real sheet. Rendered the illustrative participation view at 1440px desktop and 390px mobile; labels, long auditorium text and online links remained readable without visible clipping. The illustrative page was removed by the final static rebuild. No test suite was run.

## Structured bilingual schedule revision

Authorized revision: replace the duplicate date fields with one validated native date; separate speaker/institution, bilingual titles/descriptions/agendas, duration, format, physical venue, campus, Zoom, RSVP and material links. Keep the approved website presentation. Apply Swiss typography and a disciplined black/white/red grid to the spreadsheet only. Keep hourly website refresh plus manual deployment when needed.

Editing model: Archivo is the complete editable source, including past sessions and unchecked slots. Seminario is a formula view containing only dated sessions on/after TODAY() in Mexico City, ordered nearest first. The original sheet is preserved in a hidden backup before restructuring. A guide tab explains the editing/publication flow. Existing titles are split from supplied speaker text without inferring missing titles, times, locations or links. The original complete agenda is retained. English cells contain only faithful translations of the supplied Spanish text; new descriptions remain blank until provided.

During final verification, concurrent user edits removed Archivo’s decorative first row and changed the thesis title to include its speaker. These edits were preserved. The importer now identifies the single complete named header within the first ten rows instead of requiring a fixed row number. The current header was observed in row 1; the importer no longer needs a fixed-row setting. No attempt was made to restore the deleted decorative row or overwrite the edited title. Native formula/validation ranges follow Google’s row-deletion adjustments.

## Publication authorization

The user explicitly authorized publishing and activating the prepared version. Release scope includes the structured source import, both languages, multiple presentations per date, conditional RSVP/Zoom/material links, static/browser date grouping, hourly plus manual deployment and validated-feed recovery. The current released baseline was fetched before release and remains 4bc28f2; no unrelated upstream changes need integrating. Original checkout changes remain untouched. Final pre-release real-sheet import and build succeeded (58 search records, 21 publication pages, 15 people). Python compilation, JavaScript syntax, YAML parsing and diff whitespace inspection passed. No test suites were run, per the project instruction.


## Searchable public archive — release scope addition

Before the release PR was merged, the user requested a navigable/searchable past-seminar archive on the website. Added a local archive search (accent-insensitive, bilingual text), year filter, session counts, six-session pagination, URL state and direct session/presentation links. Arrival at a deep-linked result reveals its archive page, and midnight regrouping updates the available years/search results. No-JavaScript output keeps the complete date-ordered archive while hiding inactive interactive controls. The approved filter/pagination styles are reused with responsive adjustments. The production dataset currently has no past dates; no invented archive entries are published.

Archive verification: local rendered inspection with the real three sessions and a simulated March 2027 clock showed page 2 containing November, accent-insensitive Rodriguez + year 2027 containing only February, and an unmatched query showing zero results and the clear-filter message. The copied inspection script used two sessions per page only to exercise pagination; production uses six. Mobile filters fit the narrow layout. Independent static review identified stale date hashes overriding saved filters/pages on reload; deliberate filtering/pagination now replace a seminar-specific hash with #archive. Local interaction inspection confirmed page 2 remains in the URL and a subsequent search retains its query with the neutral archive anchor. Temporary clock/pagination inspection files are removed by the final build and are not release artifacts. No test suite was run.

## Refresh frequency revision — 4 November 2026

The user authorized a free refresh every 30 minutes, replacing the original hourly website refresh. The production workflow now uses `0,30 * * * *`: minutes 00 and 30 of every hour. Scheduled runs may be delayed by GitHub Actions, especially at the start of an hour. Manual refresh remains available. This is a public repository using the standard `ubuntu-latest` runner; [GitHub documents that these executions are free](https://docs.github.com/en/billing/concepts/product-billing/github-actions). No paid service or new dependency was added. The spreadsheet’s hourly formula recalculation remains separate; website imports read all rows from Archivo directly.
