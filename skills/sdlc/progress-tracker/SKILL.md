---
name: progress-tracker
description: 贯穿软件全生命周期的进度治理中枢。维护单一可信进度源（SSOT），自动计算双轨制进度（前期阶段粗粒度 + 后期任务精粒度），驱动阶段流转并拦截进度异常（跳过阶段、无规格编码、未自测算完成、人工闸门未签字等）。
---

# Progress Tracker

## 角色
项目进度治理中枢。维护单一可信进度源（SSOT），驱动阶段流转，拦截进度异常，管理人工闸门状态。

## 适用场景
- **项目初始化**：首次使用时创建进度追踪系统、配置模板与运维基础设施骨架
- **阶段完成更新**：用户宣告某阶段完成时，校验门控（含人工签字状态）并更新进度
- **任务级更新**：开发任务自测通过后精确更新进度
- **主动查看进度**：随时查看总体进度、阶段进度、任务列表、人工闸门状态及风险
- **风险登记**：记录和跟踪项目风险与阻碍
- **人工闸门状态查询**：查看 Gate 1/2.5/2/3 的签字状态

## 依赖与前置条件

### 必依赖项
- **目录结构**：项目已按 OpenSpec 规范建立 `openspec/changes/{变更名}/` 目录（可通过 `opsx:propose` 或手动创建）
- **外部 Skill**：
  - `task-breakdown`：生成初始 `tasks.md`
  - `executing-plans`：提供任务完成信号
  - `self-check`：提供产出物完整性校验结果
  - `finish`：变更完成时触发归档联动
  - `human`：提供人工闸门签字状态（V2.1 新增）
- **数据文件**：
  - `openspec/config.yaml`：阶段定义、门控规则、产出物规格
  - `openspec/changes/{变更名}/progress.md`：当前进度 SSOT
  - `openspec/changes/{变更名}/tasks.md`：任务清单（Checkbox + verified_by）
  - `openspec/changes/{变更名}/high-level-requirements/`、`detailed-requirements/`、`high-level-design/`、`detailed-design/`：各阶段产出物目录
  - `openspec/changes/{变更名}/human-decisions.md`：人工决策审计日志（V2.1 新增）

### 可选推断源（用于自动填充上下文）
- `package.json` / `pyproject.toml` / `Cargo.toml` / `go.mod` / `pom.xml` → 推断技术栈
- `Dockerfile` / `docker-compose.yml` / `prisma/schema.prisma` → 推断数据库与中间件
- `src/` / `apps/` / `services/` 等源码目录结构 → 推断核心模块
- Git 贡献者日志 → 推断团队规模（可选）

## 输出产物
- `openspec/changes/{变更名}/progress.md`（自动保存，SSOT）
- `ops/staging-config.yaml`（V2.1 新增，初始化时生成）
- `ops/rollback-plan.md`（V2.1 新增，初始化时生成模板）
- `ops/monitoring-rules.yaml`（V2.1 新增，初始化时生成骨架）
- 阶段切换许可 / 阻断原因
- Mermaid 甘特图（可视化）
- 风险登记表（追加到 progress.md）

## 阶段定义（12 阶段，V2.1 扩展）

> **SDLC 映射**：本表序号 1-12 对应完整项目交付链路。阶段 1（需求探索）和阶段 1.5（市场定位）由 `brainstorming` 和 `competitive-analysis` 完成，不纳入进度追踪。

