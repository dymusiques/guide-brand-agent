#!/usr/bin/env python3
"""Evaluator metric: Levenshtein edit distance vs reference (gold) + optional corrected text."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


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


def main() -> int:
    p = argparse.ArgumentParser(description="Edit distance vs gold reference")
    p.add_argument("--candidate", type=Path, required=True, help="current version e.g. versions/v0.md")
    p.add_argument("--reference", type=Path, required=True, help="standard answer e.g. reference/gold.md")
    p.add_argument("--corrected", type=Path, help="evaluator corrected text for this round")
    p.add_argument("--label", required=True, help="version label e.g. v0, v1")
    p.add_argument("--append", type=Path, help="metrics.jsonl to append")
    p.add_argument("--json", action="store_true", help="print one JSON line to stdout")
    args = p.parse_args()

    cand = normalize_text(args.candidate.read_text(encoding="utf-8"))
    ref = normalize_text(args.reference.read_text(encoding="utf-8"))
    corr_text = normalize_text(args.corrected.read_text(encoding="utf-8")) if args.corrected else None

    d_cand_ref = levenshtein(cand, ref)
    d_corr_ref = levenshtein(corr_text, ref) if corr_text is not None else None
    d_cand_corr = levenshtein(cand, corr_text) if corr_text is not None else None

    denom = max(len(ref), 1)
    row = {
        "at": datetime.now(timezone.utc).isoformat(),
        "label": args.label,
        "candidate": str(args.candidate),
        "reference": str(args.reference),
        "corrected": str(args.corrected) if args.corrected else None,
        "dist_candidate_ref": d_cand_ref,
        "dist_corrected_ref": d_corr_ref,
        "dist_candidate_corrected": d_cand_corr,
        "norm_dist_candidate_ref": round(d_cand_ref / denom, 6),
        "norm_dist_corrected_ref": round(d_corr_ref / denom, 6) if d_corr_ref is not None else None,
    }

    if args.json or not args.append:
        print(json.dumps(row, ensure_ascii=False))

    if args.append:
        args.append.parent.mkdir(parents=True, exist_ok=True)
        with args.append.open("a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
