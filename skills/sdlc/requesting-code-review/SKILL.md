---
name: requesting-code-review
description: 当用户提到'代码审查'、'code review'、'审查代码'、'检查实现质量'、'review'、'代码走读'或重构评估时触发，或在完成任务、实现主要功能、合并前、Gate 3（UAT）通过后验证工作是否符合需求时触发。分派代码审查子代理执行安全性、性能、可维护性审查，捕获级联前的问题，并输出结构化 code-review-report.md。
---

# Requesting Code Review

Dispatch a code reviewer subagent to catch issues before they cascade. The reviewer gets precisely crafted context for evaluation — never your session's history. This keeps the reviewer focused on the work product, not your thought process, and preserves your own context for continued work.

**Core principle:** Review early, review often.

## When to Request Review

**Mandatory:**
- After each task in subagent-driven development
- After completing major feature
- Before merge to main
- **After UAT passes and before release (V2.1)** — Gate 3 签字后，代码审查是发布前的最后质量门

**Optional but valuable:**
- When stuck (fresh perspective)
- Before refactoring (baseline check)
- After fixing complex bug

## How to Request

**1. Get git SHAs:**
```bash
BASE_SHA=$(git rev-parse HEAD~1)  # or origin/main
HEAD_SHA=$(git rev-parse HEAD)
```

**2. Prepare context files (V2.1 新增):**

审查前必须收集以下文件作为 reviewer 的输入上下文：
- `tasks.md`：当前变更的任务清单（用于任务追溯）
- `feature-*/design.md`：详细设计文档（用于设计符合度对比）
- `uat-report.md`（如有）：UAT 阶段发现的问题清单

**3. 执行审查（含通用审查维度）：**

审查子代理在评估代码时，除执行设计符合度对比、任务追溯和 UAT 交叉验证外，还必须按以下通用维度进行扫描：

#### 安全性
- [ ] 用户输入是否经过校验和转义（防 SQL 注入、XSS、命令注入）
- [ ] 是否存在硬编码的密钥、Token 或密码
- [ ] 数据库操作是否使用参数化查询 / ORM 绑定
- [ ] 文件上传是否限制类型和大小
- [ ] 敏感操作是否有权限校验与鉴权
- [ ] 敏感数据是否脱敏或加密存储

#### 性能
- [ ] 是否存在明显的算法复杂度问题（如 O(n²) 嵌套循环处理大数据）
- [ ] 数据库查询是否可优化（索引、N+1、JOIN、子查询）
- [ ] 是否重复计算可缓存的结果
- [ ] I/O 操作是否可批量处理
- [ ] 是否存在内存泄漏或资源未释放（连接、句柄、锁）

#### 可维护性
- [ ] 命名是否清晰表达意图（变量、函数、类）
- [ ] 函数是否遵循单一职责原则（建议不超过 50 行，圈复杂度可控）
- [ ] 是否有适当的异常处理和日志记录
- [ ] 新增代码是否有对应的单元测试或集成测试覆盖
- [ ] 注释是否解释了「为什么」而非「做了什么」
- [ ] 是否存在重复代码或可提取的公共逻辑

#### 代码规范与最佳实践
- [ ] 是否遵循项目编码规范（风格、目录结构、命名约定）
- [ ] 是否引入不必要的依赖或依赖版本冲突
- [ ] 类型注解 / 接口定义是否完整

**审查原则**：
1. **对事不对人**：评论针对代码，不针对作者
2. **解释原因**：不仅指出问题，还要说明为什么这是个问题
3. **提供替代方案**：如果可能，给出具体的改进代码示例
4. **区分阻塞与非阻塞**：阻塞问题必须修复才能合并；建议优化可以后续处理

**4. Dispatch code reviewer subagent:**

Use Task tool with `general-purpose` type, fill template at `code-reviewer.md`

**Placeholders:**
- `{DESCRIPTION}` - Brief summary of what you built
- `{PLAN_OR_REQUIREMENTS}` - What it should do
- `{BASE_SHA}` - Starting commit
- `{HEAD_SHA}` - Ending commit
- `{UAT_ISSUES}` (V2.1) - Any issues found during UAT, to avoid duplicate findings
- `{TASKS_MD}` (V2.1) - Path to tasks.md for traceability
- `{DESIGN_MD}` (V2.1) - Path to design.md for design alignment check

