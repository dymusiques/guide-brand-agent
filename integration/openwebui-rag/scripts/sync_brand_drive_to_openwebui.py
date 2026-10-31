#!/usr/bin/env python3
"""
Sync a local folder (typically Google Drive for Desktop) into Open WebUI Knowledge.

Flow (鸭哥方案):
  Drive 上传 → 桌面客户端同步到本机目录 → 本脚本 manifest + sync/diff API → 自动 reindex

Run manually, via launchd (every N minutes), or watch-gdrive-sync.sh (fswatch).
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

from openwebui_sync_lib import ManifestEntry, OpenWebUIClient, cfg, load_env, run_sync

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_ENV = SCRIPT_DIR / "brand-drive-sync.env"

TEXT_SUFFIXES = {
    ".md",
    ".txt",
    ".csv",
    ".json",
    ".yaml",
    ".yml",
    ".html",
    ".htm",
}
SKIP_NAMES = {".ds_store", "desktop.ini", ".localized"}
SKIP_SUFFIXES = {".gdoc", ".gsheet", ".gslides", ".tmp", ".download"}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def build_manifest(source_root: Path, knowledge_prefix: str) -> list[ManifestEntry]:
    if not source_root.is_dir():
        raise FileNotFoundError(f"SOURCE_FOLDER not found: {source_root}")

    prefix = knowledge_prefix.strip("/")
    manifest: list[ManifestEntry] = []

    for path in sorted(source_root.rglob("*")):
        if not path.is_file():
            continue
        if path.name.lower() in SKIP_NAMES:
            continue
        if path.suffix.lower() in SKIP_SUFFIXES:
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue

        rel = path.relative_to(source_root)
        parts = rel.parts
        if len(parts) == 1:
            kb_path = prefix
            filename = parts[0]
        else:
            subdir = "/".join(parts[:-1])
            kb_path = f"{prefix}/{subdir}" if prefix else subdir
            filename = parts[-1]

        data = path.read_bytes()
        manifest.append(
            ManifestEntry(
                filename=filename,
                path=kb_path,
                checksum=sha256_file(path),
                size=len(data),
                local_file=path,
            )
        )

    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync Google Drive local folder → Open WebUI Knowledge.")
    parser.add_argument("--env", type=Path, default=DEFAULT_ENV)
    parser.add_argument("--dry-run", action="store_true", help="Only print manifest stats, no API")
    args = parser.parse_args()

    env = load_env(args.env)
    source = Path(cfg(env, "SOURCE_FOLDER")).expanduser()
    kb_name = cfg(env, "KNOWLEDGE_NAME", "brand-ip-knowledge")
    prefix = cfg(env, "KNOWLEDGE_PATH_PREFIX", "brand-drive")

    print(f"Scanning {source} …")
    manifest = build_manifest(source, prefix)
    print(f"Manifest: {len(manifest)} text file(s)")

    if args.dry_run:
        for m in manifest[:20]:
            print(f"  {m.path}/{m.filename} ({m.size} B)")
        if len(manifest) > 20:
            print(f"  … and {len(manifest) - 20} more")
        return 0

    client = OpenWebUIClient.from_env(env)
    kb_id = client.knowledge_id_by_name(kb_name)
    print(f"Syncing → Knowledge {kb_name!r} ({kb_id})")
    run_sync(client, kb_id, manifest)
    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
