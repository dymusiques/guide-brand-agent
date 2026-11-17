#!/usr/bin/env python3
"""FAIL if deliverable pack missing 简报/架构/全文/说明 (XHS brief · oral · LI · Medium)."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANDATE = ROOT / "integration/handoff/owner-deliverable-pack-mandate.json"

MIN_ORAL_CJK = 280
MIN_XHS_LONG_CJK = 800  # below OWNER-LONGFORM target but blocks empty structure-only


def cjk_count(text: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", text))


def check_xhs_brief(path: Path) -> list[str]:
    errs: list[str] = []
    t = path.read_text(encoding="utf-8", errors="replace")
    if not re.search(r"##\s*(钩子|标题|正文)", t):
        errs.append("缺简报结构（钩子/标题/正文节）")
    if "为什么" not in t and "依据" not in t and "数据" not in t:
        errs.append("缺「为什么这样写」或数据依据")
    body = ""
    if "## 正文" in t:
        body = t.split("## 正文", 1)[-1]
    elif "longform" in t.lower():
        body = t
    else:
        body = t
    if cjk_count(body) < MIN_XHS_LONG_CJK:
        errs.append(f"完整文稿过短（CJK<{MIN_XHS_LONG_CJK}，需补长稿或 ## 正文（长稿）")
    return errs


def check_oral(path: Path) -> list[str]:
    errs: list[str] = []
    t = path.read_text(encoding="utf-8", errors="replace")
    if "## 口播全文" not in t:
        errs.append("缺 ## 口播全文")
    if "## 元数据" not in t:
        errs.append("缺 ## 元数据（简报）")
    oral = t.split("## 口播全文", 1)[-1].split("##", 1)[0]
    if cjk_count(oral) < MIN_ORAL_CJK:
        errs.append(f"口播全文过短（CJK<{MIN_ORAL_CJK}）")
    if "分镜" not in t and "架构" not in t and "结构" not in t:
        errs.append("建议含分镜/架构说明节")
    return errs


def check_li_medium(path: Path) -> list[str]:
    errs: list[str] = []
    t = path.read_text(encoding="utf-8", errors="replace")
    for need in ("简报", "架构", "完整文稿", "为什么"):
        if need not in t:
            errs.append(f"缺「{need}」节")
    sect = t.split("## 3", 1)[-1] if "## 3" in t else t
    if cjk_count(sect) < 400:
        errs.append("完整文稿节过短")
    return errs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--brief", type=Path, default=None)
    ap.add_argument("--oral", type=Path, default=None)
    ap.add_argument("--linkedin", type=Path, default=None)
    ap.add_argument("--medium", type=Path, default=None)
    args = ap.parse_args()
    path = args.brief or args.oral or args.linkedin or args.medium
    if not path:
        print("FAIL need --brief|--oral|--linkedin|--medium", file=sys.stderr)
        return 2
    if not path.is_absolute():
        path = ROOT / path
    if not path.is_file():
        print(f"FAIL missing {path}", file=sys.stderr)
        return 2
    if args.brief:
        errs = check_xhs_brief(path)
    elif args.oral:
        errs = check_oral(path)
    else:
        errs = check_li_medium(path)
    if errs:
        print("FAIL deliverable-pack:\n- " + "\n- ".join(errs), file=sys.stderr)
        return 1
    print(f"PASS deliverable-pack {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())