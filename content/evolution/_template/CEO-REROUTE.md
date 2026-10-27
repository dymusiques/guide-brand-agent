# CEO-REROUTE · <部门名> · <slug>

- 来自：00 CEO
- 日期：
- 打回轮次：n / 3（默认上限见 [CEO-AUTO-QA-LOOP.md](../../../docs/CEO-AUTO-QA-LOOP.md)）

## 失败摘要（Gate / evaluate / verify）

- 命令：
- 终端 excerpt：（粘贴关键 FAIL 行）

## GM Must 做

1. 读上表失败原因 + 当前 `versions/vN.md`
2. 出 **v(N+1)**（或 Brief 补丁），**禁止**把同一 FAIL 稿再标「请 Owner 验证」
3. 重跑：

```bash
# CEO 指定（示例）
bash scripts/manager-ceo-owner-gate.sh --brief content/xiaohongshu/<file>.md
```

4. 更新 **GM-REPORT.md**，请求 CEO 复 gate

## CEO 备注（集成/Brief/Skill 倾向，不改 kernel 除非 05 专项）

-
