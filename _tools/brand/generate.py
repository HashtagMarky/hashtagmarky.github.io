#!/usr/bin/env python3
"""Regenerate images/brand/hm-logo.svg and images/brand/hm-mark.svg.

    pip install fonttools
    python3 _tools/brand/generate.py

Top line (#M)            : M PLUS Rounded 1c Black  - rounded, heavy
Bottom line (PRODUCTIONS): Archivo Black, stroked   - outlined

Both faces are SIL OFL and are converted to outlines, so the published SVG
carries no font dependency. Colours are exposed as CSS custom properties; the
# , the M and the outlined word stay independently addressable even though the
M and the word default to the same navy.

The two .ttf files are downloaded into fonts/ on first run rather than being
committed - M PLUS Rounded is 3.6MB, which has no business in a site repo.
"""

import os
import shutil
import subprocess
import urllib.request

from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Transform

HERE = os.path.dirname(os.path.abspath(__file__))
# This script lives in _tools/ so Jekyll never publishes it; the artwork it
# writes does need to be public, so it goes to images/brand/.
OUT = os.path.join(os.path.dirname(os.path.dirname(HERE)), "images", "brand")

GF = "https://github.com/google/fonts/raw/main/ofl"
FONTS = {
    "MPLUSRounded1c-Black.ttf": f"{GF}/mplusrounded1c/MPLUSRounded1c-Black.ttf",
    "ArchivoBlack-Regular.ttf": f"{GF}/archivoblack/ArchivoBlack-Regular.ttf",
}


def font_path(name):
    """Return the local .ttf, fetching it from Google Fonts if it isn't here."""
    d = os.path.join(HERE, "fonts")
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, name)
    if os.path.exists(p):
        return p

    print(f"fetching {name} …")
    try:
        urllib.request.urlretrieve(FONTS[name], p)
    except Exception:
        # The python.org build ships without CA certificates, so HTTPS from
        # urllib fails on a stock macOS install. curl is always there.
        if not shutil.which("curl"):
            raise
        subprocess.run(["curl", "-sSLf", "-o", p, FONTS[name]], check=True)
    return p


TOP_FONT = font_path("MPLUSRounded1c-Black.ttf")
BOT_FONT = font_path("ArchivoBlack-Regular.ttf")

ORANGE = "#F09040"   # _config.yml colors.orange
NAVY = "#386098"     # _config.yml colors.navy


class Line:
    """One run of text, measured in font units."""

    def __init__(self, font, text, tracking=0):
        self.gs = font.getGlyphSet()
        self.upem = font["head"].unitsPerEm
        cmap = font.getBestCmap()
        self.items = []
        x = 0
        for ch in text:
            g = cmap[ord(ch)]
            self.items.append((g, x))
            x += self.gs[g].width + tracking

        b = BoundsPen(self.gs)
        for g, ox in self.items:
            self.gs[g].draw(TransformPen(b, Transform().translate(ox, 0)))
        self.xMin, self.yMin, self.xMax, self.yMax = b.bounds
        self.width = self.xMax - self.xMin
        self.height = self.yMax - self.yMin

    def path(self, subset=None):
        pen = SVGPathPen(self.gs, ntos=lambda v: str(round(v, 1)))
        for i, (g, ox) in enumerate(self.items):
            if subset is None or i in subset:
                self.gs[g].draw(TransformPen(pen, Transform().translate(ox, 0)))
        return pen.getCommands()


