---
context_version: "2026-10-30-l012"
repo_path: "docs/WORKFLOW-CEO-ARCHITECTURE.md"
goal: "Workflow · CEO 架构 · 分层与文件地图"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "7fa6afc9adb47412"
---

# Workflow · CEO 架构 · 分层与文件地图

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** ```bash
cd ~/Desktop/danying-brand-agent   # 或你的 clone 路径
bash scripts/ensure-venv-deps.sh
bash scripts/verify-agent-takeover.sh
bash scripts/manager-autopilot.sh
```
- **Path:** `docs/WORKFLOW-CEO-ARCHITECTURE.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`

## 章节锚点
- **L1 任务（压缩 · Open WebUI / Cursor 顶栏）**: - **Goal:** > **思维导图（须浏览器渲染，勿在 Cursor 里当代码打开）：** 终端 `bash scripts/open-workflow-mindmap.sh` → [workf…
- **章节锚点**: - **2. 是否有「总 CEO + 部门 Manager」？**: **有。**  metaphor 与实现如下：
- **新机一键（Agent Must）**: ```bash


---

## L2 正文

# Workflow · CEO 架构 · 分层与文件地图

> **思维导图（须浏览器渲染，勿在 Cursor 里当代码打开）：** 终端 `bash scripts/open-workflow-mindmap.sh` → [workflow-mindmap.html](./workflow-mindmap.html) · **Agent 生态：** [agent-ecosystem-map.html](./agent-ecosystem-map.html)（同上可 `python3 -m http.server 8765 --directory docs` 后开 `/agent-ecosystem-map.html`）  
> **是否凌乱（审计表）：** [SYSTEM-CLARITY-AUDIT.md](./SYSTEM-CLARITY-AUDIT.md)  
> **一键接手：** [AGENT-TAKEOVER.md](./AGENT-TAKEOVER.md) · [HANDOFF-MD-MANIFEST.md](./HANDOFF-MD-MANIFEST.md)


## 2. 是否有「总 CEO + 部门 Manager」？

**有。**  metaphor 与实现如下：

| 公司角色 | 本仓实现 | 汇总给 Owner 的界面 |
|----------|----------|---------------------|
| **CEO** | **00 Manager**（Cursor 规则自动激活） | `ceo-dispatch-latest.md` · `manager-dashboard-*.md` |
| **部门 Manager** | **01–09** 各 Agent（读 `INTEGRATION-PROMPT.md`） | 步内 PASS/FAIL + 产出路径 |
| **质检 / 合规** | 05 kernel · evaluate · verify-goals | `aligned: true` · `RESULT: PASS` |
| **董事会目标** | G-* · `integration/goals/registry.json` | `verify-goals.sh` |

**反馈闭环（CEO 看的三条线）：**

1. 终端 `RESULT: PASS/FAIL`（autopilot / verify）
2. `content/analytics/derived/manager-dashboard-*.md`
3. `content/analytics/derived/ceo-dispatch-latest.md`

Owner **审阅**定稿与发布；CEO **不**代替 Owner 点小红书发布。


## 一步骤 → 一文件（常用）

| 步骤 | 命令 / 动作 | 读/写文件 |
|------|-------------|-----------|
| 接手 | `danying-brand-agent` | [HANDOFF-MD-MANIFEST.md](./HANDOFF-MD-MANIFEST.md) |
| CEO 一键 | `bash scripts/manager-autopilot.sh` | derived/* · goals verify |
| 数据刷新 | analytics-fetch + pipeline | [XHS-DATA-LAYER.md](./XHS-DATA-LAYER.md) |
| 写 Brief | 04 模板 | `kernels/templates/xhs-content-brief.template.md` |
| 对齐 IP | evaluate | `scripts/evaluate-xhs-topic.py --brief …` |
| Manager 验收 | workflow verify | `scripts/manager-workflow-verify.sh content/xiaohongshu/….md` |
| 直发成稿 | Owner 复制 | `2026-10-20-publish-ready-queue.md` |
| 发帖后 | 回填 | Brief `## 发布状态` |

---

## 新机一键（Agent Must）

```bash
cd ~/Desktop/danying-brand-agent   # 或你的 clone 路径
bash scripts/ensure-venv-deps.sh
bash scripts/verify-agent-takeover.sh
bash scripts/manager-autopilot.sh
```

然后读：`docs/AGENT-TAKEOVER.md` → `ceo-dispatch-latest.md` → `docs/XHS-DATA-LAYER.md`（有小红书数据时）。