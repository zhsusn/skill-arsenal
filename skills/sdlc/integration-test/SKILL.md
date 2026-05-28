---
name: integration-test
description: 当 unit-test 覆盖率 ≥70% 通过后、用户要求'集成测试'、'端到端测试'、'E2E'、'主链路验证'，或需要生成 UAT 检查清单时触发。
---

# Integration Test（集成测试）

## 适用场景

- unit-test 覆盖率 ≥ 70% 且 Self-Validation 通过后，验证端到端业务主链路
- 用户明确要求"集成测试"、"E2E 测试"、"主链路验证"
- 作为 Gate 3（UAT）的前置门控
- 需要生成 `user-stories-checklist.md` 供人工 UAT 使用

## 前置依赖

- `tests/unit/coverage-report.md` 中覆盖率 ≥ 70% 且 Self-Validation 通过
- `feature-*/spec.md`（功能规格与验收标准）
- `interface-contracts/openapi.yaml`（接口契约）
- 完整实现代码（前后端）
- `tests/unit/.idmap.json`（单元测试稳定 ID 映射，用于 ID 连续性）

## 策略预设（Policy）

根据项目合规要求选择策略：

| 维度 | `default`（默认，敏捷/内部项目） | `strict`（合规/监管/高可信项目） |
|------|----------------------------------|----------------------------------|
| 每个用户故事最少测试数 | 1 个主链路 | 2 个（正常 + 异常主链路） |
| 负向测试 | 建议包含关键异常 | 必须包含所有 P0 异常分支 |
| 稳定 ID | 建议使用 TEST-xxxx | 强制使用 TEST-xxxx |
| 追溯完整性 | 每个 TEST 标注 FR | 100% 双向追溯，TEST ↔ FR ↔ AC |
| 契约一致性审计 | 建议执行 | 强制执行，契约破裂即阻断 |
| E2E 范围 | 仅 Top 用户流 | 所有 P0 用户流 |
| 数据清理策略 | session 级 teardown | 每个用例独立清理 + 环境验证 |

策略通过 `openspec/config.yaml` 中的 `integration-test.policy` 配置，默认 `default`。

## 硬约束

| 约束 | 说明 |
|------|------|
| 主链路覆盖 | 必须覆盖所有 P0 用户故事的端到端流程 |
| 接口一致性 | 测试用例必须基于 openapi.yaml 中的契约定义 |
| 需求追溯 | 每个测试用例标注对应需求编号（如 FR-001）与稳定测试 ID（TEST-xxxx） |
| 环境自治 | 测试环境自动搭建与销毁，测试数据自动准备与清理 |
| 代码风格 | 测试代码必须遵循对应语言的代码风格（Python → `python-google-style`、Java → `java-alibaba-style`、其他语言使用默认风格） |
| 名称无关 | 禁止硬编码 openapi.yaml / spec.md 未明确规定的客户端类名、内部 URL 构造方式、DOM 选择器名称 |

## 执行流程

### Phase 0: 契约提取与策略选择

#### 0.1 读取并分类契约

读取 `feature-*/spec.md` 与 `interface-contracts/openapi.yaml`，提取显式契约：

**显式契约（MUST assert）**：
- OpenAPI 中明确定义的路径、方法、参数名、响应字段、状态码
- spec.md 中明确引用的组件名（如 `class 'PaymentGateway'`、`endpoint '/api/v1/orders'`）
- 用户故事中明确的状态转换与业务规则

**实现自由域（MUST NOT 硬编码）**：

| 类别 | 示例 | 测试中禁止的行为 |
|------|------|------------------|
| 客户端类名 | 使用 `httpx.AsyncClient` 或 `TestClient` | 断言具体客户端类型，除非 spec 明确规定 |
| 内部 URL 拼接 | `/api/v1/orders/${id}` | 硬编码字符串拼接，应使用 OpenAPI 生成的路由或契约引用 |
| DOM 选择器 | `page.locator("[data-testid='submit']")` | 硬编码选择器名称，除非 spec 明确指定 data-testid |
| 数据库表名 | 直接操作 `users` 表 | 绕过 API 直接操作数据库（strict 模式下绝对禁止） |
| 内部服务名 | 调用 `inventory_service.check()` | 绕过 API 契约直接调用内部服务 |

#### 0.2 选择策略

读取 `openspec/config.yaml` 中的 `integration-test.policy`，默认 `default`。

输出临时制品 `INTEGRATION_CONTRACTS.md`（仅用于推理）：

```markdown
## Explicit Contracts (from openapi.yaml + spec.md)
- C-I1: POST /api/v1/orders shall create an order with 201 and return OrderSchema
- C-I2: GET /api/v1/orders/{id} shall return 404 for non-existent ID
- C-I3: User registration flow shall send SMS verification within 30s

## Implementation Freedom
- HTTP client class: NOT SPECIFIED
- DOM selector strategy: NOT SPECIFIED (use text/role-based selectors preferred)
- Database access: NOT SPECIFIED (strict: prohibited; default: discouraged)
```

