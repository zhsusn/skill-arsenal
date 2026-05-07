---
name: prd-generation
description: 当用户要求'写PRD'、'概要需求'、'系统规划'或从零开始规划新产品时触发。通过四层递进式对话生成OpenSpec五文件概要需求。
---

# PRD-000 概要需求生成器

## 适用场景
- 从零开始规划一个新产品、新系统或大型功能集
- 需要为后续详细需求（PRD-001~PRD-00N）建立不可推翻的基线约束
- 项目启动前明确 Scope、干系人、里程碑和模块边界
- 希望避免 PRD 中出现逻辑矛盾、功能遗漏或技术方案滞后

## 核心职责
1. **四层递进式对话**：严格按 Layer 1→2→3→4 推进，每层评分 < 90 分则阻塞追问
2. **红绿灯评分机制**：每层结束后调用 `references/completeness-scoring.md` 进行量化评分
3. **强制一致性校验**：Layer 4 调用 `references/consistency-checklist.md`，未通过不得输出
4. **基线冻结**：用户确认后，Scope、NFR、核心实体在详细阶段不可推翻
5. **五文件输出**：按 OpenSpec 规范输出 5 个 Markdown 文件到 `openspec/changes/{变更名}/specs/`
6. **JTBD 框架**：在需求表达中融入 Jobs-to-be-Done 格式，确保从"为什么"出发
7. **多渠道资料收集**：自动调用 `web_search` 收集竞品资料，读取 `@路径` 本地文档

## 使用说明

### 如何触发
- "我要做一个 [产品/系统名称]，先帮我写概要需求"
- "帮我定一下 [项目名] 的需求基线"
- "生成 PRD-000"
- "写 PRD"

### 用户配合要点
1. **准备材料**（可选但推荐）：提前整理业务背景、竞品分析、现有系统资料。
2. **逐层确认**：每层结束后会给出一个"完整性评分"。若标红（<90 分），请根据追问补充信息，不要跳过。
3. **明确说"不"**：当询问 Out-of-Scope 时，请明确列出"系统不需要做什么"。
4. **重视校验阶段**：第四层校验不可跳过，若发现严重问题，会列出清单请您确认。
5. **基线冻结确认**：校验通过并输出完整的 PRD-000 后，会询问"是否确认基线？"。

## 执行步骤

### Step 0: 初始化
- 读取 `openspec/config.yaml` 获取 `artifact_specs.high-level-requirements` 模板
- 检查当前是否已有进行中的变更目录；若无则提示用户先创建变更提案
- 确认 `openspec/changes/{变更名}/specs/` 存在，否则自动创建
- 读取用户提供的本地资料（`@路径`）和 brainstorming 结果

### Step 1: Layer 1 — 问题界定（Problem Framing）
目标：理解"为什么做"和"为谁做"，收集竞品与技术背景。

1. 按 `references/questioning-guide.md`「第一层提问集」逐题访谈。一次只问一个问题。
2. 在访谈中融入 JTBD 格式："When [场景], I want to [动机], so I can [结果]"。
3. 若用户未提供竞品信息，主动调用 `web_search` 搜索行业竞品供用户确认。
4. 输出「问题框架摘要」：业务痛点、目标用户画像、核心价值主张、竞品基准。
5. 调用 `references/completeness-scoring.md` 进行 Layer 1 评分。
6. 若评分 < 90 分：列出缺失项，阻塞并追问，直到 ≥ 90 分。

### Step 2: Layer 2 — 方案界定（Solution Framing）
目标：确定"系统做什么、不做什么、由哪些模块构成"。

1. 基于 Layer 1 成果，按 `references/questioning-guide.md`「第二层提问集」访谈。
2. 识别系统功能模块，输出 Component Inventory（组件清单），直接映射到后续 `feature-XX-{模块}/` 目录。
3. 明确 In-Scope / Out-of-Scope（**Out-of-Scope 必须明确列出**）。
4. 定义核心实体（名称 + 主键 + 关系）。
5. 初步确定技术方案，并与竞品主流方案进行简单对比。
6. 若用户提供产品 URL，调用 `web_search` / `web_open_url` 进行页面功能审计，补充到模块识别。
7. 调用 `references/completeness-scoring.md` 进行 Layer 2 评分。
8. 若评分 < 90 分：阻塞并追问。

### Step 3: Layer 3 — 成功标准（Success Criteria）
目标：量化北极星指标、非功能需求和里程碑。

