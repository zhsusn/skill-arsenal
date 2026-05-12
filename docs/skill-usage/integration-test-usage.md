# Integration Test Skill 使用手册

> 本文档面向 Skill 使用者，提供 integration-test 的触发方式、四阶段流水线操作指南、UAT 清单解读与常见问题。
>
> 版本: 1.0.0

---

## 1. 快速开始

### 1.1 什么是 Integration Test？

`integration-test` 是**端到端主链路验证器**。它在 unit-test 通过后，按用户故事生成端到端测试，覆盖前端 → API → DB 的完整调用链，并产出供人工 UAT 使用的检查清单。

**核心原则**：先设计后执行，每个测试必须有明确的通过/失败标准。

### 1.2 触发方式

| 方式 | 说明 |
|------|------|
| 自动触发 | unit-test 覆盖率 ≥70% 通过后自动调用 |
| 手动触发 | 用户明确要求"集成测试"、"E2E 测试"、"主链路验证" |
| 阻塞恢复 | 失败后修复，重新触发 |

---

## 2. 使用步骤

### Step 1: 确认前置条件

integration-test 需要以下输入：
- ✅ `tests/unit/coverage-report.md`（覆盖率 ≥ 70%）
- ✅ `feature-*/spec.md`（用户故事与验收标准）
- ✅ `interface-contracts/openapi.yaml`（接口契约）
- ✅ 完整实现代码（前后端）

**如果覆盖率 < 70%**：integration-test 会拒绝执行并提示："请先完成单元测试。"

### Step 2: Phase 1 - 测试设计（设计先于执行）

**强制输出测试设计文档**，不可跳过。

integration-test 自动读取 `spec.md` 和 `openapi.yaml`，然后输出：

```markdown
## 集成测试设计文档

### 用户故事 FR-001: 用户注册
**步骤**：
1. POST /api/v1/register（用户名、密码、手机号）
2. 验证响应 201
3. 查询数据库确认用户存在
4. 验证短信验证码已发送

**预期结果**：
- 通过：HTTP 201 + 数据库记录 + 短信服务调用 1 次
- 失败：HTTP 非 201 或数据库无记录或短信服务未调用
```

**自检**：步骤是否可运行？断言是否明确？

### Step 3: Phase 2 - 测试生成

按用户故事生成 `tests/integration/test_*.py`：

**技术栈自动选择**：
- 后端 API：TestClient（FastAPI）或 `httpx`
- 前端关键链路：Playwright（仅核心流程）

**生成规则**：
- 每个用户故事至少 1 个正向 + 1 个异常
- 文件顶部标注：`# FR-001: 用户注册`
- 包含 setup（建表 + 种子数据）与 teardown（清理）

**目录结构**：
```
tests/integration/
├── test_user_registration.py
├── test_order_creation.py
└── fixtures/
    ├── seed_data.sql
    └── setup_teardown.py
```

### Step 4: Phase 3 - 执行与审计

#### 4.1 执行集成测试
```bash
pytest tests/integration/ -v
```

#### 4.2 Green Mirage Audit

自动检查测试有效性：

| 检查项 | 说明 |
|--------|------|
| 空断言 | `assert True` 等无实质检查 → 要求补充 |
| 过度 mock | mock 了被测对象本身 → 要求调整层级 |
| 永真测试 | `assert 1 == 1` → 要求重写 |

**审计结果**：输出 SOLID / MIRAGE 比例。

#### 4.3 需求追溯验证
- 检查每个 FR-XXX 至少有一个通过的测试
- 输出追溯矩阵

#### 4.4 接口契约一致性
- 将测试中的请求/响应与 `openapi.yaml` 对比
- 不一致 → 测试失败，提示更新契约

### Step 5: Phase 4 - 生成 UAT 清单与门控

#### 5.1 生成 user-stories-checklist.md

```markdown
# UAT 用户故事检查清单

| 需求编号 | 用户故事 | 操作步骤 | 预期结果 | 集成测试状态 | UAT 勾选 |
|----------|----------|----------|----------|--------------|----------|
| FR-001 | 作为用户，我可以注册账号 | 1. 打开注册页 2. 填写... | 跳转到登录页 | 通过 | [ ] |
```

#### 5.2 门控结果

