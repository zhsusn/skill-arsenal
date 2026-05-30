---
name: competitive-analysis
description: 当用户要求'竞品分析'、'对比开源项目'、'技术选型调研'或'竞争对手研究'时触发。支持 mode=positioning（市场定位，服务需求阶段）与 mode=technical（技术深度对比，服务设计阶段）两种模式。
---

# Competitive Analysis

## 适用场景
- 进入新市场或评估竞争格局（`positioning` 模式）
- 概要设计前的技术选型调研（`technical` 模式）
- 开源项目对比与方案评估（`technical` 模式）
- 响应竞争对手重大动作前的结构分析（两种模式均可）

## 触发时机

| 模式 | 阶段定位 | 上游依赖 | 下游消费者 |
|------|---------|---------|-----------|
| `positioning` | 阶段 1.5（Brainstorming 之后、PRD 之前） | `brainstorming` 已产出需求草案 | `prd-generation` |
| `technical` | 阶段 3（概要设计前，与 `high-level-design` 并行或前置） | `prd-generation` 已冻结功能范围 | `high-level-design` |

> 若用户未显式指定 `mode`，默认按 `technical` 执行。

## 输入要求
- **mode**：`positioning` | `technical`（默认 `technical`）
- **分析目标**：市场领域或功能模块（如"AI 角色工厂"）
- **已知竞品**：可选，如 Midjourney、ComfyUI、D-ID
- **参考文档**：
  - `positioning`：`@openspec/changes/{变更名}/brainstorming/requirement-draft.md`
  - `technical`：`@openspec/changes/{变更名}/high-level-requirements/00-requirements-overview.md`
- **问题类型**：`market_entry` / `competitive_response` / `moat_assessment` / `positioning` / `build_buy_partner`

## 执行流程（按 mode 分支）

### Mode = positioning（市场定位模式）

目标：在需求冻结前回答"我们该不该做、做什么能差异化"。禁止深入技术架构细节。

**Round 1：情报发现**
- 执行 3-5 次 `web_search`，获取竞品概览、官方文档、关键术语
- 识别直接竞品（Primary 3-5）、相邻扩展（Secondary 3-6）、范式威胁（Non-obvious 2-3）
- 必须包含"现状维持"和"手动流程"等隐性替代方案

**Round 2：需求映射**
- 将竞品功能映射到 JTBD（Jobs-to-be-Done）框架："When [场景], I want to [动机], so I can [结果]"
- 对比各竞品满足的用户任务清单，识别未被满足的作业

**Round 3：战略分析**
- 应用战略框架（见下节"战略框架速查"）
- 重点输出：Blue Ocean ERRC 差异化空间、颠覆向量（H1/H2/H3）
- 每个结论标注证据层级 (T1-T6) 和置信度 H/M/L

**Round 4：结论提炼**
- 生成 `market-positioning.md`（结构化表格为主）
- 内容：竞争集合、JTBD 对比矩阵、Blue Ocean 分析、战略建议、假设登记册、对抗性自我批判
- **禁止输出**：数据模型 ER 图、Wardley Map、API 协议细节、`design-input.md`

### Mode = technical（技术深度模式）

目标：在概要设计前回答"别人怎么做的、我们技术怎么选"。保持现有深度。

**Round 1：情报发现**
- 执行 3-5 次 `web_search`，获取竞品概览、官方文档、关键术语
- 识别直接竞品（Primary 3-5）、相邻扩展（Secondary 3-6）、范式威胁（Non-obvious 2-3）

**Round 2：深度调研**
- 执行 5-10 次 `web_search` + `web_fetch`
- 提取技术架构细节、数据模型、功能流程、关键事件时间线
- 对 GitHub 开源项目，优先分析仓库结构、技术栈、提交历史

**Round 3：结构化分析**
- 应用战略框架（见下节）
- 按四维模型（数据模型、功能流程、技术选型、集成方式）填充实证数据
- 生成对比表格与 Mermaid 图表

**Round 4：结论提炼与设计输入**
- 生成 `competitive-analysis.md`（完整报告）
- 生成 `design-input.md`（供 `high-level-design` 直接消费的技术选型约束、架构模式、接口设计、数据模型参考）

