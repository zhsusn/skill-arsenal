# Test-Driven Development Skill 设计规格书

> 本文档面向 Skill 实现者与维护者，描述 `test-driven-development` 的完整技术架构、RED-GREEN-REFACTOR 循环纪律、与 executing-plans 的内循环集成协议。
>
> 版本: 2.0.0（从 Superpowers 原生改造）

---

## 1. 功能定位

| 维度 | 说明 |
|------|------|
| **核心职责** | 任务级测试先行方法论，通过 RED-GREEN-REFACTOR 循环驱动接口设计，防止过度工程 |
| **所处阶段** | 开发阶段（executing-plans Step 3 内部，每个任务执行时） |
| **上游输入** | executing-plans 当前任务描述、api-spec.md、验收标准 |
| **下游输出** | 内联测试代码 + 实现代码（同步产出），临时存放于 `.kimi/temp-tests/` 或同级目录 |
| **设计模式** | `inversion`（结构化需求访谈/纪律） |
| **开源对标** | Superpowers `test-driven-development`（RED-GREEN-REFACTOR、Iron Law、Testing Anti-Patterns） |

---

## 2. 总体架构

```
┌─────────────────────────────────────────────────────────────┐
│           test-driven-development Skill（任务级内循环）        │
├─────────────────────────────────────────────────────────────┤
│  触发方式：executing-plans 每个任务内部自动调用               │
│  执行模式：RED-GREEN-REFACTOR 循环，单个任务 2-5 分钟        │
│  架构模式：内嵌于 executing-plans 的任务级纪律               │
│  核心约束：Iron Law、Verify RED、Verify GREEN、最小化实现     │
└─────────────────────────────────────────────────────────────┘
```

### 2.1 改造前后对比

| 维度 | Superpowers 原生 | 本方案改造后 |
|------|------------------|-------------|
| 触发方式 | 独立 Skill 调用（`/skill:tdd`） | **内嵌于 executing-plans 每个任务**，无需单独调用 |
| 衔接关系 | 与 executing-plans 通过对话衔接 | 直接内嵌为 executing-plans Step 3 的子步骤 |
| 输出物管理 | 测试代码散落在实现附近 | 明确临时路径 `.kimi/temp-tests/{任务ID}_red.py`，Batch 后由 unit-test 统一整理 |
| 门控检查 | 无显式检查点 | 新增 **TDD 门控检查点**（5 项必确认清单） |
| 与 unit-test 关系 | 职责重叠 | **明确分离**：TDD 负责任务级正向路径，unit-test 负责模块级边界补全 |

---

## 3. 处理逻辑

### 3.1 RED-GREEN-REFACTOR 循环

```
┌─────────┐     ┌─────────────┐     ┌─────────┐     ┌─────────────┐     ┌───────────┐
│   RED   │ → → │  Verify RED │ → → │  GREEN  │ → → │ Verify GREEN│ → → │ REFACTOR  │
│写失败测试│     │ 验证确实失败 │     │ 最小实现 │     │ 验证全部通过 │     │ 安全重构  │
└─────────┘     └─────────────┘     └─────────┘     └─────────────┘     └─────┬─────┘
                                                                               │
                                    ┌──────────────────────────────────────────┘
                                    ↓
                              ┌─────────────┐
                              │  下一任务   │
                              └─────────────┘
```

### 3.2 详细步骤

#### R - RED（写失败测试）

**输入**：当前任务验收标准 + `api-spec.md` 接口定义

**要求**：
- 一个行为，一个测试
- 命名清晰（出现 "and" 则拆分）
- 使用真实代码（mock 仅用于隔离外部依赖）
- 测试必须失败（验证测试本身有效）
- **禁止先写实现代码后补测试**
- 测试文件临时存放：`.kimi/temp-tests/{任务ID}_red.py`

**好示例 vs 坏示例**：
- 好：测试真实行为（`retries failed operations 3 times`）
- 坏：测试 mock 行为（`retry works` + 断言 mock 调用次数）

#### Verify RED - 验证失败（强制步骤）

```bash
npm test path/to/test.test.ts
# 或 pytest path/to/test.py -v
```

**确认项**：
- [ ] 测试失败（不是报错）
- [ ] 失败信息符合预期
- [ ] 失败原因是功能缺失（不是拼写错误）

**异常处理**：
- 测试通过 → 修正测试（你在测已有行为）
- 测试报错 → 修正错误，重跑直到正确失败

#### G - GREEN（最小实现）

**铁律**：编写最简单、最丑但能让测试通过的实现。

**禁止项**：
- 在 GREEN 阶段优化代码结构、提取公共函数、重命名变量
- 处理当前任务范围外的边界情况
- 若发现相邻问题，记入 `NOTICED BUT NOT TOUCHING`，不修复

**好示例 vs 坏示例**：
- 好：`for (let i = 0; i < 3; i++)` —— 刚好通过
- 坏：引入 `maxRetries`、`backoff`、`onRetry` 选项 —— YAGNI

#### Verify GREEN - 验证通过（强制步骤）

**确认项**：
- [ ] 新测试通过
- [ ] 其他测试仍通过（回归保护）
- [ ] 输出干净（无报错、无警告）

**异常处理**：
- 新测试失败 → 修正代码，不是测试
- 其他测试失败 → 立即修复

#### R - REFACTOR（安全重构）

**前提**：测试全部通过。

**允许**：提取函数、重命名变量、消除重复、优化导入。

