"""Classify goal → post-gate orchestration (replay / evaluate slice / CEO full)."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OVERRIDES_PATH = ROOT / "integration/handoff/owner-orchestration-overrides.json"

STRONG_COPY_MARKERS = (
    "Brief",
    "brief",
    "定稿",
    "长稿",
    "Discovery",
    "discovery",
    "战役",
    "evaluate",
    "评估稿",
    "CEO 开始",
    "CEO开始",
    "请 CEO",
    "CEO 干活",
    "CEO 派活",
)

WEAK_COPY_MARKERS = (
    "写稿",
    "文案",
    "新题",
    "笔记",
    "小红书",
    "Medium",
    "LinkedIn",
    "领英",
    "大V",
    "对标",
    "笔触",
    "下一篇",
    "口播稿",
    "口播文案",
)

REPLAY_MARKERS = (
    "已发",
    "复盘",
    "监督",
    "补全",
    "为什么",
    "数据分析",
    "后台",
)

EVALUATE_POST_MARKERS = (
    "距离",
    "gold",
    "baseline",
    "对齐",
    "拉距",
    "evaluate",
    "评估",
    "evolution",
)

DISCUSS_ONLY_MARKERS = (
    "先讨论",
    "不要结论",
    "只聊",
    "brainstorm",
    "脑洞",
    "随便聊",
    "开放式",
)

VALID_MODES = frozenset({"replay_only", "evaluate_post_gate", "copy_ceo_full", "skip"})


def has_any(goal: str, markers: tuple[str, ...]) -> bool:
    g = (goal or "").strip()
    return any(m in g for m in markers)


def has_all(goal: str, markers: tuple[str, ...]) -> bool:
    g = (goal or "").strip()
    return all(m in g for m in markers)


def has_none(goal: str, markers: tuple[str, ...]) -> bool:
    g = (goal or "").strip()
    return not any(m in g for m in markers)


def load_overrides() -> dict:
    if not OVERRIDES_PATH.is_file():
        return {}
    return json.loads(OVERRIDES_PATH.read_text(encoding="utf-8"))


def override_mode(goal: str) -> str | None:
    """First matching rule wins (方案 2 安全阀)."""
    g = (goal or "").strip()
    if not g:
        return None
    data = load_overrides()
    for rule in data.get("rules") or []:
        mode = str(rule.get("mode") or "")
        if mode not in VALID_MODES:
            continue
        if rule.get("match_any") and not has_any(g, tuple(rule["match_any"])):
            continue
        if rule.get("match_all") and not has_all(g, tuple(rule["match_all"])):
            continue
        if rule.get("match_none") and not has_none(g, tuple(rule["match_none"])):
            continue
        return mode
    return None


def orchestration_mode(*, goal: str, brief: str = "", force_ceo: bool = False, force_replay: bool = False) -> str:
    """
    Returns:
      copy_ceo_full       — C 档 · run_ceo_full + optional auto-gate-loop
      evaluate_post_gate  — B 档 · evaluate 切片（无 HTML 战役全家桶）
      replay_only         — A 档 · gate PASS 即停
      skip                — 非 owner-content goal
    """
    g = (goal or "").strip()
    if not g and not brief:
        return "skip"
    forced = override_mode(g)
    if forced:
        return forced
    if force_replay:
        return "replay_only"
    if force_ceo or brief.strip():
        return "copy_ceo_full"
    if has_any(g, DISCUSS_ONLY_MARKERS) and not (
        has_any(g, STRONG_COPY_MARKERS) or has_any(g, WEAK_COPY_MARKERS) or has_any(g, REPLAY_MARKERS)
    ):
        return "replay_only"
    if has_any(g, STRONG_COPY_MARKERS) or has_any(g, WEAK_COPY_MARKERS):
        return "copy_ceo_full"
    if has_any(g, REPLAY_MARKERS) or has_any(g, EVALUATE_POST_MARKERS):
        return "evaluate_post_gate"
    if "口播" in g and has_any(g, ("文案", "写稿", "下一篇", "待发")):
        return "copy_ceo_full"
    if has_any(g, ("艺术家", "口播", "投放", "薯条")):
        return "evaluate_post_gate"
    return "replay_only"