# UP Economics Research Center Google Sites Design

## Purpose

Create a polished, credible public website for the Universidad Panamericana Economics Research Center. The site must be simple for faculty and staff to update through Google Sites’ visual editor, using familiar Google Workspace tools rather than a code or Git workflow.

## Audience and success

Primary audiences are UP students, faculty, researchers, prospective collaborators, public agencies, businesses, and the broader public. Visitors should quickly understand what the Center studies, meet its researchers, find research outputs, and discover or attend seminars. Editors should be able to update routine content without technical help.

Success means the site feels unmistakably connected to UP, presents the Center as a serious and broad economics research group, gives student research a welcoming path, and makes current seminars and publications easy to find and maintain.

## Platform and constraints

- Build and maintain the public site in Google Sites.
- Use native Google Sites pages, sections, themes, image blocks, buttons, embeds, and Drive-hosted files wherever practical.
- Keep the editing workflow visual and familiar. No GitHub, code, custom CMS, or developer-operated deployment for routine updates.
- The initial design must fit Google Sites’ available layout and interaction controls. Use purposeful photography, video, strong typography, generous spacing, color, and clear composition to create a premium feel. Do not depend on custom JavaScript, complex transitions, or unsupported widgets.
- Prefer real UP faculty and student photography. Do not use the train image from the current mock.
- Ask UP Communication / Digital Infrastructure to confirm institutional branding requirements, account ownership, site access, domain or subdomain options, privacy requirements, and any approved templates before public launch. Proposed domain examples such as `economia.up.edu.mx` are ideas only, not confirmed availability.

## Current mock audit and migration scope

The current Google Sites mock is more than a single landing page. It has one center homepage, nine linked research-area pages, image assets, two personal-website links, and a faculty portal link that requires login. Preserve and review this content before replacing the mock. Recreate the public-facing research substance in the new site, but do not copy private portal content or assume every project and profile remains current.

