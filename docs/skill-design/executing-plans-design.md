# Executing Plans Skill 设计规格书

> 本文档面向 Skill 实现者与维护者，描述 `executing-plans` 的完整技术架构、Batch 执行流水线、质量门控机制及与外部系统的集成协议。
>
> 版本: 2.0.0（从 Superpowers 原生改造）

---

## 1. 功能定位

| 维度 | 说明 |
|------|------|
| **核心职责** | 按 tasks.md 逐个执行编码任务，含执行前审查、强制自测、接口校验、自动勾选与批次检查点 |
| **所处阶段** | 开发阶段（任务拆解完成后 → 测试前） |
| **上游输入** | task-breakdown（tasks.md）、detailed-design、interface-first-dev |
| **下游输出** | finish、requesting-code-review |
| **设计模式** | `pipeline`（多步骤流水线） |
| **开源对标** | Superpowers `executing-plans`（Batch 执行、Critical Review、Blocker 停止）、agent-skills `incremental-implementation`（Simplicity First、Scope Discipline、Rollback-Friendly）、spellbook `develop` Phase 4（Gate Non-Collapse Rule、Inline Audit） |

---

## 2. 总体架构

```
┌─────────────────────────────────────────────────────────────┐
│                  executing-plans Skill                       │
├─────────────────────────────────────────────────────────────┤
│  触发方式：tasks.md 生成后 / 用户指令"开始实现"               │
│  执行模式：Batch 执行（默认 3 任务/批次），持久化代码文件     │
│  架构模式：主控 Agent 执行 Batch 流水线                       │
│  核心约束：Gate Non-Collapse、Simplicity First、Rollback-Friendly │
└─────────────────────────────────────────────────────────────┘
```

### 2.1 改造前后对比

| 维度 | Superpowers 原生 | 本方案改造后 |
|------|------------------|-------------|
| 执行前审查 | Critical Review（计划审查） | 增加 **接口一致性预检**（代码 vs api-spec） |
| 执行中门控 | 无（直接执行） | 增加 **强制自测**（self-check Skill 集成） |
| 执行后动作 | 标记完成 | 增加 **自动运行单测**、**自动勾选 tasks.md**、**接口一致性校验** |
| 执行纪律 | Follow plan exactly | 增加 **Simplicity First**、**Scope Discipline**、**Rollback-Friendly** |
| 批次策略 | 3 任务/批次 | 可配置（默认 3），批次间强制 Inline Audit |
| 质量门控 | 无 | 增加 **Inline Audit**（spellbook Phase 4.4） |

---

## 3. 处理逻辑

### 3.1 主控流程

```
Step 1: 加载 tasks.md + 设计文档 + 接口契约
    ↓
Step 2: Critical Review（审查任务/设计/接口一致性）
    ├── 发现问题 → 暂停并反馈用户
    └── 通过 → Step 3
    ↓
Step 3: 按 Batch 组织任务（默认 3 个/批次）
    ↓
Step 4: Batch N: 逐个执行 3 个任务
    ↓
Step 5: 任务编码实现（Simplicity First + Scope Discipline）
    ↓
Step 6: 强制自测（self-check Gate）
    ├── 失败 → 修复或暂停
    └── 通过 → Step 7
    ↓
Step 7: 接口一致性校验（代码 vs api-spec）
    ├── 失败 → 修复或暂停
    └── 通过 → Step 8
    ↓
Step 8: 自动运行单测
    ├── 失败 → 修复或暂停
    └── 通过 → Step 9
    ↓
Step 9: 自动勾选 tasks.md（- [ ] → - [x]）
    ↓
Step 10: Commit（Rollback-Friendly）
    ↓
Step 11: Batch 完成？
    ├── 否 → 返回 Step 5 执行下一个任务
    └── 是 → Step 12
    ↓
Step 12: 批次检查点（Inline Audit）
    ├── 不通过 → 返回修复
    └── 通过 → Step 13
    ↓
Step 13: 全部完成？
    ├── 否 → 返回 Step 3 组织下一 Batch
    └── 是 → Step 14
    ↓
Step 14: 交接 finish
```

