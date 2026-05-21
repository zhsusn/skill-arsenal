---
name: detailed-design
description: 当用户提到'详细设计'、'detailed-design'、'按模块输出技术细节'、'生成DDL'、'接口定义'、'状态机细化'或基于已冻结概要设计和详细需求需要进入模块级详细设计阶段时触发。逐模块输出可编码的技术细节，衔接概要架构与编码实现。
---

# Detailed Design（详细设计）

按模块输出详细设计文档，将概要设计的架构约束落地为可编码的技术细节。

## 适用场景

- `high-level-design` 评审通过（Gate 2 已签字）且 `detailed-requirements` 评审通过（Gate 2.5 已签字）
- 需要基于概要设计的架构约束，为每个功能模块生成可编码的技术细节
- 需要自动生成 DDL、OpenAPI/Swagger 接口定义、模块内部状态机 Mermaid 图
- 需要将详细需求中的功能点一一映射到技术实现方案

## 核心职责

1. **逐模块独立输出**：基于 `detail-design/feature-XX-{模块名}/` 目录，为每个模块生成 5 个标准文件
2. **架构约束继承**：概要设计中的技术选型、安全策略、部署约束必须向下传导
3. **功能点映射**：详细需求中的每个功能点必须有对应的实现方案
4. **自动化生成**：自动生成 DDL 语句、索引建议、OpenAPI 格式接口、状态机 Mermaid 图
5. **模块间矛盾检测**：检测两个模块对同一数据表字段定义冲突、接口不兼容等问题
6. **测试前置**：在编码前定义单测用例和集成测试场景，与 TDD 纪律衔接

## 前置依赖

| 上游 Skill | 产出物 | 用途 | 是否必需 |
|---|---|---|---|
| `high-level-design` | `design/*.md`（16 个文件） | 架构约束、技术选型、全局状态机 | **必须** |
| `detailed-requirements` | `feature-*/spec.md` 等 | 功能规格、io-table、logic、prototype | **必须** |
| `human` | `human-decisions.md` | Gate 2 与 Gate 2.5 签字状态 | **必须** |
| `competitive-analysis` | `competitive-analysis.md` | 技术选型参考 | 建议 |

> **硬性阻断**：Gate 2 或 Gate 2.5 未签字时，禁止启动详细设计。

## 输入数据

| 输入来源 | 具体内容 |
|----------|----------|
| 概要设计 | `design/*.md`：系统架构、技术选型、数据架构、部署架构等 16 个文件 |
| 详细需求 | `specs/feature-*/spec.md`：功能规格与验收标准 |
| 详细需求 | `specs/feature-*/io-table.md`：输入输出字段表 |
| 详细需求 | `specs/feature-*/logic.md`：业务逻辑与状态机 |
| 详细需求 | `specs/feature-*/prototype.md`：页面原型文字化布局 |
| 配置 | `openspec/config.yaml`：`high-level-design.required_sections` |

## 处理逻辑

### Step 1：约束加载与模块识别

1. 读取 `openspec/config.yaml` 中 `high-level-design.required_sections` 作为输出模板约束
2. 自动解析 `03-functional-structure.md` 或扫描 `specs/feature-*/` 目录获取模块清单
3. 读取 `design/*.md` 提取架构约束：技术栈、安全策略、性能指标、全局状态机

> **Constitution 约束传导（借鉴 developer-kit）**：将概要设计中的技术栈、安全约束、CWE 映射视为不可偏离的"架构 DNA"。详细设计阶段任何偏离均视为 BLOCKER。

### Step 2：逐模块生成（串行）

对每个 `feature-XX-{模块名}` 独立生成 5 个文件：

#### design.md — 模块内部架构与组件设计

- 模块内部分层（Controller / Service / Repository / Domain）
- 类 / 函数设计（签名、职责、依赖关系）
- 核心算法逻辑（伪代码或流程图）
- 模块依赖图（Mermaid graph TD）
- 必须遵循概要设计的分层约束，禁止擅自变更技术栈
- **代码风格传导**：类/函数命名、签名风格必须与项目代码规范一致。Python 项目遵循 `python-google-style`（snake_case、类型注解、Google docstring）；Java 项目遵循 `java-alibaba-style`（UpperCamelCase/lowerCamelCase、包装类型、Javadoc 注释）
- **公共组件引用**：若模块依赖 `shared/design.md` 中的公共算法/基类/工具类，在"依赖公共组件"章节列出：组件名、引用路径（`../shared/design.md#组件名`）、使用场景。禁止在模块目录内重复定义公共组件

#### api-spec.md — 接口定义

- RESTful / gRPC / MCP / 消息队列端点清单（方法、路径、Content-Type）
- 请求 / 响应字段表（字段名、类型、必填、约束、示例）
- 错误码定义（HTTP 状态码 + 业务错误码 + 错误消息模板）
- 权限与鉴权要求（RBAC 角色、OAuth2 scope）
- 幂等策略与限流配置
- 输出标准 OpenAPI 3.1 YAML 片段，确保与 `interface-first-dev` 零摩擦衔接
- **公共接口引用**：若模块调用 `shared/api-spec.md` 中的公共接口（如通用文件上传、全局搜索），在"依赖公共接口"章节列出：接口名、引用路径（`../shared/api-spec.md#接口名`）、调用场景。模块级 `api-spec.md` 只定义**本模块对外暴露**的接口，禁止将公共接口重复收录到模块目录