### Phase 1: 测试设计（设计先于执行）

1. 读取 `tests/unit/coverage-report.md`，确认覆盖率 ≥ 70% 且 Self-Validation 通过，否则拒绝执行
2. 读取 `feature-*/spec.md`，提取用户故事与验收标准（FR-XXX）
3. 读取 `interface-contracts/openapi.yaml`，提取接口路径、参数、响应结构
4. 读取 Phase 0 产出的 `INTEGRATION_CONTRACTS.md`
5. **强制输出测试设计文档**（不可跳过）：
   - 每个用户故事的测试步骤（基于契约，非实现）
   - 预期结果（通过/失败的二元定义）
   - 执行命令
   - 数据准备与清理策略
6. 自检：步骤是否可运行？断言是否明确？是否依赖实现自由域？

### Phase 2: 测试生成

按用户故事生成 `tests/integration/test_*.py`，遵循**名称无关**原则：

#### 2.1 后端链路：契约驱动测试

基于 `openapi.yaml` 契约生成测试，不硬编码内部 URL 或客户端类：

```python
# BAD: 硬编码 URL 和客户端类
from myapp import TestClient
def test_create_order():
    client = TestClient()
    resp = client.post("/api/v1/orders", json={"item": "book"})
    assert resp.status_code == 201

# GOOD: 基于 OpenAPI 契约的路径引用，使用通用 HTTP 客户端
def test_create_order_c_i1(http_client, base_url):
    """Covers C-I1 / FR-001: Create order via POST /api/v1/orders.
    Test-ID: TEST-0101
    Expected: 201 + OrderSchema with id, status='pending'.
    """
    resp = http_client.post(f"{base_url}/api/v1/orders", json={"item": "book"})
    assert resp.status_code == 201
    data = resp.json()
    assert "id" in data  # 契约规定字段，非实现细节
    assert data["status"] == "pending"
```

- 使用 TestClient（FastAPI）或 `httpx` 直接调用 API，但**禁止断言具体客户端类型**
- 每个测试文件顶部标注 `# FR-XXX / TEST-xxxx: {需求描述}` 追溯注释
- 包含 setup（建表 + 种子数据）与 teardown（清理）
- 使用 pytest 的 session 级 fixture 实现环境自治

#### 2.2 前端关键链路：行为驱动选择器

使用 Playwright 时，优先基于用户可见文本/ARIA 角色选择，避免硬编码 data-testid：

```python
# BAD: 硬编码 data-testid，属于实现自由域
page.locator("[data-testid='submit-button']").click()

# GOOD: 基于用户可见文本和 ARIA 角色，契约驱动
page.get_by_role("button", name="提交订单").click()
page.get_by_text("订单创建成功").wait_for()
```

仅当 spec.md / 设计文档**明确指定**了 `data-testid` 时才允许使用。

#### 2.3 稳定 ID 规则

集成测试 ID 从 `tests/unit/.idmap.json` 的 `next_test_id` 继续分配，确保单元测试与集成测试 ID 空间连续：
- 已有测试修改时**保留原 TEST-xxxx ID**
- 新增测试分配下一个可用 ID
- 更新 `tests/integration/.idmap.json`

#### 2.4 数据管理

测试数据与初始化脚本存放于 `tests/integration/fixtures/`：
- `seed_data.json` / `seed_data.sql`：主链路所需的最小数据集
- `cleanup.sql`：teardown 脚本
- 每个测试用例的数据隔离策略（default: session 级；strict: 用例级 + 验证）

### Phase 3: Self-Validation Gate（自检门控）

输出测试文件前回答：

1. **契约一致性**：每个测试用例中的请求参数、响应断言是否与 `openapi.yaml` 的 schema 一致？
   - 如果不一致 → 修正测试或标记契约破裂。
2. **名称无关性**：如果后端路由 handler 重命名、前端 DOM 选择器变更，测试是否仍能通过（只要契约不变）？
   - 如果否 → 移除硬编码名称，改为契约引用。
3. **盲写测试**：能否在不看实现代码、仅使用 `openapi.yaml` + `spec.md` 的情况下写出这些测试？
   - 如果否 → 测试包含实现细节，修正它。
4. **需求覆盖**：每个 FR-XXX 是否至少有一个 TEST-xxxx 覆盖？
   - 如果否 → 补充测试用例。

**未通过 Self-Validation Gate 的测试禁止提交。**

### Phase 4: 执行与审计

1. 执行集成测试
2. **Green Mirage Audit**（借鉴 auditing-green-mirage）：
   - 检查每个测试是否真的有断言（非空断言）
   - 检查是否过度 mock（mock 了被测对象本身）
   - 检查测试是否可能永远通过（如断言 `true === true`）
   - 输出审计报告：SOLID / GREEN MIRAGE 比例
