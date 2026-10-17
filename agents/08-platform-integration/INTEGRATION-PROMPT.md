# 08 Platform Integration · 集成

**成功目标：** `G-PLATFORM-SYNC`

1. gdocs / Drive / Gmail / Calendar：`rules/skills/skill_google_docs.md` + overlay。
2. **函数壳：** `bash scripts/agent-shells/08-platform.sh`（= `verify-integration.sh` 6 case）。
3. **验收：** `bash scripts/verify-agent-matrix.sh --agent 08` + 全仓 `verify-all.sh` 平台段。
4. **禁止** 未 Git commit 定稿仅 sync Drive（见 IMPORTANT）。
