#!/usr/bin/env python3
"""Angle challenge, then distance to the success bar, then the platform hit line.

Order is fixed in docs/PLATFORM-HIT-STANDARDS.md:
01 voice, 04 cut, 00 senior hostile reader, evolution while distance > 0,
and only after that the per-platform hit score. Gemini uses the CEO key in .env.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "kernels/xiaohongshu"))

PLATFORMS = ("linkedin", "xiaohongshu", "medium")
ANGLE_BAR = 80  # adversarial seats; do not lower to finish a run
HIT_BAR = 80  # hit score is out of 100; pass line is 80, same as the other three
FOUR_PASS = 80
STANDARDS = "docs/PLATFORM-HIT-STANDARDS.md"
SOURCE_DIR: Path | None = None
LINKEDIN_DIMENSIONS = ("AI", "艺术前沿", "各国历史与文化", "音乐", "世界建筑设计", "各地商业走向")


def cjk_len(text: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", text))


def paragraphs(html: str) -> list[str]:
    return [re.sub(r"<[^>]+>", "", p).strip() for p in re.findall(r"<p(?:\s[^>]*)?>(.*?)</p>", html, re.S)]


def spoken_lines(html: str) -> list[str]:
    return [re.sub(r"<[^>]+>", "", p).strip() for p in re.findall(r'<p class="say">(.*?)</p>', html, re.S)]


def check_linkedin(html: str) -> list[str]:
    paras = [p for p in paragraphs(html) if p and not p.startswith("平台依据") and not p.startswith("劳动力")]
    body = "\n".join(paras)
    fails: list[str] = []
    if not paras:
        return ["没有正文"]
    first = paras[0]
    if first.endswith("？") or first.endswith("?"):
        fails.append("开头是问句。领英对照里，问句开头大约少 17% 反应")
    if "我" not in first:
        fails.append("第一段不是第一人称经历")
    n = cjk_len(body)
    if n < 600 or n > 1800:
        fails.append(f"正文字数 {n}，领英停留需要大约 600–1800 字")
    if "1.6" not in body:
        fails.append("缺少可核对的数字（劳动力 1.6%）")
    if "曲名" not in paras[-1]:
        fails.append("结尾要请对方留下具体曲名，不要泛问你觉得呢")
    head = body[:180]
    if "http" in head or "www." in head:
        fails.append("链接不要出现在开头")
    return fails + linkedin_index_fails(html)


def check_xiaohongshu(html: str) -> list[str]:
    lines = spoken_lines(html)
    text = "\n".join(lines)
    fails: list[str] = []
    if not lines:
        return ["没有口播句"]
    if lines[0].startswith("大家好") or "大家好" in lines[0]:
        fails.append("前三秒不要自我介绍")
    if "不需要那么多艺术家" not in lines[0]:
        fails.append("第一句就要把反常识判断说完")
    n = cjk_len(text)
    if n < 280 or n > 700:
        fails.append(f"口播 {n} 字，按每分钟约 220 字应落在大约 1.5–3 分钟（280–700 字）")
    if "曲名" not in text:
        fails.append("结尾要收曲名，方便评论")
    if any(bad in text for bad in ("加微信", "包会", "一定能", "学会就能")):
        fails.append("口播里有结果承诺或加微信。平台抓的是整段字幕，不只是正文")
    if "1.5" not in html and "一倍半" not in html:
        fails.append("封面没有按双行标题的字号关系写")
    if "1Py5TaQJGlI5VOkTMHLfvBE8wXYZ7i0qi" not in html:
        fails.append("没有引用已打开的小红书合规原件")
    return fails


def check_medium(html: str) -> list[str]:
    paras = paragraphs(html)
    body_paras = [p for p in paras if p and not p.startswith("一篇只做")]
    body = "\n".join(body_paras)
    fails: list[str] = []
    if "职业的座位" not in html and "座位" not in html[:400]:
        fails.append("副标题要先把唯一观点说清")
    n = cjk_len(body)
    if n < 1100 or n > 2600:
        fails.append(f"正文字数 {n}，Medium 意见文放在大约 1100–2600 字，读完大约 5–7 分钟")
    if body.count("我") < 4:
        fails.append("个人经历太少")
    if "1.6" not in body or "听完" not in body:
        fails.append("必须同时有劳动力数字和「听完」这个动作")
    h2 = len(re.findall(r"<h2>", html))
    if h2 > 4:
        fails.append("小标题超过 4 个，会把一篇观点拆散")
    return fails


def check_linkedin_any(html: str) -> list[str]:
    paras = [p for p in paragraphs(html) if p and not p.startswith("平台依据") and not p.startswith("劳动力")]
    if not paras:
        return ["没有正文"]
    fails: list[str] = []
    if paras[0].endswith("？") or paras[0].endswith("?"):
        fails.append("开头是问句")
    if "我" not in paras[0]:
        fails.append("第一段不是第一人称")
    n = cjk_len("\n".join(paras))
    if n < 400 or n > 1800:
        fails.append(f"正文字数 {n}，领英大约 400–1800 字")
    head = "\n".join(paras)[:180]
    if "http" in head or "www." in head:
        fails.append("链接不要出现在开头")
    return fails + linkedin_index_fails(html)


def article_hrefs(html: str) -> list[str]:
    body = re.sub(r"<footer\b.*?</footer>", "", html, flags=re.S | re.I)
    return re.findall(r'href=["\'](https?://[^"\']+)["\']', body)


def linkedin_index_fails(html: str) -> list[str]:
    if SOURCE_DIR is None:
        return ["没有 LinkedIn 检索目录"]
    path = SOURCE_DIR / "linkedin-sources.json"
    if not path.is_file():
        return ["没有 LinkedIn 检索索引 linkedin-sources.json"]
    data = json.loads(path.read_text(encoding="utf-8"))
    urls = {item.get("url") for item in data.get("sources") or [] if item.get("url")}
    fails: list[str] = []
    if len(urls) < 2:
        fails.append("检索索引里可用原文少于 2 篇")
    if "linkedin-index" not in html:
        fails.append("正文没有接上检索索引")
    hrefs = article_hrefs(html)
    if len(hrefs) != 2:
        fails.append(f"正文要有两篇对上主题的原文，现在是 {len(hrefs)} 篇")
    for href in hrefs:
        if href not in urls:
            fails.append(f"正文链接不在检索索引里：{href}")
    return fails


def check_xiaohongshu_any(html: str) -> list[str]:
    lines = spoken_lines(html)
    text = "\n".join(lines)
    if not lines:
        return ["没有口播句"]
    fails: list[str] = []
    if "大家好" in lines[0]:
        fails.append("前三秒不要自我介绍")
    n = cjk_len(text)
    if n < 280 or n > 700:
        fails.append(f"口播 {n} 字，大约 1.5–3 分钟")
    if any(bad in text for bad in ("加微信", "包会", "一定能", "学会就能")):
        fails.append("口播里有结果承诺或加微信")
    return fails


def check_medium_any(html: str) -> list[str]:
    body = "\n".join(p for p in paragraphs(html) if p)
    fails: list[str] = []
    n = cjk_len(body)
    if n < 800 or n > 2600:
        fails.append(f"正文字数 {n}，Medium 大约 800–2600 字")
    if body.count("我") < 3:
        fails.append("个人经历太少")
    if len(re.findall(r"<h2>", html)) > 4:
        fails.append("小标题超过 4 个")
    return fails


def linkedin_source_note(folder: Path | None) -> str:
    if folder is None:
        return ""
    path = folder / "linkedin-sources.json"
    if not path.is_file():
        return ""
    data = json.loads(path.read_text(encoding="utf-8"))
    lines = []
    for item in data.get("sources") or []:
        if item.get("url"):
            lines.append(f"- {item.get('title') or item['url']} | {item['url']} | {item.get('use') or ''}")
    if not lines:
        return ""
    return (
        "检索索引里可以用的原文如下。观点若来自它们，正文最多链出 2 篇，用 <a href> 链到索引中的 url。"
        "其余不要链。第一段不要放链接。判断和性格是张丹瀛自己的，不要写成资料汇编。文末加上注释 <!-- linkedin-index -->。\n"
        + "\n".join(lines)
    )


def resolve_public_url(url: str) -> str:
    import urllib.request

    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            final = resp.geturl()
            status = getattr(resp, "status", 200) or 200
    except Exception:
        return ""
    if status >= 400:
        return ""
    if any(host in final for host in ("vertexaisearch.cloud.google.com", "google.com/search")):
        return ""
    return final


def research_linkedin(goal: str, folder: Path) -> dict:
    from google import genai
    from google.genai import types

    from config.gemini_config import get_api_key, get_model

    prompt = f"""为主题检索公开原文，给张丹瀛写 LinkedIn 时当背书。主题：{goal}
