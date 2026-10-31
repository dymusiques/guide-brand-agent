#!/usr/bin/env python3
"""
Run automatable workflow layers from integration/handoff/workflow-automation-manifest.json.

Examples:
  python3 scripts/run-workflow-from-manifest.py --list-layers
  python3 scripts/run-workflow-from-manifest.py --layer L2_CEO_START --goal "本周长文"
  python3 scripts/run-workflow-from-manifest.py --phrase "CEO 开始执行" --goal "..."
  python3 scripts/run-workflow-from-manifest.py --layer L3_BRIEF_GATE --brief content/xiaohongshu/foo-brief.md
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "integration/handoff/workflow-automation-manifest.json"


def load_manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def find_layer(manifest: dict, layer_id: str) -> dict | None:
    for layer in manifest.get("layers", []):
        if layer.get("id") == layer_id:
            return layer
    return None


def find_layer_by_phrase(manifest: dict, phrase: str) -> dict | None:
    p = phrase.strip()
    for layer in manifest.get("layers", []):
        for op in layer.get("owner_phrases") or []:
            if op in p or p in op:
                return layer
    return None


def expand_cmd(template: str, goal: str, brief: str) -> str:
    cmd = template.replace("<owner goal>", goal).replace("<path>", brief)
    cmd = cmd.replace("<owner goal>", goal)
    if brief:
        cmd = cmd.replace("<path>", brief).replace("<brief>", brief)
    return cmd


def run_shell(cmd: str, *, dry_run: bool) -> None:
    cmd = re.sub(r"\s+", " ", cmd.strip())
    print("+", cmd, flush=True)
    if dry_run:
        return
    subprocess.run(cmd, shell=True, cwd=ROOT, check=True)


def run_layer(layer: dict, *, goal: str, brief: str, dry_run: bool) -> int:
    lid = layer.get("id", "")
    recover = layer.get("recover") or layer.get("recover_first")
    if recover:
        run_shell(recover if recover.startswith("bash") else f"bash {recover}", dry_run=dry_run)

    ow = layer.get("openwebui_router") or {}
    if ow.get("must_before_manager_step_0") and goal:
        tpl = ow.get("script", "")
        if tpl:
            run_shell(expand_cmd(tpl, goal, brief), dry_run=dry_run)

    script = layer.get("script")
    if script:
        run_shell(expand_cmd(script, goal, brief), dry_run=dry_run)
        return 0

    if lid == "L3_BRIEF_GATE":
        if not brief:
            print("L3_BRIEF_GATE requires --brief", file=sys.stderr)
            return 2
        run_shell(
            f"bash scripts/manager-brief-evolution-until-gap.sh --brief {brief}",
            dry_run=dry_run,
        )
        return 0

    for s in layer.get("scripts") or []:
        run_shell(expand_cmd(s, goal, brief), dry_run=dry_run)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--list-layers", action="store_true")
    ap.add_argument("--layer", default="")
    ap.add_argument("--phrase", default="")
    ap.add_argument("--goal", "-g", default="")
    ap.add_argument("--brief", default="")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--context-reorg", action="store_true", help="Run Open WebUI context + workflow pack sync")
    args = ap.parse_args()

    if args.context_reorg:
        run_shell("bash scripts/run-context-reorg-pipeline.sh", dry_run=args.dry_run)
        run_shell("python3 scripts/build-workflow-automation-catalog.py", dry_run=args.dry_run)
        rag = "/Users/danying/Desktop/未命名/LLM-Ollama/RAG/RAG/scripts/sync_workflow_automation_pack_to_openwebui.py"
        run_shell(f"python3 {rag}", dry_run=args.dry_run)
        return 0

    manifest = load_manifest()
    if args.list_layers:
        for layer in manifest.get("layers", []):
            phrases = ", ".join(layer.get("owner_phrases") or [])[:80]
            print(layer.get("id"), "—", layer.get("name"), "|", phrases)
        return 0

    layer = None
    if args.layer:
        layer = find_layer(manifest, args.layer)
        if not layer:
            print(f"Unknown layer {args.layer}", file=sys.stderr)
            return 2
    elif args.phrase:
        layer = find_layer_by_phrase(manifest, args.phrase)
        if not layer:
            print(f"No layer matched phrase: {args.phrase}", file=sys.stderr)
            return 2
    else:
        ap.print_help()
        return 2

    return run_layer(layer, goal=args.goal, brief=args.brief, dry_run=args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
