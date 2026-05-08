# self-check（产出物自查引擎）设计文档

> 版本：V2.1  
> 最后更新：2026-05-08  
> 对应 Skill：`skills/sdlc/self-check`  
> 对应 meta.json version：`1.1.0`

---

## 1. 设计目标

`self-check` 是一个**阶段级质量门控引擎**，目标是在软件交付生命周期的每个关键阶段完成后，对阶段性产出物执行强制性的结构化质量审查。其设计意图包括：

- **零信任原则**：不假设任何上游产出物天然合规，所有交付物必须经过原子化验证。
- **证据溯源**：每一次判定都必须附带可追溯的证据与定位信息。
- **阻塞式门控**：当存在 BLOCKER 级问题时，系统明确禁止流程进入下一阶段，防止缺陷级联扩散。
- **增量演进**：V2.1 在原有 6 个检查维度基础上，新增「交互规格完整性检查」与「UAT 报告质量检查」，以适配详细需求阶段与 UAT 阶段的质量诉求。

---

## 2. 核心概念

### 2.1 术语表

| 术语 | 定义 |
|------|------|
| **阶段（Phase）** | SDLC 中一个具有明确输入与输出的里程碑，共覆盖 12 个阶段。 |
| **检查维度（Dimension）** | 质量审查的观察切面，V2.1 共定义 8 个维度。 |
| **严重度（Severity）** | 问题的影响等级，分为 BLOCKER / WARNING / INFO 三级。 |
| **门控（Gate）** | 基于检查结果判定阶段是否通过准入规则。 |
| **自查报告（Self-Check Report）** | 结构化的审查结果文档，包含问题清单、证据与改进建议。 |
| **原子化验证（Atomic Verification）** | 将检查项拆分为不可再分的最小断言，确保判定结果单一明确。 |

### 2.2 三级严重度语义

- **BLOCKER**：存在事实性错误、内部矛盾、关键缺失或安全红线问题。**存在即禁止流转**。
- **WARNING**：存在潜在风险、规范偏离或建议性改进。**不阻塞流转，但要求显式确认或排期修复**。
- **INFO**：补充性观察、最佳实践提示或文档优化建议。**仅作记录，不影响流程**。

### 2.3 检查维度（V2.1）

| 维度编号 | 维度名称 | 适用阶段示例 | 核心关注点 |
|----------|----------|--------------|------------|
| D1 | 内容一致性 | 全阶段 | 产出物与上游基准（需求、设计、代码）是否一致。 |
| D2 | 内容完整性 | 全阶段 | 必填章节、字段、附件是否齐备。 |
| D3 | 交叉引用有效性 | 设计/开发/测试 | 文档内链接、ID 引用、版本号是否可解析且未失效。 |
| D4 | 无内部矛盾 | 需求/设计/测试 | 同一份产出物内是否存在逻辑冲突或条件互斥。 |
| D5 | 接口一致性 | 开发/集成/测试 | API 定义与实现、契约与调用方是否对齐。 |
| D6 | 覆盖率/测试有效性 | 测试/集成 | 测试用例对需求的覆盖度、断言有效性、无效测试识别。 |
| D7 | 交互规格完整性 | 详细需求阶段 | 交互流程、状态转移、异常分支、边界条件是否完整定义。 |
| D8 | UAT 报告质量 | UAT 阶段 | UAT 结论的可复现性、缺陷分级合理性、遗留风险说明。 |

---

## 3. 架构设计（IPO 模型）

### 3.1 输入（Input）

```
InputSet ::= {
  phase_id          : string,          // 当前阶段标识（如 "PRD_DETAIL", "UAT"）
  artifact_bundle   : Artifact[],      // 阶段产出物集合（文档、代码、测试包等）
  baseline_refs     : Reference[],     // 上游基准引用（用于一致性校验）
  context_rules     : Rule[],          // 阶段专属检查规则子集
  history_reports   : Report[],        // 历史阶段自查报告（用于追踪问题修复闭环）
  user_instructions : string?          // 用户额外补充指令
}
```

### 3.2 处理（Process）

