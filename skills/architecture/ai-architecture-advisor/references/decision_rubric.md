# 架构决策评分标准

为你的项目选择合适 AI 架构的综合框架。

## 概述

本评分标准从七个关键维度进行评估，推荐 Skill、Agent、Prompt 和 SDK 原语的最佳组合。

## 七个维度

### 1. 任务复杂度
### 2. 可复用性需求
### 3. 上下文管理
### 4. 安全与控制
### 5. 性能需求
### 6. 维护负担
### 7. 上市时间

---

## 1. 任务复杂度分析

### 低复杂度（评分：1-3）
**特征：**
- 单一操作或简单工作流
- 清晰的输入 → 输出映射
- 无依赖或极少依赖
- 线性执行（无分支）
- 最多 1-5 个步骤
- 可用一句话描述

**建议：** **直接 Prompt**

**示例：**
- "Explain this function"
- "Fix this typo"
- "Add a comment to this class"
- "Format this JSON"
- "Translate this error message"

**实现：**
```
Simple, clear instruction to Claude without additional structure
```

---

### 中复杂度（评分：4-6）
**特征：**
- 多个相关操作
- 带步骤的结构化工作流
- 步骤间存在一定依赖
- 需要参考资料或示例
- 5-20 个步骤
- 受益于组织性和指导性
- 可复用模式

**建议：** **Skills**

**示例：**
- Generate comprehensive code review
- Create design system component
- Write technical documentation with examples
- Analyze codebase for patterns
- Generate test suite following guidelines

**实现：**
```
skill/
├── SKILL.md (main documentation)
├── references/
│   ├── patterns.md
│   ├── examples.md
│   └── guidelines.md
└── scripts/ (optional)
    └── helper.sh
```

---

### 高复杂度（评分：7-9）
**特征：**
- 多步骤自主工作流
- 需要隔离上下文
- 并行执行有益
- 不同阶段有不同需求
- 20+ 步骤或多条并行轨迹
- 需要探索、规划、执行、验证
- 不同阶段需要不同的工具权限

**建议：** **Agents/Subagents**

**示例：**
- Full codebase refactoring
- Comprehensive security audit
- Multi-file feature implementation
- Documentation generation across entire project
- Performance optimization analysis and fixes

**实现：**
```
Main Agent (orchestrator)
├── Explore Subagent (read-only, analysis)
├── Plan Subagent (planning, no execution)
├── Execute Subagent (write permissions)
└── Validate Subagent (testing, verification)
```

---

### 自定义复杂度（评分：10）
**特征：**
- 独特的工作流需求
- 需要系统集成
- 需要自定义工具
- 特定的反馈循环
- 生产环境部署
- 需要细粒度控制

**建议：** **SDK 原语**

**示例：**
- Custom CI/CD integration
- Proprietary system automation
- Domain-specific code analysis
- Production AI features
- Specialized agent behaviors

**实现：**
```typescript
import { Agent, Tool } from 'claude-agent-sdk';

const customAgent = new Agent({
  tools: [customTool1, customTool2],
  workflow: customFeedbackLoop,
  integrations: [ciSystem, deploySystem]
});
```

---

## 2. 可复用性需求

### 单次使用（评分：1-2）
**特征：**
- 一次性任务
- 项目特定
- 预期未来不会复用
- 临时需求

**建议：** **直接 Prompt**

**示例：**
- Debug this specific bug
- Update this particular file
- Answer question about this code

---

### 个人复用（评分：3-4）
**特征：**
- 你会多次使用
- 个人工作流优化
- 不与团队共享

**建议：** **Skills（个人）**

**示例：**
- Your personal code review checklist
- Your preferred refactoring patterns
- Your documentation template

**存储：** 本地 `.claude/skills/` 目录

---

### 团队复用（评分：5-7）
**特征：**
- 多名团队成员受益
- 团队级模式
- 共享知识
- 协作价值

**建议：** **Skills（团队插件）**

**示例：**
- Team coding standards
- Project-specific patterns
- Shared workflows
- Team documentation templates

**存储：** 团队仓库插件

---

### 组织级复用（评分：8-9）
**特征：**
- 跨团队受益
- 公司级标准
- 多个项目
- 组织知识

