---
context_version: "2026-10-30-l012"
repo_path: "rules/skills/skill_voice_memos.md"
goal: "Skill Router: Apple Voice Memos（只读导出）"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "ce303a48ab53838d"
---

# Skill Router: Apple Voice Memos（只读导出）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **边界：** 导出 **m4a** → intake / ASR → `owner-source-*`；不替代小红书 App 录制。
- **Path:** `rules/skills/skill_voice_memos.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`


---

## L2 正文

# Skill Router: Apple Voice Memos（只读导出）

> **边界：** 导出 **m4a** → intake / ASR → `owner-source-*`；不替代小红书 App 录制。

1. **Root skill:** `vendor/voice-memos-skill/skills/voice-memos/SKILL.md`
2. **Adoption:** [ip-content-skills-adoption.md](../../integration/ip-content-skills-adoption.md)

触发词："语音备忘录"、"Voice Memos export"。

```bash
pip install -e vendor/voice-memos-skill   # 首次
```