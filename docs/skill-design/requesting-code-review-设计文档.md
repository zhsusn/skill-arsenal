# requesting-code-review（代码审查）设计文档

> 版本：V2.1  
> 最后更新：2026-05-08  
> 对应 Skill：`skills/sdlc/requesting-code-review`  
> 对应 meta.json version：`1.1.0`

---

## 1. 设计目标

`requesting-code-review` 是一个**分布式质量捕获引擎**，核心目标是在缺陷级联到后续阶段之前，通过代码审查子代理（Subagent）提前拦截问题。其设计意图包括：

- **级联阻断**：在代码合入主干前捕获架构偏离、接口不匹配、安全漏洞等深层问题，避免它们演变为集成测试故障或线上事故。
- **发布前终极门控**：V2.1 新增 UAT 通过后、发布前的强制触发逻辑，确保即使功能验收通过，代码层面仍然经得起最终审视。
- **结构化交付**：V2.1 强制输出 `code-review-report.md`，使审查结论可存档、可追踪、可作为发布清单的前置输入。
- **多模式适配**：支持子代理驱动、计划执行、临时审查、项目交付四种工作流，适配不同团队规模和协作习惯。

---

## 2. 核心概念

### 2.1 术语表

| 术语 | 定义 |
|------|------|
| **审查子代理（Review Subagent）** | 被分派执行代码审查的独立 AI 实例，拥有独立的上下文窗口和分析视角。 |
| **级联缺陷（Cascading Defect）** | 在代码阶段引入、但在后续测试/集成/上线阶段才暴露的缺陷。 |
| **结构化报告（Structured Report）** | 遵循固定章节模板的审查报告，包含结论、问题分级、亮点与行动项。 |
| **发布前门控（Pre-Release Gate）** | UAT 通过后、正式发布前触发的最后一次代码质量审查。 |
| **占位符（Placeholder）** | 审查指令模板中的可替换变量，用于注入上下文信息。 |
| **UAT 交叉验证（UAT Cross-Validation）** | 将 UAT 阶段发现的 issues 与代码变更进行关联性复核。 |

### 2.2 审查报告结构（V2.1 强制输出）

```
code-review-report.md
├── 1. 总体结论（Executive Summary）
│   └── 通过 / 有条件通过 / 拒绝 + 一句话 verdict
├── 2. 阻塞性问题（Blockers）
│   └── 必须修复后方可合入/发布的缺陷
├── 3. 重要问题（Major Issues）
│   └── 显著影响可维护性、性能或安全的问题
├── 4. 轻微问题（Minor Issues）
│   └── 风格、命名、注释优化等建议
├── 5. 亮点（Highlights）
│   └── 值得保留和推广的良好实践
├── 6. UAT 交叉验证（UAT Cross-Validation）
│   └── UAT issues 与代码变更的关联分析
└── 7. 下一步行动（Next Actions）
    └── 明确的修复清单与责任人建议
```

### 2.3 问题严重度定义

- **Blocker**：存在安全漏洞、数据丢失风险、严重性能退化、架构原则违背。**禁止合入/发布**。
- **Major**：存在可维护性风险、边界条件处理缺失、错误处理不完整。**要求修复或提供充分理由**。
- **Minor**：命名不规范、注释缺失、格式不一致。**建议修复，不阻塞**。

---

## 3. 架构设计（IPO 模型）

### 3.1 输入（Input）

```
InputSet ::= {
  workflow_mode     : enum,           // SUBAGENT_DRIVEN | EXECUTING_PLANS | AD_HOC | PROJECT_DELIVERY
  description       : string,         // 变更背景与业务上下文（PLACEHOLDER: DESCRIPTION）
  plan_or_requirements : string,      // 关联的需求或实现计划（PLACEHOLDER: PLAN_OR_REQUIREMENTS）
  diff_context      : DiffBundle,     // 代码变更集合（PLACEHOLDER: BASE_SHA .. HEAD_SHA）
  uat_issues        : Issue[],        // UAT 阶段遗留问题（PLACEHOLDER: UAT_ISSUES）
  review_policy     : Policy,         // 团队审查策略（可选自定义规则）
  target_audience   : enum            // PRE_MERGE | PRE_RELEASE（影响门控严格度）
}

DiffBundle ::= {
  base_sha          : string,
  head_sha          : string,
  changed_files     : FileDiff[],
  total_additions   : int,
  total_deletions   : int
}
```

### 3.2 处理（Process）

