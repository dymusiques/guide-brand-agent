#!/usr/bin/env python3
"""Brainstorm/拍板前：小红书 warehouse 行数与 snapshot 对齐（防只瞄一眼表头）。"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "content/analytics/xiaohongshu/DATA-MANIFEST.json"
NOTES = ROOT / "content/analytics/xiaohongshu/notes.csv"
HANDOFF = ROOT / "integration/handoff/owner-xhs-data-drive.json"


def count_notes_csv() -> int:
    if not NOTES.is_file():
        return -1
    with NOTES.open(encoding="utf-8") as f:
        return sum(1 for _ in csv.DictReader(f))


def latest_snapshot_count() -> int | None:
    snap_dir = ROOT / "content/analytics/xiaohongshu"
    snaps = sorted(snap_dir.glob("notes-snapshot-*.json"), reverse=True)
    if not snaps:
        return None
    data = json.loads(snaps[0].read_text(encoding="utf-8"))
    items = data.get("rows") or data.get("notes") or data.get("items") or []
    return len(items)


def main() -> int:
    errs: list[str] = []
    n_csv = count_notes_csv()
    if n_csv < 0:
        errs.append("missing notes.csv — run xhs-owner-data-auto-sync")
    n_snap = latest_snapshot_count()
    manifest_n = None
    if MANIFEST.is_file():
        manifest_n = json.loads(MANIFEST.read_text(encoding="utf-8")).get("note_count")
    if n_snap is not None and n_csv >= 0 and n_csv != n_snap:
        errs.append(f"notes.csv rows={n_csv} vs latest snapshot={n_snap}")
    manifest_warn = None
    if manifest_n is not None and n_csv >= 0 and n_csv != manifest_n:
        manifest_warn = f"WARN DATA-MANIFEST note_count={manifest_n} stale vs csv={n_csv}"
    if errs:
        print("FAIL xhs-analytics-freshness:\n- " + "\n- ".join(errs), file=sys.stderr)
        if HANDOFF.is_file():
            print(f"hint: {HANDOFF}", file=sys.stderr)
        return 1
    line = f"PASS xhs-analytics-freshness notes={n_csv} snapshot={n_snap}"
    if manifest_warn:
        line += f" ({manifest_warn})"
    print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
