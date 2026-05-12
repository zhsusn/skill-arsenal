# AI项目落地工具链设计文档

> Kimi Code + OpenSpec + Superpowers + Human Gate 四工具集成方案
>
> 版本 V2.1 | 2026年5月
>
> 本次更新基于 `lifesycle.md` 审查意见，将工具链从"开发完成"扩展为"项目交付"，补充 UAT、发布、监控与四道人工闸门（Gate 1/2.5/2/3），增加 `human` Skill 作为人工决策的统一载体。
>
> **V2.2 更新（2026年5月）**：重构计划与执行阶段，引入 `writing-plans` → `task-breakdown` → `executing-plans` 三级递进工作流。
> - `writing-plans` 从 Superpowers 原生 micro-step 升级为**模块级实现计划**（plan.md），增加 Self-Review 四检与 Plan → Task 转换建议
> - `task-breakdown` **新增**，按 ≤30 分钟/任务粒度将 plan.md 拆解为 Phase 组织的 tasks.md，支持垂直切片与执行模式建议
> - `executing-plans` 增强 **Batch 执行**、**Gate Non-Collapse Rule**、**自动勾选 tasks.md**、**Inline Audit** 与 **Simplicity First / Scope Discipline / Rollback-Friendly** 执行纪律

---

## 目录

