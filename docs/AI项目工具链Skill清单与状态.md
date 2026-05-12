# AI项目工具链 Skill 清单与状态

> 基于《AI项目落地工具链使用手册 V2.4》与《lifesycle.md 审查意见》整理
> 版本：V2.4 | 2026-05-12
>
> **本次更新**：`uat-verification`、`release-management`、`monitoring-analysis` 三个 Skill 正式可用；`code-review` 能力并入 `requesting-code-review` 后删除；`human` Skill 确认可用。

---

## 一、总体概览

| 统计项 | 数量 |
|--------|------|
| 可用（已存在，基本满足/已按 lifesycle.md 增强） | **28** 个 |
| 需修改（已存在，待增强） | 0 个 |
| 需新增（当前缺失） | **0** 个 |
| 已删除（能力合并） | 1 个（`code-review` → `requesting-code-review`） |
| **活跃 Skill 合计** | **28** 个 |

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
| 5 | **human** (Gate1) | ✅ 可用 | 人工决策审计日志。记录 Gate1 评审结论（sign-off/conditional/reject），控制阶段流转权限。 |

### 阶段 2.5：详细需求（Gate 2.5 原型冻结闸）

| 序号 | Skill 名 | 状态 | 说明 |
|------|----------|------|------|
| 6 | **detailed-requirements** | ✅ 可用（V2.1 已增强） | 输出 5 文件（spec/prototype/io-table/logic/**interaction-spec**）：每个按钮必须包含触发方式、前置条件、立即反馈、成功/失败结果、异常分支、埋点事件；全部模块生成后触发 🚪 Gate 2.5 阻塞提示。 |
| 7 | **human** (Gate2.5) | ✅ 可用 | 记录 Gate2.5 原型与交互规格的人工确认结论。逐页确认按钮级交互状态机后方可解锁概要设计。 |

### 阶段 3：概要设计（Gate 2 设计冻结闸）

| 序号 | Skill 名 | 状态 | 说明 |
|------|----------|------|------|
| 8 | **competitive-analysis** (technical) | ✅ 可用 | 技术深度对比模式，输出 `competitive-analysis.md` + `design-input.md`。 |
| 9 | **high-level-design** | ✅ 可用（V2.1 已增强） | 18 个设计文档（新增 operations-architecture + rollback-plan）：运维监控三支柱、回滚触发条件/步骤/灰度策略；rollback-plan 双写（变更目录 + 项目级 `ops/`）；输出后触发 🚪 Gate 2 阻塞提示。 |
| 10 | **monitoring-setup** | ✅ 可用 | 一次性 Skill。消费 high-level-design 的运维架构章节，生成 `monitoring-rules.yaml` 初稿。人工调整阈值后生效。 |
| 11 | **human** (Gate2) | ✅ 可用 | 记录 Gate2 设计冻结结论。评审架构 + 确认 rollback-plan.md 后方可解锁详细设计。 |

### 阶段 4：详细设计

| 序号 | Skill 名 | 状态 | 说明 |
|------|----------|------|------|
| 12 | **detailed-design** | ✅ 可用（V2.3） | 按模块输出详细设计 5 文件（design.md / api-spec.md / db-schema.md / state-machine.md / test-plan.md），内置 Cross-Module Audit、规格充分性审查、设计质量自评三级门控，支持增量更新。 |

### 阶段 5：接口驱动开发

| 序号 | Skill 名 | 状态 | 说明 |
|------|----------|------|------|
| 13 | **interface-first-dev** | ✅ 可用 | 基于详细设计定义前后端接口契约。生成 `openapi.yaml` + `mock-data.json` + `mock-server-config.md` + `parallel-dev-plan.md`。 |

### 阶段 6：任务拆解

| 序号 | Skill 名 | 状态 | 说明 |
|------|----------|------|------|
| 14 | **task-breakdown** | ✅ 可用 | 基于详细设计和接口契约，将工作拆解为 ≤30 分钟/任务，生成 `tasks.md`。 |

### 阶段 7：编码实现

| 序号 | Skill 名 | 状态 | 说明 |
|------|----------|------|------|
| 15 | **writing-plans** | ✅ 可用 | 模块级实现计划（plan.md），含 Self-Review 四检与 Plan → Task 转换建议。 |
| 16 | **executing-plans** | ✅ 可用 | Superpowers 原生，按计划执行代码实现。按 Batch 消费任务，含执行前审查、强制自测、接口校验、自动勾选与批次检查点。 |
| 17 | **test-driven-development** (tdd) | ✅ 可用 | Superpowers 原生，RED-GREEN-REFACTOR 循环。executing-plans 内部每个任务自动调用。 |
| 18 | **systematic-debugging** | ✅ 可用 | Superpowers 原生，四阶段根因分析。integration-test / executing-plans 失败时可横向调用。 |

### 阶段 8：单元测试

| 序号 | Skill 名 | 状态 | 说明 |
|------|----------|------|------|
| 19 | **unit-test** | ✅ 可用 | 为已完成的模块生成单元测试，要求覆盖率 ≥ 70%。区别于 TDD（开发方法论），本 Skill 聚焦存量代码测试补全与覆盖率报告。 |

### 阶段 9：集成测试

| 序号 | Skill 名 | 状态 | 说明 |
|------|----------|------|------|
| 20 | **integration-test** | ✅ 可用 | 生成并执行集成测试，覆盖端到端主链路场景。输出 `tests/integration/` + `user-stories-checklist.md` 供 UAT 使用。 |

### 阶段 9.5：UAT 与业务验证（Gate 3 发布冻结闸）

| 序号 | Skill 名 | 状态 | 说明 |
|------|----------|------|------|
| 21 | **uat-verification** | ✅ 可用（V2.4） | 基于用户故事和集成测试结果生成 UAT 验证方案。四阶段流水线：清单增强 → 人工验证 → 生成报告 → 门控流转。输出 `uat-report.md` + `rework-tasks.md`（不通过时）。 |
| 22 | **human** (Gate3) | ✅ 可用 | 记录 Gate3 发布冻结结论。UAT 通过 + code-review-report.md 通过后方可解锁上线发布。 |

### 阶段 10：代码审查

| 序号 | Skill 名 | 状态 | 说明 |
|------|----------|------|------|
| 23 | **requesting-code-review** | ✅ 可用（V2.4 已增强） | 分派代码审查子代理，执行安全性/性能/可维护性通用审查 + design.md 对比 + tasks.md 追溯 + UAT 交叉验证。强制输出结构化 `code-review-report.md`，作为 release-management 的准入输入；UAT 通过后、发布前强制触发。 |

### 阶段 10.5：上线发布

| 序号 | Skill 名 | 状态 | 说明 |
|------|----------|------|------|
| 24 | **release-management** | ✅ 可用（V2.4） | 基于 UAT/代码审查/回滚方案生成发布清单与发布说明。四阶段流水线：风险评估 → 清单生成 → 发布说明 → 人工决策。**严禁 AI 自动执行生产发布。** |

### 阶段 11：归档收尾

| 序号 | Skill 名 | 状态 | 说明 |
|------|----------|------|------|
| 25 | **finish** | ✅ 可用（V2.1 已增强） | 八步归档流水线：分支合并 → 临时文件清理 → OpenSpec 归档 → 增量规格合并 → 纳入交付后文档 → CHANGELOG → 一致性校验 → 确认单。归档范围扩大至 7 类文档。 |

### 阶段 12：线上监控（周期性）

| 序号 | Skill 名 | 状态 | 说明 |
|------|----------|------|------|
| 26 | **monitoring-analysis** | ✅ 可用（V2.4） | 周期性运行。基于监控规则基线与运行时数据评估系统健康度。输出 `monitoring-dashboard.md` + `feedback-loop.md`，后者输入到下一变更的 brainstorming，形成闭环。 |

### 贯穿全程

| 序号 | Skill 名 | 状态 | 说明 |
|------|----------|------|------|
| 27 | **self-check** | ✅ 可用（V2.3 已增强） | 门控级自查引擎。新增阶段 4 详细设计文档质量检查（7 项维度）与变更影响分析（继承自原 prd-trace-matrix）。检查清单覆盖 interaction-spec 与 uat-report 目标。 |
| 28 | **git-automation** | ✅ 可用 | 自动生成 Conventional Commits 规范提交信息。finish 横向引用。 |

---

## 三、输入-处理-输出衔接总图

```text
阶段 0 初始化
    │
    ├──→ progress-tracker 输出：config.yaml + progress.md + ops/ 目录骨架
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
    ├──→ monitoring-setup → monitoring-rules.yaml（一次性）
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
    ├──→ writing-plans → plan.md
    ├──→ executing-plans + tdd + systematic-debugging → 代码文件
    │       └── 每个任务内循环：test-driven-development (RED-GREEN-REFACTOR)
    │       └── 遇阻时横向调用：systematic-debugging
    │
    ▼
阶段 8 单元测试
    │
    ├──→ unit-test → tests/unit/ + coverage-report.md（覆盖率 ≥70% 门控）
    │
    ▼
阶段 9 集成测试
    │
    ├──→ integration-test → tests/integration/ + user-stories-checklist.md
    │
    ▼
阶段 9.5 UAT
    │
    ├──→ uat-verification → uat-report.md（人工主导 + AI 辅助）
    │
    ├──→ 🚪 Gate 3：human 记录发布冻结 → 03-release.md 签字
    │
    ▼
阶段 10 代码审查
    │
    ├──→ requesting-code-review → code-review-report.md
    │       └── 通用审查维度：安全性 / 性能 / 可维护性 / 代码规范
    │       └── 阶段 10 特有维度：design.md 对比 / tasks.md 追溯 / UAT 交叉验证
    │
    ▼
阶段 10.5 上线发布
    │
    ├──→ release-management → release-notes.md + release-checklist.md（人工最终决策）
    │
    ▼
阶段 11 归档
    │
    ├──→ finish → archive/{变更名}/
    │       归档范围：specs/ + tasks.md + uat-report.md + release-notes.md
    │                 + human-decisions.md + code-review-report.md + merge-report.md
    │
    ▼
阶段 12 线上监控（周期性）
    │
    ├──→ monitoring-analysis → monitoring-dashboard.md + feedback-loop.md
    │
    └──→ feedback-loop.md 输入到下一变更的 brainstorming（闭环）
```

---

## 四、实施状态（全部已完成）

| 优先级 | Skill | 理由 | 状态 |
|--------|-------|------|------|
| P0 | detailed-requirements（增加 interaction-spec.md） | 交互密集型产品按钮级交互缺失是当前最大风险。 | ✅ 已完成（V2.1） |
| P0 | uat-verification（新增） | 文档完全缺失业务验证环节，上线后极易出现"功能可用但流程走不通"。 | ✅ 已完成（V2.4） |
| P0 | human（新增） | 四道人工闸门的统一载体，是所有 Gate 落地的核心依赖。 | ✅ 已完成（V2.1） |
| P1 | progress-tracker（增加 ops/ 目录 + 人工状态） | 初始化阶段补齐运维基础设施骨架。 | ✅ 已完成（V2.1） |
| P1 | high-level-design（增加 rollback-plan.md） | 设计阶段补齐回滚方案。 | ✅ 已完成（V2.1） |
| P1 | detailed-design / interface-first-dev / task-breakdown（新增） | 设计到开发的核心链路 Skill。 | ✅ 已完成（V2.2~V2.3） |
| P1 | release-management（新增） | 补齐"开发完成 → 上线交付"的最后一公里。 | ✅ 已完成（V2.4） |
| P2 | unit-test / integration-test（新增） | 测试链路核心 Skill。 | ✅ 已完成（V2.2~V2.3） |
| P2 | monitoring-setup + monitoring-analysis（新增） | 长期价值大，可观测性闭环。 | ✅ 已完成（V2.1 / V2.4） |
| P2 | self-check / requesting-code-review / prd-generation（增强） | 质量门控与审查追溯增强。 | ✅ 已完成（V2.1~V2.4） |
| P2 | code-review（删除，能力合并） | 消除与 requesting-code-review 的触发词冲突。 | ✅ 已完成（V2.4） |

---

## 五、与现有 Skill 目录的映射关系

| 工具链 Skill 名 | 项目现有目录 | 备注 |
|----------------|-------------|------|
| progress-tracker | `skills/sdlc/progress-tracker/` | 已增强（V2.1） |
| brainstorming | `skills/sdlc/brainstorming/` | 直接可用 |
| competitive-analysis | `skills/sdlc/competitive-analysis/` | 直接可用（positioning + technical 双模式） |
| prd-generation | `skills/sdlc/prd-generation/` | 已增强（V2.1） |
| human | `skills/sdlc/human/` | 直接可用（Gate 1/2.5/2/3 统一载体） |
| detailed-requirements | `skills/sdlc/detailed-requirements/` | 已增强（V2.1，含 interaction-spec.md） |
| high-level-design | `skills/sdlc/high-level-design/` | 已增强（V2.1，含 rollback-plan.md） |
| monitoring-setup | `skills/sdlc/monitoring-setup/` | 直接可用（V2.1） |
| detailed-design | `skills/sdlc/detailed-design/` | 直接可用（V2.3，三级门控） |
| interface-first-dev | `skills/sdlc/interface-first-dev/` | 直接可用 |
| task-breakdown | `skills/sdlc/task-breakdown/` | 直接可用 |
| writing-plans | `skills/sdlc/writing-plans/` | 直接可用 |
| executing-plans | `skills/sdlc/executing-plans/` | 直接可用 |
| test-driven-development (tdd) | `skills/sdlc/test-driven-development/` | 直接可用（executing-plans 内循环） |
| systematic-debugging | `skills/sdlc/systematic-debugging/` | 直接可用（横向故障排查） |
| unit-test | `skills/sdlc/unit-test/` | 直接可用 |
| integration-test | `skills/sdlc/integration-test/` | 直接可用 |
| uat-verification | `skills/sdlc/uat-verification/` | 直接可用（V2.4） |
| requesting-code-review | `skills/sdlc/requesting-code-review/` | 已增强（V2.4，含通用审查维度） |
| release-management | `skills/sdlc/release-management/` | 直接可用（V2.4） |
| finish | `skills/sdlc/finish/` | 已增强（V2.1，归档范围扩大） |
| monitoring-analysis | `skills/sdlc/monitoring-analysis/` | 直接可用（V2.4） |
| self-check | `skills/sdlc/self-check/` | 已增强（V2.3，阶段 4 检查 + 变更影响分析） |
| git-automation | `skills/sdlc/git-automation/` | 直接可用（横向） |
| requirement-analysis | `skills/sdlc/requirement-analysis/` | 非主线工具链 Skill，备用 |
| sql-optimization | `skills/data-engineering/sql-optimization/` | 数据工程分类，非 SDLC 主线 |
| skill-based-architecture | `skills/Reverse-Engineering/skill-based-architecture/` | 元技能，非工具链主线 |
| documentation | `skills/engineering-foundations/documentation/` | 工程基础分类，非 SDLC 主线 |
| ~~code-review~~ | ~~已删除~~ | ~~能力并入 requesting-code-review（V2.4）~~ |

---

*本文档随工具链迭代持续更新。新增或修改 Skill 后，应同步更新本清单、根目录 `index.json` 与各 Skill 的 `meta.json`。*
