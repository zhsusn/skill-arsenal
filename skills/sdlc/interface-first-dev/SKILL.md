---
name: interface-first-dev
description: 当用户提到'接口驱动'、'定义接口'、'生成API契约'、'OpenAPI'、'前后端并行'、'接口契约'、'mock接口'或需要基于详细设计文档生成标准化前后端接口契约时触发。贯彻"先契约、后编码"原则，输出可冻结的接口基准。
---

# Interface-First Development

基于详细设计文档自动推导 OpenAPI 3.1 接口契约、Mock 数据、Mock 服务配置及前后端并行开发计划。核心原则：**开始编码之前先定义并冻结前后端接口契约**。

## 适用场景

- detailed-design 阶段已完成，需要基于设计文档生成标准化接口契约
- 前后端团队需要并行开发，需通过 Mock 服务解耦依赖
- 用户要求生成 OpenAPI / Swagger 规范、Mock 数据或接口定义
- 需要明确前后端任务边界与联调计划

## 核心职责

1. 读取上游设计文档（design.md、db-schema.md、api-spec.md、state-machine.md），自动推导 RESTful 接口契约
2. 生成符合 OpenAPI 3.1 标准的 `openapi.yaml`，注入 RFC 7807 错误模型与标准分页结构
3. 生成按接口分组的 `mock-data.json`（正常路径 + 异常路径）
4. 输出 `mock-server-config.md`，提供 Prism / JSON Server 一键启动方案
5. 输出 `parallel-dev-plan.md`，明确前后端任务批次、接口依赖 DAG 与联调时间点
6. 所有产物自动保存到 `interface-contracts/`，完成后触发质量检查

## 前置条件

- `detailed-design` 已完成且产出物就绪：`design.md`、`db-schema.md`、`api-spec.md`
- 若涉及状态流转，需有 `state-machine.md`
- 若已有基线契约 `interface-contracts/openapi.yaml`，进入**扩展模式**（仅追加新模块端点）
- **硬性阻断**：`db-schema.md` 或 `design.md` 缺失时，提示"请先执行 detailed-design 完成数据库与模块设计"

## 处理流程

### Step 0：扫描上游文档

使用 Glob 扫描设计文档目录，读取：
- `design.md` → 模块职责、实体关系、资源边界
- `db-schema.md` → 表结构、字段类型、主外键、枚举值
- `api-spec.md` → 接口初稿（URL、Method、参数说明）
- `state-machine.md` → 状态定义、流转事件（可选）
- `05-non-functional.md` → 认证方式、安全约束

### Step 1：解析 db-schema.md → DTO Schemas

按模块分组生成 `components/schemas`：

| DB 类型 | OpenAPI Schema 映射 |
|---------|---------------------|
| `VARCHAR(n)` / `STRING` | `type: string`, `maxLength: n` |
| `INT` / `BIGINT` | `type: integer`, `format: int64`（BIGINT） |
| `DECIMAL(p,s)` | `type: number` |
| `BOOLEAN` / `TINYINT(1)` | `type: boolean` |
| `DATETIME` / `TIMESTAMP` | `type: string`, `format: date-time` |
| `JSON` | `type: object` |
| `ENUM(...)` | `type: string`, `enum: [...]` |

- 主键 / `created_at` / `updated_at` → `readOnly: true`
- `NOT NULL` → 加入 `required` 数组
- `CHECK`、`DEFAULT`、`UNIQUE` → 映射为字段约束或 description 标注
- 表名 `orders` → Schema `Order`（PascalCase，单数）
- 请求/响应分离：生成 `CreateOrderRequest`（无 id）和 `OrderResponse`（完整）

### Step 2：解析 state-machine.md → 状态流转端点

- 每个流转事件生成 `PATCH /{resources}/{id}/status` 或 `PATCH /{resources}/{id}/{event}`
- Request Body 包含 `status` 枚举字段 + 条件字段
- `operationId` 格式：`transition{Resource}{TargetStatus}`，如 `transitionOrderToPaid`
- 必须声明 `409 Conflict` 响应（非法状态流转）

