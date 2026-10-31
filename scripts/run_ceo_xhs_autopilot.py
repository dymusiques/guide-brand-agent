#!/usr/bin/env python3
"""CEO · full XHS owner delivery autopilot (Python orchestrator).

Does NOT LLM-write briefs. Runs existing bash/python integration chain.
See docs/CEO-XHS-OWNER-DELIVERY-AUTOPILOT.md · docs/AUTOMATION-LAYERS-MD-VS-PYTHON.md
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run(cmd: list[str], *, step: str, env: dict[str, str] | None = None) -> int:
    print(f"\n>>> {step}\n>>> {' '.join(cmd)}", flush=True)
    r = subprocess.run(cmd, cwd=ROOT, env=env)
    if r.returncode != 0:
        print(f"FAIL: {step} exit={r.returncode}", file=sys.stderr)
    return r.returncode


def main() -> int:
    p = argparse.ArgumentParser(description="CEO XHS autopilot (evolution + HTML + optional round2)")
    p.add_argument("--brief", action="append", default=[], help="Repeatable; Discovery → auto 01-04")
    p.add_argument("--round2", action="store_true", help="Workflow test campaign after delivery")
    p.add_argument("--skip-evolution", action="store_true", help="Only refresh HTML + verify")
    p.add_argument("--no-discovery-auto", action="store_true")
    args = p.parse_args()

    env = os.environ.copy()
    if args.round2:
        env["CEO_WORKFLOW_TEST_ROUND2"] = "1"
    if args.no_discovery_auto:
        env["CEO_DELIVERY_INCLUDE_DISCOVERY"] = "0"
    if args.brief:
        # Last brief wins for HTML owner-latest card + verify subject
        env["CEO_OWNER_EXTRA_BRIEF"] = args.brief[-1]
        env.setdefault("CEO_OWNER_HTML_HASH", "#owner-latest")

    steps: list[tuple[str, list[str]]] = []

    # 01 IP shell (static) — campaign expects function shell
    steps.append(("01 personal-ip shell", [sys.executable, "scripts/evaluate_personal_ip.py", "--check"]))

    if not args.skip_evolution:
        cmd = ["bash", "scripts/manager-ceo-xhs-owner-delivery.sh"]
        for b in args.brief:
            cmd.extend(["--brief", b])
        if args.round2:
            cmd.append("--round2")
        if args.no_discovery_auto:
            cmd.append("--no-discovery-auto")
        steps.append(("XHS owner delivery (evolution+HTML+verify)", cmd))
    else:
        steps.append(("HTML refresh+verify only", ["bash", "scripts/refresh-owner-notify-html.sh"]))

    fail = 0
    for name, cmd in steps:
        ec = run(cmd, step=name, env=env)
        if ec == 42:
            print("NEEDS_WORK: Agent must edit brief per EVOLUTION-GAP", file=sys.stderr)
            return 42
        if ec != 0:
            fail += 1

    summary = {
        "pass": fail == 0,
        "steps": [s[0] for s in steps],
        "root": str(ROOT),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if fail:
        return 1
    print("RESULT: PASS run_ceo_xhs_autopilot")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