处理架构采用**主-从代理协作模型**：

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         requesting-code-review 主控流程                       │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
              ┌───────────────────────┼───────────────────────┐
              ▼                       ▼                       ▼
    ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
    │ 1. 上下文组装层  │     │ 2. 子代理分派层  │     │ 3. 报告聚合层    │
    │ Context Builder │     │ Subagent Router │     │ Report Merge    │
    └────────┬────────┘     └────────┬────────┘     └────────┬────────┘
             │                       │                       │
             ▼                       ▼                       ▼
    ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
    │ - 填充占位符    │     │ - 静态分析代理   │     │ - 冲突消解      │
    │ - 加载审查策略  │     │ - 安全审计代理   │     │ - 严重度仲裁    │
    │ - 关联 UAT 问题 │     │ - 架构评审代理   │     │ - 结构化输出    │
    │ - 切分 Diff 包  │     │ - 性能检查代理   │     │                 │
    └─────────────────┘     └─────────────────┘     └─────────────────┘
```

**1. 上下文组装层（Context Builder）**
- 解析四个占位符（DESCRIPTION, PLAN_OR_REQUIREMENTS, BASE_SHA/HEAD_SHA, UAT_ISSUES）。
- 若 `target_audience=PRE_RELEASE`，自动附加发布前检查清单（如日志级别、配置硬编码、回滚方案可见性）。
- 将大型 Diff 切分为多个子包，供子代理并行处理。

**2. 子代理分派层（Subagent Router）**
- 根据审查策略创建多个专项审查子代理：
  - **静态分析代理**：语法、风格、类型一致性。
  - **安全审计代理**：注入、XSS、密钥硬编码、权限绕过。
  - **架构评审代理**：分层合规、依赖方向、重复代码、圈复杂度。
  - **性能检查代理**：N+1 查询、内存泄漏热点、算法复杂度。
- 各子代理独立输出原始发现（Raw Findings）。

**3. 报告聚合层（Report Merge）**
- **冲突消解**：当多个子代理对同一代码片段给出不同判断时，取最高严重度。
- **严重度仲裁**：由主控引擎根据 `review_policy` 校准严重度边界。
- **UAT 交叉验证**：将 UAT_ISSUES 与代码变更映射，确认 UAT 发现的问题是否在代码层面已有修复痕迹，或存在根因未触及的风险。
- **结构化输出**：强制生成符合 V2.1 模板的 `code-review-report.md`。

### 3.3 输出（Output）

```
OutputSet ::= {
  report            : CodeReviewReport,    // 结构化 Markdown 报告
  verdict           : enum,                // APPROVE | CONDITIONAL_APPROVE | REJECT
  blockers          : Finding[],
  majors            : Finding[],
  minors            : Finding[],
  highlights        : Highlight[],
  uat_cross_check   : CrossCheckResult,    // UAT 关联性分析结果
  next_actions      : ActionItem[]         // 可执行任务列表
}

ActionItem ::= {
  description   : string,
  severity      : enum,
  assignee_hint : string?,   // 建议的修复责任人（基于代码作者或领域）
  eta_hint      : string?    // 建议修复耗时
}
```

---

## 4. 状态机与数据模型

### 4.1 审查生命周期状态机

```
                              ┌─────────────┐
                    ┌────────>│   PENDING   │<────────┐
                    │         │  (等待审查)  │         │
                    │         └──────┬──────┘         │
                    │                │ 触发审查指令    │
                    │                ▼                │
                    │         ┌─────────────┐         │
                    │         │  ANALYZING  │         │
                    │         │  (分析中)    │         │
                    │         └──────┬──────┘         │
                    │                │                │
          ┌─────────┼────────┐       │       ┌───────┼─────────┐
          ▼         ▼        ▼       ▼       ▼       ▼         ▼
    ┌────────┐ ┌────────┐ ┌────────┐   ┌────────┐ ┌────────┐ ┌────────┐
    │APPROVED│ │COND.   │ │REJECTED│   │ABORTED │ │MERGED   │ │RELEASED│
    │        │ │APPROVE │ │        │   │        │ │        │ │        │
    └───┬────┘ └────┬───┘ └───┬────┘   └────────┘ └───┬────┘ └───┬────┘
        │           │         │                         │          │
        ▼           ▼         ▼                         ▼          ▼
   [允许合入]  [带条件合入]  [需修复后重审]           [归档]     [归档]
```

状态说明：
- **PENDING**：审查请求已创建，等待资源分配或用户确认。
- **ANALYZING**：子代理正在执行并行分析。
- **APPROVED**：无 Blocker/Major，可直接合入/发布。
- **CONDITIONAL_APPROVE**：存在 Major/Minor，但无 Blocker；要求修复 Major 后方可进入下一状态。
- **REJECTED**：存在 Blocker，必须修复并重走审查流程。
- **ABORTED**：审查因缺少必要输入（如 Diff 不可读）或用户取消而中止。
- **MERGED**：代码已合入，审查报告归档。
- **RELEASED**：发布前审查通过，报告作为发布清单附件归档。

### 4.2 数据模型

#### CodeReviewReport（审查报告）

```yaml
CodeReviewReport:
  meta:
    skill_version: "V2.1"
    meta_json_version: "1.1.0"
    report_id: UUID
    workflow_mode: enum
    target_audience: enum
    generated_at: ISO8601
    base_sha: string
    head_sha: string
  executive_summary:
    verdict: APPROVE | CONDITIONAL_APPROVE | REJECT
    summary_text: string
    risk_level: LOW | MEDIUM | HIGH
  findings:
    blockers: Finding[]
    majors: Finding[]
    minors: Finding[]
  highlights: Highlight[]
  uat_cross_validation:
    uat_issue_count: int
    addressed_count: int
    partially_addressed_count: int
    not_addressed_count: int
    risk_items: string[]
  next_actions: ActionItem[]
