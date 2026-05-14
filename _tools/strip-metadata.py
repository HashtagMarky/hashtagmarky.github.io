#!/usr/bin/env python3
"""
strip-metadata.py — Strip all metadata from images and videos, in-place.

Usage:
  ./strip-metadata.py [paths...]   Process files/dirs (default: images/)
  ./strip-metadata.py --dry-run    Preview without making changes

Requires: Pillow (`pip install Pillow`), ffmpeg (brew install ffmpeg)
"""

import sys
import argparse
import os
import subprocess
import tempfile
import shutil
from pathlib import Path
from PIL import Image

SKIP_DIRS   = {"_site", ".jekyll-cache", "node_modules"}
IMAGE_EXTS  = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".tif"}
GIF_EXT     = ".gif"
VIDEO_EXTS  = {".mp4", ".mov", ".avi", ".mkv", ".webm", ".m4v", ".3gp"}

JPEG_QUALITY = 85


def is_in_skip_dir(path: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.parts)


def strip_image(path: Path, dry_run: bool) -> str:
    if is_in_skip_dir(path):
        return "skipped (protected dir)"
    if dry_run:
        return "strip metadata"

    img = Image.open(path)
    ext = path.suffix.lower()
    suffix = ".jpg" if ext not in {".jpg", ".jpeg", ".gif", ".png"} else ext

    tmp_fd, tmp_str = tempfile.mkstemp(suffix=suffix, dir=path.parent)
    os.close(tmp_fd)
    tmp = Path(tmp_str)

    try:
        if ext == ".gif":
            _strip_gif(img, tmp)
        elif ext == ".png":
            # Keep as PNG, drop all ancillary chunks
            rgb = img.convert("RGBA") if img.mode == "RGBA" else img
            rgb.save(tmp, "PNG", optimize=True)
        else:
            if img.mode != "RGB":
                img = img.convert("RGB")
            img.save(tmp, "JPEG", quality=JPEG_QUALITY, optimize=True, exif=b"")

        out = path.with_suffix(suffix)
        shutil.move(tmp_str, out)
        if out != path and path.exists():
            path.unlink()
    except Exception:
        if tmp.exists():
            tmp.unlink()
        raise
    finally:
        img.close()

    return "done"


def _strip_gif(img: Image.Image, dst: Path):
    frames, durations = [], []
    try:
        while True:
            frames.append(img.copy().convert("RGBA"))
            durations.append(img.info.get("duration", 100))
            img.seek(img.tell() + 1)
    except EOFError:
        pass

    frames[0].save(
        dst, format="GIF", save_all=True,
        append_images=frames[1:], duration=durations,
        loop=img.info.get("loop", 0), optimize=False,
    )


def strip_video(path: Path, dry_run: bool) -> str:
    if is_in_skip_dir(path):
        return "skipped (protected dir)"
    if dry_run:
        return "strip metadata"

    tmp_fd, tmp_str = tempfile.mkstemp(suffix=path.suffix, dir=path.parent)
    os.close(tmp_fd)

    try:
        subprocess.run(
            ["ffmpeg", "-i", str(path),
             "-map_metadata", "-1", "-map_chapters", "-1",
             "-c", "copy", "-movflags", "+faststart",
             tmp_str, "-y", "-loglevel", "error"],
            check=True,
        )
        shutil.move(tmp_str, path)
    except Exception:
        if Path(tmp_str).exists():
            Path(tmp_str).unlink()
        raise

    return "done"


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


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("paths", nargs="*", default=["images"])
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    targets = [Path(p) for p in args.paths]
    missing = [t for t in targets if not t.exists()]
    if missing:
        for m in missing:
            print(f"error: not found: {m}", file=sys.stderr)
        sys.exit(1)

    files = collect_files(targets)
    if not files:
        print("No files found.")
        return

    if args.dry_run:
        print("DRY RUN — no files will be changed\n")

    counts = {"done": 0, "skip": 0, "error": 0}

    for path in files:
        ext = path.suffix.lower()
        try:
            if ext in IMAGE_EXTS or ext == GIF_EXT:
                status = strip_image(path, args.dry_run)
            elif ext in VIDEO_EXTS:
                status = strip_video(path, args.dry_run)
            else:
                continue

            if "skipped" in status:
                counts["skip"] += 1
            else:
                counts["done"] += 1
                print(f"  {path}")
        except Exception as e:
            counts["error"] += 1
            print(f"  [ERROR] {path}: {e}", file=sys.stderr)

    print(f"\nDone. {counts['done']} processed, {counts['skip']} skipped, {counts['error']} error(s).")


if __name__ == "__main__":
    main()
