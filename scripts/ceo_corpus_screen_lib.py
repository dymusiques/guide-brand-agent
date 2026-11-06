"""Full CEO Drive corpus screening — score every catalog file, tier references, no silent drops."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CATALOG = ROOT / "content/personal-ip/intake/_raw/ceo-drive-catalog-live.json"
LEGACY_CATALOG = ROOT / "content/personal-ip/intake/_raw/xhs-ip-2026-11-03/drive-listing-2026-11-03-live.json"
SCREENS_ROOT = ROOT / "content/evolution/00-manager/ceo-inbox/corpus-screens"
LATEST_POINTER = ROOT / "content/evolution/00-manager/ceo-inbox/corpus-screen-latest.json"
LEGACY_OUT_JSON = ROOT / "content/evolution/00-manager/ceo-inbox/xhs-drive-screen-latest.json"
LEGACY_OUT_MD = ROOT / "content/evolution/00-manager/ceo-inbox/xhs-drive-screen-latest.md"

CORE_THEMES = (
    "定位", "起号", "算法", "违禁", "搜索", "封面", "标题", "合规", "线索", "关键词", "人设", "笔记",
)
OFF_DOMAIN = (
    "冰淇淋", "商场", "跨境", "面试", "本地推", "快手", "视频号", "百家号", "纹绣", "潮玩", "野人先生", "美业",
)
GOAL_NOISE = (
    "小红书", "个人ip", "个人IP", "文案", "今天", "写一篇", "帮我", "打造", "一篇", "需要", "一个", "怎么", "如何",
    "CEO", "派活", "定稿", "LinkedIn", "Medium",
)
SOURCE_FOLDER_KEYWORDS: dict[str, tuple[str, ...]] = {
    "小红书": ("笔记", "起号", "运营", "种草", "小红书", "IP", "账号", "算法", "投放"),
    "品牌领域知识库": ("品牌", "营销", "定位", "战略", "视觉", "VI", "传播"),
    "Books": ("书", "阅读", "艺术", "历史", "文化", "哲学", "美学", "理论", "小说", "电子书"),
    "消费心理学": ("消费", "心理", "行为", "决策", "购买", "用户"),
    "策展相关": ("策展", "展览", "博物馆", "画廊", "艺术", "空间", "叙事"),
    "品牌策划营销": ("品牌", "策划", "营销", "campaign", "传播", "创意"),
    "01- 深度品牌档案": ("品牌", "档案", "案例", "深度", "竞品", "标杆"),
}
DOMAIN_EXTRA_TERMS = (
    "品牌", "艺术", "艺术家", "策展", "消费", "心理", "营销", "文化", "历史", "设计", "建筑", "音乐",
    "长笛", "练习", "LinkedIn", "Medium", "IP", "个人",
)
HYDRATE_DEFAULT = 8


def slugify(text: str) -> str:
    s = re.sub(r"[^\w\u4e00-\u9fff+-]+", "-", text.strip())[:80].strip("-")
    return s or "ceo-task"


def norm_name(name: str) -> str:
    name = re.sub(r"\s*\(\d+\)", "", name)
    name = re.sub(r"\s+", "", name)
    return name.casefold()


def goal_terms(goal: str, brief_text: str = "") -> list[str]:
    text = goal + "\n" + brief_text
    for noise in GOAL_NOISE:
        text = text.replace(noise, " ")
    parts = re.split(r"[的和与及了在把是要就都很还又\s，。！？、：:\[\]()#]+", text)
    terms = [p for p in parts if re.fullmatch(r"[\u4e00-\u9fff]{2,}", p)]
    for c in CORE_THEMES + DOMAIN_EXTRA_TERMS:
        if c in goal or c in brief_text:
            terms.append(c)
    terms.extend(re.findall(r"[A-Za-z][A-Za-z0-9_+-]{2,}", text))
    generic = {"笔记", "内容", "运营", "账号", "关于", "一篇", "这个", "什么", "任务", "brief", "Brief"}
    return sorted({t for t in terms if t not in generic and len(t) >= 2}, key=len, reverse=True)


def off_domain(name: str, goal: str) -> bool:
    if any(tok in name and tok not in goal for tok in OFF_DOMAIN):
        return True
    # FluteBuddy 任务勿用 WorkBuddy / 职场 / 饮食资料
    if re.search(r"FluteBuddy|Flute Buddy|长笛", goal, re.I):
        if re.search(r"WorkBuddy|职场提效", name, re.I):
            return True
    return False


def prefer_key(item: dict) -> tuple:
    name = item.get("name") or ""
    mime = item.get("mimeType") or ""
    dup = 1 if re.search(r"\(\d+\)", name) else 0
    md = 0 if mime == "text/markdown" else 1
    size = item.get("size") or "0"
    try:
        sz = int(size)
    except ValueError:
        sz = 0
    return (dup, md, len(name), sz)


def resolve_catalog(catalog: Path | None) -> Path:
    if catalog and catalog.is_file():
        return catalog if catalog.is_absolute() else ROOT / catalog
    if DEFAULT_CATALOG.is_file():
        return DEFAULT_CATALOG
    return LEGACY_CATALOG


def load_catalog(path: Path) -> tuple[list[dict], dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    files = data.get("files") if isinstance(data, dict) else data
    if not isinstance(files, list):
        raise ValueError(f"catalog has no files: {path}")
    return files, data if isinstance(data, dict) else {}


def read_brief_snippet(brief: str) -> str:
    if not brief:
        return ""
    bp = Path(brief)
    if not bp.is_absolute():
        bp = ROOT / bp
    if not bp.is_file():
        return ""
    text = bp.read_text(encoding="utf-8", errors="replace")[:12000]
    return text


def folder_match_score(source_label: str, terms: list[str], goal: str) -> tuple[int, str]:
    keys = SOURCE_FOLDER_KEYWORDS.get(source_label, ())
    hits = [k for k in keys if k in goal or any(k in t or t in k for t in terms)]
    if hits:
        return len(hits) * 3, f"资料库「{source_label}」与任务域：{'、'.join(hits[:5])}"
    for token in re.split(r"[\s\-·]+", source_label):
        if len(token) >= 2 and (token in goal or any(token in t or t in token for t in terms)):
            return 2, f"资料库文件夹名命中：{token}"
    return 0, ""


def classify_file(
    item: dict,
    *,
    terms: list[str],
    goal: str,
    folder_bonus: dict[str, tuple[int, str]],
) -> dict[str, Any]:
    name = item.get("name") or ""
    fid = item.get("id") or ""
    source_label = item.get("source_label") or ""
    if off_domain(name, goal):
        return {
            "id": fid,
            "name": name,
            "mimeType": item.get("mimeType"),
            "webViewLink": item.get("webViewLink"),
            "source_folder_id": item.get("source_folder_id"),
            "source_label": source_label,
            "score": 0,
            "tier": "excluded",
            "why": "off_domain：与任务域无关且题名含排除域关键词",
        }
    title_hits = [t for t in terms if t and t in name]
    score = sum(len(t) for t in title_hits)
    why_parts: list[str] = []
    if title_hits:
        why_parts.append("题名命中：" + "、".join(title_hits[:6]))
    fb, fw = folder_bonus.get(source_label, (0, ""))
    if fb:
        score += fb
        if fw:
            why_parts.append(fw)
    tier = "catalog_only"
    if score >= 4:
        tier = "direct_hit"
    elif score >= 1:
        tier = "reference"
    elif fb > 0:
        tier = "source_corpus"
    elif any(theme in name for theme in CORE_THEMES) and re.search(r"写|笔记|Brief|文案|小红书|IP", goal, re.I):
        tier = "xhs_theme_reserve"
        score = 1
        why_parts.append(f"写稿默认主题库：题名含运营主题词")
    return {
        "id": fid,
        "name": name,
        "mimeType": item.get("mimeType"),
        "webViewLink": item.get("webViewLink"),
        "source_folder_id": item.get("source_folder_id"),
        "source_label": source_label,
        "score": score,
        "tier": tier,
        "why": "；".join(why_parts) if why_parts else "全库索引（未命中题名/域，供审计不遗漏）",
    }


def comprehensive_screen(
    goal: str,
    *,
    brief: str = "",
    catalog_path: Path | None = None,
    hydrate_limit: int = HYDRATE_DEFAULT,
) -> dict[str, Any]:
    catalog = resolve_catalog(catalog_path)
    if not catalog.is_file():
        raise FileNotFoundError(f"catalog missing: {catalog}")
    files, cat_meta = load_catalog(catalog)
    brief_text = read_brief_snippet(brief)
    terms = goal_terms(goal, brief_text)
    slug = slugify(Path(brief).name.replace("-brief.md", "") if brief else goal)

    folder_bonus: dict[str, tuple[int, str]] = {}
    for folder in cat_meta.get("folders") or []:
        label = folder.get("label") or ""
        folder_bonus[label] = folder_match_score(label, terms, goal)

    ranked: list[dict[str, Any]] = []
    for item in files:
        ranked.append(classify_file(item, terms=terms, goal=goal, folder_bonus=folder_bonus))

    ranked.sort(key=lambda row: (-row["score"], prefer_key(row)))

    reference_tiers = {
        "direct_hit",
        "reference",
        "source_corpus",
        "xhs_theme_reserve",
    }
    reference = [r for r in ranked if r["tier"] in reference_tiers]
    excluded = [r for r in ranked if r["tier"] == "excluded"]
    catalog_only = [r for r in ranked if r["tier"] == "catalog_only"]

    # Ensure every non-excluded file in a matched source folder enters reference (域内不遗漏)
    matched_labels = {lbl for lbl, (sc, _) in folder_bonus.items() if sc > 0}
    ref_ids = {r["id"] for r in reference}
    for idx, row in enumerate(ranked):
        if row["tier"] == "excluded":
            continue
        if row["source_label"] in matched_labels and row["id"] not in ref_ids:
            why = row["why"] + "；域内资料库全量纳入参考"
            new_row = {**row, "tier": "source_corpus", "score": max(int(row["score"]), 1), "why": why}
            ranked[idx] = new_row
            reference.append(new_row)
            ref_ids.add(row["id"])

    reference.sort(key=lambda row: (-row["score"], prefer_key(row)))
    hydrate_priority = reference[: max(1, hydrate_limit)]

    by_source: dict[str, list[dict]] = {}
    for row in reference:
        by_source.setdefault(row.get("source_label") or "unknown", []).append(row)

    return {
        "screened_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "goal": goal,
        "brief": brief,
        "slug": slug,
        "catalog": str(catalog.relative_to(ROOT)) if catalog.is_relative_to(ROOT) else str(catalog),
        "catalog_listed_at": cat_meta.get("listed_at"),
        "catalog_file_count": len(files),
        "goal_terms": terms,
        "counts": {
            "reference": len(reference),
            "hydrate_priority": len(hydrate_priority),
            "catalog_only": len(catalog_only),
            "excluded": len(excluded),
            "total_ranked": len(ranked),
        },
        "policy": {
            "reference": "任务相关背书候选（题名/资料库域/写稿主题），Agent 定稿前须知晓",
            "hydrate_priority": f"gdocs 优先打开 ≤{hydrate_limit} 个写 evidence",
            "catalog_only": "全库已评分但未纳入参考层；若任务扩展可复查",
        },
        "all_ranked": ranked,
        "reference": reference,
        "hydrate_priority": hydrate_priority,
        "by_source_folder": by_source,
        "excluded_sample": excluded[:20],
    }


def write_task_bundle(payload: dict[str, Any]) -> Path:
    slug = payload["slug"]
    task_dir = SCREENS_ROOT / slug
    task_dir.mkdir(parents=True, exist_ok=True)
    (task_dir / "manifest.json").write_text(
        json.dumps(
            {
                k: payload[k]
                for k in (
                    "screened_at",
                    "goal",
                    "brief",
                    "slug",
                    "catalog",
                    "catalog_listed_at",
                    "catalog_file_count",
                    "goal_terms",
                    "counts",
                    "policy",
                )
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (task_dir / "all-ranked.json").write_text(
        json.dumps(payload["all_ranked"], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (task_dir / "reference.json").write_text(
        json.dumps(payload["reference"], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (task_dir / "hydrate-priority.json").write_text(
        json.dumps(payload["hydrate_priority"], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (task_dir / "by-source-folder.json").write_text(
        json.dumps(payload["by_source_folder"], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    md_lines = [
        f"# CEO 资料库筛选 · {slug}",
        "",
        f"- **goal:** {payload['goal']}",
        f"- **brief:** {payload.get('brief') or '—'}",
        f"- **catalog:** {payload['catalog']}（{payload['catalog_file_count']} 文件）",
        f"- **参考层（不遗漏域内）:** {payload['counts']['reference']} 篇",
        f"- **优先 hydrate:** {payload['counts']['hydrate_priority']} 篇",
        "",
        "## 优先打开（hydrate）",
        "",
    ]
    for i, row in enumerate(payload["hydrate_priority"], 1):
        md_lines.append(f"{i}. [{row['name']}]({row.get('webViewLink') or '#'}) · {row['tier']} · {row['why']}")
    md_lines.extend(["", "## 按资料库文件夹", ""])
    for label, rows in sorted(payload["by_source_folder"].items(), key=lambda x: -len(x[1])):
        md_lines.append(f"### {label}（{len(rows)}）")
        for row in rows[:15]:
            md_lines.append(f"- {row['name']} · score={row['score']}")
        if len(rows) > 15:
            md_lines.append(f"- … 另有 {len(rows) - 15} 篇见 reference.json")
        md_lines.append("")
    (task_dir / "INDEX.md").write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    return task_dir


def sync_legacy_outputs(payload: dict[str, Any], task_dir: Path) -> None:
    """Keep xhs-drive-screen-latest.* compatible with existing CEO / fusion scripts."""
    selected = []
    for row in payload["hydrate_priority"]:
        selected.append(
            {
                "name": row["name"],
                "id": row["id"],
                "mimeType": row.get("mimeType"),
                "score": row["score"],
                "why": row["why"],
                "tier": row["tier"],
                "webViewLink": row.get("webViewLink"),
                "source_label": row.get("source_label"),
            }
        )
    legacy = {
        "screened_at": payload["screened_at"],
        "goal": payload["goal"],
        "brief": payload.get("brief") or "",
        "catalog": payload["catalog"],
        "catalog_files": payload["catalog_file_count"],
        "selected_count": len(selected),
        "reference_count": payload["counts"]["reference"],
        "screen_engine": "ceo-task-drive-corpus-screen.py",
        "task_bundle_dir": str(task_dir.relative_to(ROOT)),
        "policy": "Full reference in task bundle; selected = hydrate_priority for gdocs.",
        "selected": selected,
        "reference_path": str((task_dir / "reference.json").relative_to(ROOT)),
    }
    LEGACY_OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    LEGACY_OUT_JSON.write_text(json.dumps(legacy, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    LATEST_POINTER.write_text(
        json.dumps(
            {"slug": payload["slug"], "task_dir": legacy["task_bundle_dir"], "screened_at": payload["screened_at"]},
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    LEGACY_OUT_MD.write_text((task_dir / "INDEX.md").read_text(encoding="utf-8"), encoding="utf-8")


def bind_brief_drive_screen(brief: str, legacy_payload: dict) -> Path | None:
    if not brief:
        return None
    slug = Path(brief).name.replace("-brief.md", "")
    dest = ROOT / "content/evolution/04-xhs-topic-manager" / slug / "drive-screen.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(legacy_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    ref_dest = dest.parent / "drive-reference.json"
    task_dir = ROOT / legacy_payload["task_bundle_dir"]
    if (task_dir / "reference.json").is_file():
        ref_dest.write_text((task_dir / "reference.json").read_text(encoding="utf-8"), encoding="utf-8")
    return dest
