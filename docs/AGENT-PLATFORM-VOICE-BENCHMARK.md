# 三平台大V笔触对标（Must）

> 写小红书口播 / LinkedIn / Medium **之前**，Agent Must 跑 `agent-platform-voice-benchmark.py` 并读 handoff。

## 命令

```bash
python3 scripts/agent-platform-voice-benchmark.py --goal "<选题或 Owner 原话>"
```

handoff：`integration/handoff/owner-platform-voice-benchmark-latest.json`  
roster：`integration/handoff/platform-voice-benchmark-roster.json`

## 与现有层区别

| 层 | 做什么 |
|----|--------|
| `agent-benchmark-cross-dimensions` | 艺术家 watchlist · screened.md |
| **`agent-platform-voice-benchmark`** | **小红书/LinkedIn/Medium 高互动写作者笔触** |
| `owner-copy-v-tier` | 40万级 attestation · Owner 终检 |

## 自动化

已编入 `agent-owner-research-gate.py` 层 `platform_voice_benchmark`（深度调研/写稿类 goal）。