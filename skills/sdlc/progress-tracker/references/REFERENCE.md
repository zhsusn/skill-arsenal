# Progress Tracker 详细参考

## 0. 项目上下文自动推断规则

本 Skill 遵循**最小输入原则**。在初始化时，优先通过扫描现有项目文件自动推断上下文，仅在无法推断时向用户询问。

### 推断源映射表

| 目标字段 | 推断源文件 | 推断规则 |
|----------|-----------|----------|
| `project` | 当前目录名 / git repo name / `package.json` name | 优先级：目录名 → git remote → package.json name |
| `tech_stack` | `package.json` dependencies / `pyproject.toml` / `requirements.txt` / `Cargo.toml` / `go.mod` / `pom.xml` | 识别关键依赖项，映射为技术栈描述 |
| `database` | `docker-compose.yml` / `prisma/schema.prisma` / `settings.py` DATABASES / `application.yml` | 识别 PostgreSQL / MySQL / MongoDB / Redis 等关键字 |
| `core_modules` | `src/` / `apps/` / `services/` / `packages/` 的一级子目录 | 过滤 `utils`、`common`、`test` 等非业务目录，取前 5 个 |
| `team` | `git shortlog -sn` 的 contributor 数量 | 仅作参考，不强制要求；默认值为 "未指定" |

### 推断失败处理

若上述所有推断源均不存在（如空目录或纯文档项目），Skill 会：
1. 将 `context` 字段留空或使用占位符
2. 向用户展示推断失败的文件清单
3. 询问用户是否手动补充，或接受空值并在后续阶段再填充

---

## 1. 数据模型（SSOT）

### 1.1 progress.md 结构

采用 YAML frontmatter + Markdown body 的混合格式，兼顾机器解析与人工阅读。

```markdown
---
meta:
  project: example-project          # 自动推断或用户确认
  change_id: feature-demo
  version: "1.0"
  last_updated: "2026-05-05T15:30:00+08:00"
  overall_progress: 35
  current_phase: detailed-requirements
  current_phase_status: in_progress

context:                            # 自动推断生成的项目上下文
  project: example-project
  tech_stack: "Vue3 + FastAPI + PostgreSQL"
  core_modules: ["user", "order", "payment"]
  team: "3 contributors"
  inferred_at: "2026-05-05T15:30:00+08:00"
  inference_sources: ["package.json", "docker-compose.yml", "src/"]

phases:
  - id: high-level-requirements
    name: 概要需求
    status: completed
    weight: 10
    progress: 100
    planned_days: 2
    actual_days: 2
    completed_at: "2026-05-03"
    gate_passed: true

  - id: detailed-requirements
    name: 详细需求
    status: in_progress
    weight: 15
    progress: 60
    planned_days: 3
    actual_days: 2
    started_at: "2026-05-04"
    gate_passed: false

tasks_summary:
  total: 24
  completed: 8
  in_progress: 3
  blocked: 1
  completion_rate: 33.3

risks:
  - id: R-001
    description: "角色数据模型字段可能变动，影响详细设计"
    impact: high
    probability: medium
    status: open
    mitigation: "在接口驱动阶段增加 mock 验证环节"
    owner: "@product"
    created_at: "2026-05-04"
---

# 总体进度：feature-demo

> 最后更新：2026-05-05 15:30  
> 整体进度：**35%** | 当前阶段：**详细需求（60%）**

## 阶段进度看板

| 阶段 | 状态 | 进度 | 计划 | 实际 | 完成日期 |
|------|------|------|------|------|----------|
| 概要需求 | ✅ 已完成 | 100% | 2天 | 2天 | 05-03 |
| 详细需求 | 🔄 进行中 | 60% | 3天 | 2天 | - |
| 概要设计 | ⏳ 未开始 | 0% | 2天 | - | - |

## 当前任务燃尽（P0 模块）

| 任务ID | 描述 | 状态 | 自测 | 优先级 |
|--------|------|------|------|--------|
| T-001 | 角色基础字段定义 | ✅ | ✅ 通过 | P0 |
| T-002 | 角色分类体系设计 | ✅ | ✅ 通过 | P0 |
| T-003 | 角色关系图谱 | 🔄 | ⏳ 待测 | P0 |

## 风险与阻碍

| ID | 风险描述 | 影响 | 概率 | 状态 | 应对方案 |
|----|---------|------|------|------|----------|
| R-001 | 角色数据模型字段可能变动 | 高 | 中 | 🟡 开放 | 接口驱动阶段增加 mock 验证 |
```

### 1.2 tasks.md 格式

与 `task-breakdown` Skill 产出格式兼容，增加 `verified_by` 字段用于自测门控。

```markdown
# 任务清单：feature-demo

> 生成时间：2026-05-04  
> 总任务数：24 | 已完成：8 | 进行中：3

## Phase 1: 接口与基础设施（可并行）

- [x] T-001 [后端] 角色基础字段 Schema 定义
  - 验收：Pydantic Schema 通过校验
  - 依赖：无
  - 预估：25min
  - **verified_by**: self-check-passed

- [ ] T-003 [后端] 角色分类体系 ER 图
  - 验收：DDL 通过评审
  - 依赖：T-001
  - 预估：20min
  - **verified_by**: pending
```

## 2. 进度计算算法

