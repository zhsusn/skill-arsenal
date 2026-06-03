---
name: high-level-design
description: 当用户要求'概要设计'、'high-level-design'、'HLD'、'系统架构设计'、'技术选型'或基于已冻结 PRD 进入设计阶段时触发。正向生成系统概要设计文档，回答系统拆成几块、数据怎么走、用什么技术栈。
---

# High-Level Design（概要设计）

基于已冻结的产品需求文档（PRD-000，即 `high-level-requirements/00-02.md`），正向生成系统概要设计文档。严格限定为架构层（影响 ≥2 个模块），禁止输出接口字段、类图、DDL、算法参数等详细设计内容。

## 适用场景

- 基于已冻结的 PRD-000 进入阶段 3 概要设计
- 需要确定系统分层/服务划分、技术栈选型、数据架构
- 需要定义模块间接口契约、全局状态机、核心链路时序
- 非功能需求（安全/性能/部署/测试）的架构层策略定义

## 核心职责

1. **正向设计**：基于需求产出目标架构，而非逆向分析现有代码
2. **配置驱动**：按 `config.yaml` 的 `artifact_specs.high-level-design.required_sections` 逐项输出
3. **严格边界**：只输出影响 ≥2 个模块的架构决策，禁止下钻到详细设计
4. **图表自治**：自动生成 Mermaid 架构图、ER 图、时序图、部署拓扑图。所有 Mermaid 图表必须遵循 `mermaid-diagrams` skill 的工程化规范规则（换行符标准化、样式集中声明、subgraph 分组、形状语义化、回流虚线、平行边合并、节点 ID 语义化、路由分离等），并通过其质量检查清单自检。
5. **需求追溯**：每个架构决策必须能追溯到上游需求文档；**每个主题文件末尾必须包含"需求可追溯性"段落**，列出本文件回应的 REQ-XXX 及对应验证方式
6. **运维架构与回滚方案（V2.1）**：输出运维监控架构、告警策略、可观测性方案，并生成 `rollback-plan.md`
7. **主题文件聚合（V3.0）**：将 20+ 个碎片化文件按人工检查视角合并为 6 个主题文件 + 1 份跨文件一致性自检报告，减少文件切换成本约 70%
8. **Gate 2 人工冻结提示（V2.1）**：全部主题文件输出完成后，自动宣读 🚪 Gate 2 阻塞提示，等待人工签字后方可进入详细设计阶段

## 前置依赖

| 上游 Skill | 产出物 | 用途 | 是否必需 |
|---|---|---|---|
| `prd-generation` | `high-level-requirements/00-02.md` | 产品范围、模块清单、需求边界、非功能指标 | **必须** |
| `competitive-analysis` | `design/competitive-analysis.md` | 技术选型论证支撑 | **必须** |
| `detailed-requirements` | `detailed-requirements/feature-*/module-requirements.md` | 模块功能细节，用于覆盖度校验与状态机兼容性核对 | 建议参考 |
| `human` | `human-decisions.md` | Gate 2 签字状态，未通过禁止进入详细设计 | **必须** |

> 概要设计的**核心输入**是 `prd-generation` 产出的概要需求。`detailed-requirements` 仅作为可选的校验基准，**不阻塞**概要设计启动。Gate 2 人工签字是硬性前置条件。

## 执行步骤

### Step 1: 配置加载
- 读取 `openspec/config.yaml` 中 `artifact_specs.high-level-design`
- 确认 `required_sections`、`DETAIL_LEVEL`、`FOCUS_ON_EXTENSIBILITY`、`INCLUDES_DECISION_RECORDS`、`INCLUDES_GOVERNANCE`
- 若配置缺失，使用默认值并发出警告

### Step 2: 上游文档解析
- 解析 `high-level-requirements/02-functional-requirements.md` 提取模块清单（名称、职责、优先级）
- 解析 `high-level-requirements/01-requirements-list.md` 锁定 P0/P1/P2 范围
- 解析 `high-level-requirements/00-requirements-overview.md` 提取性能/安全/可靠性指标
- 解析 `competitive-analysis.md` 提取技术选型结论
- 若已存在 `feature-*/spec.md`，解析并汇总功能点（用于可选的覆盖度校验）

