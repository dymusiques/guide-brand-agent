#!/usr/bin/env python3
"""CEO full execution: GM six-case → triple eval → double stress → autopilot → manifest → HTML.

See docs/CEO-FULL-EXECUTION-MANDATE.md · docs/CEO-SIX-CASE-GM-TO-CEO-WORKFLOW.md
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from ceo_agent_roster import build_roster, parallelism_summary  # noqa: E402


def run(cmd: list[str], *, step: str, env: dict[str, str], allow_fail: bool = False) -> int:
    print(f"\n>>> {step}\n>>> {' '.join(cmd)}", flush=True)
    r = subprocess.run(cmd, cwd=ROOT, env=env)
    if r.returncode != 0 and not allow_fail:
        print(f"FAIL: {step} exit={r.returncode}", file=sys.stderr)
    return r.returncode


def ensure_gm_report(brief: Path, *, overall: str) -> None:
    slug = brief.name.replace("-brief.md", "")
    evo = ROOT / "content/evolution/04-xhs-topic-manager" / slug
    evo.mkdir(parents=True, exist_ok=True)
    report = evo / "GM-REPORT.md"
    if report.is_file():
        return
    report.write_text(
        f"""# GM-REPORT · 04 xhs-topic-manager · {slug}

- 汇报给：00 CEO
- 日期：{datetime.now(timezone.utc).strftime("%Y-%m-%d")}
- 任务：Owner 指定 Brief · CEO full execution

## 六项 6-case 基准

- 见 `CEO-RUN-MANIFEST-latest.json`

## 部门管理

- verify / evaluate：{overall}
- 请求 CEO：已提交 manifest + Owner HTML

## 本轮分析结论

