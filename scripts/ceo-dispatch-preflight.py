#!/usr/bin/env python3
"""派活 / CEO 满链前 · deep 锁与 recover 预检（Owner 不必记 ls /tmp/…）。

见 docs/CEO-DISPATCH-PREFLIGHT.md
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
INBOX = ROOT / "content/evolution/00-manager/ceo-inbox"
HANDOFF = ROOT / "integration/handoff/ceo-dispatch-preflight-latest.json"
DEEP_LOCK = Path(os.environ.get("CEO_DEEP_LOCK", "/tmp/ceo-deep-delivery.lock"))
CAMPAIGN_LOCK = Path("/tmp/ceo-ip-all-agents-campaign.lock")
PASS_DEEP = "RESULT: PASS ceo-deep-delivery"


def _utc_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _read_lock_pid() -> int | None:
    if not DEEP_LOCK.is_file():
        return None
    raw = DEEP_LOCK.read_text(encoding="utf-8", errors="replace").strip()
    if not raw or not re.fullmatch(r"\d+", raw):
        return None
    return int(raw)


def _pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def _pgrep_deep_roots() -> list[int]:
    r = subprocess.run(
        ["pgrep", "-f", r"run-ceo-deep-delivery-cycle\.sh"],
        capture_output=True,
        text=True,
    )
    pids = []
    for line in (r.stdout or "").splitlines():
        line = line.strip()
        if line.isdigit():
            pids.append(int(line))
    # drop children whose parent is also a deep root
    roots: list[int] = []
    for pid in sorted(set(pids)):
        ppid_r = subprocess.run(
            ["ps", "-o", "ppid=", "-p", str(pid)],
            capture_output=True,
            text=True,
        )
        ppid_s = (ppid_r.stdout or "").strip()
        if ppid_s.isdigit():
            ppid = int(ppid_s)
            ppid_cmd = subprocess.run(
                ["ps", "-o", "command=", "-p", str(ppid)],
                capture_output=True,
                text=True,
            )
            if "run-ceo-deep-delivery-cycle" in (ppid_cmd.stdout or ""):
                continue
        roots.append(pid)
    return roots


def _remove_stale_lock() -> dict | None:
    pid = _read_lock_pid()
    if pid is None:
        return None
    if _pid_alive(pid):
        return None
    DEEP_LOCK.unlink(missing_ok=True)
    return {"action": "removed_stale_lock", "pid": pid}


def deep_delivery_active() -> tuple[bool, dict]:
    detail: dict = {"lock_path": str(DEEP_LOCK), "lock_pid": None, "lock_pid_alive": False}
    stale = _remove_stale_lock()
    if stale:
        detail["stale_lock_removed"] = stale
    if DEEP_LOCK.is_file():
        pid = _read_lock_pid()
        detail["lock_pid"] = pid
        if pid is not None and _pid_alive(pid):
            detail["lock_pid_alive"] = True
            return True, detail
        DEEP_LOCK.unlink(missing_ok=True)
    roots = _pgrep_deep_roots()
    detail["deep_pgrep_roots"] = roots
    if roots:
        detail["active_reason"] = "pgrep run-ceo-deep-delivery-cycle"
        return True, detail
    return False, detail


def _latest_log(glob_pat: str) -> Path | None:
    files = sorted(INBOX.glob(glob_pat), key=lambda p: p.stat().st_mtime, reverse=True)
    return files[0] if files else None


def _deep_log_status(log: Path | None) -> dict:
    if log is None or not log.is_file():
        return {"path": None, "closed_pass": False, "fatal_tail": False}
    text = log.read_text(encoding="utf-8", errors="replace")
    tail = "\n".join(text.splitlines()[-120:])
    fatal = bool(
        re.search(r"syntax error|RESULT: FAIL ceo-deep-delivery", tail)
    )
    closed = PASS_DEEP in text
    return {
        "path": str(log.relative_to(ROOT)),
        "closed_pass": closed,
        "fatal_tail": fatal and not closed,
    }


def _campaign_lock_alive() -> dict:
    if not CAMPAIGN_LOCK.is_file():
        return {"path": str(CAMPAIGN_LOCK), "present": False}
    pid = _read_lock_pid_from(CAMPAIGN_LOCK)
    alive = pid is not None and _pid_alive(pid)
    return {"path": str(CAMPAIGN_LOCK), "present": True, "pid": pid, "pid_alive": alive}


def _read_lock_pid_from(path: Path) -> int | None:
    if not path.is_file():
        return None
    raw = path.read_text(encoding="utf-8", errors="replace").strip()
    if raw.isdigit():
        return int(raw)
    return None


def build_report(*, wait_max_sec: int | None = None) -> dict:
    active, deep_detail = deep_delivery_active()
    deep_log = _deep_log_status(_latest_log("ceo-deep-delivery-*.log"))
    camp_log = _latest_log("ceo-ip-all-agents-campaign-*.log")
    camp = _campaign_lock_alive()
    roots = deep_detail.get("deep_pgrep_roots") or []
    wait_max = wait_max_sec if wait_max_sec is not None else int(
        os.environ.get("CEO_CAMPAIGN_WAIT_DEEP_SEC", "900")
    )

    recs: list[str] = []
    run_recover = False

    if deep_detail.get("stale_lock_removed"):
        recs.append("已清除僵尸 deep 锁；无需再手动 ls /tmp。")
    if len(roots) > 1:
        run_recover = True
        recs.append("检测到多个 deep 根进程 → 将跑 ceo-auto-recover-blocked（勿叠派活）。")
    elif active:
        recs.append(
            f"deep 仍在跑：满链会先等至多 {wait_max}s（CEO_CAMPAIGN_WAIT_DEEP_SEC），"
            "期间不要再发第二条「派活给 CEO」。"
        )
    elif deep_log.get("fatal_tail"):
        run_recover = True
        recs.append("最近 deep 日志含 FAIL/语法错误 → 建议 recover 后再派活。")
    elif not deep_log.get("closed_pass") and not active and deep_log.get("path"):
        recs.append("最近 deep 日志未 PASS 且当前无进程：可 recover 或检查是否中断。")
        if not roots:
            run_recover = True
    else:
        recs.append("deep 未占用 · 可正常「派活给 CEO」。")

    if camp.get("present") and camp.get("pid_alive"):
        recs.append("campaign 锁仍有效 · 勿并行第二条全员 campaign。")

    return {
        "schema": "ceo_dispatch_preflight_v1",
        "ts": _utc_iso(),
        "deep_delivery_active": active,
        "deep": deep_detail,
        "deep_log": deep_log,
        "campaign_lock": camp,
        "campaign_log": str(camp_log.relative_to(ROOT)) if camp_log else None,
        "CEO_CAMPAIGN_WAIT_DEEP_SEC": wait_max,
        "recommendations_zh": recs,
        "should_run_recover": run_recover,
        "owner_note": "满链前 Agent 自动跑本预检；Owner 无需记 ls /tmp/ceo-deep-delivery.lock。",
    }


def run_recover_script() -> tuple[int, str]:
    r = subprocess.run(
        ["bash", "scripts/ceo-auto-recover-blocked.sh"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=600,
    )
    out = ((r.stdout or "") + (r.stderr or "")).strip()
    return r.returncode, out[-3000:]


def preflight_for_full_stack(
    *,
    auto_recover: bool = True,
    write_handoff: bool = True,
) -> dict:
    """满链 gate / run_ceo_full 入口：清僵尸锁；风险时 recover；写 handoff。"""
    report = build_report()
    recover_ec = None
    recover_tail = ""
    if auto_recover and report.get("should_run_recover"):
        recover_ec, recover_tail = run_recover_script()
        report["recover"] = {
            "ran": True,
            "exit_code": recover_ec,
            "tail": recover_tail,
        }
        active_after, deep_after = deep_delivery_active()
        report["deep_delivery_active_after_recover"] = active_after
        report["deep_after_recover"] = deep_after
    else:
        report["recover"] = {"ran": False}

    if write_handoff:
        HANDOFF.parent.mkdir(parents=True, exist_ok=True)
        HANDOFF.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


def main() -> int:
    ap = argparse.ArgumentParser(description="CEO 派活前 deep 锁 / recover 预检")
    ap.add_argument("--json", action="store_true", help="打印 JSON 到 stdout")
    ap.add_argument(
        "--for-full-stack",
        action="store_true",
        help="满链模式：写 handoff + 按需 recover（与 gate 相同）",
    )
    ap.add_argument("--recover", action="store_true", help="无条件跑 ceo-auto-recover-blocked.sh")
    ap.add_argument(
        "--no-auto-recover",
        action="store_true",
        help="仅诊断 / 清僵尸锁，不自动 recover",
    )
    args = ap.parse_args()

    if args.for_full_stack:
        report = preflight_for_full_stack(auto_recover=not args.no_auto_recover)
    else:
        report = build_report()
        if args.recover:
            ec, tail = run_recover_script()
            report["recover"] = {"ran": True, "exit_code": ec, "tail": tail}
        else:
            report["recover"] = {"ran": False}
        HANDOFF.parent.mkdir(parents=True, exist_ok=True)
        HANDOFF.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if args.json or not args.for_full_stack:
        print(json.dumps(report, ensure_ascii=False, indent=2))

    if not args.json and args.for_full_stack:
        for line in report.get("recommendations_zh") or []:
            print(f"· {line}")
        if report.get("recover", {}).get("ran"):
            print(f"recover exit={report['recover'].get('exit_code')}")
        print(f"handoff: {HANDOFF.relative_to(ROOT)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())