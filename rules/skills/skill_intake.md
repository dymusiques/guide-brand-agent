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
