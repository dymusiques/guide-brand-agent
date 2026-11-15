#!/usr/bin/env python3
"""
Merge 小红书 snapshot 指标进 voice-anchor-sources.json · 保留 Owner 原话字段。

不覆盖 caption_status=owner_* / published_oral_* / draft 的 first_80_chars。
handoff → integration/handoff/owner-voice-anchor-sync-latest.json
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "integration/handoff/owner-voice-anchor-sync-latest.json"
ANCHOR_JSON = ROOT / "content/xiaohongshu/voice-anchor-sources.json"
SNAPSHOT_GLOB = "content/analytics/xiaohongshu/notes-snapshot-*.json"
LINKS = ROOT / "content/analytics/xiaohongshu/note-links.csv"

STORY_HINT = re.compile(r"泰斗|考场|嘲讽|艺术家|大师|祛魅|判断权|深度替代|剧本|不需要")
PROTECTED_STATUS = re.compile(r"^(owner_|published_oral|draft_)")


def latest_snapshot() -> Path | None:
    snaps = sorted(ROOT.glob(SNAPSHOT_GLOB), key=lambda p: p.stat().st_mtime, reverse=True)
    return snaps[0] if snaps else None


def load_links() -> dict[str, str]:
    out: dict[str, str] = {}
    if not LINKS.is_file():
        return out
    import csv

    with LINKS.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            t = (row.get("title") or "").strip()
            u = (row.get("note_url") or "").strip()
            if t and u:
                out[t] = u
    return out


def float_or(s, default=0.0) -> float:
    try:
        return float(s)
    except (TypeError, ValueError):
        return default


def protected_anchor(a: dict) -> bool:
    st = str(a.get("caption_status") or "")
    return bool(PROTECTED_STATUS.search(st)) or bool(a.get("first_80_chars"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    snap_path = latest_snapshot()
    errors: list[str] = []
    merged = 0
    added = 0

    if not snap_path:
        errors.append("no notes-snapshot-*.json")
    existing: dict = {"anchors": []}
    if ANCHOR_JSON.is_file():
        existing = json.loads(ANCHOR_JSON.read_text(encoding="utf-8"))
    by_title = {a.get("title"): dict(a) for a in (existing.get("anchors") or []) if a.get("title")}

    if snap_path:
        snap = json.loads(snap_path.read_text(encoding="utf-8"))
        links = load_links()
        for r in snap.get("rows") or []:
            title = (r.get("title") or "").strip()
            if not title:
                continue
            metrics = {
                "publish_date": r.get("publish_date", ""),
                "note_url": links.get(title) or r.get("note_url") or by_title.get(title, {}).get("note_url"),
                "follows_from_note": float_or(r.get("follows_from_note")),
                "collects": float_or(r.get("collects")),
                "cover_ctr_pct": r.get("cover_ctr_pct", ""),
                "completion_rate_pct": r.get("completion_rate_pct", ""),
                "views": r.get("views") or r.get("观看"),
            }
            if title in by_title:
                cur = by_title[title]
                if not protected_anchor(cur):
                    for k, v in metrics.items():
                        if v not in ("", None, 0, 0.0):
                            cur[k] = v
                else:
                    for k in ("follows_from_note", "collects", "cover_ctr_pct", "completion_rate_pct", "views", "publish_date"):
                        v = metrics.get(k)
                        if v not in ("", None, 0, 0.0):
                            cur[k] = v
                merged += 1
            elif STORY_HINT.search(title):
                by_title[title] = {
                    "title": title,
                    **{k: v for k, v in metrics.items() if v not in ("", None)},
                    "first_80_chars": "",
                    "caption_status": "pending_snapshot",
                    "caption_source": f"sync:{snap_path.name}",
                }
                added += 1

    anchors = list(by_title.values())
    anchors.sort(key=lambda a: (a.get("publish_date") or "", float_or(a.get("follows_from_note"))), reverse=True)

    payload_file = {
        "as_of": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "anchor_count": len(anchors),
        "transcripts": existing.get("transcripts") or "voice-anchor-transcripts-2026-10-21.md",
        "note": existing.get("note") or "first_80_chars = Owner 原话 · Agent 勿润色",
        "anchors": anchors,
        "sync_snapshot": str(snap_path.relative_to(ROOT)) if snap_path else None,
    }
    if not args.dry_run and not errors:
        ANCHOR_JSON.write_text(json.dumps(payload_file, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    handoff = {
        "schema": "owner_voice_anchor_sync_v1",
        "as_of": datetime.now(timezone.utc).isoformat(),
        "snapshot": str(snap_path.relative_to(ROOT)) if snap_path else None,
        "merged_titles": merged,
        "added_titles": added,
        "anchor_count": len(anchors),
        "errors": errors,
        "status": "PASS" if not errors else "FAIL",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(handoff, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": handoff["status"], "handoff": str(OUT.relative_to(ROOT)), "anchors": len(anchors)}))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())