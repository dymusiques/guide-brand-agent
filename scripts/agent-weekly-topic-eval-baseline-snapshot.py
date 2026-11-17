#!/usr/bin/env python3
"""Roll weekly topic eval latest → baseline + distance (mirrors pending-eval snapshot)."""

from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVAL = ROOT / "integration/handoff/owner-weekly-topic-pack-eval-latest.json"
BASELINE = ROOT / "integration/handoff/owner-weekly-topic-pack-eval-baseline.json"
OUT = ROOT / "integration/handoff/owner-weekly-topic-pack-eval-distance.json"


def file_fingerprint(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    if not EVAL.is_file():
        print("FAIL missing weekly topic eval latest", file=sys.stderr)
        return 2
    cur_fp = file_fingerprint(EVAL)
    cur = json.loads(EVAL.read_text(encoding="utf-8"))
    prev_fp = None
    distance = {"avg_match_delta": 0, "pass_count_delta": 0}
    if BASELINE.is_file():
        prev = json.loads(BASELINE.read_text(encoding="utf-8"))
        prev_fp = file_fingerprint(BASELINE)
        prev_items = {i.get("title_zh"): i.get("metrics", {}).get("match_overall") for i in prev.get("items") or []}
        deltas = []
        for it in cur.get("items") or []:
            t = it.get("title_zh")
            if t in prev_items:
                deltas.append(it.get("metrics", {}).get("match_overall", 0) - prev_items[t])
        if deltas:
            distance["avg_match_delta"] = round(sum(deltas) / len(deltas), 2)
        distance["pass_count_delta"] = int(cur.get("pass_count") or 0) - int(prev.get("pass_count") or 0)
        distance["promote_winner_changed"] = cur.get("promote_winner") != prev.get("promote_winner")
    BASELINE.write_text(EVAL.read_text(encoding="utf-8"), encoding="utf-8")
    payload = {
        "as_of": datetime.now(timezone.utc).isoformat(),
        "eval_latest": str(EVAL.relative_to(ROOT)),
        "baseline_updated_from": "weekly-topic-eval-latest",
        "fingerprint_before": prev_fp,
        "fingerprint_after": cur_fp,
        "distance": distance,
        "status": "PASS",
        "note": "每周选题包 evaluate 轮次结束滚动 baseline",
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())