**建议：** **Skills（组织市场）**

**示例：**
- Company coding standards
- Security review guidelines
- Architecture patterns
- Compliance requirements

**分发：** 内部市场

---

### 产品功能（评分：10）
**特征：**
- 面向终端用户
- 生产环境部署
- 产品差异化
- 收入影响

**建议：** **SDK 原语**

**示例：**
- AI-powered product feature
- Customer-facing automation
- Production workflow
- SaaS feature

**实现：** 自定义 SDK 集成

---

## 3. 上下文管理需求

### 最小上下文（评分：1-3）
**特征：**
- 自包含任务
- 无外部引用
- 所有信息都在 Prompt 中
- < 1000 tokens

**建议：** **直接 Prompt**

**示例：**
```
Explain this function:
[paste function]
```

---

### 结构化上下文（评分：4-6）
**特征：**
- 需要参考资料
- 信息有组织
- 渐进式披露有益
- 1K-10K tokens

**建议：** **渐进式披露的 Skills**

**示例：**
```
skill/
├── SKILL.md
└── references/
    ├── quick_reference.md (loaded first)
    ├── detailed_patterns.md (loaded on demand)
    └── examples.md (loaded when needed)
```

**模式：**
- 以最小上下文启动
- 按需加载更多
- 基于查询的检索

---

### 隔离上下文（评分：7-9）
**特征：**
- 关注点分离
- 避免上下文污染
- 并行执行
- 每个阶段有不同上下文
- 每个上下文 10K+ tokens

**建议：** **Agents/Subagents**

**示例：**
```
Explore Agent: Codebase context (read-only)
Plan Agent: Planning context (insights from explore)
Code Agent: Implementation context (plan + target files)
Review Agent: Validation context (changes + tests)
```

**优势：**
- 无上下文污染
- 边界清晰
- 并行执行
- 最优 token 使用

---

### 自定义上下文（评分：10）
**特征：**
- 特定的上下文处理
- 集成需求
- 自定义上下文来源
- 动态上下文加载

**建议：** **SDK 原语**

**示例：**
```typescript
const context = await customContextLoader({
  source: proprietarySystem,
  filter: taskSpecific,
  transform: domainFormat
});
```

---

## 4. 安全与控制需求

### 基础安全（评分：1-3）
**特征：**
- 只读操作
- 无敏感数据
- 标准防护足够
- 低风险

**建议：** **直接 Prompt + Skills**

**控制措施：**
- Standard Claude safety features
- 无需额外限制

---

### 受控访问（评分：4-6）
**特征：**
- 写操作
- 需要特定工具权限
- 部分敏感操作
- 中等风险

**建议：** **带工具限制的 Agents**

**控制措施：**
```typescript
Explore Agent: [Read, Grep, Glob]  // Read-only
Plan Agent: [TodoWrite]             // Planning only
Code Agent: [Read, Edit, Write]     // Code changes
Review Agent: [Bash, Read]          // Testing
```

**模式：**
- 白名单方式
- 最小权限
- 显式授权

---

### 高安全（评分：7-9）
**特征：**
- 敏感操作
- 合规要求
- 需要审计日志
- 高风险

**建议：** **带确认机制的 Agents**

**控制措施：**
```typescript
Agent {
  tools: allowlistOnly,
  confirmations: [
    'git push',
    'deployment',
    'data deletion',
    'sensitive operations'
  ],
  audit: true,
  denylist: dangerousCommands
}
```

**模式：**
- 默认拒绝所有
- 显式确认
- 审计所有操作
- 阻断危险命令

---

### 最高安全（评分：10）
**特征：**
- 生产系统
- 金融/医疗数据
- 监管合规
- 关键基础设施

**建议：** **SDK 原语 + 自定义安全**

**控制措施：**
```typescript
const secureAgent = new Agent({
  security: {
    denyAll: true,
    allowlist: minimalTools,
    mfa: true,
    audit: comprehensiveLogger,
    encryption: true,
    rateLimits: strict,
    monitoring: realtime,
    rollback: automatic
  }
});
```

---

## 5. 性能需求

### 标准性能（评分：1-3）
**特征：**
- 用户可以等待
- 非时间敏感
- 偶尔使用

