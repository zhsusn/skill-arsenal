# progress-tracker（进度治理中枢）设计文档

**版本**: V2.1  
**最后更新**: 2026-05-08  
**对应 Skill**: `skills/sdlc/progress-tracker`  
**对应 meta.json 版本**: 1.1.0

---

## 1. 设计目标

`progress-tracker` Skill 的核心目标是**在软件交付全周期中维护进度的单一可信源（Single Source of Truth, SSOT）**，消除因多工具、多人员维护进度而导致的信息碎片化与信任危机。

具体目标包括：

| 目标编号 | 目标描述 | 验收标准 |
|---------|---------|---------|
| G1 | 建立进度 SSOT | 任何时刻只需查看 `progress.md` 即可获知项目真实进度 |
| G2 | 支持双轨制进度计算 | 前期按阶段权重粗算，后期按任务粒度精算，平滑过渡 |
| G3 | 人工闸门强管控 | 未通过 Gate 时锁定进度上限，禁止跳过人工评审 |
| G4 | 风险显性化 | 所有识别到的风险必须登记到 `progress.md`，关联到具体阶段/任务 |
| G5 | 运维左移预埋 | V2.1 起在初始化阶段同步创建运维资产目录，打通交付与运维 |

---

## 2. 核心概念

### 2.1 术语表

| 术语 | 定义 |
|------|------|
| **SSOT** | Single Source of Truth，单一可信源。项目进度的唯一权威数据源 |
| **双轨制** | 前期（需求/设计阶段）按阶段权重计算进度；后期（开发/测试阶段）按任务完成率精算 |
| **人工闸门（Gate）** | 关键里程碑处的人工评审节点：Gate 1（需求确认）、Gate 2.5（设计预审）、Gate 2（设计冻结）、Gate 3（上线审批） |
| **human_status** | V2.1 新增字段，记录当前所处的人工闸门状态：`gate1` / `gate2_5` / `gate2` / `gate3` |
| **进度上限锁定** | V2.1 新增规则：若当前阶段对应的人工闸门未通过，总进度不得超过该阶段的进度上限阈值 |
| **Red Flag** | 禁止性规则，违反时将触发警告并阻止操作（如禁止跳过 Gate） |
| **ops/ 目录** | V2.1 新增的项目级运维资产目录，存放 `staging-config.yaml`、`rollback-plan.md`、`monitoring-rules.yaml` |

### 2.2 设计哲学

- **进度是算出来的，不是猜出来的**：基于客观完成指标（阶段权重 / 任务状态）计算，杜绝「感觉完成了 80%」。
- **闸门是硬边界，不是建议**：未通过的 Gate 是物理阻塞，进度上限锁定 + 禁止跳过。
- **风险与进度同等重要**：没有风险登记的进度报告是不完整的。

---

## 3. 架构设计（IPO 模型）

### 3.1 输入（Input）

| 输入项 | 来源 | 格式 | 必填 | 说明 |
|--------|------|------|------|------|
| `progress.md` | 既有项目资产 | Markdown | 条件 | 初始化时无需，更新时必须 |
| `config.yaml` | 项目配置 | YAML | 是 | 阶段定义、权重、Gate 映射 |
| 任务状态 | 开发/测试工具 | JSON / 手动输入 | 条件 | 任务级更新时需要 |
| 人工 Gate 状态 | 评审系统 / 手动标记 | 枚举值 | 是 | `pending` / `passed` / `failed` |
| 风险描述 | 团队成员输入 | 文本 | 否 | 风险登记工作流 |

**config.yaml 关键字段示例**：

