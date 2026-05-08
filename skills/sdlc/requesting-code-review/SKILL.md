---
name: requesting-code-review
description: 当用户提到'代码审查'、'code review'、'审查代码'、'检查实现质量'或在完成任务、实现主要功能、合并前验证工作是否符合需求时触发。分派代码审查子代理捕获级联前的问题，并输出结构化 code-review-report.md。
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

**2. Dispatch code reviewer subagent:**

Use Task tool with `general-purpose` type, fill template at `code-reviewer.md`

**Placeholders:**
- `{DESCRIPTION}` - Brief summary of what you built
- `{PLAN_OR_REQUIREMENTS}` - What it should do
- `{BASE_SHA}` - Starting commit
- `{HEAD_SHA}` - Ending commit
- `{UAT_ISSUES}` (V2.1) - Any issues found during UAT, to avoid duplicate findings

**3. Act on feedback:**
- Fix Critical issues immediately
- Fix Important issues before proceeding
- Note Minor issues for later
- Push back if reviewer is wrong (with reasoning)

**4. Output structured report (V2.1 新增)**

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

### 🟡 重要问题（建议修复）

1. **{问题标题}**
   - **位置**：`{文件路径}:{行号}`
   - **严重程度**：Important
   - **问题类型**：代码风格 / 可维护性 / 测试覆盖 / 文档缺失
   - **描述**：{具体问题}
   - **修复建议**：{建议}

### 🟢 轻微问题（可延后）

1. **{问题标题}**
   - **位置**：`{文件路径}:{行号}`
   - **严重程度**：Minor
   - **描述**：{具体问题}

### ✅ 亮点

- {代码结构清晰 / 测试覆盖充分 / 异常处理完善 / 命名规范等}

### 与 UAT 问题的交叉验证（V2.1）

| UAT 问题 ID | 是否在代码审查中发现根因 | 审查结论 |
|-------------|------------------------|----------|
| {UAT-001} | 是 / 否 | {说明} |

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

**Project Delivery Workflow (V2.1):**
- Review after Gate 3 (UAT sign-off) and before release-management
- code-review-report.md 作为 release-management 的输入之一
- 若 UAT 发现问题，审查时需验证代码中是否已修复

## Red Flags

**Never:**
- Skip review because "it's simple"
- Ignore Critical issues
- Proceed with unfixed Important issues
- Argue with valid technical feedback
- **Skip structured report output (V2.1)** — code-review-report.md 是发布决策的必要输入

**If reviewer wrong:**
- Push back with technical reasoning
- Show code/tests that prove it works
- Request clarification

## Gotchas (V2.1 新增)

- **UAT 与代码审查的互补性**：UAT 发现业务逻辑错误，代码审查发现实现缺陷。两者不可替代。若 UAT 发现问题但代码审查未发现根因，说明审查深度不足。
- **code-review-report.md 不是可选文件**：即使审查结论为"通过"，也必须输出报告，记录审查范围、结论和亮点，形成审计追溯。
- **阻塞性问题必须清零**：存在阻塞性问题的代码不得进入 release-management 阶段。
- **与 release-management 的衔接**：code-review-report.md 是 release-checklist.md 的前置输入之一。无审查报告，不得生成发布清单。

See template at: requesting-code-review/code-reviewer.md
