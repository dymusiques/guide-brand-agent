#!/usr/bin/env python3
"""Static lint for 02/03 markdown deliverables (no Gemini)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED = {
    "business_brand": ["定位", "SWOT", "与 IP 对齐"],
    "marketing": ["Campaign", "CTA", "渠道"],
}


def lint_file(kind: str, path: Path) -> list[str]:
    errors: list[str] = []
    if not path.is_file():
        return [f"file not found: {path}"]
    text = path.read_text(encoding="utf-8")
    if path.name == "README.md" and kind == "business_brand":
        # scaffold only
        pass
    for needle in REQUIRED[kind]:
        if needle not in text:
            errors.append(f"missing required block/keyword: {needle!r}")
    if kind == "marketing" and "强链接" not in text and "CTA" not in text.upper():
        errors.append("missing strong-link CTA section")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--kind", choices=("business_brand", "marketing"), required=True)
    parser.add_argument("--file", type=Path, required=True)
    args = parser.parse_args()
    path = args.file if args.file.is_absolute() else ROOT / args.file
    errs = lint_file(args.kind, path)
    if errs:
        for e in errs:
            print(f"FAIL: {e}", file=sys.stderr)
        return 1
    print(json.dumps({"lint": "pass", "kind": args.kind, "file": str(path)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
