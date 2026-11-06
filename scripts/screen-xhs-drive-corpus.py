#!/usr/bin/env python3
"""CEO Drive screen entry — delegates to full corpus screener (backward-compatible CLI)."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    p = argparse.ArgumentParser(description="Screen CEO Drive catalog for one goal (full reference bundle)")
    p.add_argument("--goal", "-g", required=True)
    p.add_argument("--brief", default="")
    p.add_argument("--catalog", type=Path, default=None)
    p.add_argument("--limit", type=int, default=12, help="Legacy: maps to --hydrate-limit (default 8 if <=8 else limit)")
    p.add_argument(
        "--refresh-catalog",
        action="store_true",
        help="Run refresh-ceo-drive-catalog.py before screen",
    )
    args = p.parse_args()
    hydrate = args.limit if args.limit > 8 else 8
    cmd = [
        sys.executable,
        str(ROOT / "scripts/ceo-task-drive-corpus-screen.py"),
        "--goal",
        args.goal.strip(),
        "--hydrate-limit",
        str(hydrate),
    ]
    if args.brief.strip():
        cmd.extend(["--brief", args.brief.strip()])
    if args.catalog:
        cmd.extend(["--catalog", str(args.catalog)])
    if args.refresh_catalog:
        cmd.append("--refresh-catalog")
    return subprocess.call(cmd, cwd=ROOT)


if __name__ == "__main__":
    raise SystemExit(main())
