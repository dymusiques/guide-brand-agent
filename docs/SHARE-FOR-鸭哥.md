# 分享给鸭哥 · Brand Agent 总览（GitHub 可读）

> **鸭哥主文档（Personal IP + CEO 派活 · 全 GitHub 链接）：** [YAGE-PERSONAL-IP-CEO-REVIEW-GUIDE.md](https://github.com/dymusiques/guide-brand-agent/blob/main/docs/YAGE-PERSONAL-IP-CEO-REVIEW-GUIDE.md)  
> **重要：** 主仓库 `guide-brand-agent` 当前为 **Private**。未登录 GitHub 或无权限的人会看到 **404**（不是文件丢了）。  
> **给鸭哥的公开链接（无需登录）：** [Gist · 本导读](https://gist.github.com/dymusiques/1efd20ba040828b8e9def78de9e56672)  
> **私有仓（仅已授权账号）：** [github.com/dymusiques/guide-brand-agent](https://github.com/dymusiques/guide-brand-agent)  
> **交互思维导图：** [htmlpreview · 导图](https://htmlpreview.github.io/?https://gist.githubusercontent.com/dymusiques/1efd20ba040828b8e9def78de9e56672/raw/owner-stack-openwebui-mindmap.html)（或 Gist 页里点 `owner-stack-openwebui-mindmap.html` → Raw）。  
> **说明：** 点导图方块 → **底部黑色栏**出现工序说明。

---

## 1. 发给鸭哥的一句话

「这是我们品牌 IP / 小红书 / 多 Agent 工作流的 **GitHub 定稿仓**。请先看 **交互导图**（上面 htmlpreview 链接），再按需点开各 MD。Open WebUI 是本地 RAG 界面；**定稿与测评在 Cursor + 仓库脚本**。」

---

## 2. 系统分三块（避免和 Open WebUI 混淆）

| 块 | 干什么 | 鸭哥怎么看 |
|----|--------|------------|
| **Git 仓（本 repo）** | 规则、CEO 工作流、Brief、脚本、验收 | 浏览器看 MD + 导图 |
| **Cursor** | 写稿、改 MD、跑 verify / evolution / 交 HTML | 我本机 IDE（鸭哥可不装） |
| **Open WebUI（本机 Docker）** | RAG 四包：Drive 背书、corpus、SOP、workflow 命令 | 需我本机；**push 不会自动更新 Knowledge** |

**Drive 资料库：** 主要在 Open WebUI 的 `brand-ip-knowledge`（镜像 Google Drive）。**用 Cursor 提炼** = 改 Git 里 MD + 跑 gate/evolution（定稿级）。

---

## 3. CEO · 测评 · Evolution

均在仓库内，**不是**只在本地 HTML。

| 能力 | GitHub 入口 |
|------|-------------|
| CEO 全量执行 | [docs/CEO-FULL-EXECUTION-MANDATE.md](https://github.com/dymusiques/guide-brand-agent/blob/main/docs/CEO-FULL-EXECUTION-MANDATE.md) · [scripts/ceo-full-execution-pipeline.sh](https://github.com/dymusiques/guide-brand-agent/blob/main/scripts/ceo-full-execution-pipeline.sh) |
| 00 Manager 指挥链 | [agents/00-manager/AUTO-WORKFLOW.md](https://github.com/dymusiques/guide-brand-agent/blob/main/agents/00-manager/AUTO-WORKFLOW.md) |
| 六项 6-case + GM 胶水 | [docs/CEO-SIX-CASE-GM-TO-CEO-WORKFLOW.md](https://github.com/dymusiques/guide-brand-agent/blob/main/docs/CEO-SIX-CASE-GM-TO-CEO-WORKFLOW.md) · [scripts/ceo-six-case-battery.sh](https://github.com/dymusiques/guide-brand-agent/blob/main/scripts/ceo-six-case-battery.sh) · [integration/agents/](https://github.com/dymusiques/guide-brand-agent/tree/main/integration/agents) |
| 成功目标 G-* | [integration/GOALS-REGISTRY.md](https://github.com/dymusiques/guide-brand-agent/blob/main/integration/GOALS-REGISTRY.md) |
| Triple eval + baseline 距离 | [scripts/ceo-triple-eval-baseline-loop.sh](https://github.com/dymusiques/guide-brand-agent/blob/main/scripts/ceo-triple-eval-baseline-loop.sh) · [docs/MANAGER-EVAL-IMPROVEMENT-LOOP.md](https://github.com/dymusiques/guide-brand-agent/blob/main/docs/MANAGER-EVAL-IMPROVEMENT-LOOP.md) |
| Evolution 测距 READY | [scripts/analyze-brief-evolution-gap.py](https://github.com/dymusiques/guide-brand-agent/blob/main/scripts/analyze-brief-evolution-gap.py) · [docs/OWNER-XHS-ADVERSARIAL-AND-EVOLUTION-MANDATE.md](https://github.com/dymusiques/guide-brand-agent/blob/main/docs/OWNER-XHS-ADVERSARIAL-AND-EVOLUTION-MANDATE.md) |
| 压测 double-stress | [scripts/ceo-double-stress.sh](https://github.com/dymusiques/guide-brand-agent/blob/main/scripts/ceo-double-stress.sh) |
| 机器步骤表 JSON | [integration/handoff/ceo-full-execution-cycle.json](https://github.com/dymusiques/guide-brand-agent/blob/main/integration/handoff/ceo-full-execution-cycle.json) |

---

## 4. 自动 Workflow · 派活

| 能力 | GitHub 入口 |
|------|-------------|
| L0–L4 自动化矩阵 | [docs/WORKFLOW-AUTOMATION-MATRIX.md](https://github.com/dymusiques/guide-brand-agent/blob/main/docs/WORKFLOW-AUTOMATION-MATRIX.md) · [integration/handoff/workflow-automation-manifest.json](https://github.com/dymusiques/guide-brand-agent/blob/main/integration/handoff/workflow-automation-manifest.json) |
| 按口令跑层 | [scripts/run-workflow-from-manifest.py](https://github.com/dymusiques/guide-brand-agent/blob/main/scripts/run-workflow-from-manifest.py) |
| Autopilot / 派活 | [docs/AUTOPILOT.md](https://github.com/dymusiques/guide-brand-agent/blob/main/docs/AUTOPILOT.md) · [scripts/manager-autopilot.sh](https://github.com/dymusiques/guide-brand-agent/blob/main/scripts/manager-autopilot.sh) |

---

## 5. Open WebUI · RAG（随仓脚本）

| 能力 | GitHub 入口 |
|------|-------------|
| 脚本与配置说明 | [integration/openwebui-rag/README.md](https://github.com/dymusiques/guide-brand-agent/blob/main/integration/openwebui-rag/README.md) |
| CEO Router | [docs/OPENWEBUI-CEO-ROUTER.md](https://github.com/dymusiques/guide-brand-agent/blob/main/docs/OPENWEBUI-CEO-ROUTER.md) |
| 上下文 L0/L1/L2 | [docs/PROMPT-CONTEXT-STANDARD.md](https://github.com/dymusiques/guide-brand-agent/blob/main/docs/PROMPT-CONTEXT-STANDARD.md) · [docs/CONTEXT-WINDOW-AND-DATA-ROUTING.md](https://github.com/dymusiques/guide-brand-agent/blob/main/docs/CONTEXT-WINDOW-AND-DATA-ROUTING.md) |
| Handoff JSON | [integration/handoff/openwebui-context-reorg-latest.json](https://github.com/dymusiques/guide-brand-agent/blob/main/integration/handoff/openwebui-context-reorg-latest.json) |

---

## 6. 新 Agent 接手（一键读序）

| 步骤 | 链接 |
|------|------|
| 新电脑口令 | [新电脑一句话.md](https://github.com/dymusiques/guide-brand-agent/blob/main/%E6%96%B0%E7%94%B5%E8%84%91%E4%B8%80%E5%8F%A5%E8%AF%9D.md) |
| 接手手册 | [docs/AGENT-TAKEOVER.md](https://github.com/dymusiques/guide-brand-agent/blob/main/docs/AGENT-TAKEOVER.md) |
| MD 清单 | [docs/HANDOFF-MD-MANIFEST.md](https://github.com/dymusiques/guide-brand-agent/blob/main/docs/HANDOFF-MD-MANIFEST.md) |
| Workflow 思维导图（CEO 部门向） | [htmlpreview · workflow-handoff-mindmap.html](https://htmlpreview.github.io/?https://raw.githubusercontent.com/dymusiques/guide-brand-agent/main/docs/workflow-handoff-mindmap.html) |

---

## 7. 与本地 `file://` HTML 的关系

- 我本机路径：`content/evolution/00-manager/ceo-inbox/CONTEXT-REORG-PIPELINE-LATEST.html`（与 `docs/owner-stack-openwebui-mindmap.html` **同源**，由 `scripts/build-context-reorg-pipeline-html.py` 生成）。
- **分享给鸭哥请用 htmlpreview / GitHub 链接**，不要发 `file://`。

---

## 8. 克隆（代码也在 GitHub）

```bash
git clone https://github.com/dymusiques/guide-brand-agent.git
```

公开只读即可浏览；无需 Cursor 也能看 MD 与导图。
