#!/usr/bin/env python3
"""Manager integration layer — 6 cases (glue only, no new classifier rules).

Calls existing scripts/functions; does not embed full IP target prose in tests.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
IMPORTANT = ROOT / "integration/IMPORTANT.md"
IP_BRIEF = ROOT / "content/personal-ip/ip-positioning-brief-2026-10-05.md"
EVAL_SCRIPT = ROOT / "scripts/evaluate-xhs-topic.py"
CONTENT_XHS = ROOT / "content/xiaohongshu"
KERNEL_TEST = ROOT / "kernels/xiaohongshu/line2/tests/test_is_xhs_growth_aligned.py"


def _py() -> str:
    venv = ROOT / ".venv/bin/python"
    return str(venv) if venv.is_file() else sys.executable


def case_1_important_file() -> tuple[bool, str]:
    if not IMPORTANT.is_file():
        return False, "missing integration/IMPORTANT.md"
    text = IMPORTANT.read_text(encoding="utf-8")
    for needle in ("跨行业", "强链接", "verify-xhs-topic"):
        if needle not in text:
            return False, f"IMPORTANT.md missing {needle!r}"
    return True, "IMPORTANT markers ok"


def case_2_ip_brief_scope() -> tuple[bool, str]:
    if not IP_BRIEF.is_file():
        return False, "missing IP brief"
    text = IP_BRIEF.read_text(encoding="utf-8")
    if "品牌合作范围" not in text or "不是家居号" not in text:
        return False, "IP brief missing 品牌合作范围 / 不是家居号"
    return True, "IP brief scope ok"


def case_3_evaluate_empty_via_api() -> tuple[bool, str]:
    """Calls existing stack: empty subject+body -> False without needing Brief file."""
    sys.path.insert(0, str(ROOT / "kernels/xiaohongshu"))
    from line2.is_xhs_growth_aligned import is_xhs_growth_aligned

    if is_xhs_growth_aligned({"subject": "", "body": ""}) is not False:
        return False, "empty dict should be False"
    return True, "core empty input False"


def case_4_evaluate_script_missing_marker() -> tuple[bool, str]:
    tmp = ROOT / ".tmp-manager-test-brief.md"
    tmp.write_text("# no classifier\n", encoding="utf-8")
    try:
        proc = subprocess.run(
            [_py(), str(EVAL_SCRIPT), "--brief", str(tmp)],
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
        if proc.returncode != 2:
            return False, f"expected exit 2, got {proc.returncode}"
        return True, "evaluate exits 2 on bad brief"
    finally:
        tmp.unlink(missing_ok=True)


def case_5_content_dir_has_pipeline() -> tuple[bool, str]:
    pipe = CONTENT_XHS / "PIPELINE.md"
    if not pipe.is_file():
        return False, "missing PIPELINE.md under content/xiaohongshu"
    return True, "pipeline doc present"


def case_6_kernel_test_module_importable() -> tuple[bool, str]:
    if not KERNEL_TEST.is_file():
        return False, "kernel test file missing"
    return True, "kernel test path exists (run verify-xhs-topic for Gemini 6)"


CASES = [
    ("集成 — IMPORTANT 标记可读", case_1_important_file),
    ("集成 — IP Brief 品牌合作范围", case_2_ip_brief_scope),
    ("集成 — 调核心空输入", case_3_evaluate_empty_via_api),
    ("集成 — evaluate 缺 marker exit 2", case_4_evaluate_script_missing_marker),
    ("集成 — content 管线文档", case_5_content_dir_has_pipeline),
    ("集成 — kernel 6-test 路径", case_6_kernel_test_module_importable),
]


def main() -> int:
    passed = failed = 0
    for desc, fn in CASES:
        try:
            ok, detail = fn()
        except Exception as exc:
            ok, detail = False, str(exc)
        if ok:
            print(f"{desc}: Passed ({detail})")
            passed += 1
        else:
            print(f"{desc}: Failed — {detail}")
            failed += 1
    print(f"\n=== Summary ===")
    print(f"cases: {passed} passed, {failed} failed (of {len(CASES)})")
    if failed:
        print("RESULT: FAIL")
        return 1
    print("RESULT: PASS — manager integration 6 cases")
    return 0


if __name__ == "__main__":
    sys.exit(main())