处理流水线采用**多阶段过滤架构**：

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  1. 预处理层     │ -> │  2. 规则加载层   │ -> │  3. 原子验证层   │ -> │  4. 门控判定层   │
│ Preprocessing   │    │ Rule Loading    │    │ Atomic Check    │    │ Gate Decision   │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
```

**1. 预处理层**
- 解析 `artifact_bundle`，提取文本、元数据、结构化字段。
- 建立与 `baseline_refs` 的索引映射，准备差异比对基线。
- 识别产出物类型（Markdown、JSON、Code、Test Report 等），选择对应解析器。

**2. 规则加载层**
- 根据 `phase_id` 从规则库中筛选激活的检查维度集合。
- 将维度展开为原子检查项（Check Item），每个检查项包含：断言表达式、期望结果、严重度、修复建议模板。

**3. 原子验证层**
- 对每个 Check Item 执行验证，产出：
  - `status`: PASS / FAIL / SKIP（当缺少必要输入时跳过）
  - `severity`: BLOCKER / WARNING / INFO（FAIL 时必填）
  - `evidence`: 引用片段、行号、对比差异、计算结果
  - `location`: 文件路径 + 锚点/坐标
  - `suggestion`: 修复建议或参考文档链接

**4. 门控判定层**
- 汇总所有 Check Item 结果。
- 应用门控规则：`∃(status=FAIL ∧ severity=BLOCKER) → Gate=REJECT`
- 生成结构化 `self-check-report.md`。

### 3.3 输出（Output）

```
OutputSet ::= {
  gate_status       : PASS | REJECT | CONDITIONAL_PASS,
  report            : SelfCheckReport,  // 结构化 Markdown 报告
  blocker_count     : int,
  warning_count     : int,
  info_count        : int,
  failed_items      : CheckItem[],      // 仅包含 FAIL 项
  next_action       : string            // 下一步指令（如"修复 BLOCKER 后重新触发"）
}
```

---

## 4. 状态机与数据模型

### 4.1 门控状态机

```
                    ┌─────────────┐
       ┌───────────>│   IDLE      │<────────────┐
       │            │  (等待触发)  │             │
       │            └──────┬──────┘             │
       │                   │ 用户触发 / 阶段完成自动触发
       │                   ▼                    │
       │            ┌─────────────┐             │
       │            │  RUNNING    │             │
       │            │  (执行检查)  │             │
       │            └──────┬──────┘             │
       │                   │                    │
       │         ┌─────────┼─────────┐          │
       │         ▼         ▼         ▼          │
       │    ┌────────┐ ┌────────┐ ┌──────────┐ │
       │    │  PASS  │ │CONDITIONAL│ │ REJECT  │ │
       │    │        │ │  _PASS   │ │         │ │
       │    └───┬────┘ └────┬───┘ └────┬────┘ │
       │        │           │          │       │
       │        ▼           ▼          ▼       │
       │   [进入下一阶段]  [带警告进入]  [停留在当前阶段]
       │                                    │
       └────────────────────────────────────┘
                         修复后重新触发
```

状态转移规则：
- **IDLE → RUNNING**：阶段完成事件或用户显式触发 `self-check` 指令。
- **RUNNING → PASS**：无 FAIL 项，或所有 FAIL 项最高严重度为 INFO。
- **RUNNING → CONDITIONAL_PASS**：存在 WARNING 级 FAIL，但无 BLOCKER。
- **RUNNING → REJECT**：存在至少一个 BLOCKER 级 FAIL。
- **REJECT → IDLE**：用户完成修复后重新触发检查（循环）。

### 4.2 数据模型

#### CheckItem（原子检查项）

```yaml
CheckItem:
  id: string            # 全局唯一，如 "D1-REQ-001"
  dimension: enum       # D1~D8
  phase_scope: string[] # 适用的阶段 ID 列表
  assertion: string     # 自然语言断言描述
  validator_type: enum  # regex | diff | lint | coverage | custom
  validator_config: {}  # 验证器参数
  default_severity: enum # BLOCKER | WARNING | INFO（FAIL 时生效）
```

#### Finding（检查结果实例）

```yaml
Finding:
  check_item_id: string
  status: PASS | FAIL | SKIP
  severity: BLOCKER | WARNING | INFO | null
  artifact_ref: string  # 被检查的文件/对象标识
  location:
    file: string
    line_start: int
    line_end: int
    anchor: string?     # Markdown 锚点或代码符号
  evidence:
    type: diff | quote | metric | link
    payload: string     # 实际证据内容
  suggestion: string    # 修复建议
```

#### SelfCheckReport（自查报告）

```yaml
SelfCheckReport:
  meta:
    skill_version: "V2.1"
    meta_json_version: "1.1.0"
    phase_id: string
    triggered_at: ISO8601
    duration_ms: int
  summary:
    total_checks: int
    passed: int
    failed: int
    skipped: int
    gate_status: PASS | REJECT | CONDITIONAL_PASS
  findings: Finding[]
  appendix:
    rule_version: string
    baseline_refs: string[]
