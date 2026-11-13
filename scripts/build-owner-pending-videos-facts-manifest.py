#!/usr/bin/env python3
"""Full-text facts manifest for Agent (decision字段). Runs after evaluate or via gate."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from pending_video_md_lib import parse_pending_video

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "content/xiaohongshu/inbox/pending-videos"
OUT = ROOT / "integration/handoff/owner-pending-videos-facts-latest.json"
SCORING_MODEL = "rule-v2-full-body-2026-11-13"


def inbox_mtimes(inbox: Path) -> dict[str, float]:
    skip = {"readme.md", "template.md"}
    out: dict[str, float] = {}
    for p in sorted(inbox.glob("*.md")):
        if p.name.lower() in skip:
            continue
        out[str(p.relative_to(ROOT))] = p.stat().st_mtime
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--inbox", type=Path, default=INBOX)
    ap.add_argument("--out", type=Path, default=OUT)
    args = ap.parse_args()

    skip = {"readme.md", "template.md"}
    paths = sorted(
        p for p in args.inbox.glob("*.md") if p.name.lower() not in skip
    )
    items = []
    for p in paths:
        it = parse_pending_video(p, ROOT)
        it.pop("body_stripped", None)
        items.append(it)
    mtimes = inbox_mtimes(args.inbox)

    payload = {
        "as_of": datetime.now(timezone.utc).isoformat(),
        "status": "ok" if items else "empty_inbox",
        "scoring_model": SCORING_MODEL,
        "facts_source": "content/xiaohongshu/inbox/pending-videos/*.md",
        "agent_must_cite_field": "decision_summary",
        "forbidden_for_decisions": ["body_preview", "human_glance_only", "excerpts_for_orientation_only"],
        "inbox_file_mtimes": mtimes,
        "inbox_latest_mtime": max(mtimes.values()) if mtimes else 0.0,
        "item_count": len(items),
        "items": items,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"OK facts {len(items)} items → {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
