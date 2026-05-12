# Unit Test Skill 使用手册

> 本文档面向 Skill 使用者，提供 unit-test 的触发方式、覆盖率门控解读、边界测试补全指南与常见问题。
>
> 版本: 1.0.0

---

## 1. 快速开始

### 1.1 什么是 Unit Test？

`unit-test` 是**模块级质量门控**。它在 executing-plans 完成一个 Batch 后，系统性地补全边界测试、生成覆盖率报告，并以 ≥70% 覆盖率作为硬性门槛阻塞下游。

**核心原则**：TDD 覆盖了正向路径，unit-test 负责补上它遗漏的边界和异常。

### 1.2 触发方式

| 方式 | 说明 |
|------|------|
| 自动触发 | executing-plans 每个 Batch 完成后自动调用 |
| 手动触发 | 用户明确要求"补全单元测试"、"检查覆盖率" |
| 阻塞恢复 | 覆盖率不足时，修复后重新触发 |

---

## 2. 使用步骤

### Step 1: 确认前置条件

unit-test 需要以下输入：
- ✅ `tasks.md` 当前 Batch 任务已勾选（TDD 内循环完成）
- ✅ `feature-*/test-plan.md`（测试策略）
- ✅ `feature-*/logic.md`（业务逻辑与状态机）
- ✅ 已完成的源代码文件

**如果任务未勾选**：unit-test 会终止并提示先完成 TDD。

### Step 2: 读取设计文档

unit-test 自动读取：
- `test-plan.md`：提取测试场景与验收标准
- `logic.md`：识别状态机与边界条件

### Step 3: 补全边界测试

unit-test **专注补全 TDD 遗漏的边界**：

| 边界类型 | 示例 |
|----------|------|
| 异常状态机转移 | 网络中断、权限不足、数据为空 |
| 输入边界 | 空值、越界、非法格式、超大值 |
| 并发场景 | 重复提交、竞态条件 |
| 外部服务异常 | 超时、降级、返回非预期格式 |

**生成规则**：每个功能点至少 1 个正向 + 2 个异常用例。

### Step 4: 组织测试代码

自动按模块组织到 `tests/unit/{模块}/`：

```
tests/unit/
├── user_service/
│   ├── test_register.py
│   └── conftest.py
├── order_service/
│   ├── test_create_order.py
│   └── conftest.py
```

### Step 5: 执行覆盖率门控

```bash
pytest tests/unit/ -v --cov={模块} --cov-report=term-missing
```

**输出示例**：
```
---------- coverage: platform linux, python 3.11 ----------
Name                      Stmts   Miss  Cover   Missing
-------------------------------------------------------
src/user_service.py          45      8    82%   23-28, 45-50
src/order_service.py         60     18    70%   35-45, 55-60
-------------------------------------------------------
TOTAL                       105     26    75%

覆盖率 75% ≥ 70%，通过。
```

**门控结果**：
- **通过**（≥ 70%）→ 继续 Step 6
- **阻塞**（< 70%）→ 输出未覆盖行号清单，返回 executing-plans 补测试

### Step 6: 生成覆盖率报告

自动保存 `tests/unit/coverage-report.md`，包含：
- 模块覆盖率汇总
- 未覆盖函数列表（精确到行号）
- 用例与需求的追溯矩阵

---

## 3. 输出解读

### 3.1 覆盖率报告结构

```markdown
# 单元测试覆盖率报告

## 汇总
| 模块 | 覆盖率 | 状态 |
|------|--------|------|
| user_service | 82% | 通过 |
| order_service | 70% | 通过 |

## 未覆盖函数列表
- `src/order_service.py:35` `apply_coupon()`

## 追溯矩阵
| 用例编号 | 需求编号 | 描述 | 状态 |
|----------|----------|------|------|
| TC-001 | FR-001 | 正常注册 | 通过 |
```

### 3.2 状态含义

| 状态 | 含义 |
|------|------|
| 通过 | 覆盖率 ≥ 70%，可进入 integration-test |
| 阻塞 | 覆盖率 < 70%，必须补测试后才能继续 |

---

## 4. 执行纪律速查

### 4.1 依赖隔离

- **禁止**真实数据库连接 → 使用 SQLite `:memory:` 或 mock
- **禁止**真实网络调用 → 使用 `unittest.mock` 或 `pytest-mock`
- **禁止**真实 Redis / 缓存 → 统一 mock

### 4.2 与 TDD 的分工

| 类型 | 谁负责 | 说明 |
|------|--------|------|
| 正向路径 | TDD | 接口契约、正常流程 |
| 边界条件 | unit-test | 异常、空值、越界 |
| 状态机转移 | unit-test | 网络中断、权限不足 |
| 外部服务超时 | unit-test | 超时、降级 |

---

## 5. 常见问题

### Q1：覆盖率可以低于 70% 吗？

**不可以。** 70% 是硬性门控，阻塞 integration-test。

如确实需要放宽，必须：
1. 用户明确同意
2. 记录原因（如"遗留代码无法测试"）
3. 标记豁免范围（精确到文件/函数）

### Q2：unit-test 会重复生成 TDD 已经写好的测试吗？

**不会。** unit-test 专注边界补全，TDD 已覆盖的正向路径测试由 unit-test 统一整理到 `tests/unit/`，避免重复。

### Q3：mock 有什么要求？

- mock 数据结构必须包含真实 API 的**所有字段**
- 禁止部分 mock（只 mock 你认识的字段）
- 优先 mock 外部依赖的底层（如 HTTP 客户端），而非被测对象本身

### Q4：覆盖率不足时怎么快速定位？

unit-test 输出未覆盖行号清单，格式：
```
未覆盖行号：src/order_service.py:35-45, 55-60
```

直接定位到具体函数，补充对应测试即可。

### Q5：可以跳过 unit-test 直接做集成测试吗？

**绝对不可以。** unit-test 是 integration-test 的前置门控。跳过 unit-test = 技术债务 + 集成测试不稳定。

### Q6：测试数据怎么准备？

使用 `conftest.py` 中的 fixture：

```python
@pytest.fixture
def mock_user():
    return {"id": 1, "name": "Alice", "email": "alice@example.com"}
```

禁止在测试用例中直接创建真实数据库记录。

---

## 6. 速查卡

```text
触发：executing-plans Batch 完成后自动调用 / 用户要求"补全单元测试"
输入：tasks.md + test-plan.md + logic.md + 源代码
输出：tests/unit/{模块}/ + coverage-report.md
原则：专注边界补全（TDD 已覆盖正向路径）、≥70% 硬性门控、独立运行
流程：前置检查 → 读取设计文档 → 补全边界测试 → 组织代码 → 覆盖率门控 → 生成报告
门控：覆盖率 < 70% → 阻塞，输出未覆盖行号清单
纪律：禁止真实外部依赖、mock 必须完整、测试必须独立
禁止：跳过覆盖率门控、重复生成正向测试、引入真实数据库连接
```
