---
name: finish
description: 当 release-management 完成且用户确认上线后触发，或用户提到'归档'、'收尾'、'变更完成'、'结束开发'、'合并分支并归档'时触发。执行分支合并、临时文件清理、OpenSpec 归档、CHANGELOG 生成和最终一致性校验。
---

# Finish（归档收尾）

变更完成时的归档收尾 Skill。整合 Superpowers 分支合并能力与 OpenSpec 归档规范，确保变更产物完整归档、规格同步、历史可追溯。

**Core principle:** 人工确认 → 合并清理 → 规格归档 → 一致性校验 → 输出确认单。

**Announce at start:** "I'm using the finish skill to archive this change."

## 适用场景

- release-management 完成后，人工确认上线成功
- 用户明确说"归档本次变更"、"收尾"、"结束开发"
- 需要将开发分支合并回主分支并清理工作区
- 需要生成 CHANGELOG 并归档 OpenSpec 变更目录

## 关键前置条件

**严禁在以下条件未满足时执行：**
- ❌ 未收到人工明确确认上线成功的信号
- ❌ release-management 阶段未标记为"已完成"
- ❌ 存在未修复的阻塞性代码审查问题

## 输入清单

执行前必须确认以下文件存在且可读：

| 文件 | 路径 | 用途 |
|------|------|------|
| tasks.md | `openspec/changes/{变更名}/tasks.md` | 任务完成确认 |
| 代码库 | 项目源码目录 | 分支合并 |
| uat-report.md | `openspec/changes/{变更名}/uat/uat-report.md` | 归档 |
| release-notes.md | `openspec/changes/{变更名}/release-notes.md` | 归档 + CHANGELOG |
| human-decisions.md | `openspec/changes/{变更名}/human-decisions.md` | 归档 |
| 需求与设计文档 | `openspec/changes/{变更名}/high-level-requirements/`、`detailed-requirements/`、`high-level-design/`、`detailed-design/` | 增量规格合并 |
| code-review 目录 | `openspec/changes/{变更名}/code-review/` | 最终一致性校验 |
| code-review/review-request.yaml | `openspec/changes/{变更名}/code-review/review-request.yaml` | 审查请求书归档 |
| code-review/review-report.yaml | `openspec/changes/{变更名}/code-review/review-report.yaml` | 审查意见书归档 |
| code-review/fix-plan.yaml | `openspec/changes/{变更名}/code-review/fix-plan.yaml` | 修复计划归档 |

## 执行流程

### Step 0: 人工最终确认（MANDATORY）

```text
【归档收尾 | Skill：finish】

release-management 已完成。请确认：
1. 变更已实际上线成功？
2. 可以执行归档收尾？

请输入 "确认归档" 继续。
```

**必须等待用户输入"确认归档"或同等明确信号。**
**严禁 AI 自动执行此步骤。**

### Step 1: 分支合并与清理（Superpowers 能力）

```bash
# 1.1 确认当前分支
CURRENT_BRANCH=$(git branch --show-current)
BASE_BRANCH=$(git merge-base HEAD main 2>/dev/null || echo "main")

# 1.2 合并到主分支
git checkout ${BASE_BRANCH}
git pull origin ${BASE_BRANCH}
git merge ${CURRENT_BRANCH} --no-ff -m "chore(finish): merge change {变更名}"

# 1.3 验证合并后测试
git push origin ${BASE_BRANCH}

# 1.4 清理临时文件
rm -rf .kimi/temp-tests/
rm -rf .kimi/temp-builds/
find . -name "*.tmp" -delete 2>/dev/null

# 1.5 删除已合并的开发分支
git branch -d ${CURRENT_BRANCH}
```

**生成分支合并报告**：
```markdown
## 分支合并报告：{变更名}

- **合并分支**：{CURRENT_BRANCH} → {BASE_BRANCH}
- **合并提交**：{MERGE_COMMIT_SHA}
- **临时文件清理**：已完成
- **开发分支删除**：已完成
```

### Step 2: OpenSpec 归档（/opsx:archive）

