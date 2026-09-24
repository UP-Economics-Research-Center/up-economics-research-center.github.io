# Google Sites v1 migration — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox syntax for tracking.

**Goal:** Rebuild the approved research-center mock as a 16-page editable English Google Site that UP colleagues can maintain without code.

**Architecture:** Native Google Sites pages render visitor content. A Center-owned Drive folder holds copy, media, and an editorial register. Google Sites search, page headings, Drive embeds, native image layouts, and YouTube embeds replace local-only mock interactions.

**Tech Stack:** Google Sites, Google Drive, Google Sheets; local HTML/CSS is a visual reference only.

**Spec:** docs/superpowers/specs/2026-09-24-google-sites-v1-migration-design.md

## Global Constraints

- Pages: Home; Research hub + nine nested areas; People; Publications; Seminars; News; About.
- Visitor-facing language is English.
- Do not publish demo records, unconfirmed dates, unsupported contact details, or unverified affiliations.
- Use native editable Sites sections; do not promise custom fonts, code search/filters, transitions, or hover states from the local mock.
- Use Center-owned Drive for source files. Record content owner and verification date.
- Keep the Site private until names, content, image reuse permission, ownership, audience, and domain are approved.

## Review Focus

- Google Sites account is not connected; create/edit only in the Center-approved Workspace account.
- Verify current research-area names and team membership.
- Embedded Drive files must be visible to intended site viewers.
- Confirm video playback on mobile.
- Domain mapping may require the site owner and Workspace administrator/DNS access.

---

### Task 1: Create the team-owned Drive source

**Inputs:** design/google-sites-migration/site-copy-pack.md; design/google-sites-migration/assets/media-sources.json; design/google-sites-migration/content-register.csv; design/google-sites-migration/assets/

- [ ] Create a shared Drive folder named “UP Economics Research Center — Website” in the Center-approved shared location; add Brand, People, Projects, Publications, Seminars, News, and Approved for Site subfolders.
- [ ] Upload twelve portraits and the campus-video poster from the assets folder. Keep the filenames in the source manifest.
- [ ] Upload the content register CSV as a Google Sheet. Keep verification/source/publication-permission columns.
- [ ] Grant editor access using the Center-owned group chosen by the site owner. Do not place working files in public viewer access.

**Deliverable:** Center-owned source folder; no unverified items marked approved.

### Task 2: Create and style the private Google Site

**Reference:** design/homepage-concept.html; design/site-concept.css; design/google-sites-migration/site-copy-pack.md.

- [ ] In the owner’s Google Workspace account, create a blank Site named “UP Economics Research Center — Website draft”.
- [ ] Keep it private. Set public site title “Economics Research Center” only after owner approval.
- [ ] In Themes, choose the closest clean sans-serif; set burgundy #8A1538 and warm white/paper surfaces with charcoal text.
- [ ] Add a text wordmark: a small burgundy square beside “Economics”, “Research Center” below, and “Universidad Panamericana” beneath. Do not draw the official UP seal.
- [ ] Choose top navigation and add Home, Research, People, Publications, Seminars, News, About.
- [ ] Create a consistent footer with verified attribution and links to the six sections.

**Deliverable:** Private shell with seven top-level pages.

### Task 3: Build Home and Research

- [ ] Build Home with its scope line, main action, campus video, nine research-area links, and concise routes to publications, seminars, people, and contact.
- [ ] Insert the existing UP Internacional Mexico City campus film with Insert → YouTube. Use click-to-play/native controls; label its source.
- [ ] Create Research hub and nine nested area pages from site-copy-pack.md.
- [ ] On each area page, add a short confirmed overview and documented team links. Do not add unverified projects or outputs.
- [ ] Test every link from Home and Research.

**Deliverable:** Home and Research hierarchy with real media and no invented research.

### Task 4: Build People

- [ ] Create Faculty Researchers and Research Professionals sections.
- [ ] Add each of the twelve profiles with approved portrait, name, short summary, source, and topic links from the copy pack.
- [ ] Have the content owner confirm abbreviated names, roles, current status, team membership, and any identity/personal details.
- [ ] Preview image crops at desktop and phone sizes. Use initials if any portrait lacks approval; no stock or generated faces.

**Deliverable:** Twelve source-backed profiles that connect to Research.

### Task 5: Build Publications, Seminars, News, About

- [ ] Publications: one page, readable full citations grouped by type/year. Use real stable DOI/repository links. Add a subpage for a year only when the list grows.
- [ ] Seminars: confirmed upcoming talks first; then General and Student series with past events by academic year.
- [ ] News: latest 3–5 confirmed dated items and yearly archive.
- [ ] About: approved scope, school affiliation, collaboration text, verified public contact. Keep akamei@up.edu.mx unpublished until confirmed.
- [ ] Keep catalog pages text-led. Use images only when a real project, event, or news item benefits from one.

**Deliverable:** Four pages with useful archive headings and no demo data.

### Task 6: Preview and prepare the domain

- [ ] Preview phone, tablet, and desktop for all pages.
- [ ] Check navigation, topic links, citations, Drive sharing, image text alternatives, and YouTube playback.
- [ ] Check Sites search and embedded-file search after the draft is indexed and visible to a designated reviewer.
- [ ] Get owner verification for names, area/team mapping, institutional identity, photo permission, actual outputs/events, contact, and public audience.
- [ ] If the owner chooses a UP subdomain, have Site owner and Workspace administrator map it and confirm DNS/certificate status.
- [ ] Publish only after the content owner approves the final draft and the access route.

**Deliverable:** A review-ready private draft and launch checklist. Publishing remains the Site owner’s decision.

## Google Sites capabilities and references

Google Sites supports pages/subpages, built-in themes, phone/tablet/desktop preview, YouTube and Drive inserts, site search, and custom domains. Google documents search of embedded Drive files; indexing requires a published/indexed Site and access to the embedded files. Work/school custom-domain setup may require an administrator.

References: [Organize pages](https://support.google.com/sites/answer/98216?hl=en), [Drive/video embeds and embedded-file search](https://support.google.com/sites/answer/90569?hl=en), [Google Sites preview and publishing](https://support.google.com/sites/answer/6372878?hl=en-AU), [Custom domains](https://support.google.com/sites/answer/9068867?hl=en-aa).
