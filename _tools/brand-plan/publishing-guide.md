# #M Productions — Publishing Guide

**Version 2.0 · May 2026**

-----

## How to Publish a Devlog Entry

1. Copy `_templates/devlog-entry.md` → `_devlog/slug.md`
   - The slug becomes the URL: `/devlog/slug/`
   - Sort order is controlled by the `date:` frontmatter field, not the filename
2. Fill in frontmatter (title, date, project, summary, description)
3. Write the entry body in Markdown
4. Commit and push to `main`
5. GitHub Pages builds and publishes automatically (~2 minutes)

## How to Publish a Book Review

1. Copy `_templates/book-review.md` (or `book-shelf.md`) → `_books/slug.md`
   - The slug becomes the URL: `/books/slug/`
2. Drop the cover image in `/images/books/slug.jpg`
3. Fill in frontmatter and write the review body
4. Commit and push

## Adding Video to a Devlog Entry

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

## Image Optimisation

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

## What Happens Automatically

- The sitemap at `/sitemap.xml` updates with every new entry
- The RSS feed at `/feed.xml` includes the new entry
- Schema.org markup (Article or Review) is generated from frontmatter
- Breadcrumb schema is generated for every devlog and book page
- Reading time is calculated and displayed on devlog entries
- `og:type: article` is applied to all collection entries automatically

## Adding a New Project to `_data/projects.yml`

The devlog project label is looked up from this file. To add a new project:

```yaml
your-slug: "Display Name"
```

Then use `project: your-slug` in the devlog entry frontmatter.

-----

## Devlog Entry Format

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

## Book Review Format

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
