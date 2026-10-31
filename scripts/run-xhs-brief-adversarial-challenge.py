#!/usr/bin/env python3
"""Per-Brief heavy adversarial challenge (Must before Owner / complete gate).

Generates content/xiaohongshu/challenge/<slug>-challenge.md (+ optional HTML).
Sections: external/saturation, other-IP crossover, FULL-DRILL multi-GM, fusion, L2-L3.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHALLENGE_DIR = ROOT / "content/xiaohongshu/challenge"
HTML_DIR = ROOT / "content/evolution/00-manager/ceo-inbox/challenge-html"
XHS = ROOT / "content/xiaohongshu"
sys.path.insert(0, str(ROOT / "kernels/xiaohongshu"))

from challenge_brief_schema import validate_challenge_markdown  # noqa: E402

sys.path.insert(0, str(ROOT / "scripts"))
from xhs_brief_longform import extract_longform_text  # noqa: E402
from xhs_clever_advocate import analyze_clever_advocate  # noqa: E402

MARKER = "<!-- xhs-classifier -->"
IP_BRIEF = ROOT / "content/personal-ip/ip-positioning-brief-2026-10-05.md"

# Known external pressure (curated; Agent refreshes dates in header)
EXTERNAL_BENCHMARKS = """
| 账号/类型 | 压力 |
|-----------|------|
| 活动加油站 · 品牌活动拆解 | 具体品牌+视觉+数据标题；纯观点难打 |
| SAGE HOUSE / Somexing · 艺术×品牌机构 | 机构案例视频；你需「人即品牌+训练背书」 |
| 平台官方叙事 · 打卡/装置/美 | 正当化装饰；你反装饰须补「专业 moment 也可拍」 |
| 同类低点击形态 | #品牌策划 短观点、无 moment/无封面判断句 |
"""

FULL_DRILL_ATTACKS = """
### 00 CEO
- 「verify 全绿，**App 零发布** — 在用 aligned 代替生意？」

### 01 personal-ip
- 「**法派+跨界形容词堆满**，签单理由一句没有 — 履历 IP？」
- 「pivot 审美 vs 旧技巧帖 — **定位漂移第几轮？**」

### 04 xhs-topic
- 「**evaluate 过了** 但像 consultant，**像本人吗？**」
- 「追故事帖数据，**认知期名片帖永远不发**。」

### 05 kernel 盲点
- 「标题筛错人 · 高 CTR 低完播 · 空泛私信合作 **无 moment** — aligned 仍 yes？」

