---
context_version: "2026-10-30-l012"
repo_path: "docs/CEO-XHS-OWNER-DELIVERY-AUTOPILOT.md"
goal: "CEO · 小红书 Owner 交付 autopilot（Must · 2026-10-28）"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "00d8763af41df872"
---

# CEO · 小红书 Owner 交付 autopilot（Must · 2026-10-28）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **Owner 要求（一次写入，永久生效）：** 改 Brief 后 **HTML 必须与 classifier 一致**；**对抗 + 多轮进化 + 压测 + 自检** 全自动，**禁止**再让 Owner 重复「为什么页面没更新 / Discovery 和测试稿分裂 / 只跑 campaign 不 rebuild」。
- **Path:** `docs/CEO-XHS-OWNER-DELIVERY-AUTOPILOT.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`

## 章节锚点
- **2. 完整闭环（顺序 · 不可跳）**: | 步 | 动作 | 脚本 / 文档 |
- **4. 迭代类型（全自动 vs Agent）**: | 类型 | 自动化 | Owner 是否重复说话 |
- **6. 相关**: - [CEO-OWNER-ONE-LINE-TRIGGERS.md](./CEO-OWNER-ONE-LINE-TRIGGERS.md) · [AUTO-WORKFLOW.md](../agents/…


---

## L2 正文

# CEO · 小红书 Owner 交付 autopilot（Must · 2026-10-28）

> **Owner 要求（一次写入，永久生效）：** 改 Brief 后 **HTML 必须与 classifier 一致**；**对抗 + 多轮进化 + 压测 + 自检** 全自动，**禁止**再让 Owner 重复「为什么页面没更新 / Discovery 和测试稿分裂 / 只跑 campaign 不 rebuild」。

**机器可读清单：** [integration/handoff/ceo-xhs-delivery-cycle.json](../integration/handoff/ceo-xhs-delivery-cycle.json)


## 2. 完整闭环（顺序 · 不可跳）

| 步 | 动作 | 脚本 / 文档 |
|----|------|-------------|
| A | 定方向 + **搜坑** MD | [BRIEF-PITFALLS-RESEARCH-SOP.md](../content/xiaohongshu/BRIEF-PITFALLS-RESEARCH-SOP.md) |
| B | 三镜头正文 + redteam L2–L3 | [OWNER-XHS-ADVERSARIAL-AND-EVOLUTION-MANDATE.md](./OWNER-XHS-ADVERSARIAL-AND-EVOLUTION-MANDATE.md) |
| C | **进化直到 READY**（非 L1 alone） | `manager-brief-evolution-until-gap.sh` |
| D | **系列统一**（测试稿 + Discovery 01–04 同案例轴） | [DISCOVERY-SERIES-UNIFIED-NARRATIVE.md](../content/xiaohongshu/DISCOVERY-SERIES-UNIFIED-NARRATIVE.md) |
| E | 同步 **publish-ready-queue**（若有直发段） | `2026-10-20-publish-ready-queue.md` |
| F | **重建** FILTER + TEST HTML | `refresh-owner-notify-html.sh` |
| G | **自检**（标题 + 禁旧稿 + HTML 不早于 Brief） | `verify-owner-html-deliverables.sh` |
| H | 工作流测试稿：**第二轮 01–12 压测** | `ceo-workflow-test-round2-finish.sh`（**勿问 Owner**） |


## 4. 迭代类型（全自动 vs Agent）

| 类型 | 自动化 | Owner 是否重复说话 |
|------|--------|-------------------|
| **内容进化**（gate + adversarial + gap 轮次） | 脚本 + **Agent 轮间改稿** | 否 |
| **HTML 与 Brief 同步** | **F+G 全自动** | 否 |
| **Discovery 系列与测试稿叙事一致** | 规则 + `DISCOVERY-SERIES` + verify 禁旧标题 | 否（改一篇须自检系列） |
| **第二轮 campaign 压测** | **H 全自动**（SKIP_GEMINI 按 lock） | 否 |
| **Prompt/SOP 双轮**（改 INTEGRATION） | `manager-ceo-double-iteration.sh` | 仅 Owner 说 consult SOP 时 |


## 6. 相关

- [CEO-OWNER-ONE-LINE-TRIGGERS.md](./CEO-OWNER-ONE-LINE-TRIGGERS.md) · [AUTO-WORKFLOW.md](../agents/00-manager/AUTO-WORKFLOW.md) · [CEO-WORKFLOW-TEST-SOP.md](./CEO-WORKFLOW-TEST-SOP.md)