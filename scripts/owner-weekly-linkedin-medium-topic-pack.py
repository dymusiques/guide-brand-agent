#!/usr/bin/env python3
"""Weekly 5–10 topics for LinkedIn + Medium only (phase 0 · no Brief)."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "content/strategy/weekly-li-medium-topic-pack"
HANDOFF = ROOT / "integration/handoff/owner-weekly-li-medium-topic-pack-latest.json"
PHASE = ROOT / "integration/handoff/owner-multichannel-flywheel-phase.json"
IP_BRIEF = ROOT / "content/personal-ip/ip-positioning-brief-2026-10-05.md"
SPARKS = ROOT / "content/personal-ip/chat-sparks"
WEEKLY_EVAL = ROOT / "integration/handoff/owner-weekly-li-medium-topic-eval-latest.json"
PASS_THRESHOLD = 58
sys.path.insert(0, str(ROOT / "scripts"))
from lib.brand_runtime import brand_python, gemini_key_available  # noqa: E402
import importlib.util

_eval_mod_path = ROOT / "scripts/evaluate-weekly-topic-candidates.py"
_spec = importlib.util.spec_from_file_location("evaluate_weekly_topic_candidates", _eval_mod_path)
_eval_mod = importlib.util.module_from_spec(_spec)
assert _spec and _spec.loader
_spec.loader.exec_module(_eval_mod)
evaluate_items = _eval_mod.evaluate_items


def load_sparks() -> list[str]:
    lines: list[str] = []
    if not SPARKS.is_dir():
        return lines
    for p in sorted(SPARKS.glob("20*.md")):
        if p.name.startswith("_"):
            continue
        t = p.read_text(encoding="utf-8", errors="replace")[:600]
        lines.append(f"- [{p.name}] {t[:300].replace(chr(10), ' ')}")
    return lines[:6]


def gemini_expand(*, brief_excerpt: str, sparks: list[str]) -> list[dict]:
    py = brand_python()
    prompt = {
        "task": "weekly_li_medium_topic_pack",
        "count_min": 5,
        "count_max": 10,
        "phase": 0,
        "ip_brief_excerpt": brief_excerpt[:2500],
        "chat_sparks": sparks,
        "each_item_fields": [
            "title_zh",
            "angle_one_liner",
            "primary_platform",
            "linkedin_angle",
            "medium_angle",
            "web_research_hints",
            "why_resonates_now",
            "strong_link_cta",
        ],
        "rules_linkedin": [
            "契合 Owner IP：法派长笛、品牌×艺术、跨行业强链接、credibility 吸引品牌方",
            "专业观察 + 个人判断，可 B2B 合作感，忌硬广清单",
        ],
        "rules_medium": [
            "有思考密度：哲学感、情感共鸣、案例线，读者感到「这人有主见」",
            "可略长、可抒情，但须有结构（论点链）",
        ],
        "rules_common": [
            "primary_platform 只能是 linkedin 或 medium；每条主打一个平台，另一平台可写「改编一句」",
            "web_research_hints 写 Google/新闻/大 V 风向检索词，禁止编造搜索量",
            "禁止写 Brief/正文，只出选题",
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
    contents="Return JSON array only: " + json.dumps(spec, ensure_ascii=False),
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
            return [_normalize_item(x) for x in arr[:10]]
    except json.JSONDecodeError:
        pass
    return []


def _normalize_item(raw: dict) -> dict:
    plat = str(raw.get("primary_platform") or "linkedin").lower()
    if plat not in ("linkedin", "medium"):
        plat = "linkedin" if "领英" in plat or "linked" in plat else "medium"
    return {
        "title_zh": raw.get("title_zh") or "待定题",
        "angle_one_liner": raw.get("angle_one_liner") or "",
        "platforms": [plat],
        "primary_platform": plat,
        "linkedin_angle": raw.get("linkedin_angle") or raw.get("angle_one_liner") or "",
        "medium_angle": raw.get("medium_angle") or raw.get("angle_one_liner") or "",
        "web_research_hints": raw.get("web_research_hints") or raw.get("why_resonates_now") or "待 Web 检索",
        "hot_search_hint": raw.get("web_research_hints") or "待 Web 检索",
        "strong_link_cta": raw.get("strong_link_cta") or "私信/评论关键词",
        "evaluate_baseline_note": f"li-medium · {plat}",
        "source": "gemini",
    }


def template_pack(sparks: list[str]) -> list[dict]:
    base = [
        {
            "title_zh": "品牌方为什么需要「不可替代的艺术专业时刻」",
            "angle_one_liner": "B2B 叙事：活动 IP 里专业背书",
            "platforms": ["linkedin"],
            "primary_platform": "linkedin",
            "linkedin_angle": "案例+判断：艺术 ROI 不是曝光而是信任",
            "medium_angle": "可扩成「商业热爱」长文",
            "web_research_hints": "Google: brand sponsorship arts 2025; LinkedIn 艺术营销",
            "hot_search_hint": "品牌 storytelling arts",
            "strong_link_cta": "私信合作评估",
            "evaluate_baseline_note": "linkedin · brand",
            "source": "template",
        },
        {
            "title_zh": "不需要那么多艺术家，但需要很多热爱艺术的人",
            "angle_one_liner": "哲学向 · 职业身份与热爱",
            "platforms": ["medium"],
            "primary_platform": "medium",
            "linkedin_angle": "可缩成首段 hook",
            "medium_angle": "情感+思辨：热爱如何成为专业护城河",
            "web_research_hints": "Medium culture essays; 创作者 economy 意义感",
            "hot_search_hint": "art passion vs profession",
            "strong_link_cta": "留言你的热爱",
            "evaluate_baseline_note": "medium · philosophy",
            "source": "template",
        },
        {
            "title_zh": "跨界对话：古典音乐 CEO 怎么看 AI 与审美",
            "angle_one_liner": "领英风向 · 科技×人文",
            "platforms": ["linkedin"],
            "primary_platform": "linkedin",
            "linkedin_angle": "强观点短帖 + 邀请品牌对话",
            "medium_angle": "可写长案例线",
            "web_research_hints": "Google News AI arts; LinkedIn 古典音乐 CEO",
            "hot_search_hint": "AI creativity classical",
            "strong_link_cta": "连接/私信",
            "evaluate_baseline_note": "linkedin · trend",
            "source": "template",
        },
        {
            "title_zh": "当孩子学乐器时，父母在谈判什么？",
            "angle_one_liner": "Medium 情感线 · 家庭与教育",
            "platforms": ["medium"],
            "primary_platform": "medium",
            "linkedin_angle": "专业版可写教育品牌洞察",
            "medium_angle": "叙事+哲思：期待、比较、身份",
            "web_research_hints": "parenting music education essays",
            "hot_search_hint": "music parenting identity",
            "strong_link_cta": "分享你的故事",
            "evaluate_baseline_note": "medium · emotion",
            "source": "template",
        },
        {
            "title_zh": "听见 Daily：一条资讯如何变成品牌人的晨读",
            "angle_one_liner": "IP 支柱 · 专业可信度",
            "platforms": ["linkedin"],
            "primary_platform": "linkedin",
            "linkedin_angle": "行业快讯+你的教学法判断",
            "medium_angle": "周度思考合集",
            "web_research_hints": "flute news; classical industry trends",
            "hot_search_hint": "classical music newsletter",
            "strong_link_cta": "订阅/咨询",
            "evaluate_baseline_note": "linkedin · daily",
            "source": "template",
        },
        {
            "title_zh": "强链接：为什么「开放跨界」比垂直涨粉慢却更稳",
            "angle_one_liner": "IP 方法论 · 可复制",
            "platforms": ["medium"],
            "primary_platform": "medium",
            "linkedin_angle": "可发短帖引用 Medium 全文",
            "medium_angle": "论证+故事：开放网络与品牌合作",
            "web_research_hints": "creator open network; personal brand philosophy",
            "hot_search_hint": "open network personal brand",
            "strong_link_cta": "私信方法论",
            "evaluate_baseline_note": "medium · ip",
            "source": "template",
        },
    ]
    if sparks:
        base.append(
            {
                "title_zh": "聊天启发 · 待精修",
                "angle_one_liner": sparks[0][:180],
                "platforms": ["linkedin"],
                "primary_platform": "linkedin",
                "linkedin_angle": "从 spark 提炼品牌向 hook",
                "medium_angle": "可深化成散文",
                "web_research_hints": "见 chat-sparks",
                "hot_search_hint": "spark",
                "strong_link_cta": "待定",
                "evaluate_baseline_note": "spark",
                "source": "chat_spark",
            }
        )
    return base[:10]


def write_md(path: Path, items: list[dict], meta: dict, phase_check: dict | None) -> None:
    lines = [
        f"# LinkedIn + Medium 每周选题 · {meta['week_date']}",
        "",
        f"- 生成：{meta['as_of']}",
        f"- **阶段**：0 · 积攒（只选题不写稿）",
        f"- 条数：**{len(items)}**（请勾选序号）",
        "- Automation **Must** 用 Web 检索补足每条 `web_research_hints`（注明日期）",
        "",
    ]
    if phase_check:
        lines.append(f"- 飞轮自检：`check-owner-flywheel-phase` → {phase_check.get('next_owner_action_zh', '')}")
        lines.append("")
    lines.extend(
        [
            "## 筛选",
            "",
            "- **LinkedIn**：IP 契合 + 能吸引品牌/专业读者",
            "- **Medium**：有思想密度 + 哲学/情感共鸣",
            "",
            "## 选题",
            "",
        ]
    )
    for i, it in enumerate(items, 1):
        plat = it.get("primary_platform") or (it.get("platforms") or ["—"])[0]
        lines.extend(
            [
                f"### {i}. {it.get('title_zh', '—')} · **{plat}**",
                f"- **角度**：{it.get('angle_one_liner', '—')}",
                f"- **LinkedIn 切入点**：{it.get('linkedin_angle', '—')}",
                f"- **Medium 切入点**：{it.get('medium_angle', '—')}",
                f"- **检索/风向**：{it.get('web_research_hints', it.get('hot_search_hint', '—'))}",
                f"- **CTA**：{it.get('strong_link_cta', '—')}",
            ]
        )
        met = it.get("metrics") or {}
        if met:
            lines.append(
                f"- **score**：{met.get('match_overall', '—')} · "
                f"{'PASS' if it.get('evaluate_pass') else 'rework'}"
            )
        lines.append("")
    lines.extend(
        [
            "## Owner 下一步",
            "",
            "1. 回「勾选序号：1,3,5」或「归聊天启发」",
            "2. **阶段 0**：不勾选 = 不写稿",
            "3. 准备金句 → **`进入写稿阶段`** 或 **`派活给 CEO` + 选题** → 全链交付包",
            "",
            "飞轮阶段说明：`docs/OWNER-MULTICHANNEL-FLYWHEEL-PHASES.md`",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def run_phase_check() -> dict | None:
    py = brand_python()
    r = subprocess.run(
        [py, str(ROOT / "scripts/check-owner-flywheel-phase.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=60,
    )
    if r.returncode != 0:
        return None
    try:
        return json.loads((r.stdout or "").strip())
    except json.JSONDecodeError:
        return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=date.today().isoformat())
    ap.add_argument("--min", type=int, default=5)
    ap.add_argument("--max", type=int, default=10)
    ap.add_argument("--no-gemini", action="store_true")
    args = ap.parse_args()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    brief_excerpt = IP_BRIEF.read_text(encoding="utf-8")[:3000] if IP_BRIEF.is_file() else ""
    sparks = load_sparks()
    items: list[dict] = []
    if gemini_key_available() and not args.no_gemini:
        items = gemini_expand(brief_excerpt=brief_excerpt, sparks=sparks)
    if len(items) < args.min:
        items = template_pack(sparks)
    items = items[: args.max]

    eval_payload = evaluate_items(items, avoid=[])
    WEEKLY_EVAL.parent.mkdir(parents=True, exist_ok=True)
    WEEKLY_EVAL.write_text(json.dumps(eval_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    by_title = {i.get("title_zh"): i for i in eval_payload.get("items") or []}
    items = [by_title.get(it.get("title_zh"), it) for it in items]

    phase_check = run_phase_check()
    md_path = OUT_DIR / f"weekly-li-medium-topic-pack-{args.date}.md"
    meta = {"week_date": args.date, "as_of": datetime.now(timezone.utc).isoformat()}
    write_md(md_path, items, meta, phase_check)

    phase_num = 0
    if PHASE.is_file():
        phase_num = int(json.loads(PHASE.read_text(encoding="utf-8")).get("current_phase", 0))

    payload = {
        "schema": "owner_weekly_li_medium_topic_pack_v1",
        "as_of": meta["as_of"],
        "week_date": args.date,
        "flywheel_phase": phase_num,
        "count": len(items),
        "items": items,
        "owner_picked_serials": [],
        "weekly_evaluate": {
            "latest": str(WEEKLY_EVAL.relative_to(ROOT)),
            "status": eval_payload.get("status"),
            "pass_count": eval_payload.get("pass_count"),
            "pass_threshold": PASS_THRESHOLD,
        },
        "phase_readiness": phase_check,
        "outputs": {"markdown": str(md_path.relative_to(ROOT))},
        "next_steps_zh": "Owner 勾选序号；阶段0不写稿；准备满链时说「进入写稿阶段」",
    }
    HANDOFF.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "status": "PASS",
                "count": len(items),
                "markdown": str(md_path.relative_to(ROOT)),
                "phase": phase_num,
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())