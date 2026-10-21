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
4. Save a **Draft**, then move it to **In review** when both languages, sources and media are ready. Saving a draft keeps the public site unchanged. The **Include on website / Mostrar en el sitio** switch controls visibility after publication; it does not approve or publish the draft. Keep it on when updating a public record.
5. A different invited editor reviews and approves the change in GitHub. The **Build editorial changes** check must pass. If changes are requested, revise the same draft; new edits need another review. Decap's **Ready** status does not replace GitHub approval.
6. Publish the approved entry, or have a maintainer merge its approved pull request. GitHub Pages updates the live site after deployment succeeds. If the build or deployment fails, ask a maintainer to inspect **Actions**.

**Activation status:** this review workflow is prepared locally. The live site still has its previous direct-publish configuration until the reviewed release is deployed. A second reviewer and GitHub approval/build requirements must be configured as part of that release. Follow [the owner activation checklist](docs/cms-approval-setup.md). Do not claim approval is enforced based only on the CMS setting.

The bilingual [editor and reviewer guide](admin/editor-guide.html) is linked from `/admin/`. Draft builds provide downloadable site files; there is no automatically hosted pull-request preview.

### Seminar information and proposals

The independent `/seminars.html` page and its Spanish version are linked from the header and footer. Edit the introduction, usual schedule, session confirmation note, proposal types and form link in **Home scope, contact and seminar information**. Fill both language fields. The official UP proposal form is in Spanish; the button is labeled Submit a proposal / Envía una propuesta without the removed language qualifier. Its description confirmed the usual monthly schedule on 2026-10-16. Verify changes against the source before editing the schedule. Add individual confirmed events in the **Seminars** collection; upcoming and past entries are separated automatically. No event dates or speakers are currently entered.

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
5. Designate at least two separate GitHub accounts for authoring and independent review. Invite the intended people with write access after owner authorization; they must accept. Preserve force-push, deletion and administrator protection. Follow the approval and required-build activation steps in [the release checklist](docs/cms-approval-setup.md).
6. After deploying the review workflow, have an editor save an authorized correction as a draft. Verify it cannot publish before a second person approves and the build passes; publish only approved content. Do not publish demo content to check the workflow.

If GitHub returns an access or organization-permission error, ask an organization owner to invite the editor or adjust repository access. Never share OAuth secrets or personal access tokens in commits or chat. To rotate credentials, update the Worker secret bindings and redeploy it; do not add credentials to this repository.

## Design guidance

Team-supplied design resources are saved in [docs/design-references.md](docs/design-references.md). The current comment-by-comment review, including agreed image treatment and the proposed research-area order, is tracked in [docs/editorial-review-2026-10-15.md](docs/editorial-review-2026-10-15.md).

Preserve the existing HTML, shared styles, and local media unless the Center approves a redesign. Keep public copy and paper metadata sourced. Editors should change content fields; the implementation plan and design decisions are in `docs/`.

### Bilingual site and October 2026 editorial changes

English is the default. **EN / ES** switches between complete static pages and remembers the reader's explicit selection when browser storage is available. The same page, research-area query, publication filters and anchor are retained. Spanish routes live under `/es/`; no translation service or account is needed. Links still select a language when storage is unavailable.

In the CMS, fill in the English fields and their **Spanish** companions before publishing. Paper titles, author names and journal names stay in their original language. Keep the complete approved area descriptions; the originals and their sources are archived under `docs/sources/`. The **Home scope, contact and seminar information** collection controls the information moved from About to the home page. Contact details remain in the final home-page block and are linked from the footer; Contact is omitted from the desktop and mobile header. Seminars has an independent page linked from the header and footer.

Research photos have source/license credits. Project photographs are optional; publications without an approved reusable first page omit the image. Set an ongoing project's Article URL to make its title and photograph open the paper. The public `/photo-credits.html` page records the photo attributions, and `/es/photo-credits.html` provides the Spanish version. The supplied Drive image remains pending access; the code supports adding it later without changing the layout. Working papers remain temporarily hidden; approved Policy briefs can appear in the publication archive. A separate working-paper series is deferred.

For local review, build with `python3 tools/build_site.py`, then serve `_site/` as described above. Inspect `/`, `/es/`, People, area pages and publication details. Project instructions prohibit running tests unless requested; this change uses the static build, syntax/path inspection and manual browser review.

