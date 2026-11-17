# Medium · 发帖数据 intake（轻量）

同 LinkedIn 分轨。模板：`inbox/TEMPLATE-post-metrics.md`

```bash
python3 scripts/ingest-owner-medium-metrics.py --file content/analytics/medium/inbox/<file>
```

产出：`content/analytics/medium/posts.jsonl` · `integration/handoff/owner-medium-metrics-latest.json`