---
name: requesting-code-review
description: 当用户提到'提交代码审查'、'request review'、'准备审查材料'、'生成审查请求书'或在任务完成、功能实现后需要触发审查流程时触发。包含变更大小评估、死代码预检、依赖变更检测，并生成结构化审查请求书。
---

# Requesting Code Review（融合版 V2.0）

> 在任务完成或功能实现后，准备审查材料并触发审查流程。
> 包含变更大小评估、死代码预检、依赖变更检测。
> 适配 Kimi Code 无 subagent 环境，采用自检模式替代外部 reviewer。

## 触发条件

- 任务完成（代码已写、本地测试通过）
- 用户明确说"审查这段代码"、"/review"
- 自动检测到 `# @review` 标记
- pipeline 从 SIZING 状态流转后触发

## 审查材料准备流程

### 1. 变更大小评估（SIZING）

```bash
# 获取变更统计
git diff --stat {BASE_SHA} {HEAD_SHA}
# 或
git diff --stat HEAD~1 HEAD
```

**评估标准（来自 addyosmani）：**
```
~100  lines → Good. 标记 sizing_assessment: Good
~300  lines → Acceptable if single logical change. 标记 sizing_assessment: Acceptable
~1000 lines → Too Large. 标记 sizing_assessment: Too Large，进入 SPLITTING 指导
```

**如果 Too Large：**
> 本次变更 {X} 行，超过 300 行建议拆分。推荐策略：
> - Stack：先提交基础接口，再提交实现
> - By file group：按 reviewer 领域分组
> - Vertical：按功能切片
> 是否现在拆分，还是继续审查？

### 2. 死代码预检（来自 addyosmani）

在提交审查前，主动检查：
```bash
# 检查新增代码是否替代了旧代码
grep -r "function_name" src/ --include="*.py" | grep -v "new_file.py"
# 检查常量/配置是否仍有引用
grep -r "OLD_API_URL" src/ --include="*.ts"
```

如发现有被替代的旧代码，记录在 `known_issues` 中：
```yaml
known_issues: "发现 formatLegacyDate() 可能已被新实现替代，建议审查时确认是否可删除"
```

### 3. 依赖变更检测（来自 addyosmani）

检查是否有新增依赖：
```bash
# Python
git diff requirements.txt
# Node
git diff package.json
# Rust
git diff Cargo.toml
# Go
git diff go.mod
```

如有新增依赖，记录到 `new_dependencies`：
```yaml
new_dependencies:
  - name: "pyjwt"
    source: "requirements.txt"
    added_in_this_change: true
```

### 4. 变更描述规范

每个变更需要独立可读的描述：

**第一行：** 简短、祈使语气、独立成句。"添加 JWT 认证中间件"而非"添加了..."
**正文：** 说明变更内容和原因，包含上下文、决策和理由。链接到需求文档、设计文档。
**反模式：** "Fix bug"、"Fix build"、"Add patch"、"Moving code from A to B"、"Phase 1"

### 5. 生成《审查请求书》

提取信息并格式化为 YAML：
- task_id：从当前任务上下文获取
- description：一句话核心目的
- requirements_source：需求文档路径或用户指令摘要
- base_sha / head_sha：git 范围
- files_changed：文件列表，含 change_type、lines_added、lines_deleted、**language**
- total_lines_changed：总行数
- sizing_assessment：Good / Acceptable / Too Large
- scope：影响范围
- test_status：已测试 / 部分测试 / 未测试
- known_issues：作者已知的待完善点 + 死代码预检发现
- new_dependencies：新增依赖清单

### 6. 自检模式切换说明

> 当前环境无独立 subagent，接下来将调用 `code-reviewer` Skill 进行自检。
>
> 自检时，必须执行角色切换：
> - 从"实现者"切换为"独立审查者"
> - 不参考任何实现思路、设计决策、会话历史
> - 仅基于《审查请求书》和代码 diff 进行判断
> - 将分三轮执行： correctness+architecture → security+performance → readability+summary

## 禁止事项

- ❌ 携带实现过程中的思考历史
- ❌ 解释为什么这样写，只陈述做了什么
- ❌ 提交未通过本地测试的代码
- ❌ 在审查请求书中为代码辩护
- ❌ 隐瞒已知的死代码或依赖风险
- ❌ 使用模糊描述如"Fix bug"作为变更说明

## 输出规范

完成《审查请求书》后，**自动将状态置为 REVIEWING_P1**，并调用 `code-reviewer` Skill。

```yaml
review_request:
  task_id: "task-002"
  timestamp: "2026-05-24T06:00:00+08:00"
  description: "添加用户认证中间件"
  requirements_source: "docs/prd/auth.md"
  base_sha: "a1b2c3d"
  head_sha: "e4f5g6h"
  files_changed:
    - path: "src/middleware/auth.py"
      change_type: "新增"
      lines_added: 45
      lines_deleted: 0
      language: "python"
  total_lines_changed: 45
  sizing_assessment: "Good"
  scope: "新增 JWT 验证逻辑，影响所有受保护路由"
  test_status: "已本地测试，未写单元测试"
  known_issues: "SECRET_KEY 临时硬编码，待配置化"
  new_dependencies: []
```

## 与上下游衔接

| 衔接点 | 动作 |
|--------|------|
| 上游: executing-plans / implementation | 编码实现完成后触发 |
| 下游: code-reviewer | 生成审查请求书后自动调用 |
| 上游: code-review-pipeline | 由 pipeline 在 SIZING 通过后调用，进入 REQUESTING 阶段 |

## Gotchas

- **死代码预检不要省略**：即使你认为没有，也至少执行一次 grep 确认。这是 addyosmani 强调的死代码卫生。
- **依赖变更必须记录**：新增依赖是技术负债，必须暴露在审查请求书中供 reviewer 评估。
- **变更描述是文档**：审查请求书中的 description 会成为决策日志的一部分，写好它。
- ** sizing_assessment 诚实标记**：不要为了跳过拆分而故意低估行数。
- **known_issues 不是免责条款**：列出已知问题是为了让 reviewer 确认修复方案，不是为了"我已经知道了所以不用修"。
- **自检不是降低标准**：无 subagent 不代表审查可以草率。三轮角色轮替必须严格执行。
- **向后兼容**：如需使用旧版 subagent 模式，参考同目录下的 `code-reviewer.md` 模板手动派发。
