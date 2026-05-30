# finish（归档收尾）设计文档

> 版本：V2.1  
> 最后更新：2026-05-12  
> 对应 Skill：`skills/sdlc/finish`  
> 对应 meta.json version：`1.0.0`

---

## 1. 设计目标

`finish` 是一个**变更归档收尾流水线**，核心目标是在人工确认上线成功后，系统化地完成分支合并、产物归档、规格同步、文档更新和最终一致性校验，确保变更的所有交付物都有迹可循、有档可查。

其设计意图包括：

- **人工最终把关**：严禁 AI 自动执行归档，必须等待人类明确的"确认归档"信号。
- **全产物归档**：除传统代码和规格外，强制纳入 UAT 报告、发布说明、人工决策记录和代码审查报告。
- **规格历史谱系**：增量规格合并到主规格时保留历史，不删除旧内容，只标记废弃。
- **一致性闭环**：通过 8 项检查清单的最终校验，防止"归档了但不完整"。
- **交付链衔接**：归档完成后自动触发周期性监控，形成完整的交付后链路。

---

## 2. 核心概念

### 2.1 术语表

| 术语 | 定义 |
|------|------|
| **归档确认单（Archive Confirmation）** | 最终输出产物，证明本次变更的所有归档动作已完成并通过校验。 |
| **增量规格合并（Spec Sync）** | 将 `changes/{变更名}/specs/` 下的文档合并到项目主规格目录的操作。 |
| **历史谱系（Lineage Preservation）** | 合并规格时不删除旧内容，而是追加新内容并标记旧内容为废弃。 |
| **7 类强制归档文档** | V2.1 规定的必须归档的文档：specs、tasks、uat-report、release-notes、human-decisions、code-review-report、分支合并报告。 |
| **人工最终信号（Human Go-Ahead）** | 用户明确输入"确认归档"或同等语义指令，AI 不得自动推断。 |
| **归档标记文件（Archive Marker）** | 若保留原始变更目录，其中放置的指向归档位置的说明文件。 |

### 2.2 归档范围（V2.1 扩展）

```
openspec/changes/archive/{变更名}/
├── specs/                      # 设计文档（增量规格）
├── tasks.md                    # 任务清单
├── uat-report.md              # UAT 报告（V2.1 强制）
├── release-notes.md           # 发布说明（V2.1 强制）
├── human-decisions.md         # 人工决策记录（V2.1 强制）
├── code-review-report.md      # 代码审查报告（V2.1 强制）
├── merge-report.md            # 分支合并报告
└── CHANGELOG-fragment.md      # 本次变更的 CHANGELOG 片段
```

---

## 3. 架构设计（IPO 模型）

### 3.1 输入（Input）

```
InputSet ::= {
  human_confirmation  : bool,           // 是否收到明确的"确认归档"信号
  change_name         : string,         // 变更名称
  source_branch       : string,         // 开发分支名
  target_branch       : string,         // 主分支名（main/master）
  artifacts           : ArtifactBundle, // 全部待归档产物
  progress_md         : string,         // progress.md 路径
  release_notes       : string,         // release-notes.md 内容
  uat_report          : string,         // uat-report.md 内容
  human_decisions     : string,         // human-decisions.md 内容
  code_review_report  : string          // code-review-report.md 内容
}

ArtifactBundle ::= {
  specs_dir           : string,
  tasks_md            : string,
  uat_report_md       : string,
  release_notes_md    : string,
  human_decisions_md  : string,
  code_review_report_md : string,
  source_code         : string          // 代码库路径
}
```

### 3.2 处理（Process）

处理架构采用**顺序流水线 + 人工闸门类比模型**：

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              finish 归档流水线                                │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
              ┌───────────────────────┼───────────────────────┐
              ▼                       ▼                       ▼
    ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
    │ Step 0: 人工闸口 │     │ Step 1-3: 合并   │     │ Step 4-5: 归档   │
    │ Human Gate      │     │ & Cleanup       │     │ & Sync          │
    └────────┬────────┘     └────────┬────────┘     └────────┬────────┘
             │                       │                       │
             ▼                       ▼                       ▼
    ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
    │ - 等待确认信号   │     │ - 分支合并      │     │ - 复制到 archive│
    │ - 严禁自动通过   │     │ - 临时文件清理   │     │ - 增量规格合并   │
    │ - 确认 release  │     │ - 合并报告生成   │     │ - 历史谱系保留   │
    │   已完成        │     │ - 分支删除      │     │                 │
    └─────────────────┘     └─────────────────┘     └─────────────────┘
                                      │
              ┌───────────────────────┼───────────────────────┐
              ▼                       ▼                       ▼
    ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
    │ Step 6: 纳入交付 │     │ Step 7: CHANGELOG│     │ Step 8: 最终校验 │
    │ 后文档           │     │ 生成            │     │ Self-Check      │
    └────────┬────────┘     └────────┬────────┘     └────────┬────────┘
             │                       │                       │
             ▼                       ▼                       ▼
    ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
    │ - uat-report    │     │ - 按版本分组    │     │ - 8 项检查清单   │
    │ - release-notes │     │ - 遵循 Keep a   │     │ - 任一失败即暂停 │
    │ - human-decisions│    │   Changelog     │     │ - 输出确认单    │
    │ - code-review   │     │ - 追加到根目录   │     │                 │
    └─────────────────┘     └─────────────────┘     └─────────────────┘
