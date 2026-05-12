# Task Breakdown Skill 使用手册

> 本文档面向 Skill 使用者，提供触发方式、使用步骤、输出解读与常见问题。
>
> 版本: 1.0.0

---

## 1. 快速开始

### 1.1 什么是 Task Breakdown？

`task-breakdown` 是设计到编码之间的**精细化调度层**。它将设计文档按 **≤30 分钟/任务** 的粒度拆解为 Phase 组织的开发任务清单（tasks.md），供 executing-plans 直接消费。

**核心原则**：
- 垂直切片优先（按功能端到端拆分，不按技术层横向拆分）
- 粒度上限刚性（>30 分钟或 >5 文件必须再拆）
- 标签明确化（前端/后端/AI模型/配置/测试）
- 验收可验证（每个任务必须有明确完成条件）

### 1.2 触发方式

| 方式 | 指令示例 |
|------|----------|
| 通用触发 | `/task-breakdown` |
| 场景触发 | 【任务拆解】请将这个设计文档拆成开发任务 |
| 阶段触发 | 【阶段 4 拆解】基于 detailed-design 生成 tasks.md |
| 衔接触发 | plan.md 完成后自动提示下一步执行 task-breakdown |

---

## 2. 使用步骤

### Step 1: 确认前置条件

task-breakdown 需要以下输入文档：
- ✅ `feature-*/design.md` 或 `design/*.md`（详细设计）
- ✅ `feature-*/api-spec.md` 或 `interface-contracts/openapi.yaml`（接口契约）
- ✅ （可选）`openspec/changes/{变更名}/plan.md`（writing-plans 输出）
- ✅ （可选）`parallel-dev-plan.md`（前后端并行计划）

**如果设计文档缺失**：task-breakdown 会暂停并提示先完成设计。

### Step 2: 执行拆解

发出触发指令后，task-breakdown 将自动执行以下动作：

1. 读取所有输入文档
2. 按垂直切片识别端到端功能路径
3. 对每个切片进行任务分级（XS/S/M/L/XL）
4. 为每个任务标注标签
5. 构建任务依赖图
6. 按拓扑排序组织为 Phase
7. 生成验收标准
8. 执行自检（覆盖度/无XL/依赖无环/标签完整/验收可验证）
9. 建议执行模式（delegated / sub_orchestrators / work_items）
10. 保存 tasks.md

### Step 3: 确认产出物

检查生成的 `tasks.md` 是否包含以下要素：
- [ ] 头部元数据（生成时间、执行模式建议、总任务数）
- [ ] 按 Phase 组织的任务列表
- [ ] 每个任务含：验收标准、依赖、触及文件、标签
- [ ] Mermaid 依赖图
- [ ] 风险与阻碍清单

---

## 3. 输出解读

### 3.1 tasks.md 结构

```markdown
# Tasks for feature-user-auth

> 生成时间: 2026-05-12 10:00
> 执行模式建议: delegated
> 总任务数: 8 | Phase 数: 3 | 预估总时长: 3.5 小时

## Phase 1: 基础设施与契约
- [ ] 1.1 [后端] 创建用户表 DDL + 索引
  - 验收: `pytest tests/unit/db/test_user_schema.py` 通过
  - 依赖: None
  - 文件: `src/db/migrations/001_user.sql`, `src/models/user.py`
  - 标签: [后端] [配置]

## Phase 2: 核心功能（垂直切片）
- [ ] 2.1 [后端] 实现用户注册 API（含参数校验）
  - 验收: `pytest tests/unit/api/test_register.py` 通过，覆盖率 ≥ 70%
  - 依赖: 1.1
  - 文件: `src/api/users.py`, `src/services/user_service.py`
  - 接口: `POST /api/v1/users`（参见 @interface-contracts/openapi.yaml#L45-80）

## Phase 3: 集成与联调
- [ ] 3.1 [测试] 端到端注册流程集成测试
  - 验收: `pytest tests/integration/test_register_e2e.py` 通过
  - 依赖: 2.1, 2.2
```

### 3.2 执行模式建议解读

| 建议模式 | 含义 | 何时适用 |
|----------|------|----------|
| `delegated` | 单会话直接执行 | < 15 个任务，单轨道 |
| `sub_orchestrators` | 分层调度 | ≥ 15 个任务 或 ≥ 2 个并行轨道 |
| `work_items` | 跨会话拆分 | ≥ 25 个任务 或 明确需要跨会话 |

