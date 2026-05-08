# high-level-design（概要设计生成器）设计文档

**版本**: V2.1  
**最后更新**: 2026-05-08  
**对应 Skill**: `skills/sdlc/high-level-design`  
**对应 meta.json 版本**: 1.1.0

---

## 1. 设计目标

`high-level-design` Skill 的核心目标是**在软件交付链路中建立架构决策的单一可信源**，确保影响 ≥2 个模块的跨边界决策在编码前被显式定义、评审并冻结。

具体目标包括：

| 目标编号 | 目标描述 | 验收标准 |
|---------|---------|---------|
| G1 | 正向生成标准化概要设计文档 | 输出覆盖 18 个章节，格式统一，可直接归档 |
| G2 | 阻断未冻结设计进入下游 | Gate 2 未通过时，禁止触发 detailed-design / task-breakdown |
| G3 | 架构可视化自治 | 所有核心视图（架构图、ER 图、时序图、部署拓扑）由 Skill 自发生成，不依赖外部绘图工具 |
| G4 | 配置驱动裁剪 | 按项目规模与领域特征，通过 `config.yaml` 动态决定必需章节 |
| G5 | 运维可观测性预埋 | V2.1 起将 rollback-plan 与运维架构纳入概要设计范畴，实现「设计即运维」左移 |

---

## 2. 核心概念

### 2.1 术语表

| 术语 | 定义 |
|------|------|
| **HLD** (High-Level Design) | 概要设计文档，描述系统组件、接口、数据流与部署关系的架构层文档 |
| **跨模块影响** | 变更触及 ≥2 个业务模块或技术分层（如同时影响订单域与支付域） |
| **Gate 2** | 人工评审闸门，由架构师/技术负责人在 HLD 完成后进行设计冻结审批 |
| **章节模板** | 预定义的 Markdown 文件模板，位于 `assets/templates/` 目录，按编号命名（如 `01-overview.md`） |
| **双写规则** | V2.1 引入的 Rollback Plan 持久化策略：同时写入变更目录与项目级 `ops/` 目录 |
| **图表自治** | Skill 在生成文档时内嵌 Mermaid 语法，无需借助 Draw.io、PlantUML 等外部工具 |

### 2.2 设计哲学

- **严格分层**：HLD 只回答「系统由什么组成、如何交互、部署在哪」，不回答「类怎么写、字段怎么命名」。
- **决策即代码**：架构决策通过配置与模板显性化，避免口头约定。
- **冻结即契约**：Gate 2 通过后，HLD 成为下游（详细设计、任务拆解、监控配置）的输入契约。

---

## 3. 架构设计（IPO 模型）

### 3.1 输入（Input）

| 输入项 | 来源 | 格式 | 必填 | 说明 |
|--------|------|------|------|------|
| PRD 文档 | `prd-generation` Skill 输出 | Markdown | 是 | 功能需求与验收标准 |
| 竞品分析报告 | `competitive-analysis` Skill 输出 | Markdown | 是 | 技术选型参考与差异化约束 |
| `config.yaml` | 用户项目配置 | YAML | 是 | `required_sections`、`project_name`、`domain` 等 |
| Gate 2 审批状态 | 人工闸门 | 枚举值 | 是 | `pending` / `approved` / `rejected` |
| 领域术语表 | 项目资产 | Markdown / JSON | 否 | 统一词汇，避免歧义 |

**config.yaml 关键字段示例**：

```yaml
project_name: order-platform
domain: ecommerce
required_sections:
  - 01-overview
  - 02-architecture-principles
  - 03-system-context
  - 04-functional-architecture
  - 05-technical-architecture
  - 06-data-architecture
  - 07-interface-design
  - 08-deployment-topology
  - 14-operations-architecture      # V2.1 新增
  - 15-rollback-plan              # V2.1 新增
  - 16-security-architecture
  - 17-performance-baseline
  - 18-appendix
skip_sections:
  - 09-non-functional-requirements  # 小型项目可跳过
```

### 3.2 处理（Process）

处理流程分为 5 个阶段：

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  P1: 前置校验  │ -> │  P2: 章节生成  │ -> │  P3: 图表嵌入  │ -> │  P4: 双写处理  │ -> │  P5: 冻结广播  │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
```

#### P1: 前置校验（Pre-flight Validation）

- 检查输入文件完整性（PRD、竞品分析是否存在）。
- 检查 Gate 2 状态：
  - 若状态为 `rejected`，直接终止并返回阻塞提示。
  - 若状态为 `pending`，生成 HLD 草稿但附加 **Gate 2 冻结阻塞提示**（V2.1 新增）。
  - 若状态为 `approved`，进入正式生成流程。
- 解析 `config.yaml`，生成章节任务队列。

#### P2: 章节生成（Section Generation）

按 `required_sections` 顺序，逐个渲染 18 个章节模板。每个章节遵循统一结构：

```markdown
## {章节编号}. {章节标题}

