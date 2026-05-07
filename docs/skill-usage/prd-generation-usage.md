# PRD-000 概要需求生成器 — 使用手册

> **Skill 版本**：2.0.0
> **适用阶段**：OpenSpec 阶段 1（概要需求生成）
> **关联 Skill**：`brainstorming`、`requirement-analysis`、`competitive-analysis`、`high-level-design`、`detailed-requirements`、`progress-tracker`、`self-check`
> **更新日期**：2026-05-06

---

## 一、适用场景

当你遇到以下情况时，应使用 **prd-generation** Skill：

- 从零开始规划一个新产品、新系统或大型功能集
- 需要为后续详细需求（PRD-001~PRD-00N）建立不可推翻的基线约束
- 项目启动前需要明确 Scope、干系人、里程碑和模块边界
- 希望避免 PRD 中出现逻辑矛盾、功能遗漏或技术方案滞后
- 已有 brainstorming 结果，需要将探索性结论转化为结构化需求文档

**不适用场景**：
- 已进入编码阶段后补写 PRD（应走变更流程）
- 仅需生成单个功能的详细规格（应使用 `prd-feature-detail`）
- 纯技术预研，无明确业务目标

---

## 二、前置条件

### 2.1 必依赖项

| 依赖类型 | 具体要求 | 说明 |
|----------|----------|------|
| **OpenSpec 目录** | `openspec/changes/{变更名}/` 已创建 | 可通过 `/opsx:propose` 或手动创建 |
| **config.yaml** | `openspec/config.yaml` 存在且包含 `artifact_specs.high-level-requirements` | Skill 读取 required_sections 作为输出模板 |
| **brainstorming** | 建议先完成（非强制） | 提供需求探索的上下文和初步结论 |

### 2.2 可选准备

- **本地资料**：已有业务文档、竞品分析、数据报表的路径（如 `@docs/legacy/xxx.md`）
- **产品 URL**：若需对现有产品进行功能审计，提供可访问的 URL
- **技术约束**：团队既定的技术栈、合规要求、部署环境等信息

---

## 三、快速开始

### 3.1 启动方式

**方式一：用户主动触发**

```kimi
💫 帮我写一下 AI 短剧生成平台的概要需求
```

或：

```kimi
 /skill:prd-generation  基于 brainstorming 结果生成概要需求。
参考文档：@openspec/changes/*/proposal.md   @docs/*/*
```

**方式二：通过 /opsx:propose 触发**

```bash
/opsx:propose "为 reelforge 增加 AI 剧本分镜自动生成功能"
```

随后 Skill 自动加载并执行。

### 3.2 典型会话流程

```
用户：我要做一个 AI 短剧生成平台，帮我写概要需求
    ↓
Kimi：[触发 prd-generation skill]
    ↓
【Step 0: 初始化】
读取 openspec/config.yaml → 检测到变更：changes/短剧生成平台-v1
    ↓
【Layer 1: 问题界定】（逐题访谈）
问题 1/9：请用 1-2 句话描述核心痛点...
用户：传统短剧制作周期 2-3 个月，成本高...
    ↓
[Layer 1 完成后]
本层评分：88 分（🟡 黄灯）
缺失项：1. 未提出可量化的北极星指标  2. 竞品信息不足
请补充...
    ↓
用户：北极星指标是单项目剧本到成片 < 48 小时。竞品是 Runway...
    ↓
补充后评分：95 分（🟢 绿灯）。进入 Layer 2...
    ↓
【Layer 2: 方案界定】→ 🟢 绿灯
【Layer 3: 成功标准】→ 🟢 绿灯
【Layer 4: 一致性校验】→ 发现 🔴 严重问题，等待用户确认...
    ↓
用户确认后 → 【Step 5: 输出与冻结】
生成 5 个文件 → 保存到 openspec/changes/短剧生成平台-v1/specs/
    ↓
宣读冻结规则 → 等待用户"确认"
    ↓
用户：确认
文档状态更新为：已冻结 ✅
```

---

## 四、各阶段详细说明

