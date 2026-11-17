# Owner 硬触发 · 派活给 CEO（满链）

## 口令（任一说即触发）

`派活给 CEO` · `派活给CEO` · `派活 CEO`（与 `owner-orchestration-overrides.json` 同步）

## 行为（Agent Must · 非闲聊）

1. **编排**：强制 `copy_ceo_full`（C 档），禁止默认 `replay_only`。
2. **门禁**：`python3 scripts/agent-owner-research-gate.py --goal "<Owner 当句原话>"`（含 QC；交付不重 `--skip-qc-task`）。
3. **Gemini**：`SKIP_GEMINI=0`；若 deep-delivery 持锁 → **等待或 recover 后重跑**，不得对本轮任务静默 `SKIP_GEMINI=1`。
4. **CEO**：`run_ceo_full_execution.py --skip-research-gate`（gate 已 PASS）+ 有 Brief 则 `--brief` + `manager-ceo-auto-gate-loop`。
5. **Open WebUI**：仅当 goal 含长稿/RAG 词（长纲、Pipe、OpenRouter）时跑 router；监督短 task 仍可 SKIP router（不等于 skip verify）。
6. **仍人工**：各平台点发送。

## 与「随便聊」分界

| Owner 说法 | 行为 |
|----------|------|
| 派活给 CEO + goal | 上表满链 |
| 先讨论 / 只聊 / 不要结论 | gate 可弱化或不跑（见 discuss_only） |
| 问架构、Thank you | 不跑 CEO |

真源：`integration/handoff/owner-owner-triggers.json`