# Econ Site

Static website for the **Economics Research Center, Universidad Panamericana**. The public site is <https://up-economics-research-center.github.io/>.

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

The CMS is at <https://up-economics-research-center.github.io/admin/>. **Sign-in becomes available only after the organization owner completes the OAuth setup below and deploys the updated Pages site.** Only GitHub accounts invited to this repository with write access can edit. The invite must be accepted first; sign-in alone does not grant access.

1. Open `/admin/` and choose **Login with GitHub**.
2. Choose Researchers, Research Areas, Publications, Site Settings, or About.
3. Edit the fields and use the preview pane to review the record. Research areas are selected from the existing area list. You do not need to edit HTML or CSS.
4. For a new record, set its “Publish this…” switch to true when it is ready. Save the record in Decap; the change commits directly to `main` and is deployed by GitHub Actions. The live site updates after the Pages workflow succeeds. Editors publish directly to `main`; no pull request is required.
5. If a Pages deployment fails, check the workflow in the repository’s **Actions** tab and ask a repository maintainer for help.

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

Preserve the existing HTML, shared styles, and local media unless the Center approves a redesign. Keep public copy and paper metadata sourced. Editors should change content fields; the implementation plan and design decisions are in `docs/`.
