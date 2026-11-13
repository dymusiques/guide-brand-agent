#!/usr/bin/env python3
"""交付前断言：若要给 pending 口播事实/薯条结论，advice gate 须 PASS（非 EXEMPT brainstorm）。"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GATE = ROOT / "integration/handoff/owner-pending-videos-advice-gate-latest.json"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--require-advice",
        action="store_true",
        help="调用方声明本轮要给口播结论（Agent 给薯条/标题前自跑）",
    )
    args = ap.parse_args()
    if not args.require_advice:
        print("SKIP assert-pending-videos-advice-gate (no --require-advice)")
        return 0
    if not GATE.is_file():
        print("FAIL missing advice-gate handoff", file=sys.stderr)
        return 1
    data = json.loads(GATE.read_text(encoding="utf-8"))
    if data.get("mode") == "brainstorm":
        print(
            "FAIL brainstorm 豁免中 — 不得交付事实结论；改跑: "
            "python3 scripts/agent-gate-pending-videos-advice.py --intent advice",
            file=sys.stderr,
        )
        return 1
    if data.get("status") != "PASS" or not data.get("advice_allowed"):
        print(f"FAIL gate status={data.get('status')}", file=sys.stderr)
        return 1
    print(f"PASS assert advice-gate as_of={str(data.get('as_of', ''))[:19]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
