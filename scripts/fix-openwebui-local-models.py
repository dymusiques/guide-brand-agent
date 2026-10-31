#!/usr/bin/env python3
"""
Open WebUI: production-local setup (course *method*, not WBR homework artifacts).

Run inside container via deploy-learning-stack.sh:
  - Keeps SQLite Access Agent (yage_sqlite) — configure Valve in UI for YOUR .db
  - Adds workspace model local-llama3.2-3b (no pre-bound course events.db)
  - Deactivates homework model wbr-llama3.2-3b if present

Optional course demo (events.db): pass --course-demo to also run WBR folder script logic.
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
import time

DB = "/app/backend/data/webui.db"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--course-demo",
        action="store_true",
        help="Download yage events.db and enable wbr-llama3.2-3b (homework only)",
    )
    args = p.parse_args()

    if args.course_demo:
        import runpy

        runpy.run_path("/tmp/fix-openwebui-wbr-sqlite.py", run_name="__main__")
        return 0

    c = sqlite3.connect(DB)
    now = int(time.time())
    user_row = c.execute("SELECT user_id FROM model LIMIT 1").fetchone()
    if not user_row:
        print("no user_id in model table", file=sys.stderr)
        return 1
    user_id = user_row[0]

    row = c.execute('SELECT valves FROM tool WHERE id="yage_sqlite"').fetchone()
    current = json.loads(row[0]) if row and row[0] else {}
    course_marker = "yage.ai/genai/example1" in (current.get("db_url") or "")
    if current.get("db_local_path") and not course_marker:
        print("yage_sqlite valves unchanged (custom):", json.dumps(current)[:120])
    else:
        default_valves = json.dumps(
            {
                "db_url": "",
                "db_local_path": "/app/backend/data/local/private.db",
            }
        )
        c.execute(
            'UPDATE tool SET valves=?, updated_at=? WHERE id="yage_sqlite"',
            (default_valves, now),
        )
        print("yage_sqlite valves → local/private.db placeholder (cleared course events.db if any)")

    model_id = "local-llama3.2-3b"
    params = {
        "system": (
            "你是本地数据分析助手。涉及库表或 SQL 时，必须先调用 SQLite Access Agent 的工具，"
            "并以工具返回为准；禁止臆造表名或未执行的 Python。"
        ),
        "function_calling": "native",
    }
    meta = {
        "profile_image_url": "/static/favicon.png",
        "description": "本地 llama3.2:3b — 聊天时按需启用 SQLite Tool（自配数据库路径）",
        "capabilities": {"builtin_tools": False},
        "toolIds": [],
        "tags": ["local", "brand-stack"],
    }

    if c.execute("SELECT id FROM model WHERE id=?", (model_id,)).fetchone():
        c.execute(
            "UPDATE model SET base_model_id=?, name=?, params=?, meta=?, updated_at=?, is_active=1 WHERE id=?",
            (
                "llama3.2:3b",
                "Local · llama3.2:3b",
                json.dumps(params),
                json.dumps(meta),
                now,
                model_id,
            ),
        )
    else:
        c.execute(
            "INSERT INTO model (id, user_id, base_model_id, name, params, meta, updated_at, created_at, is_active) "
            "VALUES (?,?,?,?,?,?,?,?,1)",
            (
                model_id,
                user_id,
                "llama3.2:3b",
                "Local · llama3.2:3b",
                json.dumps(params),
                json.dumps(meta),
                now,
                now,
            ),
        )

    c.execute("UPDATE model SET is_active=0 WHERE id=?", ("wbr-llama3.2-3b",))
    c.commit()
    print("model", model_id, "ok; wbr-llama3.2-3b deactivated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