```yaml
project_name: order-platform
phases:
  - id: P1
    name: 需求分析
    weight: 10                    # 该阶段占总进度的权重 (%)
    gate: gate1                   # 关联的人工闸门
    gate_progress_cap: 10         # 未通过 Gate 时的进度上限
  - id: P2
    name: 概要设计
    weight: 15
    gate: gate2_5
    gate_progress_cap: 25         # 10 + 15 = 25
  - id: P3
    name: 详细设计
    weight: 10
    gate: gate2
    gate_progress_cap: 35
  - id: P4
    name: 开发实现
    weight: 30
    gate: null                    # 无 Gate，按任务粒度计算
  - id: P5
    name: 测试验证
    weight: 15
    gate: null
  - id: P6
    name: UAT                     # V2.1 新增
    weight: 10
    gate: gate3
    gate_progress_cap: 90
  - id: P7
    name: 发布上线                # V2.1 新增
    weight: 5
    gate: gate3
    gate_progress_cap: 95
  - id: P8
    name: 监控运维                # V2.1 新增
    weight: 5
    gate: null

dual_track:
  threshold_phase: P4             # 从 P4 开始切换为任务级精算
```

### 3.2 处理（Process）

处理流程由 **5 个工作流** 构成：

```
┌─────────────────┐
│   工作流集合     │
├─────────────────┤
│  W1: 初始化      │
│  W2: 阶段完成更新 │
│  W3: 任务级更新   │
│  W4: 查看进度     │
│  W5: 风险登记     │
└─────────────────┘
```

#### W1: 初始化（Initialize）

触发条件：项目首次使用 progress-tracker，或 `progress.md` 不存在。

处理步骤：

1. 读取 `config.yaml`，解析 12 个阶段定义（V2.1 扩展为 12 阶段）。
2. 创建 `progress.md` 骨架，包含：
   - `phases`：各阶段状态（`not_started` / `in_progress` / `completed`）。
   - `human_status`：V2.1 新增，初始值为 `gate1`。
   - `tasks_summary`：空结构，预留任务级精算。
   - `risks`：空列表。
3. **V2.1 新增**：创建项目级 `ops/` 目录及初始文件：
   - `ops/staging-config.yaml`
   - `ops/rollback-plan.md`
   - `ops/monitoring-rules.yaml`
4. 输出初始化报告，列出已创建的文件与目录。

#### W2: 阶段完成更新（Phase Complete Update）

触发条件：某阶段工作完成，团队标记该阶段为 `completed`。

处理步骤：

1. 校验目标阶段的前置阶段是否已全部完成（**禁止跳阶段**）。
2. 检查该阶段关联的 Gate 状态：
   - 若 Gate 状态为 `pending` 或 `failed`：
     - **V2.1 新增**：触发 **进度上限锁定**——总进度不得超过 `gate_progress_cap`。
     - 返回 Red Flag 警告："Gate {gate_name} 未通过，进度已锁定在 {cap}%。"
   - 若 Gate 状态为 `passed`：允许更新阶段状态。
3. 更新 `phases` 中对应阶段状态为 `completed`，重新计算总进度。
4. 更新 `human_status` 为下一个 Gate（如完成 Gate 1 对应阶段后，`human_status` → `gate2_5`）。

#### W3: 任务级更新（Task-Level Update）

触发条件：进入双轨制精算阶段（默认从 `P4 开发实现` 开始），团队成员更新具体任务状态。

处理步骤：

1. 接收任务清单更新，格式示例：
   ```json
   {
     "phase_id": "P4",
     "tasks": [
       { "task_id": "T-401", "status": "completed", "assignee": "dev-a" },
       { "task_id": "T-402", "status": "in_progress", "assignee": "dev-b" }
     ]
   }
   ```
2. 校验任务所属阶段是否在 `dual_track.threshold_phase` 及之后。
3. 计算该阶段任务完成率：`completed_count / total_count`。
4. 将该阶段的进度从「权重占比」替换为「权重 × 任务完成率」。
5. 重新汇总总进度。

**双轨制进度计算公式**：

```
IF current_phase < threshold_phase:
    progress = SUM(completed_phases_weights)
ELSE:
    coarse = SUM(completed_phases_before_threshold)
    fine = SUM(threshold_and_after_phases_weights × task_completion_rate)
    progress = coarse + fine

# V2.1 新增：应用进度上限锁定
IF human_gate_not_passed:
    progress = MIN(progress, gate_progress_cap)
```

#### W4: 查看进度（View Progress）

触发条件：用户询问当前进度。

处理步骤：

