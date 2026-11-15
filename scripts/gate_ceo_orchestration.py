"""Classify goal → replay-only vs CEO full after research-gate PASS."""

from __future__ import annotations

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

DISCUSS_ONLY_MARKERS = (
    "先讨论",
    "不要结论",
    "只聊",
    "brainstorm",
    "脑洞",
    "随便聊",
    "开放式",
)


def has_any(goal: str, markers: tuple[str, ...]) -> bool:
    g = (goal or "").strip()
    return any(m in g for m in markers)


def orchestration_mode(*, goal: str, brief: str = "", force_ceo: bool = False, force_replay: bool = False) -> str:
    """
    Returns:
      copy_ceo_full — gate PASS 后接 run_ceo_full（--skip-research-gate）
      replay_only   — gate PASS 后停止，不接 CEO 战役
      skip          — 非 owner-content / 无关 goal
    """
    g = (goal or "").strip()
    if not g and not brief:
        return "skip"
    if force_replay:
        return "replay_only"
    if force_ceo or brief.strip():
        return "copy_ceo_full"
    if has_any(g, DISCUSS_ONLY_MARKERS) and not (
        has_any(g, STRONG_COPY_MARKERS) or has_any(g, WEAK_COPY_MARKERS)
    ):
        return "replay_only"
    if has_any(g, STRONG_COPY_MARKERS) or has_any(g, WEAK_COPY_MARKERS):
        return "copy_ceo_full"
    if has_any(g, REPLAY_MARKERS):
        return "replay_only"
    if "口播" in g and has_any(g, ("文案", "写稿", "下一篇", "待发")):
        return "copy_ceo_full"
    if has_any(g, ("艺术家", "口播", "投放", "薯条")):
        return "replay_only"
    return "replay_only"