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
5. **需求追溯**：每个架构决策必须能追溯到上游需求文档；**每个设计文件末尾必须包含"需求可追溯性"段落**，列出本文件回应的 REQ-XXX 及对应验证方式
6. **运维架构与回滚方案（V2.1 新增）**：输出运维监控架构、告警策略、可观测性方案，并生成 `rollback-plan.md`
7. **Gate 2 人工冻结提示（V2.1 新增）**：全部章节输出完成后，自动宣读 🚪 Gate 2 阻塞提示，等待人工签字后方可进入详细设计阶段

## 前置依赖

| 上游 Skill | 产出物 | 用途 | 是否必需 |
|---|---|---|---|
| `prd-generation` | `specs/01-05.md` | 产品范围、模块清单、需求边界、非功能指标 | **必须** |
| `competitive-analysis` | `design/competitive-analysis.md` | 技术选型论证支撑 | **必须** |
| `detailed-requirements` | `specs/feature-*/spec.md` | 模块功能细节，用于覆盖度校验与状态机兼容性核对 | 建议参考 |
| `human` | `human-decisions.md` | Gate 2 签字状态，未通过禁止进入详细设计 | **必须** |

> 概要设计的**核心输入**是 `prd-generation` 产出的概要需求。`detailed-requirements` 仅作为可选的校验基准，**不阻塞**概要设计启动。Gate 2 人工签字是硬性前置条件。

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

#### introduction（新增）
文档引言，包含：
- **1.1 目的**：本文档覆盖范围及目标读者
- **1.2 范围**：系统边界——包含与不包含的内容
- **1.3 术语与缩写**：统一术语表（与 `specs/02-requirements-list.md` 中的术语保持一致）
- **1.4 参考资料**：PRD 链接 + 竞品分析报告 + AI 架构决策文档（若存在）

#### design_considerations（新增）
设计前提与约束，包含：
- **假设**：业务假设、技术假设、环境假设
- **约束**：技术约束（如必须兼容的技术栈）、业务约束（如合规要求）、预算约束
- **依赖**：外部系统、第三方服务、内部模块依赖及版本要求
- **风险**：技术风险、业务风险、AI 模型风险（AI 项目），每项含影响等级（高/中/低）和缓解策略

#### system_architecture
系统整体分层、服务划分、部署拓扑。产出**双视图架构文档**：

- **技术架构图（默认）**：采用 C4-Model 分层（Context→Container→Component），展示技术组件、通信模式与部署边界
- **业务功能架构图（可选）**：当模块数 ≥ 4 或存在多业务域时，基于 `03-functional-structure.md` 的模块清单，调用 `functional-architecture-generator` 的分区方法论与颜色编码策略，输出带模块清单的功能架构图

禁止写模块内部类图。

#### tech_stack
技术项 + 选型理由 + 竞品溯源 + **架构策略对比矩阵 + ADR（Architecture Decision Record）**。

每个选型必须：
- 关联 `competitive-analysis.md` 结论
- 输出**备选方案对比矩阵**（强制）：
  | 方案 | 优点 | 缺点 | 决策 | 适用场景 |
  |------|------|------|------|----------|
  | [方案 A] | [优点] | [缺点] | 选中 | [理由] |
  | [方案 B] | [优点] | [缺点] | 放弃 | [理由] |
- 输出**关键架构决策（ADR 格式）**：
  - **决策**：[内容]
  - **背景**：[上下文]
  - **备选**：[考虑过的方案]
  - **后果**：[正面/负面影响]

禁止展开框架专属模式（如 Spring DI 配置、React Hook 模式）。

#### data_architecture
逻辑 ER 图、主数据流向、存储策略选型、分库分表策略、核心表清单。生成 Mermaid ER 图。禁止写字段类型、索引、DDL、ORM 配置。

#### interface_contracts
模块间/服务间通信模式（REST/gRPC/MCP/消息队列）、数据契约、版本策略。禁止写请求/响应 Schema、Header 定义、字段校验规则、幂等策略。

#### module_responsibilities
每个模块的输入、输出、核心职责、对外依赖。禁止写内部类图、函数签名、实现细节。

#### project_structure（V2.2 新增）

