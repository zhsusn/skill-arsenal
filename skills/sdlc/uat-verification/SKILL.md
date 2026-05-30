---
name: uat-verification
description: 当用户提到'UAT'、'用户验收测试'、'验收'、'uat-report'、'业务流程验证'或 Gate 3 人工走查前需要生成检查清单时触发。基于用户故事和集成测试结果生成 UAT 验证方案，辅助人工在预览环境完成端到端业务流程验证，产出结构化 uat-report.md。
---

# UAT Verification（用户验收测试验证）

## 适用场景

- `integration-test` 全部 P0 用例通过后，进入 Gate 3 前的业务流程验证
- 用户明确要求"UAT"、"验收测试"、"走查业务流程"
- 需要基于用户故事生成可执行的 UAT 检查清单
- 预览环境 / staging 环境已部署，准备人工验证
- 需要产出 `uat-report.md` 作为 Gate 3 签字依据

## 前置依赖

| 依赖项 | 路径 | 门控标准 |
|--------|------|----------|
| 集成测试通过 | `tests/integration/report.md` | 全部 P0 用例通过 |
| 代码审查通过 | `openspec/changes/{变更名}/code-review/review-report.yaml` | overall 为 Approve 或 Comment；blocking 问题已清零 |
| 用户故事清单 | `tests/integration/user-stories-checklist.md` | 已由 integration-test 生成 |
| 详细需求 | `openspec/changes/{变更名}/detailed-requirements/feature-*/module-requirements.md` | 存在且可读 |
| 预览环境 | staging / preview 部署 | 已部署且可访问 |

**硬性阻断**：若 integration-test P0 用例未全部通过，拒绝执行并提示："请先修复集成测试失败项，P0 用例 100% 通过后方可进入 UAT。"

## 执行流程

### Phase 1: 读取输入与生成验证清单

1. 读取 `tests/integration/user-stories-checklist.md`，获取用户故事列表与集成测试状态
2. 读取 `detailed-requirements/feature-*/module-requirements.md` §1（需求追溯与验收标准），补充业务上下文、验收标准、异常分支
3. **生成/增强 `user-stories-checklist.md`**：
   - 为每个用户故事补充**操作步骤**（具体到按钮、输入、页面跳转）
   - 为每个用户故事补充**异常分支检查项**（权限不足、数据为空、网络中断恢复）
   - 标注集成测试状态（已通过 / 待验证 / 有阻塞）
   - 增加 UAT 勾选列 `[ ]`

```markdown
| 需求编号 | 用户故事 | 操作步骤 | 预期结果 | 集成测试状态 | UAT 勾选 |
|----------|----------|----------|----------|--------------|----------|
| FR-001 | 作为用户，我可以注册账号 | 1. 打开预览环境注册页 2. 填写用户名/密码/手机号 3. 点击注册按钮 | 跳转到登录页，收到短信验证码 | 通过 | [ ] |
```

4. 生成 `uat-instructions.md`（供人工执行的补充说明）：
   - 预览环境访问地址
   - 测试账号与权限配置
   - 需重点关注的 P0 链路
   - 环境重置方法（如需要）

### Phase 2: 人工执行验证（不可替代）

**此阶段必须由人工在预览环境执行，AI 仅提供清单和记录结果。**

向用户输出 Gate 3 提示语：

```text
========================================
🚪 Gate 3: 发布冻结 —— 等待人工 UAT 走查
========================================

请在预览环境按 user-stories-checklist.md 逐项操作：

1. 正向流程：按用户故事完整走通
2. 异常分支：重复名称、超长输入、网络中断恢复
3. 权限验证：未登录访问、越权操作
4. 跨浏览器/跨设备检查（如适用）

操作完成后，请告诉我：
- 通过 / 不通过 / 有条件通过
- 发现的问题清单（如有）
- 遗留事项（如有）
```

### Phase 3: 生成 UAT 报告

根据人工反馈，生成 `openspec/changes/{变更名}/uat/uat-report.md`：