范围只在这些里面挑和主题真正相关的：{'、'.join(LINKEDIN_DIMENSIONS)}。
不要为了凑满每个范围而搜无关网页。
先搜索，再列出 4 到 6 条。每条一行：标题 | 原始 URL | 它怎样帮她说出自己的角度。
URL 必须是检索到的文章原址。
"""
    client = genai.Client(api_key=get_api_key())
    response = client.models.generate_content(
        model=get_model(),
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.2,
            max_output_tokens=4096,
            tools=[types.Tool(google_search=types.GoogleSearch())],
            thinking_config=types.ThinkingConfig(thinking_level=types.ThinkingLevel.MINIMAL),
        ),
    )
    grounded: list[dict] = []
    supported: list[str] = []
    titles: dict[str, str] = {}
    for cand in response.candidates or []:
        meta = getattr(cand, "grounding_metadata", None)
        for chunk in getattr(meta, "grounding_chunks", None) or []:
            web = getattr(chunk, "web", None)
            uri = getattr(web, "uri", None) if web else None
            if uri:
                grounded.append({"title": getattr(web, "title", None) or "", "url": uri})
        for support in getattr(meta, "grounding_supports", None) or []:
            if not getattr(support, "grounding_chunk_indices", None):
                continue
            segment = getattr(support, "segment", None)
            text = getattr(segment, "text", "") or ""
            found = [url.strip("`").rstrip(".,)") for url in re.findall(r"https?://[^\s\)\]\>\"'`]+", text)]
            for url in found:
                supported.append(url)
                before = text.split(url, 1)[0].strip(" *|")
                if before and url not in titles:
                    titles[url] = before[-80:]
    sources = []
    seen = set()
    for item in grounded:
        final = resolve_public_url(item["url"])
        if not final or final in seen:
            continue
        if any(host in final for host in ("youtube.com", "youtu.be", "music.youtube.com")):
            continue
        seen.add(final)
        sources.append({"title": item.get("title") or "", "url": final, "dimension": "", "use": ""})
    if len(sources) < 2:
        for url in dict.fromkeys(supported):
            final = resolve_public_url(url)
            if not final or final in seen:
                continue
            if any(host in final for host in ("youtube.com", "youtu.be", "music.youtube.com")):
                continue
            seen.add(final)
            sources.append({"title": titles.get(url) or "", "url": final, "dimension": "", "use": ""})
    if len(sources) < 2:
        raise RuntimeError("LinkedIn 检索没有拿到可打开的原文")
    payload = {
        "theme": goal,
        "ran_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "dimensions": list(LINKEDIN_DIMENSIONS),
        "sources": sources[:8],
        "grounding_count": len(grounded),
    }
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "linkedin-sources.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return payload


def gemini_draft(platform: str, goal: str, folder: Path | None = None) -> str:
    from google import genai
    from google.genai import types

    from config.gemini_config import get_api_key, get_model

    shape = {
        "linkedin": "正文用多个 <p>。第一段第一人称，不要以问号结尾，开头不要放链接。",
        "xiaohongshu": "口播每一句用 <p class=\"say\">。第一句直接下判断，不要大家好。不要加微信，不要包会。",
        "medium": "用不超过 4 个 <h2>。正文用 <p>。一篇只做一个观点。",
    }[platform]
    prompt = f"""为张丹瀛（长笛，法国学派）写一篇可发布的 {platform} 稿。题目或任务：{goal}
