# Econ Site

Static website for the **UP Economics Research Center, Universidad Panamericana**. The public site is <https://up-economics-research-center.github.io/>.

## How the site is built

- `index.html`, `design/`, and local media define the presentation.
- `content/` contains Decap CMS records. Only records with `published: true` appear publicly.
- `tools/build_site.py` validates editorial records and builds the complete static site into `_site/`.
- `.github/workflows/pages.yml` builds `_site/` and deploys it to GitHub Pages after a change is committed to `main`.
- `admin/` contains the Decap CMS entry point; `oauth-worker/` contains the GitHub sign-in service source.

Build locally with Python 3 (no packages required):

```sh
python3 tools/build_site.py
python3 -m http.server --directory _site 8000
```

Then open <http://localhost:8000/>. Do not edit generated `_site/` files; change the HTML/CSS or the records they are generated from.

## Using Decap CMS

The CMS is at <https://up-economics-research-center.github.io/admin/>. GitHub sign-in was verified in the published editor on 2026-10-15. Only GitHub accounts invited to this repository with write access can edit. The invite must be accepted first; sign-in alone does not grant access.

1. Open `/admin/` and choose **Login with GitHub**.
2. Choose Researchers, Research Areas, Publications, Site Settings, or Home scope and contact.
3. Edit the fields and use the preview pane to review the record. For Researchers, keep the complete name in **Name** and enter the preferred abbreviated form in **Public display name / Nombre público**. If that field is empty, the complete name appears. Publication citations keep their own author names and citation order. Research areas are selected from the existing area list. You do not need to edit HTML or CSS.
4. For a new record, set its “Publish this…” switch to true when it is ready. Save the record in Decap; the change commits directly to `main` and is deployed by GitHub Actions. The live site updates after the Pages workflow succeeds. Editors publish directly to `main`; no pull request is required.
5. If a Pages deployment fails, check the workflow in the repository’s **Actions** tab and ask a repository maintainer for help.

### Seminar information and proposals

The independent `/seminars.html` page and its Spanish version are linked from the header and footer. Edit the introduction, usual schedule, session confirmation note, proposal types and form link in **Home scope, contact and seminar information**. Fill both language fields. The official UP proposal form is in Spanish; the link says so in both languages. Its description confirmed the usual monthly schedule on 2026-10-16. Verify changes against the source before editing the schedule. Add individual confirmed events in the **Seminars** collection; upcoming and past entries are separated automatically. No event dates or speakers are currently entered.

### Adding a publication

Enter the title, author names in citation order, abstract, year, and type. A Reference URL is optional and can point to any page or document that supports the record; it does not need to be a personal website. Add a DOI or canonical publisher page when one exists, select research areas from the existing list, and add a PDF only when the Center has permission to distribute it. The site makes a detail page with the abstract, authors, citation details, topic links, publisher page, and optional PDF download. A paper appears when its `published` field is true and the Pages deployment succeeds.

### Home page, video, and featured paper

In Site Settings, edit the home heading and introduction. The featured-paper relation selects an existing published paper; upload its approved image and add alternative text, credit, and source URL before publishing the image. Without an image, the feature stays hidden. The campus video fields control the YouTube ID, title, poster, poster alternative text, and caption. The player starts muted and automatically when motion is allowed; reduced-motion settings require a click.

### Adding images

Use the CMS media chooser and provide useful alternative text. Confirm permission before uploading files. Do not upload generated or unapproved portraits. The original media register is in `design/assets/media-sources.json`; it is not copied to the public build.

### Content review

Keep affiliations, biographies, citations, and contact details accurate and reviewable. Seminar portal records remain internal and are not shown on the public website. The optional Reference URL can point to any supporting source, not only a researcher’s personal site. Leave uncertain entries unpublished and resolve open questions before setting them to published. When a record has a Reference URL, recheck it before changing the related facts.

## Owner setup: GitHub sign-in

These one-time steps require an organization/repository maintainer and access to the Center’s Cloudflare account. Until they are complete, `/admin/` displays a setup notice and editors cannot sign in.

1. Create a **GitHub OAuth App** under the organization. Set its callback URL to `https://YOUR-WORKER.workers.dev/callback`. The Worker handles only the repository’s public content and requests the `public_repo` scope.
2. In `oauth-worker/wrangler.toml`, set `SITE_ORIGIN` to `https://up-economics-research-center.github.io`. Deploy the Worker from the `oauth-worker/` directory using Cloudflare Wrangler.
3. Set the Worker secrets with Wrangler: `GITHUB_CLIENT_ID`, `GITHUB_CLIENT_SECRET`, and a long random `STATE_SIGNING_SECRET`. Never commit these values or put the client secret in Decap configuration.
4. In `admin/config.yml`, replace `backend.base_url` with the deployed Worker origin, for example `https://YOUR-WORKER.workers.dev` (without a trailing slash). Commit and merge this configuration change so GitHub Pages deploys it.
5. Invite each editor to the public site repository with write access; they must accept the invitation. Keep force-push and branch-deletion protection, and disable required pull-request reviews on `main` so Decap can commit directly.
6. Ask an invited editor to sign in at `/admin/`, make an approved small change, and confirm it appears after the Pages deployment succeeds.

