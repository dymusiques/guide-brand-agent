#!/usr/bin/env python3
"""L2 voice QA: banned consultant-AI phrases in XHS draft markdown."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# Integration prompt is canonical; keep in sync with agents/04-xhs-topic-manager/INTEGRATION-PROMPT.md
BANNED = [
    "装饰型艺术",
    "站得住的专业",
    "站得住的艺术",
    "叙事而非硬广",
    "跨行业 open",
    "专业信任",
    "可被感受的 moment",
    "moment + 判断",
    "三秒划走",
    "用户停不停",
    "不可替代的，不是装饰",
    "品牌主理人",
    "赋能",
    "高端人群",
]

ROUND1_NEED = [
    re.compile(r"^##\s*方向\s*[1-5]", re.M),
    re.compile(r"\|\s*[1-5][A-C]\s*\|", re.M),
    re.compile(r"封面\s*[12]", re.I),
]


def lint_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    for phrase in BANNED:
        if phrase in text:
            errors.append(f"{path}: banned phrase: {phrase!r}")
    if "round1" in path.name.lower() or "video-round1" in path.name.lower():
        for pat in ROUND1_NEED:
            if not pat.search(text):
                errors.append(f"{path}: Round1 structure missing pattern {pat.pattern!r}")
                break
    return errors


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*", help="files to lint (default: round1 under content/xiaohongshu)")
    args = ap.parse_args()
    paths = [Path(p) for p in args.paths] if args.paths else list(
        (ROOT / "content/xiaohongshu").glob("*video-round1*.md")
    )
    if not paths:
        print("no files to lint")
        return 0
    all_err: list[str] = []
    for p in paths:
        if p.is_file():
            all_err.extend(lint_file(p))
    if all_err:
        for e in all_err:
            print(e, file=sys.stderr)
        return 1
    print(f"RESULT: PASS voice QA lint ({len(paths)} file(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