### 设计意图
{基于 PRD 与竞品分析推导的架构决策意图}

### 方案概要
{技术方案简述，控制在 5 条 bullet 以内}

### 关键决策
| 决策点 | 选项 A | 选项 B | 选定方案 | 决策理由 |
|--------|--------|--------|----------|----------|

### 关联章节
- 上游依赖：{章节编号}
- 下游影响：{章节编号}

### 变更记录
| 版本 | 日期 | 变更内容 | 作者 |
|------|------|----------|------|
```

V2.1 新增章节：

- **14-operations-architecture.md**：监控、告警、日志、链路追踪的架构视图。
- **15-rollback-plan.md**：回滚触发条件、回滚步骤、验证清单、影响面评估。

#### P3: 图表嵌入（Diagram Embedding）

对包含架构视图的章节，自动生成 Mermaid 代码块：

| 图表类型 | 适用章节 | Mermaid 类型 |
|---------|---------|-------------|
| 系统上下文图 | 03-system-context | `graph TB` |
| 功能架构图 | 04-functional-architecture | `graph LR` |
| 技术分层图 | 05-technical-architecture | `graph TD` |
| ER 图 | 06-data-architecture | `erDiagram` |
| 接口时序图 | 07-interface-design | `sequenceDiagram` |
| 部署拓扑图 | 08-deployment-topology | `graph LR` + 节点标注 |
| 运维监控图 | 14-operations-architecture | `graph TB` |
| 回滚流程图 | 15-rollback-plan | `flowchart TD` |

图表生成规则：
- 节点命名采用 `域:实体` 格式（如 `order:Service`）。
- 边标注采用 `事件名[协议]` 格式（如 `创建订单[HTTPS]`）。
- 颜色语义：绿色 = 已存在系统，蓝色 = 新增系统，红色 = 外部依赖。

#### P4: 双写处理（Dual Write）

V2.1 新增规则，仅针对 `15-rollback-plan.md`：

```
写入路径 A: {change-dir}/15-rollback-plan.md          (变更级回滚方案)
写入路径 B: {project-root}/ops/rollback-plan.md       (项目级运维资产)
```

双写一致性保障：
- 路径 A 侧重**当前变更**的回滚步骤。
- 路径 B 为**项目级最新有效**回滚方案，每次生成 HLD 时覆盖更新。
- 若双写失败，标记 `rollback_plan_synced: false` 并写入风险日志。

#### P5: 冻结广播（Freeze Broadcast）

Gate 2 通过后：
- 在 HLD 首页追加 **"DESIGN FROZEN @ {timestamp}"** 水印。
- 向下游 Skill（`detailed-design`、`task-breakdown`、`monitoring-setup`）广播冻结事件，附带 HLD 目录路径与校验哈希。

### 3.3 输出（Output）

| 输出产物 | 路径 | 格式 | 说明 |
|---------|------|------|------|
| HLD 主文档 | `{change-dir}/DESIGN.md` | Markdown | 汇总页，含目录与章节链接 |
| 章节文件 | `{change-dir}/{NN}-{section-name}.md` | Markdown | 按编号独立文件 |
| Rollback Plan（双写） | `{change-dir}/15-rollback-plan.md` + `{project-root}/ops/rollback-plan.md` | Markdown | V2.1 新增 |
| 图表文件 | 内嵌于章节 Markdown | Mermaid | 可直接在支持 Mermaid 的渲染器查看 |
| 冻结令牌 | `{change-dir}/.frozen` | 空文件 | Gate 2 通过后创建，作为下游准入凭证 |
| 生成日志 | `{change-dir}/.hld-log.json` | JSON | 记录生成时间、配置快照、校验结果 |

---

## 4. 状态机与数据模型

### 4.1 HLD 生命周期状态机

```
                    ┌─────────────┐
                    │   INITIAL   │
                    └──────┬──────┘
                           │ 收到 PRD + 竞品分析 + config.yaml
                           ▼
                    ┌─────────────┐
         ┌─────────│   DRAFT    │◄─────────────────────────┐
         │         └──────┬──────┘                          │
         │                │ Gate 2 pending                   │
         │                ▼                                  │
         │         ┌─────────────┐     人工审批通过          │
         │         │   PENDING   │────────────────────────►│
         │         │   REVIEW    │                          │
         │         └──────┬──────┘                          │
         │                │ Gate 2 approved                  │
         │                ▼                                  │
         │         ┌─────────────┐                          │
         └─────────│   FROZEN   │─────► 变更触发 ───────────┘
                   └──────┬──────┘     (需重新走 Gate 2)
                          │
                          │ 重大架构变更
                          ▼
                   ┌─────────────┐
                   │  SUPERSEDED │ (旧版本归档)
                   └─────────────┘
