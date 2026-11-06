#!/usr/bin/env python3
"""
Validate L2 rubric file exists and meets min scores (Agent fills scores + evidence).
Does NOT auto-score prose — Agent must write rubric JSON honestly after self-check.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RUBRIC_SPEC = ROOT / "integration/handoff/owner-copy-success-rubric.json"
SCORE_DIR = ROOT / "content/xiaohongshu/rubric-scores"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--brief", required=True)
    p.add_argument("--require-file", action="store_true", default=True)
    args = p.parse_args()
    brief = args.brief.strip().lstrip("/")
    stem = Path(brief).name
    score_path = SCORE_DIR / f"{stem}.json"

    if not RUBRIC_SPEC.is_file():
        print("FAIL: missing owner-copy-success-rubric.json")
        return 1

    spec = json.loads(RUBRIC_SPEC.read_text(encoding="utf-8"))
    dims = {d["id"]: d for d in spec.get("dimensions") or []}
    overall_min = float(spec.get("overall_min_weighted") or 80)

    if not score_path.is_file():
        print(f"FAIL: missing rubric scores: {score_path.relative_to(ROOT)}")
        print("HINT: Agent Must fill L2 self-score + evidence URLs after attestation")
        print("HINT: docs/OWNER-SUCCESS-METRICS-MAP.md")
        return 1

    data = json.loads(score_path.read_text(encoding="utf-8"))
    if data.get("brief") and data["brief"] != brief:
        print(f"FAIL: rubric brief mismatch")
        return 1

    scores = data.get("scores") or {}
    fails: list[str] = []
    weighted = 0.0
    total_w = 0.0
    for did, dspec in dims.items():
        entry = scores.get(did) or {}
        sc = entry.get("score")
        if not isinstance(sc, (int, float)):
            fails.append(f"{did}: missing numeric score")
            continue
        sc = float(sc)
        w = float(dspec.get("weight") or 0)
        min_s = float(dspec.get("min_score") or 0)
        total_w += w
        weighted += sc * w
        if sc < min_s:
            fails.append(f"{did}: score {sc} < min {min_s}")
        ev = (entry.get("evidence") or "").strip()
        if spec.get("evidence_required") and len(ev) < 15:
            fails.append(f"{did}: evidence too short (need attestation URL or quote ref)")

    if total_w > 0:
        weighted /= total_w
    else:
        weighted = 0.0

    if data.get("owner_review_still_required") is not True:
        fails.append("owner_review_still_required must be true")

    if weighted < overall_min:
        fails.append(f"weighted {weighted:.1f} < overall_min {overall_min}")

    if fails:
        for f in fails:
            print(f"FAIL: {f}")
        return 1

    print(f"PASS score-owner-copy-success-rubric · weighted={weighted:.1f}")
    print("NOTE: L2 PASS = Agent self-check; Owner L3 still required for publish.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