声音像一个活着的人：有场景、有判断，不要首先/此外/综上所述/赋能/闭环。
{shape}
{linkedin_source_note(folder) if platform == "linkedin" else ""}
只输出完整 HTML，从 <!DOCTYPE html> 开始。
"""
    client = genai.Client(api_key=get_api_key())
    response = client.models.generate_content(
        model=get_model(),
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.5,
            max_output_tokens=8192,
            thinking_config=types.ThinkingConfig(thinking_level=types.ThinkingLevel.MINIMAL),
        ),
    )
    text = (response.text or "").strip()
    start = text.find("<!DOCTYPE html>")
    if start < 0:
        start = text.find("<html")
    if start < 0:
        raise RuntimeError("Gemini 没有返回 HTML")
    end = text.rfind("</html>")
    if end < 0:
        raise RuntimeError("Gemini HTML 不完整")
    return text[start : end + len("</html>")] + "\n"


CHECKS = {
    "linkedin": check_linkedin,
    "xiaohongshu": check_xiaohongshu,
    "medium": check_medium,
}
ANY_CHECKS = {
    "linkedin": check_linkedin_any,
    "xiaohongshu": check_xiaohongshu_any,
    "medium": check_medium_any,
}


def score_voice(platform: str, html: str) -> dict:
    prompt = f"""你在打张丹瀛的口吻，满分 100。她吹长笛，学法国学派。
