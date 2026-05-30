---
name: release-management
description: 当用户提到'发布'、'上线'、'release'、'部署'、'准备发布'或 UAT 通过（Gate 3 签字）后需要进入生产发布阶段时触发。基于 UAT 报告、代码审查报告和回滚方案生成发布清单与发布说明，辅助人工完成最终发布决策。
---

# Release Management（上线发布）

## 适用场景

- Gate 3（UAT）签字通过后，准备生产环境发布
- 用户明确要求"发布"、"上线"、"部署"、"生成发布说明"
- 需要基于 rollback-plan.md 确认发布前检查项
- 需要生成 `release-notes.md` 和 `release-checklist.md`
- 变更完成代码审查后，进入发布准备阶段

## 关键安全规则

> ⚠️ **AI 只负责生成文档和检查项。上线按钮必须由人按。发布窗口、回滚方案确认由人工最终决策。**

- 严禁 AI 自动执行生产环境部署命令
- 严禁 AI 在未经人工明确确认的情况下标记"发布完成"
- 生产数据库变更脚本必须由人工二次确认

## 前置依赖

| 依赖项 | 路径 | 门控标准 |
|--------|------|----------|
| UAT 报告 | `openspec/changes/{变更名}/uat/uat-report.md` | Gate 3 签字通过（无阻塞性问题） |
| 代码审查报告 | `openspec/changes/{变更名}/code-review/review-report.yaml` | overall 为 Approve 或 Comment；blocking 问题已清零 |
| 回滚方案 | `openspec/changes/{变更名}/high-level-design/05-ops-governance.md` §2（回滚方案） | 存在且可读 |
| 监控规则 | `ops/monitoring-rules.yaml` | 已确认生效（由 monitoring-setup 生成） |
| 代码分支 | Git 仓库 | commit SHA 已确定 |

**硬性阻断**：若 uat-report.md 结论为"不通过"或 code-review-report.md 存在未清零的阻塞性问题，拒绝执行并提示："存在未修复的阻塞性问题，请先修复后再进入发布阶段。"

## 执行流程

### Phase 1: 读取输入与风险评估

1. 读取 `uat-report.md`：
   - 确认总体结论为"通过"或"有条件通过"
   - 提取遗留问题清单（标记为发布后可处理或需纳入发布说明已知问题）
2. 读取 `code-review/review-report.yaml`：
   - 确认 `overall` 为 `Approve` 或 `Comment`
   - 确认 `issues.blocking` 为空数组
   - 提取 `assessment` 和 `strengths` 摘要
3. 读取 `rollback-plan.md`：
   - 确认回滚触发条件、回滚步骤、数据库回滚脚本清单、灰度策略
4. 读取 `monitoring-rules.yaml`：
   - 确认关键告警规则已配置
   - 确认业务埋点已就绪
5. 读取 Git 状态：
   - 当前分支、commit SHA、与主分支的差异

**风险评估输出**：

```markdown
## 发布风险评估

| 维度 | 状态 | 说明 |
|------|------|------|
| UAT 结论 | ✅ 通过 | 无阻塞性问题 |
| 代码审查 | ✅ 通过 | 阻塞性问题已清零 |
| 回滚方案 | ✅ 已确认 | 回滚步骤可操作，DB 脚本已准备 |
| 监控就绪 | ✅ 已配置 | monitoring-rules.yaml 已生效 |
| 遗留问题 | ⚠️ 2 项 | 均为 P2，不影响核心流程 |
| **综合风险** | 🟢 低风险 | 建议发布 |
```

### Phase 2: 生成发布清单

生成 `openspec/changes/{变更名}/release-checklist.md`：

```markdown
# 发布检查清单：{变更名}

> 发布版本：{版本号}
> 发布日期：{日期}
> 负责人：{人工填写}

## 预发布检查

- [ ] 代码审查阻塞性问题已清零
- [ ] UAT 报告结论为通过
- [ ] 回滚方案已确认且可执行
- [ ] 监控规则已生效（关键告警至少 1 条应用层 + 1 条基础设施）
- [ ] 生产环境配置已更新（ops/staging-config.yaml 已同步到生产）
- [ ] 数据库迁移脚本已review（如有 DDL 变更）

## 发布步骤

- [ ] 1. 确认发布窗口（低峰期）
- [ ] 2. 执行数据库迁移（如有）
- [ ] 3. 部署应用代码（灰度/全量）
- [ ] 4. 验证健康检查接口通过
- [ ] 5. 验证核心业务流程（参照 UAT 检查清单抽样）
- [ ] 6. 确认监控告警无异常
- [ ] 7. 通知相关方发布完成

## 回滚触发条件（紧急）

若以下任一情况发生，立即执行 rollback-plan.md：
- 错误率 > {阈值}% 持续 5 分钟
- P99 延迟 > {阈值}ms 持续 5 分钟
- 核心业务流程无法走通
- 监控告警 critical 级连续触发

## 发布后验证

- [ ] 核心链路抽样验证通过
- [ ] 监控 dashboard 数据正常
- [ ] 无异常告警
```