1. 读取当前 `progress.md`。
2. 按以下格式生成进度报告：
   - 总进度百分比（已应用上限锁定）。
   - 各阶段状态一览（✅ 完成 / 🔄 进行中 / ⬜ 未开始）。
   - 当前所处 `human_status`。
   - 待处理风险列表（高优先级前置）。
   - 下一项建议行动。

#### W5: 风险登记（Risk Register）

触发条件：团队成员识别到新风险，或已有风险状态变更。

处理步骤：

1. 接收风险信息：
   ```json
   {
     "risk_id": "R-005",
     "description": "第三方支付接口限流策略变更，可能影响订单支付成功率",
     "phase_id": "P4",
     "task_id": "T-415",
     "severity": "high",        // low / medium / high / critical
     "probability": "medium",   // low / medium / high
     "mitigation": "联系支付平台确认新限流阈值，准备降级方案",
     "owner": "dev-c",
     "status": "open"           // open / mitigated / closed / accepted
   }
   ```
2. 校验 `phase_id` 和 `task_id` 的合法性。
3. 追加到 `progress.md` 的 `risks` 列表，按严重程度和发生概率排序。
4. 若风险严重程度为 `critical` 且状态为 `open`，在进度报告中附加 ⚠️ 醒目提示。

### 3.3 输出（Output）

| 输出产物 | 路径 | 格式 | 说明 |
|---------|------|------|------|
| 进度主文档 | `{project-root}/progress.md` | Markdown | SSOT，所有进度信息的唯一权威源 |
| 进度报告 | 对话输出 | Markdown | 面向人类的可读进度摘要 |
| 运维资产 | `{project-root}/ops/` | YAML / Markdown | V2.1 新增，初始化时创建 |
| 风险登记 | 内嵌于 `progress.md` | Markdown 表格 | 按严重程度排序 |
| 操作日志 | 内嵌于 `progress.md` 尾部 | Markdown 列表 | 记录每次更新的时间、操作人、变更内容 |

---

## 4. 状态机与数据模型

### 4.1 人工闸门状态机（human_status）

```
┌─────────┐     需求评审通过      ┌───────────┐     设计预审通过      ┌─────────┐
│  gate1  │────────────────────►│  gate2_5  │────────────────────►│  gate2  │
│ (初始)  │                     │ (设计预审) │                     │(设计冻结)│
└─────────┘                     └───────────┘                     └────┬────┘
                                                                       │
                                                                       │ 上线审批通过
                                                                       ▼
                                                              ┌─────────────┐
                                                              │    gate3    │
                                                              │  (上线审批)  │
                                                              └─────────────┘
```

状态转移规则：

| 转移 | 触发条件 | 副作用 |
|------|---------|--------|
| gate1 → gate2_5 | Gate 1 评审通过（`passed`） | `human_status` 更新，解锁 P2 进度上限 |
| gate2_5 → gate2 | Gate 2.5 评审通过 | `human_status` 更新，解锁 P3 进度上限 |
| gate2 → gate3 | Gate 2 评审通过 | `human_status` 更新，解锁 P4~P5 进度上限 |
| gate3 → （完结） | Gate 3 评审通过 | 项目进入发布/监控阶段，无后续 Gate |
| * → （阻塞） | 任意 Gate 评审失败（`failed`） | 进度上限锁定在对应 `gate_progress_cap`，必须重审 |

### 4.2 阶段状态机（单阶段）

```
┌─────────────┐    阶段工作启动      ┌─────────────┐    工作完成+Gate通过   ┌─────────────┐
│ not_started │────────────────────►│ in_progress │─────────────────────►│  completed  │
└─────────────┘                     └──────┬──────┘                      └─────────────┘
                                           │
                                           │ Gate 未通过 / 发现阻塞风险
                                           ▼
                                    ┌─────────────┐
                                    │   blocked   │
                                    └─────────────┘
```

### 4.3 progress.md 数据模型

