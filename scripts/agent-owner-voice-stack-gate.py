#!/usr/bin/env python3
"""
Owner 声音锚点 stack — Must 在 platform-voice / 写稿前。

VOICE-ANCHOR + voice-anchor-sources + yage overlay · handoff owner-voice-stack-latest.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "integration/handoff/owner-voice-stack-latest.json"
ANCHOR_MD = ROOT / "content/xiaohongshu/VOICE-ANCHOR.md"
ANCHOR_JSON = ROOT / "content/xiaohongshu/voice-anchor-sources.json"
YAGE = ROOT / "rules/skills/skill_yage_voice.md"
OVERLAY = ROOT / "rules/skills/overlays/skill_yage_voice-danying.overlay.md"
V_TIER = ROOT / "integration/handoff/owner-copy-v-tier-400k.json"
TITLE_PATTERNS = (
    ("事件+情绪", r"发火|目睹|当场"),
    ("原来…", r"原来"),
    ("回应体", r"回复|被嘲讽"),
    ("A但不B", r"但(不|把)"),
    ("价值选择", r"替代|选择"),
    ("问句/判断", r"不需要|要不要|为什么"),
)


def load_json(path: Path) -> dict | None:
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def pick_anchors_for_goal(anchors: list[dict], goal: str, limit: int = 3) -> list[dict]:
    g = (goal or "").strip()
    if not g:
        return anchors[:limit]
    scored: list[tuple[int, dict]] = []
    for a in anchors:
        title = str(a.get("title") or "")
        score = 0
        for ch in g:
            if ch in title:
                score += 2
        for token in re.split(r"[^\w\u4e00-\u9fff]+", g):
            if len(token) >= 2 and token in title:
                score += 3
        if "大师课" in g and ("大师" in title or "祛魅" in title):
            score += 4
        if "艺术家" in g and "艺术家" in title:
            score += 5
        if score:
            scored.append((score, a))
    scored.sort(key=lambda x: (-x[0], str(x[1].get("publish_date") or "")))
    if scored:
        return [a for _, a in scored[:limit]]
    return anchors[:limit]


def title_pattern_for(anchor: dict) -> str:
    title = str(anchor.get("title") or "")
    for name, pat in TITLE_PATTERNS:
        if re.search(pat, title):
            return name
    return "事件+情绪"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--goal", default="")
    args = ap.parse_args()
    goal = args.goal.strip()
    errors: list[str] = []
    for label, path in (
        ("VOICE-ANCHOR", ANCHOR_MD),
        ("voice-anchor-sources", ANCHOR_JSON),
        ("skill_yage_voice", YAGE),
        ("danying_overlay", OVERLAY),
    ):
        if not path.is_file():
            errors.append(f"missing {label}: {path.relative_to(ROOT)}")

    anchors_data = load_json(ANCHOR_JSON) or {}
    anchors = list(anchors_data.get("anchors") or [])
    if len(anchors) < 5:
        errors.append(f"voice-anchor-sources anchors < 5 (got {len(anchors)})")

    picked = pick_anchors_for_goal(anchors, goal)
    primary = picked[0] if picked else {}
    openings = [
        {
            "title": a.get("title"),
            "first_80_chars": a.get("first_80_chars"),
            "title_pattern": title_pattern_for(a),
            "publish_date": a.get("publish_date"),
        }
        for a in picked
    ]

    precedence = [
        "voice_anchor_persona",
        "OWNER-LONGFORM-DE-AI-VOICE",
        "skill_yage_syntax_only",
        "rhythm_references_kol",
        "owner_copy_v_tier_style",
        "benchmark_cross_dim_facts",
    ]

    payload = {
        "schema": "owner_voice_stack_gate_v1",
        "as_of": datetime.now(timezone.utc).isoformat(),
        "goal": goal,
        "persona_source": str(ANCHOR_JSON.relative_to(ROOT)),
        "rhythm_only_kol": True,
        "precedence_order": precedence,
        "must_read": [
            str(ANCHOR_MD.relative_to(ROOT)),
            str(ANCHOR_JSON.relative_to(ROOT)),
            str(YAGE.relative_to(ROOT)),
            str(OVERLAY.relative_to(ROOT)),
        ],
        "primary_anchor": {
            "title": primary.get("title"),
            "first_80_chars": primary.get("first_80_chars"),
            "title_pattern": title_pattern_for(primary) if primary else None,
        },
        "matched_anchors": openings,
        "anchor_count": len(anchors),
        "v_tier_ref": str(V_TIER.relative_to(ROOT)) if V_TIER.is_file() else None,
        "v_tier_role": "style_checklist_after_anchor_not_persona",
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": payload["status"], "handoff": str(OUT.relative_to(ROOT))}))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())