# Editorial content

Create and maintain records through `/admin/` after the organization owner configures the GitHub OAuth Worker and invites editors. Records are JSON files in the collection folders below. A record appears on the public site and in search only when its `published` field is `true`; its facts and source must be reviewed in a pull request before that branch is merged to `main`.

- `settings/site.json`: public site name, approved home-page copy, campus video, and footer note.
- `settings/about.json`: approved About-page scope, collaboration, and public contact.
- `people/`: approved researcher profiles. Use source links for affiliation and research claims.
- `research-areas/`: approved topic labels, summaries, and links to researcher IDs.
- `publications/`: papers with ordered authors, abstracts, year, type, venue, DOI/canonical link, topics, and optional approved PDF.
- `news/`: sourced announcements with publication date and summary/body.
- `seminars/`: confirmed talks with time zone, registration/location, and source links.

The initial 11 public people profiles and nine areas were mapped from the Center source page linked by the existing directory and checked on 2026-09-24. The existing Sergio profile is retained as an unpublished draft because it was not present on that source page. Review its role and source before publishing. Recheck the source URL and profile/area associations before approving future edits. Do not use the old `[Demo]` publication or illustrative news records as source material. Do not fill missing abstracts, authors, dates, or links by inference. If a fact has not been verified, leave the record unpublished and explain what needs checking in its pull request.
