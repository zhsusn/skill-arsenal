# Code Review 在 SDLC 中的定位与上下游完整性分析

> 基于 skill-arsenal 现有 12 阶段 OpenSpec 体系，分析新版 code review skills 的插入位置、依赖缺口与修复建议。

---

## 一、现有 SDLC 阶段体系（progress-tracker V2.1）

| 序号 | SDLC 阶段 | 阶段 ID | 阶段名称 | 权重 | 进度粒度 | 前置依赖 | 人工闸门 |
|------|-----------|---------|----------|------|----------|----------|----------|
| 7 | 7 | implementation | 编码实现 | 12% | 任务级精粒度 | 序号 5~6 完成 | — |
| 8 | 8 | unit-test | 单元测试 | 8% | 任务级精粒度 | 序号 7 对应任务完成 | — |
| 9 | 9 | integration-test | 集成测试 | 4% | 任务级精粒度 | 序号 8 覆盖率门控通过 | — |
| 9.5 | 9.5 | uat-verification | UAT 验证 | 4% | 粗粒度 | 序号 9 完成 | 🚪 Gate 3 |
| 10 | 10 | release-management | 上线发布 | 4% | 粗粒度 | 序号 9.5 Gate 3 通过 | 人工最终决策 |
| 11 | 11 | finish | 收尾归档 | 0% | 粗粒度 | 序号 10 完成 | — |
| 12 | 12 | monitoring-analysis | 线上监控（周期性） | 0% | 粗粒度 | 序号 11 完成 | — |

**关键发现：现有 12 阶段体系中没有 code review 的独立位置。**

---

## 二、Code Review 在当前体系中的实际位置

### 2.1 旧版 requesting-code-review (V1.2) 的定位

旧版 `requesting-code-review` 自称 `stage-10`，但 `progress-tracker` 中 `stage-10` 是 `release-management`。这是一个**阶段编号冲突**。

旧版上下游定义：
- 上游：`executing-plans`（编码完成后触发）
- 上游：`uat-verification`（消费 uat-report.md 进行交叉验证）
- 下游：`release-management`（code-review-report.md 作为发布清单前置输入）
- 下游：`executing-plans`（不通过时生成 rework-tasks.md 返回修复）

旧版设计意图：**Gate 3（UAT）签字后，代码审查是发布前的最后质量门**（V2.1 新增）。

### 2.2 新版 code-review skills 的定位

新版技能族包含：
- `code-review-pipeline`（L1 编排器，状态机驱动）
- `requesting-code-review`（L2 提审者）
- `code-reviewer`（L2 审查者）
- `receiving-code-review`（L2 被审者）

新版设计意图：代码审查是一个**横向贯穿的质量门禁流程**，而非单一阶段。

**建议的触发时机（三级审查）：**

| 级别 | 触发时机 | 调用 Skill | 范围 | 产出 |
|------|---------|-----------|------|------|
| L0 内联审查 | executing-plans 每个 Batch 完成后 | `code-reviewer`（轻量模式） | 本 Batch 变更文件 | 简要 issues 列表 |
| L1 变更审查 | integration-test 全部通过后 | `code-review-pipeline`（完整流程） | 本次变更全部 diff | review-request.yaml + review-report.yaml + fix-plan.yaml |
| L2 专项审查 | 用户明确要求或涉及敏感模块 | `code-reviewer`（单轴深度模式） | 指定文件/轴 | 专项审查报告 |

---

## 三、上下游依赖完整性诊断

### 3.1 依赖关系全景图

```
implementation (阶段 7)
    ├── Batch N 编码完成
    │       └── L0 内联审查 (code-reviewer 轻量) ──→ 本 Batch 修复
    │
    └── 全部任务完成
            │
            ▼
    unit-test (阶段 8) ──→ 覆盖率 ≥70%
            │
            ▼
    integration-test (阶段 9) ──→ P0 用例通过
            │
            ▼
    ┌─────────────────────────────────────────┐
    │           [缺口 1] 代码审查阶段缺失        │
    │                                          │
    │   L1 变更审查 (code-review-pipeline)      │
    │   ├── review-request.yaml                 │
    │   ├── review-report.yaml                  │
    │   ├── fix-plan.yaml                       │
    │   └── docs/decisions.md                   │
    │                                          │
    └─────────────────────────────────────────┘
            │
            ▼
    uat-verification (阶段 9.5) ──→ Gate 3 签字
            │
            ▼
    release-management (阶段 10)
            │
            ▼
    finish (阶段 11) ──→ 归档
```

