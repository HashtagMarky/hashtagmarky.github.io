# Slideshow Generator

`_tools/slideshow.py` generates PNG slide images locally using Pillow. No API keys or accounts needed — all output is written to disk.

---

## Running

```bash
# List available payloads
python3 _tools/slideshow.py

# Run a specific payload (name or filename both work)
python3 _tools/slideshow.py my-campaign
python3 _tools/slideshow.py my-campaign.json

# Write output to a custom directory
python3 _tools/slideshow.py my-campaign --output /path/to/output
```

Output PNGs are written to `_tools/slideshow/output/<payload-name>/` as `01.png`, `02.png`, etc.

---

## Directory structure

```
_tools/
  slideshow.py
  slideshow/
    payloads/        ← JSON payload files go here
    fonts/           ← .ttf / .otf font files go here
    output/          ← generated PNGs (auto-created)
      my-campaign/
        01.png
        02.png
        ...
```

---

## Payload structure

A payload is a JSON file in `_tools/slideshow/payloads/`. Top-level fields set defaults for the whole slideshow; individual slides can override most of them.

### Top-level fields

| Field | Type | Default | Description |
|---|---|---|---|
| `dimensions` | string | `"square"` | Canvas size preset. See [Dimensions](#dimensions). |
| `font` | string | — | Font filename from `slideshow/fonts/`. Falls back to `PressStart2P-Regular.ttf`. |
| `maxFontSize` | number | `60` | Maximum font size for body text on text and link slides. |
| `bgColor` | string | `"black"` | Default background colour for all slides. |
| `textColor` | string | `"white"` | Default text colour for all slides. |
| `prefix` | number | `0` | Number of phantom slides to prepend to the dot indicator. See [Prefix](#prefix). |
| `slides` | array | required | List of slide objects. |

### Minimal example

```json
{
    "bgColor": "navy",
    "textColor": "white",
    "slides": [
        { "text": "Hello world." }
    ]
}
```

### Full example

```json
{
    "dimensions": "instagram",
    "font": "PressStart2P-Regular.ttf",
    "maxFontSize": 60,
    "bgColor": "navy",
    "textColor": "white",
    "prefix": 1,
    "slides": [
        {
            "type": "review-cover",
            "title": "The Name of the Wind",
            "author": "Patrick Rothfuss",
            "rating": 9
        },
        {
            "text": "A beautifully written fantasy that pulls you in from the first page."
        },
        {
            "type": "link",
            "message": "Read the full review",
            "link": "hashtagmarky.com/books/name-of-the-wind",
            "linkColor": "orange"
        }
    ]
}
```

---

## Slide types

Every slide inherits `bgColor`, `textColor`, and `font` from the top level. Any of these can be overridden per slide.

### text (default)

A plain slide with body text. Used when no `type` is set.

```json
{
    "text": "Your slide content goes here.",
    "bgColor": "navy",
    "textColor": "white",
    "font": "PressStart2P-Regular.ttf"
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `text` | string | yes | The slide body. Wraps automatically. Font size is scaled down to fit. |
| `bgColor` | string | no | Overrides the top-level background colour. |
| `textColor` | string | no | Overrides the top-level text colour. |
| `font` | string | no | Overrides the top-level font. |

Text is auto-sized between font size 20 and `maxFontSize` (default 60) to fill as much of the canvas as possible while staying within the padded area.

---

### review-cover

A book review cover slide with title, author, and star rating. Use `"type": "review-cover"`.

```json
{
    "type": "review-cover",
    "title": "The Name of the Wind",
    "author": "Patrick Rothfuss",
    "rating": 9,
    "bgColor": "orange",
    "textColor": "navy"
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `title` | string | yes | Book title. Auto-sized and wrapped to fit. |
| `author` | string | yes | Author name. Rendered at a fixed smaller size below the title. |
| `rating` | number | yes | Integer from 1–10. Divided by 2 internally to give a 0.5–5 star scale. |
| `bgColor` | string | no | Overrides the top-level background colour. |
| `textColor` | string | no | Overrides the top-level text colour. |
| `font` | string | no | Overrides the top-level font. |

Stars are rendered as Unicode characters: `★` (full), `½` (half), `☆` (empty). A rating of 9 gives `★★★★½☆`.

Layout order (vertically centred as a block): title → author → stars.

---

### link

A slide with a body message and a URL or handle on a separate line. Use `"type": "link"`.

```json
{
    "type": "link",
    "message": "Follow along for more!",
    "link": "hashtagmarky.com/devlog",
    "linkColor": "orange",
    "bgColor": "navy",
    "textColor": "white"
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `message` | string | yes | Main body text. Wraps and auto-sizes like a text slide. |
| `link` | string | yes | Link text. Always rendered on a single line, auto-sized to fit the width. |
| `linkColor` | string | no | Colour for the link line. Falls back to `textColor` if omitted. |
| `bgColor` | string | no | Overrides the top-level background colour. |
| `textColor` | string | no | Overrides the top-level text colour. |
| `font` | string | no | Overrides the top-level font. |

The message and link are laid out as a centred vertical block with a gap between them.

---

## Dimensions

Set with the top-level `"dimensions"` key. Defaults to `"square"`.

| Name | Size | Ratio | Use |
|---|---|---|---|
| `square` | 1080 × 1080 px | 1:1 | Instagram feed, takes up less vertical space in the feed |
| `instagram` | 1080 × 1350 px | 4:5 | Instagram portrait, takes up maximum vertical space in the feed |

**Which to use:**

- `square` — safe default. Works everywhere: feed, profile grid, and shares without cropping.
- `instagram` — fills more screen on mobile and performs better for engagement, but crops to square on the profile grid. Use when the extra vertical space meaningfully helps the layout (e.g. long titles on a review cover).

Add it to the top level of any payload:

```json
{
    "dimensions": "instagram",
    "bgColor": "orange",
    "textColor": "navy",
    "slides": [...]
}
```

If `"dimensions"` is omitted, it defaults to `"square"`.

---

## Colours

Colour values can be:

- **Named colours** from `_config.yml` — e.g. `"navy"`, `"orange"`, `"white"`. The script reads the `colors:` block automatically. Currently available:

| Name | Hex |
|---|---|
| `black` | `#000000` |
| `white` | `#ffffff` |
| `orange` | `#F09040` |
| `yellow` | `#F8D840` |
| `green` | `#5CB85C` |
| `red` | `#EA594d` |
| `blue` | `#5B9BD5` |
| `navy` | `#386098` |

- **Hex values** — e.g. `"#FF4500"`. Any valid CSS hex colour works directly.

Using an unrecognised name that isn't a hex value will exit with an error listing the available names.

---

## Fonts

Drop any `.ttf` or `.otf` file into `_tools/slideshow/fonts/` and reference it by filename in the payload:

```json
{ "font": "MyFont-Bold.ttf" }
```

If `font` is not set, or the named font file does not exist in the fonts directory, the script falls back to `PressStart2P-Regular.ttf`. If that is also missing, the script exits with an error.

Font size is determined automatically per slide using binary search to find the largest size that fits within the available area.

---

## Slide indicator (dots)

Every slide includes a row of dots in the bottom-right corner indicating position within the slideshow. The current slide is filled; all others are outlined. Dots are coloured using `textColor`.

### Prefix

If the generated slides are part of a larger carousel that includes slides produced outside this tool (e.g. a cover created in another app), use `"prefix"` to offset the dot position:

```json
{ "prefix": 1 }
```

With `"prefix": 1`, the first generated slide shows as dot 2 of N+1, the second as dot 3, and so on — as if one slide exists before the generated set. Set to any positive integer to account for multiple preceding slides.

---

## Book review payload

Book reviews on the website have a consistent front matter structure. This section explains how to translate that into a slideshow payload.

### Carousel structure

Instagram book review carousels follow this structure:

| Dot | Slide | Source |
|---|---|---|
| 1 | Book cover photo | Posted manually / separately — not generated |
| 2 | Review cover (title, author, stars) | `review-cover` slide |
| 3–N | Review highlights | `text` slides |
| N+1 | Link to full review | `link` slide |

Because the book cover is posted outside the generated set, use `"prefix": 1` so the dot indicator on all generated slides accounts for it.

### Mapping front matter to the payload

Each book page in `_books/` has the following relevant front matter fields:

| Front matter field | Used in payload as |
|---|---|
| `title` | `"title"` on the `review-cover` slide |
| `author` | `"author"` on the `review-cover` slide |
| `rating` | `"rating"` on the `review-cover` slide (1–10, halved internally to 0.5–5 stars) |
| `verdict` | A `text` slide — the verdict is the short punchy quote shown on the book page |
| permalink `/books/<slug>/` | `"link"` on the final `link` slide |

### Full example

```json
{
    "dimensions": "square",
    "bgColor": "orange",
    "textColor": "navy",
    "prefix": 1,
    "slides": [
        {
            "type": "review-cover",
            "title": "<title from front matter>",
            "author": "<author from front matter>",
            "rating": "<rating from front matter>"
        },
        {
            "text": "<verdict from front matter — paste verbatim>",
            "textColor": "white"
        },
        {
            "text": "<short punchy quote from the review body — one or two sentences, something intriguing rather than explanatory>"
        },
        {
            "text": "<another short quote, aim for 4 to 6 body slides total, each a self-contained thought, but one may be more poetic>"
        },
        {
            "type": "link",
            "message": "Full review available in my bio",
            "link": "hashtagmarky.com/books/<slug>",
            "linkColor": "white"
        }
    ]
}
```

### Notes

- **Colours** — the default scheme is orange background with navy text. The verdict slide overrides to white text. Body quote slides stay navy on orange. The link slide keeps the message navy but sets `linkColor: "white"` so only the URL line is white.
- **Rating** — use the raw value from front matter (1–10). The `review-cover` slide halves it internally, so `rating: 8` renders as `★★★★☆`.
- **Verdict** — use this as the first body slide verbatim. It is already written to be short and punchy. Set `"textColor": "white"` on this slide so the quote stands out.
- **Body slides** — pick 2–3 short quotes directly from your review, each as its own slide. The slideshow is a preview only, not the full review. Each quote should be a self-contained thought. Favour punchy, intriguing lines over explanatory ones. These inherit navy text on orange.
- **Link slug** — the slug matches the filename without `.md`. `_books/jade-city.md` → `hashtagmarky.com/books/jade-city`.
- **Link message** — always use `"Full review available in my bio"` as the message. The message inherits navy from the top level. Set `"linkColor": "white"` to make only the URL line white — do not set `"textColor"` on this slide or the message will also turn white.
- **Prefix** — always set to `1` for book reviews. The book cover image is the first slide in the carousel but is posted separately, so the dot count must include it.
