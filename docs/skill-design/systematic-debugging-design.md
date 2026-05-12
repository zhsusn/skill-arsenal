# systematic-debugging（系统调试）设计文档

> 版本：V2.1  
> 最后更新：2026-05-12  
> 对应 Skill：`skills/sdlc/systematic-debugging`  
> 对应 meta.json version：`1.1.0`

---

## 1. 设计目标

`systematic-debugging` 是一个**四阶段根因分析引擎**，核心目标是杜绝"症状修复"和"猜测式打补丁"，通过结构化流程将 Bug 修复的一次成功率从 40% 提升到 95% 以上。

其设计意图包括：

- **根因优先**：在任何修复尝试之前，强制完成根因调查，违反即视为调试失败。
- **压力免疫**：通过 Iron Law 和 Anti-Rationalization 框架，抵抗时间压力下的"先试试"冲动。
- **非阻塞联动**：作为被动触发 Skill，修复完成后回归原流程断点，不重置任何 Gate 状态。
- **技术债务兜底**：根因确实无法定位时，将问题转化为可追踪的技术债务，而非假装已修复。

---

## 2. 核心概念

### 2.1 术语表

| 术语 | 定义 |
|------|------|
| **Iron Law** | "NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST" — 调试的绝对铁律。 |
| **症状（Symptom）** | 错误的外在表现（如报错、数据错误、性能下降）。 |
| **根因（Root Cause）** | 导致症状产生的最初触发点，通常位于调用链上游。 |
| **假设-验证（Hypothesis-Test）** | 第三阶段的核心方法：形成单一假设 → 最小改动验证 → 确认或推翻。 |
| **架构质疑（Architecture Challenge）** | 当 3 次以上修复失败后，强制停止并质疑底层架构是否合理。 |
| **技术债务（Technical Debt）** | 根因确实无法定位时，将问题登记为风险项，供后续迭代处理。 |

### 2.2 四阶段模型

```
Phase 1: Root Cause Investigation（根因调查）
  ├── 1.1 仔细阅读错误信息
  ├── 1.2 稳定复现
  ├── 1.3 检查近期变更
  ├── 1.4 多组件系统加诊断 instrumentation
  └── 1.5 数据流反向追踪

Phase 2: Pattern Analysis（模式分析）
  ├── 2.1 寻找同类工作的正确示例
  ├── 2.2 与参考实现完整对比
  ├── 2.3 列出所有差异点
  └── 2.4 理解依赖与环境假设

Phase 3: Hypothesis and Testing（假设与验证）
  ├── 3.1 形成单一假设（"X 是根因，因为 Y"）
  ├── 3.2 最小改动验证
  ├── 3.3 确认结果（通过 → Phase 4 / 失败 → 新假设）
  └── 3.4 不懂就承认，不猜测

Phase 4: Implementation（修复实施）
  ├── 4.1 先写失败测试用例
  ├── 4.2 实施单一修复（不夹带其他改动）
  ├── 4.3 验证修复（测试通过 + 无回归）
  ├── 4.4 若失败：
  │     ├── < 3 次 → 回 Phase 1 重新分析
  │     └── ≥ 3 次 → Architecture Challenge
  └── 4.5 架构质疑：与人类讨论，不继续盲目修复
```

### 2.3 严重度与行动映射

| 场景 | 行动 |
|------|------|
| 稳定复现成功 | 继续 Phase 1 后续步骤 |
| 无法稳定复现 | 收集更多数据，禁止猜测修复 |
| 假设验证成功 | 进入 Phase 4 |
| 假设验证失败 | 形成新假设，禁止叠加修复 |
| 3 次修复失败 | 停止，进入 Architecture Challenge |
| 根因无法定位 | 登记技术债务，回归原流程 |

---

## 3. 架构设计（IPO 模型）

### 3.1 输入（Input）

```
InputSet ::= {
  trigger_source    : enum,           // EXECUTING_PLANS | UNIT_TEST | INTEGRATION_TEST | AD_HOC
  symptom           : string,         // 错误现象描述（报错信息、异常行为）
  logs              : string?,        // 相关日志输出
  code_snippet      : string?,        // 相关代码片段
  recent_changes    : DiffSummary?,   // 近期变更（git diff / commits）
  environment       : EnvSnapshot?,   // 环境差异（依赖版本、配置、OS）
  previous_fixes    : FixAttempt[]    // 之前已尝试的修复（用于计数和判断架构问题）
}

FixAttempt ::= {
  attempt_number    : int,
  hypothesis        : string,
  change_made       : string,
  result            : SUCCESS | FAILED | PARTIAL
}
```

### 3.2 处理（Process）