### 3.2 详细步骤

#### Step 1-2: 加载与 Critical Review

读取：
- `tasks.md` 当前批次任务
- `feature-*/design.md`
- `feature-*/api-spec.md`
- `interface-contracts/openapi.yaml`

审查项：
- 任务描述是否与 design.md / api-spec 一致
- 接口定义是否与 openapi.yaml 冲突
- 前置任务是否已完成（checkbox 已勾选）
- 是否存在未解决的 blocker 或风险

**STOP 条件**：审查发现关键缺口 → 暂停执行，向用户报告问题。

#### Step 3: Batch 组织

- `batch_size` 默认 3
- 同 Phase 内无依赖任务可纳入同一 Batch
- 跨 Phase 任务必须分属不同 Batch

#### Step 5: 编码实现

遵守执行纪律：

**Rule 0: Simplicity First**
- 写代码前问："What is the simplest thing that could work?"
- 写完后检查："Would a staff engineer look at this and say 'why didn't you just...?'"

**Rule 0.5: Scope Discipline**
- 严禁"顺手重构"相邻文件
- 发现但不动：记录为 `NOTICED BUT NOT TOUCHING` 列表
- 禁止添加 spec 外功能

**Rule 1-5**: One Thing at a Time、Keep It Compilable、Feature Flags、Safe Defaults、Rollback-Friendly

#### Step 6: 强制自测（Self-Check Gate）

调用 self-check Skill 检查：
- 代码 vs 设计一致性
- 异常处理完整性
- 边界条件覆盖
- 无硬编码密钥 / Token

**失败处理**：修复或暂停。禁止跳过。

#### Step 7: 接口一致性校验

对比代码与 api-spec.md / openapi.yaml：
- 路径、HTTP 方法一致
- 请求参数、响应结构一致
- 异常码覆盖设计中的异常场景

**不一致 → 标记为 blocker**，停止当前 Batch。

#### Step 8: 自动运行单测

运行 `pytest tests/unit/... -v`：
- 覆盖率 ≥ 70%（可配置）
- 现有测试不得失败（回归保护）

#### Step 9-10: 状态回写与提交

- 修改 `tasks.md`：`- [ ]` → `- [x]`，追加完成时间戳
- 按任务独立提交：`git commit -m "feat({module}): {task_description}"`

#### Step 12: Inline Audit（批次检查点）

审查本批次：
1. 代码质量（可读性、命名、复杂度）
2. 测试覆盖无回归
3. 无相邻文件被意外修改
4. 输出批次摘要

**不通过 → 返回修复**，修复后重新跑 Batch 内所有任务的自测。

#### Step 14: 完成交接

- 输出执行摘要
- 自动调用 finish Skill
- 若配置 requesting-code-review，自动触发代码审查

---

## 4. 输入输出规格

### 4.1 输入

| 输入项 | 类型 | 来源 | 说明 |
|--------|------|------|------|
| 任务清单 | Markdown | `openspec/changes/{变更名}/tasks.md` | 执行蓝图 |
| 设计文档 | Markdown | `feature-*/design.md` | 编码依据 |
| 接口契约 | YAML/Markdown | `api-spec.md`、`openapi.yaml` | 接口校验基准 |
| 配置项 | YAML | `openspec/config.yaml` | `executing_plans.*` |

### 4.2 输出

| 输出项 | 类型 | 路径 | 说明 |
|--------|------|------|------|
| 代码文件 | 源代码 | 项目源码目录 | 各任务对应的实现代码 |
| 单元测试 | 测试代码 | `tests/**` | 随编码同步产出 |
| 自测报告 | Markdown | 对话内联输出 | self-check 结果 |
| 更新后的 tasks.md | Markdown | 原路径 | checkbox 自动勾选 |
| 批次摘要 | Markdown | 对话内联输出 | 每 Batch 执行结果 |
| 接口一致性报告 | Markdown | 对话内联输出 | 代码 vs spec 对比结果 |

