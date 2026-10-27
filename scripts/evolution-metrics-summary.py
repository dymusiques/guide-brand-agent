#!/usr/bin/env python3
"""Summarize metrics.jsonl: mean edit distance, per-label series."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("metrics", type=Path, help="path to metrics.jsonl")
    p.add_argument("--field", default="dist_corrected_ref", help="or dist_candidate_ref")
    args = p.parse_args()

    rows = []
    for line in args.metrics.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))

    vals = [r[args.field] for r in rows if r.get(args.field) is not None]
    cand_vals = [r["dist_candidate_ref"] for r in rows if r.get("dist_candidate_ref") is not None]

    out = {
        "count": len(rows),
        "field": args.field,
        "mean": sum(vals) / len(vals) if vals else None,
        "mean_dist_candidate_ref": sum(cand_vals) / len(cand_vals) if cand_vals else None,
        "labels": [r.get("label") for r in rows],
    }
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
