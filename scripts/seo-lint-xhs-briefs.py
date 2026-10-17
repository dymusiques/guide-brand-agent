#!/usr/bin/env python3
"""Light SEO / discoverability lint for XHS briefs (tags, title, CTA)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
XHS = ROOT / "content/xiaohongshu"


def lint_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errs: list[str] = []
    if not re.search(r"^##\s+标签\s*$", text, re.M):
        errs.append("missing ## 标签")
    else:
        block = re.split(r"^##\s+标签\s*$", text, maxsplit=1, flags=re.M)
        if len(block) > 1:
            rest = block[1].split("\n## ", 1)[0]
            hashtags = re.findall(r"#[\w\u4e00-\u9fff]+", rest)
            bullets = [ln.strip() for ln in rest.splitlines() if ln.strip().startswith("-")]
            tag_count = len(hashtags) if hashtags else len(bullets)
            if tag_count < 3:
                errs.append(f"tags count {tag_count} < 3")
    title = ""
    if m := re.search(r"^#\s+(.+)$", text, re.M):
        title = m.group(1).strip()
    if not title or len(title) < 8:
        errs.append("title too short")
    if len(title) > 40:
        errs.append("title > 40 chars (XHS cover)")
    cta_markers = ("私信", "聊聊", "收藏", "合作", "评估", "CTA")
    if not any(c in text for c in cta_markers):
        errs.append("no soft CTA marker")
    return errs


def main() -> int:
    paths = sorted(XHS.glob("*-brief.md"))
    if not paths:
        print("WARN no briefs")
        return 0
    failed = 0
    print("=== SEO lint (XHS briefs) ===\n")
    for p in paths:
        errs = lint_file(p)
        if errs:
            print(f"  FAIL · {p.name}: {', '.join(errs)}")
            failed += 1
        else:
            print(f"  PASS · {p.name}")
    print(f"\n=== Summary ===\n{len(paths) - failed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