## 分析维度

### 全模式通用维度
1. **竞争集合**：Primary / Secondary / Non-obvious 三层分类
2. **战略框架**：根据 `question_type` 选择 3-4 个主框架（见下节）
3. **证据与置信度**：所有结论必须标注 (T1-T6) 和 H/M/L（见下节）

### technical 模式专用维度（四维模型）

#### 1. 角色数据模型设计
对比各竞品的核心实体定义、字段规范、实体关系、权限模型、数据流转。

#### 2. 核心功能流程
对比主链路流程、状态机、关键交互节点、异常处理、多角色协作流。

#### 3. 技术选型
对比前端/后端/数据库/基础设施/AI 模型/部署架构，使用 Wardley Map 定位演进阶段。

**核心组件选型评分表（V2.2 新增）**：
对关键基础设施组件（如缓存 Redis vs Memcached、数据库 PostgreSQL vs MySQL、消息队列 Kafka vs RabbitMQ、向量数据库 Pinecone vs Milvus 等），输出结构化评分表：

| 组件类别 | 候选方案 | 扩展性 | 成本 | 团队熟悉度 | 生态成熟度 | 与本项目契合度 | 推荐决策 |
|---------|---------|--------|------|-----------|-----------|--------------|---------|
| [如缓存] | Redis | [1-5] | [1-5] | [1-5] | [1-5] | [1-5] | ★ 推荐 |
| [如缓存] | Memcached | [1-5] | [1-5] | [1-5] | [1-5] | [1-5] | 备选 |

- 评分维度：扩展性 25%、成本 20%、团队熟悉度 20%、生态成熟度 20%、与本项目契合度 15%
- 每个评分必须标注证据来源（`(TX)` 层级）和置信度（H/M/L）
- 推荐决策必须给出明确理由，禁止"因为流行所以选"

#### 4. 集成方式
对比 API 风格（REST/gRPC/GraphQL）、协议、扩展机制、插件生态、第三方集成深度。

## 证据与置信度规范

所有结论必须标注证据层级与置信度：

| 层级 | 类型 | 示例 |
|------|------|------|
| T1 | 直接行为数据 | 官方文档、GitHub 数据、SEC 财报 |
| T2 | 一手研究 | 结构化访谈、采样调研 |
| T3 | 专家分析 | Stratechery、a16z、学术论文 |
| T4 | 行业报告 | Gartner、IDC、Forrester |
| T5 | 高管声明 | 新闻发布会、PR 稿 |
| T6 | 推测 | 社交媒体、博客、第一性原理推理 |

| 置信度 | 标准 |
|--------|------|
| H (>70%) | 多源交叉验证，可据以行动 |
| M (40-70%) | 方向可能，但证据混合，需验证 |
| L (<40%) | 假设，勿直接行动 |

> 规则：每个表格单元格、每个关键声明必须有 `(TX)` 标注。超过 6 个月的来源标记 `[POTENTIALLY STALE]`。

## 战略框架速查

根据 `question_type` 选择 3-4 个主框架，其余跳过并标注原因：

| 框架 | 应用场景 | 输出位置 |
|------|----------|----------|
| 7 Powers | 评估技术护城河（规模经济、网络效应、品牌、资源独占） | 7 Powers 热图（technical 模式） |
| Aggregation Theory | 判断竞品是否通过平台化 commoditize 本领域 | 集成方式分析（technical 模式） |
| JTBD | 从"用户雇佣产品完成什么任务"角度对比功能与数据模型 | 功能流程与数据模型（两种模式均适用） |
| Wardley Mapping | 定位技术组件演进阶段（Genesis→Custom→Product→Commodity） | 技术选型（technical 模式） |
| Christensen 颠覆理论 | 识别低端/新市场颠覆向量，判断市场是否过度服务 | 威胁景观（两种模式均适用） |
| Blue Ocean | 检查是否所有竞品在同一维度竞争，寻找差异化空间 | 战略建议（positioning 模式重点） |

## 输出格式

### positioning 模式产出：`market-positioning.md`

