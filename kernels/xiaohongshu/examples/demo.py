#!/usr/bin/env python3
"""
Gemini API demo — classify one XHS note dict (subject + body).

Course equivalent: module3-2-2-gemini/examples/demo.py.
Run from Guide/0 root with .env configured:

  .venv/bin/python kernels/xiaohongshu/examples/demo.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

XHS_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(XHS_ROOT))

from line2.is_xhs_growth_aligned import evaluate_xhs_growth_content

SAMPLE = {
    "subject": "法派长笛老师：品牌怎么用艺术讲清故事",
    "body": (
        "我在巴黎高师跟过歌剧院首席体系，现在帮品牌和艺术家做跨界策划。"
        "如果你正在为高端活动找一位能讲「艺术×商业×数字藏品」的策划人，"
        "私信「合作」，我们可以聊沉浸式体验怎么落地。"
    ),
}

if __name__ == "__main__":
    result = evaluate_xhs_growth_content(SAMPLE)
    print(json.dumps(result, ensure_ascii=False, indent=2))
