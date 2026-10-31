---
context_version: "2026-10-30-l012"
repo_path: "rules/skills/skill_intake.md"
goal: "Skill Router: Intake（口述 → 结构化）"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "f3147a365911295f"
---

# Skill Router: Intake（口述 → 结构化）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **边界：** 新故事落盘 `content/xiaohongshu/owner-source-*.md`；之后仍走 04 Brief + 2a 迭代。
- **Path:** `rules/skills/skill_intake.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`


---

## L2 正文

# Skill Router: Intake（口述 → 结构化）

> **边界：** 新故事落盘 `content/xiaohongshu/owner-source-*.md`；之后仍走 04 Brief + 2a 迭代。

1. **Root skill:** `vendor/intake-skill/skills/skill_intake.md`
2. **Adoption:** [ip-content-skills-adoption.md](../../integration/ip-content-skills-adoption.md)

触发词："intake"、"口述归档"、"收故事"。

```bash
source scripts/ensure-workspace-venv.sh
intake-skill doctor
# 转写: pip install -e 'vendor/intake-skill[qwen-asr]' 后再 intake-skill asr …
```