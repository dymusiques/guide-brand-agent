#!/usr/bin/env python3
"""Create Open WebUI Knowledge collection: agent-prompt-pack (SOP / INTEGRATION prompts only)."""

from __future__ import annotations

import subprocess
import sys

CONTAINER = "open-webui"
KB_NAME = "agent-prompt-pack"
KB_DESC = (
    "Agent SOP：PROMPT-CONTEXT-STANDARD、各部门 INTEGRATION-PROMPT、Cursor↔Open WebUI 路由。"
    "由 export-agent-prompt-pack.sh + sync_agent_prompt_pack_to_openwebui.py 维护。"
)

PY = """
import sqlite3, time, uuid, sys
DB = "/app/backend/data/webui.db"
KB_NAME = {kb_name!r}
KB_DESC = {kb_desc!r}
c = sqlite3.connect(DB)
user = c.execute("SELECT id FROM user WHERE role='admin' LIMIT 1").fetchone()
if not user:
    sys.exit("no admin user")
uid = user[0]
row = c.execute("SELECT id FROM knowledge WHERE name=?", (KB_NAME,)).fetchone()
now = int(time.time())
if not row:
    kid = str(uuid.uuid4())
    c.execute(
        "INSERT INTO knowledge (id,user_id,name,description,meta,created_at,updated_at,data) VALUES (?,?,?,?,?,?,?,?)",
        (kid, uid, KB_NAME, KB_DESC, "null", now, now, None),
    )
    c.commit()
    print("CREATED", kid)
else:
    print("EXISTS", row[0])
"""


def main() -> int:
    code = PY.format(kb_name=KB_NAME, kb_desc=KB_DESC)
    proc = subprocess.run(
        ["docker", "exec", CONTAINER, "python3", "-c", code],
        capture_output=True,
        text=True,
    )
    print(proc.stdout.strip())
    if proc.returncode != 0:
        print(proc.stderr, file=sys.stderr)
        return proc.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
