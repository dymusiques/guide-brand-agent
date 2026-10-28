# 11 · IP Daily Evaluator GM · 日更 Sub-Agent

> **汇报：** 00 CEO · **套件：** [../_shared/SUBAGENT-DAILY-KIT.md](../_shared/SUBAGENT-DAILY-KIT.md)

## Must（每日）

1. **Baseline：** North Star / IP gold
2. **Intake：** `evolution-rollups-latest.md` + Brief  hygiene
3. **Challenge：** 每日 2 条 X 坑（FULL-DRILL X1–X12）+ 检查 `content/xiaohongshu/challenge/*-challenge.md` 是否齐全（缺则 CEO 链应已跑 `run-xhs-brief-adversarial-challenge.py --all`）
4. **Evaluator：** 缺 redteam-pre / 缺 challenge · `metrics.jsonl` · 见 [BRIEF-ADVERSARIAL-CHALLENGE.md](../_shared/BRIEF-ADVERSARIAL-CHALLENGE.md)
5. **Self-check：** `verify-collector-evaluator.sh`

```bash
python scripts/daily-gm-11-ip-evaluator.py
```

**路径：** `content/evolution/11-ip-daily-eval/<YYYY-MM-DD>/`
