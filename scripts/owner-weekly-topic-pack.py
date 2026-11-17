#!/usr/bin/env python3
"""Weekly 5–10 topic packs · IP + analytics baseline + optional Gemini hot-angle."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "content/strategy/weekly-topic-pack"
HANDOFF = ROOT / "integration/handoff/owner-weekly-topic-pack-latest.json"
TRIGGERS = ROOT / "integration/handoff/owner-owner-triggers.json"
IP_BRIEF = ROOT / "content/personal-ip/ip-positioning-brief-2026-10-05.md"
SPARKS = ROOT / "content/personal-ip/chat-sparks"
EVAL_LATEST = ROOT / "integration/handoff/owner-pending-videos-eval-latest.json"
EVAL_BASELINE = ROOT / "integration/handoff/owner-pending-videos-eval-baseline.json"
DISTANCE = ROOT / "integration/handoff/owner-pending-eval-version-distance.json"
sys.path.insert(0, str(ROOT / "scripts"))
from lib.brand_runtime import brand_python, gemini_key_available  # noqa: E402


def load_sparks() -> list[str]:
    lines: list[str] = []
    if not SPARKS.is_dir():
        return lines
    for p in sorted(SPARKS.glob("20*.md")):
        if p.name.startswith("_"):
            continue
        t = p.read_text(encoding="utf-8", errors="replace")[:800]
        lines.append(f"- [{p.name}] {t[:400].replace(chr(10), ' ')}")
    return lines[:8]


def pending_topics_avoid() -> list[str]:
    avoid: list[str] = []
    for hp in (EVAL_LATEST, EVAL_BASELINE):
        if not hp.is_file():
            continue
        data = json.loads(hp.read_text(encoding="utf-8"))
        for item in data.get("items") or []:
            title = str(item.get("title") or item.get("subject") or "")[:120]
            if title:
                avoid.append(title)
    return avoid[:30]


def analytics_seeds() -> list[dict]:
    py = brand_python()
    r = subprocess.run(
        [py, str(ROOT / "scripts/analytics-summarize.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    derived = ROOT / "content/analytics/derived"
    latest = sorted(derived.glob("next-topics-*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    seeds: list[dict] = []
    if latest:
        text = latest[0].read_text(encoding="utf-8")
        for m in re.finditer(r"^\d+\.\s+\*\*(.+?)\*\*", text, re.M):
            seeds.append({"subject": m.group(1).strip(), "source": "analytics", "platform_hint": ["xiaohongshu"]})
    if not seeds and r.returncode != 0:
        seeds = [
            {
                "subject": "跨界品牌如何把艺术专业度做成强链接",
                "source": "ip_default",
                "platform_hint": ["xiaohongshu", "linkedin"],
            },
            {
                "subject": "古典音乐家做 IP：热爱 vs 市场需要的艺术家",
                "source": "ip_default",
                "platform_hint": ["medium", "linkedin"],
            },
        ]
    return seeds


def gemini_expand(*, brief_excerpt: str, seeds: list[dict], sparks: list[str], avoid: list[str]) -> list[dict]:
    py = brand_python()
    prompt = {
        "task": "weekly_topic_pack",
        "count_min": 5,
        "count_max": 10,
        "ip_brief_excerpt": brief_excerpt[:2500],
        "analytics_seeds": seeds,
        "chat_sparks": sparks,
        "avoid_duplicate_titles": avoid,
        "each_item_fields": [
            "title_zh",
            "angle_one_liner",
            "platforms",
            "hot_search_hint",
            "strong_link_cta",
            "evaluate_baseline_note",
        ],
        "platforms_allowed": ["xiaohongshu", "linkedin", "medium"],
        "rules": [
            "跨行业品牌 open",
            "法派长笛+品牌叙事+强链接",
            "每条标注 topic_kind: hot_trend | evergreen_ip | spark_derived",
            "hot_trend: 热点/检索向；evergreen_ip: 非热点但契合 IP、值得写；均需 Agent 延伸思考一句",
            "hot_search_hint 须写可验证方向或「待 Web 检索」；禁止编造搜索量数字",
            "平台建议 xiaohongshu/linkedin/medium 可多选并说明为何",
        ],
    }
    payload = json.dumps(prompt, ensure_ascii=False)
    code = f"""
import json, os
from google import genai
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path({str(ROOT)!r}) / ".env")
key = os.environ.get("GEMINI_API_KEY", "")
if not key:
    raise SystemExit(2)
client = genai.Client(api_key=key)
spec = json.loads({json.dumps(payload)})
resp = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Return JSON array only, no markdown: " + json.dumps(spec, ensure_ascii=False),
)
text = (resp.text or "").strip()
if text.startswith("```"):
    parts = text.split("```")
    text = parts[1] if len(parts) > 1 else text
    if text.lstrip().startswith("json"):
        text = text.split(chr(10), 1)[-1]
