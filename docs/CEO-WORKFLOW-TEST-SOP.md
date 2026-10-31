---
context_version: "2026-10-30-l012"
repo_path: "docs/CEO-WORKFLOW-TEST-SOP.md"
goal: "CEO 工作流测试 · 第二轮压测 SOP（Owner 授权 · 无需确认）"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "0cd3eeab01caa910"
---

# CEO 工作流测试 · 第二轮压测 SOP（Owner 授权 · 无需确认）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **Owner 规则：** 完成「工作流测试稿」（Brief gate PASS 或全链路 test）后，**Must 自动**跑第二轮 **01–12 campaign**，刷新 Owner HTML，**浏览器打开**，**勿**问 Owner「要不要压测」。
- **Path:** `docs/CEO-WORKFLOW-TEST-SOP.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`

## 章节锚点
- **一条命令**: ```bash
- **Agent Must（Cursor）**: - 工作流测试会话 **结束前** 自动执行上脚本（campaign FAIL 仍刷新/打开 HTML，并在派活记录写 failures 数）。
- **已知 FAIL 边界**: | 原因 | 处置 |
- **相关**: - [WORKFLOW-AUTOMATION-MATRIX.md](./WORKFLOW-AUTOMATION-MATRIX.md) · `integration/handoff/workflow-a…


---

## L2 正文

# CEO 工作流测试 · 第二轮压测 SOP（Owner 授权 · 无需确认）

> **Owner 规则：** 完成「工作流测试稿」（Brief gate PASS 或全链路 test）后，**Must 自动**跑第二轮 **01–12 campaign**，刷新 Owner HTML，**浏览器打开**，**勿**问 Owner「要不要压测」。

## 一条命令

```bash
bash scripts/ceo-workflow-test-round2-finish.sh
```

等价于：

1. `VERIFY_GOALS_SKIP_PLATFORM=1` · `run-ceo-ip-all-agents-campaign.sh`（deep 在跑时自动 `SKIP_GEMINI=1`）
2. **`refresh-owner-notify-html.sh`**（Must）→ 从最新 `*-test-brief.md` **重建** FILTER + TEST HTML · `verify-owner-html-deliverables.sh`
3. `open` · 两页 HTML · 标题须与 Brief `subject` 一致（verify 强制）

**禁止：** 只改 Brief 不跑 refresh；手改 HTML 当交付（会被下次 rebuild 覆盖）。

## Agent Must（Cursor）

- 工作流测试会话 **结束前** 自动执行上脚本（campaign FAIL 仍刷新/打开 HTML，并在派活记录写 failures 数）。
- **交 Owner：否** · 通知 HTML 即可（[OWNER-DELIVERY-NOTIFY-DEFAULT.md](./OWNER-DELIVERY-NOTIFY-DEFAULT.md)）。

## 已知 FAIL 边界

| 原因 | 处置 |
|------|------|
| Agent 08 · Drive OAuth 未授权 | `VERIFY_GOALS_SKIP_PLATFORM=1` 已默认；全绿需 Owner Connect |
| Agent 03 · Gemini 6 超时 | deep 并行时 `SKIP_GEMINI=1` |
| 06 pipeline · 单 Brief kernel 6 偶发 FAIL | 对该 Brief 再跑 `manager-ceo-gate-one-round.sh` 后重跑 campaign |

## 相关

- [WORKFLOW-AUTOMATION-MATRIX.md](./WORKFLOW-AUTOMATION-MATRIX.md) · `integration/handoff/workflow-automation-manifest.json`