- [一、系统概述](#一系统概述)
  - [1.1 四个工具的定位与关系](#11-四个工具的定位与关系)
  - [1.2 核心设计原则](#12-核心设计原则)
  - [1.3 四道人工闸门（V2.1 新增）](#13-四道人工闸门v21-新增)
- [二、各工具详解](#二各工具详解)
  - [2.1 Kimi Code —— AI编程引擎](#21-kimi-code--ai编程引擎)
  - [2.2 OpenSpec —— 规格驱动开发框架](#22-openspec--规格驱动开发框架)
  - [2.3 Superpowers —— AI编码技能框架](#23-superpowers--ai编码技能框架)
  - [2.4 Human Gate —— 人工决策审计层（V2.1 新增）](#24-human-gate--人工决策审计层v21-新增)
- [三、工具边界与职责划分](#三工具边界与职责划分)
  - [3.1 各工具的核心职责](#31-各工具的核心职责)
  - [3.2 不做什么（明确边界）](#32-不做什么明确边界)
  - [3.3 Skill 依赖关系](#33-skill-依赖关系)
- [四、集成方案](#四集成方案)
  - [4.1 四工具打通架构](#41-四工具打通架构)
  - [4.2 MCP 协议集成](#42-mcp-协议集成)
  - [4.3 数据流与交互流程](#43-数据流与交互流程)
  - [4.4 人工阻塞机制实现（V2.1 新增）](#44-人工阻塞机制实现v21-新增)
- [五、目标与价值](#五目标与价值)
  - [5.1 核心目标](#51-核心目标)
  - [5.2 价值体现](#52-价值体现)
- [六、后期发展方向](#六后期发展方向)
  - [6.1 短期规划（6-12个月）](#61-短期规划6-12个月)
  - [6.2 中期规划（1-2年）](#62-中期规划1-2年)
  - [6.3 长期愿景（3-5年）](#63-长期愿景3-5年)
  - [6.4 挑战与应对](#64-挑战与应对)

---

## 一、系统概述

### 1.1 四个工具的定位与关系

本方案以"接口驱动、自动保存、Skill 自治、最小人工干预、可追溯决策"为核心设计原则，将 Kimi Code、OpenSpec、Superpowers 和 **Human Gate（V2.1 新增）** 四个独立工具有机整合，形成一套从需求探索到线上监控的完整 AI 项目落地工具链。

| 工具 | 核心定位 | 职责比喻 |
|------|----------|----------|
| Kimi Code | AI 编程引擎 | 大脑 —— 提供智能决策和代码生成 |
| OpenSpec | 规格驱动开发框架 | 规范系统 —— 管理变更生命周期 |
| Superpowers | AI 编码技能框架 | 方法论 —— 提供结构化开发工作流 |
| **Human Gate（新增）** | **人工决策审计层** | **红绿灯 —— 在关键节点强制人工确认并记录决策** |

从职责分层来看：
- **Kimi Code** 作为"大脑"提供智能决策和代码生成能力；
- **OpenSpec** 作为"规范系统"管理项目变更的生命周期；
- **Superpowers** 作为"方法论"提供结构化的开发工作流；
- **Human Gate** 作为"红绿灯"在关键决策点强制暂停、等待人工确认、记录审计日志，确保"AI 执行 → 人工确认 → AI 再执行"的闭环。

四者相互配合，形成了从需求探索到线上监控的完整闭环，而非仅止于代码交付。

### 1.2 核心设计原则

> **● 接口驱动（Interface-First）：** 在开始编码之前先定义前后端接口契约，确保前后端可以并行开发，前端可以通过 Mock 数据提前让用户确认页面效果。
>
> **● 自动保存（Auto-Save）：** 所有产出物（PRD、设计文档、代码等）由 Skill 自动保存到指定路径，无需人工拷贝粘贴。
>
> **● Skill 自治（Skill Autonomy）：** 每个 Skill 自己决定下一步执行什么，不需要人工逐步提示。
>
> **● 最小人工干预（Minimal Intervention）：** 人工只需在关键决策点进行干预，日常执行由 AI 自主完成。
>
> **● 可追溯决策（Traceable Decisions）（V2.1 新增）：** 每个人工决策都有记录、有签字、有日期，通过 `human-decisions.md` 形成审计日志，支持历史查询与责任追溯。

### 1.3 四道人工闸门（V2.1 新增）

将人工参与从"建议性"改为**阻塞性**——AI 执行到闸门处暂停，必须获得人工信号才能继续。

| 闸门 | 名称 | 所在阶段 | 核心目的 | 不通过的风险 |
|------|------|----------|----------|--------------|
| 🚪 Gate 1 | 需求冻结闸 | 概要需求完成后 | 确认核心功能覆盖业务闭环，防止"一错全错" | AI 过度推断或遗漏隐性需求，后续所有工作偏离真实业务意图 |
| 🚪 Gate 2.5 | 原型冻结闸 | 详细需求完成后 | 逐页确认按钮级交互状态机，防止前端实现偏差 | 按钮加载态/错误态/页面流转缺失，上线后用户体验不一致 |
| 🚪 Gate 2 | 设计冻结闸 | 概要设计完成后 | 评审架构 + 确认回滚方案，防止技术选型失误 | 技术债累积、扩展性不足、上线后无回滚预案 |
| 🚪 Gate 3 | 发布冻结闸 | UAT 完成后 | 在预览环境走通完整业务流程，防止"逻辑正确但业务错误" | 集成测试通过但业务规则错误（如优惠券叠加规则理解错误），上线即故障 |

---

## 二、各工具详解

### 2.1 Kimi Code —— AI编程引擎

#### 2.1.1 产品定位

Kimi Code 是月之暗面（Moonshot AI）推出的开发者产品线，基于 Kimi K2.6-code-preview 万亿参数模型优化而成。与 Kimi Chat 的通用对话不同，Kimi Code 专注于软件开发场景，具有以下核心特征：

| 特性 | 说明 |
|------|------|
| 256K 上下文窗口 | 为代码库级别的项目调优，支持大规模代码理解 |
| 100 tokens/秒输出速度 | 专为代码生成优化，响应迅速 |
| 原生 CLI 模式 | 支持终端直接调用，无需 IDE |
| Claude Code 兼容后端 | 可作为成本更低的替代后端使用 |
| Agent Swarm 并行执行 | 支持批量编码任务的并行处理 |

#### 2.1.2 技术特点

Kimi Code 的核心竞争力在于其"Opus-style"风格的深度推理能力。在实际开发者评测中，K2.6-code-preview 的得分从 K2.5 的 83 分提升至 89 分，实际体验已达到 Sonnet 4.6 水平。其核心优化三个维度：推理深度（更严谨的逻辑推理）、Agent 规划（处理复杂项目的全局规划能力）、工具调用（多步工具调用可靠性显著提升）。

### 2.2 OpenSpec —— 规格驱动开发框架

#### 2.2.1 产品定位

OpenSpec 是一个规格驱动开发（Spec-Driven Development，SDD）框架，由 Fission AI 开发并以 MIT 许可证开源。它的核心理念是"先写规格，再写代码"，通过一套标准化的变更管理流程，确保 AI 编程助手遵循规格而不是盲目猜测。

#### 2.2.2 核心概念

OpenSpec 的工作流围绕三种关键制品类型：

1. **增量规格（Delta Specs）——** 描述建议的修改，将部分标记为"ADDED"、"MODIFIED"或"REMOVED"，清晰传达变更内容。

2. **真理源规格（Source of Truth）——** 代表系统实际状态的主要规格，所有增量变更最终合并到此文档中。

3. **归档规格（Archived Specs）——** 保留早期增量规格的历史谱系，形成审计追溯记录。

#### 2.2.3 命令体系

OpenSpec 的命令分为两大体系：

| 命令体系 | 命令 | 用途 |
|----------|------|------|
| 核心工作流 | `/opsx:propose` | 一步创建变更并生成规划制品 |
| | `/opsx:explore` | 开发前梳理思路、调研方案 |
| | `/opsx:apply` | 执行变更任务，编写代码实现功能 |
| | `/opsx:archive` | 归档已完成的变更，留存审计追溯 |
| 扩展工作流 | `/opsx:new` | 初始化新变更的基础脚手架 |
| | `/opsx:continue` | 按依赖关系逐步生成下一个制品 |
| | `/opsx:ff` | 快进生成所有规划制品 |
| | `/opsx:verify` | 验证实现与规格的一致性 |
| | `/opsx:sync` | 将增量规格合并到主规格 |
| | `/opsx:bulk-archive` | 批量归档多个已完成的变更 |

#### 2.2.4 设计哲学

OpenSpec 的设计哲学可以概括为五个关键词：灵活而非僵化（fluid not rigid）、迭代而非瀑布（iterative not waterfall）、简单而非复杂（easy not complex）、为存量项目而建（built for brownfield）、从个人到企业级可扩展（scalable）。这使得它无论是在小型个人项目还是大型企业级应用中都能发挥作用。

### 2.3 Superpowers —— AI编码技能框架

#### 2.3.1 产品定位

Superpowers 是由 obra 开发的开源 AI 编码技能框架，Star 数超过 27,000，是当前最受欢迎的 AI 编码工作流框架之一。它不是一个新的模型或工具，而是一个"行为层"（behavior layer），坐落在现有 AI 编码代理之上，为其提供结构化、可重复的工作流。

#### 2.3.2 核心工作流

Superpowers 的核心工作流遵循四个必须的阶段：

| 阶段 | 说明 |
|------|------|
| Brainstorm | 开写代码前的苏格拉底式问答，理清需求边界 |
| Isolated Workspace | 通过 Git Worktree 创建隔离的开发环境 |
| Plan | 生成精细到每个 2-5 分钟任务的实现计划 |
| Execute with TDD | 子 Agent 按 RED-GREEN-REFACTOR 循环执行，并经过两轮审查 |

> **本方案改造说明**：本方案在 Superpowers 原生工作流基础上增加了 **设计文档级计划层**（`writing-plans` 输出 plan.md）和 **微观任务拆解层**（`task-breakdown` 输出 tasks.md），形成 `plan.md → tasks.md → Batch 执行` 的三级递进。`writing-plans` 的粒度从 2-5 分钟 micro-step 升级为模块级，`executing-plans` 的执行从直接消费 micro-steps 变为按 Batch 消费 tasks.md。

#### 2.3.3 关键技能

Superpowers 提供了丰富的技能集，本方案中主要使用的技能包括：

| Skill名称 | 来源 | 当前状态 | 核心职责 |
|-----------|------|----------|----------|
| brainstorming | Superpowers | ✅ 可用 | 需求探索，苏格拉底式提问 |
| writing-plans | Superpowers | ✅ 已改造 | 编写模块级实现计划（plan.md），衔接 task-breakdown |
| executing-plans | Superpowers | ✅ 已改造 | 按 tasks.md 逐 Batch 执行，含强制自测、接口校验、自动勾选 |
| test-driven-development | Superpowers | ✅ 可用 | TDD 红绿重构循环 |
| systematic-debugging | Superpowers | ✅ 已适配 | 四阶段根因分析，新增 progress-tracker 技术债务联动 |
| requesting-code-review | Superpowers | ✅ 已改造 | 代码审查，V2.1 增强：design.md 对比、tasks.md 追溯、UAT 交叉验证、release-management 衔接 |
| finish | Superpowers | ✅ 已改造 | 归档收尾（原 finishing-a-development-branch），扩展为八步流水线：人工确认→合并清理→归档→规格同步→纳入交付后文档→CHANGELOG→一致性校验→确认单 |
| prd-generation | 本方案 | 🔧 需修改 | 概要需求生成，需增加 Gate1 确认提示 |
| competitive-analysis | 本方案 | ✅ 可用 | 竞品分析（positioning/technical 双模式） |
| high-level-design | 本方案 | 🔧 需修改 | 概要设计，需增加 rollback-plan.md |
| detailed-requirements | 本方案 | 🔧 需修改 | 详细需求，需增加 interaction-spec.md |
| progress-tracker | 本方案 | 🔧 需修改 | 进度追踪，需增加 ops/ 目录与人工状态 |
| self-check | 本方案 | 🔧 需修改 | 产出物自查，需增加交互/UAT 检查维度 |
| **human** | **本方案** | **➕ 需新增** | **人工决策审计与闸门控制** |
| **detailed-design** | **本方案** | **➕ 需新增** | **按模块输出详细设计** |
| **interface-first-dev** | **本方案** | **➕ 需新增** | **接口驱动开发** |
| **task-breakdown** | **本方案** | **✅ 可用** | **将 plan.md 按 ≤30 分钟/任务粒度拆解为 Phase 组织的 tasks.md** |
| **unit-test** | **本方案** | **➕ 需新增** | **单元测试生成与执行** |
| **integration-test** | **本方案** | **➕ 需新增** | **集成测试生成与执行** |
| **uat-verification** | **本方案** | **➕ 需新增** | **UAT 业务验证** |
| **release-management** | **本方案** | **➕ 需新增** | **发布管理** |
| **monitoring-setup** | **本方案** | **➕ 需新增** | **监控初始化（一次性）** |
| **monitoring-analysis** | **本方案** | **➕ 需新增** | **监控分析（周期性）** |

> 完整 Skill 清单与状态见 `docs/AI项目工具链Skill清单与状态.md`。

### 2.4 Human Gate —— 人工决策审计层（V2.1 新增）

#### 2.4.1 产品定位

Human Gate 不是独立的第三方工具，而是本方案定义的 Skill（`human`），作为人工决策的"审计日志 + 状态闸门"。它像 Git 的 commit + status——记录快照 + 显示当前状态。

#### 2.4.2 核心职责

1. **决策记录**：对每次人工确认生成结构化记录，包含 Gate、时间、结论、遗留问题、决策人
2. **状态控制**：根据最新决策判断当前变更是否允许进入下一阶段
3. **历史追溯**：支持查询某个变更的全部决策链，或跨变更的决策统计
4. **阻塞提示**：当用户试图跳过未通过的 Gate 时，主动拦截并提示

#### 2.4.3 决策类型

| 类型 | 含义 | 后续动作 |
|------|------|----------|
| sign-off | 签字通过 | 解锁下一阶段，记录遗留问题（如有） |
| conditional | 有条件通过 | 解锁下一阶段，但遗留问题必须记入下一阶段 tasks.md |
| reject | 驳回重做 | 锁定当前阶段，必须修复后才能再次 sign-off |
| pause | 暂停流程 | 标记为阻塞状态，等待外部资源 |
| resume | 恢复流程 | 解除暂停，回到 pause 前状态 |
| hotfix | 紧急修复 | 在已归档变更上记录紧急补丁决策 |

#### 2.4.4 使用方法

```bash
# Gate 1 通过
/skill:human gate=Gate1 action=sign-off result=passed issues="P1: 批量导入边界条件待补充"

# Gate 2.5 有条件通过
/skill:human gate=Gate2.5 action=conditional result=passed issues="P1: loading态细化；P2: 移动端适配"

# Gate 3 驳回
/skill:human gate=Gate3 action=reject reason="Safari下无法保存"

# 查询状态
/skill:human action=status
```

---

## 三、工具边界与职责划分

### 3.1 各工具的核心职责

| 工具 | 核心职责 | 典型输入/输出 |
|------|----------|---------------|
| Kimi Code | 提供 AI 编程能力 | 自然语言指令 → 代码/文档 |
| OpenSpec | 管理变更生命周期 | 变更描述 → 规格/任务/归档 |
| Superpowers | 提供结构化工作流 | 需求 → 计划/代码/测试 |
| **Human Gate** | **记录人工决策、控制阶段流转** | **人工结论 → 审计日志/阶段解锁** |

### 3.2 不做什么（明确边界）

#### Kimi Code 不做：

> • 不管理项目变更的生命周期和归档
>
> • 不强制某种开发方法论（如 TDD）
>
> • 不提供规格文档管理能力
>
> • **不替代人工做最终业务判断（V2.1 新增）**

#### OpenSpec 不做：

> • 不生成代码（只生成规格和任务清单）
>
> • 不执行具体的开发工作
>
> • 不提供需求探索的苏格拉底式对话能力
>
> • **不替代人工进行 UAT 点击验证（V2.1 新增）**

#### Superpowers 不做：

> • 不管理项目级的规格归档
>
> • 不提供统一的变更目录结构
>
> • 不替代具体的 AI 模型或工具
>
> • **不自动执行生产环境发布（V2.1 新增）**

#### Human Gate 不做：

> • **不替代人工做判断**
>
> • **不自动生成决策内容**
>
> • **不修改产出物**
>
> • 不执行代码审查或测试（只记录结论）

### 3.3 Skill 依赖关系

本方案定义了 23 个 Skill，其中 7 个来自 Superpowers 原生，16 个由本方案定义（含 10 个新增）。它们之间的依赖关系如下：

| Skill | 前置依赖 | 被什么 Skill 依赖 |
|-------|----------|-------------------|
| brainstorming | 无 | prd-generation |
| prd-generation | brainstorming | competitive-analysis(technical), detailed-requirements |
| competitive-analysis(positioning) | brainstorming | prd-generation |
| competitive-analysis(technical) | prd-generation | high-level-design |
| detailed-requirements | prd-generation | detailed-design |
| **human (Gate1)** | prd-generation | detailed-requirements |
| **human (Gate2.5)** | detailed-requirements | high-level-design |
| high-level-design | prd + CA + DR | detailed-design, **monitoring-setup** |
| **monitoring-setup** | high-level-design | **monitoring-analysis** |
| **human (Gate2)** | high-level-design | detailed-design |
| detailed-design | HLD + DR | interface-first-dev, **writing-plans** |
| interface-first-dev | detailed-design | **task-breakdown** |
| **writing-plans** | detailed-design + IFD | **task-breakdown** |
| task-breakdown | plan.md + IFD | executing-plans |
| executing-plans | tasks.md | unit-test, integration-test |
| unit-test | executing-plans | integration-test |
| integration-test | unit-test | **uat-verification** |
| **uat-verification** | integration-test | **human (Gate3)** |
| **human (Gate3)** | uat-verification | **release-management** |
| requesting-code-review | executing-plans + design.md + tasks.md | **release-management** / rework-tasks.md |
| **release-management** | uat + CR + rollback | finish（人工确认后） |
| finish | release-management（人工确认信号） | **monitoring-analysis** |
| **monitoring-analysis** | release-management | brainstorming（下一迭代） |
| self-check | 贯穿全程 | 各阶段门控 |
| progress-tracker | 贯穿全程 | 各阶段状态更新 |

---

## 四、集成方案

### 4.1 四工具打通架构

四个工具的集成架构遵循"分层解耦、接口驱动"的原则，形成一个完整的工具链：

| 层级 | 工具 | 职责 |
|------|------|------|
| 表现层（UI） | Kimi Code | 接收用户指令、展示执行结果 |
| 控制层 | MCP Protocol | 负责工具之间的通信协调 |
| 规范层 | OpenSpec | 管理变更生命周期和规格文档 |
| 方法层 | Superpowers | 提供结构化开发工作流 |
| **审计层（新增）** | **Human Gate** | **记录人工决策、控制阶段流转权限** |
| 执行层 | Kimi Code | 生成代码、执行任务 |

### 4.2 MCP 协议集成

MCP（Model Context Protocol）是 Anthropic 于 2024 年11月开源的协议，已成为 AI 工具集成的行业标准。到 2026 年，MCP 支持五种原语（tools、resources、prompts、sampling、roots）和两种传输方式（STDIO 和 Streamable HTTP）。本方案中，MCP 是实现四工具打通的关键技术基础。

#### 4.2.1 集成方式

1. **Kimi Code 作为 MCP Client——** Kimi Code 提供 MCP Client 能力，通过 MCP 协议与 OpenSpec 和 Superpowers 的 MCP Server 通信。

2. **OpenSpec 提供 MCP Server——** OpenSpec 提供规格管理相关的 tools（如 propose、apply、archive、verify 等）。

3. **Superpowers 提供 MCP Server——** Superpowers 提供开发工作流相关的 tools（如 brainstorming、writing-plans、executing-plans、tdd 等）。

4. **Human Gate 作为对话层阻塞（V2.1 新增）——** Human Gate 不依赖 MCP 协议，而是通过修改各 Skill 的 `SKILL.md`，在关键步骤后插入"人工确认节点"，利用 Kimi Code 的对话上下文自然阻塞。

### 4.3 数据流与交互流程

四工具集成后的典型数据流如下（V2.1 已补充 UAT、发布、监控与人工闸门）：

1. **启动阶段——** 用户通过 Kimi Code 发起项目，Kimi Code 通过 MCP 调用 OpenSpec 初始化目录结构和配置文件；`progress-tracker` 扫描项目并生成 `ops/` 目录骨架。

2. **需求阶段——** Kimi Code 调用 Superpowers 的 `brainstorming` 进行需求探索，然后通过 OpenSpec 创建变更提案和规格文档；`prd-generation` 产出 5 个 spec 文件后，通过 `human` Skill 触发 **Gate 1** 人工冻结。

3. **详细需求阶段——** `detailed-requirements` 按模块输出详细需求（含 `interaction-spec.md`），通过 `human` Skill 触发 **Gate 2.5** 原型冻结。

4. **设计阶段——** `high-level-design` 产出架构文档和 `rollback-plan.md`，通过 `human` Skill 触发 **Gate 2** 设计冻结；`monitoring-setup` 生成监控规则初稿。`detailed-design` 按模块输出详细设计（含 `api-spec.md`、`db-schema.md`、`state-machine.md`）。`interface-first-dev` 基于详细设计定义前后端接口契约（`openapi.yaml` + Mock 数据 + 并行开发计划）。

5. **计划阶段——** `writing-plans` 基于 detailed-design 和 interface-first-dev 的产出，生成模块级实现计划（plan.md），包含技术路线、模块实现顺序、验收标准，并输出「Plan → Task 转换建议」。plan.md 经 Self-Review 四检（Spec Coverage / Placeholder Scan / Type Consistency / Design Alignment）通过后保存。

6. **任务拆解阶段——** `task-breakdown` 读取 plan.md 和接口契约，按垂直切片原则将模块拆分为 ≤30 分钟/任务的开发清单（tasks.md），按 Phase 组织并标注 `[前端]`/`[后端]`/`[AI模型]`/`[配置]`/`[测试]` 标签。自检通过（覆盖度/无XL/依赖无环/标签完整/验收可验证）后保存。

7. **开发阶段——** Kimi Code 调用 `executing-plans` 按 tasks.md 逐 Batch（默认 3 任务/批次）执行代码开发。每个任务执行后必须经过三个独立门控：强制自测（self-check）、接口一致性校验（代码 vs api-spec）、单测运行（覆盖率 ≥ 70%）。任务完成后自动勾选 tasks.md，Batch 完成后执行 Inline Audit。执行纪律包括 Simplicity First、Scope Discipline、Rollback-Friendly。

8. **测试阶段——** `unit-test` 和 `integration-test` 生成并执行测试；`integration-test` 额外输出 `user-stories-checklist.md` 供 UAT 使用。

9. **UAT 阶段（V2.1 新增）——** `uat-verification` 生成检查清单，人工在预览环境点击走通业务流程，通过 `human` Skill 触发 **Gate 3** 发布冻结。

10. **发布阶段（V2.1 新增）——** `requesting-code-review` 输出结构化审查报告（含 design.md 设计偏差分析、tasks.md 任务追溯矩阵、UAT 交叉验证）。若结论为不通过，生成 `rework-tasks.md` 返回 `executing-plans` 修复。`release-management` 生成发布清单，人工最终确认后执行上线。**严禁 AI 自动执行生产发布。**

11. **归档阶段——** `finish` 执行八步归档流水线：人工最终确认 → 分支合并与清理 → OpenSpec 归档 → 增量规格合并（`/opsx:sync`，保留历史谱系） → 纳入交付后文档（uat-report + release-notes + human-decisions + code-review-report） → 生成 CHANGELOG.md → 最终一致性校验（8 项检查清单） → 输出归档完成确认单。**严禁 AI 自动执行归档，必须等待人工确认信号。**

12. **监控阶段（V2.1 新增）——** `monitoring-analysis` 周期性运行，输出 `feedback-loop.md` 反哺下一变更的 `brainstorming`，形成闭环。

### 4.4 人工阻塞机制实现（V2.1 新增）

#### 4.4.1 实现方式：Skill 内嵌确认节点

修改每个需要人工把关的 Skill（如 `prd-generation`、`high-level-design`、`detailed-requirements`），在其 `SKILL.md` 的"执行流程"中增加一个伪步骤：

```markdown
## 执行流程

1. 读取上游文档
2. 生成产出物并保存到指定路径
3. **人工确认节点** ← 新增
   - 输出提示语："概要需求已生成，请阅读 @openspec/changes/{变更名}/specs/ 下的 5 个文件"
   - 输出检查清单："请确认：①核心功能覆盖业务闭环 ②边界条件已定义 ③非功能性需求已量化"
   - 等待用户回复"确认"或"修改：{具体意见}"
4. 只有在收到"确认"后，才允许进入下一阶段
```

效果：AI 执行完步骤 2 后，会主动停下来输出一段提示，等你回复。你回复"确认"后，AI 继续；你说"修改"，AI 回到步骤 2 重修。

优点：零开发成本，只改 `SKILL.md` 文本。

#### 4.4.2 状态查询

通过 `human` Skill 随时查询当前变更的决策状态：

```bash
/skill:human action=status
```

输出示例：
```text
========================================
变更：reelforge-v1.2-角色工厂重构
========================================
已通过：Gate1(需求冻结) → Gate2.5(原型冻结) → Gate2(设计冻结)
当前阶段：detailed-design（进行中）
下一 Gate：Gate3（发布冻结）
状态：🟢 正常推进

⚠️ 注意：Gate2.5 为"有条件通过"，存在遗留问题：
  - P1: 创建角色按钮loading态细化（应在 detailed-design 阶段修复）
  - P2: 移动端适配（记入下一迭代 tasks.md）

可操作指令：
- /skill:detailed-design
- /skill:human action=history
```

---

## 五、目标与价值

### 5.1 核心目标

> **● 规范化开发流程：** 通过 OpenSpec 的规格驱动开发机制，确保每个变更都有清晰的边界定义和完整的文档追溯，减少因需求不清导致的返工。
>
> **● 提升代码质量：** 通过 Superpowers 的 TDD 和代码审查机制，确保每个功能都有充足的测试覆盖，单元测试覆盖率≥70%。
>
> **● 降低人工成本：** 通过 Kimi Code 的智能代码生成能力和 Skill 自治机制，将开发人员从重复性工作中解放出来，专注于更有价值的创造性工作。
>
> **● 加速交付节奏：** 通过接口驱动开发模式，实现前后端并行开发，缩短项目周期。
>
> **● 确保交付安全（V2.1 新增）：** 通过四道人工闸门和 UAT 验证，防止"开发完成但无法上线"的风险；通过 `rollback-plan.md` 和发布管理，确保上线后可回滚、可监控。
>
> **● 实现迭代闭环（V2.1 新增）：** 通过 `monitoring-analysis` 将线上反馈数据反哺到下一版需求的 `brainstorming`，形成从需求到监控的完整闭环。

### 5.2 价值体现

这套工具链的价值体现在以下几个方面：

1. **对个人开发者——** 以极低的成本（39元/月）获得接近顶级 AI 编程能力，同时享受结构化的开发流程和"AI 执行 + 人工确认"的双重保险。

2. **对团队——** 统一的工作流和规范格式降低团队成员之间的沟通成本；四道人工闸门和签字文件确保关键决策有据可查；新成员可以通过归档的规格快速了解项目历史和设计决策。

3. **对企业——** 完整的审计追溯能力满足合规要求（`human-decisions.md` 记录每个关键决策）；规范驱动的流程减少因需求变更导致的资源浪费；线上监控与反馈闭环支持数据驱动的持续迭代。

---

## 六、后期发展方向

### 6.1 短期规划（6-12个月）

> • 完善 9 个新增 Skill（`human`、`uat-verification`、`release-management`、`monitoring-setup`、`monitoring-analysis`、`detailed-design`、`interface-first-dev`、`unit-test`、`integration-test`）的实现
>
> • 改造 2 个 Superpowers 原生 Skill（`writing-plans` 从 micro-step 升级为模块级计划并衔接 task-breakdown；`executing-plans` 增加 Batch 执行、强制自测、接口校验、自动勾选、Inline Audit、Simplicity First / Scope Discipline / Rollback-Friendly 执行纪律）
>
> • 改造 3 个现有 Skill（`requesting-code-review` 新增 design.md 对比与 tasks.md 追溯；`finish` 从 finishing-a-development-branch 重命名并扩展为八步归档流水线；`systematic-debugging` 新增 progress-tracker 技术债务联动）。修改 5 个现有 Skill（`prd-generation`、`detailed-requirements`、`high-level-design`、`progress-tracker`、`self-check`），补充交互规格、回滚方案、人工状态等能力
>
> • 实现 OpenSpec 归档时自动纳入 `uat-report`、`release-notes`、`human-decisions.md`
>
> • 增强 `self-check` Skill 的能力，支持交互规格完整性检查和 UAT 报告质量检查

### 6.2 中期规划（1-2年）

> • 支持更多的 AI 编程工具作为底座（如 Cursor、Windsurf、Gemini CLI 等）
>
> • 构建团队协作功能，支持多人同时在同一项目中使用不同的 Skill
>
> • 集成项目管理工具（如 Linear、Jira等），实现需求到代码到监控的全链路追溯
>
> • 建立 Skill 市场，允许社区贡献自定义 Skill

### 6.3 长期愿景（3-5年）

> • 推动行业标准化，将本方案的工具链模式推广为 AI 辅助开发的行业最佳实践
>
> • 建立开放的 Skill 市场，允许社区贡献和交易自定义 Skill
>
> • 实现"零人工干预"的全自动化开发，从需求到部署全程由 AI 自主完成（保留人工闸门作为安全底线）

### 6.4 挑战与应对

当前面临的主要挑战包括：

> • **工具版本更新带来的兼容性问题：** 需要建立版本管理和回退机制，各 Skill 的 `meta.json` 应明确版本约束
>
> • **团队采用的学习曲线：** 需要提供完善的培训资料和模板项目；四道人工闸门初期可能感觉"繁琐"，但随着项目复杂度上升，其风险拦截价值会指数级增长
>
> • **安全与合规考量：** 特别是在企业环境中对代码生成和自动化流程的审计要求；`human-decisions.md` 和 `sign-off/` 目录提供了基础审计能力，未来可扩展为不可篡改的区块链存证（可选）
>
> • **人工闸门的执行力：** 如果用户不遵守阻塞规则，AI 无法真正阻止。需要通过 `progress-tracker` 的 Red Flag 规则和进度异常拦截来强化约束力

---

**感谢阅读**

AI项目落地工具链 | V2.1