**建议：** **任何方式均可**

---

### 快速响应（评分：4-6）
**特征：**
- 期望快速反馈
- 交互式使用
- 多次请求

**建议：** **渐进式披露的 Skills**

**优化：**
- 初始加载最小上下文
- 按需查询额外信息
- 缓存频繁查询

---

### 高性能（评分：7-9）
**特征：**
- 实时或近实时
- 并行执行有益
- 资源优化关键

**建议：** **Agents（并行执行）**

**优化：**
```
Parallel Subagents:
├── Agent 1: File 1-10
├── Agent 2: File 11-20
├── Agent 3: File 21-30
└── Agent 4: Aggregation

Execution: All run simultaneously
```

---

### 极致性能（评分：10）
**特征：**
- 生产 SLA 要求
- 亚秒级响应
- 高吞吐量
- 资源限制

**建议：** **SDK 原语 + 自定义优化**

**优化：**
```typescript
const optimizedAgent = new Agent({
  caching: aggressive,
  parallelization: maximum,
  contextCompression: true,
  earlyTermination: true,
  resourceLimits: optimized
});
```

---

## 6. 维护负担

### 低维护（评分：1-3）
**特征：**
- 设置后无需关注
- 需求稳定
- 极少更新

**建议：** **直接 Prompt（无维护）**

---

### 中等维护（评分：4-6）
**特征：**
- 定期更新
- 模式不断演进
- 团队贡献

**建议：** **Skills（易于更新）**

**维护：**
- 更新参考文档
- 添加新示例
- 版本控制友好
- 文档清晰

---

### 高维护（评分：7-9）
**特征：**
- 频繁更新
- 多名贡献者
- 需求不断演进

**建议：** **Skills + 版本控制**

**维护：**
```
skill/
├── CHANGELOG.md
├── VERSION
├── SKILL.md
└── references/
    └── (versioned docs)
```

---

### 自定义维护（评分：10）
**特征：**
- 自定义代码库
- 破坏性变更
- 集成更新
- 生产支持

**建议：** **SDK 原语（配合 CI/CD）**

**维护：**
```typescript
// Automated testing
// Version management
// Deployment pipeline
// Monitoring and alerts
```

---

## 7. 上市时间

### 即时（评分：1-3）
**特征：**
- 立即需要
- 无设置时间
- 快速见效

**建议：** **直接 Prompt**

**时间：** 秒到分钟

---

### 快速（评分：4-6）
**特征：**
- 小时到天数
- 可接受一定设置时间
- 复用性有价值

**建议：** **Skills**

**时间：** 创建需 1-4 小时

---

### 计划内（评分：7-9）
**特征：**
- 天数到周数
- 充分规划
- 复杂需求

**建议：** **Agents/Subagents**

**时间：** 设计和实现需 1-3 天

---

### 战略性（评分：10）
**特征：**
- 数周到数月
- 产品功能
- 完整开发周期

**建议：** **SDK 原语**

**时间：** 构建和部署需 1+ 周

---

## 决策矩阵

### 快速参考表

| 维度 | Prompt | Skills | Agents | SDK |
|-----------|---------|--------|--------|-----|
| **复杂度** | Low (1-3) | Medium (4-6) | High (7-9) | Custom (10) |
| **可复用性** | Single (1-2) | Team (5-7) | Org (8-9) | Product (10) |
| **上下文** | Minimal (1-3) | Structured (4-6) | Isolated (7-9) | Custom (10) |
| **安全** | Basic (1-3) | Controlled (4-6) | High (7-9) | Max (10) |
| **性能** | Standard (1-3) | Fast (4-6) | High (7-9) | Max (10) |
| **维护** | Low (1-3) | Medium (4-6) | High (7-9) | Custom (10) |
| **上市时间** | Immediate (1-3) | Quick (4-6) | Planned (7-9) | Strategic (10) |

---

## 项目评分

### 第一步：为每个维度评分
在 7 个维度上为你的项目打分（1-10）。

### 第二步：计算加权平均分
不同维度对你的使用场景可能有不同的重要性。

