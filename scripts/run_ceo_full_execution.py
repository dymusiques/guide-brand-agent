#!/usr/bin/env python3
"""Cursor CEO main chain: Drive screen → fusion → recover → optional OWUI router → evaluate → HTML.

Open WebUI is optional step -1 only (allow_fail); not the pipeline host.
See docs/CEO-FULL-EXECUTION-MANDATE.md · docs/CEO-SIX-CASE-GM-TO-CEO-WORKFLOW.md
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from ceo_agent_roster import build_roster, parallelism_summary  # noqa: E402
from ceo_goal_tracks import is_flutebuddy_goal, is_ip_ecosystem_goal  # noqa: E402


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


def goal_wants_xhs_filter_html(goal: str, brief: str) -> bool:
    if brief:
        return True
    g = goal.strip()
    if not g:
        return False
    keys = (
        "Brief",
        "brief",
        "小红书",
        "Discovery",
        "笔记",
        "长稿",
        "xhs",
        "口播",
        "FILTER",
        "筛选",
    )
    return any(k in g for k in keys)


def open_platform_three_html(hit_dir: Path, *, env: dict[str, str]) -> None:
    """Owner Must 看见三平台 HTML；与 evolve / Gate 是否 PASS 无关。"""
    names = ("linkedin.html", "xiaohongshu.html", "medium.html")
    if not all((hit_dir / name).is_file() for name in names):
        return
    run(
        ["bash", "scripts/open-owner-platform-three-html.sh", str(hit_dir)],
        step="Open Owner platform HTML (LinkedIn → 小红书 → Medium)",
        env=env,
        allow_fail=True,
    )


def main() -> int:
    p = argparse.ArgumentParser(description="CEO full execution pipeline")
    p.add_argument("--goal", default="", help="Owner goal (CEO main chain; also feeds optional Open WebUI router step -1)")
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
    elif args.goal.strip() and not goal_wants_xhs_filter_html(args.goal.strip(), ""):
        env["CEO_OWNER_HTML_REFRESH"] = "0"
        env["CEO_OWNER_HTML_OPEN"] = "0"
        goal_l = args.goal.strip().lower()
        inbox = ROOT / "content/evolution/00-manager/ceo-inbox"
        if is_ip_ecosystem_goal(args.goal.strip()):
            ip_html = inbox / f"OWNER-IP-ECOSYSTEM-DELIVERABLE-{datetime.now(timezone.utc).strftime('%Y-%m-%d')}.html"
            ip_strat = inbox / "2026-11-05-owner-ip-ecosystem-strategy.md"
            if ip_strat.is_file():
                env["CEO_OWNER_DELIVERABLE_PATH"] = str(ip_strat.relative_to(ROOT))
            elif ip_html.is_file():
                env["CEO_OWNER_DELIVERABLE_PATH"] = str(ip_html.relative_to(ROOT))
        elif is_flutebuddy_goal(args.goal.strip()):
            for p in sorted(inbox.glob("*flutebuddy*strategy*.md"), key=lambda x: x.stat().st_mtime, reverse=True):
                env["CEO_OWNER_DELIVERABLE_PATH"] = str(p.relative_to(ROOT))
                break

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

    screen_goal = args.goal.strip() or (Path(brief).stem if brief else "小红书个人IP文案")
    if screen_goal:
        ec_pf = run(
            [sys.executable, "scripts/ceo-preflight-product-context.py", "--goal", screen_goal],
            step="CEO product context preflight (owner-product-registry)",
            env=env,
            allow_fail=True,
        )
        record_step("ceo-preflight-product-context", ec_pf, cap="Owner 轨解析（产品/IP）", roster_ids=["00", "01"])
        if ec_pf == 42:
            manifest["overall"] = "NEEDS_WORK"
            manifest["product_preflight"] = "FAIL — read product-context-resolved-latest.json"
            write_manifest(manifest, invoked_ids, result_by_id)
            print("NEEDS_WORK: product preflight — fix goal/dispatch before screen or delivery", file=sys.stderr)
            return 42
        if ec_pf != 0:
            fail += 1
        if is_flutebuddy_goal(screen_goal) or is_ip_ecosystem_goal(screen_goal):
            ec_vt = run(
                ["bash", "scripts/verify-owner-copy-v-tier-mandate.sh"],
                step="V-Tier copy mandate (dual-track)",
                env=env,
                allow_fail=True,
            )
            record_step(
                "verify-owner-copy-v-tier-mandate",
                ec_vt,
                cap="40–50万粉文笔标准 · 文件验收",
                roster_ids=["00", "01", "04"],
            )
            if ec_vt != 0:
                fail += 1
    screen_cmd = [
        sys.executable,
        "scripts/ceo-task-drive-corpus-screen.py",
        "--auto",
        "--goal",
        screen_goal,
    ]
    if brief:
        screen_cmd.extend(["--brief", brief])
    ec = run(
        screen_cmd,
        step="XHS Drive corpus screen (all catalog filenames)",
        env=env,
    )
    record_step("screen-xhs-drive-corpus", ec, cap="Drive 全库筛选", roster_ids=["00"])
    if ec != 0:
        fail += 1

    env["CEO_GOAL"] = screen_goal
    if brief:
        env["CEO_SIX_CASE_BRIEF"] = brief
    fusion_cmd = [
        sys.executable,
        "scripts/build-drive-long-context-fusion.py",
        "--auto",
        "--phase",
        "ceo_dispatch",
    ]
    if brief:
        fusion_cmd.extend(["--brief", brief])
    if screen_goal:
        fusion_cmd.extend(["--goal", screen_goal])
    ec = run(
        fusion_cmd,
        step="Drive long-context fusion auto (ceo_dispatch)",
        env=env,
        allow_fail=True,
    )
    record_step(
        "build-drive-long-context-fusion",
        ec,
        cap="fusion JSON checklist + evidence path",
        roster_ids=["00"],
    )
    if ec != 0:
        fail += 1

    ec = run(["bash", "scripts/ceo-auto-recover-blocked.sh"], step="CEO recover", env=env, allow_fail=True)
    record_step("ceo-auto-recover-blocked", ec, cap="进程自愈", roster_ids=["00"])
    if ec != 0:
        fail += 1

    if args.goal.strip():
        ec = run(
            ["bash", "scripts/run-openwebui-router-pipeline.sh", "--goal", args.goal.strip()],
            step="Open WebUI CEO router (optional step -1)",
            env=env,
            allow_fail=True,
        )
        record_step("openwebui-router", ec, cap="目标路由", roster_ids=["00"])
        if ec != 0:
            fail += 1

        goal = args.goal.strip()
        if "不需要那么多艺术家" in goal:
            hit_dir = ROOT / "content/evolution/00-manager/ceo-inbox/2026-11-03-artists-three"
        else:
            slug = re.sub(r"[^\w\u4e00-\u9fff]+", "-", goal).strip("-")[:40] or "goal"
            hit_dir = ROOT / "content/evolution/00-manager/ceo-inbox/platform-hits" / slug
        writing = any(k in goal for k in ("写", "笔记", "口播", "成稿", "LinkedIn", "Medium", "艺术家", "爆款"))
        if writing:
            hit_dir.mkdir(parents=True, exist_ok=True)
            ec = run(
                [
                    sys.executable,
                    "scripts/evolve-platform-hits.py",
                    "--dir",
                    str(hit_dir),
                    "--goal",
                    goal,
                ],
                step="Platform hit evolution (Gemini API)",
                env=env,
                allow_fail=True,
            )
            record_step("evolve-platform-hits", ec, cap="换角度对抗 → 距离 → 爆款线", roster_ids=["00", "01", "04"])
            open_platform_three_html(hit_dir, env=env)
            manifest["platform_html_open"] = "linkedin→xiaohongshu→medium"
            if ec == 42:
                manifest["overall"] = "NEEDS_WORK"
                write_manifest(manifest, invoked_ids, result_by_id)
                print(
                    "NEEDS_WORK: angle distance or hit line still open. "
                    "Platform HTML still opened for Owner review. "
                    "Do not lower ANGLE_BAR. Same session must rewrite and rerun. "
                    "See docs/CEO-ADVERSARIAL-EVOLUTION-LOOP.md",
                    file=sys.stderr,
                )
                return 42
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
        print(
            "NOTE: no brief, so brief triple-eval/stress are skipped. "
            "That skip does not cancel evolve-platform-hits.py. "
            "See docs/CEO-ADVERSARIAL-EVOLUTION-LOOP.md",
            flush=True,
        )
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

    goal_s = args.goal.strip()
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if is_ip_ecosystem_goal(goal_s):
        ip_html = ROOT / "content/evolution/00-manager/ceo-inbox" / f"OWNER-IP-ECOSYSTEM-DELIVERABLE-{day}.html"
        ec_ip = run(
            [sys.executable, "scripts/build-owner-ip-ecosystem-deliverable-html.py"],
            step="Build Owner IP ecosystem HTML",
            env=env,
            allow_fail=True,
        )
        record_step("build-owner-ip-ecosystem-deliverable-html", ec_ip, cap="个人 IP 生态链 HTML", roster_ids=["00", "01"])
        if ip_html.is_file():
            env["CEO_OWNER_DELIVERABLE_PATH"] = str(ip_html.relative_to(ROOT))
        run(
            ["bash", "scripts/open-owner-ip-ecosystem-deliverable-html.sh"],
            step="Open Owner IP ecosystem HTML",
            env=env,
            allow_fail=True,
        )
    if is_flutebuddy_goal(goal_s):
        fb_html = ROOT / "content/evolution/00-manager/ceo-inbox" / f"OWNER-FLUTEBUDDY-DELIVERABLE-{day}.html"
        ec_fb = run(
            [sys.executable, "scripts/build-owner-flutebuddy-deliverable-html.py"],
            step="Build FluteBuddy Owner HTML",
            env=env,
            allow_fail=True,
        )
        record_step("build-owner-flutebuddy-deliverable-html", ec_fb, cap="FluteBuddy 可视化交付", roster_ids=["00"])
        if fb_html.is_file() and not is_ip_ecosystem_goal(goal_s):
            env["CEO_OWNER_DELIVERABLE_PATH"] = str(fb_html.relative_to(ROOT))
        run(
            ["bash", "scripts/open-owner-flutebuddy-deliverable-html.sh"],
            step="Open FluteBuddy Owner HTML",
            env=env,
            allow_fail=True,
        )

    manifest["overall"] = "PASS" if fail == 0 else "PARTIAL_FAIL"
    write_manifest(manifest, invoked_ids, result_by_id)

    if fail:
        print("RESULT: FAIL run_ceo_full_execution (partial)", file=sys.stderr)
        return 1
    print("RESULT: PASS run_ceo_full_execution")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
