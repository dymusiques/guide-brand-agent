#!/usr/bin/env python3
"""Score weekly topic-pack candidates (title + angle + platform fit)."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "integration/handoff/owner-weekly-topic-pack-eval-latest.json"

IP_KW = (
    "法派",
    "品牌",
    "艺术",
    "长笛",
    "强链接",
    "跨界",
    "听见",
    "古典",
    "演奏",
    "IP",
    "creator",
    "商业",
    "叙事",
    "专业",
)
JUDGMENT_KW = ("不要", "不必", "不是", "为什么", "判断", "祛魅", "其实", "反而", "值得")
HOOK_KW = ("？", "?", "原来", "没想到", "竟然", "却")
CTA_KW = ("私信", "咨询", "合作", "订阅", "关键词")


def clip(n: int, lo: int = 0, hi: int = 100) -> int:
    return max(lo, min(hi, n))


def _norm(s: str) -> str:
    return re.sub(r"\s+", "", (s or "").casefold())


def duplicate_penalty(title: str, avoid: list[str]) -> int:
    t = _norm(title)
    if not t:
        return 25
    for a in avoid:
        a_n = _norm(a)
        if not a_n:
            continue
        if t == a_n or t in a_n or a_n in t:
            return 35
        overlap = len(set(t) & set(a_n)) / max(len(set(t)), 1)
        if overlap > 0.65:
            return 22
    return 0


def score_item(item: dict, *, avoid: list[str]) -> dict:
    title = str(item.get("title_zh") or item.get("subject") or "")
    angle = str(item.get("angle_one_liner") or "")
    text = f"{title}\n{angle}"
    plats = item.get("platforms") or item.get("platform_hint") or []
    if isinstance(plats, str):
        plats = [plats]

    ip_hits = sum(1 for k in IP_KW if k in text)
    ip_fit = clip(35 + ip_hits * 8)

    j_hits = sum(1 for k in JUDGMENT_KW if k in text)
    h_hits = sum(1 for k in HOOK_KW if k in title)
    hook = clip(40 + j_hits * 6 + h_hits * 5)

    platform_fit = 50
    if plats:
        platform_fit = clip(55 + min(3, len(plats)) * 12)
    if "linkedin" in [p.casefold() for p in plats] and any(k in text for k in ("品牌", "专业", "cross")):
        platform_fit = clip(platform_fit + 5)

    kind = str(item.get("topic_kind") or item.get("source") or "")
    kind_bonus = 8 if kind in ("hot_trend", "evergreen_ip", "ip_pillar", "chat_spark") else 0

    dup = duplicate_penalty(title, avoid)
    cta = 10 if any(k in str(item.get("strong_link_cta") or "") for k in CTA_KW) else -5

    match = clip(int(0.35 * ip_fit + 0.30 * hook + 0.20 * platform_fit + kind_bonus + cta - dup))

    if match >= 72:
        tier = "A"
    elif match >= 58:
        tier = "B"
    else:
        tier = "C"

    basis = [
        f"IP 信号 {ip_hits}；判断/hook {j_hits}+{h_hits}；平台 {','.join(plats) or '未指定'}。",
        f"撞题惩罚 -{dup}；CTA {'有' if cta > 0 else '弱'}。",
    ]
    if dup >= 22:
        basis.append("WARN 与 pending-eval / 待发标题过近，须改题。")

    return {
        **item,
        "metrics": {
            "match_overall": match,
            "ip_fit": ip_fit,
            "hook_strength": hook,
            "platform_fit": platform_fit,
            "duplicate_penalty": dup,
        },
        "promote_tier": tier,
        "scoring_basis": basis,
        "evaluate_pass": match >= 58 and dup < 35,
    }


def evaluate_items(items: list[dict], *, avoid: list[str]) -> dict:
    scored = [score_item(it, avoid=avoid) for it in items]
    scored.sort(key=lambda x: x["metrics"]["match_overall"], reverse=True)
    for i, it in enumerate(scored, 1):
        it["rank"] = i
    pass_n = sum(1 for it in scored if it.get("evaluate_pass"))
    return {
        "as_of": datetime.now(timezone.utc).isoformat(),
        "schema": "owner_weekly_topic_pack_eval_v1",
        "scoring_model": "rule-weekly-topic-v1-2026-11-17",
        "scoring_formula": "0.35×IP + 0.30×hook + 0.20×平台 + kind/CTA − 撞题",
        "pass_threshold": 58,
        "item_count": len(scored),
        "pass_count": pass_n,
        "status": "PASS" if pass_n >= min(5, len(scored)) else "NEEDS_WORK",
        "items": scored,
        "promote_winner": scored[0].get("title_zh") if scored else None,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--items-json", help="path to JSON array or pack handoff with items[]")
    ap.add_argument("--avoid-json", default="", help="JSON array of titles to avoid")
    ap.add_argument("--out", type=Path, default=OUT)
    args = ap.parse_args()
    if not args.items_json:
        print("FAIL need --items-json", file=sys.stderr)
        return 2
    p = Path(args.items_json)
    raw = json.loads(p.read_text(encoding="utf-8"))
    if isinstance(raw, dict):
        items = raw.get("items") or []
    else:
        items = raw
    avoid: list[str] = []
    if args.avoid_json:
        avoid = json.loads(args.avoid_json)
    elif isinstance(raw, dict) and raw.get("evaluate_baseline", {}).get("avoid_titles_sample"):
        avoid = list(raw["evaluate_baseline"]["avoid_titles_sample"])
    payload = evaluate_items(items, avoid=avoid)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": payload["status"], "pass_count": payload["pass_count"], "out": str(args.out)}))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())