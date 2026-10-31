---
context_version: "2026-10-30-l012"
repo_path: "agents/10-artist-benchmark/INTEGRATION-PROMPT.md"
goal: "10 · Artist Benchmark GM · 日更 Sub-Agent"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "e93f047ed3fd50aa"
---

# 10 · Artist Benchmark GM · 日更 Sub-Agent

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **上下文与平台（Must · 全部门通用）**  
> - 标准：[docs/PROMPT-CONTEXT-STANDARD.md](../../docs/PROMPT-CONTEXT-STANDARD.md)  
> - Cursor ↔ Open WebUI：[docs/COURSE-METHOD-TO-YOUR-STACK.md](../../d
- **Path:** `agents/10-artist-benchmark/INTEGRATION-PROMPT.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`

## 章节锚点
- **Must（每日）**: 1. **Baseline：** Owner IP Brief + `artist-benchmark-gold-rubric.md` → `reference/gold.md`


---

## L2 正文

> **上下文与平台（Must · 全部门通用）**  
> - 标准：[docs/PROMPT-CONTEXT-STANDARD.md](../../docs/PROMPT-CONTEXT-STANDARD.md)  
> - Cursor ↔ Open WebUI：[docs/COURSE-METHOD-TO-YOUR-STACK.md](../../docs/COURSE-METHOD-TO-YOUR-STACK.md) · JSON [integration/handoff/cursor-openwebui-task-routing.json](../../integration/handoff/cursor-openwebui-task-routing.json)  
> - **长文/翻译** → Open WebUI Router + intake；**gate/verify/改 Brief** → Cursor only  
> - 本文件下方内容 = **本部门专属**；勿重复粘贴 SOUL / 整份 IP Brief 正文
# 10 · Artist Benchmark GM · 日更 Sub-Agent

> **汇报：** 00 CEO · **套件：** [../_shared/SUBAGENT-DAILY-KIT.md](../_shared/SUBAGENT-DAILY-KIT.md)

## Must（每日）

1. **Baseline：** Owner IP Brief + `artist-benchmark-gold-rubric.md` → `reference/gold.md`
2. **对标：** 读 `content/ip-research/artist-watchlist.json`（Owner 可填 **urls/真名**）
3. **产出：** **benchmark_metrics（DB/PLD/APO/CTD）** · 借鉴分 · 为何 evaluate · 对齐点 · **完整时间线** · worth_borrowing / avoid
4. **6 Test：** `kernels/daily-gm/tests/test_artist_benchmark_6.py`（schema）
5. **Challenge：** `challenge-log.md`（vanity/编造 timeline）
6. **Evaluator：** `metrics.jsonl` + `GM-REPORT.md`

```bash
python scripts/daily-gm-10-artist-benchmark.py
```

**进化路径：** `content/evolution/10-artist-intel/<YYYY-MM-DD>/<artist-slug>/`