### Phase 3: 生成发布说明

基于 release-notes.md 模板和本次变更内容，生成 `openspec/changes/{变更名}/release-notes.md`：

```markdown
# Release Notes：{版本号}

> 变更名：{变更名}
> 发布日期：{ISO8601}
> 关联变更：{openspec/changes/{变更名}/}

## 变更概要

{一句话描述本次变更的核心价值}

## 新增

- {来自 tasks.md 中已完成的任务摘要}

## 修复

- {来自 uat-report.md 和 code-review-report.md 的问题修复}

## 变更

- {技术升级、依赖更新等}

## 已知问题

- {来自 uat-report.md 的遗留问题}

## 回滚方案

参见 `high-level-design/05-ops-governance.md` §2。

## 监控与告警

- 关键指标：{来自 monitoring-rules.yaml 的摘要}
- Dashboard 地址：{人工填写}

## 关联文档

- UAT 报告：`uat/uat-report.md`
- 代码审查报告：`code-review/review-report.yaml`
- 设计文档：`high-level-requirements/`、`detailed-requirements/`、`high-level-design/`、`detailed-design/`
```

### Phase 4: 人工最终决策

向用户输出最终决策提示：

```text
========================================
🚀 发布准备完成 —— 等待人工最终决策
========================================

release-checklist.md 和 release-notes.md 已生成。

请人工确认以下事项：
1. 发布窗口是否合适？
2. 回滚方案是否已检查且可执行？
3. 数据库变更脚本是否已二次确认？
4. 是否确认执行生产发布？

⚠️ 严禁 AI 自动执行发布命令。
请在确认无误后，人工执行发布操作。
发布完成后，请告诉我"发布成功"以触发归档流程。
```

## 与上下游衔接

| 衔接点 | 动作 |
|--------|------|
| 上游: code-review-pipeline | 消费 `code-review/review-report.yaml`；阻塞性问题必须清零 |
| 上游: uat-verification | 消费 `uat-report.md`；必须通过 Gate 3 |
| 上游: high-level-design | 消费 `rollback-plan.md` 作为回滚基准 |
| 上游: monitoring-setup | 确认 `monitoring-rules.yaml` 已生效 |
| 下游: finish | 人工确认发布成功后触发归档收尾 |
| 横向: self-check | 检查发布清单完整性、风险覆盖度 |

## 输出物清单

| 文件 | 路径 | 说明 |
|------|------|------|
| release-checklist.md | `openspec/changes/{变更名}/release-checklist.md` | 发布前检查项与发布步骤 |
| release-notes.md | `openspec/changes/{变更名}/release-notes.md` | 面向团队/用户的发布说明 |
| release-risk-assessment.md | `openspec/changes/{变更名}/release-risk-assessment.md` | 风险评估摘要（可选） |

## Gotchas

- **严禁 AI 自动发布**：AI 在任何情况下不得执行 `kubectl apply`、`docker push`、`git push production` 等生产发布命令。这是绝对红线。
- **阻塞性问题清零门槛**：code-review-report.md 中存在未修复的阻塞性问题时，release-management 必须拒绝生成发布清单。不允许"带病发布"。
- **回滚方案必须可操作**：若 rollback-plan.md 中的步骤含糊（如"必要时回滚"而非具体命令），必须在发布清单中标记为风险项并要求人工补充。
- **数据库变更的双刃剑**：涉及 DDL（如删表、改列类型）的变更，发布清单必须单独标注"不可逆操作"，并要求人工二次确认。
- **监控规则发布前确认**：monitoring-rules.yaml 虽已生成，但发布前必须人工确认告警通道（如钉钉/Slack/PagerDuty）已配置，否则告警无法触达。
- **release-notes.md 不是内部文档**：release-notes.md 面向团队和用户，禁止包含敏感信息（如内网 IP、数据库密码、API Key）。
- **发布清单的抽样验证**：发布后验证不应重复全部 UAT 用例，而是抽样验证核心链路（1-2 个 P0 用户故事），确保发布未引入明显回归。
- **与 finish 的衔接协议**：用户说"发布成功"是触发 finish 的信号，但 AI 不得自行推断发布成功（如看到 commit 到主分支就自动归档）。必须等待明确的人工信号。
