#!/usr/bin/env python3
"""Six Gemini cases — Agent 02 business-brand strategic docs."""

from __future__ import annotations

import sys
from pathlib import Path

_LINE2 = Path(__file__).resolve().parent.parent
if str(_LINE2) not in sys.path:
    sys.path.insert(0, str(_LINE2))

from is_strategic_doc_aligned import is_strategic_doc_aligned  # noqa: E402

KIND = "business_brand"

TEST_CASES = [
    {
        "description": "正例 — 跨行业定位 + SWOT + 强链接 CTA",
        "input": {
            "kind": KIND,
            "subject": "瀛想文化 · 艺术×品牌跨界定位",
            "body": (
                "## 定位\n法派长笛传承 × 跨界策划，服务各行业品牌升维。\n"
                "## SWOT\n优势：三语+歌剧院体系；机会：沉浸式体验需求。\n"
                "## 与 IP 对齐\n跨行业 open，不单品类绑定。\n"
                "CTA：品牌方私信「跨界」预约 30 分钟策略对话。"
            ),
        },
        "expected": True,
    },
    {
        "description": "正例 — 单场跨界案例（任意行业）不绑定人设",
        "input": {
            "kind": KIND,
            "subject": "跨界方法论 · 可复用到任意行业",
            "body": (
                "## 定位\n跨行业品牌艺术体验策划（法派长笛 × 商业场景）。\n"
                "## 与 IP 对齐\n不单品类绑定；以下为 **一场** 历史快闪的方法论拆解，"
                "同样适用于奢侈品、科技、消费品，而非转型为某垂直博主。\n"
                "## SWOT\n可复用沉浸体验结构。\n"
                "CTA：品牌方私信「跨界结构」预约咨询。"
            ),
        },
        "expected": True,
    },
    {
        "description": "负例 — 单品类绑定（家居主攻号）",
        "input": {
            "kind": KIND,
            "subject": "家居建材行业首席长笛家居博主",
            "body": (
                "主攻家居建材行业，持续为卖场、建材品牌做家居系列内容，"
                "粉丝主要是装修人群，不接其他行业。"
            ),
        },
        "expected": False,
    },
    {
        "description": "负例 — 无强链接 CTA",
        "input": {
            "kind": KIND,
            "subject": "品牌定位草稿",
            "body": (
                "## 定位\n我们很专业。\n## SWOT\n很好。\n"
                "欢迎随便看看，喜欢就点赞，不需要联系。"
            ),
        },
        "expected": False,
    },
    {
        "description": "负例 — 与 IP 无关",
        "input": {
            "kind": KIND,
            "subject": "办公室团建策划",
            "body": "周六聚餐投票选餐厅，记得 RSVP。",
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
    print("RESULT: PASS — business brand 6 cases")
    return 0


if __name__ == "__main__":
    sys.exit(main())