News remains hidden from public navigation, search, routes and feeds. Seminars is restored as an independent page in both languages, linked from the header and footer and included in search. The former home-page seminar block and unconfirmed separate student-series concept have been removed. Use **Show News publicly** and **Show Seminars publicly** in Site settings to control visibility. The area-page paper section is titled Publications / Publicaciones.

The optional **Research scope** subtitle field may be left blank to omit that heading. The scope and affiliation paragraphs remain visible. Research areas follow **Display order** consistently across the home page, directory labels, and Research page; the Research grid adapts to three desktop, two tablet, and one mobile column.

### Publication display and temporary visibility

Keep author names in their original citation order in each publication record. Link each UP author with the **Researcher profile** relation (`person_id`). Public lists and detail pages group linked UP researchers first and introduce the remaining coauthors with **with** / **con**; the saved citation order is preserved. Publications appear from newest year to oldest.

In **Site Settings**, **Show working papers publicly** is off and **Show policy briefs publicly** is on. A disabled type stays editable in the CMS but does not generate public lists, filters, search results, JSON entries or detail pages. Enable its switch to restore approved records. The home-page working-paper link follows the working-paper switch.

### Research area pages

All nine areas use **Area page design → Original photo-led reference**. Its area photograph, **Team selection**, project photographs, and **Full publication features for original layout** use locally saved media. Each publication feature links to an existing publication, keeps the complete original narrative in English and Spanish, and can include podcast/blog links. These narratives do not replace the journal abstracts on publication detail pages. Leave **Team selection** empty to show researchers assigned to that area. A nonempty list controls membership and order only; photos and crop always come from People. Without a custom publication feature, the page displays the existing journal abstract. Never invent a project photograph or publication narrative.

Keep **UP Economics Research Center** unchanged in English and Spanish, including both name fields in Site Settings.

Publication titles and optional publication images always open the internal detail page, in the current language. **Abstract and details / Resumen y detalles** opens the same page. The detail page provides a **View article / Ver artículo** button to the canonical publisher or DOI URL, plus a separate PDF download when supplied. This behavior also applies to the Human Capital comparison layout.

The original portrait files shared through Drive were reviewed on October 16. Twelve People portraits now use those originals without recompression; Sergio and Esteban already used the shared resolution. Juan Álvaro retains the approved earlier portrait. All area Team photographs and crops now come from People, including Human Capital. Source files and checksums are recorded internally in `design/assets/media-sources.json`.

In **People**, upload the complete original under **Portrait**. **Portrait framing (percentages)** keeps the file intact and controls the visible rectangle: Left and Top locate its upper-left corner; Width and Height define its size within the original. Each value uses 0–100; Left + Width and Top + Height must not exceed 100. Remove this optional group for automatic framing. When replacing a photograph, reset its old framing and inspect the generated page before publishing. English and Spanish share the same photograph and framing.

The **Submit a proposal / Envía una propuesta** button appears beside **Propose a session**. Edit its destination in **Home scope, contact and seminar information**. The form-language qualifier, completion-time note and seminar questions/email line were removed at editorial review; the general home-page contact remains available. Home navigation buttons share the **Explore research** appearance.

Publication previews always show complete document pages without cropping or color filters. Upload an authentic first PDF page with its source and credit; leave the image empty when the document is unavailable. Research and Publications share the same central image. On desktop, previews align with the adjacent text; on mobile they stack at their natural proportions.

Current projects use one row per project in editorial order. Desktop project photographs align with the title and span the combined title and description height; researcher/presentation notes are excluded. In the CMS, **Image display / Presentación de imagen** defaults to **Photograph — match text height**. Choose **Complete diagram / Gráfico completo** for a chart, word cloud or image containing text that must remain readable. This keeps the whole image visible. On mobile, images stack beneath their text at their natural proportions. A project without an image uses the full row. Gallery squares and uniform People/Team portraits retain their specific framing.

Content links are underlined. Menus, language switches, breadcrumbs and button-like controls use their selection and focus styles instead.

Area-team portraits reuse the saved directory framing; explicitly selected Human Capital reference portraits keep their approved square presentation. The build reads PNG/JPEG/GIF dimensions directly from local assets and includes them in HTML and JSON feeds, so image space is reserved in the correct proportion without additional dependencies. Long area descriptions, project summaries and article narratives share a 78ch reading limit. All page footers use the same configured editorial note; do not remove that note without approval. The Image credits page distinguishes article first pages, journal captures, covers, project images and portraits, and lists only images used in the public build.

