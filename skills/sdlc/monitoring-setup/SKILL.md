---
name: monitoring-setup
description: 当用户要求'生成监控规则'、'monitoring-setup'、'配置告警'、'初始化可观测性'或在 high-level-design 完成后需要生成 monitoring-rules.yaml 时触发。基于概要设计中的运维架构章节，自动生成项目级监控规则初稿。
---

# Monitoring Setup

## 角色

你是项目可观测性初始化专家。基于概要设计中的运维架构章节，自动推导服务拓扑和技术栈，生成项目级监控规则初稿 `ops/monitoring-rules.yaml`。

## 适用场景

- 概要设计（high-level-design）完成后，需要初始化监控规则基线
- 用户显式要求生成 monitoring-rules.yaml 或配置可观测性
- 进入 Gate 2 设计冻结闸前，需补齐运维监控规则

## 核心职责

1. **架构推导自动化**：从 `design/05-ops-governance.md` §1（运维架构）和 `01-architecture-core.md` §2（技术栈）提取服务列表、中间件、部署形态
2. **技术栈模板化**：按识别到的技术栈匹配内置模板（JVM/Node/Python/Go/DB/Redis/MQ/K8s 等）
3. **输出标准化**：统一输出到 `ops/monitoring-rules.yaml`，兼容 Prometheus/云监控语法结构
4. **Gate 2 前置**：产出物随 high-level-design 一并进入人工评审

## 执行流程

### Step 1: 读取输入

按优先级读取：
1. `openspec/config.yaml` —— 提取 project_name、技术栈总览
2. `openspec/changes/{变更名}/high-level-design/05-ops-governance.md` —— 定位"运维架构"、"回滚方案"章节；`01-architecture-core.md` —— 定位"技术选型"章节；`04-quality-attributes.md` —— 定位"部署架构"章节
3. `openspec/changes/{变更名}/high-level-requirements/00-requirements-overview.md` —— 提取性能指标（RT、QPS、可用性）、告警阈值要求

### Step 2: 解析架构信息

从设计文档提取结构化信息：

- **服务列表**：服务名、端口、技术栈、部署节点
- **中间件列表**：数据库、缓存、消息队列、网关类型
- **部署形态**：Docker / Kubernetes / 裸机 / Serverless
- **性能基线**：P99 延迟、错误率、CPU/内存上限（文档未明确时使用本 skill 内置默认值）

提取策略：
- 优先读取 `05-ops-governance.md` §1（运维架构）提取监控三支柱、告警分级、SLO/SLA
- 次优读取 `04-quality-attributes.md` §5（部署架构）提取部署拓扑和 CI/CD 流程
- 再次读取 `01-architecture-core.md` §2（技术栈）提取服务列表、中间件、部署形态
- 匹配 Markdown 表格（"组件/技术/版本"列）和标题层级

### Step 3: 匹配模板与变量填充

根据技术关键词，查询本 skill 目录下 `templates/` 中的规则模板：
- 命中 → 加载对应模板
- 未命中 → 仅加载 `_base.yaml`，输出中标记 `⚠️ 未识别技术栈：{关键词}，请人工补充`
- 多技术栈共存 → 加载多个模板

执行变量替换：

| 变量 | 填充规则 |
|------|----------|
| `{{service_name}}` | 设计文档中的服务名；中间件使用类型名（如 `mysql-primary`） |
| `{{host}}` | 部署架构中的 IP/域名；无则默认 `localhost` |
| `{{port}}` | 设计文档明确端口 > 模板默认值 > 通用默认值（HTTP:8080, DB:3306, Redis:6379） |
| `{{environment}}` | 设计文档中的环境标识；无则默认 `staging` |
| `{{project_name}}` | `openspec/config.yaml` 中的 project 字段 |
| `{{team_name}}` | 设计文档中的团队名；无则默认 `unknown` |
| `{{*_threshold}}` | 设计文档明确数值 > 内置默认值 > 模板硬编码值 |

### Step 4: 多模板合并

当存在多个技术栈时，按以下规则合并：
1. **scrape_configs**：按 `job_name` 去重，冲突时保留设计文档明确指定的端口
2. **alerting_rules**：按 `alert` 名去重，冲突时添加服务名前缀（如 `user-service_HighCpuUsage`）
3. **business_metrics**：按 `name` 去重
4. 统一注入全局标签（env, project, team）

### Step 5: 生成与校验

以 `_base.yaml` 为骨架，填充合并后的三段内容，生成完整 YAML：

```yaml
project: {project_name}
version: "1.0"
generated_by: "monitoring-setup"
generated_at: "{timestamp}"
environment: {environment}

global_labels:
  env: "{environment}"
  project: "{project_name}"
  team: "{team_name}"

scrape_configs:
  ...

alerting_rules:
  ...

business_metrics:
  ...
```

校验项（全部通过方可保存）：
- YAML 语法合法性
- `scrape_configs` 每个 target 包含 `host:port`
- `alerting_rules` 每个 `expr` 包含明确阈值（禁止残留 `{{.*}}`）
- 至少包含 1 条应用层告警 + 1 条基础设施告警

校验失败时：标记错误位置，尝试自动修复（引号转义、缩进修正），失败则标记 `🔴 需人工修复`。

