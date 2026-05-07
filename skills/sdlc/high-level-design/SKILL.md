---
name: high-level-design
description: 当用户要求'概要设计'、'high-level-design'、'HLD'、'系统架构设计'、'技术选型'或基于已冻结 PRD 进入设计阶段时触发。正向生成系统概要设计文档，回答系统拆成几块、数据怎么走、用什么技术栈。
---

# High-Level Design（概要设计）

基于已冻结的产品需求文档（PRD-000，即 `specs/01-05.md`），正向生成系统概要设计文档。严格限定为架构层（影响 ≥2 个模块），禁止输出接口字段、类图、DDL、算法参数等详细设计内容。

## 适用场景

- 基于已冻结的 PRD-000 进入阶段 3 概要设计
- 需要确定系统分层/服务划分、技术栈选型、数据架构
- 需要定义模块间接口契约、全局状态机、核心链路时序
- 非功能需求（安全/性能/部署/测试）的架构层策略定义

## 核心职责

1. **正向设计**：基于需求产出目标架构，而非逆向分析现有代码
2. **配置驱动**：按 `config.yaml` 的 `artifact_specs.high-level-design.required_sections` 逐项输出
3. **严格边界**：只输出影响 ≥2 个模块的架构决策，禁止下钻到详细设计
4. **图表自治**：自动生成 Mermaid 架构图、ER 图、时序图、部署拓扑图
5. **需求追溯**：每个架构决策必须能追溯到上游需求文档

## 前置依赖

| 上游 Skill | 产出物 | 用途 | 是否必需 |
|---|---|---|---|
| `prd-generation` | `specs/01-05.md` | 产品范围、模块清单、需求边界、非功能指标 | **必须** |
| `competitive-analysis` | `design/competitive-analysis.md` | 技术选型论证支撑 | **必须** |
| `detailed-requirements` | `specs/feature-*/spec.md` | 模块功能细节，用于覆盖度校验与状态机兼容性核对 | 建议参考 |

> 概要设计的**核心输入**是 `prd-generation` 产出的概要需求。`detailed-requirements` 仅作为可选的校验基准，**不阻塞**概要设计启动。

## 执行步骤

### Step 1: 配置加载
- 读取 `openspec/config.yaml` 中 `artifact_specs.high-level-design`
- 确认 `required_sections`、`DETAIL_LEVEL`、`FOCUS_ON_EXTENSIBILITY`、`INCLUDES_DECISION_RECORDS`
- 若配置缺失，使用默认值并发出警告

### Step 2: 上游文档解析
- 解析 `03-functional-structure.md` 提取模块清单（名称、职责、优先级）
- 解析 `02-requirements-list.md` 锁定 P0/P1/P2 范围
- 解析 `05-non-functional.md` 提取性能/安全/可靠性指标
- 解析 `competitive-analysis.md` 提取技术选型结论
- 若已存在 `feature-*/spec.md`，解析并汇总功能点（用于可选的覆盖度校验）

### Step 3: 逐项生成（按 required_sections）

#### system_architecture
分层/服务划分、部署拓扑、Mermaid 架构图（支持 C4-Model 分层：Context→Container→Component）。禁止写模块内部类图。

#### tech_stack
技术项 + 选型理由 + 竞品溯源。每个选型必须关联 `competitive-analysis.md` 结论。禁止展开框架专属模式（如 Spring DI 配置、React Hook 模式）。

#### data_architecture
逻辑 ER 图、主数据流向、存储策略选型、分库分表策略、核心表清单。生成 Mermaid ER 图。禁止写字段类型、索引、DDL、ORM 配置。

#### interface_contracts
模块间/服务间通信模式（REST/gRPC/MCP/消息队列）、数据契约、版本策略。禁止写请求/响应 Schema、Header 定义、字段校验规则、幂等策略。

#### module_responsibilities
每个模块的输入、输出、核心职责、对外依赖。禁止写内部类图、函数签名、实现细节。

#### state_machine_global
跨模块核心实体状态流转（如"剧本：草稿→审核→发布"）。生成 Mermaid 状态图。禁止写单模块内部状态转换规则、触发事件、校验规则。

#### sequence_diagrams
跨模块关键流程时序图（如"用户提交→AI 生成→回调通知"）。生成 Mermaid 时序图。禁止写模块内部 Controller→Service→Repository 调用链。

#### algorithm_selection（AI 项目必选）
识别需求中的 AI/智能功能，输出模型基座选择、选型理由、输入输出维度约定、与其他模块的耦合方式。禁止写算法流程、参数配置、Prompt 模板、回退策略。

#### security_design
认证授权方案（RBAC/OAuth2）、数据加密策略、网络隔离。参考 `references/section-templates.md` 横切关注点清单。

#### performance_design
QPS 预估、缓存策略（Redis/CDN）、异步化方案、容量规划。禁止写缓存 Key 设计、过期策略、连接池配置。

