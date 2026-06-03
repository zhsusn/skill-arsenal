# Job-Hunting 分类 Skill 使用手册

> 生成日期：2026-06-02  |  总 Skill 数：23

本文档面向 AI 编程助手和使用者，说明 `skills/job-hunting/` 目录下所有 Skill 的触发场景、核心能力、输入要求和典型使用流程。

## 目录

- [简历](#简历)
  - [resume-academic-cv-builder](#resumeacademiccvbuilder)
  - [resume-ats-formatter](#resumeatsformatter)
  - [resume-bullet-writer](#resumebulletwriter)
  - [resume-career-changer-translator](#resumecareerchangertranslator)
  - [resume-creative-portfolio](#resumecreativeportfolio)
  - [resume-executive-resume-writer](#resumeexecutiveresumewriter)
  - [resume-jd-optimizer](#resumejdoptimizer)
  - [resume-section-builder](#resumesectionbuilder)
  - [resume-tech-resume-optimizer](#resumetechresumeoptimizer)
  - [resume-version-manager](#resumeversionmanager)
- [面试](#面试)
  - [interview-data-governance](#interviewdatagovernance)
  - [interview-generation](#interviewgeneration)
  - [interview-prep](#interviewprep)
  - [interview-requirements-prioritization-drill](#interviewrequirementsprioritizationdrill)
  - [interview-system-design](#interviewsystemdesign)
- [求职材料](#求职材料)
  - [cover-letter-generator](#coverlettergenerator)
  - [portfolio-case-study-writer](#portfoliocasestudywriter)
  - [reference-list-builder](#referencelistbuilder)
- [平台/联动](#平台联动)
  - [linkedin-profile-optimizer](#linkedinprofileoptimizer)
  - [resume-linkedin-optimizer](#resumelinkedinoptimizer)
- [Offer/谈判](#Offer谈判)
  - [offer-negotiation](#offernegotiation)
- [工具](#工具)
  - [jd-scraper](#jdscraper)
- [调度器](#调度器)
  - [career-ops](#careerops)

---

## 求职全生命周期使用流程

```
阶段1：简历准备
  ├─ resume-section-builder → 构建简历结构
  ├─ resume-bullet-writer → 精修每条经历
  ├─ resume-ats-formatter → 检查ATS兼容性
  ├─ resume-tech-resume-optimizer / resume-executive-resume-writer / resume-academic-cv-builder → 按场景专项优化
  └─ resume-version-manager → 维护多版本

阶段2：平台联动
  ├─ linkedin-profile-optimizer → 优化LinkedIn
  └─ resume-linkedin-optimizer → 确保简历与领英一致性

阶段3：投递策略
  ├─ resume-jd-optimizer → 分析JD + 定向定制简历
  ├─ cover-letter-generator → 生成求职信
  └─ jd-scraper → 批量抓取JD

阶段4：面试准备
  ├─ interview-prep → 按轮次准备 + 复盘
  ├─ interview-system-design / interview-data-governance → 技术/领域专项面试
  └─ interview-requirements-prioritization-drill → PM专项演练

阶段5：Offer谈判
  └─ offer-negotiation → 对比Offer + 薪资谈判
```

---

## 简历

### resume-academic-cv-builder

**路径：** `skills/job-hunting/resume-academic-cv-builder`

**触发场景：** Format CVs for academic positions with publications, grants, and teaching

**核心能力：**
- Structure CVs for academic positions
- Format publications, presentations, and grants
- Organize teaching and research experience
- Include appropriate academic sections
- Tailor for different academic roles (tenure-track, postdoc, lecturer)

**输出格式：** When creating an academic CV:

**关键红线：**
- **不要把学术 CV 压缩成工业界简历长度**：早期学者 2–4 页、资深教授 15–30+ 页都属正常，强行压缩会削弱学术可信度。
- **作者顺序就是学术信用**：在理工领域，第一作者和通讯作者的地位截然不同，标注错误可能被视为学术不端。
- **“审稿中”论文必须诚实标注状态**：In Preparation、Submitted、Under Review、Revise & Resubmit 的区分必须准确，不能将仅有个想法的论文写成待发表。

**标签：** career


### resume-ats-formatter

**路径：** `skills/job-hunting/resume-ats-formatter`

**触发场景：** 当用户提到'ATS优化'、'简历格式'、'简历排版'、'机器筛选'或需要确保简历通过ATS系统时触发。提供格式兼容性检查、关键词匹配度分析与ATS友好排版建议。

**关键红线：**
- **双受众陷阱**：简历必须同时满足 ATS 机器解析和人类快速扫描。不要为了追求美观而牺牲解析正确性。
- **PDF 不是万能的**：很多 ATS 对 PDF 的解析效果不如 DOCX。除非职位明确要求 PDF，否则优先提交 `.docx`。
- **精确匹配 > 同义词**：ATS 通常搜索精确短语。如果 JD 写 "project management"，写 "project coordination" 可能匹配失败。

**标签：** career, ats, resume


### resume-bullet-writer

**路径：** `skills/job-hunting/resume-bullet-writer`

**触发场景：** 当用户希望优化简历 bullet points、添加量化指标、将模糊描述转化为成果导向陈述，或说"没有数据""无法量化"时触发。涵盖 XYZ 公式、STAR/CAR 框架、隐藏指标发现与估算技巧。

**核心能力：**
- Transform weak bullets into achievement-focused statements
- Apply STAR/CAR methods and X-Y-Z formula
- Find hidden metrics in any experience
- Estimate numbers when exact data is unavailable
- Use strong action verbs and quantify impact

**输出格式：** When rewriting bullets, provide:

**关键红线：**
- **Don't fabricate numbers you can't defend in an interview** — use conservative estimates or ranges instead
- **Avoid numbers that reveal confidential information** — use percentages or omit sensitive figures
- **Don't use numbers that make you look bad** — context matters; "resolved 2 tickets/day" is weak without quality context

**标签：** career


### resume-career-changer-translator

**路径：** `skills/job-hunting/resume-career-changer-translator`

**触发场景：** Translate skills from one industry to another, identify transferable skills

**核心能力：**
- Identify transferable skills across industries
- Translate experience into new industry language
- Reframe achievements for target roles
- Bridge skill gaps strategically
- Position career changes positively

**输出格式：** When helping a career changer:

**关键红线：**
- **不要用“热情”替代可验证的技能**：转行简历中最危险的信号是通篇强调“我对 XX 充满热情”却缺乏项目、认证或桥梁经验支撑。
- **不要完全抛弃原行业的量化成果**：招聘方更看重“你带来了什么可迁移的成绩”，而不是“你学了什么新工具”。保留原行业的数字成果并翻译成目标行业语言。
- **警惕术语包装过度**：把“发邮件”翻译成“跨部门利益相关者沟通”会被经验丰富的招聘官识破，确保每一个转换后的术语都经得起面试追问。

**标签：** job-search


### resume-creative-portfolio

**路径：** `skills/job-hunting/resume-creative-portfolio`

**触发场景：** Balance visual design with ATS compatibility for creative roles

**核心能力：**
- Balance visual appeal with ATS compatibility
- Design resumes for creative roles
- Integrate portfolio elements with resume content
- Advise on when to use creative vs. traditional formats
- Guide visual hierarchy and design choices

**输出格式：** When creating a creative resume:

**关键红线：**
- **不要把设计版简历直接上传到 ATS 系统**：多栏、图文混排、图标字体在 ATS 中会变成乱码，导致直接被淘汰。网申必须提交 ATS-compatible 版本。
- **避免使用实验性字体或复杂图形**：招聘官可能在手机、黑白打印或旧版 PDF 阅读器中查看简历，过于前卫的设计可能完全失效。
- **作品集链接必须是活链且可访问**：简历中放置失效的 portfolio URL 是创意岗位的最大红线，务必在投递前再次点击测试。

**标签：** career


### resume-executive-resume-writer

**路径：** `skills/job-hunting/resume-executive-resume-writer`

**触发场景：** Create C-suite and VP level resumes emphasizing strategic leadership

**核心能力：**
- Write resumes for C-suite and VP-level positions
- Emphasize strategic leadership and business transformation
- Showcase P&L responsibility and organizational impact
- Balance achievements with leadership philosophy
- Format for executive recruiters and board presentations

**输出格式：** When writing an executive resume:

**关键红线：**
- **严禁泄露前雇主的机密数据**：未公开的营收、尚未披露的并购标的、内部战略数字都属于保密信息，用百分比或范围替代绝对值。
- **不要使用 IC 级别的战术语言**：高管简历中出现“协助”“参与”“负责日常管理”等词汇会严重削弱领导力定位，应使用“主导”“ orchestrate”“ transformation”等战略级动词。
- **短任期必须给出合理叙事，但不能撒谎**：18 个月的任期可以包装为“被聘请来完成 post-merger integration”，但不能虚构职位或延长任职时间。

**标签：** career


### resume-jd-optimizer

**路径：** `skills/job-hunting/resume-jd-optimizer`

**触发场景：** 当用户拿到目标岗位JD、需要分析匹配度并据此优化简历时触发。执行JD分析→匹配评分→定向改写→关键词植入的端到端流程。

**标签：** career, job-search, resume, interview


### resume-section-builder

**路径：** `skills/job-hunting/resume-section-builder`

**触发场景：** Create targeted resume sections optimized for different experience levels and roles

**核心能力：**
- Build targeted professional summaries
- Structure skills sections effectively
- Optimize experience sections
- Create education sections appropriately
- Add supplementary sections strategically

**输出格式：** When building resume sections:

**关键红线：**
- **不要把所有经历都塞进简历**：相关性永远大于完整性。与目标岗位无关的早期经历或技能只会稀释核心信息，降低 ATS 匹配度。
- **避免在 Skills 中列出无法深入讨论的技术**：如果你只会写“Hello World”却列出 Rust 或 Kubernetes，技术面试中一旦被追问底层原理就会露馅。
- **不要为了填满页面而添加无关的“兴趣爱好”节**：招聘官不会因为你喜欢滑雪而给你面试机会，除非该爱好与岗位或公司文化有直接关联。

**标签：** career


### resume-tech-resume-optimizer

**路径：** `skills/job-hunting/resume-tech-resume-optimizer`

**触发场景：** Optimize resumes for software engineering, PM, and technical roles

**核心能力：**
- Optimize resumes for technical roles (SWE, PM, Data, DevOps)
- Structure technical skills sections effectively
- Highlight projects and technical achievements
- Balance technical depth with business impact
- Format for both ATS and technical recruiters

**输出格式：** When optimizing a tech resume:

**关键红线：**
- **不要在简历中列出“精通”但实际只会基础操作的技术**：技术面试官会针对简历上的每一项技能追问实现细节，夸大技能是最高频的翻车点。
- **严禁使用技能进度条或星级评分**：ATS 无法解析图形化评分，且资深工程师看到“Python ★★★★☆”会认为候选人缺乏专业判断力。
- **GitHub 链接必须保持活跃**：简历上放了一个 2 年前就停止维护、README 为空或 build failing 的仓库，反而会成为负面信号，要么维护要么移除。

**标签：** career


### resume-version-manager

**路径：** `skills/job-hunting/resume-version-manager`

**触发场景：** Track different resume versions, maintain master resume, manage tailored versions

**核心能力：**
- Create and maintain master resume document
- Track tailored resume versions
- Organize resume versions by role/industry
- Maintain consistent source of truth
- Streamline resume updates

**输出格式：** When managing resume versions:

**关键红线：**
- **不要直接修改 Master Resume**：Master 是 source of truth，应从中复制出 tailored 版本后再编辑。
- **命名混乱**：避免使用 "resume_final_v2_updated.docx" 这类无意义文件名，严格遵循 `LastName_Role_Company_Date.pdf` 格式。
- **版本失控**：不要在多个 "master" 之间反复切换，永远只维护一个 master。

**标签：** career


---

## 面试

### interview-data-governance

**路径：** `skills/job-hunting/interview-data-governance`

**触发场景：** 当用户明确要求生成数据治理领域的面试练习题，或提到'数据治理面试题'、'data governance interview'、'DAMA面试'、'数据治理练习'时触发。生成覆盖数据标准、数据质量、元数据、数据血缘、主数据管理（MDM）、数据安全六大核心域的结构化面试题，支持概念框架、场景设计、合规案例、技术工具四种题型。

**关键红线：**
- **Regulatory accuracy**: When referencing specific regulations (e.g., 银保监会指引 Article X), verify the article exists or frame as "per regulatory guidance" rather than citing fake articles.
- **Tool neutrality**: Avoid questions that assume a single vendor stack. Candidates should be evaluated on principles, not product certifications.
- **Ambiguity is intentional**: The best scenario questions are deliberately under-specified to test the candidate's ability to ask clarifying questions.

**标签：** interview, data-engineering, data-governance


### interview-generation

**路径：** `skills/job-hunting/interview-generation`

**触发场景：** Generates Python coding interview practice prompts in this repository's 4-part format. Use only when the user explicitly asks to create or refine interview practice questions/prompts (not for general coding tasks).

**关键红线：**
- **严禁跳过“扫描现有内容”步骤直接生成**：如果忽略仓库中已有的题目，极易产生变体重叠（如又一个 LRU Cache 或 Message Broker），浪费题库价值。
- **不要依赖冷门算法或数学技巧作为核心考点**：面试题的设计意图是考察工程思维和代码质量，如果候选人因为不知道某个小众算法而失败，题目本身就有缺陷。
- **Part 4 必须是真实的系统设计/生产环境讨论**：禁止把脑筋急转弯、纯理论概念或八股文背诵作为 Part 4 的内容。

**标签：** interview


### interview-prep

**路径：** `skills/job-hunting/interview-prep`

**触发场景：** 当用户需要准备面试、分析JD、复盘面试记录、或者询问面试策略时触发。支持面试前准备（STAR故事库+问题预测+按轮次策略）和面试后复盘（逐题拆解+模式识别）双模式。

**关键红线：**
- **轮次错位是最高频失败原因**：初面考执行力，终面考战略思维。同一套策略打所有轮次必死。
- **STAR的Action必须是"你"**：不是"我们"做了什么。面试官要听你的具体行动。
- **弱点不要假贬真褒**："我工作太努力"是red flag。必须给真实弱点 + 改进行动。

**标签：** interview


### interview-requirements-prioritization-drill

**路径：** `skills/job-hunting/interview-requirements-prioritization-drill`

**触发场景：** Runs a rapid system design drill focused on clarification questions and requirement prioritization before architecture work. Use when the user wants to practice follow-up questions, requirement scoping, or turning an ambiguous prompt into a small set of prioritized functional and non-functional requirements.

**关键红线：**
- **不要替用户生成“标准答案”后再让用户背诵**：演练的价值在于用户自己思考追问，如果提前 dump 理想答案，就变成记忆训练而非能力训练。
- **避免生成过于宽泛、无法在 5 分钟内收敛的题目**：如果 prompt 涉及“设计一个电商平台”而没有明确边界，用户会陷入功能罗列，无法练习 prioritization。
- **不要过早泄露 CAP 立场或具体技术选型**：在 requirements 阶段就告诉用户“这里应该用 eventual consistency”会破坏练习目标，技术决策应留到架构阶段。

**标签：** interview


### interview-system-design

**路径：** `skills/job-hunting/interview-system-design`

**触发场景：** Generates systems design interview practice (prompt + solution files), acts as an interactive interviewer, and reviews whiteboard designs via Excalidraw. Use when the user asks to create, practice, or get feedback on a system design interview.

**关键红线：**
- **Prompt 文件中严禁包含任何答案、提示或参考材料**：candidate 可能会在练习前误读 prompt 文件，任何内嵌的 hint 都会破坏面试的公平性。
- **避免使用 URL Shortener、Parking Lot 等过度使用的经典题目**：这些题目有大量现成答案，无法有效区分候选人的真实水平，应优先选择业务场景题。
- **作为面试官时绝不要主动泄露 solution 文件内容**：即使候选人卡壳，也只能给出方向性提示（如“你漏了一个一致性相关的 NFR”），不能说出“这里应该用 Raft”。

**标签：** interview


---

## 求职材料

### cover-letter-generator

**路径：** `skills/job-hunting/cover-letter-generator`

**触发场景：** Create personalized, compelling cover letters from resume and job description

**核心能力：**
- Generate personalized cover letters from resume + job description
- Match tone to company culture
- Address qualification gaps strategically
- Create compelling opening hooks
- Structure persuasive arguments for candidacy

**输出格式：** When generating a cover letter, provide:

**关键红线：**
- **不要发送未经人工检查的 AI 生成求职信**：AI 可能幻觉出虚假的公司新闻、错误的产品名或并不存在的共同联系人，发送前必须逐句验证。
- **不要在求职信中重复简历上的所有内容**：求职信的价值是补充简历无法传达的动机、个性和具体公司研究，机械复述简历是浪费机会。
- **同一公司的不同岗位不要使用同一封求职信**：招聘系统会存档所有投递记录，内容雷同的求职信会被视为缺乏诚意。

**标签：** career


### portfolio-case-study-writer

**路径：** `skills/job-hunting/portfolio-case-study-writer`

**触发场景：** Transform resume bullets into detailed portfolio case studies

**核心能力：**
- Transform resume bullets into detailed case studies
- Structure case studies for maximum impact
- Create compelling project narratives
- Balance technical detail with business context
- Format for portfolio websites

**输出格式：** When creating a case study:

**关键红线：**
- **严禁泄露前雇主的敏感商业数据**：真实的用户数、营收、转化率、内部系统架构图必须脱敏或模糊化处理，否则可能违反保密协议并引发法律风险。
- **不要把团队成果包装成个人英雄主义**：案例研究中如果通篇使用“我”而忽略跨职能团队，面试时追问细节极易穿帮。必须明确划分个人贡献与团队协作边界。
- **禁止编造“前后对比”数据**：如果无法获得真实的 Before/After 指标，宁可不写具体数字，也不要捏造 35% 提升或 $2M 收益，背景调查可能核实。

**标签：** career


### reference-list-builder

**路径：** `skills/job-hunting/reference-list-builder`

**触发场景：** Format professional references properly and prepare reference materials

**核心能力：**
- Format professional reference lists
- Guide reference selection strategy
- Prepare reference briefing materials
- Anticipate reference check questions
- Handle difficult reference situations

**输出格式：** When building a reference list:

**关键红线：**
- **绝对禁止未经同意就将某人列为推荐人**：突然接到背调电话会让对方措手不及，甚至可能因不知情而给出模棱两可的评价，直接毁掉 offer。
- **不要提供可能给出中性或负面评价的联系人**：如果你不确定某位前上司对你的真实看法，宁可少提供一个推荐人，也不要冒险。
- **推荐人组合不能全是平级同事**：缺少直属上级的推荐人名单会触发 HR 警觉，至少包含一位最近 3 年内的 direct supervisor。

**标签：** career


---

## 平台/联动

### linkedin-profile-optimizer

**路径：** `skills/job-hunting/linkedin-profile-optimizer`

**触发场景：** Optimize LinkedIn profile for searchability, recruiter visibility, and engagement

**核心能力：**
- Optimize headline for searchability
- Write compelling About/Summary sections
- Structure Experience section for impact
- Improve profile completeness score
- Add relevant keywords for recruiter searches

**输出格式：** When optimizing a LinkedIn profile:

**关键红线：**
- **不要为了提高搜索排名而堆砌无关关键词**：在 Headline 或 About 中塞入与自身经验无关的热门技能，会在面试追问时暴露水分，且降低专业可信度。
- **“Open to Work”绿标可能降低议价能力**：虽然绿标能增加 recruiter 主动联系，但也会让 HR 在薪资谈判前就知道你处于求职状态。高管或被动求职者建议仅对 recruiter 可见。
- **不要直接复制粘贴简历内容到 About section**：LinkedIn 的语气应比简历更对话化、更有个人品牌色彩，机械复制会显得呆板且浪费 2,600 字符的宝贵空间。

**标签：** career


### resume-linkedin-optimizer

**路径：** `skills/job-hunting/resume-linkedin-optimizer`

**触发场景：** 当用户提到'优化简历'、'LinkedIn'、'领英'、'求职'或需要根据目标岗位同时优化简历和LinkedIn个人资料时触发。提供简历与领英联动的统一优化方案。

**关键红线：**
- **经历真实性**：不编造经历。不得虚构未任职的公司、未参与的项目或未获得的证书。
- **成果量化**：不夸大成果。将"参与"改写成"主导"属于诚信风险。建议用户提供具体数据，模型仅负责润色表达。
- **去重检查**：不照抄 JD 原句。直接复制岗位要求会导致 ATS 系统标记为关键词堆砌，应做语义转换和同义替换。

**标签：** interview, career, hr


---

## Offer/谈判

### offer-negotiation

**路径：** `skills/job-hunting/offer-negotiation`

**触发场景：** 当用户拿到多个offer需要比较、或需要就单个offer进行薪资谈判时触发。提供总薪酬对比分析、加权决策矩阵、谈判策略与Counter脚本。

**核心能力：**
- Compare total compensation across offers
- Build negotiation strategy and scripts
- Create weighted decision frameworks
- Calculate true offer value
- Prepare counter-offer responses

**关键红线：**
- ** verbal promises ≠ written offer**：任何口头承诺（如"我们明年会给你涨薪"）如果没有写进 offer letter，都不具备约束力。务必要求书面确认。
- **Equity 的税务陷阱**：RSU 在归属时按普通收入征税，行权时可能触发 AMT（替代性最低税）。Options 的行权成本容易被忽略，需提前准备现金。不同国家/地区的股权税务处理差异巨大，建议咨询税务顾问。
- **Non-compete 和 IP 条款**：签字前仔细阅读竞业限制和知识产权归属条款。某些州的 non-compete 可能不具法律效力，但签字后产生纠纷依然耗时耗力。如有疑虑，请律师审阅。

**标签：** interview, compensation, negotiation, career


---

## 工具

### jd-scraper

**路径：** `skills/job-hunting/jd-scraper`

**触发场景：** 当用户需要抓取招聘网站的职位描述（JD）时触发。支持 Indeed、Glassdoor、LinkedIn、BOSS直聘、猎聘、拉勾等平台，提供浏览器自动化、API聚合、反爬策略和数据标准化方案。适用于批量收集JD用于简历定制、求职分析或建立个人职位库。

**输出格式：** When delivering scraped results:

**关键红线：**
- **Legal gray area**: Scraping publicly visible data is generally legal (hiQ v. LinkedIn), but violating a platform's ToS carries civil risk. Never resell scraped data or spam ATS systems.
- **LinkedIn bans accounts, not just IPs**: A banned LinkedIn account is hard to recover. Use commercial services or throwaway accounts for DIY.
- **BOSS直聘验证码**: After ~50 rapid requests, BOSS serves slider captchas. Slow down or switch to Puppeteer with captcha-solving service.

**标签：** interview, job-search, scraping, automation


---

## 调度器

### career-ops

**路径：** `skills/job-hunting/career-ops`

**触发场景：** 当用户需要一站式求职支持但不确定该用哪个专项 skill 时触发。负责识别意图并将请求路由到 interview 分类下的对应专项 skill，不执行具体业务逻辑。

**关键红线：**
- **不要重复造轮子**：career-ops 只负责路由，所有具体工作由专项 skill 完成。若发现用户诉求在上表中无精确匹配，优先推荐最接近的 skill，而非自行处理。
- **模糊意图处理**：如果用户意图不明确（如只说"帮我找工作"），先询问澄清（当前阶段、具体卡点、目标岗位类型），不要猜测后错误路由。
- **避免串行过载**：不要一次性调用多个 skill。先解决用户当前最核心的一项诉求，完成后再视情况引导至下一项。

**标签：** job-search


---

## 典型使用示例

### 示例1：投技术岗前的完整准备

1. **用户输入：** "帮我优化简历，我要投大数据架构师"
2. **推荐 Skill 序列：**
   - `resume-bullet-writer`：先精修经历描述，补充量化数据
   - `resume-tech-resume-optimizer`：按技术岗标准重组技能列表和项目展示
   - `resume-ats-formatter`：检查格式兼容性和关键词匹配度
   - `linkedin-profile-optimizer`：同步优化领英资料

### 示例2：拿到JD后的定向投递

1. **用户输入：** "分析这个JD，帮我改简历" + 粘贴JD文本
2. **推荐 Skill 序列：**
   - `resume-jd-optimizer`：一站式完成JD分析→匹配评分→简历改写
   - `cover-letter-generator`：基于匹配结果生成针对性求职信

### 示例3：面试前准备

1. **用户输入：** "我下周有终面，帮我准备一下"
2. **推荐 Skill 序列：**
   - `interview-prep`：准备模式 → 按终面轮次生成策略、STAR故事库、预测问题
   - `interview-system-design`（如投架构岗）：专项系统设计演练

### 示例4：拿到Offer后

1. **用户输入：** "我拿了两个Offer，帮我比较一下"
2. **推荐 Skill：** `offer-negotiation` → 总薪酬拆解 + 加权决策矩阵 + 谈判脚本

---

## 快速索引表

| Skill | 触发关键词 | 所属阶段 |
|-------|-----------|---------|
| offer-negotiation | 当用户拿到多个offer需要比较、或需要就单个offer进行... | Offer/谈判 |
| jd-scraper | 当用户需要抓取招聘网站的职位描述（JD）时触发。支持 Ind... | 工具 |
| linkedin-profile-optimizer | Optimize LinkedIn profile for ... | 平台/联动 |
| resume-linkedin-optimizer | 优化简历 / LinkedIn / 领英 | 平台/联动 |
| cover-letter-generator | Create personalized, compellin... | 求职材料 |
| portfolio-case-study-writer | Transform resume bullets into ... | 求职材料 |
| reference-list-builder | Format professional references... | 求职材料 |
| resume-academic-cv-builder | Format CVs for academic positi... | 简历 |
| resume-ats-formatter | ATS优化 / 简历格式 / 简历排版 | 简历 |
| resume-bullet-writer | 没有数据 / 无法量化 | 简历 |
| resume-career-changer-translator | Translate skills from one indu... | 简历 |
| resume-creative-portfolio | Balance visual design with ATS... | 简历 |
| resume-executive-resume-writer | Create C-suite and VP level re... | 简历 |
| resume-jd-optimizer | 当用户拿到目标岗位JD、需要分析匹配度并据此优化简历时触发。... | 简历 |
| resume-section-builder | Create targeted resume section... | 简历 |
| resume-tech-resume-optimizer | Optimize resumes for software ... | 简历 |
| resume-version-manager | Track different resume version... | 简历 |
| career-ops | 当用户需要一站式求职支持但不确定该用哪个专项 skill 时... | 调度器 |
| interview-data-governance | 数据治理面试题 / data governance interview / DAMA面试 | 面试 |
| interview-generation | Generates Python coding interv... | 面试 |
| interview-prep | 当用户需要准备面试、分析JD、复盘面试记录、或者询问面试策略... | 面试 |
| interview-requirements-prioritization-drill | Runs a rapid system design dri... | 面试 |
| interview-system-design | Generates systems design inter... | 面试 |