### 3.2 发现的 6 个缺口

#### 缺口 1：progress-tracker 中没有 code review 阶段

**严重性：🔴 高**

**表现：**
- `progress-tracker` 的 12 阶段表中没有 code review 的独立序号、权重和阶段 ID
- 无法追踪代码审查进度（REVIEWING / RECEIVING / VERIFYING 等子状态）
- 无法计算 code review 对总体进度的贡献
- 旧版 `requesting-code-review` 错误地自标记为 `stage-10`，与 `release-management` 冲突

**影响：**
- 代码审查在项目中"隐形"，管理者无法从 progress.md 看到审查状态
- 审查阻塞时无法被进度追踪系统识别为风险
- finish 的归档清单中 code-review 相关文件缺乏阶段归属

**修复建议：**
方案 A（推荐）：将 code review 设计为**阶段间横向门禁**，不占用独立阶段序号，但在 progress.md 中增加 `code_review_status` 字段：
```yaml
phases:
  implementation: {status: completed, weight: 12%}
  unit-test: {status: completed, weight: 8%}
  integration-test: {status: completed, weight: 4%}
  code_review: {status: completed, gate: passed}  # 新增横向门禁
  uat-verification: {status: not_started, weight: 4%}
```

方案 B：在 integration-test (9) 和 uat-verification (9.5) 之间插入新阶段 `code-review`（序号 9.25），权重 2%：
```yaml
| 9.25 | 9.25 | code-review | 代码审查 | 2% | 粗粒度 | 序号 9 完成 | — |
```

---

#### 缺口 2：executing-plans 下游指向错误阶段

**严重性：🟠 中**

**表现：**
`executing-plans/SKILL.md` 第 172 行：
> "若用户明确要求或处于项目交付流程中，自动触发 `requesting-code-review`（阶段 10）"

但阶段 10 是 `release-management`。此处"阶段 10"引用是错误的。

**影响：**
- 开发者可能被误导认为 code review 在发布阶段才执行
- 实际上 code review 应在集成测试之后、UAT 之前执行

**修复建议：**
修改 `executing-plans/SKILL.md`：
```markdown
| 下游: integration-test | 全部任务完成后，进入端到端集成测试阶段 |
| 下游: code-review-pipeline | integration-test 通过后触发变更级代码审查 |
| 下游: finish | 最终交接收尾 Skill（阶段 11，经 release-management 后） |
```

同时删除"阶段 10"的表述，改为：
> "若用户明确要求或处于项目交付流程中，自动触发 `code-review-pipeline`（变更级审查）"

---

#### 缺口 3：integration-test 缺少 code review 下游衔接

**严重性：🟠 中**

**表现：**
`integration-test/SKILL.md` 的上下游衔接表中，只有上游 `unit-test`，下游 `uat-verification`，缺少 `code-review`。

**影响：**
- 集成测试通过后，不会自动触发代码审查流程
- 需要用户手动触发，增加遗漏风险

**修复建议：**
在 `integration-test/SKILL.md` 的"与上下游衔接"中增加：
```markdown
| 下游: code-review-pipeline | P0 用例全部通过后，触发变更级代码审查 |
```

---

#### 缺口 4：uat-verification 与 code review 的时序模糊

**严重性：🟠 中**

**表现：**
- 旧版 `requesting-code-review` 将 `uat-verification` 列为**上游**
- 但 `release-management` 要求 `code-review-report.md` 和 `uat-report.md` **同时**作为前置
- 新版 `code-review-pipeline` 的状态机中，没有与 UAT 的交互定义

**影响：**
- 用户不清楚应该先 UAT 还是先 code review
- 如果先 UAT 后 code review，UAT 发现的业务问题可能需要返工，导致 code review 重复执行
- 如果先 code review 后 UAT，代码审查可以预先捕获实现缺陷，减少 UAT 返工

**修复建议：**
明确时序：**code review 在 integration-test 之后、uat-verification 之前**。

理由：
1. code review 发现的技术问题（安全、性能、架构）应在 UAT 前修复
2. UAT 应基于已通过代码审查的代码进行，避免 UAT 发现的问题实际上是已知的 code review 问题
3. `release-management` 需要两份报告同时作为前置，说明它们是串行而非并行的前置