#### exception_handling_global
全局异常分类体系、降级策略、熔断规则、重试策略。禁止写单接口异常码、补偿事务、日志格式。

#### deployment_architecture
容器化/K8s/Serverless 拓扑、CI/CD 流程。生成 Mermaid 部署拓扑图。

#### test_strategy
测试金字塔、分层策略、自动化覆盖率目标、测试边界定义。禁止写单测用例、Mock 策略、数据构造方案。

#### extensibility_design（可选，FOCUS_ON_EXTENSIBILITY=true）
功能添加/修改/集成模式，预留扩展点。参考 `references/section-templates.md` 扩展性框架。

#### decision_records（可选，INCLUDES_DECISION_RECORDS=true）
关键决策正向论证：Context / Factors / Decision / Consequences / Future Flexibility。至少覆盖架构模式选择、技术栈选择、数据存储选型。

#### governance_rules（可选，INCLUDES_GOVERNANCE=true）
架构一致性维护规则、自动化检查建议、架构评审流程定义。

### Step 4: 边界自检
每生成一章后检查：
- 是否包含字段级定义（如 `varchar(64)`、`@RequestBody`）
- 是否包含代码片段（函数签名、类定义、SQL）
- 是否包含单模块内部实现细节
若检测到，标记"内容下钻"警告，建议移至详细设计。

### Step 5: 覆盖度校验
- 架构是否覆盖 `03-functional-structure.md` 中所有 P0 模块（核心校验）
- 每个技术选型是否在 `competitive-analysis.md` 中有溯源
- 每个全局状态是否能在需求清单中找到业务规则追溯
- 若提供了 `feature-*/spec.md`，校验全局状态机是否与模块状态描述兼容

### Step 6: 输出与保存
按命名规范保存到 `openspec/changes/{变更名}/design/`：
```
01-system-architecture.md
02-tech-stack.md
03-data-architecture.md
04-interface-contracts.md
05-module-responsibilities.md
06-state-machine-global.md
07-sequence-diagrams.md
08-algorithm-selection.md
09-security-design.md
10-performance-design.md
11-exception-handling-global.md
12-deployment-architecture.md
13-test-strategy.md
14-extensibility-design.md      # 可选
15-decision-records.md          # 可选
16-governance-rules.md          # 可选
```

### Step 7: 触发 self-check
自动调用 `self-check` skill 校验一致性、完整性、交叉引用有效性、边界合规性。

## 阶段切换门控

- 概要设计评审通过（用户确认）
- `self-check` 无 BLOCKER
- **禁止在概要设计评审通过前进入 `detailed-design` 或编码实现**

## 常见陷阱检查清单

- [ ] 将接口字段校验写入 `interface-contracts` → 应移至 `detailed-design/api-spec.md`
- [ ] 将数据库字段/索引写入 `data-architecture` → 应移至 `detailed-design/db-schema.md`
- [ ] 将算法参数写入 `algorithm-selection` → 应移至 `detailed-design/algorithm.md`
- [ ] 将单模块状态机写入 `state-machine-global` → 应移至 `detailed-design/state-machine.md`
- [ ] 将类图/函数签名写入任何章节 → 应移至 `detailed-design/design.md`

## 下游消费

| 下游 Skill | 消费文档 | 衔接规则 |
|---|---|---|
| `detailed-design` | `design/*.md` | 评审通过后按模块逐一下钻 |
| `task-breakdown` | `design/*.md` + `specs/feature-*/design.md` | 基于架构分层拆解任务 |

## 深度参考

- 各章节详细写作指南与模板见 `references/section-templates.md`
- 边界红线与变更影响范围判定见 `references/boundary-rules.md`

## Gotchas

- **正向设计，非逆向分析**：基于需求生成架构，不是扫描现有代码。若项目已有代码，仅作参考不作依据。
- **边界红线不可越**：概要设计只定义影响 ≥2 模块的决策。任何字段级、代码级、单模块内部细节必须拦截。
- **技术选型必须溯源**：每个技术选型必须关联 `competitive-analysis.md` 结论，无溯源则视为 WARNING。
- **模块遗漏 = BLOCKER**：未覆盖 `03-functional-structure.md` 中 P0 模块的架构设计不得通过自查。
- **状态机兼容**：若提供了详细需求（`feature-*/spec.md`），全局状态机应与其各模块状态描述兼容，发现冲突时标记 BLOCKER。
- **禁止自动下钻**：生成时若 AI 自发输出详细设计内容，必须自我拦截并提升抽象层级，不得直接保存。
- **设计锁定原则**：用户确认评审通过后，概要设计冻结。变更需重新走架构评审会，禁止偷偷修改已冻结文档。
- **ADR 流于形式**：若输出决策记录，必须包含"备选方案及排除原因"，否则视为不完整。
- **图表一致性**：Mermaid 图表必须从文本架构描述自动生成，禁止图表与文字描述矛盾。
