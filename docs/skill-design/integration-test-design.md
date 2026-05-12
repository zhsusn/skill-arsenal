# Integration Test Skill 设计规格书

> 本文档面向 Skill 实现者与维护者，描述 `integration-test` 的完整技术架构、端到端测试生成策略、Green Mirage Audit 机制及与 unit-test / UAT 的衔接协议。
>
> 版本: 1.0.0

---

## 1. 功能定位

| 维度 | 说明 |
|------|------|
| **核心职责** | 生成并执行端到端集成测试，覆盖主链路业务场景，验证模块间协作与接口契约一致性，产出 UAT 检查清单 |
| **所处阶段** | 测试阶段（阶段 9），前置依赖 unit-test（覆盖率 ≥ 70%），被 UAT / Gate 3 依赖 |
| **上游输入** | `feature-*/spec.md`、`interface-contracts/openapi.yaml`、完整实现代码、`tests/unit/coverage-report.md` |
| **下游输出** | `tests/integration/test_*.py`、`tests/integration/fixtures/`、`tests/integration/user-stories-checklist.md`、集成测试报告 |
| **设计模式** | `pipeline`（多步骤流水线） |
| **开源对标** | spellbook `isolated-testing`（设计先于执行纪律）、`auditing-green-mirage`（测试有效性审计）、`develop` Verification 阶段（双层验证） |

---

## 2. 总体架构

```
┌─────────────────────────────────────────────────────────────┐
│                  integration-test Skill                      │
├─────────────────────────────────────────────────────────────┤
│  触发方式：unit-test 覆盖率 ≥70% 通过后自动调用               │
│  执行模式：四阶段流水线（设计→生成→执行审计→门控）            │
│  架构模式：读取设计文档 → 推导端到端用例 → 执行审计 → 输出 UAT │
│  核心约束：主链路覆盖、接口一致性、需求追溯、环境自治           │
└─────────────────────────────────────────────────────────────┘
```

### 2.1 开源借鉴分析

| 能力 | 来源 | 融入方式 |
|------|------|----------|
| 设计先于执行 | spellbook `isolated-testing` Step 2 | Phase 1 强制输出测试设计文档，不可跳过 |
| 二元证据理念 | spellbook `isolated-testing` | 每个用例明确通过/失败标准，不允许"部分通过" |
| 混沌检测 | spellbook `isolated-testing` | 检查跳过前置条件、混合用户故事、未确认环境状态 |
| Green Mirage Audit | spellbook `auditing-green-mirage` | Phase 3 子步骤：检查空断言、过度 mock、永真测试 |
| 双层验证 | spellbook `develop` Verification | Phase 3：第一层运行套件，第二层逐条验证测试结果是否等于业务正确 |
| Quality Gates | spellbook 通用设计 | 作为 unit-test 和 UAT 之间的强制门控 |

---

## 3. 处理逻辑

### 3.1 四阶段流水线

```
Phase 1: 测试设计（设计先于执行）
    ├── 读取 coverage-report.md（≥70% 门控）
    ├── 读取 spec.md 提取用户故事（FR-XXX）
    ├── 读取 openapi.yaml 提取接口契约
    ├── 强制输出测试设计文档
    └── 自检：步骤可运行？断言明确？
    ↓
Phase 2: 测试生成
    ├── 按用户故事生成 tests/integration/test_*.py
    ├── 标注 # FR-XXX 追溯注释
    ├── 生成 user-stories-checklist.md
    └── 准备 fixtures/（种子数据 + 初始化脚本）
    ↓
Phase 3: 执行与审计
    ├── 执行集成测试
    ├── Green Mirage Audit
    ├── 需求追溯验证（FR-XXX 全覆盖？）
    └── 接口契约一致性校验
    ↓
Phase 4: 门控与输出
    ├── P0 通过 + 契约一致 → 解锁 Gate 3
    └── 存在失败 → 失败分析 + 修复建议
```

### 3.2 详细步骤

#### Phase 1: 测试设计（设计先于执行）

**前置检查**：
- 读取 `tests/unit/coverage-report.md`
- 确认覆盖率 ≥ 70%，否则**拒绝执行**并提示："请先完成单元测试，覆盖率需 ≥ 70%"