### 09 analytics
- 「没对照 **notes.csv** 钩子结构就写 Brief — 数据装饰？」
"""


def extract_brief(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if MARKER not in text:
        raise ValueError(f"missing classifier: {path}")
    after = text.split(MARKER, 1)[1]
    m = re.search(r"```(?:json)?\s*\n([\s\S]*?)\n```", after)
    data = json.loads(m.group(1).strip())
    return {"subject": str(data.get("subject") or ""), "body": str(data.get("body") or ""), "file": path.name}


def slug_base(brief: Path) -> str:
    return brief.name.replace("-brief.md", "")


def gemini_crossover(subject: str, body: str) -> str:
    """Optional: 3 hard 'other IP' attack lines."""
    try:
        sys.path.insert(0, str(ROOT / "kernels/xiaohongshu"))
        sys.path.insert(0, str(ROOT / "kernels/xiaohongshu/line2"))
        from google import genai
        from google.genai import types

        from config.gemini_config import get_api_key, get_model

        prompt = (
            "你是红队：模拟小红书「艺术×品牌」赛道里机构号、活动拆解号、教学号对下列笔记的"
            "**极挑战性**三句攻击（每句≤40字，中文，具体可验证）。不要安慰，不要改稿。\n\n"
            f"标题：{subject}\n正文：{body[:2000]}\n\n"
            "输出格式：\n1. …\n2. …\n3. …"
        )
        client = genai.Client(api_key=get_api_key())
        r = client.models.generate_content(
            model=get_model(),
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.3, max_output_tokens=512),
        )
        t = (r.text or "").strip()
        if t:
            return t
    except Exception as exc:
        return f"_（Gemini 对打句跳过：{exc}）_\n\n"
    return ""


def fusion_checks(subject: str, body: str) -> str:
    combined = subject + body
    rows = []
    # L2 · 难自动纠：关键词过 gate 但无案例（X2/X11）
    case_markers = (
        "NGV", "Cartier", "MSO", "百富", "Frieze", "RCM", "Gandel",
        "Microsoft", "British Museum", "White Cube", "某夜", "我不点名",
    )
    has_named_case = any(m in combined for m in case_markers) or re.search(
        r"[A-Z]{2,}|[\u4e00-\u9fff]{2,6}(展|夜|馆|厅|发布)", combined
    )
    platitude_title = any(
        p in subject for p in ("什么是", "买的到底是啥", "到底在干什么", "如何理解")
    )
    checks = [
        ("三镜头 · 可辨认案例（L2）", has_named_case and not platitude_title),
        ("跨行业 open · 不绑单品类", any(x in combined for x in ("跨行业", "品类", "open", "不绑")) or "家居" not in combined),
        ("强链接 CTA", any(x in combined for x in ("私信", "聊聊", "收藏", "合作"))),
        ("认知期 · 价值判断非硬推销", "体验季" not in combined and "报价" not in combined),
        ("trade-off 或隐患（L2）", any(x in combined for x in ("隐患", "洗艺", "代价", "得罪", "会丢", "翻车", "壁纸", "wallpaper"))),
        ("约课非 KPI", "评估" not in subject and "约课" not in subject),
    ]
    for label, ok in checks:
        rows.append(f"| {label} | {'✅' if ok else '⚠️ 待加强'} |")
    return "\n".join(rows)


def build_challenge(brief: Path, use_gemini: bool = True) -> str:
    note = extract_brief(brief)
    sub, body = note["subject"], note["body"]
    base = slug_base(brief)
    redteam = XHS / "redteam" / f"{base}-pre.md"
    redteam_excerpt = ""
    if redteam.is_file():
        redteam_excerpt = redteam.read_text(encoding="utf-8")[:800]

    crossover = ""
    if use_gemini:
        crossover = gemini_crossover(sub, body)
    if not crossover.strip() or crossover.startswith("_（Gemini"):
        crossover = (
            "1. 机构号：「又一个讲艺术营销的，**案例呢？** 数据呢？」\n"
            "2. 活动拆解号：「**命题撞车** — 我们上周刚发过品牌活动结构。」\n"
            "3. 路人粉：「法派长笛？**关我品牌什么事** — 划走。」"
        )

    lf = extract_longform_text(brief)
    clever = analyze_clever_advocate(lf or "")
    clever_rows = (
        f"| 反方席小节 | {'✅' if clever['has_clever_section'] else '⚠️ 缺 杠精席/Clever'} |\n"
        f"| 反方人设 ≥{clever['min_personas']} | {'✅' if clever['persona_count'] >= clever['min_personas'] else '⚠️'} · n={clever['persona_count']} |\n"
        f"| 作者收束（收进包里/回杠） | {'✅' if clever['has_author_rebuttal'] else '⚠️'} |"
    )

    today = datetime.now().strftime("%Y-%m-%d %H:%M")
    doc = f"""# Adversarial challenge · {base} · {today}

> **Must 节：** 交 Owner / complete gate 前自动生成 · `run-xhs-brief-adversarial-challenge.py`  
> Brief: `{brief.relative_to(ROOT)}` · 标题：**{sub}**

## 外部 · 类似命题 / 大 V 压力

{EXTERNAL_BENCHMARKS}

**本篇命题：** 「{sub}」→ 若仅抽象判断、无 moment/封面判断句，易落入「类似但点击一般」。

## 其它 IP 产出 · 对打句

