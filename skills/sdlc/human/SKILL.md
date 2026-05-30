---
name: human
description: 当用户说'评审通过'、'确认了'、'可以发版'、'驳回'、'暂停'或需要查询人工闸门状态时触发。作为四道人工闸门的统一载体，支持语义化命名和自动推断，记录审计日志并控制阶段流转。
---

# Human Gate —— 人工决策审计层

人工决策的"审计日志 + 状态闸门"。像 Git 的 commit + status——记录快照 + 显示当前状态。

**核心原则：不替代人工做判断，只记录判断结果并控制流转。**

## 适用场景

- 概要需求产出后，人工评审完毕，说"需求评审通过"
- 详细需求产出后，人工逐页确认交互规格，说"原型确认了"
- 概要设计产出后，人工评审架构，说"设计评审通过"
- UAT 通过后，人工确认发布许可，说"可以发布了"
- 随时查询当前变更的决策状态和下一步该做什么
- 紧急情况下记录 hotfix 决策

## 核心职责

1. **决策记录**：对每次人工确认生成结构化记录，包含 Gate、时间、结论、遗留问题、决策人
2. **状态控制**：根据最新决策判断当前变更是否允许进入下一阶段
3. **自动推断**：不指定 Gate 时，根据当前进度自动推断应该确认哪个闸门
4. **历史追溯**：支持查询某个变更的全部决策链
5. **签字文件生成**：为每个 Gate 生成独立的 sign-off 文件

## 四道人工闸门

| 内部编号 | 语义化名称（推荐） | 触发时机 | 常用说法 |
|----------|-------------------|----------|----------|
| Gate 1 | `req` / `requirements` / `需求冻结` | `prd-generation` 输出 5 个 spec 后 | "需求评审通过" |
| Gate 2.5 | `proto` / `prototype` / `原型冻结` | `detailed-requirements` 输出全部模块后 | "原型确认了" |
| Gate 2 | `design` / `设计冻结` | `high-level-design` 输出架构文档后 | "设计评审通过" |
| Gate 3 | `release` / `uat` / `发布冻结` | `uat-verification` + `code-review` 通过后 | "可以发布了" |

> **别名规则**：以上所有名称等价互通。`req` = `requirements` = `需求冻结` = `Gate1`。Skill 内部统一映射为 `Gate1/2.5/2/3`。

## 决策类型

| 类型 | 含义 | 后续动作 |
|------|------|----------|
| `sign-off` | 签字通过 | 解锁下一阶段 |
| `conditional` | 有条件通过 | 解锁下一阶段，遗留问题记入 `tasks.md` |
| `reject` | 驳回重做 | 锁定当前阶段，重修上游 Skill |
| `pause` | 暂停流程 | 阻塞，等待外部资源 |
| `resume` | 恢复流程 | 解除 pause |
| `hotfix` | 紧急修复 | 已归档变更的补丁决策 |

## 使用方式（三种，按推荐度排序）

### 方式一：自然语言触发（最推荐）

直接说出你的结论，Skill 自动推断 Gate 和 action：

```bash
# Gate 1 通过
/skill:human 需求评审通过了

# Gate 2.5 有条件通过
/skill:human 原型确认了，但 loading 态还需要细化

# Gate 2 通过
/skill:human 设计评审通过

# Gate 3 驳回
/skill:human Safari 下无法保存，发布驳回

# 查询状态
/skill:human 现在状态怎么样？
/skill:human 下一步该做什么？
```

**自然语言关键词映射：**

| 用户说法 | 推断 Gate | 推断 action | 示例 |
|----------|-----------|-------------|------|
| "需求通过" / "需求确认了" / "PRD 没问题" | Gate 1 | sign-off | `需求评审通过了` |
| "原型通过" / "交互确认了" / "页面 OK" | Gate 2.5 | sign-off | `原型确认了` |
| "设计通过" / "架构确认了" / "HLD 没问题" | Gate 2 | sign-off | `设计评审通过` |
| "可以发布" / "上线" / "UAT 通过" | Gate 3 | sign-off | `可以发布了` |
| "但..." / "不过..." / "遗留问题" | 同当前 Gate | conditional | `需求通过了，但边界条件还要补充` |
| "驳回" / "重做" / "不行" | 当前待确认 Gate | reject | `设计不行，架构选错了` |
| "暂停" / "先停一下" / "阻塞" | 当前待确认 Gate | pause | `等第三方接口文档，先暂停` |
| "继续" / "恢复" / "可以走了" | 最近 paused Gate | resume | `接口文档到了，恢复` |

### 方式二：语义化命名（次推荐）

用直观的阶段名代替数字：

