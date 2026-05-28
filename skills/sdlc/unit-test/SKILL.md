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
- `feature-*/spec.md`（功能规格与验收标准，用于契约提取）

## 策略预设（Policy）

根据项目合规要求选择策略，影响测试深度与追溯严格度：

| 维度 | `default`（默认，敏捷/内部项目） | `strict`（合规/监管/高可信项目） |
|------|----------------------------------|----------------------------------|
| 每个功能点最少测试数 | 1 正向 + 2 异常 | 2 正向 + 3 异常 |
| 负向测试 | 建议包含 | 必须包含 |
| 边界条件覆盖 | ≥2 个边界/功能点 | ≥4 个边界/功能点 |
| 稳定 ID | 建议使用 TEST-xxxx | 强制使用 TEST-xxxx |
| 追溯完整性 | 允许少量缺口 | 100% 覆盖，每个 TEST 必须映射到 REQ/FR |
| 契约一致性审计 | 建议执行 | 强制执行 |

策略通过 `openspec/config.yaml` 中的 `unit-test.policy` 配置，默认 `default`。

## 硬约束

| 约束 | 说明 |
|------|------|
| 覆盖率 ≥ 70% | 不满足则阻塞下游 integration-test |
| 独立运行 | 不依赖外部服务（数据库、缓存、第三方 API） |
| 内存数据库 | 使用 SQLite :memory: 或 mock 替代真实 DB |
| 边界覆盖 | 必须包含错误路径、异常分支、空值/越界输入 |
| 代码风格 | 测试代码必须遵循对应语言的代码风格（Python → `python-google-style`、Java → `java-alibaba-style`、其他语言使用默认风格） |
| 名称无关 | 禁止硬编码需求文档未明确规定的类名、方法名、变量名 |

## 执行流程

### Step 0: 契约提取（Contract Extraction）

读取 `feature-*/spec.md` 与 `feature-*/test-plan.md`，将需求分为两类：

**显式契约（MUST assert）**：
- 功能行为："系统应检测重复照片"
- 输入/输出类型："接受文件路径列表，返回重复项字典"
- 明确命名：**仅当** spec.md 使用引号明确写出时（如 `class 'PhotoManager'`、`method named 'process_files'`）
- 错误行为："路径无效时抛出异常"
- 边界条件："处理空列表"、"最多处理 10,000 条"

**实现自由域（MUST NOT 出现在测试中）**：

| 类别 | 示例 | 测试中禁止的行为 |
|------|------|------------------|
| 方法名 | "实现一个查找重复项的函数" | 调用 `obj.find_duplicates()` |
| 类名 | "创建一个整理照片的组件" | 直接实例化 `PhotoOrganizer()` |
| 参数名 | "接收 source 和 target 两个参数" | 在顺序未指定时使用位置参数 |
| 异常类型 | "会话无效时抛出错误" | 断言 `pytest.raises(ValueError)`，除非 spec 明确引用了类型 |
| 内部状态 | "维护缓存以提升性能" | 访问 `obj._cache` 或 `obj.__internal_map` |
| 算法选择 | "使用哈希比较检测重复" | 断言哈希值或特定算法步骤 |

输出临时制品 `CONTRACTS.md`（仅用于推理，不提交）：

```markdown
## Explicit Contracts
- C1: System shall detect duplicate items in a collection
- C2: System shall support rollback of session state

## Implementation Freedom
- Method names: NOT SPECIFIED
- Class names: NOT SPECIFIED
- Exception types: NOT SPECIFIED
- Internal data structures: NOT SPECIFIED
```

### Step 1: 前置检查

确认当前 Batch 的 TDD 内循环已完成：
- 读取 `tasks.md`，检查当前 Batch 的所有任务已勾选
- 若存在未完成任务，终止并提示先完成 TDD

### Step 2: 读取设计文档

1. 读取 `feature-*/test-plan.md`，提取测试场景与验收标准
2. 读取 `feature-*/logic.md`，识别状态机与边界条件
3. 读取 Step 0 产出的 `CONTRACTS.md`，确认显式契约清单

### Step 3: 生成名称无关的边界测试（TDD 遗漏补全）

