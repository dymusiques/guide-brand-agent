# AI 编程核心方法论

> **上游：** [grapeot/context-infrastructure · bestpractice_ai_programming_mindset.md](https://github.com/grapeot/context-infrastructure/blob/main/rules/skills/bestpractice_ai_programming_mindset.md)（standalone 拷贝；公理全文见上游 `rules/axioms/`，本仓不 vendor。）

## 元数据

- **类型**: BestPractice
- **适用场景**: AI 辅助编程、Agent 系统设计、改本仓 `scripts/` 与 verify 管线
- **创建日期**: 2026-02-21
- **来源**: 多次 AI 编程实践总结
- **最后更新**: 2026-03-01
- **本仓安装**: 2026-10-19

---

## 基础公理（本仓对齐，不展开 axioms 目录）

- **T05**：认知是资产，代码是消耗品 — IP/Pitch/红线在 `content/personal-ip/`、`rules/USER.md`；脚本与集成可迭代。
- **T02**：结果确定性优于过程确定性 — 与 [bestpractice_skill_writing.md](./bestpractice_skill_writing.md) 一致。

---

## "70% 问题"的诊断与解决

### 问题本质

AI 编程中常见的"70% 问题"——AI 能完成 70%，但最后 30% 总是各种问题——根本原因是**自我迭代反馈环被打破**：

1. **AI 无法感知产出是否符合期望**：没有"眼睛"看结果
2. **成功标准太主观**：缺乏明确的"好"的定义，AI 不知道往什么方向迭代

### 解决方案

1. **为 AI 打开感知通道**：
   - 让 AI 能看到运行结果（截图、日志、测试输出）
   - 提供 UI 时附带视觉反馈
   - 执行命令后返回完整输出

2. **建立清晰的成功标准**：
   - 明确"什么是好"（不只是"能跑"）
   - 量化指标优于主观描述
   - 提供参考案例或期望输出

---

## Reasoning Model 与 Agentic Workflow 的关系

### 互补而非替代

- **Reasoning Model**：擅长深度分析、复杂推理、规划
- **Agentic Workflow**：擅长协调执行、工具调用、状态管理

### Reasoning Model 的局限

Reasoning Model 的"反思"是 stateless 的——它无法感知外部世界的变化。思考结束后，世界已经变了。

### 推荐架构

生产环境采用**混合架构**：
- Reasoning Model 做深度分析和规划
- Agentic Workflow 做协调执行和状态管理
- 外部 orchestration 负责整体流程控制

**本仓映射：** [agents/00-manager/AUTO-WORKFLOW.md](../../agents/00-manager/AUTO-WORKFLOW.md) · `bash scripts/manager-workflow-verify.sh` · `bash scripts/verify-handoff-program.sh`

---

## 认知外包的界限

在 AI 能力越来越强、成本越来越低的时代，需要明确哪些任务可以外包、哪些必须保留：

### 可以外包的

- 查漏补缺：信息收集、格式整理
- 机械执行：重复性编码、文档生成
- 快速原型：探索性实现

### 必须保留的

- 形成自己的观点
- 定义问题和成功标准
- 关键决策的价值判断
- 对输出质量的最终审核

**本仓映射：** Owner 定目标与发布；Brief 未 `aligned: true` 不 commit（见 [integration/IMPORTANT.md](../../integration/IMPORTANT.md)）。

---

## "直觉"优于"程序"拐点

对于复杂语义任务，LLM 的"黑盒直觉"可能比显性逻辑代码更具韧性和效率。

当任务涉及：
- 复杂语义理解
- 多因素权衡
- 边界模糊的判断

LLM 的端到端处理可能比显式规则更 robust。这是从"程序思维"到"直觉思维"的范式转变。

**本仓边界：** 小红书 growth **aligned** 以 `evaluate-xhs-topic.py` + kernel 为可验证 gate；语义创作在 gate 内完成，**不**用「直觉」跳过验收。

---

## 文件系统作为天然状态机

本地 Agent 模式的核心设计原则：
- 文件系统本身就是最可靠的状态持久化层
- 状态变更 = 文件操作，天然可审计、可回滚
- 避免「内存状态 + 手动持久化」的复杂性

**本仓映射：** 定稿进 Git `content/`；私有凭证在 `vendor/gdocs-skill/secrets/`、`rules/skills/overlays/*.local.md`。

---

## AI 时代数据科学家三大原型

技能正在贬值，但特质与性格越来越重要。三种角色：

1. **架构师**：定义问题、设计系统、编排能力边界
2. **审计师**：评估 quality、发现模式、交叉验证
3. **全栈构建者**：端到端交付、快速原型、集成验证

核心洞察：同一人可以扮演不同角色，但明确当前角色能避免思维混乱。

---

## 注意事项

- **生产力陷阱**：为节省微小 Token 成本而牺牲开发者心智带宽和 Flow 状态，属于过早优化
- **物理锚点**：时间敏感事实需核对（本仓见 [check.md](../../check.md)、[`docs/VERIFY-TIERS.md`](../../docs/VERIFY-TIERS.md)；上游 [`bestpractice_temporal_info_verification.md`](https://github.com/grapeot/context-infrastructure/blob/main/rules/skills/bestpractice_temporal_info_verification.md) 未安装）
- **上下文腐烂**：定期反思和固化方法论，避免上下文在 session 间丢失 — 新机读 [docs/AGENT-TAKEOVER.md](../../docs/AGENT-TAKEOVER.md)

---

## AI 落地核心决策

### 1. 用本地 Coding Agent 而非 ChatGPT

- 降低上下文传递与落地 friction
- Agent 直接操作代码库，而非复制粘贴
- ChatGPT 适合快速问答，不适合系统开发

### 2. 动手前先定义成功标准

- 建立测试作为 feedback loop
- 明确"什么是好"，不只"能跑"
- 测试是给 AI 的 navigation 信号

### 3. 让 Agent 自己处理 corner case

- 结果确定性 vs 过程确定性
- 不要事无巨细规定步骤，让 AI 自己决策实现路径
- 关注产出是否符合预期，而非实现过程是否"正确"

### 4. Divide and conquer 应对 context window saturation

- 多个 sub-agent 并行处理（按任务需要，不必固定数量）
- 每个 sub-agent 职责单一
- 最后汇总而非一次性塞入所有信息

### 5. Prompt 自举且结果导向

- 让 AI 自己迭代和改进
- 不规定每一步怎么做
- 用短 prompt 撬动长执行 — AI 是杠杆

---

**最后更新**: 2026-03-01（本仓本地化：2026-10-19）
