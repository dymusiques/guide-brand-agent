#!/usr/bin/env python3
"""
三平台大V笔触对标 — Must 层（写稿/口播/brainstorm 前）。

读 platform-voice-benchmark-roster.json → 写 owner-platform-voice-benchmark-latest.json
Agent 须在 handoff 内填 per_platform_style_notes（本轮若 --goal 则写 synthesis 草稿）。

FAIL：roster 缺平台 / 无 xhs+linkedin+medium 各 ≥2 参考
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
)


def goal_needs_copy(goal: str) -> bool:
    g = (goal or "").strip()
    return any(t in g for t in COPY_TRIGGERS) or bool(g)


def default_synthesis(goal: str) -> dict:
    """机械默认：第五篇「不走专业为什么还要公开大师课」对标摘要。"""
    return {
        "topic": goal or "不走专业为什么还要公开大师课",
        "xiaohongshu": {
            "hook_pattern": "问句封面 + 6 字（如「看台下一小时」）",
            "voice": "现场目击者 · 短段 · 每段一个判断；学小手说琴「一条一个自查」；开场别 OK一说到",
            "cta": "评论要「台下偷到的一句话」；合作私信「合作」",
            "avoid": ["长铺垫", "纯技巧", "意大利误标"]
        },
        "linkedin": {
            "hook_pattern": "This masterclass is not about… / 读者 stakes 一句",
            "voice": "Tracey 式 interpretation reflection；Maria 式短行；法派+家长+不推销专业",
            "cta": "结尾问：Would you still fly to a public masterclass if your child won't major?",
            "avoid": ["海报体 Delighted to perform", "堆履历"]
        },
        "medium": {
            "hook_pattern": "具体场景：公开大师课台下那一小时",
            "voice": "Maureen：process not product；Laurel：场景→内化；段落 4–6，800–1200 词",
            "cta": "收束：标准长什么样 ≠ 当不当艺术家",
            "avoid": ["碎碎念无结构", "重复小红书全文"]
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
    fail = 0
    for plat in ("xiaohongshu", "linkedin", "medium"):
        items = roster.get(plat) or []
        if len(items) < 2:
            print(f"FAIL: {plat} roster < 2", file=sys.stderr)
            fail += 1

    synthesis = default_synthesis(goal)
    if goal and not re.search("|".join(map(re.escape, COPY_TRIGGERS[:8])), goal):
        synthesis["topic"] = goal

    payload = {
        "schema": "owner_platform_voice_benchmark_v1",
        "as_of": datetime.now(timezone.utc).isoformat(),
        "goal": goal,
        "roster_path": str(ROSTER.relative_to(ROOT)),
        "v_tier_mandate": str(V_TIER.relative_to(ROOT)) if V_TIER.is_file() else None,
        "mandatory_before_draft": [
            "读 roster 每平台 ≥2 URL（或帖）",
            "写稿须分三平台语气，禁止剪贴同一篇",
            "小红书 60–90s 口播；LinkedIn 800–1200 字符英文或中英；Medium 长文",
            "Owner 终检前：verify-owner-copy-v-tier-attestation 若 brief 绑定",
        ],
        "roster_summary": {
            k: [{"handle": i.get("handle"), "url": i.get("url")} for i in (roster.get(k) or [])[:3]]
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