---
context_version: "2026-10-30-l012"
repo_path: "rules/skills/workflow_parallel_subagents.md"
goal: "并行 Subagent 工作流"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "ad0e3280aaf47119"
---

# 并行 Subagent 工作流

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** - 2–3 个精心设计的 subagent 通常优于 5 个松散任务。
- 并行消耗更多 token；轻量任务不要「多 agent 仪式」。
- Research / 大规模探索：关键中间工件整理到 `tmp/parallel/<session_slug>/`。
- **Path:** `rules/skills/workflow_parallel_subagents.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`

## 章节锚点
- **L1 任务（压缩 · Open WebUI / Cursor 顶栏）**: - **Goal:** > **上游：** [grapeot/context-infrastructure · workflow_parallel_subagents.md](https://gith…
- **章节锚点**: - **元数据**: - **类型**: Workflow
- **注意事项**: - 2–3 个精心设计的 subagent 通常优于 5 个松散任务。
- **常见错误**: | 错误 | 正确做法 |


---

## L2 正文

# 并行 Subagent 工作流

> **上游：** [grapeot/context-infrastructure · workflow_parallel_subagents.md](https://github.com/grapeot/context-infrastructure/blob/main/rules/skills/workflow_parallel_subagents.md)（standalone 拷贝，已做 Cursor / 本仓裁剪。）  
> **本仓边界：** 与 [integration/parallel-subagents-adoption.md](../../integration/parallel-subagents-adoption.md) 一起读；**品牌 Brief 定稿链**仍以 [agents/00-manager/AUTO-WORKFLOW.md](../../agents/00-manager/AUTO-WORKFLOW.md) **顺序**为准。  
> **私有路径：** [overlays/workflow-parallel-subagents.local.example.md](./overlays/workflow-parallel-subagents.local.example.md) → `workflow-parallel-subagents.local.md`

## 元数据

- **类型**: Workflow
- **适用场景**: 独立 review、并行调研探索；**仅 Owner 明确要求**时的实现委派
- **本仓安装**: 2026-10-19


## 核心判断

Subagent 的主要价值不是模拟人类团队，也不是把普通任务包装得更复杂。它解决的是三类具体问题：

1. **上下文窗口隔离**：不同 agent 各自持有一段可控上下文，避免主线程同时塞入大量文件、网页、日志和中间判断。
2. **并行读与独立探索**：多个 agent 同时搜索、阅读、定位、复核，减少单一路径依赖。
3. **交叉验证**：不同 agent 在有意重叠的范围内独立得出结论，用一致和分歧暴露遗漏、误读和假设冲突。

Multi-agent 在 research-heavy、read-heavy、高价值任务上更容易成立；在需要大量共享状态、连续协调写入、实时互相修正的任务上成本高且脆弱。

## 委派边界与何时使用并行模式

先决定是否委派，再决定是否并行：**实现默认主线程亲自做**，仅 Owner **明确要求**委派实现时才分派。多文件、模块独立、省上下文或模型便宜均**不构成**授权。

Code / privacy / design review 通常交 **独立** Task 或 Bugbot 子代理，主线程（或 00 Manager）最终验收。广泛调研探索可按独立维度拆分多个 Task。

启动多个 subagent 并行时，满足以下条件中的 **至少 2 条**，且没有命中下方反模式：

1. **信息面宽**：多个文件、网页、数据源、时间段，主线程一次性读完会污染上下文。
2. **可拆分为独立读任务**：至少 2 个相对独立的探索方向，每个方向预期 **≥5** 个 tool call。
3. **需要独立判断**：反方审稿、事实核查、竞品对照、方案对比。
4. **存在高价值不确定性**：结果影响后续决策、公开输出、代码改动或高成本行动。
5. **主线程需要保留整合能力**：主 agent 负责拆分、标准、整合证据和最终判断。

不满足时：主线程直接执行，或 **单次** 独立 review。

## 反模式

1. **单点小任务**：1–2 个文件或轻微改动（单次 review 仍按风险判断）。
2. **强顺序依赖**：下一步必须依赖上一步输出（**含 Brief：evaluate 前须成稿 → 对齐 00 Manager 步 2→3**）。
3. **共享状态写入**：多 agent 同时改同一 Brief、同一份 `content/` 定稿。
4. **上下文必须完整共享**：拆分后丢条件。
5. **验证标准不清**：无输出格式、证据要求或验收条件。

## 任务类型参考

| 任务类型 | 是否适合 | 推荐方式 |
|---|---|---|
| 外部调研、市场/竞品 survey | 高 | 2–3 个 Task，按证据功能切分，30–50% overlap |
| 大型代码库理解、verify 脚本定位 | 高 | `explore` 按模块切分，主线程整合 |
| 代码 / 设计 review | 高 | 1 个独立 reviewer 或 `bugbot`；主线程验收 |
| 小红书 Brief 写稿 + evaluate | 低（并行写） | **顺序** 04 → evaluate；调研阶段可并行读 IP/竞品 |
| 工程实现（多文件） | 默认不委派 | 仅 Owner 明确要求时分派 |
| 多 agent 同时写同一文件 | 低 | 先并行读/审，**单一 writer** 写定稿 |


## 路由决策（本仓）

1. 库内探索 → `explore`；广义调研 → `generalPurpose`。
2. 用户指定 review → `bugbot`（见 `$0/review-bugbot/SKILL.md`）或 Owner 指令。
3. **Brief / IP / 触达定稿** → 不走并行写；走 00 Manager 链 + `manager-workflow-verify.sh`。
4. 隐私与 Dry Run → [integration/IMPORTANT.md](../../integration/IMPORTANT.md)。

---

## 注意事项

- 2–3 个精心设计的 subagent 通常优于 5 个松散任务。
- 并行消耗更多 token；轻量任务不要「多 agent 仪式」。
- Research / 大规模探索：关键中间工件整理到 `tmp/parallel/<session_slug>/`。

## 常见错误

| 错误 | 正确做法 |
|------|---------|
| 并行写同一 Brief | 并行调研，单线程写稿 + evaluate |
| 用并行代替 00 Manager 步序 | 步 2→3 顺序不变 |
| 编造 subagent 类型 | 仅用 schema 列出的类型 |
| 中文会话却用英文 prompt 模板 | prompt 内显式 LANGUAGE 要求 |
| subagent 总结不落盘 | parent 补落盘或要求 child 写文件 |