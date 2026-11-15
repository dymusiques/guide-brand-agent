#!/usr/bin/env python3
"""
gate PASS 后：写稿类 → run_ceo_full（--skip-research-gate）；复盘类 → SKIP。

handoff: integration/handoff/owner-gate-ceo-orchestrator-latest.json
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "integration/handoff/owner-gate-ceo-orchestrator-latest.json"
GATE_HANDOFF = ROOT / "integration/handoff/owner-research-gate-latest.json"
sys.path.insert(0, str(ROOT / "scripts"))
from gate_ceo_orchestration import orchestration_mode  # noqa: E402


def run(cmd: list[str], *, timeout: int = 3600) -> tuple[int, str]:
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=timeout)
    out = ((r.stdout or "") + (r.stderr or "")).strip()
    return r.returncode, out[-4000:]


def gate_passes_for_goal(goal: str) -> tuple[bool, str]:
    if not GATE_HANDOFF.is_file():
        return False, "missing owner-research-gate-latest.json"
    data = json.loads(GATE_HANDOFF.read_text(encoding="utf-8"))
    if data.get("status") != "PASS":
        return False, f"gate status={data.get('status')!r}"
    hg = str(data.get("goal") or "")
    if goal and goal not in hg and hg not in goal:
        if not any(k in goal and k in hg for k in ("复盘", "艺术家", "口播", "CEO", "小红书", "写稿")):
            return False, f"gate goal mismatch: {goal!r} vs {hg!r}"
    return True, "gate PASS"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--goal", required=True)
    ap.add_argument("--brief", default="", help="content/xiaohongshu/...-brief.md")
    ap.add_argument("--skip-brief-loop", action="store_true")
    ap.add_argument("--require-gate-pass", action="store_true", default=True)
    ap.add_argument("--no-require-gate-pass", action="store_false", dest="require_gate_pass")
    ap.add_argument("--force-ceo", action="store_true")
    ap.add_argument("--force-replay", action="store_true")
    args = ap.parse_args()
    goal = args.goal.strip()
    brief = args.brief.strip()
    mode = orchestration_mode(
        goal=goal,
        brief=brief,
        force_ceo=args.force_ceo,
        force_replay=args.force_replay,
    )

    payload: dict = {
        "schema": "owner_gate_ceo_orchestrator_v1",
        "as_of": datetime.now(timezone.utc).isoformat(),
        "goal": goal,
        "brief": brief,
        "mode": mode,
        "steps": [],
        "status": "SKIP",
    }

    if mode == "skip":
        OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"status": "SKIP", "mode": mode, "handoff": str(OUT.relative_to(ROOT))}))
        return 0

    if mode == "replay_only":
        payload["status"] = "SKIP"
        payload["note"] = "复盘/监督类 · gate PASS 即停 · 不自动 CEO full"
        OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"status": "SKIP", "mode": mode, "handoff": str(OUT.relative_to(ROOT))}))
        return 0

    if args.require_gate_pass:
        ok, msg = gate_passes_for_goal(goal)
        if not ok:
            payload["status"] = "FAIL"
            payload["error"] = msg
            OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(json.dumps(payload), file=sys.stderr)
            return 1

    ceo_cmd = [
        sys.executable,
        "scripts/run_ceo_full_execution.py",
        "--goal",
        goal,
        "--skip-research-gate",
    ]
    if brief:
        ceo_cmd.extend(["--brief", brief])

    ec, tail = run(ceo_cmd, timeout=2400)
    payload["steps"].append({"name": "run_ceo_full_execution", "exit_code": ec, "tail": tail[-800:]})

    brief_loop_ec: int | None = None
    if brief and not args.skip_brief_loop and ec in (0, 42):
        ec_bl, tail_bl = run(
            ["bash", "scripts/manager-ceo-auto-gate-loop.sh", "--brief", brief, "--max-rounds", "3"],
            timeout=2400,
        )
        brief_loop_ec = ec_bl
        payload["steps"].append({"name": "manager_ceo_auto_gate_loop", "exit_code": ec_bl, "tail": tail_bl[-800:]})

    if ec == 0 and (brief_loop_ec is None or brief_loop_ec == 0):
        payload["status"] = "PASS"
    elif ec == 42 or brief_loop_ec == 42:
        payload["status"] = "NEEDS_WORK"
    else:
        payload["status"] = "FAIL"

    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": payload["status"], "mode": mode, "handoff": str(OUT.relative_to(ROOT))}))
    return 0 if payload["status"] in ("PASS", "NEEDS_WORK", "SKIP") else 1


if __name__ == "__main__":
    raise SystemExit(main())