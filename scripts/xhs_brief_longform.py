"""Extract Owner longform body from XHS brief or linked draft."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DRAFT_LINK = re.compile(r"长稿见[：:]\s*`([^`]+)`")


def extract_longform_text(brief: Path) -> str:
    if not brief.is_file():
        return ""
    text = brief.read_text(encoding="utf-8")
    link = DRAFT_LINK.search(text)
    if link:
        p = ROOT / link.group(1).strip()
        if p.is_file():
            return p.read_text(encoding="utf-8").strip()
    m = re.search(r"^## 正文（长稿[^\n]*\n([\s\S]*?)(?=\n## |\Z)", text, re.M)
    if m:
        body = m.group(1).strip()
        if body and not body.startswith("（") and not body.startswith("长稿见"):
            return body
    return ""


def count_cjk_chars(s: str) -> int:
    """Count CJK unified + fullwidth punctuation (rough 汉字量)."""
    return len(re.findall(r"[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]", s))