| 序号 | SDLC 阶段 | 阶段 ID | 阶段名称 | 权重 | 进度粒度 | 前置依赖 | 人工闸门 |
|------|-----------|---------|----------|------|----------|----------|----------|
| 1 | 2 | high-level-requirements | 概要需求 | 8% | 粗粒度 | — | 🚪 Gate 1 |
| 2 | 2.5 | detailed-requirements | 详细需求 | 12% | 粗粒度 | 序号 1 基线冻结 | 🚪 Gate 2.5 |
| 3 | 3 | high-level-design | 概要设计 | 12% | 粗粒度 | 序号 1 基线冻结 | 🚪 Gate 2 |
| 4 | 4 | detailed-design | 详细设计 | 12% | 粗粒度 | 序号 3 完成 + 对应模块详细需求评审通过 | — |
| 5 | 5 | interface-first-dev | 接口驱动开发 | 8% | 粗粒度 | 序号 3~4 完成 | — |
| 6 | 6 | task-breakdown | 任务拆解 | 4% | 粗粒度 | 序号 5 完成 | — |
| 7 | 7 | implementation | 编码实现 | 12% | 任务级精粒度 | 序号 5~6 完成 | — |
| 8 | 8 | unit-test | 单元测试 | 8% | 任务级精粒度 | 序号 7 对应任务完成 | — |
| 9 | 9 | integration-test | 集成测试 | 4% | 任务级精粒度 | 序号 8 覆盖率门控通过 | — |
| 9.25 | 9.25 | code-review | 代码审查 | 0% | 粗粒度 | 序号 9 P0 用例通过 | — |
| 9.5 | 9.5 | uat-verification | UAT 验证 | 4% | 粗粒度 | 序号 9.25 代码审查通过 | 🚪 Gate 3 |
| 10 | 10 | release-management | 上线发布 | 4% | 粗粒度 | 序号 9.5 Gate 3 通过 + 序号 9.25 代码审查通过 | 人工最终决策 |
| 11 | 11 | finish | 收尾归档 | 0% | 粗粒度 | 序号 10 完成 | — |
| 12 | 12 | monitoring-analysis | 线上监控（周期性） | 0% | 粗粒度 | 序号 11 完成 | — |

### 阶段并行规则

> **粗粒度并行原则**：前期阶段（序号 1-4）在人工闸门约束下可部分并行。
> - 概要需求（序号 1）冻结且 🚪 **Gate 1 签字**后，详细需求（序号 2）与概要设计（序号 3）可**同时启动**
> - 概要设计（序号 3）完成且 🚪 **Gate 2 签字**、详细需求（序号 2）完成且 🚪 **Gate 2.5 签字**后，方可启动详细设计（序号 4）
> - 详细设计（序号 4）可在对应模块的详细需求评审通过后即启动，无需等待全部 PRD-001~00N 完成
>
> **编码门禁原则**：序号 7（编码实现）必须等待序号 5（接口驱动开发）和序号 6（任务拆解）完成，不可提前启动（RF-02：禁止无规格编码）。
>
> **交付后链路（V2.1 新增）**：序号 9.5（UAT）必须在预览环境由人工走通业务流程；序号 10（发布）必须人工最终确认；序号 12（监控）周期性执行，不占用项目总进度权重。
>
> **代码审查门禁（V2.2 新增）**：序号 9.25（代码审查）为强制性技术门禁，不占用进度权重，但阻塞性问题未清零时禁止进入 UAT 和发布阶段。代码审查由 `code-review-pipeline` 驱动，状态写入 `progress.md` 的 `code_review` 字段。

## 双轨制进度计算规则

**前期阶段（1-6：需求 + 设计）**：
- 按阶段权重加权平均计算
- 已完成阶段按 100% 计入
- 进行中阶段按当前完成比例 × 权重计入
- 公式：`overall = Σ(已完成阶段权重) + 进行中阶段权重 × 当前进度比例`

**后期阶段（7-11：开发 + 测试 + 交付）**：
- 切换到任务级精确计算
- 仅统计 `verified_by` 标记为 `self-check-passed`、`user-confirmed` 或 `auto-passed` 的任务
- 公式：`completion_rate = 已完成且验证通过的任务数 / 总任务数 × 100%`
- 开发阶段进度 = `impl_weight × completion_rate`

**总进度上限规则（V2.1 新增）**：
- 若存在未通过的 🚪 Gate，总进度不得超过该 Gate 所在阶段的权重上限
- 例如：Gate 2（概要设计）未签字，总进度上限 = 序号 1~2 权重之和 = 20%

## Red Flag 规则（进度异常拦截）

1. **禁止跳过前置依赖阶段**：某阶段的**前置依赖阶段**未标记"已完成"时，不允许该阶段进入"进行中"。
2. **禁止无规格编码**：若 `high-level-requirements/` 和 `high-level-design/` 目录为空，开发阶段进度强制为 0%
3. **禁止未自测算完成**：`tasks.md` 中勾选但未通过自测的任务，视为"进行中"
4. **禁止未经评审的需求变更**：概要需求变更若未走评审流程，进度回滚至序号 1
5. **禁止无测试宣告完成**：未通过单元测试覆盖率门控（≥70%）不得进入集成测试阶段
6. **🚪 禁止跳过人工闸门（V2.1 新增）**：
   - Gate 1 未签字（`human_status.gate1 != passed`）：禁止进入详细需求阶段
   - Gate 2.5 未签字（`human_status.gate2_5 != passed`）：禁止进入**详细设计**阶段
   - Gate 2 未签字（`human_status.gate2 != passed`）：禁止进入详细设计阶段
   - Gate 3 未签字（`human_status.gate3 != passed`）：禁止进入发布阶段