```

状态转移规则：

| 转移 | 触发条件 | 副作用 |
|------|---------|--------|
| INITIAL → DRAFT | 输入文件齐全且通过 schema 校验 | 创建输出目录，初始化 `.hld-log.json` |
| DRAFT → PENDING REVIEW | 自动生成完成，Gate 2 状态为 `pending` | 附加阻塞提示水印，禁止下游触发 |
| DRAFT/PENDING REVIEW → FROZEN | Gate 2 状态变为 `approved` | 创建 `.frozen` 令牌，广播冻结事件 |
| FROZEN → DRAFT | 检测到 PRD 或 config.yaml 发生实质性变更 | 作废旧 `.frozen`，更新日志 |
| * → SUPERSEDED | 发布新版 HLD 且旧版不再维护 | 旧版目录移动到 `archive/` |

### 4.2 数据模型

#### 4.2.1 HLD 配置模型（Config Schema）

```yaml
HldConfig:
  type: object
  required:
    - project_name
    - domain
    - required_sections
  properties:
    project_name:
      type: string
      pattern: '^[a-z0-9-]+$'
      maxLength: 64
    domain:
      type: string
      enum: [ecommerce, fintech, saas, iot, gaming, enterprise]
    required_sections:
      type: array
      items:
        type: string
        pattern: '^\d{2}-[a-z-]+$'
      minItems: 5
      maxItems: 18
    skip_sections:
      type: array
      items:
        type: string
        pattern: '^\d{2}-[a-z-]+$'
    gate2_approver:
      type: string
    operations:
      type: object
      properties:
        dual_write_rollback:
          type: boolean
          default: true
        generate_mermaid:
          type: boolean
          default: true
