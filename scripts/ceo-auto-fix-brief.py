#!/usr/bin/env python3
"""Mechanical CEO reroute fixes after gate FAIL (no Owner). Writes CEO-REROUTE stub."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVO = ROOT / "content/evolution/04-xhs-topic-manager"


def slug_from_brief(brief: Path) -> str:
    return brief.name.replace("-brief.md", "")


def write_reroute(brief: Path, round_n: int, reasons: list[str]) -> None:
    slug = slug_from_brief(brief)
    dest = EVO / slug / "CEO-REROUTE.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    body = [
        f"# CEO-REROUTE · {slug} · round {round_n}",
        "",
        f"- at: {datetime.now().isoformat(timespec='seconds')}",
        f"- brief: `{brief.relative_to(ROOT)}`",
        "",
        "## FAIL 项（自动检测）",
        "",
    ]
    for r in reasons:
        body.append(f"- {r}")
    body += [
        "",
        "## Prompt Change 提案（GM/AI 必填 · 改稿前填写）",
        "",
        "- 改什么：（文件路径 + 段落）",
        "- 一句 diff：",
        "- 依据（FAIL / verify-logs）：",
        "- 预期哪条 gate 变绿：",
        "- 风险：",
        "",
        "## GM Must（无人值守下一轮）",
        "",
        "1. 完成上节 **提案** 再改 classifier JSON / 正文 / INTEGRATION-PROMPT",
        "2. `python scripts/ensure-redteam-pre.py --brief …`（若 redteam 缺）",
        "3. `python scripts/evaluate-xhs-brief-complete.py --brief …`",
        "4. PASS 后更新 Brief Verify log · **GM-REPORT 本轮分析结论**",
        "",
        "**Owner 不参与 verify。**",
    ]
    dest.write_text("\n".join(body), encoding="utf-8")
    print(f"WROTE {dest.relative_to(ROOT)}")

    report = dest.parent / "GM-REPORT.md"
    stamp = datetime.now().isoformat(timespec="seconds")
    line = f"- `{stamp}` · round {round_n} gate FAIL · **本轮分析结论（必填）：** （AI 填写：原因 + 下一轮改什么）"
    if report.is_file():
        text = report.read_text(encoding="utf-8")
        if "本轮分析结论" not in text:
            report.write_text(text.rstrip() + "\n\n## 本轮分析结论（PASS/FAIL 均写）\n\n" + line + "\n", encoding="utf-8")
        else:
            report.write_text(text.rstrip() + "\n" + line + "\n", encoding="utf-8")
    else:
        report.write_text(
            f"# GM-REPORT · 04 xhs topic · {slug}\n\n## 本轮分析结论（PASS/FAIL 均写）\n\n{line}\n",
            encoding="utf-8",
        )
    print(f"WROTE {report.relative_to(ROOT)}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--brief", type=Path, required=True)
    ap.add_argument("--round", type=int, default=1)
    ap.add_argument("--report-json", type=Path, help="evaluate-xhs-brief-complete output")
    args = ap.parse_args()
    brief = args.brief if args.brief.is_absolute() else ROOT / args.brief
    reasons: list[str] = []
    if args.report_json and args.report_json.is_file():
        rep = json.loads(args.report_json.read_text(encoding="utf-8"))
        if not rep.get("redteam_pre", {}).get("pass"):
            reasons.append("missing redteam-pre → run ensure-redteam-pre.py")
        ac = rep.get("adversarial_challenge") or {}
        if not ac.get("pass"):
            reasons.append("adversarial challenge missing/invalid → run run-xhs-brief-adversarial-challenge.py")
        for c in rep.get("l1_six_on_this_brief") or []:
            if not c.get("pass"):
                reasons.append(f"{c.get('id')}: {c.get('kernel_ref')}")
        ge = rep.get("gemini_evaluate") or {}
        if not ge.get("aligned"):
            reasons.append("Gemini evaluate not aligned — edit classifier body/subject")
        kr = rep.get("kernel_six_regression")
        if kr and not kr.get("pass"):
            reasons.append("kernel 6 regression failed — retry or check GEMINI_API_KEY/region")
    if not reasons:
        reasons.append("gate failed — inspect verify-logs JSON")
    # Always ensure redteam attempt
    import subprocess

    py = ROOT / ".venv/bin/python"
    subprocess.run([str(py), str(ROOT / "scripts/ensure-redteam-pre.py"), "--brief", str(brief.relative_to(ROOT))], cwd=ROOT)
    subprocess.run(
        [str(py), str(ROOT / "scripts/run-xhs-brief-adversarial-challenge.py"), "--brief", str(brief.relative_to(ROOT))],
        cwd=ROOT,
    )
    write_reroute(brief, args.round, reasons)
    return 0


if __name__ == "__main__":
    sys.exit(main())
