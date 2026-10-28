# Owner 输入原则 · 简单说，系统内化

> **Owner（2026-10-27）：** 基线抬高、LLM/提示词能力变强，应体现在 **系统内部**；**面向 Owner 仍是最简单、最直接的表达**，不要求公式化或「evaluate 过的提示词」。

---

## Owner 侧（唯一要求）

**你怎么方便就怎么来：**

- 口语、碎片、多段、带情绪、有错别字、同时好几件事  
- 可以只有意图（「帮我把 pivot E 写顺」）或只丢文件/链接  
- **不需要** 按 Agent 编号、Skill 名、Brief 模板、verify 口令来说话  

**你只管：** 目标 + 资料（有就给）+ 必要时 **确认**（能发吗、gold、发布）。

---

## 系统侧（Agent Must 内化）

| Owner 说的 | 系统内部做什么（Owner 无感） |
|------------|---------------------------|
| 任意自然语言 | **CEO（00）** 解析意图 → 派 **部门 GM** · slug · G-* |
| 文案/数据/原话 | **Collector** → `intake/`（即抬高素材基线） |
| 模糊表述 | GM 结合 intake + IP Brief + Intake Stack **补全**，缺关键决策才问一句 |
| 「提示词」在文档里 | 指 **内部** Skill · INTEGRATION-PROMPT · Brief 块 — **由 Agent 选用与迭代**，不是 Owner 要写的模板 |

**基线 + 准确度变高：** 靠 intake/gold 积累 + 内部打回改稿 + Manager's Loop 改集成层提示词 — **不** 靠 Owner 越说越「专业」。

---

## 「Gate」是什么（给你一句话，不用你操作）

**Gate = 内部质检门**：Agent 在交给你看之前，用脚本检查（例如小红书 aligned、声音 QA、Brief 规范）。  
**标准可以内部越收越严**；**你的使用门槛不变** — 你不跑 gate、不需要懂 gate 这个词。

**「待 Gate」** 只表示批量脚本当时未重跑 Gate，不等于「永远不能发」；以 Brief 内 `Verify log` 的 **aligned: true** 与 HTML 报告说明为准。

**报告怎么给你看：** 汇总类交付用 **HTML**（可点开、可弹出全文），不用 MD 当主交付。见 [CONTENT-DELIVERY-FOR-OWNER.md](../content/xiaohongshu/CONTENT-DELIVERY-FOR-OWNER.md)。

详见 [CEO-AUTO-QA-LOOP.md](./CEO-AUTO-QA-LOOP.md)（面向 Agent；Owner 可跳过细节）。

---

## 与双螺旋的关系

[COLLECTOR-EVALUATOR-PIPELINE.md §双螺旋](./COLLECTOR-EVALUATOR-PIPELINE.md#双螺旋基线升高--标准升高) 里的「标准升高」= **内部** 离 gold 更近、内部质检更稳；**不是** 要求 Owner 输入更规范。
