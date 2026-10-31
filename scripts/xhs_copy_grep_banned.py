#!/usr/bin/env python3
"""Scan Xiaohongshu Markdown for banned lexicon (xhs-copy-self-check.md §11).

Mechanical helper only — does not replace the full self-check checklist.
Source lexicon aligned with grapeot/writing-skill rules.py (subset for XHS).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Longer phrases first at match time (sorted below).
BANNED_PHRASES: tuple[str, ...] = (
    "值得关注",
    "值得一提",
    "值得注意",
    "值得一读",
    "意义重大",
    "深入探讨",
    "毫无疑问",
    "不言而喻",
    "至关重要",
    "按我们的理解",
    "在我们的理解",
    "我们的理解是",
    "按我们的推断",
    "在我们看来",
    "我们认为",
    "我们觉得",
    "竞赛才刚刚开始",
    "为后续奠定",
    "叙事弧线",
    "叙事弧",
    "范式转移",
    "奠定基础",
    "疯狂发版",
    "一地鸡毛",
    "闭眼编",
    "颠覆性",
    "从这个角度看",
    "需要注意的是",
    "核心要素",
    "核心约束",
    "这意味着",
    "长出来",
    "击穿",
    "打穿",
    "拆解",
    "收口",
    "赋能",
    "颠覆",
    "结构性",
    "很稳",
    "更稳",
    "卡点",
    "撑破",
    "撑不住",
    "尺子",
    "算账",
    "生长",
    "值得",
)

CODE_FENCE_RE = re.compile(r"^```", re.M)
FRONT_MATTER_RE = re.compile(r"\A---\n.*?\n---\n", re.S)


def _strip_for_scan(text: str) -> tuple[str, list[int]]:
    """Return (body, line_map) where line_map[i] = 1-based source line for body line i."""
    raw = text.replace("\r\n", "\n").replace("\r", "\n")
    body = raw
    if raw.startswith("---"):
        m = FRONT_MATTER_RE.match(raw)
        if m:
            body = raw[m.end() :]
    fm_lines = raw[: len(raw) - len(body)].count("\n") if body != raw else 0

    out_lines: list[str] = []
    line_map: list[int] = []
    in_fence = False
    for i, line in enumerate(body.splitlines()):
        src_line = fm_lines + i + 1
        if CODE_FENCE_RE.match(line.strip()):
            in_fence = not in_fence
            out_lines.append("")
            line_map.append(src_line)
            continue
        if in_fence:
            out_lines.append("")
        else:
            out_lines.append(line)
        line_map.append(src_line)
    return "\n".join(out_lines), line_map


def _build_pattern() -> re.Pattern[str]:
    ordered = sorted(BANNED_PHRASES, key=len, reverse=True)
    parts = [re.escape(p) for p in ordered]
    return re.compile("|".join(parts))


def scan_text(text: str, path: str = "<stdin>") -> list[tuple[int, str, str]]:
    body, line_map = _strip_for_scan(text)
    pattern = _build_pattern()
    hits: list[tuple[int, str, str]] = []
    for i, line in enumerate(body.splitlines()):
        for m in pattern.finditer(line):
            src_line = line_map[i] if i < len(line_map) else i + 1
            hits.append((src_line, m.group(0), line.strip()[:100]))
    return hits


def scan_path(path: Path) -> list[tuple[int, str, str]]:
    return scan_text(path.read_text(encoding="utf-8"), path=str(path))


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Grep banned AI-slop phrases in XHS Markdown (see xhs-copy-self-check.md §11).",
    )
    p.add_argument("path", type=Path, help="Markdown file under content/xiaohongshu/ or elsewhere")
    p.add_argument("--quiet", action="store_true", help="Only print summary line")
    args = p.parse_args(argv)

    if not args.path.is_file():
        print(f"error: not a file: {args.path}", file=sys.stderr)
        return 2

    try:
        hits = scan_path(args.path)
    except OSError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    if not hits:
        print(f"PASS: no banned lexicon hits in {args.path}")
        return 0

    if not args.quiet:
        print(f"FAIL: {len(hits)} banned lexicon hit(s) in {args.path}")
        print("      (review xhs-copy-self-check.md §11; exceptions need Owner note)\n")
        for line_no, word, snippet in hits:
            print(f"  L{line_no}  [{word}]  {snippet}")
    else:
        print(f"FAIL: {len(hits)} hit(s) in {args.path}")

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