### Step 3: 逐项生成（按主题文件）

每个主题文件内部包含多个原子章节，用 `##` / `###` 分隔。各原子章节的**边界红线独立生效**，物理聚合不改变边界规则。

---

#### 主题一：00-design-overview.md

**合并来源**：原 `00-introduction.md` + `19-design-considerations.md`

内部结构：

```markdown
# 设计总览

## 1. 引言
### 1.1 目的
### 1.2 范围
### 1.3 术语与缩写（与 specs/02-requirements-list.md 保持一致）
### 1.4 参考资料

## 2. 设计考量
### 2.1 假设（业务/技术/环境）
### 2.2 约束（技术/业务/预算/合规）
### 2.3 依赖（外部系统、第三方服务、内部模块及版本）
### 2.4 风险（技术/业务/AI 模型风险，每项含影响等级+缓解策略）

## 3. 设计索引与检查清单

| 主题文件 | 核心决策点 | 风险等级 | 检查状态 |
|---------|-----------|---------|---------|
| 01-architecture-core.md | 分层策略、技术选型、目录结构 | 高 | ☐ |
| 02-data-flow.md | 存储选型、接口模式、模块边界 | 高 | ☐ |
| 03-runtime-behavior.md | 状态流转、核心链路、错误处理 | 高 | ☐ |
| 04-quality-attributes.md | 安全方案、性能基线、部署拓扑 | 中 | ☐ |
| 05-ops-governance.md | 监控覆盖、回滚可操作性 | 高 | ☐ |

## 4. 跨文件一致性重点（源自 self-check-report.md）
> 此处自动引用自检报告中的 ⚠️ 警告项和 ❌ 阻断项，检查者重点确认。

## 5. Gate 2 评审签字区
- [ ] 技术选型符合团队能力栈
- [ ] 数据流与部署架构满足 NFR
- [ ] 全局状态机与模块职责兼容
- [ ] 回滚步骤可操作
- [ ] 告警策略覆盖核心链路
- [ ] 目录分层与架构分层一致

评审人：________ 日期：________
```

**边界红线**：
- 引言：术语表必须与 `specs/02-requirements-list.md` 严格一致，发现术语冲突时标记 BLOCKER
- 设计考量：风险项必须标注影响等级（高/中/低），禁止只列风险不列缓解策略

---

#### 主题二：01-architecture-core.md

**合并来源**：原 `01-system-architecture.md` + `02-tech-stack.md` + `20-project-structure.md` + `17-decision-records.md`（若 `INCLUDES_DECISION_RECORDS=true`，作为本文件附录）

**合并理由**：架构分层决定目录结构，目录结构反映技术栈选型，ADR 记录架构选择的上下文。检查者必须对照阅读，故聚合在同一文件。

内部结构：

```markdown
# 架构核心

## 1. 系统架构
### 1.1 技术架构图（C4-Model：Context→Container→Component）
### 1.2 业务功能架构图（可选，模块≥4时，调用 functional-architecture-generator 方法论）

## 2. 技术栈
### 2.1 选型清单（类别/选型/版本约束/选型理由/竞品溯源）
### 2.2 选型矩阵（方案A/B对比：优点/缺点/决策/适用场景）
### 2.3 关键架构决策（ADR格式：Context/Factors/Decision/Consequences）

## 3. 项目结构
### 3.1 目录树（ASCII，与架构分层严格对应）
### 3.2 目录职责说明表（对应架构层、允许文件类型、禁止内容）

## 4. 决策记录（可选，INCLUDES_DECISION_RECORDS=true）
```

**边界红线（每章独立生效）**：
- 系统架构：禁止写模块内部类图
- 技术栈：禁止展开框架专属模式（如 Spring DI、React Hook）
- 项目结构：禁止写具体类名、函数签名

---

#### 主题三：02-data-flow.md

**合并来源**：原 `03-data-architecture.md` + `04-interface-contracts.md` + `05-module-responsibilities.md`

**合并理由**：数据从哪来（模块职责）、怎么走（接口契约）、存哪里（数据架构），是同一检查视角的三面。

内部结构：

