# Monitoring Setup 实现指南

## 模板编写规范

每个模板文件必须包含三个标准段：

```yaml
meta:
  tech_stack: "标识名"
  version: "1.0"

scrape_configs:
  - job_name: "{{service_name}}-xxx"
    ...

alerting_rules:
  - alert: "{{service_name}}_AlertName"
    expr: '...'
    ...

business_metrics:
  - name: "{{service_name}}_metric_name"
    ...
```

## 变量占位符规范

| 占位符 | 来源 | 默认值 |
|--------|------|--------|
| `{{service_name}}` | 设计文档服务列表 | 必填 |
| `{{host}}` | 部署架构 | localhost |
| `{{port}}` | 设计文档或模板默认 | 8080/3306/6379 等 |
| `{{environment}}` | 设计文档 | staging |
| `{{project_name}}` | openspec/config.yaml | unknown |
| `{{team_name}}` | 设计文档 | unknown |
| `{{cpu_threshold}}` | config.yaml default_thresholds | 80 |
| `{{memory_threshold}}` | config.yaml default_thresholds | 85 |
| `{{error_rate_threshold}}` | config.yaml default_thresholds | 1.0 |
| `{{p99_latency_threshold}}` | config.yaml default_thresholds | 500 |
| `{{db_connections_threshold}}` | config.yaml default_thresholds | 80 |
| `{{cache_hit_rate_threshold}}` | config.yaml default_thresholds | 90 |
| `{{mq_consumer_lag_threshold}}` | config.yaml default_thresholds | 1000 |

## 新增技术栈模板步骤

1. 在 `config.yaml` `tech_stack_mapping` 下新增映射条目
2. 在 `templates/` 下新建 `{category}-{tech}.yaml` 文件
3. 确保模板包含 `meta`、`scrape_configs`、`alerting_rules`、`business_metrics` 四段
4. 运行 `python3 scripts/validate.py --skill skills/sdlc/monitoring-setup` 校验

## 告警级别定义

- **critical**：立即响应，可能伴随 PagerDuty/电话通知
- **warning**：工作时间内响应，Slack/邮件通知
- **info**：仅记录，不触发实时通知

## 兼容性说明

模板使用 Prometheus PromQL 标准语法。若目标后端为 VictoriaMetrics、Thanos、M3 或云监控，需注意：
- `histogram_quantile()` 在部分后端中 bucket 标签名可能不同
- `rate()` 要求至少两个数据点，初始启动时可能报空
- 云监控通常需将 expr 转译为对应查询语言（如阿里云的 CMS DSL）
