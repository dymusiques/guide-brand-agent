#!/usr/bin/env python3
"""Upload every file under brand-knowledge-mirror/_rag into Open WebUI (retry, no cleanup)."""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

from openwebui_rag_paths import brand_drive_sync_env, brand_knowledge_mirror
from openwebui_sync_lib import OpenWebUIClient, cfg, load_env, run_sync
from sync_brand_drive_to_openwebui import build_manifest

DEFAULT_ENV = brand_drive_sync_env()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", type=Path, default=DEFAULT_ENV)
    parser.add_argument("--mirror", type=Path, default=None)
    parser.add_argument("--retries", type=int, default=3)
    parser.add_argument("--sleep", type=float, default=4.0)
    args = parser.parse_args()
    mirror = args.mirror or brand_knowledge_mirror()

    env = load_env(args.env)
    rag = mirror / "_rag"
    if not rag.is_dir():
        print(f"No _rag at {rag}", file=sys.stderr)
        return 2

    manifest = build_manifest(rag, cfg(env, "KNOWLEDGE_PATH_PREFIX", "brand-drive"))
    print(f"RAG manifest: {len(manifest)} file(s)")

    client = OpenWebUIClient.from_env(env)
    kb_id = client.knowledge_id_by_name(cfg(env, "KNOWLEDGE_NAME", "brand-ip-knowledge"))

    for attempt in range(1, args.retries + 1):
        print(f"=== sync attempt {attempt}/{args.retries} ===")
        try:
            run_sync(
                client,
                kb_id,
                manifest,
                continue_on_error=True,
                skip_cleanup=True,
            )
        except Exception as exc:
            print(f"attempt {attempt} error: {exc}")
        time.sleep(args.sleep)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