```bash
# 需求冻结签字
/skill:human gate=req action=sign-off

# 原型冻结有条件通过
/skill:human gate=proto action=conditional issues="P1: loading态细化"

# 设计冻结驳回
/skill:human gate=design action=reject reason="回滚方案不可操作"

# 发布冻结签字
/skill:human gate=release action=sign-off
```

**支持的 gate 别名：**

| 你想确认 | 可用写法 |
|----------|----------|
| 需求冻结（Gate 1） | `req`, `requirements`, `requirement-freeze`, `需求`, `需求冻结`, `Gate1` |
| 原型冻结（Gate 2.5） | `proto`, `prototype`, `prototype-freeze`, `原型`, `原型冻结`, `Gate2.5` |
| 设计冻结（Gate 2） | `design`, `design-freeze`, `设计`, `设计冻结`, `HLD`, `Gate2` |
| 发布冻结（Gate 3） | `release`, `release-freeze`, `uat`, `发布`, `发布冻结`, `上线`, `Gate3` |

### 方式三：自动推断（极简）

不指定 gate，让 Skill 根据当前进度自动判断：

```bash
# 自动推断当前待确认的 Gate，执行签字
/skill:human action=sign-off

# 自动推断当前 Gate，执行驳回
/skill:human action=reject reason="Safari下无法保存角色"

# 查询状态
/skill:human action=status
/skill:human action=history
```

> ⚠️ **自动推断规则**：读取 `progress-tracker` 的 `human_status`，找到第一个状态不为 `passed` 的 Gate。若所有 Gate 均已通过，提示"当前变更所有闸门已通过"。

## 参数说明

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `gate` | 否 | `auto` | 闸门标识。支持语义化别名、`auto`、或自然语言推断 |
| `action` | 是 | — | `sign-off` / `conditional` / `reject` / `pause` / `resume` / `status` / `history` |
| `issues` | 条件 | `""` | `conditional` 必填，`sign-off` 可选。遗留问题清单 |
| `reason` | 条件 | `""` | `reject` / `pause` 必填。驳回或暂停原因 |

> `result=passed` 已设为默认值，无需再写。

## 处理逻辑

### Step 1: 意图识别与 Gate 解析

**路径 A：自然语言输入**
1. 提取用户输入中的关键词
2. 按"自然语言关键词映射表"匹配 Gate 和 action
3. 若匹配到 Gate 关键词但未匹配 action，默认 `sign-off`
4. 若同时出现"通过/确认"和"但/不过/遗留"，推断为 `conditional`
5. 若未匹配到任何 Gate 关键词，进入路径 B

**路径 B：语义化命名或 `auto`**
1. 解析 `gate` 参数
2. 若 `gate=auto` 或未提供：
   - 读取 `progress-tracker` 的 `human_status`
   - 返回第一个非 `passed` 状态的 Gate
   - 若全部通过，返回提示"当前变更所有闸门已通过"
3. 若 `gate` 提供了具体值，按"gate 别名映射表"解析为内部编号

**路径 C：显式数字 Gate（兼容旧用法）**
- `Gate1` / `Gate2.5` / `Gate2` / `Gate3` 直接识别

### Step 2: 前置状态检查

1. 读取当前变更的 `human-decisions.md`
2. 检查该 Gate 的前置 Gate 是否已通过：
   - `req`（Gate 1）：无前置
   - `proto`（Gate 2.5）：要求 `req` 状态为 `passed`
   - `design`（Gate 2）：要求 `req` 状态为 `passed`（`proto` 不阻塞 `design`）
   - `release`（Gate 3）：要求 `design` 状态为 `passed`
3. 若前置 Gate 未通过，返回阻塞提示：
   ```text
   ❌ 无法确认「{当前 Gate 中文名}」：前置「{前置 Gate 中文名}」尚未签字。

   当前进度：
   ✅ 需求冻结（req）    — 已通过
   ⏳ 原型冻结（proto）  — 待确认 ← 你在这里
   ⏸️ 设计冻结（design） — 未就绪（等原型确认）
   ⏸️ 发布冻结（release）— 未就绪

   请先完成「原型冻结」的评审签字：
   /skill:human gate=proto action=sign-off
   或：/skill:human 原型确认了
   ```
4. 若该 Gate 已有 `sign-off` 记录且 action 不是 `hotfix`，提示覆盖确认

### Step 3: 决策记录与文件生成

生成 `human-decisions.md` 记录和 `sign-off/*.md` 签字文件，格式同前版。

### Step 4: 状态更新联动

更新 `progress-tracker` 的 `human_status`，`conditional` 时提示遗留问题跟踪。

### Step 5: 输出确认

