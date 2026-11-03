#!/usr/bin/env python3
"""Post-download: PDF→text, verify manifest, emit corpus stats (lossless raw preserved)."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_RAW = ROOT / "content/personal-ip/intake/_raw/xhs-ip-2026-11-03"
DEFAULT_MIRROR = DEFAULT_RAW / "drive-mirror/小红书"
DEFAULT_MANIFEST = DEFAULT_RAW / "drive-manifest-dry-run.json"
DEFAULT_PDF_TEXT = DEFAULT_RAW / "pdf-text"


def pdftotext(pdf: Path, out: Path) -> bool:
    out.parent.mkdir(parents=True, exist_ok=True)
    try:
        subprocess.run(
            ["pdftotext", "-enc", "UTF-8", str(pdf), str(out)],
            check=True,
            capture_output=True,
        )
        return out.is_file() and out.stat().st_size > 0
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def main() -> int:
    p = argparse.ArgumentParser(description="XHS Drive corpus ingest helpers")
    p.add_argument("--raw-dir", type=Path, default=DEFAULT_RAW)
    p.add_argument("--mirror", type=Path, default=DEFAULT_MIRROR)
    p.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    p.add_argument("--pdf-text-dir", type=Path, default=DEFAULT_PDF_TEXT)
    p.add_argument("--pdftotext", action="store_true", help="Extract all PDFs under mirror to pdf-text/")
    p.add_argument("--verify", action="store_true", help="Compare manifest file_count vs mirror files")
    args = p.parse_args()

    if args.verify:
        if not args.manifest.is_file():
            print(f"manifest missing: {args.manifest}", file=sys.stderr)
            return 1
        data = json.loads(args.manifest.read_text(encoding="utf-8"))
        expected = data.get("file_count", len(data.get("files", [])))
        on_disk = 0
        if args.mirror.is_dir():
            on_disk = sum(1 for f in args.mirror.rglob("*") if f.is_file())
        print(json.dumps({"expected_files": expected, "mirror_files": on_disk, "ok": on_disk >= expected}, indent=2))
        return 0 if on_disk >= expected else 2

    if args.pdftotext:
        if not args.mirror.is_dir():
            print(f"mirror missing: {args.mirror}", file=sys.stderr)
            return 1
        pdfs = sorted(args.mirror.rglob("*.pdf"))
        ok, fail = 0, 0
        for pdf in pdfs:
            rel = pdf.relative_to(args.mirror)
            out = args.pdf_text_dir / rel.with_suffix(".txt")
            if out.is_file() and out.stat().st_size > 0:
                ok += 1
                continue
            if pdftotext(pdf, out):
                ok += 1
            else:
                fail += 1
        print(json.dumps({"pdfs": len(pdfs), "ok": ok, "fail": fail}, indent=2))
        return 0 if fail == 0 else 3

    p.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
