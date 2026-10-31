---
context_version: "2026-10-30-l012"
repo_path: "rules/skills/bestpractice_ai_programming_mindset.md"
goal: "AI 编程核心方法论"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "3b26fa7a82ea5f8a"
---

# AI 编程核心方法论

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **上游：** [grapeot/context-infrastructure · bestpractice_ai_programming_mindset.md](https://github.com/grapeot/context-infrastructure/blob/main/rules/skills/bestpractice_ai_program
- **Path:** `rules/skills/bestpractice_ai_programming_mindset.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`

## 章节锚点
- **元数据**: - **类型**: BestPractice
- **"70% 问题"的诊断与解决**
- **认知外包的界限**: 在 AI 能力越来越强、成本越来越低的时代，需要明确哪些任务可以外包、哪些必须保留：
- **文件系统作为天然状态机**: 本地 Agent 模式的核心设计原则：
- **注意事项**: - **生产力陷阱**：为节省微小 Token 成本而牺牲开发者心智带宽和 Flow 状态，属于过早优化


---

## L2 正文

# AI 编程核心方法论

> **上游：** [grapeot/context-infrastructure · bestpractice_ai_programming_mindset.md](https://github.com/grapeot/context-infrastructure/blob/main/rules/skills/bestpractice_ai_programming_mindset.md)（standalone 拷贝；公理全文见上游 `rules/axioms/`，本仓不 vendor。）

## 元数据

- **类型**: BestPractice
- **适用场景**: AI 辅助编程、Agent 系统设计、改本仓 `scripts/` 与 verify 管线
- **创建日期**: 2026-02-21
- **来源**: 多次 AI 编程实践总结
- **最后更新**: 2026-03-01
- **本仓安装**: 2026-10-19


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


## 文件系统作为天然状态机

本地 Agent 模式的核心设计原则：
- 文件系统本身就是最可靠的状态持久化层
- 状态变更 = 文件操作，天然可审计、可回滚
- 避免「内存状态 + 手动持久化」的复杂性

**本仓映射：** 定稿进 Git `content/`；私有凭证在 `vendor/gdocs-skill/secrets/`、`rules/skills/overlays/*.local.md`。


## 注意事项

- **生产力陷阱**：为节省微小 Token 成本而牺牲开发者心智带宽和 Flow 状态，属于过早优化
- **物理锚点**：时间敏感事实需核对（[bestpractice_temporal_info_verification.md](./bestpractice_temporal_info_verification.md) · [check.md](../../check.md) · [`docs/VERIFY-TIERS.md`](../../docs/VERIFY-TIERS.md)）
- **上下文腐烂**：定期反思和固化方法论，避免上下文在 session 间丢失 — 新机读 [docs/AGENT-TAKEOVER.md](../../docs/AGENT-TAKEOVER.md)


**最后更新**: 2026-03-01（本仓本地化：2026-10-19）