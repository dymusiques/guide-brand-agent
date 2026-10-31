---
context_version: "2026-10-30-l012"
repo_path: "rules/skills/skill_online_media.md"
goal: "Skill Router: Online Media（下载 · 转写 · 字幕）"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "ff31956ee3949fbd"
---

# Skill Router: Online Media（下载 · 转写 · 字幕）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **边界：** 外链媒体 / 听见类 **非 XHS Brief**；Agent 纠错断句，CLI 做 coverage/validate。
- **Path:** `rules/skills/skill_online_media.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`


---

## L2 正文

# Skill Router: Online Media（下载 · 转写 · 字幕）

> **边界：** 外链媒体 / 听见类 **非 XHS Brief**；Agent 纠错断句，CLI 做 coverage/validate。

1. **Root skill:** `vendor/online-media-skill/skills/online_media.md`
2. **Adoption:** [ip-content-skills-adoption.md](../../integration/ip-content-skills-adoption.md)

触发词："下载转写"、"双语字幕"、"medley 识曲"。

```bash
pip install -e vendor/online-media-skill   # 首次
```