#!/usr/bin/env python3
"""Restore notes.csv from latest notes-snapshot-*.json when csv/snapshot diverge."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIR = ROOT / "content/analytics/xiaohongshu"
NOTES = DIR / "notes.csv"
FIELDNAMES = [
    "note_id",
    "publish_date",
    "title",
    "pillar",
    "impressions",
    "views",
    "likes",
    "collects",
    "comments",
    "shares",
    "follows_from_note",
    "dm_count",
    "dm_keywords",
    "aligned_at_publish",
    "brief_path",
    "cover_ctr_pct",
    "avg_watch_sec",
    "completion_rate_pct",
    "exit_2s_rate_pct",
    "detail_source",
]


def main() -> int:
    snaps = sorted(DIR.glob("notes-snapshot-*.json"), reverse=True)
    if not snaps:
        print("FAIL no snapshot", file=sys.stderr)
        return 2
    data = json.loads(snaps[0].read_text(encoding="utf-8"))
    rows = data.get("rows") or []
    if not rows:
        print("FAIL empty snapshot", file=sys.stderr)
        return 2
    with NOTES.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDNAMES, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in FIELDNAMES})
    print(f"OK restored {len(rows)} rows from {snaps[0].name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
