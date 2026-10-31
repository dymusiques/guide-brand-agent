---
context_version: "2026-10-30-l012"
repo_path: "kernels/xiaohongshu/docs/03-six-test-cases.md"
goal: "六个必过测试用例说明"
openwebui_route: "rag_l2"
cursor_route: "read"
content_sha256: "4586c46dc0cea73b"
---

# 六个必过测试用例说明

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** **执行源（唯一真相）：** `line2/tests/test_is_xhs_growth_aligned.py`  
Test 仅 `from is_xhs_growth_aligned import is_xhs_growth_aligned`（真文件在 `line2/is_xhs_growth_aligned.py`），不引用 `learning2/
- **Path:** `kernels/xiaohongshu/docs/03-six-test-cases.md`
- **Open WebUI:** `rag_l2`
- **Cursor:** `read`

## 章节锚点
- **设计意图**: - **1–2：** 覆盖「显性」与「隐性」符合规则的笔记。
- **运行**: ```bash


---

## L2 正文

# 六个必过测试用例说明

**执行源（唯一真相）：** `line2/tests/test_is_xhs_growth_aligned.py`  
Test 仅 `from is_xhs_growth_aligned import is_xhs_growth_aligned`（真文件在 `line2/is_xhs_growth_aligned.py`），不引用 `learning2/docstring_shell.py`。  
本文便于人读；改用例时请 **只改 test 文件**，并同步更新本节。

| # | 类型 | 描述 | 期望 |
|---|------|------|------|
| 1 | 正例 | 明确 IP（法派长笛 × 品牌策划）+ 目标人群 + 私信「合作」类强链接 CTA | `True` |
| 2 | 正例 | 未写「数字藏品」，但教育专业度 + 私信「评估」清晰 | `True` |
| 3 | 负例 | 办公室聚餐 RSVP，与 IP/涨粉/筛客无关 | `False` |
| 4 | 歧义 | 标题无关（天气），正文品牌/跨界案例 + 私信「案例」→ **以正文为准** | `True` |
| 5 | 歧义 | 标题蹭 IP/数字藏品，正文仅晒图抽奖 → **无链接价值** | `False` |
| 6 | 边界 | `subject=""`, `body=""` | `False`（不调 Gemini） |

## 设计意图

- **1–2：** 覆盖「显性」与「隐性」符合规则的笔记。  
- **3：** 纯无关内容必须拒绝。  
- **4–5：** 对齐 Module 3 邮件课「标题/正文冲突时看正文」的模式。  
- **6：** 空输入安全默认 + 节省 API。

## 运行

```bash
bash scripts/verify-xhs-topic.sh
```

或：

```bash
.venv/bin/python kernels/xiaohongshu/line2/tests/test_is_xhs_growth_aligned.py
```