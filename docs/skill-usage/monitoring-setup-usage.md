# monitoring-setup 使用手册

> 本文档面向项目开发者、架构师和 SRE，说明如何触发、使用和维护 `monitoring-setup` Skill 生成的监控规则。
>
> 对应实现：`skills/sdlc/monitoring-setup/`

---

## 目录

1. [适用场景](#适用场景)
2. [触发方式](#触发方式)
3. [前置准备](#前置准备)
4. [执行流程](#执行流程)
5. [输出说明](#输出说明)
6. [完整示例](#完整示例)
7. [Gate 2 人工评审清单](#gate-2-人工评审清单)
8. [技术栈适配速查](#技术栈适配速查)
9. [常见问题与排错](#常见问题与排错)
10. [扩展指南](#扩展指南)

---

## 适用场景

| 场景 | 说明 |
|---|---|
| ✅ **概要设计完成后** | `high-level-design` 已产出 `design/14-operations-architecture.md`，需要初始化监控规则基线 |
| ✅ **显式命令触发** | 用户直接要求"生成监控规则"、"配置告警"、"初始化可观测性" |
| ✅ **Gate 2 前置补齐** | 进入设计冻结闸前，发现 ops 目录下缺少 `monitoring-rules.yaml`，需紧急补齐 |
| ❌ **已有成熟监控体系** | 项目已运行多年，监控规则由 SRE 团队手动维护，无需 AI 生成初稿 |
| ❌ **纯 Serverless 无服务器** | 若所有组件均为托管服务（如 Vercel + Supabase），监控由平台自带，本 Skill 价值有限 |
| ❌ **重复执行** | 同一变更生命周期内已执行过 `monitoring-setup`，再次执行会覆盖人工调整 |

---

## 触发方式

### 推荐触发命令

```
/skill:monitoring-setup 基于运维架构章节，生成 monitoring-rules.yaml 初稿。
```

### 语义化触发关键词

AI 助手在听到以下关键词时应自动激活本 Skill：

- "生成监控规则"、"monitoring-setup"
- "配置告警"、"初始化可观测性"
- "运维架构确定了，帮我写 Prometheus 规则"
- "ops 目录还缺监控规则，补一下"

---

## 前置准备

执行本 Skill 前，请确保以下文档已就绪：

| 输入文档 | 路径示例 | 必需 | 用途 |
|---|---|---|---|
| 项目配置 | `openspec/config.yaml` | **必须** | 提取 `project_name`、技术栈总览 |
| 运维架构 | `design/14-operations-architecture.md` | **必须** | 服务拓扑、部署节点、中间件清单 |
| 技术选型 | `design/02-tech-stack.md` | **必须** | 精确的技术栈关键词（用于模板匹配） |
| 非功能需求 | `specs/05-non-functional.md` | 强烈建议 | 性能基线（RT、QPS、可用性）、告警阈值要求 |

### 文档编写建议（提高识别准确率）

1. **服务列表使用 Markdown 表格**：
   ```markdown
   | 服务名 | 技术栈 | 端口 | 部署节点 |
   |--------|--------|------|----------|
   | order-service | Spring Boot 3.2 | 8080 | k8s-cluster-1 |
   | redis-cache | Redis 7.0 | 6379 | k8s-cluster-1 |
   ```

2. **技术选型章节使用明确关键词**：
   - ✅ 写"使用 **Spring Boot** + **MySQL** + **Redis** + **Kafka**"
   - ❌ 避免模糊描述如"主流 Java 技术栈 + 关系型数据库"

3. **非功能需求中明确数值**：
   - ✅ "API P99 延迟 < 200ms，错误率 < 0.5%"
   - ❌ "系统要快，不能出错"

---

## 执行流程

AI 助手执行本 Skill 时，会按以下 6 个步骤自动处理：

### Step 1：读取输入
- 读取 `openspec/config.yaml` 提取项目名
- 读取 `design/*.md` 定位"运维架构"、"部署架构"、"技术选型"章节
- 读取 `specs/05-non-functional.md` 提取性能指标和阈值要求

### Step 2：解析架构信息
- **服务列表**：名称、端口、技术栈、部署节点
- **中间件列表**：数据库、缓存、消息队列、网关
- **部署形态**：Docker / Kubernetes / 裸机 / Serverless
- **性能基线**：P99 延迟、错误率、CPU/内存上限

### Step 3：匹配模板与变量填充
- 根据技术关键词匹配 `templates/` 下的 YAML 片段
- 未命中时仅加载 `_base.yaml`，并标记 `⚠️ 未识别技术栈`
- 执行变量替换（服务名、端口、阈值等）

### Step 4：多模板合并
- 合并 `scrape_configs`（按 `job_name` 去重）
- 合并 `alerting_rules`（按 `alert` 名去重，冲突时加前缀）
- 合并 `business_metrics`（按 `name` 去重）
- 统一注入全局标签

### Step 5：生成与校验
- 以 `_base.yaml` 为骨架填充内容
- 校验 YAML 语法、target 完整性、阈值明确性
- 保存到 `ops/monitoring-rules.yaml`（覆盖写入）

### Step 6：输出摘要与 Gate 2 提示
- 输出执行摘要（识别技术栈数、生成规则数、使用默认值清单）
- 宣读 🚪 Gate 2 阻塞提示，等待人工确认

---

## 输出说明

### 文件位置

```
ops/monitoring-rules.yaml
```

> 注意：项目初始化时 `progress-tracker` 已创建 `ops/` 目录骨架（含 `monitoring-rules.yaml` 空骨架），本 Skill 负责**覆盖填充**内容。

### YAML 顶级结构

| 键 | 说明 | 示例 |
|---|---|---|
| `project` | 项目名 | `ecommerce-order` |
| `version` | 规则版本 | `"1.0"` |
| `generated_by` | 生成工具标识 | `"monitoring-setup"` |
| `generated_at` | ISO 8601 时间戳 | `"2026-05-10T10:00:00Z"` |
| `environment` | 环境标识 | `staging` / `production` |
| `global_labels` | 全局标签 | `env`, `project`, `team` |
| `scrape_configs` | 采集任务列表 | Prometheus `job_name` + `targets` |
| `alerting_rules` | 告警规则列表 | PromQL `expr` + `severity` |
| `business_metrics` | 业务埋点占位 | histogram / counter / gauge 定义 |

### 告警级别定义

| 级别 | 响应时效 | 通知渠道建议 | 典型场景 |
|---|---|---|---|
| `critical` | 立即（5 分钟内） | PagerDuty / 电话 / 企业微信 | 错误率飙升、服务不可达、数据库连接耗尽 |
| `warning` | 工作时间内 | Slack / 钉钉 / 邮件 | CPU/内存使用率偏高、P99 延迟上升、消费组积压 |

---

## 完整示例

### 输入：技术选型文档片段

```markdown
## 技术选型

| 组件 | 技术 | 版本 | 端口 |
|------|------|------|------|
| API 网关 | Nginx | 1.24 | 80 |
| 订单服务 | Spring Boot | 3.2 | 8080 |
| 支付服务 | Spring Boot | 3.2 | 8081 |
| 数据库 | MySQL | 8.0 | 3306 |
| 缓存 | Redis | 7.0 | 6379 |
| 消息队列 | Kafka | 3.5 | 9092 |
| 基础设施 | Kubernetes | 1.29 | — |

## 非功能性需求
- API P99 延迟 < 200ms
- 可用性 99.9%
- 错误率 < 0.1%
```

### 输出：ops/monitoring-rules.yaml（节选）

```yaml
project: ecommerce-order
version: "1.0"
generated_by: "monitoring-setup"
generated_at: "2026-05-10T10:00:00Z"
environment: staging

global_labels:
  env: "staging"
  project: "ecommerce-order"
  team: "backend"

scrape_configs:
  - job_name: "order-service-actuator"
    metrics_path: "/actuator/prometheus"
    static_configs:
      - targets: ["order-service:8080"]

  - job_name: "pay-service-actuator"
    metrics_path: "/actuator/prometheus"
    static_configs:
      - targets: ["pay-service:8081"]

  - job_name: "mysql-primary-exporter"
    static_configs:
      - targets: ["mysql-primary:3306"]

  - job_name: "redis-cache-exporter"
    static_configs:
      - targets: ["redis-cache:6379"]

  - job_name: "kafka-exporter"
    static_configs:
      - targets: ["kafka-0:9092"]

  - job_name: "gw-nginx-metrics"
    metrics_path: "/metrics"
    static_configs:
      - targets: ["nginx-gateway:80"]

  - job_name: "k8s-kubelet"
    static_configs:
      - targets: ["node-1:10250"]

alerting_rules:
  # Spring Boot 服务层
  - alert: "order-service_HighErrorRate"
    expr: 'rate(http_server_requests_seconds_count{service="order-service",status=~"5.."}[5m]) > 0.001'
    for: "2m"
    labels:
      severity: critical
      team: "backend"
    annotations:
      summary: "服务 order-service 错误率超过 0.1%"

  - alert: "order-service_HighP99Latency"
    expr: 'histogram_quantile(0.99, rate(http_server_requests_seconds_bucket{service="order-service"}[5m])) > 0.2'
    for: "3m"
    labels:
      severity: warning
      team: "backend"
    annotations:
      summary: "服务 order-service P99 延迟超过 200ms"

  # ...（其他规则省略，详见 examples/monitoring-rules.yaml）

business_metrics:
  - name: "order-service_core_api_latency"
    type: histogram
    labels: ["api_path", "method"]
    buckets: [50, 100, 200, 500, 1000, 2000]
```

---

## Gate 2 人工评审清单

`monitoring-rules.yaml` 生成后，必须随 `high-level-design` 产出物一并进入 **Gate 2 设计冻结闸** 评审。请按以下清单逐项确认：

### 覆盖度检查

- [ ] **所有服务节点是否已覆盖？**
  - 检查 `scrape_configs` 中是否包含每个后端服务的 `job_name`
  - 特别关注：是否有遗漏的微服务、定时任务服务、后台 worker

- [ ] **所有中间件是否已覆盖？**
  - 数据库（MySQL/PostgreSQL/MongoDB/Elasticsearch）
  - 缓存（Redis/Memcached）
  - 消息队列（Kafka/RabbitMQ/RocketMQ）
  - 网关（Nginx/Kong/Spring Cloud Gateway）

- [ ] **部署形态是否匹配？**
  - K8s 环境应包含 `infra-k8s.yaml` 的 Pod/Node 级规则
  - 裸机/Docker 环境应包含 `infra-docker.yaml`（如有）或节点级 exporter 规则
  - 避免 K8s 与 Docker 模板同时命中导致的重复采集

### 阈值合理性检查

- [ ] **API 延迟阈值是否符合业务容忍度？**
  - 用户-facing 接口（如商品详情页）：通常 P99 < 200ms
  - 内部服务间调用：通常 P99 < 500ms
  - 批处理/报表接口：可放宽至 P99 < 3000ms

- [ ] **错误率阈值是否过松/过紧？**
  - 核心支付链路：建议 < 0.1%（甚至 < 0.01%）
  - 非核心查询接口：可放宽至 < 1%
  - 注意：阈值过紧会导致告警风暴，过松会漏掉真实故障

- [ ] **资源使用率阈值是否留有缓冲？**
  - CPU 80% / 内存 85% 是通用默认值
  - 若服务有突发流量（如秒杀），建议预留更多缓冲（CPU 70%）

### 规则有效性检查

- [ ] **expr 语法是否正确？**
  - 确认使用的监控后端支持 `rate()` 和 `histogram_quantile()`
  - 云监控（如阿里云 CMS）需将 PromQL 转译为对应 DSL

- [ ] **business_metrics 中的埋点是否完整？**
  - 核心链路（下单 → 支付 → 回调）是否都有 latency histogram
  - 关键业务事件（订单创建、支付成功、退款）是否都有 counter

- [ ] **标签（labels）是否足够用于后续排障？**
  - 建议至少包含：`service`, `instance`, `env`, `team`
  - 业务指标建议额外包含：`api_path`, `method`, `status`

### 确认动作

评审通过后，执行：

```
/skill:human gate=Gate2 action=sign-off
```

⚠️ **未获得人工确认前，禁止进入 `detailed-design` 或编码实现阶段。**

---

## 技术栈适配速查

| 你的技术栈 | 会匹配的模板 | 需要的 Exporter / 埋点库 |
|---|---|---|
| Spring Boot | `app-jvm-springboot.yaml` | Micrometer + Prometheus Registry（内置） |
| NestJS / Express | `app-node.yaml` | prom-client + 中间件埋点 |
| FastAPI / Flask | `app-python.yaml` | prometheus_client + 装饰器埋点 |
| Go / Gin | `app-go.yaml` | prometheus/client_golang + 中间件 |
| Vue3 / React | `app-frontend.yaml` | Web Vitals API + 自定义 RUM SDK |
| MySQL | `db-mysql.yaml` | mysqld-exporter |
| PostgreSQL | `db-postgresql.yaml` | postgres-exporter |
| Redis | `cache-redis.yaml` | redis-exporter |
| Kafka | `mq-kafka.yaml` | kafka-exporter |
| Nginx | `gw-nginx.yaml` | nginx-prometheus-exporter 或 VTS 模块 |
| Kubernetes | `infra-k8s.yaml` | kube-state-metrics + node-exporter |

---

## 常见问题与排错

### Q1：生成的 monitoring-rules.yaml 中缺少某个中间件（如 MongoDB）

**原因**：当前模板库暂未覆盖该技术栈。

**解决**：
1. 在 `config.yaml` 的 `tech_stack_mapping` 中新增映射
2. 在 `templates/` 下新建 `{category}-{tech}.yaml` 模板文件
3. 参考现有模板结构，填写 `scrape_configs`、`alerting_rules`、`business_metrics`
4. 重新运行 `python scripts/validate.py --skill skills/sdlc/monitoring-setup`

### Q2：告警阈值全部使用了默认值，与设计文档中的要求不符

**原因**：设计文档（`05-non-functional.md`）中未明确写出具体数值，或数值格式无法被正则提取。

**解决**：
- 短期：在 Gate 2 评审时手动修改 `ops/monitoring-rules.yaml` 中的阈值
- 长期：规范 `05-non-functional.md` 的编写格式，使用"指标 < 数值"的标准写法

### Q3：两个服务使用了相同技术栈，job_name 冲突了

**现象**：Prometheus 只保留了最后一个服务的采集任务。

**原因**：合并时未正确添加服务名前缀。

**解决**：检查生成的 YAML 中 `job_name` 是否已自动添加前缀（如 `order-service-actuator` vs `pay-service-actuator`）。若未添加，在 `SKILL.md` 的"多模板合并"逻辑中强制要求：冲突时必须添加 `{{service_name}}-` 前缀。

### Q4：expr 中有 `{{memory_limit_bytes}}` 等未替换的变量

**原因**：设计文档未提供容器/进程内存限制信息，且模板中该变量无默认值。

**解决**：
- 手动在 YAML 中填入实际内存限制（如 `1073741824` 表示 1GB）
- 或在 `config.yaml` 的 `default_thresholds` 中补充该变量的默认值

### Q5：我的项目使用云监控（阿里云 CMS / AWS CloudWatch），不是 Prometheus

**原因**：当前模板使用 PromQL 语法，与云监控 DSL 不兼容。

**解决**：
- **方案 A**：在基础设施层使用 Prometheus Remote Write 或 exporter 将指标写入云监控，保留现有 YAML 结构
- **方案 B**：新增云监控专用模板集（如 `templates/cloud-aliyun-cms/`），将 PromQL 转译为对应 DSL
- **方案 C**：在 Gate 2 评审时，由 SRE 手动将 `expr` 转译为云监控查询语句

### Q6：能否重复执行 monitoring-setup？

**回答**：**不建议。** 本 Skill 设计为一次性执行。若重复执行：
- 会覆盖 `ops/monitoring-rules.yaml` 上的所有人工调整
- 会丢失 Gate 2 评审后修改的阈值、标签、注释

如需更新监控规则，建议：
1. 手动编辑 `ops/monitoring-rules.yaml`
2. 或使用下游 Skill `monitoring-analysis` 进行周期性调优建议

---

## 扩展指南

### 新增一个技术栈模板

以 **MongoDB** 为例：

**Step 1：注册映射**

编辑 `skills/sdlc/monitoring-setup/config.yaml`：

```yaml
tech_stack_mapping:
  # ... 现有映射
  db_mongodb:
    keywords: ["MongoDB", "Mongo", "NoSQL"]
    template: "db-mongodb.yaml"
```

**Step 2：创建模板**

新建 `skills/sdlc/monitoring-setup/templates/db-mongodb.yaml`：

```yaml
meta:
  tech_stack: "db_mongodb"
  version: "1.0"

scrape_configs:
  - job_name: "{{service_name}}-mongodb"
    static_configs:
      - targets: ["{{host}}:{{port}}"]

alerting_rules:
  - alert: "{{service_name}}_MongoConnectionsHigh"
    expr: 'mongodb_connections{service="{{service_name}}",state="current"} > {{db_connections_threshold}}'
    for: "2m"
    labels:
      severity: critical
      team: "{{team_name}}"
    annotations:
      summary: "MongoDB {{service_name}} 连接数超过阈值"

business_metrics:
  - name: "{{service_name}}_query_duration"
    type: histogram
    labels: ["database", "operation"]
    buckets: [1, 5, 10, 25, 50, 100]
```

**Step 3：校验**

```bash
python scripts/validate.py --skill skills/sdlc/monitoring-setup
```

**Step 4：更新索引（如需发布）**

`index.json` 通常无需修改，除非变更了 Skill 的 `description` 或 `metadata`。

### 修改默认阈值

编辑 `skills/sdlc/monitoring-setup/config.yaml` 中的 `default_thresholds`：

```yaml
default_thresholds:
  api_p99_latency_ms: 300        # 从 500 调整为 300
  api_error_rate_percent: 0.5    # 从 1.0 调整为 0.5
  # ...
```

修改后对所有**后续新生成**的项目生效，不影响已存在的 `ops/monitoring-rules.yaml`。

---

## 变更日志

| 版本 | 日期 | 变更内容 |
|---|---|---|
| 1.0.0 | 2026-05-10 | 初始版本，支持 11 类技术栈模板，Prometheus 语法，Gate 2 人工评审节点 |
