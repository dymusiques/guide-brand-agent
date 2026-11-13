#!/usr/bin/env python3
"""Merge 笔记列表明细表 exports + detail xlsx → notes.csv · snapshots · Owner Excel."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "analytics"))

from schemas import XHS_CSV_FIELDNAMES  # noqa: E402
from xhs_convert_notes_detail import read_notes_sheet, write_csv  # noqa: E402
from xhs_note_detail import load_details_from_dir, merge_details_into_rows  # noqa: E402
from xhs_note_links import (  # noqa: E402
    DEFAULT_REGISTRY,
    DEFAULT_WORKBOOK,
    _rows_for_workbook,
    apply_links_to_rows,
    load_registry,
    merge_registry,
    write_registry,
    write_workbook,
)

DETAIL_GLOB = "*数据明细表.xlsx"
LIST_GLOB = "notes-detail.xlsx"
ACCOUNT_GLOB = "account-*.xlsx"


def _count_notes(path: Path) -> int:
    try:
        return len(read_notes_sheet(path))
    except (ValueError, OSError):
        return 0


def discover_list_exports(raw_root: Path) -> list[Path]:
    found: list[Path] = []
    if not raw_root.is_dir():
        return found
    for path in sorted(raw_root.glob("*/notes-detail.xlsx")):
        if path.is_file():
            found.append(path)
    for path in sorted(raw_root.glob("*/notes-list-*.xlsx")):
        if path.is_file():
            found.append(path)
    sync = raw_root / "drive-sync-latest"
    for pattern in ("笔记列表明细表*.xlsx", "*notes-detail*.xlsx"):
        found.extend(sorted(sync.glob(pattern)) if sync.is_dir() else [])
    # de-dup
    seen: set[str] = set()
    out: list[Path] = []
    for p in found:
        key = str(p.resolve())
        if key in seen:
            continue
        seen.add(key)
        out.append(p)
    return out


def merge_list_rows(exports: list[Path]) -> list[dict[str, str]]:
    exports_sorted = sorted(exports, key=_count_notes, reverse=True)
    by_key: dict[tuple[str, str], dict[str, str]] = {}
    for path in exports_sorted:
        try:
            rows = read_notes_sheet(path)
        except ValueError as exc:
            print(f"skip list {path.name}: {exc}", file=sys.stderr)
            continue
        for r in rows:
            by_key[(r["publish_date"], r["title"])] = r
    return sorted(by_key.values(), key=lambda x: (x["publish_date"], x["title"]), reverse=True)


def stage_uploads(source: Path, raw_root: Path, as_of: str) -> Path:
    archive = raw_root / as_of
    archive.mkdir(parents=True, exist_ok=True)
    detail_dir = raw_root / "note-details"
    detail_dir.mkdir(parents=True, exist_ok=True)
    if not source.is_dir():
        raise FileNotFoundError(source)
    for path in sorted(source.iterdir()):
        if not path.is_file() or path.suffix.lower() != ".xlsx":
            continue
        name = path.name
        if "笔记列表明细表" in name or "notes-detail" in name.lower():
            safe = re.sub(r"[^\w\u4e00-\u9fff.-]+", "-", path.stem)[:40]
            list_dest = archive / f"notes-list-{safe}.xlsx"
            shutil.copy2(path, list_dest)
            canonical = archive / "notes-detail.xlsx"
            if (not canonical.exists()) or _count_notes(path) >= _count_notes(canonical):
                shutil.copy2(path, canonical)
            print(f"staged list → {list_dest.relative_to(ROOT)}")
        elif "数据明细表" in name:
            dest_name = name
            if not re.search(r"数据明细表\.xlsx$", name):
                dest_name = re.sub(r"-?\d+\.xlsx$", ".xlsx", name)
                if not dest_name.endswith("数据明细表.xlsx"):
                    dest_name = name
            shutil.copy2(path, detail_dir / dest_name)
            print(f"staged detail → note-details/{dest_name}")
        elif "近7日" in name or "近30日" in name:
            dest = None
            for key, fname in (
                ("观看", "account-views-7d.xlsx"),
                ("互动", "account-interaction-7d.xlsx"),
                ("涨粉", "account-followers-7d.xlsx"),
                ("发布", "account-publish-7d.xlsx"),
            ):
                if key in name:
                    dest = archive / fname
                    break
            if dest is None:
                stem = re.sub(r"[^\w\u4e00-\u9fff]+", "-", path.stem)[:48]
                dest = archive / f"account-{stem}.xlsx"
            shutil.copy2(path, dest)
            print(f"staged account → {archive.name}/{dest.name}")
    return archive


ACCOUNT_7D_KINDS = (
    ("观看", "views", "近7日观看数据", "account-*views*"),
    ("互动", "interaction", "近7日互动数据", "account-*interaction*"),
    ("涨粉", "followers", "近7日涨粉数据", "account-*followers*"),
    ("发布", "publish", "近7日发布数据", "account-*publish*"),
)


def _resolve_account_file(archive: Path, glob_pat: str) -> Path | None:
    for path in sorted(archive.glob(glob_pat)):
        if path.is_file():
            return path
    return None


def _parse_account_overview_xlsx(path: Path) -> dict[str, str]:
    try:
        import openpyxl
    except ImportError:
        return {}
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb.active
    out: dict[str, str] = {}
    for row in ws.iter_rows(max_row=40, values_only=True):
        if not row or row[0] is None:
            continue
        key = str(row[0]).strip()
        if key == "指标":
            continue
        val = row[1] if len(row) > 1 else ""
        if val is None:
            continue
        out[key] = str(val).strip() if isinstance(val, float) and val == int(val) else str(val)
    wb.close()
    return out


def _mom_pct(metrics: dict[str, str], base_key: str) -> str:
    for suffix in (f"{base_key}环比(%)", f"{base_key}环比"):
        if suffix in metrics:
            return metrics[suffix]
    return ""


def build_account_7d_rows(archive: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for dimension, _slug, source_label, glob_pat in ACCOUNT_7D_KINDS:
        path = _resolve_account_file(archive, glob_pat)
        if not path:
            continue
        metrics = _parse_account_overview_xlsx(path)
        skip_suffix = "环比"
        for key, val in metrics.items():
            if skip_suffix in key:
                continue
            rows.append(
                {
                    "dimension": dimension,
                    "metric": key,
                    "value_7d": val,
                    "mom_pct": _mom_pct(metrics, key),
                    "source_file": source_label,
                    "source_path": path.name,
                }
            )
    return rows


def write_account_7d_json(rows: list[dict[str, str]], as_of: str) -> Path:
    payload = {"as_of": as_of, "window": "近7日", "metrics": rows}
    dest = ROOT / f"content/analytics/xiaohongshu/account-7d-summary-{as_of}.json"
    dest.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return dest


def _copy_sheet_values(src_ws, dest_wb, title: str) -> None:
    import openpyxl
    from openpyxl.styles import Font

    safe = title[:31]
    if safe in dest_wb.sheetnames:
        del dest_wb[safe]
    dest = dest_wb.create_sheet(safe)
    for row in src_ws.iter_rows(values_only=True):
        if row and any(c is not None for c in row):
            dest.append(list(row))
    if dest.max_row:
        for cell in dest[1]:
            if cell.value in ("指标", "日期"):
                for c in dest[1]:
                    c.font = Font(bold=True)
                break


def export_account_7d_workbook(archive: Path, as_of: str) -> Path | None:
    """账号近7日 · 独立工作簿（与笔记全量分离，禁止合并口径）。"""
    try:
        import openpyxl
        from openpyxl.styles import Font
    except ImportError:
        print("warn: openpyxl missing; skip account 7d export", file=sys.stderr)
        return None

    summary_rows = build_account_7d_rows(archive)
    if not summary_rows:
        return None
    json_path = write_account_7d_json(summary_rows, as_of)

    export_name = f"小红书账号近7日-{as_of}.xlsx"
    export_path = ROOT / "content/analytics/xiaohongshu" / export_name

    wb = openpyxl.Workbook()
    ws_sum = wb.active
    ws_sum.title = "账号近7日总览"
    ws_sum.append(["维度", "指标", "近7日数值", "环比(%)", "数据来源", "归档文件名"])
    for cell in ws_sum[1]:
        cell.font = Font(bold=True)
    for r in summary_rows:
        ws_sum.append(
            [
                r["dimension"],
                r["metric"],
                r["value_7d"],
                r["mom_pct"],
                r["source_file"],
                r["source_path"],
            ]
        )

    prefixes = {
        "views": "观看",
        "interaction": "互动",
        "followers": "涨粉",
        "publish": "发布",
    }
    for _dim, slug, _label, glob_pat in ACCOUNT_7D_KINDS:
        path = _resolve_account_file(archive, glob_pat)
        if not path:
            continue
        prefix = prefixes.get(slug, slug)
        src_wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
        for sheet_name in src_wb.sheetnames:
            title = f"{prefix}·{sheet_name}"[:31]
            _copy_sheet_values(src_wb[sheet_name], wb, title)
        src_wb.close()

    guide = wb.create_sheet("使用说明")
    guide.append(["本文件", "账号近7日（观看/互动/涨粉/发布）"])
    guide.append(["不是", f"笔记24篇全量 → 请打开 小红书笔记全量-{as_of}.xlsx"])
    guide.append(["趋势", "见各「观看·」「互动·」等工作表"])
    guide.append(["更新", as_of])

    wb.save(export_path)
    downloads = Path.home() / "Downloads" / export_name
    shutil.copy2(export_path, downloads)
    print(f"account 7d export → {export_path.relative_to(ROOT)} · {downloads}")
    return export_path


def run_merge(
    raw_root: Path,
    detail_dir: Path,
    registry: Path,
    *,
    as_of: str | None = None,
) -> tuple[list[dict[str, str]], Path, Path]:
    as_of = as_of or date.today().isoformat()
    exports = discover_list_exports(raw_root)
    if not exports:
        raise SystemExit("error: no 笔记列表明细表 / notes-detail.xlsx under raw/xiaohongshu")
    rows = merge_list_rows(exports)
    if not rows:
        raise SystemExit("error: no note rows after merge")
    reg = load_registry(registry)
    rows, link_n = apply_links_to_rows(rows, reg)
    by_title = load_details_from_dir(detail_dir)
    rows, detail_n = merge_details_into_rows(rows, by_title)
    print(f"warehouse: {len(rows)} rows · links {link_n} · details {detail_n}")

    notes_csv = ROOT / "content/analytics/xiaohongshu/notes.csv"
    write_csv(rows, notes_csv)

    # registry scaffold for rows that only appear in newest export
    newest = max(exports, key=lambda p: p.stat().st_mtime)
    try:
        new_only = read_notes_sheet(newest)
    except ValueError:
        new_only = []
    if new_only:
        merged_reg = merge_registry(
            reg,
            [
                {
                    "publish_date": r["publish_date"],
                    "title": r["title"],
                    "note_url": "",
                    "brief_path": "",
                }
                for r in new_only
            ],
        )
        write_registry(registry, merged_reg)

    base_xlsx = max(exports, key=_count_notes)
    wb_rows = _rows_for_workbook(base_xlsx, load_registry(registry))
    merged_by = {(r["publish_date"], r["title"]): r for r in rows}
    out_wb_data: list[dict[str, str]] = []
    for wr in wb_rows:
        m = merged_by.get((wr["publish_date"], wr["title"]))
        if m:
            nid = m.get("note_id") or ""
            wr.update(
                {
                    "impressions": m.get("impressions", wr.get("impressions", "")),
                    "views": m.get("views", wr.get("views", "")),
                    "likes": m.get("likes", wr.get("likes", "")),
                    "collects": m.get("collects", wr.get("collects", "")),
                    "comments": m.get("comments", wr.get("comments", "")),
                    "shares": m.get("shares", wr.get("shares", "")),
                    "follows_from_note": m.get("follows_from_note", wr.get("follows_from_note", "")),
                    "pillar": m.get("pillar", wr.get("pillar", "")),
                    "note_url": nid if nid.startswith("http") else wr.get("note_url", ""),
                }
            )
        out_wb_data.append(wr)
    old_keys = {(r["publish_date"], r["title"]) for r in wb_rows}
    for m in rows:
        k = (m["publish_date"], m["title"])
        if k in old_keys:
            continue
        out_wb_data.append(
            {
                "publish_date": m["publish_date"],
                "title": m["title"],
                "impressions": m.get("impressions", ""),
                "views": m.get("views", ""),
                "likes": m.get("likes", ""),
                "collects": m.get("collects", ""),
                "comments": m.get("comments", ""),
                "shares": m.get("shares", ""),
                "follows_from_note": m.get("follows_from_note", ""),
                "pillar": m.get("pillar", ""),
                "note_url": m.get("note_id") if (m.get("note_id") or "").startswith("http") else "",
                "brief_path": m.get("brief_path", ""),
            }
        )
    out_wb_data.sort(key=lambda x: (x["publish_date"], x["title"]), reverse=True)
    write_workbook(DEFAULT_WORKBOOK, out_wb_data)

    export_name = f"小红书笔记全量-{as_of}.xlsx"
    export_path = ROOT / "content/analytics/xiaohongshu" / export_name
    try:
        import openpyxl
        from openpyxl.styles import Font

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "笔记全量24篇"
        extra_keys = (
            "cover_ctr_pct",
            "avg_watch_sec",
            "completion_rate_pct",
            "exit_2s_rate_pct",
            "detail_source",
        )
        headers = [
            "首次发布时间",
            "笔记标题",
            "曝光",
            "观看量",
            "点赞",
            "收藏",
            "评论",
            "分享",
            "涨粉",
            "支柱",
            "笔记链接",
            "封面点击率%",
            "平均观看秒",
            "完播率%",
            "2秒退出率%",
            "明细来源xlsx",
        ]
        ws.append(headers)
        for cell in ws[1]:
            cell.font = Font(bold=True)
        ws.freeze_panes = "A2"
        url_by = {(w["publish_date"], w["title"]): w.get("note_url", "") for w in out_wb_data}
        for m in rows:
            ws.append(
                [
                    m["publish_date"],
                    m.get("title", ""),
                    m.get("impressions", ""),
                    m.get("views", ""),
                    m.get("likes", ""),
                    m.get("collects", ""),
                    m.get("comments", ""),
                    m.get("shares", ""),
                    m.get("follows_from_note", ""),
                    m.get("pillar", ""),
                    url_by.get((m["publish_date"], m["title"]), ""),
                    m.get("cover_ctr_pct", ""),
                    m.get("avg_watch_sec", ""),
                    m.get("completion_rate_pct", ""),
                    m.get("exit_2s_rate_pct", ""),
                    m.get("detail_source", ""),
                ]
            )
        guide = wb.create_sheet("使用说明")
        guide.append(["本文件", "笔记全量（24篇）· 每篇累计指标"])
        guide.append(["不是", f"账号近7日 → 请打开 小红书账号近7日-{as_of}.xlsx"])
        guide.append(["行数", len(rows)])
        guide.append(["更新", as_of])
        wb.save(export_path)
        downloads_notes = Path.home() / "Downloads" / export_name
        shutil.copy2(export_path, downloads_notes)
        print(f"notes export → {export_path.relative_to(ROOT)} · {downloads_notes}")
    except Exception as exc:
        print(f"warn: notes workbook {exc}", file=sys.stderr)
        shutil.copy2(DEFAULT_WORKBOOK, export_path)

    archive = raw_root / as_of
    if archive.is_dir():
        export_account_7d_workbook(archive, as_of)

    snap = {
        "as_of": as_of,
        "rows": [
            {
                "publish_date": r["publish_date"],
                "title": r["title"],
                "note_id": r.get("note_id", ""),
                "pillar": r.get("pillar", ""),
                "impressions": r.get("impressions", ""),
                "views": r.get("views", ""),
                "likes": r.get("likes", ""),
                "collects": r.get("collects", ""),
                "comments": r.get("comments", ""),
                "follows_from_note": r.get("follows_from_note", ""),
                "cover_ctr_pct": r.get("cover_ctr_pct", ""),
                "completion_rate_pct": r.get("completion_rate_pct", ""),
                "brief_path": r.get("brief_path", ""),
                "detail_source": r.get("detail_source", ""),
            }
            for r in rows
        ],
    }
    snap_path = ROOT / f"content/analytics/xiaohongshu/notes-snapshot-{as_of}.json"
    snap_path.write_text(json.dumps(snap, ensure_ascii=False, indent=2), encoding="utf-8")

    return rows, notes_csv, export_path


def cmd_merge(args: argparse.Namespace) -> int:
    raw = args.raw_root if args.raw_root.is_absolute() else (ROOT / args.raw_root).resolve()
    detail = args.detail_dir if args.detail_dir.is_absolute() else (ROOT / args.detail_dir).resolve()
    reg = args.registry if args.registry.is_absolute() else (ROOT / args.registry).resolve()
    run_merge(raw, detail, reg, as_of=args.as_of)
    return 0


def cmd_stage_and_merge(args: argparse.Namespace) -> int:
    src = args.from_dir if args.from_dir.is_absolute() else Path(args.from_dir).resolve()
    raw = ROOT / "content/analytics/raw/xiaohongshu"
    as_of = args.as_of or date.today().isoformat()
    stage_uploads(src, raw, as_of)
    return cmd_merge(
        argparse.Namespace(
            raw_root=raw,
            detail_dir=raw / "note-details",
            registry=DEFAULT_REGISTRY,
            as_of=as_of,
        )
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="XHS analytics warehouse merge + Excel export")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_merge = sub.add_parser("merge", help="Merge all raw list xlsx + details → notes.csv + Excel")
    p_merge.add_argument("--raw-root", type=Path, default=ROOT / "content/analytics/raw/xiaohongshu")
    p_merge.add_argument("--detail-dir", type=Path, default=ROOT / "content/analytics/raw/xiaohongshu/note-details")
    p_merge.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    p_merge.add_argument("--as-of", default=None)
    p_merge.set_defaults(func=cmd_merge)

    p_stage = sub.add_parser("stage", help="Copy Owner uploads into raw/ + merge")
    p_stage.add_argument("--from-dir", type=Path, required=True)
    p_stage.add_argument("--as-of", default=None)
    p_stage.set_defaults(func=cmd_stage_and_merge)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
