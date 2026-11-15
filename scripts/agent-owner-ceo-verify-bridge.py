#!/usr/bin/env python3
"""
老 CEO 写稿 verify 子集 → 并进 research-gate（整链 CEO 仍走 ceo-full-execution-pipeline）。

handoff → integration/handoff/owner-ceo-verify-bridge-latest.json
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "integration/handoff/owner-ceo-verify-bridge-latest.json"

COPY_KW = ("文案", "口播", "写稿", "长稿", "Medium", "LinkedIn", "领英", "大师课", "不走专业")
LONGFORM_KW = ("长稿", "longform", "Clever", "3000", "Brief")


def run_cmd(cmd: list[str], *, timeout: int = 300) -> tuple[int, str]:
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=timeout)
    return r.returncode, ((r.stdout or "") + (r.stderr or "")).strip()[-2500:]


def goal_is_copy(goal: str) -> bool:
    g = goal or ""
    return any(k in g for k in COPY_KW)


def find_brief_for_goal(goal: str) -> Path | None:
    candidates: list[Path] = []
    patterns = ["**/*-brief.md", "**/Brief.md", "**/*longform*.md"]
    roots = [
        ROOT / "content/evolution/04-xhs-topic-manager",
        ROOT / "content/xiaohongshu",
    ]
    for base in roots:
        if not base.is_dir():
            continue
        for pat in patterns:
            candidates.extend(base.glob(pat))
    if not candidates:
        return None
    g = goal.strip()
    scored: list[tuple[int, Path]] = []
    for p in candidates:
        text = p.read_text(encoding="utf-8", errors="replace")[:8000]
        name = p.name.lower()
        score = 0
        for token in re_split_goal(g):
            if token and (token in text or token in name):
                score += 2
        if score:
            scored.append((score, p))
    if scored:
        scored.sort(key=lambda x: (-x[0], -x[1].stat().st_mtime))
        if scored[0][0] >= 3:
            return scored[0][1]
    return None


def re_split_goal(g: str) -> list[str]:
    import re

    return [t for t in re.split(r"[^\w\u4e00-\u9fff]+", g) if len(t) >= 2]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--goal", default="")
    ap.add_argument("--skip-if-not-copy", action="store_true")
    args = ap.parse_args()
    goal = (args.goal or "").strip()

    if args.skip_if_not_copy and goal and not goal_is_copy(goal):
        payload = {
            "schema": "owner_ceo_verify_bridge_v1",
            "status": "SKIP",
            "goal": goal,
            "reason": "not copy/longform goal",
        }
        OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"status": "SKIP", "handoff": str(OUT.relative_to(ROOT))}))
        return 0

    checks: list[dict] = []
    fail = 0

    ec, tail = run_cmd(["bash", "scripts/verify-owner-copy-v-tier-mandate.sh"])
    st = "PASS" if ec == 0 else "FAIL"
    checks.append({"id": "v_tier_mandate_wiring", "status": st, "exit_code": ec, "tail": tail[-400:]})
    if st == "FAIL":
        fail += 1

    ec, tail = run_cmd(["bash", "scripts/verify-xhs-voice-qa.sh"])
    if ec == 0:
        vq_st = "PASS"
    elif "WARN no round1" in tail and "voice-anchor-sources.json: 5 titles OK" in tail:
        vq_st = "PASS"
        checks.append(
            {"id": "voice_qa", "status": vq_st, "note": "anchor OK · round1 lint skipped", "tail": tail[-400:]}
        )
    else:
        vq_st = "FAIL"
        checks.append({"id": "voice_qa", "status": vq_st, "exit_code": ec, "tail": tail[-400:]})
        fail += 1
    if vq_st == "PASS" and not any(c.get("id") == "voice_qa" for c in checks):
        checks.append({"id": "voice_qa", "status": vq_st, "exit_code": ec, "tail": tail[-400:]})

    wants_longform = any(k in goal for k in LONGFORM_KW)
    brief = find_brief_for_goal(goal) if goal and wants_longform else None
    if brief:
        ec, tail = run_cmd(["bash", "scripts/verify-xhs-clever-advocate.sh", "--brief", str(brief)])
        st = "PASS" if ec == 0 else "FAIL"
        checks.append(
            {
                "id": "clever_advocate",
                "status": st,
                "brief": str(brief.relative_to(ROOT)),
                "exit_code": ec,
                "tail": tail[-400:],
            }
        )
        if st == "FAIL":
            fail += 1
    else:
        checks.append(
            {
                "id": "clever_advocate",
                "status": "SKIP",
                "reason": "no brief matched goal — 定稿长稿时再跑",
            }
        )

    manifest = ROOT / "integration/handoff/workflow-automation-manifest.json"
    payload = {
        "schema": "owner_ceo_verify_bridge_v1",
        "as_of": datetime.now(timezone.utc).isoformat(),
        "goal": goal,
        "purpose_zh": "老 CEO verify 子集并进 research-gate；整链仍用 ceo-full-execution-pipeline.sh",
        "workflow_automation_manifest": str(manifest.relative_to(ROOT)) if manifest.is_file() else None,
        "checks": checks,
        "fail_count": fail,
        "status": "PASS" if fail == 0 else "FAIL",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": payload["status"], "handoff": str(OUT.relative_to(ROOT)), "fail_count": fail}))
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())