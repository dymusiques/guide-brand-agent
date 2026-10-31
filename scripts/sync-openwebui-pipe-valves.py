#!/usr/bin/env python3
"""Sync yage Pipe Valves from Open WebUI OpenRouter connection (index 0).

Never reads CEO brand-agent GEMINI_API_KEY — upstream billing key comes only
from Open WebUI Admin Connections (Docker sqlite). brand-drive-sync.env may
set OPENWEBUI_PIPE_UPSTREAM_MODEL (model slug only).
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

PIPE_IDS = ("yage_cot", "yage_long_context")
DOCKER_CONTAINER = os.environ.get("OPENWEBUI_DOCKER", "open-webui")
DB_PATH = "/app/backend/data/webui.db"

ROOT = Path(__file__).resolve().parents[1]
ENV_FILE = Path(
    os.environ.get(
        "BRAND_DRIVE_SYNC_ENV",
        str(Path(__file__).resolve().parent.parent / "integration/openwebui-rag/scripts/brand-drive-sync.env"),
    )
)


def load_env(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    if not path.is_file():
        return out
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        out[k.strip()] = v.strip()
    return out


def docker_python(code: str) -> str:
    proc = subprocess.run(
        ["docker", "exec", DOCKER_CONTAINER, "python3", "-c", code],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or "docker exec failed")
    return proc.stdout.strip()


def main() -> int:
    env = load_env(ENV_FILE)
    # Long-form pipes: prefer dedicated OpenRouter GPT slug; do not fall back to CEO Gemini.
    model = (
        env.get("OPENWEBUI_PIPE_UPSTREAM_MODEL")
        or env.get("OPENWEBUI_PIPE_MODEL")
        or "deepseek/deepseek-v4.1-flash-1017"
    )

    code = r"""
import json, sqlite3
c = sqlite3.connect(%r)
def cfg(key):
    row = c.execute('SELECT value FROM config WHERE key=?', (key,)).fetchone()
    return row[0] if row else None
urls = json.loads(cfg('openai.api_base_urls') or '[]')
keys = json.loads(cfg('openai.api_keys') or '[]')
configs = json.loads(cfg('openai.api_configs') or '{}')
idx = None
for i, u in enumerate(urls):
    cc = configs.get(str(i), configs.get(i, {}))
    if isinstance(cc, dict) and cc.get('enable'):
        idx = i
        break
if idx is None:
    raise SystemExit('no enabled OpenAI-compatible connection')
base = urls[idx]
key = keys[idx] if idx < len(keys) else ''
if not key or key.startswith('Put your'):
    raise SystemExit('connection api key missing')
print(json.dumps({'base_url': base, 'api_key': key, 'my_model_id': %r}))
""" % (
        DB_PATH,
        model,
    )

    line = docker_python(code)
    conn = json.loads(line)
    base_url = conn["base_url"]
    api_key = conn["api_key"]

    for fid in PIPE_IDS:
        row = docker_python(
            f"""
import sqlite3, json
c=sqlite3.connect({DB_PATH!r})
r=c.execute('SELECT valves FROM function WHERE id=?', ({fid!r},)).fetchone()
v=json.loads(r[0]) if r and r[0] else {{}}
print(json.dumps(v))
"""
        )
        valves = json.loads(row) if row else {}
        valves["base_url"] = base_url
        valves["api_key"] = api_key
        valves["my_model_id"] = model
        payload = json.dumps(valves)
        docker_python(
            f"""
import sqlite3, json
c=sqlite3.connect({DB_PATH!r})
c.execute('UPDATE function SET valves=? WHERE id=?', ({payload!r}, {fid!r}))
c.commit()
print('ok')
"""
        )

    print(f"Synced {', '.join(PIPE_IDS)} → {base_url} model={model}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        raise SystemExit(1)