**sign-off 成功（语义化输出）**：
```text
✅ 「需求冻结」签字已记录

========================================
变更：reelforge-v1.2-角色工厂重构
========================================
已通过：需求冻结 → 原型冻结 → 设计冻结
当前阶段：UAT 验证（🟡 可启动）

签字文件：openspec/changes/{变更名}/sign-off/03-release.md
审计日志：openspec/changes/{变更名}/human-decisions.md

下一步：
- /skill:uat-verification 生成 UAT 检查清单
- 或直接在预览环境按 user-stories-checklist.md 操作
```

**conditional 成功**：
```text
⚠️ 「原型冻结」有条件通过

遗留问题已记录，请在详细设计阶段跟踪：
  • P1: 创建角色按钮 loading 态细化
  • P2: 移动端适配（记入下一迭代）

签字文件：openspec/changes/{变更名}/sign-off/02.5-prototype.md

请执行：/skill:task-breakdown 将 P1 问题加入 tasks.md
```

**reject 成功**：
```text
❌ 「设计冻结」已驳回

驳回原因：回滚方案中数据库回滚脚本不存在，不可操作。

当前变更已锁定在「概要设计」阶段。
请修改后重新执行：/skill:high-level-design
然后再次申请：/skill:human 设计评审通过
```

### Step 6: 状态查询（action=status）

```text
========================================
人工闸门状态 | 变更：reelforge-v1.2-角色工厂重构
========================================

✅ 需求冻结（req）      已通过   2026-05-06 14:32
⏳ 原型冻结（proto）    待确认   ← 这是你当前的位置
⏸️ 设计冻结（design）   未就绪   （等原型冻结确认）
⏸️ 发布冻结（release）  未就绪   （等设计冻结确认）

========================================
💡 下一步：确认「原型冻结」
========================================

请阅读以下产出物：
  • openspec/changes/{变更名}/detailed-requirements/feature-*/module-requirements.md

然后执行以下任一方式确认：
  /skill:human 原型确认了
  /skill:human gate=proto action=sign-off

如果发现问题：
  /skill:human gate=proto action=reject reason="具体问题描述"
```

### Step 7: 历史查询（action=history）

```text
========================================
决策历史 | 变更：reelforge-v1.2-角色工厂重构
========================================

[001] 需求冻结（req）       sign-off   05-06 14:32  通过
[002] 原型冻结（proto）     conditional 05-07 09:15  通过（遗留：loading态细化）
[003] 设计冻结（design）    sign-off   05-08 11:00  通过

========================================
统计：通过 3 | 有条件 1 | 驳回 0 | 暂停 0
========================================
```

## 输出路径

```
openspec/changes/{变更名}/
├── human-decisions.md          # 审计日志
└── sign-off/
    ├── 01-requirements.md      # 需求冻结签字
    ├── 02.5-prototype.md       # 原型冻结签字
    ├── 02-design.md            # 设计冻结签字
    └── 03-release.md           # 发布冻结签字
```

## 快速参考卡

| 你想做什么 | 推荐命令 |
|-----------|----------|
| 需求评审通过 | `/skill:human 需求评审通过了` |
| 原型确认 | `/skill:human 原型确认了` |
| 设计评审通过 | `/skill:human 设计评审通过` |
| 可以发布 | `/skill:human 可以发布了` |
| 有条件通过（带遗留问题） | `/skill:human 需求通过了，但边界条件还要补充` |
| 驳回 | `/skill:human 设计不行，架构选错了` |
| 查看状态 | `/skill:human 现在状态怎么样？` |
| 查看历史 | `/skill:human action=history` |
| 暂停 | `/skill:human 等第三方文档，先暂停` |
| 恢复 | `/skill:human 文档到了，恢复` |

## Gotchas

- **自然语言不是万能钥匙**：如果说法太模糊（如"通过了"），Skill 会询问"请确认是指哪个阶段通过：需求/原型/设计/发布？"并列出当前待确认的 Gate。
- **自动推断的边界**：`action=reject` / `pause` 自动推断时，默认作用于当前待确认的 Gate。若你想驳回一个已经通过的 Gate，必须显式指定 `gate=`。
- **conditional 必须带问题**：自然语言触发 conditional 时，输入中必须包含"但/不过/遗留/还有问题"等关键词，否则会被识别为 `sign-off`。
- **多人协作时**：若 A 说"原型确认了"，B 说"原型还要改"，以最新一条 DECISION 为准，但两条都保留在 `human-decisions.md` 中。
- **hotfix 必须显式指定**：`hotfix` 不能通过自然语言推断，必须显式写 `/skill:human gate=hotfix action=sign-off`。
- **status 不修改任何文件**：纯读取操作，可安全频繁调用。建议在每个阶段开始前先查一下 status。
- **语义化名称大小写不敏感**：`req` = `REQ` = `Req` = `requirements`。