针对每个模块生成测试，**重点补全 TDD 未覆盖的边界**。生成时必须遵循**名称无关原则**：

#### 3.1 边界覆盖清单

- 异常状态机转移（如网络中断、权限不足、数据为空）
- 空值 / 越界 / 并发输入
- 外部服务超时 / 降级场景
- 每个功能点（default：1 正向 + 2 异常；strict：2 正向 + 3 异常）

#### 3.2 名称无关测试模式（Mandatory Patterns）

**Pattern A: 工厂入口点（Factory Entry Point）**

当 spec.md 描述了模块或组件但未命名类时，禁止直接硬编码类名：

```python
# BAD: 硬编码实现中的类名
from photo_organizer import PhotoOrganizer
def test_find_duplicates():
    org = PhotoOrganizer()
    result = org.find_duplicates([...])

# GOOD: 使用工厂或公共入口点，不依赖名称
def test_detects_duplicates(create_processor):
    """Covers C1: detect duplicate items. Name-agnostic."""
    processor = create_processor()  # 工厂由 conftest.py 或测试头定义
    result = processor.process(["a.jpg", "b.jpg", "a.jpg"])
    assert "a.jpg" in result  # 行为断言
```

**Pattern B: 行为断言优先（Behavior-State Assertion）**

断言外部可观察的行为，而非内部方法调用：

```python
# BAD: 假设 resume 方法名和内部状态
session.resume()
assert session._active is True

# GOOD: 断言可观察行为
session.process("resume")  # 或通过工厂调用
assert session.is_active()  # 公共状态查询
```

**Pattern C: 异常无关错误测试（Exception-Agnostic Error Testing）**

当 spec.md 只说"抛出错误"而未指定类型时：

```python
# BAD: 假设特定异常类型
with pytest.raises(RuntimeError):
    session.resume()

# GOOD: 任何异常均可接受；断言错误后的安全状态
with pytest.raises(Exception):
    session.process("resume")
assert not session.is_active()  # 系统仍处于安全状态
```

**Pattern D: 需求可追溯（Requirement Traceability）**

每个测试 docstring 必须映射到契约编号或需求编号：

```python
def test_detects_duplicate_photos(create_processor):
    """Covers C1 / REQ-0001: System shall detect duplicate items.

    Scenario: Two files with identical content hashes.
    Expected: Both file paths appear in the duplicate report.
    Test-ID: TEST-0001
    """
```

#### 3.3 稳定 ID 规则

测试用例使用稳定 ID（`TEST-xxxx`），规则如下：
- 基于测试内容指纹生成内部 ID，映射到 `TEST-xxxx`
- 已有测试用例修改时**保留原 ID**，除非语义发生实质性变化
- 新增测试分配下一个可用 ID
- ID 映射持久化到 `tests/unit/.idmap.json`（建议提交到版本控制）

```json
{
  "tests": {
    "a1b2c3d4": "TEST-0001",
    "e5f6g7h8": "TEST-0002"
  },
  "next_test_id": 3
}
```

#### 3.4 依赖隔离规范

- DB 连接：使用 `unittest.mock` 或 `pytest-mock` 替换，或使用 SQLite `:memory:`
- Redis / 缓存：统一 mock
- HTTP 客户端：禁止测试用例中出现真实网络调用
- 外部服务：使用 fixture 自动注入 mock
- mock 数据结构必须包含真实 API 的所有字段，禁止部分 mock

### Step 4: Self-Validation Gate（自检门控）

输出测试文件前，必须回答以下问题：

1. **UUID 重命名测试**：如果将实现中的每个方法和类重命名为随机 UUID，这些测试是否仍能编译和运行？
   - 如果否 → 存在硬编码名称，修正它。
2. **盲写测试**：能否在不看实现代码、仅使用 spec.md / test-plan.md 的情况下写出这些测试？
   - 如果否 → 测试包含实现细节，修正它。
3. **失败含义测试**：当测试失败时，是否明确意味着"行为错误"而非"命名不同"？
   - 如果否 → 过度指定，修正它。
4. **契约覆盖测试**：每个显式契约（C1, C2...）是否至少有一个 TEST 覆盖？
   - 如果否 → 补充测试用例。

