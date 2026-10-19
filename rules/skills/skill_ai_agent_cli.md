# Skill Router: AI Agent CLI

> **唯一 discovery 入口。** 各 CLI 细则在 vendor 内按需加载，**不**单独占 INDEX 行。

## 激活顺序

1. **Overlay（Must 读本仓边界）:** [integration/ai-agent-cli-adoption.md](../../integration/ai-agent-cli-adoption.md)
2. **私有路径/模型/ scratch：** `rules/skills/overlays/ai-agent-cli.local.example.md` → `ai-agent-cli.local.md`（gitignored）
3. **Root skill:** `vendor/ai-agent-cli-skill/skills/skill_ai_agent_cli.md`
4. **Focused（按需）:** `vendor/ai-agent-cli-skill/skills/cursor_cli.md` · `antigravity_cli.md` · `claude_code.md` · 等

## When to Use

从 **脚本 / 父 Agent / CI** 非交互调用 **Claude Code、Codex、OpenCode、Antigravity (`agy`)、Grok、Cursor `cursor agent -p`**。触发词：headless agent、CLI 委派、`cursor agent -p`、file-response 契约、独立 fresh context review。

**本仓默认：** Owner 已在 **Cursor IDE** 内用 00 Manager → **不必**再套一层 `cursor agent -p`，除非 Owner 要 **并行隔离 turn、订阅配额、或自动化 pipeline**。

## Quick Check（Cursor CLI · 可选）

```bash
cursor agent --version
cursor agent about
# 首次 CLI 鉴权（与 IDE 分开）：cursor agent login
```

Scratch 与 prompt/result 路径见 overlay；**勿** commit prompt/result 含任务正文。
