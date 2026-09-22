#!/usr/bin/env python3
"""Export a #M Productions logo SVG to PNG.

    python3 export.py hm-logo.svg -w 2000
    python3 export.py hm-logo.svg -w 2000 --bg "#16161a" --ink "#ffffff"
    python3 export.py hm-mark-accent.svg -w 512 -o favicon.png

Colours default to whatever the SVG's <style> block says; any --bg/--hash/--m/
--word/--ink flag overrides that for this export only, leaving the file alone.

The CSS custom properties are resolved into plain attributes before rendering,
so the renderer never has to understand var().
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)


def read_vars(text):
    """Pull the `--name: value;` declarations out of the <style> block."""
    return {
        m.group(1): m.group(2).strip()
        for m in re.finditer(r"--([\w-]+)\s*:\s*([^;]+);", text)
    }


def flatten(path, overrides, ink):
    """Return SVG markup with the variables baked into plain attributes."""
    with open(path) as fh:
        text = fh.read()

    values = read_vars(text)
    values.update({k: v for k, v in overrides.items() if v})

    def colour(name, fallback="#000000"):
        v = values.get(name, fallback)
        return ink if v == "currentColor" else v

    root = ET.fromstring(text)
    for style in root.findall(f"{{{SVG_NS}}}style"):
        root.remove(style)

    for el in root.iter():
        cls = el.get("class")
        target = el if cls else None
        if cls is None:
            # The paths sit inside a transformed <g>.
            continue
        if cls == "bg":
            target.set("fill", values.get("bg", "none"))
        elif cls == "hash":
            target.set("fill", colour("hash", ink))
        elif cls == "m":
            target.set("fill", colour("m", ink))
        elif cls == "word":
            target.set("fill", "none")
            target.set("stroke", colour("word", ink))
            target.set("stroke-width", values.get("word-weight", "55"))
            target.set("stroke-linejoin", "round")
        target.attrib.pop("class", None)

    return ET.tostring(root, encoding="unicode")


def viewbox(markup):
    vb = ET.fromstring(markup).get("viewBox").split()
    return float(vb[2]), float(vb[3])


def render(markup, out, width):
    """Rasterise with the best backend available."""
    vb_w, vb_h = viewbox(markup)
    height = round(width * vb_h / vb_w)

    try:
        import cairosvg

        cairosvg.svg2png(
            bytestring=markup.encode(), write_to=out,
            output_width=width, output_height=height,
        )
        return "cairosvg"
    except Exception:
        pass

    with tempfile.TemporaryDirectory() as tmp:
        src = os.path.join(tmp, "logo.svg")
        with open(src, "w") as fh:
            fh.write(markup)

        if shutil.which("rsvg-convert"):
            subprocess.run(
                ["rsvg-convert", "-w", str(width), "-h", str(height),
                 "-o", out, src],
                check=True,
            )
            return "rsvg-convert"

        # Last resort: Quick Look. It always flattens onto opaque white, so
        # transparency is lost, and it pads to a square that we crop back off.
        from PIL import Image

        subprocess.run(["qlmanage", "-t", "-s", str(max(width, height)),
                        "-o", tmp, src],
                       check=True, capture_output=True)
        thumb = os.path.join(tmp, "logo.svg.png")
        if not os.path.exists(thumb):
            sys.exit("No renderer available. Run: brew install cairo")
        im = Image.open(thumb).convert("RGBA")
        s = im.width
        cw, ch = (s, round(s * vb_h / vb_w)) if vb_w >= vb_h else (
            round(s * vb_w / vb_h), s)
        left, top = (s - cw) // 2, (s - ch) // 2
        im.crop((left, top, left + cw, top + ch)).resize(
            (width, height), Image.LANCZOS).save(out)
        return "qlmanage (background forced to white)"


def main():
    p = argparse.ArgumentParser(description="Export a logo SVG to PNG.")
    p.add_argument("svg")
    p.add_argument("-w", "--width", type=int, default=2000,
                   help="output width in pixels (default: 2000)")
    p.add_argument("-o", "--out", help="output file (default: <svg name>.png)")
    p.add_argument("--ink", default="#1d1d1d",
                   help="colour to use wherever the SVG says currentColor")
    for name in ("bg", "hash", "m", "word"):
        p.add_argument(f"--{name}", help=f"override the --{name} colour")
    a = p.parse_args()

    out = a.out or os.path.splitext(a.svg)[0] + ".png"
    markup = flatten(a.svg, {"bg": a.bg, "hash": a.hash, "m": a.m,
                             "word": a.word}, a.ink)
    backend = render(markup, out, a.width)
    print(f"{out}  ({a.width}px wide, via {backend})")


if __name__ == "__main__":
    main()