处理架构采用**严格顺序流水线**，禁止跳阶段：

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        systematic-debugging 主控流程                          │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
              ┌───────────────────────┼───────────────────────┐
              ▼                       ▼                       ▼
    ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
    │ 1. 现象解析层    │     │ 2. 根因追踪层    │     │ 3. 假设验证层    │
    │ Symptom Parser  │     │ Root Tracer     │     │ Hypothesis Lab  │
    └────────┬────────┘     └────────┬────────┘     └────────┬────────┘
             │                       │                       │
             ▼                       ▼                       ▼
    ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
    │ - 错误信息精读   │     │ - 数据流反向追踪 │     │ - 单一假设形成   │
    │ - 复现确认      │     │ - 多组件边界诊断 │     │ - 最小改动验证   │
    │ - 近期变更扫描   │     │ - 参考实现对比   │     │ - 结果判定      │
    │ - 环境差异分析   │     │ - 差异点枚举    │     │ - 计数器管理    │
    └─────────────────┘     └─────────────────┘     └─────────────────┘
                                      │
                                      ▼
                            ┌─────────────────┐
                            │ 4. 修复实施层    │
                            │ Fix Implementer │
                            └────────┬────────┘
                                     │
                                     ▼
                            ┌─────────────────┐
                            │ - 失败测试先行   │
                            │ - 单一修复原则   │
                            │ - 回归验证      │
                            │ - 架构质疑出口   │
                            └─────────────────┘
```

**1. 现象解析层（Symptom Parser）**
- 精读错误信息与堆栈，提取行号、文件路径、错误码。
- 确认复现稳定性；若不稳定，标记为需要更多数据，禁止进入修复阶段。
- 扫描近期变更（git diff、依赖更新、配置变更）。

**2. 根因追踪层（Root Tracer）**
- 对深层调用栈执行反向数据流追踪（参见 `root-cause-tracing.md`）。
- 多组件系统时，在每个边界增加 instrumentation，定位失败层级。
- 寻找同类工作的正确示例，完整阅读参考实现，枚举所有差异。

**3. 假设验证层（Hypothesis Lab）**
- 强制形成单一书面假设："I think X is the root cause because Y"。
- 执行最小改动验证，一次只改一个变量。
- 维护修复尝试计数器；达到 3 次时触发 Architecture Challenge。

**4. 修复实施层（Fix Implementer）**
- 先写失败测试用例（调用 `test-driven-development` Skill）。
- 实施单一修复，严禁"顺手重构"。
- 验证：测试通过 + 无回归 + 原问题确实解决。

### 3.3 输出（Output）

```
OutputSet ::= {
  root_cause_report   : RootCauseReport,   // 根因分析报告
  fix_plan            : FixPlan,           // 修复方案
  verification_result : VerificationResult,// 验证结果
  technical_debt      : TechnicalDebt?,    // 若根因无法定位
  return_point        : ReturnPoint        // 回归断点信息
}

RootCauseReport ::= {
  symptom             : string,
  root_cause          : string,
  evidence_chain      : Evidence[],
  investigation_depth : enum              // SURFACE | DEEP | ARCHITECTURAL
}

FixPlan ::= {
  target_file         : string,
  line_range          : [int, int],
  change_description  : string,
  test_case           : string            // 先写的失败测试
}

TechnicalDebt ::= {
  debt_id             : string,           // 如 "R-001"
  module              : string,
  symptom_summary     : string,
  phase               : string,
  created_at          : ISO8601,
  status              : OPEN
}
```

---

## 4. 状态机与数据模型

### 4.1 调试生命周期状态机

```
                    ┌─────────────┐
           ┌───────>│   TRIGGERED │<───────┐
           │        │  (被动触发)  │        │
           │        └──────┬──────┘        │
           │               │ 开始四阶段     │
           │               ▼               │
           │        ┌─────────────┐        │
           │        │INVESTIGATING│        │
           │        │  (调查中)    │        │
           │        └──────┬──────┘        │
           │               │               │
     ┌─────┼─────┐    ┌────┴────┐   ┌─────┼─────┐
     ▼     ▼     ▼    ▼         ▼   ▼     ▼     ▼
┌────────┐    ┌────────┐   ┌────────┐   ┌────────┐
│ FIXED  │    │ARCH.   │   │DEBT    │   │ABORTED │
│        │    │CHALLENGE      │   │        │   │        │
└───┬────┘    └───┬────┘   └───┬────┘   └────────┘
    │             │            │
    ▼             ▼            ▼
[回归原流程]  [人类讨论]   [记入progress.md]
```

状态说明：
- **TRIGGERED**：任意阶段的 Bug/异常触发了 systematic-debugging。
- **INVESTIGATING**：正在执行四阶段流程。
- **FIXED**：根因定位成功，修复通过验证，返回原流程断点。
- **ARCH_CHALLENGE**：3 次以上修复失败，停止并质疑架构。
- **DEBT**：根因确实无法定位（环境/时序/外部因素），登记为技术债务。
- **ABORTED**：用户主动中断或缺少必要上下文。

### 4.2 关键数据模型

#### Evidence（证据项）

```yaml
Evidence:
  type: enum              # ERROR_LOG | GIT_DIFF | STACK_TRACE | INSTRUMENTATION | REFERENCE_COMPARE
  source: string          # 文件路径或命令
  snippet: string         # 关键片段
  observation: string     # 观察结论
