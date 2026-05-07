---
name: progress-tracker
description: 贯穿软件全生命周期的进度治理中枢。维护单一可信进度源（SSOT），自动计算双轨制进度（前期阶段粗粒度 + 后期任务精粒度），驱动阶段流转并拦截进度异常（跳过阶段、无规格编码、未自测算完成等）。
---

# Progress Tracker

## 角色
项目进度治理中枢。维护单一可信进度源（SSOT），驱动阶段流转，拦截进度异常。

## 适用场景
- **项目初始化**：首次使用时创建进度追踪系统与配置模板
- **阶段完成更新**：用户宣告某阶段完成时，校验门控并更新进度
- **任务级更新**：开发任务自测通过后精确更新进度
- **主动查看进度**：随时查看总体进度、阶段进度、任务列表及风险
- **风险登记**：记录和跟踪项目风险与阻碍

## 依赖与前置条件

### 必依赖项
- **目录结构**：项目已按 OpenSpec 规范建立 `openspec/changes/{变更名}/` 目录（可通过 `opsx:propose` 或手动创建）
- **外部 Skill**：
  - `task-breakdown`：生成初始 `tasks.md`
  - `executing-plans`：提供任务完成信号
  - `self-check`：提供产出物完整性校验结果
  - `finish`：变更完成时触发归档联动
- **数据文件**：
  - `openspec/config.yaml`：阶段定义、门控规则、产出物规格
  - `openspec/changes/{变更名}/progress.md`：当前进度 SSOT
  - `openspec/changes/{变更名}/tasks.md`：任务清单（Checkbox + verified_by）
  - `openspec/changes/{变更名}/specs/`：各阶段产出物目录

### 可选推断源（用于自动填充上下文）
- `package.json` / `pyproject.toml` / `Cargo.toml` / `go.mod` / `pom.xml` → 推断技术栈
- `Dockerfile` / `docker-compose.yml` / `prisma/schema.prisma` → 推断数据库与中间件
- `src/` / `apps/` / `services/` 等源码目录结构 → 推断核心模块
- Git 贡献者日志 → 推断团队规模（可选）

## 输出产物
- `openspec/changes/{变更名}/progress.md`（自动保存，SSOT）
- 阶段切换许可 / 阻断原因
- Mermaid 甘特图（可视化）
- 风险登记表（追加到 progress.md）

## 阶段定义（10 阶段）

| 序号 | 阶段 ID | 阶段名称 | 权重 | 进度粒度 | 前置依赖 |
|------|---------|----------|------|----------|----------|
| 1 | high-level-requirements | 概要需求 | 10% | 粗粒度 | — |
| 2 | detailed-requirements | 详细需求 | 15% | 粗粒度 | 阶段 1 基线冻结 |
| 3 | high-level-design | 概要设计 | 15% | 粗粒度 | 阶段 1 基线冻结 |
| 4 | detailed-design | 详细设计 | 15% | 粗粒度 | 阶段 3 完成 + 对应模块详细需求评审通过 |
| 5 | interface-first-dev | 接口驱动开发 | 10% | 粗粒度 | 阶段 3~4 完成 |
| 6 | task-breakdown | 任务拆解 | 5% | 粗粒度 | 阶段 5 完成 |
| 7 | implementation | 编码实现 | 15% | 任务级精粒度 | 阶段 5~6 完成 |
| 8 | unit-test | 单元测试 | 10% | 任务级精粒度 | 阶段 7 对应任务完成 |
| 9 | integration-test | 集成测试 | 5% | 任务级精粒度 | 阶段 8 覆盖率门控通过 |
| 10 | finish | 收尾归档 | 0% | 粗粒度 | 阶段 9 完成 |

### 阶段并行规则

> **粗粒度并行原则**：前期阶段（1-4）不要求严格串行。概要需求（阶段 1）冻结后，详细需求（阶段 2）和概要设计（阶段 3）可**同时启动**；详细设计（阶段 4）可在对应模块的详细需求评审通过后即启动，无需等待全部 PRD-001~00N 完成。
>
> **编码门禁原则**：阶段 7（编码实现）必须等待阶段 5（接口驱动开发）和阶段 6（任务拆解）完成，不可提前启动（RF-02：禁止无规格编码）。

