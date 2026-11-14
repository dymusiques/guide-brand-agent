#!/usr/bin/env python3
"""Version-1 vs version-2 distance: pending eval JSON snapshot + diff summary."""

from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVAL = ROOT / "integration/handoff/owner-pending-videos-eval-latest.json"
BASELINE = ROOT / "integration/handoff/owner-pending-videos-eval-baseline.json"
OUT = ROOT / "integration/handoff/owner-pending-eval-version-distance.json"


def file_fingerprint(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    if not EVAL.is_file():
        print("FAIL missing eval latest", file=sys.stderr)
        return 2
    cur_fp = file_fingerprint(EVAL)
    cur = json.loads(EVAL.read_text(encoding="utf-8"))
    prev_fp = None
    distance = {"items_changed": 0, "promote_winner_changed": False}
    if BASELINE.is_file():
        prev = json.loads(BASELINE.read_text(encoding="utf-8"))
        prev_fp = file_fingerprint(BASELINE)
        ids_cur = {i.get("id") for i in cur.get("items") or []}
        ids_prev = {i.get("id") for i in prev.get("items") or []}
        distance["items_added"] = sorted(ids_cur - ids_prev)
        distance["items_removed"] = sorted(ids_prev - ids_cur)
        distance["items_changed"] = len(distance["items_added"]) + len(distance["items_removed"])
        distance["promote_winner_changed"] = cur.get("promote_winner") != prev.get("promote_winner")
    BASELINE.write_text(EVAL.read_text(encoding="utf-8"), encoding="utf-8")
    payload = {
        "as_of": datetime.now(timezone.utc).isoformat(),
        "eval_latest": str(EVAL.relative_to(ROOT)),
        "baseline_updated_from": "eval-latest",
        "fingerprint_before": prev_fp,
        "fingerprint_after": cur_fp,
        "distance": distance,
        "status": "PASS",
        "note": "每次 gate 将 latest 滚动为 baseline；distance 描述相对上一轮",
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