基于 `system_architecture` 的分层决策和 `tech_stack` 的技术选型，推导项目源码目录结构。

- 目录结构必须与架构分层严格对应（如 DDD → `domain/` / `application/` / `infrastructure/`；MVC → `controllers/` / `services/` / `repositories/` / `models/`）
- 每个目录标注：对应架构层、允许存放的文件类型、禁止存放的内容
- 按模块划分子包/子目录，与 `03-functional-structure.md` 中的模块名保持一致（kebab-case）
- 输出格式：ASCII tree + 目录职责说明表格

```markdown
src/
├── domain/              # 领域层：实体、值对象、领域服务
│   ├── order/           # 订单模块（对应 feature-01-order）
│   └── user/            # 用户模块（对应 feature-02-user）
├── application/         # 应用层：用例、DTO、Mapper
├── infrastructure/      # 基础设施层：Repository 实现、外部服务客户端
└── interfaces/          # 接口层：Controller、消息队列消费者
```

禁止写具体类名、文件名、函数签名。只定义目录层级和职责边界。

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
全局错误处理与重试策略。必须包含：
- **错误分类**：业务错误 / 系统错误 / 网络错误 / AI 模型错误（AI 项目）
- **处理策略**：降级 / 重试 / 熔断 / 人工介入
- **重试策略**：指数退避、最大重试次数、死信队列
- **与 rollback-plan.md 的衔接**：明确哪些错误类别触发回滚，哪些仅触发告警

禁止写单接口异常码、补偿事务、日志格式。

#### deployment_architecture
容器化/K8s/Serverless 拓扑、CI/CD 流程。生成 Mermaid 部署拓扑图。

#### test_strategy
测试金字塔、分层策略、自动化覆盖率目标、测试边界定义。禁止写单测用例、Mock 策略、数据构造方案。

#### extensibility_design（可选，FOCUS_ON_EXTENSIBILITY=true）
功能添加/修改/集成模式，预留扩展点。参考 `references/section-templates.md` 扩展性框架。

#### decision_records（可选，INCLUDES_DECISION_RECORDS=true）
关键决策正向论证：Context / Factors / Decision / Consequences / Future Flexibility。至少覆盖架构模式选择、技术栈选择、数据存储选型。

#### operations_architecture（V2.1 新增）
运维监控架构、日志/链路追踪/指标三支柱方案、告警分级策略（P0/P1/P2）、SLO/SLA 定义、可观测性数据流。禁止写具体监控项阈值、Dashboard JSON、告警通知人配置。

#### rollback_plan（V2.1 新增，AI 项目必选）
回滚触发条件（如错误率 > 1%、核心功能不可用）、回滚步骤（代码回滚 → 配置回滚 → 数据回滚）、数据库回滚脚本清单、灰度/金丝雀策略、回滚验证检查点。禁止写具体脚本内容、连接串、密钥。

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
00-introduction.md              # 新增：引言、范围、术语、参考资料
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
14-operations-architecture.md
15-rollback-plan.md             # 同时生成 ops/rollback-plan.md 副本
16-extensibility-design.md      # 可选
17-decision-records.md          # 可选
18-governance-rules.md          # 可选
19-design-considerations.md     # 新增：假设、约束、依赖、风险
20-project-structure.md         # 新增（V2.2）：源码目录结构规范与目录骨架创建规则
```

> **rollback-plan.md 双写规则**：一份保存在变更目录 `design/15-rollback-plan.md`，另一份同步更新项目级 `ops/rollback-plan.md`（若存在）。确保回滚方案与变更绑定，同时项目级 ops 目录保持最新。
>
> **project-structure.md 输出规则（V2.2 新增）**：`20-project-structure.md` 作为设计文档的一部分保存到 `design/` 目录。目录骨架的物理创建推迟到 Gate 2 签字之后，避免评审不通过时产生无效目录。

### Step 7: 触发 self-check
自动调用 `self-check` skill 校验一致性、完整性、交叉引用有效性、边界合规性。

### Step 8: 🚪 Gate 2 设计冻结（V2.1 新增）
self-check 通过后，自动宣读阻塞提示：

```text
========================================
🚪 Gate 2: 设计冻结 —— 等待人工评审
========================================
产出物已保存至：openspec/changes/{变更名}/design/

