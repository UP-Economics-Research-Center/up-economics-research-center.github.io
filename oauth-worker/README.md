# Decap GitHub OAuth Worker

This Cloudflare Worker implements the GitHub OAuth endpoints expected by Decap CMS at `/auth` and `/callback`. It is intentionally separate from GitHub Pages, which cannot keep an OAuth client secret.

## Deploy

1. Create a GitHub OAuth App for the Center. Set its authorization callback URL to `https://YOUR-WORKER.workers.dev/callback`.
2. In `wrangler.toml`, set `SITE_ORIGIN` to the exact Pages origin (`https://up-economics-research-center.github.io`).
3. From this directory, authenticate Wrangler and deploy:

   ```sh
   npx wrangler login
   npx wrangler deploy
   ```

4. Bind the app credentials and a newly generated random state-signing secret:

   ```sh
   npx wrangler secret put GITHUB_CLIENT_ID
   npx wrangler secret put GITHUB_CLIENT_SECRET
   npx wrangler secret put STATE_SIGNING_SECRET
   ```

   Paste each value only at Wrangler's interactive prompt. Do not add secrets to files, commits, or Pages settings. `GITHUB_CLIENT_ID` is public to the OAuth protocol, but storing it as a Worker secret keeps deployment configuration together.

5. Update `backend.base_url` in the site's `admin/config.yml` to the Worker origin, without a trailing slash. Merge that change to `main` and wait for the Pages deployment.
6. Confirm `/admin/` no longer shows its owner-setup notice. Test with an invited collaborator account and verify the edit opens a pull request before anything appears publicly.

The Worker requests GitHub's `public_repo` scope. Editors also need repository write access; organization membership alone does not grant access. Keep `main` protected by requiring maintainer review. Rotate a credential by setting the new Worker secret and redeploying; never expose a secret in browser code or logs.
