# Skill Router: ASR（本地转写）

> **边界：** 产出 **owner 复核** 的文稿 → `voice-anchor-transcripts-*.md` / `owner-source-*`；**不** 直接写进 Brief 定稿。  
> **anchor≥10：** 才建议批量历史口播 ASR（见 adoption §0）。

1. **Root skill:** `vendor/asr-skill/skills/asr/SKILL.md`
2. **Adoption:** [ip-content-skills-adoption.md](../../integration/ip-content-skills-adoption.md)

触发词："转写"、"ASR"、"视频转文稿"。

```bash
pip install -e vendor/asr-skill   # 首次 · macOS 26+ / MLX 见 vendor README
```
