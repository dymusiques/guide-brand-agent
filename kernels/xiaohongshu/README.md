# Xiaohongshu Topic Manager · Gemini Kernel

Module 3 课纲线（docstring → line2 核心函数 → 6 case 验收）在本仓的小红书选题判定实现。

**Owner 角色：** 小红书 IP Manager — 选题是否对齐个人 IP、涨粉路径、强链接客群（非纯 vanity 流量）。

## 文件清单（Git 定稿，不依赖聊天记录）

| 路径 | 作用 |
|------|------|
| `learning2/docstring_shell.py` | Step 2：规则写在 docstring 的函数壳 |
| `line2/is_xhs_growth_aligned.py` | Step 3：核心实现 + Gemini yes/no → bool |
| `line2/tests/test_is_xhs_growth_aligned.py` | 6 个必过用例 + Terminal Summary |
| `examples/demo.py` | 单条 dict 试跑，JSON 输出 |
| `config/gemini_config.py` | 读 `Guide/0/.env` 的 Key / Model |
| `docs/01-workflow-step-order.md` | 你的步骤顺序是否与课纲一致（审阅结论） |
| `docs/02-gemini-and-functions.md` | Gemini 调用方式与 API 说明 |
| `docs/03-six-test-cases.md` | 六个测试用例说明（与 test 文件同源） |
| 仓库根 `scripts/verify-xhs-topic.sh` | 一键验收 |
| 仓库根 `.env.example` | Key 模板（`.env` gitignore） |
| 仓库根 `requirements-gemini.txt` | `google-genai` + `python-dotenv` |
| 仓库根 `check.md` | 交付前 verify 路由表 |

## 快速开始

```bash
cd /path/to/Guide/0
source .venv/bin/activate
pip install -r requirements-gemini.txt
cp .env.example .env   # 编辑 GEMINI_API_KEY、可选 GEMINI_MODEL
bash scripts/verify-xhs-topic.sh
.venv/bin/python kernels/xiaohongshu/examples/demo.py
```

## 数据形状（强制 dict）

- **输入：** `{"subject": str, "body": str}` — 标题 + 正文（含 hook / CTA）
- **核心函数返回：** `bool` — `is_xhs_growth_aligned(content)`
- **管线推荐返回：** `evaluate_xhs_growth_content(content)` → `subject`, `body`, `aligned`

分类规则全文在 `is_xhs_growth_aligned` 的 docstring；Gemini prompt 从同一 docstring 抽取，保证「文档 = 模型规则」。

## 与 Module 3 参考仓的关系

课纲参考 monorepo / `module3-2-2-gemini` 的 `demo.py` + 6 test 模式；本 kernel 业务规则替换为小红书 IP / 涨粉 / 强链接，技术模式相同。

## 下一步（未在本目录实现）

- `.cursor/skills/xiaohongshu/` 扩展为 **Topic Manager Skill**（选题 → Brief → 自动 verify）
- P 层指标（1700 → 5000 → 10000 粉丝）不进单元测试，单独跟踪
