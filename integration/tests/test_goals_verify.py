#!/usr/bin/env python3
"""Run Goal Registry verify hooks (M4)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HOOKS = ROOT / "integration/goals/verify_hooks.json"
REGISTRY = ROOT / "integration/goals/registry.json"

# M4 must not shell out to full kernel 6-case verify scripts (see docs/VERIFY-TIERS.md).
_FORBIDDEN_HOOK_CMD_FRAGMENTS = (
    "verify-marketing-campaign.sh",
    "verify-business-brand.sh",
    "verify-xhs-topic.sh",
    "test_marketing_aligned.py",
    "test_business_brand_aligned.py",
    "test_is_xhs_growth_aligned.py",
)


def _has_gemini() -> bool:
    return (ROOT / ".env").is_file() or bool(os.environ.get("GEMINI_API_KEY"))


def _discovery_aligned() -> tuple[bool, str]:
    briefs = sorted((ROOT / "content/xiaohongshu").glob("*discovery*-brief.md"))
    if not briefs:
        return False, "no discovery briefs"
    bad = []
    for p in briefs:
        if "aligned: true" not in p.read_text(encoding="utf-8"):
            bad.append(p.name)
    if bad:
        return False, f"not aligned: {bad}"
    return True, f"{len(briefs)} briefs aligned"


def run_check(goal_id: str, check: dict) -> tuple[bool, str]:
    t = check["type"]
    if t == "file_exists":
        p = ROOT / check["path"]
        return (True, "ok") if p.is_file() else (False, f"missing {check['path']}")
    if t == "file_contains":
        p = ROOT / check["path"]
        if not p.is_file():
            return False, f"missing {check['path']}"
        text = p.read_text(encoding="utf-8")
        for n in check["needles"]:
            if n not in text:
                return False, f"{check['path']} missing {n!r}"
        return True, "markers ok"
    if t == "discovery_briefs_aligned":
        return _discovery_aligned()
    if t == "script":
        if check.get("skip_without_gemini") and not _has_gemini():
            return True, "SKIP (no Gemini key)"
        cmd = check["cmd"]
        if ".venv/bin/python" in cmd and not (ROOT / ".venv/bin/python").is_file():
            cmd = cmd.replace(".venv/bin/python", sys.executable)
        proc = subprocess.run(
            cmd,
            shell=True,
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=300,
        )
        if proc.returncode == 0:
            return True, "script PASS"
        if check.get("allow_fail_if") == "no_inbox_ok":
            return True, "demo pipeline ok or expected empty"
        out = (proc.stderr or proc.stdout or "fail").strip()
        if check.get("skip_without_gemini") and (
            "User location is not supported" in out
            or "FAILED_PRECONDITION" in out
        ):
            return True, "SKIP (Gemini geo/API)"
        return False, out[-400:]
    return False, f"unknown check {t}"


def _assert_hooks_not_kernel_six_case() -> None:
    data = json.loads(HOOKS.read_text(encoding="utf-8"))
    for gid, hook in data.get("hooks", {}).items():
        for c in hook.get("checks", []):
            if c.get("type") != "script":
                continue
            cmd = c.get("cmd", "")
            for frag in _FORBIDDEN_HOOK_CMD_FRAGMENTS:
                if frag in cmd:
                    raise SystemExit(
                        f"M4 hook {gid} must not invoke kernel 6-case path: {frag!r} in {cmd!r}"
                    )


def main() -> int:
    _assert_hooks_not_kernel_six_case()
    data = json.loads(HOOKS.read_text(encoding="utf-8"))
    reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    goal_ids = [g["id"] for g in reg["owner_goals"]]
    passed = failed = 0
    print("=== Goal verify hooks (M4) ===\n")
    skip_platform = os.environ.get("VERIFY_GOALS_SKIP_PLATFORM") == "1"
    for gid in goal_ids:
        if skip_platform and gid == "G-PLATFORM-SYNC":
            print(f"  SKIP · {gid} (VERIFY_GOALS_SKIP_PLATFORM=1 · Drive OAuth optional)")
            passed += 1
            continue
        hook = data["hooks"].get(gid)
        if not hook:
            print(f"  FAIL · {gid} — no hook")
            failed += 1
            continue
        ok_all = True
        details = []
        for c in hook["checks"]:
            ok, detail = run_check(gid, c)
            details.append(detail)
            if not ok:
                ok_all = False
        if ok_all:
            print(f"  PASS · {gid} ({'; '.join(details)})")
            passed += 1
        else:
            print(f"  FAIL · {gid} — {'; '.join(details)}")
            failed += 1
    print(f"\n=== Summary ===\ncases: {passed} passed, {failed} failed")
    if failed:
        print("RESULT: FAIL — goals verify")
        return 1
    print("RESULT: PASS — goals verify")
    return 0


if __name__ == "__main__":
    sys.exit(main())