```bash
# 2.1 创建归档目录
mkdir -p openspec/changes/archive/{变更名}/

# 2.2 复制变更全部产物
cp -r openspec/changes/{变更名}/* openspec/changes/archive/{变更名}/

# 2.3 保留原始目录的归档标记（可选，取决于团队规范）
# 某些团队选择保留原目录作为"当前变更"，仅复制到 archive/
# 另一些团队移动后在原位置放置 archive-marker.md
```

**归档范围（V2.1 扩展）**：
- ✅ high-level-requirements/、detailed-requirements/、high-level-design/、detailed-design/ 目录（全部需求与设计文档）
- ✅ tasks.md（任务清单）
- ✅ uat-report.md（UAT 报告）
- ✅ release-notes.md（发布说明）
- ✅ human-decisions.md（人工决策记录）
- ✅ code-review/ 目录（审查请求书、意见书、修复计划、决策日志）
- ✅ 分支合并报告
- ✅ CHANGELOG.md（生成后纳入）

### Step 3: 增量规格合并（/opsx:sync）

将本次变更的增量规格合并到项目主规格：

1. 读取 `openspec/changes/{变更名}/high-level-requirements/`、`detailed-requirements/`、`high-level-design/`、`detailed-design/` 下的所有规格文件
2. 对比项目主规格目录（如 `docs/specs/` 或 `openspec/specs/`）
3. 合并新增或修改的规格章节
4. 在合并位置添加变更溯源标记：
   ```markdown
   > 更新时间：{ISO8601} | 来源变更：{变更名} | 合并人：AI
   ```
5. 保留历史谱系：主规格中不删除旧内容，仅追加或标记废弃

### Step 4: 纳入交付后文档（V2.1 新增）

确保以下文档已复制到归档目录：

```bash
# UAT 报告
cp openspec/changes/{变更名}/uat-report.md openspec/changes/archive/{变更名}/

# 发布说明
cp openspec/changes/{变更名}/release-notes.md openspec/changes/archive/{变更名}/

# 人工决策记录
cp openspec/changes/{变更名}/human-decisions.md openspec/changes/archive/{变更名}/

# 代码审查产物
cp -r openspec/changes/{变更名}/code-review openspec/changes/archive/{变更名}/
```

### Step 5: 生成 CHANGELOG.md

基于 release-notes.md 和本次变更信息，生成或追加 CHANGELOG：

```markdown
## [{版本号}] - {日期}

### 变更概要
{变更名}: {一句话描述}

### 新增
- {来自 release-notes.md}

### 修复
- {来自 release-notes.md}

### 变更
- {来自 release-notes.md}

### 归档位置
`openspec/changes/archive/{变更名}/`

### 关联决策
参见 `human-decisions.md` 中 Gate 1/2.5/2/3 签字记录。
```

追加到项目根目录 `CHANGELOG.md`（若不存在则创建）。

### Step 6: 最终一致性校验（Self-Check 归档版）

调用 `self-check` Skill 执行归档级自查：

| 检查项 | 标准 | 结果 |
|--------|------|------|
| 归档目录完整性 | archive/{变更名}/ 包含全部 8 类文档 | 是 / 否 |
| 需求/设计文档与主规格同步 | 主规格已合并增量内容 | 是 / 否 |
| CHANGELOG 已更新 | 根目录 CHANGELOG.md 包含本次变更 | 是 / 否 |
| uat-report 归档 | archive/ 包含 uat-report.md | 是 / 否 |
| release-notes 归档 | archive/ 包含 release-notes.md | 是 / 否 |
| human-decisions 归档 | archive/ 包含 human-decisions.md | 是 / 否 |
| 代码审查产物归档 | archive/ 包含 code-review/ 目录 | 是 / 否 |
| 分支已合并 | main/master 包含合并提交 | 是 / 否 |

**任一检查项为"否" → 暂停归档，报告缺失项，等待修复后重新校验。**

### Step 7: 更新 progress-tracker

```yaml
# 更新 openspec/changes/{变更名}/progress.md
phases:
  finish: {status: completed, completed_at: {ISO8601}}
overall_progress: 100%  # 或按实际规则计算
```

通知 `progress-tracker` 阶段 11（finish）已完成。

### Step 8: 输出归档完成确认单

