"""L1 schema for per-Brief adversarial challenge markdown (Must sections)."""

from __future__ import annotations

import re
from pathlib import Path

REQUIRED_HEADINGS = (
    "## 外部 · 类似命题 / 大 V 压力",
    "## 其它 IP 产出 · 对打句",
    "## FULL-DRILL · 多 GM 攻击",
    "## 与 ip-positioning 融合",
    "## L2–L3 隐蔽风险",
    "## 驳/改 · 必做项",
)


def validate_challenge_markdown(text: str) -> tuple[bool, list[str]]:
    errs: list[str] = []
    for h in REQUIRED_HEADINGS:
        if h not in text:
            errs.append(f"missing section: {h}")
    if len(text.strip()) < 400:
        errs.append("challenge too short (<400 chars)")
    if not re.search(r"攻击|对打|风险", text):
        errs.append("no adversarial keywords")
    return (len(errs) == 0, errs)


def validate_challenge_file(path: Path) -> tuple[bool, list[str]]:
    if not path.is_file():
        return False, [f"missing file: {path}"]
    return validate_challenge_markdown(path.read_text(encoding="utf-8"))