```

**Step 0: 人工闸口（Human Gate）**
- 向用户展示确认提示，等待明确信号。
- 若用户未确认或拒绝，流水线中止。
- 这是整个流程中唯一的人工决策点。

**Step 1-3: 分支合并与清理**
- 切换到主分支，拉取最新代码。
- 合并开发分支（`--no-ff` 保留历史）。
- 验证合并后测试通过。
- 清理 `.kimi/temp-tests/`、`.kimi/temp-builds/` 等临时目录。
- 删除已合并的开发分支。
- 生成分支合并报告。

**Step 4-5: OpenSpec 归档与规格同步**
- 创建 `openspec/changes/archive/{变更名}/` 目录。
- 复制全部 7 类文档到归档目录。
- 将增量规格合并到项目主规格（追加模式）。
- 在合并处添加变更溯源标记。
- 旧规格标记为废弃而非删除。

**Step 6: 纳入交付后文档（V2.1）**
- 确保 UAT 报告、发布说明、人工决策记录、代码审查报告已进入归档目录。
- 这些是发布决策和合规审计的关键依据，不可遗漏。

**Step 7: CHANGELOG 生成**
- 基于 release-notes.md 生成版本化 CHANGELOG 条目。
- 遵循 Keep a Changelog 规范（Added / Fixed / Changed / Deprecated）。
- 追加到项目根目录 `CHANGELOG.md`。

**Step 8: 最终一致性校验**
- 执行 8 项检查清单（见 4.2 节）。
- 全部通过 → 生成归档完成确认单。
- 任一失败 → 暂停，输出缺失清单，等待修复后重新校验。

### 3.3 输出（Output）

```
OutputSet ::= {
  confirmation       : ArchiveConfirmation,  // 归档完成确认单
  archive_path       : string,              // 归档目录路径
  changelog_updated  : bool,                // CHANGELOG 是否更新
  merge_commit_sha   : string,              // 合并提交 SHA
  self_check_result  : SelfCheckResult,     // 一致性校验结果
  next_stage         : enum                 // MONITORING_ANALYSIS
}

ArchiveConfirmation ::= {
  change_name        : string,
  archived_at        : ISO8601,
  archive_path       : string,
  merge_result       : string,
  cleanup_result     : string,
  spec_sync_result   : string,
  documents_count    : int,                 // 应 = 7
  self_check_passed  : bool
}
```

---

## 4. 状态机与数据模型

### 4.1 归档生命周期状态机

```
                              ┌─────────────┐
                    ┌────────>│   IDLE      │<────────┐
                    │         │ (等待触发)   │         │
                    │         └──────┬──────┘         │
                    │                │ 用户说"归档"    │
                    │                ▼                │
                    │         ┌─────────────┐         │
                    │         │WAITING_HUMAN│         │
                    │         │ (等待确认)   │         │
                    │         └──────┬──────┘         │
                    │                │                │
          ┌─────────┼────────┐       │       ┌───────┼─────────┐
          ▼         ▼        ▼       ▼       ▼       ▼         ▼
    ┌────────┐ ┌────────┐ ┌────────┐   ┌────────┐ ┌────────┐ ┌────────┐
    │MERGING │ │ARCHIVING      │ │SYNCING │   │CHECKING│ │COMPLETE│ │ABORTED │
    │        │ │        │ │        │   │        │ │        │ │        │
    └───┬────┘ └───┬────┘ └───┬────┘   └───┬────┘ └───┬────┘ └────────┘
        │          │          │            │          │
        └──────────┴──────────┴────────────┘          │
                          │                           │
                          ▼                           ▼
                   [流水线执行中]               [进入 monitoring]
```

状态说明：
- **IDLE**：等待触发。
- **WAITING_HUMAN**：已收到归档请求，等待用户确认"确认归档"。
- **MERGING**：执行分支合并与清理。
- **ARCHIVING**：复制产物到 archive 目录。
- **SYNCING**：增量规格合并到主规格。
- **CHECKING**：执行最终一致性校验。
- **COMPLETE**：全部通过，输出确认单，进入 monitoring-analysis。
- **ABORTED**：用户取消或校验失败未修复。

### 4.2 最终一致性校验清单（Self-Check Archive Edition）

| 序号 | 检查项 | 通过标准 | 失败处理 |
|------|--------|----------|----------|
| 1 | 归档目录完整性 | `archive/{变更名}/` 存在且包含全部 7 类文档 | 暂停，补全缺失文档 |
| 2 | specs 与主规格同步 | 主规格目录已合并增量内容 | 暂停，重新执行 /opsx:sync |
| 3 | CHANGELOG 已更新 | 根目录 `CHANGELOG.md` 包含本次变更条目 | 暂停，重新生成 CHANGELOG |
| 4 | uat-report 归档 | archive/ 包含 `uat-report.md` | 暂停，复制 UAT 报告 |
| 5 | release-notes 归档 | archive/ 包含 `release-notes.md` | 暂停，复制发布说明 |
| 6 | human-decisions 归档 | archive/ 包含 `human-decisions.md` | 暂停，复制决策记录 |
| 7 | code-review-report 归档 | archive/ 包含 `code-review-report.md` | 暂停，复制审查报告 |
| 8 | 分支已合并 | main/master 包含本次合并提交 | 暂停，检查合并状态 |

---

## 5. 集成方案

### 5.1 与 release-management 的衔接

```
[release-management] ---(人工确认上线)---> [finish]
                                              │
                                              ▼
                                    ┌─────────────────────┐
                                    │ 输入清单：            │
                                    │ - 上线确认信号        │
                                    │ - release-notes.md    │
                                    │ - uat-report.md       │
                                    └─────────────────────┘