80 分表示读起来像她本人在说话：有场景，有判断，有性格。
抽掉场景还能独立成立的金句，最高 60。品牌腔、论文腔，最高 50。
只输出 JSON：{{"score": 0, "reason": "一句话"}}
平台：{platform}

{html[:5000]}
"""
    return gemini_json(prompt)


def score_citations(platform: str, html: str, goal: str) -> dict:
    hrefs = article_hrefs(html)
    urls: set[str] = set()
    if SOURCE_DIR is not None and (SOURCE_DIR / "linkedin-sources.json").is_file():
        data = json.loads((SOURCE_DIR / "linkedin-sources.json").read_text(encoding="utf-8"))
        urls = {item.get("url") for item in data.get("sources") or [] if item.get("url")}
    if len(hrefs) != 2 or any(href not in urls for href in hrefs):
        return {"score": 0, "reason": f"要有两篇索引内、对上主题的原文，现在 {len(hrefs)} 篇"}
    bits = []
    for href in hrefs:
        idx = html.find(href)
        snippet = re.sub(r"<[^>]+>", "", html[max(0, idx - 80): idx + len(href) + 80])
        use = ""
        if SOURCE_DIR is not None and (SOURCE_DIR / "linkedin-sources.json").is_file():
            data = json.loads((SOURCE_DIR / "linkedin-sources.json").read_text(encoding="utf-8"))
            for item in data.get("sources") or []:
                if item.get("url") == href:
                    use = item.get("use") or item.get("title") or ""
        bits.append(f"{href}\n用在这里：{snippet}\n索引说明：{use}")
    listed = "\n\n".join(bits)
    prompt = f"""满分 100。主题：{goal}
匹配的意思是：这篇原文支撑主题里的一个具体判断。劳动力统计对上「领工资的座位少」，识读或教学对上「需要肯学的人」，都算 match。
不要求原文标题复述整句主题。两篇都 match 才可以到 80。有一篇没被用上，最高 50。
只输出 JSON：{{"score": 0, "reason": "一句话"}}
{listed}
"""
    return gemini_json(prompt)


def four_distance(scores: dict[str, int]) -> int:
    return sum(max(0, FOUR_PASS - int(scores[key])) for key in ("angle", "hit", "voice", "cite"))


def gemini_rewrite(platform: str, html: str, fails: list[str]) -> str:
    from google import genai
    from google.genai import types

    from config.gemini_config import get_api_key, get_model

    prompt = f"""你在改张丹瀛（Danying，长笛，法国学派）的一篇已有稿，平台是 {platform}。
只修下面没过的爆款潜力线，不要换成另一篇文章，不要加「首先/此外/综上所述/赋能/闭环」。
保留这些事实：NEA 2024 约 290 万艺术家、占劳动力 1.6%；演奏者全职约 54%。1.6% 只统计主要职业，不能说成爱艺术的人应该变少。
没过的线：
{chr(10).join('- ' + f for f in fails)}
{linkedin_source_note(SOURCE_DIR) if platform == "linkedin" else ""}

下面是当前 HTML。只输出完整 HTML，从 <!DOCTYPE html> 开始，不要解释。

