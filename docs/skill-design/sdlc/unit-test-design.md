# Unit Test Skill 设计规格书

> 本文档面向 Skill 实现者与维护者，描述 `unit-test` 的完整技术架构、边界补全策略、覆盖率门控机制及与 TDD / integration-test 的衔接协议。
>
> 版本: 1.0.0

---

## 1. 功能定位

| 维度 | 说明 |
|------|------|
| **核心职责** | Batch 完成后系统性地补全模块级测试，专注边界条件与异常路径，执行 ≥70% 覆盖率硬门控 |
| **所处阶段** | 测试阶段（阶段 8），前置依赖 executing-plans（TDD 内循环完成），被 integration-test 依赖 |
| **上游输入** | `feature-*/test-plan.md`、`feature-*/logic.md`、已完成源代码、TDD 内联测试 |
| **下游输出** | `tests/unit/{模块}/test_*.py`、`tests/unit/{模块}/conftest.py`、`tests/unit/coverage-report.md` |
| **设计模式** | `reviewer`（审查员/验证器） |
| **开源对标** | docs-internal 自定义设计（无直接开源对标，TDD 正向路径已由 Superpowers 覆盖） |

---

## 2. 总体架构

```
┌─────────────────────────────────────────────────────────────┐
│                     unit-test Skill                          │
├─────────────────────────────────────────────────────────────┤
│  触发方式：executing-plans Batch 完成后自动调用               │
│  执行模式：模块级批量测试生成 + 覆盖率审计                    │
│  架构模式：读取设计文档 → 补全边界 → 组织测试 → 覆盖率门控    │
│  核心约束：覆盖率 ≥70%、独立运行、边界覆盖、需求追溯           │
└─────────────────────────────────────────────────────────────┘
```

### 2.1 与 TDD 的职责分离

| 维度 | test-driven-development | unit-test |
|------|------------------------|-----------|
| 定位 | 开发方法论 | 质量门控 |
| 执行时机 | 编码过程中（任务级） | 编码完成后（模块级） |
| 工作模式 | RED-GREEN-REFACTOR | 读取代码 + 设计文档 → 补全测试 |
| 核心目的 | 驱动设计，约束接口 | 验证质量，产出审计级报告 |
| 覆盖重点 | 正向路径、接口契约 | 边界条件、异常路径、状态机转移 |
| 输出物 | 内联测试（临时目录） | `tests/unit/` 目录 + `coverage-report.md` |

---

## 3. 处理逻辑

### 3.1 主控流程

```
Step 1: 前置检查（tasks.md Batch 任务已勾选？）
    ├── 未完成 → 终止，提示先完成 TDD
    └── 完成 → Step 2
    ↓
Step 2: 读取 test-plan.md + logic.md
    ↓
Step 3: 按模块补全边界测试（1 正向 + 2 异常）
    ↓
Step 4: 组织到 tests/unit/{模块}/ 目录
    ↓
Step 5: 执行 pytest --cov={模块} --cov-report=term-missing
    ├── 覆盖率 < 70% → 输出未覆盖清单，阻塞，返回 executing-plans
    └── 覆盖率 ≥ 70% → Step 6
    ↓
Step 6: 生成 coverage-report.md（含追溯矩阵）
    ↓
Step 7: 通过，解锁 integration-test
```

### 3.2 详细步骤

#### Step 1: 前置检查

- 读取 `tasks.md`，确认当前 Batch 所有任务已勾选
- 若存在未完成任务 → **终止**，向用户报告："请先完成当前 Batch 的 TDD 内循环"

#### Step 2: 读取设计文档

1. 读取 `feature-*/test-plan.md`，提取：
   - 测试场景（场景编号、描述、前置条件、步骤、预期结果）
   - 验收标准（AC-XXX）

2. 读取 `feature-*/logic.md`，提取：
   - 状态机定义（状态列表、转移条件、触发事件）
   - 边界条件（空值、越界、并发、超时）
   - 异常分支（权限不足、数据冲突、外部服务失败）

#### Step 3: 补全边界测试

**核心原则**：专注 TDD 遗漏的边界，不重复生成正向路径测试。

**生成规则**：
- 每个功能点：至少 1 个正向 + 2 个异常用例
- 异常状态机转移：网络中断、权限不足、数据为空、超时
- 输入边界：空值、越界、非法格式、并发输入
- 外部依赖：使用 mock / SQLite `:memory:`，禁止真实网络调用

**依赖隔离模板**：

```python
# conftest.py 示例
import pytest
from unittest.mock import Mock

@pytest.fixture
def mock_db():
    # SQLite :memory: 或 mock 连接
    ...

@pytest.fixture
def mock_redis():
    return Mock()

@pytest.fixture
def mock_http_client():
    client = Mock()
    client.request.return_value = {"status": "ok"}
    return client
```

#### Step 4: 组织测试代码

