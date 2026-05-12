# SDLC Skill 一致性审计报告

> **审计基准**：`docs/AI项目落地工具链_完全手动操作手册.md` V2.3
> **审计范围**：`skills/sdlc/` 下全部 23 个 skill
> **审计日期**：2026-05-12
> **状态**：已修复（2026-05-12）

---

## 一、缺失的 Skill（3 个）✅ 已补齐

手册明确列出、但 `skills/sdlc/` 中**不存在的 skill**。

> **修复状态**：2026-05-12 已完成三个 Skill 的设计与实现，目录位置如下：

| # | 手册阶段 | Skill 名称 | 在流程中的位置 | 影响说明 |
|---|---------|-----------|---------------|---------|
| 1 | 9.5 | `uat-verification` | `integration-test` → **uat-verification** → `human (Gate 3)` | ✅ 已补齐：`skills/sdlc/uat-verification/` |
| 2 | 10.5 | `release-management` | `requesting-code-review` → **release-management** → `finish` | ✅ 已补齐：`skills/sdlc/release-management/` |
| 3 | 12 | `monitoring-analysis` | `finish` → **monitoring-analysis** → `brainstorming`（下一循环） | ✅ 已补齐：`skills/sdlc/monitoring-analysis/` |

### 证据链

- `requesting-code-review/SKILL.md` line 139：明确写入"与 release-management 的衔接"
- `finish/SKILL.md` line 255-260：上游是 `release-management`，下游是 `monitoring-analysis`
- `monitoring-setup/SKILL.md` line 178-182：下游消费表中列出 `monitoring-analysis` 和 `release-management`
- `integration-test/SKILL.md` line 86：产出 `user-stories-checklist.md` 供 Gate 3 人工 UAT 走查，但缺少 `uat-verification` 作为 UAT 报告生成阶段

---

## 二、多余的 / 重叠的 Skill（1 个主要 + 1 个次要）

| # | Skill | 问题 | 分析 | 状态 |
|---|-------|------|------|------|
| 1 | ~~`code-review`~~ | ~~与 `requesting-code-review` **触发词和职责高度重叠**~~ | ~~`code-review` 触发词："review"、"代码走读"、"检查代码质量"；`requesting-code-review` 触发词："代码审查"、"code review"、"审查代码"、"检查实现质量"。手册阶段 10 明确使用 `requesting-code-review`。`code-review` 缺少上下游衔接说明，处于流程孤岛。~~ | ✅ **已处理**：能力并入 `requesting-code-review`（新增安全性/性能/可维护性通用审查维度 + 触发词扩展），`skills/sdlc/code-review/` 已删除 |
| 2 | `requirement-analysis` | 手册速查表无位置，但 `prd-generation` 将其列为上游 | 定位模糊。与 `brainstorming` 有一定重叠，但 `prd-generation` 依赖它作为上游输入。影响较小，可保留作为可选前置。 | 保留 |

---

## 三、上下游衔接断裂（6 处）✅ 已修复

| # | 断裂点 | 现状 | 期望 | 严重级别 | 修复方式 |
|---|--------|------|------|---------|----------|
| 1 | `integration-test` → `uat-verification` | 下游直接是 `human (Gate 3)` | 应经过 `uat-verification` 生成 `uat-report.md` 后再进入 Gate 3 | 🔴 高 | `integration-test/SKILL.md` 下游改为 `uat-verification`；新增 `uat-verification` skill |
| 2 | `requesting-code-review` → `release-management` | `release-management` skill 缺失 | 审查通过后进入发布准备阶段 | 🔴 高 | 新增 `release-management` skill；`requesting-code-review/SKILL.md` 新增标准衔接表格明确下游为 `release-management` |
| 3 | `finish` → `monitoring-analysis` | `monitoring-analysis` skill 缺失 | 归档完成后进入周期性监控 | 🟡 中 | 新增 `monitoring-analysis` skill |
| 4 | `monitoring-setup` → `release-management` | `release-management` 缺失 | 发布时确认监控规则已生效 | 🔴 高 | `release-management` skill 已补齐，自然修复 |
| 5 | `monitoring-setup` → `monitoring-analysis` | `monitoring-analysis` 缺失 | 周期性读取监控规则作为分析基准 | 🟡 中 | `monitoring-analysis` skill 已补齐，自然修复 |
| 6 | `executing-plans` 下游声明 | 下游只有 `requesting-code-review` / `finish` | 手册流程中编码后是单元测试 → 集成测试 → UAT → 代码审查 → 发布 → 归档 | 🟢 低 | `executing-plans/SKILL.md` 修复下游衔接表格（新增 `unit-test` / `integration-test`）；Step 11 完成交接改为触发 `integration-test` 而非直接 `finish` |

---

## 四、修复方案

### 4.1 必须新增（3 个 Skill）

#### `uat-verification`（阶段 9.5）

| 属性 | 内容 |
|------|------|
| **触发场景** | 当用户提到'UAT'、'用户验收测试'、'验收'、'uat-report'或 Gate 3 人工走查前生成检查清单时触发 |
| **上游** | `integration-test`（消费 `user-stories-checklist.md`） |
| **下游** | `human (Gate 3)`、`requesting-code-review`（UAT 问题交叉验证输入） |
| **核心产出** | `uat-report.md`、`user-stories-checklist.md` |
| **前置条件** | `integration-test` 全部 P0 用例通过 |
| **关键红线** | UAT 发现严重问题 → 立即驳回，生成 `rework-tasks.md` 返回 `executing-plans` 修复 |

