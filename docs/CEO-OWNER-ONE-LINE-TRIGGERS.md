---
context_version: "2026-10-30-l012"
repo_path: "docs/CEO-OWNER-ONE-LINE-TRIGGERS.md"
goal: "Owner 一句话 · 启动 CEO（不必贴 bash）"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "b788a446e056c23a"
---

# Owner 一句话 · 启动 CEO（不必贴 bash）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **结论：** 你**不需要**每次把 `manager-ceo-double-iteration.sh` 或 campaign 命令贴进终端或 chat。在本仓库里，**口语目标 = 已授权 00 Manager / CEO 自动跑脚本**（见 `.cursor/rules/danying-manager-auto.mdc`）。
- **Path:** `docs/CEO-OWNER-ONE-LINE-TRIGGERS.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`

## 章节锚点
- **1. 在 Cursor 里（推荐）**: 对本 chat 说任意一句即可，Agent **Must 自动**读 SOP、recover、再执行，**勿**反问「要不要跑 verify」：
- **2. 在终端（可选 · 一键看状态）**: 不代替 chat 里的 Agent，只帮你**看 CEO 下一项该干啥**：
- **3. 和「consult SOP.md」的关系**: Owner 口语 **「consult SOP」** = 读 [`agents/00-manager/CEO-DOUBLE-ITERATION-SOP.md`](../agents/00-manage…
- **4. 相关**: - [AUTO-WORKFLOW.md](../agents/00-manager/AUTO-WORKFLOW.md) · [CEO-DISPATCH-SOP.md](../agents/00-man…


---

## L2 正文

# Owner 一句话 · 启动 CEO（不必贴 bash）

> **结论：** 你**不需要**每次把 `manager-ceo-double-iteration.sh` 或 campaign 命令贴进终端或 chat。在本仓库里，**口语目标 = 已授权 00 Manager / CEO 自动跑脚本**（见 `.cursor/rules/danying-manager-auto.mdc`）。

## 1. 在 Cursor 里（推荐）

对本 chat 说任意一句即可，Agent **Must 自动**读 SOP、recover、再执行，**勿**反问「要不要跑 verify」：

| 你说（示例） | CEO 应做什么 |
|--------------|--------------|
| **danying-brand-agent** / **新机接手** / **完全克隆到本机** | Hub `clone-all.sh`（若换机）→ **`bash scripts/new-machine-bootstrap.sh`**（自动写 daily 09:00 后台配置 · 不必记 `setup-background-goal-evolution.sh`）→ 读 HANDOFF 包 → 接手摘要 |
| **CEO 开始执行** / **请 CEO 开始工作** / **CEO 开始** / **CEO 干活** | **Must** [`CEO-FULL-EXECUTION-MANDATE.md`](./CEO-FULL-EXECUTION-MANDATE.md) → `bash scripts/ceo-full-execution-pipeline.sh --goal "<原话>"`（含 recover · Router · IP 壳 · 矩阵 test · **`run_ceo_xhs_autopilot.py`** · **浏览器弹 HTML**）→ 读 dispatch 叠加 campaign / 深交付 / 双轮 ⑤ 派活记录 |
| **consult SOP，对 Discovery 02 双轮** | 读 `CEO-DOUBLE-ITERATION-SOP.md` → `manager-ceo-double-iteration.sh --phase 1` → 改稿填 log → `--phase 2` |
| **今晚截止 / 深交付 / 交 HTML** | `run-ceo-deep-delivery-cycle.sh`（见 `CEO-OWNER-DEADLINE-DELIVERY.md`） |
| **全员动起来 / 01–12 campaign** | 落盘或更新 dispatch → `run-ceo-ip-all-agents-campaign.sh` |
| **纯解释、不用文件** | 直接答，不强制跑脚本 |

**你不必记：** evaluate、challenge、adversarial、gate — CEO 改 Brief 后 Must 自动跑（`BRIEF-AUTO-GATE-PIPELINE.md`）。

## 2. 在终端（可选 · 一键看状态）

不代替 chat 里的 Agent，只帮你**看 CEO 下一项该干啥**：

```bash
bash scripts/ceo-start-work.sh
```

需要 Agent 已在 chat 里派活、你只想本机看 recover 结果时用这个。真正长跑（Gemini / campaign）仍建议在 **Cursor Agent 会话**里触发，便于改稿与填 `ITERATION-LOG`。

## 3. 和「consult SOP.md」的关系

Owner 口语 **「consult SOP」** = 读 [`agents/00-manager/CEO-DOUBLE-ITERATION-SOP.md`](../agents/00-manager/CEO-DOUBLE-ITERATION-SOP.md)（不是单独一个叫 `SOP.md` 的文件）。CEO 双轮改 Brief 时用；日常 **「CEO 开始工作」** 则按 dispatch 决定走 campaign、深交付还是双轮。

## 4. 相关

- [AUTO-WORKFLOW.md](../agents/00-manager/AUTO-WORKFLOW.md) · [CEO-DISPATCH-SOP.md](../agents/00-manager/CEO-DISPATCH-SOP.md) · [CEO-AUTO-RECOVER-AND-RETRY.md](./CEO-AUTO-RECOVER-AND-RETRY.md)