**未通过 Self-Validation Gate 的测试禁止提交。**

### Step 5: 组织测试代码

按模块统一组织到 `tests/unit/{模块}/` 目录：

```
tests/unit/
├── {module}/
│   ├── test_*.py          # 测试用例（含稳定 ID 注释）
│   └── conftest.py        # 模块级 fixture（含工厂定义）
```

若 `instruction.md` / `spec.md` 未定义工厂，在 `conftest.py` 或测试文件头部生成：

```python
import importlib
import pytest

@pytest.fixture
def create_processor():
    """Discovers the entry point without hardcoding its name."""
    module = importlib.import_module("photo_organizer")
    entry = getattr(module, "create_organizer", None) or \
            getattr(module, "main", None) or \
            getattr(module, "process", None)
    if entry is None:
        for name in dir(module):
            obj = getattr(module, name)
            if callable(obj) and not name.startswith("_"):
                return obj
    return entry
```

### Step 6: 执行测试与覆盖率门控

```bash
pytest tests/unit/ -v --cov={模块} --cov-report=term-missing
```

**门控逻辑：**
- 覆盖率 ≥ 70%：通过，继续 Step 7
- 覆盖率 < 70%：输出未覆盖行号清单，**阻塞流程**，返回 executing-plans 补 TDD 或补边界测试

### Step 7: 生成测试审计报告

保存 `tests/unit/coverage-report.md`，包含：

```markdown
# 单元测试审计报告

## 汇总
| 模块 | 覆盖率 | Self-Validation | 状态 |
|------|--------|-----------------|------|
| {module} | {cov}% | 通过/未通过 | 通过/阻塞 |

## 未覆盖函数列表
- `{file}:{line}` `{function}`

## 追溯矩阵（TEST ↔ REQ/FR）
| 测试编号 | 需求编号 | 契约编号 | 描述 | 状态 |
|----------|----------|----------|------|------|
| TEST-0001 | FR-001 | C1 | 检测重复项正向路径 | 通过 |
| TEST-0002 | FR-001 | C1 | 空输入边界 | 通过 |

## 契约覆盖审计
- [x] C1: 已覆盖（TEST-0001, TEST-0002）
- [ ] C2: 未覆盖 → 阻塞原因

## 名称无关审计
- [x] 无硬编码类名
- [x] 无硬编码方法名
- [x] 无内部状态断言
```

## 与上下游衔接

| 衔接点 | 动作 |
|--------|------|
| 上游: executing-plans | Batch 完成后触发；TDD 已覆盖正向路径 |
| 上游: detailed-design | 消费 `test-plan.md` 中的测试策略与契约定义 |
| 下游: integration-test | 输出 `coverage-report.md` 作为门控输入；覆盖率 < 70% 或 Self-Validation 未通过则阻塞 |
| 横向: self-check | 验证契约覆盖完整性与追溯一致性 |

## Gotchas

- **禁止跳过覆盖率门控**：覆盖率 < 70% 时绝不允许进入 integration-test
- **禁止跳过 Self-Validation**：未通过 UUID 重命名/盲写/失败含义检查的测试视为无效测试
- **专注边界补全**：不要重复生成 TDD 已覆盖的正向路径测试，避免冗余
- **Mock 必须完整**：mock 数据结构必须包含真实 API 的所有字段，禁止部分 mock
- **测试必须独立**：每个测试用例可独立运行，禁止测试间状态污染
- **不得引入真实外部依赖**：任何真实网络调用、真实数据库连接均为红线
- **未覆盖清单必须精确到行号**：覆盖率报告需输出具体未覆盖的行号范围，便于快速定位
- **与 test-plan 的追溯一致性**：自检时检查每个验收标准是否至少有一个测试用例覆盖
- **需求文档没写的名称，测试一个字都不能写死**：若 spec.md 未明确引用类名/方法名，测试必须通过工厂或行为痕迹调用
- **异常类型未明确时禁止过度断言**：spec.md 只说"抛出错误"时，使用 `pytest.raises(Exception)` 而非假设具体类型
- **稳定 ID 不可重排**：修改测试内容时保留原 TEST-xxxx ID，语义大变时才分配新 ID
