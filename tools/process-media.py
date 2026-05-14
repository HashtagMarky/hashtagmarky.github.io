#!/usr/bin/env python3
"""
process-media.py — Convert images to JPEG, resize for web, strip all metadata.

Usage:
  ./process-media.py [paths...]   Process files/dirs (default: images/)
  ./process-media.py --dry-run    Preview without making changes
  ./process-media.py --help       Show this help

By default, files are processed in-place. If a PNG is converted to JPEG, the
original PNG is removed. GIFs (animated pixel art) are stripped of metadata
but kept as GIFs. Favicons, social OG cards/icons, and GBA screenshots
(240×160, 480×320) are never resized.

Requires: Pillow (`pip install Pillow`), ffmpeg (brew install ffmpeg)
"""

import sys
import os
import argparse
import subprocess
import tempfile
import shutil
from pathlib import Path
from PIL import Image

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

JPEG_QUALITY = 85

# Directories whose contents must never be touched (exact directory name match)
SKIP_DIRS = {"favicon", "_site", ".jekyll-cache", "node_modules"}

# Subdirectory paths (relative segments) to keep at original size
KEEP_SIZE_PATHS = {
    ("social-pages", "cards"),   # 1200×630 OG cards
    ("social-pages", "icons"),   # Discord logos etc.
}

# GBA native / 2× / 3× / 4× screenshot resolutions — never upscale or downscale
GBA_SIZES = {(240, 160), (480, 320), (720, 480), (960, 640)}

# Max (width, height) per top-level images subfolder. Aspect ratio is preserved.
# None means no limit on that axis.
SIZE_RULES = {
    "books":    (600, 900),     # portrait book covers
    "projects": (1200, 800),    # box art, screenshots, wallpapers
    "devlog":   (1200, 900),    # IRL photos; GBA shots handled by GBA_SIZES
    "infernape":(800, 800),     # character art
}

DEFAULT_MAX = (1200, 900)  # fallback for anything not matched above

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".tif"}
GIF_EXT    = ".gif"
VIDEO_EXTS = {".mp4", ".mov", ".avi", ".mkv", ".webm", ".m4v", ".3gp"}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def is_in_skip_dir(path: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.parts)

def is_keep_size_path(path: Path) -> bool:
    parts = path.parts
    for keep in KEEP_SIZE_PATHS:
        if all(k in parts for k in keep):
            # Verify the order matches
            indices = [parts.index(k) for k in keep if k in parts]
            if indices == sorted(indices):
                return True
    return False

def get_max_dims(path: Path) -> tuple[int | None, int | None] | None:
    """Return (max_w, max_h) for the given path, or None to skip entirely."""
    if is_in_skip_dir(path):
        return None
    if is_keep_size_path(path):
        return (None, None)  # no resize, but still strip metadata
    parts = path.parts
    for folder, rule in SIZE_RULES.items():
        if folder in parts:
            return rule
    return DEFAULT_MAX

def fit_dimensions(w: int, h: int, max_w: int | None, max_h: int | None) -> tuple[int, int]:
    if max_w is None and max_h is None:
        return (w, h)
    scale = 1.0
    if max_w and w > max_w:
        scale = min(scale, max_w / w)
    if max_h and h > max_h:
        scale = min(scale, max_h / h)
    return (max(1, round(w * scale)), max(1, round(h * scale)))

def to_rgb(img: Image.Image) -> Image.Image:
    if img.mode == "RGB":
        return img
    if img.mode in ("RGBA", "LA", "PA"):
        bg = Image.new("RGB", img.size, (255, 255, 255))
        alpha = img.convert("RGBA").split()[3]
        bg.paste(img.convert("RGB"), mask=alpha)
        return bg
    return img.convert("RGB")

# ---------------------------------------------------------------------------
# Image processing
# ---------------------------------------------------------------------------

