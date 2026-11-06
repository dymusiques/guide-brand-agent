#!/usr/bin/env python3
"""Per CEO task: screen entire Drive corpus — reference layer + hydrate priority + task folder bundle.

Must run after catalog refresh. Wired from CEO full execution / router / screen-xhs-drive-corpus.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _load_lib():
    spec = importlib.util.spec_from_file_location("ceo_corpus_screen_lib", ROOT / "scripts/ceo_corpus_screen_lib.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("ceo_corpus_screen_lib missing")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def resolve_auto_args(goal: str, brief: str) -> tuple[str, str]:
    g, b = goal.strip(), brief.strip()
    if not g:
        g = os.environ.get("CEO_GOAL", "").strip()
    if not b:
        b = os.environ.get("CEO_SIX_CASE_BRIEF", "") or os.environ.get("CEO_OWNER_EXTRA_BRIEF", "")
        b = b.strip()
    manifest = ROOT / "content/evolution/00-manager/ceo-inbox/CEO-RUN-MANIFEST-latest.json"
    if manifest.is_file():
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
            g = g or str(data.get("goal") or "")
            b = b or str(data.get("brief") or "")
        except json.JSONDecodeError:
            pass
    return g, b


def main() -> int:
    p = argparse.ArgumentParser(description="CEO task Drive corpus screen (full catalog, no silent omit)")
    p.add_argument("--goal", "-g", default="")
    p.add_argument("--brief", default="")
    p.add_argument("--catalog", type=Path, default=None)
    p.add_argument("--hydrate-limit", type=int, default=8)
    p.add_argument("--auto", action="store_true", help="Read goal/brief from env + CEO manifest")
    p.add_argument("--refresh-catalog", action="store_true", help="Run refresh-ceo-drive-catalog.py first")
    p.add_argument("--json", action="store_true", help="Print summary JSON to stdout")
    args = p.parse_args()

    if args.refresh_catalog:
        import subprocess

        py = sys.executable
        subprocess.run([py, str(ROOT / "scripts/refresh-ceo-drive-catalog.py")], cwd=ROOT, check=False)

    goal, brief = (resolve_auto_args(args.goal, args.brief) if args.auto else (args.goal.strip(), args.brief.strip()))
    if not goal:
        print("empty goal — pass --goal or --auto with CEO_GOAL", file=sys.stderr)
        return 2

    lib = _load_lib()
    try:
        payload = lib.comprehensive_screen(
            goal,
            brief=brief,
            catalog_path=args.catalog,
            hydrate_limit=max(1, args.hydrate_limit),
        )
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    task_dir = lib.write_task_bundle(payload)
    lib.sync_legacy_outputs(payload, task_dir)
    legacy_path = lib.LEGACY_OUT_JSON
    legacy = json.loads(legacy_path.read_text(encoding="utf-8"))
    bound = lib.bind_brief_drive_screen(brief, legacy)

    summary = {
        "slug": payload["slug"],
        "task_dir": str(task_dir.relative_to(ROOT)),
        "reference_count": payload["counts"]["reference"],
        "hydrate_priority": payload["counts"]["hydrate_priority"],
        "catalog_files": payload["catalog_file_count"],
        "bound_brief": str(bound.relative_to(ROOT)) if bound else "",
        "index_md": str((task_dir / "INDEX.md").relative_to(ROOT)),
    }
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(summary, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
