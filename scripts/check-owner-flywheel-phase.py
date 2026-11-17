#!/usr/bin/env python3
"""Report flywheel phase 0/1/2 and readiness hints for entering phase 1."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PHASE = ROOT / "integration/handoff/owner-multichannel-flywheel-phase.json"
LI_LEDGER = ROOT / "content/analytics/linkedin/posts.jsonl"
MED_LEDGER = ROOT / "content/analytics/medium/posts.jsonl"
LI_TOPICS = ROOT / "integration/handoff/owner-weekly-li-medium-topic-pack-latest.json"


def count_jsonl(path: Path) -> int:
    if not path.is_file():
        return 0
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())


def xhs_fresh() -> bool:
    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts/verify-xhs-analytics-freshness.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    return r.returncode == 0


def main() -> int:
    if not PHASE.is_file():
        print("FAIL missing phase json", file=sys.stderr)
        return 2
    cfg = json.loads(PHASE.read_text(encoding="utf-8"))
    phase = int(cfg.get("current_phase", 0))
    sug = cfg.get("suggested_readiness_before_phase_1") or {}
    li_min = int(sug.get("linkedin_metrics_rows_min") or 2)
    med_min = int(sug.get("medium_metrics_rows_min") or 2)
    li_n = count_jsonl(LI_LEDGER)
    med_n = count_jsonl(MED_LEDGER)
    fresh = xhs_fresh()
    owner_picked = False
    if LI_TOPICS.is_file():
        data = json.loads(LI_TOPICS.read_text(encoding="utf-8"))
        owner_picked = bool(data.get("owner_picked_serials"))

    checks = {
        "linkedin_metrics_ok": li_n >= li_min,
        "medium_metrics_ok": med_n >= med_min,
        "xhs_freshness_ok": fresh,
        "owner_picked_topic_ok": owner_picked,
    }
    ready_score = sum(1 for v in checks.values() if v)
    suggest_phase_1 = ready_score >= 3 and checks["linkedin_metrics_ok"] and checks["medium_metrics_ok"]

    out = {
        "schema": "owner_flywheel_phase_check_v1",
        "as_of": datetime.now(timezone.utc).isoformat(),
        "current_phase": phase,
        "phase_label": (cfg.get("phase_labels") or {}).get(str(phase), ""),
        "metrics": {"linkedin_rows": li_n, "medium_rows": med_n, "xhs_fresh": fresh},
        "readiness_checks": checks,
        "suggest_owner_may_say_enter_phase_1": suggest_phase_1,
        "owner_trigger_phase_1": cfg.get("owner_enter_phase_1_phrases_any"),
        "owner_trigger_phase_2": cfg.get("owner_enter_phase_2_phrases_any"),
        "next_owner_action_zh": (
            "进入写稿阶段（或 派活给 CEO + 选题）"
            if suggest_phase_1 and phase == 0
            else "继续阶段 0：发帖后填 inbox 数据 + 周日收选题；勾选序号即可"
        ),
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())