**禁止**：修改接口签名、新增功能、处理 `NOTICED BUT NOT TOUCHING` 中的问题。

**要求**：每次重构后必须重新运行测试。

---

## 4. TDD 门控检查点

每个任务完成后必须确认：

| 检查项 | 说明 |
|--------|------|
| RED 先写且失败 | 测试确实先于实现编写，且首次运行失败 |
| GREEN 最小化 | 实现无过度设计，无任务外功能 |
| REFACTOR 全绿 | 重构后所有测试通过 |
| Rollback-Friendly | 优先新增文件，便于回滚 |
| NOTICED 清单已更新 | 发现的相邻问题已记录，未当场修复 |

---

## 5. 输入输出规格

### 5.1 输入

| 输入项 | 类型 | 来源 | 说明 |
|--------|------|------|------|
| 任务描述 | Markdown | executing-plans 当前任务 | 功能点描述 |
| 接口定义 | Markdown/YAML | `api-spec.md` / `openapi.yaml` | 接口契约 |
| 验收标准 | Markdown | 任务描述内嵌 | 预期行为 |

### 5.2 输出

| 输出项 | 类型 | 路径 | 说明 |
|--------|------|------|------|
| 内联测试 | 测试代码 | `.kimi/temp-tests/{任务ID}_red.py` 或同级目录 | RED 阶段产出的失败测试 |
| 实现代码 | 源代码 | 项目源码目录 | GREEN 阶段产出的最小实现 |
| 重构后代码 | 源代码 | 项目源码目录 | REFACTOR 阶段清理后的代码 |
| NOTICED 清单 | Markdown | 对话内联 / `NOTICED_BUT_NOT_TOUCHING.md` | 记录的相邻问题 |

---

## 6. 与上下游衔接

| 衔接点 | 动作 |
|--------|------|
| 上游: executing-plans | 每个开发任务的内部执行纪律，由 executing-plans 在 Step 3 调用 |
| 横向: unit-test | TDD 产出的内联测试在 Batch 完成后由 unit-test 统一整理到 `tests/unit/` |
| 横向: self-check | GREEN 阶段完成后可调用 self-check 验证代码与设计一致性 |

---

## 7. 开源复用分析

### 7.1 能力映射

| TDD 能力 | 可对标的开源 Skill | 复用度 | 差距分析 |
|---------|-------------------|--------|----------|
| RED-GREEN-REFACTOR | Superpowers `test-driven-development` | ✅ 高 | 直接复用，增加门控检查点 |
| Iron Law | Superpowers `test-driven-development` | ✅ 高 | 直接复用 |
| Testing Anti-Patterns | Superpowers `test-driven-development` | ✅ 高 | 保留 `@testing-anti-patterns.md` 引用 |
| 任务级内循环 | docs-internal 降级方案 | ⚠️ 改造 | 从独立 Skill 转为 executing-plans 内置纪律 |

### 7.2 改造要点

| 改造项 | 原因 | 实现方式 |
|--------|------|----------|
| 内嵌 executing-plans | 减少上下文切换，降低 Skill 维护数量 | 在 executing-plans Step 3 中显式调用 TDD 循环 |
| 增加门控检查点 | 确保 RED 不被跳过、GREEN 不膨胀 | 5 项必确认清单 |
| 明确与 unit-test 边界 | 避免职责重叠 | TDD 负责任务级正向路径，unit-test 负责模块级边界补全 |
| 临时测试路径规范 | 便于 Batch 后统一整理 | `.kimi/temp-tests/{任务ID}_red.py` |

---

## 8. 风险与规避

| 风险 | 规避方法 |
|------|----------|
| RED 阶段被跳过（先写实现后补测试） | 文件时间戳检查：代码文件修改时间早于测试文件 = 拒绝进入 GREEN |
| GREEN 阶段过度设计 | Iron Law + Simplicity First：只允许最小实现 |
| REFACTOR 阶段顺手修 bug | 禁止处理 `NOTICED BUT NOT TOUCHING` 中的问题 |
| TDD 内循环导致单个任务耗时增加 | 前 2 个 Batch 放宽节奏；或调整 Batch 大小为 2 任务 |
| 与 unit-test 测试重复 | TDD 测试保留在临时目录，最终由 unit-test 统一去重整理 |

---

## 9. 附录：测试阶段三 Skill 协作图

```
executing-plans (Batch 执行)
    │
    ├── 任务 N 内部: test-driven-development (RED-GREEN-REFACTOR)
    │       └── 产出: 实现代码 + 内联测试（任务级）
    │
    └── Batch 完成后: unit-test (模块级验证)
            ├── 读取 test-plan.md + logic.md
            ├── 补全边界测试（异常/空值/越界/超时）
            ├── 统一组织到 tests/unit/{模块}/
            ├── 运行 pytest --cov={模块} --cov-report=term-missing
            ├── 覆盖率 ≥ 70% ?
            │       ├── 通过 → 保存 coverage-report.md → 进入 integration-test
            │       └── 不通过 → 返回 executing-plans 补 TDD 或补边界测试
            │
            └── integration-test (端到端验证)
                    ├── 前置检查: coverage-report.md ≥ 70%
                    ├── 读取 spec.md + openapi.yaml
                    ├── Phase 1: 测试设计（步骤/预期/命令）
                    ├── Phase 2: 生成 tests/integration/test_*.py
                    ├── Phase 3: 执行 + Green Mirage Audit
                    └── Phase 4: 生成 user-stories-checklist.md → 解锁 Gate 3 (UAT)
```