print(text.strip())
"""
    r = subprocess.run([py, "-c", code], cwd=ROOT, capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        return []
    try:
        arr = json.loads((r.stdout or "").strip())
        if isinstance(arr, list):
            return arr[:10]
    except json.JSONDecodeError:
        pass
    return []


def template_pack(seeds: list[dict], sparks: list[str]) -> list[dict]:
    base = [
        {
            "title_zh": s.get("subject", "主题"),
            "angle_one_liner": "延续数据支柱 + Owner 观点",
            "platforms": s.get("platform_hint") or ["xiaohongshu"],
            "hot_search_hint": "周日 Automation 可补 Web 检索",
            "strong_link_cta": "私信关键词合作/评估",
            "evaluate_baseline_note": "对标 pending-eval 勿重复标题",
            "source": s.get("source", "template"),
        }
        for s in seeds
    ]
    extras = [
        {
            "title_zh": "听见 Daily：一条可转 LinkedIn 的专业资讯角度",
            "angle_one_liner": "长笛/古典行业快讯 + 教学法观点",
            "platforms": ["linkedin", "medium"],
            "hot_search_hint": "古典音乐 + 教育",
            "strong_link_cta": "订阅/咨询",
            "evaluate_baseline_note": "11 ip-daily",
            "source": "ip_pillar",
        },
        {
            "title_zh": "小红书：品牌活动里「不可替代的专业时刻」",
            "angle_one_liner": "认知期 Discovery 线",
            "platforms": ["xiaohongshu"],
            "hot_search_hint": "品牌 storytelling",
            "strong_link_cta": "私信案例",
            "evaluate_baseline_note": "04 brief 候选",
            "source": "ip_pillar",
        },
    ]
    out = base + extras
    if sparks:
        out.append(
            {
                "title_zh": "聊天启发衍生题（待 Owner 定方向）",
                "angle_one_liner": sparks[0][:200],
                "platforms": ["xiaohongshu", "linkedin", "medium"],
                "hot_search_hint": "见 chat-sparks",
                "strong_link_cta": "待定",
                "evaluate_baseline_note": "spark",
                "source": "chat_spark",
            }
        )
    while len(out) < 5:
        out.append(
            {
                "title_zh": f"IP 储备题 #{len(out)+1}",
                "angle_one_liner": "法派×商业×艺术体验",
                "platforms": ["linkedin"],
                "hot_search_hint": "待检索",
                "strong_link_cta": "私信",
                "evaluate_baseline_note": "placeholder",
                "source": "fill",
            }
        )
    return out[:10]


def write_md(path: Path, items: list[dict], meta: dict) -> None:
    lines = [
        f"# 每周选题包 · {meta['week_date']}",
        "",
        f"- 生成：{meta['as_of']}",
        f"- 条数：**{len(items)}**（Owner 自选 LinkedIn / 小红书 / Medium）",
        f"- 真源：`integration/handoff/owner-owner-triggers.json` · evaluate baseline 已读",
        "",
        "## 筛选标准",
        "",
        "1. IP：法派、品牌×艺术、强链接、跨行业 open",
        "2. 热点：脚本/Gemini 给出方向；Automation 内 Agent 应用 Web 检索佐证",
        "3. 不与 pending-eval 标题重复",
        "",
        "## 选题",
        "",
    ]
    for i, it in enumerate(items, 1):
        plats = it.get("platforms") or it.get("platform_hint") or []
        if isinstance(plats, str):
            plats = [plats]
        lines.extend(
            [
                f"### {i}. {it.get('title_zh', it.get('subject', '—'))}",
                f"- **角度**：{it.get('angle_one_liner', '—')}",
                f"- **建议平台**：{', '.join(plats)}",
                f"- **热点/检索**：{it.get('hot_search_hint', '—')}",
                f"- **强链接 CTA**：{it.get('strong_link_cta', '—')}",
                f"- **evaluate baseline**：{it.get('evaluate_baseline_note', '—')}",
                "",
            ]
        )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=date.today().isoformat())
    ap.add_argument("--min", type=int, default=5)
    ap.add_argument("--max", type=int, default=10)
    ap.add_argument("--no-gemini", action="store_true")
    args = ap.parse_args()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    brief_excerpt = IP_BRIEF.read_text(encoding="utf-8")[:3000] if IP_BRIEF.is_file() else ""
    seeds = analytics_seeds()
    sparks = load_sparks()
    avoid = pending_topics_avoid()
    distance_note = None
    if DISTANCE.is_file():
        distance_note = json.loads(DISTANCE.read_text(encoding="utf-8")).get("distance")

    items: list[dict] = []
    if gemini_key_available() and not args.no_gemini:
        items = gemini_expand(brief_excerpt=brief_excerpt, seeds=seeds, sparks=sparks, avoid=avoid)
    if len(items) < args.min:
        items = template_pack(seeds, sparks)

    items = items[: args.max]
    if len(items) < args.min:
        print(f"WARN only {len(items)} topics", file=sys.stderr)

    md_path = OUT_DIR / f"weekly-topic-pack-{args.date}.md"
    meta = {"week_date": args.date, "as_of": datetime.now(timezone.utc).isoformat()}
    write_md(md_path, items, meta)

    payload = {
        "schema": "owner_weekly_topic_pack_v1",
        "as_of": meta["as_of"],
        "week_date": args.date,
        "count": len(items),
        "items": items,
        "evaluate_baseline": {
            "avoid_titles_sample": avoid[:10],
            "distance": distance_note,
        },
        "outputs": {
            "markdown": str(md_path.relative_to(ROOT)),
            "analytics_derived": "content/analytics/derived/next-topics-*.md",
        },
        "next_steps_zh": "Owner 勾选 → 派活给 CEO 或 04 写 Brief → gate → evaluate",
    }
    HANDOFF.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "count": len(items), "markdown": str(md_path.relative_to(ROOT))}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())