#### `release-management`（阶段 10.5）

| 属性 | 内容 |
|------|------|
| **触发场景** | 当用户提到'发布'、'上线'、'release'、'部署'或 UAT 通过后准备生产发布时触发 |
| **上游** | `requesting-code-review`（`code-review-report.md`）、`uat-verification`（`uat-report.md`）、`high-level-design`（`rollback-plan.md`） |
| **下游** | `finish`（必须人工确认上线成功后方可触发） |
| **核心产出** | `release-notes.md`、`release-checklist.md` |
| **人工决策** | 确认发布窗口、检查回滚方案、人工执行最终发布命令（AI 不自动执行生产发布） |

#### `monitoring-analysis`（阶段 12）

| 属性 | 内容 |
|------|------|
| **触发场景** | 当用户提到'监控分析'、'线上健康检查'、'周期性监控'、'feedback-loop'或归档后进入运维阶段时触发 |
| **上游** | `finish`（归档完成确认单）、`monitoring-setup`（`ops/monitoring-rules.yaml`） |
| **下游** | `brainstorming`（`feedback-loop.md` 输入下一变更） |
| **核心产出** | `monitoring-dashboard.md`、`feedback-loop.md` |
| **执行频率** | 周期性（如每周/每迭代）自动执行 |

### 4.2 必须删除 / 重构（1 个 Skill）

**`code-review` 的处理方案**

- **推荐：删除 `code-review`，将其能力融入 `requesting-code-review`**
  - `requesting-code-review` 已包含 design.md 对比、tasks.md 追溯、UAT 交叉验证等阶段 10 特有的审查维度
  - 将 `code-review` 中的通用审查清单（安全性、性能、可维护性）作为 `requesting-code-review` 的"通用审查维度"章节并入
  - 避免触发词冲突，消除流程孤岛

- **次选：保留但缩小触发范围**
  - 修改 `code-review` 的 description 为："当用户要求进行**提交前快速审查**、**重构评估**或**代码走读**时触发"
  - 修改 `requesting-code-review` 的 description 强调"**阶段 10 正式代码审查**"、"**Gate 3 通过后**"

### 4.3 必须修复的衔接文档（3 处）✅ 已实施

| # | 文件 | 修复内容 | 状态 |
|---|------|---------|------|
| 1 | `integration-test/SKILL.md` | 在"与上下游衔接"表格中，将下游从 `human (Gate 3)` 改为 `uat-verification`，并注明"UAT 验证通过后进入 Gate 3" | ✅ 已修复 |
| 2 | `executing-plans/SKILL.md` | 下游衔接表格新增 `unit-test` / `integration-test`；Step 11 完成交接改为触发 `integration-test` 而非直接 `finish` | ✅ 已修复 |
| 3 | `requesting-code-review/SKILL.md` | 新增标准"与上下游衔接"表格，明确下游为 `release-management`，返工路径为 `executing-plans` | ✅ 已修复 |

---

## 五、核对总览图

```text
手册要求（V2.4）                          实际存在
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
0 progress-tracker      ✅ 存在
1 brainstorming         ✅ 存在
1.5 competitive-analysis ✅ 存在
2 prd-generation        ✅ 存在
2.5 detailed-requirements ✅ 存在
3 前置 competitive-analysis ✅ 存在
3 high-level-design     ✅ 存在
3.5 monitoring-setup    ✅ 存在
4 detailed-design       ✅ 存在
5 interface-first-dev   ✅ 存在
5.5 writing-plans       ✅ 存在
6 task-breakdown        ✅ 存在
7 executing-plans       ✅ 存在
8 unit-test             ✅ 存在
9 integration-test      ✅ 存在
9.5 uat-verification    ✅ 存在（V2.4 新增）
10 requesting-code-review ✅ 存在
10.5 release-management ✅ 存在（V2.4 新增）
11 finish               ✅ 存在
12 monitoring-analysis  ✅ 存在（V2.4 新增）

额外存在但未在手册速查表中：
  ~~code-review~~         ❌ 已删除（能力并入 requesting-code-review）
  test-driven-development ⚠️ executing-plans 内循环，可保留
  systematic-debugging   ⚠️ 横向故障排查，integration-test 引用，可保留
  requirement-analysis   ⚠️ prd-generation 上游依赖，可保留
  git-automation         ⚠️ finish 横向引用，可保留
  self-check             ⚠️ 横向门控，贯穿各阶段，可保留
  human                  ⚠️ Gate 签字，可保留
```

---

## 六、实施优先级建议

| 优先级 | 事项 | 原因 | 状态 |
|--------|------|------|------|
| P0 | 新增 `uat-verification` | 阻断 Gate 3 流程，UAT 是发布前的硬性门控 | ✅ 已完成 |
| P0 | 新增 `release-management` | 阻断 finish 流程，finish 明确依赖它作为上游 | ✅ 已完成 |
| P1 | 新增 `monitoring-analysis` | 阻断归档后的闭环，finish 和 monitoring-setup 均引用 | ✅ 已完成 |
| P1 | 删除/重构 `code-review` | 消除触发词冲突，减少用户困惑 | ✅ 已完成 |
| P2 | 修复 `integration-test` 下游衔接文档 | 文档同步，skill 补齐后自然修复 | ✅ 已完成 |
| P2 | 修复 `executing-plans` 下游衔接文档 | 明确编码后进入测试链路的顺序 | ✅ 已完成 |
| P2 | 修复 `requesting-code-review` 下游衔接文档 | 新增标准衔接表格，明确 release-management 下游 | ✅ 已完成 |