- （Agent 若改稿后补：变好/变差/距 gold）
""",
        encoding="utf-8",
    )


def finalize_manifest(manifest: dict, invoked_ids: set[str], result_by_id: dict[str, str]) -> None:
    manifest["roster"] = build_roster(invoked_ids, result_overrides=result_by_id)
    manifest["parallelism"] = parallelism_summary(manifest["roster"])


def write_manifest(manifest: dict, invoked_ids: set[str], result_by_id: dict[str, str]) -> None:
    finalize_manifest(manifest, invoked_ids, result_by_id)
    env = os.environ.copy()
    env["CEO_RUN_MANIFEST_JSON"] = json.dumps(manifest, ensure_ascii=False)
    subprocess.run([sys.executable, "scripts/ceo_write_run_manifest.py"], cwd=ROOT, env=env, check=False)


def main() -> int:
    p = argparse.ArgumentParser(description="CEO full execution pipeline")
    p.add_argument("--goal", default="", help="Owner goal for Open WebUI router")
    p.add_argument("--brief", action="append", default=[], help="XHS brief path(s)")
    p.add_argument("--no-discovery-auto", action="store_true")
    p.add_argument("--skip-integration", action="store_true", help="(legacy) skip not used if six-case runs")
    p.add_argument("--skip-six-case", action="store_true")
    p.add_argument("--skip-triple-eval", action="store_true")
    p.add_argument("--skip-stress", action="store_true")
    p.add_argument("--skip-matrix", action="store_true", help="six-case includes fused; skip redundant")
    p.add_argument("--round2", action="store_true")
    args = p.parse_args()

    env = os.environ.copy()
    brief = args.brief[-1] if args.brief else ""
    if brief:
        env["CEO_OWNER_EXTRA_BRIEF"] = brief
        env.setdefault("CEO_OWNER_HTML_HASH", "#owner-latest")
        env["CEO_SIX_CASE_BRIEF"] = brief

    manifest: dict = {
        "overall": "FAIL",
        "goal": args.goal.strip(),
        "brief": brief,
        "agents": [],
        "steps": [],
        "eval_rounds": [],
    }
    invoked_ids: set[str] = {"00"}
    result_by_id: dict[str, str] = {}

    def record_step(
        name: str,
        ec: int,
        *,
        agent: str = "00 CEO",
        cap: str = "",
        roster_ids: list[str] | None = None,
    ) -> None:
        manifest["steps"].append(f"{name} → exit {ec}")
        res = "PASS" if ec == 0 else f"FAIL({ec})"
        if cap:
            manifest["agents"].append({"agent": agent, "capability": cap, "result": res})
        for rid in roster_ids or ["00"]:
            invoked_ids.add(rid)
            if ec == 0:
                result_by_id[rid] = "PASS"
            elif rid not in result_by_id or result_by_id[rid] == "PASS":
                result_by_id[rid] = res

    fail = 0

    ec = run(["bash", "scripts/ceo-auto-recover-blocked.sh"], step="CEO recover", env=env, allow_fail=True)
    record_step("ceo-auto-recover-blocked", ec, cap="进程自愈", roster_ids=["00"])
    if ec != 0:
        fail += 1

    if args.goal.strip():
        ec = run(
            ["bash", "scripts/run-openwebui-router-pipeline.sh", "--goal", args.goal.strip()],
            step="Open WebUI CEO router",
            env=env,
            allow_fail=True,
        )
        record_step("openwebui-router", ec, cap="目标路由", roster_ids=["00"])
        if ec != 0:
            fail += 1

    if not args.skip_six_case:
        cmd = ["bash", "scripts/ceo-six-case-battery.sh"]
        if brief:
            cmd.append(brief)
        ec = run(cmd, step="六项 6-case battery (integration + 01/04/05 fused + L1/kernel)", env=env)
        record_step(
            "ceo-six-case-battery",
            ec,
            agent="01/04/05/08",
            cap="六项 6-case verify",
            roster_ids=["01", "04", "05", "08"],
        )
        if ec != 0:
            fail += 1
    else:
        ec = run([sys.executable, "scripts/evaluate_personal_ip.py", "--check"], step="01 personal-ip shell", env=env)
        record_step("evaluate_personal_ip", ec, agent="01", cap="IP 函数壳", roster_ids=["01"])
        if ec != 0:
            fail += 1

    if brief and not args.skip_triple_eval:
        ec = run(
            ["bash", "scripts/ceo-triple-eval-baseline-loop.sh", "--brief", brief],
            step="三重 evaluate + baseline/gold 距离",
            env=env,
        )
        record_step(
            "ceo-triple-eval-baseline-loop",
            ec,
            agent="04",
            cap="triple eval ×3 + gap + metrics",
            roster_ids=["04", "05"],
        )
        if ec == 42:
            manifest["overall"] = "NEEDS_WORK"
            write_manifest(manifest, invoked_ids, result_by_id)
            print("NEEDS_WORK: triple eval — Agent must edit brief per EVOLUTION-GAP", file=sys.stderr)
            return 42
        if ec != 0:
            fail += 1

    if brief and not args.skip_stress:
        stress_cmd = ["bash", "scripts/ceo-double-stress.sh", "--brief", brief]
        if not args.round2 and "-test-brief" not in brief:
            stress_cmd.append("--skip-round2")
        ec = run(stress_cmd, step="双重压测 (adversarial ×2 + round2 if test brief)", env=env, allow_fail=True)
        record_step("ceo-double-stress", ec, agent="04", cap="stress ×2", roster_ids=["04"])
        if "-test-brief" in brief or args.round2:
            invoked_ids.update({"01", "02", "03", "06", "07", "09", "10", "11", "12"})
            result_by_id.setdefault("01", "PASS")
        if ec != 0:
            fail += 1

    if brief:
        ensure_gm_report(ROOT / brief if not brief.startswith("/") else Path(brief), overall="pending")

    ap_cmd = [sys.executable, "scripts/run_ceo_xhs_autopilot.py"]
    if args.no_discovery_auto:
        ap_cmd.append("--no-discovery-auto")
    if args.round2:
        ap_cmd.append("--round2")
    for b in args.brief:
        ap_cmd.extend(["--brief", b])
    if not args.brief:
        ap_cmd = [sys.executable, "scripts/run_ceo_xhs_autopilot.py", "--skip-evolution"]

    ec = run(ap_cmd, step="run_ceo_xhs_autopilot (evolution + HTML + verify + open)", env=env)
    record_step("run_ceo_xhs_autopilot", ec, cap="CEO XHS autopilot + HTML", roster_ids=["00", "04"])
    if ec == 42:
        manifest["overall"] = "NEEDS_WORK"
        write_manifest(manifest, invoked_ids, result_by_id)
        return 42
    if ec != 0:
        fail += 1

    if brief:
        bp = ROOT / brief if not Path(brief).is_absolute() else Path(brief)
        ensure_gm_report(bp, overall="PASS" if fail == 0 else "PARTIAL")

    manifest["overall"] = "PASS" if fail == 0 else "PARTIAL_FAIL"
    write_manifest(manifest, invoked_ids, result_by_id)

    if fail:
        print("RESULT: FAIL run_ceo_full_execution (partial)", file=sys.stderr)
        return 1
    print("RESULT: PASS run_ceo_full_execution")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