#### db-schema.md — 数据表结构

- **本模块独占表**：DDL 语句（CREATE TABLE / INDEX / CONSTRAINT）、字段类型映射、索引策略、缓存 Key 设计、连接池配置建议
- **公共表引用**：若模块使用 `shared/db-schema.md` 中的公共表（如用户表、权限表），在"依赖公共表"章节列出：表名、引用路径（`../shared/db-schema.md#表名`）、使用方式（读/写/关联查询）、本模块对该表的扩展字段（如有）
- **禁止重复定义**：公共表的完整 DDL 必须且只能存在于 `shared/db-schema.md` 中，模块级 `db-schema.md` 禁止重复书写公共表的 CREATE TABLE 语句
- 禁止硬编码连接串、密码

#### state-machine.md — 模块内部状态机

- 将概要设计的全局状态机拆解到模块内部状态流转
- Mermaid `stateDiagram-v2` 语法
- 每个状态转换标注：触发条件、校验规则、异常分支
- 与全局状态机的映射关系（哪个局部状态对应哪个全局状态）

#### test-plan.md — 测试策略

- 单元测试用例（Given/When/Then 格式）
- 集成测试场景（模块间交互、外部服务 Mock 策略）
- 边界条件覆盖（空值、越界、并发、超时）
- 与详细需求验收标准（AC）的追溯关系
- 测试数据构造方案与清理策略

### Step 3：架构视图生成（借鉴 CodeArchDoc）

为每个模块自动生成：
- 模块内类图 / 组件图（Mermaid `classDiagram`）
- 核心流程时序图（Mermaid `sequenceDiagram`）
- ER 子图（仅本模块涉及的实体关系）

> 图表必须与文本描述严格一致，禁止图表与文字矛盾。

### Step 4：模块间矛盾检测（借鉴 reviewing-impl-plans）

所有模块生成完毕后执行 Cross-Module Design Audit：

**模块间矛盾检测**：
- 同名字段在不同模块的 `db-schema.md` 中类型 / 约束是否一致
- 接口 request/response 中同一数据结构的字段是否兼容
- 状态枚举值是否冲突
- 两个模块对同一数据表的写权限是否冲突
- 模块间接口的 request/response/error 格式是否显式定义

**模块与公共内容一致性检测**：
- 模块 `db-schema.md` 中是否存在与 `shared/db-schema.md` 同名的表定义（重复定义 = Error）
- 各模块对同一公共表的"扩展字段"定义是否矛盾（如模块 A 说用户表有 `avatar_url`，模块 B 说没有 = Error）
- 模块 `api-spec.md` 中是否存在与 `shared/api-spec.md` 同名的接口定义（重复定义 = Error）
- 模块 `design.md` 中是否存在与 `shared/design.md` 同名的组件/算法定义（重复定义 = Error）

Error 数量 > 0 时阻塞进入下游阶段，返回修复。

### Step 5：输出后质量门控（借鉴 reviewing-design-docs）

对生成的 5 文件执行"能否不猜就编码"审查：
- 对每个规格项判定 **SPECIFIED / VAGUE / MISSING**
- 检测模糊语言："标准方案"、"按需"、"TBD"、"as needed"
- 检测 magic number、未标注单位的数值
- 接口必须包含完整的 request/response/error 格式
- 数据库设计必须包含完整的 DDL + 索引 + 约束

判定规则：
- MISSING → 🔴 BLOCKER（必须修复）
- VAGUE 数量 ≥ 3 → 🟡 WARNING（建议修复）
- 所有核心接口 SPECIFIED → ✅ 通过

### Step 6：设计质量自评（借鉴 design-exploration）

触发 `/design-assessment` 等效自检（自主执行）：
- 评分维度：完备性、清晰度、准确性、可测试性、可扩展性
- 阻塞维度（完备性、清晰度、准确性）< 3 分时暂停并报告缺口
- 无 CRITICAL 或 HIGH 发现项方可进入下游

### Step 7：保存与触发下游

按模块保存到 `openspec/changes/{变更名}/detail-design/feature-XX-{模块名}/`

同时保存以下两类全局文件到 `openspec/changes/{变更名}/detail-design/` 根目录：

- **`_design-index.md`**：全局模块索引，记录各模块状态、设计版本、追溯关系、变更历史
- **`shared/` 目录**：跨模块公共技术能力，包含被 ≥2 个 feature 共用的数据表、接口、算法/组件

**`shared/` 目录结构**：
```
detail-design/shared/
├── _index.md              # 公共能力目录索引
├── design.md              # 公共算法、公共组件、基类、工具类设计
├── api-spec.md            # 公共接口定义（通用查询、文件上传、认证鉴权等）
└── db-schema.md           # 公共数据表（用户表、权限表、配置表、日志表等）
```

