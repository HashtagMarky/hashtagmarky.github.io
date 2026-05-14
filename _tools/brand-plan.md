# #M Productions — HashtagMarky Brand & Content Plan

**Version 2.0 · May 2026**

> This document is the source of truth for the HashtagMarky brand. It covers who Marky is, what they make, how the website works, how content is structured, and what the plan is going forward.

-----

## Table of Contents

1. [Who is HashtagMarky](#1-who-is-hashtagmarky)
2. [Website Architecture](#2-website-architecture)
3. [Publishing Guide](#3-publishing-guide)
4. [Devlog Entry Format](#4-devlog-entry-format)
5. [Book Review Format](#5-book-review-format)
6. [Active Projects & Devlog Ideas](#6-active-projects--devlog-ideas)
7. [Instagram Strategy](#7-instagram-strategy)
8. [SEO Reference](#8-seo-reference)
9. [Domain & Branding](#9-domain--branding)
10. [Quick Reference](#10-quick-reference)

-----

## 1. Who is HashtagMarky

|Field      |Value                                                           |
|-----------|----------------------------------------------------------------|
|Handle     |@hashtagmarky (Instagram, TikTok) · @hashtagmrky (Twitter/X)    |
|Brand name |#M Productions                                                  |
|Description|Self-taught Pokémon ROM hacker, book lover, and tech builder    |
|Website    |hashtagmarky.github.io → custom domain (see Section 9)          |
|GitHub     |github.com/HashtagMarky                                         |
|YouTube    |@hashtag-marky                                                  |

### Brand Pillars

Everything Marky makes sits within three content pillars. Each pillar has its own visual accent colour used consistently across the website, devlog entries, and social posts.

|Pillar         |Content                                           |Accent Colour|Hex    |
|---------------|--------------------------------------------------|-------------|-------|
|🎮 ROM Hacking  |Pokémon Ikigai (active), future ROM hack projects |Orange       |#F09040|
|📚 Books        |Sci-fi & fantasy reviews, shelf entries           |Green        |#5CB85C|
|🔧 Tech & Builds|Lego Gameboy (in progress), Homelab (planned)     |Blue         |#5B9BD5|

Colours are defined in `_config.yml` under `colors:` and are applied site-wide through Jekyll-processed CSS. To change a colour, update `_config.yml` only — no CSS editing needed.

### Tone of Voice

- Conversational and honest — not corporate, not trying to be a brand account
- Specific over vague — names routes, book titles, exact problems
- Shows the work, including failures — build logs especially
- Nerd-fluent — comfortable with Pokémon lore, ROM hack terminology, hardware jargon

### Personal Brand vs Studio

HashtagMarky is a **personal brand**, not a studio. @hashtagmarky is the lead identity across all platforms. `#M Productions` works as a site/project label but the handle is the thing people follow and search for.

-----

## 2. Website Architecture

**Tech stack:** GitHub Pages (free hosting) · Jekyll (static site generator) · Markdown content files · HTML/CSS templates. No database, no server, no cost.

The Jekyll rebuild is complete. All pages are template-driven. New devlog entries and book reviews are written as Markdown files — no HTML required.

### Current Site Map

|URL                |Page                        |Notes                                      |
|-------------------|----------------------------|-------------------------------------------|
|`/`                |Homepage                    |Three pillars, about snapshot, contact     |
|`/ikigai`          |Pokémon Ikigai              |Project page — in development              |
|`/ikigai/credits`  |Ikigai Credits              |Ikigai + pokeemerald-expansion credits     |
|`/productions`     |#M Productions              |All projects overview                      |
|`/lablights`       |Pokémon Labradorescent Lights|Completed project page                     |
|`/devlog`          |Devlog feed                 |Auto-populated from `_devlog/` collection  |
|`/devlog/[slug]`   |Devlog entry                |e.g. `/devlog/ikigai-map-layout`           |
|`/books`           |Books index                 |Auto-populated from `_books/` collection   |
|`/books/[slug]`    |Book entry                  |e.g. `/books/the-name-of-the-wind`         |
|`/about`           |About                       |Full bio, tools, projects, social links    |

### Folder Structure

```
/
├── _config.yml              # Site settings, colours, collections, plugins
├── _data/
│   └── projects.yml         # Project slug → display name dictionary
├── _layouts/
│   ├── default.html         # Base template (header, nav, footer, all SEO meta)
│   ├── devlog.html          # Devlog entry layout (auto-applied to _devlog/)
│   └── book.html            # Book review/shelf layout (auto-applied to _books/)
├── _includes/
│   ├── contact.html         # Reusable contact section
│   └── pokeemerald-expansion/
│       └── credits.md       # RHH credits — update via CI when needed
├── _devlog/                 # Devlog entries — slug.md (date set in frontmatter)
├── _books/                  # Book entries — slug.md
├── _templates/              # Content templates (not processed by Jekyll)
│   ├── devlog-entry.md      # Copy to _devlog/ to start a new entry
│   ├── book-review.md       # Copy to _books/ for a full review
│   └── book-shelf.md        # Copy to _books/ for a shelf/to-read entry
├── assets/css/
│   ├── main.css             # Strata theme base styles
│   └── custom.css           # Jekyll-processed overrides (Liquid colour variables)
├── devlog/index.html        # Devlog feed page
├── books/index.html         # Books index page
├── ikigai/
│   ├── index.html           # Ikigai project page
│   ├── credits.html         # Credits page
│   ├── credits.md           # Ikigai credits data (excluded from Jekyll)
│   └── ikigai.md            # Ikigai description data (excluded from Jekyll)
├── index.html               # Homepage
├── about.md                 # About page
├── productions.html         # Productions overview page
├── lablights.html           # Labradorescent Lights page
├── 404.html                 # 404 page
├── robots.txt               # Search engine directives
└── brand-plan.md            # This document (excluded from Jekyll)
```

### Adding a New Project

1. Create `your-project.html` at the root with `layout: default`, `og_image`, and `og_url` in frontmatter
2. Add a social card image to `/images/social-pages/cards/`
3. Add a card to `productions.html` following the existing pillar card pattern
4. Add the slug → display name to `_data/projects.yml` if it will be used in devlog entries
5. Add the new URL to `_includes/contact.html` as `{% include contact.html id="N" %}` if a contact section is needed

-----

## 3. Publishing Guide

### How to Publish a Devlog Entry

1. Copy `_templates/devlog-entry.md` → `_devlog/slug.md`
   - The slug becomes the URL: `/devlog/slug/`
   - Sort order is controlled by the `date:` frontmatter field, not the filename
2. Fill in frontmatter (title, date, project, summary, description)
3. Write the entry body in Markdown
4. Commit and push to `main`
5. GitHub Pages builds and publishes automatically (~2 minutes)

### How to Publish a Book Review

1. Copy `_templates/book-review.md` (or `book-shelf.md`) → `_books/slug.md`
   - The slug becomes the URL: `/books/slug/`
2. Drop the cover image in `/images/books/slug.jpg`
3. Fill in frontmatter and write the review body
4. Commit and push

### Adding Video to a Devlog Entry

Videos are stored in `images/devlog/entry-slug/` alongside screenshots. The source recording is typically a `.MP4` screen capture at 4K (3240×2160 for GBA content).

**Convert for web** using ffmpeg. Output to a different name from the source to avoid macOS case-insensitive filesystem collisions:

```bash
ffmpeg -i source.MP4 -vf scale=1620:1080 -c:v libx264 -crf 12 output.mp4
```

- `scale=1620:1080` — 1080p at GBA's 3:2 aspect ratio (1920×1080 would distort it)
- `crf 12` — high quality; use `crf 28` for less important clips where file size matters more
- Keep audio by default; add `-an` only if the clip has no useful sound

**Extract a poster frame** (shown before the video loads):

```bash
ffmpeg -i output.mp4 -ss 00:00:00 -vframes 1 -vf scale=240:160 -update 1 poster.jpg
```

**Embed in Markdown** with `width` and `height` set to display at native GBA size (240×160) — the higher-resolution encode gives crispness on HiDPI screens:

```html
<video src="/images/devlog/entry-slug/output.mp4"
       poster="/images/devlog/entry-slug/poster.jpg"
       controls playsinline title="Description"
       width="240" height="160"></video>
```

**Side-by-side with a GIF or image**, wrap both in a flex div:

```html
<div style="display: flex; flex-wrap: wrap; gap: 8px; align-items: flex-start;">
  <video src="..." poster="..." controls playsinline title="..." width="240" height="160"></video>
  <img src="..." alt="..." width="240" height="160">
</div>
```

### Image Optimisation

All images committed to the site should be web-optimised before publishing. The rules below apply to everything in `images/`.

**Format rules:**
- Use **JPG** for all photos and opaque artwork
- Keep **PNG** only for images with true transparency (logos, overlays, favicons, social cards)
- Favicons in `images/infernape/favicon/` must always stay PNG

**Size rules — target under 300KB per image:**

| Image type | Max dimension |
|---|---|
| Book covers | 1200px longest side |
| Project box art / title screens | 1200px longest side |
| Devlog photos (GBA build etc.) | 1200px longest side |
| Character art / avatars | 1200px longest side |
| Game screenshots (full-width) | 1200px longest side |
| Devlog game captures (small inline) | Already small — leave as-is |

**How to convert and compress a new image:**

```bash
# Convert PNG → JPG (only if no real transparency)
sips -s format jpeg input.png --out output.jpg

# Resize to max 1200px and compress to ~80% quality
ffmpeg -i input.jpg \
  -vf "scale=w='min(iw,1200)':h='min(ih,1200)':force_original_aspect_ratio=decrease" \
  -q:v 4 -y output.jpg
```

**Checking for real transparency (before converting PNG → JPG):**

```python
from PIL import Image
img = Image.open("file.png").convert("RGBA")
print(any(p[3] < 255 for p in img.getdata()))  # True = keep as PNG
```

**What to keep as PNG:**
- `assets/css/images/overlay.png`
- `images/social-pages/cards/*.png` (Open Graph images)
- `images/social-pages/icons/discord-logo.png`
- `images/projects/lablight-title-screen*.png` (transparent background)

-----

### What Happens Automatically

- The sitemap at `/sitemap.xml` updates with every new entry
- The RSS feed at `/feed.xml` includes the new entry
- Schema.org markup (Article or Review) is generated from frontmatter
- Breadcrumb schema is generated for every devlog and book page
- Reading time is calculated and displayed on devlog entries
- `og:type: article` is applied to all collection entries automatically

### Adding a New Project to `_data/projects.yml`

The devlog project label is looked up from this file. To add a new project:

```yaml
your-slug: "Display Name"
```

Then use `project: your-slug` in the devlog entry frontmatter.

-----

## 4. Devlog Entry Format

Copy `_templates/devlog-entry.md` to `_devlog/slug.md` to start. The `layout`, `og_type`, and `sitemap` fields are set automatically — do not add them manually.

### Frontmatter Reference

```yaml
---
title: "Entry Title"
date: YYYY-MM-DD
project: ikigai
# project options: ikigai | lego-gameboy | homelab | or add to _data/projects.yml
episode: 1
summary: "One-sentence teaser shown on the devlog index card — also used as the
  meta description if no description is set. Write it like a search result."
description: "Slightly longer version for search engines and social sharing,
  if you want it separate from the summary."
# next_entry: "What comes next"
stats:
  Hours logged: 12
  Commits: 4
---
```

**Field notes:**
- `summary` — shown on the index feed card and used as meta description fallback
- `description` — only in `<meta>` tags, for search and social. Skip if summary covers it.
- `stats` — any key/value pairs, rendered as pills on the entry page
- `episode` — optional episode number shown in the meta line
- `next_entry` — optional teaser shown at the bottom of the entry

### Markdown Body Structure

**For Ikigai entries:**

```markdown
## What's Been Happening
2–3 sentence opening — specific, keyword-rich, reads like a search result.

## Screenshots
![Alt text describing what's shown](path/to/screenshot.png)
*Caption: name the location. "Route 3 entrance from the west" beats "screenshot 1".*

## Maps & Routes
What was built or revised. Name specific locations and design decisions.

## Mechanics & Code
Scripting changes, new features, bug fixes. Describe what changed and why.

## Story & Characters
Spoiler-lite story progress. New dialogue, rival scenes, character updates.
```

**For build log entries:**

```markdown
## The Situation
Where things stood at the end of the last entry and what this one covers.

## What I Built / Changed
The main update. "Used X instead of Y because Z" is useful. "Made progress" is not.

![Photo of build](path/to/photo.jpg)
*Caption: describe what's shown.*

## What Didn't Work
Optional but often the most valuable section. Name the problem clearly.

## Parts & Tools Used
- Part/tool name — why it was used or where it was sourced
```

**For feature branch entries** (standalone pokeemerald features published as their own branches):

```markdown
## Why I Made It
Personal motivation — what problem this solves or what dissatisfied you about the vanilla behaviour.
Keep it short. One or two sentences with a personal angle.

## What It Does
Describe the feature from a user/developer perspective. What changes, what options exist,
what it replaces.

![Screenshot or GIF](path/to/media.jpg)

## How It Works
Technical implementation. Name specific files, functions, structs, and config options.
Include any non-obvious constraints or design decisions.

### Configuration
Table of config options if the feature has a header file with defines.

### Adding / Extending
How another developer would add new items, options, or variants.

### Updates
Bullet list of post-release fixes and additions, dated by month and year.

## Installation
Link to the branch or diff. List any dependencies and any expansion-specific changes needed.

## Credits / Why It's In Ikigai
Who contributed or inspired the work, and why this feature exists in Pokémon Ikigai specifically.
```

**For expansion collaboration entries** (features merged into pokeemerald-expansion):

```markdown
## How It Started
The backstory — what existed before, who was involved, how the collaboration began.
Bullet points work well here for setting the scene quickly.

## How It Works
What the feature does from a player/developer perspective. Use a bullet list for the
feature set. Include a media block (video or GIF) at the top of this section.

<div style="display: flex; flex-wrap: wrap; gap: 8px; align-items: flex-start;">
  <video src="..." poster="..." controls playsinline title="..." width="240" height="160"></video>
  <img src="..." alt="..." width="240" height="160">
</div>

## How It Went
The development story — who did what, how the review process went, what was hard.
Be specific about contributions. End with the merge stats and PR link.

## What This Means for Ikigai
Why this matters for Pokémon Ikigai specifically. How it will be used.
```

### Devlog Checklist

- [ ] Frontmatter complete (title, date, project, summary)
- [ ] Description set if summary is too short for a meta description
- [ ] Opening paragraph is SEO-ready — specific, reads like a search result
- [ ] At least 2 screenshots or photos with descriptive alt text and captions
- [ ] 2–4 update sections (skip any section with nothing to report — don't pad)
- [ ] Under 600 words

-----

## 5. Book Review Format

Copy `_templates/book-review.md` or `_templates/book-shelf.md` to `_books/slug.md`. The `layout` and `og_type` are set automatically.

### Review Frontmatter

```yaml
---
title: "Book Title"
author: "Author Name"
date: YYYY-MM-DD
type: review
rating: 4
genres: [Fantasy, Epic]
pages: 000
year_published: 0000
# series: "Series Name #1"
image: "/images/books/slug.jpg"
verdict: "One-line pull quote shown above the review body."
description: "One or two sentences for search engines and social sharing."
# cr_via: "Audiobook — Audible"
---
```

### Shelf Frontmatter

```yaml
---
title: "Book Title"
author: "Author Name"
date: YYYY-MM-DD
type: shelf
genres: [Sci-fi]
# edition: "Hardcover"
image: "/images/books/slug.jpg"
description: "One or two sentences for search engines and social sharing."
# note: "Short note shown below the cover."
---
```

**Field notes:**
- `type` — `review` or `shelf`. Controls which layout template renders.
- `verdict` — pull-quote blockquote shown above the body. Make it memorable — it appears on the index card.
- `rating` — 1–5, integers only. Only used for `type: review`.
- `cr_via` — "currently read via", shown at the bottom of the entry.
- `description` — for `<meta>` tags only. Not shown on page.
- Review schema (star ratings in Google search results) is generated automatically for `type: review` entries.

### Markdown Body

Four short paragraphs, 200–350 words total:

```markdown
**One-sentence hook.** The most interesting thing about this book. Lead with it.

Plot summary, 2–3 sentences, no spoilers. Who, what, where — what makes it compelling.

Your actual take. Be specific — not "the writing was good" but "the second act drags
until the reveal in chapter 18."

Who should read this? Compare to something or note who it's not for.
```

### Book Review Checklist

- [ ] Cover image in `/images/books/` before publishing
- [ ] Frontmatter complete (type, rating, verdict, description)
- [ ] Four paragraphs: hook / plot / take / who's it for
- [ ] 200–350 words
- [ ] `verdict` is a memorable pull-quote, not a summary

> **Cross-posting tip:** The four-paragraph structure maps directly to an Instagram carousel — Slide 1: cover + rating, Slide 2: hook + plot, Slide 3: your take, Slide 4: who's it for + verdict. Write it once, post it twice.

-----

## 6. Active Projects & Devlog Ideas

### 🎮 Pokémon Ikigai

A custom Pokémon Emerald ROM hack built on pokeemerald-expansion. Original region (Vyraton), story, and mechanics. Player becomes a Gym Leader, not a challenger. In active development.

|Entry idea                  |Format notes                                                                            |
|----------------------------|----------------------------------------------------------------------------------------|
|State of the Project        |"Where things stand" intro entry. What exists, what's next, what the vision is.        |
|A specific route or area    |Name the location. What inspired the design? Screenshots of before/after if available.  |
|A mechanic or scripted event|What was implemented, why it was needed, what made it tricky.                           |
|A character or story beat   |Spoiler-lite. Who is this character, what role do they play.                            |
|A technical explainer       |How ROM hacking works, what pokeemerald-expansion adds, how a specific tool is used.    |
|A build comparison          |Side-by-side of an older version vs current. Shows progress visually.                   |

**SEO keywords:** `pokeemerald` · `pokeemerald-expansion` · `Pokémon Emerald ROM hack` · `GBA ROM hack` · `custom region Pokémon hack` · `Pokémon fan game` · `Pokémon Ikigai`

-----

### 🧱 Lego Gameboy (Project Hail Mary)

A functioning Gameboy-compatible handheld built inside a custom Lego shell. Goal: play Pokémon Ikigai on a device Marky built himself.

**Build phases:**

1. Research & parts list
2. Lego shell design and casing build
3. Hardware assembly (Pi, display, buttons)
4. Software setup (RetroPie or custom stack)
5. Play Ikigai on it — the finish line

|Entry idea          |Format notes                                                                               |
|--------------------|-------------------------------------------------------------------------------------------|
|Why Am I Doing This |Origin post. Motivation, inspiration, first sketches. Good for entry #1.                   |
|Parts List & Budget |What hardware, where from, running cost total.                                             |
|Shell Design        |The Lego build process for the casing. Photos at every stage.                              |
|Fitting the Hardware|Getting the Pi Zero inside. What didn't fit, what had to be redesigned.                    |
|Wiring & Buttons    |GPIO soldering, button input testing, first sign of life.                                  |
|Software Setup      |RetroPie install, emulator config, control mapping.                                        |
|The Finished Build  |Final result. Video if possible. Play Ikigai on it.                                        |

**SEO keywords:** `Raspberry Pi Gameboy` · `Lego Gameboy build` · `DIY Gameboy handheld` · `Raspberry Pi Zero portable gaming` · `RetroPie Lego case`

-----

### 🖥 Homelab (Planned)

A home server build for self-hosted services, NAS storage, and network experimentation.

|Entry idea         |Format notes                                               |
|-------------------|-----------------------------------------------------------|
|Why Build a Homelab|What it is, why it's useful, what the plan is. Entry #1.   |
|Hardware Selection |What to buy and why. Budget build vs rack setup.           |
|First Services     |What to self-host first (Nextcloud, Jellyfin, Pihole, etc.)|
|Networking         |VLANs, reverse proxy, remote access.                       |

**SEO keywords:** `homelab build` · `self-hosted server` · `beginner homelab` · `Nextcloud` · `Jellyfin` · `Pihole` · `home NAS`

-----

## 7. Instagram Strategy

Instagram is the primary social platform for the HashtagMarky brand. The goal is to grow both the ROM hacking and bookstagram audiences while cross-linking to the website for long-form content and SEO.

### Account Setup

|Setting     |Action                                                                                |
|------------|--------------------------------------------------------------------------------------|
|Account type|Switch to Creator account if not already — required for Google indexing of posts      |
|Bio         |`Pokémon ROM Hacker | Sci-Fi & Fantasy Bookstagram | Building Pokémon Ikigai`         |
|Link in bio |Live site URL                                                                         |
|Alt text    |Fill in on every post — Instagram uses it for indexing                                |

### Caption Structure

Every caption follows this structure regardless of post type:

```
[Hook — first line, no hashtags, keyword-rich sentence]
What I built: an image processor that runs in the browser.

[Body — 2–4 lines expanding on the hook]
No uploads, no server. Pure client-side JS using the Canvas API.
Drag in an image, pick a filter, download the result.

[Call to action]
Full breakdown on my site — link in bio.

[Hashtags — after a blank line, at the very end]
#pokemonromhack #pokeemerald #romhacking
```

**Why this order matters:** Instagram indexes the first line for search. It also truncates captions in the feed after ~125 characters, so the hook is what people see without tapping. Put the actual topic there — not a teaser, not a question, not an emoji string.

**Keyword placement rules:**
- First caption line: primary topic keyword (name the thing — "Route 3 redesign", "canvas image processor", "Name of the Wind review")
- Alt text on every image: describe what's literally shown + topic context. Do not leave it auto-generated.
- Location tag: add if relevant — it's an additional indexing signal

### Post Structure — Going Forward

**Content format by reach:**

| Format | Algorithm reach | Save/share weight | Notes |
|---|---|---|---|
| Reels | Highest — pushed to Explore | Medium | Best for discovery; first 1–3 seconds decide watch-time |
| Carousels | Medium | High — saves weighted more than likes | Underrated; high save rate signals quality content |
| Static image | Low | Low | Mostly reaches existing followers |
| Stories | Followers only — not indexed | — | Use for link stickers and driving traffic, not discovery |

**Book review post:**

- Carousel format: 5–7 slides
- Slide 1: Cover image + title + author + star rating
- Slide 2: Hook sentence + plot summary
- Slide 3: Your take
- Slide 4: Who's it for
- Slide 5: Verdict quote + rating breakdown
- Caption: first line = keyword-rich summary (title + author + one-word take). Hashtags at end.
- Alt text: `[Book title] by [Author] — [one sentence description]`

**Devlog / project post:**

- Reel format preferred for discovery (30–60 seconds)
- Show something moving — a route being walked, a map scrolling, a button press
- On-screen text overlay with key info; subtitles help retention
- Caption: episode number + 2–3 sentence summary + "full devlog at link in bio"
- Hashtags: 5–8 tags placed at the end after a blank line

### Driving Traffic to the Site

The goal of every post is to move people from Instagram to the site, where they stay longer and generate signals that improve search ranking.

**Mechanics:**
- **Link in bio** — point directly to `hashtagmarky.github.io` or use a tool like Later to create a multi-link landing page (latest devlog, books index, site home)
- **Link sticker in Stories** — available to all accounts. Post a Story teasing a devlog or review, add a link sticker pointing to the specific post URL (`/devlog/slug/` or `/books/slug/`)
- **Explicit CTA in every caption** — "full breakdown at link in bio" or "read the devlog at link in bio." People don't click unless prompted.
- **Reels that cut off** — show 30 seconds of a project walkthrough then end with "full writeup on my site" — traffic from that Reel is a behavioral signal Google weights

**Note on Instagram links and SEO:** Instagram profile links are `nofollow` — they don't pass link authority directly to your site. The SEO value comes from the referral traffic itself. People arriving from Instagram and spending time on your site is a behavioral signal. Build brand association around your name and niche so that when people search `hashtagmarky` or `pokémon ikigai rom hack`, your site ranks because they already know to look for it.

### Hashtag Strategy

**Volume mix — aim for 5–10 tags per post:**

| Type | Volume | Example | Purpose |
|---|---|---|---|
| Broad | 1M–10M posts | `#pokemonromhack` | Visibility ceiling — you won't rank but you get seen by followers of the tag |
| Mid | 50k–500k posts | `#pokeemerald` | Realistic ranking potential — most value here |
| Niche | 5k–50k posts | `#pokemonroutescripting` | High signal-to-noise, smaller but engaged audience |

**Avoid tags with 10M+ posts** — your post will never surface in them. The feed moves too fast.

**Maintain a consistent core set of 10–15 tags** across posts in the same content pillar. Instagram uses tag history to classify your account. Jumping between unrelated tags every post resets that signal.

**Tag sets by pillar:**

- ROM hacking: `#pokemonromhack` · `#pokeemerald` · `#romhacking` · `#gbaromhack` · `#pokeemeraldexpansion` · `#pokemonhack`
- Books: `#bookstagram` · `#scifibooks` · `#fantasybooks` · `#bookreview` · + exact series/author tag when applicable
- Lego Gameboy / builds: `#buildlog` · `#raspberrypi` · `#diygameboy` · `#legotech` · `#raspberrypizero`

**Posting cadence:** Consistency beats frequency. Three posts per week maintained is worth more to the algorithm than seven posts one week then nothing. The engagement window after posting is roughly the first hour — reply to comments in that window.

### Account Setup

| Setting | Action |
|---|---|
| Account type | Switch to **Creator** (not Business) — required for Insights and Google indexing of posts |
| Bio | `Pokémon ROM Hacker \| Sci-Fi & Fantasy Bookstagram \| Building Pokémon Ikigai` |
| Link in bio | Live site URL (or Later multi-link if linking to specific posts) |
| Alt text | Fill in on every post — Instagram uses it for indexing. Write it, don't leave it auto-generated. |
| Category label | Set to match your niche — signals context to the algorithm |

**Why Creator over Business:** Same analytics access, more flexible link-in-bio options, better DM organisation. Business accounts are for companies with ad spend. Creator is right for solo builders and content creators.

-----

## 8. SEO Reference

### What's Implemented

All SEO groundwork is in place. The following are live:

|Feature                        |Implementation                                                   |
|-------------------------------|-----------------------------------------------------------------|
|Canonical tags                 |`<link rel="canonical">` in default layout                       |
|Sitemap                        |Auto-generated by `jekyll-sitemap` — updates on every build      |
|RSS feed                       |Auto-generated by `jekyll-feed` at `/feed.xml`                   |
|robots.txt                     |Allows all crawlers, points to sitemap                           |
|`lang="en"` on `<html>`        |Default layout                                                   |
|Open Graph tags                |All pages — title, description, image, type, locale, URL         |
|`og:locale`                    |`en_GB` site-wide                                                |
|`og:type`                      |`website` by default, `article` auto-set for devlog/books        |
|Twitter/X Cards                |Summary large image, with `twitter:creator` attribution          |
|Schema.org Person              |Homepage — links all social profiles to the same identity        |
|Schema.org Article             |Auto-generated on every devlog entry                             |
|Schema.org Review              |Auto-generated on book reviews — enables star ratings in Google  |
|Schema.org BreadcrumbList      |Auto-generated on all devlog and book pages                      |
|Meta description fallback chain|`description` → `summary` → site description                     |
|`og:type: profile`             |About page                                                       |
|404 excluded from sitemap      |`sitemap: false` on 404.html                                     |

### Targeting "Pokémon Ikigai" in Search

Currently the name is effectively unclaimed for the ROM hack meaning. Gap exists because of limited indexed content — will close as content builds.

|Action                                                      |Impact                                               |When                  |
|------------------------------------------------------------|-----------------------------------------------------|----------------------|
|3+ devlog entries with "Pokémon Ikigai" in title and summary|Stacks indexed pages all pointing to the same project|When publishing begins|
|PokéCommunity forum thread for Ikigai                       |High-authority backlink pointing to your site        |When ready            |
|Submit to Hackdex / ROM hack listing sites                  |More backlinks, community discovery                  |After content exists  |
|YouTube video or Reel with "Pokémon Ikigai" in title        |Video results appear in Google search                |When ready            |

**Realistic timeline:**

- "Pokémon Ikigai ROM hack" — rankable within **2–4 weeks** of first content being published
- "Pokémon Ikigai" — rankable within **2–3 months** as content builds up

### Meta Descriptions (Current)

```
/
Pokémon ROM Hacker & Bookstagrammer — follow the development of Pokémon Ikigai,
a custom GBA ROM hack, plus sci-fi and fantasy book reviews.

/ikigai
Pokémon Ikigai — a custom Pokémon Emerald ROM hack built on pokeemerald-expansion.
Original region, story, and mechanics.

/devlog
Development logs and build diaries — Pokémon Ikigai ROM hack updates,
a Lego Gameboy build, and future tech projects by HashtagMarky.

/books
Sci-fi and fantasy book reviews by HashtagMarky — honest takes, star ratings,
and reading recommendations from a book lover and audiobook listener.

/about
HashtagMarky — self-taught Pokémon ROM hacker, book lover, and tech builder.
Creator of Pokémon Ikigai.

/productions
All projects and releases by #M Productions — Pokémon Ikigai, Pokémon
Labradorescent Lights, and future releases.
```

### Keyword Reference

|Content     |Keywords to use naturally                                                                                                                                           |
|------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|ROM Hacking |`pokeemerald` · `pokeemerald-expansion` · `Pokémon Emerald ROM hack` · `GBA ROM hack` · `custom region Pokémon hack` · `Pokémon fan game` · `self-taught ROM hacker`|
|Lego Gameboy|`Raspberry Pi Gameboy` · `Lego Gameboy build` · `DIY handheld` · `Raspberry Pi Zero portable` · `RetroPie Lego case`                                                |
|Homelab     |`homelab build` · `self-hosted server` · `Nextcloud` · `Jellyfin` · `Pihole` · `home NAS` · `beginner homelab`                                                      |
|Books       |`sci-fi book review` · `fantasy book review` · `bookstagram` · exact book title · exact author name · series name                                                   |

> **The most important SEO rule:** Each devlog entry is a new indexed page. Write the opening paragraph of every entry like a search result snippet — specific, keyword-rich, useful. Twenty devlog entries means twenty pages Google can find. This compounds over time.

-----

## 9. Domain & Branding

### The Branding Decision

**Stick with the personal brand. No rebrand needed.**

- **@hashtagmarky** = the person, the social handle, what people search
- **#M Productions** = the site/umbrella label, used in the site title and branding

### Domain Options

|Domain              |Verdict                                                                                                                    |
|--------------------|---------------------------------------------------------------------------------------------------------------------------|
|`hashtagmarky.dev`  |**Best choice.** Matches the handle exactly. `.dev` signals tech/builder. Best SEO alignment with social handle.          |
|`hashtagmarky.com`  |Strong fallback. Most recognisable TLD. Good for broader non-tech audiences.                                               |
|`hashtagmarky.co.uk`|Only if you want to explicitly signal UK base. Limits international discovery slightly.                                    |

### Custom Domain Setup (When Ready)

1. Buy the domain (Namecheap or Porkbun — both ~£10/year)
2. In the registrar, add a `CNAME` record pointing to `hashtagmarky.github.io`
3. In GitHub repo Settings → Pages → Custom domain, enter the domain
4. Enable **Enforce HTTPS** — GitHub provides the SSL certificate free
5. Update all social bio links to the new domain

-----

## 10. Quick Reference

### Devlog Checklist

- [ ] Frontmatter complete (title, date, project, summary)
- [ ] `description` set if summary is too short for a meta description
- [ ] Opening paragraph reads like a search result — specific, keyword-rich
- [ ] At least 2 screenshots/photos with descriptive alt text and captions
- [ ] 2–4 update sections (skip empty sections — don't pad)
- [ ] Under 600 words

### Book Review Checklist

- [ ] Cover image in `/images/books/` before publishing
- [ ] Frontmatter complete — type, rating (if review), verdict, description
- [ ] Four paragraphs: hook / plot / take / who's it for
- [ ] 200–350 words
- [ ] `verdict` is memorable — it shows on the index card

### Instagram Post Checklist

- [ ] First caption line contains the primary keyword (names the thing — not a teaser)
- [ ] Caption ends with a CTA pointing to the site ("full devlog at link in bio")
- [ ] Hashtags placed at the end after a blank line — 5–10 tags, mix of broad/mid/niche
- [ ] Alt text written on every image (not auto-generated)
- [ ] Bio link is up to date (site URL or multi-link landing page)
- [ ] Creator account mode active (required for Insights and Google indexing)
- [ ] For devlog posts: link sticker Story published pointing to the specific `/devlog/slug/` URL
- [ ] Replied to comments within the first hour after posting

### Project Colour Reference

- 🎮 ROM Hacking / Ikigai — Orange `#F09040`
- 📚 Books — Green `#5CB85C`
- 🔧 Tech & Builds — Blue `#5B9BD5`

Colours are defined in `_config.yml` → `colors:`. Changing them there updates the whole site.

### Key File Locations

|Task                          |File                                 |
|------------------------------|-------------------------------------|
|Add a devlog entry            |`_devlog/slug.md`                    |
|Add a book review             |`_books/slug.md`                     |
|Add a new project label       |`_data/projects.yml`                 |
|Update contact section        |`_includes/contact.html`             |
|Change site colours           |`_config.yml` → `colors:`           |
|Add a new social link         |`_config.yml` + `_layouts/default.html`|
|Update Ikigai credits         |`ikigai/credits.md`                  |
|Update RHH credits            |`_includes/pokeemerald-expansion/credits.md`|

-----

*#M Productions · HashtagMarky Brand & Content Plan · v2.0 · May 2026*
