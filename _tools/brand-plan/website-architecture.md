# #M Productions — Website Architecture

**Version 2.0 · May 2026**

-----

**Tech stack:** GitHub Pages (free hosting) · Jekyll (static site generator) · Markdown content files · HTML/CSS templates. No database, no server, no cost.

The Jekyll rebuild is complete. All pages are template-driven. New devlog entries and book reviews are written as Markdown files — no HTML required.

## Current Site Map

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

## Folder Structure

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
├── _tools/                  # Internal scripts and utilities (not processed by Jekyll)
│   ├── brand-plan.md        # Index of all brand/content docs
│   ├── process-media.py     # Image/video optimisation helper
│   └── strip-metadata.py    # Strips EXIF/metadata from images before committing
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
└── robots.txt               # Search engine directives
```

## Adding a New Project

1. Create `your-project.html` at the root with `layout: default`, `og_image`, and `og_url` in frontmatter
2. Add a social card image to `/images/social-pages/cards/`
3. Add a card to `productions.html` following the existing pillar card pattern
4. Add the slug → display name to `_data/projects.yml` if it will be used in devlog entries
5. Add the new URL to `_includes/contact.html` as `{% include contact.html id="N" %}` if a contact section is needed

## Key File Locations

|Task                          |File                                           |
|------------------------------|-----------------------------------------------|
|Add a devlog entry            |`_devlog/slug.md`                              |
|Add a book review             |`_books/slug.md`                               |
|Add a new project label       |`_data/projects.yml`                           |
|Update contact section        |`_includes/contact.html`                       |
|Change site colours           |`_config.yml` → `colors:`                     |
|Add a new social link         |`_config.yml` + `_layouts/default.html`        |
|Update Ikigai credits         |`ikigai/credits.md`                            |
|Update RHH credits            |`_includes/pokeemerald-expansion/credits.md`   |
|Generate Instagram carousel   |`_tools/canva-slideshow.py`                    |
|Optimise images/video         |`_tools/process-media.py`                      |