```markdown
# 数据流与模块交互

## 1. 数据架构
### 1.1 逻辑 ER 图（Mermaid）
### 1.2 主数据流向
### 1.3 存储策略与分库分表策略
### 1.4 核心表清单（无字段类型）

## 2. 接口契约
### 2.1 通信模式（REST/gRPC/MCP/消息队列）
### 2.2 数据契约与版本策略

## 3. 模块职责
### 3.1 各模块输入/输出/核心职责/对外依赖
```

**边界红线**：
- 数据架构：禁止写字段类型、索引、DDL、ORM 配置
- 接口契约：禁止写请求/响应 Schema、Header 定义、字段校验规则
- 模块职责：禁止写内部类图、函数签名

---

#### 主题四：03-runtime-behavior.md

**合并来源**：原 `06-state-machine-global.md` + `07-sequence-diagrams.md` + `11-exception-handling-global.md` + `08-algorithm-selection.md`（AI 项目必选）

**合并理由**：运行时行为检查：状态怎么转、流程怎么走、错了怎么办、AI 怎么介入。这四者共同描述系统"活起来"的样子。

内部结构：

```markdown
# 运行时行为

## 1. 全局状态机
### 1.1 跨模块核心实体状态流转（Mermaid 状态图）

## 2. 关键流程时序图
### 2.1 跨模块流程（Mermaid 时序图）

## 3. 异常处理全局
### 3.1 错误分类（业务/系统/网络/AI）
### 3.2 处理策略（降级/重试/熔断/人工介入）
### 3.3 重试策略（指数退避、最大次数、死信队列）
### 3.4 与回滚方案的衔接（哪些错误触发回滚）

## 4. 算法选型（AI 项目必选）
### 4.1 模型基座选择
### 4.2 选型理由与输入输出维度
### 4.3 与其他模块的耦合方式
```

**边界红线**：
- 状态机：禁止写单模块内部状态转换规则、触发事件
- 时序图：禁止写模块内部 Controller→Service→Repository 调用链
- 异常处理：禁止写单接口异常码、补偿事务、日志格式
- 算法选型：禁止写算法流程、参数配置、Prompt 模板

---

#### 主题五：04-quality-attributes.md

**合并来源**：原 `09-security-design.md` + `10-performance-design.md` + `16-extensibility-design.md`（可选，`FOCUS_ON_EXTENSIBILITY=true`）+ `13-test-strategy.md` + `12-deployment-architecture.md`

**合并理由**：非功能需求统一检查，避免安全方案与性能/部署方案冲突（如 HTTPS 卸载影响性能、扩展点设计影响测试边界）。

内部结构：

```markdown
# 质量属性与部署

## 1. 安全设计
### 1.1 认证授权（RBAC/OAuth2）
### 1.2 数据加密策略
### 1.3 网络隔离

## 2. 性能设计
### 2.1 QPS 预估与容量规划
### 2.2 缓存策略（Redis/CDN）
### 2.3 异步化方案

## 3. 扩展性设计（可选，FOCUS_ON_EXTENSIBILITY=true）
### 3.1 功能添加/修改/集成模式
### 3.2 预留扩展点

## 4. 测试策略
### 4.1 测试金字塔与分层策略
### 4.2 自动化覆盖率目标
### 4.3 测试边界定义

## 5. 部署架构
### 5.1 容器化/K8s/Serverless 拓扑（Mermaid 部署图）
### 5.2 CI/CD 流程
```

**边界红线**：
- 性能设计：禁止写缓存 Key 设计、过期策略、连接池配置
- 测试策略：禁止写单测用例、Mock 策略、数据构造方案
- 部署架构：禁止写具体 YAML 配置、Ingress 规则

---

#### 主题六：05-ops-governance.md

**合并来源**：原 `14-operations-architecture.md` + `15-rollback-plan.md` + `18-governance-rules.md`（可选，`INCLUDES_GOVERNANCE=true`）

**合并理由**：运维视角统一：怎么监控、怎么回滚、怎么保架构不腐化。回滚方案与运维架构天然绑定（监控告警触发回滚）。

内部结构：

