# CEO 双线 workflow · FluteBuddy × 个人 IP

同一仓库、同一 CEO 主链（Drive screen → fusion → recover → autopilot），**两条 goal 轨**：

| 轨 | 触发词（示例） | preflight | 交付 HTML |
|----|----------------|-----------|-----------|
| **A · 产品** | FluteBuddy、长笛练习 App | `owner-product-registry.json` | `OWNER-FLUTEBUDDY-DELIVERABLE-<date>.html` |
| **B · 个人 IP** | 个人IP、生态链、张丹瀛、听见、多维度 | `owner-ip-track.json` | `OWNER-IP-ECOSYSTEM-DELIVERABLE-<date>.html` |

**混合 goal**（同时出现产品与 IP）→ 两条 HTML 都会 build + open；manifest 主交付优先 IP HTML。

## 命令

```bash
# B 轨 · IP 生态链
bash scripts/open-owner-ip-ecosystem-deliverable-html.sh

bash scripts/ceo-full-execution-pipeline.sh \
  --goal "张丹瀛 个人IP 生态链 三平台 多维度" --no-discovery-auto

# A 轨 · FluteBuddy（不变）
bash scripts/open-owner-flutebuddy-deliverable-html.sh
```

## 不弹 FILTER

非 Brief 的 A/B 轨均设 `CEO_OWNER_HTML_REFRESH=0` · 见 [CEO-OWNER-HTML-ROUTING.md](./CEO-OWNER-HTML-ROUTING.md)。

## 文案（双线共用 · 半自动）

- **40–50 万粉大 V 文笔档：** [OWNER-COPY-V-TIER-400K-MANDATE.md](./OWNER-COPY-V-TIER-400K-MANDATE.md) · JSON `integration/handoff/owner-copy-v-tier-400k.json`
- **Workflow 说明（是否全自动）：** [OWNER-DUAL-TRACK-COPY-WORKFLOW.md](./OWNER-DUAL-TRACK-COPY-WORKFLOW.md) · manifest `L2c_DUAL_TRACK_COPY`
- 验收：`bash scripts/verify-owner-copy-v-tier-mandate.sh` · **Owner 终检文笔**（脚本不替代）

## 真源

- IP 内容：`content/evolution/00-manager/ceo-inbox/owner-ip-ecosystem-content.json`
- IP 战略：`content/evolution/00-manager/ceo-inbox/2026-11-05-owner-ip-ecosystem-strategy.md`
- 轨检测：`scripts/ceo_goal_tracks.py`
- 上下文：`content/evolution/00-manager/ceo-inbox/owner-context-resolved-latest.json`
