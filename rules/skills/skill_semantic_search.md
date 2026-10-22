# Skill Router: Semantic Search（本地 embedding）

> **边界：** 检索 **本仓** anchor / transcripts / packages；**不**替代 04 Brief 写稿。  
> **何时用：** [ip-content-skills-adoption.md](../../integration/ip-content-skills-adoption.md) §1（anchor≥10 建索引；此前可手工读 transcripts）。

1. **Overlay（可选）：** `rules/skills/overlays/semantic-search.local.example.md`
2. **Root skill:** `vendor/semantic-search-skill/skills/skill_semantic_search.md`
3. **Adoption:** [ip-content-skills-adoption.md](../../integration/ip-content-skills-adoption.md)

触发词："语义检索"、"找类似原话"、"search my transcripts"。

```bash
source .venv/bin/activate
pip install -e vendor/semantic-search-skill   # 首次 · 见 vendor README
```