**公共内容判定标准**：
- 被 ≥2 个 feature 的模块设计直接依赖
- 不属于任何一个 feature 的独立业务边界
- 若某表/接口/组件仅被一个 feature 使用，放在该 feature 目录下，不进入 `shared/`

全部模块保存后：
1. 调用 `self-check` skill 执行阶段 4 详细设计自查
2. 调用 `progress-tracker` 更新阶段 4 为"已完成"
3. 提示用户可并行启动 `interface-first-dev` 或 `writing-plans`

## 输出数据

| 产出物 | 内容说明 | 保存路径 |
|--------|----------|----------|
| `design.md` | 模块内部架构、组件划分、类/函数设计、算法逻辑 | `detail-design/feature-XX-{模块名}/` |
| `api-spec.md` | 接口定义（方法/路径/字段/错误码/权限） | `detail-design/feature-XX-{模块名}/` |
| `db-schema.md` | DDL、索引、缓存策略、连接池配置 | `detail-design/feature-XX-{模块名}/` |
| `state-machine.md` | 模块内部状态流转 Mermaid 图、转换条件、异常分支 | `detail-design/feature-XX-{模块名}/` |
| `test-plan.md` | 单测用例、集成场景、边界覆盖、Mock 策略 | `detail-design/feature-XX-{模块名}/` |
| `_design-index.md` | 全局模块索引（状态、版本、追溯关系、变更历史） | `detail-design/` |
| `shared/design.md` | 公共算法、公共组件、基类、工具类设计 | `detail-design/shared/` |
| `shared/api-spec.md` | 公共接口定义（通用查询、文件上传、认证鉴权等） | `detail-design/shared/` |
| `shared/db-schema.md` | 公共数据表（用户表、权限表、配置表、日志表等） | `detail-design/shared/` |

> **结构约定**：`detail-design/` 根目录下，`feature-*/` 为模块私有产出，`shared/` 为跨模块公共技术能力，`_design-index.md` 为全局索引。模块级文件只定义**本模块独占**的内容；对公共内容的依赖通过引用 `shared/` 中的定义实现，禁止在模块目录内重复定义公共表/接口/组件。

## 下游消费

| 下游 Skill | 消费文档 | 衔接规则 |
|---|---|---|
| `interface-first-dev` | `api-spec.md` + `db-schema.md` | 生成 OpenAPI / Swagger 契约 |
| `writing-plans` | `design.md` + `api-spec.md` + `db-schema.md` | 编写实现计划 |
| `task-breakdown` | `design.md` + `api-spec.md` + `state-machine.md` | 拆解开发任务 |
| `executing-plans` | `design.md` + `api-spec.md` + `test-plan.md` | 编码与 TDD 依据 |
| `unit-test` | `test-plan.md` | 补全单测与覆盖率验证 |

## 增量更新支持（借鉴 CodeArchDoc Smart Diff）

当需求发生变更时，支持局部重生成：
1. 对比变更前后的 `specs/feature-*/spec.md` / `specs/feature-*/io-table.md`，识别受影响模块
2. 仅重新生成受影响模块的 5 个文件
3. 未受影响模块保持原设计冻结状态
4. 重生成后重新执行 Cross-Module Audit 和质量门控

## Gotchas

- **Gate 阻断**：Gate 2 或 Gate 2.5 未签字时绝对禁止启动，不可跳过
- **串行生成**：逐个模块输出，防止上下文丢失和编号混乱
- **架构约束不可偏离**：技术栈、安全策略必须与概要设计一致，擅自变更 = BLOCKER
- **字段级细节拦截**：概要设计只定义影响 ≥2 模块的决策，详细设计只定义模块内部细节，二者不可越位
- **状态机映射**：模块状态机必须与概要设计全局状态机兼容，发现冲突时标记 BLOCKER
- **DDL 必须与选型一致**：若概要设计选定 MySQL，禁止在 db-schema 中生成 PostgreSQL 专属语法
- **接口 URI 动词红线**：`api-spec.md` 中禁止出现 `/getOrder`、`/createUser` 等动词 URI，必须使用资源导向路径
- **缓存 Key 禁止硬编码环境信息**：如域名、端口号不得写入缓存 Key 模板
- **测试计划必须追溯 AC**：每个测试用例必须能追溯到详细需求中的至少一个验收标准
- **模糊语言零容忍**：发现"TBD"、"standard approach"、"as needed"等模糊表达，标记 VAGUE 并要求具体化
- **模块间矛盾不可静默忽略**：Cross-Module Audit 发现 Error 时必须返回修复，不可跳过
- **OpenAPI 片段必须可解析**：`api-spec.md` 中的 YAML 片段语法必须正确，确保 `interface-first-dev` 可直接消费
- **禁止在详细设计阶段做架构变更**：若发现概要设计有缺陷，应暂停并反馈用户走架构变更流程，禁止在详细设计中偷偷修正
- **设计锁定原则**：详细设计评审通过后冻结，后续变更需重新执行 `detailed-design` 并走变更流程
- **图表一致性**：Mermaid 图表必须从文本描述自动生成，禁止图表与文字描述矛盾