### Step 3：解析 design.md + api-spec.md → 标准 CRUD

按模块生成标准 REST 端点集：

| 方法 | 路径 | 用途 |
|------|------|------|
| GET | `/{resources}` | 列表查询（分页） |
| POST | `/{resources}` | 创建 |
| GET | `/{resources}/{id}` | 详情 |
| PUT | `/{resources}/{id}` | 全量更新 |
| PATCH | `/{resources}/{id}` | 部分更新 |
| DELETE | `/{resources}/{id}` | 删除 |

- 若 `api-spec.md` 已有初稿，以其 URI 和方法为基准补全 Schema 引用和参数
- 集合端点必须实现分页（Cursor 或 Offset）

### Step 4：组装 OpenAPI 3.1（注入全局组件）

基础骨架：
```yaml
openapi: "3.1.0"
info:
  title: "{项目名} API"
  version: "1.0.0"
servers:
  - url: /api/v1
```

必须注入的全局组件：
- `components/schemas/CursorPage` — 标准分页响应
- `components/schemas/Problem` — RFC 7807 错误详情
- `components/responses/BadRequest`、`Unauthorized`、`NotFound`、`TooManyRequests`、`Conflict`
- `components/securitySchemes/BearerAuth`（若安全需求要求 JWT）

### Step 5：生成 Mock 数据

为每个 GET 端点生成至少 3 组示例：
- **正常路径**：完整有效数据
- **空状态**：空数组 / `null` 字段
- **边界状态**：超长字符串、最大值、特殊字符

为 POST/PATCH 端点生成请求体示例。输出格式：
```json
{
  "operationId": {
    "200": { ... },
    "400": { ... }
  }
}
```

### Step 6：生成 Mock 服务配置

输出 `mock-server-config.md`，包含：
- **Prism 方案（推荐）**：`npx @stoplight/prism-cli mock openapi.yaml -p 4010`
- **JSON Server 方案（备选）**：`npx json-server --watch mock-data.json`
- CORS 配置、延迟模拟、鉴权绕过说明
- 前端接入示例：`fetch('http://localhost:4010/api/v1/...')`

### Step 7：生成并行开发计划

输出 `parallel-dev-plan.md`，包含：
- **接口依赖 DAG**：无依赖接口标记为 P0（可先行）
- **前端任务边界**：基于 Mock 可独立完成的页面列表
- **后端任务边界**：需实现的真实接口列表（按 P0/P1/P2）
- **联调时间点**：前后端约定首次联调的接口批次
- **版本规划**：基线 `/api/v1`，破坏性变更走 `/api/v2`

### Step 8：自动保存

所有产物写入 `interface-contracts/`：
```
interface-contracts/
├── openapi.yaml
├── mock-data.json
├── mock-server-config.md
└── parallel-dev-plan.md
```

### Step 9：质量检查

内置检查：
- 所有 `$ref` 指向存在的 Schema
- 无重复 `operationId`
- 集合端点含分页参数
- 错误响应统一引用 `Problem`

外部检查（环境有 Node.js 时）：
- `npx @redocly/cli lint interface-contracts/openapi.yaml`
- 输出 `lint-report.md`

## 约束

### MUST DO
- 遵循 REST 原则：资源导向、正确使用 HTTP 方法
- 命名一致：字段 camelCase，URI kebab-case，全局统一
- 完整 OpenAPI 3.1：每个端点必须有 `operationId`、`summary`、`tags`
- 错误响应符合 RFC 7807，统一使用 `application/problem+json`，`type` 为稳定 URI
- 所有集合端点实现分页
- 文档化认证与授权方式
- 每个端点至少提供一个请求示例和一个响应示例
- 状态流转端点必须包含 `409 Conflict` 响应
- 基线 API 版本必须为 `/api/v1`

### MUST NOT DO
- URI 中不使用动词（用 `/orders/{id}`，不用 `/getOrder/{id}` 或 `/orders/{id}/cancel`）
- 不返回不一致的响应结构
- 不跳过错误码文档
- 不忽视 HTTP 状态码语义（201 创建、204 删除、200 查询）
- 不在 API 表面暴露实现细节（数据库表名、框架内部类名）
- 不在 DTO 中混用 ORM 注解
- 不自动生成生产环境发布命令