更新 `uat-verification/SKILL.md`：
```markdown
| 上游: code-review-pipeline | 确认代码审查已通过（blocking 问题清零） |
```

更新 `requesting-code-review/SKILL.md`（新版）中删除 `uat-verification` 作为上游的描述。

---

#### 缺口 5：release-management 前置依赖与新产物路径不匹配

**严重性：🟡 低-中**

**表现：**
`release-management` 要求：
> "代码审查报告 | `openspec/changes/{变更名}/code-review-report.md` | 结论为通过或有条件通过"

但新版 code review 产物是：
- `review-request.yaml`
- `review-report.yaml`
- `fix-plan.yaml`
- `docs/progress.md`（审查看板）
- `docs/decisions.md`（决策日志）

旧版的 `code-review-report.md`（Markdown 格式）与新版的 `review-report.yaml`（YAML 格式）不兼容。

**影响：**
- `release-management` 无法读取新版产物
- 归档时产物路径不一致

**修复建议：**
方案 A（推荐）：统一产物路径和格式
```
openspec/changes/{变更名}/
└── code-review/
    ├── review-request.yaml      # 审查请求书
    ├── review-report.yaml       # 审查意见书（替代旧版 code-review-report.md）
    ├── fix-plan.yaml            # 修复计划
    └── decisions.md             # 审查决策日志（可并入 human-decisions.md）
```

同时修改 `release-management/SKILL.md`：
```markdown
| 代码审查报告 | `openspec/changes/{变更名}/code-review/review-report.yaml` | overall 为 Approve 或 Comment；blocking 问题已清零 |
```

方案 B：保留旧版 `code-review-report.md` 作为对外报告
在 `code-review-pipeline` 的 SUMMARY 阶段，除了输出 YAML，额外生成 `code-review-report.md`（Markdown 格式）供 `release-management` 和人工阅读。

---

#### 缺口 6：finish 归档清单与新产物不匹配

**严重性：🟡 低**

**表现：**
`finish/SKILL.md` 的归档清单包含 `code-review-report.md`，但未包含：
- `review-request.yaml`
- `review-report.yaml`
- `fix-plan.yaml`
- `docs/decisions.md`（审查决策）
- `docs/progress.md`（审查看板）

**影响：**
- 归档不完整，审查历史可能丢失

**修复建议：**
更新 `finish/SKILL.md` 的归档范围：
```markdown
- ✅ code-review/review-request.yaml（审查请求书）
- ✅ code-review/review-report.yaml（审查意见书）
- ✅ code-review/fix-plan.yaml（修复计划）
- ✅ code-review/decisions.md（审查决策日志）
```

---

## 四、Code Review 与横向 Skill 的关系

### 4.1 与 self-check 的关系

| 维度 | self-check | code-reviewer |
|------|-----------|---------------|
| **执行时机** | 每个任务编码完成后 | Batch 完成后 / 变更完成后 |
| **执行者视角** | 实现者自检 | 独立第三方审查 |
| **深度** | 快速：一致性、完整性、接口契约 | 深度：四阶段 × 五轴 |
| **关系** | **互补，不替代** | **互补，不替代** |

**结论：** executing-plans 中的 self-check 应保留，code review 在其之后执行。

### 4.2 与 progress-tracker 的关系

建议增加 code review 状态回写接口：
```yaml
# progress.md 中新增 code_review 字段
phases:
  code_review:
    status: reviewing      # not_started / reviewing / fixing / verifying / passed / failed
    started_at: "2026-05-26T10:00:00+08:00"
    completed_at: null
    overall: "Request Changes"   # Approve / Comment / Request Changes
    blocking_count: 2
    important_count: 1
    current_state: "RECEIVING"   # pipeline 子状态
```

### 4.3 与 human gate 的关系

建议方案：**code review 不增加独立人工闸门**，但将其作为 Gate 3（UAT）的**前置技术门禁**。

理由：
- 避免过多人工闸门降低效率
- code review 由 AI 执行，人工仅在 blocking 问题争议时介入
- UAT 签字人（Gate 3）应能看到 code review 结论作为参考

---

## 五、修复建议汇总

### 5.1 必须修复（P0）

