#!/usr/bin/env python3
"""
slideshow.py — Generate slideshow images locally using Pillow.

No API keys or accounts needed. Colours, text, and layout are fully controlled
via the payload.

USAGE
-----
    python3 slideshow.py                   # lists available payloads
    python3 slideshow.py my-campaign       # slideshow/payloads/my-campaign.json
    python3 slideshow.py my-campaign.json  # same

Output is written to slideshow/output/<payload-name>/ by default.

FONTS
-----
Drop any .ttf or .otf file into slideshow/fonts/ and reference it by
filename in the payload:

    "font": "MyFont-Bold.ttf"

If omitted, the script falls back to PressStart2P-Regular.ttf.

INPUT FORMAT
------------
{
    "dimensions": "square",
    "font": "MyFont-Bold.ttf",
    "maxFontSize": 60,
    "bgColor": "navy",
    "textColor": "white",
    "prefix": 1,
    "slides": [
        {
            "type": "review-cover",
            "title": "Book Title",
            "author": "Author Name",
            "rating": 4
        },
        {
            "text": "A regular slide with body text."
        },
        {
            "type": "link",
            "message": "Follow along for more!",
            "link": "hashtagmarky.com/devlog",
            "linkColor": "orange"
        }
    ]
}

Cover slides use "type": "review-cover" with title, author, and rating (1-10, halved internally to 0.5-5 stars).
Regular slides use "text". Link slides use "type": "link" with message and link.
All slide types support textColor, bgColor, and font as per-slide overrides.
maxFontSize caps body text size (default: 60).
"""

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR / "slideshow"
PAYLOADS_DIR = DATA_DIR / "payloads"
FONTS_DIR = DATA_DIR / "fonts"

DIMENSIONS = {
    "square":       (1080, 1080),
    "instagram":    (1080, 1350),
    "full-screen":  (1080, 1920),
}

PADDING = 100
LINE_SPACING = 1.4
DEFAULT_MAX_FONT_SIZE = 60

DOT_RADIUS = 6
DOT_SPACING = 20
STAR_FONT_SIZE = 80
AUTHOR_FONT_SIZE = 36
COVER_TITLE_MAX_FONT_SIZE = 100
COVER_BLOCK_GAP = 40
FONT_SIZE_MIN = 20
LINK_GAP = 40
LINK_MAX_FONT_SIZE = 60


# ---------------------------------------------------------------------------
# Config colours
# ---------------------------------------------------------------------------

def _load_config_colors() -> dict[str, str]:
    colors = {}
    config_file = SCRIPT_DIR.parent / "_config.yml"
    if not config_file.exists():
        return colors
    in_colors = False
    for line in config_file.read_text().splitlines():
        if line.strip() == "colors:":
            in_colors = True
            continue
        if in_colors:
            if line and not line[0].isspace():
                break
            if ":" in line:
                key, _, val = line.partition(":")
                colors[key.strip().lower()] = val.strip().strip('"')
    return colors


COLOR_MAP = _load_config_colors()


def _resolve_color(value: str) -> str:
    resolved = COLOR_MAP.get(value.lower())
    if resolved is None and not value.startswith("#"):
        raise SystemExit(f"Unknown colour '{value}'. Available names: {', '.join(COLOR_MAP)}")
    return resolved or value


# ---------------------------------------------------------------------------
# Font loading
# ---------------------------------------------------------------------------

DEFAULT_FONT = "PressStart2P-Regular.ttf"


def _load_font(name: str | None, size: int) -> ImageFont.FreeTypeFont:
    for candidate in [name, DEFAULT_FONT]:
        if candidate:
            path = FONTS_DIR / candidate
            if path.exists():
                return ImageFont.truetype(str(path), size)
    raise SystemExit(f"Font '{name}' not found and default {DEFAULT_FONT} is missing from {FONTS_DIR}/")


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
    lo, hi = FONT_SIZE_MIN, max_size
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


def _fit_single_line(text: str, font_name: str | None, max_width: int, max_size: int, draw: ImageDraw.ImageDraw) -> ImageFont.FreeTypeFont:
    lo, hi = FONT_SIZE_MIN, max_size
    best = _load_font(font_name, lo)
    while lo <= hi:
        mid = (lo + hi) // 2
        font = _load_font(font_name, mid)
        if draw.textlength(text, font=font) <= max_width:
            best = font
            lo = mid + 1
        else:
            hi = mid - 1
    return best


