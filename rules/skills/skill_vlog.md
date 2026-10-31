---
context_version: "2026-10-30-l012"
repo_path: "rules/skills/skill_vlog.md"
goal: "Skill Router: vlog（HeyGen · 地图字幕）"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "aaa5a3cf9b67aeb9"
---

# Skill Router: vlog（HeyGen · 地图字幕）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **边界：** 重讲解片、人在回路；**不**替代手机/Insta360 真人一条过。见 [bilibili-inst360-channel-adoption.md](../../integration/bilibili-inst360-channel-adoption.md)。
- **Path:** `rules/skills/skill_vlog.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`


---

## L2 正文

# Skill Router: vlog（HeyGen · 地图字幕）

> **边界：** 重讲解片、人在回路；**不**替代手机/Insta360 真人一条过。见 [bilibili-inst360-channel-adoption.md](../../integration/bilibili-inst360-channel-adoption.md)。

1. **Root skill:** `vendor/vlog-skill/skills/vlog/SKILL.md`
2. **Adoption:** [ip-content-skills-adoption.md](../../integration/ip-content-skills-adoption.md)

触发词："vlog skill"、"HeyGen 讲解片"、"论证地图字幕"。

```bash
pip install -e vendor/vlog-skill   # 首次 · HeyGen 等见 vendor README
```