| 文件 | 修改内容 |
|------|---------|
| `skills/sdlc/progress-tracker/SKILL.md` | 阶段定义表中增加 `code-review` 作为横向门禁或独立阶段（9.25）；更新进度计算规则 |
| `skills/sdlc/executing-plans/SKILL.md` | 删除"阶段 10"的表述；下游增加 `code-review-pipeline` |
| `skills/sdlc/integration-test/SKILL.md` | 下游衔接增加 `code-review-pipeline` |
| `skills/sdlc/uat-verification/SKILL.md` | 上游衔接增加 `code-review-pipeline`；前置依赖增加"代码审查通过" |
| `skills/sdlc/release-management/SKILL.md` | 修改 code-review 产物路径为 `code-review/review-report.yaml` |
| `skills/sdlc/finish/SKILL.md` | 归档清单增加 `code-review/` 目录下的 4 个新产物 |
| `skills/sdlc/requesting-code-review/meta.json` | 删除 "stage-10" 标签，改为 "stage-9.25" 或不标注阶段 |

### 5.2 建议修复（P1）

| 文件 | 修改内容 |
|------|---------|
| `skills/sdlc/code-review-pipeline/SKILL.md` | 增加与 progress-tracker 的状态回写接口定义 |
| `skills/sdlc/code-review-pipeline/SKILL.md` | 产物输出路径统一为 `openspec/changes/{变更名}/code-review/` |
| `skills/sdlc/code-reviewer/SKILL.md` | 增加轻量模式（L0 内联审查）的触发条件和简化输出格式 |

### 5.3 可选增强（P2）

| 文件 | 修改内容 |
|------|---------|
| `skills/sdlc/human/SKILL.md` | 增加 code review 争议仲裁的决策模板 |
| `openspec/config.yaml`（模板）| 增加 code-review 阶段的 required_sections 定义 |

---

## 六、修正后的完整依赖链

```
implementation (阶段 7)
    ├── Batch N
    │   ├── TDD 内循环 (test-driven-development)
    │   ├── self-check (任务级自查)
    │   └── L0 内联审查 (code-reviewer 轻量) ──→ 本 Batch 修复
    │
    └── 全部任务完成 ──→ progress-tracker 更新 implementation 为 completed
            │
            ▼
    unit-test (阶段 8) ──→ 覆盖率 ≥70% ──→ progress-tracker 更新
            │
            ▼
    integration-test (阶段 9) ──→ P0 用例通过 ──→ progress-tracker 更新
            │
            ▼
    code-review-pipeline (横向门禁 / 阶段 9.25)
            ├── requesting-code-review ──→ review-request.yaml
            ├── code-reviewer ──→ review-report.yaml
            ├── receiving-code-review ──→ fix-plan.yaml
            ├── FIXING ──→ 修复执行
            ├── VERIFYING ──→ 复查通过
            └── DONE ──→ docs/decisions.md + progress-tracker 更新
            │
            ▼
    uat-verification (阶段 9.5) ──→ Gate 3 签字 ──→ progress-tracker 更新
            │
            ▼
    release-management (阶段 10)
            ├── 读取 code-review/review-report.yaml（blocking 清零）
            ├── 读取 uat-report.md（Gate 3 通过）
            ├── 生成 release-checklist.md
            └── 生成 release-notes.md
            │
            ▼
    finish (阶段 11)
            ├── 分支合并
            ├── OpenSpec 归档（含 code-review/ 目录）
            ├── 生成 CHANGELOG
            └── 一致性校验
            │
            ▼
    monitoring-analysis (阶段 12)
```

---

## 七、结论

1. **Code Review 必须插入 integration-test 与 uat-verification 之间**，作为技术质量门禁，而非与 release-management 并行。

2. **现有体系存在 6 个明确缺口**，其中阶段编号冲突和阶段缺失是最严重的问题，会导致进度追踪失效和流程断裂。

3. **建议采用"横向门禁"模式**：code review 不占用独立阶段权重，但作为一个强制性质量门控存在于 integration-test 和 uat-verification 之间，其状态写入 progress.md。

4. **产物路径需要统一**：将所有 code review 产物收敛到 `openspec/changes/{变更名}/code-review/` 目录，便于 release-management 消费和 finish 归档。

5. **self-check 与 code review 互补**：executing-plans 中的任务级 self-check 保留，变更级 code review 在 integration-test 后执行，两者不替代。
