---
name: integration-test
description: 当 unit-test 覆盖率 ≥70% 通过后、用户要求'集成测试'、'端到端测试'、'E2E'、'主链路验证'，或需要生成 UAT 检查清单时触发。
---

# Integration Test（集成测试）

## 适用场景

- unit-test 覆盖率 ≥ 70% 通过后，验证端到端业务主链路
- 用户明确要求"集成测试"、"E2E 测试"、"主链路验证"
- 作为 Gate 3（UAT）的前置门控
- 需要生成 `user-stories-checklist.md` 供人工 UAT 使用

## 前置依赖

- `tests/unit/coverage-report.md` 中覆盖率 ≥ 70%
- `feature-*/spec.md`（功能规格与验收标准）
- `interface-contracts/openapi.yaml`（接口契约）
- 完整实现代码（前后端）

## 硬约束

| 约束 | 说明 |
|------|------|
| 主链路覆盖 | 必须覆盖所有 P0 用户故事的端到端流程 |
| 接口一致性 | 测试用例必须基于 openapi.yaml 中的契约定义 |
| 需求追溯 | 每个测试用例标注对应需求编号（如 FR-001） |
| 环境自治 | 测试环境自动搭建与销毁，测试数据自动准备与清理 |

## 执行流程

### Phase 1: 测试设计（设计先于执行）

1. 读取 `tests/unit/coverage-report.md`，确认覆盖率 ≥ 70%，否则拒绝执行并提示先完成单元测试
2. 读取 `feature-*/spec.md`，提取用户故事与验收标准（FR-XXX）
3. 读取 `interface-contracts/openapi.yaml`，提取接口路径、参数、响应结构
4. **强制输出测试设计文档**（不可跳过）：
   - 每个用户故事的测试步骤
   - 预期结果（通过/失败的二元定义）
   - 执行命令
5. 自检：步骤是否可运行？断言是否明确？

### Phase 2: 测试生成

按用户故事生成 `tests/integration/test_*.py`：

- 后端链路：使用 TestClient（FastAPI）或 `httpx` 直接调用 API
- 前端关键链路：使用 Playwright（参考 currents-dev/testdino 最佳实践）
- 每个测试文件顶部标注 `# FR-XXX: {需求描述}` 追溯注释
- 包含 setup（建表 + 种子数据）与 teardown（清理）
- 使用 pytest 的 session 级 fixture 实现环境自治

测试数据与初始化脚本存放于 `tests/integration/fixtures/`。

### Phase 3: 执行与审计

6. 执行集成测试
7. **Green Mirage Audit**（借鉴 auditing-green-mirage）：
   - 检查每个测试是否真的有断言（非空断言）
   - 检查是否过度 mock（mock 了被测对象本身）
   - 检查测试是否可能永远通过（如断言 `true === true`）
   - 输出审计报告：SOLID / GREEN MIRAGE 比例
8. 需求追溯验证：每个 FR-XXX 至少有一个通过的测试覆盖
9. 接口契约一致性校验：测试用例中的请求参数、响应断言必须与 openapi.yaml 的 schema 一致；若接口变更导致契约破裂，测试失败并提示更新 openapi.yaml

### Phase 4: 输出物与门控

10. 生成 `tests/integration/user-stories-checklist.md`（供 Gate 3 人工 UAT 使用）：

```markdown
# UAT 用户故事检查清单

| 需求编号 | 用户故事 | 操作步骤 | 预期结果 | 集成测试状态 | UAT 勾选 |
|----------|----------|----------|----------|--------------|----------|
| FR-001 | 作为用户，我可以注册账号 | 1. 打开注册页 2. 填写... | 跳转到登录页 | 通过 | [ ] |
```

11. 生成集成测试报告，包含：
    - 测试通过率
    - 需求追溯矩阵（需求编号 ↔ 测试文件 ↔ 通过状态）
    - Green Mirage Audit 结果
    - 接口契约一致性结论

12. **门控**：
    - 全部 P0 用例通过 + 契约一致 → 解锁 Gate 3（UAT）
    - 存在失败 → 输出失败分析 + 修复建议（可调用 systematic-debugging 模式）

## 与上下游衔接

| 衔接点 | 动作 |
|--------|------|
| 上游: unit-test | 读取 `coverage-report.md` 作为门控；覆盖率 < 70% 拒绝执行 |
| 下游: uat-verification | 输出 `user-stories-checklist.md` 供 UAT 验证阶段使用；P0 通过后解锁 uat-verification |
| 下游: human (Gate 3) | uat-verification 完成后进入 Gate 3 人工签字 |
| 横向: systematic-debugging | 集成测试失败时可调用进行系统化调试 |

## Gotchas

- **覆盖率 < 70% 绝不开门**：unit-test 门控未通过时，integration-test 拒绝启动
- **设计文档不可跳过**：必须先输出完整测试设计（步骤、预期、命令），再执行测试
- **禁止混合多个用户故事**：一个测试用例应聚焦一个用户故事，避免混沌测试
- **禁止跳过前置条件**：每个测试必须确认环境状态（数据库、种子数据）后再执行
- **Playwright 仅用于前端关键链路**：非关键 UI 不强制使用 Playwright，避免过度工程化
- **契约破裂必须阻断**：接口实现与 openapi.yaml 不一致时，标记为 blocker 并停止
- **二元证据原则**：每个测试用例必须有明确的通过标准和失败标准，不允许"部分通过"
- **测试数据自动清理**：session 级 teardown 必须确保测试数据不污染后续环境