| 结果 | 说明 |
|------|------|
| 通过 | 全部 P0 用例通过 + 契约一致 → 解锁 Gate 3（人工 UAT） |
| 失败 | 输出失败分析 + 修复建议，可调用 systematic-debugging |

---

## 3. 输出解读

### 3.1 集成测试报告

```markdown
# 集成测试报告

## 测试通过率
| 用户故事 | 测试文件 | 状态 |
|----------|----------|------|
| FR-001 | test_user_registration.py | 通过 |
| FR-002 | test_order_creation.py | 失败 |

## 需求追溯矩阵
| 需求编号 | 测试文件 | 通过状态 |
|----------|----------|----------|
| FR-001 | test_user_registration.py | 通过 |
| FR-002 | test_order_creation.py | 失败 |

## Green Mirage Audit
SOLID: 4, MIRAGE: 1
- test_order_creation.py:45 空断言

## 接口契约一致性
- 通过：FR-001, FR-003
- 失败：FR-002（请求参数 `discount` 与 openapi.yaml 不一致）
```

### 3.2 user-stories-checklist.md

此文件直接用于 Gate 3 人工 UAT：
- 测试人员按"操作步骤"手动执行
- 对比"预期结果"
- 在"UAT 勾选"列标记 [x] 或 [ ]

---

## 4. 执行纪律速查

### 4.1 设计先于执行

- **禁止**跳过测试设计文档直接写代码
- 必须先输出完整测试设计（步骤、预期、命令）
- 自检通过后才能进入 Phase 2

### 4.2 用户故事聚焦

- 一个测试用例聚焦一个用户故事
- 禁止混合多个用户故事
- 禁止跳过前置条件

### 4.3 Playwright 使用范围

- **仅前端关键链路**使用 Playwright（如注册、支付）
- 非关键 UI 不强制使用 Playwright
- 后端链路优先使用 TestClient / httpx

---

## 5. 常见问题

### Q1：unit-test 覆盖率 65%，可以跑集成测试吗？

**不可以。** 70% 是硬性前置门控。integration-test 会读取 `coverage-report.md`，未达标直接拒绝。

### Q2：测试设计文档可以跳过吗？

**不可以。** "设计先于执行"是借鉴 spellbook isolated-testing 的核心纪律。跳过设计 = 混沌测试。

### Q3：接口实现和 openapi.yaml 不一致怎么办？

1. 如果接口实现是正确的 → 更新 `openapi.yaml`
2. 如果 openapi.yaml 是正确的 → 修正接口实现
3. **禁止**在契约不一致的情况下继续测试

### Q4：Green Mirage 是什么意思？

来自 spellbook `auditing-green-mirage`：测试通过了，但证明不了任何东西。常见形式：
- 空断言（`assert response`）
- 过度 mock（mock 了被测对象）
- 永真测试（`assert True`）

### Q5：user-stories-checklist.md 怎么用？

交给测试/产品经理，按以下步骤执行：
1. 按"操作步骤"在系统上手动操作
2. 观察实际结果是否与"预期结果"一致
3. 一致 → 勾选 [x]；不一致 → 标记 [ ] 并记录缺陷

### Q6：集成测试失败了怎么调试？

1. 查看集成测试报告中的失败详情
2. 检查是否接口契约不一致
3. 检查是否环境/数据问题
4. 可调用 `systematic-debugging` Skill 进行系统化调试

### Q7：测试数据会污染正式环境吗？

**不会。** integration-test 使用独立的测试数据库，session 级 teardown 自动清理。

---

## 6. 速查卡

```text
触发：unit-test ≥70% 后自动调用 / 用户要求"集成测试""E2E"
输入：coverage-report.md + spec.md + openapi.yaml + 完整代码
输出：tests/integration/ + user-stories-checklist.md + 集成测试报告
原则：设计先于执行、主链路覆盖、需求追溯、环境自治
流程：Phase 1 设计 → Phase 2 生成 → Phase 3 执行审计 → Phase 4 门控
审计：Green Mirage Audit（空断言/过度 mock/永真测试）
门控：P0 通过 + 契约一致 → 解锁 Gate 3 (UAT)
纪律：禁止跳过设计、禁止混合用户故事、Playwright 仅关键链路
禁止：覆盖率 <70% 时执行、跳过前置条件、契约破裂继续
```
