# Executing Plans Skill 使用手册

> 本文档面向 Skill 使用者，提供触发方式、使用步骤、Batch 执行解读与常见问题。
>
> 版本: 2.0.0

---

## 1. 快速开始

### 1.1 什么是 Executing Plans？

`executing-plans` 是**编码执行引擎**。它按 tasks.md 逐个执行开发任务，含：
- 执行前 Critical Review
- Batch 执行（默认 3 任务/批次）
- 强制自测 + 接口校验 + 单测门控
- 自动勾选 tasks.md
- 批次 Inline Audit

**核心原则**：遇阻不问猜，质量门控不合并，范围不膨胀。

### 1.2 触发方式

| 方式 | 指令示例 |
|------|----------|
| 通用触发 | `/executing-plans` |
| 场景触发 | 【开始实现】按 tasks.md 执行任务 |
| 阶段触发 | 【阶段 5 执行】开始编码实现 |
| 自动触发 | task-breakdown 完成后自动提示执行 |

---

## 2. 使用步骤

### Step 1: 确认前置条件

executing-plans 需要以下输入：
- ✅ `openspec/changes/{变更名}/tasks.md`（task-breakdown 输出）
- ✅ `feature-*/design.md`（编码依据）
- ✅ `feature-*/api-spec.md` 或 `interface-contracts/openapi.yaml`（接口校验基准）
- ✅ 当前不在 main/master 分支（或用户明确同意）

### Step 2: 执行 Critical Review

executing-plans 启动后会先执行审查：
- 任务描述是否与 design.md / api-spec 一致
- 接口定义是否与 openapi.yaml 冲突
- 前置任务是否已完成
- 是否存在未解决的 blocker

**如果审查发现问题**：暂停执行，向用户报告问题，等待决策。

### Step 3: Batch 执行

审查通过后，按 Batch（默认 3 任务）执行：

```
Batch 1: 任务 1.1, 1.2, 1.3
  → 逐个编码 → 自测 → 接口校验 → 单测 → 勾选 → Commit
  → Inline Audit
Batch 2: 任务 2.1, 2.2, 2.3
  → ...
```

### Step 4: 确认完成

全部任务完成后：
- 输出执行摘要
- 自动调用 finish Skill
- （如配置）自动触发 requesting-code-review

---

## 3. 输出解读

### 3.1 批次执行摘要

每 Batch 结束后输出：

```markdown
## Batch 1 执行摘要

| 任务 | 状态 | 自测 | 接口校验 | 单测 | 备注 |
|------|------|------|----------|------|------|
| 1.1 | ✅ | 通过 | 通过 | 通过 | — |
| 1.2 | ✅ | 通过 | 通过 | 通过 | — |
| 1.3 | ❌ | 失败 | — | — | Blocker: 依赖服务未启动 |

**批次状态**: 存在 Blocker
**下一步**: 等待用户决策
```

### 3.2 状态图标含义

| 图标 | 含义 |
|------|------|
| ✅ | 通过 |
| ❌ | 失败 / Blocker |
| ⏸️ | 暂停等待用户 |
| 🔄 | 修复中 |

### 3.3 tasks.md 自动勾选

任务完成后自动修改：
```markdown
- [x] 2.1 [后端] 实现用户注册 API（含参数校验）
  - 完成时间: 2026-05-12 10:30
```

tasks.md 是执行进度的**唯一可信源**，以 checkbox 状态为准。

---

## 4. 执行纪律速查

### 4.1 Simplicity First（Rule 0）

- 写代码前问："最简单的可行方案是什么？"
- 写完后检查："资深工程师会不会说'为什么不直接...'"

### 4.2 Scope Discipline（Rule 0.5）

**严禁顺手重构**。发现相邻文件问题：
- 不动代码
- 记入 `NOTICED BUT NOT TOUCHING` 列表
- 禁止添加 spec 外功能

### 4.3 Rollback-Friendly（Rule 5）

- 优先新增文件（易回滚）
- 修改现有代码尽量最小化
- DB 迁移配回滚脚本
- 禁止同一 commit 既删又替

---

## 5. 质量门控说明

每个任务必须通过三个**独立**门控：

| 门控 | 检查内容 | 工具/方法 |
|------|----------|----------|
| **Self-Check Gate** | 代码 vs 设计一致性、异常处理、边界条件 | 调用 self-check Skill |
| **Interface Gate** | 代码接口 vs api-spec / openapi.yaml | 字段级对比 |
| **Unit Test Gate** | pytest 通过 + 覆盖率 ≥ 70% | `pytest --cov` |