### Fechas de publicaciones y Medios

En Publications, la fecha exacta de publicación y su URL de fuente primaria son opcionales. Escribe la fecha como `YYYY-MM-DD` y usa una fuente HTTPS que confirme ese día; no basta conocer el año o la fecha de revisión. El generador rechaza fechas imposibles o futuras. Solo con ambos campos se permite **New / Nueva** durante los primeros 90 días UTC (se retira al cumplir 90 días). El navegador actualiza la etiqueta aunque no se reconstruya el sitio; sin JavaScript queda oculta. No modifica el orden ni la visibilidad de publicaciones. ISBN es opcional para libros.

Media / Medios permite añadir entradas repetibles con título y resumen EN/ES, tipo, medio, URL principal HTTPS, autores comprobados, fecha opcional y relaciones con investigador y publicación. Deja la fecha vacía si no está verificada. Añade la fuente de verificación y revisa ambos idiomas antes de activar la visibilidad y solicitar revisión editorial. El enlace está en el pie; los registros visibles se incluyen en búsqueda y en `media.json` EN/ES. Guardar en el CMS sigue el proceso de aprobación existente y no equivale a publicar remotamente.

En la vista previa de octubre, la fecha del libro de Eugenio es 2026-08-27 según el registro primario ISBN; las fuentes y la limitación de acceso directo se documentan en `docs/editorial-gallery-release-2026-10-19.md`. La fecha del podcast sigue vacía. Las áreas con libros usan el encabezado general Publicaciones, para no presentarlos como artículos de revista.

### Team photographs / Fotografías de Team

People is the single source for each person’s photograph and framing. Edit the photo and crop there once; every research-area Team uses the same settings. Area Team selection controls membership and order only, with no separate photo upload. Older reference-photo metadata and files remain preserved but are no longer displayed. / Cambia la fotografía y el encuadre una sola vez en People: se aplican a todos los equipos. La selección del equipo solo cambia integrantes y orden.


### Avisos legales y miniaturas

Los avisos EN/ES se editan en **Legal notices / Avisos legales**. Privacidad y Términos remiten a las publicaciones oficiales de UP; los textos anteriores se conservan en `docs/legal-drafts-before-official-links-2026-10-21.json`. Cada enlace puede tener una URL alternativa en inglés (`url_en`); si se deja vacía, se usa la URL principal. Los marcadores `{{contact_name}}`, `{{contact_email}}` y `{{official_privacy_url}}` usan los campos compartidos. El estado `draft` y las notas de revisión son internos: ya no generan un aviso público de espera. Mantén el registro de revisión sin inventar una aprobación; para marcar aprobado, registra revisor y fecha. La aplicación del aviso oficial y las autorizaciones de medios siguen documentadas en las notas internas.

Las imágenes de publicaciones deben ser primeras páginas auténticas, con fuente y crédito. Déjalas vacías cuando falte el documento. Las áreas reutilizan la imagen de Publications; no permiten otra miniatura. No uses capturas de webs editoriales como sustitutos.

La dirección visual y los pendientes documentales están en [las notas de la versión](docs/editorial-gallery-release-2026-10-19.md).


### Policy Briefs and companion briefs

Policy Briefs is an archive category and remains in the type filter even with zero records while its visibility switch is enabled. The two UNICEF briefs were removed from public display at the team’s request; they remain unpublished in the CMS. To add a brief beside an article, first create and approve a Publications record with **Type: Policy brief**, then select it under that article’s **Companion policy brief / Nota de política asociada**. The same brief stays in the archive, appears beside the article on desktop (below it on mobile), and is linked from Research. Leave the relation empty until the association is confirmed; do not infer a companion brief from a similar topic.

### Publication preview permissions

Upload an authentic first-page image, then record **Image reuse status**, a public rights-evidence URL and the license name/link where applicable. Pending is the default: the image remains in source but is omitted from the generated site. Research and Publications omit the preview when no reusable image is available. Publisher webpage captures also require a rights basis; they are not an automatic workaround. Do not put private permission correspondence in public CMS fields.

For project photos, **Photograph focus / Zona principal de la foto** selects top, center or bottom when the title-and-description frame crops the image. Use it to keep the important subject visible.
