#!/usr/bin/env python3
"""
MVP: Orchestrate Brand/IP weekly flow (course practice — full automation entry).

Does NOT replace ceo-full-execution-pipeline.sh. Calls existing scripts:
  sync-openwebui-pipe-valves → optional Drive sync → Open WebUI router → optional CEO pipeline.

Usage:
  python3 scripts/automation/brand_ip_weekly_pipeline.py --goal "本周 IP 深度长文提纲" [--run-ceo]
  python3 scripts/automation/brand_ip_weekly_pipeline.py --goal "..." --dry-run
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAG_SCRIPTS = Path(
    "/Users/danying/Desktop/未命名/LLM-Ollama/RAG/RAG/scripts"
)


def run(cmd: list[str], *, cwd: Path | None = None) -> None:
    print("+", " ".join(cmd), flush=True)
    subprocess.run(cmd, cwd=cwd or ROOT, check=True)


def main() -> int:
    p = argparse.ArgumentParser(description="Brand IP weekly automation MVP")
    p.add_argument("--goal", "-g", required=True, help="Owner goal (same as CEO --goal)")
    p.add_argument("--brief", default="", help="Optional brief path")
    p.add_argument("--dry-run", action="store_true", help="Router only, no Open WebUI HTTP")
    p.add_argument("--skip-drive", action="store_true", help="Skip Drive→Knowledge sync")
    p.add_argument("--run-ceo", action="store_true", help="After router, run ceo-full-execution-pipeline.sh")
    p.add_argument(
        "--workflow-layer",
        default="",
        help="After router, run manifest layer e.g. L2_CEO_START (requires --run-ceo or runs layer only if --skip-router)",
    )
    p.add_argument(
        "--skip-router",
        action="store_true",
        help="Skip Open WebUI HTTP; only workflow layer / CEO",
    )
    p.add_argument(
        "--context-reorg",
        action="store_true",
        help="Refresh Open WebUI Knowledge (context + workflow packs)",
    )
    args = p.parse_args()

    if args.context_reorg:
        run(["bash", str(ROOT / "scripts/run-context-reorg-pipeline.sh")])
        return 0

    run([sys.executable, str(ROOT / "scripts/sync-openwebui-pipe-valves.py")])

    if not args.skip_drive:
        sync_py = RAG_SCRIPTS / "sync_brand_drive_to_openwebui.py"
        if sync_py.is_file():
            run([sys.executable, str(sync_py)], cwd=RAG_SCRIPTS)
        else:
            print("WARN: no sync_brand_drive_to_openwebui.py — skip Drive sync", file=sys.stderr)

    router = [sys.executable, str(ROOT / "scripts/route-openwebui-for-goal.py"), "--goal", args.goal]
    if args.brief:
        router.extend(["--brief", args.brief])
    router.append("--json")
    out = subprocess.check_output(router, cwd=ROOT, text=True)
    route = json.loads(out)
    print(json.dumps(route, indent=2, ensure_ascii=False))

    if args.skip_router:
        print("skip-router: no Open WebUI HTTP", flush=True)
    elif args.dry_run or route.get("route") == "SKIP":
        print("Router SKIP or dry-run — stop before Open WebUI HTTP.", flush=True)
    else:
        cmd = ["bash", str(ROOT / "scripts/run-openwebui-router-pipeline.sh"), "--goal", args.goal]
        if args.brief:
            cmd.extend(["--brief", args.brief])
        run(cmd)

    if args.workflow_layer:
        wf = [
            sys.executable,
            str(ROOT / "scripts/run-workflow-from-manifest.py"),
            "--layer",
            args.workflow_layer,
            "--goal",
            args.goal,
        ]
        if args.brief:
            wf.extend(["--brief", args.brief])
        run(wf)
    elif args.run_ceo:
        ceo = ["bash", str(ROOT / "scripts/ceo-full-execution-pipeline.sh"), "--goal", args.goal]
        if args.brief:
            ceo.extend(["--brief", args.brief])
        run(ceo)

    print("brand_ip_weekly_pipeline: done", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