### 4.1 Layer 1 — 问题界定（Problem Framing）

**目标**：理解"为什么做"和"为谁做"。

**你会经历什么**：
- AI 会一次只问一个问题，共 9 个核心问题
- 问题围绕：业务痛点、目标用户、价值主张、北极星指标、竞品
- 会主动用 **JTBD 格式**帮你提炼需求："When [场景], I want to [动机], so I can [结果]"

**评分标准**：
- 🟢 ≥90 分：进入 Layer 2
- 🟡 70-89 分：补充 1-3 项关键信息
- 🔴 <70 分：大规模返工

**典型追问示例**：
- 你说"提升效率" → AI 追问："具体是哪个环节？当前耗时多少？目标耗时多少？"
- 你说"用户体验不好" → AI 追问："能否描述一个具体的用户失败场景？"

---

### 4.2 Layer 2 — 方案界定（Solution Framing）

**目标**：确定"系统做什么、不做什么、由哪些模块构成"。

**你会经历什么**：
- 基于 Layer 1 的结论，AI 引导你识别功能模块
- 输出 **Component Inventory**（组件清单），直接决定后续详细需求的拆分目录
- 必须明确列出 **Out-of-Scope**（本次不做什么）
- 定义核心实体（如：项目、剧本、角色、订单）及其关系

**关键输出**：
- In-Scope / Out-of-Scope 清单
- 模块清单（模块名 = 后续 `feature-XX-{模块名}/` 目录名）
- Component Inventory（UI 组件级拆解）

**相反测试示例**：
- 你说"不做支付" → AI 追问："如果用户需要购买高级功能，Phase 1 怎么处理？"

---

### 4.3 Layer 3 — 成功标准（Success Criteria）

**目标**：量化北极星指标、非功能需求和里程碑。

**你会经历什么**：
- 定义可量化的北极星指标（当前值 + 目标值）
- 定义全局 NFR（性能、并发、安全、兼容、可维护），附行业对标档位
- 制定 Phase 1/2/3 里程碑

**NFR 行业对标档位**：
- AI 会告诉你："同类 SaaS 通常承诺 99.9% SLA，你设定 99.95% 属于高档位"
- 帮助你判断是否存在过度设计或明显短板

---

### 4.4 Layer 4 — 一致性校验与竞品对标（强制，不可跳过）

**目标**：捕获内部矛盾、方案缺陷和技术滞后问题。

**校验内容**：
1. **内部一致性**：Scope 是否自洽？实体与模块是否匹配？NFR 与技术选型是否兼容？
2. **竞品对标**：功能是否遗漏？技术方案是否过时？合规基线是否完整？

**问题分级**：
- 🔴 **严重（阻塞）**：必须解决或经你明确确认接受风险，否则不生成 PRD
- 🟡 **建议（待决策）**：AI 列出建议，由你决定是否采纳
- 🟢 **提示（信息补充）**：自动写入风险提示章节

**典型发现示例**：
> 🔴 严重：Out-of-Scope 包含"支付系统"，但 In-Scope 包含"会员购买"。商业模式存在逻辑缺口。
> - 建议：Phase 1 采用免费+申请试用，支付系统放入 Phase 2
> - 请你确认：A. 按建议调整  B. 保持原方案并说明原因

---

### 4.5 输出与冻结

**生成的 5 个文件**：

| 文件 | 内容 | 下游影响 |
|------|------|----------|
| `01-product-overview.md` | 痛点、北极星指标、JTBD、竞品对标 | 全局上下文 |
| `02-requirements-list.md` | P0/P1/P2 需求、用户故事、术语表 | 测试追溯基准 |
| `03-functional-structure.md` | 模块树、Component Inventory、详细 PRD 清单 | **决定详细需求拆分粒度** |
| `04-business-rules.md` | Mermaid 流程图、RBAC 矩阵、状态机 | 详细设计输入 |
| `05-non-functional.md` | 性能/安全/并发、技术栈、里程碑、风险提示 | 架构约束 |

