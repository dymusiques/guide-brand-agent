#!/usr/bin/env python3
"""Evaluate LinkedIn + Medium ledger · baseline snapshot (mirrors pending/topic loop)."""

from __future__ import annotations

import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVAL_LATEST = ROOT / "integration/handoff/owner-multichannel-post-eval-latest.json"
EVAL_BASELINE = ROOT / "integration/handoff/owner-multichannel-post-eval-baseline.json"
DISTANCE = ROOT / "integration/handoff/owner-multichannel-post-eval-distance.json"
LI_LEDGER = ROOT / "content/analytics/linkedin/posts.jsonl"
MD_LEDGER = ROOT / "content/analytics/medium/posts.jsonl"

_spec = importlib.util.spec_from_file_location(
    "evaluate_weekly_topic_candidates",
    ROOT / "scripts/evaluate-weekly-topic-candidates.py",
)
_mod = importlib.util.module_from_spec(_spec)
assert _spec and _spec.loader
_spec.loader.exec_module(_mod)
evaluate_items = _mod.evaluate_items


def load_ledger() -> list[dict]:
    items: list[dict] = []
    for path in (LI_LEDGER, MD_LEDGER):
        if not path.is_file():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                items.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return items


def snapshot_baseline(eval_payload: dict) -> None:
    prev_fp = None
    distance: dict = {}
    if EVAL_BASELINE.is_file():
        prev = json.loads(EVAL_BASELINE.read_text(encoding="utf-8"))
        prev_fp = prev.get("fingerprint")
        distance["pass_count_delta"] = int(eval_payload.get("pass_count") or 0) - int(
            prev.get("pass_count") or 0
        )
    import hashlib

    fp = hashlib.sha256(json.dumps(eval_payload, sort_keys=True).encode()).hexdigest()[:24]
    EVAL_BASELINE.write_text(json.dumps(eval_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    dist = {
        "as_of": datetime.now(timezone.utc).isoformat(),
        "fingerprint_before": prev_fp,
        "fingerprint_after": fp,
        "distance": distance,
        "status": "PASS",
    }
    DISTANCE.write_text(json.dumps(dist, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    rows = load_ledger()
    if not rows:
        payload = {
            "as_of": datetime.now(timezone.utc).isoformat(),
            "schema": "owner_multichannel_post_eval_v1",
            "status": "PASS",
            "mode": "empty_ledger",
            "items": [],
        }
        EVAL_LATEST.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        snapshot_baseline(payload)
        print(json.dumps({"status": "PASS", "mode": "empty_ledger"}))
        return 0

    avoid: list[str] = []
    scored = evaluate_items(rows, avoid=avoid)
    scored["schema"] = "owner_multichannel_post_eval_v1"
    EVAL_LATEST.write_text(json.dumps(scored, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    snapshot_baseline(scored)
    print(
        json.dumps(
            {
                "status": scored.get("status"),
                "pass_count": scored.get("pass_count"),
                "item_count": scored.get("item_count"),
            }
        )
    )
    return 0 if scored.get("status") == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())