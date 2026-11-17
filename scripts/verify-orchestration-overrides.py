#!/usr/bin/env python3
"""CI: owner-orchestration-overrides + gate_ceo_orchestration 接线."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OVERRIDES = ROOT / "integration/handoff/owner-orchestration-overrides.json"


def main() -> int:
    fail = 0
    if not OVERRIDES.is_file():
        print("FAIL: missing owner-orchestration-overrides.json", file=sys.stderr)
        return 1
    data = json.loads(OVERRIDES.read_text(encoding="utf-8"))
    if not data.get("rules"):
        print("FAIL: overrides rules empty", file=sys.stderr)
        fail += 1
    sys.path.insert(0, str(ROOT / "scripts"))
    from gate_ceo_orchestration import orchestration_mode, override_mode  # noqa: E402

    if override_mode("CEO 开始执行新一轮小红书战役") != "copy_ceo_full":
        print("FAIL: override should force copy_ceo_full for CEO 开始执行", file=sys.stderr)
        fail += 1
    if override_mode("先讨论发圈节奏和封面") != "replay_only":
        print("FAIL: discuss-only override should be replay_only", file=sys.stderr)
        fail += 1
    if orchestration_mode(goal="只要复盘结论不要 CEO") == "copy_ceo_full":
        print("FAIL: explicit no-ceo override", file=sys.stderr)
        fail += 1
    if fail:
        return 1
    print("PASS verify-orchestration-overrides")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())