```

#### AntiPatternLog（反模式记录）

用于追踪调试过程中是否出现 Red Flag 思维：

```yaml
AntiPatternLog:
  pattern: enum           # QUICK_FIX | SKIP_TEST | MULTIPLE_FIXES | GUESSING | ADAPT_PATTERN
  timestamp: ISO8601
  triggered_by: string    # 哪条思考触发了反模式
  resolution: string      # 如何纠正（回退到哪个 Phase）
```

---

## 5. 集成方案

### 5.1 与执行流水线的集成

```
executing-plans / unit-test / integration-test
    └── 遇到 Bug/异常
         └── 自动触发 systematic-debugging
              ├── 输出：根因报告 + 修复方案
              └── 验证修复后
                   └── 返回原流程断点继续执行
                        ├── 若在 executing-plans 中触发 → 回到当前任务
                        ├── 若在 unit-test 中触发 → 重新运行当前模块测试
                        └── 若在 integration-test 中触发 → 重新运行集成测试
```

**关键规则**：
- 不阻塞主流程进度。
- 调试完成后回到触发点，不重置 Gate 状态。
- 若在 `executing-plans` 的 Batch 中触发，修复后重新执行当前任务的 self-check 和单元测试。

### 5.2 与 progress-tracker 的联动（V2.1）

当根因无法定位时：

```
systematic-debugging
    └── 根因无法定位
         └── 生成 TechnicalDebt
              └── 写入 progress.md risks 数组
                   └── progress-tracker 更新风险登记
```

```yaml
# progress.md 中的风险登记示例
risks:
  - id: R-042
    type: technical-debt
    description: "[支付模块] 偶发超时 — 根因未定位，疑为第三方网关时序问题"
    phase: integration-test
    created_at: "2026-05-12T10:30:00Z"
    status: open
```

### 5.3 与相关 Skill 的协作

| Skill | 协作方式 |
|-------|----------|
| `test-driven-development` | Phase 4 修复前，调用其编写失败测试用例 |
| `self-check` | 修复完成后，调用其验证修复质量 |
| `progress-tracker` | 根因无法定位时，登记技术债务；修复成功后更新任务状态 |

---

## 6. 安全与约束

### 6.1 调试纪律约束

| 约束 | 说明 | 违反后果 |
|------|------|----------|
| Iron Law | 未完成 Phase 1 不得提议修复 | 视为调试失败，强制回退 |
| 单一假设 | Phase 3 每次只验证一个假设 | 叠加修复导致无法归因 |
| 3 次上限 | 3 次修复失败必须质疑架构 | 继续盲目修复视为违规 |
| 测试先行 | Phase 4 必须先写失败测试 | 无测试的修复不视为完成 |
| 非阻塞 | 不得重置 Gate 状态 | 违规影响进度追踪准确性 |

### 6.2 审计追踪

- 每次调试过程建议记录到 `.kimi/logs/debugging-{timestamp}.md`。
- 记录内容：触发来源、四阶段关键决策、假设列表、修复尝试计数、最终结论。
- 技术债务项必须保留在 `progress.md` 中直至关闭。

---

## 7. 后期演进方向

### 7.1 短期（V2.2）

- **历史模式匹配**：将当前 Bug 的特征与历史调试记录匹配，推荐最可能的根因方向。
- **自动化 instrumentation**：对多组件系统，自动生成边界日志代码，减少手动添加工作量。
- **修复影响预测**：基于代码依赖图，预测某修复可能影响的测试范围。

### 7.2 中期（V3.0）

- **时序问题专项**：增加对 race condition、死锁、异步时序问题的专项诊断流程。
- **性能根因分析**：扩展四阶段模型至性能问题（CPU/Memory/IO 瓶颈定位）。
- **跨会话记忆**：技术债务的调试历史在后续会话中可恢复，避免重复调查。

### 7.3 长期（V4.0）

- **预防性调试**：基于代码变更模式，在编码阶段实时提示"此变更与历史上某 Bug 模式相似"。
- **根因知识库**：将项目历史 Bug 的根因沉淀为可查询知识库，供新成员学习。
- **人机协作闭环**：人类开发者的调试结论反馈给 AI，持续校准根因识别准确率。

---

## 附录：版本变更日志

| 版本 | 日期 | 变更内容 |
|------|------|----------|
| V1.0 | — | Superpowers 原生四阶段调试框架。 |
| V2.0 | — | 引入 Anti-Rationalization 框架、Red Flags、Architecture Challenge。 |
| V2.1 | 2026-05 | 新增与 progress-tracker 的技术债务联动；本地化 skill 引用；description 中文化；新增 meta.json。 |
