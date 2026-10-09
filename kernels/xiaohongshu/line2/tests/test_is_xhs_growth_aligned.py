#!/usr/bin/env python3
"""Step 3: six test cases for is_xhs_growth_aligned (Module 3 pattern).

Imports the real implementation module only — not learning2/docstring_shell.py.
"""

from __future__ import annotations

import sys
from pathlib import Path

# line2/is_xhs_growth_aligned.py (sibling of tests/)
_LINE2_DIR = Path(__file__).resolve().parent.parent
if str(_LINE2_DIR) not in sys.path:
    sys.path.insert(0, str(_LINE2_DIR))

from is_xhs_growth_aligned import is_xhs_growth_aligned  # noqa: E402

TEST_CASES = [
    {
        "description": "正例 — 明确提到：IP + 人群 + 强链接 CTA",
        "input": {
            "subject": "法派长笛老师：品牌怎么用艺术讲清故事",
            "body": (
                "我在巴黎高师跟过歌剧院首席体系，现在帮品牌和艺术家做跨界策划。"
                "如果你正在为高端活动找一位能讲「艺术×商业×数字藏品」的策划人，"
                "私信「合作」，我们可以聊沉浸式体验怎么落地。"
            ),
        },
        "expected": True,
    },
    {
        "description": "正例 — 隐含提到：未写数字藏品，但专业+教育+咨询链接清晰",
        "input": {
            "subject": "孩子学长笛，家长最该先看这一件事",
            "body": (
                "别急着比进度。法派体系里，呼吸和音乐句读比「练哪本教材」更重要。"
                "我带的学生里，有几位已经走向国际院校方向。"
                "想聊孩子适不适合走专业路径，可以私信「评估」。"
            ),
        },
        "expected": True,
    },
    {
        "description": "负例 — 无关：与 IP、涨粉、筛客无关",
        "input": {
            "subject": "周末办公室聚餐去哪吃",
            "body": (
                "本周六团队聚餐，大家投票选餐厅。"
                "记得周四前 RSVP，地点在商场 B1，停车券我会发到群里。"
            ),
        },
        "expected": False,
    },
    {
        "description": "歧义 — 标题无关、内容相关：应看正文 Pass",
        "input": {
            "subject": "今天天气真好",
            "body": (
                "分享一个最近常被品牌方问到的问题："
                "为什么「艺术体验」比硬广更能让高净值用户停留？"
                "我从一次品牌×长笛×摄影的跨界项目里总结了三条可复用方法。"
                "面向各行业品牌升级与沉浸式体验需求，欢迎私信关键词案例领取结构清单。"
            ),
        },
        "expected": True,
    },
    {
        "description": "歧义 — 标题相关、内容无关：标题蹭 IP，正文无链接价值",
        "input": {
            "subject": "法派长笛 × AI 创新 × 数字藏品",
            "body": (
                "今天随手拍了几张练琴房照片，滤镜调了半小时，大家觉得哪张好看？"
                "点赞最多的下次发 vlog，评论区抽三位送贴纸。"
            ),
        },
        "expected": False,
    },
    {
        "description": "边界 — 空白内容",
        "input": {
            "subject": "",
            "body": "",
        },
        "expected": False,
    },
]


def test_is_xhs_growth_aligned() -> int:
    passed = failed = 0
    for test in TEST_CASES:
        try:
            result = is_xhs_growth_aligned(test["input"])
        except Exception as exc:
            print(f"{test['description']}: Failed — {exc}")
            failed += 1
            continue
        ok = result == test["expected"]
        status = "Passed" if ok else "Failed"
        print(f"{test['description']}: {status}")
        if ok:
            passed += 1
        else:
            failed += 1
            print(f"  expected={test['expected']!r}, got={result!r}")

    total = passed + failed
    print(f"\n=== Summary ===")
    print(f"cases: {passed} passed, {failed} failed (of {total})")
    if failed:
        print("RESULT: FAIL")
        return 1
    print("RESULT: PASS — all 6 cases passed")
    return 0


if __name__ == "__main__":
    sys.exit(test_is_xhs_growth_aligned())