## 输出检查清单

| # | 检查项 | 验证方式 | 阻断 |
|---|--------|----------|:----:|
| 1 | 资源模型和关系表已生成 | `components/schemas` 数量 ≥ 实体表数量 | 是 |
| 2 | 端点规范完整 | 每个端点含 URI + Method + operationId | 是 |
| 3 | OpenAPI 3.1 YAML 语法正确 | Redocly lint 无 error | 是 |
| 4 | 认证与授权流程已声明 | `securitySchemes` 和 `security` 存在 | 否 |
| 5 | 错误响应目录完整 | 含 BadRequest/Unauthorized/NotFound/TooManyRequests/Conflict | 是 |
| 6 | 分页和过滤模式已应用 | 所有 GET 集合端点含 cursor/limit 或 page/size | 是 |
| 7 | Mock 数据覆盖正常 + 异常路径 | 每个 operationId ≥ 2 组示例 | 否 |
| 8 | 并行开发计划含前后端边界 | 含前端任务、后端任务、联调时间点 | 否 |

## 与上下游衔接

- **上游**：`detailed-design`（必须完成后方可启动）
- **横向并行**：`writing-plans`（与接口驱动开发并行，基于同一套 design.md 生成实现计划 plan.md）
- **下游**：`task-breakdown`（基于 `parallel-dev-plan.md` 的后端任务边界 + `plan.md` 拆解任务）
- **横向**：
  - `self-check`：执行完毕后自动触发接口契约质量检查
  - `human` Gate 2.5：契约冻结前需人工 sign-off

## Gate 2.5 阻塞提示

质量检查通过后，自动宣读：

```text
========================================
🚪 Gate 2.5: 接口冻结 —— 等待人工确认
========================================
产出物已保存至：interface-contracts/

请执行以下操作：
1. 阅读 openapi.yaml，确认 URI 设计符合前端路由规划
2. 阅读 parallel-dev-plan.md，确认前后端任务边界合理
3. 启动 Mock 服务验证：npx @stoplight/prism-cli mock interface-contracts/openapi.yaml
4. 确认无误后执行：/skill:human gate=Gate2.5 action=sign-off

⚠️ 未获得人工确认前，禁止进入 task-breakdown 阶段。

> **流程纪律**：`interface-first-dev` 与 `writing-plans` 并行启动，均依赖 `detailed-design` 完成。
> 若 `writing-plans` 尚未执行，请先执行 `/skill:writing-plans` 生成 plan.md，再进入 `task-breakdown`。
> 顺序：`detailed-design` → [`interface-first-dev` ∥ `writing-plans`] → `task-breakdown`
```

## Gotchas

- **硬性前置**：`db-schema.md` 或 `design.md` 缺失时直接阻断，不可凭空生成接口
- **扩展模式**：若已有 `interface-contracts/openapi.yaml`，仅追加新模块端点，禁止覆盖现有路径
- **Schema 解析降级**：`db-schema.md` 表格格式不标准时，降级为启发式解析并输出警告，要求人工复核
- **状态机歧义**：复杂嵌套条件的状态机，输出最保守的通用 `PATCH /{resource}/{id}` 设计，并在 `parallel-dev-plan.md` 中标注"需人工细化"
- **Mock 占位**：复杂嵌套 Schema 导致示例缺失时，填充占位值并标注 `TODO：替换为真实业务值`
- **URI 动词红线**：发现 `api-spec.md` 初稿中含动词 URI（如 `/getOrder`）时，必须修正为资源导向路径，不可原样照搬
- **Redocly 失败阻断**：lint 发现 error 时自动修复常见错误（如重复 operationId），无法自动修复则阻断并输出报告
- **契约冻结后不可随意变更**：Gate 2.5 sign-off 后的 `openapi.yaml` 是 task-breakdown 的不可变输入基准，后续变更需走变更流程
