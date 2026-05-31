# Brainstorming → 下游 Skill 衔接契约

## 下游 Skill

Brainstorming 完成后，必须衔接 `prd-generation`（概要需求生成）。

**禁止直接衔接**：
- `writing-plans`（实现计划）：未生成 PRD 前不得编写实现计划
- `executing-plans`（编码执行）：未通过设计评审前不得编码
- `high-level-design`（概要设计）：除非预检结论明确建议先进行技术选型评审

## 传递包 (Handover Package)

### 必需项

| 传递项 | 格式 | 说明 |
|--------|------|------|
| `requirement-draft.md` | 文件路径 | 结构化需求摘要，prd-generation 的核心输入 |
| `research-report.md` | 文件路径 | 资料收集报告，用于 prd-generation 补充背景 |
| `brainstorming-log.md` | 文件路径 | 完整问答日志，用于追溯决策依据 |
| `clarification_score` | float | 澄清度评分（0-1），必须 ≥ 0.8 |
| `red_flags` | string[] | 未解决的风险点和待确认项 |
| `key_metrics` | object | 关键数值口径清单，必须包含：Skill 数量、用户规模、性能基线、容量上限。格式见下。 |
| `data_calibration` | string | 数据口径声明文件路径（`requirement-draft.md` 中的 `## 数据口径声明` 章节） |

### 可选项

| 传递项 | 格式 | 说明 |
|--------|------|------|
| `knowledge_graph_tags` | string[] | 关联的历史模块/技术/规则标签 |
| `preflight_conclusions` | object | 技术预检结论（技术债务、风险、约束） |
| `recommended_strategy` | object | 智能推荐后续路径 |

### 传递示例

```yaml
handover_package:
  requirement_draft: "openspec/changes/rendering-refactor/brainstorming/requirement-draft.md"
  research_report: "openspec/changes/rendering-refactor/brainstorming/research-report.md"
  brainstorming_log: "openspec/changes/rendering-refactor/brainstorming/brainstorming-log.md"
  clarification_score: 0.85
  red_flags:
    - "GPU 实时预览与现有 CPU 批处理架构冲突，需确认双模式策略"
    - "企业客户兼容性问题尚未完全澄清"
  key_metrics:
    skill_count_sdlc: 25
    skill_count_total: 41
    skill_count_source: "skill-arsenal/skills/sdlc 目录扫描"
    skill_count_rationale: "MVP 聚焦 SDLC 阶段，仅使用 sdlc 子目录下的 25 个核心 Skill；平台架构支持扩展至 41 个"
    skill_count_conflict_status: "已声明"  # 新增：冲突是否已显式声明
    concurrent_users_mvp: 10
    concurrent_users_source: "团队规模估算"
  data_calibration: "openspec/changes/{变更名}/brainstorming/requirement-draft.md#数据口径声明"
  knowledge_graph_tags:
    - "模块:渲染中心"
    - "技术:FFmpeg"
    - "规则:权限继承"
  preflight_conclusions:
    tech_debts:
      - "Celery 任务队列适合批处理，实时预览需引入 WebSocket"
    risks:
      - "GPU 实时预览需 RTX 4090 级别硬件，成本增加"
    constraints:
      - "必须兼容现有 RBAC 权限模型"
  recommended_strategy:
    next_skill: "prd-generation"
    reason: "需求已澄清，可直接进入概要需求生成"
```

## 条件分支触发

Brainstorming 完成后，根据预检结论选择下游路径：

```
brainstorming 完成
    │
    ├─ 澄清度 < 0.8 ──→ 返回 brainstorming，补充提问
    │
    ├─ 澄清度 ≥ 0.8 + 技术债务高 ──→ 建议先触发 high-level-design（技术选型评审）
    │                       └─ 用户确认后进入设计阶段
    │
    └─ 澄清度 ≥ 0.8 + 标准情况 ──→ 触发 prd-generation（正常路径）
```

**技术债务高的判定标准**（满足任一）：
- 涉及架构模式变更（如从批处理改为实时流）
- 引入与现有技术栈冲突的新技术（如项目用 REST，需求提到 GraphQL）
- 需要修改核心数据模型或权限体系
- 性能需求超出历史基线 10 倍以上

## 异常处理

### 用户拒绝确认
若用户不愿书面确认需求摘要：
- 标记 `red_flags: ["用户未正式确认需求摘要"]`
- 允许进入 prd-generation，但必须在 `requirement-draft.md` 中显式标注
- prd-generation 生成后需再次提请用户确认

### 澄清度不达标
若 5 轮后澄清度仍 < 0.8：
- 输出当前最佳摘要
- 标记 `[风险] 需求未完全澄清`
- 列出未澄清项清单
- 允许进入 prd-generation，但附加风险提示

### 资料收集失败
- 网络搜索无结果：扩大关键词，仍无则标记并继续
- 本地文件不存在：提示用户，跳过并记录
- 混合模式冲突：按 `local_first` 规则处理，向用户确认

## 会话初始化模板

当新会话衔接 prd-generation 时，携带最小必要上下文：

```text
【会话初始化 | 阶段 1 → 阶段 2】

变更：{变更名}
阶段：阶段 2 概要需求生成
上游：brainstorming 已完成，澄清度 {score}

参考文档：
- @openspec/changes/{变更名}/brainstorming/requirement-draft.md
- @openspec/changes/{变更名}/brainstorming/research-report.md

未解决风险：
- {风险 1}
- {风险 2}

请基于以上上下文继续工作。
```
