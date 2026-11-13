#!/usr/bin/env python3
"""
Agent 唯一机械入口（讨论 vs 拍板）。

  route   — 只输出 JSON 决策（不跑子脚本）
  discuss — brainstorm 预检（xhs + pending facts + Drive catalog+screen）
  decide  — 仅 Owner 明示拍板时 advice gate
  execute — route + 自动跑 discuss 或 decide（Agent 默认用此）

stdout 末行或全文为 JSON：agent_owner_content_session_v1
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from pending_videos_gate_policy import (  # noqa: E402
    classify_goal,
    owner_wants_decision,
)

SESSION_JSON = ROOT / "integration/handoff/agent-owner-content-session-contract.json"
TRIGGERS = (
    "小红书",
    "笔记",
    "待发",
    "pending",
    "口播",
    "字幕",
    "Drive",
    "背书",
    "战略",
    "薯条",
    "投放",
    "brainstorm",
    "第四条",
    "法国",
    "意大利",
)


def session_triggers(goal: str) -> bool:
    g = (goal or "").strip()
    return any(t in g for t in TRIGGERS)


def run_script(name: str, *extra: str) -> tuple[int, str]:
    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / name), *extra],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    out = ((r.stdout or "") + (r.stderr or "")).strip()
    return r.returncode, out[-1200:]


def build_route(goal: str) -> dict:
    g = (goal or "").strip()
    if owner_wants_decision(g):
        return {
            "schema": "agent_owner_content_session_v1",
            "mode": "decide",
            "goal": g,
            "run_command": [sys.executable, "scripts/agent-gate-pending-videos-advice.py", "--intent", "advice"],
            "handoff_primary": "integration/handoff/owner-pending-videos-advice-gate-latest.json",
            "facts_json": "integration/handoff/owner-pending-videos-facts-latest.json",
            "agent_may_deliver": ["拍板级薯条/标题/排序", "须引 decision_summary"],
            "agent_must_not": ["body_preview", "human_glance_only", "只读 Drive 文件名"],
            "delivery_line_template": "GATE: PASS · pending-advice · <as_of>",
        }
    if session_triggers(g) or classify_goal(g) in ("brainstorm", "eval", "advice_gate"):
        # Owner 未拍板 → 一律 discuss（含 pending 语境）
        if not owner_wants_decision(g) and classify_goal(g) == "advice_gate":
            classify_hint = "advice_gate_suppressed_until_owner_decision"
        else:
            classify_hint = classify_goal(g)
        return {
            "schema": "agent_owner_content_session_v1",
            "mode": "discuss",
            "goal": g,
            "classify_hint": classify_hint,
            "run_command": [
                sys.executable,
                "scripts/agent-brainstorm-preflight.py",
                "--goal",
                g or "小红书 IP brainstorm",
            ],
            "handoff_primary": "integration/handoff/owner-brainstorm-preflight-latest.json",
            "layers": {
                "xhs": "scripts/verify-xhs-analytics-freshness.py",
                "pending": "agent-gate-pending-videos-advice.py --intent brainstorm",
                "drive": "screen-xhs-drive-corpus.py --refresh-catalog",
            },
            "agent_may_deliver": ["多方案", "对比", "Drive+数据背书", "请 Owner 拍板"],
            "agent_must_not": ["最终投流定稿", "未读全文下地点/目击者事实", "body_preview"],
            "owner_decision_markers_ref": "pending_videos_gate_policy.owner_decision_markers()",
        }
    return {
        "schema": "agent_owner_content_session_v1",
        "mode": "skip",
        "goal": g,
        "reason": "未命中 owner-content 触发词；无需本入口",
        "sole_doc_monorepo": "docs/agent/AGENT-OWNER-CONTENT-SESSION.json",
    }


def cmd_route(goal: str) -> int:
    print(json.dumps(build_route(goal), ensure_ascii=False, indent=2))
    return 0


def cmd_discuss(goal: str) -> int:
    ec, tail = run_script("agent-brainstorm-preflight.py", "--goal", goal or "小红书 IP brainstorm")
    payload = build_route(goal)
    payload["executed"] = "discuss"
    payload["exit_code"] = ec
    payload["log_tail"] = tail
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return ec


def cmd_decide(goal: str) -> int:
    if not owner_wants_decision(goal):
        payload = build_route(goal)
        payload["error"] = "Owner 未明示拍板（拍板/定稿/就这条/帮我定…）"
        payload["executed"] = "decide_refused"
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 2
    ec, tail = run_script("agent-gate-pending-videos-advice.py", "--intent", "advice")
    payload = build_route(goal)
    payload["executed"] = "decide"
    payload["exit_code"] = ec
    payload["log_tail"] = tail
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return ec


def cmd_execute(goal: str) -> int:
    route = build_route(goal)
    if route["mode"] == "skip":
        print(json.dumps(route, ensure_ascii=False, indent=2))
        return 0
    if route["mode"] == "decide":
        return cmd_decide(goal)
    return cmd_discuss(goal)


def main() -> int:
    ap = argparse.ArgumentParser(description="Agent sole entry: discuss vs Owner decide")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("route", "discuss", "decide", "execute"):
        p = sub.add_parser(name)
        p.add_argument("--goal", "-g", default="", help="Owner 原话")
    args = ap.parse_args()
    goal = (args.goal or "").strip()

    if args.cmd == "route":
        return cmd_route(goal)
    if args.cmd == "discuss":
        return cmd_discuss(goal)
    if args.cmd == "decide":
        return cmd_decide(goal)
    return cmd_execute(goal)


if __name__ == "__main__":
    raise SystemExit(main())