```markdown
---
project_name: order-platform
version: 2.1
last_updated: 2026-05-08T14:00:00Z
---

# Project Progress

## Human Status
`gate2`   <!-- V2.1 新增字段 -->

## Phases

| ID | 名称 | 权重 | 状态 | 完成率 | Gate | 进度上限 |
|----|------|------|------|--------|------|----------|
| P1 | 需求分析 | 10% | completed | 100% | gate1 | 10% |
| P2 | 概要设计 | 15% | completed | 100% | gate2_5 | 25% |
| P3 | 详细设计 | 10% | completed | 100% | gate2 | 35% |
| P4 | 开发实现 | 30% | in_progress | 45% | - | - |
| P5 | 测试验证 | 15% | not_started | 0% | - | - |
| P6 | UAT | 10% | not_started | 0% | gate3 | 90% |
| P7 | 发布上线 | 5% | not_started | 0% | gate3 | 95% |
| P8 | 监控运维 | 5% | not_started | 0% | - | - |

> **Current Progress: 48.5%** (locked at cap if Gate not passed)

## Tasks Summary (Dual-Track)

### P4: 开发实现

| Task ID | 描述 | 负责人 | 状态 |
|---------|------|--------|------|
| T-401 | 订单服务接口开发 | dev-a | completed |
| T-402 | 支付回调处理 | dev-b | in_progress |
| ... | ... | ... | ... |

## Risks

| ID | 描述 | 阶段 | 严重度 | 概率 | 应对措施 | 负责人 | 状态 |
|----|------|------|--------|------|----------|--------|------|
| R-001 | 第三方接口限流 | P4 | high | medium | 联系平台确认阈值 | dev-c | open |

## Change Log

- 2026-05-08 14:00 | 更新 P4 任务状态 (T-401 completed) | by: progress-tracker
- 2026-05-07 09:30 | Gate 2 通过，human_status 更新为 gate3 | by: arch-lead
```

### 4.4 进度上限锁定规则（V2.1 新增）

```python
def calculate_progress(phases, human_status, tasks_summary):
    raw_progress = compute_dual_track(phases, tasks_summary)
    
    # 查找当前 human_status 对应的进度上限
    cap = None
    for phase in phases:
        if phase.gate == human_status and phase.gate != null:
            cap = phase.gate_progress_cap
            break
    
    if cap is not None:
        return min(raw_progress, cap)
    return raw_progress
```

---

## 5. 集成方案

### 5.1 上游依赖

| 上游 Skill / 实体 | 集成方式 | 数据契约 |
|------------------|---------|---------|
| `prd-generation` | 文件系统 | PRD 文档确认后，触发 progress-tracker 初始化 |
| `high-level-design` | 文件系统 | Gate 2 冻结后，progress-tracker 更新 `human_status` 为 `gate3` 前置准备 |
| 人工评审 | 状态文件 / API | `.gate-status/{gate-name}` 文件值为 `passed` / `failed` / `pending` |

### 5.2 下游消费

| 下游 Skill / 实体 | 消费内容 | 触发条件 |
|------------------|---------|---------|
| `executing-plans` | 当前阶段与任务清单 | 任务级更新后 |
| `monitoring-setup` | `ops/monitoring-rules.yaml` | V2.1 初始化时创建，monitoring-setup 可读取并扩展 |
| 项目管理者 | 进度报告与风险列表 | 查看进度工作流 |

### 5.3 文件系统约定

```
{project-root}/
├── progress.md                      # SSOT 进度文档
├── config.yaml                      # 阶段与权重配置
├── ops/                             # V2.1 新增：运维资产目录
│   ├── staging-config.yaml
│   ├── rollback-plan.md
│   └── monitoring-rules.yaml
└── .gate-status/
    ├── gate1           # 内容: passed / failed / pending
    ├── gate2_5
    ├── gate2
    └── gate3
```

---

## 6. 文件格式规范

### 6.1 progress.md 规范

- 文件编码：UTF-8，LF 换行。
- 顶部 Frontmatter 必须包含 `project_name`、`version`、`last_updated`。
- `## Human Status` 为 V2.1 新增必填节，值为当前所处 Gate。
- `## Phases` 表格必须包含 `进度上限` 列（V2.1 新增）。
- `## Tasks Summary` 仅在进入双轨制精算阶段后填充。
- `## Risks` 表格按 `严重度 × 概率` 降序排列。
- `## Change Log` 逆序排列，最新记录在前。

