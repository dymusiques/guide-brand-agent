#!/usr/bin/env python3
"""Agent 01 · personal-ip function shell (static · no Gemini).

Content/truth lives in MD + Playbook; this script only verifies markers for campaign/autopilot.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IP_BRIEF = ROOT / "content/personal-ip/ip-positioning-brief-2026-10-05.md"
PLAYBOOK = ROOT / "content/personal-ip/2026-10-18-key-person-of-influence-capstone-playbook.md"
INTEGRATION = ROOT / "agents/01-personal-ip/INTEGRATION-PROMPT.md"

REQUIRED_IN_IP = (
    "品牌合作范围",
    "不单品类绑定",
)
REQUIRED_ANY_OF = ("三支柱", "三内容支柱")


def check_ip_brief() -> list[str]:
    errs: list[str] = []
    if not IP_BRIEF.is_file():
        return [f"missing: {IP_BRIEF.relative_to(ROOT)}"]
    text = IP_BRIEF.read_text(encoding="utf-8")
    for needle in REQUIRED_IN_IP:
        if needle not in text:
            errs.append(f"ip-positioning-brief missing: {needle!r}")
    if not any(n in text for n in REQUIRED_ANY_OF):
        errs.append(f"ip-positioning-brief missing one of: {REQUIRED_ANY_OF!r}")
    return errs


def check_playbook_stack() -> list[str]:
    errs: list[str] = []
    for p in (PLAYBOOK, INTEGRATION):
        if not p.is_file():
            errs.append(f"missing: {p.relative_to(ROOT)}")
    if PLAYBOOK.is_file():
        pb = PLAYBOOK.read_text(encoding="utf-8")
        if "CAPSTONE" not in pb and "Key Person" not in pb:
            errs.append("playbook missing CAPSTONE / Key Person anchor")
    return errs


def main() -> int:
    p = argparse.ArgumentParser(description="01 personal-ip evaluate (static shell)")
    p.add_argument("--check", action="store_true", help="exit 0/1 for campaign (default)")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    errs = check_ip_brief() + check_playbook_stack()
    row = {
        "agent": "01-personal-ip",
        "layer": "static_function_shell",
        "ip_brief": str(IP_BRIEF.relative_to(ROOT)),
        "pass": len(errs) == 0,
        "errors": errs,
        "note": "IP positioning content = MD+Playbook+Prompt; this is verify-only",
    }

    if args.json or not args.check:
        print(json.dumps(row, ensure_ascii=False, indent=2))

    if errs:
        for e in errs:
            print(f"FAIL: {e}", file=sys.stderr)
        return 1
    if args.check:
        print("RESULT: PASS evaluate_personal_ip --check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
