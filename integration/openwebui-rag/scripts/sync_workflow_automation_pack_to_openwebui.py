#!/usr/bin/env python3
"""Sync workflow-automation-pack mirror → Open WebUI Knowledge."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from openwebui_rag_paths import REPO_ROOT, brand_drive_sync_env, rag_subdir
from openwebui_sync_lib import OpenWebUIClient, load_env, run_sync
from sync_brand_drive_to_openwebui import build_manifest

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_ENV = brand_drive_sync_env()
KB_NAME = "workflow-automation-pack"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", type=Path, default=DEFAULT_ENV)
    args = parser.parse_args()

    export = REPO_ROOT / "scripts/export-workflow-automation-pack.sh"
    if export.is_file():
        subprocess.run(["bash", str(export)], check=False)

    pack = rag_subdir("workflow-automation-pack")
    if not pack.is_dir():
        print(f"Missing {pack}", file=sys.stderr)
        return 2

    manifest = build_manifest(pack, "workflows")
    print(f"workflow-automation-pack manifest: {len(manifest)} file(s)")

    env = load_env(args.env)
    client = OpenWebUIClient.from_env(env)
    kb_id = client.knowledge_id_by_name(KB_NAME)
    run_sync(client, kb_id, manifest, continue_on_error=True, skip_cleanup=False)
    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