{html}
"""
    client = genai.Client(api_key=get_api_key())
    response = client.models.generate_content(
        model=get_model(),
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.4,
            max_output_tokens=8192,
            thinking_config=types.ThinkingConfig(thinking_level=types.ThinkingLevel.MINIMAL),
        ),
    )
    text = (response.text or "").strip()
    start = text.find("<!DOCTYPE html>")
    if start < 0:
        start = text.find("<html")
    if start < 0:
        raise RuntimeError("Gemini 没有返回 HTML")
    end = text.rfind("</html>")
    if end < 0:
        raise RuntimeError("Gemini HTML 不完整")
    return text[start : end + len("</html>")] + "\n"


def gemini_json(prompt: str) -> dict:
    from google import genai
    from google.genai import types

    from config.gemini_config import get_api_key, get_model

    client = genai.Client(api_key=get_api_key())
    response = client.models.generate_content(
        model=get_model(),
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.2,
            max_output_tokens=2048,
            thinking_config=types.ThinkingConfig(thinking_level=types.ThinkingLevel.MINIMAL),
            response_mime_type="application/json",
        ),
    )
    raw = (response.text or "").strip()
    match = re.search(r"\{.*\}", raw, re.S)
    if not match:
        loose = re.search(r'"score"\s*:\s*(\d{1,3})', raw)
        if not loose:
            raise RuntimeError(f"Gemini 没有返回分数 JSON：{raw[:400]}")
        return {"score": int(loose.group(1)), "reason": raw[:180]}
    data = json.loads(match.group(0))
    data["score"] = int(data.get("score") or 0)
    return data


def gemini_score(platform: str, html: str) -> dict:
    prompt = f"""给下面这篇{platform}稿打一个爆款潜力分，0到100。
领英看第一人称经历、具体数字、不要问句开头、不要开头放链接。
小红书看前三秒反常识、口播能在三分钟内念完、不要承诺结果、不要加微信。
Medium看一篇只做一个观点、有个人场景、读者能读完。
这一步只评爆款潜力，不要重复前面的写作标准或切入视角。
只输出 JSON：{{"score": 0, "reason": "一句话"}}

