---
context_version: "2026-10-30-l012"
repo_path: "agents/11-ip-daily-evaluator/INTEGRATION-PROMPT.md"
goal: "11 · IP Daily Evaluator GM · 日更 Sub-Agent"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "463d79c48297b940"
---

# 11 · IP Daily Evaluator GM · 日更 Sub-Agent

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **上下文与平台（Must · 全部门通用）**  
> - 标准：[docs/PROMPT-CONTEXT-STANDARD.md](../../docs/PROMPT-CONTEXT-STANDARD.md)  
> - Cursor ↔ Open WebUI：[docs/COURSE-METHOD-TO-YOUR-STACK.md](../../d
- **Path:** `agents/11-ip-daily-evaluator/INTEGRATION-PROMPT.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`

## 章节锚点
- **Must（每日）**: 1. **Baseline：** North Star / IP gold


---

## L2 正文

> **上下文与平台（Must · 全部门通用）**  
> - 标准：[docs/PROMPT-CONTEXT-STANDARD.md](../../docs/PROMPT-CONTEXT-STANDARD.md)  
> - Cursor ↔ Open WebUI：[docs/COURSE-METHOD-TO-YOUR-STACK.md](../../docs/COURSE-METHOD-TO-YOUR-STACK.md) · JSON [integration/handoff/cursor-openwebui-task-routing.json](../../integration/handoff/cursor-openwebui-task-routing.json)  
> - **长文/翻译** → Open WebUI Router + intake；**gate/verify/改 Brief** → Cursor only  
> - 本文件下方内容 = **本部门专属**；勿重复粘贴 SOUL / 整份 IP Brief 正文
# 11 · IP Daily Evaluator GM · 日更 Sub-Agent

> **汇报：** 00 CEO · **套件：** [../_shared/SUBAGENT-DAILY-KIT.md](../_shared/SUBAGENT-DAILY-KIT.md)

## Must（每日）

1. **Baseline：** North Star / IP gold
2. **Intake：** `evolution-rollups-latest.md` + Brief  hygiene
3. **Challenge：** 每日 2 条 X 坑（FULL-DRILL X1–X12）+ 检查 `content/xiaohongshu/challenge/*-challenge.md` 是否齐全（缺则 CEO 链应已跑 `run-xhs-brief-adversarial-challenge.py --all`）
4. **Evaluator：** 缺 redteam-pre / 缺 challenge · `metrics.jsonl` · 见 [BRIEF-ADVERSARIAL-CHALLENGE.md](../_shared/BRIEF-ADVERSARIAL-CHALLENGE.md)
5. **Self-check：** `verify-collector-evaluator.sh`

```bash
python scripts/daily-gm-11-ip-evaluator.py
```

**路径：** `content/evolution/11-ip-daily-eval/<YYYY-MM-DD>/`