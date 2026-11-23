# Seminar import repair — 23 November 2026

## Confirmed cause

Archivo contains three checked November 27 presentations. Rows 2–3 share the
original November ID, while row 4 carries a different copied legacy ID. The old
importer rejects the entire source with “presentations on the same date must share
ID de sesión”. This is separate from GitHub scheduled runs arriving hours apart.

## Released change

- Group solely by the editorial date. Ignore and stop requiring ID de sesión.
- Keep the three originally released date anchors in versioned configuration,
  not in spreadsheet cells. All other dates get deterministic date-based anchors.
- Report invalid published presentations and duplicates with their Archivo row
  and presentation name; report missing editorial headers by name.
- Keep whole-source validation and validated last-deployment recovery. Do not
  silently skip invalid checked presentations or alter the source workbook.
- Supply a private Google Apps Script edit trigger plus 30-minute safety timer.
  Its owner authorization is a separate activation step; the native GitHub
  schedule remains best-effort until and after that activation.

## Inspection

The real source import at 2026-11-23T19:27:47Z succeeded without editing the sheet:

| Date | Checked presentations |
| --- | --- |
| 2026-11-27 | José Miguel Montoya; Santiago Robles; Dr. Juan Carlos Perez |
| 2027-01-15 | Sandro Navarro-Castañeda |
| 2027-02-12 | Sergio Rodríguez García |
| 2027-03-12 | Akito, y Esteban |

The bilingual static build succeeded with 60 search records, 21 publication pages
and 15 people. Inspected the generated feed and both seminar pages. Python AST,
JSON, Apps Script JavaScript syntax and diff whitespace inspection passed.
No tests ran. No content, translations, times or locations were inferred.
No independent critic participated.

Production deployment is verified separately through the release PR, Actions and
the live feed. Google trigger activation requires the private setup in
[seminar-refresh-setup.md](seminar-refresh-setup.md); do not claim it is active
without an externally triggered deployment.
