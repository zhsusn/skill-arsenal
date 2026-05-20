---
name: unit-test
description: 当 executing-plans 完成一个 Batch 后、用户要求'补全单元测试'、'覆盖率检查'、'运行单测'，或需要模块级边界测试与 ≥70% 覆盖率门控时触发。
---

# Unit Test（单元测试）

## 适用场景

- executing-plans 一个 Batch 编码完成后，系统性地补全模块级测试
- 用户明确要求"生成单元测试"、"检查覆盖率"
- 作为进入 integration-test 的前置门控
- 验证边界条件、异常路径、状态机覆盖

## 前置依赖

- executing-plans 当前 Batch 的 TDD 内循环已完成（tasks.md 中任务已勾选）
- 已完成的源代码文件
- `feature-*/test-plan.md`（测试策略与用例设计）
- `feature-*/logic.md`（业务逻辑与状态机）

## 硬约束

| 约束 | 说明 |
|------|------|
| 覆盖率 ≥ 70% | 不满足则阻塞下游 integration-test |
| 独立运行 | 不依赖外部服务（数据库、缓存、第三方 API） |
| 内存数据库 | 使用 SQLite :memory: 或 mock 替代真实 DB |
| 边界覆盖 | 必须包含错误路径、异常分支、空值/越界输入 |
| 代码风格 | 测试代码必须遵循对应语言的代码风格（Python → `python-google-style`、Java → `java-alibaba-style`、其他语言使用默认风格） |

## 执行流程

### Step 1: 前置检查

确认当前 Batch 的 TDD 内循环已完成：
- 读取 `tasks.md`，检查当前 Batch 的所有任务已勾选
- 若存在未完成任务，终止并提示先完成 TDD

### Step 2: 读取设计文档

1. 读取 `feature-*/test-plan.md`，提取测试场景与验收标准
2. 读取 `feature-*/logic.md`，识别状态机与边界条件

### Step 3: 补全边界测试（TDD 通常遗漏的部分）

针对每个模块生成测试，重点补全 TDD 未覆盖的边界：

- 异常状态机转移（如网络中断、权限不足、数据为空）
- 空值 / 越界 / 并发输入
- 外部服务超时 / 降级场景
- 每个功能点：至少 1 个正向 + 2 个异常用例

**依赖隔离规范：**
- DB 连接：使用 `unittest.mock` 或 `pytest-mock` 替换，或使用 SQLite `:memory:`
- Redis / 缓存：统一 mock
- HTTP 客户端：禁止测试用例中出现真实网络调用
- 外部服务：使用 fixture 自动注入 mock

### Step 4: 组织测试代码

按模块统一组织到 `tests/unit/{模块}/` 目录：

```
tests/unit/
├── {module}/
│   ├── test_*.py          # 测试用例
│   └── conftest.py        # 模块级 fixture
```

### Step 5: 执行测试与覆盖率门控

```bash
pytest tests/unit/ -v --cov={模块} --cov-report=term-missing
```

**门控逻辑：**
- 覆盖率 ≥ 70%：通过，继续 Step 6
- 覆盖率 < 70%：输出未覆盖行号清单，**阻塞流程**，返回 executing-plans 补 TDD 或补边界测试

### Step 6: 生成覆盖率报告

保存 `tests/unit/coverage-report.md`，包含：

```markdown
# 单元测试覆盖率报告

## 汇总
| 模块 | 覆盖率 | 状态 |
|------|--------|------|
| {module} | {cov}% | 通过/阻塞 |

## 未覆盖函数列表
- `{file}:{line}` `{function}`

## 追溯矩阵（用例 ↔ 需求）
| 用例编号 | 需求编号 | 描述 | 状态 |
|----------|----------|------|------|
| TC-001 | FR-001 | xxx | 通过 |
```

## 与上下游衔接

| 衔接点 | 动作 |
|--------|------|
| 上游: executing-plans | Batch 完成后触发；TDD 已覆盖正向路径 |
| 下游: integration-test | 输出 `coverage-report.md` 作为门控输入；覆盖率 < 70% 则阻塞 |

## Gotchas

- **禁止跳过覆盖率门控**：覆盖率 < 70% 时绝不允许进入 integration-test
- **专注边界补全**：不要重复生成 TDD 已覆盖的正向路径测试，避免冗余
- **Mock 必须完整**：mock 数据结构必须包含真实 API 的所有字段，禁止部分 mock
- **测试必须独立**：每个测试用例可独立运行，禁止测试间状态污染
- **不得引入真实外部依赖**：任何真实网络调用、真实数据库连接均为红线
- **未覆盖清单必须精确到行号**：覆盖率报告需输出具体未覆盖的行号范围，便于快速定位
- **与 test-plan 的追溯一致性**：自检时检查每个验收标准是否至少有一个测试用例覆盖
