# Brainstorming Skill 使用手册

> **Skill 版本**：2.2.0
> **适用阶段**：OpenSpec 阶段 1（需求探索与澄清）
> **更新日期**：2026-05-07

---

## 一、适用场景

当你遇到以下情况时，应使用 Brainstorming Skill：

- 收到新的产品需求或变更提案
- 需要从零开始规划一个功能或模块
- 对现有功能进行重大优化或重构
- 用户提出的需求模糊，需要澄清边界和规则
- 技术选型或架构调整前的需求确认

**不适用场景**：
- 纯技术预研（无业务需求背景）
- 仅修改文案、样式等无需澄清的微小变更
- 已进入编码阶段后的需求变更（应走变更流程）

---

## 二、前置条件

1. **OpenSpec 环境已初始化**：
   - `openspec/config.yaml` 存在且包含 `context` 字段
   - `openspec/changes/` 目录已创建

2. **Skill 已安装**：
   - `brainstorming` Skill  可用
   - `prd-generation` Skill 已就绪（下游衔接用）

3. **可选准备**：
   - 若需本地资料支撑，提前准备文档路径（如 `@docs/legacy/xxx.md`）
   - 若了解竞品，可准备竞品名称供搜索参考

---

## 三、快速开始

### 3.1 启动方式

**方式一：用户主动触发**

```kimi
💫 /skill:brainstorming 帮我头脑风暴下，打算做个通过剧本生成短剧的平台产品，本地资料：@docs/ref/*.md
```

**方式二：通过 /opsx:propose 触发**

```bash
/opsx:propose "为 reelforge 增加 AI 剧本分镜自动生成功能"
```

随后 Skill 自动加载并执行。

### 3.2 典型会话流程

```
你：【阶段 1 需求探索 | Skill：brainstorming】变更描述："..."

Kimi：正在收集资料...
      [网络] 搜索到 ComfyUI、Sora 等 5 条相关资料
      [本地] 已读取 @docs/legacy/剧本模块PRD.md
      
      资料收集完成。开始苏格拉底式提问。
      
      Round 1 / 用户价值
      "这个功能主要解决编剧还是导演的痛点？"
      
你：解决导演的痛点，他们需要快速看到剧本的可视化效果

Kimi：Round 2 / 边界范围
      "现有的手动绘制分镜流程是否需要保留，还是被完全替代？"
      
你：保留手动流程，AI 生成作为辅助

...（多轮提问）...

Kimi：澄清度已达 0.85。正在生成结构化需求摘要...
      已保存到 openspec/changes/ai-storyboard/brainstorming/
      
      推荐进入下游 Skill：prd-generation
      是否继续？
      
你：继续

Kimi：【阶段 2 概要需求 | Skill：prd-generation】...
```

---

## 四、分步操作指南

### Step 1: 提供变更描述

向 Kimi 提供清晰、完整的变更描述。描述应包含：
- **做什么**：功能或变更的核心内容
- **为什么做**：业务背景或用户痛点
- **给谁做**：目标用户群体

**好的示例**：
> "为 reelforge 增加 AI 剧本分镜自动生成功能。导演上传剧本后，系统自动生成关键场景的分镜草图，支持文生图和图生视频两种模式，目标是将分镜制作时间从 2 天缩短到 2 小时。"

**差的示例**：
> "加个 AI 功能"（过于模糊，缺乏背景和范围）

### Step 2: 资料收集（自动）

Skill 自动执行资料收集。你只需：
- **提供本地资料路径**（可选）：如有历史 PRD、用户反馈、技术文档，用 `@路径` 格式提供
- **补充搜索关键词**（可选）：如了解特定竞品或技术，可告知 Kimi

**本地资料示例**：
```text
本地资料：@docs/legacy/剧本模块PRD.md @docs/feedback/导演痛点_Q1.xlsx
```

### Step 3: 回答苏格拉底式提问

Kimi 会从 6 个维度逐轮提问。**每次只回答 1 个问题**。

**回答技巧**：
- 尽量具体，避免"看情况""可能"等模糊表述
- 如涉及选择，可直接选 Kimi 提供的选项
- 如不确定，明确说"不确定，需要调研"，不要猜测

### Step 4: 澄清度评估

每轮结束后，Kimi 会评估澄清度。你可以：
- 主动补充信息以提升澄清度
- 提出新的边界或约束
- 纠正 Kimi 的理解偏差

**何时可以停止**：
- 澄清度 ≥ 0.8 且你对摘要满意
- 已回答 5 轮且核心问题已明确
- 你主动要求终止并进入下游

### Step 5: 审查结构化摘要

Kimi 生成 `requirement-draft.md` 后，请你审查：
- 核心问题是否准确反映你的意图
- 边界范围是否与你理解的 IN/OUT 一致
- 风险点是否被正确识别
- 待确认项是否有遗漏

**如需修改**：直接提出，Kimi 会修正并重新执行 Self-Check。