**文档提取**：
1. `feature-*/spec.md`：提取用户故事（格式 `FR-XXX: {描述}`）与验收标准
2. `interface-contracts/openapi.yaml`：提取接口路径、HTTP 方法、参数 schema、响应结构

**强制输出测试设计文档**：

```markdown
## 集成测试设计文档

### 用户故事 FR-001: 用户注册
**步骤**：
1. POST /api/v1/register（用户名、密码、手机号）
2. 验证响应 201
3. 查询数据库确认用户存在
4. 验证短信验证码已发送

**预期结果（二元定义）**：
- 通过：HTTP 201 + 数据库记录 + 短信服务调用 1 次
- 失败：HTTP 非 201 或数据库无记录或短信服务未调用

**执行命令**：
pytest tests/integration/test_user_registration.py -v
```

**自检问题**：
- 步骤是否可独立运行？
- 断言是否明确、可量化？
- 是否存在模糊的预期（如"应该正常"）？

#### Phase 2: 测试生成

**技术栈选择**（根据 `config.yaml` 的 `tech_stack` 自动判断）：

| 链路类型 | 技术方案 | 适用场景 |
|----------|----------|----------|
| 后端 API | TestClient（FastAPI）或 httpx | 所有后端接口验证 |
| 前端关键链路 | Playwright | 用户注册、下单支付等核心流程 |

**生成规则**：
- 每个用户故事至少 1 个正向流程 + 1 个异常分支（权限不足、数据冲突）
- 每个测试文件顶部标注追溯注释：`# FR-XXX: {需求描述}`
- 使用 pytest session 级 fixture 实现环境自治

**目录结构**：
```
tests/integration/
├── test_user_registration.py   # FR-001
├── test_order_creation.py      # FR-002
├── test_payment_flow.py        # FR-003
└── fixtures/
    ├── seed_data.sql
    └── setup_teardown.py
```

**Setup/Teardown 模板**：
```python
@pytest.fixture(scope="session", autouse=True)
def integration_setup():
    # 创建测试数据库
    # 运行迁移
    # 注入种子数据
    yield
    # 清理测试数据
    # 删除测试数据库
```

#### Phase 3: 执行与审计

**3.1 执行集成测试**
```bash
pytest tests/integration/ -v
```

**3.2 Green Mirage Audit**

借鉴 spellbook `auditing-green-mirage`，检查：

| 审计项 | 检查内容 | 失败处理 |
|--------|----------|----------|
| 空断言 | `assert True`、`assert response` 等无实质检查 | 标记为 MIRAGE，要求补充具体断言 |
| 过度 mock | mock 了被测对象本身（而非外部依赖） | 标记为 MIRAGE，要求调整 mock 层级 |
| 永真测试 | 断言恒成立（如 `assert 1 == 1`） | 标记为 MIRAGE，要求重写测试 |
| 无需求覆盖 | 测试存在但未标注 FR-XXX | 要求补充追溯注释 |

**审计报告格式**：
```markdown
## Green Mirage Audit 报告

| 测试文件 | 状态 | 问题 |
|----------|------|------|
| test_user_registration.py | SOLID | — |
| test_order_creation.py | MIRAGE | 空断言：第 45 行 |

**SOLID / MIRAGE 比例**: 4:1
```

**3.3 需求追溯验证**
- 检查每个 FR-XXX 至少有一个通过的测试覆盖
- 输出追溯矩阵：需求编号 ↔ 测试文件 ↔ 通过状态

**3.4 接口契约一致性校验**
- 将测试中的请求参数、响应断言与 `openapi.yaml` 的 schema 对比
- 不一致时：**测试失败**，提示更新 `openapi.yaml` 或修正实现

#### Phase 4: 输出物与门控

**生成 user-stories-checklist.md**（供 Gate 3 人工 UAT）：

