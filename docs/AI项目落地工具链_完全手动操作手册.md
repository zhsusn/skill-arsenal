# AI项目落地工具链 —— 完全手动操作手册

> 本文档为 `docs/AI项目落地工具链使用手册.md` 的配套文档。
>
> 当 MCP Server 不可用（网络不通、服务未部署或权限不足）时，按本手册逐条执行命令，完成从需求到发布的全生命周期操作。
>
> 版本 V2.4 | 2026年5月
>
> **V2.4 更新**：补齐 `uat-verification`（阶段 9.5）、`release-management`（阶段 10.5）、`monitoring-analysis`（阶段 12）三个 Skill。修复 `integration-test` 下游衔接（改为 `uat-verification`）。
>
> **V2.3 更新**：`detailed-design` Skill 正式可用，内置三级质量门控与 Cross-Module Audit，支持增量更新。`self-check` 新增阶段 4 详细设计文档质量检查（7 项维度）。
>
> **适用场景**：
> - 前期环境搭建阶段，MCP Server 尚未部署
> - 网络受限环境（内网、离线场景）
> - 权限不足，无法启动外部服务
> - 偏好纯命令行手动控制的团队

---

## 目录

- [一、手动方式说明](#一手动方式说明)
- [二、完整命令执行流程速查](#二完整命令执行流程速查)
- [三、各阶段详细命令列表](#三各阶段详细命令列表)
- [四、常见问题与排除](#四常见问题与排除)

---

## 一、手动方式说明

当 MCP Server 不可用时（网络不通、服务未部署或权限不足），可以通过手动方式按顺序执行命令。手动方式的核心原则是：

- 每个命令按固定顺序执行，不能跳过或并行
- 每个命令的输出作为下一个命令的输入
- **每个 Gate 完成后需要人工确认签字后才能进入下一阶段**
- 自查环节必不可少，确保产出物质量

**与工具集成方式的关系：**
两种方式的产出物格式和目录结构完全一致，可以在任何时候切换。工具集成方式下如果 MCP Server 不可用，系统会提示切换到手动方式。

---

## 二、完整命令执行流程速查

| 步骤   | 命令                     | 说明         | 产出物                                            | 人工闸门        |
| ---- | ---------------------- | ---------- | ---------------------------------------------- | ----------- |
| 0    | progress-tracker       | 初始化目录结构    | config.yaml + ops/                             | —           |
| 1    | /opsx:propose          | 创建变更提案     | proposal.md                                    | —           |
| 1    | brainstorming          | 需求探索       | 探索记录                                           | —           |
| 1.5  | competitive-analysis   | 市场定位分析（可选） | market-positioning.md                          | —           |
| 2    | prd-generation         | 生成概要需求     | 01-05.md                                       | 🚪 Gate 1   |
| 2.5  | detailed-requirements  | 生成详细需求     | feature-*/                                     | 🚪 Gate 2.5 |
| 3 前置 | competitive-analysis   | 技术竞品分析     | competitive-analysis.md + design-input.md      | —           |
| 3    | high-level-design      | 概要设计       | design/*.md + rollback-plan.md                 | 🚪 Gate 2   |
| 3.5  | monitoring-setup       | 监控初始化（一次性） | monitoring-rules.yaml                          | —           |
| 4    | detailed-design        | 详细设计       | feature-*/design.md                            | —           |
| 5    | interface-first-dev    | 接口驱动       | openapi.yaml                                   | —           |
| 5.5  | writing-plans          | 编写实现计划     | plan.md                                        | —           |
| 6    | task-breakdown         | 任务拆解       | tasks.md                                       | —           |
| 7    | executing-plans        | 编码实现       | 代码文件                                           | —           |
| 8    | unit-test              | 单元测试       | tests/unit/                                    | —           |
| 9    | integration-test       | 集成测试       | tests/integration/ + user-stories-checklist.md | —           |
| 9.5  | uat-verification       | UAT 验证     | uat-report.md                                  | 🚪 Gate 3   |
| 10   | requesting-code-review | 代码审查       | code-review-report.md（含 design.md 对比、tasks.md 追溯） | —           |
| 10.5 | release-management     | 上线发布       | release-notes.md                               | 人工最终决策      |
| 11   | finish                 | 归档收尾       | archive/ + CHANGELOG.md + 归档完成确认单       | —           |
| 12   | monitoring-analysis    | 线上监控（周期性）  | monitoring-dashboard.md                        | —           |

---

## 三、各阶段详细命令列表

### 步骤 0：初始化变更目录

```bash
# 1. 创建目录结构
mkdir -p openspec/{specs,changes,archive}
mkdir -p openspec/changes/{变更名}/{specs,design,uat,sign-off}
mkdir -p .kimi/skills/
mkdir -p docs/ai-output
mkdir -p tests/{unit,integration}
mkdir -p ops/

# 2. 创建配置文件 openspec/config.yaml
cat > openspec/config.yaml << 'EOF'
schema: {项目名}-sdd
version: "1.0"
context: |
  项目：{项目名称}
  技术栈：{前端框架} + {后端框架} + {数据库}
  规范：所有变更必须通过概要评审和详细评审
EOF

# 3. 创建运维基础设施骨架
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

---

### 步骤 1：创建变更提案

```bash
/opsx:propose "{变更描述}"
```

说明：创建 `openspec/changes/{变更名}/proposal.md`。

---

### 步骤 1：需求探索

```bash
/skill:brainstorming 帮我脑暴一下，打算做个{产品描述}，
本地资料：@docs/ref/*.md

/skill:progress-tracker 请更新进度
```

---

### 步骤 2：生成概要需求 + 🚪 Gate 1

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

---

### 步骤 2.5：生成详细需求 + 🚪 Gate 2.5

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

---

### 步骤 3 前置：技术竞品分析

```bash
/skill:competitive-analysis mode=technical 请自动搜索相关竞品，执行技术深度对比分析。

分析维度：角色数据模型设计、核心功能流程、技术选型、集成方式
参考文档：@openspec/changes/{变更名}/specs/

/skill:progress-tracker 请更新进度
```

---

### 步骤 3：概要设计 + 🚪 Gate 2

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

---

### 步骤 4：详细设计（V2.3 增强）

**前置检查：**
```bash
# 确认 Gate 2 和 Gate 2.5 已签字
/skill:human action=status
```

**执行命令：**
```bash
/skill:detailed-design 按模块输出详细设计。
参考：@openspec/changes/{变更名}/design/
@openspec/changes/{变更名}/specs/feature-*/
```

**生成中自动执行的三级门控：**
- Cross-Module Design Audit（模块间矛盾检测：字段类型、接口兼容性、状态枚举冲突）
- 规格充分性审查（SPECIFIED/VAGUE/MISSING 判定，模糊语言零容忍）
- 设计质量自评（阻塞维度评分：完备性/清晰度/准确性 < 3 分暂停）

**执行 self-check（阶段 4，7 项检查）：**
```bash
/skill:self-check 详细设计
```

**产出（每个模块 5 文件）：**
| 文件 | 内容 |
|------|------|
| `design.md` | 模块内部架构、组件设计、类/函数签名、算法逻辑 |
| `api-spec.md` | 接口定义、OpenAPI 3.1 YAML 片段、错误码、权限 |
| `db-schema.md` | DDL、索引策略、缓存 Key 设计、连接池配置 |
| `state-machine.md` | Mermaid 状态图、转换条件、异常分支、全局映射 |
| `test-plan.md` | 单测用例（Given/When/Then）、集成场景、边界覆盖 |

**关键红线：**
- 技术栈必须与概要设计一致（禁止擅自变更数据库类型）
- URI 必须资源导向（禁止 `/getOrder` 等动词 URI）
- 模糊语言零容忍（"TBD"/"standard approach" → VAGUE）
- 状态机必须与全局状态机兼容

---

### 步骤 5：接口驱动开发

```bash
/skill:interface-first-dev 基于详细设计定义前后端接口契约。
参考：@openspec/changes/{变更名}/detail-design/feature-*/api-spec.md
@openspec/changes/{变更名}/detail-design/feature-*/db-schema.md

/skill:self-check 接口契约
```

---

### 步骤 5.5：编写实现计划

```bash
/skill:writing-plans 基于详细设计和接口契约，生成模块级实现计划。
参考：@openspec/changes/{变更名}/detail-design/feature-*/design.md
@openspec/changes/{变更名}/interface-contracts/openapi.yaml

/skill:self-check 实现计划
```

产出：`openspec/changes/{变更名}/plan.md`。

---

### 步骤 6：任务拆解

```bash
/skill:task-breakdown 基于 plan.md 和接口契约，生成开发任务清单。
参考：@openspec/changes/{变更名}/plan.md
@openspec/changes/{变更名}/interface-contracts/openapi.yaml
```

产出：`openspec/changes/{变更名}/tasks.md`。

---

### 步骤 7：编码实现

```bash
# 按 Batch（默认 3 任务/批次）执行：
/skill:executing-plans 按 tasks.md 逐 Batch 执行开发任务。
参考：@openspec/changes/{变更名}/tasks.md
@openspec/changes/{变更名}/detail-design/feature-*/design.md
@openspec/changes/{变更名}/interface-contracts/openapi.yaml

# 每个 Batch 完成后执行 Inline Audit
# 每个任务完成后：
/skill:self-check 编码任务
```

**执行纪律：**
- **Simplicity First**：先写最简单可行方案
- **Scope Discipline**：严禁顺手重构
- **Rollback-Friendly**：优先新增文件，禁止同一 commit 既删又替
- **Gate Non-Collapse**：自测、接口校验、单测必须独立执行

---

### 步骤 8：单元测试

```bash
/skill:unit-test 为已完成的模块生成单元测试。
参考：@openspec/changes/{变更名}/detail-design/feature-*/test-plan.md

pytest tests/unit/ -v --cov={模块路径} --cov-report=term-missing

/skill:self-check 单元测试
```

---

### 步骤 9：集成测试

```bash
/skill:integration-test 生成集成测试。
参考：@openspec/changes/{变更名}/specs/feature-*/spec.md
@openspec/changes/{变更名}/interface-contracts/openapi.yaml

/skill:self-check 集成测试
```

产出：`tests/integration/` + `user-stories-checklist.md`。

---

### 步骤 9.5：UAT 验证 + 🚪 Gate 3

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

---

### 步骤 10：代码审查

```bash
/skill:requesting-code-review 对已完成的代码进行审查。
参考：@openspec/changes/{变更名}/tasks.md
      @openspec/changes/{变更名}/detail-design/feature-*/design.md
      @openspec/changes/{变更名}/uat-report.md
```

产出：`code-review-report.md`（含总体结论、阻塞性问题、设计偏差分析、任务追溯矩阵、UAT 交叉验证）。

**若结论为不通过：**
```bash
# 生成 rework-tasks.md，返回 executing-plans 修复
/skill:executing-plans 修复代码审查发现的阻塞性问题
# 修复完成后重新触发 requesting-code-review
```

---

### 步骤 10.5：上线发布

```bash
/skill:release-management 准备发布。
输入：
  - uat-report.md（通过）
  - code-review-report.md（通过/有条件通过）
  - rollback-plan.md（来自阶段 3）
  - 代码分支/commit SHA
```

**人工操作（阻塞，最终决策）：**
- 确认发布窗口
- 检查回滚方案
- 人工执行最终发布命令（AI 不自动执行生产发布）

产出：`release-notes.md` + `release-checklist.md`。

---

### 步骤 11：归档收尾

```bash
# 必须等待人工确认上线成功后方可执行
/skill:finish
```

**Step 0 人工确认（严禁自动执行）：**
```text
请输入 "确认归档" 继续归档收尾流程。
```

**归档流水线（8 步）：**
1. 合并开发分支到主分支 → 生成合并报告
2. 清理临时文件（`.kimi/temp-*`）
3. OpenSpec 归档：复制全部产物到 `openspec/changes/archive/{变更名}/`
4. 增量规格合并（`/opsx:sync`）：追加到主规格，保留历史谱系
5. 纳入交付后文档：uat-report.md + release-notes.md + human-decisions.md + code-review-report.md
6. 生成 CHANGELOG.md（遵循 Keep a Changelog）
7. 最终一致性校验（8 项检查清单）
8. 输出归档完成确认单

**强制归档的 7 类文档：**
- specs/、tasks.md、uat-report.md、release-notes.md、human-decisions.md、code-review-report.md、merge-report.md

---

### 步骤 12：线上监控（周期性）

```bash
/skill:monitoring-analysis 生成本周健康报告。
```

产出：`monitoring-dashboard.md` + `feedback-loop.md` → 输入下一变更 `brainstorming`。

---

## 四、常见问题与排除

### Q1：可以跳过某些阶段吗？

A：不建议。每个阶段的产出物都是下一个阶段的输入，跳过会导致产出物质量下降。特殊情况下可以简化某个阶段，但不建议完全跳过。

### Q2：自查失败怎么办？

A：根据自查报告修复问题，修复后重新执行自查。如果是内容不一致问题，需要回到上游阶段修复。

### Q3：多个变更可以并行进行吗？

A：不建议。手动方式下应该一次只处理一个变更，避免上下文混淆。

### Q4：UAT 发现严重问题怎么办？

A：立即驳回。执行 `/skill:human gate=Gate3 action=reject reason="{问题描述}"`，AI 会自动生成 `rework-tasks.md`，修复后重新申请 Gate3 sign-off。

### Q5：如何切换到工具集成方式？

A：两种方式产生的文档格式和目录结构完全一致，可以在任何时候切换。当 MCP Server 可用后，从当前阶段继续使用工具集成方式即可。

### Q6：产出物格式与工具集成方式兼容吗？

A：兼容。两种方式产生的文档格式和目录结构完全一致，可以在任何时候切换。

### Q7：需要多少人工干预？

A：主要在以下节点需要人工确认：概要需求评审签字（Gate 1）、原型逐页确认（Gate 2.5）、架构评审与回滚方案确认（Gate 2）、UAT 业务流程走通（Gate 3）、发布窗口最终决策。其他环节由 AI 自主完成。

### Q8：详细设计可以跳过某些模块吗？

A：不可以。每个 P0/P1 模块必须独立输出 5 个文件。若某模块确实无数据库/无状态机，仍需输出说明文件（如"本模块无持久化存储，db-schema.md N/A"），不可省略。

### Q9：需求变更后需要重新生成所有模块的详细设计吗？

A：不需要。detailed-design 支持增量更新：对比新旧 spec.md / io-table.md 识别受影响模块 → 仅重新生成受影响模块的 5 个文件 → 未受影响模块保持冻结 → 重新执行 Cross-Module Audit。

---

**速查卡**

```text
原则：顺序执行、不跳过、Gate 后人工确认、必自查
流程：0 初始化 → 1 提案/探索 → 2 概要需求(Gate1) → 2.5 详细需求(Gate2.5)
       → 3 概要设计(Gate2) → 4 详细设计 → 5 接口驱动 → 5.5 编写计划
       → 6 任务拆解 → 7 编码实现 → 8 单元测试 → 9 集成测试
       → 9.5 UAT(Gate3) → 10 代码审查 → 10.5 发布 → 11 归档 → 12 监控
```