def style_block(stroke=None):
    rows = [
        ("--bg", "none", "background: none | #ffffff | #16161a | …"),
        ("--hash", ORANGE, "the #"),
        ("--m", NAVY, "the M"),
    ]
    rules = [
        ".bg   { fill: var(--bg); }",
        ".hash { fill: var(--hash); }",
        ".m    { fill: var(--m); }",
    ]
    if stroke is not None:
        rows.append(("--word", NAVY, "PRODUCTIONS outline"))
        rows.append(("--word-weight", f"{stroke:.0f}", "outline thickness"))
        rules.append(
            ".word { fill: none; stroke: var(--word); "
            "stroke-width: var(--word-weight); stroke-linejoin: round; }"
        )
    decls = "\n".join(
        f"\t\t\t{n}: {v};".ljust(32) + f"/* {c} */" for n, v, c in rows
    )
    return ("\t<style>\n\t\tsvg {\n" + decls + "\n\t\t}\n"
            + "\n".join(f"\t\t{r}" for r in rules) + "\n\t</style>")


def group(line, scale, x, baseline, cls, subset=None, attrs=""):
    # Font units are y-up, SVG is y-down, hence the negative y scale.
    t = f"translate({x:.2f} {baseline:.2f}) scale({scale:.5f} {-scale:.5f})"
    return (f'\t<g transform="{t}"><path class="{cls}"{attrs} '
            f'd="{line.path(subset)}"/></g>')


def build(mark_only=False, tracking_em=0.10, gap_ratio=0.045,
          stroke_em=0.055, pad_ratio=0.05):
    top = Line(TTFont(TOP_FONT), "#M")
    W = 1000.0
    s_top = W / top.width
    pad = pad_ratio * W

    # Presentation attributes are the no-CSS fallback; the <style> block wins
    # wherever custom properties are supported.
    def top_parts(tx, ty):
        return [
            group(top, s_top, tx, ty, "hash", subset={0},
                  attrs=f' fill="{ORANGE}"'),
            group(top, s_top, tx, ty, "m", subset={1},
                  attrs=f' fill="{NAVY}"'),
        ]

    if mark_only:
        h = top.height * s_top
        box_w, box_h = W + pad * 2, h + pad * 2
        tx, ty = pad - top.xMin * s_top, pad + top.yMax * s_top
        return box_w, box_h, style_block(), top_parts(tx, ty)

    bot_font = TTFont(BOT_FONT)
    stroke = stroke_em * bot_font["head"].unitsPerEm
    bot = Line(bot_font, "PRODUCTIONS", tracking=tracking_em * bot_font["head"].unitsPerEm)
    # Justify to the same width, allowing for the stroke sitting half outside.
    s_bot = W / (bot.width + stroke)

    gap = gap_ratio * W
    top_h = top.height * s_top
    bot_h = bot.height * s_bot + stroke * s_bot

    box_w = W + pad * 2
    box_h = top_h + gap + bot_h + pad * 2

    tx, ty = pad - top.xMin * s_top, pad + top.yMax * s_top
    bx = pad - bot.xMin * s_bot + stroke * s_bot / 2
    by = pad + top_h + gap + bot.yMax * s_bot + stroke * s_bot / 2

    parts = top_parts(tx, ty)
    parts.append(group(
        bot, s_bot, bx, by, "word",
        attrs=(f' fill="none" stroke="{NAVY}" stroke-width="{stroke:.0f}"'
               ' stroke-linejoin="round"'),
    ))
    return box_w, box_h, style_block(stroke), parts


def svg(box_w, box_h, style, parts, title):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 '
        f'{box_w:.2f} {box_h:.2f}" role="img" aria-label="{title}">\n'
        f"\t<title>{title}</title>\n{style}\n"
        f'\t<rect class="bg" width="{box_w:.2f}" height="{box_h:.2f}" fill="none"/>\n'
        + "\n".join(parts) + "\n</svg>\n"
    )


if __name__ == "__main__":
    jobs = {
        "hm-logo.svg": (build(), "#M Productions"),
        "hm-mark.svg": (build(mark_only=True), "#M"),
    }
    os.makedirs(OUT, exist_ok=True)
    for fn, (geom, title) in jobs.items():
        p = os.path.join(OUT, fn)
        with open(p, "w") as fh:
            fh.write(svg(*geom, title=title))
        print(fn, os.path.getsize(p), "bytes")
