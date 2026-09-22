# #M Productions — logo files

The artwork lives in `images/brand/` because the site serves it. The tooling and
these notes live here in `_tools/` because Jekyll never publishes an
underscore-prefixed directory — keep it that way, or the scripts end up on the
public site.

| File | Use |
|---|---|
| `images/brand/hm-logo.svg` | Full lockup: `#M` over outlined `PRODUCTIONS`. |
| `images/brand/hm-mark.svg` | `#M` only — favicons, avatars, anywhere small. |
| `_tools/brand/export.py` | Turns either of the above into a PNG. |
| `_tools/brand/generate.py` | Rebuilds both SVGs from the source typefaces. |

All commands below are run from the repo root.

Default colours are the brand orange `#F09040` for the `#` and navy `#386098`
for the `M` and the outlined word, both from `_config.yml`.

Typefaces: **M PLUS Rounded 1c Black** for `#M`, **Archivo Black** for
`PRODUCTIONS`. Both are SIL OFL. The letters are stored as outline paths, so
nothing needs the fonts installed — the files are self-contained.

There are no separate one-colour or accent files. The three parts are
independently addressable, so a single SVG covers every colourway.

## Changing the colours

Open either `.svg` in `images/brand/` in a text editor. The top of the file has a `<style>` block —
these five lines are the only thing you ever need to touch:

```css
svg {
    --bg: none;                  /* background: none | #ffffff | #16161a | … */
    --hash: #F09040;             /* the # */
    --m: #386098;                /* the M */
    --word: #386098;             /* PRODUCTIONS outline */
    --word-weight: 55;           /* outline thickness */
}
```

Replace a value with any CSS colour (`#5CB85C`, `white`, `rgb(0 0 0 / 50%)`).
`--hash`, `--m` and `--word` stay separate even though the last two match by
default, so you can recolour the `M` without touching the word, or vice versa.

`--bg: none` is a transparent background. Give it a colour and the logo gets a
solid panel behind it, filling the whole rectangle including the outer padding.

`--word-weight` is measured in the same units as the artwork, not pixels. 55 is
the default; 40 is noticeably finer, 75 is heavy.

Setting a part to `currentColor` makes it inherit whatever text colour surrounds
it — useful when the logo is embedded in a page that has both a light and a dark
mode, since one file then adapts to both.

### A few combinations

```css
--bg: none;      --hash: #F09040; --m: #386098; --word: #386098;  /* default */
--bg: none;      --hash: #F09040; --m: #ffffff; --word: #ffffff;  /* dark backgrounds */
--bg: #386098;   --hash: #F09040; --m: #ffffff; --word: #ffffff;  /* navy panel */
--bg: #F09040;   --hash: #ffffff; --m: #386098; --word: #386098;  /* orange panel */
--bg: none;      --hash: #F09040; --m: currentColor; --word: currentColor;  /* adapts to the page */
```

The other pillar accents work here too — green `#5CB85C` for books, blue
`#5B9BD5` for tech builds.

> One caveat: a handful of apps ignore stylesheets inside SVGs. Each shape also
> carries a plain `fill`/`stroke` attribute as a fallback, so those apps show the
> *default* orange-and-navy rather than your edits. Browsers, this repo's site,
> and `export.py` all read the `<style>` block correctly.

## Exporting a PNG

```sh
python3 _tools/brand/export.py images/brand/hm-logo.svg -w 2000
```

That writes `images/brand/hm-logo.png` at 2000px wide, height scaled to match.

| Flag | Does |
|---|---|
| `-w 2000` | Output width in pixels. Default 2000. |
| `-o name.png` | Output path. Defaults to the SVG's name. |
| `--bg "#ffffff"` | Override the background for this export only. |
| `--hash`, `--m`, `--word` | Override those parts for this export only. |
| `--ink "#ffffff"` | The colour to use wherever a part is set to `currentColor`. |

The override flags don't modify the SVG — they apply to that one PNG. Use them
to spin off variants without keeping a separate file for each:

```sh
# Avatar: white on navy
python3 _tools/brand/export.py images/brand/hm-mark.svg -w 512 --bg "#386098" --m "#ffffff" -o avatar.png

# Social card artwork on white
python3 _tools/brand/export.py images/brand/hm-logo.svg -w 2400 --bg "#ffffff" -o share.png

# Reversed out of an orange panel
python3 _tools/brand/export.py images/brand/hm-logo.svg -w 2000 --bg "#F09040" --hash "#ffffff" \
    --m "#386098" --word "#386098"
```

### About transparency

The script uses whichever renderer it finds. Right now this machine falls back
to macOS Quick Look, which **always flattens onto white** — fine when you pass a
`--bg`, but it means you can't get a transparent PNG yet. It tells you which
renderer it used on every run.

To enable transparent PNGs, install Cairo once:

```sh
brew install cairo
```

`cairosvg` is already installed via pip and starts working the moment Cairo is
there. Nothing else changes — the same commands then honour `--bg: none` and
write a real alpha channel. (`brew install librsvg` works as an alternative.)

For a transparent PNG once that's done, just leave `--bg` off:

```sh
python3 _tools/brand/export.py images/brand/hm-logo.svg -w 2000
```

## Rebuilding the SVGs

Only needed if you want to change the typefaces, spacing or proportions —
day-to-day colour changes don't require this.

```sh
pip install fonttools
python3 _tools/brand/generate.py
```

It rewrites `images/brand/hm-logo.svg` and `images/brand/hm-mark.svg` in place. The tuning knobs are the
keyword arguments of `build()` near the bottom of `generate.py`:

| Argument | Default | Controls |
|---|---|---|
| `gap_ratio` | `0.045` | Vertical gap between `#M` and `PRODUCTIONS`. |
| `tracking_em` | `0.10` | Letter-spacing on `PRODUCTIONS`. |
| `stroke_em` | `0.055` | Outline thickness (also the `--word-weight` default). |
| `pad_ratio` | `0.05` | Padding around the whole lockup. |

On first run it downloads the two `.ttf` files into `_tools/brand/fonts/`. That directory is
gitignored — M PLUS Rounded is 3.6MB and has no business in a site repo. The
SVGs don't need it; the letters are already outlines.

## Licensing

**Yes, both typefaces are free for commercial use.** Each is licensed under the
**SIL Open Font License 1.1**, confirmed in the fonts' own metadata:

| Typeface | Copyright | Licence |
|---|---|---|
| M PLUS Rounded 1c Black | 2016 The Rounded M+ Project Authors | OFL 1.1 |
| Archivo Black | 2017 The Archivo Black Project Authors ([Omnibus-Type](https://github.com/Omnibus-Type/ArchivoBlack)) | OFL 1.1 |

The OFL explicitly permits commercial use, modification and redistribution, and
using a font to set a logo is fine — the licence covers the *font software*, not
the artwork you make with it. Because the glyphs here are converted to outline
paths, the SVGs contain no font software at all, so the OFL doesn't propagate to
them. You can use this logo commercially and trademark it.

The three conditions that do apply, none of which this setup trips:

- **Don't sell the fonts on their own.** Bundling them inside a larger package
  is fine; selling the `.ttf` by itself is not. They aren't committed here anyway.
- **Keep the licence with the fonts** if you ever redistribute the `.ttf` files.
- **Don't release a modified font under its original name.** Neither font has a
  Reserved Font Name declared, and nothing here modifies or ships a font.

Not legal advice — but this is the ordinary, intended use of OFL fonts, and it's
why Google Fonts hosts them.
