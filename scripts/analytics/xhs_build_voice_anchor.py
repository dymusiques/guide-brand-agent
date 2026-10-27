#!/usr/bin/env python3
"""Build voice-anchor-sources.json from snapshot + note-links (titles + metrics + URLs).

Note body text is NOT in Creator Center Excel. Optional fetch via xhs_fetch_note_captions.py.
"""

from __future__ import annotations

import csv
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SNAPSHOT = ROOT / "content/analytics/xiaohongshu/notes-snapshot-2026-10-20.json"
LINKS = ROOT / "content/analytics/xiaohongshu/note-links.csv"
OUT = ROOT / "content/xiaohongshu/voice-anchor-sources.json"
ANCHOR_N = 5
# Story/judgment posts (not numbered tutorial series)
TUTORIAL_RE = re.compile(r"教你|怎么按|姿势|指法|误区|颤音|双吐|连贯|音头|头晕|低音")
HARD_EXCLUDE = re.compile(r"揭秘|秘籍")
STORY_HINT = re.compile(r"泰斗|考场|嘲讽|比赛|自媒体|深度替代|剧本|判断权")


def load_links() -> dict[str, str]:
    out: dict[str, str] = {}
    if not LINKS.is_file():
        return out
    with LINKS.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            title = (row.get("title") or "").strip()
            url = (row.get("note_url") or "").strip()
            if title and url:
                out[title] = url
    return out


def float_or_zero(s: str) -> float:
    try:
        return float(s)
    except (TypeError, ValueError):
        return 0.0


def main() -> int:
    snap = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    links = load_links()
    rows = snap.get("rows") or []
    candidates = []
    for r in rows:
        title = (r.get("title") or "").strip()
        if not title:
            continue
        follows = float_or_zero(r.get("follows_from_note", "0"))
        collects = float_or_zero(r.get("collects", "0"))
        if HARD_EXCLUDE.search(title):
            continue
        if TUTORIAL_RE.search(title) and not STORY_HINT.search(title):
            continue
        if not STORY_HINT.search(title) and follows < 40:
            continue
        candidates.append(
            {
                "title": title,
                "publish_date": r.get("publish_date", ""),
                "note_url": links.get(title, r.get("note_id", "")),
                "follows_from_note": follows,
                "collects": collects,
                "cover_ctr_pct": r.get("cover_ctr_pct", ""),
                "completion_rate_pct": r.get("completion_rate_pct", ""),
                "first_80_chars": "",
                "caption_status": "pending",
                "caption_source": "",
            }
        )
    candidates.sort(key=lambda x: (x["follows_from_note"], x["collects"]), reverse=True)
    anchors = candidates[:ANCHOR_N]
    payload = {
        "as_of": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "anchor_count": len(anchors),
        "note": "first_80_chars: run xhs_fetch_note_captions.py after XHS login, or Owner paste from App.",
        "anchors": anchors,
    }
    if OUT.is_file():
        prev = json.loads(OUT.read_text(encoding="utf-8"))
        by_title = {a.get("title"): a for a in (prev.get("anchors") or [])}
        for a in anchors:
            old = by_title.get(a["title"]) or {}
            if old.get("caption_status", "").startswith("owner"):
                for k in ("first_80_chars", "caption_status", "caption_source", "agent_note"):
                    if old.get(k):
                        a[k] = old[k]
        if prev.get("transcripts"):
            payload["transcripts"] = prev["transcripts"]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT} ({len(anchors)} anchors)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
