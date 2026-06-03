# Skill Draft 使用手册

> 本手册对应 `skills/draft/` 目录下的 26 个候选 Skill，覆盖数据治理、求职运营、面试准备、简历优化、求职策略五大领域。各 Skill 目前处于 Draft 状态，待评审后可按项目规范迁移至正式分类目录。

---

## 目录

1. [概述](#概述)
2. [Skill 总览表](#skill-总览表)
3. [按领域详细说明](#按领域详细说明)
   - [数据治理](#一数据治理)
   - [求职运营](#二求职运营)
   - [面试准备](#三面试准备)
   - [简历与求职材料](#四简历与求职材料)
   - [求职策略与决策](#五求职策略与决策)
   - [辅助工具](#六辅助工具)
4. [按求职阶段的使用路线图](#按求职阶段的使用路线图)
5. [Kimi Code 兼容性说明](#kimi-code-兼容性说明)

---

## 概述

`docs-internal/interview` 目录下沉淀了多组面向求职与职业发展的 AI Skill。经梳理，共提取出 **26 个独立 Skill**，按职责可分为六大类：

- **数据治理**：企业级数据治理全生命周期管理。
- **求职运营**：从职位扫描、公司研究到申请跟踪的全流程指挥中心。
- **面试准备**：面试题生成、系统设计练习、行为面试故事库、面试复盘。
- **简历与求职材料**：ATS 优化、要点撰写、格式化、量化、定制、版本管理，以及学术/高管/创意/技术/转行等垂类简历。
- **求职策略与决策**：JD 分析、LinkedIn 优化、Offer 比较、薪资谈判、求职信生成。
- **辅助工具**：作品集案例撰写、推荐信管理。

这些 Skill 遵循统一的渐进式披露结构（`SKILL.md` + `meta.json`），Frontmatter 已按 Kimi Code 严格白名单规范精简为 `name` + `description` 两个字段。

---

## Skill 总览表

| # | Skill 名称 | 领域 | 核心功能 | 典型触发词 |
|---|-----------|------|---------|-----------|
| 1 | [data-governance](#data-governance) | 数据治理 | 数据标准、质量、血缘、MDM、安全治理 | 数据治理、血缘分析、主数据、落标检查 |
| 2 | [career-ops](#career-ops) | 求职运营 | 扫描职位、评估 JD、生成简历、跟踪申请 | 求职、找工作、申请跟踪、职位扫描 |
| 3 | [interview-prep-review](#interview-prep-review) | 面试准备 | 按轮次制定策略、逐题复盘、识别卡点模式 | 准备面试、复盘面试、分析 JD、终面策略 |
| 4 | [interview-generation](#interview-generation) | 面试准备 | 生成 4 段式 Python 编程面试题 | 生成面试题、Python 面试、编程练习 |
| 5 | [interview-requirements-prioritization-drill](#interview-requirements-prioritization-drill) | 面试准备 | 系统设计需求澄清与优先级训练 | 需求训练、跟进问题、范围界定 |
| 6 | [interview-system-design](#interview-system-design) | 面试准备 | 生成/练习/评审系统设计面试 | 系统设计面试、白板设计、架构面试 |
| 7 | [interview-prep-generator](#interview-prep-generator) | 面试准备 | 生成 STAR 故事、预测问题、准备话术 | 面试准备、STAR 故事、行为面试 |
| 8 | [job-description-analyzer](#job-description-analyzer) | 求职策略 | 解析 JD、计算匹配分、识别红旗 | 分析职位、匹配分数、是否申请 |
| 9 | [linkedin-profile-optimizer](#linkedin-profile-optimizer) | 求职策略 | 优化头像、标题、About、技能、关键词 | LinkedIn、招聘人员可见性、个人资料优化 |
| 10 | [offer-comparison-analyzer](#offer-comparison-analyzer) | 求职策略 | 多 Offer 总包对比与加权决策矩阵 | 比较 offer、多个 offer、选哪个工作 |
| 11 | [salary-negotiation-prep](#salary-negotiation-prep) | 求职策略 | 调研市场薪酬、撰写还价脚本 | 薪资谈判、还价、补偿方案 |
| 12 | [cover-letter-generator](#cover-letter-generator) | 求职策略 | 基于简历+JD 生成个性化求职信 | 求职信、申请信、cover letter |
| 13 | [resume-executive-resume-writer](#resume-executive-resume-writer) | 简历材料 | C-suite/VP 级别战略型简历 | 高管简历、C-suite、董事会 |
| 14 | [resume-tech-resume-optimizer](#resume-tech-resume-optimizer) | 简历材料 | 软件工程师/PM/技术岗简历优化 | 技术简历、开发者简历、SWE |
| 15 | [resume-academic-cv-builder](#resume-academic-cv-builder) | 简历材料 | 学术职位 CV（论文、基金、教学） | 学术 CV、教职、博士后 |
| 16 | [resume-creative-portfolio](#resume-creative-portfolio) | 简历材料 | 设计师/创意岗视觉简历与作品集 | 创意简历、设计师、视觉简历 |
| 17 | [resume-career-changer-translator](#resume-career-changer-translator) | 简历材料 | 跨行业技能翻译与可迁移经验重构 | 转行、跨行业、可迁移技能 |
| 18 | [resume-ats-optimizer](#resume-ats-optimizer) | 简历材料 | ATS 兼容性检查与关键词匹配优化 | ATS、没面试、简历没反应 |
| 19 | [resume-bullet-writer](#resume-bullet-writer) | 简历材料 | 将职责描述改写为成就导向要点 | 优化要点、量化成就、结果导向 |
| 20 | [resume-formatter](#resume-formatter) | 简历材料 | 版式、字体、间距、ATS 安全格式化 | 格式化简历、排版、布局 |
| 21 | [resume-quantifier](#resume-quantifier) | 简历材料 | 为无数据的经验寻找/估算量化指标 | 加数字、量化、没数据 |
| 22 | [resume-section-builder](#resume-section-builder) | 简历材料 | 按职业阶段构建各简历章节 | 简历章节、摘要、技能部分 |
| 23 | [resume-tailor](#resume-tailor) | 简历材料 | 针对特定 JD 定制简历（不造假） | 定制简历、针对性修改 |
| 24 | [resume-version-manager](#resume-version-manager) | 简历材料 | 主简历维护与多版本追踪管理 | 版本管理、主简历、追踪 |
| 25 | [portfolio-case-study-writer](#portfolio-case-study-writer) | 辅助工具 | 将简历要点扩展为完整项目案例 | 案例研究、作品集、项目撰写 |
| 26 | [reference-list-builder](#reference-list-builder) | 辅助工具 | 格式化推荐信列表与准备 briefing | 推荐信、推荐人、背景调查 |

---

## 按领域详细说明

### 一、数据治理

#### data-governance

**功能**：企业级数据治理全生命周期管理 Skill，覆盖六大核心域：数据标准、数据质量、元数据、数据血缘、主数据管理（MDM）、数据安全。

**使用场景**：
- 金融机构/供应链金融场景的监管合规要求对齐（银保监会数据治理指引）。
- 输出数据治理成熟度评估报告、标准规范书、血缘图谱、质量看板、MDM 架构方案。
- 支持隐私计算方案设计（联邦学习、多方安全计算）。

**工作模式**：
1. **Assess（评估）**：基于 DAMA-DMBOK + DCAM 框架的成熟度评估。
2. **Design（设计）**：数据标准与质量规则库设计，含落标检查脚本。
3. **Trace（追溯）**：字段级血缘解析与影响分析。
4. **MDM（主数据）**：黄金记录、匹配合并、分发策略。
5. **Secure（安全）**：分级分类、脱敏加密、隐私计算架构。
6. **Operate（运营）**：治理组织 RACI 与 KPI 体系。

**触发词**：数据治理、数据质量、血缘分析、主数据、元数据、数据标准、数据安全、落标检查、数据分级、隐私计算。

---

### 二、求职运营

#### career-ops

**功能**：AI 求职指挥中心，采用 Router 模式，根据输入自动路由到 15+ 子模式。

**使用场景**：
- 粘贴 JD 文本或 URL → 自动执行 `auto-pipeline`（评估 + 报告 + PDF + 跟踪）。
- 管理申请漏斗：`scan` 扫描招聘网站 → `pipeline` 处理待办 URL → `tracker` 查看状态。
- 社交破冰：`contacto` 查找联系人并起草 LinkedIn 消息。
- 批量投递：`batch` 并行处理多份申请。
- 面试后跟进：`followup` 标记逾期并生成跟进草稿。

**核心模式**：
| 模式 | 功能 |
|------|------|
| auto-pipeline | 粘贴 JD 自动评估+生成报告+PDF+跟踪 |
| scan | 扫描招聘网站发现新职位 |
| oferta | 单职位 A-F 评级评估 |
| ofertas | 多职位对比排序 |
| pdf | 生成 ATS 优化 PDF 简历 |
| interview-prep | 生成公司专属面试准备文档 |
| apply | 实时申请表单辅助填写 |
| tracker | 申请状态总览 |
| batch | 批量并行处理 |
| patterns | 分析拒信模式并优化定位 |
| followup | 跟进节奏跟踪 |

**触发词**：求职、找工作、扫描职位、评估 offer、申请跟踪、生成简历。

---

### 三、面试准备

#### interview-prep-review

**功能**：面试准备与复盘系统，解决"用同一套方法打所有轮次""面完不知道哪里出问题""反复卡在同类型问题"三大痛点。

**使用场景**：
- **准备模式**：输入 JD + 个人简历 + 面试轮次 → 输出按轮次定制的面试准备文档（含 JD 分析、轮次策略、公司研究 5 问、问题预测、作答策略）。
- **复盘模式**：输入面试记录/笔记 + 自我体感 → 输出逐题拆解复盘文档（回答 → 面试官期望 → 问题本质 → 结构化模型）+ 长期提升方向。

**核心能力**：
- 把 JD 翻译成"面试官真正想考什么"。
- 按轮次（初面/中面/终面）匹配不同策略。
- 用三段式定义法回答定义类问题；STAR+方法论提炼行为类问题。
- 识别用户反复出现的卡点模式（定义类/方法论类/压力应对/薪资谈判）。

**触发词**：准备面试、分析 JD、终面策略、刚面完、复盘面试、面试哪里出问题。

---

#### interview-generation

**功能**：生成 4 段式 Python 编程面试练习题（Part 1 核心实现 → Part 2 扩展 → Part 3 深层变体 → Part 4 讨论）。

**使用场景**：
- 需要创建新的编程面试题供自己或团队练习。
- 避免与已有题目重复（会自动扫描仓库）。
- 支持 Implementation-focused / Algorithm-leaning / Mixed 三种风格。
- 可选生成测试代码（使用 fake clock injection）。

**输出物**：单份 Markdown 文件，含背景、4 段题目、代码骨架、评估标准表。

**触发词**：生成面试题、Python 面试、创建编程练习、实现类面试题。

---

#### interview-requirements-prioritization-drill

**功能**：针对系统设计面试前 5-10 分钟的快速训练：解析模糊 prompt → 提出澄清问题 → 压缩为优先需求集合。

**使用场景**：
- 想练习系统设计的跟进问题（follow-up questions）。
- 想提高需求范围界定（scoping）能力。
- 在正式系统设计前的快速热身（reps-based）。

**训练流程**：
1. 生成模糊但现实的设计 prompt（1-3 句话）。
2. 用户驱动提出澄清问题。
3. AI 以面试官角色回答（简洁、一致、不过度指定）。
4. 用户提交功能+非功能需求列表。
5. AI 反馈：What was strong / What to tighten / Suggested improved set / Ideal follow-up questions。
6. 可立即开始下一轮。

**触发词**：练习跟进问题、需求训练、范围界定、快速 drill、系统设计热身。

---

#### interview-system-design

**功能**：系统设计面试的生成、互动练习、评审三合一 Skill。

**使用场景**：
- **生成模式**：创建新的系统设计面试题（`sd_{name}_interview.md` + `sd_{name}_solution.md`），参考 hellointerview.com 并避免重复主题。
- **面试模式**：作为面试官角色互动，回答澄清问题，不 dump 答案，按公司风格（FAANG / 初创 / 基础设施）调整语气。
- **评审模式**：读取用户填写的解答区和 Excalidraw 白板，对照参考答案给出评分卡（Problem Navigation / Solution Design / Technical Excellence / Communication）与可执行建议。

**输出物**：面试题 prompt 文件、参考答案文件、评分反馈报告。

**触发词**：系统设计面试、生成系统面试、练习系统设计、评审白板设计、架构面试。

---

#### interview-prep-generator

**功能**：从简历生成 STAR 故事库、预测面试问题、准备话术与提问清单。

**使用场景**：
- 拿到面试通知后，需要快速生成角色专属的问答准备材料。
- 将简历要点转化为可讲述的 STAR 故事（Situation → Task → Action → Result）。
- 准备"告诉我一次你..."类行为面试问题。
- 生成针对不同面试官（Hiring Manager / 团队成员 / 高管）的提问清单。

**核心框架**：
- 角色分析 → 故事库（领导/问题解决/协作/成就/失败成长各 1-2 个）→ 模拟准备 → 问题清单。
- 每个故事提供完整版（2 分钟）、简短版（60 秒）、一句话版（15 秒）。

**触发词**：面试准备、STAR 故事、行为面试、预测问题、准备话术。

---

### 四、简历与求职材料

#### resume-executive-resume-writer

**功能**：为 C-suite、VP、总监级别撰写强调战略领导力的简历。

**使用场景**：
- 申请高管岗位（CEO、CFO、COO、VP）。
- 需要展示 P&L 责任、组织变革、并购整合、董事会经验。
- 简历长度可接受 2-3 页，重点讲"so what"而非"what"。

**核心差异**：
| 普通简历 | 高管简历 |
|---------|---------|
| 列技能 | 展示领导力品牌 |
| 展示任务 | 展示战略影响 |
| 聚焦"做了什么" | 聚焦"带来了什么改变" |
| 1-2 页 | 2-3 页 |

**结构**：Executive Profile → Core Competencies → Career Highlights → Professional Experience → Board & Advisory → Education。

**触发词**：高管简历、C-suite、VP 简历、董事会、高管求职。

---

#### resume-tech-resume-optimizer

**功能**：针对软件工程师、技术 PM、数据工程师、DevOps 的简历优化。

**使用场景**：
- 技术岗求职，需要在简历中平衡技术深度与业务影响。
- 优化技术技能章节（按语言/框架/数据库/云/工具分类）。
- 突出规模指标（DAU、QPS、数据量、延迟、成本节省）。
- 补充 Projects 章节（对初级/转行者尤其重要）。

**技术要点公式**：`[动词] + [技术动作] + [规模/影响] + [使用的技术]`

**触发词**：技术简历、开发者简历、SWE 简历、工程师简历、GitHub 优化。

---

#### resume-academic-cv-builder

**功能**：为学术职位（教职、博士后、研究岗）构建 Curriculum Vitae。

**使用场景**：
- 申请 tenure-track、讲师、研究科学家岗位。
- 需要格式化出版物（按学科规范）、基金、教学经历、指导学生、学术服务。
- CV 长度随职业阶段增长（研究生 2-4 页 → 资深教授 15-30+ 页）。

**标准章节**：Contact → Education → Academic Positions → Publications → Presentations → Grants → Teaching → Mentoring → Service → Memberships → Honors。

**触发词**：学术 CV、curriculum vitae、教职申请、教授简历、研究 CV。

---

#### resume-creative-portfolio

**功能**：为设计、营销、写作等创意岗位平衡视觉设计与 ATS 兼容性。

**使用场景**：
- 创意岗位求职，简历本身即是设计作品。
- 需要同时维护两个版本：ATS 兼容版（在线申请）+ 视觉设计版（作品集/直投/面试）。
- 整合作品集链接与案例研究直达链接。

**双版本策略**：
- **ATS 版**：单栏、无图、标准字体、关键词完整。
- **设计版**：可双栏、可配色、可图标、体现品牌一致性。

**触发词**：创意简历、设计师简历、作品集简历、视觉简历、营销简历。

---

#### resume-career-changer-translator

**功能**：跨行业技能翻译，将原行业经验重构为目标行业语言。

**使用场景**：
- 教师 → 企业培训/L&D
- 军人 → 企业管理
- 零售 → 销售/客户管理
- 医疗 → 科技/医药
-  hospitality → 客户成功

**核心方法**：
- 识别通用可迁移技能（领导力、沟通、分析、运营）。
- 建立术语翻译表（如"lesson plans" → "training curriculum"）。
- 使用功能/混合简历格式，按技能分组而非按时间排序。
- 构建"桥梁经验"（志愿、自由职业、认证、副业项目）。

**触发词**：转行、跨行业、可迁移技能、职业转换、 pivot。

---

#### resume-ats-optimizer

**功能**：检查简历是否可通过 Applicant Tracking Systems（ATS）解析，并优化关键词匹配。

**使用场景**：
- 在线投递后没有回音，怀疑被 ATS 过滤。
- 需要确保文件格式、字体、章节标题、关键词密度符合 ATS 要求。
- 计算简历与 JD 的关键词匹配分（目标 80%+）。

**检查维度**：
- 文件格式（.docx / 文本型 .pdf）
- 排版（无表格/多栏/文本框/页眉页脚/图片）
- 章节标题标准化
- 关键词提取与 placement 策略（摘要 → 技能 → 经验）

**触发词**：ATS、简历没反应、关键词优化、自动筛选、解析失败。

---

#### resume-bullet-writer

**功能**：将 weak、被动、无数据的职责描述改写为成就导向的要点。

**使用场景**：
- 简历要点全是"Responsible for...""Helped with..."，需要全面改写。
- 应用 X-Y-Z 公式（Google 方法）："通过 [Z] 实现了 [X]，衡量标准为 [Y]"。
- 或应用 STAR/CAR 方法压缩故事为 1-2 行要点。

**行业示例覆盖**：软件工程、产品管理、销售、营销、客户成功、数据分析、运营/项目管理。

**触发词**：优化要点、量化成就、改进简历、结果导向、动词强化。

---

#### resume-formatter

**功能**：确保简历在 ATS 兼容的前提下具有最佳可读性与视觉层次。

**使用场景**：
- 简历排版混乱、字体不统一、间距不一致。
- 需要决定页边距、字体、字号、行距、章节顺序。
- 处理多职位同公司、短期任职、合同工等特殊版式。

**核心规则**：
- 单栏、标准字体（Arial/Calibri/Georgia/Times）、10-12pt 正文。
- 标准章节标题（Professional Experience / Education / Skills）。
- 联系信息放正文（不在页眉）。
- 保存为 .docx 或文本型 .pdf。

**触发词**：格式化简历、排版、布局、简历设计、清理格式。

---

#### resume-quantifier

**功能**：为"没有数据"的经验寻找隐藏指标或提供保守估算策略。

**使用场景**：
- 用户说"我的工作没法量化"。
- 需要为每条要点至少添加一个数字。
- 不知道具体数字时，使用范围估计、最小边界、时间反推等方法。

**六大量化维度**：金钱、时间、百分比、规模/体量、质量、频率。

**常见"没数字"场景的解决方案**：
- "我只是团队一员" → 量化你的具体贡献比例。
- "我没权限看业务数据" → 量化活动量与输入。
- "结果是保密的" → 使用百分比或范围。
- "我是初级岗位" → 量化处理量、准确率、学习速度。

**触发词**：加数字、量化、没数据、估算指标、简历数字。

---

#### resume-section-builder

**功能**：针对不同职业阶段和角色类型，构建/优化简历的各个章节。

**使用场景**：
- 不知道 Professional Summary 该不该写、怎么写。
- 技能章节不知如何组织（简单列表 / 分类 / 熟练度）。
- 经验章节该写几条要点、如何按职业阶段调整。
- 教育章节对于应届生/中层/高管分别该放什么。
- 需要额外章节（Projects / Volunteer / Languages / Awards）的决策建议。

**按角色推荐的章节顺序**：标准版 / 技术岗（技能优先）/ 应届生（教育优先）/ 高管（职业亮点优先）/ 转行（摘要+可迁移技能优先）。

**触发词**：简历章节、摘要部分、技能部分、经验部分、教育部分。

---

#### resume-tailor

**功能**：在保持真实性的前提下，针对特定 JD 调整简历的侧重点。

**使用场景**：
- 有一份"万能简历"，想为心仪公司深度定制。
- 需要调整专业摘要措辞、技能排序、经验要点优先级。
- 处理"最相关经验不在最近"的情况（可调整展示顺序）。

**核心原则**：不是造假，而是 Highlight 最相关的真实经历。

**调整范围**：
- 摘要：重写以镜像 JD 关键词。
- 技能：重排顺序，补充缺失关键词。
- 经验：调整要点顺序，融入 JD 术语。
- 教育：突出相关课程/认证。

**触发词**：定制简历、针对性修改、为某职位调整、目标岗位简历。

---

#### resume-version-manager

**功能**：管理多份简历版本，维护单一"主简历"作为真相源。

**使用场景**：
- 投了几十家公司，忘记发给 A 公司的是哪个版本。
- 需要建立文件夹结构、命名规范、申请追踪表。
- 主简历更新后，如何同步到各分类版本。

**推荐文件夹结构**：
```
Resume/
├── Master/
├── Tailored/
│   ├── ProductManagement/
│   ├── Engineering/
│   └── General/
├── CoverLetters/
└── Applications/ (tracker)
```

**命名规范**：`LastName_Role_Company_Date.pdf`

**触发词**：版本管理、主简历、追踪版本、不同简历、文件命名。

---

### 五、求职策略与决策

#### job-description-analyzer

**功能**：深度解析职位描述，计算匹配分数，识别红旗，输出申请策略。

**使用场景**：
- 看到一份 JD，不确定自己是否应该申请。
- 想快速了解"硬性要求 vs 加分项"。
- 需要一份定制简历的先行分析（应与 resume-tailor 配合使用）。

**输出物**：
- 整体匹配分（90-100% 过qualified / 75-89% 强匹配 / 60-74% 可尝试 / <50% 不建议）。
- 硬性技能、加分技能、软技能逐项对比。
- 红旗检测（"多面手""快节奏"" competitive salary" 等）。
- 简历定制策略 + 求职信话术建议 + 申请时间线。

**触发词**：分析职位、匹配分数、是否申请、JD 解析、职位要求。

---

#### linkedin-profile-optimizer

**功能**：优化 LinkedIn 个人资料，提高在招聘人员搜索中的可见度与互动率。

**使用场景**：
- 希望吸引主动邀约（inbound opportunities）。
- 同步简历与 LinkedIn，但利用平台差异（LinkedIn 可更长、更口语化、关键词更宽泛）。
- 配置 Open to Work、关键词布局、内容发布策略。

**优化维度**：头像、背景横幅、标题（220 字符）、About（首 300 字符最关键）、经验、技能（50 个全填满）、Featured、推荐信。

**触发词**：LinkedIn、招聘人员、个人资料优化、LinkedIn 标题、Open to Work。

---

#### offer-comparison-analyzer

**功能**：并排比较多个工作 offer，计算总包并引入非货币因素加权评分。

**使用场景**：
- 手握多个 offer，难以横向比较（base 不同、股权结构不同、福利不同）。
- 需要把"感觉"转化为数据：职业成长、工作生活平衡、团队文化、风险。
- 识别 offer 中的红旗（vague bonus、无流动性路径的股权、过长的 cliff）。

**总包计算维度**：现金（base + sign-on + bonus）、股权（RSU/Options 年化）、福利（401k match + 保险）、额外福利（假期远程办公 = 折算现金价值）。

**加权决策矩阵**：自定义权重（如薪酬 25%、成长 25%、工作生活 20%、文化 20%、通勤 10%）→ 按 1-10 分评分 → 计算加权总分。

**触发词**：比较 offer、多个 offer、选哪个工作、总包分析、决策矩阵。

---

#### salary-negotiation-prep

**功能**：调研市场薪酬、制定谈判策略、生成还价邮件/电话脚本。

**使用场景**：
- 收到 offer 后不知道要多少、怎么开口。
- 需要基于 Levels.fyi / Glassdoor / Blind 等来源建立市场分位范围。
- 处理常见谈判场景：first offer 偏低、对方不肯动 base、有 competing offer、被问当前薪资。

**核心原则**：84% 的雇主期望候选人谈判；不谈判一生可能少赚 $500K-$1M。

**谈判维度**：base、signing bonus、annual bonus、equity、benefits、PTO、remote、title、start date。

**触发词**：薪资谈判、还价、counter offer、补偿谈判、市场薪酬。

---

#### cover-letter-generator

**功能**：基于简历 + JD 生成个性化、有 hook 的求职信。

**使用场景**：
- 申请需要求职信的公司。
- 想展示对公司的具体研究（产品发布、新闻、文化）。
- 需要通过求职信解释职业转换或资质缺口。

**结构**：
- Opening Hook（5 秒内抓住注意力）：公司知识 / 共同联系人 / 解决对方痛点 / 亮眼成就 / 行业洞察。
- Body 1：最强匹配经验 → 对方核心需求。
- Body 2：额外价值 + 主动处理潜在担忧。
- Closing：具体贡献 + 明确行动号召。

**触发词**：求职信、cover letter、申请信、求职信模板。

---

### 六、辅助工具

#### portfolio-case-study-writer

**功能**：将简历要点扩展为结构化的作品集案例研究。

**使用场景**：
- 产品经理、UX 设计师、营销人员需要 portfolio case studies。
- 简历只展示了 WHAT，案例研究需要展示 HOW 和 WHY。

**标准结构**：Overview → Problem → Process（Research / Ideation / Decisions）→ Solution → Results（Before/After 数据表）→ Learnings。

**按角色调整侧重点**：PM 侧重策略与指标；UX 侧重用户研究与可用性；工程师侧重架构与性能；营销侧重渠道与 ROI。

**触发词**：案例研究、作品集、项目撰写、work samples、portfolio piece。

---

#### reference-list-builder

**功能**：格式化专业推荐信列表，并准备推荐人 briefing 材料。

**使用场景**：
- 终面后被要求提供推荐信。
- 不知道选谁、如何措辞、如何 briefing。
- 处理特殊情况：现任雇主不知道、前上司已离职、与前上司关系不佳、工作经验有限。

**核心流程**：
1. 选择 3-5 位推荐人（最近直属上司最有价值）。
2. 征得同意并提供职位信息。
3. 发送 briefing 包（简历 + JD + 希望他们强调的关键点 + 合作项目清单）。
4. 跟进感谢。

**触发词**：推荐信、推荐人、背景调查、reference check、reference list。

---

## 按求职阶段的使用路线图

```
┌─────────────────────────────────────────────────────────────────────┐
│ 阶段 1：自我定位与材料准备                                            │
├─────────────────────────────────────────────────────────────────────┤
│ • resume-version-manager → 建立主简历与文件夹结构                     │
│ • resume-section-builder → 搭建各章节框架                             │
│ • resume-bullet-writer   → 将职责改写成成就要点                       │
│ • resume-quantifier      → 为每条要点添加数字                         │
│ • resume-formatter       → 确保 ATS 安全且美观                        │
│ • resume-executive-resume-writer / resume-tech-resume-optimizer / academic-cv-    │
│   builder / resume-creative-portfolio / resume-career-changer-translator    │
│   → 按身份选择垂类优化                                               │
│ • linkedin-profile-optimizer → 同步优化在线形象                       │
│ • portfolio-case-study-writer → 准备作品集案例                        │
└─────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│ 阶段 2：职位发现与筛选                                                │
├─────────────────────────────────────────────────────────────────────┤
│ • career-ops scan          → 扫描招聘网站发现新职位                   │
│ • job-description-analyzer → 解析 JD、计算匹配分、识别红旗            │
│ • resume-tailor            → 针对高匹配职位定制简历                   │
│ • resume-ats-optimizer     → 确保定制版通过 ATS 筛选                  │
└─────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│ 阶段 3：投递与跟踪                                                    │
├─────────────────────────────────────────────────────────────────────┤
│ • cover-letter-generator   → 为心仪公司写求职信                       │
│ • career-ops apply / batch → 单个或批量辅助填写申请表                 │
│ • career-ops tracker       → 记录投递状态与跟进时间                   │
│ • reference-list-builder   → 提前准备好推荐人名单                     │
└─────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│ 阶段 4：面试准备                                                      │
├─────────────────────────────────────────────────────────────────────┤
│ • interview-prep-review    → 按轮次策略 + 公司研究准备                │
│ • interview-prep-generator → 生成 STAR 故事库与预测问题               │
│ • interview-system-design  → 生成/练习/评审系统设计                   │
│ • interview-requirements-prioritization-drill → 需求澄清训练                   │
│ • interview-generation     → 生成 Python 编程练习题                   │
│ • career-ops interview-prep → 公司专属面试准备文档                    │
└─────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│ 阶段 5：复盘与决策                                                    │
├─────────────────────────────────────────────────────────────────────┤
│ • interview-prep-review    → 逐题复盘，识别卡点模式                   │
│ • offer-comparison-analyzer → 多 Offer 总包与非货币因素对比           │
│ • salary-negotiation-prep  → 调研市场薪酬，准备还价                   │
│ • career-ops followup      → 跟进未回复的申请                         │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Kimi Code 兼容性说明

- 所有 Draft Skill 的 `SKILL.md` Frontmatter **仅包含 `name` 和 `description`**，符合 Kimi Code CLI 严格白名单要求。
- 扩展元数据（`version`、`pattern`、`tags`、`platforms`）已迁移至同目录的 `meta.json`。
- 若需安装到 Kimi Code CLI，可直接复制 `skills/draft/<skill-name>/` 到 `~/.kimi/skills/` 或项目级 `.kimi/skills/`。
- 若需迁移为正式 Skill，建议按领域归入：
  - `data-governance` → `skills/data-engineering/data-governance/`
  - `career-ops` → `skills/office/career-ops/`
  - 面试/简历类 → `skills/office/` 或 `skills/learning/`

---

*本手册最后更新：2026-06-02*
