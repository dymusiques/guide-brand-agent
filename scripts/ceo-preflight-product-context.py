#!/usr/bin/env python3
"""Resolve Owner track: FluteBuddy product and/or personal IP ecosystem before CEO screen."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from ceo_goal_tracks import is_flutebuddy_goal, is_ip_ecosystem_goal, primary_track  # noqa: E402

REGISTRY = ROOT / "integration/handoff/owner-product-registry.json"
IP_TRACK = ROOT / "integration/handoff/owner-ip-track.json"
COPY_V_TIER = ROOT / "integration/handoff/owner-copy-v-tier-400k.json"
COPY_MANDATE_PATHS = [
    "docs/OWNER-COPY-V-TIER-400K-MANDATE.md",
    "docs/OWNER-DUAL-TRACK-COPY-WORKFLOW.md",
    "integration/handoff/owner-copy-v-tier-400k.json",
    "integration/handoff/owner-copy-benchmarks-tier2.json",
]
OUT = ROOT / "content/evolution/00-manager/ceo-inbox/product-context-resolved-latest.json"
OUT_OWNER = ROOT / "content/evolution/00-manager/ceo-inbox/owner-context-resolved-latest.json"


def load_registry() -> dict:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def load_ip_track() -> dict:
    if IP_TRACK.is_file():
        return json.loads(IP_TRACK.read_text(encoding="utf-8"))
    return {}


def grep_repo(term: str, limit: int = 12) -> list[str]:
    r = subprocess.run(
        ["rg", "-l", "-i", term, "content", "rules", "integration", "docs"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    lines = [ln.strip() for ln in (r.stdout or "").splitlines() if ln.strip()]
    return lines[:limit]


def match_product(goal: str, registry: dict) -> tuple[dict | None, list[str]]:
    errors: list[str] = []
    goal_cf = goal.casefold()
    for prod in registry.get("products") or []:
        for name in prod.get("canonical_names") or []:
            if name.casefold() in goal_cf or name.replace(" ", "").casefold() in goal_cf.replace(" ", ""):
                return prod, errors
    if re.search(r"buddy|app|软件|练习", goal, re.I):
        if is_flutebuddy_goal(goal):
            pass
        elif "flute" not in goal_cf and "长笛" not in goal:
            errors.append("goal 像产品/App 任务但未出现 FluteBuddy/长笛 — 先读 owner-product-registry.json")
    return None, errors


def main() -> int:
    p = argparse.ArgumentParser(description="CEO owner context preflight (product + IP track)")
    p.add_argument("--goal", "-g", required=True)
    args = p.parse_args()
    goal = args.goal.strip()
    reg = load_registry() if REGISTRY.is_file() else {"products": []}
    ip_cfg = load_ip_track()
    prod, errs = match_product(goal, reg)
    ip_ok = is_ip_ecosystem_goal(goal)
    track = primary_track(goal)

    paths: list[str] = []
    if prod:
        for rel in prod.get("must_read") or []:
            pth = ROOT / rel
            if pth.is_file():
                paths.append(str(pth.relative_to(ROOT)))
        paths.extend(grep_repo(prod["canonical_names"][0]))
    if ip_ok:
        for rel in ip_cfg.get("must_read") or []:
            pth = ROOT / rel
            if pth.is_file():
                paths.append(str(pth.relative_to(ROOT)))
        for rel in (ip_cfg.get("benchmark_creators_json"), ip_cfg.get("content_json")):
            if rel:
                pth = ROOT / rel
                if pth.is_file():
                    paths.append(str(pth.relative_to(ROOT)))

    if track in ("product", "personal_ip", "mixed"):
        for rel in COPY_MANDATE_PATHS:
            pth = ROOT / rel
            if pth.is_file():
                paths.append(str(pth.relative_to(ROOT)))
        if COPY_V_TIER.is_file():
            vt = json.loads(COPY_V_TIER.read_text(encoding="utf-8"))
            tr = vt.get("tracks") or {}
            if prod and track in ("product", "mixed"):
                for rel in (tr.get("flutebuddy_product") or {}).get("must_read_extra") or []:
                    pth = ROOT / rel
                    if pth.is_file():
                        paths.append(str(pth.relative_to(ROOT)))
            if ip_ok and track in ("personal_ip", "mixed"):
                for rel in (tr.get("personal_ip_ecosystem") or {}).get("must_read_extra") or []:
                    pth = ROOT / rel
                    if pth.is_file():
                        paths.append(str(pth.relative_to(ROOT)))

    bad = any("但未出现" in e for e in errs)
    if track == "general":
        ok = not bad
    elif track == "personal_ip":
        ok = ip_ok
    elif track == "product":
        ok = prod is not None and not bad
    elif track == "mixed":
        ok = prod is not None and ip_ok and not bad
    else:
        ok = False

    payload = {
        "goal": goal,
        "track": track,
        "product_id": prod["id"] if prod else None,
        "product_names": prod.get("canonical_names") if prod else [],
        "ip_track_id": ip_cfg.get("track_id") if ip_ok else None,
        "must_read": list(dict.fromkeys(paths))[:24],
        "copy_v_tier_standard": "owner_copy_v_tier_400k",
        "copy_workflow_doc": "docs/OWNER-DUAL-TRACK-COPY-WORKFLOW.md",
        "owner_copy_review_required": True,
        "errors": errs,
        "pass": ok,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    OUT.write_text(text, encoding="utf-8")
    OUT_OWNER.write_text(text, encoding="utf-8")
    print(text)
    if not ok:
        print("NEEDS_WORK: owner context unresolved — read owner-context-resolved-latest.json", file=sys.stderr)
        return 42
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