**默认权重：**
- 任务复杂度：25%
- 可复用性：20%
- 上下文管理：15%
- 安全：15%
- 性能：10%
- 维护：10%
- 上市时间：5%

### 第三步：解读评分

**平均分 1-3：** 直接 Prompt
- 简单、清晰的指令
- 无需额外结构

**平均分 4-6：** Skills
- 组织化的专业知识
- 渐进式披露
- 参考资料

**平均分 7-9：** Agents/Subagents
- 复杂工作流
- 隔离上下文
- 并行执行

**平均分 10：** SDK 原语
- 自定义实现
- 完全控制
- 生产环境部署

---

## 特殊情况

### 混合架构
**适用时机：** 评分跨越多个区间

**解决方案：** 组合多种方式
- 简单任务使用直接 Prompt
- 可复用的专业知识使用 Skills
- 复杂工作流使用 Agents

**示例：**
```
Project with scores:
- Complexity: 7 (Agents)
- Reusability: 5 (Skills)
- Context: 4 (Skills)
- Security: 6 (Skills/Agents)

Recommendation: Agents + Skills
- Use Agents for complex workflows
- Load Skills for domain expertise
- Direct Prompts for simple operations
```

---

## 决策树

```
Start
│
├─ Is it a simple, one-time task?
│  └─ YES → Direct Prompts
│  └─ NO → Continue
│
├─ Do you need reusable expertise?
│  └─ YES → Continue
│  └─ NO → Continue
│     │
│     ├─ Is it complex with multiple phases?
│     │  └─ YES → Agents
│     │  └─ NO → Direct Prompts
│
├─ Is it complex with isolated contexts needed?
│  └─ YES → Agents
│  └─ NO → Skills
│
├─ Is it a production feature or unique workflow?
│  └─ YES → SDK Primitives
│  └─ NO → Agents or Skills
│
└─ Default → Skills (best balance)
```

---

## 评估示例

### 示例 1：代码审查自动化

**评分：**
- 复杂度：5（结构化工作流）
- 可复用性：7（团队级）
- 上下文：5（参考资料）
- 安全：4（读操作）
- 性能：5（交互式）
- 维护：6（标准不断演进）
- 上市时间：5（设置需数小时）

**平均分：** 5.3

**建议：** **Skills**
- 创建 code-review skill
- 包含团队标准
- 渐进式披露指南
- 模式参考资料

---

### 示例 2：代码库迁移

**评分：**
- 复杂度：9（多阶段、自主执行）
- 可复用性：3（一次性迁移）
- 上下文：8（每阶段隔离）
- 安全：7（写操作）
- 性能：8（并行执行）
- 维护：3（临时性）
- 上市时间：7（充分规划）

**平均分：** 6.4

**建议：** **Agents**
- 尽管可复用性低，但复杂度要求使用 Agents
- Explore Agent：分析代码库
- Plan Agent：制定迁移策略
- Migrate Agent：执行变更
- Validate Agent：运行测试

---

### 示例 3：快速修复 Bug

**评分：**
- 复杂度：2（单次修复）
- 可复用性：1（一次性）
- 上下文：2（最小化）
- 安全：3（单文件变更）
- 性能：2（可以等待）
- 维护：1（无需维护）
- 上市时间：1（即时）

**平均分：** 1.7

**建议：** **直接 Prompt**
- 简单指令
- 快速执行
- 无额外开销

---

### 示例 4：AI 驱动的产品功能

**评分：**
- 复杂度：10（自定义工作流）
- 可复用性：10（产品功能）
- 上下文：10（自定义处理）
- 安全：9（生产环境）
- 性能：9（SLA 要求）
- 维护：10（持续支持）
- 上市时间：10（战略性）

**平均分：** 9.7

**建议：** **SDK 原语**
- 自定义 Agent 实现
- 生产级安全
- 完整的监控和控制
- 与产品集成

---

## 总结

使用本评分标准来：
1. **评分** —— 在 7 个维度上为项目打分
2. **计算** —— 加权平均分
3. **解读** —— 评分以获取建议
4. **验证** —— 使用决策树
5. **回顾** —— 评估示例

**核心原则：** 从简单开始，按需扩展复杂度。

**记住：** 最好的架构是满足你需求的最简单架构。
