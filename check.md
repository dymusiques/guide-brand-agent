# check · 指针

做完自己复查 — **canonical 总则**在 hub：

**[danying-apps/rules/check/check.md](https://github.com/dymusiques/danying-apps/blob/main/rules/check/check.md)**

**全仓 verify 形态对照**（审计前先读，避免在本仓找 Module 3 课纲 test）：

**[danying-apps/rules/check/VERIFY-MAP.md](https://github.com/dymusiques/danying-apps/blob/main/rules/check/VERIFY-MAP.md)**

---

## 本仓验收范围

| 类型 | 命令 / 动作 | 说明 |
|------|-------------|------|
| **接手完整性** | `scripts/verify-handoff.sh` | Git 骨架、IP Brief、OAuth 文件等是否存在 → PASS/WARN/FAIL |
| **Drive 读写** | 写入后 `read_file` 读回 | 手工 smoke；**未**自动化断言（见下「不含」） |
| **gdocs CLI** | 检查 exit code 与 JSON stdout | 报错路径见 `SETUP.md` |

**本仓不含**（请按 VERIFY-MAP 去对应仓）：

- Module 3 课纲 **`is_genai_email` + 6 Python test** → [`module3-2-2-gemini`](https://github.com/dymusiques/module3-2-2-gemini) · Playbook §5  
- Bookmarklet 六条浏览器手测 → `danying-agent-workspace` / `bookmarklet-search-switcher`  
- 听见 Daily 栏目 verify → `danying-tingjian-daily` · `verify_daily_issue.py`

---

## 交付前（Agent）

1. 跑 `scripts/verify-handoff.sh`  
2. 若动过 Drive/gdocs：按上表做读回 / exit code 检查  
3. 总则：模拟 Owner 终端、查到不对先修再报 → hub `check.md`
