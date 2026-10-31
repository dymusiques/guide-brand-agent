---
context_version: "2026-10-30-l012"
repo_path: "docs/CEO-XHS-NEW-BRIEF-AUTOPILOT.md"
goal: "Owner 给新小红书主题 · 全自动（Must · 2026-10-30）"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "6691f00403dcb3f2"
---

# Owner 给新小红书主题 · 全自动（Must · 2026-10-30）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **不必逐步说「跑 evaluate / autopilot」。** Owner 在 chat 给出主题（如《…》）→ Agent **Must 自动**完成下列步骤并 **`run_ceo_xhs_autopilot.py`**。
- **Path:** `docs/CEO-XHS-NEW-BRIEF-AUTOPILOT.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`

## 章节锚点
- **Agent Must（单会话）**: 1. **Intake** → `content/evolution/04-xhs-topic-manager/<slug>/intake/`（Owner 原话）
- **Cursor 规则**: 见 `.cursor/rules/danying-manager-auto.mdc` · Owner 新小红书主题 = 触发本 SOP。
- **不是测试稿时**: 默认 **不** `--round2` campaign；仅 `*-test-brief.md` READY 后自动 round2（见 CEO-WORKFLOW-TEST-SOP）。
- **Owner 要不要每次说「跑 autopilot」？**: **不用。** 在 Cursor 里只要 Owner 给了新篇主题/目标任务，Agent 按本 SOP **Must 自跑**；没有 Owner 任务时不跑后台 daemon。


---

## L2 正文

# Owner 给新小红书主题 · 全自动（Must · 2026-10-30）

> **不必逐步说「跑 evaluate / autopilot」。** Owner 在 chat 给出主题（如《…》）→ Agent **Must 自动**完成下列步骤并 **`run_ceo_xhs_autopilot.py`**。

## Agent Must（单会话）

1. **Intake** → `content/evolution/04-xhs-topic-manager/<slug>/intake/`（Owner 原话）  
2. **Pitfalls** → `content/xiaohongshu/research/<slug>-pitfalls.md`（WebSearch ≥3）  
3. **Redteam pre** → `redteam/<slug>-pre.md`  
4. **Brief** → `content/xiaohongshu/<date>-<slug>-brief.md` + classifier（三镜头 · 系列案例轴）  
5. **Gold-body（可选）** → `reference/gold-body.md`  
6. **长稿 Must：** [OWNER-LONGFORM-XHS-SPEC.md](../content/xiaohongshu/OWNER-LONGFORM-XHS-SPEC.md)（3000–5000 字 · 检索引用 · 风格固定）

7. **一条命令（CEO 全量 · 默认不连带 Discovery 01–04）：**

```bash
bash scripts/ceo-full-execution-pipeline.sh --goal "<Owner 主题原话>" --brief content/xiaohongshu/<file>-brief.md --no-discovery-auto
# 仅 autopilot 子链：
bash scripts/ceo-new-xhs-brief-pipeline.sh --brief content/xiaohongshu/<file>-brief.md
```

8. **NEEDS_WORK (42)** → 同会话改 Brief/长稿 → 再跑 7，**勿问 Owner**  
9. **派活记录：** READY · HTML verify PASS · 路径  
10. **Owner 必看到 HTML：** `#owner-latest` 自动弹出 **长稿全文**；Must `open-owner-xhs-deliverable-html.sh`

## Cursor 规则

见 `.cursor/rules/danying-manager-auto.mdc` · Owner 新小红书主题 = 触发本 SOP。

## 不是测试稿时

默认 **不** `--round2` campaign；仅 `*-test-brief.md` READY 后自动 round2（见 CEO-WORKFLOW-TEST-SOP）。

## Owner 要不要每次说「跑 autopilot」？

**不用。** 在 Cursor 里只要 Owner 给了新篇主题/目标任务，Agent 按本 SOP **Must 自跑**；没有 Owner 任务时不跑后台 daemon。