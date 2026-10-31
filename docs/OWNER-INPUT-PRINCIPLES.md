---
context_version: "2026-10-30-l012"
repo_path: "docs/OWNER-INPUT-PRINCIPLES.md"
goal: "Owner 输入原则 · 简单说，系统内化"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "68ecc648023b6a49"
---

# Owner 输入原则 · 简单说，系统内化

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **Owner（2026-10-27）：** 基线抬高、LLM/提示词能力变强，应体现在 **系统内部**；**面向 Owner 仍是最简单、最直接的表达**，不要求公式化或「evaluate 过的提示词」。
- **Path:** `docs/OWNER-INPUT-PRINCIPLES.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`

## 章节锚点
- **系统侧（Agent Must 内化）**: | Owner 说的 | 系统内部做什么（Owner 无感） |
- **与双螺旋的关系**: [COLLECTOR-EVALUATOR-PIPELINE.md §双螺旋](./COLLECTOR-EVALUATOR-PIPELINE.md#双螺旋基线升高--标准升高) 里的「标准升高」= **…


---

## L2 正文

# Owner 输入原则 · 简单说，系统内化

> **Owner（2026-10-27）：** 基线抬高、LLM/提示词能力变强，应体现在 **系统内部**；**面向 Owner 仍是最简单、最直接的表达**，不要求公式化或「evaluate 过的提示词」。


## 系统侧（Agent Must 内化）

| Owner 说的 | 系统内部做什么（Owner 无感） |
|------------|---------------------------|
| 任意自然语言 | **CEO（00）** 解析意图 → 派 **部门 GM** · slug · G-* |
| 文案/数据/原话 | **Collector** → `intake/`（即抬高素材基线） |
| 模糊表述 | GM 结合 intake + IP Brief + Intake Stack **补全**，缺关键决策才问一句 |
| 「提示词」在文档里 | 指 **内部** Skill · INTEGRATION-PROMPT · Brief 块 — **由 Agent 选用与迭代**，不是 Owner 要写的模板 |

**基线 + 准确度变高：** 靠 intake/gold 积累 + 内部打回改稿 + Manager's Loop 改集成层提示词 — **不** 靠 Owner 越说越「专业」。


## 与双螺旋的关系

[COLLECTOR-EVALUATOR-PIPELINE.md §双螺旋](./COLLECTOR-EVALUATOR-PIPELINE.md#双螺旋基线升高--标准升高) 里的「标准升高」= **内部** 离 gold 更近、内部质检更稳；**不是** 要求 Owner 输入更规范。