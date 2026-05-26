---
name: executing-plans
description: 当用户拥有已编写的 tasks.md 或 plan.md，需要按任务逐个执行编码实现时触发。按 Batch 消费任务清单，含执行前审查、强制自测、接口校验、自动勾选与批次检查点。
---

# Executing Plans

按 tasks.md 逐个执行编码任务，含强制自测、接口校验、自动勾选。上游是 task-breakdown，下游是 finish。

**Announce at start:** "I'm using the executing-plans skill to implement this plan."

## 适用场景

- task-breakdown 生成 tasks.md 后，需要按任务执行编码
- 用户明确要求 "开始实现"、"按 plan 执行"、"执行任务清单"
- 多步骤开发任务需要批量执行与检查点控制

## 执行纪律（改编自 agent-skills/incremental-implementation）

### Rule 0: Simplicity First

写代码前问："What is the simplest thing that could work?"
写完后检查："Would a staff engineer look at this and say 'why didn't you just...?'"

### Rule 0.5: Scope Discipline

- 严禁"顺手重构"相邻文件
- 发现但不动：记录为 `NOTICED BUT NOT TOUCHING` 列表
- 禁止添加 spec 外功能

### Rule 1: One Thing at a Time

每个增量只改一个逻辑事物。禁止一个 commit 混合：新组件 + 重构 + 构建配置更新。

### Rule 2: Keep It Compilable

每个增量后项目必须构建通过，现有测试必须通过。

### Rule 3: Feature Flags for Incomplete

未完成特性默认隐藏，通过环境变量开关。

### Rule 4: Safe Defaults

新代码默认保守行为（如通知默认关闭）。

### Rule 5: Rollback-Friendly

- 优先新增文件（易回滚）
- 修改现有代码尽量最小化
- DB 迁移需配套回滚脚本
- 禁止同一 commit 既删又替

## 处理流程

### Step 1: 加载与审查（Critical Review）

1. 读取 `tasks.md` 当前批次任务 + `feature-*/design.md` + `feature-*/api-spec.md` + `interface-contracts/openapi.yaml`
2. **Critical Review**：检查以下项目，任一发现问题暂停并反馈用户
   - 任务描述是否与 design.md / api-spec 一致
   - 接口定义是否与 openapi.yaml 冲突
   - 任务依赖的前置任务是否已完成（checkbox 已勾选）
   - 是否存在未解决的 blocker 或风险

**STOP 条件**：审查发现关键缺口 → 暂停执行，向用户报告问题，不强行推进。

### Step 2: Batch 组织

按 `batch_size`（默认 3）分组：
- 同 Phase 内无依赖任务可纳入同一 Batch
- 跨 Phase 任务必须分属不同 Batch
- 每个 Batch 执行前输出："开始 Batch N：任务 X.Y, X.Z, X.W"

### Step 3: 编码实现（含 TDD 内循环）

每个任务内部必须调用 test-driven-development Skill 执行 RED-GREEN-REFACTOR：

**R - RED**：基于当前任务验收标准 + api-spec.md，先写失败测试  
**G - GREEN**：写最小实现让测试通过  
**R - REFACTOR**：清理代码，严禁顺手重构  

遵守执行纪律：
- **Simplicity First**：先写最简单可行方案
- **Scope Discipline**：不碰相邻文件，发现的重构点记入 `NOTICED BUT NOT TOUCHING`
- **精确路径**：严格遵循 tasks.md 中指定的文件路径
- **TDD 门控**：每个任务完成后确认 RED 先写、GREEN 最小、REFACTOR 后测试全绿
- **代码风格规范**：生成任何源代码时，必须遵循对应语言的代码风格。Python 遵循 `python-google-style` Skill（Google Python Style Guide）；Java 遵循 `java-alibaba-style` Skill（阿里巴巴Java开发手册）；其他语言使用该语言社区默认风格（TypeScript/ESLint、Go/gofmt、Rust/rustfmt 等）

### Step 4: 强制自测（Self-Check Gate）

每个任务编码完成后调用 self-check Skill：
- 代码 vs 设计一致性
- 异常处理完整性
- 边界条件覆盖
- 无硬编码密钥 / Token

**失败处理**：修复或暂停。禁止跳过自测进入下一步。

### Step 5: 接口一致性校验

将实现的接口与 api-spec.md / openapi.yaml 对比：
- 路径、HTTP 方法一致
- 请求参数、响应结构一致
- 异常码覆盖设计中的异常场景

**不一致 → 标记为 blocker**，停止当前 Batch。

### Step 6: Batch 完成后触发 Unit-Test 门控

当前 Batch 全部任务编码完成后，调用 unit-test Skill 执行模块级验证：

1. 读取 `feature-*/test-plan.md` 与 `logic.md`
2. 补全边界测试（异常状态机、空值/越界、外部服务超时）
3. 统一组织到 `tests/unit/{模块}/` 目录
4. 运行 `pytest tests/unit/ -v --cov={模块} --cov-report=term-missing`
5. **门控**：覆盖率 ≥ 70%？是 → 继续 Step 7；否 → 输出未覆盖清单，返回 Step 3 补 TDD 或补边界测试

**现有测试不得失败**：任何增量导致回归，立即停止当前 Batch

### Step 7: 自动勾选 tasks.md

修改 `tasks.md`：
```markdown
- [x] 2.1 [后端] 实现用户注册 API（含参数校验）
  - 完成时间: {timestamp}
```

自动保存文件。

### Step 8: Commit

按任务独立提交，遵循 Rollback-Friendly：
```bash
git add {files}
git commit -m "feat({module}): {task_description}"
```

### Step 9: 批次检查点（Inline Audit）

