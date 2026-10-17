#!/usr/bin/env python3
"""Gemini classifier for business-brand & marketing strategic docs (not XHS notes)."""

from __future__ import annotations

import inspect
import re
import sys
import time
from pathlib import Path
from typing import Any, Literal

STRATEGIC_ROOT = Path(__file__).resolve().parent.parent
XHS_ROOT = STRATEGIC_ROOT.parent / "xiaohongshu"
if str(XHS_ROOT) not in sys.path:
    sys.path.insert(0, str(XHS_ROOT))

from google import genai
from google.genai import types

from config.gemini_config import get_api_key, get_model

DocKind = Literal["business_brand", "marketing"]
MAX_BODY_CHARS = 12_000
_GEMINI_RETRIES = 3
_GEMINI_RETRY_SLEEP_S = 1.5


def normalize_strategic_content(content: Any) -> dict[str, str]:
    if not isinstance(content, dict):
        raise TypeError("content must be a dict")
    kind = content.get("kind") or content.get("doc_kind")
    if kind not in ("business_brand", "marketing"):
        raise ValueError("kind must be business_brand or marketing")
    subject = str(content.get("subject") or "").strip()
    body = str(content.get("body") or "").strip()
    return {"kind": kind, "subject": subject, "body": body}


def _parse_yes_no(text: str) -> bool:
    t = (text or "").strip().lower()
    if t.startswith("yes"):
        return True
    if t.startswith("no"):
        return False
    raise ValueError(f"Expected yes/no, got: {text!r}")


def _build_prompt(note: dict[str, str]) -> str:
    docstring = inspect.getdoc(is_strategic_doc_aligned) or ""
    rules = docstring.split("Classification rules", 1)[-1].split("Args:", 1)[0]
    kind_label = "商业品牌策划文档" if note["kind"] == "business_brand" else "营销 Campaign Brief"
    return (
        f"You classify {kind_label} for Owner IP alignment.\n\n"
        f"Rules:{rules}\n\n"
        f"Subject/title:\n{note['subject']}\n\n"
        f"Document body:\n{note['body'][:MAX_BODY_CHARS]}\n\n"
        "Answer with exactly one word: yes or no."
    )


def _call_gemini(prompt: str) -> bool:
    client = genai.Client(api_key=get_api_key())
    model = get_model()
    last_err: Exception | None = None
    for attempt in range(_GEMINI_RETRIES):
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config=types.GenerateContentConfig(temperature=0),
            )
            return _parse_yes_no(response.text or "")
        except Exception as exc:
            last_err = exc
            if attempt < _GEMINI_RETRIES - 1:
                time.sleep(_GEMINI_RETRY_SLEEP_S)
    assert last_err is not None
    raise last_err


def is_strategic_doc_aligned(content: dict) -> bool:
    """
    Classify business-brand or marketing strategic documents.

    Input: ``{"kind": "business_brand"|"marketing", "subject": str, "body": str}``.
    Returns ``False`` without Gemini when both subject and body are empty.

    Classification rules (answer **yes** when ALL hold):

    - **IP fit:** French-school flute lineage × cross-disciplinary brand strategy;
      art, education, AI innovation, digital collectibles (数字藏品). No NFT/Web3 hype.
    - **G-NOT-SINGLE-VERTICAL-LOCK:** Owner is **open** to any industry/product
      collaboration. **No** when the doc frames Owner as primarily a **single-vertical
      account** (e.g. 主攻家居/母婴/美妆). **Yes** when a specific industry appears
      only as a **case study** or one campaign, with general cross-brand capability.
    - **Strong link:** Document includes actionable CTA path (consultation,
      collaboration, DM keyword, meeting next step) — not vanity-only messaging.
    - **Doc-type fit:** For ``business_brand``, positioning/SWOT-level strategy;
      for ``marketing``, campaign audience, channels, CTA — not empty template fluff.

    Answer **no** when:

    - Generic filler with no IP, no CTA, or wrong-audience positioning.
    - Single-vertical lock-in as account identity.
    - Subject/body conflict: judge primarily by **body**.

    Args:
        content: dict with kind, subject, body.

    Returns:
        bool aligned.
    """
    note = normalize_strategic_content(content)
    if not note["subject"] and not note["body"]:
        return False
    prompt = _build_prompt(note)
    return _call_gemini(prompt)


def evaluate_strategic_doc(content: dict) -> dict[str, Any]:
    note = normalize_strategic_content(content)
    aligned = is_strategic_doc_aligned(note)
    return {
        "aligned": aligned,
        "kind": note["kind"],
        "subject": note["subject"],
        "classifier": "strategic_docs/line2/is_strategic_doc_aligned",
    }
