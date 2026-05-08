# AI项目落地工具链使用手册

> 工具集成方式 + 完全手动方式完整指南
> 版本 V2.1 | 2026年5月
>
> 本次更新基于 `lifesycle.md` 审查意见，补充 UAT、发布、监控环节，明确四道人工闸门（Gate 1/2.5/2/3），增加 `human` Skill 统一记录人工决策。

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
- [四、完全手动方式（无MCP Server）](#四完全手动方式无mcp-server)
  - [4.1 手动方式说明](#41-手动方式说明)
  - [4.2 完整命令执行流程](#42-完整命令执行流程)
  - [4.3 各阶段详细命令列表](#43-各阶段详细命令列表)
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

安装以下 Skill，本方案共需要 **23 个 Skill**（V2.1 从 18 个扩充至 23 个）：

| Skill名称 | 来源 | 当前状态 | 安装路径 |
|-----------|------|----------|----------|
| brainstorming | Superpowers | ✅ 可用 | .kimi/skills/superpowers/ |
| writing-plans | Superpowers | ✅ 可用 | .kimi/skills/superpowers/ |
| executing-plans | Superpowers | ✅ 可用 | .kimi/skills/superpowers/ |
| test-driven-development | Superpowers | ✅ 可用 | .kimi/skills/superpowers/ |
| systematic-debugging | Superpowers | ✅ 可用 | .kimi/skills/superpowers/ |
| requesting-code-review | Superpowers | 🔧 需修改 | .kimi/skills/superpowers/ |
| finishing-a-development-branch | Superpowers | ✅ 可用 | .kimi/skills/superpowers/ |
| prd-generation | 本方案 | 🔧 需修改 | .kimi/skills/prd-generation/ |
| progress-tracker | 本方案 | 🔧 需修改 | .kimi/skills/progress-tracker/ |
| self-check | 本方案 | 🔧 需修改 | .kimi/skills/self-check/ |
| competitive-analysis | 本方案 | ✅ 可用 | .kimi/skills/competitive-analysis/ |
| high-level-design | 本方案 | 🔧 需修改 | .kimi/skills/high-level-design/ |
| detailed-requirements | 本方案 | 🔧 需修改 | .kimi/skills/detailed-requirements/ |
| detailed-design | 本方案 | ➕ 需新增 | .kimi/skills/detailed-design/ |
| interface-first-dev | 本方案 | ➕ 需新增 | .kimi/skills/interface-first-dev/ |
| task-breakdown | 本方案 | ➕ 需新增 | .kimi/skills/task-breakdown/ |
| unit-test | 本方案 | ➕ 需新增 | .kimi/skills/unit-test/ |
| integration-test | 本方案 | ➕ 需新增 | .kimi/skills/integration-test/ |
| uat-verification | 本方案 | ➕ 需新增 | .kimi/skills/uat-verification/ |
| release-management | 本方案 | ➕ 需新增 | .kimi/skills/release-management/ |
| monitoring-setup | 本方案 | ➕ 需新增 | .kimi/skills/monitoring-setup/ |
| monitoring-analysis | 本方案 | ➕ 需新增 | .kimi/skills/monitoring-analysis/ |
| human | 本方案 | ➕ 需新增 | .kimi/skills/human/ |

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
15. **任务拆解 ——** 调用 `task-breakdown` 将工作拆解为≤30分钟/任务
16. **编码实现 ——** 调用 `executing-plans` + `tdd` 执行开发任务
17. **单元测试 ——** 调用 `unit-test` 生成并执行单元测试（覆盖率≥70%）
18. **集成测试 ——** 调用 `integration-test` 生成并执行集成测试（含 `user-stories-checklist.md`）
19. **UAT 验证 ——** 调用 `uat-verification` + 人工在预览环境走通业务流程
20. **🚪 Gate 3：发布冻结 ——** 人工确认 UAT 通过，调用 `human gate=Gate3 action=sign-off`
21. **代码审查 ——** 调用 `requesting-code-review` 输出结构化审查报告
22. **上线发布 ——** 调用 `release-management` 生成发布清单，人工最终确认后上线
23. **归档收尾 ——** 调用 OpenSpec 的 `archive` + Superpowers 的 `finishing-a-development-branch`
24. **线上监控 ——** 周期性调用 `monitoring-analysis`，输出 `feedback-loop.md` 反哺下一变更

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

#### 阶段 6：任务拆解

```bash
/skill:task-breakdown 基于详细设计和接口契约，生成开发任务清单。
原则：每个任务 ≤ 30 分钟
```

产出：`openspec/changes/{变更名}/tasks.md`，按 Phase 组织

---

#### 阶段 7：编码实现

```bash
/skill:executing-plans 按 tasks.md 逐个执行任务。
约束：符合项目编码规范 + 包含异常处理 + 完成后自测

# 每个任务完成后：
/skill:self-check 编码任务
```

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
参考：@openspec/changes/{变更名}/tasks.md
```

产出： **`code-review-report.md`（V2.1 新增）** —— 结构化记录通过/有条件通过/不通过结论及阻塞性问题清单

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
# 归档变更
/opsx:archive

# 最终自查
/skill:self-check 最终自查
```

说明：归档范围扩大（V2.1），纳入 `uat-report` + `release-notes` + `human-decisions.md`

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

## 四、完全手动方式（无MCP Server）

### 4.1 手动方式说明

当 MCP Server 不可用时（网络不通、服务未部署或权限不足），可以通过手动方式按顺序执行命令。手动方式的核心原则是：

- 每个命令按固定顺序执行，不能跳过或并行
- 每个命令的输出作为下一个命令的输入
- **每个 Gate 完成后需要人工确认签字后才能进入下一阶段（V2.1 强化）**
- 自查环节必不可少，确保产出物质量

### 4.2 完整命令执行流程

| 步骤 | 命令 | 说明 | 产出物 | 人工闸门 |
|------|------|------|--------|----------|
| 0 | progress-tracker | 初始化目录结构 | config.yaml + ops/ | — |
| 1 | /opsx:propose | 创建变更提案 | proposal.md | — |
| 1 | brainstorming | 需求探索 | 探索记录 | — |
| 1.5 | competitive-analysis | 市场定位分析（可选） | market-positioning.md | — |
| 2 | prd-generation | 生成概要需求 | 01-05.md | 🚪 Gate 1 |
| 2.5 | detailed-requirements | 生成详细需求 | feature-*/ | 🚪 Gate 2.5 |
| 3 前置 | competitive-analysis | 技术竞品分析 | competitive-analysis.md + design-input.md | — |
| 3 | high-level-design | 概要设计 | design/*.md + rollback-plan.md | 🚪 Gate 2 |
| 3.5 | monitoring-setup | 监控初始化（一次性） | monitoring-rules.yaml | — |
| 4 | detailed-design | 详细设计 | feature-*/design.md | — |
| 5 | interface-first-dev | 接口驱动 | openapi.yaml | — |
| 6 | task-breakdown | 任务拆解 | tasks.md | — |
| 7 | executing-plans | 编码实现 | 代码文件 | — |
| 8 | unit-test | 单元测试 | tests/unit/ | — |
| 9 | integration-test | 集成测试 | tests/integration/ + user-stories-checklist.md | — |
| 9.5 | uat-verification | UAT 验证 | uat-report.md | 🚪 Gate 3 |
| 10 | requesting-code-review | 代码审查 | code-review-report.md | — |
| 10.5 | release-management | 上线发布 | release-notes.md | 人工最终决策 |
| 11 | archive + finish | 归档收尾 | archive/ | — |
| 12 | monitoring-analysis | 线上监控（周期性） | monitoring-dashboard.md | — |

### 4.3 各阶段详细命令列表

#### 步骤 0：初始化变更目录（V2.1 增加 ops/ 目录）

```bash
# 1. 创建目录结构
mkdir -p openspec/{specs,changes,archive}
mkdir -p openspec/changes/{变更名}/{specs,design,uat,sign-off}
mkdir -p .kimi/skills/
mkdir -p docs/ai-output
mkdir -p tests/{unit,integration}
mkdir -p ops/                      # V2.1 新增

# 2. 创建配置文件 openspec/config.yaml
cat > openspec/config.yaml << 'EOF'
schema: {项目名}-sdd
version: "1.0"
context: |
  项目：{项目名称}
  技术栈：{前端框架} + {后端框架} + {数据库}
  规范：所有变更必须通过概要评审和详细评审
EOF

# 3. 创建运维基础设施骨架（V2.1 新增）
cat > ops/staging-config.yaml << 'EOF'
# 预发布环境配置模板
environment: staging
database: {连接串}
api_keys: {第三方API Key}
EOF

cat > ops/rollback-plan.md << 'EOF'
# 回滚方案模板
## 回滚触发条件
## 回滚步骤
## 数据库回滚脚本清单
## 灰度策略
EOF

# 4. 初始化进度跟踪
/skill:progress-tracker 初始化{项目名}项目目录
```

#### 步骤 1：创建变更提案

```bash
/opsx:propose "{变更描述}"
```

说明：创建 `openspec/changes/{变更名}/proposal.md`。

#### 步骤 1：需求探索

```bash
/skill:brainstorming 帮我脑暴一下，打算做个{产品描述}，
本地资料：@docs/ref/*.md

/skill:progress-tracker 请更新进度
```

#### 步骤 2：生成概要需求 + 🚪 Gate 1

```bash
/skill:prd-generation 基于 brainstorming 结果生成概要需求。
参考文档：@openspec/changes/*/proposal.md @docs/*/*

/skill:progress-tracker 请更新进度
/skill:self-check 概要需求
```

**人工操作（阻塞）：**
```bash
# 阅读 5 个 spec 文件后
/skill:human gate=Gate1 action=sign-off result=passed issues="遗留问题（如有）"
```

#### 步骤 2.5：生成详细需求 + 🚪 Gate 2.5

```bash
/skill:detailed-requirements 基于概要需求，按模块输出详细需求。
参考文档：@openspec/changes/{变更名}/specs/01-*.md
@openspec/changes/{变更名}/specs/03-*.md

/skill:progress-tracker 请更新进度
```

产出：每个模块包含 `spec.md`、`prototype.md`、`io-table.md`、`logic.md`、`interaction-spec.md`。

**人工操作（阻塞）：**
```bash
# 逐页确认 interaction-spec.md 中每个按钮的交互状态机
/skill:human gate=Gate2.5 action=sign-off result=passed issues=""
```

#### 步骤 3 前置：技术竞品分析

```bash
/skill:competitive-analysis mode=technical 请自动搜索相关竞品，执行技术深度对比分析。

分析维度：角色数据模型设计、核心功能流程、技术选型、集成方式
参考文档：@openspec/changes/{变更名}/specs/

/skill:progress-tracker 请更新进度
```

#### 步骤 3：概要设计 + 🚪 Gate 2

```bash
/skill:high-level-design 生成概要设计。
参考：@openspec/changes/{变更名}/specs/
@openspec/changes/{变更名}/design/competitive-analysis.md
@openspec/changes/{变更名}/design/design-input.md

/skill:self-check 概要设计
```

产出：`design/` 目录下的 16 个 Markdown 文件 + `rollback-plan.md`。

**人工操作（阻塞）：**
```bash
# 评审架构 + 确认 rollback-plan.md
/skill:human gate=Gate2 action=sign-off result=passed issues=""
```

#### 步骤 4：详细设计

```bash
/skill:detailed-design 按模块输出详细设计。
参考：@openspec/changes/{变更名}/design/
@openspec/changes/{变更名}/specs/feature-*/

/skill:self-check 详细设计
```

产出：每个模块目录下增加 `design.md`、`api-spec.md`、`db-schema.md`、`state-machine.md`、`test-plan.md`。

#### 步骤 5：接口驱动开发

```bash
/skill:interface-first-dev 基于详细设计定义前后端接口契约。
参考：@openspec/changes/{变更名}/specs/feature-*/api-spec.md
@openspec/changes/{变更名}/specs/feature-*/db-schema.md

/skill:self-check 接口契约
```

#### 步骤 6：任务拆解

```bash
/skill:task-breakdown 基于详细设计和接口契约，生成开发任务清单。
参考：@openspec/changes/{变更名}/specs/feature-*/design.md
@openspec/changes/{变更名}/interface-contracts/openapi.yaml
```

产出：`openspec/changes/{变更名}/tasks.md`。

#### 步骤 7：编码实现

```bash
# 对每个任务执行：
/skill:executing-plans 执行任务 {任务ID}。
参考：@openspec/changes/{变更名}/tasks.md
@openspec/changes/{变更名}/specs/feature-*/design.md

# 每个任务完成后：
/skill:self-check 编码任务
```

#### 步骤 8：单元测试

```bash
/skill:unit-test 为已完成的模块生成单元测试。
参考：@openspec/changes/{变更名}/specs/feature-*/test-plan.md

pytest tests/unit/ -v --cov={模块路径} --cov-report=term-missing

/skill:self-check 单元测试
```

#### 步骤 9：集成测试

```bash
/skill:integration-test 生成集成测试。
参考：@openspec/changes/{变更名}/specs/feature-*/spec.md
@openspec/changes/{变更名}/interface-contracts/openapi.yaml

/skill:self-check 集成测试
```

产出：`tests/integration/` + `user-stories-checklist.md`。

#### 步骤 9.5：UAT 验证 + 🚪 Gate 3

```bash
/skill:uat-verification 基于用户故事生成 UAT 检查清单。
参考：@openspec/changes/{变更名}/specs/feature-*/user-stories.md
```

**人工操作（阻塞，必须）：**
1. 在预览环境按 `user-stories-checklist.md` 逐项操作
2. 记录问题
3. 确认通过后执行：

```bash
/skill:human gate=Gate3 action=sign-off result=passed issues=""
```

产出：`uat-report.md`。

#### 步骤 10：代码审查

```bash
/skill:requesting-code-review 对已完成的代码进行审查。
```

产出：`code-review-report.md`。

#### 步骤 10.5：上线发布

```bash
/skill:release-management 准备发布。
```

**人工操作（阻塞，最终决策）：**
- 确认发布窗口
- 检查回滚方案
- 人工执行最终发布命令（AI 不自动执行生产发布）

产出：`release-notes.md` + `release-checklist.md`。

#### 步骤 11：归档收尾

```bash
/skill:requesting-code-review
/opsx:archive
/skill:self-check 最终自查
```

#### 步骤 12：线上监控（周期性）

```bash
/skill:monitoring-analysis 生成本周健康报告。
```

产出：`monitoring-dashboard.md` + `feedback-loop.md` → 输入下一变更 `brainstorming`。

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

**Q1：可以跳过某些阶段吗？**

A：不建议。每个阶段的产出物都是下一个阶段的输入，跳过会导致产出物质量下降。特殊情况下可以简化某个阶段，但不建议完全跳过。

**Q2：自查失败怎么办？**

A：根据自查报告修复问题，修复后重新执行自查。如果是内容不一致问题，需要回到上游阶段修复。

**Q3：多个变更可以并行进行吗？**

A：不建议。手动方式下应该一次只处理一个变更，避免上下文混淆。

**Q4：UAT 发现严重问题怎么办？**

A：立即驳回。执行 `/skill:human gate=Gate3 action=reject reason="{问题描述}"`，AI 会自动生成 `rework-tasks.md`，修复后重新申请 Gate3 sign-off。

### 6.3 通用问题

**Q1：如何切换两种方式？**

A：在工具集成方式下，如果 MCP Server 不可用，系统会自动提示切换到手动方式。也可以通过命令 `/mode:manual` 手动切换。

**Q2：两种方式的产出物兼容吗？**

A：兼容。两种方式产生的文档格式和目录结构完全一致，可以在任何时候切换。

**Q3：需要多少人工干预？**

A：主要在以下节点需要人工确认：概要需求评审签字（Gate 1）、原型逐页确认（Gate 2.5）、架构评审与回滚方案确认（Gate 2）、UAT 业务流程走通（Gate 3）、发布窗口最终决策。其他环节由 AI 自主完成。

**Q4：按钮级交互规格为什么这么重要？**

A：对于强交互型产品，AI 可能只描述"点击生成按钮，系统生成剧本"，但不描述按钮加载态、失败态、页面跳转关系。这会导致前端开发凭经验猜测，上线后用户体验不一致。`interaction-spec.md` 强制要求每个交互元素的状态机必须完整。

---

AI项目落地工具链 | V2.1
