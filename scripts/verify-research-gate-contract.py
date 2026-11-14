#!/usr/bin/env python3
"""CI: agent-owner-research-gate 合同与入口脚本（无 Google / 不长跑 gate）。"""

from __future__ import annotations

import json
import py_compile
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTRACT = ROOT / "integration/handoff/agent-owner-research-gate-contract.json"
ENTRY = ROOT / "scripts/agent-owner-research-gate.py"
LAYERS_MIN = 10


def main() -> int:
    fail = 0
    for p in (CONTRACT, ENTRY):
        if not p.is_file():
            print(f"FAIL verify-research-gate-contract: missing {p}", file=sys.stderr)
            fail += 1
    if fail:
        return 1
    try:
        py_compile.compile(str(ENTRY), doraise=True)
    except py_compile.PyCompileError as e:
        print(f"FAIL compile agent-owner-research-gate: {e}", file=sys.stderr)
        return 1
    data = json.loads(CONTRACT.read_text(encoding="utf-8"))
    layers = data.get("layers_required") or []
    if len(layers) < LAYERS_MIN:
        print(f"FAIL: layers_required count {len(layers)} < {LAYERS_MIN}", file=sys.stderr)
        fail += 1
    if data.get("entry_script") != "scripts/agent-owner-research-gate.py":
        print("FAIL: contract entry_script mismatch", file=sys.stderr)
        fail += 1
    pre = (ROOT / "scripts/agent-brainstorm-preflight.py").read_text(encoding="utf-8")
    if "agent-owner-research-gate.py" not in pre:
        print("FAIL: brainstorm-preflight must invoke research-gate", file=sys.stderr)
        fail += 1
    gate = (ROOT / "scripts/agent-owner-research-gate.py").read_text(encoding="utf-8")
    if "agent-platform-voice-benchmark.py" not in gate:
        print("FAIL: research-gate must invoke platform-voice-benchmark", file=sys.stderr)
        fail += 1
    if "agent-owner-copy-pipeline-gate.py" not in gate:
        print("FAIL: research-gate must invoke owner-copy-pipeline-gate", file=sys.stderr)
        fail += 1
    sess = (ROOT / "scripts/agent-owner-content-session.py").read_text(encoding="utf-8")
    if '"--deep"' not in sess:
        print("FAIL: content-session must pass --deep on deep goals", file=sys.stderr)
        fail += 1
    if fail:
        return 1
    print("PASS verify-research-gate-contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())