```markdown
# UAT 报告：{变更名}

> 验证日期：{ISO8601}
> 验证环境：{staging/preview URL}
> 验证人：{人工名称 / AI 辅助}

## 总体结论

| 项目 | 结果 |
|------|------|
| 总体评估 | ✅ 通过 / ⚠️ 有条件通过 / ❌ 不通过 |
| P0 用户故事验证率 | {N}/{M} |
| 阻塞性问题数 | {N} |
| 遗留问题数 | {N} |

## 验证明细

| 需求编号 | 用户故事 | UAT 结果 | 问题描述 | 严重级别 |
|----------|----------|----------|----------|----------|
| FR-001 | ... | 通过 | — | — |
| FR-002 | ... | 不通过 | 支付后未跳转订单页 | 🔴 P0 |

## 问题清单

### 🔴 阻塞性问题（必须修复）
1. **{标题}**
   - **关联需求**：FR-XXX
   - **复现步骤**：...
   - **预期结果**：...
   - **实际结果**：...
   - **建议**：...

### 🟡 遗留问题（下一迭代处理）
1. **{标题}** — {说明}

## 与集成测试的交叉验证

| UAT 问题 | 集成测试是否覆盖 | 说明 |
|----------|------------------|------|
| {问题} | 是 / 否 | ... |

## 签字

- UAT 执行人：___________ 日期：___________
```

### Phase 4: 门控与流转

| 结论 | 动作 |
|------|------|
| 通过 | 提示用户执行 `/skill:human gate=Gate3 action=sign-off`，进入 `release-management` |
| 有条件通过 | 提示用户执行 `/skill:human gate=Gate3 action=conditional result=passed issues="..."`，轻微遗留问题进入下一迭代 |
| 不通过 | 生成 `rework-tasks.md`，返回 `executing-plans` 修复阻塞性问题，修复后重新申请 Gate 3 |

## 与上下游衔接

| 衔接点 | 动作 |
|--------|------|
| 上游: integration-test | 消费 `user-stories-checklist.md`；P0 用例未通过则拒绝启动 |
| 上游: code-review-pipeline | 确认代码审查已通过（blocking 问题清零） |
| 下游: human (Gate 3) | 输出 `uat-report.md` 供人工签字；阻塞性问题必须清零才能签字 |
| 下游: release-management | uat-report.md 作为发布风险评估输入 |
| 横向: self-check | 执行 UAT 质量检查（检查清单完整性、问题分级合理性） |

## 输出物清单

| 文件 | 路径 | 说明 |
|------|------|------|
| user-stories-checklist.md | `tests/integration/user-stories-checklist.md` | 增强版检查清单（含操作步骤、异常分支） |
| uat-instructions.md | `openspec/changes/{变更名}/uat/uat-instructions.md` | 人工执行指南（环境地址、账号、注意事项） |
| uat-report.md | `openspec/changes/{变更名}/uat/uat-report.md` | 结构化 UAT 报告（通过/不通过/遗留问题） |
| rework-tasks.md | `openspec/changes/{变更名}/uat/rework-tasks.md` | 不通过时生成，返回 executing-plans 修复 |

## Gotchas

- **人工不可替代**：UAT 必须由真实用户在预览环境点击、输入、验证，AI 不能代替人工完成验证。AI 的职责是生成清单、记录结果、辅助分析问题。
- **P0 用例是硬门槛**：integration-test 的 P0 用例未全部通过时，uat-verification 必须拒绝启动。不允许"边测边修"的并行模式。
- **阻塞性问题必须清零**：uat-report.md 中存在阻塞性问题（🔴 P0）时，不得进入 Gate 3 签字，必须生成 rework-tasks.md 返回开发。
- **与集成测试的互补性**：UAT 发现业务逻辑错误（如流程跳转、文案提示），集成测试发现技术缺陷（如接口契约破裂）。UAT 发现问题但集成测试未覆盖，说明测试设计遗漏。
- **环境一致性**：UAT 必须在独立环境（staging / preview）执行，禁止在开发环境或生产环境直接验证。
- **user-stories-checklist.md 不是静态文件**：即使 integration-test 已生成，uat-verification 仍需基于详细需求的 user-stories.md 增强操作步骤和异常分支，确保人工可执行。
- **遗留问题的边界**：有条件通过时，遗留问题必须是"不影响当前发布"的轻微问题（如文案优化、UI 微调）。任何影响核心业务流程的问题都不得标记为遗留。
- **rework-tasks.md 的闭环**：生成 rework-tasks.md 后，必须明确标注关联的 UAT 问题 ID 和原始需求编号（FR-XXX），确保修复后可追溯验证。
