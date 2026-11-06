#!/usr/bin/env python3
"""List all CEO corpus Drive folders and write merged catalog for screen-xhs-drive-corpus."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FOLDERS_JSON = ROOT / "integration/handoff/ceo-drive-corpus-folders.json"
SECRETS = ROOT / "vendor/gdocs-skill/secrets"
LEGACY_CATALOG = (
    ROOT / "content/personal-ip/intake/_raw/xhs-ip-2026-11-03/drive-listing-2026-11-03-live.json"
)


def _import_drive_client():
    sys.path.insert(0, str(ROOT / "vendor/gdocs-skill"))
    from gdocs.drive_client import DriveClient, FOLDER

    return DriveClient, FOLDER


def web_view_link(file_id: str) -> str:
    return f"https://drive.google.com/file/d/{file_id}/view?usp=drivesdk"


def normalize_file(item: dict, *, source_folder_id: str, source_label: str) -> dict:
    fid = item.get("id") or ""
    return {
        "id": fid,
        "name": item.get("name") or "",
        "mimeType": item.get("mimeType") or "",
        "size": str(item.get("size") or ""),
        "modifiedTime": item.get("modifiedTime") or "",
        "webViewLink": item.get("webViewLink") or web_view_link(fid),
        "source_folder_id": source_folder_id,
        "source_label": source_label,
    }


def list_folder_files(client, folder_id: str, *, recursive: bool, FolderMime: str) -> list[dict]:
    """List files in folder; optional one-level subfolders (not full tree download)."""
    out: list[dict] = []

    def walk(parent_id: str) -> None:
        for item in client.children(parent_id):
            mime = item.get("mimeType") or ""
            if mime == FolderMime and recursive:
                walk(item["id"])
                continue
            if mime == FolderMime:
                continue
            out.append(item)

    walk(folder_id)
    return out


def load_config(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def merge_legacy_if_missing(cfg: dict, merged_files: list[dict], listed_folder_ids: set[str]) -> list[dict]:
    """If API list fails for a folder, keep prior catalog entries for that folder."""
    out_path = ROOT / cfg["catalog_output"]
    if out_path.is_file():
        prior = json.loads(out_path.read_text(encoding="utf-8"))
        for f in prior.get("files") or []:
            sid = f.get("source_folder_id") or prior.get("folder_id") or ""
            if sid and sid not in listed_folder_ids:
                merged_files.append(f)
    if LEGACY_CATALOG.is_file():
        legacy_id = "1SrD2n_zXN2HjhH_YPbQa-_54YakKXbzZ"
        if legacy_id not in listed_folder_ids:
            legacy = json.loads(LEGACY_CATALOG.read_text(encoding="utf-8"))
            for f in legacy.get("files") or []:
                merged_files.append(
                    normalize_file(
                        f,
                        source_folder_id=legacy_id,
                        source_label="小红书 IP 资料",
                    )
                )
    return merged_files


def main() -> int:
    p = argparse.ArgumentParser(description="Refresh merged CEO Drive catalog from integration/handoff/ceo-drive-corpus-folders.json")
    p.add_argument("--config", type=Path, default=FOLDERS_JSON)
    p.add_argument(
        "--no-recursive",
        action="store_true",
        help="Only list files in folder root (default: include all subfolders)",
    )
    p.add_argument("--dry-run", action="store_true", help="Print counts only, do not write catalog")
    args = p.parse_args()

    cfg_path = args.config if args.config.is_absolute() else ROOT / args.config
    if not cfg_path.is_file():
        print(f"config missing: {cfg_path}", file=sys.stderr)
        return 2
    cfg = load_config(cfg_path)
    folders = cfg.get("folders") or []
    if not folders:
        print("no folders in config", file=sys.stderr)
        return 2

    DriveClient, FOLDER = _import_drive_client()
    client = DriveClient(SECRETS)

    merged: list[dict] = []
    folder_meta: list[dict] = []
    listed_ids: set[str] = set()
    errors: list[str] = []

    for spec in folders:
        fid = spec.get("drive_folder_id") or ""
        label = spec.get("label") or fid
        if not fid:
            continue
        try:
            try:
                meta = client.metadata(fid)
                drive_name = (meta.get("name") or "").strip()
                if drive_name:
                    label = drive_name
            except Exception:
                pass
            raw = list_folder_files(client, fid, recursive=not args.no_recursive, FolderMime=FOLDER)
            listed_ids.add(fid)
            folder_meta.append(
                {
                    "label": label,
                    "drive_folder_id": fid,
                    "drive_link": spec.get("drive_link") or f"https://drive.google.com/drive/folders/{fid}",
                    "file_count": len(raw),
                    "recursive": not args.no_recursive,
                }
            )
            for item in raw:
                merged.append(normalize_file(item, source_folder_id=fid, source_label=label))
        except Exception as exc:  # noqa: BLE001 — report per folder, merge legacy
            errors.append(f"{label} ({fid}): {exc}")

    if not merged and errors:
        merged = merge_legacy_if_missing(cfg, merged, listed_ids)
        if not merged:
            print("\n".join(errors), file=sys.stderr)
            return 1

    # Dedupe by file id (same file should not appear twice)
    by_id: dict[str, dict] = {}
    for f in merged:
        by_id[f["id"]] = f
    files = list(by_id.values())
    total_bytes = sum(int(f.get("size") or 0) for f in files if str(f.get("size") or "").isdigit())

    payload = {
        "listed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "version": cfg.get("version") or "ceo-drive-catalog",
        "folders": folder_meta,
        "folder_count": len(folder_meta),
        "file_count": len(files),
        "total_bytes": total_bytes,
        "files": files,
        "errors": errors,
        "config": str(cfg_path.relative_to(ROOT)),
    }

    if args.dry_run:
        print(json.dumps({"file_count": len(files), "folders": folder_meta, "errors": errors}, ensure_ascii=False, indent=2))
        return 0 if files else 1

    out = ROOT / cfg["catalog_output"]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary = {
        "wrote": str(out.relative_to(ROOT)),
        "file_count": len(files),
        "folder_count": len(folder_meta),
        "per_folder": {m["drive_folder_id"]: m["file_count"] for m in folder_meta},
        "errors": errors,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if errors:
        return 1
    return 0 if files else 1


if __name__ == "__main__":
    raise SystemExit(main())