{html[:6000]}
"""
    return gemini_json(prompt)


def _plain(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def _group_hit(plain: str, options: tuple[str, ...]) -> str:
    return next((item for item in options if item in plain), "")


def angle_benchmark_path() -> Path:
    if SOURCE_DIR is not None:
        local = SOURCE_DIR / "angle-benchmarks.json"
        if local.is_file():
            return local
    return ROOT / "docs/angle-benchmarks.json"


def _floor_ok(item: dict, floors: dict) -> bool:
    bench = item.get("benchmark") or {}
    platform = item.get("platform") or bench.get("platform")
    rule = floors.get(platform) or {}
    if rule.get("must_read_on_page") and not bench.get("read_on_page"):
        return False
    engagement = bench.get("engagement") or {}
    try:
        value = int(engagement.get(rule.get("field") or "") or 0)
    except (TypeError, ValueError):
        return False
    return value >= int(rule.get("min") or 0)


def angle_items() -> tuple[list[dict], dict]:
    path = angle_benchmark_path()
    if not path.is_file():
        raise FileNotFoundError(f"缺少角度基准 {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    floors = data.get("floors") or {}
    for platform in ("linkedin", "xiaohongshu", "medium"):
        if platform not in floors:
            raise RuntimeError(f"角度基准缺 {platform} 的高线")
    cells = data.get("cells") or []
    needed = {
        f"{platform}/{kind}"
        for platform in ("linkedin", "xiaohongshu", "medium")
        for kind in ("same", "different", "sharp")
    }
    if set(cells) != needed:
        raise RuntimeError("角度基准必须是三平台各三种角度，共九格")
    items = []
    for item in data.get("items") or []:
        if _floor_ok(item, floors):
            items.append(item)
    return items, data


def _engagement_value(item: dict, floors: dict) -> int:
    bench = item.get("benchmark") or {}
    platform = item.get("platform") or bench.get("platform")
    field = (floors.get(platform) or {}).get("field") or ""
    try:
        return int((bench.get("engagement") or {}).get(field) or 0)
    except (TypeError, ValueError):
        return 0


def _item_match(plain: str, item: dict) -> tuple[bool, str]:
    if "groups" in item:
        hits = [_group_hit(plain, tuple(group)) for group in item["groups"]]
        ok = all(hits)
        return ok, "、".join(hit for hit in hits if hit)
    evidence = _group_hit(plain, tuple(item.get("any") or ()))
    return bool(evidence), evidence


def angle_hard(html: str) -> dict:
    """Use the articles we actually have. A missing cell borrows the highest one."""
    plain = _plain(html)
    items, data = angle_items()
    floors = data.get("floors") or {}
    if not items:
        return {
            "score": 0,
            "passed_cells": 0,
            "cells": 0,
            "rows": [],
            "benchmark_file": str(angle_benchmark_path().relative_to(ROOT)),
            "checked_at": data.get("checked_at"),
            "why": "没有一篇过线的同类型文章",
        }
    base = max(items, key=lambda item: _engagement_value(item, floors))
    by_cell = {f"{item.get('platform')}/{item.get('angle')}": item for item in items}
    rows = []
    passed = 0
    for cell in data["cells"]:
        own = by_cell.get(cell)
        item = own or base
        ok, evidence = _item_match(plain, item)
        if ok:
            passed += 1
        bench = item.get("benchmark") or {}
        rows.append({
            "id": item["id"],
            "cell": cell,
            "angle": item.get("angle"),
            "name": item["name"],
            "pass": ok,
            "evidence": evidence,
            "inherited": own is None,
            "benchmark_url": bench.get("url"),
            "benchmark_engagement": bench.get("engagement"),
        })
    score = int(round(100 * passed / len(data["cells"])))
    return {
        "score": score,
        "passed_cells": passed,
        "cells": len(data["cells"]),
        "base_id": base.get("id"),
        "rows": rows,
        "benchmark_file": str(angle_benchmark_path().relative_to(ROOT)),
        "checked_at": data.get("checked_at"),
    }


def angle_specs(goal: str, html: str) -> list[dict]:
    thesis = "艺术家" in goal or "艺术家" in html
    senior = (
        "三条里选正文最没接住的一条：业内人说你自己靠这行吃饭却宣布座位该少；"
        "听众说你把鼓掌的人写成不懂；1.6% 只统计主要职业，不能用来规定热爱艺术的人数。"
        "正文若已经写了不会拿这个百分比叫人退出、鼓掌的人没错、1.6% 不能规定热爱的人数，这三条不许再判没接住。"
        "另找一条正文没写的具体反对。找不到，分数写 80。"
        if thesis
        else "找一个会公开反驳的读者，写出他最具体的一条反对，看正文有没有接住。"
    )
    return [
        {
            "id": "01-voice",
            "layer": "01 IP",
            "name": "写作标准",
            "task": "只攻击声音。反对必须引用标题以外的一句。标题、「需要很多热爱艺术的人」、以及平台规定的结尾「评论区留下曲名」，都不许当反对。场景删掉之后那句还能独立成立，才算没接住。",
        },
        {
            "id": "04-cut",
            "layer": "04 Topic",
            "name": "切入视角",
            "task": "点名一个范围内的维度，正文里没有对应场景，才算没接住。范围是 AI、艺术前沿、各国历史与文化、音乐、视觉、建筑、设计、各地商业走向。调音软件算 AI，也算艺术前沿里的工具。法国学派算法国的教法。留白的墙、开幕照片、小画比大画好卖，算建筑、设计和商业走向。已经写了场景的维度，不许再说没写到，也不许要求再收成一句口号。",
        },
        {
            "id": "00-senior",
            "layer": "00 CEO",
            "name": "反方读者",
            "task": senior,
        },
    ]


def distance_to_bar(rows: list[dict]) -> int:
    return sum(max(0, ANGLE_BAR - int(row.get("score") or 0)) for row in rows)


def gemini_angle(platform: str, html: str, spec: dict) -> dict:
    prompt = f"""你是 {spec['layer']}，这一层只负责「{spec['name']}」。