### 6.2 ops/ 目录初始文件模板（V2.1）

**ops/staging-config.yaml**：

```yaml
# Generated by progress-tracker V2.1
environment: staging
database:
  host: "localhost"
  port: 5432
  name: "order_platform_staging"
features:
  flags: {}
```

**ops/monitoring-rules.yaml**：

```yaml
# Generated by progress-tracker V2.1
version: "1.0"
rules: []
# TODO: 由 monitoring-setup Skill 扩展
```

---

## 7. 安全与审计

### 7.1 输入安全

- 任务状态更新必须校验 `task_id` 格式（`T-{phase_number}{seq}`），防止注入。
- 风险描述中的 HTML / Markdown 特殊字符需转义。

### 7.2 状态一致性

- `progress.md` 必须加文件锁（或采用原子写：先写 `.progress.md.tmp` 再重命名），防止并发更新丢失数据。
- `human_status` 的更新只能由 Gate 状态驱动，禁止手动随意修改。

### 7.3 Red Flag 规则（禁止跳过人工闸门）

以下操作将被拒绝并返回 Red Flag：

| 规则编号 | 规则描述 | 触发后果 |
|---------|---------|---------|
| RF-001 | 尝试标记阶段为 completed，但其关联 Gate 状态不为 `passed` | 操作拒绝，返回警告 |
| RF-002 | 尝试将 `human_status` 从 `gate1` 直接跳至 `gate2`（跳过 `gate2_5`） | 操作拒绝，返回警告 |
| RF-003 | 尝试在未完成前置阶段的情况下，标记后续阶段为 completed | 操作拒绝，返回警告 |
| RF-004 | 双轨制精算阶段，任务完成率超过 100% 或小于 0% | 数据校验失败，拒绝写入 |

### 7.4 审计追踪

`progress.md` 尾部的 `## Change Log` 必须记录：
- 每次阶段状态变更。
- 每次任务级批量更新（记录任务数量与影响阶段）。
- 每次风险新增/状态变更。
- 每次 `human_status` 变更（含 Gate 审批人信息）。

---

## 8. 后期演进方向

| 版本 | 演进项 | 优先级 |
|------|--------|--------|
| V2.2 | 支持多项目聚合视图（Portfolio 级进度看板） | 中 |
| V2.2 | 与 GitHub/GitLab Issues 自动同步任务状态 | 高 |
| V2.3 | 风险自动关联相似历史风险（知识库匹配） | 中 |
| V2.3 | 支持燃尽图（Burndown Chart）Mermaid 自动生成 | 低 |
| V3.0 | 引入预测性进度分析（基于历史速率预测完工日期） | 低 |
| V3.0 | 与 CI/CD  pipeline 集成，自动更新阶段状态 | 高 |

---

## 附录 A：接口定义速查

### A.1 Skill 触发接口（伪代码）

```
invoke(skill="progress-tracker", workflow="W1", inputs={
  "config_path": "config.yaml",
  "project_root": "."
})

invoke(skill="progress-tracker", workflow="W3", inputs={
  "progress_path": "progress.md",
  "task_updates": [
    { "phase_id": "P4", "task_id": "T-401", "status": "completed" }
  ]
})

invoke(skill="progress-tracker", workflow="W5", inputs={
  "progress_path": "progress.md",
  "risk": {
    "risk_id": "R-005",
    "description": "...",
    "severity": "high",
    "phase_id": "P4"
  }
})
```

### A.2 进度查询接口

```python
def query_progress(progress_path: str) -> dict:
    progress = parse_progress_md(progress_path)
    return {
        "total_progress": progress.calculate(),          # 已应用上限锁定
        "raw_progress": progress.calculate_raw(),        # 未锁定前的原始进度
        "human_status": progress.human_status,
        "blocked_by_gate": progress.get_blocking_gate(), # 若被锁定，返回哪个 Gate
        "open_risks": progress.risks.filter(status="open"),
        "next_recommended_action": progress.suggest_next_action()
    }
```
