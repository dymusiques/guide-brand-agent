# IMPORTANT · Manager / 集成层必读（<!-- important -->）

集成 Agent **只读本文件 + 各 agent 的 INTEGRATION-PROMPT**，**不复制** classifier docstring 全文。

## Owner 目标（P 层）

- **强链接** 客户：品牌（**跨行业 open**）、艺术家、教育、AI×数字藏品创新者 —— 非 vanity 流量。
- **质量涨粉：** 约 1700 → 5000 → 10000（小红书为主渠道之一）。
- **不单品类绑定：** 不排斥任何品类合作；但 **不得** 把账号绑成某一商品/行业的主攻号（家居/建材仅是曾误绑示例；**对所有垂直同样适用**）。富森美类案例仅历史一笔，不作系列默认。

## 黑盒核心（勿在集成层改规则）

- `kernels/xiaohongshu/line2/is_xhs_growth_aligned.py`
- 验收：`bash scripts/verify-xhs-topic.sh`（**6 Gemini case**）

## 集成调用（胶水）

- 单条：`python scripts/evaluate-xhs-topic.py --brief content/xiaohongshu/<file>.md`
- 批量：`bash scripts/verify-xhs-content-dir.sh`
- 全仓集成构建：`bash scripts/verify-all.sh` · 目标表 `integration/GOALS-REGISTRY.md`
- IP 真相：`content/personal-ip/ip-positioning-brief-2026-10-05.md`

## 后台目标链（Owner · setup 一次）

- 机器层：`bash scripts/setup-background-goal-evolution.sh` → Process Launcher 常驻 · [docs/BACKGROUND-GOAL-EVOLUTION.md](../docs/BACKGROUND-GOAL-EVOLUTION.md)  
- 验收 / evolution rollup / dispatch / `agent-work-queue` **自动**；Cursor CEO 读队列写稿；**不** 要求 Owner 每次说 verify。

## Owner 打开对话 · Artist 对标审阅（Must · 不每日提示）

- GM10 **每天**更新分析；合并目录 `content/ip-research/artist-intel-catalog.md`  
- Owner **打开对话**时若有未审条目 → Agent **一次性列全**待裁决清单 · 见 [docs/OWNER-ARTIST-CATALOG-ON-OPEN.md](../docs/OWNER-ARTIST-CATALOG-ON-OPEN.md)

## Owner 怎么说话（Must · 零公式）

- **最简单、最直接即可**（口语、碎片、多意图）；系统 **内化** 为 intake + 派活 + 内部提示词，**不要** 要求 Owner 按 Skill/Brief/verify 口令说话。见 [docs/OWNER-INPUT-PRINCIPLES.md](../docs/OWNER-INPUT-PRINCIPLES.md)。

## CEO 交 Owner 前（Must · 内部 Gate，不抬高 Owner 门槛）

- **Agent 自验，默认不让 Owner 逐条跑 verify。** Gate = 内部质检（aligned 等），仅 Agent 跑 `manager-ceo-owner-gate.sh`；FAIL 打回 GM，同会话改稿（默认 ≤3 轮）。见 [docs/CEO-AUTO-QA-LOOP.md](../docs/CEO-AUTO-QA-LOOP.md)。

## 红线

- 未 `aligned: true` → 不 sync Drive；不只 Drive 不 commit。
- 集成层 **不写算法层 prompt**；失败时先区分：集成路径 / Brief 内容 / kernel。

## 扩展与预留（架构）

- **默认运行：** Cursor + 00 Manager + 按需 autopilot；Process Launcher **工具箱、非常驻**（见 [process-launcher-adoption.md](./process-launcher-adoption.md) §0）。
- **以后加能力：** 先查 [EXTENSION-POINTS.md](./EXTENSION-POINTS.md) 接接口，再改 vendor/router/overlay；禁止平行第二 CEO 或第二派活文件。

## Dry Run（破坏性 / 发布侧 · 摘录）

小红书 Brief 三阶段与状态见 [content/xiaohongshu/PIPELINE.md](../content/xiaohongshu/PIPELINE.md)。以下为 **全仓** 集成层在动线上环境前的检查（参考 [grapeot staged approach](https://github.com/grapeot/context-infrastructure/blob/main/rules/skills/bestpractice_staged_approach.md)，本仓不装 standalone MD）。

**默认禁止（除非 Owner 当轮明确授权）：** 代发小红书/私信 mass、Gmail 发送、Drive 覆盖定稿、删库/硬重置、对 `main` 的 force 操作。

**破坏性操作前必过：**

- [ ] **范围**：影响哪些路径/记录（列清单，避免 `git add .` 盲加）
- [ ] **内容**：变更 diff 或命令语义与 Owner 意图一致
- [ ] **可回滚**：Git 可 revert；secrets 不在 commit 内
- [ ] **环境**：脚本/verify 在本地 repo 跑通；非 Owner 生产账号上的不可逆写

**常见映射：** CSV → `content/analytics/inbox/` 只读归档后再 pipeline（见 analytics README）；Brief 发布仅 Owner；`gdocs` 写操作先 overlay 路径再 CLI。
