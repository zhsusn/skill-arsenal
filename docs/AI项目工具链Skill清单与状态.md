# AI项目工具链 Skill 清单与状态

> 基于《AI项目落地工具链使用手册 V2.0》与《lifesycle.md 审查意见》整理
> 版本：V2.1 | 2026-05-08

---

## 一、总体概览

| 统计项 | 数量 |
|--------|------|
| 可用（已存在，基本满足/已按 lifesycle.md 增强） | 13 个 |
| 需修改（已存在，待增强） | 0 个 |
| 需新增（当前缺失） | 10 个 |
| **合计** | **23 个** |

---

## 二、按使用顺序的 Skill 清单

> 流程已按 `lifesycle.md` 建议补充 UAT、发布、监控环节与四道人工闸门（Gate 1/2.5/2/3）。

### 阶段 0：项目初始化

| 序号 | Skill 名 | 状态 | 说明 |
|------|----------|------|------|
| 1 | **progress-tracker** | ✅ 可用（V2.1 已增强） | 初始化增加 `ops/` 目录（staging-config.yaml、rollback-plan.md、monitoring-rules.yaml 骨架）与 `human_status` 字段；12 阶段定义含 UAT/发布/监控；Gate 拦截规则与总进度上限。 |

### 阶段 1：需求探索

| 序号 | Skill 名 | 状态 | 说明 |
|------|----------|------|------|
| 2 | **brainstorming** | ✅ 可用 | Superpowers 原生，需求探索与苏格拉底式提问。 |
| 3 | **competitive-analysis** (positioning) | ✅ 可用 | 市场定位模式，在 PRD 前分析竞争格局与差异化空间。 |

### 阶段 2：概要需求（Gate 1 需求冻结闸）

| 序号 | Skill 名 | 状态 | 说明 |
|------|----------|------|------|
| 4 | **prd-generation** | ✅ 可用（V2.1 已增强） | 输出 5 个 spec 文件后，自动宣读 🚪 Gate 1 阻塞提示；基线冻结需等待 `human` Skill 签字；与 progress-tracker/self-check 联动。 |
| 5 | **human** (Gate1) | ➕ 需新增 | 人工决策审计日志。记录 Gate1 评审结论（sign-off/conditional/reject），控制阶段流转权限。 |

### 阶段 2.5：详细需求（Gate 2.5 原型冻结闸）

