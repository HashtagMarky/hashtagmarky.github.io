#!/usr/bin/env python3
"""
instagram-slideshow.py — Generate Instagram slideshow images locally using Pillow.

No API keys or accounts needed. Colours, text, and layout are fully controlled
via the payload.

USAGE
-----
    python3 instagram-slideshow.py                   # lists available payloads
    python3 instagram-slideshow.py my-campaign       # instagram-slideshow/payloads/my-campaign.json
    python3 instagram-slideshow.py my-campaign.json  # same

Output is written to instagram-slideshow/output/<payload-name>/ by default.

FONTS
-----
Drop any .ttf or .otf file into instagram-slideshow/fonts/ and reference it by
filename in the payload:

    "font": "MyFont-Bold.ttf"

If omitted, the script falls back to Helvetica Neue (macOS system font).

INPUT FORMAT
------------
{
    "font": "MyFont-Bold.ttf",
    "maxFontSize": 72,
    "slides": [
        {
            "text": "First slide text",
            "textColor": "#ffffff",
            "bgColor": "#1a1a2e"
        },
        {
            "text": "Second slide text",
            "textColor": "#000000",
            "bgColor": "#f5f5f5",
            "font": "MyFont-Regular.ttf"
        }
    ]
}

maxFontSize caps how large the text can grow (default: 72). Per-slide font
overrides the top-level font.
"""

import argparse
import json
from pathlib import Path

from PIL import Image, ImageColor, ImageDraw, ImageFont

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR / "instagram-slideshow"
PAYLOADS_DIR = DATA_DIR / "payloads"
FONTS_DIR = DATA_DIR / "fonts"

WIDTH = 1080
HEIGHT = 1350
PADDING = 100
LINE_SPACING = 1.4
DEFAULT_MAX_FONT_SIZE = 60

DOT_RADIUS = 6
DOT_SPACING = 20  # center to center