```

---

## 5. 集成方案

### 5.1 触发集成（12 阶段覆盖）

`self-check` 通过阶段完成指令触发，覆盖以下 12 个阶段：

| 序号 | 阶段 | 典型触发指令关键词 |
|------|------|-------------------|
| 1 | 需求概要 | `完成需求概要`、`概要需求评审` |
| 2 | 详细需求 | `完成详细需求`、`交互规格确认` |
| 3 | 技术设计 | `完成技术设计`、`架构评审` |
| 4 | 接口设计 | `完成接口设计`、`API 评审` |
| 5 | 数据库设计 | `完成数据库设计`、`Schema 评审` |
| 6 | 开发实现 | `完成开发`、`代码提交` |
| 7 | 单元测试 | `完成单元测试`、`UT 评审` |
| 8 | 集成测试 | `完成集成测试`、`集成评审` |
| 9 | UAT | `完成 UAT`、`验收报告` |
| 10 | 发布准备 | `准备发布`、`发布评审` |
| 11 | 部署上线 | `部署完成`、`上线检查` |
| 12 | 项目收尾 | `项目归档`、`收尾检查` |

### 5.2 与上下游 Skill 的衔接

- **上游**：`requirement-analysis`、`technical-design-document-generator`、`test-driven-development` 等产出物作为 `artifact_bundle` 输入。
- **下游**：`requesting-code-review` 在代码审查前可调用 `self-check` 对审查输入物进行预检；`release-management` 将 `self-check-report.md` 作为发布清单的必备附件。
- **闭环**：`progress-tracker` 读取报告中的 BLOCKER 列表，自动创建修复任务并追踪状态。

### 5.3 工作流嵌入模式

- **自动门控模式**：阶段完成事件自动触发，无需人工干预。
- **手动触发模式**：用户通过对话指令（如 `/self-check` 或「请对当前产出物进行自查」）显式调用。
- **批量审计模式**：对历史多阶段报告进行回溯性批量检查，用于项目复盘。

---

## 6. 文件格式规范

### 6.1 报告输出规范

自查报告必须输出为**结构化 Markdown**，文件名推荐：`self-check-report-{phase_id}-{timestamp}.md`。

报告固定包含以下章节：

```markdown
# Self-Check Report: {phase_name}

## 元信息
| 字段 | 值 |
|------|-----|
| 阶段 | ... |
| 触发时间 | ... |
| Skill 版本 | V2.1 |
| 门控结果 | PASS / REJECT / CONDITIONAL_PASS |

## 摘要统计
- 总检查项：{N}
- 通过：{N} | 失败：{N} | 跳过：{N}
- BLOCKER：{N} | WARNING：{N} | INFO：{N}

## 详细发现

### BLOCKER
<!-- 每个 BLOCKER 按以下格式 -->
#### [{check_item_id}] {断言标题}
- **位置**：`{file}:{line}`
- **证据**：{evidence}
- **建议**：{suggestion}

### WARNING
<!-- 同上 -->

### INFO
<!-- 同上 -->

## 下一步行动
{根据 gate_status 生成的明确指令}
```

### 6.2 meta.json 扩展字段

```json
{
  "name": "self-check",
  "version": "1.1.0",
  "pattern": "reviewer",
  "tags": ["sdlc", "quality-gate", "audit", "verification"],
  "platforms": ["kimi", "claude", "cursor"],
  "dimensions_count": 8,
  "severity_levels": ["BLOCKER", "WARNING", "INFO"],
  "phase_coverage": 12
}
```

---

## 7. 安全与审计

### 7.1 安全约束

- **禁止绕过**：任何 BLOCKER 不得通过用户指令（如「忽略这个问题」）直接跳过；必须提供修复证据并重新触发检查。
- **输入隔离**：检查引擎不执行产出物中的可执行代码（如脚本），仅进行静态分析或文本比对。
- **敏感信息扫描**：D2（内容完整性）和 D4（无内部矛盾）检查项默认包含硬编码密钥、Token、密码正则模式，发现即 BLOCKER。

### 7.2 审计追踪

- 每次检查生成唯一的 `report_id`（UUIDv4）。
- 报告元信息中记录 `triggered_at`、`duration_ms` 和 `rule_version`。
- 历史报告保留在 `.kimi/audit/self-check/` 目录（建议），用于项目复盘和合规审计。
- 状态转移日志（IDLE → RUNNING → REJECT → RUNNING → PASS）应被完整记录。

---

## 8. 后期演进方向

### 8.1 短期（V2.2）

- **规则热更新**：支持从外部 URL 或 Git 仓库动态拉取检查规则，无需更新 Skill 本体。
- **增量检查**：仅对变更部分执行检查，降低大型项目报告生成耗时。
- **自定义维度**：允许项目级 `self-check.config.yaml` 注册团队专属检查维度。

### 8.2 中期（V3.0）

- **多模态检查**：扩展至架构图、UI 截图、API 契约的可视化一致性比对。
- **智能严重度调整**：基于历史数据和项目上下文，由模型动态调整 WARNING/BLOCKER 边界（需人工确认）。
- **与 CI/CD 集成**：提供 JSON 输出模式，供 GitHub Actions / GitLab CI 解析并生成检查注解。

### 8.3 长期（V4.0）

- **预测性质量分析**：基于历史阶段缺陷分布，预测下一阶段高风险维度并提前预警。
- **跨项目知识库**：将 Findings 聚合为企业级知识库，识别重复性规范违规并自动生成团队规范补丁。

---

## 附录：版本变更日志

| 版本 | 日期 | 变更内容 |
|------|------|----------|
| V1.0 | — | 基础 6 维度检查框架、三级严重度、阻塞门控。 |
| V2.0 | — | 扩展至 12 阶段全覆盖、结构化报告模板。 |
| V2.1 | 2026-05 | 新增 D7（交互规格完整性）、D8（UAT 报告质量）；优化报告可读性；meta.json 升级至 1.1.0。 |