```markdown
# 运维与治理

## 1. 运维架构
### 1.1 监控三支柱（日志/链路追踪/指标）
### 1.2 告警分级策略（P0/P1/P2）
### 1.3 SLO/SLA 定义
### 1.4 可观测性数据流

## 2. 回滚方案
### 2.1 触发条件（错误率>1%、核心功能不可用）
### 2.2 回滚步骤（代码→配置→数据）
### 2.3 数据库回滚脚本清单（只列清单，不写脚本）
### 2.4 灰度/金丝雀策略
### 2.5 回滚验证检查点

## 3. 治理规则（可选，INCLUDES_GOVERNANCE=true）
### 3.1 架构一致性维护规则
### 3.2 自动化检查建议
### 3.3 架构评审流程定义
```

**边界红线**：
- 运维架构：禁止写具体监控项阈值、Dashboard JSON、告警通知人配置
- 回滚方案：禁止写具体脚本内容、连接串、密钥

**双写规则保留**：
`05-ops-governance.md` 中的回滚方案同时保存为 `ops/rollback-plan.md`（项目级），确保回滚方案与变更绑定，同时项目级 ops 目录保持最新。

---

### Step 4: 边界自检
每生成一个主题文件后，检查内部各原子章节是否越界：
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
按主题文件结构保存到 `openspec/changes/{变更名}/high-level-design/`：

```
00-design-overview.md          # 索引 + 引言 + 设计考量 + Gate 2 签字区
01-architecture-core.md        # 系统架构 + 技术栈 + 项目结构 + 决策记录
02-data-flow.md                # 数据架构 + 接口契约 + 模块职责
03-runtime-behavior.md         # 全局状态机 + 时序图 + 异常处理 + 算法选型
04-quality-attributes.md       # 安全 + 性能 + 扩展性 + 测试策略 + 部署架构
05-ops-governance.md           # 运维架构 + 回滚方案 + 治理规则
```

> **rollback-plan.md 双写规则**：一份保存在变更目录 `design/05-ops-governance.md`（回滚章节），另一份同步更新项目级 `ops/rollback-plan.md`（若存在）。确保回滚方案与变更绑定，同时项目级 ops 目录保持最新。
>
> **project-structure.md 输出规则（V2.2→V3.0 保留）**：`01-architecture-core.md` 中的"项目结构"章节定义目录层级。物理目录骨架的创建推迟到 Gate 2 签字之后，避免评审不通过时产生无效目录。

### Step 7: 边界自检与覆盖度校验（不变）
每生成一个主题文件后，检查内部各原子章节是否越界（字段级、代码级、单模块内部细节）。

### Step 7.5: 跨文件一致性自检（V3.0 新增）
在 Step 7 之后、Step 8 之前，自动执行以下检查并生成 `self-check-report.md`：

**检查维度**：

| 检查项 | 涉及主题文件 | 自动检查逻辑 | 结论等级 |
|--------|-------------|-------------|---------|
| 技术栈覆盖度 | 01-architecture-core ↔ 02-data-flow | 技术栈中声明的存储组件是否覆盖数据架构中的全部存储需求 | ✅/⚠️/❌ |
| 架构-目录一致性 | 01-architecture-core（系统架构 vs 项目结构） | 架构分层与目录层级是否一一对应 | ✅/⚠️/❌ |
| 状态机-模块职责兼容性 | 03-runtime-behavior ↔ 02-data-flow | 全局状态机中的状态是否在模块职责中有对应处理方 | ✅/⚠️/❌ |
| 异常-回滚联动 | 03-runtime-behavior ↔ 05-ops-governance | 异常处理中标记"触发回滚"的类别是否在回滚方案中有步骤 | ✅/⚠️/❌ |
| 性能-部署匹配 | 04-quality-attributes（性能 vs 部署） | QPS 预估与部署拓扑的节点数/规格是否匹配 | ✅/⚠️/❌ |
| 安全-接口契约一致性 | 04-quality-attributes ↔ 02-data-flow | 安全方案要求的认证方式是否与接口契约中的通信模式兼容 | ✅/⚠️/❌ |
| ADR 溯源 | 01-architecture-core ↔ competitive-analysis.md | 每个 ADR 是否能在竞品分析中找到支撑 | ✅/⚠️/❌ |