---

## 5. 执行纪律详解

### 5.1 Simplicity First（Rule 0）

- 先写最简单可行方案，而非完美方案
- 完成后反向检查：是否有更简单的实现方式被遗漏

### 5.2 Scope Discipline（Rule 0.5）

```markdown
## NOTICED BUT NOT TOUCHING

- `src/services/order_service.py:123` —— 发现重复代码，但不在本任务范围内
- `config/database.yml` —— 发现连接池配置可优化，但不在本任务范围内
```

### 5.3 Rollback-Friendly（Rule 5）

- 优先新增文件（`git add` 即可回滚）
- 修改现有代码尽量最小化
- DB 迁移需配套回滚脚本
- 禁止同一 commit 既删又替

---

## 6. 配置项

```yaml
# openspec/config.yaml
executing_plans:
  batch_size: 3                    # 每批次任务数
  force_self_check: true           # 每个任务后强制自测
  auto_run_unit_test: true         # 编码后自动运行单测
  coverage_threshold: 70           # 单测覆盖率阈值
  auto_tick_tasks: true            # 自动勾选 tasks.md
  interface_validation: true       # 接口一致性校验
  blocker_behavior: "ask_user"     # 遇阻策略: ask_user | pause | rollback
  simplicity_check: true           # 启用 Simplicity First 检查
  scope_discipline: true           # 启用 Scope Discipline
  rollback_friendly: true          # 启用 Rollback-Friendly 提交策略
  inline_audit_per_batch: true     # 每批次后 Inline Audit
  git:
    commit_per_task: true          # 每任务独立提交
    commit_template: "feat({module}): {task_description}"
  auto_save:
    update_tasks_md: true          # 自动更新 tasks.md 状态
    update_progress_tracker: true  # 自动通知 progress-tracker
```

---

## 7. Blocker 处理规范

遇阻不问猜，立即停止并报告用户：

| Blocker 类型 | 示例 | 处理方式 |
|-------------|------|----------|
| 缺失依赖 | 第三方服务未启动、库未安装 | 暂停，向用户报告，等待解决 |
| 测试反复失败 | 运行 3 次仍失败 | 暂停，报告错误日志，等待决策 |
| 指令不清 | tasks.md 描述模糊无法执行 | 暂停，要求澄清 |
| 设计矛盾 | 代码实现与 design.md 冲突 | 暂停，反馈设计问题 |
| 接口不一致 | 代码与 api-spec 不一致且无法决定 | 暂停，标记 blocker |

Blocker 报告格式：
```markdown
## Blocker 报告

- **任务**: {task_id}
- **类型**: {missing_dependency / test_failure / unclear_instruction / design_conflict}
- **现象**: {描述}
- **已尝试**: {尝试过的解决方式}
- **需要决策**: {请用户明确的选项}
```

---

## 8. Gate Non-Collapse Rule

自测、接口校验、单测是三个**独立**门控，**禁止合并**：

| 门控 | 检查内容 | 失败处理 |
|------|----------|----------|
| Self-Check Gate | 代码 vs 设计一致性、异常处理、边界条件 | 修复或暂停 |
| Interface Gate | 代码接口 vs api-spec / openapi.yaml | 修复或暂停 |
| Unit Test Gate | pytest 通过 + 覆盖率 ≥ 70% | 修复或暂停 |

**禁止**："一起检查"、"合并门控"、"自测通过就不用跑接口校验了"。

---

## 9. 与上下游衔接

