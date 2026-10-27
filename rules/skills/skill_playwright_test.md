# Skill Router: Playwright Test（CDP 调试）

> **边界：** 调试 bilibili / XHS Playwright 步骤；非内容写作。

1. **Root skill:** `vendor/playwright-test-skill/skills/skill_playwright_test.md`
2. **Adoption:** [ip-content-skills-adoption.md](../../integration/ip-content-skills-adoption.md)

触发词："playwright 调试"、"CDP step"。

**用法（本仓）：** 不要用 `pw-test --help`（会尝试连 CDP）。无参数运行 `pw-test` 或在 adoption §5 查 USAGE。先起 Chrome CDP，见 vendor skill。

```bash
source scripts/ensure-workspace-venv.sh
pip install -e vendor/playwright-test-skill   # 首次
# pw-test goto https://…   # 需 CDP 已监听
```
