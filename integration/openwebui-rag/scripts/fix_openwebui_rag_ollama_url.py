#!/usr/bin/env python3
"""Point Open WebUI RAG embedding Ollama at host.docker.internal (Docker Desktop on macOS)."""

from __future__ import annotations

import subprocess
import sys

CONTAINER = "open-webui"
TARGET = "http://host.docker.internal:11434"

PY = f"""
import sqlite3, time
c = sqlite3.connect("/app/backend/data/webui.db")
now = int(time.time())
c.execute(
    "UPDATE config SET value=?, updated_at=? WHERE key=?",
    ('"{TARGET}"', now, "rag.ollama.base_url"),
)
c.commit()
print("rag.ollama.base_url ->", {TARGET!r}, "rows", c.total_changes)
"""


def main() -> int:
    proc = subprocess.run(
        ["docker", "exec", CONTAINER, "python3", "-c", PY],
        capture_output=True,
        text=True,
    )
    print(proc.stdout.strip())
    if proc.returncode != 0:
        print(proc.stderr, file=sys.stderr)
        return proc.returncode
    test = subprocess.run(
        [
            "docker",
            "exec",
            CONTAINER,
            "curl",
            "-sf",
            f"{TARGET}/api/tags",
        ],
        capture_output=True,
        text=True,
    )
    if test.returncode != 0:
        print("WARN: container cannot reach Ollama at", TARGET, file=sys.stderr)
        return 1
    print("Ollama reachable from container.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
