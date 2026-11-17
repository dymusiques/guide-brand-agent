#!/usr/bin/env python3
"""Owner: 记进启发 / 归到聊天启发 → content/personal-ip/chat-sparks/YYYY-MM-DD-<slug>.md"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPARKS = ROOT / "content/personal-ip/chat-sparks"
TEMPLATE = SPARKS / "_TEMPLATE.md"


def slugify(s: str) -> str:
    s = s.strip()[:48]
    s = re.sub(r"[^\w\u4e00-\u9fff]+", "-", s).strip("-").lower()
    return s or "spark"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--title", required=True, help="一句话标题")
    ap.add_argument("--claim", required=True, help="主张一句")
    ap.add_argument("--source", choices=["chat", "url"], default="chat")
    ap.add_argument("--source-ref", default="", help="URL 或对话摘要")
    ap.add_argument("--platforms", default="xhs,linkedin,medium", help="逗号分隔")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    SPARKS.mkdir(parents=True, exist_ok=True)
    day = date.today().isoformat()
    path = SPARKS / f"{day}-{slugify(args.title)}.md"
    n = 0
    while path.exists():
        n += 1
        path = SPARKS / f"{day}-{slugify(args.title)}-{n}.md"
    body = f"""# Chat spark · {args.title.strip()}

- **as_of**: {day}
- **source**: {args.source}
- **source_ref**: {args.source_ref.strip() or "（Owner 对话）"}
- **status**: draft

## 主张（一句）

{args.claim.strip()}

## IP 契合（法派 / 品牌×艺术 / 强链接）

（Agent 或 Owner 补一句）

## 可发展平台（{args.platforms}）
"""
    if args.dry_run:
        print(body)
        return 0
    path.write_text(body, encoding="utf-8")
    print(path.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())