#!/usr/bin/env python3
"""
三平台笔触 — 人格=VOICE-ANCHOR；KOL=rhythm_only。

读 platform-voice-benchmark-roster.json + voice-anchor-sources → handoff
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ROSTER = ROOT / "integration/handoff/platform-voice-benchmark-roster.json"
ANCHOR_JSON = ROOT / "content/xiaohongshu/voice-anchor-sources.json"
VOICE_STACK = ROOT / "integration/handoff/owner-voice-stack-latest.json"
OUT = ROOT / "integration/handoff/owner-platform-voice-benchmark-latest.json"
V_TIER = ROOT / "docs/OWNER-COPY-V-TIER-400K-MANDATE.md"

COPY_TRIGGERS = (
    "文案",
    "口播",
    "下一篇",
    "brainstorm",
    "Medium",
    "LinkedIn",
    "领英",
    "大V",
    "对标",
    "笔触",
    "写稿",
    "标题",
    "第五",
    "不走专业",
    "大师课",
    "艺术家",
)


def goal_needs_copy(goal: str) -> bool:
    g = (goal or "").strip()
    return any(t in g for t in COPY_TRIGGERS) or bool(g)


def load_json(path: Path) -> dict | None:
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def pick_primary_anchor(goal: str, stack: dict | None, anchors: list[dict]) -> dict:
    if stack and stack.get("primary_anchor", {}).get("title"):
        p = stack["primary_anchor"]
        for a in anchors:
            if a.get("title") == p.get("title"):
                return a
    g = goal.lower()
    for a in anchors:
        t = str(a.get("title") or "")
        if goal and goal in t or (goal and any(k in t for k in goal.split() if len(k) > 1)):
            return a
    if "艺术家" in goal:
        for a in anchors:
            if "艺术家" in str(a.get("title") or ""):
                return a
    if "大师课" in goal:
        for a in anchors:
            if "大师" in str(a.get("title") or "") or "祛魅" in str(a.get("title") or ""):
                return a
    return anchors[0] if anchors else {}


def anchor_synthesis(goal: str, primary: dict, rhythm: dict) -> dict:
    title = str(primary.get("title") or "")
    open80 = str(primary.get("first_80_chars") or "")[:80]
    xhs_r = (rhythm.get("xiaohongshu") or [])[:2]
    li_r = (rhythm.get("linkedin") or [])[:2]
    me_r = (rhythm.get("medium") or [])[:2]
    rhythm_x = " · ".join(sum([r.get("style_axes") or [] for r in xhs_r], [])[:3])
    rhythm_li = " · ".join(sum([r.get("style_axes") or [] for r in li_r], [])[:3])
    rhythm_me = " · ".join(sum([r.get("style_axes") or [] for r in me_r], [])[:3])

    return {
        "topic": goal or title,
        "persona_source": "voice-anchor-sources.json",
        "rhythm_only": True,
        "primary_anchor_title": title,
        "primary_opening_80": open80,
        "xiaohongshu": {
            "hook_pattern": f"标题弧对齐锚点「{title[:20]}…」",
            "voice": f"开口对齐 Owner 原话：「{open80[:40]}…」；节奏参考：{rhythm_x or '一条一判断'}",
            "cta": "评论收「台下偷到的一句话」或真实经历（锚点回应体）",
            "avoid": ["KOL 人设覆盖", "长铺垫", "意大利误标"],
        },
        "linkedin": {
            "hook_pattern": "stakes 一句（家长/标准）· 非海报体",
            "voice": f"人格=锚点「{title}」；节奏：{rhythm_li or '短行'}",
            "cta": "结尾一句问读者 stakes",
            "avoid": ["Delighted to announce", "堆履历"],
        },
        "medium": {
            "hook_pattern": f"场景：从锚点「{title}」延伸的现场",
            "voice": f"第一人称感想≥60%；节奏：{rhythm_me or '场景→内化'}",
            "cta": "process not product · 与「走不走专业」分轨",
            "avoid": ["复制小红书全文", "KOL 人格"],
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--goal", default="", help="本轮选题/Owner 原话")
    ap.add_argument("--skip-if-unrelated", action="store_true")
    args = ap.parse_args()
    goal = args.goal.strip()

    if args.skip_if_unrelated and goal and not goal_needs_copy(goal):
        print(json.dumps({"status": "SKIP", "reason": "goal not copy/brainstorm"}))
        return 0

    if not ROSTER.is_file():
        print(f"FAIL: missing {ROSTER}", file=sys.stderr)
        return 1
    roster = json.loads(ROSTER.read_text(encoding="utf-8"))
    anchors_data = load_json(ANCHOR_JSON) or {}
    anchors = list(anchors_data.get("anchors") or [])
    stack = load_json(VOICE_STACK)

    fail = 0
    min_a = int((roster.get("owner_anchors") or {}).get("min_entries") or 5)
    if len(anchors) < min_a:
        print(f"FAIL: owner anchors < {min_a}", file=sys.stderr)
        fail += 1

    rhythm = roster.get("rhythm_references") or {}
    for plat in ("xiaohongshu", "linkedin", "medium"):
        items = rhythm.get(plat) or []
        if len(items) < 2:
            print(f"FAIL: rhythm_references {plat} < 2", file=sys.stderr)
            fail += 1

    primary = pick_primary_anchor(goal, stack, anchors)
    synthesis = anchor_synthesis(goal, primary, rhythm)

    payload = {
        "schema": "owner_platform_voice_benchmark_v2",
        "as_of": datetime.now(timezone.utc).isoformat(),
        "goal": goal,
        "persona_source": roster.get("persona_source"),
        "rhythm_only_kol": True,
        "precedence_order": roster.get("precedence_order"),
        "roster_path": str(ROSTER.relative_to(ROOT)),
        "voice_stack_handoff": str(VOICE_STACK.relative_to(ROOT)),
        "v_tier_mandate": str(V_TIER.relative_to(ROOT)) if V_TIER.is_file() else None,
        "v_tier_role": "after_anchor_style_checklist_not_persona",
        "mandatory_before_draft": [
            "Must owner-voice-stack PASS",
            "人格真源=voice-anchor-sources",
            "KOL=rhythm_only",
            "三平台分稿",
            "Owner 终检前 verify-owner-copy-v-tier-attestation 若 brief 绑定",
        ],
        "matched_anchor": {
            "title": primary.get("title"),
            "first_80_chars": primary.get("first_80_chars"),
        },
        "rhythm_summary": {
            k: [{"handle": i.get("handle"), "rhythm_only": i.get("rhythm_only")} for i in (rhythm.get(k) or [])[:2]]
            for k in ("xiaohongshu", "linkedin", "medium")
        },
        "platform_synthesis": synthesis,
        "status": "PASS" if fail == 0 else "FAIL",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": payload["status"], "handoff": str(OUT.relative_to(ROOT))}))
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())