### Step 5.5: 可选市场定位分析（Recommended）

当市场格局不确定、或需要结构化竞品输入来支撑 PRD 时，触发 `competitive-analysis` 的 `positioning` 模式：

```text
【阶段 1.5 市场定位 | Skill：competitive-analysis mode=positioning】

分析目标：{基于 requirement-draft.md 中的模块初分}
问题类型：market_entry | positioning
参考文档：@openspec/changes/{变更名}/brainstorming/requirement-draft.md
```

- 输出 `market-positioning.md` 到 `openspec/changes/{变更名}/brainstorming/`
- 若用户明确说"不做竞品分析"或"市场已经很清楚"，可跳过此步骤
- 此步骤产出将直接作为 `prd-generation` 的竞品输入，替代 AI 自行搜索的碎片化信息

### Step 6: 确认进入下游

审查通过后，明确告知 Kimi：
> "确认无误，进入 prd-generation"

Kimi 将自动衔接下游 Skill，并携带完整的 Handover Package（含 `market-positioning.md`，如已执行 Step 5.5）。

---

## 五、输出文件说明

Brainstorming 完成后，以下文件自动保存到 `openspec/changes/{变更名}/brainstorming/`：

### 5.1 brainstorming-log.md

**用途**：完整记录探索过程，用于决策追溯。

**内容**：
- 资料收集记录（网络/本地/交叉验证）
- 每轮提问、你的回答、Skill 分析
- 澄清度变化曲线
- 最终摘要与建议

**何时查阅**：
- 后续阶段发现需求矛盾时，回溯原始决策依据
- 项目复盘时，回顾需求是如何被澄清的

### 5.2 research-report.md

**用途**：资料收集报告，为架构设计和竞品分析提供输入。

**内容**：
- 网络资料摘要（含 URL、相关度）
- 本地文档摘要（含路径、引用段落）
- 交叉验证结果（冲突/一致标记）
- 关键发现总结

**何时查阅**：
- 阶段 3 概要设计时，参考技术选型和竞品差异
- 阶段 4 详细设计时，确认集成依赖

### 5.3 requirement-draft.md

**用途**：结构化需求摘要，作为 `prd-generation` 的核心输入。

**内容**：
- 核心问题、边界范围、业务假设
- 模块初分与优先级
- 风险点与待确认项
- 关键决策记录

**何时查阅**：
- `prd-generation` 生成 PRD 时，作为需求基线
- 后续变更时，对比原始意图是否偏离

### 5.4 market-positioning.md（可选，由 Step 5.5 产出）

**用途**：结构化市场定位报告，为 `prd-generation` 的 Layer 1 和 Layer 4 提供竞品输入。

**内容**：
- 竞争集合（Primary / Secondary / Non-obvious）
- JTBD 对比矩阵、Blue Ocean ERRC 分析
- 战略建议（O→I→R→C→W）、假设登记册

**何时查阅**：
- `prd-generation` Layer 1 收集竞品背景时，直接引用而非重新搜索
- `prd-generation` Layer 4 一致性校验时，作为竞品对标基准

---

## 六、常见场景示例

### 场景 1：纯网络资料探索（全新功能）

```text
【阶段 1 需求探索 | Skill：brainstorming | source_type: network】

变更描述："为 reelforge 增加 AI 剧本分镜自动生成功能"

请自动搜索网络资料，然后进行苏格拉底式提问。
```

**预期执行**：
- 自动生成关键词：`reelforge 剧本分镜 AI生成`, `AI storyboard generation open source`
- 搜索到 ComfyUI、Sora 等技术方案
- 提问："搜索到两种技术路线，我们的生成方式是文生图还是图生视频？"

### 场景 2：本地资料优先（已有 PRD 草稿）

```text
【阶段 1 需求探索 | Skill：brainstorming | source_type: local】

变更描述："优化角色工厂的表单交互"

本地资料：@docs/legacy/角色工厂PRD.md @docs/feedback/用户反馈_2026Q1.md

请读取本地文档，结合现有方案进行苏格拉底式提问。
```

**预期执行**：
- 读取 PRD 提取现有功能结构
- 读取用户反馈提取痛点
- 提问："现有 PRD 中角色创建需 7 步，用户反馈集中在步骤 4 的权限配置过于复杂，本次优化是重构权限流程还是仅简化 UI？"

### 场景 3：混合模式（默认，最常用）

```text
【阶段 1 需求探索 | Skill：brainstorming】

变更描述："设计 reelforge 的渲染中心模块"

本地资料：@docs/ai-output/概要设计_渲染中心.md
```

**预期执行**：
- 读取本地概要设计文档
- 自动搜索网络资料：`reelforge rendering pipeline`, `video rendering architecture`
- 交叉验证：本地设计采用 FFmpeg 方案，网络搜索发现 GPU 加速新方案
- 提问："本地设计采用 CPU 渲染，搜索到 GPU 加速可提升 10 倍性能，是否考虑调整技术选型？"