**结论等级**：
- ✅ 通过：机器判定一致，人工可快速跳过
- ⚠️ 警告：存在潜在不一致，人工必须确认
- ❌ 阻断：明确冲突，必须修复后才能进入 Gate 2

**与 Gate 2 的衔接**：
`00-design-overview.md` 的"跨文件一致性重点"章节自动引用本报告中所有 ⚠️ 警告和 ❌ 阻断项。检查者在此文件中即可完成重点确认。

**报告保存路径**：`openspec/changes/{变更名}/high-level-design/self-check-report.md`

### Step 8: 🚪 Gate 2 设计冻结（V3.0 修订版）

self-check 与跨文件一致性检查通过后，自动宣读阻塞提示：

```text
========================================
🚪 Gate 2: 设计冻结 —— 等待人工评审
========================================
产出物已保存至：openspec/changes/{变更名}/high-level-design/

请按以下顺序评审：
1. 打开 00-design-overview.md，确认索引表与检查清单
2. 对照 self-check-report.md 中的 ⚠️ 警告/❌ 阻断项重点检查
3. 按需下钻到 01-05 主题文件确认细节

评审焦点：
- 技术选型是否符合团队现有技术债与能力栈（01-architecture-core.md）
- 数据流与部署架构是否满足 NFR 中的性能/安全指标（02 + 04）
- 全局状态机是否与详细需求中的模块状态描述兼容（03-runtime-behavior.md）
- 回滚步骤是否可操作（05-ops-governance.md）
- 告警策略是否覆盖核心链路（05-ops-governance.md）
- 目录分层与架构分层是否一致（01-architecture-core.md）

确认后执行：/skill:human gate=Gate2 action=sign-off
⚠️ 未获得人工确认前，禁止进入 detailed-design 或编码实现阶段。
```

等待人工签字后：
1. 将 `00-design-overview.md` 头部状态更新为"已冻结"
2. 调用 `progress-tracker`，标记阶段 3 为"已完成"
3. 读取 `01-architecture-core.md` 中的项目结构章节，在项目源码根目录创建对应的空目录骨架（`mkdir -p`）。只创建目录，不创建任何代码文件；若目录已存在，跳过不覆盖。创建完成后输出目录树供用户确认
4. 提示用户可并行启动 `monitoring-setup` 生成监控规则初稿

## 阶段切换门控

- 概要设计评审通过（用户确认）
- `self-check` 无 BLOCKER
- 跨文件一致性自检无 ❌ 阻断
- **禁止在概要设计评审通过前进入 `detailed-design` 或编码实现**

## 常见陷阱检查清单

| 原陷阱 | 新位置 | 拦截规则 |
|--------|--------|----------|
| 接口字段校验写入 interface-contracts | 02-data-flow.md §2 | 应移至 detailed-design/api-spec.md |
| 数据库字段/索引写入 data-architecture | 02-data-flow.md §1 | 应移至 detailed-design/db-schema.md |
| 算法参数写入 algorithm-selection | 03-runtime-behavior.md §4 | 应移至 detailed-design/algorithm.md |
| 单模块状态机写入 state-machine-global | 03-runtime-behavior.md §1 | 应移至 detailed-design/state-machine.md |
| 类图/函数签名写入任何章节 | 任何主题文件 | 应移至 detailed-design/design.md |
| 运维监控阈值写入 operations-architecture | 05-ops-governance.md §1 | 应移至 monitoring-setup/monitoring-rules.yaml |
| 数据库回滚脚本写入 rollback-plan | 05-ops-governance.md §2 | 应移至 ops 目录独立脚本文件，plan 中只写清单 |

## 需求可追溯性格式（每个主题文件末尾强制附加）

每个主题文件末尾必须包含以下段落，合并后需追溯多个上游需求：

```markdown
### 需求可追溯性

| 需求编号 | 需求描述（来自 `high-level-requirements/01-requirements-list.md`） | 本文件对应章节 | 验证方式 |
|---------|---------------------------------------------|-------------|---------|
| REQ-XXX | [需求原文摘要] | [章节编号/标题] | [评审类型] |
```

