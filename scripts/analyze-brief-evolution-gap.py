#!/usr/bin/env python3
"""Analyze Brief vs baseline verify, gold, adversarial fusion — write EVOLUTION-GAP-latest.md."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from xhs_brief_longform import count_cjk_chars, extract_longform_text  # noqa: E402
from xhs_clever_advocate import analyze_clever_advocate  # noqa: E402

MARKER = "<!-- xhs-classifier -->"
LONGFORM_MIN = int(__import__("os").environ.get("CEO_LONGFORM_MIN_CHARS", "3000"))
LONGFORM_MAX = int(__import__("os").environ.get("CEO_LONGFORM_MAX_CHARS", "7200"))
RESEARCH = ROOT / "content/xiaohongshu/research"
EVO = ROOT / "content/evolution/04-xhs-topic-manager"
LOGS = ROOT / "content/xiaohongshu/verify-logs"
CHALLENGE = ROOT / "content/xiaohongshu/challenge"

def levenshtein(a: str, b: str) -> int:
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        curr = [i]
        for j, cb in enumerate(b, 1):
            ins = curr[j - 1] + 1
            delete = prev[j] + 1
            sub = prev[j - 1] + (0 if ca == cb else 1)
            curr.append(min(ins, delete, sub))
        prev = curr
    return prev[-1]


def normalize_text(s: str) -> str:
    return " ".join(s.split())


def slug_from_brief(brief: Path) -> str:
    return brief.name.replace("-brief.md", "")


def evolution_dir(slug: str) -> Path:
    return EVO / slug


def latest_verify_log(slug: str) -> Path | None:
    candidates = sorted(LOGS.glob(f"{slug}-complete-*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    return candidates[0] if candidates else None


def extract_body(brief: Path) -> str:
    text = brief.read_text(encoding="utf-8")
    if MARKER not in text:
        return normalize_text(text)
    after = text.split(MARKER, 1)[1]
    m = re.search(r"```(?:json)?\s*\n([\s\S]*?)\n```", after)
    if not m:
        return ""
    data = json.loads(m.group(1).strip())
    sub = str(data.get("subject") or "")
    body = str(data.get("body") or "")
    return normalize_text(sub + "\n" + body)


def fusion_warnings(challenge_path: Path) -> list[str]:
    if not challenge_path.is_file():
        return ["（缺 challenge 文件）"]
    text = challenge_path.read_text(encoding="utf-8")
    warns = []
    for line in text.splitlines():
        if "⚠️" in line and line.strip().startswith("|"):
            warns.append(line.strip())
    return warns


def verify_pass(report: dict) -> bool:
    if report.get("overall_pass") is True:
        return True
    ge = report.get("gemini_evaluate") or {}
    if ge.get("aligned") is False:
        return False
    l1 = report.get("l1_six_on_this_brief") or []
    if l1 and any(not x.get("pass") for x in l1):
        return False
    adv = report.get("adversarial_challenge") or {}
    if adv.get("pass") is False:
        return False
    rt = report.get("redteam_pre") or {}
    if rt.get("pass") is False:
        return False
    return bool(ge.get("aligned"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--brief", type=Path, required=True)
    p.add_argument("--gold-norm-max", type=float, default=float(__import__("os").environ.get("CEO_GOLD_NORM_MAX", "0.45")))
    args = p.parse_args()
    brief = args.brief if args.brief.is_absolute() else ROOT / args.brief
    if not brief.is_file():
        print(f"FAIL: brief not found: {brief}", file=sys.stderr)
        return 2

    slug = slug_from_brief(brief)
    evo = evolution_dir(slug)
    evo.mkdir(parents=True, exist_ok=True)
    out = evo / "EVOLUTION-GAP-latest.md"

    pitfalls = RESEARCH / f"{slug}-pitfalls.md"
    gold_body = evo / "reference/gold-body.md"
    gold = gold_body if gold_body.is_file() else evo / "reference/gold.md"
    challenge = CHALLENGE / f"{slug}-challenge.md"
    vlog = latest_verify_log(slug)

    report: dict = {}
    if vlog and vlog.is_file():
        report = json.loads(vlog.read_text(encoding="utf-8"))

    body = extract_body(brief)
    norm_dist = None
    if gold.is_file():
        ref = normalize_text(gold.read_text(encoding="utf-8"))
        d = levenshtein(body, ref)
        norm_dist = round(d / max(len(body), len(ref), 1), 6)

    fusion_warn = fusion_warnings(challenge)
    gate_ok = verify_pass(report) if report else False
    pitfalls_ok = pitfalls.is_file()
    fusion_ok = len(fusion_warn) == 0
    gold_ok = norm_dist is None or norm_dist <= args.gold_norm_max

    longform = extract_longform_text(brief)
    lf_n = count_cjk_chars(longform) if longform else 0
    longform_ok = LONGFORM_MIN <= lf_n <= LONGFORM_MAX if longform else False
    clever = analyze_clever_advocate(longform or "")
    clever_ok = clever["pass"] if longform else False

    ready = gate_ok and fusion_ok and pitfalls_ok and gold_ok and longform_ok and clever_ok
    status = "READY" if ready else "NEEDS_WORK"

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    md = f"""# EVOLUTION-GAP · {slug} · {now}

**状态：** `{status}`

## 闭环检查（Owner Mandate §2）

| 项 | 结果 |
|----|------|
| verify gate | {'✅' if gate_ok else '❌'} {vlog.name if vlog else '（无 verify-log）'} |
| fusion 无 ⚠️ | {'✅' if fusion_ok else '❌'} |
| pitfalls 文件 | {'✅' if pitfalls_ok else '❌'} `{pitfalls.relative_to(ROOT) if pitfalls_ok else pitfalls.name}` |
| gold 距离 | {'✅' if gold_ok else '❌'} norm_dist={norm_dist if norm_dist is not None else 'n/a'} (max {args.gold_norm_max}) |
| 长稿 {LONGFORM_MIN}–{LONGFORM_MAX} 字 | {'✅' if longform_ok else '❌'} chars={lf_n} |
| Clever 反方席 ≥{clever['min_personas']} | {'✅' if clever_ok else '❌'} personas={clever['persona_count']} |

## fusion ⚠️ 待加强

{chr(10).join(fusion_warn) if fusion_warn else '（无）'}

## 距 gold（有 reference 时）

- path: `{gold.relative_to(ROOT) if gold.is_file() else '（无 gold）'}`
- norm_dist_candidate_ref: **{norm_dist if norm_dist is not None else 'n/a'}**

## Analyze · Agent Must 填写下轮

- 变好：
- 变差：
- 距终极目标还差：
- 下一轮只改（1–3 条）：

## 命令

```bash
bash scripts/manager-ceo-gate-one-round.sh --brief {brief.relative_to(ROOT)}
python scripts/analyze-brief-evolution-gap.py --brief {brief.relative_to(ROOT)}
```
"""
    out.write_text(md, encoding="utf-8")
    print(f"WROTE {out.relative_to(ROOT)}")
    print(f"STATUS: {status}")
    return 0 if ready else 42


if __name__ == "__main__":
    raise SystemExit(main())
