# Editorial content

Create and maintain records through `/admin/` after the organization owner configures the GitHub OAuth Worker and invites editors. Records are JSON files in the collection folders below. A record appears on the public site and in search only when its `published` field is `true`; its facts must be reviewed in a pull request before that branch is merged to `main`. The optional Reference URL may point to any supporting page or document; it need not be a personal website.

- `settings/site.json`: public site name, approved home-page copy, campus video, and footer note.
- `settings/about.json`: approved About-page scope, collaboration, and public contact.
- `people/`: approved researcher profiles. Add an optional Reference URL when a useful supporting page or document is available.
- `research-areas/`: approved topic labels, short `summary`, fuller `overview`, repeatable `projects` (each with title, summary, and researcher names), links to researcher IDs, and an optional Reference URL. Keep current projects separate from publication records.
- `publications/`: papers with ordered authors, abstracts, year, type, venue, DOI/canonical link, topics, and optional approved PDF.
- `news/`: sourced announcements with publication date and summary/body.
- `seminars/`: confirmed talks with time zone, registration/location, and optional supporting references.

The initial 11 public people profiles and nine areas were mapped from Akito Kamei’s Center and research-area pages and checked on 2026-09-24. Area projects and publication records are summarized from the cited public pages; summaries are editorial paraphrases. Recheck any available reference links and individual publication pages before changing bibliographic facts. The existing Sergio profile is retained as an unpublished draft because it was not present on that source page. Review its role and source before publishing. Review the facts and profile/area associations before approving future edits. Do not use the old `[Demo]` publication or illustrative news records as source material. Do not fill missing abstracts, authors, dates, or links by inference. If a fact has not been verified, leave the record unpublished and explain what needs checking in its pull request.
