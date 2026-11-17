"""Parse Owner TEMPLATE-post-metrics.md tables into a flat dict."""

from __future__ import annotations

import re
from pathlib import Path


def _table_rows(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for line in text.splitlines():
        if not line.strip().startswith("|"):
            continue
        if "---" in line:
            continue
        parts = [p.strip() for p in line.split("|") if p.strip()]
        if len(parts) >= 2 and parts[0].lower() not in ("字段", "指标", "field", "metric"):
            out[parts[0]] = parts[1]
    return out


def parse_metrics_md(path: Path, *, platform: str) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    blocks = re.split(r"^##\s+", text, flags=re.M)
    meta: dict[str, str] = {}
    metrics: dict[str, str] = {}
    owner_note = ""
    for block in blocks:
        title = block.split("\n", 1)[0].strip().casefold()
        body = block.split("\n", 1)[-1] if "\n" in block else ""
        if "元数据" in title or "metadata" in title:
            meta = _table_rows(body)
        elif "指标" in title or "metrics" in title:
            metrics = _table_rows(body)
        elif "owner" in title or "判断" in title:
            owner_note = body.strip()[:2000]

    published = meta.get("published_at") or meta.get("发帖日") or ""
    as_of = meta.get("metrics_as_of") or meta.get("数据截止") or ""
    url = meta.get("post_url") or meta.get("url") or ""
    title = meta.get("title_or_hook") or meta.get("title") or path.stem

    def _intish(v: str) -> int | None:
        v = (v or "").replace(",", "").replace("，", "").strip()
        if not v or v in ("—", "-", ""):
            return None
        try:
            return int(float(v))
        except ValueError:
            return None

    numeric_metrics = {k: _intish(v) if _intish(v) is not None else v for k, v in metrics.items()}

    return {
        "platform": platform,
        "source_file": path.name,
        "published_at": published,
        "metrics_as_of": as_of,
        "post_url": url,
        "title": title,
        "brief_slug": meta.get("brief_slug") or "",
        "metrics": numeric_metrics,
        "owner_note": owner_note,
        "raw_meta": meta,
    }