| 序号 | Skill 名 | 状态 | 说明 |
|------|----------|------|------|
| 6 | **detailed-requirements** | ✅ 可用（V2.1 已增强） | 输出 5 文件（spec/prototype/io-table/logic/**interaction-spec**）：每个按钮必须包含触发方式、前置条件、立即反馈、成功/失败结果、异常分支、埋点事件；全部模块生成后触发 🚪 Gate 2.5 阻塞提示。 |
| 7 | **human** (Gate2.5) | ➕ 需新增 | 记录 Gate2.5 原型与交互规格的人工确认结论。逐页确认按钮级交互状态机后方可解锁概要设计。 |

### 阶段 3：概要设计（Gate 2 设计冻结闸）

| 序号 | Skill 名 | 状态 | 说明 |
|------|----------|------|------|
| 8 | **competitive-analysis** (technical) | ✅ 可用 | 技术深度对比模式，输出 `competitive-analysis.md` + `design-input.md`。 |
| 9 | **high-level-design** | ✅ 可用（V2.1 已增强） | 18 个设计文档（新增 operations-architecture + rollback-plan）：运维监控三支柱、回滚触发条件/步骤/灰度策略；rollback-plan 双写（变更目录 + 项目级 `ops/`）；输出后触发 🚪 Gate 2 阻塞提示。 |
| 10 | **monitoring-setup** | ➕ 需新增 | 一次性 Skill。消费 high-level-design 的运维架构章节，生成 `monitoring-rules.yaml` + `alert-channels.md` 初稿，人工调整阈值后生效。建议在 progress-tracker 初始化阶段触发。 |
| 11 | **human** (Gate2) | ➕ 需新增 | 记录 Gate2 设计冻结结论。评审架构 + 确认 rollback-plan.md 后方可解锁详细设计。 |

### 阶段 4：详细设计

| 序号 | Skill 名 | 状态 | 说明 |
|------|----------|------|------|
| 12 | **detailed-design** | ➕ 需新增 | 按模块输出详细设计：`design.md`、`api-spec.md`、`db-schema.md`、`state-machine.md`、`test-plan.md`。不同于 `technical-design-document-generator`（输出完整八章节 SDD），本 Skill 按 feature-XX-{模块}/ 目录逐模块下钻。 |

### 阶段 5：接口驱动开发

| 序号 | Skill 名 | 状态 | 说明 |
|------|----------|------|------|
| 13 | **interface-first-dev** | ➕ 需新增 | 基于详细设计定义前后端接口契约。生成 `openapi.yaml` + `mock-data.json` + `mock-server-config.md` + `parallel-dev-plan.md`。 |

### 阶段 6：任务拆解

| 序号 | Skill 名 | 状态 | 说明 |
|------|----------|------|------|
| 14 | **task-breakdown** | ➕ 需新增 | 基于详细设计和接口契约，将工作拆解为 ≤30 分钟/任务，生成 `tasks.md`。 |

### 阶段 7：编码实现

| 序号 | Skill 名 | 状态 | 说明 |
|------|----------|------|------|
| 15 | **writing-plans** | ✅ 可用 | Superpowers 原生，生成精细到 2-5 分钟任务的实现计划。 |
| 16 | **executing-plans** | ✅ 可用 | Superpowers 原生，按计划执行代码实现。 |
| 17 | **test-driven-development** (tdd) | ✅ 可用 | Superpowers 原生，RED-GREEN-REFACTOR 循环。 |
| 18 | **systematic-debugging** | ✅ 可用 | Superpowers 原生，四阶段根因分析。 |

### 阶段 8：单元测试

| 序号 | Skill 名 | 状态 | 说明 |
|------|----------|------|------|
| 19 | **unit-test** | ➕ 需新增 | 为已完成的模块生成单元测试，要求覆盖率 ≥ 70%。区别于 TDD（开发方法论），本 Skill 聚焦存量代码测试补全与覆盖率报告。 |

### 阶段 9：集成测试

| 序号 | Skill 名 | 状态 | 说明 |
|------|----------|------|------|
| 20 | **integration-test** | ➕ 需新增 | 生成并执行集成测试，覆盖端到端主链路场景。**输出增加 `user-stories-checklist.md`**，将详细需求中的用户故事转为可勾选测试项，供 UAT 使用。 |

### 阶段 9.5：UAT 与业务验证（Gate 3 发布冻结闸）

| 序号 | Skill 名 | 状态 | 说明 |
|------|----------|------|------|
| 21 | **uat-verification** | ➕ 需新增 | 人工主导（产品经理/业务方）+ AI 辅助生成测试清单模板。输入：integration-test 通过记录 + `feature-*/user-stories.md` + 预览环境 URL。输出：`uat-report.md`（通过/不通过/遗留问题/严重级别）。 |
| 22 | **human** (Gate3) | ➕ 需新增 | 记录 Gate3 发布冻结结论。UAT 通过 + code-review-report.md 通过后方可解锁上线发布。 |

### 阶段 10：代码审查

| 序号 | Skill 名 | 状态 | 说明 |
|------|----------|------|------|
| 23 | **requesting-code-review** | ✅ 可用（V2.1 已增强） | 审查后强制输出结构化 `code-review-report.md`（总体结论/阻塞性/重要/轻微问题分级/与 UAT 交叉验证），作为 release-management 的准入输入；UAT 通过后、发布前强制触发。 |

### 阶段 10.5：上线发布

| 序号 | Skill 名 | 状态 | 说明 |
|------|----------|------|------|
| 24 | **release-management** | ➕ 需新增 | 输入：uat-report.md + code-review-report.md + rollback-plan.md + 代码分支/commit SHA。人工最终决策 + AI 辅助生成发布清单和 Release Notes。输出：`release-notes.md` + `release-checklist.md` + 生产部署确认单。**严禁 AI 自动执行生产发布。** |

### 阶段 11：归档收尾

| 序号 | Skill 名 | 状态 | 说明 |
|------|----------|------|------|
| 25 | **finishing-a-development-branch** (finish) | ✅ 可用 | Superpowers 原生，变更完成时联动归档。 |

### 阶段 12：线上监控（周期性）

| 序号 | Skill 名 | 状态 | 说明 |
|------|----------|------|------|
| 26 | **monitoring-analysis** | ➕ 需新增 | 周期性运行。输入：运行时日志/告警（Sentry/Prometheus）+ 埋点数据 + `monitoring-rules.yaml`。AI 辅助生成周度摘要报告。输出：`monitoring-dashboard.md` + `feedback-loop.md`，后者输入到下一变更的 brainstorming，形成闭环。 |

### 贯穿全程

| 序号 | Skill 名 | 状态 | 说明 |
|------|----------|------|------|
| 27 | **self-check** | ✅ 可用（V2.1 已增强） | 新增两个检查维度：① 交互规格完整性（元素覆盖度/状态机完整性/异常分支/埋点/页面跳转一致性）；② UAT 报告质量（用户故事覆盖度/缺陷记录/遗留问题处理计划/与 code-review 一致性）。检查清单覆盖 interaction-spec 与 uat-report 目标。 |

---

## 三、输入-处理-输出衔接总图

```text
阶段 0 初始化
    │
    ├──→ progress-tracker 输出：config.yaml + progress.md + ops/ 目录骨架（新增）
    │
    ▼
