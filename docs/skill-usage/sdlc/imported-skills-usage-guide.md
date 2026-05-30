# 新增 Skill 使用指南

> 本文档涵盖 25 个 Skill，按五大能力域分类整理。
> 
> **适用对象**：个人用户、团队协作者、AI 助手编排者。
> **阅读建议**：先根据"场景速查表"定位 Skill，再查看对应分类的详细触发方式和组合建议。

---

## 目录

1. [概述与快速开始](#概述与快速开始)
2. [场景速查表](#场景速查表)
3. [学习知识类（learning/）](#学习知识类learning)
4. [办公沟通类（office/）](#办公沟通类office)
5. [研究决策类（research/）](#研究决策类research)
6. [内容表达类（content-creation/）](#内容表达类content-creation)
7. [工程基础类（engineering-foundations/）](#工程基础类engineering-foundations)
8. [组合使用建议](#组合使用建议)
9. [触发关键词索引](#触发关键词索引)

---

## 概述与快速开始

本次新增的 25 个 Skill，保留了原始设计中的"输入 → 工作流程 → 输出格式 → 约束"结构，并针对本项目规范做了以下适配：

- **Frontmatter** 仅保留 `name` + `description`（Kimi Code 兼容）。
- **Gotchas** 升级为"行为标签 + 风险场景 + 规避方法"三段式，兼具硬性约束与经验陷阱提示。
- **元数据** 统一存放在同目录 `meta.json` 中，支持跨平台检索。

### 安装到本地 AI 工具

```bash
# 安装全部新增 skill（以 Kimi 为例）
./scripts/install.sh --tool kimi --skill skills/learning/structured-notes-generator --target .

# 批量安装某一分类
./scripts/install.sh --tool kimi --skill skills/office/meeting-notes-organizer --target .

# 验证格式
python3 scripts/validate.py --skill skills/research/deep-research-synthesizer
```

---

## 场景速查表

| 你的场景 | 推荐 Skill | 分类 |
|---------|-----------|------|
| 读完一篇文章/论文，想做结构化笔记 | `structured-notes-generator` | learning |
| 马上要考试，需要模拟题自测 | `exam-prep-generator` | learning |
| 想系统学习一门新技术，需要周计划 | `learning-roadmap-generator` | learning |
| 要给非技术同事讲清楚一个复杂概念 | `complex-concept-explainer` | learning |
| 写论文/研究报告，需要搭结构框架 | `academic-paper-drafter` | learning |
| 背单词/背概念，需要记忆卡片 | `flashcard-creator` | learning |
| 备考时间紧，需要排学习日程 | `study-session-planner` | learning |
| 需要写一封得体的商务邮件 | `professional-email-drafter` | office |
| 开完会，需要整理纪要和行动项 | `meeting-notes-organizer` | office |
| 准备求职，需要优化简历和领英 | `cv-linkedin-optimizer` | office |
| 要做汇报/路演，需要搭 PPT 结构 | `presentation-prep-skill` | office |
| 读了多份材料，需要提炼洞察 | `deep-research-synthesizer` | research |
| 看到一篇文章，不确定可信度 | `source-validation-skill` | research |
| 笔记太乱，需要整理成知识库 | `knowledge-structuring-skill` | research |
| 要做竞品分析/技术选型对比 | `competitive-intelligence-skill` | research |
| 要拍短视频，需要脚本结构 | `video-script-generator` | content-creation |
| 写文章/视频，开头总是没吸引力 | `hook-generator` | content-creation |
| 业务流程复杂，需要可视化流程图 | `flowchart-decision-builder` | content-creation |
| 写完了代码，需要补技术文档 | `code-documenter` | engineering-foundations |
| 需要为函数补单元测试 | `unit-test-generator` | engineering-foundations |
| 遇到 Bug，需要系统排查根因 | `debug-assistant` | engineering-foundations |
| 要写正则表达式，怕写错 | `regex-builder-explainer` | engineering-foundations |
| 提交代码，需要规范 commit message | `conventional-commit-generator` | engineering-foundations |
| 收到 PR，需要做代码审查 | `code-review-skill` | engineering-foundations |
| 想把一件复杂事交给 Agent 自动执行 | `workflow-automation-agent` | engineering-foundations |

---

## 学习知识类（learning/）

> 适用场景：个人学习、团队培训、知识管理、考试备考。

### 1. structured-notes-generator（结构化笔记生成器）

**触发方式**：提到"整理笔记""结构化笔记""学习总结""提炼概念"。

**典型输入**：文章、PDF、课堂笔记、视频转录稿。

**输出价值**：将零散材料转化为"总览 → 子主题 → 关键点 → 示例"四层结构，附带概念关系图和复习问题。

**使用建议**：
- 适合在**阅读后立即使用**，趁记忆新鲜时整理。
- 若材料跨多个主题，建议分主题多次调用，避免单份笔记过于庞大。

### 2. exam-prep-generator（考试准备器）

**触发方式**：提到"出题""模拟题""考试准备""复习测验"。

**典型输入**：课程大纲、教材章节、内部培训材料。

**输出价值**：按记忆/理解/应用/分析四类能力分层出题，附答案解析和难度标注。

**使用建议**：
- 企业培训场景下，可将内部制度/产品手册直接转化为小测验。
- 建议与 `flashcard-creator` 配合使用：先出模拟题定位薄弱点，再针对错题生成记忆卡片。

### 3. learning-roadmap-generator（学习路线图生成器）

**触发方式**：提到"学习路线""学习计划""能力提升""技术入门"。

**典型输入**：目标技术/领域、当前水平、每周可用时间、目标完成时间。

**输出价值**：4-12 周阶段性计划，每周含主题、资源、练习和可验证检查点。

**使用建议**：
- 高管可用此 Skill 为团队制定**岗位能力升级路径**。
- 检查点务必写成"能完成什么"（可验收任务），而非"理解什么"（主观描述）。

### 4. complex-concept-explainer（复杂概念解释器）

**触发方式**：提到"解释概念""通俗讲解""技术科普""跨部门沟通"。

**典型输入**：一个复杂概念、目标读者、期望深度。

**输出价值**：一句话解释 → 类比 → 基础版 → 中级版 → 技术版，层层递进。

**使用建议**：
- 架构师向非技术团队解释系统复杂性时，优先使用"类比 + 基础版"组合。
- 务必在文末标注**类比边界**（什么情况下类比会失效），避免误导。

### 5. academic-paper-drafter（学术论文写作器）

**触发方式**：提到"写论文""学术写作""研究报告""论文大纲"。

**典型输入**：主题、文章类型、目标字数、引用格式、已有资料。

**输出价值**：生成论文结构大纲、各章节草稿、引用占位和待补资料清单。

**使用建议**：
- **此 Skill 只负责结构和初稿**，不生成最终论文。所有引用位置必须标 `[需要引用]`，由用户自行补全。
- 商业报告和技术方案同样适用此结构方法论。

### 6. flashcard-creator（记忆卡片生成器）

**触发方式**：提到"记忆卡片""Anki""Quizlet""主动回忆"。

**典型输入**：学习材料、笔记或文档。

**输出价值**：编号化问答卡片，含标签、难度排序，支持间隔重复学习。

**使用建议**：
- 与 `structured-notes-generator` 形成闭环：先整理笔记提取概念，再拆分为卡片强化记忆。
- 每张卡片必须**独立可理解**，禁止卡片之间存在隐性依赖。

### 7. study-session-planner（学习时段规划器）

**触发方式**：提到"学习计划""备考安排""复习日程""时间规划"。

**典型输入**：科目、截止日期、每天可用时间、难度和优先级。

**输出价值**：按考试临近程度和难度排序的日程表，含间隔复习点和风险提醒。

**使用建议**：
- 本质是**资源排程 Skill**，也可用于高强度证书备考或团队培训排期。
- 每天有效学习上限 6 小时，超过后认知收益递减，模型会自动提示取舍。

---

## 办公沟通类（office/）

> 适用场景：商务沟通、会议管理、求职准备、高管汇报。

### 8. professional-email-drafter（专业邮件撰写器）

**触发方式**：提到"写邮件""发邮件""邮件草稿""客户沟通"。

**典型输入**：邮件目的、收件人关系、背景事实、期望动作、语气要求。

**输出价值**：邮件主题 + 正文 + 可选备选语气版本。

**使用建议**：
- 高风险邮件（裁员、合同终止、价格上调）会在文末附加**风险提示**，建议经法务/HR 二次确认。
- 提供"冷静版"和"坚定版"双选项，避免 AI 替用户决定情绪基调。

### 9. meeting-notes-organizer（会议纪要组织器）

**触发方式**：提到"会议纪要""会议整理""会议记录""行动项"。

**典型输入**：会议记录或转录稿、可选参会人/日期/项目名。

**输出价值**：摘要 + 已做决策 + 行动项（owner/动作/截止时间）+ 开放问题 + 风险依赖。

**使用建议**：
- **如果只允许先上一个办公 Skill，优先选这个。** 它是行动系统的入口。
- 严格区分"会上有人提议"和"会议最终决议"，避免把讨论写成决策。

### 10. cv-linkedin-optimizer（简历与领英优化器）

**触发方式**：提到"优化简历""LinkedIn""领英""求职""内部转岗"。

**典型输入**：当前简历、目标岗位 JD、真实经历、可量化成果。

**输出价值**：职业简介 + 经历改写 + 技能关键词 + 领英标题 + 能力缺口分析。

**使用建议**：
- HR 和团队管理者可**反向使用**：输入岗位 JD，检查描述是否清楚、关键词是否覆盖目标人群。
- 严禁将"参与"改写为"主导"，所有成果必须基于用户提供的真实数据。

### 11. presentation-prep-skill（演示文稿准备器）

**触发方式**：提到"做 PPT""演示文稿""汇报结构""演讲准备"。

**典型输入**：演示主题、目标听众、时长、已有材料。

**输出价值**：叙事线 + 逐页结构 + 每页关键点 + 视觉建议 + 讲者备注。

**使用建议**：
- 15-20 分钟汇报不超过 20 页，每页不超过 3-4 个要点。
- 核心是把"资料"压成"叙事"，高管汇报场景下尤其需要克制信息堆砌。

---

## 研究决策类（research/）

> 适用场景：行业研究、竞品分析、战略决策、知识库建设。

### 12. deep-research-synthesizer（深度研究合成器）

**触发方式**：提到"深度研究""行业研究""竞品调研""多源分析"。

**典型输入**：多个来源材料、研究问题、输出目标。

**输出价值**：来源分层 + 关键事实 + 主要洞察 + 分歧与风险 + 下一步建议。

**使用建议**：
- 管理决策的底层能力。输出时务必区分"事实""推测"和"作者判断"。
- 不要把单一来源的观点写成行业共识，重要结论必须标注来源编号。

### 13. source-validation-skill（来源验证器）

**触发方式**：提到"验证来源""信息可信度""交叉验证""事实核查"。

**典型输入**：链接、文章、报告或引用、需要验证的问题。

**输出价值**：来源列表 + 可信度评分（五级）+ 可确认事实 + 不确定信息 + 使用建议。

**使用建议**：
- 投研、公众号写作、企业决策中应**长期保留**此 Skill。
- 超过 2 年的数据自动标 `[需确认时效性]`，企业白皮书自动标利益相关。

### 14. knowledge-structuring-skill（知识结构化器）

**触发方式**：提到"知识整理""结构化知识""知识库""资料归档"。

**典型输入**：零散笔记、文章、会议材料或资料包。

**输出价值**：总体框架 + 分类目录 + 核心概念 + 关系说明 + 待补资料。

**使用建议**：
- 个人知识库和团队知识库的**入口 Skill**。先结构化，再沉淀到长期存储。
- 不要为了分类"美观"而合并语义不同的概念，宁可在体系中保留"待归类"桶。

### 15. competitive-intelligence-skill（竞争情报分析器）

**触发方式**：提到"竞品分析""竞争情报""市场对比""产品定位"。

**典型输入**：竞品列表、分析目标、资料来源、关注维度。

**输出价值**：对比表 + 每个竞品摘要 + 优势/弱点 + 机会点 + 风险待验证问题。

**使用建议**：
- 高管看此类输出时，最重要的是分清"已确认"和"待验证"。
- 官网功能列表与实际产品能力之间存在差距，需标注"官方声称，待验证"。

---

## 内容表达类（content-creation/）

> 适用场景：短视频脚本、文章写作、流程可视化、社交媒体。

### 16. video-script-generator（视频脚本生成器）

**触发方式**：提到"视频脚本""短视频""口播稿""内容传播"。

**典型输入**：主题、目标观众、视频时长、平台、核心观点。

**输出价值**：标题 + 开场钩子 + 分段脚本 + 画面建议 + 结尾行动。

**使用建议**：
- 抖音 15 秒和 B 站 10 分钟的叙事节奏完全不同，必须按平台时长匹配输出。
- 每段脚本至少包含一个具体信息点（数据、案例、步骤），禁止纯口号堆叠。

### 17. hook-generator（开场钩子生成器）

**触发方式**：提到"开场钩子""标题""吸引读者""开篇"。

**典型输入**：主题、目标读者、内容类型、核心观点。

**输出价值**：判断型 / 问题型 / 场景型 / 数据型钩子 + 最推荐版本。

**使用建议**：
- 钩子必须能被正文支撑。若正文尚未撰写，模型会提示"请确认正文包含以下要点，否则建议换钩子"。
- 健康、财务、教育类内容禁止制造虚假焦虑。

### 18. flowchart-decision-builder（流程图与决策树构建器）

**触发方式**：提到"流程图""决策树""Mermaid""业务流程""审批规则"。

**典型输入**：流程描述、决策条件、输出格式偏好。

**输出价值**：节点列表 + 条件分支 + Mermaid 流程图 + 异常路径。

**使用建议**：
- 架构师和业务负责人对齐流程时的**实用工具**。复杂流程超过 15 个节点时，建议拆分为子流程图。
- 禁止自行添加用户未说明的决策条件。

---

## 工程基础类（engineering-foundations/）

> 适用场景：代码文档、测试生成、调试排查、正则构建、提交规范、代码审查、工作流编排。

### 19. code-documenter（代码文档生成器）

**触发方式**：提到"生成文档""代码注释""API 文档""技术文档"。

**典型输入**：源代码、语言和框架、文档格式要求。

**输出价值**：文档注释 + 使用示例 + 参数说明 + 返回值说明 + 边界情况。

**使用建议**：
- **先读代码，不是按函数名猜**。对不确定的副作用标 `[待确认]`。
- 示例必须可运行，或明确标注为伪代码。`getUserById(id)` 不需要写"通过 ID 获取用户"，应聚焦边界和异常。

### 20. unit-test-generator（单元测试生成器）

**触发方式**：提到"写测试""单元测试""补测试""测试覆盖"。

**典型输入**：待测代码、测试框架、现有测试风格。

**输出价值**：测试文件 + 测试用例说明 + 覆盖点清单 + 未覆盖风险。

**使用建议**：
- 测行为，不测内部实现细节。禁止断言私有变量状态或函数内部调用顺序。
- 每个测试必须独立，不依赖执行顺序（测试框架可能并行运行）。

### 21. debug-assistant（调试助手）

**触发方式**：提到"调试""Bug""报错""堆栈""线上问题"。

**典型输入**：错误信息、堆栈、相关代码、运行环境。

**输出价值**：现象 + 根因候选 + 定位证据 + 修复方案 + 预防建议。

**使用建议**：
- 上下文不足时，模型会列出"需要补充以下信息"清单，而不是猜测根因。
- 多个可能原因按概率排序，优先给出**影响范围最小、改动成本最低**的方案。

### 22. regex-builder-explainer（正则表达式构建与解释器）

**触发方式**：提到"正则表达式""regex""匹配规则""提取文本"。

**典型输入**：想匹配或提取的内容、正则引擎、示例字符串。

**输出价值**：正则表达式 + 分段解释 + 匹配/不匹配示例 + 限制说明。

**使用建议**：
- 优先可读性。复杂正则建议拆分为多行注释版（Python `re.VERBOSE` 风格）。
- 必须标注适用的正则引擎（JavaScript、Python、PCRE、Go 的语法存在差异）。

### 23. conventional-commit-generator（规范化提交信息生成器）

**触发方式**：提到"提交信息""commit message""Conventional Commits""变更说明"。

**典型输入**：git diff、修改文件列表、变更目的。

**输出价值**：符合 Conventional Commits 规范的 commit message + 可选正文 + 拆分建议。

**使用建议**：
- 一个提交对应一个逻辑变更。若 diff 中同时包含 `feat` 和 `fix`，必须建议拆分。
- 提交信息是未来人和 Agent 一起理解代码历史的重要上下文资产。

### 24. code-review-skill（代码审查 Skill）

**触发方式**：提到"代码审查""PR Review""Review""走查"。

**典型输入**：代码 diff、相关文件、变更目标、测试结果。

**输出价值**：按严重程度排序的 Findings + 文件行号 + 风险说明 + 修复建议 + 测试缺口。

**使用建议**：
- **如果只给工程团队装一个 Skill，优先考虑代码审查。**
- 零问题时明确说"未发现阻塞性问题"，禁止为了"显得认真"而硬找风格问题凑数。

### 25. workflow-automation-agent（工作流自动化智能体）

**触发方式**：提到"工作流""自动化""流程编排""Agent 任务"。

**典型输入**：目标、可用工具、数据源、风险边界、期望输出。

**输出价值**：目标定义 + 步骤清单 + 工具映射 + 权限边界 + 人工确认点 + 验收标准。

**使用建议**：
- 25 个 Skill 中最像"管理入口"的一个。它不直接做某件事，而是把一件事变成可以交给 Agent 的流程。
- 涉及发送、删除、付款、生产变更时，默认设为"人工确认"，不得自动执行。

---

## 组合使用建议

### 学习闭环组合

```
structured-notes-generator → flashcard-creator → exam-prep-generator
        (整理概念)              (强化记忆)           (检验掌握)
```

### 研究决策组合

```
deep-research-synthesizer + source-validation-skill → competitive-intelligence-skill
      (多源提炼洞察)           (验证可信度)                (形成对比结论)
```

### 工程质量组合

```
code-documenter → unit-test-generator → code-review-skill → conventional-commit-generator
  (补全文档)        (生成测试)           (审查质量)            (规范提交)
```

### 会议行动组合

```
meeting-notes-organizer → professional-email-drafter
    (提取行动项)                (跟进邮件)
```

---

## 触发关键词索引

| 关键词 | 激活 Skill |
|--------|-----------|
| 整理笔记、结构化笔记、学习总结 | `structured-notes-generator` |
| 出题、模拟题、考试准备 | `exam-prep-generator` |
| 学习路线、学习计划、技术入门 | `learning-roadmap-generator` |
| 解释概念、通俗讲解、跨部门沟通 | `complex-concept-explainer` |
| 写论文、学术写作、研究报告 | `academic-paper-drafter` |
| 记忆卡片、Anki、主动回忆 | `flashcard-creator` |
| 备考安排、复习日程、时间规划 | `study-session-planner` |
| 写邮件、发邮件、客户沟通 | `professional-email-drafter` |
| 会议纪要、会议整理、行动项 | `meeting-notes-organizer` |
| 优化简历、LinkedIn、领英、求职 | `cv-linkedin-optimizer` |
| 做 PPT、演示文稿、汇报结构 | `presentation-prep-skill` |
| 深度研究、行业研究、竞品调研 | `deep-research-synthesizer` |
| 验证来源、信息可信度、交叉验证 | `source-validation-skill` |
| 知识整理、知识库、资料归档 | `knowledge-structuring-skill` |
| 竞品分析、竞争情报、市场对比 | `competitive-intelligence-skill` |
| 视频脚本、短视频、口播稿 | `video-script-generator` |
| 开场钩子、标题、吸引读者 | `hook-generator` |
| 流程图、决策树、Mermaid | `flowchart-decision-builder` |
| 生成文档、代码注释、API 文档 | `code-documenter` |
| 写测试、单元测试、测试覆盖 | `unit-test-generator` |
| 调试、Bug、报错、堆栈 | `debug-assistant` |
| 正则表达式、regex、匹配规则 | `regex-builder-explainer` |
| 提交信息、commit message | `conventional-commit-generator` |
| 代码审查、PR Review、走查 | `code-review-skill` |
| 工作流、自动化、流程编排 | `workflow-automation-agent` |
