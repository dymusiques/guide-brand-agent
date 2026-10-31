---
context_version: "2026-10-30-l012"
repo_path: "kernels/xiaohongshu/docs/01-workflow-step-order.md"
goal: "工作方式与步骤顺序审阅"
openwebui_route: "rag_l2"
cursor_route: "read"
content_sha256: "64bd7d241f0f0472"
---

# 工作方式与步骤顺序审阅

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** 本文把对话里约定的做法写成**可交接文档**，并回答：**每一步的方式对不对、顺序对不对。**
- **Path:** `kernels/xiaohongshu/docs/01-workflow-step-order.md`
- **Open WebUI:** `rag_l2`
- **Cursor:** `read`

## 章节锚点
- **结论（简短）**: **你的顺序和 Module 3 / Superlinear 课纲一致，可以沿用。** 唯一建议：在「核心函数能跑通」之后，立刻把说明写进 Git（本 `kernels/xiaohongshu/` 目…
- **推荐顺序 vs 你实际做的**: | 顺序 | 步骤 | 是否正确 | 说明 |
- **常见误区（你没有犯）**: - ❌ 在 test 文件里写 Gemini 调用 —— 你没有。
- **你刚补充的一步**: **完全正确，且应紧接在 verify 通过之后。** 代码已在 Git 工作区；本文档目录补全**流程审阅、API 说明、用例说明、README 索引**，以后新 Agent 只读文件即可接手。
- **当前这一步（test 卫生 · Module 3）**: | 动作 | 是否正确 |
- **仍未实现、但顺序正确的后续**: | 顺序 | 步骤 | 说明 |
- **建议的后续固定节奏（选题 Manager）**: 1. 在 `content/xiaohongshu/` 写 Brief（dict 或模板转 dict）。


---

## L2 正文

# 工作方式与步骤顺序审阅

本文把对话里约定的做法写成**可交接文档**，并回答：**每一步的方式对不对、顺序对不对。**

## 结论（简短）

**你的顺序和 Module 3 / Superlinear 课纲一致，可以沿用。** 唯一建议：在「核心函数能跑通」之后，立刻把说明写进 Git（本 `kernels/xiaohongshu/` 目录），避免只留在聊天里 —— 这正是你当前这一步要做的事。

## 推荐顺序 vs 你实际做的

| 顺序 | 步骤 | 是否正确 | 说明 |
|------|------|----------|------|
| 1 | 定成功标准与 **输出形状**（dict + `subject` / `body`） | ✅ | 先定形状再写逻辑，避免后面改接口；`normalize_xhs_content` / `evaluate_xhs_growth_content` 与此一致。 |
| 2 | 定 **分类规则**（IP、人群、强链接、涨粉意图） | ✅ | 规则进 **docstring**，与课纲「规则在 docstring、Gemini 只答 yes/no」一致。 |
| 3 | 写 **6 个 test case**（含歧义、边界） | ✅ | 应先于或紧接核心函数；test 只 import 核心函数，不内嵌 Gemini 逻辑 —— 已满足。 |
| 4 | 配置 **`.env` / API**（Key 不进 Git） | ✅ | Agent 在 Terminal 自验，不在聊天粘贴 Key；`gemini_config.py` + `.env.example` 正确。 |
| 5 | `learning2/docstring_shell.py` → **`line2` 实现** | ✅ | 课纲 Step 2 → Step 3 的标准路径。 |
| 6 | **`examples/demo.py`** 单条试跑 | ✅ | 与 `module3-2-2-gemini/examples/demo.py` 同角色。 |
| 7 | **`scripts/verify-xhs-topic.sh`** + **`check.md` 路由** | ✅ | 交付前一条命令 6/6；与 `verify-handoff` / `verify-integration` 并列、不混淆。 |
| 8 | **Skill / 内容管线**（Brief → verify → commit） | ⏳ 合理后置 | 应在 kernel **6/6 稳定**后再做；你现在的优先级对。 |
| 9 | **P 层业务 KPI**（粉丝 5000/10k） | ✅ 不进单测 | 与课纲一致：单元测试测分类器，不测运营数字。 |

## 常见误区（你没有犯）

- ❌ 在 test 文件里写 Gemini 调用 —— 你没有。
- ❌ 规则只写在聊天、docstring 空壳 —— 已实现 line2 且 prompt 读 docstring。
- ❌ 用 Web3/NFT 文案 —— 规则要求 **数字藏品**，与 `rules/USER.md` 一致。
- ❌ 把 Module 3 的 `is_genai_email` 6 test 混进本仓 —— `check.md` 已路由到课纲仓。

## 你刚补充的一步

> 「把所有 AI 生成实现的内容都保存成独立的文件，不要只留在聊天里。」

**完全正确，且应紧接在 verify 通过之后。** 代码已在 Git 工作区；本文档目录补全**流程审阅、API 说明、用例说明、README 索引**，以后新 Agent 只读文件即可接手。

## 当前这一步（test 卫生 · Module 3）

| 动作 | 是否正确 |
|------|----------|
| 删除 `line2/tests/` 下占位 test / 空壳（若有） | ✅ 应在接真实现后立即做 |
| test 顶部 **只从** `line2/is_xhs_growth_aligned.py` import | ✅ 不要 import `learning2/docstring_shell` 或在 test 里写假函数 |
| 保留全部 6 case，删掉 test 内 mock/stub 实现 | ✅ |

本仓 `line2/tests/` 目前仅有 `test_is_xhs_growth_aligned.py`，无额外占位文件；test 无内嵌假函数。

## 仍未实现、但顺序正确的后续

| 顺序 | 步骤 | 说明 |
|------|------|------|
| A | **Git commit** 定稿 kernel + docs | 换机/新 Agent 真相源 |
| B | 扩展 **xiaohongshu Skill**（Brief dict → evaluate → verify） | 在 test 接真文件之后 |
| C | `content/xiaohongshu/` 管线 + 可选 Drive sync | 走 `integrations/index.md` |
| D | 与 `verify-handoff.sh` 并列的 Owner 验收习惯 | XHS 6 case 已在 `check.md` |

## 建议的后续固定节奏（选题 Manager）

1. 在 `content/xiaohongshu/` 写 Brief（dict 或模板转 dict）。
2. 调用 `evaluate_xhs_growth_content` 或跑 verify 同类逻辑。
3. 6/6 或单条 aligned 后再 commit 定稿。
4. Owner 要求时再 sync Drive `05-xiaohongshu/`（folder ID 走 overlay，不臆造）。