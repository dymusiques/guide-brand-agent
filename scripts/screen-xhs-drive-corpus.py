#!/usr/bin/env python3
"""Screen the Xiaohongshu IP Drive catalog for one writing goal.

Reads every filename in the live listing (not a sample outline) and writes a
shortlist the CEO pipeline must open. Does not download or paste file bodies.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CATALOG = (
    ROOT
    / "content/personal-ip/intake/_raw/xhs-ip-2026-11-03/drive-listing-2026-11-03-live.json"
)
OUT_JSON = ROOT / "content/evolution/00-manager/ceo-inbox/xhs-drive-screen-latest.json"
OUT_MD = ROOT / "content/evolution/00-manager/ceo-inbox/xhs-drive-screen-latest.md"

# One file per theme so a generic「写文案」still has method backing.
CORE_THEMES = (
    "定位",
    "起号",
    "算法",
    "违禁",
    "搜索",
    "封面",
    "标题",
    "合规",
    "线索",
    "关键词",
    "人设",
    "笔记",
)

# Drop these unless the goal itself names the domain.
OFF_DOMAIN = (
    "冰淇淋",
    "商场",
    "跨境",
    "面试",
    "本地推",
    "快手",
    "视频号",
    "百家号",
    "纹绣",
    "潮玩",
    "野人先生",
    "美业",
)

GOAL_NOISE = (
    "小红书",
    "个人ip",
    "个人IP",
    "文案",
    "今天",
    "写一篇",
    "帮我",
    "打造",
    "一篇",
    "需要",
    "一个",
    "怎么",
    "如何",
)


def norm_name(name: str) -> str:
    name = re.sub(r"\s*\(\d+\)", "", name)
    name = re.sub(r"\s+", "", name)
    return name.casefold()


def goal_terms(goal: str) -> list[str]:
    text = goal
    for noise in GOAL_NOISE:
        text = text.replace(noise, " ")
    parts = re.split(r"[的和与及了在把是要就都很还又\s，。！？、：:]+", text)
    terms = [p for p in parts if re.fullmatch(r"[\u4e00-\u9fff]{2,}", p)]
    compounds = CORE_THEMES + (
        "关键词",
        "违禁词",
        "长笛",
        "练习",
        "投放",
        "薯条",
        "聚光",
        "留资",
        "私信",
        "评论",
        "养号",
        "矩阵",
    )
    terms.extend(c for c in compounds if c in goal)
    terms.extend(re.findall(r"[A-Za-z][A-Za-z0-9_+-]{2,}", goal))
    generic = {"笔记", "内容", "运营", "品牌", "账号", "关于", "一篇", "这个", "什么"}
    return sorted({t for t in terms if t not in generic and len(t) >= 2}, key=len, reverse=True)


def off_domain(name: str, goal: str) -> bool:
    return any(tok in name and tok not in goal for tok in OFF_DOMAIN)


def prefer_key(item: dict) -> tuple:
    name = item["name"]
    mime = item.get("mimeType") or ""
    dup = 1 if re.search(r"\(\d+\)", name) else 0
    md = 0 if mime == "text/markdown" else 1
    return (dup, md, len(name), int(item.get("size") or 0))


def load_catalog(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    files = data.get("files") if isinstance(data, dict) else data
    if not isinstance(files, list) or not files:
        raise ValueError(f"catalog has no files: {path}")
    return files


def dedupe(files: list[dict]) -> list[dict]:
    best: dict[str, dict] = {}
    for item in files:
        key = norm_name(item.get("name") or "")
        if not key:
            continue
        current = best.get(key)
        if current is None or prefer_key(item) < prefer_key(current):
            best[key] = item
    return list(best.values())


def screen(files: list[dict], goal: str, limit: int) -> tuple[list[dict], int]:
    unique = dedupe(files)
    terms = goal_terms(goal)
    ranked: list[tuple[int, dict, str]] = []
    for item in unique:
        name = item.get("name") or ""
        if off_domain(name, goal):
            continue
        hits = [t for t in terms if t and t in name]
        score = sum(len(t) for t in hits)
        why = "、".join(hits[:4]) if hits else ""
        ranked.append((score, item, why))

    picked: list[dict] = []
    seen: set[str] = set()

    def add(item: dict, why: str, score: int) -> None:
        key = norm_name(item.get("name") or "")
        if key in seen or len(picked) >= limit:
            return
        seen.add(key)
        picked.append(
            {
                "name": item.get("name"),
                "id": item.get("id"),
                "mimeType": item.get("mimeType"),
                "score": score,
                "why": why,
                "webViewLink": item.get("webViewLink"),
            }
        )

    for score, item, why in sorted(ranked, key=lambda row: (-row[0], prefer_key(row[1]))):
        if score <= 0:
            break
        add(item, f"题名命中：{why}", score)

    for theme in CORE_THEMES:
        if len(picked) >= limit:
            break
        candidates = [item for item in unique if theme in (item.get("name") or "") and not off_domain(item.get("name") or "", goal)]
        if not candidates:
            continue
        best = sorted(candidates, key=prefer_key)[0]
        add(best, f"写文案默认要核对的主题：{theme}", 0)

    return picked, len(unique)


def write_outputs(goal: str, catalog: Path, total: int, unique: int, picked: list[dict]) -> None:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "screened_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "goal": goal,
        "catalog": str(catalog.relative_to(ROOT)),
        "catalog_files": total,
        "unique_after_dedupe": unique,
        "selected_count": len(picked),
        "screened_out": unique - len(picked),
        "policy": "Open selected Drive files before drafting. Open WebUI split is for the long draft only.",
        "selected": picked,
    }
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 小红书 Drive 筛选结果",
        "",
        f"- goal: {goal}",
        f"- 全库文件名: {total}（去重后 {unique}）",
        f"- 本篇入选: {len(picked)}",
        f"- 本篇不用: {unique - len(picked)}（仍在 Drive，没有删除）",
        "- 下一步: 按下面的 Drive id 打开原件再写。入选名单不是正文。",
        "- Open WebUI 切分只用于这一篇长稿的输出，不用于代替打开原件。",
        "",
        "| 文件 | Drive id | 入选原因 |",
        "|------|----------|----------|",
    ]
    for item in picked:
        lines.append(f"| {item['name']} | `{item['id']}` | {item['why']} |")
    lines.append("")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser(description="Screen XHS Drive catalog filenames for one goal")
    p.add_argument("--goal", "-g", required=True)
    p.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    p.add_argument("--limit", type=int, default=12)
    args = p.parse_args()
    goal = args.goal.strip()
    if not goal:
        print("empty goal", file=sys.stderr)
        return 2
    catalog = args.catalog if args.catalog.is_absolute() else ROOT / args.catalog
    if not catalog.is_file():
        print(f"catalog missing: {catalog}", file=sys.stderr)
        return 2
    files = load_catalog(catalog)
    picked, unique = screen(files, goal, max(1, args.limit))
    if not picked:
        print("screen produced an empty shortlist", file=sys.stderr)
        return 2
    write_outputs(goal, catalog, len(files), unique, picked)
    print(
        json.dumps(
            {
                "catalog_files": len(files),
                "unique_after_dedupe": unique,
                "selected": len(picked),
                "markdown": str(OUT_MD.relative_to(ROOT)),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
