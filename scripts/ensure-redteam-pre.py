#!/usr/bin/env python3
"""Ensure redteam-pre exists for each *-brief.md (AUTO · no Owner). Idempotent."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REDTEAM = ROOT / "content/xiaohongshu/redteam"
XHS = ROOT / "content/xiaohongshu"

# Default trap pairs by theme (X ids from shared_traps)
THEME_TRAPS: list[tuple[tuple[str, ...], tuple[str, str]]] = [
    (("discovery", "品牌", "艺术"), ("X7", "X5")),
    (("narrative", "硬广", "预算"), ("X3", "X9")),
    (("trust", "专业"), ("X2", "X8")),
    (("open", "收口", "跨行业"), ("X7", "X3")),
    (("artist", "benchmark", "violakid"), ("X10", "X11")),
    (("brand-art", "叙事"), ("X3", "X5")),
]


def pre_path(brief: Path) -> Path:
    base = brief.name.replace("-brief.md", "")
    return REDTEAM / f"{base}-pre.md"


def pick_traps(brief: Path, text: str) -> tuple[str, str]:
    blob = (brief.name + text).lower()
    for keys, (a, b) in THEME_TRAPS:
        if any(k in blob for k in keys):
            return a, b
    return "X5", "X6"


def template(slug: str, x1: str, x2: str) -> str:
    return f"""# Redteam pre · {slug} · AUTO

> 由 `ensure-redteam-pre.py` 自动生成；CEO/04 应在改 Brief 时细化驳/改。

- **攻击 1**（{x1}）：同质化 / 空泛 / 无 moment → 数据策略 Top 帖需故事+判断。
- **驳/改：** 前 3 行加具体 moment；CTA 品牌向收藏+聊聊。

- **攻击 2**（{x2}）：弱 CTA 或误读为教学号/硬广。
- **驳/改：** 对齐 ip-positioning；标签≥3（交付规范 10）。

- **CEO：** 允许迭代 Brief；须 `evaluate-xhs-brief-complete.py` PASS 再交 Owner。
"""


def ensure_one(brief: Path, force: bool = False) -> bool:
    rt = pre_path(brief)
    if rt.is_file() and rt.stat().st_size > 80 and not force:
        return False
    REDTEAM.mkdir(parents=True, exist_ok=True)
    text = brief.read_text(encoding="utf-8") if brief.is_file() else ""
    slug = brief.name.replace("-brief.md", "")
    x1, x2 = pick_traps(brief, text)
    rt.write_text(template(slug, x1, x2), encoding="utf-8")
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--brief", type=Path, action="append", default=[])
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    briefs: list[Path] = []
    if args.all:
        briefs = sorted(XHS.glob("*-brief.md"))
    for b in args.brief:
        briefs.append(b if b.is_absolute() else ROOT / b)
    if not briefs:
        ap.error("--brief or --all")
    created = 0
    for b in briefs:
        if not b.is_file():
            print(f"FAIL missing {b}", file=sys.stderr)
            return 1
        if ensure_one(b, force=args.force):
            print(f"CREATED {pre_path(b).relative_to(ROOT)}")
            created += 1
        else:
            print(f"OK {pre_path(b).relative_to(ROOT)}")
    print(f"ensure-redteam-pre: {created} created, {len(briefs) - created} already ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
