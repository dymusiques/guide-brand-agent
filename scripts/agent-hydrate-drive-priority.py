#!/usr/bin/env python3
"""
Hydrate CEO screen hydrate-priority files: download + full text extract (PDF/Office/md).

Supervision: records char_count, truncated, method per file — 禁止只读前几行当结论。
handoff → integration/handoff/owner-drive-hydrate-latest.json
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "integration/handoff/owner-drive-hydrate-latest.json"
SCREEN_JSON = ROOT / "content/evolution/00-manager/ceo-inbox/xhs-drive-screen-latest.json"
SECRETS = ROOT / "vendor/gdocs-skill/secrets"
MIRROR = ROOT / "content/personal-ip/intake/_mirror/hydrate-supervision"

sys.path.insert(0, str(ROOT / "scripts"))
from brand_gdocs_python import resolve_gdocs_python  # noqa: E402

MAX_CHARS = 50_000


def load_extractor():
    spec = importlib.util.spec_from_file_location(
        "drive_corpus_extract_text", ROOT / "scripts/drive_corpus_extract_text.py"
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("drive_corpus_extract_text missing")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_selected(limit: int) -> list[dict]:
    if not SCREEN_JSON.is_file():
        return []
    data = json.loads(SCREEN_JSON.read_text(encoding="utf-8"))
    task = data.get("task_bundle_dir")
    if task:
        hp = ROOT / task / "hydrate-priority.json"
        if hp.is_file():
            return json.loads(hp.read_text(encoding="utf-8"))[:limit]
    sel = data.get("selected") or []
    direct = [r for r in sel if r.get("tier") == "direct_hit"]
    use = direct if direct else sel
    return use[:limit]


def gdocs_download(file_id: str, out_dir: Path) -> bool:
    py = resolve_gdocs_python()
    out_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        str(py),
        "-m",
        "gdocs",
        "--secrets-dir",
        str(SECRETS),
        "drive",
        "download",
        file_id,
        "--output-dir",
        str(out_dir),
    ]
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=300)
    return r.returncode == 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=8)
    args = ap.parse_args()
    extract = load_extractor()
    items: list[dict] = []
    fail = 0

    for row in load_selected(args.limit):
        fid = str(row.get("id") or "")
        name = str(row.get("name") or fid)
        if not fid:
            continue
        mirror = MIRROR / fid
        ok_dl = gdocs_download(fid, mirror)
        text = ""
        method = "none"
        truncated = False
        if ok_dl:
            files = list(mirror.rglob("*"))
            files = [f for f in files if f.is_file() and f.name != ".DS_Store"]
            if files:
                target = max(files, key=lambda p: p.stat().st_size)
                text, method = extract.extract_text_from_path(target, max_chars=MAX_CHARS)
                truncated = len(text) >= MAX_CHARS - 2
        scan_only = "pdf empty or unreadable" in method or "OCR" in method
        blocked_dl = not ok_dl
        status = "PASS" if len(text.strip()) >= 200 else ("PARTIAL" if scan_only else "FAIL")
        if blocked_dl:
            status = "BLOCKED"
        if status == "FAIL":
            fail += 1
        items.append(
            {
                "id": fid,
                "name": name,
                "status": status,
                "mimeType": row.get("mimeType"),
                "download_ok": ok_dl,
                "char_count": len(text),
                "truncated": truncated,
                "extract_method": method,
                "supervision": {
                    "min_chars_for_decisions": 200,
                    "read_complete": len(text.strip()) >= 500,
                    "forbid": "仅用文件名或前 3 行摘录下薯条/投流结论",
                },
                "text_path": str((mirror / "extracted.txt").relative_to(ROOT)) if text else "",
            }
        )
        if text:
            (mirror / "extracted.txt").write_text(text, encoding="utf-8")

    complete = sum(1 for i in items if i.get("supervision", {}).get("read_complete"))
    partial = sum(1 for i in items if i.get("status") == "PARTIAL")
    need = min(4, len(items)) if items else 0
    ok = complete + partial >= need and complete >= max(1, need - 1)
    payload = {
        "as_of": datetime.now(timezone.utc).isoformat(),
        "source": str(SCREEN_JSON.relative_to(ROOT)),
        "items": items,
        "read_complete_count": complete,
        "partial_scan_pdf_count": partial,
        "status": "PASS" if ok else "PARTIAL" if complete else "FAIL",
        "fail_count": fail,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": payload["status"], "handoff": str(OUT.relative_to(ROOT))}))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
