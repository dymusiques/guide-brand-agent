#!/usr/bin/env python3
"""Sync brand-knowledge-mirror/_rag/agent-prompt-pack → Open WebUI Knowledge agent-prompt-pack."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from openwebui_rag_paths import REPO_ROOT, brand_drive_sync_env, rag_subdir
from openwebui_sync_lib import OpenWebUIClient, load_env, run_sync
from sync_brand_drive_to_openwebui import build_manifest

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_ENV = brand_drive_sync_env()
KB_NAME = "agent-prompt-pack"
PREFIX = "agent-prompts"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", type=Path, default=DEFAULT_ENV)
    args = parser.parse_args()

    brand_root = REPO_ROOT
    export_sh = brand_root / "scripts/export-agent-prompt-pack.sh"
    if export_sh.is_file():
        import subprocess

        subprocess.run(["bash", str(export_sh)], check=False)

    pack = rag_subdir("agent-prompt-pack")
    if not pack.is_dir():
        print(f"Missing {pack} — run export-agent-prompt-pack.sh first", file=sys.stderr)
        return 2

    manifest = build_manifest(pack, PREFIX)
    print(f"agent-prompt-pack manifest: {len(manifest)} file(s)")

    env = load_env(args.env)
    client = OpenWebUIClient.from_env(env)
    kb_id = client.knowledge_id_by_name(KB_NAME)
    run_sync(client, kb_id, manifest, continue_on_error=True, skip_cleanup=False)
    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
