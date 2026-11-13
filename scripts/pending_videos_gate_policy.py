#!/usr/bin/env python3
"""L2d / CEO: 默认 brainstorm；仅 Owner 明示拍板才 advice_gate。短语可 overlay JSON 扩展。"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PHRASES_OVERLAY = ROOT / "integration/handoff/pending-videos-goal-phrases.json"

EVAL_TRIGGERS = (
    "评估待发",
    "待发口播",
    "口播评估",
    "评估 pending",
    "评估口播",
    "同步待发视频",
    "口播打分",
    "run-owner-pending-videos-eval",
)

ADVICE_GATE_TRIGGERS = (
    "pending-videos",
    "待发评估",
    "advice-gate",
    "L2d-G",
)

# 仅 Owner 明示要 Agent 交付拍板结论（默认禁止 Agent 自拟拍板）
OWNER_DECISION_MARKERS = (
    "拍板",
    "定稿",
    "就这条",
    "就这个",
    "按这个发",
    "帮我定",
    "你帮我定",
    "给最终",
    "最终方案",
    "可以发了",
    "你定",
    "替我定",
    "定下来",
)

PENDING_CONTEXT_MARKERS = (
    "待发",
    "pending",
    "薯条",
    "口播",
    "字幕",
    "第四条",
    "已拍",
    "inbox",
)

BRAINSTORM_MARKERS = (
    "brainstorm",
    "脑洞",
    "随便聊",
    "先讨论",
    "不要结论",
    "先别想",
    "只聊方向",
    "开放式",
    "发散",
    "头脑风暴",
)


def _load_overlay_list(key: str) -> tuple[str, ...]:
    if not PHRASES_OVERLAY.is_file():
        return ()
    try:
        data = json.loads(PHRASES_OVERLAY.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return ()
    items = (data.get("phrases") or {}).get(key) or []
    if items and isinstance(items[0], dict):
        return tuple(x["phrase"] for x in items if x.get("phrase"))
    return tuple(str(x) for x in items)


def eval_triggers() -> tuple[str, ...]:
    return EVAL_TRIGGERS + _load_overlay_list("eval")


def advice_triggers() -> tuple[str, ...]:
    return ADVICE_GATE_TRIGGERS + _load_overlay_list("advice")


def owner_decision_markers() -> tuple[str, ...]:
    return OWNER_DECISION_MARKERS + _load_overlay_list("owner_decision")


OWNER_DECISION_NEGATION = (
    "不要拍板",
    "不拍板",
    "别拍板",
    "无需拍板",
    "不要结论",
    "不要定稿",
    "不要帮我定",
)


def owner_wants_decision(goal: str) -> bool:
    g = (goal or "").strip()
    if any(neg in g for neg in OWNER_DECISION_NEGATION):
        return False
    return any(m in g for m in owner_decision_markers())


def pending_context(goal: str) -> bool:
    g = (goal or "").strip()
    return any(m in g for m in PENDING_CONTEXT_MARKERS) or any(
        t in g for t in advice_triggers()
    )


def classify_goal(goal: str) -> str:
    """
    Returns: eval | advice_gate | brainstorm | skip

    - 默认不跑 L2d（skip），避免 CEO 噪音
    - advice_gate **仅** Owner 明示拍板 + pending 语境
  - eval：显式评估待发口令
    - brainstorm：显式脑洞或（有 pending 语境但 Owner 未拍板）→ 仅预检/讨论，不替 Owner 定稿
    """
    g = (goal or "").strip()
    if not g:
        return "skip"
    if any(t in g for t in eval_triggers()):
        return "eval"
    if owner_wants_decision(g) and pending_context(g):
        return "advice_gate"
    if any(b in g for b in BRAINSTORM_MARKERS):
        return "brainstorm"
    if pending_context(g) and not owner_wants_decision(g):
        return "brainstorm"
    return "skip"