# ---------------------------------------------------------------------------
# Slide indicator
# ---------------------------------------------------------------------------

def _draw_indicator(draw: ImageDraw.ImageDraw, slide_num: int, total: int, text_color: str, width: int, height: int) -> None:
    total_width = (total - 1) * DOT_SPACING
    start_x = (width - PADDING) - total_width
    y = height - PADDING

    for i in range(total):
        x = start_x + i * DOT_SPACING
        bbox = [x - DOT_RADIUS, y - DOT_RADIUS, x + DOT_RADIUS, y + DOT_RADIUS]
        if i == slide_num - 1:
            draw.ellipse(bbox, fill=text_color)
        else:
            draw.ellipse(bbox, outline=text_color, width=2)


# ---------------------------------------------------------------------------
# Stars
# ---------------------------------------------------------------------------

def _stars_string(rating: float) -> str:
    full = int(rating)
    half = 1 if (rating - full) >= 0.5 else 0
    empty = 5 - full - half
    return "★" * full + ("½" if half else "") + "☆" * empty


def _draw_stars(draw: ImageDraw.ImageDraw, rating: float, color: str, font_name: str | None, y: float, width: int) -> None:
    text = _stars_string(rating)
    font = _load_font(font_name, STAR_FONT_SIZE)
    w = draw.textlength(text, font=font)
    draw.text(((width - w) / 2, y), text, font=font, fill=color)


# ---------------------------------------------------------------------------
# Slide rendering
# ---------------------------------------------------------------------------

def render_review_cover(title: str, author: str, rating: float, bg_color: str, text_color: str, font_name: str | None, slide_num: int, total_slides: int, width: int, height: int) -> Image.Image:
    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    max_width = width - PADDING * 2
    author_font = _load_font(font_name, AUTHOR_FONT_SIZE)
    author_height = author_font.size * LINE_SPACING

    stars_font = _load_font(font_name, STAR_FONT_SIZE)
    stars_height = stars_font.size * LINE_SPACING
    title_max_height = height - PADDING * 2 - stars_height - author_height - COVER_BLOCK_GAP * 2

    title_font, title_lines = _fit_font(title, font_name, max_width, title_max_height, COVER_TITLE_MAX_FONT_SIZE, draw)
    title_line_h = title_font.size * LINE_SPACING
    title_block_h = title_line_h * len(title_lines)

    total_block_h = title_block_h + COVER_BLOCK_GAP + author_height + COVER_BLOCK_GAP + stars_height
    y = (height - total_block_h) / 2

    for line in title_lines:
        x = (width - draw.textlength(line, font=title_font)) / 2
        draw.text((x, y), line, font=title_font, fill=text_color)
        y += title_line_h

    y += COVER_BLOCK_GAP
    author_w = draw.textlength(author, font=author_font)
    draw.text(((width - author_w) / 2, y), author, font=author_font, fill=text_color)
    y += author_height + COVER_BLOCK_GAP

    _draw_stars(draw, rating, text_color, font_name, y, width)
    _draw_indicator(draw, slide_num, total_slides, text_color, width, height)

    return img


def render_slide(text: str, bg_color: str, text_color: str, font_name: str | None, max_font_size: int, slide_num: int, total_slides: int, width: int, height: int) -> Image.Image:
    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    max_text_width = width - PADDING * 2
    max_text_height = height - PADDING * 2

    font, lines = _fit_font(text, font_name, max_text_width, max_text_height, max_font_size, draw)
    line_height = font.size * LINE_SPACING
    total_text_height = line_height * len(lines)

    y = (height - total_text_height) / 2

    for line in lines:
        x = (width - draw.textlength(line, font=font)) / 2
        draw.text((x, y), line, font=font, fill=text_color)
        y += line_height

    _draw_indicator(draw, slide_num, total_slides, text_color, width, height)

    return img


