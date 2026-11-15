#!/usr/bin/env python3
"""CI: agent-owner-research-gate 合同与入口脚本（无 Google / 不长跑 gate）。"""

from __future__ import annotations

import json
import py_compile
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTRACT = ROOT / "integration/handoff/agent-owner-research-gate-contract.json"
UNION = ROOT / "integration/handoff/agent-gate-layer-union.json"
ENTRY = ROOT / "scripts/agent-owner-research-gate.py"
LAYERS_MIN = 10
TRACK_RE = re.compile(r"""track\s*\(\s*["']([^"']+)["']""")


def extract_track_names(gate_src: str) -> list[str]:
    """Source-order track() layer names (conditional tracks still listed once in file)."""
    return TRACK_RE.findall(gate_src)


def is_subsequence_ordered(haystack: list[str], needle: list[str]) -> bool:
    it = iter(haystack)
    for name in needle:
        for item in it:
            if item == name:
                break
        else:
            return False
    return True


def main() -> int:
    fail = 0
    for p in (CONTRACT, UNION, ENTRY):
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
    union = json.loads(UNION.read_text(encoding="utf-8"))
    pipeline = data.get("pipeline_order") or []
    union_pipe = union.get("pipeline_order") or []
    layers = data.get("layers_required") or []
    if len(layers) < LAYERS_MIN:
        print(f"FAIL: layers_required count {len(layers)} < {LAYERS_MIN}", file=sys.stderr)
        fail += 1
    if pipeline != union_pipe:
        print("FAIL: contract.pipeline_order must match agent-gate-layer-union.pipeline_order", file=sys.stderr)
        fail += 1
    deprecated = {d.get("name") for d in (data.get("layers_deprecated_skip") or []) if d.get("name")}
    for bad in ("pending_facts",):
        if bad in layers:
            print(f"FAIL: layers_required must not contain subsumed layer {bad!r}", file=sys.stderr)
            fail += 1
    for dep in deprecated:
        if dep in layers:
            print(f"FAIL: deprecated SKIP layer {dep!r} must not be in layers_required", file=sys.stderr)
            fail += 1
    if "platform_evolution_slice" in pipeline or "platform_evolution_slice" in layers:
        print("FAIL: use platform_evolution_artists_three not platform_evolution_slice", file=sys.stderr)
        fail += 1
    if data.get("entry_script") != "scripts/agent-owner-research-gate.py":
        print("FAIL: contract entry_script mismatch", file=sys.stderr)
        fail += 1
    gate = ENTRY.read_text(encoding="utf-8")
    track_names = extract_track_names(gate)
    if not track_names:
        print("FAIL: no track() layers found in agent-owner-research-gate.py", file=sys.stderr)
        fail += 1
    elif not is_subsequence_ordered(pipeline, track_names):
        print(
            "FAIL: contract.pipeline_order must contain track() names in script source order",
            file=sys.stderr,
        )
        print(f"  track order: {track_names}", file=sys.stderr)
        print(f"  pipeline:    {pipeline}", file=sys.stderr)
        fail += 1
    must_be_in_pipeline = ("ceo_six_case_battery", "ceo_manifest_slice")
    for name in must_be_in_pipeline:
        if name not in pipeline:
            print(f"FAIL: pipeline_order missing append layer {name!r}", file=sys.stderr)
            fail += 1
    try:
        bi = pipeline.index("ceo_owner_verify_bridge")
        ci = pipeline.index("owner_copy_pipeline_gate")
    except ValueError:
        print("FAIL: pipeline missing bridge or copy layer", file=sys.stderr)
        fail += 1
    else:
        if bi >= ci:
            print(
                "FAIL: ceo_owner_verify_bridge must appear before owner_copy_pipeline_gate in pipeline_order",
                file=sys.stderr,
            )
            fail += 1
    pre = (ROOT / "scripts/agent-brainstorm-preflight.py").read_text(encoding="utf-8")
    if "agent-owner-research-gate.py" not in pre:
        print("FAIL: brainstorm-preflight must invoke research-gate", file=sys.stderr)
        fail += 1
    if "agent-platform-voice-benchmark.py" not in gate:
        print("FAIL: research-gate must invoke platform-voice-benchmark", file=sys.stderr)
        fail += 1
    if "agent-owner-copy-pipeline-gate.py" not in gate:
        print("FAIL: research-gate must invoke owner-copy-pipeline-gate", file=sys.stderr)
        fail += 1
    if "agent-owner-voice-stack-gate.py" not in gate:
        print("FAIL: research-gate must invoke owner-voice-stack-gate", file=sys.stderr)
        fail += 1
    if "agent-owner-ceo-verify-bridge.py" not in gate:
        print("FAIL: research-gate must invoke owner-ceo-verify-bridge", file=sys.stderr)
        fail += 1
    vi = gate.find("agent-owner-voice-stack-gate.py")
    br = gate.find("agent-owner-ceo-verify-bridge.py")
    cp = gate.find("agent-owner-copy-pipeline-gate.py")
    if vi < 0 or cp < 0 or vi > cp:
        print("FAIL: voice-stack must run before copy-pipeline-gate", file=sys.stderr)
        fail += 1
    if br < 0 or cp < 0 or br > cp:
        print("FAIL: ceo-verify-bridge must run before copy-pipeline-gate", file=sys.stderr)
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