**4. Act on feedback:**
- Fix Critical issues immediately
- Fix Important issues before proceeding
- Note Minor issues for later
- Push back if reviewer is wrong (with reasoning)

**5. Output structured report (V2.1)**

审查完成后，必须输出 `code-review-report.md` 到 `openspec/changes/{变更名}/`：

```markdown
## 代码审查报告：{变更名}

> 审查范围：{BASE_SHA}..{HEAD_SHA} | 审查时间：{ISO8601}
> 审查人：AI Subagent | 被审查人：{开发者}

### 总体结论

| 项目 | 结果 |
|------|------|
| 总体评估 | ✅ 通过 / ⚠️ 有条件通过 / ❌ 不通过 |
| 阻塞性问题数 | {N} |
| 重要问题数 | {N} |
| 轻微问题数 | {N} |
| 是否允许合并 | 是 / 否（需修复阻塞性问题） |

### 🔴 阻塞性问题（必须修复）

1. **{问题标题}**
   - **位置**：`{文件路径}:{行号}`
   - **严重程度**：Critical
   - **问题类型**：安全性 / 性能 / 逻辑错误 / 数据完整性 / 异常处理缺失
   - **描述**：{具体问题}
   - **修复建议**：{建议}
   - **关联 UAT 问题（如有）**：{uat-issue-id}
   - **关联任务编号（如有）**：{task-id}

### 🟡 重要问题（建议修复）

1. **{问题标题}**
   - **位置**：`{文件路径}:{行号}`
   - **严重程度**：Important
   - **问题类型**：代码风格 / 可维护性 / 测试覆盖 / 文档缺失
   - **描述**：{具体问题}
   - **修复建议**：{建议}
   - **关联任务编号（如有）**：{task-id}

### 🟢 轻微问题（可延后）

1. **{问题标题}**
   - **位置**：`{文件路径}:{行号}`
   - **严重程度**：Minor
   - **描述**：{具体问题}

### ✅ 亮点

- {代码结构清晰 / 测试覆盖充分 / 异常处理完善 / 命名规范等}

### 📐 实现与设计偏差分析（V2.1 新增）

基于 `feature-*/design.md` 对比当前实现：

| 设计章节 | 设计意图 | 实现状态 | 偏差说明 | 结论 |
|----------|----------|----------|----------|------|
| {章节} | {意图} | 已实现 / 未实现 / 偏离 | {说明} | 符合 / 需澄清 / 需修复 |

**总体设计符合度**：{高 / 中 / 低}
**关键偏离**：{如有，列出与核心设计意图偏离的部分}

### 📋 任务追溯矩阵（V2.1 新增）

基于 `tasks.md` 检查代码变更对任务的覆盖度：

| 任务编号 | 任务描述 | 代码中是否体现 | 审查意见 | 状态 |
|----------|----------|----------------|----------|------|
| T-001 | {描述} | 是 / 否 / 部分 | {意见} | 通过 / 需补全 |

**未覆盖任务**：{如有，列出 tasks.md 中有但代码中未体现的任务}
**额外实现**：{如有，列出代码中实现但 tasks.md 中未规划的内容，标记为 scope deviation}

### 🔄 与 UAT 问题的交叉验证（V2.1）

| UAT 问题 ID | 是否在代码审查中发现根因 | 审查结论 |
|-------------|------------------------|----------|
| {UAT-001} | 是 / 否 | {说明} |

### 🚀 与 release-management 的衔接

- **审查结论为通过 / 有条件通过**：code-review-report.md 作为 release-checklist.md 的前置输入，用于生成发布清单的风险评估
- **审查结论为不通过**：生成 `rework-tasks.md`，返回 `executing-plans` 修复，修复完成后重新触发代码审查
- **阻塞性问题状态**：{已清零 / 剩余 N 项}

### 下一步行动

- [ ] 修复阻塞性问题并重新审查
- [ ] 修复重要问题（建议在合并前）
- [ ] 轻微问题记入技术债清单
```

## Example

