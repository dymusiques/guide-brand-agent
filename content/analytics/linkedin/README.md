# LinkedIn · 发帖数据 intake（轻量）

**不**与小红书 `notes.csv` 合并。真源：`integration/handoff/owner-multichannel-post-flywheel.json`

## Owner

1. 发帖后 **48–72h 或随周节奏** 填 `inbox/TEMPLATE-post-metrics.md` 副本，或导出 CSV/JSON 丢进 `inbox/`。
2. chat 说「LinkedIn 数据」并附文件即可 · **不必**记 ingest 命令。

## Agent

```bash
python3 scripts/ingest-owner-linkedin-metrics.py --file content/analytics/linkedin/inbox/<file>
```

产出：

- `content/analytics/linkedin/posts.jsonl`（追加）
- `integration/handoff/owner-linkedin-metrics-latest.json`