请评审以下内容：
1. 技术选型是否符合团队现有技术债与能力栈
2. 数据流与部署架构是否满足 NFR 中的性能/安全指标
3. 全局状态机是否与详细需求中的模块状态描述兼容
4. rollback-plan.md 中的回滚步骤是否可操作（特别是数据库回滚）
5. operations-architecture 中的告警策略是否覆盖核心链路
6. project-structure.md 中的目录分层是否与 system_architecture 的架构分层一致

确认后执行：/skill:human gate=Gate2 action=sign-off
⚠️ 未获得人工确认前，禁止进入 detailed-design 或编码实现阶段。
```

等待人工签字后：
1. 将设计文件头部状态更新为"已冻结"
2. 调用 `progress-tracker`，标记阶段 3 为"已完成"
3. 读取 `20-project-structure.md`，在项目源码根目录创建对应的空目录骨架（`mkdir -p`）。只创建目录，不创建任何代码文件；若目录已存在，跳过不覆盖。创建完成后输出目录树供用户确认
4. 提示用户可并行启动 `monitoring-setup` 生成监控规则初稿

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
- [ ] 将运维监控阈值写入 `operations-architecture` → 应移至 `monitoring-setup/monitoring-rules.yaml`
- [ ] 将数据库回滚脚本写入 `rollback-plan` → 应移至 ops 目录下的独立脚本文件，plan 中只写脚本清单和触发条件

## 需求可追溯性格式（每个设计文件末尾强制附加）

每个设计文件（`00-introduction.md` 至 `19-design-considerations.md`）末尾必须包含以下段落：

```markdown
### 需求可追溯性

| 需求编号 | 需求描述（来自 `specs/02-requirements-list.md`） | 本文件对应章节 | 验证方式 |
|---------|---------------------------------------------|-------------|---------|
| REQ-XXX | [需求原文摘要] | [章节编号/标题] | [评审类型] |
```

- 若某文件不直接回应任何需求，标注"本文件为架构支撑文档，不直接映射单一需求"
- `rollback-plan.md` 必须追溯至 `05-non-functional.md` 中的可靠性/可用性需求
- `19-design-considerations.md` 的风险项必须追溯至 `brainstorming/requirement-draft.md` 中的风险点

## 下游消费

| 下游 Skill | 消费文档 | 衔接规则 |
|---|---|---|
| `detailed-design` | `design/*.md` + `20-project-structure.md` | 基于已有目录骨架按模块逐一下钻，填充类/接口文件 |
| `task-breakdown` | `design/*.md` + `detail-design/feature-*/design.md` | 基于架构分层拆解任务 |
| `monitoring-setup` | `14-operations-architecture.md` | 基于运维架构生成监控规则初稿 |
| `human` | `design/*.md` + `rollback-plan.md` | Gate 2 人工冻结确认与决策记录 |

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
- **ADR 流于形式**：若输出决策记录或 `02-tech-stack.md` 中的架构策略，必须包含"备选方案及排除原因"，否则视为不完整
- **引言不可空泛**：`00-introduction.md` 的术语表必须与 `specs/02-requirements-list.md` 严格一致，发现术语冲突时标记 BLOCKER
- **设计考量必须量化**：`19-design-considerations.md` 的风险项必须标注影响等级（高/中/低），禁止只列风险不列缓解策略
- **错误处理与回滚联动**：`11-exception-handling-global.md` 必须明确哪些错误类别触发 `rollback-plan.md` 中的回滚步骤，未明确联动视为 WARNING
- **图表一致性**：Mermaid 图表必须从文本架构描述自动生成，禁止图表与文字描述矛盾。
- **rollback-plan 必须可执行**：回滚步骤不能只写"回滚数据库"，必须明确到"执行 rollback-v1.2.sql → 验证核心表数据行数 → 切换流量"。不可操作的回滚方案 = BLOCKER。
- **运维架构不是运维手册**：`operations-architecture` 只定义监控三支柱的架构方案（用什么采集、存储、展示），不写具体 Dashboard 配置或告警通知人。
- **Gate 2 必须确认 rollback-plan**：很多技术债的根源是"能上线不能回滚"，人工必须逐条确认回滚步骤的可操作性。
