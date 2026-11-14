#!/usr/bin/env python3
"""
Drive 备份全文 + 三平台大V笔触 · 统一硬门禁 handoff。

命中 copy/deep 触发词时 research-gate 必须本层 PASS。
handoff → integration/handoff/owner-copy-pipeline-gate-latest.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "integration/handoff/owner-copy-pipeline-gate-latest.json"
HYDRATE = ROOT / "integration/handoff/owner-drive-hydrate-latest.json"
SCREEN = ROOT / "content/evolution/00-manager/ceo-inbox/xhs-drive-screen-latest.json"
MANIFEST = ROOT / "integration/handoff/owner-drive-backup-manifest.json"
VOICE = ROOT / "integration/handoff/owner-platform-voice-benchmark-latest.json"
ROSTER = ROOT / "integration/handoff/platform-voice-benchmark-roster.json"
MONOREPO_PIPELINE = Path.home() / "Desktop/未命名/docs/agent/AGENT-OWNER-COPY-PIPELINE-GATE.json"

COPY_TRIGGERS = (
    "文案",
    "口播",
    "下一篇",
    "Medium",
    "LinkedIn",
    "领英",
    "大V",
    "对标",
    "笔触",
    "写稿",
    "小红书",
    "薯条",
    "Drive",
    "大师课",
)
DEEP_TRIGGERS = ("已发", "后台", "复盘", "监督", "补全", "数据分析", "为什么")


def goal_requires_pipeline(goal: str) -> bool:
    g = (goal or "").strip()
    if not g:
        return True
    hits = COPY_TRIGGERS + DEEP_TRIGGERS
    return any(t in g for t in hits)


def load_json(path: Path) -> dict | list | None:
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def direct_hit_ids(screen: dict | None, manifest: dict | None) -> set[str]:
    ids: set[str] = set()
    if screen:
        for row in screen.get("selected") or []:
            if row.get("tier") == "direct_hit" and row.get("id"):
                ids.add(str(row["id"]))
    if manifest:
        for row in manifest.get("pinned_drive_files") or []:
            if row.get("id"):
                ids.add(str(row["id"]))
    return ids


def check_drive(hydrate: dict | None, want_ids: set[str], rules: dict) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    ok_names: list[str] = []
    if not hydrate:
        return ["missing owner-drive-hydrate-latest.json"], ok_names
    items_by_id = {str(i.get("id")): i for i in (hydrate.get("items") or []) if i.get("id")}
    min_partial = int(rules.get("min_partial_chars") or 200)
    block = set(rules.get("block_statuses") or ["BLOCKED", "FAIL"])

    for fid in sorted(want_ids):
        it = items_by_id.get(fid)
        if not it:
            errors.append(f"Drive 未 hydrate: {fid}")
            continue
        name = str(it.get("name") or fid)
        st = str(it.get("status") or "")
        sup = it.get("supervision") or {}
        complete = bool(sup.get("read_complete"))
        cc = int(it.get("char_count") or 0)
        if st in block:
            errors.append(f"{name}: status={st} download_ok={it.get('download_ok')}")
            continue
        if complete:
            ok_names.append(name)
            continue
        if st == "PARTIAL" and cc >= min_partial:
            ok_names.append(f"{name} (PARTIAL/OCR)")
            continue
        errors.append(f"{name}: 未全文 read_complete char_count={cc} status={st}")
    return errors, ok_names


def check_voice(voice: dict | None, roster: dict | None, goal: str, rules: dict) -> list[str]:
    errors: list[str] = []
    min_n = int(rules.get("min_accounts_per_platform") or 2)
    plats = rules.get("platforms") or ["xiaohongshu", "linkedin", "medium"]
    if not voice or voice.get("status") != "PASS":
        errors.append(f"platform_voice handoff missing or status!=PASS ({(voice or {}).get('status')})")
    elif goal and goal not in str(voice.get("goal") or "") and str(voice.get("goal") or "") not in goal:
        errors.append(f"platform_voice goal mismatch: {voice.get('goal')!r} vs {goal!r}")
    if not roster:
        errors.append("missing platform-voice-benchmark-roster.json")
    else:
        for plat in plats:
            if len(roster.get(plat) or []) < min_n:
                errors.append(f"{plat} roster < {min_n}")
    return errors


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--goal", default="")
    ap.add_argument("--skip-if-unrelated", action="store_true")
    args = ap.parse_args()
    goal = (args.goal or "").strip()

    if args.skip_if_unrelated and goal and not goal_requires_pipeline(goal):
        payload = {
            "schema": "owner_copy_pipeline_gate_v1",
            "status": "SKIP",
            "goal": goal,
            "reason": "goal not in copy/deep triggers",
        }
        OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"status": "SKIP", "handoff": str(OUT.relative_to(ROOT))}))
        return 0

    rules_drive = {"min_partial_chars": 200, "block_statuses": ["BLOCKED", "FAIL"]}
    rules_voice = {"min_accounts_per_platform": 2, "platforms": ["xiaohongshu", "linkedin", "medium"]}
    if MONOREPO_PIPELINE.is_file():
        pipe = load_json(MONOREPO_PIPELINE)
        if isinstance(pipe, dict):
            rules_drive.update(pipe.get("drive_backup_rules") or {})
            rules_voice.update(pipe.get("platform_voice_rules") or {})

    screen = load_json(SCREEN)
    manifest = load_json(MANIFEST)
    hydrate = load_json(HYDRATE)
    voice = load_json(VOICE)
    roster = load_json(ROSTER)
    want = direct_hit_ids(screen if isinstance(screen, dict) else None, manifest if isinstance(manifest, dict) else None)
    if not want and isinstance(manifest, dict):
        want = {str(r["id"]) for r in manifest.get("pinned_drive_files") or [] if r.get("id")}

    drive_err, drive_ok = check_drive(hydrate if isinstance(hydrate, dict) else None, want, rules_drive)
    voice_err = check_voice(voice if isinstance(voice, dict) else None, roster if isinstance(roster, dict) else None, goal, rules_voice)
    all_err = drive_err + voice_err
    status = "PASS" if not all_err else "FAIL"

    payload = {
        "schema": "owner_copy_pipeline_gate_v1",
        "as_of": datetime.now(timezone.utc).isoformat(),
        "goal": goal,
        "monorepo_contract": str(MONOREPO_PIPELINE) if MONOREPO_PIPELINE.is_file() else None,
        "drive": {
            "direct_hit_ids_count": len(want),
            "files_ok": drive_ok,
            "errors": drive_err,
        },
        "platform_voice": {
            "handoff": str(VOICE.relative_to(ROOT)),
            "errors": voice_err,
        },
        "hard_thresholds": {
            "drive_read_complete_or_partial": True,
            "platform_roster_per_platform_min": rules_voice.get("min_accounts_per_platform"),
            "forbid_blocked_download": True,
        },
        "status": status,
        "fail_count": len(all_err),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": status, "handoff": str(OUT.relative_to(ROOT)), "fail_count": len(all_err)}))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())