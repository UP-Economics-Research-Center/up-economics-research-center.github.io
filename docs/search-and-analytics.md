# Search and analytics operation

## Ownership and service boundaries

Search Console and Cloudflare setup use the account explicitly selected by the user, `jadrk040507@gmail.com`. No other users are invited, no DNS is changed, and GitHub Pages remains the host. Name an institutional owner and backup before handover; these roles have not been assigned or enforced by this change.

Cloudflare Web Analytics is for aggregate traffic and real-user page performance. It does not provide custom click/download event reports in this integration. The beacon loads only after acceptance on the configured production hostname. Declining, a Global Privacy Control signal or Do Not Track prevents the beacon from loading. The first-visit prompt and persistent footer control are bilingual and keyboard operable. Preferences use `up-analytics-consent-v1` localStorage for up to 180 days; language uses the separate existing `up-language` key. No account passwords or API secrets enter generated files.

## What the build maintains

- Complete static HTML for all published research areas in both languages, including projects, portraits, publication previews, editorial notes and the distinct Human Capital composition. No browser fetch is needed to read their content.
- Stable area URLs under `/research/<slug>/` and `/es/research/<slug>/`; old query URLs remain compatible through a client-side redirect. GitHub Pages does not provide configurable HTTP 301 redirects here. Keep old links working until upstream references are updated.
- Sitemap of canonical public EN/ES pages, excluding admin, duplicate design routes, legacy area selectors, contact redirects and paused sections. No fabricated update dates. `robots.txt` advertises the sitemap and permits crawling. Admin pages use `noindex`; this is not authentication or protected storage.
- Page-specific canonical, EN/ES and x-default links, descriptions, Open Graph/Twitter preview metadata, schema.org site/organization/publication records and citation metadata. Original article titles retain their original language. No unverified author, rating, date or institutional approval is invented.

## Search Console activation

1. Use the URL-prefix property `https://up-economics-research-center.github.io/`.
2. The selected owner's HTML-tag verification value is stored in `content/settings/discovery.json`. Publish it, verify ownership, and retain it for continued access.
3. Submit `https://up-economics-research-center.github.io/sitemap.xml` in Sitemaps.
4. Inspect the home, research index, a static research area and a publication. Request indexing where appropriate; an accepted request is not confirmation of indexing.
5. Monitor Pages, Performance and Core Web Vitals. New reports can take time; low-volume pages may not have performance field data.

Bing's verification field is prepared but is not evidence of an active Bing Webmaster Tools account. Google Scholar citation metadata is supplied where applicable; Scholar eligibility/indexing is a separate process and is not guaranteed.

## Analytics activation and recovery

The Web Analytics site must match `up-economics-research-center.github.io`. Use its public beacon token from **Manage site**, not an API token. Install manually so the consent gate controls when code loads. Keep automatic DNS/proxy injection disabled: it could bypass this consent gate. No Cloudflare proxy is needed.

To disable collection, clear `cloudflare_analytics_token`, build and deploy. To replace the site token, update that field and recheck acceptance/rejection on production. Removing code stops future page loads from collecting; already open tabs can continue until refreshed. Revocation through the footer ends collection on the current page by reloading it. Browser privacy signals and blockers can reduce the reported sample. Consent-based measurement is not a census of all visitors.

## Monthly checklist

The designated site maintainer and backup should:

1. Check deployment success and follow the existing restoration guide if it fails.
2. Review Search Console indexing errors and unexpectedly excluded canonical pages.
3. Check research/publication links, approved content and EN/ES navigation.
4. Review traffic, referrers and page-performance trends in Cloudflare; do not treat small samples as representative.
5. Recheck accept/reject/reopen/withdraw controls after any analytics change and update the storage/services description to match actual behavior.

Review owner access quarterly. Keep accounts individually owned, use MFA and the providers' recovery flows; do not share passwords. A future UP domain requires coordinated canonical, sitemap, verification, analytics-host and redirect work. Do not switch it by editing only one setting.

## Sources

- Google: [sitemaps](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap), [localized pages](https://developers.google.com/search/docs/specialty/international/localized-versions), [verification](https://support.google.com/webmasters/answer/9008080).
- Cloudflare: [manual setup](https://developers.cloudflare.com/web-analytics/get-started/), [collection](https://developers.cloudflare.com/web-analytics/data-metrics/data-origin-and-collection/), [disable SPA measurement](https://developers.cloudflare.com/web-analytics/get-started/web-analytics-spa/).
- Mexican institutional privacy references remain in the site's legal records; technical configuration does not establish legal approval or compliance on its own.

## Verification record

Release preparation, 21 October 2026: the static build, changed JavaScript syntax and whitespace checks passed. Artifact inspection covered 102 public HTML files, all schema JSON blocks and all root-relative href/src targets; no missing targets were found. The sitemap contains 82 unique URLs, all backed by generated pages, including 18 complete research-area pages. CMS YAML parses. Manual review covered EN/ES static research pages, a zero-project state, 320/390/1024/1440px layouts, legacy query redirect with language/hash preserved, and privacy preferences. The browser’s privacy signal disabled acceptance and kept the provider script absent; rejecting remained effective after reload. The normal acceptance/withdrawal path still requires a browser without a privacy signal for end-to-end provider verification. No tests were run, per project instructions.

Cloudflare’s Web Analytics site was created for the exact hostname in the selected account. Google’s HTML-tag token was prepared with explicit owner authorization. Deployment, ownership verification and sitemap submission follow these local checks; consult the provider interfaces for their live status. Do not describe the site as indexed or visitor data as received until those are confirmed separately.
