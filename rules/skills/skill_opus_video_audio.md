---
context_version: "2026-10-30-l012"
repo_path: "rules/skills/skill_opus_video_audio.md"
goal: "Skill Router: opus-video-audio（代码渲染 · 包装）"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "5760d368fdc61643"
---

# Skill Router: opus-video-audio（代码渲染 · 包装）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **边界：** B-roll / 片头 / 动效；**不**写小红书 Round1 口播。
- **Path:** `rules/skills/skill_opus_video_audio.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`


---

## L2 正文

# Skill Router: opus-video-audio（代码渲染 · 包装）

> **边界：** B-roll / 片头 / 动效；**不**写小红书 Round1 口播。

1. **Root skill:** `vendor/opus-video-audio-skill/skills/procedural-video-frames/SKILL.md`
2. **Adoption:** [ip-content-skills-adoption.md](../../integration/ip-content-skills-adoption.md)

触发词："opus 视频"、"procedural video"、"片头包装"。

**无 pip 包** — 不查 `.venv/bin`；触发时读 vendor skill + 按文档跑 `vendor/opus-video-audio-skill/scripts/`。