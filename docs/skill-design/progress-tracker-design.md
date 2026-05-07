# Progress Tracker 设计文档

> **版本**：1.0.0  
> **定位**：贯穿软件全生命周期的进度治理中枢 Skill  
> **设计依据**：`skills/info.txt` 规格说明、`skills/kimi+OpenSpec+superpower-v1.1.md` 10 阶段工作流  
> **兼容平台**：Kimi、Claude、Cursor、Codex、Gemini、Windsurf

---

## 1. 设计背景与动机

在 `kimi+OpenSpec+superpower-v1.1.md` 定义的 10 阶段 AI 项目落地工作流（概要需求 → 详细需求 → 概要设计 → 详细设计 → 接口驱动 → 任务拆解 → 编码 → 单元测试 → 集成测试 → 收尾）中，**进度不透明**和**阶段违规切换**是两大核心痛点：

- 开发者容易在阶段 1 尚未评审通过时，直接跳到阶段 7 写代码
- 任务完成状态依赖人工勾选，未自测的代码被错误地计入 100% 完成
- 风险与阻碍散落在多轮对话中，没有单一可信源（SSOT）

`skills/info.txt` 的调研进一步确认：**开源生态中没有即插即用的等价 Skill**。最接近的 Claude Code `Progress Tracker` 缺少阶段门控、风险登记和时间追踪；`OpenSpec Change Archiver` 仅在归档时触发验证，非实时门控。因此需要自研一个贯穿全生命周期的治理型 Skill。

---

## 2. 设计哲学

| 原则 | 说明 |
|------|------|
| **单一可信源（SSOT）** | `progress.md` 是所有 Skill 读写的唯一进度文件，禁止人工直接修改其 YAML frontmatter |
| **渐进式披露** | 遵循本项目三级加载规范：`SKILL.md` 提供触发规则与约束，`references/REFERENCE.md` 提供算法细节，`assets/config-template.yaml` 提供可定制模板 |
| **双轨制进度** | 前期（需求+设计）用阶段权重粗算，后期（开发+测试+交付）用任务级 Checkbox 精算，兼顾宏观可视与微观可控 |
| **质量门控驱动** | 进度 ≠ 勾选数。只有 `verified_by: self-check-passed` 的任务才算完成，从源头杜绝"假进度" |
| **声明式规则** | 阶段门控、Red Flags、产出物规格全部写入 `config.yaml`，项目可定制，Skill 只负责解释执行 |
| **最小输入原则** | Skill 优先通过扫描项目文件自动推断上下文（技术栈、模块、项目名），仅在推断失败或结果不确定时才向用户询问 |

---

## 3. 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                        项目文件系统                           │
│  package.json / pyproject.toml / go.mod / Dockerfile / src/  │
└──────────────┬──────────────────────────────────────────────┘
               │ 自动扫描推断（初始化时一次性）
               ▼
┌─────────────────────────────────────────────────────────────┐
│                     用户 / 其他 Skill                         │
│   (executing-plans / task-breakdown / self-check / user)    │
└──────────────┬──────────────────────────────────────────────┘
               │ 阶段完成信号 / 任务更新信号 / 风险登记指令
               ▼
┌─────────────────────────────────────────────────────────────┐
│                   Progress Tracker (Skill)                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │  进度计算引擎 │  │  门控校验引擎 │  │    风险检测引擎     │ │
│  │ (双轨制算法) │  │(config.yaml)│  │ (Red Flags + 自动) │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
└──────────────┬──────────────────────────────────────────────┘
               │ 读写
               ▼
┌─────────────────────────────────────────────────────────────┐
│                         SSOT 文件层                          │
│  openspec/config.yaml          ← 阶段定义、门控规则、规格标准  │
│  openspec/changes/{id}/        ← 变更目录                    │
│    ├── progress.md             ← 唯一进度可信源（YAML+Markdown）│
│    ├── tasks.md                ← 任务 Checkbox + verified_by │
│    └── specs/                  ← 各阶段产出物                │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. 数据模型

### 4.1 主文件：progress.md

采用 YAML frontmatter + Markdown body 的混合格式，兼顾机器解析与人工阅读。

```markdown
---
meta:
  project: example-project
  change_id: feature-demo
  version: "1.0"
  last_updated: "2026-05-05T15:30:00+08:00"
  overall_progress: 35
  current_phase: detailed-requirements
  current_phase_status: in_progress

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
| T-003 | 角色关系图谱 | 🔄 | ⏳ 待测 | P0 |

## 风险与阻碍

| ID | 风险描述 | 影响 | 概率 | 状态 | 应对方案 |
|----|---------|------|------|------|----------|
| R-001 | 角色数据模型字段可能变动 | 高 | 中 | 🟡 开放 | 接口驱动阶段增加 mock 验证 |
```

