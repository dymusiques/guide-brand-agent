#!/usr/bin/env python3
"""Six Gemini cases — Agent 03 marketing campaign docs."""

from __future__ import annotations

import sys
from pathlib import Path

_LINE2 = Path(__file__).resolve().parent.parent
if str(_LINE2) not in sys.path:
    sys.path.insert(0, str(_LINE2))

from is_strategic_doc_aligned import is_strategic_doc_aligned  # noqa: E402

KIND = "marketing"

TEST_CASES = [
    {
        "description": "正例 — Campaign + 渠道 + 强链接 CTA",
        "input": {
            "kind": KIND,
            "subject": "Q4 品牌艺术体验 Campaign",
            "body": (
                "## Campaign 名称\n艺术体验季\n## 目标受众\n跨行业品牌市场负责人\n"
                "## 渠道与节奏\n小红书深度 + IG Daily\n"
                "## CTA（强链接）\n私信「体验季」领取结构清单并预约通话\n"
                "## 与 IP Brief 关系\n不单品类绑定，案例可跨垂直。"
            ),
        },
        "expected": True,
    },
    {
        "description": "正例 — 单次行业活动、非系列绑定",
        "input": {
            "kind": KIND,
            "subject": "单场母婴品牌艺术工作坊",
            "body": (
                "一次性 workshop 合作，不将账号定位改为母婴主攻；"
                "活动后引流至跨界策划咨询。CTA：私信「工作坊复盘」。"
            ),
        },
        "expected": True,
    },
    {
        "description": "负例 — 母婴号系列化 Campaign",
        "input": {
            "kind": KIND,
            "subject": "母婴博主涨粉计划",
            "body": (
                "连续 12 期母婴种草，账号转型为母婴垂直，"
                "只接奶粉尿布品牌，不要其他行业。"
            ),
        },
        "expected": False,
    },
    {
        "description": "负例 — 只有曝光无 CTA",
        "input": {
            "kind": KIND,
            "subject": "曝光 Campaign",
            "body": "多发视频冲播放量，无需私信转化。",
        },
        "expected": False,
    },
    {
        "description": "负例 — 无关",
        "input": {
            "kind": KIND,
            "subject": "滤镜分享",
            "body": "今天滤镜好看吗？评论区抽奖贴纸。",
        },
        "expected": False,
    },
    {
        "description": "边界 — 空白",
        "input": {"kind": KIND, "subject": "", "body": ""},
        "expected": False,
    },
]


def main() -> int:
    passed = failed = 0
    for test in TEST_CASES:
        try:
            result = is_strategic_doc_aligned(test["input"])
        except Exception as exc:
            print(f"{test['description']}: Failed — {exc}")
            failed += 1
            continue
        ok = result == test["expected"]
        print(f"{test['description']}: {'Passed' if ok else 'Failed'}")
        if ok:
            passed += 1
        else:
            failed += 1
            print(f"  expected={test['expected']!r}, got={result!r}")
    print(f"\n=== Summary ===\ncases: {passed} passed, {failed} failed (of {len(TEST_CASES)})")
    if failed:
        print("RESULT: FAIL")
        return 1
    print("RESULT: PASS — marketing 6 cases")
    return 0


if __name__ == "__main__":
    sys.exit(main())