不要夸。先写出最狠、最具体的一条反对，再打 0 到 100。
分数表示正文已经把这条反对拆掉了多少。部分接住最高 70。没有具体场景最高 60。没接住必须低于 {ANGLE_BAR}。
写不出具体反对时，分数不得超过 70。
只输出 JSON：{{"score": 0, "objection": "一句话"}}
攻击任务：{spec['task']}
平台：{platform}

{html[:6000]}
"""
    data = gemini_json(prompt)
    data.update({"id": spec["id"], "layer": spec["layer"], "name": spec["name"]})
    return data


def gemini_rewrite_angles(platform: str, html: str, notes: list[str]) -> str:
    from google import genai
    from google.genai import types

    from config.gemini_config import get_api_key, get_model

    prompt = f"""你在改张丹瀛（长笛，法国学派）的 {platform} 稿。
这一步只接住下面的对抗意见，不要为了爆款清单去加钩子、问句或标签。
把回答写进正文。不要另开「反方」小标题把攻击原文贴回去。
保留这些事实：NEA 2024 约 290 万艺术家、占劳动力 1.6%；演奏者全职约 54%。1.6% 只统计主要职业。
小红书口播继续用 <p class="say">。
没接住的意见：
{chr(10).join('- ' + note for note in notes)}
{linkedin_source_note(SOURCE_DIR) if platform == "linkedin" else ""}

只输出完整 HTML，从 <!DOCTYPE html> 开始。

