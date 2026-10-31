---
context_version: "2026-10-30-l012"
repo_path: "rules/skills/skill_voice_lora.md"
goal: "Skill Router: voice-lora（detect / rewrite）"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "819da7d5233983e0"
---

# Skill Router: voice-lora（detect / rewrite）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **边界：** **detect** → 外稿、B 站简介、Owner 说明；**rewrite** → 仅 Owner 点名润色且 **非** XHS Brief/evaluate。  
> **小红书 Brief** → L2 `verify-xhs-voice-qa.sh` + Owner 选稿。
- **Path:** `rules/skills/skill_voice_lora.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`


---

## L2 正文

# Skill Router: voice-lora（detect / rewrite）

> **边界：** **detect** → 外稿、B 站简介、Owner 说明；**rewrite** → 仅 Owner 点名润色且 **非** XHS Brief/evaluate。  
> **小红书 Brief** → L2 `verify-xhs-voice-qa.sh` + Owner 选稿。

1. **Root detect:** `vendor/voice-lora/skills/voice-lora-detect/SKILL.md`
2. **Root rewrite（按需）:** `vendor/voice-lora/skills/voice-lora-rewrite/SKILL.md`
3. **Adoption:** [ip-content-skills-adoption.md](../../integration/ip-content-skills-adoption.md)

触发词："AI 味检测"、"voice-lora"、"去 AI 腔"（Brief 仍禁 rewrite）。

```bash
source scripts/ensure-workspace-venv.sh
voice-lora score path/to.md --paragraphs 3
```