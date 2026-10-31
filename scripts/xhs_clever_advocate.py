#!/usr/bin/env python3
"""Clever multi-persona 'against' blocks in Owner longform — see docs/OWNER-LONGFORM-CLEVER-ADVOCATE.md."""

from __future__ import annotations

import re
from pathlib import Path

from xhs_brief_longform import extract_longform_text

ROOT = Path(__file__).resolve().parent.parent

# Persona label: **反方·xxx** or **@xxx**
PERSONA_BOLD = re.compile(r"\*\*(?:反方·|@)[^*]{2,40}\*\*")
CLEVER_SECTION_RE = re.compile(
    r"(杠精席|Clever|反方席|多立场反驳|网红.*杠)",
    re.I,
)
REBUTTAL_RE = re.compile(
    r"(收进包里|我回杠|杠完仍|反驳之后|仍不反悔|我认.*但)",
)


def analyze_clever_advocate(longform: str) -> dict:
    text = longform or ""
    unique: list[str] = []
    seen: set[str] = set()
    for p in PERSONA_BOLD.findall(text):
        if p not in seen:
            seen.add(p)
            unique.append(p)
    has_section = bool(CLEVER_SECTION_RE.search(text))
    has_rebuttal = bool(REBUTTAL_RE.search(text))
    min_personas = int(__import__("os").environ.get("CEO_CLEVER_MIN_PERSONAS", "4"))
    n = len(unique)
    ok = has_section and n >= min_personas and has_rebuttal
    return {
        "pass": ok,
        "persona_count": n,
        "min_personas": min_personas,
        "has_clever_section": has_section,
        "has_author_rebuttal": has_rebuttal,
        "personas": unique[:12],
    }


def analyze_brief(brief: Path) -> dict:
    lf = extract_longform_text(brief if brief.is_absolute() else ROOT / brief)
    out = analyze_clever_advocate(lf)
    out["longform_chars"] = len(lf)
    return out


def main() -> int:
    import argparse
    import json
    import sys

    ap = argparse.ArgumentParser()
    ap.add_argument("--brief", type=Path, required=True)
    args = ap.parse_args()
    brief = args.brief if args.brief.is_absolute() else ROOT / args.brief
    if not brief.is_file():
        print(f"FAIL: missing {brief}", file=sys.stderr)
        return 2
    r = analyze_brief(brief)
    print(json.dumps(r, ensure_ascii=False, indent=2))
    if r["pass"]:
        print("RESULT: PASS xhs-clever-advocate")
        return 0
    print("RESULT: FAIL xhs-clever-advocate", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
