---
name: career-ops
description: 当用户需要一站式求职支持但不确定该用哪个专项 skill 时触发。负责识别意图并将请求路由到 interview 分类下的对应专项 skill，不执行具体业务逻辑。
---

# Career Ops Router

## 适用场景

当用户需要一站式求职支持但不确定该用哪个专项 skill 时触发。本 skill 仅做意图识别与路由，所有具体工作由下游专项 skill 完成。

## 命令映射表

| 用户输入 | 调用 Skill | 说明 |
|----------|-----------|------|
| 分析JD / 评估岗位匹配度 / 根据JD改简历 | resume-jd-optimizer | 执行JD分析 → 匹配评分 → 定向改写 → 关键词植入 |
| 优化简历 bullet / 量化经历 / 强动词替换 | resume-bullet-writer | 精修 bullet points、XYZ 公式、STAR/CAR 框架、隐藏指标发现 |
| 检查ATS兼容性 / 机器筛选 / 简历格式 | resume-ats-formatter | 格式诊断 + 关键词匹配度分析 + ATS友好排版建议 |
| 技术简历优化 / 工程师简历 / PM简历 | resume-tech-resume-optimizer | 针对软件工程、PM 及技术岗位的简历专项优化 |
| 转行简历 / 技能迁移 / 跨行业翻译 | resume-career-changer-translator | 识别可迁移技能、跨行业话术翻译 |
| 学术CV / 科研简历 / 高校申请 | resume-academic-cv-builder | 学术导向的 CV 构建与格式规范 |
| 高管简历 / 领导力经历 / C-level | resume-executive-resume-writer | 高管级别简历的叙事策略与影响力表达 |
| 创意作品集 / 设计师简历 | resume-creative-portfolio | 创意行业作品集与视觉叙事简历 |
| 简历版本管理 / 多份简历维护 | resume-version-manager | 维护 master resume 与各定向版本 |
| 简历章节构建 / 某一段不会写 | resume-section-builder | 按章节（Summary / Experience / Skills 等）结构化构建 |
| 简历+LinkedIn联合优化 | resume-linkedin-optimizer | 简历与 LinkedIn 资料的一致性联动优化 |
| 生成求职信 / Cover Letter | cover-letter-generator | 基于简历 + JD 生成个性化求职信 |
| 面试准备 / 预测问题 / 复盘面试 | interview-prep | STAR 故事库 + 按轮次策略 + 面试后复盘 |
| 系统设计面试 / 白板设计 | interview-system-design | 生成系统设计方案、模拟面试官、评审白板设计 |
| 数据治理面试 / 数据岗位 | interview-data-governance | 数据治理领域专项面试准备 |
| 面试题生成 / 模拟面试 | interview-generation | 自动生成面试题库与模拟对话 |
| 薪资谈判 / 比较多个Offer | offer-negotiation | 总薪酬对比 + 加权决策矩阵 + 谈判策略 + Counter 脚本 |
| 优化LinkedIn / 资料完善 | linkedin-profile-optimizer | 资料优化 + 关键词策略 + 搜索可见性提升 |
| 抓取JD / 爬取招聘信息 | jd-scraper | 支持主流招聘平台的 JD 自动化抓取与数据标准化 |
| 作品集案例 / Case Study | portfolio-case-study-writer | 项目案例结构化写作，用于作品集展示 |
| 推荐信列表 / Reference联系人 | reference-list-builder | 整理推荐人列表与沟通策略 |
| 需求优先级练习 / PM面试题 | interview-requirements-prioritization-drill | PM 面试中的需求排序与权衡训练 |

## 使用方式

1. **识别用户意图**：分析用户当前输入的核心诉求。
2. **查表匹配**：在上表中找到最贴近的专项 skill。
3. **路由执行**：将用户请求转交给对应 skill 处理，并明确告知用户正在调用哪个专项能力。
4. **禁止越权**：不要在本 skill 内实现任何具体业务逻辑（如改写简历、生成求职信、模拟面试等）。

## Gotchas

- **不要重复造轮子**：career-ops 只负责路由，所有具体工作由专项 skill 完成。若发现用户诉求在上表中无精确匹配，优先推荐最接近的 skill，而非自行处理。
- **模糊意图处理**：如果用户意图不明确（如只说"帮我找工作"），先询问澄清（当前阶段、具体卡点、目标岗位类型），不要猜测后错误路由。
- **避免串行过载**：不要一次性调用多个 skill。先解决用户当前最核心的一项诉求，完成后再视情况引导至下一项。
- **skill 名称引用**：路由时必须使用 skill 的准确 kebab-case 名称（如 `resume-jd-optimizer`），确保调用方正确加载。