{crossover}

## FULL-DRILL · 多 GM 攻击

{FULL_DRILL_ATTACKS}

**redteam-pre 摘录：**

```
{redteam_excerpt or "（缺 redteam-pre — ensure-redteam-pre.py 应先跑）"}
```

## 与 ip-positioning 融合

| 红线 | 本篇 |
|------|------|
{fusion_checks(sub, body)}

## Clever · 长稿多网红反方（Must · OWNER-LONGFORM-CLEVER-ADVOCATE）

| 检查 | 结果 |
|------|------|
{clever_rows}

**Must：** 长稿含 ≥4 个 `**反方·…**` 立场 + 「收进包里」式收束 · 见 `verify-xhs-clever-advocate.sh` · CEO triple-eval / double-stress 已编排。

## L2–L3 隐蔽风险

- **L2：** aligned 通过但标题吸引泛粉 → 品牌 DM 不增（09 口径）。
- **L2：** 与 discovery 系列相邻篇 **语义重叠** → 连发疲劳。
- **L3：** 反「装饰」与平台 **打卡美学** 冲突 → 封面双标风险。
- **L3：** 无匿名案例锚点 → 被读成 generic consultant opinion。

## 驳/改 · 必做项

- [ ] 前 3 行：**具体 moment** 或冲突（对照 xhs-data-strategy）
- [ ] 标签 10 个 · 封面文字海报 · 人设层不绑垂直
- [ ] 改后重跑：`evaluate-xhs-brief-complete.py` + 本 challenge 刷新

"""
    ok, errs = validate_challenge_markdown(doc)
    if not ok:
        doc += "\n<!-- schema WARN: " + "; ".join(errs) + " -->\n"
    return doc


def write_html(md_path: Path, md_text: str) -> Path:
    HTML_DIR.mkdir(parents=True, exist_ok=True)
    out = HTML_DIR / (md_path.stem + ".html")
    body = md_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    body = re.sub(r"^### (.+)$", r"<h3>\1</h3>", body, flags=re.M)
    body = re.sub(r"^## (.+)$", r"<h2>\1</h2>", body, flags=re.M)
    body = re.sub(r"^# (.+)$", r"<h1>\1</h1>", body, flags=re.M)
    body = body.replace("\n", "<br>\n")
    html = f"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"/>
<title>{md_path.stem}</title>
<style>body{{font-family:-apple-system,"PingFang SC",sans-serif;max-width:820px;margin:24px auto;padding:16px;line-height:1.5}}</style>
</head><body>{body}</body></html>"""
    out.write_text(html, encoding="utf-8")
    return out


def process_brief(brief: Path, use_gemini: bool) -> tuple[bool, Path]:
    CHALLENGE_DIR.mkdir(parents=True, exist_ok=True)
    base = slug_base(brief)
    out = CHALLENGE_DIR / f"{base}-challenge.md"
    text = build_challenge(brief, use_gemini=use_gemini)
    out.write_text(text, encoding="utf-8")
    write_html(out, text)
    ok, errs = validate_challenge_markdown(text)
    if not ok:
        print(f"FAIL schema {brief.name}: {errs}", file=sys.stderr)
    return ok, out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--brief", type=Path, action="append", default=[])
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--no-gemini", action="store_true")
    args = ap.parse_args()
    briefs: list[Path] = []
    if args.all:
        briefs = sorted(XHS.glob("*-brief.md"))
    for b in args.brief:
        briefs.append(b if b.is_absolute() else ROOT / b)
    if not briefs:
        ap.error("--brief or --all")
    use_gemini = not args.no_gemini
    fail = 0
    for b in briefs:
        if not b.is_file():
            print(f"FAIL missing {b}", file=sys.stderr)
            fail += 1
            continue
        ok, path = process_brief(b, use_gemini)
        print(f"{'PASS' if ok else 'FAIL'} challenge → {path.relative_to(ROOT)}")
        if not ok:
            fail += 1
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
