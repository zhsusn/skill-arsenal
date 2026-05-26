---
name: receiving-code-review
description: 当用户收到审查意见、需要处理 code review feedback、修复审查发现的问题、或进入复查阶段时触发。技术严谨地处理反馈，生成修复计划，支持状态回写与复查联动。
---

# Receiving Code Review（融合版）

> 收到审查意见后，技术严谨地处理反馈。
> 融合 obra 的硬核验证纪律与 awesome-skills 的协作式响应规范。
> 支持状态回写、修复计划生成、与 code-reviewer 复查联动。

## 输入

《审查意见书》（来自 code-reviewer 自检或外部 reviewer）

## 处理流程

### Step 1: 分类与澄清（阻塞性步骤）

读取所有 issue，按严重性分组处理：

| 严重性 | 处理策略 | 下一步 |
|--------|---------|--------|
| 🔴 blocking | 必须理解 + 必须修复 | 加入 fix_plan |
| 🟠 important | 理解无误后修复；有异议可讨论 | 加入 fix_plan 或 pushback_list |
| 🟡 nit | 可忽略；如同意则顺手修复 | 加入 fix_plan（低优先级）或忽略 |
| 🔵 suggestion | 值得考虑，非强制 | 加入 defer_list 或 fix_plan |
| 📚 learning | 了解即可 | 记录到知识库 |
| 🌟 praise | 无需行动 | 记录到 progress.md strengths |

**澄清规则（来自 obra）：**
```
IF 任何 item 不理解:
  STOP — 不要实施任何修复
  ASK 澄清

WHY: Items 可能相互关联。部分理解 = 错误实现。
```

**澄清示例（协作式语气，来自 awesome-skills）：**
```
Reviewer: "Fix items 1-6"
你理解 1,2,3,6，不理解 4,5

❌ 错误：先实现 1,2,3,6，稍后问 4,5
✅ 正确："理解 items 1,2,3,6。需要澄清 4 和 5 后再实施：
  - item 4：你指的是修改 A 函数还是 B 函数？
  - item 5：这里的'优化'是指性能还是可读性？"
```

### Step 2: 生成《修复计划》

按优先级排序，生成结构化修复计划：

```yaml
fix_plan:
  task_id: "{对应 review_request.task_id}"
  total_issues: 5
  blocking: 1
  important: 1
  nit: 1
  suggestion: 1
  items:
    - id: "B1"
      severity: blocking
      action: "fix"          # fix | pushback | defer
      approach: "{具体修复方案}"
      files: ["src/middleware/auth.py"]
      test_required: true
      estimated_time: "10min"
    - id: "S1"
      severity: suggestion
      action: "defer"
      defer_reason: "需要引入 Redis，超出本次范围"
      follow_up_task: "task-005"
  execution_order: ["B1", "I1", "N1"]
```

**执行纪律（来自 obra + addyosmani）：**
- 一次只改一项，改完测完再改下一项
- 如果修复引入新 issue，立即停止，重新进入 REVIEWING
- 不接受 "I'll fix it later" — 经验证明 deferred cleanup 很少发生
- 每项修复后运行相关测试

### Step 3: 处理死代码清理（来自 addyosmani）

如果审查意见书包含 `dead_code_identified`：
1. 逐一验证是否确实无引用
2. 询问用户："以下死代码已确认无引用，是否删除：{list}？"
3. 用户确认后删除，不静默删除不确定的代码

### Step 4: 处理依赖审查（来自 addyosmani）

如果审查意见书包含 `new_dependencies` 问题：
1. 检查现有栈是否能解决同样需求
2. 检查依赖体积、维护状态、漏洞、许可证
3. 如建议移除依赖，给出替代方案

### Step 5: 状态回写与复查触发

修复完成后，pipeline 自动：
1. 将状态置为 VERIFYING
2. 再次调用 `code-reviewer` Skill 复查（仅审查修改过的文件）
3. 输出《复查报告》

## 与 obra 原版的差异

| 原版 obra | 融合版 |
|----------|--------|
| 面向人类 reviewer 的响应礼仪 | 面向 AI 自检 + 结构化 pipeline |
| 禁止表演式认同（保留） | 保留：禁止"Great point!"、"You're absolutely right!" |
| 无固定输出格式 | 增加 fix_plan YAML 结构化输出 |
| 无状态概念 | 增加 execution_order 优先级排序 |
| 人工判断下一步 | 增加状态回写指令（自动触发 VERIFYING） |
| 无进度追踪 | 集成 docs/progress.md 和 docs/decisions.md |
| 无死代码/依赖处理 | 增加 addyosmani 的死代码清理和依赖审查流程 |

## 禁止响应（保留 obra 核心规则）

**NEVER：**
- "You're absolutely right!"（表演式认同）
- "Great point!" / "Excellent feedback!"（表演式）
- "Let me implement that now"（未验证就实施）
- "Thanks for catching that!"（感谢用语）
- "I'll clean it up later"（延期清理 — 来自 addyosmani）

**INSTEAD：**
- 陈述技术事实："Fixed. 将 SECRET_KEY 移至环境变量。"
- 有理有据反驳："This suggestion breaks backward compat because..."
- 直接展示代码：修改后的 diff 就是最好的回应
- 需要澄清时：具体提问
- 对 suggestion："Defer to task-005: 需要引入 Redis，超出本次范围。"

## 处理外部 Reviewer 反馈

如果审查意见来自外部（非自检）：
1. 检查：是否适合 THIS 代码库？
2. 检查：是否破坏现有功能？
3. 检查：与当前架构决策是否冲突？
4. 如果冲突：先与你的 human partner（用户）确认，不擅自决定
5. 如果外部 reviewer 错误：用技术推理反驳，引用工作测试/代码证明

## Gotchas

- **不理解就停**：任何 item 只要存在理解模糊，必须澄清后再实施。部分理解 = 错误实现。
- **一次只改一项**：不要批量修改所有问题后再测试。逐项修复、逐项验证。
- **修复引入新问题**：如果在修复过程中发现新问题或引入回归，立即停止当前修复，重新进入审查流程。
- **延期不是忽略**：defer 必须有明确的 follow_up_task 和理由，记录在 docs/decisions.md 中。
- **死代码不静默删除**：即使 reviewer 标记为死代码，也要自己 grep 确认无引用后再删除。
- **表演式认同是垃圾信息**：在结构化输出中禁止一切情感化回应，只陈述技术事实。
- **外部反馈需适配**：外部 reviewer 不了解项目全部上下文，冲突时必须与用户确认。
