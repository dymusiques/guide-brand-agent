#!/usr/bin/env python3
"""FAIL if brand repo not on main or ahead/behind remotes (Automation 旧分支防护)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PIN = ROOT / "integration/handoff/cursor-automation-branch-pin.json"


def run(cmd: list[str]) -> str:
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    return (r.stdout or r.stderr or "").strip()


def main() -> int:
    errs: list[str] = []
    branch = run(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    if branch != "main":
        errs.append(f"本地分支是 {branch}，Must 为 main")
    for remote in ("github", "origin"):
        line = run(["git", "rev-parse", f"{remote}/main"])
        if not line or "fatal" in line:
            errs.append(f"缺少 remote/{remote}/main")
            continue
        ahead = run(["git", "rev-list", "--count", f"{remote}/main..HEAD"])
        behind = run(["git", "rev-list", "--count", f"HEAD..{remote}/main"])
        if behind and behind != "0":
            errs.append(f"落后 {remote}/main {behind} commits — git pull {remote} main")
        if ahead and ahead != "0":
            errs.append(f"领先 {remote}/main {ahead} commits（Automation 云端用 remote · 请 push）")
    head = run(["git", "rev-parse", "--short", "HEAD"])
    if errs:
        print("FAIL cursor-automation-branch-pin:\n- " + "\n- ".join(errs), file=sys.stderr)
        return 1
    pin = json.loads(PIN.read_text(encoding="utf-8"))
    print(
        json.dumps(
            {
                "status": "PASS",
                "branch": branch,
                "head": head,
                "canonical": pin["canonical"],
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())