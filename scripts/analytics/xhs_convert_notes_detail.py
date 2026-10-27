#!/usr/bin/env python3
"""Convert 小红书「笔记列表明细表」xlsx → inbox CSV (schema in analytics/schemas.py)."""

from __future__ import annotations

import argparse
import csv
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "analytics"))

from schemas import XHS_CSV_FIELDNAMES  # noqa: E402
from xhs_note_detail import load_details_from_dir, merge_details_into_rows  # noqa: E402
from xhs_note_links import DEFAULT_REGISTRY, apply_links_to_rows, load_registry  # noqa: E402

try:
    import openpyxl
except ImportError:
    print("error: pip install openpyxl", file=sys.stderr)
    sys.exit(2)

HEADER_ROW_MARKERS = ("笔记标题", "首次发布时间")
DATE_RE = re.compile(
    r"(\d{4})年(\d{1,2})月(\d{1,2})日"
)


def parse_publish_date(raw: object) -> str:
    if raw is None:
        return ""
    s = str(raw).strip()
    m = DATE_RE.search(s)
    if not m:
        return s[:10] if len(s) >= 10 else s
    y, mo, d = m.group(1), int(m.group(2)), int(m.group(3))
    return f"{y}-{mo:02d}-{d:02d}"


def note_id_from(title: str, publish_date: str) -> str:
    t = title.strip().replace(",", " ")
    return f"xhs:{publish_date}:{t[:80]}"


def default_pillar(title: str) -> str:
    brand_kw = ("品牌", "跨界", "叙事", "艺术?", "站得住", "不可替代")
    if any(k in title for k in brand_kw):
        return "跨界品牌"
    return "艺术专业"


def read_notes_sheet(path: Path) -> list[dict[str, str]]:
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    wb.close()
    header_idx = None
    for i, row in enumerate(rows):
        if row and row[0] == HEADER_ROW_MARKERS[0]:
            header_idx = i
            break
    if header_idx is None:
        raise ValueError(f"{path}: cannot find header row 笔记标题")
    header = [str(c).strip() if c is not None else "" for c in rows[header_idx]]
    col = {name: idx for idx, name in enumerate(header)}

    def get(row: tuple, name: str, default: str = "") -> str:
        idx = col.get(name)
        if idx is None or idx >= len(row) or row[idx] is None:
            return default
        return str(row[idx]).strip()

    out: list[dict[str, str]] = []
    for row in rows[header_idx + 1 :]:
        if not row or not row[0]:
            continue
        title = get(row, "笔记标题")
        if not title or title.startswith("最多导出"):
            continue
        pub = parse_publish_date(get(row, "首次发布时间"))
        nid = note_id_from(title, pub)
        out.append(
            {
                "note_id": nid,
                "publish_date": pub,
                "title": title,
                "pillar": default_pillar(title),
                "impressions": get(row, "曝光", "0"),
                "views": get(row, "观看量", "0"),
                "likes": get(row, "点赞", "0"),
                "collects": get(row, "收藏", "0"),
                "comments": get(row, "评论", "0"),
                "shares": get(row, "分享", "0"),
                "follows_from_note": get(row, "涨粉", "0"),
                "dm_count": "0",
                "dm_keywords": "",
                "aligned_at_publish": "",
                "brief_path": "",
                "cover_ctr_pct": "",
                "avg_watch_sec": "",
                "completion_rate_pct": "",
                "exit_2s_rate_pct": "",
                "detail_source": "",
            }
        )
    return out


def write_csv(rows: list[dict[str, str]], dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=XHS_CSV_FIELDNAMES, extrasaction="ignore")
        w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k, "") for k in XHS_CSV_FIELDNAMES})


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--xlsx", type=Path, required=True)
    parser.add_argument(
        "--out",
        type=Path,
        help="Output CSV (default: content/analytics/inbox/xiaohongshu-YYYY-MM-DD.csv)",
    )
    parser.add_argument(
        "--links",
        type=Path,
        default=DEFAULT_REGISTRY,
        help="note-links registry CSV (default: content/analytics/xiaohongshu/note-links.csv)",
    )
    parser.add_argument(
        "--detail-dir",
        type=Path,
        default=ROOT / "content/analytics/raw/xiaohongshu/note-details",
        help="Folder with *数据明细表.xlsx (single-note exports)",
    )
    args = parser.parse_args()
    if not args.xlsx.is_file():
        print(f"error: not found {args.xlsx}", file=sys.stderr)
        return 2
    rows = read_notes_sheet(args.xlsx)
    if not rows:
        print("error: no note rows parsed", file=sys.stderr)
        return 1
    links_path = args.links if args.links.is_absolute() else (ROOT / args.links).resolve()
    registry = load_registry(links_path)
    if registry:
        rows, applied = apply_links_to_rows(rows, registry)
        print(f"note links: {applied}/{len(rows)} from {links_path.relative_to(ROOT)}")
    detail_dir = (
        args.detail_dir if args.detail_dir.is_absolute() else (ROOT / args.detail_dir).resolve()
    )
    by_title = load_details_from_dir(detail_dir)
    if by_title:
        rows, dmerged = merge_details_into_rows(rows, by_title)
        print(f"note detail metrics: {dmerged}/{len(rows)} from {detail_dir.relative_to(ROOT)}")
    out = args.out or (
        ROOT / "content/analytics/inbox" / f"xiaohongshu-{date.today().isoformat()}.csv"
    )
    if not out.is_absolute():
        out = (ROOT / out).resolve()
    write_csv(rows, out)
    print(f"wrote {len(rows)} rows → {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    from datetime import date

    sys.exit(main())