SYSTEM_FONT_FALLBACKS = [
    "/System/Library/Fonts/HelveticaNeue.ttc",
    "/System/Library/Fonts/Helvetica.ttc",
    "/System/Library/Fonts/Arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]

# ---------------------------------------------------------------------------
# Font loading
# ---------------------------------------------------------------------------

def _load_font(name: str | None, size: int) -> ImageFont.FreeTypeFont:
    if name:
        custom = FONTS_DIR / name
        if custom.exists():
            return ImageFont.truetype(str(custom), size)
    
    raise SystemExit(f"  Warning: font '{name}' not found in {FONTS_DIR}/.")


# ---------------------------------------------------------------------------
# Text layout
# ---------------------------------------------------------------------------

def _wrap_text(text: str, font: ImageFont.FreeTypeFont, max_width: int, draw: ImageDraw.ImageDraw) -> list[str]:
    words = text.split()
    lines = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if draw.textlength(candidate, font=font) <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def _fit_font(text: str, font_name: str | None, max_width: int, max_height: int, max_size: int, draw: ImageDraw.ImageDraw) -> tuple[ImageFont.FreeTypeFont, list[str]]:
    lo, hi = 20, max_size
    best_font = _load_font(font_name, lo)
    best_lines = [text]

    while lo <= hi:
        mid = (lo + hi) // 2
        font = _load_font(font_name, mid)
        lines = _wrap_text(text, font, max_width, draw)
        line_height = font.size * LINE_SPACING
        total_height = line_height * len(lines)

        if total_height <= max_height:
            best_font = font
            best_lines = lines
            lo = mid + 1
        else:
            hi = mid - 1

    return best_font, best_lines


# ---------------------------------------------------------------------------
# Slide indicator
# ---------------------------------------------------------------------------

def _draw_indicator(draw: ImageDraw.ImageDraw, slide_num: int, total: int, text_color: str, bg_color: str) -> None:
    total_width = (total - 1) * DOT_SPACING
    right_x = WIDTH - PADDING
    start_x = right_x - total_width
    y = HEIGHT - PADDING

    for i in range(total):
        x = start_x + i * DOT_SPACING
        bbox = [x - DOT_RADIUS, y - DOT_RADIUS, x + DOT_RADIUS, y + DOT_RADIUS]
        if i == slide_num - 1:
            draw.ellipse(bbox, fill=text_color)
        else:
            draw.ellipse(bbox, outline=text_color, width=2)


# ---------------------------------------------------------------------------
# Slide rendering
# ---------------------------------------------------------------------------

def render_slide(text: str, bg_color: str, text_color: str, font_name: str | None, max_font_size: int, slide_num: int, total_slides: int) -> Image.Image:
    img = Image.new("RGB", (WIDTH, HEIGHT), bg_color)
    draw = ImageDraw.Draw(img)

    max_text_width = WIDTH - PADDING * 2
    max_text_height = HEIGHT - PADDING * 2

    font, lines = _fit_font(text, font_name, max_text_width, max_text_height, max_font_size, draw)
    line_height = font.size * LINE_SPACING
    total_text_height = line_height * len(lines)

    y = (HEIGHT - total_text_height) / 2

    for line in lines:
        line_width = draw.textlength(line, font=font)
        x = (WIDTH - line_width) / 2
        draw.text((x, y), line, font=font, fill=text_color)
        y += line_height

    _draw_indicator(draw, slide_num, total_slides, text_color, bg_color)

    return img


# ---------------------------------------------------------------------------
# Payload resolution
# ---------------------------------------------------------------------------

def _resolve_payload(name: str | None) -> Path:
    if name is None:
        available = sorted(PAYLOADS_DIR.glob("*.json"))
        if not available:
            raise SystemExit(
                f"No payloads found in {PAYLOADS_DIR}/\n"
                "Create a JSON payload there and pass its name as the first argument."
            )
        names = "\n  ".join(p.stem for p in available)
        raise SystemExit(f"Available payloads:\n  {names}\n\nUsage: python instagram-slideshow.py <name>")

    candidate = Path(name)
    if candidate.is_absolute() or candidate.exists():
        return candidate

    stem = candidate.stem if candidate.suffix == ".json" else candidate.name
    resolved = PAYLOADS_DIR / f"{stem}.json"
    if not resolved.exists():
        available = ", ".join(p.stem for p in sorted(PAYLOADS_DIR.glob("*.json")))
        raise SystemExit(
            f"Payload not found: {resolved}\n"
            f"Available: {available or '(none)'}"
        )
    return resolved


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Generate an Instagram slideshow with Pillow")
    parser.add_argument(
        "payload",
        nargs="?",
        help="Payload name (e.g. 'my-campaign') or path to a JSON file.",
    )
    parser.add_argument(
        "--output",
        default=str(DATA_DIR / "output"),
        help="Output directory (default: instagram-slideshow/output/)",
    )
    args = parser.parse_args()

    payload_path = _resolve_payload(args.payload)
    print(f"Using payload: {payload_path.name}\n")
    payload = json.loads(payload_path.read_text())
    slides = payload.get("slides", [])
    if not slides:
        raise SystemExit("No slides found in payload.")

    default_font = payload.get("font")
    max_font_size = payload.get("maxFontSize", DEFAULT_MAX_FONT_SIZE)
    total_slides = len(slides)
    output_dir = Path(args.output) / payload_path.stem
    output_dir.mkdir(parents=True, exist_ok=True)

    for i, slide in enumerate(slides, 1):
        text = slide.get("text", "")
        bg = slide.get("bgColor", "#F09040")
        fg = slide.get("textColor", "#ffffff")
        font_name = slide.get("font", default_font)

        print(f"[{i}/{total_slides}] '{text[:60]}'")
        img = render_slide(text, bg, fg, font_name, max_font_size, i, total_slides)
        dest = output_dir / f"{i:02d}.png"
        img.save(dest, "PNG")
        print(f"  saved → {dest}")

    print(f"\nDone. {total_slides} slide(s) exported to {output_dir}/")


if __name__ == "__main__":
    main()
