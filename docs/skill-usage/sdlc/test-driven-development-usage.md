# Test-Driven Development Skill 使用手册

> 本文档面向 Skill 使用者，提供 TDD 的触发方式、RED-GREEN-REFACTOR 循环操作指南与常见问题。
>
> 版本: 2.0.0

---

## 1. 快速开始

### 1.1 什么是 TDD？

`test-driven-development` 是**任务级测试先行方法论**。它要求你在写任何实现代码之前，先写一个失败的测试，然后写最小实现让它通过，最后安全重构。

**核心原则**：如果你没看到测试失败，你就不知道它测的是不是正确的东西。

### 1.2 触发方式

TDD **不再作为独立 Skill 调用**，而是内嵌在 `executing-plans` 的每个任务中自动执行。

| 方式 | 说明 |
|------|------|
| 自动触发 | executing-plans Step 3 每个任务内部自动调用 |
| 手动强调 | 在任务描述中明确要求"严格 TDD" |
| 独立调用 | 如需要单独使用，可直接引用 `@skills/sdlc/test-driven-development/SKILL.md` |

---

## 2. 使用步骤

### Step 1: 理解当前任务

在执行 TDD 前，确保你有：
- ✅ 当前任务的验收标准
- ✅ `api-spec.md` 或 `openapi.yaml` 中的接口定义
- ✅ 清晰的输入输出预期

### Step 2: RED - 写失败测试

**先写测试，禁止先写实现。**

```typescript
// 好示例：测试真实行为
test('rejects empty email', async () => {
  const result = await submitForm({ email: '' });
  expect(result.error).toBe('Email required');
});
```

**要求**：
- 一个测试只测一个行为
- 命名清晰（出现 "and" 则拆分）
- 使用真实代码，避免 mock（除非隔离外部依赖）
- 测试文件临时存放：`.kimi/temp-tests/{任务ID}_red.py`

### Step 3: Verify RED - 验证失败

运行测试，确认：
- ✅ 测试失败（不是报错）
- ✅ 失败信息符合预期
- ✅ 失败原因是功能缺失

```bash
$ pytest .kimi/temp-tests/task_2_1_red.py -v
FAILED: expected 'Email required', got undefined
```

**如果测试通过了？** 你在测试已有行为，修正测试。

**如果测试报错了？** 修正错误，重跑直到正确失败。

### Step 4: GREEN - 最小实现

写最简单、最丑但能让测试通过的代码。

```typescript
function submitForm(data: FormData) {
  if (!data.email?.trim()) {
    return { error: 'Email required' };
  }
  // ...
}
```

**禁止**：
- 优化代码结构
- 提取公共函数
- 处理任务范围外的边界情况
- 添加 spec 外功能

### Step 5: Verify GREEN - 验证通过

运行测试，确认：
- ✅ 新测试通过
- ✅ 其他测试仍通过
- ✅ 输出干净（无报错、无警告）

### Step 6: REFACTOR - 安全重构

在测试全部通过的前提下清理代码：
- 允许：提取函数、重命名变量、消除重复
- 禁止：修改接口签名、新增功能

**每次重构后必须重新运行测试。**

---

## 3. TDD 门控检查点

每个任务完成后，确认以下 5 项：

| 检查项 | 确认方式 |
|--------|----------|
| RED 先写且失败 | 测试文件创建时间早于实现文件 |
| GREEN 最小化 | 实现无过度设计，无任务外功能 |
| REFACTOR 全绿 | `pytest` 全部通过 |
| Rollback-Friendly | 优先新增文件，最小化修改现有代码 |
| NOTICED 清单已更新 | 发现的相邻问题已记录，未当场修复 |

---

## 4. 常见合理化借口与反制

| 借口 | 反制 |
|------|------|
| "太简单了不用测" | 简单代码也会坏。测试只需 30 秒。 |
| "我后面再测" | 后面写的测试立即通过，证明不了什么。 |
| "已经手动测过了" | 手动测试是临时性的，没有记录，无法重跑。 |
| "删掉 X 小时的工作太浪费了" | 沉没成本谬误。不能信任的代码才是浪费。 |
| "TDD 太教条，我要务实" | TDD 就是务实：提前发现 bug 比事后调试快。 |

---

## 5. 常见问题

### Q1：TDD 和 unit-test 有什么区别？

| 维度 | TDD | unit-test |
|------|-----|-----------|
| 时机 | 编码过程中（任务级） | 编码完成后（模块级） |
| 目的 | 驱动设计 | 验证质量 |
| 覆盖 | 正向路径、接口契约 | 边界条件、异常路径 |
| 输出 | 内联测试（临时目录） | `tests/unit/` + 覆盖率报告 |

**关系**：TDD 产出的内联测试在 Batch 完成后由 unit-test 统一整理。

### Q2：可以先写实现后补测试吗？

**绝对不可以。** 先写实现后补测试 = 技术债务。必须删除实现，从测试重新开始。

### Q3：测试文件必须放在 `.kimi/temp-tests/` 吗？

建议存放于 `.kimi/temp-tests/{任务ID}_red.py`，便于 Batch 后由 unit-test 统一整理。如果项目结构要求放在其他位置，也可以接受，但需确保 unit-test 能识别和整理。

### Q4：发现相邻文件有问题怎么办？

**不动代码**，记入 `NOTICED BUT NOT TOUCHING` 列表。例如：

```markdown
## NOTICED BUT NOT TOUCHING

- `src/services/order_service.py:123` —— 重复代码，建议后续重构
```

### Q5：GREEN 阶段可以顺手修个小 bug 吗？

**不可以。** GREEN 阶段只允许最小实现。所有发现的问题记入 NOTICED 清单，后续任务处理。

---

## 6. 速查卡

```text
触发：executing-plans 每个任务内部自动调用
输入：任务描述 + api-spec.md + 验收标准
输出：实现代码 + 内联测试（临时目录）
原则：先写测试 → 看它失败 → 最小实现 → 测试通过 → 安全重构
纪律：一个行为一个测试、真实代码优先、GREEN 不优化、REFACTOR 不新增功能
禁止：先写实现后补测试、跳过 RED 验证、GREEN 阶段顺手重构、处理任务外问题
检查点：RED 先写、GREEN 最小、REFACTOR 全绿、Rollback-Friendly、NOTICED 已更新
```
