# check · 验收

做完自己复查 — **canonical 总则**在 hub：

**[danying-apps/rules/check/check.md](https://github.com/dymusiques/danying-apps/blob/main/rules/check/check.md)**

**各仓 verify 形态对照**（防查错仓 · Module 3 的 6 test 不在本仓）：

**[danying-apps/rules/check/VERIFY-MAP.md](https://github.com/dymusiques/danying-apps/blob/main/rules/check/VERIFY-MAP.md)**

---

## 本仓 verify（两层）

| 层级 | 脚本 | 检查什么 | 终端 |
|------|------|----------|------|
| **接手** | `bash scripts/verify-handoff.sh` | Git 骨架、IP Brief、OAuth 文件是否存在 | PASS / WARN / FAIL |
| **集成** | `bash scripts/verify-integration.sh` | 6 case：gdocs 读/错 JSON、Git 读、Drive 搜 | PASS / SKIP / FAIL |

### 集成 6 case（`scripts/verify_integration.py`）

1. `import gdocs`
2. OAuth secrets 存在（缺则 3–4–6 **SKIP**，不阻塞接手）
3. **读路径** — `gmail profile` → exit 0 + JSON stdout
4. **错路径** — 无效 Drive id → exit 1 + JSON stderr
5. **Git 读** — `content/personal-ip/` 与 `USER.md` 事实一致
6. **Drive 读** — Knowledge Bank 根文件夹 search 有结果

### 小红书 Topic Manager（6 case · Gemini · Module 3 课纲线）

| 层级 | 脚本 | 检查什么 |
|------|------|----------|
| **核心 + 6 test** | `bash scripts/verify-xhs-topic.sh` | `is_xhs_growth_aligned` · IP/涨粉/强链接 · 读 `Guide/0/.env` |

Key：`cp .env.example .env` → 填 `GEMINI_API_KEY`（不进 git）。Python 启动时 `load_dotenv()` 读取。  
说明文档：[kernels/xiaohongshu/README.md](kernels/xiaohongshu/README.md)（含步骤审阅、Gemini/API、6 case 表）。  
Topic Manager Skill：`.cursor/skills/xiaohongshu/topic-manager.md` · 单条选题 `python scripts/evaluate-xhs-topic.py --brief …`

### 本仓不含（见 VERIFY-MAP）

- Module 3 课纲 **`is_genai_email` + 6 Python test** → [`module3-2-2-gemini`](https://github.com/dymusiques/module3-2-2-gemini)
- Bookmarklet 六条浏览器手测 → `danying-agent-workspace` / `bookmarklet-search-switcher`
- 听见 Daily 每期 verify → `danying-tingjian-daily` · `verify_daily_issue.py`

---

## Agent 交付前（Owner 不必记）

1. 先跑 `bash scripts/verify-handoff.sh`
2. 再跑 `bash scripts/verify-integration.sh`（有 OAuth 时应 6/6 PASS）
3. 可选 Owner 要求：Drive 写入后 MCP `read_file` 读回（不占必须；Git 已定稿即可）

需代理访问 Google 时：`export HTTPS_PROXY=…` 后再跑集成脚本。
