#!/usr/bin/env python3
"""Sync cursor-brand-corpus mirror (L1 primary + MASTER index) → Open WebUI Knowledge."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from openwebui_rag_paths import REPO_ROOT, brand_drive_sync_env, rag_subdir
from openwebui_sync_lib import ManifestEntry, OpenWebUIClient, load_env, run_sync
from sync_brand_drive_to_openwebui import build_manifest, sha256_file

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_ENV = brand_drive_sync_env()
KB_NAME = "cursor-brand-corpus"
REORG = REPO_ROOT / "scripts/reorganize-brand-corpus-l012.py"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", type=Path, default=DEFAULT_ENV)
    parser.add_argument("--tier", choices=("l1", "all"), default="l1")
    args = parser.parse_args()

    if REORG.is_file():
        subprocess.run([sys.executable, str(REORG)], check=False)

    corpus = rag_subdir("cursor-brand-corpus")
    if not corpus.is_dir():
        print(f"Missing {corpus}", file=sys.stderr)
        return 2

    manifest_entries: list = []
    if args.tier == "l1":
        manifest_entries.extend(build_manifest(corpus / "l1", "corpus-l1"))
        master = corpus / "MASTER-L0-INDEX.md"
        if master.is_file():
            data = master.read_bytes()
            manifest_entries.append(
                ManifestEntry(
                    filename=master.name,
                    path="corpus-index",
                    checksum=sha256_file(master),
                    size=len(data),
                    local_file=master,
                )
            )
    else:
        for sub, prefix in (("l0", "corpus-l0"), ("l1", "corpus-l1"), ("l2", "corpus-l2")):
            d = corpus / sub
            if d.is_dir():
                manifest_entries.extend(build_manifest(d, prefix))
        if (corpus / "MASTER-L0-INDEX.md").is_file():
            manifest_entries.extend(build_manifest(corpus, "corpus-index"))

    seen: set[tuple[str, str]] = set()
    manifest = []
    for e in manifest_entries:
        key = (e.path, e.filename)
        if key in seen:
            continue
        seen.add(key)
        manifest.append(e)

    print(f"cursor-brand-corpus manifest: {len(manifest)} file(s) (tier={args.tier})")

    env = load_env(args.env)
    client = OpenWebUIClient.from_env(env)
    kb_id = client.knowledge_id_by_name(KB_NAME)
    run_sync(client, kb_id, manifest, continue_on_error=True, skip_cleanup=False)
    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
