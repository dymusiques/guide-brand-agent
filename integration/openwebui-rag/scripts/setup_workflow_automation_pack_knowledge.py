#!/usr/bin/env python3
"""Create Open WebUI Knowledge: workflow-automation-pack."""

from __future__ import annotations

import subprocess
import sys

CONTAINER = "open-webui"
KB_NAME = "workflow-automation-pack"
KB_DESC = (
    "可自动化 workflow：manifest 层级 L0–L4、gate/CEO/campaign 命令、Open WebUI 步 −1。"
    "build-workflow-automation-catalog.py + sync_workflow_automation_pack_to_openwebui.py"
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
