# Econ Site

Static website for the **Economics Research Center, Universidad Panamericana**. The live organization site is <https://up-economics-research-center.github.io/>.

## Project files

- `index.html` and `design/` contain the site pages, shared styles, scripts, and original media.
- `docs/` contains design decisions, migration materials, and the CMS design specification.
- `admin/` and `content/` are reserved for the Decap CMS editor and its records.

The current site is a static mock hosted by GitHub Pages. Its layout and visual design remain in the existing HTML and `design/site-concept.css`.

## Decap CMS for editors

**Setup status:** Decap CMS is being prepared. The steps below describe the agreed workflow; `/admin/` will be ready after the CMS and GitHub sign-in service are deployed.

1. Open <https://up-economics-research-center.github.io/admin/> and choose **Login with GitHub**. The organization owner must first invite you to the repository and you must authorize the sign-in application.
2. Choose a section such as People, Research Areas, Publications, Seminars, News, or Site Settings.
3. Open an existing item to update it, or choose **New** to add one. Fill in the named fields, keep the source link and verification information, and use the preview to review the result. You do not need to edit HTML or CSS.
4. Save your work as a draft, then mark it ready for review. Decap creates a pull request; this does not publish the change.
5. A maintainer checks the facts, sources, image permissions, links, and preview. The change goes live only after a maintainer approves and merges the pull request.
6. GitHub Actions deploys the approved change to the public site after the merge. The site update may take a short time to appear.

People who are not invited to the CMS can propose a change by opening a pull request from GitHub. A maintainer reviews it before publication.

### Adding or changing an image

Use the CMS media chooser to add the image. Enter useful alternative text, keep the original media source and permission information, and preview the crop. Do not upload generated or unapproved portraits. The source media register is `design/assets/media-sources.json`.

### Content review

- Keep research biographies, affiliations, event dates, citations, and contact details current and sourced.
- Do not publish illustrative publication records, unconfirmed events, or unsupported contact information as facts.
- If a record has not been verified, leave it in draft and mention what needs checking in the pull request.

### Owner setup required before editors can sign in

The organization owner needs to deploy the OAuth Worker, create a GitHub OAuth App, store its secret in Cloudflare, invite editors to the repository, and require a pull request review for `main`. Never put a client secret or access token in this repository. The implementation guide will replace this setup note with the final account steps once the CMS is installed.

## Local preview

From the repository root, run:

```sh
python3 -m http.server 8000
```

Then visit <http://localhost:8000/>. Open `design/homepage-concept.html` to compare the source design page. GitHub Pages serves `index.html` at the organization root.

## Editorial and visual guidance

- Preserve the existing HTML, shared styles, and local media unless the Center asks for a redesign.
- Keep dates and citations current and link each item to its canonical source.
- Editors should change content fields, not page styling.
- See `AGENTS.md` for project-wide editing guidance and use the setup status above to tell whether CMS sign-in is available yet.