### 4.2 任务文件：tasks.md

兼容 `task-breakdown` Skill 产出格式，关键扩展是 `verified_by` 字段：

- `self-check-passed`：自测通过，可计入 completed
- `user-confirmed`：用户确认通过，可计入 completed
- `auto-passed`：自动化验证通过，可计入 completed
- `pending`：待验证，视为进行中

---

## 5. 核心算法

### 5.1 双轨制进度计算

```text
前期阶段（current_idx < 6）：
  overall = Σ(已完成阶段权重) + 进行中阶段权重 × 当前进度比例

后期阶段（current_idx ≥ 6）：
  completion_rate = verified_by通过的任务数 / 总任务数
  overall = Σ(已完成前期阶段权重) + implementation权重 × completion_rate
```

### 5.2 门控校验引擎

采用声明式规则：每个阶段在 `config.yaml` 中定义 `gate_to_next`，支持：

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

---

## 6. 风险检测机制

内置三类自动识别规则：

1. **延期风险**：`actual_days > planned_days × 1.2` 自动标红
2. **规格漂移**：阶段完成后产物文件被修改，触发 warning
3. **任务阻塞**：存在 `blocked` 状态任务时，自动列入风险表

---

## 7. 协作接口与依赖关系

### 7.1 必依赖的上下游 Skill

| 上下游 Skill | 交互方式 | 缺失时的影响 |
|-------------|----------|-------------|
| `task-breakdown` | 生成 `tasks.md` 后，progress-tracker 解析并初始化 `tasks_summary` | 无任务清单，无法计算开发阶段精粒度进度 |
| `executing-plans` | 每完成一个任务并自测通过后，发送信号触发进度重算 | 任务完成后需手动发送指令更新进度 |
| `self-check` | 提供产出物完整性报告，作为阶段门控的输入条件 | 阶段门控缺少自动化校验，仅依赖人工确认 |
| `finish` | 变更完成时，联动执行 `opsx:archive`，将 `progress.md` 同步归档 | 需手动复制 progress.md 到归档目录 |

### 7.2 依赖的框架与环境

| 依赖项 | 用途 | 替代方案 |
|--------|------|----------|
| OpenSpec 目录结构 (`openspec/changes/`) | 存放变更产物与进度文件 | 手动创建等效目录结构 |
| `opsx:propose` | 创建变更目录 | 手动 `mkdir openspec/changes/{变更名}` |
| `opsx:archive` | 触发归档联动 | 手动复制 `progress.md` 到 `openspec/archive/` |

---

## 8. 与开源 Skill 的能力对比

| 能力 | 本 Skill | Claude Progress Tracker | OpenSpec Archiver | Kanban Tracker |
|------|----------|------------------------|-------------------|----------------|
| SSOT 进度文件 | ✅ progress.md | ✅ feature_list.json | ❌ | ✅ Kanban.md |
| 阶段门控（声明式） | ✅ config.yaml | ❌ | ⚠️ 仅归档验证 | ❌ |
| 任务级 Checkbox 驱动 | ✅ tasks.md | ❌ | ❌ | ✅ |
| 自测通过才算完成 | ✅ verified_by | ❌ | ❌ | ❌ |
| 时间追踪（计划/实际） | ✅ | ❌ | ❌ | ❌ |
| 风险登记 | ✅ | ❌ | ❌ | ⚠️ 部分 |
| 产出物完整性校验 | ✅ artifact_specs | ❌ | ✅ | ❌ |
| Mermaid 可视化 | ✅ 自动甘特图 | ❌ | ❌ | ❌ |

---

## 9. 目录结构

```
skills/tools/progress-tracker/
├── SKILL.md                    # 核心指令（< 500 行，Frontmatter 仅含 name + description）
├── meta.json                   # 扩展元数据（版本、标签、兼容平台）
├── references/
│   └── REFERENCE.md            # 详细技术参考：数据模型、算法、门控规则、归档联动
└── assets/
    └── config-template.yaml    # 项目级 OpenSpec 配置模板（10 阶段 + Red Flags）
```

---

## 10. 约束与红线

- **唯一写入口**：禁止人工直接修改 `progress.md` 的 YAML frontmatter，所有更新必须通过本 Skill
- **自测门控**：`tasks.md` 中 `verified_by` 不为通过状态的任务，不计入 completed 统计
- **阻断优先**：任何 Red Flag 中的 `blocker` 级异常，必须修复后才能更新进度
- **归档联动**：变更完成执行 `opsx:archive` 时，自动将 `progress.md` 同步归档到 `openspec/archive/{变更名}/`
- **最小输入原则**：Skill 优先通过扫描项目文件自动推断上下文（技术栈、模块、项目名），仅在推断失败或结果不确定时才向用户询问
