#!/usr/bin/env python3
"""All agents · 6 cases each (10 × 6 = 60)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from integration.agents._runner import AGENT_MODULES, run_agent_module, run_all_agents  # noqa: E402

AGENT_BY_NUM = {
    "00": AGENT_MODULES[0],
    "01": AGENT_MODULES[1],
    "02": AGENT_MODULES[2],
    "03": AGENT_MODULES[3],
    "04": AGENT_MODULES[4],
    "05": AGENT_MODULES[5],
    "06": AGENT_MODULES[6],
    "07": AGENT_MODULES[7],
    "08": AGENT_MODULES[8],
    "09": AGENT_MODULES[9],
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent", help="Run single agent id 00-09")
    args = parser.parse_args()
    print("=== Agent integration matrix verify ===")
    if args.agent:
        mod = AGENT_BY_NUM.get(args.agent.zfill(2) if len(args.agent) == 1 else args.agent)
        if not mod:
            print(f"Unknown agent {args.agent}")
            return 2
        p, f, _ = run_agent_module(mod)
        if f:
            print("RESULT: FAIL")
            return 1
        print("RESULT: PASS — single agent matrix")
        return 0
    return run_all_agents()


if __name__ == "__main__":
    sys.exit(main())
