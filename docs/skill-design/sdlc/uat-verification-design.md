# uat-verification 设计文档

> 本文档面向 AI 助手开发者和项目维护者，说明 `uat-verification` Skill 的架构设计、核心机制与扩展方式。
>
> 对应实现：`skills/sdlc/uat-verification/`
> 版本：1.0.0

---

## 目录

1. [概述](#概述)
2. [架构总览](#架构总览)
3. [处理逻辑](#处理逻辑)
4. [输入输出规格](#输入输出规格)
5. [工具链衔接](#工具链衔接)
6. [开源参考与借鉴](#开源参考与借鉴)
7. [关键设计决策](#关键设计决策)
8. [风险与规避](#风险与规避)

---

## 概述

### 定位

`uat-verification` 是 **SDLC 阶段 9.5（UAT 验证）** 的核心 Skill，职责是：

> 基于 `integration-test` 产出的用户故事清单和详细需求中的验收标准，生成可执行的 UAT 检查清单，辅助人工在预览环境完成端到端业务流程验证，产出结构化 `uat-report.md` 作为 Gate 3 签字依据。

### 核心差异化

与开源社区通用的"测试顾问型"Skill 不同，`uat-verification` 是**流程嵌入型**——它不接替代人工执行 UAT，而是将 AI 的能力聚焦在"生成清单 → 记录结果 → 辅助分析"三个环节，确保 UAT 过程可追溯、可复现、有门控。

| 维度 | 通用测试顾问型 | uat-verification（流程嵌入型） |
|---|---|---|
| 输入 | 用户对话中的测试需求 | `user-stories-checklist.md` + `specs/feature-*/user-stories.md` |
| 输出 | 测试建议、通用检查项 | 结构化 `uat-report.md` + `rework-tasks.md`（不通过时） |
| 与 SDLC 衔接 | 独立使用 | 嵌入 Gate 3 发布冻结闸，阻塞性门控 |
| 人工角色 | 可选辅助 | **不可替代**：必须由人工在预览环境执行验证 |

---

## 架构总览

### 数据流

```
┌─────────────────────────────────────────────────────────────────────┐
│                        uat-verification                              │
│                                                                      │
│  ┌──────────────────┐   ┌──────────────────┐                       │
│  │ integration-test │   │ detailed-requirements                     │
│  │ user-stories-    │   │ user-stories.md  │                       │
│  │ checklist.md     │   │                  │                       │
│  └────────┬─────────┘   └────────┬─────────┘                       │
│           │                      │                                  │
│           └──────────┬───────────┘                                  │
│                      ▼                                               │
│           ┌──────────────────┐                                      │
│           │  清单增强与补充   │  ← 补充操作步骤、异常分支            │
│           │  · 正向流程       │                                      │
│           │  · 异常分支       │                                      │
│           │  · 权限验证       │                                      │
│           └────────┬─────────┘                                      │
│                    ▼                                                 │
│           ┌──────────────────┐                                      │
│           │  人工执行验证     │  ← 不可替代（预览环境点击/输入）      │
│           │  · 用户操作       │                                      │
│           │  · 结果反馈       │                                      │
│           └────────┬─────────┘                                      │
│                    ▼                                                 │
│           ┌──────────────────┐                                      │
│           │  生成 uat-report │  ← 结构化报告（通过/不通过/遗留）     │
│           │  · 验证明细       │                                      │
│           │  · 问题分级       │                                      │
│           │  · 交叉验证       │                                      │
│           └────────┬─────────┘                                      │
│                    ▼                                                 │
│           ┌──────────────────┐                                      │
│           │  🚪 Gate 3 门控   │  ← 阻塞性签字                         │
│           │  · 通过 → 代码审查 │                                      │
│           │  · 不通过 → rework│                                      │
│           └──────────────────┘                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 执行时机

```
integration-test (P0 通过)
    └── uat-verification
            ├── Phase 1: 清单增强
            ├── Phase 2: 人工验证（阻塞）
            ├── Phase 3: 生成报告
            └── Phase 4: 门控流转
                    ├── 通过 → human(Gate3) → requesting-code-review
                    └── 不通过 → rework-tasks.md → executing-plans
```

---

## 处理逻辑

### 四阶段流水线

#### Phase 1: 读取输入与生成验证清单

**前置检查**：
- 读取 `tests/integration/report.md`
- 确认全部 P0 用例通过，否则**拒绝执行**

**清单增强策略**：

| 来源 | 内容 | 增强动作 |
|------|------|----------|
| `user-stories-checklist.md` | 需求编号、用户故事、集成测试状态 | 补充具体操作步骤 |
| `user-stories.md` | 验收标准、业务规则、异常分支 | 补充异常分支检查项 |
| `interaction-spec.md` | 按钮级交互规格 | 补充页面跳转、加载态、失败态检查 |

#### Phase 2: 人工执行验证（MANDATORY）

AI 输出 Gate 3 提示语后进入阻塞状态，等待人工反馈：
- 通过 / 不通过 / 有条件通过
- 问题清单（含复现步骤）
- 遗留事项

#### Phase 3: 生成 UAT 报告

报告结构：
1. 总体结论（通过/有条件通过/不通过）
2. 验证明细（需求编号 ↔ 结果 ↔ 问题）
3. 问题清单（阻塞性/遗留）
4. 与集成测试的交叉验证（发现测试覆盖盲区）
5. 签字栏

#### Phase 4: 门控与流转

| 结论 | 下游动作 |
|------|----------|
| 通过 | `human gate=Gate3 action=sign-off` → `requesting-code-review` |
| 有条件通过 | `human gate=Gate3 action=conditional` → `requesting-code-review`（遗留问题入下一迭代） |
| 不通过 | 生成 `rework-tasks.md` → `executing-plans` |

---

## 输入输出规格

### 输入

| 输入项 | 类型 | 来源 | 说明 |
|--------|------|------|------|
| 用户故事清单 | Markdown | `tests/integration/user-stories-checklist.md` | 已由 integration-test 生成 |
| 详细需求 | Markdown | `specs/feature-*/user-stories.md` | 补充业务上下文 |
| 集成测试报告 | Markdown | `tests/integration/report.md` | P0 通过门控 |
| 交互规格 | Markdown | `specs/feature-*/interaction-spec.md` | 补充按钮级检查项 |
| 人工反馈 | 对话 | 用户输入 | 验证结果与问题描述 |

### 输出

| 输出项 | 类型 | 路径 | 说明 |
|--------|------|------|------|
| 增强版检查清单 | Markdown | `tests/integration/user-stories-checklist.md` | 含操作步骤、异常分支、UAT 勾选 |
| UAT 执行指南 | Markdown | `openspec/changes/{变更名}/uat/uat-instructions.md` | 环境地址、账号、注意事项 |
| UAT 报告 | Markdown | `openspec/changes/{变更名}/uat/uat-report.md` | 结构化验收报告 |
| 返工任务 | Markdown | `openspec/changes/{变更名}/uat/rework-tasks.md` | 不通过时生成 |

---

## 工具链衔接

### 前置依赖

| Skill | 关系 | 说明 |
|---|---|---|
| `integration-test` | **强依赖** | 必须等待 P0 用例全部通过 |
| `detailed-requirements` | **输入依赖** | 读取 user-stories.md 和 interaction-spec.md |

### 后置消费

| Skill | 关系 | 说明 |
|---|---|---|
| `human` | **阻塞闸** | Gate 3 人工签字 |
| `requesting-code-review` | **消费者** | uat-report.md 作为 UAT 交叉验证输入 |
| `release-management` | **消费者** | uat-report.md 作为发布风险评估输入 |
| `executing-plans` | **返工路径** | 不通过时生成 rework-tasks.md 返回修复 |

---

## 开源参考与借鉴

### 参考一：spellbook `isolated-testing`

- **借鉴点**："设计先于执行"纪律、二元证据原则（通过/失败的明确区分）
- **融入方式**：Phase 1 强制输出可执行的检查清单，每个检查项必须有明确的通过标准和失败标准

### 参考二：spellbook `auditing-green-mirage`

- **借鉴点**：测试有效性审计、避免"看起来通过了但实际上没验证"的虚假通过
- **融入方式**：uat-report.md 中的"与集成测试交叉验证"章节，识别测试覆盖盲区

### 参考三：MLOps-Courses/mlops-coding-skills（Verification）

- **借鉴点**：Checklist 风格、分层验证（正向/异常/权限）
- **融入方式**：user-stories-checklist.md 的三层检查结构

---

## 关键设计决策

| 决策 | 选择 | 理由 |
|---|---|---|
| **AI 是否代替人工执行 UAT** | 否，AI 只生成清单和记录结果 | UAT 的核心价值是真实用户的真实体验，AI 无法模拟人类的直觉和上下文判断 |
| **P0 用例是否作为硬门槛** | 是，未通过拒绝启动 | 防止"边测边修"的混沌模式，确保技术质量底线 |
| **清单增强 vs 重新生成** | 增强（基于 integration-test 产出） | 避免重复劳动，保持需求编号、用户故事的一致性 |
| **有条件通过的边界** | 遗留问题必须不影响核心业务流程 | 防止"将阻塞性问题降级为遗留问题"的绕过行为 |
| **rework-tasks.md 的格式** | 与 tasks.md 格式兼容 | 确保返回 executing-plans 后可无缝接入 Batch 执行流程 |

---

## 风险与规避

| 风险 | 规避方法 |
|------|----------|
| 人工跳过验证直接要求签字 | AI 必须输出清单并等待人工反馈，不得在没有反馈的情况下生成"通过"报告 |
| 将阻塞性问题标记为遗留 | uat-report.md 中明确分级标准：影响核心流程 = 阻塞性 |
| 环境不一致导致验证无效 | uat-instructions.md 中必须明确环境地址和版本号 |
| 测试覆盖盲区未被发现 | 强制要求"与集成测试交叉验证"章节 |
| rework-tasks.md 无法追溯到原始需求 | 必须标注关联的 UAT 问题 ID 和 FR-XXX 需求编号 |