def render_link(message: str, link: str, bg_color: str, text_color: str, link_color: str, font_name: str | None, max_font_size: int, slide_num: int, total_slides: int, width: int, height: int) -> Image.Image:
    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    max_width = width - PADDING * 2

    link_font = _fit_single_line(link, font_name, max_width, LINK_MAX_FONT_SIZE, draw)
    link_height = link_font.size * LINE_SPACING

    max_message_height = height - PADDING * 2 - link_height - LINK_GAP
    message_font, message_lines = _fit_font(message, font_name, max_width, max_message_height, max_font_size, draw)
    message_line_h = message_font.size * LINE_SPACING
    message_block_h = message_line_h * len(message_lines)

    total_block_h = message_block_h + LINK_GAP + link_height
    y = (height - total_block_h) / 2

    for line in message_lines:
        x = (width - draw.textlength(line, font=message_font)) / 2
        draw.text((x, y), line, font=message_font, fill=text_color)
        y += message_line_h

    y += LINK_GAP
    link_w = draw.textlength(link, font=link_font)
    draw.text(((width - link_w) / 2, y), link, font=link_font, fill=link_color)

    _draw_indicator(draw, slide_num, total_slides, text_color, width, height)

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
        raise SystemExit(f"Available payloads:\n  {names}\n\nUsage: python slideshow.py <name>")

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
# Slide dispatch
# ---------------------------------------------------------------------------

def _process_review_cover(slide: dict, bg: str, fg: str, font_name: str | None, dot_num: int, dot_total: int, width: int, height: int) -> Image.Image:
    title = slide.get("title", "")
    author = slide.get("author", "")
    rating = int(slide.get("rating", 0)) / 2
    print(f"[{dot_num}/{dot_total}] review-cover — '{title}' by {author} ({rating}★)")
    return render_review_cover(title, author, rating, bg, fg, font_name, dot_num, dot_total, width, height)


def _process_link(slide: dict, bg: str, fg: str, font_name: str | None, max_font_size: int, dot_num: int, dot_total: int, width: int, height: int) -> Image.Image:
    message = slide.get("message", "")
    link = slide.get("link", "")
    link_color = _resolve_color(slide["linkColor"]) if "linkColor" in slide else fg
    print(f"[{dot_num}/{dot_total}] link — '{message[:40]}' → {link[:40]}")
    return render_link(message, link, bg, fg, link_color, font_name, max_font_size, dot_num, dot_total, width, height)


def _process_text(slide: dict, bg: str, fg: str, font_name: str | None, max_font_size: int, dot_num: int, dot_total: int, width: int, height: int) -> Image.Image:
    text = slide.get("text", "")
    print(f"[{dot_num}/{dot_total}] '{text[:60]}'")
    return render_slide(text, bg, fg, font_name, max_font_size, dot_num, dot_total, width, height)


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
        help="Output directory (default: slideshow/output/)",
    )
    args = parser.parse_args()

    payload_path = _resolve_payload(args.payload)
    print(f"Using payload: {payload_path.name}\n")
    payload = json.loads(payload_path.read_text())

    dim_name = payload.get("dimensions", "square")
    if dim_name not in DIMENSIONS:
        raise SystemExit(f"Unknown dimensions '{dim_name}'. Available: {', '.join(DIMENSIONS)}")
    width, height = DIMENSIONS[dim_name]

    slides = payload.get("slides", [])
    if not slides:
        raise SystemExit("No slides found in payload.")
    dot_offset = payload.get("prefix", 0)

    default_font = payload.get("font")
    max_font_size = payload.get("maxFontSize", DEFAULT_MAX_FONT_SIZE)
    default_bg = payload.get("bgColor", "black")
    default_fg = payload.get("textColor", "white")
    total_slides = len(slides)
    output_dir = Path(args.output) / payload_path.stem
    output_dir.mkdir(parents=True, exist_ok=True)

    for i, slide in enumerate(slides, 1):
        bg = _resolve_color(slide.get("bgColor", default_bg))
        fg = _resolve_color(slide.get("textColor", default_fg))
        font_name = slide.get("font", default_font)

        dot_num = i + dot_offset
        dot_total = total_slides + dot_offset
        if slide.get("type") == "review-cover":
            img = _process_review_cover(slide, bg, fg, font_name, dot_num, dot_total, width, height)
        elif slide.get("type") == "link":
            img = _process_link(slide, bg, fg, font_name, max_font_size, dot_num, dot_total, width, height)
        else:
            img = _process_text(slide, bg, fg, font_name, max_font_size, dot_num, dot_total, width, height)

        dest = output_dir / f"{i:02d}.png"
        img.save(dest, "PNG")
        print(f"  saved → {dest}")

    print(f"\nDone. {total_slides} slide(s) exported to {output_dir}/")


if __name__ == "__main__":
    main()