7. **禁止跳过代码审查（V2.2 新增）**：`code_review.status != passed` 或存在未清零的 blocking 问题时，禁止进入 UAT 和发布阶段
8. **禁止 AI 自动发布（V2.1 新增）**：`release-management` 阶段必须人工最终确认，AI 不得自动标记为"已完成"

## 工作流

### 1. 项目初始化
```text
【初始化 | Skill：progress-tracker】

请为当前项目初始化进度追踪系统。
```
Skill 自动执行：
1. **扫描推断**：自动读取项目根目录下的 `package.json`、`pyproject.toml`、`requirements.txt`、`Dockerfile` 等文件，推断技术栈与核心模块
2. **生成配置**：基于推断结果和 `config-template.yaml` 生成 `openspec/config.yaml`
   > ⚠️ **必须严格保留模板的 `artifact/check/action` 格式**，禁止简化为 `required_specs: [high-level-requirements.md]` 等单文件形式。概要需求阶段的门控必须列出全部 5 个文件（01~05）。
3. **创建结构**：创建 `openspec/changes/{变更名}/` 目录结构
4. **创建运维基础设施骨架（V2.1 新增）**：
   - 创建 `ops/` 目录（若不存在）
   - 生成 `ops/staging-config.yaml` 模板（预发布环境配置）
   - 生成 `ops/rollback-plan.md` 模板（回滚方案骨架）
   - 生成 `ops/monitoring-rules.yaml` 骨架（监控规则初稿）
5. **生成 SSOT**：生成初始 `progress.md`（所有阶段为"未开始"，含 `human_status` 字段）
6. **确认输出**：向用户展示推断出的项目上下文（项目名、技术栈、核心模块、ops 目录结构），请用户确认或修正

> **最小输入原则**：若项目根目录已有明确的构建文件或源码结构，用户无需手动填写技术栈和团队信息。Skill 会自动推断并列出，用户仅需确认或微调。

### 2. 阶段完成更新
```text
【阶段 N 完成 | Skill：progress-tracker】

阶段 N 已完成，请更新进度。
```
Skill 自动执行：
- 读取 `config.yaml` 中当前阶段的 `gate_to_next` 规则
- 校验产出物完整性（`high-level-requirements/` 和 `high-level-design/` 目录是否包含 `required_sections`）
- **检查人工闸门状态（V2.1 新增）**：读取 `human-decisions.md`，确认当前阶段对应 Gate 为 `passed`
  - Gate 1 → 阶段 1（概要需求）
  - Gate 2.5 → 阶段 2.5（详细需求）
  - Gate 2 → 阶段 3（概要设计）
  - Gate 3 → 阶段 9.5（UAT）
- 若通过：标记阶段为 ✅已完成，计算 `overall_progress`，重写 `progress.md`
- **检查可启动的下游阶段**：若某下游阶段的前置依赖（含对应人工闸门签字）已全部满足，自动将该下游阶段标记为 🟡 可启动，并提示用户
- 若未通过：返回阻断原因清单，要求修复

### 3. 任务级更新（由其他 Skill 调用）
```text
【任务更新 | Skill：progress-tracker】

任务 T-XXX 已完成，自测通过（verified_by: self-check-passed）。
```
Skill 自动执行：
- 更新 `tasks.md` 中对应任务为 `- [x]` 并追加 `verified_by`
- 重新计算 `implementation` 阶段完成率
- 更新 `progress.md` 中的 `tasks_summary`
- 若所有任务完成且验证通过，自动标记 `implementation` 为 ✅已完成

### 4. 查看进度
```text
【查看进度 | Skill：progress-tracker】

请展示当前总体进度、阶段进度、任务列表及风险阻碍。
```
Skill 自动执行：
- 读取当前 `progress.md`
- 展示总体进度看板（含 Mermaid 甘特图）
- 列出当前任务列表（P0 优先）
- 展示 🚪 人工闸门状态（已通过 / 待确认 / 未启动）
- 展示风险与阻碍清单

### 5. 风险登记
```text
【风险登记 | Skill：progress-tracker】

新增风险：{描述}，影响{级别}，应对方案：{方案}
```
Skill 自动执行：
- 生成风险 ID（R-XXX）
- 追加到 `progress.md` YAML frontmatter 的 `risks` 数组
- 更新 Markdown body 的风险表格

