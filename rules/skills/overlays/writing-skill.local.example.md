---
context_version: "2026-10-30-l012"
repo_path: "rules/skills/overlays/writing-skill.local.example.md"
goal: "writing-skill · Local Overlay (example)"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "f8376d707603c3f9"
---

# writing-skill · Local Overlay (example)

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** Copy to `writing-skill.local.md` (gitignored) if you add private paths or channel defaults.
- **Path:** `rules/skills/overlays/writing-skill.local.example.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`

## 章节锚点
- **Policy (this workspace · 1-A)**: | 任务 | 路由 |
- **Paths**: | Key | Value |


---

## L2 正文

# writing-skill · Local Overlay (example)

Copy to `writing-skill.local.md` (gitignored) if you add private paths or channel defaults.

## Policy (this workspace · 1-A)

| 任务 | 路由 |
|------|------|
| 小红书 `*-brief.md` | **禁止** external writing 全流程覆盖；04 + PIPELINE + evaluate |
| 听见 Daily 长文/专栏 | 可用 external workflow + **temporal** skill |
| 内部 memo / 合作 brief Word 前草稿 | internal workflow |

## Paths

| Key | Value |
|-----|-------|
| Vendored repo | `vendor/writing-skill/` |
| Root skill | `vendor/writing-skill/skills/writing_workflows.md` |