### 场景 4：复杂变更（意图漂移风险）

```text
变更描述："优化渲染中心性能"

（多轮后用户逐渐提到 GPU、实时预览、WebSocket 等）
```

**预期执行**：
- Kimi 检测到意图漂移：原始描述是"优化性能"，当前方向是"架构重构"
- 提示："我注意到你的回答中提到了 GPU 实时预览和 WebSocket，这在原始描述中并未涉及。请确认这是本次变更的一部分，还是意味着原始方向需要调整？"

---

## 七、常见问题与处理

### Q1: 澄清度一直达不到 0.8 怎么办？

**处理**：
- 检查是否遗漏了某个维度的回答
- 主动补充你已知但未被问到的约束
- 如确实无法澄清（如依赖第三方未定事项），允许标记风险后继续

### Q2: 资料收集发现网络与本地结论冲突怎么办？

**处理**：
- Kimi 会向你提问确认
- 默认以本地文档为准，但你可以明确选择网络方案
- 如两者可共存，说明共存场景

### Q3: 我可以跳过 Brainstorming 直接进入 prd-generation 吗？

**回答**：不建议。Brainstorming 的产出是 `prd-generation` 的核心输入，跳过会导致：
- PRD 缺乏资料支撑
- 边界不清导致范围蔓延
- 隐性规则遗漏导致后期返工

如需求确实极其简单（如修改按钮文案），可由用户明确声明"无需 brainstorming"，但需承担风险。

### Q4: 输出文件可以手动修改吗？

**回答**：可以，但建议通过 Kimi 修改。原因：
- 手动修改可能导致 `brainstorming-log.md` 与 `requirement-draft.md` 不一致
- 通过 Kimi 修改会自动更新 Self-Check 状态

### Q5: 如何复用历史 Brainstorming 结果？

**回答**：
- 历史结果保存在 `openspec/changes/{变更名}/brainstorming/`
- 新变更涉及相同模块时，在本地资料中引用历史路径：
  ```text
  本地资料：@openspec/changes/历史变更/brainstorming/requirement-draft.md
  ```

---

## 八、下游衔接操作

Brainstorming 完成后，按以下方式衔接 `prd-generation`：

```text
【阶段 2 概要需求 | Skill：prd-generation】

基于 brainstorming 结果，生成概要需求。

参考文档：
- @openspec/changes/{变更名}/brainstorming/requirement-draft.md
- @openspec/changes/{变更名}/brainstorming/research-report.md
- @openspec/changes/{变更名}/brainstorming/market-positioning.md（如有）

请按配置文件中 artifact_specs.high-level-requirements.required_sections 输出。
```

> Skill 自动识别：读取 requirement-draft.md 中的模块初分，按 required_sections 逐项生成。若存在 `market-positioning.md`，Layer 1 和 Layer 4 将直接引用其中的竞品结论，避免重复搜索。

---

## 九、红线与禁忌

| 红线 | 后果 |
|------|------|
| 在澄清度 < 0.8 时强行进入 prd-generation | 生成的 PRD 缺乏依据，后期大量返工 |
| 不提供变更描述直接要求提问 | 提问无的放矢，浪费轮次 |
| 回答问题时自相矛盾且不确认 | Self-Check 反复失败，阻塞流程 |
| 将本地资料路径写错且不纠正 | 资料收集缺失，基于不完整信息推断 |
| 跳过资料收集直接要求生成摘要 | 摘要成为无依据的猜测 |

---

## 十、附录

### A. 六维提问速查卡

| 维度 | 核心问题 | 用于澄清 |
|------|----------|----------|
| 用户价值 | 解决谁的什么问题？不做的代价？ | 需求必要性 |
| 边界范围 | 哪些不在本次范围？需兼容的历史功能？ | 范围蔓延防控 |
| 业务规则 | 并发优先级？异常回退？ | 隐性规则挖掘 |
| 数据假设 | 核心实体字段？现有数据源？ | 详细设计铺垫 |
| 竞品差异 | 与竞品相比差异化点？ | 竞争定位 |
| 集成依赖 | 对接现有模块？接口契约？ | 技术约束识别 |

### B. 澄清度自评参考

如果你不确定当前澄清度是否足够，可以对照以下清单自评：

- [ ] 我能用一句话说清楚这个功能解决什么问题
- [ ] 我能列出至少 3 个明确不做的事情
- [ ] 我知道异常情况下系统应该怎么表现
- [ ] 我能画出（或描述）核心数据实体之间的关系
- [ ] 我知道这个功能与现有系统的集成点在哪里
- [ ] 我能预估这个功能影响的模块数量

6 项全选 = 澄清度约 0.9+，可以进入下游。
4-5 项 = 澄清度约 0.7-0.8，建议再补充 1 轮。
≤3 项 = 澄清度 < 0.7，需要继续探索。
