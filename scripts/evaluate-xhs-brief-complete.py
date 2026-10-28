#!/usr/bin/env python3
"""One-shot Brief gate: redteam-pre + 6 L1 rubric cases on THIS brief + Gemini evaluate.

Usage:
  .venv/bin/python scripts/evaluate-xhs-brief-complete.py --brief content/xiaohongshu/foo-brief.md
  .venv/bin/python scripts/evaluate-xhs-brief-complete.py --all-discovery

Writes JSON log under content/xiaohongshu/verify-logs/
Exit 0 only if all steps PASS (including aligned: true).
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "kernels/xiaohongshu"))
from challenge_brief_schema import validate_challenge_file  # noqa: E402
REDTEAM = ROOT / "content/xiaohongshu/redteam"
LOG_DIR = ROOT / "content/xiaohongshu/verify-logs"
EVAL = ROOT / "scripts/evaluate-xhs-topic.py"
MARKER = "<!-- xhs-classifier -->"


def slug_from_brief(path: Path) -> str:
    name = path.name.replace("-brief.md", "")
    # redteam file: 2026-10-17-discovery-01-irreplaceability-pre.md
    if name.startswith("2026-"):
        return name
    return name


def redteam_pre_path(brief: Path) -> Path:
    base = brief.name.replace("-brief.md", "")
    return REDTEAM / f"{base}-pre.md"


def extract_classifier(brief: Path) -> dict[str, str]:
    text = brief.read_text(encoding="utf-8")
    if MARKER not in text:
        raise ValueError(f"missing {MARKER}")
    after = text.split(MARKER, 1)[1]
    m = re.search(r"```(?:json)?\s*\n([\s\S]*?)\n```", after)
    if not m:
        raise ValueError("no classifier json")
    data = json.loads(m.group(1).strip())
    return {"subject": str(data.get("subject") or ""), "body": str(data.get("body") or "")}


def run_l1_six(note: dict[str, str]) -> list[dict]:
    sub, body = note["subject"], note["body"]
    combined = sub + "\n" + body

    def has(*words: str) -> bool:
        return any(w in combined for w in words)

    cases: list[dict] = []

    # 1 — 正例 IP + 强链接 CTA（对标 kernel case 1）
    c1 = has("品牌", "艺术", "跨界", "法派", "长笛", "IP", "策划") and has(
        "私信", "聊聊", "收藏", "合作", "评估"
    )
    cases.append(
        {
            "id": "L1-1",
            "kernel_ref": "正例 — IP + 人群 + 强链接 CTA",
            "pass": c1,
            "detail": "subject/body 须含 IP/品牌命题 + 强链接 CTA 词",
        }
    )

    # 2 — 正例 专业 + 咨询链路（对标 kernel case 2）
    c2 = has("法派", "专业", "训练", "体系", "句读", "信任", "判断") and has(
        "私信", "聊聊", "收藏", "合作", "评估"
    )
    cases.append(
        {
            "id": "L1-2",
            "kernel_ref": "正例 — 专业+教育/咨询链接",
            "pass": c2,
            "detail": "专业信任信号 + CTA",
        }
    )

    # 3 — 负例：不应像无关帖（对标 kernel case 3）
    c3 = not (
        has("聚餐", "RSVP", "办公室") and not has("品牌", "艺术", "跨界")
    )
    cases.append(
        {
            "id": "L1-3",
            "kernel_ref": "负例 — 与 IP/涨粉/筛客无关",
            "pass": c3,
            "detail": "不得主导为团建/无关话题",
        }
    )

    # 4 — 标题偏泛但正文须相关（对标 kernel case 4 精神）
    title_generic = sub.strip() in ("今天天气真好", "") or len(sub) < 4
    body_on_ip = has("品牌", "艺术", "跨界", "长笛", "法派", "合作", "叙事")
    c4 = body_on_ip if title_generic else True
    cases.append(
        {
            "id": "L1-4",
            "kernel_ref": "歧义 — 标题弱时正文须承载 IP",
            "pass": c4,
            "detail": f"title_generic={title_generic}, body_on_ip={body_on_ip}",
        }
    )

    # 5 — 标题蹭 IP 正文空洞（对标 kernel case 5）
    title_ip = has("法派", "长笛", "品牌", "艺术", "AI", "数字藏品")
    body_shallow = len(body) < 80 or (
        has("滤镜", "vlog", "抽奖", "贴纸") and not has("品牌", "跨界", "合作", "聊聊")
    )
    c5 = not (title_ip and body_shallow and not has("私信", "合作", "聊聊", "收藏"))
    cases.append(
        {
            "id": "L1-5",
            "kernel_ref": "歧义 — 标题相关、正文须有链接价值",
            "pass": c5,
            "detail": "防标题党+空正文",
        }
    )

    # 6 — 边界 非空（对标 kernel case 6）
    c6 = len(sub.strip()) >= 4 and len(body.strip()) >= 40
    cases.append(
        {
            "id": "L1-6",
            "kernel_ref": "边界 — 空白/过短内容",
            "pass": c6,
            "detail": f"subject_len={len(sub.strip())}, body_len={len(body.strip())}",
        }
    )

    return cases


def run_gemini_evaluate(brief: Path, py: str) -> dict:
    proc = subprocess.run(
        [py, str(EVAL), "--brief", str(brief.relative_to(ROOT))],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    out = proc.stdout.strip() or proc.stderr.strip()
    try:
        data = json.loads(out)
    except json.JSONDecodeError:
        data = {"error": out, "aligned": False}
    data["_exit"] = proc.returncode
    return data


def run_kernel_six(py: str) -> dict:
    proc = subprocess.run(
        ["bash", str(ROOT / "scripts/verify-xhs-topic.sh")],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    return {
        "pass": proc.returncode == 0,
        "exit": proc.returncode,
        "tail": (proc.stdout + proc.stderr)[-2000:],
        "note": "分类器内核 6 固定用例回归（整仓健康；与 L1-1..6 互补）",
    }


def process_brief(brief: Path, py: str, skip_kernel: bool, ensure_redteam: bool) -> dict:
    if ensure_redteam:
        subprocess.run(
            [py, str(ROOT / "scripts/ensure-redteam-pre.py"), "--brief", str(brief.relative_to(ROOT))],
            cwd=ROOT,
            check=False,
        )
    rt = redteam_pre_path(brief)
    note = extract_classifier(brief)
    ch_path = ROOT / "content/xiaohongshu/challenge" / f"{brief.name.replace('-brief.md', '')}-challenge.md"
    ch_ok, ch_errs = validate_challenge_file(ch_path)
    report = {
        "brief": str(brief.relative_to(ROOT)),
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "adversarial_challenge": {
            "path": str(ch_path.relative_to(ROOT)) if ch_path.is_file() else None,
            "pass": ch_ok,
            "errors": ch_errs,
        },
        "redteam_pre": {
            "path": str(rt.relative_to(ROOT)) if rt.is_file() else None,
            "pass": rt.is_file() and rt.stat().st_size > 50,
        },
        "l1_six_on_this_brief": run_l1_six(note),
        "gemini_evaluate": None,
        "kernel_six_regression": None,
    }
    report["gemini_evaluate"] = run_gemini_evaluate(brief, py)
    if not skip_kernel:
        report["kernel_six_regression"] = run_kernel_six(py)

    l1_ok = all(c["pass"] for c in report["l1_six_on_this_brief"])
    gem_ok = report["gemini_evaluate"].get("aligned") is True and report["gemini_evaluate"].get("_exit") == 0
    rt_ok = report["redteam_pre"]["pass"]
    ch_ok = report["adversarial_challenge"]["pass"]
    kern_ok = skip_kernel or (report["kernel_six_regression"] or {}).get("pass", False)
    report["overall_pass"] = l1_ok and gem_ok and rt_ok and ch_ok and kern_ok
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--brief", type=Path, action="append", default=[])
    parser.add_argument("--all-discovery", action="store_true")
    parser.add_argument("--skip-kernel-six", action="store_true", help="Skip verify-xhs-topic.sh (faster)")
    parser.add_argument("--no-ensure-redteam", action="store_true")
    args = parser.parse_args()

    py = str(ROOT / ".venv/bin/python") if (ROOT / ".venv/bin/python").is_file() else sys.executable
    briefs: list[Path] = []
    if args.all_discovery:
        briefs = sorted((ROOT / "content/xiaohongshu").glob("*discovery*-brief.md"))
    for b in args.brief:
        briefs.append(b if b.is_absolute() else ROOT / b)
    if not briefs:
        parser.error("pass --brief or --all-discovery")

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    all_pass = True
    for brief in briefs:
        if not brief.is_file():
            print(f"FAIL missing {brief}", file=sys.stderr)
            all_pass = False
            continue
        try:
            rep = process_brief(brief, py, args.skip_kernel_six, not args.no_ensure_redteam)
        except Exception as exc:
            print(f"FAIL {brief.name}: {exc}", file=sys.stderr)
            all_pass = False
            continue
        slug = brief.name.replace("-brief.md", "")
        log_path = LOG_DIR / f"{slug}-complete-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        log_path.write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
        status = "PASS" if rep["overall_pass"] else "FAIL"
        print(f"\n=== {status} · {brief.name} ===")
        print(f"  redteam-pre: {'PASS' if rep['redteam_pre']['pass'] else 'FAIL'}")
        print(f"  adversarial-challenge: {'PASS' if rep['adversarial_challenge']['pass'] else 'FAIL'}")
        for c in rep["l1_six_on_this_brief"]:
            print(f"  {c['id']}: {'PASS' if c['pass'] else 'FAIL'} · {c['kernel_ref']}")
        ge = rep["gemini_evaluate"]
        print(f"  Gemini evaluate: {'PASS aligned' if ge.get('aligned') else 'FAIL'} exit={ge.get('_exit')}")
        if rep.get("kernel_six_regression"):
            k = rep["kernel_six_regression"]
            print(f"  kernel 6 regression: {'PASS' if k['pass'] else 'FAIL'}")
        print(f"  log: {log_path.relative_to(ROOT)}")
        if not rep["overall_pass"]:
            all_pass = False

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
