#!/usr/bin/env python3
"""Merge all GM10 daily runs into Owner review catalog (no daily ping)."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INTEL = ROOT / "content/evolution/10-artist-intel"
OUT_JSON = ROOT / "content/ip-research/artist-intel-catalog.json"
OUT_MD = ROOT / "content/ip-research/artist-intel-catalog.md"
STATE = ROOT / "content/ip-research/artist-intel-review-state.json"


def main() -> int:
    entries: list[dict] = []
    for v0 in sorted(INTEL.glob("**/v0-benchmark.json")):
        if "watchlist-curated" in str(v0):
            continue
        try:
            data = json.loads(v0.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        parts = v0.parts
        try:
            idx = parts.index("10-artist-intel")
            day = parts[idx + 1]
            slug = parts[idx + 2] if len(parts) > idx + 2 else data.get("artist_slug", "?")
        except ValueError:
            day, slug = "?", data.get("artist_slug", "?")
        entries.append(
            {
                "date": day,
                "slug": slug,
                "artist_slug": data.get("artist_slug"),
                "borrow_score": data.get("borrow_score"),
                "why_evaluate": data.get("why_evaluate"),
                "alignment_points": data.get("alignment_points"),
                "timeline_len": len(data.get("timeline") or []),
                "sources_note": data.get("sources_note"),
                "path": str(v0.relative_to(ROOT)),
                "owner_verdict": None,
            }
        )

    # Dedupe by date+slug keep latest path
    seen: dict[str, dict] = {}
    for e in entries:
        key = f"{e['date']}:{e.get('artist_slug') or e['slug']}"
        seen[key] = e
    entries = sorted(seen.values(), key=lambda x: (x["date"], x.get("artist_slug") or ""))

    catalog = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "count": len(entries),
        "entries": entries,
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")

    if not STATE.is_file():
        STATE.write_text(
            json.dumps({"last_owner_review_at": None, "verdicts": {}}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    lines = [
        "# Artist 对标目录 · 供 Owner 打开对话时一次性审阅",
        "",
        f"_更新：{catalog['updated_at']} · 共 {len(entries)} 条 · 不每日打扰 Owner_",
        "",
        "审阅后告诉 Agent：**适合 / 不适合 / 为什么**；Agent 写入 `artist-intel-review-state.json`。",
        "",
        "| 日期 | slug | 借鉴分 | 摘要 | 文件 |",
        "|------|------|--------|------|------|",
    ]
    for e in entries[-30:]:
        why = (e.get("why_evaluate") or "")[:60].replace("|", "/") + "…"
        lines.append(
            f"| {e['date']} | {e.get('artist_slug') or e['slug']} | {e.get('borrow_score')} | {why} | `{e['path']}` |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_JSON} ({len(entries)} entries)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