- 若某主题文件不直接回应需求，标注"本文件为架构支撑文档，不直接映射单一需求"
- `00-design-overview.md` 中的风险项追溯至 `brainstorming/requirement-draft.md`
- `05-ops-governance.md` 中的回滚方案追溯至 `high-level-requirements/00-requirements-overview.md` 中的可靠性/可用性需求
- `01-architecture-core.md` 中的技术选型追溯至 `competitive-analysis.md`

## 下游消费

| 下游 Skill | 消费文档 | 衔接规则 |
|---|---|---|
| `detailed-design` | `01-05` 主题文件 | 基于 `01-architecture-core.md` 的目录骨架，按模块逐一下钻，填充类/接口文件 |
| `monitoring-setup` | `05-ops-governance.md` §1 | 基于运维架构生成监控规则初稿 |
| `human` | `00-design-overview.md` + `self-check-report.md` | Gate 2 人工冻结确认与决策记录 |

## 深度参考

- 各主题文件详细写作指南与模板见 `references/section-templates.md`
- 边界红线与变更影响范围判定见 `references/boundary-rules.md`

## Gotchas

- **正向设计，非逆向分析**：基于需求生成架构，不是扫描现有代码。若项目已有代码，仅作参考不作依据。
- **边界红线不可越**：概要设计只定义影响 ≥2 模块的决策。任何字段级、代码级、单模块内部细节必须拦截。
- **技术选型必须溯源**：每个技术选型必须关联 `competitive-analysis.md` 结论，无溯源则视为 WARNING。
- **模块遗漏 = BLOCKER**：未覆盖 `03-functional-structure.md` 中 P0 模块的架构设计不得通过自查。
- **状态机兼容**：若提供了详细需求（`feature-*/spec.md`），全局状态机应与其各模块状态描述兼容，发现冲突时标记 BLOCKER。
- **禁止自动下钻**：生成时若 AI 自发输出详细设计内容，必须自我拦截并提升抽象层级，不得直接保存。
- **设计锁定原则**：用户确认评审通过后，概要设计冻结。变更需重新走架构评审会，禁止偷偷修改已冻结文档。
- **ADR 流于形式**：若输出决策记录或 `01-architecture-core.md` 中的架构策略，必须包含"备选方案及排除原因"，否则视为不完整。
- **引言不可空泛**：`00-design-overview.md` 的术语表必须与 `high-level-requirements/01-requirements-list.md` 严格一致，发现术语冲突时标记 BLOCKER。
- **设计考量必须量化**：`00-design-overview.md` 的风险项必须标注影响等级（高/中/低），禁止只列风险不列缓解策略。
- **错误处理与回滚联动**：`03-runtime-behavior.md` §3.4 必须明确哪些错误类别触发 `05-ops-governance.md` 中的回滚步骤，未明确联动视为 WARNING。
- **图表一致性**：Mermaid 图表必须从文本架构描述自动生成，禁止图表与文字描述矛盾。
- **Mermaid 工程规范**：概要设计产出的 Mermaid 图表将被下游详细设计和编码直接消费，必须遵守：节点 ID 语义化（Pg_/Dec_/St_ 前缀）、样式集中声明、subgraph 按阶段分组、回流线用虚线、换行符用 `<br>` 而非 `<br/>`。违反任一项在自检报告中标记 ⚠️ 警告。
- **rollback-plan 必须可执行**：回滚步骤不能只写"回滚数据库"，必须明确到"执行 rollback-v1.2.sql → 验证核心表数据行数 → 切换流量"。不可操作的回滚方案 = BLOCKER。
- **运维架构不是运维手册**：`05-ops-governance.md` §1 只定义监控三支柱的架构方案（用什么采集、存储、展示），不写具体 Dashboard 配置或告警通知人。
- **Gate 2 必须确认 rollback-plan**：很多技术债的根源是"能上线不能回滚"，人工必须逐条确认回滚步骤的可操作性。
- **主题文件聚合不改变边界**：物理上将多个章节放入同一文件，不等于可以混淆边界。各原子章节的禁止项仍然独立生效。
- **自检报告不是形式主义**：跨文件一致性自检中发现的 ❌ 阻断项必须修复后方可进入 Gate 2，禁止人工跳过。
