# workflow-parallel-subagents · Local Overlay (example)

复制为 `workflow-parallel-subagents.local.md`（gitignored）。

| Key | Value |
|-----|-------|
| Parallel scratch root | `tmp/parallel/`（中间工件，**不** commit） |
| Session slug 约定 | `YYYY-MM-DD-<topic>` 例如 `2026-10-19-competitor-xhs` |
| 单 session 目录 | `tmp/parallel/<session_slug>/` |
| Canonical 定稿 | 仅 `content/<domain>/`  after evaluate / Owner 认可 |
| 独立 review | Bugbot 或 Task reviewer；产物可暂存 `tmp/parallel/<slug>/review.md` |

**禁止：** 多个并行 Task 直接写同一 `content/xiaohongshu/*-brief.md`。