If GitHub returns an access or organization-permission error, ask an organization owner to invite the editor or adjust repository access. Never share OAuth secrets or personal access tokens in commits or chat. To rotate credentials, update the Worker secret bindings and redeploy it; do not add credentials to this repository.

## Design guidance

Team-supplied design resources are saved in [docs/design-references.md](docs/design-references.md). The current comment-by-comment review, including agreed image treatment and the proposed research-area order, is tracked in [docs/editorial-review-2026-10-15.md](docs/editorial-review-2026-10-15.md).

Preserve the existing HTML, shared styles, and local media unless the Center approves a redesign. Keep public copy and paper metadata sourced. Editors should change content fields; the implementation plan and design decisions are in `docs/`.

### Bilingual site and October 2026 editorial changes

English is the default. **EN / ES** switches between complete static pages and remembers the reader's explicit selection when browser storage is available. The same page, research-area query, publication filters and anchor are retained. Spanish routes live under `/es/`; no translation service or account is needed. Links still select a language when storage is unavailable.

In the CMS, fill in the English fields and their **Spanish** companions before publishing. Paper titles, author names and journal names stay in their original language. Keep the complete approved area descriptions; the originals and their sources are archived under `docs/sources/`. The **Home scope, contact and seminar information** collection controls the information moved from About to the home page. Contact details remain in the final home-page block and are linked from the footer; Contact is omitted from the desktop and mobile header. Seminars has an independent page linked from the header and footer.

Research photos have source/license credits. Project and paper photos are optional and disappear when absent. Set an ongoing project's Article URL to make its title and photograph open the paper. The public `/photo-credits.html` page records the photo attributions, and `/es/photo-credits.html` provides the Spanish version. The supplied Drive image remains pending access; the code supports adding it later without changing the layout. Working papers and policy briefs are temporarily hidden from public publications; a separate working-paper series is deferred.

For local review, build with `python3 tools/build_site.py`, then serve `_site/` as described above. Inspect `/`, `/es/`, People, area pages and publication details. Project instructions prohibit running tests unless requested; this change uses the static build, syntax/path inspection and manual browser review.

News remains hidden from public navigation, search, routes and feeds. Seminars is restored as an independent page in both languages, linked from the header and footer and included in search. The former home-page seminar block and unconfirmed separate student-series concept have been removed. Use **Show News publicly** and **Show Seminars publicly** in Site settings to control visibility. The area-page paper section is titled Publications / Publicaciones.

The optional **Research scope** subtitle field may be left blank to omit that heading. The scope and affiliation paragraphs remain visible. Research areas follow **Display order** consistently across the home page, directory labels, and Research page; the Research grid adapts to three desktop, two tablet, and one mobile column.

### Publication display and temporary visibility

Keep author names in their original citation order in each publication record. Link each UP author with the **Researcher profile** relation (`person_id`). Public lists and detail pages group linked UP researchers first and introduce the remaining coauthors with **with** / **con**; the saved citation order is preserved. Publications appear from newest year to oldest.

In **Site Settings**, **Show working papers publicly** and **Show policy briefs publicly** are currently off. These records stay editable in the CMS, but do not generate public lists, filters, search results, JSON entries or detail pages. Turn the switches back on to restore the approved records. The home-page working-paper link follows the working-paper switch.

### Human Capital comparison page

Human Capital uses **Area page design → Original photo-led reference**. Its **Original cover photograph**, **Original page team**, project photographs, and **Full publication features for original layout** reproduce the original page with locally saved media. Each publication feature links to an existing publication, keeps the complete original narrative in English and Spanish, and can include podcast/blog links. These narratives do not replace the journal abstracts on publication detail pages. The original page team only controls this comparison layout; directory area assignments stay independent. Other areas retain the standard design.

Publication titles and optional publication images always open the internal detail page, in the current language. **Abstract and details / Resumen y detalles** opens the same page. The detail page provides a **View article / Ver artículo** button to the canonical publisher or DOI URL, plus a separate PDF download when supplied. This behavior also applies to the Human Capital comparison layout.

The original portrait files shared through Drive were reviewed on October 16. Twelve People portraits now use those originals without recompression; Sergio and Esteban already used the shared resolution. Juan Álvaro retains the approved earlier portrait. The Human Capital comparison page retains its separately approved reference photographs. Source files and checksums are recorded internally in `design/assets/media-sources.json`.

In **People**, upload the complete original under **Portrait**. **Portrait framing (percentages)** keeps the file intact and controls the visible rectangle: Left and Top locate its upper-left corner; Width and Height define its size within the original. Each value uses 0–100; Left + Width and Top + Height must not exceed 100. Remove this optional group for automatic framing. When replacing a photograph, reset its old framing and inspect the generated page before publishing. English and Spanish share the same photograph and framing.