必须包含以下章节：
1. **竞争集合**（Primary / Secondary / Non-obvious）
2. **JTBD 对比矩阵**（竞品 × 用户任务，标注满足度）
3. **Blue Ocean ERRC 分析**（剔除-减少-提升-创造四象限）
4. **颠覆向量与威胁景观**（H1/H2/H3 三视野）
5. **战略建议**（O→I→R→C→W 级联格式）
6. **假设登记册**（假设、支撑框架、置信度、推翻条件）
7. **对抗性自我批判**（≥3 个真实弱点）
8. **来源**（按证据层级分类，带日期）

> 格式要求：结构化表格为主，避免长段落，确保 `prd-generation` 能直接提取约束。

### technical 模式产出

#### 主报告：`competitive-analysis.md`
必须包含以下章节：
1. **竞争集合**（Primary / Secondary / Non-obvious）
2. **角色数据模型设计对比**（实体对比表 + ER 图）
3. **核心功能流程对比**（Mermaid 流程图 + 功能矩阵）
4. **技术选型对比**（技术栈对比表 + Wardley Map）
5. **集成方式对比**（API 对比表 + 生态矩阵）
6. **7 Powers 热图**（🟢🟡🔴 评分 + T1-T6 证据）
7. **切换成本分解**（7 类成本 1-10 分 + 进度条）
8. **颠覆向量与威胁景观**（H1/H2/H3 三视野）
9. **战略建议**（O→I→R→C→W 级联格式）
10. **假设登记册**（假设、支撑框架、置信度、推翻条件）
11. **对抗性自我批判**（≥3 个真实弱点）
12. **来源**（按证据层级分类，带日期）

#### 设计输入：`design-input.md`
专供 `high-level-design` Skill 消费，结构化提取：
- **技术选型约束**：组件、竞品主流方案、推荐方案、理由、置信度
- **核心组件选型评分表**：类别、候选方案、五维评分、加权总分、推荐决策、理由
- **架构模式参考**：模式、来源竞品、适用性、风险
- **接口设计约束**：API 风格、协议、标准建议
- **数据模型参考**：实体、竞品设计、本方案决策
- **差异化空间**（Blue Ocean ERRC）
- **风险提示**：风险、来源、观测指标

## 下游联动

| 模式 | 下游 Skill | 衔接规则 |
|------|-----------|---------|
| `positioning` | `prd-generation` | `market-positioning.md` 作为 Layer 1 和 Layer 4 的竞品输入 |
| `technical` | `high-level-design` | 与 `high-level-design` 并行或前置执行；`high-level-design` 启动时自动引用 `design-input.md` |

两种模式完成后均触发 `progress-tracker` 更新阶段状态。

## Gotchas

- **禁止无证据声明**：每个关键结论必须有 `(TX)` 标注。若证据不足，标记 `[EVIDENCE-LIMITED]` 而非编造。
- **避免功能对比陷阱**：不要只罗列功能矩阵。必须先做结构分析（7 Powers、护城河、JTBD），再补功能矩阵。
- **时间敏感性**：超过 6 个月的来源必须标记 `[POTENTIALLY STALE]`，不可仅凭旧数据做行动建议。
- **框架选择而非堆砌**：根据 `question_type` 选 3-4 个主框架，禁止为了显得专业而堆砌所有框架。
- **跨框架矛盾是信号**：当两个框架结论冲突，必须显式呈现矛盾并说明权重。
- **竞品营销≠证据**：竞品的 PR 稿、发布会声明最多为 T5，不可当作事实直接引用。
- **不要忽略"不做任何事"**：竞争集合必须包含"现状维持"和"手动流程"等隐性替代方案。
- **设计输入可消费性**：`design-input.md` 和 `market-positioning.md` 必须使用结构化表格，避免长段落。
- **搜索轮次控制**：若网络信息已充足，不必强行完成 4 轮。情报质量 > 搜索次数。
- **mode 不可混淆**：`positioning` 模式禁止输出技术架构深度内容（如 Wardley Map、ER 图、API 协议细节），避免给需求阶段造成技术预设。
