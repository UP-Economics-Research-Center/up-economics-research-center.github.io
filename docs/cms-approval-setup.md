# Activate approval before publishing

Prepared locally on 2026-10-18 at the user's request. This file describes the intended release; it does not assert that the live editor has switched.

## Current GitHub state inspected

- `main` has administrator enforcement enabled, with force pushes and branch deletion disabled.
- Required pull-request reviews: none. Required status checks: none. No additional repository rulesets were returned.
- Only `jadrk040507` currently has write/review access. The user designated Akito Kamei as the reviewer and will provide his GitHub username later. His invitation and accepted access remain pending before independent approval can work. Do not share that account or its credentials.
- No repository settings or collaborator access were changed during this review.

## Prepared changes

- Decap `publish_mode: editorial_workflow`: drafts are saved separately from `main`, and requests for review can be made before publishing.
- Clear bilingual visibility labels: `published` remains the saved visibility field; it is not an approval record. A public entry being edited keeps `published: true` in its draft, while its existing approved version stays live until merge.
- Bilingual content previews include images, current projects and publication features. The file-collection previews are registered under their file names (`site` and `about`). They show content; they do not claim to be hosted previews of the full page layout.
- The `Review editorial changes` pull-request workflow builds EN/ES, validates the records and uploads an `editorial-site-preview` artifact. It has read-only repository permissions and no deployment step. The separate Pages workflow still deploys only changes merged to `main`.
- Editor instructions: `/admin/editor-guide.html`.

## Coordinated activation by the repository owner

1. Confirm the second person's GitHub username. Invite only the intended editor/reviewer with write access; they must accept. The author cannot approve their own pull request. This step requires the owner's explicit authorization to change access.
2. Prepare a release pull request containing the reviewed editor changes. Inspect the first `Build editorial changes` run and its generated files. This workflow runs a static build, not a test suite.
3. Before merging, edit the existing protection for `main` in GitHub → Settings → Branches. Preserve administrator enforcement and the existing force-push/deletion restrictions. Require a pull request, **one approving review**, and **dismiss stale approvals when new commits are pushed**. Keep review bypass lists empty. Require the **Build editorial changes** check after that check has appeared in the release PR. Do not replace existing protection with a weaker rule.
4. Have the second person review and approve the release. Merge only once approval and the build succeed. During this coordinated switch, do not save changes from the old direct-publish editor; its writes are intentionally blocked by the new protection.
5. Wait for GitHub Pages to deploy. Confirm the live `admin/config.yml` uses `editorial_workflow`, the new guidance appears, and the user can sign in normally. Do not send users to a local editor to perform real GitHub writes; the authentication service is configured for the published site origin.
6. With the owner's permission, save a real approved content correction as a draft. Confirm it creates a `cms/...` branch and review request without changing `main` or starting Pages deployment. Confirm publishing is blocked before independent approval. After the reviewer approves and the build succeeds, publish and confirm the deployment. Do not create or publish sample content just for this check.

Activation and this authenticated draft/publish check remain pending until Akito’s GitHub username/access is available and the release is authorized. No live publication, invitations, security-setting changes or CMS writes were performed during local review.

## Editorial decisions

- Save / Draft: work in progress; public site unchanged.
- In review: another editor is asked to verify the facts, both languages, media and visibility.
- Ready: a CMS workflow status. It does not count as a GitHub approving review.
- Changes requested: revise the same draft. New content changes invalidate the old approval once the protection is activated.
- Approve: another authorized person approves the exact proposed changes in GitHub.
- Publish: merge approved content and deploy. If visibility is off, that approved publication hides the record.

The UI does not provide a separate reviewer permission role: the second person has repository write access, and GitHub's protected branch enforces independent review. Do not claim role separation based only on a Decap status or a `published` boolean.

## Sources

- [Decap editorial workflow](https://decapcms.org/docs/editorial-workflows/)
- [Decap GitHub backend](https://decapcms.org/docs/github-backend/)
- [GitHub protected branches and required reviews](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
