# Tools

Scripts for preparing site media and social content. They live in `_tools/`
because Jekyll never publishes an underscore-prefixed directory, so none of this
ends up on the public site.

All commands below are run from the **repo root**.

| Tool | Does |
|---|---|
| [`review-reel.py`](#review-reelpy) | Turns a book cover into a 9:16 zoom-out video for Instagram Reels. |
| [`slideshow.py`](#slideshowpy) | Generates PNG slides for Instagram carousels from a JSON payload. |
| [`process-media.py`](#process-mediapy) | Converts images to JPEG, resizes them for the web, strips metadata. |
| [`strip-metadata.py`](#strip-metadatapy) | Strips metadata from images and videos without resizing. |
| [`brand/`](#brand) | Exports and rebuilds the #M Productions logo. |

**Requirements:** Python 3, Pillow (`pip install Pillow`) and ffmpeg
(`brew install ffmpeg`). The brand tools need a little more; see their README.

---

## review-reel.py

Makes a 1080×1920 MP4 from a book cover. The cover sits over a blurred copy of
itself. The video starts zoomed in on a point you choose, zooms out until the
cover fills the screen width, then holds still. There's no audio or text, so
captions, voiceover and music are added in the Instagram editor.

```sh
python3 _tools/review-reel.py jade-city                          # all defaults
python3 _tools/review-reel.py jade-city --focus 0.5,0.33 --zoom 2.1
python3 _tools/review-reel.py jade-city --focus 0.5,0.33 --zoom 2.1 --preview
python3 _tools/review-reel.py images/books/jade-city.jpg         # any image works
```

The input can be a review slug (it reads `image:` from `_books/<slug>.md`), a
review `.md` file, or an image path.

Videos are written to `_tools/reels/output/<name>.mp4`, which is gitignored.
A 15 second video takes about 40 seconds to render.

### Flags

| Flag | Default | Does |
|---|---|---|
| `--focus X,Y` | `0.5,0.5` | The point the video starts zoomed in on, as fractions of the image. |
| `--zoom Z` | `1.5` | How far zoomed in the first frame is. `1` means no zoom. |
| `--duration S` | `15` | Video length in seconds. |
| `--zoom-start S` | `0` | Second the zoom-out begins. The first frame holds still until then. |
| `--speed V` | `0.05` | How fast it zooms out, in zoom per second. |
| `--zoom-end S` | — | Second the zoom-out finishes. Overrides `--speed`. |
| `--size F` | `1` | Cover width at the end, as a fraction of the screen. `1` is full width; `0.85` leaves blurred strips down the sides. |
| `--blur R` | `40` | Background blur strength. |
| `--preview` | — | Saves a PNG of the first and last frames instead of a video. Takes about a second. |
| `-o PATH` | — | Output file. |

The defaults for zoom, duration and speed are constants near the top of the
script (`DEFAULT_ZOOM`, `DEFAULT_DURATION`, `DEFAULT_SPEED`) if you want to
change them permanently.

### Choosing the starting point

`--focus X,Y` uses fractions of the image, so it works whatever the image size:
`0,0` is the top-left corner, `1,1` is the bottom-right and `0.5,0.5` is the
centre. In the first frame, that point is in the middle of the screen.

`--zoom` sets how much is visible around it. At the default `--size 1`:

- **width shown** = image width ÷ zoom
- **height shown** = width shown × 1.78 (the screen is 9:16)

To plan from pixels, open the image in any editor that shows cursor
coordinates and find the point you want to start on and roughly how wide the
first frame should be. Then:

- **focus** = point's x ÷ image width, point's y ÷ image height
- **zoom** = image width ÷ the width you want the first frame to show

For example, Jade City's image is 1055×1200. To start on the title at about
(530, 400) with about 500px across:

```sh
# focus = 530/1055, 400/1200 ≈ 0.5, 0.33    zoom = 1055/500 ≈ 2.1
python3 _tools/review-reel.py jade-city --focus 0.5,0.33 --zoom 2.1 --preview
```

Every run prints the area the first frame covers, in image pixels:

```
Image is 1055×1200px. First frame shows x 276–779, y -51–843 (values outside the image are blurred background)
```

`--preview` saves `_tools/reels/output/<name>-preview.png`. The left half is the
first frame. The right half is the last frame with a red box around the
starting area and a cross on the focus point. Adjust and re-run until it looks
right, then drop `--preview` to render the video.

### Timing: duration, zoom start, speed and zoom end

A video has up to three parts:

```
0s            --zoom-start           zoom end                 --duration
|-- hold still --|------ zooming out ------|------ hold still ------|
   (first frame)                              (full cover)
```

- **`--duration`** is the total length. It never changes because of the other
  flags.
- **`--zoom-start`** is when the movement begins. Use it to hold on the
  zoomed-in detail for a moment, e.g. while the hook text is on screen.
- **When the zoom ends** is set one of two ways:
  - **By speed (default):** zoom end = zoom start + (zoom − 1) ÷ speed. At the
    default speed of `0.05`, a `1.5` zoom takes 10s and a `2` zoom takes 20s.
    Because it's a rate, a deeper zoom takes longer, but the motion looks the
    same from video to video.
  - **By time:** `--zoom-end` sets the exact second and ignores `--speed`.
- Whatever is left after the zoom ends holds on the full cover.

The movement eases in and out, so it starts and stops gently. `--speed` is the
average speed across the zoom; it moves fastest in the middle.

If the zoom would end after the video does, it's sped up to finish on the last
frame and the script prints a note. Each run prints the timing it used:

```
Holds 2s, zooms out 2–12.0s, then holds 3.0s
```

Examples:

| Command | Result |
|---|---|
| defaults | Zooms 1.5 → 1 over 0–10s, holds 5s. |
| `--zoom 1.25` | Zooms over 0–5s, holds 10s. |
| `--zoom-start 3` | Holds 3s, zooms over 3–13s, holds 2s. |
| `--speed 0.1` | Faster: zooms over 0–5s, holds 10s. |
| `--zoom-start 2 --zoom-end 4` | Holds 2s, zooms over 2–4s, holds 11s. |
| `--zoom 3 --duration 10 --zoom-start 2` | Zoom would need until 42s, so it's sped up to finish at 10s. |
| `--zoom 2 --duration 25` | Zooms over 0–20s, holds 5s. |

### Finishing in Instagram

Upload the MP4 as a Reel, then add your voiceover, the **Captions** sticker for
auto-subtitles, the verdict and rating as text, and music. Record the voiceover
in Instagram rather than elsewhere so auto-captions can pick it up.

---

## slideshow.py

Generates PNG slides for Instagram carousels from a JSON payload, using Pillow.
No accounts or API keys needed.

```sh
python3 _tools/slideshow.py                 # list available payloads
python3 _tools/slideshow.py jade-city       # _tools/slideshow/payloads/jade-city.json
python3 _tools/slideshow.py jade-city --output /path/to/folder
```

Payloads go in `_tools/slideshow/payloads/` and slides are written to
`_tools/slideshow/output/<payload-name>/01.png`, `02.png`, and so on. Both
folders are gitignored. Fonts go in `_tools/slideshow/fonts/`.

The full payload format (slide types, colours, dimensions, fonts, link
placement) is documented in
[`brand-plan/slideshow.md`](brand-plan/slideshow.md) and at the top of
`slideshow.py`.

---

## process-media.py

Prepares images for the site: converts them to JPEG, resizes them, and strips
all metadata (including location data). Files are changed **in place**. A PNG
converted to JPEG has the original PNG deleted.

```sh
python3 _tools/process-media.py --dry-run       # preview what would change
python3 _tools/process-media.py                 # process everything in images/
python3 _tools/process-media.py images/books    # just one folder or file
```

Images are shrunk to fit a maximum size depending on their folder, keeping
their aspect ratio:

| Folder | Max size |
|---|---|
| `images/books` | 600×900 |
| `images/projects` | 1200×800 |
| `images/devlog` | 1200×900 |
| `images/infernape` | 800×800 |
| anything else | 1200×900 |

These are never resized, only stripped:
- GIFs, which stay as GIFs
- social cards and icons in `social-pages/cards` and `social-pages/icons`
- GBA screenshots (240×160 and its 2×, 3× and 4× sizes)

Anything in a `favicon` folder is left completely alone. Videos are stripped of
metadata too. The size rules are in `SIZE_RULES` at the
top of the script.

---

## strip-metadata.py

Strips metadata from images and videos in place, without converting or
resizing anything. Use it for files that must keep their exact format and size.

```sh
python3 _tools/strip-metadata.py --dry-run
python3 _tools/strip-metadata.py                # everything in images/
python3 _tools/strip-metadata.py path/to/file.jpg
```

---

## brand/

Exports the #M Productions logo to PNG in any colourway, and rebuilds the logo
SVGs from their typefaces.

```sh
python3 _tools/brand/export.py images/brand/hm-logo.svg -w 2000
```

Colours, export flags, transparency setup, rebuilding and font licensing are
covered in [`brand/README.md`](brand/README.md).
