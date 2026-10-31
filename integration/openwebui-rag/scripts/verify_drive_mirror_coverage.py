#!/usr/bin/env python3
"""Compare Drive inventory → local mirror → Open WebUI knowledge_file counts."""

from __future__ import annotations

import json
import sqlite3
import subprocess
import sys
from pathlib import Path

from openwebui_rag_paths import brand_knowledge_mirror

SCRIPT_DIR = Path(__file__).resolve().parent
_LEGACY_INV = Path(
    "/Users/danying/Desktop/未命名/LLM-Ollama/RAG/RAG/scripts/state/drive-inventory.json"
)
INVENTORY = SCRIPT_DIR / "state" / "drive-inventory.json"
if not INVENTORY.is_file() and _LEGACY_INV.is_file():
    INVENTORY = _LEGACY_INV
MIRROR = brand_knowledge_mirror()
KB_NAME = "brand-ip-knowledge"


def main() -> int:
    if not INVENTORY.is_file():
        print("No drive-inventory.json — run brand_knowledge_watch --scan first")
        return 2

    inv = json.loads(INVENTORY.read_text(encoding="utf-8"))
    drive_n = inv.get("file_count") or len(inv.get("files") or {})

    orig_n = sum(1 for _ in (MIRROR / "_originals").rglob("*") if _.is_file()) if (MIRROR / "_originals").is_dir() else 0
    rag_n = sum(1 for _ in (MIRROR / "_rag").rglob("*.md") if _.is_file()) if (MIRROR / "_rag").is_dir() else 0

    proc = subprocess.run(
        [
            "docker",
            "exec",
            "open-webui",
            "python3",
            "-c",
            f"import sqlite3;c=sqlite3.connect('/app/backend/data/webui.db');"
            f"k=c.execute('SELECT id FROM knowledge WHERE name=?',('{KB_NAME}',)).fetchone();"
            f"print(c.execute('SELECT COUNT(*) FROM knowledge_file WHERE knowledge_id=?',(k[0],)).fetchone()[0] if k else 0)",
        ],
        capture_output=True,
        text=True,
    )
    kb_n = int(proc.stdout.strip() or "0")

    print(f"Drive inventory (metadata): {drive_n}")
    print(f"Local _originals files:     {orig_n}")
    print(f"Local _rag .md:             {rag_n}")
    print(f"Open WebUI {KB_NAME}:      {kb_n}")

    if orig_n < drive_n * 0.9:
        print("NOTE: mirror still catching up (originals < 90% of inventory)")
        return 1
    if kb_n < rag_n * 0.5:
        print("NOTE: many _rag files not yet indexed in Open WebUI — re-run sync_all_brand_rag_to_openwebui.py")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
