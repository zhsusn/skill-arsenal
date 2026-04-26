# SDD 章节深度解析

## 撰写有效的系统概述

系统概述应回答以下问题：
1. 本系统做什么？
2. 谁使用它？
3. 它与哪些系统交互？

**良好示例：**
> 认证服务负责用户身份验证和会话管理。它与用户服务集成以获取个人资料数据，与通知服务集成以发送安全警报。客户端应用（Web、移动端、API）通过 REST 端点与其交互。

**不良示例：**
> 本系统负责认证。

## 数据模型最佳实践

必须包含：
- 带约束的字段类型
- 可空性
- 索引
- 外键关系
- 默认值

```typescript
// Good
interface User {
  id: string;              // UUID, PK, indexed
  email: string;           // VARCHAR(255), unique, not null
  passwordHash: string;    // VARCHAR(255), not null
  role: 'user' | 'admin';  // ENUM, default 'user'
  createdAt: Date;         // TIMESTAMP, default now(), indexed
  deletedAt: Date | null;  // TIMESTAMP, nullable (soft delete)
}
```

## API 设计指南

1. 使用 RESTful 规范
2. 对 API 进行版本控制（`/api/v1/`）
3. 记录所有错误响应
4. 包含请求/响应示例

```typescript
// Document both success and error cases
/**
 * POST /api/v1/users
 *
 * Success (201):
 * { id: "uuid", email: "user@example.com", createdAt: "2025-01-10T00:00:00Z" }
 *
 * Error (400):
 * { error: "VALIDATION_ERROR", message: "Email is required", field: "email" }
 *
 * Error (409):
 * { error: "CONFLICT", message: "Email already exists" }
 */
```

## 时序图表示法（ASCII）

对于复杂流程，请使用 ASCII 时序图：

```
Client          API Gateway       Auth Service      Database
  |                 |                  |               |
  |-- Login Req -->|                  |               |
  |                 |-- Validate -->  |               |
  |                 |                  |-- Query -->  |
  |                 |                  |<-- User --   |
  |                 |<-- Token ----   |               |
  |<-- Response ---|                  |               |
```

## 组件图模式

### 分层架构
```
┌─────────────────────────────────────┐
│           Presentation Layer        │
│  (React Components, API Handlers)   │
├─────────────────────────────────────┤
│            Business Layer           │
│    (Services, Domain Logic)         │
├─────────────────────────────────────┤
│             Data Layer              │
│   (Repositories, ORM, Database)     │
└─────────────────────────────────────┘
```

### 微服务模式
```
┌──────────┐    ┌──────────┐    ┌──────────┐
│   Auth   │    │   User   │    │  Orders  │
│ Service  │    │ Service  │    │ Service  │
└────┬─────┘    └────┬─────┘    └────┬─────┘
     │               │               │
     └───────────────┼───────────────┘
                     │
              ┌──────┴──────┐
              │ API Gateway │
              └─────────────┘
```

## 错误处理模式

### 错误响应格式
```typescript
interface ErrorResponse {
  error: string;          // Machine-readable error code
  message: string;        // Human-readable message
  details?: Record<string, string>;  // Field-specific errors
  requestId?: string;     // For debugging
}
```

### 错误分类
| HTTP 状态码 | 使用场景 |
|-------------|----------|
| 400 | 验证错误，请求格式不正确 |
| 401 | 缺失或无效的认证 |
| 403 | 认证有效但权限不足 |
| 404 | 资源未找到 |
| 409 | 冲突（重复、版本不匹配） |
| 422 | 语义上无效（业务规则） |
| 500 | 意外服务器错误 |

## 安全考量

### 认证策略
- **JWT**：无状态，适用于 API，需包含过期时间
- **Sessions**：服务端状态，更易于吊销
- **OAuth**：第三方认证，委托给提供商

### 授权模式
- **RBAC**：基于角色的访问控制
- **ABAC**：基于属性的访问控制
- **Resource-based**：基于资源的权限

### 数据保护
- 对静态敏感数据进行加密（AES-256）
- 传输中的数据使用 TLS 1.3
- 使用 bcrypt 对密码进行哈希（成本因子 12+）
- 对输入进行清理以防止注入攻击

## 性能策略

### 缓存层级
1. **Browser cache**：静态资源（CSS、JS、图片）
2. **CDN**：地理分布式内容
3. **Application cache**：Redis/Memcached 用于热数据
4. **Database cache**：查询结果缓存

### 数据库优化
- 为频繁查询的字段建立索引
- 使用连接池
- 对大数据集实现分页
- 对于读密集型负载，考虑使用只读副本

## 详细设计模板

```markdown
### 7.X [Component Name] Design

#### Responsibilities
- [What this component is responsible for]
- [Single responsibility principle]

#### Interface
\`\`\`typescript
interface ComponentInterface {
  method1(input: Input): Promise<Output>;
  method2(id: string): Promise<void>;
}
\`\`\`

#### Dependencies
- [Service A] - for [purpose]
- [Library B] - for [purpose]

#### State Management
- [What state is maintained]
- [How state changes]

#### Error Handling
- [How errors are handled]
- [What errors are propagated]

#### Implementation Notes
- [Specific algorithms or patterns]
- [Edge cases to handle]
- [Performance considerations]
```

## 可追溯性矩阵示例

| 需求 | 设计组件 | 验证方式 |
|-------------|-----------------|--------------|
| REQ-001 | 用户表，/api/users 端点 | 集成测试 |
| REQ-002 | OAuth 服务，登录流程 | 端到端测试 |
| REQ-050 | 密码验证中间件 | 单元测试 |
