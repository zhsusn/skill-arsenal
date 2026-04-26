# 真实场景用例示例

常见场景下 AI 架构的综合示例，包含详细的实现指导。

## 目录

1. [代码质量与审查](#代码质量--审查)
2. [功能开发](#功能开发)
3. [文档](#文档)
4. [测试与质量保证](#测试--质量保证)
5. [重构与现代化](#重构--现代化)
6. [安全与合规](#安全--合规)
7. [DevOps 与自动化](#devops--自动化)
8. [数据分析](#数据分析)
9. [客户支持](#客户支持)
10. [内容生成](#内容生成)

---

## 代码质量 & 审查

### 用例 1：自动化代码审查系统

**需求：**
- 自动审查所有 PR
- 检查编码规范
- 识别安全问题
- 提出改进建议
- 保持团队一致性

**复杂度分析：**
- 任务复杂度：6（结构化工作流）
- 可复用性：8（组织级）
- 上下文：5（需要编码规范）
- 安全性：5（读取操作）

**推荐架构：** **Skills + 直接提示**

**实现：**

**1. 创建 code-review-expert skill：**
```
code-review-expert/
├── SKILL.md
├── references/
│   ├── coding_standards.md
│   ├── security_patterns.md
│   ├── performance_guidelines.md
│   └── review_checklist.md
└── scripts/
    └── review_pr.sh
```

**2. PR 使用方式：**
```
简单 PR（< 50 行）：
  → 直接提示
  "Using code-review-expert skill, review PR #123"

复杂 PR（> 500 行）：
  → Agent + Skill
  Review Agent:
    - Load code-review-expert skill
    - Analyze all changed files
    - Generate comprehensive review
```

**3. coding_standards.md：**
```markdown
# Team Coding Standards

## TypeScript
- Use strict mode
- Explicit return types
- No `any` types
- Prefer const over let
- 100 character line limit

## Patterns
- Repository pattern for data access
- Dependency injection for services
- Factory pattern for object creation

## Security
- Validate all inputs
- Sanitize user data
- Use parameterized queries
- Never log sensitive data
```

**4. 审查工作流：**
```bash
#!/bin/bash
# review_pr.sh

PR_NUMBER=$1

echo "Reviewing PR #$PR_NUMBER..."

# Get PR diff
gh pr diff $PR_NUMBER > /tmp/pr_diff.txt

# Review with Claude + skill
claude "Using code-review-expert skill, review this PR:

Changes:
$(cat /tmp/pr_diff.txt)

Check for:
1. Coding standards compliance
2. Security vulnerabilities
3. Performance issues
4. Best practices adherence
5. Test coverage

Format: Provide detailed review with specific line numbers and suggestions."
```

**收益：**
- 审查一致性
- 强制执行团队规范
- 可复用于所有 PR
- 快速反馈

**指标：**
- 审查时间：2-5 分钟
- 覆盖率：100% PR
- 误报率：< 5%
- 开发者满意度：高

---

### 用例 2：代码质量仪表盘

**需求：**
- 分析整个代码库
- 追踪历史指标趋势
- 识别问题区域
- 生成报告

**推荐架构：** **并行 Agents**

**实现：**

```
Quality Dashboard Workflow

Coordinator Agent
│
├─┬─ Complexity Agent → Analyze code complexity
│ │
│ ├─ Coverage Agent → Check test coverage
│ │
│ ├─ Security Agent → Find vulnerabilities
│ │
│ └─ Duplication Agent → Detect code duplication
│
└─→ Dashboard Agent → Generate visual report

All agents run in parallel → 4x faster
```

**代码：**
```typescript
// Launch parallel agents
const [
  complexityReport,
  coverageReport,
  securityReport,
  duplicationReport
] = await Promise.all([
  analyzeComplexity(codebase),
  analyzeCoverage(codebase),
  analyzeSecurity(codebase),
  analyzeDuplication(codebase)
]);

// Aggregate results
const dashboard = generateDashboard({
  complexity: complexityReport,
  coverage: coverageReport,
  security: securityReport,
  duplication: duplicationReport
});
```

---

## 功能开发

### 用例 3：全栈功能实现

**需求：**
- 实现用户认证
- 前端 + 后端 + 数据库
- 测试与文档
- 部署到预发布环境

**推荐架构：** **专家 Agent 团队 + Skills**

**实现：**

```
Project Lead Agent
│
├── Frontend Agent
│   Load: frontend-designer-skill
│   Tasks:
│   - Create login/signup components
│   - Add form validation
│   - Implement token storage
│   - Add loading states
│
├── Backend Agent
│   Load: api-design-expert-skill
│   Tasks:
│   - Create auth endpoints
│   - Implement JWT generation
│   - Add refresh token logic
│   - Database queries
│
├── Database Agent
│   Load: database-expert-skill
│   Tasks:
│   - Design user schema
│   - Create migrations
│   - Add indexes
│   - Seed test data
│
├── Testing Agent
│   Load: testing-strategies-skill
│   Tasks:
│   - Unit tests
│   - Integration tests
│   - E2E tests
│   - Coverage reports
│
└── DevOps Agent
    Load: deployment-expert-skill
    Tasks:
    - Update configs
    - Deploy to staging
    - Run smoke tests
    - Monitor deployment
```

**执行：**
```
Phase 1: Planning (Sequential)
  Lead Agent creates detailed plan

Phase 2: Implementation (Parallel)
  All specialist agents work simultaneously
  - Frontend: 15 minutes
  - Backend: 15 minutes
  - Database: 10 minutes
  - Tests: 20 minutes
  Total: 20 minutes (vs 70 minutes sequential)

Phase 3: Integration (Sequential)
  Lead Agent coordinates integration

Phase 4: Deployment (Sequential)
  DevOps Agent deploys to staging
```

**收益：**
- 并行执行（提速 70%）
- 每层具备专业 expertise
- 全面的测试覆盖
- 自动化部署

---

### 用例 4：功能开关系统

**需求：**
- 添加功能开关能力
- 最小风险实现
- 支持灰度发布
- 集成分析统计

**推荐架构：** **Skills + 多阶段 Agents**

**实现：**

```
Phase 1: Exploration Agent
  Tools: [Read, Grep, Glob]
  Load: architecture-patterns-skill
  Task:
    - Analyze current architecture
    - Identify integration points
    - Research feature flag patterns
    - Assess risk areas

Phase 2: Design Agent
  Tools: [TodoWrite]
  Load: system-design-skill
  Task:
    - Design feature flag service
    - Plan database schema
    - Define API contracts
    - Create rollout strategy

Phase 3: Implementation Agent
  Tools: [Read, Edit, Write]
  Load: coding-standards-skill
  Task:
    - Implement feature flag service
    - Add database migrations
    - Create admin UI
    - Write documentation

Phase 4: Testing Agent
  Tools: [Bash, Read]
  Load: testing-strategies-skill
  Task:
    - Unit tests
    - Integration tests
    - Load testing
    - Rollback testing

Phase 5: Deployment Agent
  Tools: [Bash]
  Load: deployment-patterns-skill
  Confirmations: ['deployment', 'database migration']
  Task:
    - Deploy to staging
    - Run validation tests
    - Deploy to production (10% users)
    - Monitor metrics
```

---

## 文档

### 用例 5：API 文档生成器

**需求：**
- 从代码生成 API 文档
- 包含示例
- 文档与代码保持同步
- 多种输出格式

**推荐架构：** **Skills**

**实现：**

```
api-documentation-skill/
├── SKILL.md
├── references/
│   ├── openapi_spec.md
│   ├── documentation_guidelines.md
│   └── example_formats.md
├── templates/
│   ├── endpoint_template.md
│   ├── schema_template.md
│   └── example_template.md
└── scripts/
    └── generate_docs.sh
```

**使用方式：**
```
Using api-documentation-skill, generate complete API
documentation for all endpoints in src/api/

Include:
- OpenAPI spec
- Request/response examples
- Authentication details
- Error responses
- Rate limiting info

Format: Markdown with code examples
```

**输出：**
```markdown
# User API

## POST /api/users

Create a new user account.

### Request
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "name": "John Doe"
}
```

### Response (201 Created)
```json
{
  "id": "usr_123",
  "email": "user@example.com",
  "name": "John Doe",
  "createdAt": "2025-01-15T10:30:00Z"
}
```

### Errors
- 400: Invalid email format
- 409: Email already exists
- 429: Rate limit exceeded
```

---

### 用例 6：入职文档

**需求：**
- 帮助新开发者快速上手
- 多种学习路径
- 交互式教程
- 与代码库保持同步

**推荐架构：** **渐进式披露 Skill**

**实现：**

```
onboarding-guide/
├── SKILL.md
├── index.md (learning paths)
├── getting_started/
│   ├── day_1.md
│   ├── day_2.md
│   └── week_1.md
├── by_role/
│   ├── frontend_dev.md
│   ├── backend_dev.md
│   └── fullstack_dev.md
├── by_topic/
│   ├── architecture.md
│   ├── deployment.md
│   └── testing.md
└── interactive/
    ├── setup_walkthrough.sh
    └── first_pr_guide.sh
```

**渐进式披露：**
```
New developer: "I'm a frontend developer, where do I start?"

1. Load: index.md
   → Shows: Learning paths

2. Load: by_role/frontend_dev.md
   → Shows: Frontend-specific onboarding

3. Load: getting_started/day_1.md
   → Shows: Day 1 tasks

4. As they progress:
   → Load additional topics on demand
```

---

## 测试 & 质量保证

### 用例 7：综合测试套件生成器

**需求：**
- 为新功能生成测试
- 多种测试类型
- 高覆盖率目标
- 与 CI/CD 集成

**推荐架构：** **Agent + Skills**

**实现：**

```
Test Generation Agent
│
Load Skills:
├── testing-strategies-skill
└── code-analysis-skill

Workflow:
1. Analyze code to test
2. Identify test scenarios
3. Generate unit tests
4. Generate integration tests
5. Generate E2E tests
6. Verify coverage > 80%
```

**示例：**
```
Using testing-strategies-skill, generate comprehensive test suite
for UserService class:

Coverage requirements:
- Unit tests: 90%+
- Integration tests: All API endpoints
- E2E tests: Critical user flows

Test frameworks:
- Jest for unit/integration
- Playwright for E2E

Include:
- Happy paths
- Error cases
- Edge cases
- Security tests
```

**生成输出：**
```typescript
// user-service.test.ts
describe('UserService', () => {
  describe('createUser', () => {
    it('should create user with valid data', async () => {
      // Test implementation
    });

    it('should reject invalid email', async () => {
      // Test implementation
    });

    it('should reject duplicate email', async () => {
      // Test implementation
    });

    it('should hash password', async () => {
      // Test implementation
    });
  });

  // ... more tests
});
```

---

### 用例 8：回归测试套件维护

**需求：**
- 保持测试最新
- 移除过时测试
- 针对 API 变更更新
- 修复不稳定测试

**推荐架构：** **多阶段 Agents**

**实现：**

```
Phase 1: Analysis Agent
  - Identify failing tests
  - Find flaky tests
  - Detect obsolete tests
  - Check coverage gaps

Phase 2: Cleanup Agent
  - Remove obsolete tests
  - Update outdated assertions
  - Fix broken imports

Phase 3: Enhancement Agent
  - Improve flaky tests
  - Add missing test cases
  - Increase coverage

Phase 4: Validation Agent
  - Run full test suite
  - Verify improvements
  - Generate report
```

---

## 重构 & 现代化

### 用例 9：遗留代码现代化

**需求：**
- 从 JavaScript 升级到 TypeScript
- 更新已弃用 API
- 提升代码质量
- 保持功能不变

**推荐架构：** **多阶段 Agents + Skills**

**实现：**

```
Modernization Pipeline

Phase 1: Assessment Agent
  Load: code-quality-skill
  - Analyze current codebase
  - Identify modernization opportunities
  - Assess risk levels
  - Create priority list

Phase 2: Planning Agent
  Load: refactoring-patterns-skill
  - Create detailed migration plan
  - Define phases and milestones
  - Identify dependencies
  - Plan rollback strategy

Phase 3: TypeScript Migration Agent
  Load: typescript-migration-skill
  - Convert .js to .ts
  - Add type definitions
  - Fix type errors
  - Update build config

Phase 4: API Update Agent
  Load: api-modernization-skill
  - Replace deprecated APIs
  - Update to new patterns
  - Modernize syntax
  - Optimize performance

Phase 5: Testing Agent
  Load: testing-strategies-skill
  - Run existing tests
  - Add new tests
  - Verify functionality
  - Check performance

Phase 6: Validation Agent
  - Compare behavior (before/after)
  - Run regression tests
  - Performance benchmarks
  - Generate migration report
```

**安全措施：**
```
- Git branch per phase
- Tests after each phase
- Rollback capability
- Progressive rollout
- Monitoring and alerts
```

---

### 用例 10：微服务拆分

**需求：**
- 从单体应用中拆分服务
- 最小化停机时间
- 数据迁移
- 灰度发布

**推荐架构：** **SDK 自定义工作流**

**实现：**

```typescript
const microserviceExtraction = {
  phases: [
    {
      name: 'Analysis',
      agent: analysisAgent,
      tasks: [
        'Identify service boundaries',
        'Map dependencies',
        'Plan data separation',
        'Design API contracts'
      ]
    },
    {
      name: 'Preparation',
      agent: prepAgent,
      tasks: [
        'Create new service structure',
        'Set up database',
        'Implement API',
        'Add monitoring'
      ]
    },
    {
      name: 'Migration',
      agent: migrationAgent,
      confirmations: ['database migration', 'traffic routing'],
      tasks: [
        'Migrate data',
        'Deploy service',
        'Route 10% traffic',
        'Monitor metrics'
      ]
    },
    {
      name: 'Validation',
      agent: validationAgent,
      tasks: [
        'Compare responses',
        'Check performance',
        'Verify data consistency',
        'Gradual increase to 100%'
      ]
    }
  ]
};
```

---

## 安全 & 合规

### 用例 11：安全审计系统

**需求：**
- 自动化安全扫描
- OWASP 合规
- 漏洞检测
- 修复指导

**推荐架构：** **专家 Agents + 安全 Skill**

**实现：**
```
Security Audit Coordinator
│
├── OWASP Scanner Agent
│   Load: owasp-security-skill
│   Check: OWASP Top 10 vulnerabilities
│
├── Dependency Scanner Agent
│   Load: dependency-security-skill
│   Check: Vulnerable dependencies
│
├── Code Scanner Agent
│   Load: secure-coding-skill
│   Check: Code vulnerabilities
│
├── Config Scanner Agent
│   Load: secure-config-skill
│   Check: Insecure configurations
│
└── Report Agent
    Aggregate: All findings
    Prioritize: By severity
    Recommend: Remediation steps
```

**安全 Skill 结构：**
```
owasp-security-skill/
├── SKILL.md
├── references/
│   ├── owasp_top_10_2024.md
│   ├── vulnerability_patterns.md
│   ├── remediation_guides.md
│   └── secure_coding_practices.md
└── checklist/
    ├── injection.md
    ├── authentication.md
    ├── sensitive_data.md
    └── ...
```

---

## DevOps & 自动化

### 用例 12：CI/CD 流水线生成器

**需求：**
- 生成 CI/CD 流水线
- 多平台支持（GitHub、GitLab 等）
- 内置最佳实践
- 可定制工作流

**推荐架构：** **Skills**

**实现：**

```
cicd-generator-skill/
├── SKILL.md
├── references/
│   ├── pipeline_patterns.md
│   ├── best_practices.md
│   └── optimization_tips.md
├── templates/
│   ├── github_actions/
│   │   ├── basic.yml
│   │   ├── advanced.yml
│   │   └── monorepo.yml
│   ├── gitlab_ci/
│   └── jenkins/
└── scripts/
    └── generate_pipeline.sh
```

**使用方式：**
```
Using cicd-generator-skill, generate GitHub Actions pipeline for:

Project type: Node.js API
Requirements:
- Lint on PR
- Run tests (unit, integration)
- Build Docker image
- Deploy to staging (on main branch)
- Deploy to production (on release tag)
- Security scanning
- Code coverage reports

Include:
- Caching for faster builds
- Parallel jobs where possible
- Proper secrets management
```

**生成流水线：**
```yaml
name: CI/CD Pipeline

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]
    tags: ['v*']

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
      - run: npm ci
      - run: npm run lint

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
      - run: npm ci
      - run: npm test -- --coverage
      - uses: codecov/codecov-action@v3

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm audit
      - uses: snyk/actions/node@master

  # ... more jobs
```

---

## 数据分析

### 用例 13：日志分析与洞察

**需求：**
- 分析应用日志
- 识别模式
- 检测异常
- 生成洞察

**推荐架构：** **Agents + 渐进式披露 Skill**

**实现：**

```
Log Analysis Pipeline

1. Collection Agent
   - Gather logs from various sources
   - Normalize formats
   - Filter relevant entries

2. Pattern Recognition Agent
   Load: log-analysis-patterns-skill
   - Identify error patterns
   - Find performance bottlenecks
   - Detect security threats
   - Track user behavior

3. Anomaly Detection Agent
   - Compare against baselines
   - Flag unusual patterns
   - Assess severity

4. Insights Agent
   - Aggregate findings
   - Generate recommendations
   - Create visualizations
   - Prioritize actions
```

**日志分析 Skill：**
```
log-analysis-patterns-skill/
├── patterns/
│   ├── error_patterns.md
│   ├── performance_patterns.md
│   ├── security_patterns.md
│   └── user_behavior_patterns.md
└── insights/
    ├── common_issues.md
    └── remediation_steps.md
```

---

## 内容生成

### 用例 14：技术博客文章生成器

**需求：**
- 根据功能生成博客文章
- SEO 优化
- 品牌声音一致性
- 包含代码示例

**推荐架构：** **Skills**

**实现：**

```
technical-blog-generator-skill/
├── SKILL.md
├── references/
│   ├── brand_voice.md
│   ├── seo_guidelines.md
│   ├── blog_structure.md
│   └── code_example_formats.md
├── templates/
│   ├── feature_announcement.md
│   ├── tutorial.md
│   ├── deep_dive.md
│   └── comparison.md
└── examples/
    └── published_posts.md
```

**使用方式：**
```
Using technical-blog-generator-skill, create a blog post about
our new API rate limiting feature:

Target audience: Backend developers
Tone: Technical but accessible
Include:
- Why rate limiting matters
- How to implement
- Code examples (Node.js, Python)
- Best practices
- Common pitfalls

SEO keywords: API rate limiting, request throttling, API security
```

---

## 总结

**按用例划分的关键模式：**

| 用例 | 架构 | 原因 |
|----------|-------------|-----|
| Code Review | Skills + Prompts | Reusable standards, simple workflow |
| Feature Development | Specialist Agents + Skills | Complex, multi-layer, parallel work |
| Documentation | Progressive Disclosure Skill | Large knowledge base, context efficiency |
| Testing | Agents + Skills | Autonomous generation, quality standards |
| Refactoring | Multi-Phase Agents | Complex, risky, needs validation |
| Security | Specialist Agents + Skills | Multiple scan types, expertise needed |
| CI/CD | Skills | Template generation, best practices |
| Data Analysis | Agents + Skills | Pattern recognition, insights |
| Content | Skills | Brand consistency, SEO requirements |

**决策框架：**
1. 分析你的需求
2. 匹配到相似的用例
3. 适配架构模式
4. 实现并迭代
5. 度量并优化

**提示：** 这些只是起点。根据你的具体需求和约束进行调整。