```

#### Finding（审查发现）

```yaml
Finding:
  id: string              # 如 "SEC-001"
  category: enum          # SECURITY | ARCHITECTURE | PERFORMANCE | MAINTAINABILITY | CORRECTNESS
  severity: enum          # BLOCKER | MAJOR | MINOR
  file: string
  line_range: [int, int]
  code_snippet: string
  description: string     # 问题描述
  root_cause: string?     # 根因分析（Blocker/Major 必填）
  recommendation: string  # 修复建议
  reference_links: string[]
```

#### Highlight（亮点）

```yaml
Highlight:
  id: string
  file: string
  line_range: [int, int]
  code_snippet: string
  description: string     # 为什么这是好实践
  promote_suggestion: string?  # 是否建议推广到其他模块
```

---

## 5. 集成方案

### 5.1 四种工作流集成

#### 模式 A：Subagent-Driven（子代理驱动）

- **适用**：大规模变更（>20 文件或 >500 行变更），需要多维度深度审查。
- **流程**：
  1. 主控 Skill 接收审查请求。
  2. 自动创建 3-4 个专项子代理，分别负责安全、架构、性能、可维护性。
  3. 子代理并行分析，输出 Raw Findings。
  4. 主控聚合、仲裁、生成结构化报告。
- **优势**：利用多代理并行，突破单上下文长度限制。

#### 模式 B：Executing Plans（计划执行集成）

- **适用**：已有明确的 `executing-plans` Skill 执行计划，代码审查作为计划中的一个标准步骤。
- **流程**：
  1. 执行计划进入「代码审查」步骤。
  2. `requesting-code-review` 自动读取计划中的 `BASE_SHA` 和 `HEAD_SHA`。
  3. 输出报告后，计划自动解析 `next_actions` 并创建后续修复任务。
- **优势**：无缝嵌入既有工作流，无需额外触发指令。

#### 模式 C：Ad-Hoc（临时审查）

- **适用**：突发性的代码审查需求，如线上热修后的紧急 review、同事随手发的代码片段。
- **流程**：
  1. 用户粘贴代码片段或提供 PR 链接。
  2. Skill 识别为 Ad-Hoc 模式，跳过 SHA 占位符填充。
  3. 执行轻量级单代理审查，快速输出结论。
- **优势**：低门槛、快反馈。

#### 模式 D：Project Delivery（项目交付集成）

- **适用**：项目收尾阶段的全量代码基线审查，或技术交接前的兜底 review。
- **流程**：
  1. 扫描项目全量代码（而非仅 Diff）。
  2. 结合需求文档和测试报告，做端到端一致性审查。
  3. 输出完整的项目级审查报告，作为交付物之一。
- **优势**：覆盖基线质量，而不仅是增量质量。

### 5.2 与 release-management 的衔接

`code-review-report.md` 是发布清单（Release Checklist）的**前置输入**：

```
[requesting-code-review] ---(code-review-report.md)---> [release-management]
                                                              │
                                                              ▼
                                                  ┌─────────────────────┐
                                                  │ 发布清单必备附件：   │
                                                  │ - code-review-report│
                                                  │ - self-check-report │
                                                  │ - UAT sign-off      │
                                                  └─────────────────────┘
```

发布管理 Skill 在生成发布清单时：
- 检查 `code-review-report.md` 是否存在且 verdict ≠ REJECT。
- 若存在未关闭的 Blocker，发布清单标记为「不可发布」。
- 将 UAT 交叉验证结果与发布风险声明合并展示。

### 5.3 Placeholder 注入规范

| 占位符 | 来源 | 用途 | 是否必填 |
|--------|------|------|----------|
| `DESCRIPTION` | 用户对话或 PR 描述 | 业务上下文 | 是 |
| `PLAN_OR_REQUIREMENTS` | 关联的需求文档或执行计划 | 一致性审查基准 | 是 |
| `BASE_SHA` | Git 差异基线 | 代码范围定义 | 是（除 Ad-Hoc） |
| `HEAD_SHA` | Git 差异目标 | 代码范围定义 | 是（除 Ad-Hoc） |
| `UAT_ISSUES` | UAT 阶段输出 | 交叉验证数据源 | 仅 PRE_RELEASE |

---

## 6. 文件格式规范

### 6.1 报告输出规范

文件名固定为：`code-review-report.md`（或带时间戳版本）。

```markdown
# Code Review Report