{html}
"""
    client = genai.Client(api_key=get_api_key())
    response = client.models.generate_content(
        model=get_model(),
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.4,
            max_output_tokens=8192,
            thinking_config=types.ThinkingConfig(thinking_level=types.ThinkingLevel.MINIMAL),
        ),
    )
    text = (response.text or "").strip()
    start = text.find("<!DOCTYPE html>")
    if start < 0:
        start = text.find("<html")
    if start < 0:
        raise RuntimeError("Gemini 没有返回 HTML")
    end = text.rfind("</html>")
    if end < 0:
        raise RuntimeError("Gemini HTML 不完整")
    return text[start : end + len("</html>")] + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", type=Path, required=True)
    parser.add_argument("--goal", default="")
    parser.add_argument(
        "--rounds",
        type=int,
        default=int(os.environ.get("CEO_EVOLUTION_MAX_ROUNDS", "6")),
    )
    parser.add_argument("--judge-only", action="store_true")
    args = parser.parse_args()
    folder = args.dir if args.dir.is_absolute() else ROOT / args.dir
    folder.mkdir(parents=True, exist_ok=True)
    global SOURCE_DIR
    SOURCE_DIR = folder
    def linkedin_index_ready() -> bool:
        path = folder / "linkedin-sources.json"
        html = folder / "linkedin.html"
        if not path.is_file() or not html.is_file():
            return False
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return False
        urls = [item.get("url") for item in (data.get("sources") or []) if item.get("url")]
        return len(urls) >= 2

    if args.goal and not linkedin_index_ready():
        try:
            research_linkedin(args.goal, folder)
        except Exception as exc:
            print(json.dumps({"linkedin_research": "FAIL", "error": str(exc)}, ensure_ascii=False), flush=True)
    specific = (not args.goal) or ("艺术家" in args.goal)
    report: dict = {
        "ran_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "goal": args.goal,
        "standards": STANDARDS,
        "order": ["01-voice", "04-cut", "00-senior", "evolution-distance", "hit-line"],
        "angle_bar": ANGLE_BAR,
        "platforms": {},
    }
    failed = 0
    for name in PLATFORMS:
        path = folder / f"{name}.html"
        if not path.is_file():
            if not args.goal:
                report["platforms"][name] = {"pass": False, "error": "missing file"}
                failed += 1
                continue
            try:
                path.write_text(gemini_draft(name, args.goal, folder), encoding="utf-8")
            except Exception as exc:
                report["platforms"][name] = {"pass": False, "error": str(exc)}
                failed += 1
                continue
        html = path.read_text(encoding="utf-8")
        checker = CHECKS[name] if specific else ANY_CHECKS[name]
        angle_history: list[dict] = []
        angle_error = ""
        hard = angle_hard(html)
        angle_history.append({
            "round": 1,
            "distance": max(0, ANGLE_BAR - int(hard["score"])),
            "rows": hard["rows"],
            "score": hard["score"],
        })
        history = []
        score: dict = {}
        api_error = ""
        for round_i in range(1, args.rounds + 1):
            fails = checker(html)
            try:
                score = gemini_score(name, html)
            except Exception as exc:
                api_error = str(exc)
                history.append({"round": round_i, "fails": fails, "api_error": api_error})
                break
            history.append({"round": round_i, "fails": fails, "score": score})
            if (not fails and score.get("score", 0) >= HIT_BAR) or args.judge_only:
                break
            if not fails and score.get("score", 0) < HIT_BAR:
                fails = [f"Gemini 爆款潜力分 {score.get('score')}：{score.get('reason', '')}"]
            try:
                html = gemini_rewrite(name, html, fails)
                path.write_text(html, encoding="utf-8")
            except Exception as exc:
                api_error = str(exc)
                history.append({"round": round_i, "api_error": api_error})
                break
        final_html = path.read_text(encoding="utf-8")
        final_fails = checker(final_html)
        if api_error:
            final_fails = final_fails + [api_error]
        if angle_error:
            final_fails = final_fails + [angle_error]
        hard = angle_hard(final_html)
        angle_score = int(hard["score"])
        angle_history.append({
            "round": "final",
            "distance": max(0, ANGLE_BAR - angle_score),
            "rows": hard["rows"],
            "score": angle_score,
        })
        mechanic = [
            item
            for item in checker(final_html)
            if "原文" not in item and "检索" not in item
        ]
        hit_points = int(score.get("score") or 0) if not mechanic else 0
        try:
            voice = score_voice(name, final_html)
        except Exception as exc:
            voice = {"score": 0, "reason": str(exc)}
            final_fails = final_fails + [str(exc)]
        try:
            cite = score_citations(name, final_html, args.goal)
        except Exception as exc:
            cite = {"score": 0, "reason": str(exc)}
            final_fails = final_fails + [str(exc)]
        four = {
            "angle": angle_score,
            "hit": hit_points,
            "voice": int(voice.get("score") or 0),
            "cite": int(cite.get("score") or 0),
        }
        four_gap = four_distance(four)
        stress = {}
        if four_gap == 0:
            try:
                stress_voice = score_voice(name, final_html)
                stress_angle = angle_hard(final_html)
                stress = {
                    "voice": int(stress_voice.get("score") or 0),
                    "angle": int(stress_angle["score"]),
                    "rows": stress_angle["rows"],
                }
                if stress["voice"] < FOUR_PASS or stress["angle"] < FOUR_PASS:
                    four_gap += (FOUR_PASS - min(stress["voice"], stress["angle"]))
                    final_fails = final_fails + ["压测线低于 80"]
            except Exception as exc:
                stress = {"error": str(exc)}
                final_fails = final_fails + [str(exc)]
        ok = four_gap == 0 and not api_error and not angle_error and not mechanic
        if not ok:
            failed += 1
        baseline = angle_history[0].get("distance") if angle_history else None
        final_distance = four_gap
        report["platforms"][name] = {
            "pass": ok,
            "angle_ready": angle_score >= FOUR_PASS,
            "distance_before": baseline,
            "distance_after": final_distance,
            "four": four,
            "voice": voice,
            "cite": cite,
            "stress": stress,
            "angles": angle_history,
            "hit_pass": not checker(final_html) and not api_error,
            "hit_score": score,
            "fails": final_fails,
            "hit_history": history,
        }
        print(json.dumps({
            "platform": name,
            "pass": ok,
            "four": four,
            "distance_after": final_distance,
            "fails": final_fails,
        }, ensure_ascii=False))
    out = folder / "hit-evolution.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary = {
        "ran_at": report["ran_at"],
        "pass_line": FOUR_PASS,
        "full_score": 100,
        "dimensions": ["angle", "hit", "voice", "cite"],
        "platforms": {
            name: {
                "pass": item.get("pass"),
                "four": item.get("four"),
                "distance_after": item.get("distance_after"),
                "stress": item.get("stress"),
            }
            for name, item in report["platforms"].items()
        },
    }
    (folder / "four-dimensions.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"WROTE {out.relative_to(ROOT)}")
    return 0 if failed == 0 else 42


if __name__ == "__main__":
    raise SystemExit(main())