每 Batch 完成后执行 Inline Audit：
1. 审查本批次代码质量（可读性、命名、复杂度）
2. 检查测试覆盖无回归
3. 确认无相邻文件被意外修改
4. 输出批次摘要

**不通过 → 返回修复**，修复后重新跑 Batch 内所有任务的自测。

### Step 10: Blocker 处理

遇阻不问猜，立即停止并报告用户：
- 缺失依赖 / 第三方服务不可用
- 测试反复失败且原因不明
- 指令不清或设计矛盾
- 接口校验不一致且无法自行决定

报告格式：
```markdown
## Blocker 报告

- **任务**: {task_id}
- **类型**: {missing_dependency / test_failure / unclear_instruction / design_conflict}
- **现象**: {描述}
- **已尝试**: {尝试过的解决方式}
- **需要决策**: {请用户明确的选项}
```

### Step 11: 完成交接

全部任务完成后：
- 输出执行摘要：总任务数、通过数、失败数、耗时
- **自动触发 `integration-test`**：所有 Batch 编码与单元测试通过后，进入端到端集成测试阶段
- 若用户明确要求或处于项目交付流程中，自动触发 `code-review-pipeline`（阶段 9.25）
- 严禁在未完成集成测试和 UAT 的情况下直接调用 `finish`

## 批次执行摘要模板

每 Batch 结束后输出：

```markdown
## Batch {N} 执行摘要

| 任务 | 状态 | 自测 | 接口校验 | 单测 | 备注 |
|------|------|------|----------|------|------|
| 2.1 | ✅ | 通过 | 通过 | 通过 | — |
| 2.2 | ✅ | 通过 | 通过 | 通过 | — |
| 2.3 | ❌ | 失败 | — | — | Blocker: 依赖服务未启动 |

**批次状态**: {通过 / 需修复 / 存在 Blocker}
**下一步**: {继续 Batch N+1 / 修复后重试 / 等待用户决策}
```

## Anti-Rationalization Framework

| 模式 | 信号短语 | 反制 |
|------|----------|------|
| Time Pressure | "这个改动小，不用跑测试了" | 再小也必须跑单测；跳过测试 = 技术债务 |
| Phase Collapse | "自测和接口校验一起做了吧" | Gate Non-Collapse Rule：自测、接口校验、单测是独立门控，禁止合并 |
| Scope Expansion | "顺便把那个也优化一下" | 记入 NOTICED BUT NOT TOUCHING，禁止顺手重构 |
| Momentum Preservation | "进度不错，跳过检查点继续" | 检查点存在是因为速度≠质量；无检查点不继续 |
| Self-Review Substitution | "我自己看代码没问题" | 必须跑 self-check Skill，不能凭感觉 |

## 与上下游衔接

| 衔接点 | 动作 |
|--------|------|
| 上游: task-breakdown | 消费 tasks.md 作为执行蓝图；解析 checkbox 识别未完成任务 |
| 上游: detailed-design | 读取 feature-*/design.md 作为编码依据 |
| 上游: interface-first-dev | 读取 api-spec.md / openapi.yaml 作为接口校验基准 |
| 横向: test-driven-development | 每个任务内部调用，执行 RED-GREEN-REFACTOR 内循环 |
| 横向: self-check | 每个任务后调用 self-check 进行产出物自查 |
| 横向: unit-test | Batch 完成后触发模块级验证与覆盖率门控（≥70%） |
| 横向: progress-tracker | 每批次完成后自动更新进度 |
| 下游: unit-test | 每个 Batch 完成后触发模块级验证与覆盖率门控（≥70%） |
| 下游: integration-test | 全部任务完成后，进入端到端集成测试阶段 |
| 下游: code-review-pipeline | 编码与测试全部完成后自动触发变更级代码审查（阶段 9.25） |
| 下游: finish | 最终交接收尾 Skill（阶段 11，经 code-review + release-management 后） |

## Gotchas

- **遇阻不问猜**：遇到 blocker（缺失依赖、测试失败、指令不清）必须立即停止并报告用户，严禁强行推进或猜测用户意图
- **Gate Non-Collapse Rule**：自测、接口校验、单测是三个独立门控，禁止合并为"一起检查"；每个门控必须独立执行并通过
- **严禁顺手重构**：Scope Discipline 是硬性规则；发现相邻文件问题只能记录为 `NOTICED BUT NOT TOUCHING`，不得当场修改
- **Rollback-Friendly 提交**：优先新增文件、最小化修改现有代码、DB 迁移配回滚脚本；禁止同一 commit 既删又替
- **Batch 间强制检查点**：无论 Batch 大小，完成后必须执行 Inline Audit，不通过不得进入下一 Batch
- **接口不一致 = blocker**：代码实现的接口与 api-spec / openapi.yaml 不一致时，必须停止并修复，不得妥协
- **tasks.md 是状态机**：自动勾选是执行进度的唯一可信源；禁止口头汇报"做完了"而不勾选
- **main/master 分支保护**：严禁在 main/master 上直接执行，除非用户明确同意
- **现有测试是底线**：任何增量不得导致现有测试失败；出现回归立即停止当前 Batch
- **Simplicity First 不是简陋**：最简单可行方案仍需处理边界条件和异常路径，只是不预先过度工程化
- **执行模式降级**：若 executing-plans 执行中发现任务比 tasks.md 预估更复杂，暂停并建议用户重新执行 task-breakdown
- **TDD 内循环不可跳过**：每个任务必须先写失败测试，再写实现，最后重构；代码文件修改时间早于测试文件 = 拒绝进入 GREEN
- **Unit-Test 门控独立执行**：覆盖率检查是 Batch 完成后的独立门控，禁止与自测、接口校验合并（Gate Non-Collapse）
