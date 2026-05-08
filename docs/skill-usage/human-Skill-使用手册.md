# human Skill 使用手册

> 四道人工闸门的统一入口
>
> 版本 V1.0 | 2026-05-08
>
> 本文档面向工具链使用者，提供 human Skill 的完整操作指南、场景示例和常见问题解答。

---

## 目录

- [一、human Skill 是什么](#一human-skill-是什么)
- [二、四道人工闸门速查](#二四道人工闸门速查)
- [三、三种使用方式](#三三种使用方式)
  - [3.1 自然语言触发（最推荐）](#31-自然语言触发最推荐)
  - [3.2 语义化命名（精确控制）](#32-语义化命名精确控制)
  - [3.3 自动推断（极简）](#33-自动推断极简)
- [四、完整场景示例](#四完整场景示例)
  - [4.1 场景：需求评审通过](#41-场景需求评审通过)
  - [4.2 场景：原型有条件通过](#42-场景原型有条件通过)
  - [4.3 场景：设计被驳回](#43-场景设计被驳回)
  - [4.4 场景：等待第三方接口](#44-场景等待第三方接口)
  - [4.5 场景：查看当前状态](#45-场景查看当前状态)
- [五、决策类型详解](#五决策类型详解)
- [六、状态查询与历史追溯](#六状态查询与历史追溯)
- [七、常见问题](#七常见问题)
- [八、快速参考卡](#八快速参考卡)

---

## 一、human Skill 是什么

在 AI 项目落地工具链中，很多关键节点需要**人工确认**后才能继续：

- AI 生成概要需求后 → **你需要确认**需求是否覆盖了业务闭环
- AI 生成详细需求的交互规格后 → **你需要逐页确认**按钮状态机
- AI 生成架构设计后 → **你需要确认**技术选型和回滚方案
- UAT 测试通过后 → **你需要确认**可以上线发布

**human Skill 就是记录这些确认的统一入口。**

它像 Git 的 commit——你说"确认了"，它就帮你：
1. 记录这次决策（谁、什么时候、什么结论）
2. 解锁下一个阶段
3. 生成签字文件供归档审计

**核心原则：它不替代你做判断，只帮你记录判断结果。**

---

## 二、四道人工闸门速查

工具链中有 **4 个必须人工确认的节点**，称为"闸门"：

| 阶段 | 闸门名称 | 你要确认什么 | 常用说法 |
|------|---------|-------------|----------|
| 概要需求完成后 | **需求冻结** | 5 个 spec 文件是否覆盖业务闭环 | "需求通过了" |
| 详细需求完成后 | **原型冻结** | 每个按钮的交互状态机是否正确 | "原型确认了" |
| 概要设计完成后 | **设计冻结** | 架构选型、回滚方案是否合理 | "设计通过了" |
| UAT + 代码审查后 | **发布冻结** | 是否可以在生产环境发布 | "可以发布了" |

> 💡 **记不住编号没关系**：你不需要记 "Gate1"、"Gate2.5" 这些数字。直接说 "需求通过了"、"原型确认了"，human Skill 会自动识别你在确认哪个闸门。

---

## 三、三种使用方式

### 3.1 自然语言触发（最推荐）

**直接说出你的结论**，像平时说话一样。human Skill 会自动识别你在确认哪个阶段。

```bash
# ✅ 需求评审通过
/skill:human 需求评审通过了

# ✅ 原型确认（有条件通过，带遗留问题）
/skill:human 原型确认了，但 loading 态还需要细化

# ✅ 设计评审通过
/skill:human 设计评审通过

# ✅ 可以发布上线
/skill:human 可以发布了

# ❌ 驳回设计
/skill:human 设计不行，回滚方案不可操作

# ⏸️ 暂停流程
/skill:human 等第三方接口文档，先暂停一下

# ▶️ 恢复流程
/skill:human 接口文档到了，恢复流程
```

**关键词对照表**：

| 你想表达 | 这样说 | human Skill 会识别为 |
|----------|--------|---------------------|
| 需求通过 | "需求通过了" / "PRD 没问题" / "需求确认了" | Gate 1 sign-off |
| 原型通过 | "原型确认了" / "交互 OK" / "页面没问题" | Gate 2.5 sign-off |
| 设计通过 | "设计通过了" / "架构没问题" / "HLD OK" | Gate 2 sign-off |
| 发布通过 | "可以发布了" / "上线" / "UAT 通过" | Gate 3 sign-off |
| 有条件通过 | "通过了，但..." / "没问题，不过..." | conditional（自动识别"但/不过"） |
| 驳回 | "不行" / "驳回" / "重做" / "设计错了" | reject |
| 暂停 | "暂停" / "先停一下" / "阻塞" | pause |
| 恢复 | "继续" / "恢复" / "可以走了" | resume |
| 查状态 | "状态怎么样" / "现在到哪了" / "下一步该做什么" | status |

> ⚠️ **如果说法太模糊**（比如只说"通过了"，没说是哪个阶段），human Skill 会询问："请确认是指哪个阶段通过：需求/原型/设计/发布？"并列出你当前待确认的闸门。

---

### 3.2 语义化命名（精确控制）

当你需要精确控制，或者自然语言没识别对时，用阶段名：

```bash
# 需求冻结
/skill:human gate=req action=sign-off

# 原型冻结（有条件通过）
/skill:human gate=proto action=conditional issues="P1: loading态细化"

# 设计冻结（驳回）
/skill:human gate=design action=reject reason="回滚方案不可操作"

# 发布冻结
/skill:human gate=release action=sign-off
```

**gate 别名对照表**（大小写不敏感）：

| 你想确认 | 可以写的 gate 值 |
|----------|-----------------|
| 需求冻结 | `req`、`requirements`、`requirement-freeze`、`需求`、`需求冻结`、`Gate1` |
| 原型冻结 | `proto`、`prototype`、`prototype-freeze`、`原型`、`原型冻结`、`Gate2.5` |
| 设计冻结 | `design`、`design-freeze`、`设计`、`设计冻结`、`HLD`、`Gate2` |
| 发布冻结 | `release`、`release-freeze`、`uat`、`发布`、`发布冻结`、`上线`、`Gate3` |

> 💡 **`action` 只有 6 种**：`sign-off`（通过）、`conditional`（有条件通过）、`reject`（驳回）、`pause`（暂停）、`resume`（恢复）、`status`（查状态）、`history`（查历史）。

---

### 3.3 自动推断（极简）

**什么都不指定**，让 human Skill 自己判断当前该确认哪个闸门：

```bash
# 自动推断当前待确认的闸门，执行签字
/skill:human action=sign-off

# 自动推断当前闸门，执行驳回
/skill:human action=reject reason="Safari下无法保存"

# 查询当前状态
/skill:human action=status
```

**自动推断规则**：
1. human Skill 查看当前变更的进度
2. 找到第一个还没通过的闸门
3. 自动把决策记到那个闸门上

> ⚠️ **什么情况下自动推断会失效？**
> - 你想驳回一个**已经通过**的闸门 → 必须显式指定 `gate=`
> - 当前有多个闸门都处于待确认状态 → 按顺序取第一个
> - 所有闸门都通过了 → 提示"所有闸门已通过"

---

## 四、完整场景示例

### 4.1 场景：需求评审通过

**背景**：AI 生成了 5 个概要需求文档（01-product-overview 到 05-non-functional），你阅读后认为没问题。

**操作**：
```bash
/skill:human 需求评审通过了
```

**human Skill 的响应**：
```text
✅ 「需求冻结」签字已记录

========================================
变更：reelforge-v1.2-角色工厂重构
========================================
已通过：需求冻结
当前阶段：详细需求（🟡 可启动）

签字文件：openspec/changes/{变更名}/sign-off/01-requirements.md
审计日志：openspec/changes/{变更名}/human-decisions.md

下一步：
- /skill:detailed-requirements 生成模块级详细需求
```

**产出的文件**：
- `human-decisions.md` 中新增一条 DECISION 记录
- `sign-off/01-requirements.md` 生成签字确认单

---

### 4.2 场景：原型有条件通过

**背景**：AI 生成了详细需求的交互规格（interaction-spec.md），你检查后发现大部分没问题，但创建角色的 loading 态还没细化。

**操作**：
```bash
/skill:human 原型确认了，但创建角色的 loading 态还需要细化
```

**human Skill 的响应**：
```text
⚠️ 「原型冻结」有条件通过

遗留问题已记录，请在详细设计阶段跟踪：
  • P1: 创建角色按钮 loading 态细化

签字文件：openspec/changes/{变更名}/sign-off/02.5-prototype.md

请执行：/skill:task-breakdown 将上述遗留问题加入 tasks.md
```

**关键点**：
- "但有..." 会被自动识别为 `conditional`（有条件通过）
- 遗留问题会被记录，后续 `self-check` 会检查是否已修复
- 下游 Skill（如 `high-level-design`）可以正常启动

---

### 4.3 场景：设计被驳回

**背景**：AI 生成了架构设计，但你发现回滚方案中缺少数据库回滚脚本，不可操作。

**操作**：
```bash
/skill:human 设计不行，回滚方案里数据库回滚脚本不存在
```

**human Skill 的响应**：
```text
❌ 「设计冻结」已驳回

驳回原因：回滚方案里数据库回滚脚本不存在

当前变更已锁定在「概要设计」阶段。
请修改后重新执行：/skill:high-level-design
然后再次申请：/skill:human 设计评审通过
```

**关键点**：
- 驳回后，当前阶段被锁定
- 必须重新执行上游 Skill（`high-level-design`）修复问题
- 不能直接在原文件上改完后重新 sign-off（必须通过 Skill 重新生成）

---

### 4.4 场景：等待第三方接口

**背景**：概要设计评审到一半，发现需要等第三方支付接口文档确认，无法继续。

**操作**：
```bash
/skill:human 等第三方支付接口文档，先暂停
```

**几天后，文档到了**：
```bash
/skill:human 接口文档到了，恢复
```

**关键点**：
- `pause` 会阻塞所有下游阶段
- `resume` 后回到 pause 之前的状态
- 暂停期间，任何下游 Skill 都无法启动

---

### 4.5 场景：查看当前状态

**操作**：
```bash
/skill:human 现在状态怎么样？
```

**human Skill 的响应**：
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
  • openspec/changes/{变更名}/specs/feature-*/interaction-spec.md

然后执行以下任一方式确认：
  /skill:human 原型确认了
  /skill:human gate=proto action=sign-off

如果发现问题：
  /skill:human gate=proto action=reject reason="具体问题描述"
```

---

## 五、决策类型详解

| 类型 | 什么时候用 | 后续影响 | 示例 |
|------|-----------|----------|------|
| **sign-off** | 完全通过，无遗留问题 | 解锁下一阶段 | "需求通过了" |
| **conditional** | 主要通过，有小问题可延后 | 解锁下一阶段，但遗留问题必须记入 `tasks.md` | "原型确认了，但 loading 态还要细化" |
| **reject** | 有严重问题，必须返工 | 锁定当前阶段，重修上游 Skill | "设计不行，架构选错了" |
| **pause** | 因外部依赖暂时无法继续 | 阻塞所有下游，等待恢复 | "等第三方接口文档，先暂停" |
| **resume** | 外部依赖已解决 | 解除 pause，回到之前状态 | "文档到了，恢复" |
| **hotfix** | 已归档的变更需要紧急补丁 | 直接记录，不走完整 Gate 流程 | `/skill:human gate=hotfix action=sign-off` |

**重要提醒**：
- `conditional` 的遗留问题**不是optional**——如果不处理，后续 `self-check` 会报警
- `reject` 后**不能直接改文件重新 sign-off**——必须通过上游 Skill 重新生成产出物
- `hotfix` 只能用于已归档的变更，正常流程中不要用

---

## 六、状态查询与历史追溯

### 查当前状态

```bash
/skill:human 现在状态怎么样？
# 或
/skill:human action=status
```

输出内容：
- 4 个闸门的通过状态和时间
- 你当前在哪个位置
- 下一步该做什么
- 推荐命令

### 查历史决策

```bash
/skill:human action=history
```

输出内容：
- 所有决策记录（DECISION-001、002...）
- 每次决策的时间、决策人、结论
- 统计：通过几次、有条件通过几次、驳回几次

### 文件位置

所有决策记录保存在：
```
openspec/changes/{变更名}/
├── human-decisions.md          ← 审计日志（所有决策）
└── sign-off/
    ├── 01-requirements.md      ← Gate 1 签字文件
    ├── 02.5-prototype.md       ← Gate 2.5 签字文件
    ├── 02-design.md            ← Gate 2 签字文件
    └── 03-release.md           ← Gate 3 签字文件
```

> 这些文件会被 `opsx:archive` 自动纳入归档范围。

---

## 七、常见问题

### Q1：我不记得当前该确认哪个闸门了怎么办？

**A**：直接说：
```bash
/skill:human 现在状态怎么样？
```
human Skill 会告诉你当前在哪个位置、下一步该确认什么、推荐用什么命令。

### Q2：自然语言没识别对怎么办？

**A**：如果说法太模糊（比如只说"通过了"），human Skill 会询问你要确认哪个阶段。你也可以直接用语义化命名：
```bash
/skill:human gate=proto action=sign-off
```

### Q3：我想驳回一个已经通过的闸门，怎么做？

**A**：必须显式指定 gate：
```bash
/skill:human gate=design action=reject reason="发现严重架构缺陷"
```
自动推断只能作用于当前待确认的闸门，不能作用于已通过的闸门。

### Q4：conditional 的遗留问题不处理会怎样？

**A**：后续 `self-check` 会检查 `tasks.md` 中是否有对应的遗留问题任务。如果没有，会报警。建议在 conditional 后立即执行：
```bash
/skill:task-breakdown 将遗留问题加入 tasks.md
```

### Q5：多人协作时，如果两个人做出了不同决策？

**A**：以**最新一条**决策为准，但**两条都保留**在 `human-decisions.md` 中作为追溯依据。例如：
- A 说"原型确认了" → 记录为 passed
- B 说"原型还要改" → 记录为 rejected，并以这条为准

### Q6：status 查询会修改任何文件吗？

**A**：**不会**。`status` 和 `history` 是纯读取操作，可以安全地频繁调用。建议在每个阶段开始前先查一下状态。

### Q7：我可以跳过某个闸门直接确认下一个吗？

**A**：**不可以**。human Skill 会检查前置闸门是否已通过。例如，如果你想确认"设计冻结"但"需求冻结"还没通过，会返回：
```text
❌ 无法确认「设计冻结」：前置「需求冻结」尚未签字。
```

### Q8：Gate 2.5（原型冻结）不通过，会影响 Gate 2（设计冻结）吗？

**A**：**不会**。根据工具链设计，Gate 2.5 和 Gate 2 是并行的：
- Gate 2（概要设计）只要求 Gate 1（需求冻结）已通过
- Gate 2.5（原型冻结）通过后才启动详细设计
- 但概要设计可以在原型冻结之前启动

---

## 八、快速参考卡

打印出来贴在显示器旁边：

```
┌─────────────────────────────────────────────────────────────┐
│                    human Skill 快速参考                      │
├─────────────────────────────────────────────────────────────┤
│ 需求通过      →  /skill:human 需求评审通过了                  │
│ 原型确认      →  /skill:human 原型确认了                      │
│ 设计通过      →  /skill:human 设计评审通过                    │
│ 可以发布      →  /skill:human 可以发布了                      │
│ 有条件通过    →  /skill:human 通过了，但 xxx 还要补充         │
│ 驳回          →  /skill:human 不行，原因是 xxx                │
│ 暂停          →  /skill:human 等 xxx，先暂停                  │
│ 恢复          →  /skill:human 恢复了，继续                    │
│ 查状态        →  /skill:human 现在状态怎么样？                │
│ 查历史        →  /skill:human action=history                  │
├─────────────────────────────────────────────────────────────┤
│ 精确控制（当自然语言不识别时）：                              │
│   gate=req/proto/design/release action=sign-off             │
│   gate=req/proto/design/release action=conditional          │
│   gate=req/proto/design/release action=reject               │
│   gate=req/proto/design/release action=pause                │
│   gate=req/proto/design/release action=resume               │
├─────────────────────────────────────────────────────────────┤
│ 自动推断（不指定 gate）：                                     │
│   /skill:human action=sign-off                              │
│   /skill:human action=reject reason="xxx"                   │
└─────────────────────────────────────────────────────────────┘
```

---

*本文档随 human Skill 迭代持续更新。如有问题，请查看 `skills/sdlc/human/SKILL.md` 获取最完整的规范。*