```

#### 4.2.2 章节元数据模型（Section Meta）

```json
{
  "section_id": "15-rollback-plan",
  "section_number": 15,
  "title": "Rollback Plan",
  "version": "2.1",
  "is_new_in_v21": true,
  "diagrams_required": ["flowchart"],
  "dual_write_target": "{project-root}/ops/rollback-plan.md",
  "template_path": "assets/templates/15-rollback-plan.md",
  "cross_module_impact": true
}
```

#### 4.2.3 冻结令牌模型（Freeze Token）

```json
{
  "frozen_at": "2026-05-08T10:30:00Z",
  "approved_by": "arch-lead@company.com",
  "hld_hash": "sha256:abc123...",
  "config_hash": "sha256:def456...",
  "downstream_permitted": [
    "detailed-design",
    "task-breakdown",
    "monitoring-setup"
  ]
}
```

---

## 5. 集成方案

### 5.1 上游依赖

| 上游 Skill | 集成方式 | 数据契约 |
|-----------|---------|---------|
| `prd-generation` | 文件系统约定 | `{project-root}/docs/prd/*.md`，含 `## 功能需求` 与 `## 验收标准` |
| `competitive-analysis` | 文件系统约定 | `{project-root}/docs/competitive-analysis.md`，含 `## 技术选型参考` |
| Human Gate 2 | 人工评审 + 状态文件 | `{change-dir}/.gate2-status`，值为 `pending/approved/rejected` |

### 5.2 下游消费

| 下游 Skill | 触发条件 | 消费内容 |
|-----------|---------|---------|
| `detailed-design` | 检测到 `.frozen` 令牌 | 按 HLD 章节拆分模块详细设计 |
| `task-breakdown` | 检测到 `.frozen` 令牌 | 基于架构组件拆解开发任务 |
| `monitoring-setup` | 检测到 `.frozen` 令牌 | 读取 `14-operations-architecture.md` 生成监控规则 |

### 5.3 文件系统约定

```
{project-root}/
├── docs/
│   ├── prd/
│   │   └── PRD-{feature-id}.md
│   └── competitive-analysis.md
├── design/
│   └── {change-id}/                 <-- HLD 输出目录
│       ├── DESIGN.md
│       ├── 01-overview.md
│       ├── ...
│       ├── 15-rollback-plan.md
│       ├── .frozen                  <-- 冻结令牌（Gate 2 后生成）
│       └── .hld-log.json
├── ops/                             <-- V2.1 项目级运维资产
│   └── rollback-plan.md             <-- 双写目标 B
└── config.yaml
```

---

## 6. 文件格式规范

### 6.1 Markdown 章节规范

- 文件编码：UTF-8，LF 换行。
- 标题层级：章节主标题使用 `##`，子标题使用 `###`，禁止出现 `####` 及以下层级。
- 表格对齐：文本左对齐，数字右对齐。
- Mermaid 块：必须标注 ````mermaid`，且前后空一行。
- 变更记录：每个章节末尾必须包含 `### 变更记录` 表格。

### 6.2 章节编号与命名规范

| 编号 | 文件名 | 英文名 | V2.1 状态 |
|------|--------|--------|----------|
| 01 | 01-overview.md | Overview | 既有 |
| 02 | 02-architecture-principles.md | Architecture Principles | 既有 |
| 03 | 03-system-context.md | System Context | 既有 |
| 04 | 04-functional-architecture.md | Functional Architecture | 既有 |
| 05 | 05-technical-architecture.md | Technical Architecture | 既有 |
| 06 | 06-data-architecture.md | Data Architecture | 既有 |
| 07 | 07-interface-design.md | Interface Design | 既有 |
| 08 | 08-deployment-topology.md | Deployment Topology | 既有 |
| 09 | 09-non-functional-requirements.md | Non-Functional Requirements | 既有 |
| 10 | 10-security-architecture.md | Security Architecture | 既有 |
| 11 | 11-performance-baseline.md | Performance Baseline | 既有 |
| 12 | 12-scalability-plan.md | Scalability Plan | 既有 |
| 13 | 13-integration-strategy.md | Integration Strategy | 既有 |
| 14 | 14-operations-architecture.md | Operations Architecture | **V2.1 新增** |
| 15 | 15-rollback-plan.md | Rollback Plan | **V2.1 新增** |
| 16 | 16-disaster-recovery.md | Disaster Recovery | 既有 |
| 17 | 17-cost-estimation.md | Cost Estimation | 既有 |
| 18 | 18-appendix.md | Appendix | 既有 |

---

## 7. 安全与审计

### 7.1 输入安全

- `config.yaml` 必须通过 YAML Safe Loader 解析，禁止执行任意代码。
- PRD 与竞品分析文档中的 HTML 标签需转义，防止 Markdown 渲染时产生 XSS。

### 7.2 输出安全

- `.frozen` 令牌采用只读文件属性（`chmod 444` 或等效机制）。
- 回滚方案（`15-rollback-plan.md`）涉及生产环境操作，必须包含 **"需运维双人复核"** 警示语。

### 7.3 审计追踪

`.hld-log.json` 必须记录以下字段：

```json
{
  "run_id": "uuid",
  "timestamp": "ISO8601",
  "config_snapshot": { "base64": "..." },
  "inputs_hash": { "prd": "sha256:...", "competitive": "sha256:..." },
  "sections_generated": ["01-overview", "02-..."],
  "gate2_status_at_generation": "pending",
  "dual_write_status": { "rollback_plan": true },
  "errors": [],
  "warnings": ["Gate 2 not approved; downstream blocked"]
}
```

---

## 8. 后期演进方向

| 版本 | 演进项 | 优先级 |
|------|--------|--------|
| V2.2 | 支持 AI 辅助架构决策对比（自动生成决策矩阵评分） | 高 |
| V2.2 | 章节模板插件化，允许用户自定义 `assets/templates/custom/` | 中 |
| V2.3 | 与 `detailed-design` Skill 的反向追溯：当详细设计变更触发架构调整时，自动提示 HLD 重审 | 高 |
| V2.3 | Mermaid 图自动生成 SVG 静态文件，用于邮件/文档离线分发 | 中 |
| V3.0 | 引入架构决策记录（ADR）索引，每个关键决策自动生成独立 ADR 文件 | 低 |
| V3.0 | 支持多语言输出（中英文 HLD 并行生成） | 低 |

---

## 附录 A：接口定义速查

### A.1 Skill 触发接口（伪代码）

```
invoke(skill="high-level-design", inputs={
  "prd_path": "docs/prd/PRD-001.md",
  "competitive_analysis_path": "docs/competitive-analysis.md",
  "config_path": "config.yaml",
  "output_dir": "design/change-001",
  "gate2_status": "pending"   // 或 "approved"
})
```

### A.2 下游准入检查

```python
def permit_downstream(hld_dir: str) -> bool:
    frozen_path = Path(hld_dir) / ".frozen"
    if not frozen_path.exists():
        return False
    token = json.loads((frozen_path).read_text())
    return token["approved_by"] is not None
```
