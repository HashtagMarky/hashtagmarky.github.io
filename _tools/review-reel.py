#!/usr/bin/env python3
"""
review-reel.py — Turn a book cover into a 9:16 zoom-out video for Instagram Reels.

The cover sits over a blurred copy of itself. The video starts zoomed in on a
focus point you choose, then zooms out to the full cover and holds there.
Captions, voiceover, and music are left for the Instagram editor.

USAGE
-----
    python3 review-reel.py jade-city                    # reads image: from _books/jade-city.md
    python3 review-reel.py images/books/jade-city.jpg   # or any image path
    python3 review-reel.py jade-city --focus 0.5,0.3 --zoom 1.8
    python3 review-reel.py jade-city --focus 0.5,0.3 --preview   # check framing first

Output is written to reels/output/<name>.mp4 by default.

OPTIONS
-------
    --focus X,Y     Starting point of the zoom, as fractions of the cover
                    (0,0 = top-left, 1,1 = bottom-right). Default: 0.5,0.5
    --zoom Z        How far zoomed in the first frame is (1 = no zoom). Default: 1.5
    --duration S    Length of the video in seconds. Default: 15
    --zoom-start S  Second at which the zoom-out begins; the first frame holds
                    still until then. Default: 0
    --speed V       Average zoom-out speed, in zoom per second (0.05 = a 1.5 zoom
                    takes 10s). The cover holds still once it finishes. Default: 0.05
    --zoom-end S    Second at which the zoom-out finishes, instead of --speed.
                    If the zoom would run past --duration, it is sped up to
                    finish on the last frame.
    --size F        Width of the cover at rest, as a fraction of the screen.
                    Default: 1 (zooms out until the cover fills the screen width)
    --blur R        Background blur radius. Default: 40
    --preview       Save a PNG of the first and last frames instead of a video.
                    The focus point is marked with a crosshair and the area
                    the first frame shows is outlined.
    -o PATH         Output file

Requires: Pillow (`pip install Pillow`), ffmpeg (brew install ffmpeg)
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

SCRIPT_DIR = Path(__file__).parent
REPO_DIR = SCRIPT_DIR.parent
BOOKS_DIR = REPO_DIR / "_books"
OUTPUT_DIR = SCRIPT_DIR / "reels" / "output"

WIDTH, HEIGHT = 1080, 1920
FPS = 30
BG_BRIGHTNESS = 0.7

DEFAULT_ZOOM = 1.5
DEFAULT_DURATION = 15  # seconds
DEFAULT_SPEED = 0.05   # zoom per second


# ---------------------------------------------------------------------------
# Input
# ---------------------------------------------------------------------------

def resolve_image(arg: str) -> tuple[Path, str]:
    """Return (image path, output name) for an image path, review file, or slug."""
    path = Path(arg)
    if path.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp"):
        if not path.exists():
            sys.exit(f"Image not found: {path}")
        return path, path.stem

    review = path if path.suffix == ".md" else BOOKS_DIR / f"{arg}.md"
    if not review.exists():
        sys.exit(f"Review not found: {review}")
    match = re.search(r'^image:\s*"?([^"\n]+)"?\s*$', review.read_text(), re.MULTILINE)
    if not match:
        sys.exit(f"No image: in front matter of {review}")
    image = REPO_DIR / match.group(1).lstrip("/")
    if not image.exists():
        sys.exit(f"Image not found: {image}")
    return image, review.stem


def parse_focus(value: str) -> tuple[float, float]:
    try:
        x, y = (float(v) for v in value.split(","))
    except ValueError:
        raise argparse.ArgumentTypeError("focus must be X,Y, e.g. 0.5,0.3")
    if not (0 <= x <= 1 and 0 <= y <= 1):
        raise argparse.ArgumentTypeError("focus values must be between 0 and 1")
    return x, y


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def make_background(cover: Image.Image, blur: float) -> Image.Image:
    scale = max(WIDTH / cover.width, HEIGHT / cover.height)
    w, h = round(cover.width * scale), round(cover.height * scale)
    bg = cover.resize((w, h), Image.LANCZOS)
    left, top = (w - WIDTH) // 2, (h - HEIGHT) // 2
    bg = bg.crop((left, top, left + WIDTH, top + HEIGHT))
    bg = bg.filter(ImageFilter.GaussianBlur(blur))
    return ImageEnhance.Brightness(bg).enhance(BG_BRIGHTNESS).convert("RGBA")


def ease(p: float) -> float:
    """Smootherstep: gentle start and stop."""
    p = min(max(p, 0.0), 1.0)
    return p * p * p * (p * (p * 6 - 15) + 10)


class Reel:
    def __init__(self, cover, focus, zoom, size, blur):
        self.cover = cover.convert("RGBA")
        self.background = make_background(cover.convert("RGB"), blur)
        self.focus = focus
        self.zoom = zoom

        # Cover size and position at rest (end of the zoom)
        w = WIDTH * size
        h = w * cover.height / cover.width
        self.rest_w, self.rest_h = w, h
        self.rest_left, self.rest_top = (WIDTH - w) / 2, (HEIGHT - h) / 2

    def frame(self, p: float) -> Image.Image:
        """Render the frame at progress p (0 = zoomed in on focus, 1 = at rest)."""
        p = ease(p)
        scale = self.zoom + (1 - self.zoom) * p
        fx, fy = self.focus

        # The focus point moves from the centre of the screen to its rest position
        start_x, start_y = WIDTH / 2, HEIGHT / 2
        end_x = self.rest_left + fx * self.rest_w
        end_y = self.rest_top + fy * self.rest_h
        screen_x = start_x + (end_x - start_x) * p
        screen_y = start_y + (end_y - start_y) * p

        w, h = self.rest_w * scale, self.rest_h * scale
        left, top = screen_x - fx * w, screen_y - fy * h

        # Affine maps each output pixel back into the source, so motion is sub-pixel smooth
        a = self.cover.width / w
        layer = self.cover.transform(
            (WIDTH, HEIGHT), Image.AFFINE,
            (a, 0, -left * a, 0, a, -top * a),
            resample=Image.BICUBIC,
        )
        return Image.alpha_composite(self.background, layer).convert("RGB")


def render_video(reel: Reel, duration: float, zoom_start: float, zoom_end: float, output: Path):
    frames = round(duration * FPS)
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{WIDTH}x{HEIGHT}", "-r", str(FPS),
        "-i", "-",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart",
        str(output),
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(frames):
        p = (i / FPS - zoom_start) / (zoom_end - zoom_start)
        proc.stdin.write(reel.frame(p).tobytes())
        print(f"\r  Frame {i + 1}/{frames}", end="", flush=True)
    proc.stdin.close()
    print()
    if proc.wait() != 0:
        sys.exit("ffmpeg failed")


def start_window(reel: Reel) -> tuple[float, float, float, float]:
    """The area of the source image shown in the first frame, in image pixels."""
    k = reel.rest_w / reel.cover.width * reel.zoom  # screen pixels per image pixel at the start
    cx, cy = reel.focus[0] * reel.cover.width, reel.focus[1] * reel.cover.height
    half_w, half_h = WIDTH / 2 / k, HEIGHT / 2 / k
    return cx - half_w, cy - half_h, cx + half_w, cy + half_h


def render_preview(reel: Reel, output: Path):
    first, last = reel.frame(0), reel.frame(1)
    draw = ImageDraw.Draw(last)
    x = reel.rest_left + reel.focus[0] * reel.rest_w
    y = reel.rest_top + reel.focus[1] * reel.rest_h
    draw.line((x - 40, y, x + 40, y), fill="red", width=6)
    draw.line((x, y - 40, x, y + 40), fill="red", width=6)

    # Outline what the first frame shows
    k = reel.rest_w / reel.cover.width
    x1, y1, x2, y2 = start_window(reel)
    draw.rectangle((reel.rest_left + x1 * k, reel.rest_top + y1 * k,
                    reel.rest_left + x2 * k, reel.rest_top + y2 * k), outline="red", width=6)

    sheet = Image.new("RGB", (WIDTH * 2 + 40, HEIGHT), "white")
    sheet.paste(first, (0, 0))
    sheet.paste(last, (WIDTH + 40, 0))
    sheet.resize((sheet.width // 2, sheet.height // 2), Image.LANCZOS).save(output)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Turn a book cover into a 9:16 zoom-out video for Instagram Reels.")
    parser.add_argument("input", help="Review slug (e.g. jade-city), review .md file, or image path")
    parser.add_argument("--focus", type=parse_focus, default=(0.5, 0.5),
                        help="Zoom starting point as X,Y fractions of the cover (default 0.5,0.5)")
    parser.add_argument("--zoom", type=float, default=DEFAULT_ZOOM,
                        help=f"Starting zoom (default {DEFAULT_ZOOM})")
    parser.add_argument("--duration", type=float, default=DEFAULT_DURATION,
                        help=f"Video length in seconds (default {DEFAULT_DURATION})")
    parser.add_argument("--speed", type=float, default=DEFAULT_SPEED,
                        help=f"Zoom-out speed in zoom per second (default {DEFAULT_SPEED})")
    parser.add_argument("--zoom-start", type=float, default=0, help="Second the zoom-out begins (default 0)")
    parser.add_argument("--zoom-end", type=float, help="Second the zoom-out finishes (overrides --speed)")
    parser.add_argument("--size", type=float, default=1.0, help="Cover width at rest, fraction of screen (default 1)")
    parser.add_argument("--blur", type=float, default=40, help="Background blur radius (default 40)")
    parser.add_argument("--preview", action="store_true", help="Save first/last frame PNG instead of video")
    parser.add_argument("-o", "--output", type=Path, help="Output file")
    args = parser.parse_args()

    if args.zoom < 1:
        parser.error("--zoom must be 1 or more")
    if args.speed <= 0:
        parser.error("--speed must be greater than 0")
    if not 0 <= args.zoom_start < args.duration:
        parser.error("--zoom-start must be between 0 and --duration")
    if args.zoom_end is not None and args.zoom_end <= args.zoom_start:
        parser.error("--zoom-end must be after --zoom-start")

    zoom_start = args.zoom_start
    if args.zoom_end is not None:
        zoom_end = args.zoom_end
    elif args.zoom > 1:
        zoom_end = zoom_start + (args.zoom - 1) / args.speed
    else:
        zoom_end = args.duration  # nothing to zoom; any span works
    if zoom_end > args.duration:
        print(f"Note: zoom-out would finish at {zoom_end:.1f}s but the video is {args.duration:g}s, "
              f"so it is sped up to finish at {args.duration:g}s")
        zoom_end = args.duration

    image, name = resolve_image(args.input)
    output = args.output or OUTPUT_DIR / f"{name}{'-preview.png' if args.preview else '.mp4'}"
    output.parent.mkdir(parents=True, exist_ok=True)

    reel = Reel(Image.open(image), args.focus, args.zoom, args.size, args.blur)
    print(f"{image.name} → {output}")
    x1, y1, x2, y2 = start_window(reel)
    print(f"Image is {reel.cover.width}×{reel.cover.height}px. "
          f"First frame shows x {x1:.0f}–{x2:.0f}, y {y1:.0f}–{y2:.0f} "
          f"(values outside the image are blurred background)")
    print(f"Holds {zoom_start:g}s, zooms out {zoom_start:g}–{zoom_end:.1f}s, "
          f"then holds {args.duration - zoom_end:.1f}s")
    if args.preview:
        render_preview(reel, output)
    else:
        render_video(reel, args.duration, zoom_start, zoom_end, output)
    print("Done.")


if __name__ == "__main__":
    main()