| Homepage card | Existing linked page | Content to carry forward |
| --- | --- | --- |
| Education & Human Capital Investment | [Education and Human Capital](https://sites.google.com/view/akitokamei/up-economics-research/education-and-human-capital) | Area overview, project and publication entries, named UP researchers |
| Digital and Business Economics | [Digital and Business Economics](https://sites.google.com/view/akitokamei/up-economics-research/digital-and-business-economics) | Area overview, project and publication entries, named UP researchers |
| Political Economy | [Political Economy](https://sites.google.com/view/akitokamei/up-economics-research/political-economy) | Area overview, project and publication entries, named UP researchers |
| Macro Economics | [Macro Economy](https://sites.google.com/view/akitokamei/up-economics-research/macro-economy) | Area overview, project and publication entries, named UP researchers |
| Development Economics | [Development Economics](https://sites.google.com/view/akitokamei/up-economics-research/development-economics) | Area overview, current projects, journal publications, team members |
| Health Economics | [Water and Sanitation](https://sites.google.com/view/akitokamei/up-economics-research/water-and-sanitation) | Health, water and sanitation overview, projects, publications, researchers; confirm whether URL/title should be renamed or card relabeled |
| Agriculture Economics | [Agriculture Economics](https://sites.google.com/view/akitokamei/up-economics-research/agriculture-economics) | Area overview, current projects, journal publications, team members |
| Environmental/Climate Economics | [Environmental Economics](https://sites.google.com/view/akitokamei/up-economics-research/environmental-economics) | Area overview, project and publication entries, named UP researchers |
| Economic Demography | [Demographic Economics](https://sites.google.com/view/akitokamei/up-economics-research/demographic-economics) | Area overview, current projects, journal publications, team members |

The homepage introduces the Center as an empirical, policy-relevant group working on social and economic challenges in Mexico and around the world. It includes the tagline “Generating empirical evidence to move society UP ward,” lead researcher profiles, research professional profiles, a general contact address, Ciudad UP address, personal website links, and a login link to the UP ERC Faculty Portal. It does not expose dedicated seminar or publications indexes from the accessible homepage. Treat the tagline, roster, links, and contact/address as draft content pending owner approval.

The current revision prioritizes research substance: Home identifies the Center and routes visitors to research and people; Research lists the nine areas; each area page foregrounds actual projects, researchers, and citations; People presents the current roster; Seminars and Publications use only verified records; About is brief. The visual treatment may extend beyond the institutional color palette while retaining approved UP identity assets. See `design/google-sites-build-map.md` and `design/*.html`.

The visible roster has six lead researchers (Akito Kamei, Eugenio Gómez Alatorre, Esteban Colla-De-Robertis, Majo, Arnulfo, and Sergio) and six research professionals (José Miguel, Marytell, Juan Álvaro, Andrea, Joshua, and Luciano). Confirm names, diacritics, official titles, current status, profile copy, and image permissions with the Center before migration.

Each research-area subpage follows a useful repeatable editorial model: overview, team, current projects, and journal publications. Some accessible pages provide rich project descriptions and publication context, not just area summaries. The new Google Sites design should retain this model using one reusable area-page layout. On the Research landing page, show the nine areas as cards linking to dedicated area subpages; do not flatten all research into a short list or omit project/publication details.

The following linked resources need an explicit migration decision: the two “Personal Website” links, all linked project/publication records, image originals, and the UP ERC Faculty Portal login link. Preserve approved public links; replace low-resolution or inconsistent images with approved originals. Keep the portal link only if the Center confirms its purpose and audience. Search indexing confirms all nine destination URLs, but some pages could not be fetched directly during this audit; validate full contents in Google Sites with an editor account before final copy migration.

## Visual direction

**Thesis:** an editorial, multi-page research journal shaped by Universidad Panamericana’s identity. Use the latest institutional guide’s university burgundy (#8A1538) and gold (#BA9357) as anchors, with warm white and dark ink. Confirm mark, typography, and exact application with Comunicación Institucional. Do not create a separate Center logo.

- Replace repeated card grids with large editorial headlines, open space, thin rules, numbered research links, asymmetric layouts, and varied section rhythm.
- The Home page opens with a people-led image and short invitation, then moves through research, seminars, and publication pathways. Research, Seminars, Publications, People, and About each have distinct top-level pages; the nine research areas keep dedicated subpages.
- Favor authentic UP portraits, seminar moments, campus details, and research activity. Use a consistent photo treatment and crop ratios.
- Use video selectively on dedicated Seminars or Publications pages; use an institutional host, never autoplay, and provide captions or transcripts where available.
- Keep motion subtle and optional. Do not make navigation or content depend on animation unsupported by Google Sites.
- Ensure readable contrast, descriptive image text, keyboard-friendly native controls, and desktop/mobile legibility.

## Information architecture and page content

### 1. Home

Purpose: establish identity and guide visitors to the Center’s active work.

Recommended sections, in order:

1. **Hero:** “Economics research for a better understanding of Mexico and the world.” Supporting line: “The UP Economics Research Center brings faculty and students together to produce rigorous, policy-relevant research on economic and social challenges.” Primary links: “Explore our research” and “Upcoming seminars.” Use a real faculty-and-student image, not a train or generic stock image.
2. **Current work:** three or four selected research area cards, linked to the Research page.
3. **Next seminar:** one featured upcoming event with date, speaker, title, format/location, and a clear details link. If there is no scheduled event, show a brief seminar-series introduction and link to past talks.
4. **Selected research and publications:** three recent or representative outputs across journal articles, working papers, books, and public-facing analysis.
5. **People:** compact faculty and student researcher feature with link to the Team page.
6. **Collaborate:** a concise invitation for academic, government, business, and civil-society partners, linking to contact details.

Keep opening view concise and visually strong; do not place a long institutional essay above current content.

### 2. Research

Purpose: show the Center’s breadth without locking it into development economics alone.

Use an introductory statement such as: “We conduct empirical and applied economics research on questions that matter for Mexico and beyond. Our work spans economic opportunity, institutions, markets, public policy, and human well-being.”

Show the nine research areas from the mock as cards linking to dedicated subpages: Education and Human Capital Investment; Digital and Business Economics; Political Economy; Macroeconomics; Development Economics; Health / Water and Sanitation (label to confirm); Agricultural Economics; Environmental and Climate Economics; and Economic Demography. Confirm final names with faculty. These pages represent the current portfolio, not necessarily an approved permanent strategic-area taxonomy.

Use one repeatable Google Sites layout for every area subpage: plain-language overview, current projects, related UP researchers and collaborators, selected publications, and approved materials/links. Carry forward project descriptions and outputs from the mock after owners confirm they remain current. Use links to the Publications page for shared records when practical, while keeping area pages useful as topic-specific entry points. Add topics such as labor, inequality, industrial organization, and competition to relevant areas or researcher profiles where supported by the current mock; do not silently erase them because the homepage lacks separate cards.

### 3. Seminars

Purpose: make the seminar program easy to browse and welcoming to students.

- Separate **General Research Seminars** and **Student Research Seminars** as clear sections or filters by page anchors, while inviting students to attend general seminars.
- Describe student seminars as a supportive space for early research projects, feedback, and discussion. A “Student Research Seminar Month” may be offered when organizers confirm a schedule; present it as a possible format, not a standing promise.
- Show upcoming events first, then a compact archive of past seminars and recordings/slides where speakers permit publication.
- Use a repeatable event format: title, presenter, affiliation, date and time with time zone, room or online link, abstract, audience, registration/contact, and optional recording/slides.
- Provide a simple “Propose a seminar” contact link only after the Center confirms the correct owner and address.

### 4. Team

Purpose: introduce faculty and student research professionals with a consistent, human presentation.

- Group the current mock roster under **Lead Researchers** and **Research Professionals** (or updated approved role labels), preserving the distinction. Feature student researchers as an explicit pathway and opportunity, without implying all research professionals are students.
- Use real, consistent headshots with names, roles, research interests, short biographies, and approved links to personal websites or publications.
- Keep profile copy concise and editable as repeated content blocks. Confirm names, titles, biographies, photos, and permission before publishing.
- Do not imply that every profile is a faculty appointment or that all listed people are current without confirmation.

### 5. Publications

Purpose: represent academic excellence alongside work that reaches policy and public audiences.

Organize outputs into **Peer-Reviewed Research**, **Working Papers**, **Books and Chapters**, and **Policy and Public-Facing Analysis**. Retain Q1/Q2 journal ambition as one important measure without making it the only visible output.

Each record should include title, author(s), year, type, outlet or series, abstract/short description, topic tags, and DOI or stable full-text link. Use a repeatable Google Sites layout and link PDFs from an approved Drive folder or repository. Do not host unpublished or restricted material publicly.

### 6. About and Contact

Purpose: explain mission, scope, collaboration, and contact routes.

- State the Center’s mission and institutional home in the School of Government and Economics, subject to official naming approval.
- Explain that the Center seeks research collaboration with UP schools and campuses, government agencies, companies, research centers, and national and international organizations.
- Invite institutions to share policy and research needs as an initial step toward identifying applied research opportunities.
- Include the confirmed general contact email, UP location/address if needed, and institutional links. The current mock lists `akamei@up.edu.mx`; confirm this remains the intended public contact before launch.
- Include the required UP privacy and brand links or footer treatment specified by the institution.

## Editing and maintenance model

- Use Google Sites as the source of truth for public page content.
- Assign a small number of named editors with UP accounts; keep ownership with an institutional account or approved group, not one individual’s personal account.
- Use native page sections and duplicated content blocks as templates. Do not promise automatic databases or dynamic CMS behavior that Google Sites does not provide.
- Maintain a shared Drive media folder with approved headshots, event photos, logos, video links, publication PDFs, and naming guidance.
- Use a lightweight review habit: event details checked before posting; bios, publications, and images checked by the relevant researcher; a named site owner reviews navigation and stale items once per term.
- Editors should be able to add an event or publication by duplicating a standard block, replacing labeled fields, and adding a link or image.

## Content policy and launch dependencies

- Site language: English for the initial site, as requested. Confirm whether Spanish pages are needed later.
- Treat current mock content as draft source material. Confirm research descriptions, personnel, contact details, strategic-area names, and publication records with their owners before publication.
- Ask faculty to confirm whether “empirical and applied economics” is the preferred public scope statement.
- Ask the Center to decide if a student thesis recognition, mentoring, student research opportunities, or a student seminar month are actual programs. Do not present suggestions as existing commitments.
- Obtain Communication / Digital Infrastructure approval for brand assets, domain/subdomain, page template, accessibility and privacy requirements, and any video or analytics tools.
- Obtain permission for all people photography, recordings, and unpublished work.

## Acceptance criteria

1. A visitor can identify the Center’s scope, find an upcoming seminar, browse research areas, meet researchers, and access publications from the top-level navigation.
2. General and student seminar opportunities are visibly distinguished; students remain welcome at general seminars.
3. The publication structure includes peer-reviewed work and complementary working papers, books, and public-facing analysis.
4. The site uses authentic, approved UP community imagery and contains no train-led hero image.
5. A nontechnical editor can add or update a seminar and publication using a documented duplicate-and-edit pattern in Google Sites.
6. All text and media work in English and remain readable on desktop and mobile.
7. No unconfirmed contact details, strategic commitments, institutional branding, or domain claims appear as facts.
8. Institutional ownership, editor access, approved brand assets, public contact, and domain/hosting route are confirmed before launch.