```markdown
# UAT 用户故事检查清单

| 需求编号 | 用户故事 | 操作步骤 | 预期结果 | 集成测试状态 | UAT 勾选 |
|----------|----------|----------|----------|--------------|----------|
| FR-001 | 作为用户，我可以注册账号 | 1. 打开注册页 2. 填写用户名/密码/手机号 3. 点击注册 | 跳转到登录页，收到短信验证码 | 通过 | [ ] |
| FR-002 | 作为用户，我可以下单购买商品 | 1. 登录 2. 浏览商品 3. 加入购物车 4. 结算 | 生成订单，扣减库存 | 通过 | [ ] |
```

**门控逻辑**：

| 条件 | 结果 |
|------|------|
| 全部 P0 用例通过 + 契约一致 + Green Mirage Audit 通过 | 解锁 Gate 3（UAT） |
| 存在失败 | 输出失败分析 + 修复建议，可调用 systematic-debugging |

---

## 4. 输入输出规格

### 4.1 输入

| 输入项 | 类型 | 来源 | 说明 |
|--------|------|------|------|
| 覆盖率报告 | Markdown | `tests/unit/coverage-report.md` | 门控基准（≥70%） |
| 功能规格 | Markdown | `feature-*/spec.md` | 用户故事与验收标准 |
| 接口契约 | YAML | `interface-contracts/openapi.yaml` | 接口路径、参数、响应 schema |
| 完整代码 | 源代码 | 项目源码目录 | 前后端实现 |
| 技术栈配置 | YAML | `config.yaml` | 决定 TestClient / Playwright |

### 4.2 输出

| 输出项 | 类型 | 路径 | 说明 |
|--------|------|------|------|
| 集成测试 | 测试代码 | `tests/integration/test_*.py` | 端到端测试用例 |
| 测试数据 | SQL/Python | `tests/integration/fixtures/` | 种子数据与初始化脚本 |
| UAT 清单 | Markdown | `tests/integration/user-stories-checklist.md` | 人工 UAT 操作步骤与勾选框 |
| 集成测试报告 | Markdown | 对话内联 / `tests/integration/report.md` | 通过率、追溯矩阵、审计结果 |

---

## 5. 硬约束详解

### 5.1 主链路覆盖

- 必须覆盖所有 P0 用户故事的端到端流程
- P0 定义：系统不可用则业务无法运转的核心流程
- 每个 P0 用户故事至少 1 个正向 + 1 个异常测试

### 5.2 接口一致性

- 测试用例的请求参数必须与 `openapi.yaml` 的 schema 一致
- 响应断言必须与 `openapi.yaml` 定义的响应结构一致
- 契约破裂 → 测试失败，提示更新 `openapi.yaml`

### 5.3 需求追溯

- 每个测试文件顶部必须标注 `# FR-XXX: {需求描述}`
- 报告中必须输出追溯矩阵
- 每个 FR-XXX 至少有一个通过的测试覆盖

### 5.4 环境自治

- 测试环境自动搭建（创建测试数据库、运行迁移）
- 种子数据自动注入
- 测试完成后自动清理（删除数据、关闭连接）
- 使用 pytest session 级 fixture 实现

---

## 6. 与上下游衔接

| 衔接点 | 动作 |
|--------|------|
| 上游: unit-test | 读取 `coverage-report.md` 作为门控；覆盖率 < 70% 拒绝执行 |
| 下游: human (Gate 3) | 输出 `user-stories-checklist.md` 供人工 UAT 走查 |
| 横向: systematic-debugging | 集成测试失败时可调用进行系统化调试 |

---

## 7. 风险与规避

| 风险 | 规避方法 |
|------|----------|
| 覆盖率 < 70% 时强行执行 | 硬性前置检查：未通过 unit-test 门控直接拒绝 |
| 设计文档被跳过 | Phase 1 强制输出测试设计文档，不可跳过 |
| 测试混合多个用户故事 | 混沌检测：一个测试用例聚焦一个用户故事 |
| 前置条件被跳过 | 每个测试必须确认环境状态后再执行 |
| Playwright 过度使用 | 仅前端关键链路使用 Playwright，非关键 UI 不强制 |
| 契约破裂未被发现 | Phase 3.4 接口契约一致性校验，破裂即 blocker |
| 测试数据污染 | session 级 teardown 必须清理测试数据 |

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