## 双轨制进度计算规则

**前期阶段（1-6：需求 + 设计）**：
- 按阶段权重加权平均计算
- 已完成阶段按 100% 计入
- 进行中阶段按当前完成比例 × 权重计入
- 公式：`overall = Σ(已完成阶段权重) + 进行中阶段权重 × 当前进度比例`

**后期阶段（7-10：开发 + 测试 + 交付）**：
- 切换到任务级精确计算
- 仅统计 `verified_by` 标记为 `self-check-passed`、`user-confirmed` 或 `auto-passed` 的任务
- 公式：`completion_rate = 已完成且验证通过的任务数 / 总任务数 × 100%`
- 开发阶段进度 = `impl_weight × completion_rate`

## Red Flag 规则（进度异常拦截）

1. **禁止跳过前置依赖阶段**：某阶段的**前置依赖阶段**未标记"已完成"时，不允许该阶段进入"进行中"。例如：阶段 3（概要设计）的前置是阶段 1（概要需求），而非阶段 2（详细需求），因此阶段 1 完成后即可启动阶段 3，无需等待阶段 2。
2. **禁止无规格编码**：若 `specs/` 目录为空，开发阶段进度强制为 0%
3. **禁止未自测算完成**：`tasks.md` 中勾选但未通过自测的任务，视为"进行中"
4. **禁止未经评审的需求变更**：概要需求变更若未走评审流程，进度回滚至阶段 1
5. **禁止无测试宣告完成**：未通过单元测试覆盖率门控（≥70%）不得进入集成测试阶段

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
4. **生成 SSOT**：生成初始 `progress.md`（所有阶段为"未开始"）
5. **确认输出**：向用户展示推断出的项目上下文（项目名、技术栈、核心模块），请用户确认或修正

> **最小输入原则**：若项目根目录已有明确的构建文件或源码结构，用户无需手动填写技术栈和团队信息。Skill 会自动推断并列出，用户仅需确认或微调。

### 2. 阶段完成更新
```text
【阶段 N 完成 | Skill：progress-tracker】

阶段 N 已完成，请更新进度。
```
Skill 自动执行：
- 读取 `config.yaml` 中当前阶段的 `gate_to_next` 规则
- 校验产出物完整性（`specs/` 目录是否包含 `required_sections`）
- 检查是否有 `user_review` 签字记录
- 若通过：标记阶段为 ✅已完成，计算 `overall_progress`，重写 `progress.md`
- **检查可并行启动的下游阶段**：若某下游阶段的前置依赖已全部满足（即使其紧前阶段尚未完成），自动将该下游阶段标记为 🟡 可启动，并提示用户
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

## 与其他 Skill 的协作

| Skill | 协作方式 |
|-------|----------|
| `self-check` | 提供产出物完整性校验结果，作为阶段门控输入 |
| `task-breakdown` | 生成初始 `tasks.md`，progress-tracker 解析并初始化任务摘要 |
| `executing-plans` | 提供任务完成信号，触发任务级进度更新 |
| `finish` | 变更完成后联动归档，将 `progress.md` 复制到 `archive/{变更名}/` |

## 约束

- **唯一写入口**：禁止人工直接修改 `progress.md` 的 YAML frontmatter，所有更新必须通过本 Skill
- **自测门控**：`tasks.md` 中 `verified_by` 不为 `self-check-passed` 的任务，不计入 completed 统计
- **阻断优先**：任何 Red Flag 中的 blocker 级异常，必须修复后才能更新进度
- **归档联动**：变更完成执行 `opsx:archive` 时，自动将 `progress.md` 同步归档
- **最小输入原则**：Skill 优先通过扫描项目文件自动推断上下文（技术栈、模块、项目名），仅在推断失败或结果不确定时才向用户询问

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
概要需求阶段已完成，产出物已保存到 specs/ 目录，请更新进度。
```
