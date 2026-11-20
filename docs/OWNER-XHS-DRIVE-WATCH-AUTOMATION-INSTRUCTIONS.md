# 复制到 Cursor Automation · Drive 小红书日检

**名称（建议）：** `品牌仓 · Drive 小红书日检`  
**automation_slug：** `xhs-drive-watch`  
**Cron：** `30 2 * * *`（UTC）= 每天 **10:30 GMT+8**  

标准：[OWNER-AUTOMATION-HTML-CHROME-STANDARD.md](./OWNER-AUTOMATION-HTML-CHROME-STANDARD.md)

---

## 粘贴块（整段复制）

```
你是品牌仓数据 Agent · guide-brand-agent / main only。禁止 checkout 其它分支；禁止请 Owner 开终端。Must：本机 Automation。

cd ~/Desktop/danying-brand-agent
DATE=$(date +%Y-%m-%d)
mkdir -p integration/handoff/owner-automation-html
OUT=integration/handoff/owner-automation-html/xhs-drive-watch-latest.json

python3 scripts/compare-owner-xhs-drive-listing.py --sync 2>&1 | tee /tmp/xhs-drive-watch-${DATE}.log
# 根据输出判断：CHANGED / unchanged / FAIL

## 写入 ${OUT}（Must）
{
  "version": "2026-11-19",
  "automation_slug": "xhs-drive-watch",
  "automation_title_zh": "品牌仓 · Drive 小红书日检",
  "run_date": "${DATE}",
  "status": "PASS|NEEDS_WORK|INFO",
  "summary_zh": "一行：同步结果",
  "md_path": "docs/OWNER-XHS-DRIVE-WATCH-ARCHITECTURE.md",
  "items": [
    {
      "zone": "data",
      "title_zh": "Drive Listing 对比",
      "excerpt_zh": "粘贴脚本关键输出一行（CHANGED/unchanged/FAIL 原因）",
      "source_name": "compare-owner-xhs-drive-listing.py",
      "url": "file:///Users/danying/Desktop/danying-brand-agent/integration/handoff/owner-xhs-data-drive.json",
      "info_date": "${DATE}"
    }
  ]
}
若 CHANGED：items 可追加每条变更文件名（url 填 Drive 文件 id 或本地 mirror 路径若有）。

## HTML + Chrome（Must）
python3 scripts/build-owner-automation-run-html.py --slug xhs-drive-watch
bash scripts/open-owner-automation-run-chrome.sh --slug xhs-drive-watch

## 交付 chat
- 首句：Chrome + HTML 路径
- unchanged：仍生成 HTML（status INFO），一句「今日无变更」
- FAIL：status NEEDS_WORK，列出修复建议

真源：docs/OWNER-XHS-DRIVE-WATCH-ARCHITECTURE.md
```