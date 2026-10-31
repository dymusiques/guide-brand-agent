#!/usr/bin/env python3
"""One-shot Open WebUI setup: brand-ip-knowledge + enable API keys + create key."""

from __future__ import annotations

import json
import subprocess
import sys
import time
import uuid
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ENV_PATH = SCRIPT_DIR / "brand-drive-sync.env"
CONTAINER = "open-webui"
KB_NAME = "brand-ip-knowledge"
KB_DESC = (
    "品牌/IP/策划/视觉背书库：Google Drive 镜像 → RAG。"
    "Embedding Ollama bge-m3；由 sync_brand_drive_to_openwebui.py 维护。"
)


PY = r"""
import sqlite3, json, time, uuid, sys

DB = "/app/backend/data/webui.db"
KB_NAME = {kb_name!r}
KB_DESC = {kb_desc!r}

c = sqlite3.connect(DB)
user = c.execute("SELECT id FROM user WHERE role='admin' LIMIT 1").fetchone()
if not user:
    print("ERROR: no admin user", file=sys.stderr)
    sys.exit(1)
uid = user[0]

# enable API keys
rows = list(c.execute("SELECT key,value FROM config WHERE key='auth.enable_api_keys'"))
if rows:
    c.execute("UPDATE config SET value='true' WHERE key='auth.enable_api_keys'")
else:
    c.execute("INSERT INTO config (key,value) VALUES ('auth.enable_api_keys','true')")

# knowledge
row = c.execute("SELECT id FROM knowledge WHERE name=?", (KB_NAME,)).fetchone()
now = int(time.time())
if not row:
    kid = str(uuid.uuid4())
    c.execute(
        "INSERT INTO knowledge (id,user_id,name,description,meta,created_at,updated_at,data) VALUES (?,?,?,?,?,?,?,?)",
        (kid, uid, KB_NAME, KB_DESC, "null", now, now, None),
    )
    print("KNOWLEDGE_CREATED", kid)
else:
    print("KNOWLEDGE_EXISTS", row[0])

# api key
existing = c.execute(
    "SELECT key FROM api_key WHERE user_id=? ORDER BY created_at DESC LIMIT 1", (uid,)
).fetchone()
if existing:
    print("API_KEY", existing[0])
else:
    key = "sk-" + uuid.uuid4().hex
    aid = str(uuid.uuid4())
    c.execute(
        "INSERT INTO api_key (id,user_id,key,data,expires_at,last_used_at,created_at,updated_at) VALUES (?,?,?,?,?,?,?,?)",
        (aid, uid, key, "null", None, None, now, now),
    )
    print("API_KEY", key)

c.commit()
"""


def main() -> int:
    code = PY.format(kb_name=KB_NAME, kb_desc=KB_DESC)
    proc = subprocess.run(
        ["docker", "exec", CONTAINER, "python3", "-c", code],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        print(proc.stderr or proc.stdout, file=sys.stderr)
        return proc.returncode

    api_key = None
    for line in proc.stdout.splitlines():
        print(line)
        if line.startswith("API_KEY "):
            api_key = line.split(" ", 1)[1].strip()

    if not api_key:
        print("Could not parse API key from setup output", file=sys.stderr)
        return 1

    lines = []
    if ENV_PATH.is_file():
        lines = ENV_PATH.read_text(encoding="utf-8").splitlines()

    def set_kv(key: str, val: str) -> None:
        nonlocal lines
        prefix = key + "="
        found = False
        for i, ln in enumerate(lines):
            if ln.startswith(prefix):
                lines[i] = prefix + val
                found = True
        if not found:
            lines.append(prefix + val)

    set_kv("OPENWEBUI_BASE_URL", "http://127.0.0.1:3000")
    set_kv("KNOWLEDGE_NAME", KB_NAME)
    set_kv("OPENWEBUI_API_KEY", api_key)
    set_kv("OPENWEBUI_RAG_MODEL", "google/gemini-3.1-flash-lite")
    set_kv("KNOWLEDGE_PATH_PREFIX", "brand-drive")

    ENV_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {ENV_PATH} (OPENWEBUI_API_KEY set; file is gitignored)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
