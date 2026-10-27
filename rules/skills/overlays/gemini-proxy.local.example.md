# Gemini 代理 overlay（复制为 gemini-proxy.local.md · gitignore）

在 `.env` 增加一行（推荐）：

```bash
GEMINI_HTTP_PROXY=http://127.0.0.1:3213
```

或在本文件同目录创建 `gemini-proxy.local.md` 仅作备忘；**生效以 `.env` / `.local-config.json` 的 `gemini_http_proxy` 为准。

验证：

```bash
bash scripts/verify-xhs-topic.sh
```
