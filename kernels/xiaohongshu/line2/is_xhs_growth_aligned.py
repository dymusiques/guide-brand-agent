#!/usr/bin/env python3
"""Xiaohongshu note classifier — IP, follower growth, strong-link audience fit."""

from __future__ import annotations

import inspect
import re
import sys
import time
from pathlib import Path
from typing import Any

XHS_ROOT = Path(__file__).resolve().parent.parent
if str(XHS_ROOT) not in sys.path:
    sys.path.insert(0, str(XHS_ROOT))

from google import genai
from google.genai import types

from config.gemini_config import get_api_key, get_model

MAX_BODY_CHARS = 10_000
_GEMINI_RETRIES = 3
_GEMINI_RETRY_SLEEP_S = 1.5


def normalize_xhs_content(content: Any) -> dict[str, str]:
    """
    Normalize caller payload to ``{"subject": str, "body": str}``.

    All pipeline inputs/outputs for this kernel use this shape.
    """
    if not isinstance(content, dict):
        content = {}
    subject = content.get("subject") or ""
    body = content.get("body") or ""
    if not isinstance(subject, str):
        subject = str(subject)
    if not isinstance(body, str):
        body = str(body)
    return {"subject": subject, "body": body}


def _parse_yes_no(raw: str | None) -> str:
    if not raw or not str(raw).strip():
        raise ValueError("Gemini response is empty")
    text = str(raw).strip().lower()
    first = text.splitlines()[0].strip().rstrip(".")
    if first in ("yes", "no"):
        return first
    if first.startswith("yes"):
        return "yes"
    if first.startswith("no"):
        return "no"
    match = re.search(r"\b(yes|no)\b", text)
    if match:
        return match.group(1)
    raise ValueError(f"Gemini response is not 'yes' or 'no': {raw!r}")


def _classification_rules_text() -> str:
    """Rules sent to Gemini — sourced from this function's docstring."""
    return (inspect.getdoc(is_xhs_growth_aligned) or "").strip()


def _build_gemini_prompt(subject: str, body: str) -> str:
    rules = _classification_rules_text()
    return (
        f"{rules}\n\n"
        "---\n"
        "Task: Apply the rules above to classify the note between NOTE_START and NOTE_END.\n"
        "Do NOT continue, translate, or summarize the note.\n"
        "Reply with exactly one word on the first line: yes or no.\n"
        "No punctuation, no explanation, no other lines.\n\n"
        "NOTE_START\n"
        f"Subject (title): {subject}\n"
        f"Body: {body}\n"
        "NOTE_END\n\n"
        "Classification (yes or no only):"
    )


def _call_gemini_yes_no(prompt: str) -> str:
    """Call Gemini like examples/demo.py — single generate_content, parse yes/no."""
    client = genai.Client(api_key=get_api_key())
    last_err: Exception | None = None
    for attempt in range(_GEMINI_RETRIES):
        response = client.models.generate_content(
            model=get_model(),
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0,
                max_output_tokens=256,
                system_instruction=(
                    "You are a strict binary classifier. "
                    "Output only yes or no on the first line. "
                    "Never quote or continue the user's note text."
                ),
            ),
        )
        try:
            return _parse_yes_no(response.text)
        except ValueError as exc:
            last_err = exc
            if attempt < _GEMINI_RETRIES - 1:
                time.sleep(_GEMINI_RETRY_SLEEP_S)
    assert last_err is not None
    raise last_err


def is_xhs_growth_aligned(content: dict) -> bool:
    """
    Classify whether a Xiaohongshu note aligns with IP, growth, and strong-link goals.

    Input must be a dict with ``subject`` (title) and ``body`` (hook + body + CTA).
    Use :func:`normalize_xhs_content` to coerce payloads. Returns ``False`` without
    calling Gemini when both ``subject`` and ``body`` are empty.

    Classification rules (answer **yes** when the note meets ALL of):

    - **Personal IP:** French-school flute lineage × cross-disciplinary brand strategy;
      classical art, AI innovation, digital collectibles (数字藏品). Do not require
      Web3 or NFT wording; those terms must not appear in drafts.
    - **Audience fit:** brands, artists, music-education (students/parents), or
      AI / digital-collectible innovators.
    - **Strong link potential:** consultation, collaboration, deep trust, or DM —
      not empty virality or giveaway-only engagement.
    - **Growth intent:** supports growing ~1700 followers toward 5000 then 10000
      with quality, IP-aligned followers.

    Answer **no** when:

    - Unrelated logistics or generic lifestyle with no IP/growth/link value.
    - Title suggests IP but body does not deliver professional or audience value.
    - Title and body conflict: judge primarily by **body** (Module 3 email pattern).
    - Content would attract the wrong audience or has no path to meaningful connection.

    Args:
        content: ``{"subject": str, "body": str}``

    Returns:
        bool: ``True`` if aligned (Gemini yes), ``False`` if not (Gemini no).

    Raises:
        ValueError: If Gemini's response is not ``yes`` or ``no`` after retries.
        RuntimeError: If API key is missing (see ``config/gemini_config.py``).
    """
    note = normalize_xhs_content(content)
    subject, body = note["subject"], note["body"]

    if subject == "" and body == "":
        return False

    body = body[:MAX_BODY_CHARS]
    prompt = _build_gemini_prompt(subject, body)
    answer = _call_gemini_yes_no(prompt)
    return answer == "yes"


def evaluate_xhs_growth_content(content: dict) -> dict[str, str | bool]:
    """
    Classify and return a dict payload (subject, body, aligned).

    All downstream Manager outputs should use this shape for traceability.
    """
    note = normalize_xhs_content(content)
    aligned = is_xhs_growth_aligned(note)
    return {"subject": note["subject"], "body": note["body"], "aligned": aligned}
