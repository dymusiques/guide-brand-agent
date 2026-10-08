#!/usr/bin/env python3
"""Evaluate one Xiaohongshu note dict against IP/growth/strong-link rules (Gemini).

Used by Topic Manager Skill after drafting a brief.

Examples:
  python scripts/evaluate-xhs-topic.py --subject "标题" --body "正文含 CTA"
  python scripts/evaluate-xhs-topic.py --json-file note.topic.json
  python scripts/evaluate-xhs-topic.py --brief content/xiaohongshu/2026-10-08-slug-brief.md
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
XHS_KERNEL = ROOT / "kernels" / "xiaohongshu"
sys.path.insert(0, str(XHS_KERNEL))

from line2.is_xhs_growth_aligned import (  # noqa: E402
    evaluate_xhs_growth_content,
    normalize_xhs_content,
)

CLASSIFIER_MARKER = "<!-- xhs-classifier -->"


def _load_json_path(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("JSON root must be an object")
    return normalize_xhs_content(data)


def _extract_classifier_json_from_brief(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if CLASSIFIER_MARKER not in text:
        raise ValueError(
            f"Missing {CLASSIFIER_MARKER} in {path}. "
            "Use kernels/templates/xhs-content-brief.template.md"
        )
    after = text.split(CLASSIFIER_MARKER, 1)[1]
    match = re.search(r"```(?:json)?\s*\n([\s\S]*?)\n```", after)
    if not match:
        raise ValueError(f"No ```json block after classifier marker in {path}")
    data = json.loads(match.group(1).strip())
    return normalize_xhs_content(data)


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate XHS topic alignment")
    parser.add_argument("--subject", type=str, help="Note title")
    parser.add_argument("--body", type=str, help="Hook + body + CTA as one string")
    parser.add_argument("--json-file", type=Path, help="JSON file with subject and body")
    parser.add_argument("--brief", type=Path, help="Markdown brief with xhs-classifier block")
    args = parser.parse_args()

    try:
        if args.brief:
            note = _extract_classifier_json_from_brief(args.brief)
        elif args.json_file:
            note = _load_json_path(args.json_file)
        elif args.subject is not None or args.body is not None:
            note = normalize_xhs_content(
                {"subject": args.subject or "", "body": args.body or ""}
            )
        else:
            raw = sys.stdin.read().strip()
            if not raw:
                parser.error("Provide --brief, --json-file, --subject/--body, or JSON on stdin")
            note = normalize_xhs_content(json.loads(raw))
    except (json.JSONDecodeError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2

    try:
        result = evaluate_xhs_growth_content(note)
    except Exception as exc:
        print(json.dumps({"error": str(exc), **note}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("aligned") else 1


if __name__ == "__main__":
    sys.exit(main())
