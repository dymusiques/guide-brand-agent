---
context_version: "2026-10-30-l012"
repo_path: "rules/skills/skill_asr.md"
goal: "Skill Router: ASR（本地转写）"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "9c4186083ddfbfe7"
---

# Skill Router: ASR（本地转写）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **边界：** 产出 **owner 复核** 的文稿 → `voice-anchor-transcripts-*.md` / `owner-source-*`；**不** 直接写进 Brief 定稿。  
> **anchor≥10：** 才建议批量历史口播 ASR（见 adoption §0）。
- **Path:** `rules/skills/skill_asr.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`


---

## L2 正文

# Skill Router: ASR（本地转写）

> **边界：** 产出 **owner 复核** 的文稿 → `voice-anchor-transcripts-*.md` / `owner-source-*`；**不** 直接写进 Brief 定稿。  
> **anchor≥10：** 才建议批量历史口播 ASR（见 adoption §0）。

1. **Root skill:** `vendor/asr-skill/skills/asr/SKILL.md`
2. **Adoption:** [ip-content-skills-adoption.md](../../integration/ip-content-skills-adoption.md)

触发词："转写"、"ASR"、"视频转文稿"。

```bash
source scripts/ensure-workspace-venv.sh
pip install -e vendor/asr-skill   # 首次 · macOS 26+ / MLX 见 vendor README
# 转写权重未装时 verify-ip-skills-env 会 WARN — 按需装 vendor 文档中的 MLX 依赖
```