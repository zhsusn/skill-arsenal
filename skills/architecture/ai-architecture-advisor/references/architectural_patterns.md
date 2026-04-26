# 架构模式

针对常见用例的成熟 AI 架构模式综合目录。

## 目录

1. [Skill 优先模式](#skills-first-patterns)
2. [基于 Agent 的模式](#agent-based-patterns)
3. [混合模式](#hybrid-patterns)
4. [SDK 自定义模式](#sdk-custom-patterns)
5. [渐进式披露模式](#progressive-disclosure-patterns)
6. [安全模式](#security-patterns)

---

## Skill 优先模式

### 模式 1：领域专家 Skill

**适用场景：**
- 需要特定领域知识
- 团队范围内共享专业知识
- 一致地应用各类模式

**结构：**
```
domain-expert-skill/
├── SKILL.md
├── references/
│   ├── core_concepts.md
│   ├── patterns/
│   │   ├── pattern_1.md
│   │   ├── pattern_2.md
│   │   └── pattern_3.md
│   ├── best_practices.md
│   └── examples/
│       ├── example_1.md
│       └── example_2.md
└── scripts/
    └── validate.sh
```

**示例：安全专家 Skill**
```
security-expert/
├── SKILL.md
├── references/
│   ├── owasp_top_10.md
│   ├── patterns/
│   │   ├── authentication.md
│   │   ├── authorization.md
│   │   ├── encryption.md
│   │   └── input_validation.md
│   ├── threat_models.md
│   └── examples/
│       ├── secure_api.md
│       └── secure_storage.md
└── scripts/
    └── security_audit.sh
```

**用法：**
```
Using the security-expert skill, review this authentication flow
for vulnerabilities following OWASP guidelines.
```

**优势：**
- 集中式专业知识
- 一致的安全审查
- 团队知识共享
- 安全模式的渐进式披露

---

### 模式 2：工作流自动化 Skill

**适用场景：**
- 可重复的多步骤工作流
- 团队范围流程标准化
- 交互式脚本执行

**结构：**
```
workflow-automation-skill/
├── SKILL.md
├── workflows/
│   ├── workflow_1.md
│   ├── workflow_2.md
│   └── workflow_3.md
├── scripts/
│   ├── step_1.sh
│   ├── step_2.sh
│   └── orchestrate.sh
└── templates/
    ├── template_1.md
    └── template_2.md
```

**示例：发布管理 Skill**
```
release-management/
├── SKILL.md
├── workflows/
│   ├── version_bump.md
│   ├── changelog_generation.md
│   ├── deployment.md
│   └── rollback.md
├── scripts/
│   ├── bump_version.sh
│   ├── generate_changelog.sh
│   ├── deploy.sh
│   └── release.sh (orchestrator)
└── templates/
    ├── changelog_template.md
    └── release_notes.md
```

**用法：**
```
Using the release-management skill, prepare a new release:
- Bump version to 2.1.0
- Generate changelog from commits
- Create release notes
```

**优势：**
- 标准化流程
- 减少错误
- 更快执行
- 团队一致性

---

### 模式 3：渐进式披露 Skill

**适用场景：**
- 庞大的知识库
- 上下文限制是关注点
- 基于查询的信息检索

**结构：**
```
progressive-skill/
├── SKILL.md
├── query_tool.sh
├── index.md (high-level navigation)
├── expertise/
│   ├── by_task/
│   │   ├── task_1.md
│   │   └── task_2.md
│   ├── by_category/
│   │   ├── category_1.md
│   │   └── category_2.md
│   └── quick_reference/
│       └── cheat_sheet.md
└── examples/
    └── contextualized_examples.md
```

**示例：API 设计 Skill**
```
api-design-expert/
├── SKILL.md
├── query_expertise.sh
├── index.md
├── expertise/
│   ├── by_task/
│   │   ├── rest_api.md
│   │   ├── graphql.md
│   │   └── webhooks.md
│   ├── by_concern/
│   │   ├── authentication.md
│   │   ├── rate_limiting.md
│   │   ├── versioning.md
│   │   └── documentation.md
│   └── quick_reference/
│       ├── http_methods.md
│       └── status_codes.md
└── examples/
    └── real_world_apis.md
```

**用法：**
```
Using api-design-expert, show me best practices for:
- RESTful resource design
- Authentication and authorization
- Rate limiting strategy
```

**查询流程：**
1. Agent 加载 index.md（高层概览）
2. Agent 识别相关任务："rest_api.md"
3. Skill 仅提供 REST API 模式
4. 如需认证，加载 authentication.md
5. 渐进式披露信息

**优势：**
- 最小化上下文占用
- 快速响应
- 可扩展的知识库
- 高效的 Token 消耗

---

## 基于 Agent 的模式

### 模式 4：多阶段 Agent 流水线

**适用场景：**
- 具有不同阶段的复杂工作流
- 每个阶段具有不同的工具权限
- 隔离的上下文是有益的

**结构：**
```
Main Agent (orchestrator)
│
├── Phase 1: Explore Agent
│   Tools: [Read, Grep, Glob]
│   Context: Codebase exploration
│   Output: Insights, patterns, structure
│
├── Phase 2: Plan Agent
│   Tools: [TodoWrite]
│   Context: Insights from Phase 1
│   Output: Detailed plan
│
├── Phase 3: Execute Agent
│   Tools: [Read, Edit, Write]
│   Context: Plan + target files
│   Output: Code changes
│
└── Phase 4: Validate Agent
    Tools: [Bash, Read]
    Context: Changes + tests
    Output: Validation results
```

**示例：功能实现**
```
Feature Implementation Pipeline

1. Explore Agent
   - Analyze existing codebase
   - Find related code patterns
   - Identify integration points
   → Output: Architecture analysis

2. Design Agent
   - Review analysis
   - Create detailed design
   - Plan file changes
   → Output: Implementation plan

3. Code Agent
   - Implement feature
   - Follow design plan
   - Write tests
   → Output: Code changes

4. Review Agent
   - Run tests
   - Check coverage
   - Validate functionality
   → Output: Pass/fail + feedback

5. Main Agent
   - Aggregate results
   - Report to user
   - Handle iterations
```

**用法：**
```
Implement a new user authentication feature:
1. Analyze current auth system
2. Design JWT-based auth
3. Implement changes
4. Validate with tests
```

**优势：**
- 清晰的阶段分离
- 每个阶段最小权限
- 隔离的上下文（无污染）
- 可并行执行
- 易于调试和迭代

---

### 模式 5：并行 Agent 执行

**适用场景：**
- 可独立运行的任务
- 大型代码库或数据集
- 时间敏感型操作

**结构：**
```
Coordinator Agent
│
├─┬─ Worker Agent 1: Task Subset 1
│ │
│ ├─ Worker Agent 2: Task Subset 2
│ │
│ ├─ Worker Agent 3: Task Subset 3
│ │
│ └─ Worker Agent 4: Task Subset 4
│
└── Aggregator Agent: Combine Results
```

**示例：代码库分析**
```
Analysis Coordinator
│
├─┬─ Analyze Agent 1: /src/components/
│ │  → Component patterns
│ │
│ ├─ Analyze Agent 2: /src/services/
│ │  → Service patterns
│ │
│ ├─ Analyze Agent 3: /src/utils/
│ │  → Utility patterns
│ │
│ └─ Analyze Agent 4: /tests/
│    → Test coverage
│
└── Aggregator Agent
    → Combined analysis report
```

**用法：**
```
Analyze entire codebase for:
- Code patterns
- Test coverage
- Performance issues
- Security vulnerabilities

Execute in parallel for speed.
```

**优势：**
- 极大提速（4 个 Agent 提升 4 倍）
- 独立执行
- 资源优化
- 可扩展至大型代码库

---

### 模式 6：专家 Agent 团队

**适用场景：**
- 需要不同专业领域
- 协作式任务执行
- 审查与验证工作流

**结构：**
```
Project Lead Agent (orchestrator)
│
├── Frontend Specialist Agent
│   Expertise: UI/UX, components, accessibility
│   Tools: Frontend-specific
│
├── Backend Specialist Agent
│   Expertise: APIs, databases, services
│   Tools: Backend-specific
│
├── DevOps Specialist Agent
│   Expertise: CI/CD, deployment, infrastructure
│   Tools: DevOps-specific
│
└── QA Specialist Agent
    Expertise: Testing, validation, quality
    Tools: Testing-specific
```

**示例：全栈功能**
```
Feature: Add user profile page

Project Lead Agent
│
├── Frontend Agent
│   - Create profile component
│   - Add routing
│   - Implement responsive design
│   Load: frontend-designer skill
│
├── Backend Agent
│   - Create profile API endpoint
│   - Add database queries
│   - Implement validation
│   Load: api-design-expert skill
│
├── DevOps Agent
│   - Update deployment config
│   - Add environment variables
│   - Configure monitoring
│   Load: devops-expert skill
│
└── QA Agent
    - Write integration tests
    - Validate end-to-end flow
    - Check accessibility
    Load: qa-test-planner skill
```

**用法：**
```
Implement user profile feature across the stack:
- Frontend: Profile page with edit capability
- Backend: CRUD API for profile data
- DevOps: Deploy to staging
- QA: Full test coverage
```

**优势：**
- 专业化知识
- 并行执行
- 按专家加载 Skill
- 职责清晰
- 全面覆盖

---

## 混合模式

### 模式 7：Agent + Skill 混合

**适用场景：**
- 需要领域专业知识的复杂工作流
- 可复用知识 + 自主执行
- 兼顾两种方案的优点

**结构：**
```
Agent Workflow
│
├── Explore Agent
│   Loads: codebase-analysis-skill
│   Expertise: Pattern recognition
│   Tools: [Read, Grep, Glob]
│
├── Plan Agent
│   Loads: architecture-patterns-skill
│   Expertise: Design patterns
│   Tools: [TodoWrite]
│
└── Execute Agent
    Loads: coding-standards-skill
    Expertise: Team conventions
    Tools: [Read, Edit, Write]
```

**示例：重构流水线**
```
Refactoring Workflow

1. Analysis Agent
   Load: code-quality-skill
   - Identify code smells
   - Find duplication
   - Analyze complexity
   Use skill's: anti-patterns reference

2. Planning Agent
   Load: refactoring-patterns-skill
   - Choose refactoring patterns
   - Plan step-by-step changes
   - Estimate risk
   Use skill's: safe refactoring strategies

3. Execution Agent
   Load: team-coding-standards-skill
   - Apply refactorings
   - Follow team style
   - Maintain tests
   Use skill's: style guide and examples

4. Validation Agent
   Load: testing-strategies-skill
   - Run test suite
   - Check coverage
   - Verify behavior
   Use skill's: test validation patterns
```

**用法：**
```
Refactor the UserService class:
- Load relevant skills for expertise
- Use agents for autonomous execution
- Progressive disclosure of skill knowledge
- Isolated contexts per phase
```

**优势：**
- 可复用的专业知识（Skill）
- 自主执行（Agent）
- 渐进式披露
- 隔离的上下文
- 两全其美

---

### 模式 8：Prompt + Skill 降级

**适用场景：**
- 由简入繁，逐步提升复杂度
- 大部分任务简单，部分复杂
- 成本优化

**结构：**
```
Task Router
│
├── Simple task? → Direct Prompt
│
├── Needs expertise? → Load Skill
│   └── Still simple? → Skill + Prompt
│   └── Complex? → Skill + Agent
│
└── Very complex? → Agents + Skills
```

**示例：代码审查系统**
```
Code Review Router

1. Check complexity
   - Small PR (< 50 lines)? → Direct Prompt
     "Review this PR for basic issues"

   - Medium PR (50-500 lines)? → Load Skill
     Using code-review-skill, review this PR
     Skill provides: checklist, patterns

   - Large PR (> 500 lines)? → Agent + Skill
     Review Agent loads code-review-skill
     - Explore codebase context
     - Apply review checklist
     - Generate comprehensive review
```

**优势：**
- 成本效益高（简单 → 便宜）
- 可扩展（复杂 → 强大）
- 灵活（自适应任务）
- 渐进增强

---

## SDK 自定义模式

### 模式 9：自定义工具集成

**适用场景：**
- 与专有系统集成
- 需要自定义工具
- 领域特定操作

**结构：**
```typescript
import { Agent, Tool } from 'claude-agent-sdk';

// Define custom tool
const customTool: Tool = {
  name: 'custom-tool',
  description: 'Interacts with proprietary system',
  execute: async (params) => {
    // Custom implementation
    return await proprietarySystem.call(params);
  }
};

// Create agent with custom tool
const agent = new Agent({
  tools: [customTool, ...standardTools],
  systemPrompt: 'You are an expert with custom-system access'
});
```

**示例：CRM 集成 Agent**
```typescript
// Custom CRM tools
const getCRMData: Tool = {
  name: 'get-crm-data',
  description: 'Fetch customer data from CRM',
  execute: async ({ customerId }) => {
    return await crmAPI.getCustomer(customerId);
  }
};

const updateCRMData: Tool = {
  name: 'update-crm-data',
  description: 'Update customer data in CRM',
  execute: async ({ customerId, data }) => {
    return await crmAPI.updateCustomer(customerId, data);
  }
};

// Agent with CRM access
const crmAgent = new Agent({
  tools: [getCRMData, updateCRMData],
  systemPrompt: `You are a CRM assistant with access to customer data.
    Help users query and update customer information.`
});
```

**用法：**
```typescript
const response = await crmAgent.run({
  task: 'Get customer data for customer ID 12345 and update their email'
});
```

**优势：**
- 直接系统集成
- 自定义业务逻辑
- 专有数据访问
- 细粒度控制

---

### 模式 10：自定义反馈循环

**适用场景：**
- 特定工作流需求
- 独特的验证逻辑
- 自定义迭代模式

**结构：**
```typescript
const customWorkflow = async (task: Task) => {
  let result;
  let iterations = 0;
  const maxIterations = 5;

  while (iterations < maxIterations) {
    // Step 1: Generate
    result = await agent.generate(task);

    // Step 2: Custom validation
    const validation = await customValidator(result);

    // Step 3: Custom decision
    if (validation.passed) {
      break; // Success
    }

    // Step 4: Custom feedback
    task = customFeedback(task, validation.issues);
    iterations++;
  }

  return result;
};
```

**示例：带自定义 Linter 的代码生成**
```typescript
const codeGenerationWorkflow = async (spec: Specification) => {
  let code;
  let attempt = 0;

  while (attempt < 3) {
    // Generate code
    code = await codeAgent.generate(spec);

    // Custom linter validation
    const lintResults = await customLinter.check(code);

    if (lintResults.errors.length === 0) {
      // Passed linting
      break;
    }

    // Custom feedback loop
    spec = addLintingFeedback(spec, lintResults.errors);
    attempt++;
  }

  // Custom post-processing
  code = await customFormatter.format(code);

  return code;
};
```

**优势：**
- 自定义验证逻辑
- 特定迭代模式
- 业务规则强制执行
- 独特的工作流

---

## 渐进式披露模式

### 模式 11：基于查询的披露

**适用场景：**
- 庞大的知识库
- 上下文优化至关重要
- 需要任务特定信息

**结构：**
```
skill/
├── SKILL.md (high-level overview)
├── query.sh (interactive query tool)
├── index.md (navigation)
└── content/
    ├── topic_1/
    │   ├── overview.md (loaded first)
    │   ├── detailed.md (on demand)
    │   └── examples.md (when requested)
    └── topic_2/
        ├── overview.md
        ├── detailed.md
        └── examples.md
```

**查询模式：**
```bash
# User queries skill
"Using skill, how do I implement authentication?"

# Skill loading strategy
1. Load: index.md (< 500 tokens)
   → Find relevant topic: authentication
2. Load: authentication/overview.md (< 1000 tokens)
   → Provides high-level guidance
3. If user needs more:
   Load: authentication/detailed.md
   → In-depth patterns
4. If user wants examples:
   Load: authentication/examples.md
   → Real code samples
```

**优势：**
- 最小初始上下文
- 按需加载更多内容
- 高效的 Token 使用
- 快速初始响应

---

### 模式 12：分层披露

**适用场景：**
- 具有深度的复杂主题
- 需要渐进式学习
- 多个专业水平

**结构：**
```
skill/
├── level_1_basics/
│   └── (fundamental concepts)
├── level_2_intermediate/
│   └── (common patterns)
├── level_3_advanced/
│   └── (complex techniques)
└── level_4_expert/
    └── (edge cases, optimization)
```

**披露流程：**
```
User: "Help me with caching"

Skill responds:
├─ Level 1: Basic caching concepts
│  User: "I know basics, show me patterns"
│
├─ Level 2: Common caching patterns
│  User: "Show me advanced optimization"
│
├─ Level 3: Cache optimization techniques
│  User: "What about distributed caching?"
│
└─ Level 4: Distributed caching strategies
```

**优势：**
- 适配用户专业水平
- 避免信息过载
- 渐进式深度
- 高效学习

---

## 安全模式

### 模式 13：Allowlist 安全模式

**适用场景：**
- 敏感操作
- 受控工具访问
- 安全关键型应用

**结构：**
```typescript
const secureAgent = new Agent({
  tools: allowlistOnly([
    'Read',      // Safe: read-only
    'Grep',      // Safe: read-only
    'Glob',      // Safe: read-only
  ]),
  denylist: [
    'rm -rf',
    'sudo',
    'curl',      // Could leak data
    'wget',      // Could leak data
  ],
  confirmations: [
    'git push',
    'deployment',
    'data deletion'
  ]
});
```

**示例：生产环境 Agent**
```typescript
const productionAgent = new Agent({
  name: 'production-agent',

  // Minimal permissions
  tools: [
    'Read',          // View configs
    'Grep',          // Search logs
  ],

  // Block dangerous operations
  denylist: [
    'rm',
    'delete',
    'drop',
    'truncate',
    'sudo',
    'chmod',
    'exec'
  ],

  // Require confirmation
  confirmations: [
    'restart service',
    'change config',
    'modify database'
  ],

  // Audit all operations
  audit: {
    enabled: true,
    logLevel: 'verbose',
    destination: 'security-log'
  }
});
```

**优势：**
- 默认拒绝所有
- 显式权限
- 敏感操作需确认
- 完整审计追踪

---

### 模式 14：纵深防御

**适用场景：**
- 高安全要求
- 需要多层安全
- 关键系统

**结构：**
```
Security Layers:

Layer 1: Tool Allowlist
  → Only approved tools

Layer 2: Command Validation
  → Validate command safety

Layer 3: Confirmation Required
  → Human approval for sensitive ops

Layer 4: Sandbox Execution
  → Isolated environment

Layer 5: Audit Logging
  → Full operation trail

Layer 6: Rollback Capability
  → Undo mechanism
```

**示例：金融系统 Agent**
```typescript
const financialAgent = new Agent({
  // Layer 1: Tool Allowlist
  tools: allowlistOnly(['Read', 'Grep']),

  // Layer 2: Command Validation
  preExecute: async (command) => {
    return await securityValidator.validate(command);
  },

  // Layer 3: Confirmation Required
  confirmations: 'all',

  // Layer 4: Sandbox
  sandbox: {
    enabled: true,
    isolated: true,
    networkBlocked: true
  },

  // Layer 5: Audit
  audit: {
    enabled: true,
    level: 'detailed',
    retention: '7years',
    immutable: true
  },

  // Layer 6: Rollback
  rollback: {
    enabled: true,
    autoSnapshot: true,
    quickRevert: true
  }
});
```

**优势：**
- 多层安全
- 防御各种威胁
- 满足合规要求
- 最高安全性

---

## 总结

根据需求选择模式：

**简单任务：** 直接 Prompt
**可复用专业知识：** Skill（模式 1-3）
**复杂工作流：** Agent（模式 4-6）
**兼顾两者：** 混合模式（模式 7-8）
**自定义需求：** SDK（模式 9-10）
**庞大知识库：** 渐进式披露（模式 11-12）
**安全关键：** 安全模式（模式 13-14）

**核心原则：** 由简入繁，仅在必要时增加复杂度。
