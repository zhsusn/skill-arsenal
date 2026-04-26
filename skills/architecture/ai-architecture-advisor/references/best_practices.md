# AI 架构最佳实践 (2025)

经过验证的、用于设计、构建和维护基于 AI 的系统的最佳实践。

## 目录

1. [核心设计原则](#核心设计原则)
2. [渐进式披露](#渐进式披露)
3. [上下文管理](#上下文管理)
4. [安全与防护](#安全与防护)
5. [性能优化](#性能优化)
6. [Skill 设计](#skill-设计)
7. [Agent 设计](#agent-设计)
8. [测试与验证](#测试与验证)
9. [维护与演进](#维护与演进)
10. [成本优化](#成本优化)

---

## 核心设计原则

### 1. 从简单开始，按需扩展复杂度

**原则：** 始终从满足需求的最简单方案开始。

**原因：** 避免过度工程化和不必要的复杂性。

**方法：**
```
Level 1: 尝试直接提示词
  └─ 有效？→ 完成
  └─ 太复杂？→ 继续

Level 2: 创建 Skill
  └─ 有效？→ 完成
  └─ 需要隔离？→ 继续

Level 3: 使用 Agent
  └─ 有效？→ 完成
  └─ 需要自定义工作流？→ 继续

Level 4: SDK 原语
  └─ 获得完全控制
```

**示例：**
```
任务：生成代码审查

❌ 错误：立即构建自定义 SDK Agent
✅ 正确：先尝试直接提示词

"Review this PR for:
- Code quality issues
- Security vulnerabilities
- Performance concerns"

如果不一致 → 创建 code-review skill
如果太复杂 → 使用多阶段 Agent
```

---

### 2. 渐进式披露优先

**原则：** 仅在需要时展示所需内容。

**原因：** 优化上下文使用、降低成本、提升性能。

**方法：**
```
按层级结构组织信息：
├── 索引/概览（始终加载）
├── 主题概览（按需加载）
├── 详细内容（请求时加载）
└── 示例（需要时加载）
```

**反模式：**
```markdown
❌ 不要：将整个 skill 倾倒进上下文

skill/
└── SKILL.md (100KB 的所有内容)
    → 上下文过载
    → 响应变慢
    → 成本高昂
```

**最佳实践：**
```markdown
✅ 要：按渐进式披露结构组织

skill/
├── SKILL.md (概览, 2KB)
├── index.md (导航, 1KB)
└── topics/
    ├── topic_1/
    │   ├── overview.md (1KB)
    │   └── details.md (请求时加载)
    └── topic_2/
        ├── overview.md (1KB)
        └── details.md (请求时加载)

初始加载总量：~4KB vs 100KB
```

---

### 3. 将上下文视为宝贵资源

**原则：** 将每个 token 视为宝贵且有限的资源。

**原因：** 上下文窗口存在限制和成本。

**上下文预算：**
```
大语言模型: 200K tokens
- 预留：50K 用于响应
- 可用：150K 用于上下文
- 明智地规划预算！
```

**最佳实践：**
- ✅ 仅加载必要信息
- ✅ 总结大型输出
- ✅ 使用渐进式披露
- ✅ 定期重置上下文
- ✅ 压缩重复信息
- ❌ 不要倾倒原始日志
- ❌ 不要加载未使用的参考资料
- ❌ 不要重复信息

---

### 4. 清晰、明确的指令

**原则：** 大语言模型对明确的指导响应最佳。

**原因：** 减少错误、提高一致性、获得更好结果。

**对比：**
```
❌ 模糊：
"Make the code better"

✅ 清晰：
"Refactor this function to:
1. Extract magic numbers to constants
2. Add type annotations
3. Improve variable names for clarity
4. Add error handling for edge cases
Format: Return only the refactored code"
```

**模板：**
```
<instructions>
TASK: [清晰的任务定义]

REQUIREMENTS:
- [具体需求 1]
- [具体需求 2]
- [具体需求 3]

OUTPUT FORMAT:
[期望的确切格式]

CONSTRAINTS:
- [约束 1]
- [约束 2]
</instructions>

<examples>
[2-3 个展示期望模式的示例]
</examples>
```

---

### 5. 安全设计

**原则：** 默认拒绝，采用白名单机制。

**原因：** 构建安全、可控的 AI 系统。

**安全检查清单：**
- [ ] 最小化工具权限
- [ ] 仅白名单批准的工具
- [ ] 拒绝危险命令
- [ ] 敏感操作需要确认
- [ ] 审计所有操作
- [ ] 实现回滚能力
- [ ] 验证所有输入
- [ ] 尽可能在沙箱中执行

**默认 Agent 安全配置：**
```typescript
const secureAgent = new Agent({
  // 默认拒绝
  tools: [],

  // 显式允许最小工具集
  allowlist: [
    'Read',   // 只读
    'Grep',   // 仅搜索
    'Glob'    // 仅查找
  ],

  // 阻止危险操作
  denylist: [
    'rm -rf',
    'sudo',
    'exec',
    'eval'
  ],

  // 需要确认
  confirmations: [
    'git push',
    'deployment',
    'data modification'
  ]
});
```

---

## 渐进式披露

### 模式：基于查询的披露

**最佳实践：**
```
skill/
├── SKILL.md
│   内容：高层概述
│   大小：< 2KB
│   用途：介绍 skill 能力
│
├── index.md
│   内容：导航/目录
│   大小：< 1KB
│   用途：引导可用主题
│
└── content/
    └── topic/
        ├── overview.md (优先加载)
        ├── details.md (按需加载)
        └── examples.md (请求时加载)
```

**加载策略：**
```
1. 初始加载：SKILL.md + index.md (~3KB)
2. 用户询问 "authentication"
3. 加载：authentication/overview.md (~1KB)
4. 用户需要详细信息
5. 加载：authentication/details.md (~3KB)
6. 用户想要示例
7. 加载：authentication/examples.md (~2KB)

总计：加载 9KB vs 一次性倾倒 50KB
节省：82% 上下文缩减
```

---

### 模式：分层专业知识

**最佳实践：**
```
expertise/
├── by_task/
│   ├── authentication.md
│   ├── api_design.md
│   └── testing.md
├── by_language/
│   ├── typescript.md
│   ├── python.md
│   └── rust.md
├── by_pattern/
│   ├── repository.md
│   └── factory.md
└── quick_reference/
    └── cheatsheet.md
```

**查询示例：**
```
"如何实现认证？" → 加载：by_task/authentication.md
"TypeScript 风格指南？" → 加载：by_language/typescript.md
"Repository pattern?" → 加载：by_pattern/repository.md
"快速命名规范？" → 加载：quick_reference/cheatsheet.md
```

---

## 上下文管理

### 最佳实践 1：定期重置上下文

**原因：** 长时间会话会积累无关上下文。

**何时重置：**
- 完成主要任务后
- 感觉上下文"臃肿"
- 响应变慢
- 接近 token 限制

**方法：**
```
选项 1：新会话
- 开始全新会话
- 提供先前工作的摘要

选项 2：显式重置请求
- 要求大语言模型忘记无关上下文
- 总结需要保留的关键点

选项 3：使用独立 Agent
- 不同任务使用不同 Agent
- 每个任务保持干净上下文
```

---

### 最佳实践 2：总结，不要倾倒

**反模式：**
```
❌ 不要：倾倒原始日志

"Here are the test results:"
[10,000 lines of test output]
```

**最佳实践：**
```
✅ 要：总结关键信息

"Test Results Summary:
- Total: 1,247 tests
- Passed: 1,245 (99.8%)
- Failed: 2
  - test_auth_token_expiration (line 456)
  - test_rate_limiting (line 789)
- Duration: 2m 34s"
```

---

### 最佳实践 3：压缩重复信息

**反模式：**
```
❌ 不要：重复相同信息

Task 1: "Following these coding standards: [full standards]"
Task 2: "Following these coding standards: [full standards]"
Task 3: "Following these coding standards: [full standards]"
```

**最佳实践：**
```
✅ 要：一次性引用，使用 skill

Task 1: Load: coding-standards-skill
Task 2: "Continue following loaded coding standards"
Task 3: "Continue following loaded coding standards"
```

---

## 安全与防护

### 最佳实践 1：最小权限

**原则：** 仅授予任务所需的最小工具集。

**示例：代码分析**
```typescript
const analysisAgent = new Agent({
  tools: [
    'Read',   // 读取代码
    'Grep',   // 搜索代码
    'Glob'    // 查找文件
  ]
  // 禁止 Write、Edit、Bash 等。
});
```

**示例：代码修改**
```typescript
const codeAgent = new Agent({
  tools: [
    'Read',   // 读取现有代码
    'Edit'    // 修改代码
  ]
  // 禁止 Bash（无法执行）
  // 禁止完整 Write（为安全起见使用 Edit）
});
```

---

### 最佳实践 2：敏感操作需要确认

**始终要求确认：**
- git push
- 部署命令
- 数据删除
- 系统修改
- 对生产环境的 API 调用
- 数据库变更

**实现：**
```typescript
const deployAgent = new Agent({
  confirmations: [
    'git push',
    'npm publish',
    'kubectl apply',
    'terraform apply',
    'aws',
    'gcloud'
  ]
});
```

---

### 最佳实践 3：审计日志

**原因：** 追踪所有 AI 操作以保障安全和调试。

**需要记录的内容：**
- 工具使用
- 执行的命令
- 修改的文件
- 发起的 API 调用
- 遇到的错误
- 用户确认

**实现：**
```typescript
const auditedAgent = new Agent({
  audit: {
    enabled: true,
    level: 'verbose',
    includeContext: true,
    destination: './logs/agent-audit.log',
    retention: '90days'
  }
});
```

---

## 性能优化

### 最佳实践 1：并行执行

**在可能的情况下，并行化：**

**反模式：**
```
❌ 串行（慢）：
1. Analyze file1.ts → 10s
2. Analyze file2.ts → 10s
3. Analyze file3.ts → 10s
Total: 30s
```

**最佳实践：**
```
✅ 并行（快）：
1. Analyze file1.ts ──┐
2. Analyze file2.ts ──┼→ 全部同时运行
3. Analyze file3.ts ──┘
Total: 10s (快 3 倍)
```

**实现：**
```
并行启动 3 个 Agent：
- Agent 1: file1.ts
- Agent 2: file2.ts
- Agent 3: file3.ts
聚合结果
```

---

### 最佳实践 2：缓存高频查询

**模式：**
```
skill/
└── cache/
    ├── frequently_asked.md
    └── common_patterns.md
```

**示例：**
```
常见查询："How to handle errors?"

无需每次重新处理：
1. 维护：error_handling.md 作为综合指南
2. 查询 → 立即加载缓存响应
3. 快速、一致的响应
```

---

### 最佳实践 3：优化 Token 使用

**Token 优化检查清单：**
- [ ] 使用渐进式披露
- [ ] 总结大型输出
- [ ] 移除冗余信息
- [ ] 压缩重复内容
- [ ] 在示例中使用更短的变量名
- [ ] 移除不必要的空白
- [ ] 引用外部文档而非嵌入

**示例：**
```
❌ 高 Token 使用：
const myVeryLongDescriptiveVariableName = 'value';
const anotherVeryLongDescriptiveVariableName = 'value';

✅ 优化后：
const user = 'value';
const data = 'value';
// 依然清晰，Token 更少
```

---

## Skill 设计

### 最佳实践 1：单一职责

**原则：** 每个 skill 应有一个清晰的目的。

**反模式：**
```
❌ 不要：做所有事的巨型 skill

super-skill/
├── frontend/
├── backend/
├── database/
├── devops/
└── testing/
→ 范围太广，上下文过载
```

**最佳实践：**
```
✅ 要：聚焦的 skill

frontend-expert/
├── components/
├── styling/
└── accessibility/

backend-expert/
├── apis/
├── services/
└── databases/
```

---

### 最佳实践 2：清晰文档

**Skill 文档模板：**
```markdown
---
name: skill-name
description: One-sentence description
---

# Skill Name

## 本 Skill 的功能
[2-3 句话解释用途]

## 何时使用
- ✅ 使用场景 1
- ✅ 使用场景 2
- ❌ 不适用于使用场景 3

## 快速开始
[简单示例]

## 参考资料
- file1.md - 描述
- file2.md - 描述

## 示例
[2-3 个具体示例]
```

---

### 最佳实践 3：Skill 版本管理

**原因：** 追踪变更、支持回滚、传达更新。

**结构：**
```
skill/
├── VERSION (例如, 2.1.0)
├── CHANGELOG.md
├── SKILL.md
└── references/
```

**CHANGELOG.md：**
```markdown
# Changelog

## [2.1.0] - 2025-01-15
### 新增
- 新模式：异步错误处理
- TypeScript 5.x 示例

### 变更
- 更新 REST API 指南

### 修复
- 修正认证示例

## [2.0.0] - 2024-12-01
### 破坏性变更
- 重组参考资料
```

---

## Agent 设计

### 最佳实践 1：清晰的 Agent 边界

**原则：** 每个 Agent 应有清晰、明确的职责。

**反模式：**
```
❌ 不要：做所有事的单体 Agent

BigAgent
├── 探索代码库
├── 规划变更
├── 执行变更
├── 运行测试
├── 部署
└── 监控
→ 职责过多，难以调试
```

**最佳实践：**
```
✅ 要：专业化 Agent

主编排器
├── 探索 Agent（只读）
├── 规划 Agent（规划）
├── 编码 Agent（实现）
├── 测试 Agent（验证）
└── 报告 Agent（聚合）
```

---

### 最佳实践 2：Agent 通信模式

**模式：父子**
```
Main Agent
│
├─→ Subagent 1: 任务
│   └─→ 返回：结果
│
├─→ Subagent 2: 任务
│   └─→ 返回：结果
│
└─→ Main 聚合结果
```

**模式：流水线**
```
Agent 1: 探索
  └─→ 输出：分析
      └─→ Agent 2: 规划
          └─→ 输出：计划
              └─→ Agent 3: 执行
                  └─→ 输出：变更
```

**模式：并行工作者**
```
Coordinator
├─┬─ Worker 1 ──┐
│ ├─ Worker 2 ──┤
│ ├─ Worker 3 ──┼→ Aggregator → Result
│ └─ Worker 4 ──┘
```

---

### 最佳实践 3：Agent 错误处理

**原则：** 优雅地失败和恢复。

**模式：**
```typescript
const resilientAgent = async (task) => {
  try {
    const result = await agent.run(task);
    return result;
  } catch (error) {
    // 记录错误
    logger.error('Agent failed', error);

    // 尝试恢复
    if (isRecoverable(error)) {
      return await retryWithBackoff(agent, task);
    }

    // 回退策略
    return await fallbackStrategy(task);
  }
};
```

---

## 测试与验证

### 最佳实践 1：测试 Skill

**需要测试的内容：**
- Skill 正确加载
- 参考资料可访问
- 示例有效
- 脚本成功执行

**示例：**
```bash
#!/bin/bash
# test_skill.sh

echo "Testing skill: $1"

# Test 1: Skill file exists
if [ ! -f "$1/SKILL.md" ]; then
  echo "❌ SKILL.md not found"
  exit 1
fi

# Test 2: References are valid
for ref in $1/references/*.md; do
  if [ ! -f "$ref" ]; then
    echo "❌ Reference missing: $ref"
    exit 1
  fi
done

# Test 3: Scripts are executable
for script in $1/scripts/*.sh; do
  if [ ! -x "$script" ]; then
    echo "❌ Script not executable: $script"
    exit 1
  fi
done

echo "✅ All tests passed"
```

---

### 最佳实践 2：验证 Agent 输出

**模式：**
```typescript
const validateAgentOutput = async (output) => {
  // 模式验证
  if (!matchesSchema(output)) {
    throw new Error('Invalid output schema');
  }

  // 业务逻辑验证
  if (!meetsRequirements(output)) {
    throw new Error('Output doesn\'t meet requirements');
  }

  // 安全检查
  if (containsDangerousContent(output)) {
    throw new Error('Output contains dangerous content');
  }

  return output;
};
```

---

## 维护与演进

### 最佳实践 1：定期更新 Skill

**计划：**
- 每月：审查并更新示例
- 每季度：针对新模式进行重大更新
- 每年：全面审查和重构

**更新检查清单：**
- [ ] 新增模式
- [ ] 移除已弃用模式
- [ ] 更新示例至当前版本
- [ ] 改进文档
- [ ] 纳入用户反馈
- [ ] 提升版本号
- [ ] 更新变更日志

---

### 最佳实践 2：弃用策略

**弃用时：**
```markdown
## [3.0.0] - 2025-06-01

### 已弃用
⚠️ 旧模式（已弃用，将在 4.0.0 中移除）：
[旧模式示例]

✅ 新模式（请改用）：
[新模式示例]

迁移指南：参见 MIGRATION.md
```

**弃用时间线：**
1. 宣布弃用（版本 N）
2. 同时维护两种模式（版本 N+1）
3. 移除旧模式（版本 N+2）

---

## 成本优化

### 最佳实践 1：Token 效率

**策略：**
- 使用渐进式披露（加载更少）
- 总结输出（更少 token）
- 缓存高频查询（复用）
- 压缩重复内容（去重）
- 在可能的情况下选择较小模型（轻量模型 vs 中型模型）

**示例：**
```
任务：简单语法错误修复

❌ 昂贵：对所有任务使用中型模型
成本：每次请求 $X

✅ 优化：对简单任务使用轻量模型
成本：每次请求 $X/5
节省：80%
```

---

### 最佳实践 2：模型选择

**根据复杂度选择模型：**

**轻量模型（快速、便宜）：**
- 简单查询
- 直接明确的任务
- 定义明确的操作
- 对成本敏感的应用

**中型模型（平衡）：**
- 中等复杂度
- 大多数通用任务
- 能力与成本的良好平衡
- 默认选择

**大型模型（强大、昂贵）：**
- 复杂推理
- 关键任务
- 高风险决策
- 质量优先于成本

---

## 总结检查清单

**设计阶段：**
- [ ] 从最简单方案开始
- [ ] 应用渐进式披露
- [ ] 规划上下文效率
- [ ] 设计安全边界
- [ ] 考虑性能需求

**实现阶段：**
- [ ] 遵循单一职责
- [ ] 实现清晰文档
- [ ] 添加版本控制
- [ ] 包含错误处理
- [ ] 添加审计日志

**测试阶段：**
- [ ] 测试 skill 加载
- [ ] 验证 agent 输出
- [ ] 检查安全控制
- [ ] 验证性能
- [ ] 测试边界情况

**维护阶段：**
- [ ] 定期更新
- [ ] 弃用策略
- [ ] 用户反馈闭环
- [ ] 成本监控
- [ ] 性能优化

---

**记住：** 最佳实践在不断演进。请持续关注 AI 领域的更新和社区模式。