```

**关键协议**：
- `release-management` 完成后，由人类（而非 AI）判断是否可以归档。
- `finish` 不检查 `release-management` 的具体内容，只确认其阶段状态为"已完成"。
- 若 `release-management` 未标记完成，`finish` 拒绝启动。

### 5.2 与 self-check 的衔接

Step 8 的最终一致性校验本质上是一次特殊的 `self-check`：

```
[finish] ---(调用 self-check)---> [归档级校验]
                                       │
                                       ▼
                              ┌────────────────┐
                              │ 检查项：归档完整性  │
                              │ 检查项：规格同步    │
                              │ 检查项：CHANGELOG   │
                              └────────────────┘
```

- `self-check` 使用归档专用检查项，而非通用阶段检查项。
- 校验结果写入确认单，不作为独立报告输出。

### 5.3 与 progress-tracker 的衔接

```
[finish] ---(阶段 11 完成)---> [progress-tracker]
                                    │
                                    ▼
                           ┌─────────────────┐
                           │ 更新 progress.md │
                           │ - finish: completed │
                           │ - overall_progress  │
                           └─────────────────┘
```

### 5.4 与 monitoring-analysis 的衔接

```
[finish] ---(归档完成)---> [monitoring-analysis]
                                 │
                                 ▼
                        ┌─────────────────┐
                        │ 启动周期性监控   │
                        │ 产出 feedback-loop.md │
                        │ 输入到下一变更的 brainstorming │
                        └─────────────────┘
```

---

## 6. 安全与约束

### 6.1 绝对约束

| 约束 | 说明 | 违反后果 |
|------|------|----------|
| 严禁自动归档 | AI 不得在没有明确人工信号的情况下执行 Step 1+ | 视为严重违规，立即停止 |
| 7 类文档强制归档 | 缺任何一类，一致性校验必须失败 | 归档视为不完整 |
| 追加非覆盖 | 规格合并时必须保留历史 | 历史谱系断裂 |
| 临时文件清理 | 必须清理 `.kimi/temp-*` 目录 | 工作区污染 |

### 6.2 审计追踪

- 归档完成确认单必须包含时间戳、合并提交 SHA、文档清单。
- 建议将确认单保存到 `.kimi/audit/archive-{变更名}-{日期}.md`。
- `CHANGELOG.md` 的每次追加都是不可篡改的历史记录。

---

## 7. 后期演进方向

### 7.1 短期（V2.2）

- **归档模板自定义**：支持项目级 `.archive-policy.yaml`，自定义归档目录结构和额外文档类型。
- **自动标签生成**：基于变更内容自动生成 Git Tag 和 GitHub Release Draft。
- **归档压缩**：对历史归档目录自动压缩为 `.tar.gz`，减少存储占用。

### 7.2 中期（V3.0）

- **跨变更依赖分析**：归档前检查本次变更是否与其他未完成变更有代码冲突或规格冲突。
- **智能规格合并**：AI 辅助解决增量规格与主规格的章节冲突，减少人工介入。
- **归档检索**：建立归档目录的全文索引，支持按关键词、时间、变更名快速检索历史交付物。

### 7.3 长期（V4.0）

- **变更影响图谱**：基于历史归档数据，生成模块-变更-缺陷的关联图谱，预测高风险模块。
- **自动回滚触发**：当 monitoring-analysis 发现线上异常与某变更强相关时，自动定位归档中的回滚方案。
- **合规审计自动化**：根据行业合规要求（如 ISO、等保），自动生成审计所需的变更追踪报告。

---

## 附录：版本变更日志

| 版本 | 日期 | 变更内容 |
|------|------|----------|
| V1.0 | — | Superpowers 原生 `finishing-a-development-branch`，专注分支合并与工作区清理。 |
| V2.0 | — | 引入 OpenSpec /opsx:archive 能力，增加规格归档与同步。 |
| V2.1 | 2026-05 | 重命名为 `finish`；强制人工确认信号；归档范围扩展至 7 类文档（新增 uat-report、release-notes、human-decisions、code-review-report）；增加最终一致性校验（8 项清单）；增加 CHANGELOG 生成；与 monitoring-analysis 正式衔接。 |
