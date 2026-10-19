# Editorial content

Create and maintain records through `/admin/` after the organization owner configures the GitHub OAuth Worker and invites editors. Records are JSON files in the collection folders below. A record appears on the public site and in search only when its `published` field is `true`; check the facts before setting `published` to `true`. In the prepared editorial workflow, Save stores a draft for review; only merging an independently approved change to `main` triggers deployment. The `published` field controls visibility after that merge, not approval. Activation requirements and current live status are in `docs/cms-approval-setup.md`. The optional Reference URL may point to any supporting page or document; it need not be a personal website.

- `settings/site.json`: public site name, approved home-page copy, campus video, and footer note.
- `settings/about.json`: approved About-page scope, collaboration, and public contact.
- `people/`: approved researcher profiles. Add an optional Reference URL when a useful supporting page or document is available.
- `research-areas/`: approved topic labels, short `summary`, fuller `overview`, repeatable `projects` (each with title, summary, and researcher names), links to researcher IDs, and an optional Reference URL. Keep current projects separate from publication records.
- `publications/`: papers with ordered authors, abstracts, year, type, venue, DOI/canonical link, topics, and optional approved PDF.
- `news/`: sourced announcements with publication date and summary/body.
- `seminars/`: confirmed talks with time zone, registration/location, and optional supporting references.

The initial 11 public people profiles and nine areas were mapped from Akito Kamei’s Center and research-area pages and checked on 2026-09-24. Area projects and publication records are summarized from the cited public pages; summaries are editorial paraphrases. Recheck any available reference links and individual publication pages before changing bibliographic facts. Sergio’s profile is public and his latest approved area is Political Economy. Review the facts and profile/area associations before publishing future edits. Do not use the old `[Demo]` publication or illustrative news records as source material. Do not fill missing abstracts, authors, dates, or links by inference. If a fact has not been verified, leave the record unpublished and resolve what needs checking before publishing.

## English and Spanish editorial workflow (October 2026)

The English field and its companion **Spanish** field describe the same content. Complete both before publishing. Paper titles, author names and journal names keep their original spelling in both languages. The build stops when a published profile, research area, project or abstract is missing its required Spanish text. Interface translations are maintained in `settings/interface-es.json`.

The nine area descriptions and ongoing research were transcribed from Akito's linked pages on 2026-10-15. Keep that English wording intact unless an editorial update is approved; translate it faithfully into Spanish. Full source transcriptions are retained in `docs/sources/`. These source texts replace the earlier paraphrased area descriptions; publication abstracts remain separately maintained editorial summaries. The latest complete biographies and publication abstracts from the public main branch were retained during publication integration, with matching Spanish translations.

`settings/about.json` now supplies the scope, affiliation, collaboration and contact blocks on the home page. Preserve its editorial note until it is resolved. Contact navigation leads to the bottom of the home page; the old About address redirects there.

Use **Display order** on research areas to retain the agreed sequence. Marytell and Majo are assigned to Development Economics; Sergio is assigned to Political Economy by the latest review.

Photographs are optional. Supply descriptive alternative text in both languages, credit/license, and a source link. With no photo, the public block disappears without a placeholder. A project's optional Article URL links both its title and photo. Publication titles/photos open the same localized internal detail page; its View article button opens the publisher or DOI page. The small paper image is separate from the broader area photograph; do not imply that a general area photograph documents a particular study. Bundled area photo provenance is recorded in `design/assets/research/photo-sources.json` and exposed in the site's photo credits.

The supplied Drive file could not be read with the connected account (file not found). No substitute has been presented as that supplied photograph. Add the approved paper photographs when they become accessible. A separate working-paper series is deferred; use the Working paper publication type in the existing publications list.

Use **Display order** on researcher profiles to control their position within their group; lower numbers appear first. The first desktop row pairs Akito with Esteban, with Arnulfo later. Mobile keeps the same reading order in one column.

Researchers can have a **Personal website URL** as well as an **Official profile URL**. Verified personal sites appear beneath the biography as Personal website / Sitio web personal. Leave the field empty when no verified website is known; the link is omitted.
