#!/usr/bin/env python3
"""
B 档 · gate PASS 后 evaluate 切片（无 run_ceo_full / HTML 战役全家桶）。

handoff: integration/handoff/owner-evaluate-post-gate-latest.json
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "integration/handoff/owner-evaluate-post-gate-latest.json"
ARTISTS_HIT = ROOT / "content/evolution/00-manager/ceo-inbox/2026-11-03-artists-three"
VENV_PY = ROOT / ".venv/bin/python3"


def run(cmd: list[str], *, timeout: int = 900) -> tuple[int, str]:
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=timeout)
    out = ((r.stdout or "") + (r.stderr or "")).strip()
    return r.returncode, out[-3000:]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--goal", required=True)
    ap.add_argument("--brief", default="")
    ap.add_argument("--max-triple-rounds", type=int, default=1)
    args = ap.parse_args()
    goal = args.goal.strip()
    brief = (args.brief or "").strip()
    py = str(VENV_PY if VENV_PY.is_file() else sys.executable)
    steps: list[dict] = []
    fail = 0

    ec, tail = run([py, "scripts/evaluate_personal_ip.py", "--check"], timeout=120)
    steps.append({"name": "evaluate_personal_ip", "exit_code": ec, "status": "PASS" if ec == 0 else "FAIL", "tail": tail})
    if ec != 0:
        fail += 1

    ec, tail = run([py, "scripts/agent-pending-eval-baseline-snapshot.py"], timeout=180)
    steps.append(
        {
            "name": "pending_eval_baseline_snapshot",
            "exit_code": ec,
            "status": "PASS" if ec == 0 else "FAIL",
            "tail": tail,
        }
    )
    if ec != 0:
        fail += 1

    if brief:
        brief_path = brief if brief.startswith("/") else str(ROOT / brief)
        if Path(brief_path).is_file():
            ec, tail = run(
                [
                    "bash",
                    "scripts/ceo-triple-eval-baseline-loop.sh",
                    "--brief",
                    brief_path,
                    "--max",
                    str(max(1, args.max_triple_rounds)),
                ],
                timeout=1800,
            )
            st = "PASS" if ec == 0 else ("NEEDS_WORK" if ec == 42 else "FAIL")
            steps.append({"name": "ceo_triple_eval_baseline_loop", "exit_code": ec, "status": st, "tail": tail})
            if ec not in (0, 42):
                fail += 1
        else:
            steps.append({"name": "ceo_triple_eval_baseline_loop", "status": "SKIP", "note": f"brief missing: {brief}"})

    if ARTISTS_HIT.is_dir() and any(k in goal for k in ("艺术家", "不需要", "已发", "复盘", "监督")):
        ec, tail = run([py, "scripts/verify-four-dimension-bar.py"], timeout=120)
        steps.append(
            {
                "name": "four_dimension_bar",
                "exit_code": ec,
                "status": "PASS" if ec == 0 else "NEEDS_WORK",
                "tail": tail,
            }
        )

    payload = {
        "schema": "owner_evaluate_post_gate_v1",
        "as_of": datetime.now(timezone.utc).isoformat(),
        "goal": goal,
        "brief": brief,
        "steps": steps,
        "fail_count": fail,
        "status": "PASS" if fail == 0 else "FAIL",
        "note_zh": "B 档 · 无 run_ceo_full · 无 autopilot HTML",
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": payload["status"], "handoff": str(OUT.relative_to(ROOT)), "fail_count": fail}))
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())