```
[Just completed Task 2: Add verification function]

You: Let me request code review before proceeding.

BASE_SHA=$(git log --oneline | grep "Task 1" | head -1 | awk '{print $1}')
HEAD_SHA=$(git rev-parse HEAD)

[Dispatch code reviewer subagent]
  DESCRIPTION: Added verifyIndex() and repairIndex() with 4 issue types
  PLAN_OR_REQUIREMENTS: Task 2 from docs/superpowers/plans/deployment-plan.md
  BASE_SHA: a7981ec
  HEAD_SHA: 3df7661
  UAT_ISSUES: "None"  # or list UAT issues if any
  TASKS_MD: "openspec/changes/{变更名}/tasks.md"
  DESIGN_MD: "openspec/changes/{变更名}/detail-design/feature-001/design.md"

[Subagent returns]:
  Strengths: Clean architecture, real tests
  Issues:
    Important: Missing progress indicators
    Minor: Magic number (100) for reporting interval
  Assessment: Ready to proceed

You: [Fix progress indicators]
[Output code-review-report.md]
[Continue to Task 3]
```

## Integration with Workflows

**Subagent-Driven Development:**
- Review after EACH task
- Catch issues before they compound
- Fix before moving to next task

**Executing Plans:**
- Review after each task or at natural checkpoints
- Get feedback, apply, continue

**Ad-Hoc Development:**
- Review before merge
- Review when stuck

## 与上下游衔接

| 衔接点 | 动作 |
|--------|------|
| 上游: executing-plans | 编码实现完成后触发；或 Gate 3（UAT）签字后作为发布前最后质量门 |
| 上游: uat-verification | 消费 `uat-report.md` 进行 UAT 交叉验证 |
| 下游: release-management | `code-review-report.md` 作为发布清单的前置输入；阻塞性问题清零方可进入发布 |
| 下游: executing-plans | 不通过时生成 `rework-tasks.md` 返回修复 |
| 横向: self-check | 审查报告质量校验（结构化、分级、追溯完整性） |

**Project Delivery Workflow (V2.1):**
- Review after Gate 3 (UAT sign-off) and before release-management
- code-review-report.md 作为 release-management 的输入之一
- 若 UAT 发现问题，审查时需验证代码中是否已修复
- 审查意见必须与 tasks.md 任务编号关联，确保可追溯
- 必须对比 design.md，确认实现未偏离设计意图

## Red Flags

**Never:**
- Skip review because "it's simple"
- Ignore Critical issues
- Proceed with unfixed Important issues
- Argue with valid technical feedback
- **Skip structured report output (V2.1)** — code-review-report.md 是发布决策的必要输入
- **忽略 design.md 对比 (V2.1)** — 实现偏离设计是严重的架构风险
- **忽略 tasks.md 追溯 (V2.1)** — 未覆盖的任务意味着交付不完整

**If reviewer wrong:**
- Push back with technical reasoning
- Show code/tests that prove it works
- Request clarification

## Gotchas (V2.1 新增)

- **UAT 与代码审查的互补性**：UAT 发现业务逻辑错误，代码审查发现实现缺陷。两者不可替代。若 UAT 发现问题但代码审查未发现根因，说明审查深度不足。
- **code-review-report.md 不是可选文件**：即使审查结论为"通过"，也必须输出报告，记录审查范围、结论和亮点，形成审计追溯。
- **阻塞性问题必须清零**：存在阻塞性问题的代码不得进入 release-management 阶段。
- **与 release-management 的衔接**：code-review-report.md 是 release-checklist.md 的前置输入之一。无审查报告，不得生成发布清单。
- **design.md 对比不可跳过**：代码审查必须检查实现是否偏离设计意图。若实现优于设计，标记为"正向偏离"并说明理由；若劣于设计，标记为阻塞性问题。
- **tasks.md 追溯必须精确**：每个审查意见尽可能关联到 tasks.md 中的任务编号。无法关联的任务可能意味着 scope creep 或遗漏交付。
- **不通过时的 rework-tasks.md**：若结论为"不通过"，必须生成 `rework-tasks.md`，列出阻塞性问题的修复任务，返回 `executing-plans` 执行修复。

See template at: requesting-code-review/code-reviewer.md
