#!/usr/bin/env python3
"""Evaluate a business-brand markdown doc (Gemini · Agent 02)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINE2 = ROOT / "kernels/strategic_docs/line2"
sys.path.insert(0, str(LINE2))

from is_strategic_doc_aligned import evaluate_strategic_doc  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=Path, required=True)
    parser.add_argument("--subject", type=str, default="")
    args = parser.parse_args()
    path = args.file if args.file.is_absolute() else ROOT / args.file
    body = path.read_text(encoding="utf-8")
    subject = args.subject.strip() or path.stem
    result = evaluate_strategic_doc(
        {"kind": "business_brand", "subject": subject, "body": body}
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("aligned") else 1


if __name__ == "__main__":
    sys.exit(main())