def process_image(path: Path, dry_run: bool) -> str:
    """Process a single raster image. Returns a short status string."""
    dims = get_max_dims(path)
    if dims is None:
        return "skipped (protected dir)"

    img = Image.open(path)
    orig_w, orig_h = img.size
    is_animated = getattr(img, "is_animated", False)

    # GBA screenshots: strip metadata but never resize
    if (orig_w, orig_h) in GBA_SIZES:
        dims = (None, None)

    max_w, max_h = dims
    new_w, new_h = fit_dimensions(orig_w, orig_h, max_w, max_h)
    resized = (new_w, new_h) != (orig_w, orig_h)

    out_ext = path.suffix.lower()
    convert_to_jpeg = (out_ext not in {".jpg", ".jpeg", ".gif"}) and not is_animated

    if dry_run:
        action = []
        if convert_to_jpeg:
            action.append(f"→ .jpg")
        if resized:
            action.append(f"{orig_w}×{orig_h} → {new_w}×{new_h}")
        action.append("strip metadata")
        return ", ".join(action) if action else "metadata strip only"

    # Work on a temp file to be atomic
    suffix = ".jpg" if convert_to_jpeg else path.suffix
    tmp_fd, tmp_path_str = tempfile.mkstemp(suffix=suffix, dir=path.parent)
    os.close(tmp_fd)
    tmp_path = Path(tmp_path_str)

    try:
        if out_ext == ".gif":
            # Strip metadata from GIF without re-encoding frames
            _strip_gif_metadata(img, path, tmp_path)
        else:
            rgb = to_rgb(img)
            if resized:
                rgb = rgb.resize((new_w, new_h), Image.LANCZOS)
            rgb.save(tmp_path, "JPEG", quality=JPEG_QUALITY, optimize=True, exif=b"")

        out_path = path.with_suffix(suffix)
        shutil.move(tmp_path_str, out_path)

        # Remove the original if we changed its extension
        if out_path != path and path.exists():
            path.unlink()

    except Exception:
        if tmp_path.exists():
            tmp_path.unlink()
        raise

    img.close()
    status = []
    if convert_to_jpeg:
        status.append(f"converted to jpg")
    if resized:
        status.append(f"resized {orig_w}×{orig_h} → {new_w}×{new_h}")
    status.append("metadata stripped")
    return ", ".join(status)

def _strip_gif_metadata(img: Image.Image, src: Path, dst: Path):
    """Copy GIF frames without metadata (comment blocks, XMP, etc.)."""
    frames, durations = [], []
    try:
        while True:
            frames.append(img.copy().convert("RGBA"))
            durations.append(img.info.get("duration", 100))
            img.seek(img.tell() + 1)
    except EOFError:
        pass

    if not frames:
        shutil.copy2(src, dst)
        return

    frames[0].save(
        dst,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=img.info.get("loop", 0),
        optimize=False,
    )

# ---------------------------------------------------------------------------
# Video processing
# ---------------------------------------------------------------------------

def process_video(path: Path, dry_run: bool) -> str:
    if is_in_skip_dir(path):
        return "skipped (protected dir)"
    if dry_run:
        return "strip metadata (ffmpeg -map_metadata -1)"

    suffix = path.suffix
    tmp_fd, tmp_path_str = tempfile.mkstemp(suffix=suffix, dir=path.parent)
    os.close(tmp_fd)

    try:
        cmd = [
            "ffmpeg", "-i", str(path),
            "-map_metadata", "-1",   # strip all global metadata
            "-map_chapters", "-1",   # strip chapter markers
            "-c", "copy",            # no re-encode
            "-movflags", "+faststart",
            tmp_path_str, "-y", "-loglevel", "error",
        ]
        subprocess.run(cmd, check=True)
        shutil.move(tmp_path_str, path)
    except Exception:
        if Path(tmp_path_str).exists():
            Path(tmp_path_str).unlink()
        raise

    return "metadata stripped"

# ---------------------------------------------------------------------------
# Walk & dispatch
# ---------------------------------------------------------------------------

def collect_files(targets: list[Path]) -> list[Path]:
    files = []
    for t in targets:
        if t.is_file():
            files.append(t)
        elif t.is_dir():
            for p in sorted(t.rglob("*")):
                if p.is_file():
                    files.append(p)
    return files

def process_file(path: Path, dry_run: bool) -> tuple[str, str]:
    """Returns (category, status)."""
    ext = path.suffix.lower()
    if ext in IMAGE_EXTS or ext == GIF_EXT:
        return ("image", process_image(path, dry_run))
    if ext in VIDEO_EXTS:
        return ("video", process_video(path, dry_run))
    return ("skip", "not a recognised media file")

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "paths", nargs="*", default=["images"],
        help="Files or directories to process (default: images/)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Preview what would happen without making any changes",
    )
    args = parser.parse_args()

    targets = [Path(p) for p in args.paths]
    missing = [t for t in targets if not t.exists()]
    if missing:
        for m in missing:
            print(f"error: path not found: {m}", file=sys.stderr)
        sys.exit(1)

    files = collect_files(targets)
    if not files:
        print("No files found.")
        return

    if args.dry_run:
        print("DRY RUN — no files will be changed\n")

    counts = {"image": 0, "video": 0, "skip": 0, "error": 0}

    for path in files:
        try:
            category, status = process_file(path, args.dry_run)
            counts[category] += 1
            if category != "skip":
                print(f"  [{category}] {path}  →  {status}")
        except Exception as e:
            counts["error"] += 1
            print(f"  [ERROR] {path}: {e}", file=sys.stderr)

    print(
        f"\nDone. "
        f"{counts['image']} image(s), "
        f"{counts['video']} video(s), "
        f"{counts['skip']} skipped, "
        f"{counts['error']} error(s)."
    )

if __name__ == "__main__":
    main()
