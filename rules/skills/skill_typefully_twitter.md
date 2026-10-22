# Skill Router: Typefully / X

> **边界：** 英文/X 排期；小红书仍走 xiaohongshu skill。

1. **Overlay:** `rules/skills/overlays/typefully-twitter.local.example.md`（待建则 copy 自 vendor .env.example）
2. **Root skill:** `vendor/typefully-twitter-skill/skills/skill_typefully_twitter.md`
3. **Adoption:** [ip-content-skills-adoption.md](../../integration/ip-content-skills-adoption.md)

触发词："Typefully"、"发 X"、"Twitter 排期"。

```bash
pip install -e vendor/typefully-twitter-skill   # 首次 · token 进 overlay/.env
```
