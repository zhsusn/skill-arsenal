# monitoring-setup 设计文档

> 本文档面向 AI 助手开发者和项目维护者，说明 `monitoring-setup` Skill 的架构设计、核心机制与扩展方式。
> 
> 对应实现：`skills/sdlc/monitoring-setup/`

---

## 目录

1. [概述](#概述)
2. [架构总览](#架构总览)
3. [技术栈模板系统](#技术栈模板系统)
4. [配置系统](#配置系统)
5. [元数据与依赖管理](#元数据与依赖管理)
6. [校验与质量控制](#校验与质量控制)
7. [工具链衔接](#工具链衔接)
8. [开源参考与借鉴](#开源参考与借鉴)
9. [关键设计决策](#关键设计决策)
10. [待扩展项](#待扩展项)

---

## 概述

### 定位

`monitoring-setup` 是 **SDLC 阶段 3（概要设计）** 的配套 Skill，职责是：

> 基于 `high-level-design` 产出的运维架构章节，自动推导服务拓扑和技术栈，生成项目级监控规则初稿 `ops/monitoring-rules.yaml`。

### 核心差异化

开源社区在"AI 自动从架构设计推导监控规则"这一细分领域尚无成熟方案。现有监控类 Skill（如 agent-skills-hub 的 observability-monitoring-monitor-setup）均为**通用顾问型**——用户告诉 AI 要监控什么，AI 再输出方案；而 `monitoring-setup` 是**架构推导型**——AI 主动从设计文档中读取服务列表、中间件类型、部署形态，自动生成匹配技术栈的监控规则 YAML。

| 维度 | 通用顾问型 Skill | monitoring-setup（架构推导型） |
|---|---|---|
| 输入 | 用户对话中的监控需求描述 | 概要设计文档（design/*.md）中的运维架构章节 |
| 输出 | 配置建议、检查清单、代码片段 | 可直接落地的 `monitoring-rules.yaml` 初稿 |
| 技术栈适配 | 需要用户逐条说明 | 自动识别 Spring Boot/Node.js/Python/Go/MySQL/Redis/Kafka/K8s 等 |
| 与 SDLC 衔接 | 独立使用 | 嵌入 Gate 2 设计冻结闸，作为设计评审的必要产出物 |

---

## 架构总览

### 数据流

```
┌─────────────────────────────────────────────────────────────────────┐
│                         monitoring-setup                             │
│                                                                      │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐             │
│  │ openspec/    │   │ design/*.md  │   │ 05-non-      │             │
│  │ config.yaml  │   │ 运维架构章节  │   │ functional.md│             │
│  └──────┬───────┘   └──────┬───────┘   └──────┬───────┘             │
│         │                  │                  │                      │
│         └──────────────────┼──────────────────┘                      │
│                            ▼                                         │
│                   ┌────────────────┐                                 │
│                   │  架构信息解析   │  ← 三级提取策略                  │
│                   │  · 服务列表     │     (表格 → 标题 → 关键词)       │
│                   │  · 中间件列表   │                                 │
│                   │  · 部署形态     │                                 │
│                   │  · 性能基线     │                                 │
│                   └───────┬────────┘                                 │
│                           ▼                                          │
│                   ┌────────────────┐                                 │
│                   │  技术栈模板匹配 │  ← config.yaml 映射表            │
│                   │  · _base.yaml  │                                 │
│                   │  · app-*.yaml  │                                 │
│                   │  · db-*.yaml   │                                 │
│                   │  · infra-*.yaml│                                 │
│                   └───────┬────────┘                                 │
│                           ▼                                          │
│                   ┌────────────────┐                                 │
│                   │  变量填充与合并 │  ← 11 类占位符 + 去重逻辑         │
│                   │  · 服务名/端口  │                                 │
│                   │  · 阈值替换     │                                 │
│                   │  · job_name 去重│                                 │
│                   └───────┬────────┘                                 │
│                           ▼                                          │
│                   ┌────────────────┐                                 │
│                   │  YAML 生成与校验│                                 │
│                   │  · 语法合法性   │                                 │
│                   │  · 占位符残留   │                                 │
│                   │  · 覆盖率检查   │                                 │
│                   └───────┬────────┘                                 │
│                           ▼                                          │
│              ┌────────────────────────┐                              │
│              │ ops/monitoring-rules.yaml│  ← 项目级监控规则基线        │
│              └────────────────────────┘                              │
│                           │                                          │
│                           ▼                                          │
│              ┌────────────────────────┐                              │
│              │ 🚪 Gate 2 人工评审节点  │  ← 阻塞性设计冻结闸          │
│              └────────────────────────┘                              │
└─────────────────────────────────────────────────────────────────────┘
```

### 执行时机

```
high-level-design → monitoring-setup → human(Gate2) → detailed-design
         ↑                                    ↓
   输入：运维架构章节                   确认：架构+监控+回滚方案
```

- **前置依赖**：`high-level-design` 必须完成，产出 `design/14-operations-architecture.md`
- **并行**：可与 `self-check` 概要设计自查并行
- **后置消费**：`monitoring-analysis`（周期性运行时读取基准规则）、`release-management`（发布前确认监控已配置）

---

## 技术栈模板系统

### 模板分类

模板按"组件类型 + 具体技术"两级组织，存储于 `skills/sdlc/monitoring-setup/templates/`：

| 类别 | 模板文件 | 覆盖场景 |
|---|---|---|
| 基础骨架 | `_base.yaml` | 所有项目的通用 YAML 结构 |
| 应用-JVM | `app-jvm-springboot.yaml` | Spring Boot + Micrometer |
| 应用-Node | `app-node.yaml` | NestJS/Express/Fastify |
| 应用-Python | `app-python.yaml` | FastAPI/Flask/Django |
| 应用-Go | `app-go.yaml` | Gin/Echo/Fiber |
| 应用-前端 | `app-frontend.yaml` | Vue3/React/SPA（RUM 指标） |
| 数据库-MySQL | `db-mysql.yaml` | MySQL/MariaDB |
| 数据库-PG | `db-postgresql.yaml` | PostgreSQL |
| 缓存 | `cache-redis.yaml` | Redis |
| 消息队列 | `mq-kafka.yaml` | Kafka |
| 网关 | `gw-nginx.yaml` | Nginx/反向代理 |
| 基础设施 | `infra-k8s.yaml` | Kubernetes |

### 模板内部结构

每个模板严格包含四段：

```yaml
meta:
  tech_stack: "标识名"      # 用于调试与追踪
  version: "1.0"

scrape_configs:              # 采集端点定义
  - job_name: "{{service_name}}-xxx"
    ...

alerting_rules:              # 告警规则（PromQL 标准语法）
  - alert: "{{service_name}}_AlertName"
    expr: '...'
    for: "2m"
    labels:
      severity: warning|critical
      team: "{{team_name}}"
    annotations:
      summary: "..."

business_metrics:            # 业务自定义埋点（占位符）
  - name: "{{service_name}}_xxx"
    type: histogram|counter|gauge
    labels: ["..."]
    buckets: [...]
```

### 变量占位符规范

| 占位符 | 来源 | 默认值 | 说明 |
|---|---|---|---|
| `{{service_name}}` | 设计文档服务列表 | **必填** | 中间件使用类型名（如 `mysql-primary`） |
| `{{host}}` | 部署架构 IP/域名 | `localhost` | — |
| `{{port}}` | 设计文档 > 模板默认 > 通用默认 | 8080/3306/5432/6379 | HTTP/MySQL/PG/Redis 各不同 |
| `{{environment}}` | 设计文档环境标识 | `staging` | — |
| `{{project_name}}` | `openspec/config.yaml` | `unknown` | — |
| `{{team_name}}` | 设计文档团队名 | `unknown` | — |
| `{{cpu_threshold}}` | `config.yaml` `default_thresholds` | 80 | 单位：百分比 |
| `{{memory_threshold}}` | `config.yaml` `default_thresholds` | 85 | 单位：百分比 |
| `{{error_rate_threshold}}` | `config.yaml` `default_thresholds` | 1.0 | 单位：百分比 |
| `{{p99_latency_threshold}}` | `config.yaml` `default_thresholds` | 500 | 单位：毫秒 |
| `{{db_connections_threshold}}` | `config.yaml` `default_thresholds` | 80 | 单位：百分比或绝对值 |
| `{{cache_hit_rate_threshold}}` | `config.yaml` `default_thresholds` | 90 | 单位：百分比 |
| `{{mq_consumer_lag_threshold}}` | `config.yaml` `default_thresholds` | 1000 | 单位：消息数 |

### 多模板合并策略

当项目存在多个技术栈（如 Spring Boot + MySQL + Redis + Kafka）时，按以下规则合并：

1. **scrape_configs**：按 `job_name` 去重。冲突时保留设计文档明确指定的端口，若仍冲突则自动添加服务名前缀（如 `actuator` → `order-service-actuator`）。
2. **alerting_rules**：按 `alert` 名去重。冲突时添加服务名前缀（如 `user-service_HighCpuUsage` vs `pay-service_HighCpuUsage`）。
3. **business_metrics**：按 `name` 去重。
4. **全局标签注入**：统一在顶层注入 `env`、`project`、`team`。

---

## 配置系统

### config.yaml 结构

```yaml
project:
  output_path: "ops/monitoring-rules.yaml"
  default_scrape_interval: "15s"
  default_evaluation_interval: "1m"

tech_stack_mapping:
  jvm_springboot:
    keywords: ["Spring Boot", "SpringBoot", "Java", "JVM", "Micrometer"]
    template: "app-jvm-springboot.yaml"
  # ... 其他映射

default_thresholds:
  api_p99_latency_ms: 500
  api_error_rate_percent: 1.0
  cpu_usage_percent: 80
  # ... 其他阈值

global_labels:
  env: "{{environment}}"
  project: "{{project_name}}"
  team: "{{team_name}}"
```

### 设计意图

- **离线可用**：模板库和配置全部内置在 Skill 目录下，不依赖远程拉取，符合 Kimi Code 本地优先工作模式。
- **可扩展**：新增技术栈只需在 `tech_stack_mapping` 中注册映射，并在 `templates/` 下新建 YAML 片段，无需修改 SKILL.md 核心逻辑。
- **安全兜底**：设计文档未明确阈值时，使用 `default_thresholds` 中的保守值，并在输出摘要中明确列出"以下项使用了默认值"。

---

## 元数据与依赖管理

### meta.json 设计

```json
{
  "name": "monitoring-setup",
  "version": "1.0.0",
  "pattern": "generator",
  "domain": "observability",
  "tags": ["sdlc", "observability", "monitoring", "prometheus", "ops", "openspec", "stage-3"],
  "platforms": ["kimi", "claude", "cursor", "codex", "gemini"],
  "dependencies": ["high-level-design"],
  "consumed_by": ["monitoring-analysis", "release-management"],
  "run_once_per_change": true,
  "language": "zh-CN"
}
```

### 双轨制说明

本项目采用 **Kimi Code 兼容性双轨制**：

- `SKILL.md` Frontmatter **仅限 `name` + `description`**（Kimi Code 严格白名单要求）
- 扩展元数据（版本、依赖、标签、平台）全部存入同目录的 `meta.json`

此设计避免 Kimi Code CLI 因 Frontmatter 中存在额外字段而拒绝加载 Skill。

---

## 校验与质量控制

### 三级校验机制

| 层级 | 校验项 | 失败处理 |
|---|---|---|
| **语法层** | YAML 格式合法性（标准解析器） | 输出错误行号，尝试自动修复缩进/引号 |
| **内容层** | `scrape_configs` 每个 target 必须包含 `host:port`；`alerting_rules` 每个 `expr` 必须包含明确阈值；禁止残留 `{{.*}}` | 标记具体位置，回退到变量填充步骤重新处理 |
| **覆盖层** | 最终文件至少包含 1 条应用层告警 + 1 条基础设施告警 | 若缺失，加载 `_base.yaml` 时强制注入一条兜底告警 |

### 禁止性约束（红线）

1. **严禁生成空规则文件**：至少包含 `_base.yaml` 骨架 + 1 条告警。
2. **严禁残留未替换变量**：所有 `{{.*}}` 必须在输出前完成替换或标记为需人工修复。
3. **严禁修改设计文档**：只读取不写入，确保上游文档的完整性。
4. **严禁重复执行**：同一变更生命周期内只执行一次，避免覆盖人工调整。

---

## 工具链衔接

### 前置依赖

| Skill | 关系 | 说明 |
|---|---|---|
| `high-level-design` | **强依赖** | 必须等待概要设计完成，获取 `14-operations-architecture.md` 中的运维架构章节 |

### 后置消费

| Skill | 关系 | 说明 |
|---|---|---|
| `monitoring-analysis` | 消费者 | 周期性运行时读取 `monitoring-rules.yaml` 作为分析基准 |
| `release-management` | 参考者 | 发布时确认监控规则已生效 |
| `human` | 阻塞闸 | Gate 2 人工冻结确认 |

### 在 OpenSpec 工作流中的位置

```
阶段 3 概要设计
├── high-level-design          → 产出 design/*.md（含 14-operations-architecture）
├── self-check                 → 自查一致性（可与 monitoring-setup 并行）
├── monitoring-setup           → 产出 ops/monitoring-rules.yaml（本 Skill）
└── human gate=Gate2           → 人工评审：架构 + 监控 + 回滚方案
         │
         ▼
    阶段 4 详细设计
```

---

## 开源参考与借鉴

### 参考一：agent-skills-hub/observability-monitoring-monitor-setup

- **来源**：GitHub - agent-skills-hub/agent-skills-hub
- **功能定位**：通用监控和可观测性专家，提供指标采集、分布式追踪、日志聚合、Dashboard 创建的全流程指导。
- **借鉴点**：
  - **结构化输出格式**：Infrastructure Assessment → Monitoring Architecture → Implementation Plan → Metric Definitions → Dashboard Templates → Alert Runbooks → SLO Definitions → Integration Guide 的八段式输出，用于设计本 Skill 的 Gate 2 人工评审清单。
  - **渐进式披露结构**：SKILL.md 保持核心指令，详细模式存储在 `resources/implementation-playbook.md` 中。本 Skill 对应设计为 `SKILL.md` + `references/REFERENCE.md`。

### 参考二：MLOps-Courses/mlops-coding-skills（Observability）

- **来源**：GitHub - MLOps-Courses/mlops-coding-skills
- **功能定位**：MLOps 场景下的可观测性 Skill，覆盖日志、血缘、监控三大支柱。
- **借鉴点**：
  - **Checklist 风格**：Monitoring Checklist（Random seeds fixed / MLflow tracking enabled / Alerts configured）用于设计本 Skill 的 Gate 2 检查项。
  - **分级告警**：Local（桌面通知）vs Production（PagerDuty/Slack）的分级思路，用于设计 `severity: warning` 与 `severity: critical` 的区分策略。
  - **可复用代码片段**：`references/mlflow-tracking.py` 的"复制即用"思路，用于设计 `business_metrics` 的"占位符 + 开发阶段手动注入"机制。

---

## 关键设计决策

| 决策 | 选择 | 理由 |
|---|---|---|
| **模板形态：YAML 片段 vs 完整文件** | YAML 片段 | 便于多技术栈合并。每个模板只负责一个组件的规则片段，最终由 Skill 逻辑合并为完整项目级规则文件。 |
| **模板存储：内置 vs 远程拉取** | 内置在 `templates/` 下 | 保证离线可用性，符合 Kimi Code 本地优先工作模式；模板变更频率低，随 Skill 版本迭代即可。 |
| **阈值来源：设计文档 vs 内置默认** | 设计文档优先，未明确时 fallback 到 `default_thresholds` | 监控阈值直接影响告警噪音和故障发现能力，必须经 SRE/架构师确认。默认值仅作为安全兜底。 |
| **执行频次：一次性 vs 周期性** | 一次性（`run_once_per_change: true`） | 监控规则基线在项目初期确定，后续迭代通过 `monitoring-analysis` 调优或人工编辑，避免重复生成覆盖人工调整。 |
| **部署形态冲突：Docker vs K8s** | 以设计文档明确的部署形态为准，模板同时命中时二选一 | 防止容器级（Docker）和 Pod 级（K8s）指标重复采集。 |
| **expr 语法标准** | Prometheus PromQL | 社区最广泛支持的语法，同时兼容 VictoriaMetrics、Thanos 等后端（少量差异需在 Gate 2 评审时调整）。 |

---

## 待扩展项

| 任务 | 优先级 | 说明 |
|---|---|---|
| 模板扩充：MongoDB / Elasticsearch / RabbitMQ | P1 | 当前模板库覆盖主流技术栈，但缺少文档型数据库和 AMQP 消息队列 |
| 云监控语法适配层 | P2 | 当前模板使用 PromQL，若项目使用阿里云 CMS / AWS CloudWatch / GCP Monitoring，需增加转译逻辑或独立模板集 |
| 与 progress-tracker 联调 | P1 | 执行完成后自动触发进度更新：`monitoring-setup: done` |
| 与 high-level-design 输出格式联调 | P1 | 确认 `14-operations-architecture.md` 的章节结构可被本 Skill 稳定解析 |
| 规则有效性自动校验 | P2 | 引入 PromQL 语法检查（如使用 promtool 或 VictoriaMetrics 的 lint），当前仅做正则级占位符检查 |
