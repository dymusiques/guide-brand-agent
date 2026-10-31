---
context_version: "2026-10-30-l012"
repo_path: "docs/CEO-FULL-EXECUTION-MANDATE.md"
goal: "CEO 全量执行 · Owner 固定（Must · 2026-10-30）"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "a971d2ea99a64eb1"
---

# CEO 全量执行 · Owner 固定（Must · 2026-10-30）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **一句话：** Owner 给**任何目标任务**，或说 **「CEO 开始执行 / CEO 开始工作 / CEO 干活」** → Agent **Must** 以 **00 CEO** 派活 **01–12 + 函数壳 + evaluate + 对抗 + 进化 + 压测 + HTML 浏览器弹出**，**禁止**再问 Owner「要不要跑脚本 / e
- **Path:** `docs/CEO-FULL-EXECUTION-MANDATE.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`

## 章节锚点
- **0. GM → CEO · 六项 6-case + 三重 evaluate + 双重压测**: **完整定义：** [`CEO-SIX-CASE-GM-TO-CEO-WORKFLOW.md`](./CEO-SIX-CASE-GM-TO-CEO-WORKFLOW.md) · 机器清单 [`inte…
- **1. 机器入口（Must · 每次 CEO 会话）**: ```bash
- **2. 执行顺序（不可跳 · Agent 单会话扮演各 GM）**: | 步 | 谁 | 做什么 | 脚本 / 文档 |
- **3. Cursor 规则锚点**: - [`.cursor/rules/danying-manager-auto.mdc`](../.cursor/rules/danying-manager-auto.mdc) · **§0 CEO 全…
- **4. Owner 不必重复的话**: - evaluate / challenge / adversarial / gate / evolution


---

## L2 正文

# CEO 全量执行 · Owner 固定（Must · 2026-10-30）

> **一句话：** Owner 给**任何目标任务**，或说 **「CEO 开始执行 / CEO 开始工作 / CEO 干活」** → Agent **Must** 以 **00 CEO** 派活 **01–12 + 函数壳 + evaluate + 对抗 + 进化 + 压测 + HTML 浏览器弹出**，**禁止**再问 Owner「要不要跑脚本 / evaluate / autopilot」。

## 0. GM → CEO · 六项 6-case + 三重 evaluate + 双重压测

**完整定义：** [`CEO-SIX-CASE-GM-TO-CEO-WORKFLOW.md`](./CEO-SIX-CASE-GM-TO-CEO-WORKFLOW.md) · 机器清单 [`integration/handoff/ceo-full-execution-cycle.json`](../integration/handoff/ceo-full-execution-cycle.json)  
**Cursor 交 Owner 格式：** [`OWNER-CHAT-DELIVERY-FORMAT.md`](./OWNER-CHAT-DELIVERY-FORMAT.md) · 产物 `ceo-inbox/CEO-RUN-MANIFEST-latest.json`

## 1. 机器入口（Must · 每次 CEO 会话）

```bash
# 推荐：recover + Router + IP 壳 + 集成/矩阵抽检 + XHS autopilot + 打开 HTML
bash scripts/ceo-full-execution-pipeline.sh --goal "<Owner 原话>" [--brief content/xiaohongshu/<file>-brief.md]

# 等价 Python
.venv/bin/python scripts/run_ceo_full_execution.py --goal "<Owner 原话>" [--brief …]
```

**小红书新篇：** 先按 [`CEO-XHS-NEW-BRIEF-AUTOPILOT.md`](./CEO-XHS-NEW-BRIEF-AUTOPILOT.md) + [`OWNER-LONGFORM-XHS-SPEC.md`](../content/xiaohongshu/OWNER-LONGFORM-XHS-SPEC.md) 写 intake/pitfalls/长稿 Brief，再：

```bash
bash scripts/ceo-full-execution-pipeline.sh --goal "<主题>" --brief content/xiaohongshu/<file>-brief.md
```

## 2. 执行顺序（不可跳 · Agent 单会话扮演各 GM）

| 步 | 谁 | 做什么 | 脚本 / 文档 |
|----|-----|--------|-------------|
| 0 | **CEO** | 进程自愈 | `ceo-auto-recover-blocked.sh` → 读 `ceo-auto-recover-latest.md` |
| −1 | **Router** | Open WebUI / 目标路由 | `run-openwebui-router-pipeline.sh --goal "…"` |
| 1 | **01 IP** | 函数壳 / KPI 边界 | `evaluate_personal_ip.py --check` |
| 2 | **集成** | Google/Drive 读、handoff | `verify-integration.sh`（FAIL 写 terminal-once，**不** chat 甩 Connect） |
| 3 | **01–12 矩阵** | sub-agent **test 函数** 抽检 | `verify-agent-matrix.sh --agent 01` … `04` …（全量可选 `CEO_FULL_MATRIX_ALL=1`） |
| 4 | **04** | 搜坑 · 三镜头 · **长稿 3000–5000 字** | pitfalls · [`OWNER-LONGFORM-XHS-SPEC.md`](../content/xiaohongshu/OWNER-LONGFORM-XHS-SPEC.md) |
| 5 | **04+05** | redteam L2–L3 · **evaluate** · **Clever 反方席** · 对抗 | `evaluate-xhs-brief-complete.py`（含 clever）· `verify-xhs-clever-advocate.sh` · `run-xhs-brief-adversarial-challenge.py` |
| 6 | **CEO** | **Python autopilot** 闭环 | **`run_ceo_xhs_autopilot.py`**（进化 + HTML rebuild + verify） |
| 7 | **CEO** | 工作流 **round2 压测**（测试稿 READY） | `ceo-workflow-test-round2-finish.sh` |
| 8 | **CEO** | **Owner 必见 HTML** | `refresh-owner-notify-html.sh` → **`open-owner-xhs-deliverable-html.sh`**（`#owner-latest`） |

深交付 / 全员 campaign：**另**按 dispatch 跑 `run-ceo-deep-delivery-cycle.sh` / `run-ceo-ip-all-agents-campaign.sh`（与上表并行时遵守 lock · 见 IMPORTANT.md）。

## 3. Cursor 规则锚点

- [`.cursor/rules/danying-manager-auto.mdc`](../.cursor/rules/danying-manager-auto.mdc) · **§0 CEO 全量执行**
- [`CEO-OWNER-ONE-LINE-TRIGGERS.md`](./CEO-OWNER-ONE-LINE-TRIGGERS.md) · 口语 **「CEO 开始执行」**
- [`agents/00-manager/AUTO-WORKFLOW.md`](../agents/00-manager/AUTO-WORKFLOW.md) · 指挥链
- [`CEO-XHS-OWNER-DELIVERY-AUTOPILOT.md`](./CEO-XHS-OWNER-DELIVERY-AUTOPILOT.md) · evaluate + HTML + round2
- [`OWNER-DELIVERY-NOTIFY-DEFAULT.md`](./OWNER-DELIVERY-NOTIFY-DEFAULT.md) · 浏览器打开 Must

## 4. Owner 不必重复的话

- evaluate / challenge / adversarial / gate / evolution  
- `run_ceo_xhs_autopilot.py` / refresh HTML / **弹出 HTML**  
- 长稿 **3000–5000 字**、Web 搜引用、吸睛幽默犀利  
- sub-agent 矩阵 / `evaluate_personal_ip` / 集成 verify  

以上已全部写入本 Mandate + 04 INTEGRATION-PROMPT + intake 模板。