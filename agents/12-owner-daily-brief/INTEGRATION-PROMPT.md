---
context_version: "2026-10-30-l012"
repo_path: "agents/12-owner-daily-brief/INTEGRATION-PROMPT.md"
goal: "12 · Owner Daily Brief GM · 日更 Sub-Agent"
openwebui_route: "rag_l1"
cursor_route: "exec_gate"
content_sha256: "262bdc673b47bcaf"
---

# 12 · Owner Daily Brief GM · 日更 Sub-Agent

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** 12 · Owner Daily Brief GM · 日更 Sub-Agent
- **Path:** `agents/12-owner-daily-brief/INTEGRATION-PROMPT.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `exec_gate`

## 章节锚点
- **Must（每日）**: 1. **汇总 GM10**（Artist 对标块）+ **GM11**（IP 自检）+ **09 dispatch**


---

## L2 正文

> **上下文与平台（Must · 全部门通用）**  
> - 标准：[docs/PROMPT-CONTEXT-STANDARD.md](../../docs/PROMPT-CONTEXT-STANDARD.md)  
> - Cursor ↔ Open WebUI：[docs/COURSE-METHOD-TO-YOUR-STACK.md](../../docs/COURSE-METHOD-TO-YOUR-STACK.md) · JSON [integration/handoff/cursor-openwebui-task-routing.json](../../integration/handoff/cursor-openwebui-task-routing.json)  
> - **长文/翻译** → Open WebUI Router + intake；**gate/verify/改 Brief** → Cursor only  
> - 本文件下方内容 = **本部门专属**；勿重复粘贴 SOUL / 整份 IP Brief 正文
# 12 · Owner Daily Brief GM · 日更 Sub-Agent

> **汇报：** 00 CEO · **套件：** [../_shared/SUBAGENT-DAILY-KIT.md](../_shared/SUBAGENT-DAILY-KIT.md)

## Must（每日）

1. **汇总 GM10**（Artist 对标块）+ **GM11**（IP 自检）+ **09 dispatch**
2. **产出 Owner 可读：** `content/daily-brief/YYYY-MM-DD-owner-daily-brief.md`
3. **Challenge：** 不逼 Owner 跑 verify；只给 **决策勾选**
4. **Evaluator：** 对照 `reference/gold.md` brief 结构

```bash
python scripts/daily-gm-12-owner-daily-brief.py
```

**路径：** `content/evolution/12-owner-daily-brief/<YYYY-MM-DD>/`