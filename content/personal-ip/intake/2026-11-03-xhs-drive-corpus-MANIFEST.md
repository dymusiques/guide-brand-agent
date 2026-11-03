# intake · xhs-drive-corpus-manifest

- **source:** google drive folder
- **drive_folder_id:** `1SrD2n_zXN2HjhH_YPbQa-_54YakKXbzZ`
- **drive_link:** https://drive.google.com/drive/folders/1SrD2n_zXN2HjhH_YPbQa-_54YakKXbzZ?usp=drive_link
- **goal_one_line:** 小红书 IP 资料与分析库 · 无损镜像 + 分块摘录 · 供 Agent 背书
- **ingested_at:** 2026-11-03
- **machine_manifest（当前）：** `content/personal-ip/intake/_raw/xhs-ip-2026-11-03/drive-listing-2026-11-03-live.json`（2026-11-03 从 Drive API 两页拉全 · **380** 文件 · 旧 dry-run 215 已过期 · 新增 165 · 删除 0）
- **machine_manifest（旧）：** `content/personal-ip/intake/_raw/xhs-ip-2026-11-03/drive-manifest-dry-run.json`

## 类型统计

| mime | 数量 |
|------|------|
| application/pdf | 253 |
| text/markdown | 94 |
| presentation (.pptx) | 14 |
| word (.docx) | 12 |
| spreadsheet / csv / xls | 7 |

## 本地路径约定

| 用途 | 路径 |
|------|------|
| 无损镜像 | `_raw/xhs-ip-2026-11-03/drive-mirror/小红书/` |
| PDF 纯文本 | `_raw/xhs-ip-2026-11-03/pdf-text/`（与 mirror 相对路径一致） |
| 下载日志 | `_raw/xhs-ip-2026-11-03/download.log` |

## 验收命令

```bash
python3 scripts/ingest-xhs-drive-corpus.py --verify
python3 scripts/ingest-xhs-drive-corpus.py --pdftotext   # 镜像完成后
```

## 未解决 / 待 verify

- [ ] 镜像对齐 live JSON 的 380（当前远少于这个数）。未镜像的按 file id 从 Drive 打开
- [ ] 同名 `(1)` `(2)` 副本约 19 组，引用时认一份，不要当成两套方法
- [ ] 扫描版 PDF 空文本 → OCR 队列
- [ ] 正文按任务打开 1–3 份，不做全库总摘要
