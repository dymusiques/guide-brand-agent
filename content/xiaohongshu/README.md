# 小红书 Brief（Git 真相源）

Topic Manager 产出目录。命名建议：

`YYYY-MM-DD-<slug>-brief.md`

每个 Brief 须含 `<!-- xhs-classifier -->` JSON 块（见 `kernels/templates/xhs-content-brief.template.md`）。

验收：

```bash
python scripts/evaluate-xhs-topic.py --brief content/xiaohongshu/<file>.md
bash scripts/verify-xhs-topic.sh   # kernel 改动的交班前
```

Skill：`.cursor/skills/xiaohongshu/topic-manager.md`