### 3.3 标签含义速查

| 标签 | 责任域 | 典型任务 |
|------|--------|----------|
| `[前端]` | UI/UX | 页面、组件、样式、前端状态 |
| `[后端]` | 服务端 | API、业务逻辑、数据访问 |
| `[AI模型]` | AI/ML | 模型调用、Prompt、Embedding |
| `[配置]` | 基础设施 | CI/CD、环境变量、迁移脚本 |
| `[测试]` | 质量保障 | 单测、集成测试、E2E |

---

## 4. 自检 Gate 说明

task-breakdown 生成后会自动执行五项检查：

| 检查项 | 通过标准 | 失败处理 |
|--------|----------|----------|
| 覆盖度 | 设计文档每个模块/接口/状态机均有任务 | 返回补充遗漏任务 |
| 无 XL | 所有任务 ≤ 30 分钟 且 ≤ 5 文件 | 返回拆分 XL 任务 |
| 依赖无环 | DAG 拓扑排序成功 | 暂停并反馈循环依赖 |
| 标签完整 | 每个任务至少一个标签 | 返回补充标签 |
| 验收可验证 | 验收标准含命令或可观察行为 | 返回补充验证方式 |

**注意**：自检失败时，task-breakdown 会自动返回修复，无需用户手动干预。

---

## 5. 常见问题

### Q1：task-breakdown 和 writing-plans 有什么区别？

| 维度 | writing-plans | task-breakdown |
|------|---------------|----------------|
| 粒度 | 模块级（设计文档级） | 任务级（≤30 分钟） |
| 输出 | plan.md | tasks.md |
| 侧重点 | "做什么、按什么顺序、做到什么标准" | "拆成多小的任务、谁来做、花多久" |
| 标签 | 无 | [前端]/[后端]/[AI模型]/[配置]/[测试] |
| 关系 | 上游 | 下游 |

### Q2：为什么任务必须 ≤30 分钟？

30 分钟是一个经验阈值，确保：
- 每个任务可以一次性完成，不会被中断
- 任务边界清晰，便于并行分配
- executing-plans 可以按 Batch 高效执行
- 出现 Blocker 时回滚成本低

### Q3：垂直切片是什么意思？

**垂直切片** = 按功能端到端拆分。

- ✅ 正确："用户注册" = DB 模型 + API + 前端页面（每个切片可独立验证）
- ❌ 错误："先写所有 DAO，再写所有 Service，最后写所有 Controller"

垂直切片确保每个任务交付可验证的功能增量，而非半成品。

### Q4：tasks.md 生成后可以手动修改吗？

**不建议**。tasks.md 是 executing-plans 的执行蓝图，手动修改可能导致：
- 任务编号与依赖关系不一致
- 验收标准与实际实现脱节
- 执行进度跟踪失效

如果设计变更，建议重新执行 task-breakdown 生成新的 tasks.md。

### Q5：任务依赖图出现循环依赖怎么办？

task-breakdown 会在自检阶段检测循环依赖。如果发现：
1. **暂停拆解**
2. **报告用户**具体的循环路径
3. **建议修复设计文档**（通常是模块边界划分不当）

循环依赖必须在设计层面解决，不能在任务调度层面绕过。

### Q6：执行模式建议可以忽略吗？

可以，但建议参考。执行模式建议基于任务总量自动计算：
- 小项目（< 15 任务）用 `delegated` 最轻量
- 多轨道并行（前后端分离）用 `sub_orchestrators` 避免上下文膨胀
- 大项目（≥ 25 任务）用 `work_items` 避免单会话超时

---

## 6. 速查卡

```text
触发：/task-breakdown 或 【任务拆解】
输入：design.md + openapi.yaml +（可选）plan.md
输出：openspec/changes/{变更名}/tasks.md
原则：垂直切片、≤30分钟、≤5文件、禁止XL、标签明确、验收可验证
流程：读取 → 切片 → 分级 → 标签 → 依赖 → Phase → 验收 → 自检 → 保存
检查：覆盖度 / 无XL / 依赖无环 / 标签完整 / 验收可验证
模式：<15任务 delegated / ≥15任务 sub_orchestrators / ≥25任务 work_items
注意：tasks.md 原则上不手动修改，设计变更请重新执行 task-breakdown
```
