# ai-agent-cli · Local Overlay (example)

复制为 `ai-agent-cli.local.md`（gitignored）。**勿** commit 含任务正文或 token 的 prompt/result。

| Key | Value |
|-----|-------|
| Workspace root | `~/Desktop/danying-brand-agent` |
| Headless scratch | `tmp/ai-agent-cli/<job_id>/` |
| Prompt file | `tmp/ai-agent-cli/<job_id>/prompt.md` |
| Result file | `tmp/ai-agent-cli/<job_id>/result.md`（或任务指定路径） |
| Logs | `stdout.json` / `stderr.log` / `stream.ndjson` 同目录 |
| 默认 Cursor 模型（headless） | 以 `cursor agent --list-models` 为准；caller 显式 `--model` |
| IDE vs CLI | IDE 会话 = 00 Manager；CLI 仅 Owner/脚本显式启用 |

## 包装脚本占位（将来 launcher 可调）

`scripts/` 下新增 `run-cursor-agent-job.sh` 时：读 overlay 路径、写 prompt、跑 `cursor agent -p "Read … prompt.md …"`、`--trust --workspace $ROOT`，验收 result 非空后再退出 0。

## 红线

- Brief 定稿仍走 `content/` + evaluate，**不**用 CLI stdout 代替 aligned。  
- prompt/result 含品牌未发布内容 → 仅本地 scratch，不进 Git。