1. 按 `references/questioning-guide.md`「第三层提问集」访谈。
2. 定义量化北极星指标（当前值 + 目标值）。
3. 定义全局 NFR（性能、并发、安全、兼容、可维护），附行业对标档位（高/中/低）。
4. 制定里程碑（Phase 1/2/3），确保 Phase 1 为最小可用闭环。
5. 调用 `references/completeness-scoring.md` 进行 Layer 3 评分。
6. 若评分 < 90 分：阻塞并追问。

### Step 4: Layer 4 — 一致性校验与竞品对标（强制）
目标：捕获内部矛盾、方案缺陷和技术滞后问题。**未通过本层不得输出最终 PRD**。

1. 激活 `references/consistency-checklist.md`：
   - 执行「内部一致性校验」（Scope 自洽性、实体-模块一致性、NFR-技术一致性、角色-权限一致性、**术语行为一致性**）
   - 执行「竞品对标与技术方案校验」（功能完整性、技术先进性、合规完整性）
2. 若用户未提供竞品技术细节，主动调用 `web_search` 搜索竞品最新功能和技术方案。
3. 问题分级：
   - 🔴 严重：列出问题清单，使用 checklist 中的「用户确认模板」展示，**等待用户明确答复**
   - 🟡 建议：列为「待决策项」
   - 🟢 提示：写入「风险提示」章节
4. **若存在未解决的 🔴 严重问题，禁止进入 Step 5**。
5. 校验完成后，向用户公示「校验摘要」。

### Step 5.0: 章节对齐校验（输出前强制检查）
在写入五文件前，必须执行以下刚性检查，确保与 `config.yaml` 的 `required_sections` 对齐：

1. 读取 `openspec/config.yaml` 当前阶段（`high-level-requirements`）的 `gate_to_next.required_sections` 清单。
2. 读取 `references/system-outline-template.md` 的五文件映射表，确认每个 required_section 的物理归宿文件。
3. 检查待生成的 Markdown 中是否存在对应 H2 标题或明确章节。允许**语义等价映射**（如"核心问题"≈"项目背景与目标"、"边界范围"≈"系统范围（Scope）"），但必须在输出摘要中向用户明示映射关系。
4. 若 required_section 在对应文件中无实质内容（空表、空列表、仅占位符），标记为 🔴 阻塞，禁止进入保存步骤。
5. 若使用了语义等价标题但未精确匹配 config.yaml 的字面要求，标记为 🟡 提示，写入 05-non-functional.md 的「待决策项」。

### Step 5: 输出与冻结
1. 按 `references/system-outline-template.md` 和 OpenSpec 五文件规范输出：
   - `01-product-overview.md`：产品概述、目标用户、核心价值、JTBD 列表
   - `02-requirements-list.md`：需求清单（P0/P1/P2）、用户故事（US-XXX）、业务术语表
   - `03-functional-structure.md`：功能结构（模块-功能点树状图）、Component Inventory、模块到 feature 目录的映射
   - `04-business-rules.md`：全局业务规则、权限矩阵、业务流程图（Mermaid）
   - `05-non-functional.md`：性能/安全/可靠性 NFR、原型草图、技术栈建议
2. 自动保存到 `openspec/changes/{变更名}/specs/`
3. 在 `03-functional-structure.md` 末尾附加「详细 PRD 清单」，列出 PRD-001~PRD-00N 的模块映射：
   | 编号 | 模块名称 | 对应目录 | 状态 |
   | PRD-001 | {模块A} | `feature-01-{模块A}/` | 待编写 |
4. 向用户宣读冻结规则，等待用户回复"确认"。
5. 用户确认后，执行基线冻结操作：
   a. 将五文件头部的 `版本：PRD-000 v1.0-draft` 统一替换为 `版本：PRD-000 v1.0`。
   b. 将五文件头部的 `状态：待用户确认基线后冻结` 统一替换为 `状态：已冻结（基线）`。
   c. 更新 `last_updated` 为当前日期。
   d. 保存文件后，向用户宣读："PRD-000 基线已冻结，五文件元数据已同步更新。后续详细阶段不可推翻 Scope、NFR 与核心实体定义。"

## 输出格式

### 五文件结构（OpenSpec 规范）

