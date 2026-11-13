#!/usr/bin/env python3
"""
Brainstorm 前机械预检（Owner 未说拍板时 Must）。

- 小红书 xlsx/csv 对齐
- pending 字幕全文 facts（非 advice 拍板）
- Drive 背书：禁止仅凭文件名；须 screen / corpus plan 或已有 screen 产物

不写拍板结论；handoff → owner-brainstorm-preflight-latest.json
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "integration/handoff/owner-brainstorm-preflight-latest.json"
sys.path.insert(0, str(ROOT / "scripts"))
from pending_videos_gate_policy import owner_wants_decision  # noqa: E402

XHS_KW = (
    "小红书",
    "笔记",
    "薯条",
    "曝光",
    "互动",
    "xlsx",
    "后台",
    "近7",
    "近30",
    "数据",
    "已发",
    "复盘",
    "投流",
    "聚光",
)
DEEP_KW = ("已发", "后台", "复盘", "为什么", "监督", "深度", "补全", "数据分析", "6-case", "六项")
PENDING_KW = ("待发", "pending", "口播", "字幕", "inbox", "法国", "意大利", "目击者")
DRIVE_KW = (
    "Drive",
    "drive",
    "背书",
    "资料库",
    "语料",
    "fusion",
    "corpus",
    "战略",
    "心法",
    "投放",
    "薯条",
    "小红书",
)
SCREEN_MAX_AGE_S = 86400


def goal_needs(goal: str, kws: tuple[str, ...]) -> bool:
    return any(k in goal for k in kws)


def run_py(script: str, *extra: str) -> tuple[int, str]:
    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / script), *extra],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    out = (r.stdout or "") + (r.stderr or "")
    return r.returncode, out.strip()[-500:]


def ensure_pending_facts() -> dict:
    ec, tail = run_py("agent-gate-pending-videos-advice.py", "--intent", "brainstorm")
    return {
        "status": "PASS" if ec == 0 else "FAIL",
        "exit_code": ec,
        "tail": tail,
        "rule": "pending 事实来自全文 facts manifest；禁止 body_preview",
    }


def screen_stale(screen: Path) -> bool:
    if not screen.is_file():
        return True
    import time

    return (time.time() - screen.stat().st_mtime) > SCREEN_MAX_AGE_S


def goal_needs_deep(goal: str) -> bool:
    return any(k in goal for k in DEEP_KW)


def auto_drive_screen(goal: str) -> tuple[int, str]:
    g = goal.strip() or "小红书 IP brainstorm 背书"
    cmd = [
        sys.executable,
        str(ROOT / "scripts/screen-xhs-drive-corpus.py"),
        "--goal",
        g,
        "--refresh-catalog",
        "--limit",
        "12",
    ]
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    out = (r.stdout or "") + (r.stderr or "")
    return r.returncode, out.strip()[-800:]


def check_drive_screen(goal: str, *, auto: bool) -> dict:
    screen = ROOT / "content/evolution/00-manager/ceo-inbox/xhs-drive-screen-latest.md"
    stale = screen_stale(screen)
    if auto and stale:
        ec, tail = auto_drive_screen(goal)
        if ec != 0:
            return {
                "status": "FAIL",
                "auto_screen": True,
                "exit_code": ec,
                "tail": tail,
            }
    if screen.is_file():
        return {
            "status": "PASS",
            "screen": str(screen.relative_to(ROOT)),
            "catalog_refreshed": auto and stale,
            "rule": "全库 catalog refresh + screen 后打开入选文件全文",
        }
    return {
        "status": "FAIL",
        "agent_must": "screen-xhs-drive-corpus.py --refresh-catalog",
        "forbid": "仅凭 Drive 标题/文件名下结论",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--goal", default="", help="Owner 原话（判定要跑哪些层）")
    ap.add_argument("--deep", action="store_true", help="深度链：hydrate + 6-case + CEO 切片")
    args = ap.parse_args()
    goal = args.goal.strip()

    if owner_wants_decision(goal):
        print(
            "NOTE Owner 已明示拍板 — 用 agent-gate-pending-videos-advice.py --intent advice",
            file=sys.stderr,
        )
        return 2

    layers: dict = {}
    fail = 0

    if not goal or goal_needs(goal, XHS_KW):
        ec, tail = run_py("verify-xhs-analytics-freshness.py")
        layers["xhs_analytics"] = {
            "status": "PASS" if ec == 0 else "FAIL",
            "exit_code": ec,
            "hint": tail.split("\n")[-1] if tail else "",
        }
        if ec != 0:
            fail += 1

    if not goal or goal_needs(goal, PENDING_KW):
        layers["pending_subtitles"] = ensure_pending_facts()
        if layers["pending_subtitles"]["status"] == "FAIL":
            fail += 1

    need_drive = not goal or goal_needs(goal, DRIVE_KW)
    if need_drive:
        layers["drive_corpus"] = check_drive_screen(goal or "小红书 IP", auto=True)
        if layers["drive_corpus"].get("status") == "FAIL":
            fail += 1

    deep = args.deep or goal_needs_deep(goal)
    deep_handoff = None
    if deep:
        ec_d, tail_d = run_py("agent-brainstorm-deep-preflight.py", "--goal", goal or "深度复盘")
        layers["deep_chain"] = {
            "status": "PASS" if ec_d == 0 else "FAIL",
            "exit_code": ec_d,
            "tail": tail_d,
            "handoff": "integration/handoff/owner-brainstorm-deep-preflight-latest.json",
        }
        deep_handoff = layers["deep_chain"]["handoff"]
        if ec_d != 0:
            fail += 1

    payload = {
        "as_of": datetime.now(timezone.utc).isoformat(),
        "mode": "brainstorm_deep" if deep else "brainstorm",
        "owner_decision_default": "Owner 拍板；Agent 不自拟最终投流/标题定稿",
        "agent_may_deliver": ["多方案", "对比", "风险", "引用 decision_summary 作讨论依据（非拍板）"],
        "layers": layers,
        "deep_preflight_handoff": deep_handoff,
        "status": "PASS" if fail == 0 else "FAIL",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    monorepo_drive = Path.home() / "Desktop/未命名/scripts/run-drive-corpus-c2.py"
    if monorepo_drive.is_file():
        payload["drive_corpus_c2"] = str(monorepo_drive)

    if fail:
        print(f"FAIL brainstorm-preflight layers={fail}", file=sys.stderr)
        print(json.dumps(layers, ensure_ascii=False, indent=2))
        return 1
    print("PASS agent-brainstorm-preflight")
    print(f"handoff → {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