```markdown
# 归档完成确认单

| 项目 | 状态 |
|------|------|
| 变更名称 | {变更名} |
| 归档时间 | {ISO8601} |
| 归档路径 | `openspec/changes/archive/{变更名}/` |
| 分支合并 | ✅ {CURRENT_BRANCH} → {BASE_BRANCH} @ {MERGE_COMMIT_SHA} |
| 临时文件清理 | ✅ 已完成 |
| 规格归档 | ✅ 8 类文档已归档 |
| 主规格同步 | ✅ 增量已合并 |
| CHANGELOG | ✅ 已更新 |
| 一致性校验 | ✅ 全部通过 |

## 归档清单

- [x] high-level-requirements/、detailed-requirements/、high-level-design/、detailed-design/（全部需求与设计文档）
- [x] tasks.md
- [x] uat-report.md
- [x] release-notes.md
- [x] human-decisions.md
- [x] code-review-report.md
- [x] 分支合并报告
- [x] CHANGELOG.md（追加）

## 下一步

归档完成。进入阶段 12：周期性监控（`monitoring-analysis`）。
```

## 与上下游衔接

```
release-management 完成（人工确认上线后）
    └── 自动触发 finish
         ├── 1. 分支合并 + 清理
         ├── 2. OpenSpec 归档
         ├── 3. 增量规格合并
         ├── 4. 纳入交付后文档
         ├── 5. 生成 CHANGELOG
         ├── 6. 最终一致性校验（self-check）
         ├── 7. 更新 progress-tracker
         └── 8. 输出归档完成确认单
              └── 进入 monitoring-analysis 周期性监控
```

| 衔接点 | 动作 |
|--------|------|
| 上游: release-management | 必须人工确认上线成功后方可触发 |
| 上游: progress-tracker | 阶段 11 开始时读取进度状态 |
| 横向: self-check | Step 6 调用，执行归档一致性校验 |
| 横向: git-automation | Step 1 分支合并时可调用辅助 |
| 下游: monitoring-analysis | 归档完成后进入周期性监控 |
| 下游: brainstorming | monitoring-analysis 产出的 feedback-loop.md 输入到下一变更 |

## Red Flags

**Never:**
- AI 自动执行归档（必须人工确认）
- 未实际上线就归档
- 遗漏 uat-report.md / release-notes.md / human-decisions.md / code-review/ 目录
- 不执行最终一致性校验就直接宣告完成
- 删除原始变更目录而不保留 archive/ 副本
- 合并分支前不确认 release-management 完成

**Always:**
- 等待明确的"确认归档"信号
- 归档全部 8 类文档（含 code-review/ 目录）
- 执行 self-check 归档版校验
- 更新 CHANGELOG.md
- 同步更新 progress-tracker
- 保留历史谱系（主规格不删除旧内容）

## Gotchas

- **严禁 AI 自动归档**：必须等用户明确输入"确认归档"或同等信号。即使 release-management 已完成，AI 也不得主动执行 Step 1 及以后。
- **归档范围扩大（V2.1）**：除原有规格和代码外，必须纳入 UAT 报告、发布说明、人工决策记录、代码审查报告。遗漏任何一项，一致性校验必须失败。
- **原始目录 vs 归档目录**：归档后，原始 `openspec/changes/{变更名}/` 可保留为"当前变更"标记，或替换为 `archive-marker.md` 指向归档位置。禁止直接删除导致链接失效。
- **主规格合并策略**：采用追加而非覆盖，保留历史谱系。若新规格与旧规格矛盾，标记旧规格为"已废弃"并说明替代变更名。
- **CHANGELOG 格式**：遵循 [Keep a Changelog](https://keepachangelog.com/) 规范，按版本号分组，包含变更概要、新增、修复、变更、归档位置、关联决策。
- **一致性校验是最后防线**：即使前面步骤都已完成，Step 6 发现缺失仍必须暂停并修复。禁止"差不多就行"。
- **与 monitoring-analysis 的衔接**：归档完成后，周期性监控启动。监控产出的 `feedback-loop.md` 应保存到 `openspec/feedback/` 目录，作为下一变更 `brainstorming` 的输入。
