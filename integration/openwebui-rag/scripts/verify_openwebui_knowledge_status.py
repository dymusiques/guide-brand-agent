#!/usr/bin/env python3
"""Report Open WebUI Knowledge file counts (brand-ip-knowledge + agent-prompt-pack)."""

from __future__ import annotations

import subprocess
import sys

CONTAINER = "open-webui"

PY = r"""
import sqlite3
c = sqlite3.connect('/app/backend/data/webui.db')
for name in (
    'brand-ip-knowledge',
    'agent-prompt-pack',
    'cursor-brand-corpus',
    'workflow-automation-pack',
):
    row = c.execute('SELECT id, description FROM knowledge WHERE name=?', (name,)).fetchone()
    if not row:
        print(name, 'MISSING', 0)
        continue
    kid, desc = row[0], (row[1] or '')[:80]
    n = c.execute('SELECT COUNT(*) FROM knowledge_file WHERE knowledge_id=?', (kid,)).fetchone()[0]
    print(name, 'OK', n, 'files', '|', desc)
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
