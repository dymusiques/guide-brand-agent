#!/usr/bin/env python3
"""Score all pending-videos/*.md → owner-pending-videos-eval-latest.json (count not fixed)."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from pending_video_md_lib import parse_pending_video  # noqa: E402

INBOX = ROOT / "content/xiaohongshu/inbox/pending-videos"
OUT = ROOT / "integration/handoff/owner-pending-videos-eval-latest.json"
PIPELINE = ROOT / "integration/handoff/owner-pending-videos-pipeline.json"
FACTS_MANIFEST = ROOT / "integration/handoff/owner-pending-videos-facts-latest.json"

STORY_KW = (
    "那天",
    "大师",
    "小姑娘",
    "法国",
    "意大利",
    "夏令营",
    "请下来",
    "哈欠",
    "迟到",
    "施南子",
    "Löic",
    "上课",
    "考场",
    "嘲讽",
    "走廊",
    "泰斗",
)
JUDGMENT_KW = ("尊重", "不应该", "不推荐", "审美", "判断", "教养", "没意思", "难吃", "多余")
HOOK_KW = ("?", "？", "原来", "没想到", "其实", "不要", "不必", "OK", "今天")
TECH_MARKERS = re.compile(r"Vibrato|vibrato|Rubato|指法|双吐|节拍器|✅\d+")
FB_KW = ("FluteBuddy", "内测", "裁判", "PDF谱", "扣分", "录屏")
LISTICLE_KW = ("第一", "第二个", "第三个", "三个点", "几点")


def clip(n: int, lo: int = 0, hi: int = 100) -> int:
    return max(lo, min(hi, n))


def read_item(path: Path) -> dict:
    parsed = parse_pending_video(path, ROOT)
    body = parsed.pop("body_stripped")
    title = parsed["title"]
    track = parsed["track"]
    text_path = path.read_text(encoding="utf-8")
    if track == "IP" and any(k in text_path for k in FB_KW):
        track = "FB"

    narrative_facts = parsed["narrative_facts"]
    setting_france = narrative_facts["setting_france"]
    witness = narrative_facts["witness_not_protagonist"] or any(
        k in body for k in ("不是发生在我身上", "看到了整个")
    )
    location_mismatch = narrative_facts["title_location_mismatch"]

    open_150 = body[:150]
    tail_200 = body[-200:] if len(body) > 200 else body
    scan_text = f"{text_path.split('## 口播全文', 1)[0]}\n{body}"

    cjk = parsed["cjk_chars"]
    story_hits = sum(1 for k in STORY_KW if k in scan_text)
    judgment_hits = sum(1 for k in JUDGMENT_KW if k in body)
    has_moment = any(k in body for k in ("迟到", "哈欠", "请下来", "怒了", "发火"))

    story_fit = clip(40 + story_hits * 9 + (25 if has_moment else 0) + judgment_hits * 4)
    data_fit = story_fit
    if TECH_MARKERS.search(body) and not has_moment and judgment_hits < 3:
        data_fit = clip(data_fit - 20)
    if "不需要那么多艺术家" in body or "走专业" in body:
        data_fit = clip(data_fit + 15)
    if has_moment and judgment_hits >= 2:
        data_fit = clip(data_fit + 10)

    hook_lead = sum(7 for k in HOOK_KW if k in open_150)
    hook_tail = sum(5 for k in HOOK_KW if k in tail_200)
    hook = clip(45 + hook_lead + hook_tail)
    if open_150.strip().startswith("OK"):
        hook = clip(hook - 8)
    if witness and judgment_hits >= 2:
        hook = clip(hook + 5)

    completion_risk = 35
    if cjk > 1100:
        completion_risk += 30
    elif cjk > 700:
        completion_risk += 18
    if any(k in body for k in ("朗", "王羽佳", "马斯克", "黄仁勋")):
        completion_risk += 12
    if has_moment and cjk < 900:
        completion_risk = clip(completion_risk - 10, 15, 100)

    ease = 85 if cjk < 500 else (72 if cjk < 900 else 55)
    volume = 80
    if LISTICLE_KW[0] in body or "三个点" in body:
        volume = clip(volume + 5)

    match = round(0.35 * story_fit + 0.35 * data_fit + 0.15 * ease + 0.15 * volume)

    basis: list[str] = [
        f"故事信号 {story_hits} 个关键词；判断信号 {judgment_hits} 个；具体 moment={'有' if has_moment else '弱'}。",
        f"口播约 {cjk} 汉字（小红书口播建议 300–500 字/60–90s；超长抬完播风险 {completion_risk}）。",
        "数据对照：你后台 S 级为「故事+冲突+判断」（泰斗/考场）；纯技巧连载偏弱。",
        f"决策事实（全文）：{parsed['decision_summary']}",
    ]
    if cjk > 700:
        basis.append("建议：剪版去掉重复铺垫，前 3 秒直接进冲突或反常识句。")
    if open_150.strip().startswith("OK"):
        basis.append("开头「OK一说到…」偏聊天口癖，封面+字幕 hook 需另写 6 字。")
    if witness:
        basis.append("叙事：目击者视角（非当事人）— 标题勿写「我让…发火」除非实拍确为自己引发。")
    if setting_france:
        basis.append("地点：法国课堂/夏令营（须与标题一致，勿误标意大利）。")
    if location_mismatch:
        basis.append("WARN 标题含意大利但正文主场景为法国 — 须改标题或文件名。")
        match = clip(match - 15)

    if match >= 78 and completion_risk <= 45:
        promo, promo_note = "A", "自然发 72h 后可选薯条 75–150 元测播放（Drive：内容为1薯条为0）"
    elif match >= 62:
        promo, promo_note = "B", "先自然流；完播达标再试薯条；可先剪短再发"
    else:
        promo, promo_note = "C", "先剪/改 hook；不建议付费加热"

    if track == "FB":
        promo_note += " · 本条为 IP，非 FB 转化向"

    excerpts = parsed["excerpts_for_orientation_only"]
    glance = f"{excerpts['lead_150']} … {excerpts['tail_200']}"

    return {
        **{k: parsed[k] for k in ("id", "file", "title", "track", "sha256", "cjk_chars", "narrative_facts")},
        "metrics": {
            "match_overall": match,
            "story_fit": story_fit,
            "data_fit": data_fit,
            "hook_strength": hook,
            "completion_risk": completion_risk,
            "ease_shoot": ease,
            "volume_priority": volume,
        },
        "scoring_basis": basis,
        "promote_tier": promo,
        "promote_note": promo_note,
        "decision_summary": parsed["decision_summary"],
        "agent_decision_source": FACTS_MANIFEST.relative_to(ROOT).as_posix(),
        "body_reading": parsed["body_reading"],
        "human_glance_only": {
            "preview_concat": re.sub(r"\s+", " ", glance).strip(),
            "not_for_decisions": True,
            "use_instead": FACTS_MANIFEST.relative_to(ROOT).as_posix(),
        },
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--inbox", type=Path, default=INBOX)
    p.add_argument("--out", type=Path, default=OUT)
    args = p.parse_args()
    paths = sorted(args.inbox.glob("*.md"))
    skip = {"readme.md", "template.md"}
    paths = [x for x in paths if x.name.lower() not in skip]
    if not paths:
        payload = {
            "as_of": datetime.now(timezone.utc).isoformat(),
            "status": "empty_inbox",
            "inbox": str(args.inbox.relative_to(ROOT)),
            "items": [],
            "scoring_model": "rule-v2-full-body-2026-11-13",
            "message": "No .md in pending-videos — add scripts then rerun",
            "agent_decision_source": str(FACTS_MANIFEST.relative_to(ROOT)),
            "forbidden_for_agent_decisions": ["body_preview", "human_glance_only"],
        }
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"WARN empty inbox → {args.out}")
        return 0
    items = [read_item(p) for p in paths]
    items.sort(key=lambda x: x["metrics"]["match_overall"], reverse=True)
    for i, it in enumerate(items, 1):
        it["rank"] = i
    payload = {
        "as_of": datetime.now(timezone.utc).isoformat(),
        "status": "ok",
        "scoring_model": "rule-v2-full-body-2026-11-13",
        "scoring_formula": "0.35×故事 + 0.35×数据像 + 0.15×好发 + 0.15×提量",
        "pipeline": str(PIPELINE.relative_to(ROOT)),
        "inbox": str(args.inbox.relative_to(ROOT)),
        "item_count": len(items),
        "items": items,
        "promote_winner": items[0]["id"] if items else None,
        "agent_decision_source": str(FACTS_MANIFEST.relative_to(ROOT)),
        "forbidden_for_agent_decisions": ["body_preview", "human_glance_only"],
        "agent_advice_gate_script": "scripts/agent-gate-pending-videos-advice.py",
        "drive_refs": ["content/personal-ip/intake/_cache/drive-ref/如何投放好小红书薯条.md"],
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"OK {len(items)} items → {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