| 衔接点 | 动作 |
|--------|------|
| 上游: task-breakdown | 消费 tasks.md 作为执行蓝图；解析 checkbox 识别未完成任务 |
| 上游: detailed-design | 读取 feature-*/design.md 作为编码依据 |
| 上游: interface-first-dev | 读取 api-spec.md / openapi.yaml 作为接口校验基准 |
| 横向: self-check | 每个任务后调用 self-check 进行产出物自查 |
| 横向: unit-test | 编码后自动运行单测；unit-test Skill 负责生成补充测试用例 |
| 横向: progress-tracker | 每批次完成后自动更新进度 |
| 下游: requesting-code-review | 全部完成后自动触发代码审查 |
| 下游: finish | 最终交接收尾 Skill |

---

## 10. 开源复用分析

### 10.1 能力映射

| executing-plans 能力 | 可对标的开源 Skill | 复用度 | 差距分析 |
|---------------------|-------------------|--------|----------|
| Batch 执行 | Superpowers `executing-plans` | ✅ 高 | 直接复用 3 任务/批次策略 |
| Critical Review | Superpowers `executing-plans` | ✅ 高 | 直接复用，增加接口一致性预检 |
| Blocker 停止规则 | Superpowers `executing-plans` | ✅ 高 | 直接复用 |
| Simplicity First | agent-skills `incremental-implementation` | ✅ 高 | 直接吸收 Rule 0 |
| Scope Discipline | agent-skills `incremental-implementation` | ✅ 高 | 直接吸收 Rule 0.5 |
| Rollback-Friendly | agent-skills `incremental-implementation` | ✅ 高 | 直接吸收 Rule 5 |
| Gate Non-Collapse | spellbook `develop` Phase 4 | ✅ 高 | 直接复用：TDD / Audit / Review 分四次独立调度 |
| Inline Audit | spellbook `develop` Phase 4.4 | ⚠️ 部分 | 每 Batch 后执行（非每 Task） |

### 10.2 改造要点

| 改造项 | 原因 | 实现方式 |
|--------|------|----------|
| 增加执行纪律 | agent-skills 的 6 条规则可显著减少顺手重构和过度工程 | 在 SKILL.md 中嵌入完整纪律章节 |
| 增加 Gate Non-Collapse | spellbook 证明合并门控会静默丢弃质量维度 | 明确三个门控必须独立执行 |
| 增加自动勾选 tasks.md | tasks.md 是执行进度的唯一可信源 | 每个任务完成后自动修改 checkbox |
| 增加 Inline Audit | 每 Batch 后需要全局质量检查 | Batch 完成后执行代码质量 + 回归检查 |
| 增加接口一致性校验 | 前后端并行开发中接口漂移是常见问题 | 每个任务后对比 api-spec / openapi.yaml |

---

## 11. 风险与规避

| 风险 | 规避方法 |
|------|----------|
| 顺手重构导致范围膨胀 | Scope Discipline 硬性规则 + NOTICED BUT NOT TOUCHING 列表 |
| 门控被跳过 | Gate Non-Collapse Rule：三个门控必须独立执行 |
| Blocker 被强行推进 | 遇阻不问猜：必须暂停并报告用户 |
| 回归未被发现 | 每个任务后运行现有测试 + Batch 后 Inline Audit |
| main 分支被污染 | 严禁在 main/master 上直接执行 |
| 任务复杂度超预期 | 暂停并建议用户重新执行 task-breakdown |

---

## 12. 附录：三 Skill 协作总图

```
detailed-design + interface-first-dev
         ↓
   【writing-plans】→ plan.md（模块级计划）
         ↓
   【task-breakdown】→ tasks.md（≤30分钟/任务，Phase组织）
         ↓
   【executing-plans】→ 代码文件 + 单元测试 + 自测报告
         ↓
   【finish】→ 收尾
```

**协作规则**：
- writing-plans 产出 plan.md 后，必须经用户确认（或 Self-Review 通过）才能进入 task-breakdown
- task-breakdown 产出 tasks.md 后，executing-plans 按 Batch 消费，自动勾选状态回写
- executing-plans 执行中遇 blocker，暂停并通知用户；修复后从当前任务继续
- 三 Skill 共享 `openspec/changes/{变更名}/` 目录，所有产出物自动保存