## progress.md 结构（V2.1 更新）

```yaml
---
project: {项目名}
change: {变更名}
overall_progress: 0%
phases:
  high-level-requirements: {status: not_started, weight: 8%}
  detailed-requirements: {status: not_started, weight: 12%}
  high-level-design: {status: not_started, weight: 12%}
  detailed-design: {status: not_started, weight: 12%}
  interface-first-dev: {status: not_started, weight: 8%}
  task-breakdown: {status: not_started, weight: 4%}
  implementation: {status: not_started, weight: 12%}
  unit-test: {status: not_started, weight: 8%}
  integration-test: {status: not_started, weight: 4%}
  code-review: {status: not_started, weight: 0%}
  uat-verification: {status: not_started, weight: 4%}
  release-management: {status: not_started, weight: 4%}
  finish: {status: not_started, weight: 0%}
  monitoring-analysis: {status: not_started, weight: 0%}
human_status:                          # V2.1 新增
  gate1: {status: not_started, signed_by: null, signed_at: null}
  gate2_5: {status: not_started, signed_by: null, signed_at: null}
  gate2: {status: not_started, signed_by: null, signed_at: null}
  gate3: {status: not_started, signed_by: null, signed_at: null}
tasks_summary: {total: 0, completed: 0, verified: 0}
risks: []
last_updated: {ISO8601}
---
```

## 与其他 Skill 的协作

| Skill | 协作方式 |
|-------|----------|
| `self-check` | 提供产出物完整性校验结果，作为阶段门控输入 |
| `task-breakdown` | 生成初始 `tasks.md`，progress-tracker 解析并初始化任务摘要 |
| `executing-plans` | 提供任务完成信号，触发任务级进度更新 |
| `finish` | 变更完成后联动归档，将 `progress.md` 复制到 `archive/{变更名}/` |
| `human`（V2.1 新增） | 读取签字状态，作为阶段流转硬性门控 |
| `monitoring-setup`（V2.1 新增） | 初始化时生成 ops/ 骨架，运行时更新监控状态 |

## 约束

- **唯一写入口**：禁止人工直接修改 `progress.md` 的 YAML frontmatter，所有更新必须通过本 Skill
- **自测门控**：`tasks.md` 中 `verified_by` 不为 `self-check-passed` 的任务，不计入 completed 统计
- **阻断优先**：任何 Red Flag 中的 blocker 级异常，必须修复后才能更新进度
- **归档联动**：变更完成执行 `opsx:archive` 时，自动将 `progress.md` 同步归档
- **最小输入原则**：Skill 优先通过扫描项目文件自动推断上下文（技术栈、模块、项目名），仅在推断失败或结果不确定时才向用户询问
- **人工闸门状态同步（V2.1 新增）**：`human_status` 字段只能由 `human` Skill 更新，progress-tracker 只读取不写入

## 使用示例

**查看当前进度：**
```text
【查看进度 | Skill：progress-tracker】
请展示当前进度。
```

**登记风险：**
```text
【风险登记 | Skill：progress-tracker】
新增风险：数据库 Schema 可能随需求变动，影响接口契约。
影响级别：高。应对方案：在接口驱动阶段增加 mock 验证。
```

**阶段完成：**
```text
【阶段 1 完成 | Skill：progress-tracker】
概要需求阶段已完成，产出物已保存到 high-level-requirements/ 目录，请更新进度。
```

## Gotchas

- **禁止人工直接修改 progress.md**：所有进度更新必须通过本 Skill 执行，人工修改会导致 SSOT 失效和进度计算错误
- **人工闸门状态只读**：`human_status` 字段只能由 `human` Skill 更新，progress-tracker 只读取不写入。若发现 `human_status` 与阶段状态不一致，标记为 WARNING 并提示用户同步
- **ops/ 目录初始化不覆盖已有文件**：若项目已存在 `ops/rollback-plan.md`，初始化时只生成模板骨架，不覆盖已有内容
- **双轨制进度不可混用**：前期阶段（1-6）用权重计算，后期阶段（7-11）用任务完成率计算，禁止在编码阶段使用权重估算进度
- **UAT 和监控阶段权重为 0%**：这两个阶段不贡献项目总进度百分比，但仍是阶段流转的必要环节
- **总进度上限规则必须严格执行**：未通过的 Gate 会锁定总进度上限，防止"进度虚高"误导决策
- **并行阶段标记需谨慎**：自动标记下游阶段为"可启动"时，必须确认其所有前置依赖（含人工闸门）均已满足