**保存路径**：
```
openspec/changes/{变更名}/specs/
├── 01-product-overview.md
├── 02-requirements-list.md
├── 03-functional-structure.md
├── 04-business-rules.md
└── 05-non-functional.md
```

**冻结规则**：
确认基线后，`Out-of-Scope`、`全局 NFR`、`核心实体主键`、`模块清单` 在后续详细 PRD 中不可推翻。如需修改，必须升级 PRD-000 版本号并重新评审所有关联详细 PRD。

---

## 五、指令速查表

| 你想让 Kimi 做... | 发送的指令 |
|-------------------|-----------|
| 开始生成概要需求 | "我要做一个 [产品名]，帮我写概要需求" |
| 指定参考文档 | "参考文档：@openspec/changes/{变更名}/proposal.md" |
| 查看产出物 | "打开 openspec/changes/{变更名}/specs/01-product-overview.md" |
| 继续被阻塞的层 | 直接回答 AI 的追问即可 |
| 确认基线冻结 | "确认" |
| 跳过某层（不推荐） | 明确告诉 AI "跳过 Layer X"（AI 会警告风险） |

---

## 六、常见问题

**Q1：为什么 AI 不一次性把所有问题问完？**
> 四层递进式对话的设计目的是确保每层信息完整后再进入下一层。如果一次性问完，用户可能在信息不全的情况下做出错误判断，导致后续大规模返工。

**Q2：评分 < 90 分一定要补充吗？**
> 强烈建议补充。如果某维度确实无法提供（如确实无竞品），AI 允许标记为"已知缺失"并降权处理，但其他缺失项仍需补充。

**Q3：Layer 4 发现严重问题，AI 会自己修吗？**
> **不会**。AI 会列出问题清单和修正建议，等待你确认后才修正。这是为了防止 AI 误解你的意图而擅自改动需求。

**Q4：模块名确定后还能改吗？**
> 冻结后不建议改。因为 `03-functional-structure.md` 中的模块名直接映射到 `feature-XX-{模块}/` 目录，修改会导致下游所有 Skill 的目录引用失效。

**Q5：没有 OpenSpec 环境能用吗？**
> 可以运行，但 AI 会提示你初始化 OpenSpec 目录。没有 config.yaml 时，Skill 会使用内置默认模板输出。

**Q6：和 `prd-system-outline` 有什么区别？**
> `prd-system-outline` 输出单文件 PRD-000；`prd-generation` 输出五文件（与 OpenSpec 深度集成），并增加了 JTBD 框架、Component Inventory、原子声明分解验证等增强功能。

---

## 七、输出物使用指南

### 7.1 下游 Skill 接力

```
prd-generation (产出 5 文件)
    ├──→ competitive-analysis (读取 01-product-overview.md 第 3 章)
    ├──→ high-level-design (读取 04/05 进行概要设计)
    ├──→ detailed-requirements (读取 03 按模块拆分 PRD-001~PRD-00N)
    └──→ self-check (读取全部 5 文件执行最终校验)
```

### 7.2 模块拆分示例

若 `03-functional-structure.md` 定义了以下模块：

| 编号 | 模块名称 | 对应目录 |
|------|----------|----------|
| PRD-001 | 剧本工坊 | `feature-01-script-workshop/` |
| PRD-002 | 角色工厂 | `feature-02-character-factory/` |

则后续 `detailed-requirements` Skill 会：
1. 为每个模块独立生成详细需求文档
2. 保存在对应的 `feature-XX-{模块}/` 目录下
3. 确保模块名与 PRD-000 保持一致

---

## 八、版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 2.0.0 | 2026-05-06 | 重构为 prd-generation。融合 abeejuice/johnnychauvet/cdeust 开源项目优势。输出改为 OpenSpec 五文件规范，增加 JTBD 框架、Component Inventory、原子声明分解验证。 |
| 1.1.0 | 2026-04-26 | 增加第四层"一致性校验与竞品对标"机制。 |
| 1.0.0 | 2026-04-20 | 初始版本（prd-system-outline）。 |
