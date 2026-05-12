# AI项目落地工具链使用手册

> 工具集成方式 + 完全手动方式完整指南
> 版本 V2.1 | 2026年5月
>
> 本次更新基于 `lifesycle.md` 审查意见，补充 UAT、发布、监控环节，明确四道人工闸门（Gate 1/2.5/2/3），增加 `human` Skill 统一记录人工决策。
>
> **V2.2 更新（2026年5月）**：重构计划与执行阶段，引入 `writing-plans` → `task-breakdown` → `executing-plans` 三级递进工作流。
> - `writing-plans` 从 Superpowers 原生 micro-step 升级为**模块级实现计划**（plan.md），增加 Self-Review 四检与 Plan → Task 转换建议
> - `task-breakdown` **新增**，按 ≤30 分钟/任务粒度将 plan.md 拆解为 Phase 组织的 tasks.md，支持垂直切片与执行模式建议
> - `executing-plans` 增强 **Batch 执行**（3 任务/批次）、**Gate Non-Collapse Rule**（自测/接口校验/单测独立门控）、**自动勾选 tasks.md**、**Inline Audit** 与 **Simplicity First / Scope Discipline / Rollback-Friendly** 执行纪律

---

## 目录

- [一、系统要求与环境准备](#一系统要求与环境准备)
  - [1.1 必备工具](#11-必备工具)
  - [1.2 目录结构初始化](#12-目录结构初始化)
  - [1.3 Skill 安装清单](#13-skill-安装清单)
- [二、核心概念：四道人工闸门](#二核心概念四道人工闸门)
- [三、工具集成方式（MCP Server模式）](#三工具集成方式mcp-server模式)
  - [3.1 三工具打通前提条件](#31-三工具打通前提条件)
  - [3.2 完整工作流程](#32-完整工作流程)
  - [3.3 各阶段操作指令](#33-各阶段操作指令)
- [四、完全手动方式（无 MCP Server）](#四完全手动方式无-mcp-server)
- [五、人工参与规范（新增）](#五人工参与规范新增)
  - [5.1 人工角色的五层定义](#51-人工角色的五层定义)
  - [5.2 人工指令集](#52-人工指令集)
  - [5.3 签字文件模板](#53-签字文件模板)
- [六、常见问题与排除](#六常见问题与排除)

---

## 一、系统要求与环境准备

### 1.1 必备工具

| 工具 | 作用 | 安装方式 |
|------|------|----------|
| Kimi Code | AI 编程引擎，提供智能决策和代码生成 | kimi.com/code 下载 |
| OpenSpec | 规格驱动开发框架，管理变更生命周期 | `npm i -g @fission-ai/openspec` |
| Superpowers | AI 编码技能框架，提供结构化工作流 | GitHub 克隆 |

### 1.2 目录结构初始化

在开始使用之前，需要创建以下目录结构：

```bash
# OpenSpec 核心目录
mkdir -p openspec/{specs,changes,archive,schemas/{项目名}/templates}

# Superpowers Skill 目录
mkdir -p .kimi/skills/

# AI 产出物目录
mkdir -p docs/ai-output

# 测试目录
mkdir -p tests/{unit,integration}

# 运维基础设施目录（V2.1 新增）
mkdir -p ops/
```

### 1.3 Skill 安装清单

> 详细 Skill 状态与衔接关系见 `docs/AI项目工具链Skill清单与状态.md`。

---

## 二、核心概念：四道人工闸门

本工具链将人工参与从"建议性"改为**阻塞性**——AI 执行到闸门处暂停，必须获得人工信号才能继续。

| 闸门 | 名称 | 所在阶段 | 人工动作 | Skill 辅助动作 |
|------|------|----------|----------|----------------|
| 🚪 Gate 1 | 需求冻结闸 | 概要需求完成后 | 评审并签字 specs/01-05.md | `human` 记录决策，`self-check` 预检 |
| 🚪 Gate 2.5 | 原型冻结闸 | 详细需求完成后 | 逐页确认 interaction-spec.md 中每个按钮的交互状态机 | `human` 记录决策，`detailed-requirements` 生成交互规格模板 |
| 🚪 Gate 2 | 设计冻结闸 | 概要设计完成后 | 评审架构 + 确认 rollback-plan.md | `human` 记录决策，`self-check` 预检 |
| 🚪 Gate 3 | 发布冻结闸 | UAT 完成后 | 在预览环境走通完整业务流程，确认 uat-report.md | `human` 记录决策，`uat-verification` 生成检查清单 |

**关键规则**：每个 🚪 闸门处，AI 必须暂停并等待人工输入，不能自动进入下一阶段。

---

## 三、工具集成方式（MCP Server模式）

### 3.1 三工具打通前提条件

工具集成方式需要满足以下前提条件：

- **MCP 协议支持：** Kimi Code 支持 MCP Client 模式，能够通过 MCP 协议与外部服务通信。
- **OpenSpec MCP Server：** OpenSpec 提供 MCP Server，暴露 propose、apply、archive、verify 等 tools。
- **Superpowers MCP Server：** Superpowers 提供 MCP Server，暴露 brainstorming、writing-plans、executing-plans、tdd 等 tools。
- **配置文件：** `openspec/config.yaml` 已创建并配置完毕。
- **人工闸门配置：** `human` Skill 的 `config.yaml` 已定义 Gate 规则与阻塞策略。

### 3.2 完整工作流程

在工具集成模式下，整个工作流程如下（V2.1 已按 `lifesycle.md` 建议补充 UAT、发布、监控与人工闸门）：

1. **初始化 ——** 通过 `progress-tracker` 初始化项目目录、配置文件和运维基础设施（`ops/` 目录）
2. **变更提案 ——** 使用 `/opsx:propose` 创建变更提案
3. **需求探索 ——** 调用 `brainstorming` 进行需求探索
4. **市场定位（可选）——** 调用 `competitive-analysis mode=positioning` 执行市场定位与差异化分析
5. **概要需求 ——** 调用 `prd-generation` 生成概要需求文档
6. **🚪 Gate 1：需求冻结 ——** 人工评审签字，调用 `human gate=Gate1 action=sign-off`
7. **详细需求 ——** 调用 `detailed-requirements` 生成模块化详细需求（含 `interaction-spec.md`）
8. **🚪 Gate 2.5：原型冻结 ——** 人工逐页确认按钮交互，调用 `human gate=Gate2.5 action=sign-off`
9. **技术竞品分析 ——** 调用 `competitive-analysis mode=technical` 执行技术深度对比
10. **概要设计 ——** 调用 `high-level-design` 生成系统架构设计（含 `rollback-plan.md`）
11. **监控初始化 ——** 调用 `monitoring-setup` 生成监控规则初稿（一次性）
12. **🚪 Gate 2：设计冻结 ——** 人工评审架构，调用 `human gate=Gate2 action=sign-off`
13. **详细设计 ——** 调用 `detailed-design` 按模块输出详细设计
14. **接口驱动 ——** 调用 `interface-first-dev` 定义前后端接口契约
15. **编写实现计划 ——** 调用 `writing-plans` 生成模块级实现计划（plan.md）
16. **任务拆解 ——** 调用 `task-breakdown` 基于 plan.md 和接口契约，将工作拆解为≤30分钟/任务的开发清单（tasks.md）
17. **编码实现 ——** 调用 `executing-plans` 按 tasks.md 逐 Batch 执行开发任务（含强制自测、接口校验、自动勾选），内部调用 `test-driven-development` 遵循 RED-GREEN-REFACTOR 循环
18. **单元测试 ——** 调用 `unit-test` 生成并执行单元测试（覆盖率≥70%）
19. **集成测试 ——** 调用 `integration-test` 生成并执行集成测试（含 `user-stories-checklist.md`）
20. **UAT 验证 ——** 调用 `uat-verification` + 人工在预览环境走通业务流程
21. **🚪 Gate 3：发布冻结 ——** 人工确认 UAT 通过，调用 `human gate=Gate3 action=sign-off`
22. **代码审查 ——** 调用 `requesting-code-review` 输出结构化审查报告（含 design.md 设计偏差分析、tasks.md 任务追溯矩阵、UAT 交叉验证）
23. **上线发布 ——** 调用 `release-management` 生成发布清单，人工最终确认后上线
24. **归档收尾 ——** 调用 `finish` 执行八步归档流水线（人工确认 → 分支合并 → OpenSpec 归档 → 规格同步 → 纳入交付后文档 → CHANGELOG → 一致性校验 → 确认单）
25. **线上监控 ——** 周期性调用 `monitoring-analysis`，输出 `feedback-loop.md` 反哺下一变更

### 3.3 各阶段操作指令

#### 阶段 0：初始化项目

```bash
# 初始化 OpenSpec 目录结构
npx @fission-ai/openspec@latest init

# 初始化项目配置（V2.1：增加 ops/ 目录与运维基础设施骨架）
/skill:progress-tracker 初始化项目目录
```

产出：`openspec/config.yaml` + `ops/` 目录（`staging-config.yaml`、`rollback-plan.md` 模板、`monitoring-rules.yaml` 骨架）+ `progress.md`

---

#### 阶段 1：需求探索

```bash
# 1. 创建变更提案
/opsx:propose "描述你的变更需求"

# 2. 调用 Superpowers 的 brainstorming
/skill:brainstorming 请读取变更提案：@openspec/changes/{变更名}/proposal.md
在此基础上进行需求探索。资料来源：自动搜索网络 + 读取本地项目文档

# 3. 更新进度
/skill:progress-tracker 请更新进度
```

产出：`openspec/changes/{变更名}/proposal.md` + 需求探索记录

---

#### 阶段 1.5：市场定位分析（可选但推荐）

```bash
# 调用 competitive-analysis 的 positioning 模式
/skill:competitive-analysis mode=positioning 请基于需求探索结果，执行市场定位竞品分析。

分析目标：{基于需求草案中的模块初分}
问题类型：market_entry | positioning
参考文档：@openspec/changes/{变更名}/brainstorming/requirement-draft.md
```

产出：`openspec/changes/{变更名}/brainstorming/market-positioning.md`

---

#### 阶段 2：生成概要需求

```bash
# 调用 prd-generation
/skill:prd-generation 基于 brainstorming 结果，生成概要需求。
参考文档：@openspec/changes/{变更名}/proposal.md

# 更新进度
/skill:progress-tracker 请更新进度
```

产出：`specs/` 目录下的 5 个 Markdown 文件：`01-product-overview.md`、`02-requirements-list.md`、`03-functional-structure.md`、`04-business-rules.md`、`05-non-functional.md`

**末尾 AI 提示语（V2.1 新增）：**
```text
========================================
🚪 Gate 1: 需求冻结 —— 等待人工评审
========================================
产出物已保存至：@openspec/changes/{变更名}/specs/
请执行以下操作：
1. 阅读 5 个 spec 文件
2. 如有修改意见，直接编辑文件或在对话中提出
3. 确认无误后，执行：/skill:human gate=Gate1 action=sign-off
```

---

#### 🚪 Gate 1：需求冻结

```bash
# 人工阅读并确认后
/skill:human gate=Gate1 action=sign-off result=passed issues="遗留问题清单（如有）"

# 或：有条件通过
/skill:human gate=Gate1 action=conditional result=passed issues="P1: xxx待补充"

# 或：驳回
/skill:human gate=Gate1 action=reject reason="概要需求偏差描述"
```

产出：`openspec/changes/{变更名}/human-decisions.md` + `sign-off/01-requirements.md`

---

#### 阶段 2.5：生成详细需求

```bash
# 默认模式（批量标准化，推荐）
/skill:detailed-requirements 基于概要需求，按模块独立输出详细需求。
从 P0 模块开始，逐个模块输出。

# 单模块深度模式（模块数 ≤3 或需穷尽式人工协作时）
/skill:detailed-requirements 基于概要需求，对 feature-01-{模块名} 使用单模块深度模式。
```

产出：每个模块一个独立目录 `feature-XX-{模块名}/`，包含：
- `spec.md` — 需求追溯与验收标准
- `prototype.md` — 页面原型（文字化布局）
- `io-table.md` — 输入输出字段表
- `logic.md` — 业务逻辑与状态机
- **`interaction-spec.md`（V2.1 新增）** — 按钮级交互规格（触发方式、前置条件、立即反馈、成功/失败结果、异常分支、埋点事件）

**末尾 AI 提示语（V2.1 新增）：**
```text
========================================
🚪 Gate 2.5: 原型冻结 —— 等待人工逐页确认
========================================
请打开各模块的 interaction-spec.md，检查每个页面是否包含：
- [ ] 每个可交互元素的说明（按钮、输入框、下拉框）
- [ ] 交互状态机：点击前 → 点击中（loading） → 点击后（成功/失败）
- [ ] 异常分支：网络中断、权限不足、数据为空时的页面表现
- [ ] 页面间跳转关系
确认后执行：/skill:human gate=Gate2.5 action=sign-off
```

---

#### 🚪 Gate 2.5：原型冻结

```bash
/skill:human gate=Gate2.5 action=sign-off result=passed issues=""
```

产出：`sign-off/02.5-prototype.md`

---

#### 阶段 3 前置：技术竞品分析

```bash
# 调用 competitive-analysis 的 technical 模式
/skill:competitive-analysis mode=technical 请自动搜索相关竞品，执行技术深度对比分析。

分析维度：角色数据模型设计、核心功能流程、技术选型、集成方式
参考文档：@openspec/changes/{变更名}/specs/

/skill:progress-tracker 请更新进度
```

产出：`openspec/changes/{变更名}/design/competitive-analysis.md` + `design-input.md`

---

#### 阶段 3：概要设计

```bash
# 调用 high-level-design 生成概要设计
/skill:high-level-design 生成概要设计。
参考文档：@openspec/changes/{变更名}/specs/
@openspec/changes/{变更名}/design/competitive-analysis.md
@openspec/changes/{变更名}/design/design-input.md

# 生成监控规则初稿（一次性）
/skill:monitoring-setup 基于运维架构章节，生成 monitoring-rules.yaml 初稿。
```

产出：`design/` 目录下的 16 个 Markdown 文件 + **`rollback-plan.md`（V2.1 新增）** + `monitoring-rules.yaml`

**末尾 AI 提示语（V2.1 新增）：**
```text
========================================
🚪 Gate 2: 设计冻结 —— 等待人工评审
========================================
请评审：
1. 技术选型是否符合团队现有技术债
2. 数据流与部署架构是否合理
3. rollback-plan.md 中的回滚步骤是否可操作
确认后执行：/skill:human gate=Gate2 action=sign-off
```

---

#### 🚪 Gate 2：设计冻结

```bash
/skill:human gate=Gate2 action=sign-off result=passed issues=""
```

产出：`sign-off/02-design.md`

---

#### 阶段 4：详细设计

```bash
/skill:detailed-design 按模块输出详细设计。
参考文档：@openspec/changes/{变更名}/design/
@openspec/changes/{变更名}/specs/feature-*/

/skill:self-check 详细设计
```

产出：每个模块目录下增加 `design.md`、`api-spec.md`、`db-schema.md`、`state-machine.md`、`test-plan.md`

---

#### 阶段 5：接口驱动开发

```bash
/skill:interface-first-dev 基于详细设计定义前后端接口契约。
生成：OpenAPI/Swagger + Mock数据 + 并行开发计划

/skill:self-check 接口契约
```

产出：`interface-contracts/` 目录下的 `openapi.yaml`、`mock-data.json`、`mock-server-config.md`、`parallel-dev-plan.md`

---

#### 阶段 5.5：编写实现计划（新增）

```bash
/skill:writing-plans 基于详细设计和接口契约，生成模块级实现计划。
参考：@openspec/changes/{变更名}/specs/feature-*/design.md
@openspec/changes/{变更名}/interface-contracts/openapi.yaml

/skill:self-check 实现计划
```

产出：`openspec/changes/{变更名}/plan.md`

**plan.md 核心内容：**
- Goal + Architecture + Tech Stack
- Module Breakdown（每个模块的实现顺序、关键决策、依赖关系、验收标准）
- 全局任务依赖总图（Mermaid DAG）
- **Plan → Task 转换建议**（指导 task-breakdown 的 Phase 划分与任务数估算）

**末尾 AI 提示语：**
```text
========================================
Plan 已生成，下一步 REQUIRED: task-breakdown
========================================
Plan 已保存至：@openspec/changes/{变更名}/plan.md

请确认 plan.md 中的以下内容：
1. 模块划分是否与详细设计一致
2. 技术选型是否可执行
3. 验收标准是否可验证

确认无误后，执行：/skill:task-breakdown 将 Plan 转换为可执行任务清单。
```

---

#### 阶段 6：任务拆解

```bash
/skill:task-breakdown 基于 plan.md 和接口契约，生成开发任务清单。
原则：每个任务 ≤ 30 分钟，垂直切片优先，标签明确

参考：@openspec/changes/{变更名}/plan.md
@openspec/changes/{变更名}/interface-contracts/openapi.yaml
```

产出：`openspec/changes/{变更名}/tasks.md`，按 Phase 组织

---

#### 阶段 7：编码实现

```bash
/skill:executing-plans 按 tasks.md 逐 Batch 执行开发任务。
约束：Batch 大小=3、强制自测、接口校验、Rollback-Friendly Commit

参考：@openspec/changes/{变更名}/tasks.md
@openspec/changes/{变更名}/specs/feature-*/design.md
@openspec/changes/{变更名}/interface-contracts/openapi.yaml
```

**执行纪律（新增）：**
- **Simplicity First**：先写最简单可行方案
- **Scope Discipline**：严禁顺手重构，发现相邻问题记入 `NOTICED BUT NOT TOUCHING`
- **Rollback-Friendly**：优先新增文件，禁止同一 commit 既删又替
- **Gate Non-Collapse**：自测、接口校验、单测三个门控必须独立执行，禁止合并

---

#### 阶段 8：单元测试

```bash
/skill:unit-test 为已完成的模块生成单元测试。
要求：覆盖率 ≥ 70%，独立运行

# 运行单元测试
pytest tests/unit/ -v --cov={模块路径} --cov-report=term-missing

/skill:self-check 单元测试
```

产出：`tests/unit/` 目录 + 覆盖率报告

---

#### 阶段 9：集成测试

```bash
/skill:integration-test 生成集成测试，覆盖端到端主链路场景。
参考文档：@openspec/changes/{变更名}/specs/feature-*/spec.md
@openspec/changes/{变更名}/interface-contracts/openapi.yaml

/skill:self-check 集成测试
```

产出：`tests/integration/` 目录 + **`user-stories-checklist.md`（V2.1 新增，供 UAT 使用）**

---

#### 阶段 9.5：UAT 与业务流程验证（V2.1 新增）

```bash
# AI 辅助生成测试清单
/skill:uat-verification 基于详细需求中的用户故事，执行业务流程验证。
验证清单：@openspec/changes/{变更名}/specs/feature-*/user-stories.md
环境：staging / preview 部署
```

**人工操作（必须，不可替代）：**
1. 打开预览环境地址
2. 按 `user-stories-checklist.md` 逐个执行：
   - 正向流程：按用户故事完整走通
   - 异常分支：重复名称、超长输入、网络中断恢复
   - 权限验证：未登录访问、越权操作
3. 记录问题到 `uat-issues.md`
4. 严重问题 → 退回开发；轻微问题 → 记入下一迭代

```bash
/skill:progress-tracker 请更新进度
/skill:self-check UAT验证
```

产出：`openspec/changes/{变更名}/uat/uat-report.md`（通过/不通过/遗留问题/严重级别）

**末尾 AI 提示语：**
```text
========================================
🚪 Gate 3: 发布冻结 —— 等待人工走通确认
========================================
请在预览环境按 user-stories-checklist.md 逐个操作。
确认所有 P0 用户故事已验证通过后，执行：
/skill:human gate=Gate3 action=sign-off
```

---

#### 🚪 Gate 3：发布冻结

```bash
/skill:human gate=Gate3 action=sign-off result=passed issues=""
```

产出：`sign-off/03-release.md`

---

#### 阶段 10：代码审查

```bash
/skill:requesting-code-review 对已完成的代码进行审查。
参考：
  - @openspec/changes/{变更名}/tasks.md（任务追溯基准）
  - @openspec/changes/{变更名}/specs/feature-*/design.md（设计对齐基准）
  - @openspec/changes/{变更名}/uat-report.md（UAT 交叉验证）
```

产出： **`code-review-report.md`（V2.1 增强）** —— 结构化记录：
- 总体结论（通过 / 有条件通过 / 不通过）
- 阻塞性问题清单
- 实现与设计偏差分析（对比 design.md）
- 任务追溯矩阵（审查意见 ↔ tasks.md 任务编号）
- UAT 交叉验证结果

**不通过时的处理：**
- 生成 `rework-tasks.md`
- 返回 `executing-plans` 修复阻塞性问题
- 修复完成后重新触发 `requesting-code-review`

---

#### 阶段 10.5：上线发布（V2.1 新增）

```bash
# AI 辅助生成发布清单
/skill:release-management 准备上线发布。
输入：
  - uat-report.md（通过）
  - code-review-report.md（通过）
  - rollback-plan.md（来自阶段 3）
  - 代码分支/commit SHA

# 人工最终决策（必须）
# 严禁 AI 自动执行生产发布
```

产出：`release-notes.md` + `release-checklist.md` + 生产部署确认单

**关键安全规则：**
- AI 只负责生成文档和检查项
- 上线按钮必须由人按
- 发布窗口、回滚方案确认由人工最终决策

---

#### 阶段 11：归档收尾

```bash
# 必须等待人工确认上线成功后方可执行
/skill:finish
```

**Step 0 人工确认（严禁自动执行）：**
```text
请输入 "确认归档" 继续归档收尾流程。
```

**八步归档流水线：**
1. **分支合并**：开发分支合并到主分支，生成合并报告
2. **临时文件清理**：删除 `.kimi/temp-tests/`、`.kimi/temp-builds/` 等
3. **OpenSpec 归档**：将全部产物复制到 `openspec/changes/archive/{变更名}/`
4. **增量规格合并**（`/opsx:sync`）：追加到主规格，保留历史谱系
5. **纳入交付后文档**：uat-report.md + release-notes.md + human-decisions.md + code-review-report.md
6. **生成 CHANGELOG.md**：遵循 Keep a Changelog 规范，追加到根目录
7. **最终一致性校验**（`self-check` 归档版）：8 项检查清单，全过方可继续
8. **输出归档完成确认单**：记录归档路径、合并 SHA、校验结果

**强制归档的 7 类文档：**
- specs/（设计文档）
- tasks.md（任务清单）
- uat-report.md（UAT 报告）
- release-notes.md（发布说明）
- human-decisions.md（人工决策记录）
- code-review-report.md（代码审查报告）
- merge-report.md（分支合并报告）

---

#### 阶段 12：线上监控（V2.1 新增，周期性）

```bash
# 周期性运行（建议每周一次）
/skill:monitoring-analysis 生成本周健康报告。
输入：
  - 运行时日志/告警（Sentry/Prometheus）
  - 埋点数据
  - monitoring-rules.yaml
```

产出：`monitoring-dashboard.md` + `feedback-loop.md`

**闭环规则：** `feedback-loop.md` 输入到下一变更的 `brainstorming` 阶段，形成从监控到需求的闭环。

---

## 四、完全手动方式（无 MCP Server）

当 MCP Server 不可用时（网络不通、服务未部署或权限不足），可通过手动方式按顺序执行命令完成全生命周期操作。

**适用场景**：
- 前期环境搭建阶段，MCP Server 尚未部署
- 网络受限环境（内网、离线场景）
- 偏好纯命令行手动控制的团队

**核心原则**：
- 每个命令按固定顺序执行，不能跳过或并行
- 每个命令的输出作为下一个命令的输入
- **每个 Gate 完成后需要人工确认签字后才能进入下一阶段**
- 自查环节必不可少，确保产出物质量

**完整命令速查表**：

| 步骤 | 命令 | 说明 | 产出物 | 人工闸门 |
|------|------|------|--------|----------|
| 0 | progress-tracker | 初始化目录结构 | config.yaml + ops/ | — |
| 1 | /opsx:propose + brainstorming | 创建提案 + 需求探索 | proposal.md + 探索记录 | — |
| 1.5 | competitive-analysis | 市场定位分析（可选） | market-positioning.md | — |
| 2 | prd-generation | 生成概要需求 | 01-05.md | 🚪 Gate 1 |
| 2.5 | detailed-requirements | 生成详细需求 | feature-*/ | 🚪 Gate 2.5 |
| 3 前置 | competitive-analysis | 技术竞品分析 | CA.md + design-input.md | — |
| 3 | high-level-design | 概要设计 | design/*.md + rollback-plan.md | 🚪 Gate 2 |
| 3.5 | monitoring-setup | 监控初始化（一次性） | monitoring-rules.yaml | — |
| 4 | detailed-design | 详细设计 | feature-*/design.md | — |
| 5 | interface-first-dev | 接口驱动 | openapi.yaml | — |
| 5.5 | writing-plans | 编写实现计划 | plan.md | — |
| 6 | task-breakdown | 任务拆解 | tasks.md | — |
| 7 | executing-plans | 编码实现 | 代码文件 | — |
| 8 | unit-test | 单元测试 | tests/unit/ | — |
| 9 | integration-test | 集成测试 | tests/integration/ + checklist.md | — |
| 9.5 | uat-verification | UAT 验证 | uat-report.md | 🚪 Gate 3 |
| 10 | requesting-code-review | 代码审查 | code-review-report.md（含 design 对比、任务追溯） | — |
| 10.5 | release-management | 上线发布 | release-notes.md | 人工最终决策 |
| 11 | finish | 归档收尾 | archive/ + CHANGELOG.md + 确认单 | — |
| 12 | monitoring-analysis | 线上监控（周期性） | dashboard.md | — |

> 📄 **详细命令、参数和人工操作步骤见独立文档**：
> [`docs/AI项目落地工具链_完全手动操作手册.md`](./AI项目落地工具链_完全手动操作手册.md)

---

## 五、人工参与规范（新增）

### 5.1 人工角色的五层定义

在不同阶段，人工承担不同角色：

| 阶段 | 人工角色 | 核心动作 | 体现形式 |
|------|----------|----------|----------|
| 需求 | 校准者 | 提供业务背景、纠正用户画像偏差、删减和聚焦 | 在对话中直接回复修正意见 |
| 设计 | 约束施加者 | 评审技术选型、施加"什么不能做"的约束 | sign-off 文件中注明限制条件 |
| 开发 | 抽查者 | Review 关键算法和安全相关代码、抽查覆盖率 | 对话中 @ 具体文件提问 |
| 测试/UAT | 体验者 | 在预览环境亲自点击每个页面走通业务流程 | uat-report.md 记录体验问题 |
| 发布 | 最终决策人 | 确认发布窗口、检查回滚方案、按下最终按钮 | sign-off/03-release.md 签字 |

### 5.2 人工指令集

通过 `human` Skill 显式触发人工介入：

| 指令格式 | 作用 | 使用场景 |
|----------|------|----------|
| `/skill:human gate={Gate} action=sign-off result=passed issues={遗留问题}` | 签字通过 | 每个 Gate 结束时 |
| `/skill:human gate={Gate} action=conditional result=passed issues={遗留问题}` | 有条件通过 | 存在可延期修复的问题时 |
| `/skill:human gate={Gate} action=reject reason={原因}` | 驳回重做 | 发现严重偏差时 |
| `/skill:human action=status` | 查询当前变更状态 | 随时查看卡在哪个 Gate |
| `/skill:human action=history` | 查询决策历史 | 追溯某变更的全部人工决策 |

### 5.3 签字文件模板

每个 Gate 对应一份不可篡改的签字文件，保存在 `openspec/changes/{变更名}/sign-off/` 目录下：

**Gate 1 模板（`01-requirements.md`）：**
```markdown
# 需求冻结签字单

## 变更信息
- 变更名：{变更名}
- 版本：{日期}-v{N}
- 评审日期：{日期}

## 评审对象
- specs/01-product-overview.md
- specs/02-requirements-list.md
- specs/03-functional-structure.md
- specs/04-business-rules.md
- specs/05-non-functional.md

## 评审结论
□ 通过 □ 有条件通过 □ 不通过

## 遗留问题
1. [P1] {问题描述}

## 签字
- 产品负责人：___________ 日期：___________
```

---

## 六、常见问题与排除

### 6.1 工具集成方式常见问题

**Q1：MCP Server 连接失败怎么办？**

A：检查网络连接，确认 MCP Server 已启动。可以使用命令 `mcp inspector` 进行诊断。如果仍然不能解决，切换到完全手动方式。

**Q2：Skill 识别不到怎么办？**

A：检查 Skill 目录是否正确，确认 `SKILL.md` 文件存在。尝试重启 Kimi Code 或重新加载 Skill。

**Q3：产出物保存路径错误怎么办？**

A：检查 `openspec/config.yaml` 中的 `auto_save.base_path` 配置，确认目录权限正确。

**Q4：人工闸门可以跳过吗？**

A：不可以。四道人工闸门是阻塞性的，未通过 `human` Skill 签字确认，AI 不应进入下一阶段。如果强行跳过，进度看板会标记为 🔴 异常。

### 6.2 手动方式常见问题

手动方式（无 MCP Server）的详细 FAQ（含命令示例、排查步骤、切换指引）见独立文档：

> 📄 [`docs/AI项目落地工具链_完全手动操作手册.md`](./AI项目落地工具链_完全手动操作手册.md)

### 6.3 通用问题

**Q3：需要多少人工干预？**

A：主要在以下节点需要人工确认：概要需求评审签字（Gate 1）、原型逐页确认（Gate 2.5）、架构评审与回滚方案确认（Gate 2）、UAT 业务流程走通（Gate 3）、发布窗口最终决策。其他环节由 AI 自主完成。

**Q4：按钮级交互规格为什么这么重要？**

A：对于强交互型产品，AI 可能只描述"点击生成按钮，系统生成剧本"，但不描述按钮加载态、失败态、页面跳转关系。这会导致前端开发凭经验猜测，上线后用户体验不一致。`interaction-spec.md` 强制要求每个交互元素的状态机必须完整。

---

AI项目落地工具链 | V2.1