```
tests/unit/
├── user_service/
│   ├── test_register.py
│   ├── test_login.py
│   └── conftest.py
├── order_service/
│   ├── test_create_order.py
│   ├── test_cancel_order.py
│   └── conftest.py
```

**规范**：
- 按模块划分子目录
- 每个子目录一个 `conftest.py`
- 测试文件命名：`test_{功能}.py`

#### Step 5: 覆盖率门控

```bash
pytest tests/unit/ -v --cov={模块} --cov-report=term-missing
```

**门控逻辑**：

| 覆盖率 | 动作 |
|--------|------|
| ≥ 70% | 通过，继续 Step 6 |
| < 70% | **阻塞**，输出未覆盖行号清单，返回 executing-plans 补测试 |

**输出示例**：
```
---------- coverage: platform linux, python 3.11 ----------
Name                      Stmts   Miss  Cover   Missing
-------------------------------------------------------
src/user_service.py          45     12    73%   23-28, 45-50
src/order_service.py         60     25    58%   15-20, 35-45, 55-60
-------------------------------------------------------
TOTAL                       105     37    65%

覆盖率 65% < 70%，阻塞。未覆盖行号：23-28, 45-50, 15-20, 35-45, 55-60
```

#### Step 6: 生成覆盖率报告

保存 `tests/unit/coverage-report.md`：

```markdown
# 单元测试覆盖率报告

## 汇总
| 模块 | 覆盖率 | 状态 |
|------|--------|------|
| user_service | 73% | 通过 |
| order_service | 58% | 阻塞 |

## 未覆盖函数列表
- `src/order_service.py:15` `validate_discount()`
- `src/order_service.py:35` `apply_coupon()`

## 追溯矩阵（用例 ↔ 需求）
| 用例编号 | 需求编号 | 描述 | 状态 |
|----------|----------|------|------|
| TC-001 | FR-001 | 正常注册 | 通过 |
| TC-002 | FR-001 | 空用户名注册 | 通过 |
| TC-003 | FR-001 | 重复手机号注册 | 通过 |
```

---

## 4. 输入输出规格

### 4.1 输入

| 输入项 | 类型 | 来源 | 说明 |
|--------|------|------|------|
| 测试策略 | Markdown | `feature-*/test-plan.md` | 测试场景与验收标准 |
| 业务逻辑 | Markdown | `feature-*/logic.md` | 状态机与边界条件 |
| 源代码 | 源代码 | 项目源码目录 | 已完成的功能实现 |
| TDD 内联测试 | 测试代码 | `.kimi/temp-tests/` 或同级目录 | 参考已有正向测试 |
| 任务状态 | Markdown | `tasks.md` | 确认 Batch 已完成 |

### 4.2 输出

| 输出项 | 类型 | 路径 | 说明 |
|--------|------|------|------|
| 单元测试 | 测试代码 | `tests/unit/{模块}/test_*.py` | 按模块组织的测试用例 |
| Fixture | Python | `tests/unit/{模块}/conftest.py` | 模块级 mock / 内存数据库 |
| 覆盖率报告 | Markdown | `tests/unit/coverage-report.md` | 模块覆盖率、未覆盖清单、追溯矩阵 |

---

## 5. 硬约束详解

### 5.1 覆盖率 ≥ 70%

- **硬性门控**，不满足则阻塞下游 integration-test
- 输出未覆盖行号清单，精确到函数级别
- 允许用户手动放宽阈值（需明确同意并记录原因）

### 5.2 独立运行

- 禁止依赖外部服务：数据库、Redis、第三方 API
- 禁止使用真实网络调用
- 必须使用 mock 或内存替代方案

### 5.3 边界覆盖

必须包含以下类型：
- 错误路径：异常抛出、失败分支
- 空值/越界输入：`None`、空字符串、负数、超大值
- 并发输入：竞态条件、重复提交
- 外部服务异常：超时、降级、返回非预期格式

---

## 6. 与上下游衔接

| 衔接点 | 动作 |
|--------|------|
| 上游: executing-plans | Batch 完成后触发；TDD 已覆盖正向路径 |
| 上游: test-driven-development | 消费 TDD 产出的内联测试，避免重复生成正向用例 |
| 下游: integration-test | 输出 `coverage-report.md` 作为门控输入；覆盖率 < 70% 则阻塞 |

---

## 7. 风险与规避

| 风险 | 规避方法 |
|------|----------|
| 与 TDD 测试重复 | unit-test 专注边界补全；TDD 正向测试保留在临时目录，unit-test 统一去重整理 |
| 覆盖率门控被绕过 | 硬性约束：coverage-report.md 是 integration-test 的必需输入 |
| mock 不完整导致测试无效 | mock 数据结构必须包含真实 API 的所有字段 |
| 测试间状态污染 | 每个测试用例独立运行，使用 pytest fixture 隔离 |
| 真实外部依赖被引入 | 代码审查：禁止出现真实网络调用、真实数据库连接 |

---

## 8. 附录：测试阶段三 Skill 协作图

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