保存路径：`ops/monitoring-rules.yaml`（覆盖写入，不追加）。

### Step 6: 输出摘要与 Gate 2 提示

保存后输出执行摘要：

```text
========================================
monitoring-setup 执行完成
========================================
识别技术栈：{列表}
加载模板：{N} 个
生成规则：
  - 采集任务：{N} 个
  - 告警规则：{N} 条（critical: {N}, warning: {N}）
  - 业务埋点：{N} 个
输出路径：ops/monitoring-rules.yaml

⚠️ 以下项使用默认值，请人工确认：
  - API P99 延迟阈值：500ms（设计文档未明确）
  - ...

========================================
🚪 Gate 2: 设计冻结 —— 监控规则待确认
========================================
请在评审概要设计时同步检查 monitoring-rules.yaml：
1. 所有服务节点是否已覆盖？
2. 告警阈值是否符合业务容忍度？
3. 是否缺少关键中间件？
4. business_metrics 中的核心链路埋点是否完整？

确认后执行：/skill:human gate=Gate2 action=sign-off
```

## 输出格式规范

`ops/monitoring-rules.yaml` 必须包含以下顶级键：

| 键 | 说明 |
|---|---|
| `project` | 项目名 |
| `version` | 规则版本，固定 `"1.0"` |
| `generated_by` | 固定 `"monitoring-setup"` |
| `generated_at` | ISO 8601 时间戳 |
| `environment` | staging / production |
| `global_labels` | 全局标签（env, project, team） |
| `scrape_configs` | 采集任务列表 |
| `alerting_rules` | 告警规则列表 |
| `business_metrics` | 业务自定义埋点（占位） |

## 约束

- 严禁生成空规则文件（至少包含 `_base.yaml` 骨架 + 1 条告警）
- 严禁残留未替换的变量占位符（`{{.*}}`）进入最终 YAML
- 严禁修改设计文档原文，只读取不写入
- 本 Skill 为一次性执行，同一变更生命周期内禁止重复执行
- 中间件默认端口：MySQL 3306、PostgreSQL 5432、Redis 6379、Kafka 9092、RabbitMQ 5672

## 错误处理

| 场景 | 处理 |
|------|------|
| 设计文档无"运维架构"章节 | 加载 `_base.yaml` + 所有疑似技术栈关键词的模板，标记 `⚠️ 未找到运维架构章节，基于关键词推测生成` |
| 技术栈关键词未命中任何模板 | 加载 `_base.yaml`，标记 `⚠️ 未识别技术栈：{关键词}` |
| 多模板 `job_name` 冲突 | 自动添加服务名前缀去重 |
| YAML 语法校验失败 | 输出错误行号，尝试自动修复，失败标记 `🔴 需人工修复` |

## 下游消费

| 下游 Skill | 说明 |
|---|---|
| `monitoring-analysis` | 周期性读取 `ops/monitoring-rules.yaml` 作为分析基准 |
| `release-management` | 发布时确认监控规则已生效 |
| `human` | Gate 2 人工冻结确认 |

## 深度参考

- 技术栈模板与详细实现指南见 `references/REFERENCE.md`
- 完整输出示例见 `examples/monitoring-rules.yaml`

## Gotchas

- **架构推导不是运维手册**：本 skill 只生成监控规则的"初稿"，不输出 Dashboard JSON、告警通知人配置或具体的 Prometheus Server 部署方案。
- **阈值必须人工确认**：默认阈值（如 CPU 80%、P99 500ms）仅为安全兜底，禁止将其视为生产环境的最终配置。生成的 YAML 摘要中必须明确列出所有使用了默认值的项。
- **禁止覆盖人工调整**：本 skill 设计为一次性执行。若用户已在 `ops/monitoring-rules.yaml` 上进行过人工调整，重复执行将覆盖这些修改。执行前需确认文件是否已存在且包含 `generated_by: "monitoring-setup"` 以外的手工注释。
- **技术栈识别有盲区**：文档中未显式提及的技术栈（如通过 SDK 隐式引入的 MongoDB、Elasticsearch）不会被自动识别，需在 Gate 2 人工检查中补充。
- **job_name 冲突陷阱**：当多个服务使用相同技术栈模板时（如两个 Spring Boot 服务），默认 job_name 会冲突。合并逻辑必须自动添加服务名前缀，否则 Prometheus 会只保留最后一个任务。
- **expr 语法差异**：不同监控后端（Prometheus/VictoriaMetrics/云监控）对 `rate()` 和 `histogram_quantile()` 的支持有细微差异。模板中使用 Prometheus 标准语法，若项目使用其他后端，需在 Gate 2 评审时调整。
- **业务埋点仅为占位**：`business_metrics` 段生成的 histogram/counter 定义是"待实现"占位符，真正的埋点代码需要在开发阶段由开发人员手动注入（如 Micrometer、Prometheus Client）。
- **K8s 与裸机指标不可混用**：若模板同时命中 `infra-k8s.yaml` 和 `infra-docker.yaml`，会产生容器级和 Pod 级重复采集。合并时应根据部署架构二选一，默认以设计文档明确的部署形态为准。
