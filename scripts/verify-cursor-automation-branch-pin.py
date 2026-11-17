#!/usr/bin/env python3
"""FAIL if brand repo not on main or ahead/behind remotes (Automation 旧分支防护)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PIN = ROOT / "integration/handoff/cursor-automation-branch-pin.json"
FORBID_REMOTE_BRANCH_PREFIXES = ("cursor/",)


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
    for remote in ("github", "origin"):
        lines = run(["git", "branch", "-r", "--list", f"{remote}/*"]).splitlines()
        for line in lines:
            if "->" in line:
                continue
            ref = line.strip().split()[0]
            if ref.endswith("/HEAD"):
                continue
            if not ref.startswith(f"{remote}/"):
                continue
            b = ref[len(remote) + 1 :]
            if b == "main":
                continue
            if any(b.startswith(p) for p in FORBID_REMOTE_BRANCH_PREFIXES):
                errs.append(f"远程多余分支 {remote}/{b}（Automation 只看 main · 请删除）")
            else:
                errs.append(f"远程非 main 分支 {remote}/{b}（易混淆 · 删除或合并后只留 main）")
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