阶段 1 需求探索
    │
    ├──→ brainstorming → 需求草案
    ├──→ competitive-analysis (positioning) → market-positioning.md
    │
    ▼
阶段 2 概要需求
    │
    ├──→ prd-generation → specs/01-05.md
    │
    ├──→ 🚪 Gate 1：human 记录 sign-off → 01-requirements.md 签字
    │
    ▼
阶段 2.5 详细需求
    │
    ├──→ detailed-requirements → feature-*/{spec,prototype,io-table,logic,interaction-spec}.md
    │
    ├──→ 🚪 Gate 2.5：human 记录原型确认 → 02.5-prototype.md 签字
    │
    ▼
阶段 3 概要设计
    │
    ├──→ competitive-analysis (technical) → competitive-analysis.md + design-input.md
    ├──→ high-level-design → design/*.md + rollback-plan.md
    ├──→ monitoring-setup → monitoring-rules.yaml + alert-channels.md（一次性）
    │
    ├──→ 🚪 Gate 2：human 记录设计冻结 → 02-design.md 签字
    │
    ▼
阶段 4 详细设计
    │
    ├──→ detailed-design → feature-*/{design,api-spec,db-schema,state-machine,test-plan}.md
    │
    ▼
阶段 5 接口驱动
    │
    ├──→ interface-first-dev → interface-contracts/{openapi,mock-data,mock-server-config,parallel-dev-plan}.md
    │
    ▼
阶段 6 任务拆解
    │
    ├──→ task-breakdown → tasks.md
    │
    ▼
阶段 7 编码实现
    │
    ├──→ writing-plans → 精细计划
    ├──→ executing-plans + tdd + systematic-debugging → 代码文件
    │
    ▼
阶段 8 单元测试
    │
    ├──→ unit-test → tests/unit/ + 覆盖率报告
    │
    ▼
阶段 9 集成测试
    │
    ├──→ integration-test → tests/integration/ + user-stories-checklist.md
    │
    ▼
阶段 9.5 UAT（新增）
    │
    ├──→ uat-verification → uat-report.md（人工主导 + AI 辅助）
    │
    ├──→ 🚪 Gate 3：human 记录发布冻结 → 03-release.md 签字
    │
    ▼
