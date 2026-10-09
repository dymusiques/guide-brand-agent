#!/usr/bin/env python3
"""Validate and import platform analytics CSV into content/analytics/."""

from __future__ import annotations

import argparse
import csv
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from analytics.schemas import CANONICAL_FILES, OPTIONAL_COLUMNS, PLATFORMS, REQUIRED  # noqa: E402


def _read_header(path: Path) -> list[str]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        row = next(csv.reader(f), None)
    if not row:
        raise ValueError(f"empty CSV: {path}")
    return [c.strip() for c in row]


def validate_csv(platform: str, path: Path) -> list[str]:
    if platform not in PLATFORMS:
        raise ValueError(f"unknown platform {platform!r}")
    header = _read_header(path)
    missing = [c for c in REQUIRED[platform] if c not in header]
    if missing:
        raise ValueError(f"{path}: missing columns {missing}")
    return header


def import_csv(platform: str, source: Path, *, replace: bool = True) -> Path:
    validate_csv(platform, source)
    dest_dir = ROOT / "content" / "analytics" / platform
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / CANONICAL_FILES[platform]
    if dest.exists() and not replace:
        raise FileExistsError(f"refusing to overwrite {dest} (use --replace)")
    shutil.copy2(source, dest)
    return dest


def main() -> int:
    parser = argparse.ArgumentParser(description="Import analytics CSV")
    parser.add_argument(
        "--platform",
        choices=PLATFORMS,
        required=True,
        help="xiaohongshu | instagram | youtube",
    )
    parser.add_argument("--file", type=Path, required=True, help="Source CSV path")
    parser.add_argument(
        "--replace",
        action="store_true",
        default=True,
        help="Overwrite canonical file (default true)",
    )
    args = parser.parse_args()
    if not args.file.is_file():
        print(f"error: not found {args.file}", file=sys.stderr)
        return 2
    try:
        dest = import_csv(args.platform, args.file, replace=args.replace)
    except (ValueError, FileExistsError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"imported → {dest.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