## 元信息
| 字段 | 值 |
|------|-----|
| 审查模式 | Subagent-Driven / Executing Plans / Ad-Hoc / Project Delivery |
| 目标受众 | Pre-Merge / Pre-Release |
| 基线范围 | `BASE_SHA`..`HEAD_SHA` |
| 生成时间 | ... |
| Skill 版本 | V2.1 |

## 总体结论
**裁决：APPROVE / CONDITIONAL_APPROVE / REJECT**
**风险等级：LOW / MEDIUM / HIGH**
{一句话总结}

## 阻塞性问题（Blockers）
> 存在 Blocker 时，本代码不可合入或发布。

### [SEC-001] {标题}
- **文件**：`{file}` `{start_line}-{end_line}`
- **代码**：
  ```{lang}
  {snippet}
  ```
- **问题**：{description}
- **根因**：{root_cause}
- **建议**：{recommendation}
- **参考**：{links}

## 重要问题（Major Issues）
<!-- 同上格式 -->

## 轻微问题（Minor Issues）
<!-- 同上格式 -->

## 亮点（Highlights）
### [HL-001] {标题}
- **文件**：...
- **说明**：...
- **推广建议**：...

## UAT 交叉验证
- UAT 问题总数：{N}
- 已完全解决：{N} | 部分解决：{N} | 未触及：{N}
- **风险提示**：{如果存在未触及的 UAT 问题，说明代码层面未修复根因}

## 下一步行动
1. [BLOCKER] {action} — 建议由 {assignee} 在 {eta} 内完成
2. [MAJOR] {action} — ...
3. ...
```

### 6.2 meta.json 扩展字段

```json
{
  "name": "requesting-code-review",
  "version": "1.1.0",
  "pattern": "reviewer",
  "tags": ["sdlc", "code-review", "quality-gate", "subagent", "pre-release"],
  "platforms": ["kimi", "claude", "cursor"],
  "report_schema_version": "2.1",
  "supports_workflows": ["subagent-driven", "executing-plans", "ad-hoc", "project-delivery"],
  "release_gate_enabled": true
}
```

---

## 7. 安全与审计

### 7.1 安全约束

- **密钥零容忍**：安全审计代理对硬编码密钥、Token、密码连接串执行绝对 BLOCKER 策略，不因任何业务理由降级。
- **注入防护**：审查报告中不得直接执行被审查代码；所有代码片段以 Markdown 代码块形式静态展示。
- **权限最小化**：子代理仅接收与审查相关的 Diff 内容，不访问完整代码库无关区域。

### 7.2 审计追踪

- 每次审查生成全局唯一的 `report_id`。
- 报告元信息记录 `base_sha`、`head_sha`、`workflow_mode`、`generated_at`。
- 历史报告建议归档至 `.kimi/audit/code-review/`。
- 发布前审查（PRE_RELEASE）的报告必须永久保留，作为合规审计依据。

---

## 8. 后期演进方向

### 8.1 短期（V2.2）

- **增量审查**：仅审查自上次审查后新增的变更，减少重复评审。
- **团队风格配置**：支持项目级 `.codereview-policy.yaml`，自定义团队编码规范与严重度映射。
- **评论级集成**：支持直接输出 GitHub/GitLab PR Review Comment 格式的 JSON，一键导入。

### 8.2 中期（V3.0）

- **语义化 Diff**：不仅看文本差异，还分析变更对调用链、数据流、API 契约的影响。
- **智能责任人推荐**：基于代码作者历史、模块所有权、问题类型，自动建议最优修复人。
- **审查疲劳检测**：当同一文件被反复审查时，自动提示"该模块可能需要重构"。

### 8.3 长期（V4.0）

- **预测性审查**：基于历史缺陷模式，在开发者编码时实时提示高风险变更区域（IDE 集成）。
- **跨项目知识迁移**：将 A 项目的审查发现沉淀为规则，自动应用于 B 项目的同类场景。
- **人机协作闭环**：与人类 Reviewer 的评审结论进行比对学习，持续校准 AI 审查标准。

---

## 附录：版本变更日志

| 版本 | 日期 | 变更内容 |
|------|------|----------|
| V1.0 | — | 基础代码审查框架，支持单代理审查与简单报告。 |
| V2.0 | — | 引入子代理驱动模式、四种工作流、占位符系统。 |
| V2.1 | 2026-05 | 新增 UAT 通过后强制触发逻辑；强制输出结构化 `code-review-report.md`；新增 UAT 交叉验证章节；与 `release-management` 正式衔接；meta.json 升级至 1.1.0。 |