阶段 10 代码审查
    │
    ├──→ requesting-code-review → code-review-report.md
    │
    ▼
阶段 10.5 上线发布（新增）
    │
    ├──→ release-management → release-notes.md + release-checklist.md（人工最终决策）
    │
    ▼
阶段 11 归档
    │
    ├──→ opsx:archive + finish → archive/{变更名}/
    │       归档范围扩大：纳入 uat-report + release-notes + human-decisions.md
    │
    ▼
阶段 12 线上监控（新增，周期性）
    │
    ├──→ monitoring-analysis → monitoring-dashboard.md + feedback-loop.md
    │
    └──→ feedback-loop.md 输入到下一变更的 brainstorming（闭环）
```

---

## 四、实施优先级建议

| 优先级 | Skill | 理由 |
|--------|-------|------|
| **P0** | detailed-requirements（修改：增加 interaction-spec.md） | 交互密集型产品按钮级交互缺失是当前最大风险。 |
| **P0** | uat-verification（新增） | 文档完全缺失业务验证环节，上线后极易出现"功能可用但流程走不通"。 |
| **P0** | human（新增） | 四道人工闸门的统一载体，是所有 Gate 落地的核心依赖。 |
| ~~P1~~ | ~~progress-tracker（修改：增加 ops/ 目录 + 人工状态）~~ | ~~已完成。~~ |
| ~~P1~~ | ~~high-level-design（修改：增加 rollback-plan.md）~~ | ~~已完成。~~ |
| **P1** | release-management（新增） | 补齐"开发完成 → 上线交付"的最后一公里。 |
| **P1** | detailed-design / interface-first-dev / task-breakdown（新增） | 设计到开发的核心链路 Skill，当前完全缺失。 |
| **P2** | unit-test / integration-test（新增） | 测试链路核心 Skill，可用现有 TDD 部分覆盖，但独立测试 Skill 仍必要。 |
| **P2** | monitoring-setup + monitoring-analysis（新增） | 长期价值大，但短期内不影响 MVP 上线。 |
| ~~P2~~ | ~~self-check / requesting-code-review / prd-generation（修改）~~ | ~~已完成。~~ |

---

## 五、与现有 Skill 目录的映射关系

| 工具链 Skill 名 | 项目现有目录 | 备注 |
|----------------|-------------|------|
| brainstorming | `skills/sdlc/brainstorming/` | 直接可用 |
| writing-plans | `skills/sdlc/writing-plans/` | 直接可用 |
| executing-plans | `skills/sdlc/executing-plans/` | 直接可用 |
| test-driven-development (tdd) | `skills/sdlc/test-driven-development/` | 直接可用 |
| systematic-debugging | `skills/sdlc/systematic-debugging/` | 直接可用 |
| requesting-code-review | `skills/sdlc/requesting-code-review/` | 已增强（V2.1） |
| finishing-a-development-branch (finish) | `skills/sdlc/finishing-a-development-branch/` | 直接可用 |
| prd-generation | `skills/sdlc/prd-generation/` | 已增强（V2.1） |
| progress-tracker | `skills/sdlc/progress-tracker/` | 已增强（V2.1） |
| self-check | `skills/sdlc/self-check/` | 已增强（V2.1） |
| competitive-analysis | `skills/sdlc/competitive-analysis/` | 直接可用 |
| high-level-design | `skills/sdlc/high-level-design/` | 已增强（V2.1） |
| detailed-requirements | `skills/sdlc/detailed-requirements/` | 已增强（V2.1） |
| requirement-analysis | `skills/sdlc/requirement-analysis/` | 非主线工具链 Skill，备用 |
| technical-design-document-generator | `skills/sdlc/technical-design-document-generator/` | 非工具链主线，detailed-design 替代 |
| code-review | `skills/sdlc/code-review/` | 非工具链主线，requesting-code-review 替代 |

---

*本文档随工具链迭代持续更新。新增或修改 Skill 后，应同步更新本清单、根目录 `index.json` 与各 Skill 的 `meta.json`。*
