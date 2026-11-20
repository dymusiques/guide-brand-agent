# Automation 交付标准 · HTML + Google Chrome + 出处

**Owner 定稿 · 2026-11-19**

所有 Cursor **本地（This Computer）** Automation 在跑完后 Must：

1. 写入 **结构化 JSON**（见下）  
2. 写入或更新 **Markdown 真源**（若该 Automation 已有 md 路径则沿用）  
3. 运行 `build-owner-automation-run-html.py`  
4. 运行 `open-owner-automation-run-chrome.sh`（**Google Chrome**）

**禁止：** 仅在 chat 里交付、无 JSON、无 HTML。  
**禁止：** Cloud-only Automation 调用 `open`（无法弹本机 Chrome）——此类 Must 标为 **本机 Automation**。

---

## JSON 路径（统一）

```
integration/handoff/owner-automation-html/<slug>-latest.json
```

`<slug>` 见 [OWNER-CURSOR-AUTOMATIONS-INDEX.md](./OWNER-CURSOR-AUTOMATIONS-INDEX.md)。

---

## JSON 最小 schema

```json
{
  "version": "2026-11-19",
  "automation_slug": "daily-ai-intel",
  "automation_title_zh": "品牌仓 · 每日 AI 资讯简报",
  "run_date": "YYYY-MM-DD",
  "status": "PASS|NEEDS_WORK|INFO",
  "summary_zh": "Owner 80 字内",
  "md_path": "content/.../optional.md",
  "items": [
    {
      "zone": "general|ip|topic|verify|reminder|data",
      "title_zh": "条目标题",
      "excerpt_zh": "摘录或结论（可多条合成一条）",
      "source_name": "媒体名 / 脚本名 / Drive",
      "url": "https://... 或 file:///... 或空",
      "info_date": "YYYY-MM-DD"
    }
  ]
}
```

**出处 Must：** 每条 `items[]` 在 HTML 中渲染为：

- 正文：`excerpt_zh`  
- 下方一行：**来源：** `source_name` · **链接：** 可点击 `url` · **日期：** `info_date`

无外链时：`url` 填本机真源路径（`md` / `json` / `脚本名`），`source_name` 填 `本仓脚本` 或 `Google Drive`。

---

## 机械链（每条 Automation 末尾相同）

```bash
cd ~/Desktop/danying-brand-agent
python3 scripts/build-owner-automation-run-html.py --slug <slug>
bash scripts/open-owner-automation-run-chrome.sh --slug <slug>
```

HTML 输出：

```
content/evolution/00-manager/ceo-inbox/automation-runs/OWNER-AUTOMATION-<slug>-<YYYY-MM-DD>.html
```

同时写指针：`integration/handoff/owner-automation-html/<slug>-latest.html`（相对路径字符串）。

---

## Chrome

`open-owner-automation-run-chrome.sh` 使用：

```bash
open -a "Google Chrome" "file://${HTML}"
```

`CEO_OWNER_HTML_OPEN=0` 时跳过打开（仅生成文件）。

---

## 与 Layer C / Git

- `owner-automation-html/*-latest.json` 默认 **不进 Git**（与 `owner-*-latest.json` 同层 hygiene）；**当日 HTML** 可选 commit（Owner 定稿时说）。  
- **出处 URL** 必须真实；禁止编造。