**Gate Non-Collapse Rule**：三个门控必须**独立执行**，禁止合并为"一起检查"。

---

## 6. Blocker 处理

遇阻不问猜，立即停止：

| Blocker 类型 | 示例 | 用户决策选项 |
|-------------|------|-------------|
| 缺失依赖 | Redis 未启动 | 启动服务 / 跳过该任务 / 终止执行 |
| 测试反复失败 | 运行 3 次仍失败 | 查看日志 / 放宽阈值 / 终止执行 |
| 指令不清 | tasks.md 写"优化性能"无具体指标 | 补充指标 / 跳过该任务 |
| 设计矛盾 | 代码需多表关联但 design.md 未定义 | 修改设计 / 简化实现 |
| 接口不一致 | 代码参数名与 api-spec 不一致 | 修改代码 / 修改 spec |

---

## 7. 常见问题

### Q1：executing-plans 和 subagent-driven-development 有什么区别？

| 维度 | executing-plans | subagent-driven-development |
|------|-----------------|---------------------------|
| 执行方式 | Batch 执行（本会话） | 每任务独立子 Agent |
| 适用场景 | 中小项目、单轨道 | 大项目、多轨道、需要隔离上下文 |
| 检查点 | Batch 后 Inline Audit | 每任务后 Review |
| 速度 | 较快（无子 Agent 调度开销） | 较慢但质量更高 |

**建议**：< 15 个任务用 executing-plans；≥ 15 个任务用 subagent-driven-development。

### Q2：Batch 大小可以调整吗？

可以，在 `openspec/config.yaml` 中配置：

```yaml
executing_plans:
  batch_size: 5   # 默认 3，可根据团队节奏调整
```

**注意**：Batch 越大，Inline Audit 时回滚成本越高。不建议超过 5。

### Q3：可以跳过某个门控吗？

**不可以**。Gate Non-Collapse Rule 是硬性约束：
- 跳过 Self-Check → 可能遗漏设计偏差
- 跳过 Interface Gate → 前后端接口漂移
- 跳过 Unit Test Gate → 回归风险

任何跳过都必须经用户明确同意，并记录原因。

### Q4：遇到 Blocker 后怎么继续？

1. 用户解决 Blocker（如启动服务、补充文档）
2. 从**当前任务**重新执行（非 Batch 开头）
3. 重新跑该任务的三个门控
4. 通过后继续 Batch 内剩余任务

### Q5：Inline Audit 不通过怎么办？

Inline Audit 审查本批次整体质量：
- 不通过 → 返回修复
- 修复后 → 重新跑 Batch 内**所有任务**的自测
- 通过 → 进入下一 Batch

### Q6：执行过程中发现 tasks.md 有问题怎么办？

**小修**（如错别字、文件路径微调）：
- 可以当场修正 tasks.md
- 记录修正内容

**大改**（如任务缺失、粒度不合适）：
- 暂停 executing-plans
- 重新执行 task-breakdown
- 用新的 tasks.md 继续执行

### Q7：可以在 main 分支上执行吗？

**严禁**。除非用户明确同意，否则 executing-plans 会拒绝在 main/master 上启动。

建议的工作流：
```bash
git checkout -b feature/xxx
# 执行 executing-plans
git push origin feature/xxx
```

### Q8：NOTICED BUT NOT TOUCHING 列表有什么用？

这是 Scope Discipline 的执行痕迹：
- 记录发现但未修改的相邻文件问题
- 便于后续创建独立的优化任务
- 证明执行过程中没有顺手重构

示例：
```markdown
## NOTICED BUT NOT TOUCHING

- `src/services/order_service.py:123` —— 重复代码，建议后续重构
- `config/database.yml` —— 连接池配置可优化
```

---

## 8. 速查卡

```text
触发：/executing-plans 或 【开始实现】
输入：tasks.md + design.md + api-spec.md
输出：代码文件 + 测试 + 更新后的 tasks.md
原则：遇阻不问猜、Simplicity First、Scope Discipline、Rollback-Friendly
流程：加载 → Critical Review → Batch 组织 → 编码 → 自测 → 接口校验 → 单测 → 勾选 → Commit → Inline Audit
门控：Self-Check / Interface / Unit Test（独立执行，禁止合并）
Batch：默认 3 任务/批次，批次间强制检查点
Blocker：暂停 → 报告用户 → 解决后从当前任务继续
纪律：One Thing at a Time / Keep It Compilable / Feature Flags / Safe Defaults
注意：严禁 main 分支执行；tasks.md 是进度唯一可信源
```
