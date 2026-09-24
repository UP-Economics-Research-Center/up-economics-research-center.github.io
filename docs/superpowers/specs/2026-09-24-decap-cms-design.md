# UP Economics Research Center CMS Design

**Date:** 2026-09-24  
**Status:** Proposed for review

## Goal

Give Center editors a clear visual way to maintain approved site content while keeping the current static design, GitHub Pages hosting, and a review step before any content reaches the live site.

## Agreed editorial workflow

- Editors sign in with GitHub.
- People granted write access to the site repository can use the CMS to prepare changes.
- CMS changes are staged as pull requests. A maintainer reviews and merges each change; only changes merged into main are published by GitHub Pages.
- People without repository access cannot sign in to the CMS. They may propose changes by opening a pull request from GitHub; a maintainer decides whether to merge it.
- The public repository does not make write access public. The admin page may be publicly reachable, but GitHub authentication and repository permissions control editing.
- Do not enable Decap Open Authoring in v1. It would let any GitHub user use the CMS to propose changes from a fork, while the agreed workflow reserves CMS access for invited editors.

## Architecture

The public site remains a static site deployed from the repository named up-economic-research-center.github.io at https://up-economics-research-center.github.io/. GitHub Actions builds and publishes the site from the repository root source on pushes to main.

Decap CMS is served at /admin/. Its GitHub backend targets UP-Economics-Research-Center/up-economic-research-center.github.io on main and uses editorial workflow mode. A small Cloudflare Worker provides the OAuth authorization and callback endpoints Decap needs; GitHub Pages itself does not provide server-side authentication. The Worker holds OAuth application credentials as secrets. The repository contains only the public client identifier and Worker address, never a client secret or access token.

The existing HTML pages and shared CSS remain the presentation source of truth. Content is stored as named JSON records under content/ and edited through explicit Decap fields. A dependency-free Python build step reads those records and places approved content into the existing HTML templates, copying local media and admin files into the Pages artifact. The build publishes only approved records; illustrative or draft records remain out of the public artifact. The script escapes text and attributes before inserting them into HTML.

Media remains local under design/assets/. Decap uploads new media into the same tree, and content fields store paths relative to the published site. Existing images are retained.

## CMS collections and fields

- Site settings: site label, homepage introduction, footer attribution, verified contact details, and the campus video ID and caption.
- People: stable ID, name, role, biography, portrait path, profile URL, research-area IDs, source URL, verification date, and publication approval.
- Research areas: stable ID, name, summary, associated people IDs, source URL, verification date, and publication approval.
- Publications: stable ID, title, authors, type, year, venue, DOI or canonical URL, topic IDs, source URL, and publication approval. Demo records are excluded until individually approved.
- Seminars: stable ID, series, title, speaker, date and time, description, location or URL, source URL, and publication approval. Unconfirmed events are excluded.
- News: stable ID, title, date, summary, body, canonical URL, source URL, and publication approval.
- About-page copy: approved scope, affiliation, collaboration text, and verified public contact.

Stable IDs and topic references preserve links between people, research areas, publications, and seminars. Editors update records through familiar labels and repeatable lists; they do not edit HTML or CSS.

## Publishing and access controls

Use GitHub OAuth through the Cloudflare Worker and Decap's GitHub backend. Only named GitHub collaborators with repository write access can sign in to v1 CMS. Ask every editor to authorize the GitHub application before editing. Use the narrowest OAuth scope compatible with Decap and public-repository fork/PR review; do not place credentials in client-side configuration.

Protect main with a rule that requires a pull request and at least one approval before merge. Do not grant CMS editors bypass permission. If GitHub does not permit the repository's desired rule on the current organization plan, keep merge permission limited to named maintainers and explain the manual review procedure. Merging a pull request triggers the existing Pages deployment. A failed build does not publish the new version.

The initial GitHub OAuth App redirect URI is the Cloudflare Worker callback. Set its client ID and secret as Worker environment configuration; do not commit the secret. Set the Decap CMS base URL to the Worker host. Local CMS development uses Decap's local backend and must be documented as development-only; it must not become the production backend.

## Data and build flow

1. An editor signs in at /admin/ and edits a named record.
2. Decap creates or updates a review branch and pull request against main.
3. The maintainer checks the visual content preview, sources, approval flags, links, and changed record, then approves and merges.
4. GitHub Actions builds the static artifact. Draft and unapproved records are omitted.
5. The Pages deployment replaces the live artifact at the organization root URL.

## Error handling and accessibility

The admin page must explain failed sign-in, missing repository access, and unsaved or unsubmitted drafts in plain language and link to the repository owner for access help. Preview templates use the current visual components, preserve semantic headings and labels, and show the media alternatives editors enter. The public site remains usable without the CMS JavaScript. The build fails with a useful file and field error when a record is malformed or a required reference is missing; it must not silently publish partial or fabricated content.

The CMS interface is form-based, keyboard-operable, and labelled for screen readers. The site retains responsive layouts and reduced-motion behavior. Editors see only content fields, not implementation details.

## Rollout and prerequisites

1. Add Decap admin assets and collection configuration, structured content records, and the static build step while retaining the current design.
2. Review and map only the existing approved material. Keep demo publications and unconfirmed events out of the published artifact.
3. Update GitHub Actions to build then upload the generated artifact; retain the current root-site Pages deployment.
4. Deploy the OAuth Worker after the organization owner creates the GitHub OAuth App. Configure its secret through Cloudflare, then set its public URL in Decap configuration.
5. Invite editors as repository collaborators with the minimum required role and ask them to authorize the OAuth application.
6. Configure branch review protection and verify a draft pull request, approval, merge, Pages deployment, and resulting public page.

The Center owner must provide or create the Cloudflare account, create the GitHub OAuth App, and configure its secret in Cloudflare. No secret is requested through chat or committed to Git.

## Out of scope

- Redesigning the approved HTML/CSS visual direction.
- Replacing local source media with generated imagery or remote assets.
- Publishing demo publications, unconfirmed events, unsupported contacts, or unverified claims as facts.
- Using Clerk in v1. Clerk could authenticate a separate custom editing service, but Decap does not use Clerk as a drop-in GitHub backend; doing so would add a custom authorization and GitHub-writing layer.
- Moving the public site away from GitHub Pages.

## Acceptance conditions

- A named collaborator can sign in at /admin/ and edit a record without editing code.
- A CMS save creates a pull request and does not deploy to the live branch.
- A person without write access is denied CMS editing; a separately submitted public-repository pull request remains reviewable by a maintainer.
- Only an approved, merged record reaches the static artifact and the public Pages site.
- Existing CSS, JavaScript, image paths, navigation, and responsive page structure work at the organization root URL.
- No secret is present in Git history, CMS configuration, or the Pages artifact.
- The README explains editor access, review, publishing, and required owner setup in plain language.