| 文件 | 对应章节 | 核心内容 | 下游影响 |
|------|----------|----------|----------|
| `01-product-overview.md` | 项目背景与目标、竞品分析 | 痛点、北极星指标、JTBD、竞品对标 | 全局上下文 |
| `02-requirements-list.md` | 需求清单、业务术语、用户故事 | P0/P1/P2 需求、US-XXX 用户故事、术语表 | 测试追溯基准 |
| `03-functional-structure.md` | 功能架构、Component Inventory | 模块树、组件清单、模块→目录映射 | **决定详细需求拆分粒度** |
| `04-business-rules.md` | 业务流程、权限矩阵、业务规则 | Mermaid 流程图、RBAC 矩阵、状态机 | 详细设计输入 |
| `05-non-functional.md` | NFR、原型草图、技术约束 | 性能/安全/并发指标、技术栈、里程碑 | 架构约束 |

### 优先级标记
- **P0**：必须交付，缺一则系统不可用
- **P1**：重要，影响核心体验
- **P2**：优化项，可延后

### 模块命名约束
`03-functional-structure.md` 中的模块名必须与 `feature-XX-{模块名}/` 目录名保持一致（kebab-case），直接影响 `detailed-requirements` Skill 的目录拆分。

## 协作接口

| 方向 | Skill/文档 | 说明 |
|------|-----------|------|
| 上游 | `brainstorming` | 提供初步需求探索结果 |
| 上游 | `requirement-analysis` | 提供结构化需求输入 |
| 下游 | `competitive-analysis` | 读取 01-product-overview.md 进行深度竞品分析 |
| 下游 | `high-level-design` | 读取 04/05 进行概要设计 |
| 下游 | `detailed-requirements` | 读取 03 的模块清单按 feature-XX-{模块}/ 拆分 |
| 贯穿 | `progress-tracker` | 每完成一层更新进度 |
| 贯穿 | `self-check` | Layer 4 后自动触发最终自查 |

## Gotchas

- **不要一次问完所有问题**。必须分层进行，每层确认完整性后再进入下一层。
- **第四层校验不可跳过**。即使前三层评分都是绿灯，也必须在输出前执行一致性校验。
- **发现严重问题时禁止自动修改**。必须列出问题清单，等待用户确认后再修正 PRD。
- **Out-of-Scope 与 In-Scope 同等重要**。很多需求蔓延源于只定义了"做什么"却没定义"不做什么"。
- **核心实体一旦定义，不可在详细 PRD 中擅自新增**。如果详细阶段发现需要新实体，必须回溯修改 PRD-000 并升版。
- **P0 需求必须可测试**。每个 P0 需求应对应至少一个用户故事的验收标准。
- **Component Inventory 不是 UI 设计稿**。它是功能模块的组件级拆解，供后续 AI 编码工具快速读取，不包含像素级设计细节。
- **模块名一旦确定，详细阶段不可改**。修改模块名会导致 `feature-XX-{模块}/` 目录重命名，影响所有下游 Skill。

## 示例

### 示例：AI 短剧生成平台概要需求

**用户输入**：
> "我们要做一个 AI 短剧生成平台，让用户能从剧本直接生成视频。"

**Layer 1 摘要**：
- 痛点：传统短剧制作周期长（2-3 个月），成本高
- 目标用户：独立制片人、MCN 机构内容团队
- 价值主张：剧本到成片时间从月级缩短到天级
- 竞品基准：Runway（AI 视频生成）、剪映（剪辑工具）

**Layer 2 摘要**：
- 模块：剧本工坊、角色工厂、分镜工作室、渲染中心、系统设置
- Out-of-Scope：视频分发、版权交易、支付系统（Phase 1）
- Component Inventory：剧本编辑器、角色形象生成器、分镜时间轴、渲染队列面板

**Layer 3 摘要**：
- 北极星指标：单项目从剧本到成片 < 48 小时
- NFR：支持 10 人同时在线编辑；1 万行 Excel 导入 < 5s
- 行业对标：渲染性能处于中档

**Layer 4（校验示例）**：
- 🔴 严重：Out-of-Scope 包含"支付系统"，但 In-Scope 未明确"用户如何付费使用高级功能"。用户补充"Phase 1 免费+申请试用"后解除。

## 变更日志

- 2026-05-06: v2.0 重构为 prd-generation。融合 abeejuice 访谈模板、johnnychauvet JTBD+Component Inventory、cdeust 多文件拆分与验证算法。输出改为 OpenSpec 五文件规范。
- 2026-04-26: v1.1 增加第四层"一致性校验与竞品对标"机制。
- 2026-04-20: v1.0 初始版本（prd-system-outline）
