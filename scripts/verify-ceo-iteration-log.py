#!/usr/bin/env python3
"""Validate ITERATION-LOG before CEO double-iteration phase 2. See CEO-DOUBLE-ITERATION-SOP.md."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def default_log_for_brief(brief: Path) -> Path:
    slug = brief.name.replace("-brief.md", "")
    return ROOT / "content/evolution/04-xhs-topic-manager" / slug / "ITERATION-LOG.md"


def validate_phase2(text: str) -> list[str]:
    errs: list[str] = []
    if "迭代 1" not in text:
        errs.append("missing section「迭代 1」")
    if not re.search(r"分析|Analyze", text, re.I):
        errs.append("missing iteration-1 analysis（分析 / Analyze）")
    if not re.search(r"迭代\s*2\s*将只改|已读迭代\s*1\s*分析", text):
        errs.append("missing bridge to iter 2（「迭代 2 将只改」或「已读迭代 1 分析」）")
    if not re.search(r"###\s*提案|提案（迭代", text):
        errs.append("missing Prompt Change 提案（### 提案 或 提案（迭代）")
    if "## 迭代 2" not in text and "迭代 2" not in text:
        errs.append("missing「迭代 2」section or heading")
    return errs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--log", type=Path, help="ITERATION-LOG.md path")
    ap.add_argument("--brief", type=Path, help="derive default log path from brief")
    ap.add_argument("--phase", choices=("2",), default="2")
    args = ap.parse_args()

    log = args.log
    if log is None:
        if not args.brief:
            print("FAIL: --log or --brief required", file=sys.stderr)
            return 2
        brief = args.brief if args.brief.is_absolute() else ROOT / args.brief
        log = default_log_for_brief(brief)
    else:
        log = log if log.is_absolute() else ROOT / log

    if not log.is_file():
        print(f"FAIL: ITERATION-LOG not found: {log.relative_to(ROOT)}")
        return 1

    text = log.read_text(encoding="utf-8")
    errs = validate_phase2(text)
    if errs:
        for e in errs:
            print(f"FAIL: {e}")
        print(f"FAIL: fix {log.relative_to(ROOT)} then re-run --phase 2")
        return 1

    print(f"PASS: ITERATION-LOG ready for phase 2 · {log.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