### 2.1 双轨制计算伪代码

```python
def calculate_overall_progress(progress_md, config_yaml, tasks_md):
    """
    双轨制计算：
    - 前期阶段（需求+设计）：按阶段权重加权平均
    - 后期阶段（开发+测试+交付）：按任务完成率精确计算
    """
    phases = config_yaml['phases']
    current_phase_id = progress_md['meta']['current_phase']
    current_idx = next(i for i, p in enumerate(phases) if p['id'] == current_phase_id)
    
    PRE_PHASE_COUNT = 6  # 前6个阶段为前期
    
    if current_idx < PRE_PHASE_COUNT:
        # 粗粒度：权重法
        completed_weight = sum(
            p['weight'] for p in phases[:current_idx] 
            if p['status'] == 'completed'
        )
        current_weight = phases[current_idx]['weight']
        current_progress = progress_md['phases'][current_idx]['progress'] / 100
        overall = completed_weight + (current_weight * current_progress)
    else:
        # 精粒度：任务完成率（仅统计 verified_by 通过的任务）
        tasks = parse_tasks_md(tasks_md)
        total = len(tasks)
        completed = len([
            t for t in tasks 
            if t['checked'] and t['verified_by'] in ['self-check-passed', 'user-confirmed', 'auto-passed']
        ])
        overall = sum(p['weight'] for p in phases if p['status'] == 'completed')
        impl_phase = phases[6]  # implementation
        overall += impl_phase['weight'] * (completed / total if total > 0 else 0)
    
    return round(overall, 1)
```

### 2.2 任务解析规则

- `total`：所有 `- [ ]` 或 `- [x]` 条目的总数
- `completed`：`- [x]` 且 `verified_by` 为通过状态的任务数
- `in_progress`：`- [ ]` 但有部分子任务完成，或存在依赖阻塞
- `blocked`：明确标记为阻塞，或依赖任务未完成导致无法开始

## 3. 门控校验引擎

### 3.1 声明式门控规则

```yaml
phases:
  - id: high-level-requirements
    gate_to_next:
      - artifact: specs/01-product-overview.md
        check: exists
      - artifact: specs/02-requirements-list.md
        check: sections_match
      - action: user_review
        label: "概要需求评审通过"

  - id: code-review
    gate_to_next:
      - artifact: code-review/review-report.yaml
        check: exists
      - artifact: code-review/review-report.yaml
        check: blocking_count == 0
      - action: self_check
        label: "代码审查通过，无阻塞性问题"
```

### 3.2 校验类型

| 校验类型 | 说明 |
|----------|------|
| `exists` | 文件存在性检查 |
| `sections_match` | 检查文件是否包含 required_sections 中定义的所有章节 |
| `glob_count >= N` | 匹配 glob 模式的文件数量是否达标 |
| `all_exist` | 所有匹配 glob 的文件均存在 |
| `tasks_all_le_30min` | 所有任务预估时间 ≤ 30 分钟 |
| `all_tasks_completed_and_verified` | 所有任务已勾选且 verified_by 通过 |
| `coverage >= N` | 测试覆盖率达标 |
| `user_review` | 人工评审签字确认 |
| `self_check` | 自动自查通过 |

### 3.3 门控伪代码

```python
def check_phase_transition(current_phase_id, config_yaml, change_dir, progress_md):
    phase_config = next(p for p in config_yaml['phases'] if p['id'] == current_phase_id)
    gates = phase_config.get('gate_to_next', [])
    
    results = []
    for gate in gates:
        if gate.get('action') == 'user_review':
            passed = check_user_signoff(progress_md, gate['label'])
        elif gate.get('action') == 'self_check':
            passed = check_self_check_report(change_dir)
        else:
            artifact_path = gate['artifact'].replace('{变更名}', change_id)
            passed = check_artifact(artifact_path, gate['check'])
        
        results.append({
            'rule': gate,
            'passed': passed,
            'blocker': not passed
        })
    
    return all(r['passed'] for r in results), results
```

## 4. 风险自动识别规则

内置风险检测模式：

| 触发条件 | 检测逻辑 | 风险模板 |
|----------|----------|----------|
| 延期 | `actual_days > planned_days * 1.2` | 阶段 {name} 已延期 {delta} 天 |
| 规格漂移 | 阶段完成后产出物被修改 | 检测到 {file} 在阶段完成后被修改 |
| 任务阻塞 | 存在 blocked 状态任务 | 当前有 {count} 个任务被阻塞 |
| 覆盖率不足 | 测试覆盖率 < 70% | 单元测试覆盖率 {rate}% 未达标 |

## 5. 归档联动规则

当收到 `opsx:archive` 信号时：
1. 校验所有阶段是否已完成（finish 阶段状态为 completed）
2. 将 `progress.md` 复制到 `openspec/archive/{变更名}/`
3. 在归档目录中追加归档摘要（归档时间、总体耗时、最终进度 100%）
4. 将 `changes/{变更名}/` 标记为已归档（progress.md 中 `meta.archived: true`）

## 6. 命名规范

- 变更名：kebab-case，如 `feature-role-factory`
- 任务 ID：T-XXX，如 `T-001`
- 风险 ID：R-XXX，如 `R-001`
- 阶段 ID：kebab-case，如 `high-level-requirements`
