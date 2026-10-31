---
context_version: "2026-10-30-l012"
repo_path: "docs/OWNER-GOOGLE-GRANT-AGENT.md"
goal: "Owner · Google 已全权授权 Agent（勿再 chat 确认）"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "6d35a8126d56c887"
---

# Owner · Google 已全权授权 Agent（勿再 chat 确认）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **Owner 口径（2026-10-28）：** Google 使用权 **已全部交给 Agent**；**不要**在对话里一遍遍问「要不要 Connect / 确认 OAuth / 授权 Drive」。
- **Path:** `docs/OWNER-GOOGLE-GRANT-AGENT.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`

## 章节锚点
- **Agent Must**: 1. **启动任何任务前**（可选快检）：`bash scripts/check-google-auth-for-agent.sh` → 读 `integration/handoff/google-a…
- **Owner 仅需（极少 · Terminal 一次）**: | 情况 | Owner 动作 |
- **凭证位置（gitignore · 已存在即视为已授权）**: - `vendor/gdocs-skill/secrets/credentials.json`
- **相关**: - [SETUP.md](../SETUP.md) §3–4 · [skill_google_docs.md](../rules/skills/skill_google_docs.md) · `int…


---

## L2 正文

# Owner · Google 已全权授权 Agent（勿再 chat 确认）

> **Owner 口径（2026-10-28）：** Google 使用权 **已全部交给 Agent**；**不要**在对话里一遍遍问「要不要 Connect / 确认 OAuth / 授权 Drive」。

## Agent Must

1. **启动任何任务前**（可选快检）：`bash scripts/check-google-auth-for-agent.sh` → 读 `integration/handoff/google-auth-status.json`。
2. **`verify_integration: PASS`** → **禁止**在 chat 请 Owner 确认 Google；**Must** 用 CLI：
   ```bash
   .venv/bin/python -m gdocs --secrets-dir vendor/gdocs-skill/secrets …
   ```
3. **Cursor MCP**（Drive/Gmail/Calendar 插件）与 CLI **是两条路**；MCP 显示 `needsAuth` 时 → **改用 CLI**，**不要**把 MCP Connect 卡片转给 Owner（除非 CLI 也 FAIL 且 token 失效）。
4. **Campaign / verify-goals：** 集成 PASS 时脚本 **自动** `VERIFY_GOALS_SKIP_PLATFORM=0`（见 `run-ceo-ip-all-agents-campaign.sh`）；FAIL 时自动 SKIP，**仍不** chat 追问。

## Owner 仅需（极少 · Terminal 一次）

| 情况 | Owner 动作 |
|------|------------|
| 换机 / token 删了 | 恢复 `credentials.json` + `token.json` 或 `python -m gdocs … create` 浏览器授权 **一次** |
| CLI 与 verify-integration 均 FAIL | 同上 · **不在 Cursor chat 里反复确认** |

## 凭证位置（gitignore · 已存在即视为已授权）

- `vendor/gdocs-skill/secrets/credentials.json`
- `vendor/gdocs-skill/secrets/token.json`

## 相关

- [SETUP.md](../SETUP.md) §3–4 · [skill_google_docs.md](../rules/skills/skill_google_docs.md) · `integration/handoff/google-auth-manifest.json`