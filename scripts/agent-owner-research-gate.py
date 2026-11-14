#!/usr/bin/env python3
"""
Owner 已发复盘 / 监督 / 补全 — 唯一硬门禁。

任一层 FAIL → exit 1 · handoff owner-research-gate-latest.json
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "integration/handoff/owner-research-gate-latest.json"
MONOREPO = Path.home() / "Desktop/未命名"
C2_LOG = ROOT / "tmp/research-gate-c2.log"
ARTISTS_HIT = ROOT / "content/evolution/00-manager/ceo-inbox/2026-11-03-artists-three"
VENV_PY = ROOT / ".venv/bin/python3"


def run(cmd: list[str], *, cwd: Path | None = None, timeout: int = 900) -> tuple[int, str]:
    r = subprocess.run(
        cmd,
        cwd=cwd or ROOT,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    out = ((r.stdout or "") + (r.stderr or "")).strip()
    return r.returncode, out[-4000:]


def layer(name: str, ec: int, tail: str, *, ok_ec: set[int] | None = None) -> dict:
    allowed = ok_ec or {0}
    st = "PASS" if ec in allowed else "FAIL"
    return {"name": name, "status": st, "exit_code": ec, "tail": tail}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--goal", required=True)
    ap.add_argument("--session", default="owner-research-gate")
    ap.add_argument("--skip-qc-task", action="store_true", help="仅 CI；交付 Must 跑 QC")
    args = ap.parse_args()
    goal = args.goal.strip()
    layers: list[dict] = []
    fail = 0
    C2_LOG.parent.mkdir(parents=True, exist_ok=True)
    log_lines: list[str] = []

    def track(name: str, ec: int, tail: str, *, ok_ec: set[int] | None = None) -> None:
        nonlocal fail
        L = layer(name, ec, tail, ok_ec=ok_ec)
        layers.append(L)
        log_lines.append(f"=== {name} exit={ec} {L['status']} ===\n{tail[-800:]}\n")
        if L["status"] == "FAIL":
            fail += 1

    ec, tail = run(
        [
            sys.executable,
            "scripts/screen-xhs-drive-corpus.py",
            "--goal",
            goal,
            "--refresh-catalog",
            "--limit",
            "12",
        ],
        timeout=600,
    )
    track("drive_catalog_screen", ec, tail, ok_ec={0})

    # base brainstorm (no deep recurse)
    ec, tail = run([sys.executable, "scripts/verify-xhs-analytics-freshness.py"], timeout=60)
    if ec != 0:
        ec2, tail2 = run([sys.executable, "scripts/agent-restore-notes-csv-from-snapshot.py"], timeout=60)
        layers.append(
            {
                "name": "xhs_csv_restore",
                "status": "PASS" if ec2 == 0 else "FAIL",
                "exit_code": ec2,
                "tail": tail2,
            }
        )
        if ec2 != 0:
            fail += 1
        ec, tail = run([sys.executable, "scripts/verify-xhs-analytics-freshness.py"], timeout=60)
    track("xhs_analytics", ec, tail)

    ec, tail = run(
        [sys.executable, "scripts/agent-brainstorm-preflight.py", "--goal", goal, "--no-deep"],
        timeout=600,
    )
    track("brainstorm_preflight", ec, tail)

    ec, tail = run([sys.executable, "scripts/agent-hydrate-drive-priority.py", "--limit", "8"], timeout=600)
    track("drive_hydrate_fulltext", ec, tail, ok_ec={0, 1})
    hp = ROOT / "integration/handoff/owner-drive-hydrate-latest.json"
    if hp.is_file():
        hd = json.loads(hp.read_text(encoding="utf-8"))
        screen = json.loads(
            (ROOT / "content/evolution/00-manager/ceo-inbox/xhs-drive-screen-latest.json").read_text(
                encoding="utf-8"
            )
        )
        tier_ok = {r["id"] for r in screen.get("selected") or [] if r.get("tier") == "direct_hit"}
        pdfs = [
            i
            for i in hd.get("items") or []
            if "pdf" in (i.get("mimeType") or "").lower() and i.get("id") in tier_ok
        ]
        bad_pdf = [
            p["name"]
            for p in pdfs
            if p.get("status") not in ("PARTIAL", "BLOCKED", "SKIP")
            and not p.get("supervision", {}).get("read_complete")
        ]
        if bad_pdf:
            track("drive_hydrate_pdf_mandatory", 1, f"direct_hit PDF 未全文: {bad_pdf}")
        elif pdfs:
            layers.append(
                {
                    "name": "drive_hydrate_pdf_mandatory",
                    "status": "PASS",
                    "exit_code": 0,
                    "tail": f"direct_hit PDFs ok: {[p['name'] for p in pdfs]}",
                }
            )

    ec, tail = run([sys.executable, "scripts/agent-read-ip-brief-gate.py"])
    track("ip_brief_full", ec, tail)
    ec, tail = run([sys.executable, "scripts/agent-benchmark-cross-dimensions.py"])
    track("benchmark_cross_dim", ec, tail)

    ec, tail = run(["bash", "scripts/ceo-six-case-battery.sh"], timeout=900)
    core = ec == 0 or (
        "PASS six-case · fused-04" in tail
        and "PASS six-case · fused-05" in tail
        and "all 6 cases passed" in tail
    )
    layers.append(
        {
            "name": "ceo_six_case_battery",
            "status": "PASS" if ec == 0 else ("PARTIAL" if core else "FAIL"),
            "exit_code": ec,
            "tail": tail,
        }
    )
    if not core:
        fail += 1

    if MONOREPO.is_dir():
        ec, tail = run(
            ["python3", "scripts/agent-workflow.py", "read", "--step", "prompt-six-case", "--domain", "xhs"],
            cwd=MONOREPO,
        )
        track("prompt_six_case_xhs", ec, tail)

    ec, tail = run([sys.executable, "scripts/agent-pending-eval-baseline-snapshot.py"])
    track("pending_eval_baseline", ec, tail)

    py = str(VENV_PY if VENV_PY.is_file() else sys.executable)
    if ARTISTS_HIT.is_dir() and any(k in goal for k in ("艺术家", "不需要", "已发", "复盘")):
        ec, tail = run(
            [
                py,
                "scripts/evolve-platform-hits.py",
                "--dir",
                str(ARTISTS_HIT),
                "--goal",
                goal,
            ],
            timeout=600,
        )
        track("platform_evolution_artists_three", ec, tail, ok_ec={0, 42})
        ec4, tail4 = run([sys.executable, "scripts/verify-four-dimension-bar.py"], timeout=120)
        layers.append(
            {
                "name": "four_dimension_bar",
                "status": "PASS" if ec4 == 0 else "NEEDS_WORK",
                "exit_code": ec4,
                "tail": tail4,
                "note": "NEEDS_WORK 不阻断 gate；交付须写明未过 80 线",
            }
        )
    else:
        layers.append({"name": "platform_evolution_artists_three", "status": "SKIP", "note": "无艺术家语境"})

    ec, tail = run(
        [
            sys.executable,
            "scripts/run_ceo_full_execution.py",
            "--goal",
            goal,
            "--skip-triple-eval",
            "--skip-stress",
        ],
        timeout=1200,
    )
    layers.append(
        {
            "name": "ceo_manifest_slice",
            "status": "PASS" if ec == 0 else ("PARTIAL" if ec == 42 else "FAIL"),
            "exit_code": ec,
            "tail": tail,
        }
    )
    if ec not in (0, 42):
        fail += 1

    C2_LOG.write_text("\n".join(log_lines), encoding="utf-8")

    payload = {
        "schema": "agent_owner_research_gate_v1",
        "as_of": datetime.now(timezone.utc).isoformat(),
        "goal": goal,
        "layers": layers,
        "fail_count": fail,
        "status": "PASS" if fail == 0 else "FAIL",
        "root_cause_doc": "docs/AGENT-WHY-RESEARCH-GAPS.md",
        "contract": "integration/handoff/agent-owner-research-gate-contract.json",
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if MONOREPO.is_dir():
        ec, tail = run(
            [
                "python3",
                "scripts/agent-workflow.py",
                "qc",
                "handoff",
                "--slug",
                "brand-ceo",
                "--session",
                args.session,
                "--c2-log",
                str(C2_LOG),
            ],
            cwd=MONOREPO,
        )
        track("qc_handoff", ec, tail)
        payload["layers"] = layers
        payload["fail_count"] = fail
        payload["status"] = "PASS" if fail == 0 else "FAIL"
        OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        if not args.skip_qc_task:
            ec, tail = run(
                [
                    sys.executable,
                    "scripts/agent-qc-gate-report.py",
                    "--session",
                    args.session,
                    "--gate-json",
                    str(OUT),
                ],
            )
            track("qc_verify", ec, tail)
            payload["layers"] = layers
            payload["fail_count"] = fail
            payload["status"] = "PASS" if fail == 0 else "FAIL"
            OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        else:
            layers.append({"name": "qc_verify", "status": "SKIP", "note": "--skip-qc-task"})

    print(json.dumps({"status": payload["status"], "handoff": str(OUT.relative_to(ROOT)), "fail_count": fail}))
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
