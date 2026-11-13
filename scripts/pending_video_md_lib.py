#!/usr/bin/env python3
"""Parse pending-videos/*.md from full file (metadata + 口播全文). Single parser for eval + facts + gate."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

TECH_MARKERS = re.compile(r"Vibrato|vibrato|Rubato|指法|双吐|节拍器|✅\d+")
FRANCE_MARKERS = ("法国", "去了法国", "到法国", "法国站")
ITALY_MARKERS = ("意大利", "意大利站", "意大利那一站", "意大利的时候")
WITNESS_MARKERS = (
    "不是发生在我身上",
    "不是我",
    "目击",
    "目睹",
    "看到了整个",
    "我在下面",
    "从头到尾",
    "全程",
    "旁观者",
)
SELF_PROTAGONIST_MARKERS = ("我让对方", "我让泰斗", "我说了一句话", "我当场")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def meta_table_field(text: str, label: str) -> str | None:
    m = re.search(
        rf"\|\s*\*\*{re.escape(label)}\*\*\s*\|\s*([^|\n]+)",
        text,
        re.I,
    )
    return m.group(1).strip() if m else None


def parse_pending_video(path: Path, root: Path | None = None) -> dict:
    text = path.read_text(encoding="utf-8")
    title_m = re.search(r"^#\s*发布标题[：:]\s*(.+)$", text, re.M)
    title = title_m.group(1).strip() if title_m else path.stem

    track_m = re.search(r"\|\s*\*\*轨\*\*\s*\|\s*(IP|FB)", text, re.I)
    if not track_m:
        track_m = re.search(r"轨[：:]\s*(IP|FB)", text, re.I)
    track = track_m.group(1).upper() if track_m else "IP"

    meta_block = text.split("## 口播全文", 1)[0] if "## 口播全文" in text else text
    location_meta = meta_table_field(meta_block, "地点")
    perspective_meta = meta_table_field(meta_block, "叙事视角")

    body_m = re.search(r"##\s*口播全文\s*\n([\s\S]+)", text)
    body_raw = body_m.group(1) if body_m else text
    body_stripped = body_raw.split("## 可选", 1)[0].strip()

    open_150 = body_stripped[:150]
    tail_200 = body_stripped[-200:] if len(body_stripped) > 200 else body_stripped
    scan_text = f"{meta_block}\n{body_stripped}"

    setting_france = any(k in scan_text for k in FRANCE_MARKERS)
    setting_italy = any(k in scan_text for k in ITALY_MARKERS)
    witness = any(k in scan_text for k in WITNESS_MARKERS)
    self_protagonist = any(k in scan_text for k in SELF_PROTAGONIST_MARKERS)
    title_italy = "意大利" in title
    location_mismatch = title_italy and setting_france and not any(
        k in body_stripped for k in ("意大利", "意大利站")
    )

    cjk = len(re.findall(r"[\u4e00-\u9fff]", body_stripped))

    narrative_facts = {
        "setting_france": setting_france,
        "setting_italy_mentioned": setting_italy,
        "witness_not_protagonist": witness and not self_protagonist,
        "title_location_mismatch": location_mismatch,
        "location_meta": location_meta,
        "perspective_meta": perspective_meta,
    }

    setting_zh = (
        "法国（主场景）"
        if setting_france and not location_mismatch
        else (
            "意大利（主场景）"
            if setting_italy and not setting_france
            else "多场景/见元数据"
        )
    )
    if location_meta:
        setting_zh = f"{setting_zh} · 元数据地点={location_meta}"
    perspective_zh = perspective_meta or (
        "全场目击者·非当事人" if narrative_facts["witness_not_protagonist"] else "当事人或混称（见全文）"
    )

    decision_summary = (
        f"【{title}】地点={setting_zh}；叙事={perspective_zh}；"
        f"witness_not_protagonist={narrative_facts['witness_not_protagonist']}；"
        f"title_location_mismatch={location_mismatch}；口播{cjk}字。"
    )
    if location_mismatch:
        decision_summary += " WARN：标题/文件名与正文主场景不一致，改标题后再给薯条/封面建议。"

    try:
        rel = str(path.relative_to(root)) if root else str(path)
    except ValueError:
        rel = str(path)

    return {
        "body_stripped": body_stripped,
        "id": path.stem,
        "file": rel,
        "title": title,
        "track": track,
        "sha256": sha256_file(path),
        "bytes": path.stat().st_size,
        "cjk_chars": cjk,
        "narrative_facts": narrative_facts,
        "decision_summary": decision_summary,
        "agent_decision_source": "full_md_parse",
        "forbid_agent": "禁止使用 body_preview / human_glance_only 做薯条·标题·地点·视角结论",
        "excerpts_for_orientation_only": {
            "lead_150": re.sub(r"\s+", " ", open_150).strip(),
            "tail_200": re.sub(r"\s+", " ", tail_200).strip(),
            "not_for_decisions": True,
        },
        "body_reading": {
            "must_read": "full_md_from_h2_口播全文_through_end",
            "scanned_chars_cjk": cjk,
        },
    }