3. **契约一致性校验**：测试用例中的请求参数、响应断言必须与 `openapi.yaml` 的 schema 一致；若接口变更导致契约破裂，测试失败并提示更新 `openapi.yaml`
4. **需求追溯验证**：每个 FR-XXX 至少有一个通过的 TEST-xxxx 覆盖
5. **名称无关审计**：扫描测试代码中是否存在硬编码的类名、方法名、DOM 选择器（白名单除外）

### Phase 5: 输出物与门控

1. 生成 `tests/integration/user-stories-checklist.md`（供 Gate 3 人工 UAT 使用）：

```markdown
# UAT 用户故事检查清单

| 需求编号 | 测试编号 | 用户故事 | 操作步骤 | 预期结果 | 集成测试状态 | UAT 勾选 |
|----------|----------|----------|----------|----------|--------------|----------|
| FR-001 | TEST-0101 | 作为用户，我可以注册账号 | 1. 打开预览环境注册页 2. 填写用户名/密码/手机号 3. 点击注册按钮 | 跳转到登录页，收到短信验证码 | 通过 | [ ] |
```

2. 生成集成测试报告 `tests/integration/report.md`，包含：
   - 测试通过率
   - 需求追溯矩阵（FR ↔ TEST ↔ 通过状态）
   - Green Mirage Audit 结果
   - 契约一致性结论
   - Self-Validation Gate 结果
   - 名称无关审计结果

3. 生成集中式追溯矩阵 `tests/TRACEABILITY.csv`（合并 unit + integration）：

```csv
REQ_ID,TEST_ID,TYPE,POLICY,STATUS
FR-001,TEST-0001,unit,default,PASS
FR-001,TEST-0101,integration,default,PASS
FR-002,TEST-0002,unit,default,PASS
FR-002,,integration,default,GAP
```

4. **门控**：
   - 全部 P0 用例通过 + 契约一致 + Self-Validation 通过 → 解锁 Gate 3（UAT）
   - 存在失败 → 输出失败分析 + 修复建议（可调用 systematic-debugging 模式）
   - strict 模式下存在追溯缺口（FR 无 TEST 覆盖）→ 阻断，要求补充测试

## 与上下游衔接

| 衔接点 | 动作 |
|--------|------|
| 上游: unit-test | 消费覆盖率报告与 `.idmap.json`；覆盖率 < 70% 或 Self-Validation 未通过则拒绝启动 |
| 上游: executing-plans | 消费实现代码与 `openapi.yaml` 契约 |
| 上游: detailed-design | 消费 `test-plan.md` 中的集成测试场景与契约定义 |
| 下游: code-review-pipeline | P0 用例全部通过后，触发变更级代码审查（阶段 9.25） |
| 下游: uat-verification | 生成 `user-stories-checklist.md` 供 Gate 3 人工 UAT 使用；P0 通过后解锁 uat-verification |
| 下游: human (Gate 3) | uat-verification 完成后进入 Gate 3 人工签字 |
| 横向: progress-tracker | 阶段 9 完成后更新进度 |
| 横向: self-check | 执行集成测试质量检查（Green Mirage Audit、契约一致性、名称无关审计） |
| 横向: systematic-debugging | 集成测试失败时可调用进行系统化调试 |

## Gotchas

- **覆盖率 < 70% 绝不开门**：unit-test 门控未通过时，integration-test 拒绝启动
- **Self-Validation 未通过禁止提交**：未通过 UUID 重命名/盲写/契约一致性检查的测试视为无效
- **设计文档不可跳过**：必须先输出完整测试设计（步骤、预期、命令），再执行测试
- **禁止混合多个用户故事**：一个测试用例应聚焦一个用户故事，避免混沌测试
- **禁止跳过前置条件**：每个测试必须确认环境状态（数据库、种子数据）后再执行
- **Playwright 仅用于前端关键链路**：非关键 UI 不强制使用 Playwright，避免过度工程化
- **契约破裂必须阻断**：接口实现与 `openapi.yaml` 不一致时，标记为 blocker 并停止
- **二元证据原则**：每个测试用例必须有明确的通过标准和失败标准，不允许"部分通过"
- **测试数据自动清理**：session 级 teardown 必须确保测试数据不污染后续环境（strict 模式要求用例级清理 + 验证）
- **需求文档没写的名称，测试一个字都不能写死**：`openapi.yaml` / `spec.md` 未明确引用的类名、方法名、DOM 选择器名称均视为实现自由域
- **稳定 ID 不可重排**：修改测试内容时保留原 TEST-xxxx ID，语义大变时才分配新 ID
- **strict 模式下追溯缺口即阻断**：任何无 TEST 覆盖的 FR 都必须补充测试或明确记录豁免理由
- **禁止直接操作数据库**：集成测试应通过 API 契约验证行为，strict 模式下直接 SQL 操作视为红线
