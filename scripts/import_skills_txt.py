#!/usr/bin/env python3
"""Import skills from docs-internal/Skills.txt into the project."""

import json
import os
from pathlib import Path

ROOT = Path(__file__).parent.parent
SKILLS_DIR = ROOT / "skills"
INDEX_FILE = ROOT / "index.json"

# Define skills grouped by category
categories = {
    "learning": [
        {
            "name": "structured-notes-generator",
            "description": "当用户提到'整理笔记'、'结构化笔记'、'学习总结'、'提炼概念'或需要将学习材料转化为结构化笔记时触发。适用于提炼概念、定义、例子、关系图和复习问题的学习场景。",
            "title": "结构化笔记生成器",
            "inputs": [
                "主题、文章、PDF 内容、课堂笔记或视频转录稿",
                "可选：学习目标、读者水平、考试范围",
            ],
            "workflow": [
                "先识别材料的核心主题和层级。",
                "提取关键概念、定义、例子和公式。",
                "按'总览 -> 子主题 -> 关键点 -> 示例'组织。",
                "标出概念之间的关系。",
                "生成 3-5 个复习问题。",
            ],
            "output": [
                "主题标题",
                "一页总览",
                "分层笔记",
                "概念关系",
                "复习问题",
            ],
            "constraints": [
                "不编造源材料中没有的信息。",
                "不为了通俗牺牲准确性。",
                "缺少上下文的地方标记为 [需要补充]。",
            ],
            "tags": ["learning", "notes", "education"],
            "pattern": "generator",
        },
        {
            "name": "exam-prep-generator",
            "description": "当用户提到'出题'、'模拟题'、'考试准备'、'复习测验'或需要根据材料生成练习题时触发。适用于复习、自测和培训考核。",
            "title": "考试准备器",
            "inputs": [
                "学习材料、课程大纲或考试范围",
                "可选：考试类型、题量、难度比例",
            ],
            "workflow": [
                "识别最可能被考察的概念。",
                "按记忆、理解、应用、分析四类能力设计题目。",
                "生成选择题、简答题和案例题。",
                "给出答案和解释。",
                "标注每题难度。",
            ],
            "output": [
                "选择题 5-10 题",
                "简答题 3-5 题",
                "案例题 1-2 题",
                "答案与解析",
            ],
            "constraints": [
                "所有题目基于材料。",
                "不在多题里重复考同一个点。",
                "干扰项要真实，不写明显错误的选项。",
            ],
            "tags": ["learning", "exam", "education"],
            "pattern": "generator",
        },
        {
            "name": "learning-roadmap-generator",
            "description": "当用户提到'学习路线'、'学习计划'、'能力提升'、'技术入门'或需要为学习目标制定路线图时触发。适用于学习新技术、新岗位能力或新业务领域。",
            "title": "学习路线图生成器",
            "inputs": [
                "想学习的主题",
                "当前水平",
                "每周可投入时间",
                "目标完成时间",
            ],
            "workflow": [
                "明确最终目标和当前起点。",
                "将目标拆成 4-12 周阶段。",
                "每周给出主题、目标、资源和练习。",
                "每周设置可验证检查点。",
                "标出前置依赖和风险。",
            ],
            "output": [
                "最终目标",
                "当前水平假设",
                "周计划表",
                "每周练习",
                "检查点",
            ],
            "constraints": [
                "不默认安排超过每周 5-7 小时。",
                "推荐付费资源时给出免费替代。",
                "检查点写成'能完成什么'，不写'理解什么'。",
            ],
            "tags": ["learning", "planning", "education"],
            "pattern": "generator",
        },
        {
            "name": "complex-concept-explainer",
            "description": "当用户提到'解释概念'、'通俗讲解'、'技术科普'、'跨部门沟通'或需要用不同深度解释复杂概念时触发。适用于技术概念、业务概念、金融概念或跨部门沟通。",
            "title": "复杂概念解释器",
            "inputs": [
                "一个复杂概念",
                "目标读者",
                "期望深度",
            ],
            "workflow": [
                "先用一个直观类比建立直觉。",
                "用零术语版本解释。",
                "再给中级版本，引入必要术语。",
                "最后给技术版本。",
                "补充常见误解和相关概念。",
            ],
            "output": [
                "一句话解释",
                "类比",
                "基础版",
                "中级版",
                "技术版",
                "常见误解",
                "延伸概念",
            ],
            "constraints": [
                "类比不能误导。",
                "简化不等于失真。",
                "不确定的地方要标注边界。",
            ],
            "tags": ["learning", "communication", "education"],
            "pattern": "generator",
        },
        {
            "name": "academic-paper-drafter",
            "description": "当用户提到'写论文'、'学术写作'、'研究报告'、'论文大纲'或需要组织正式研究写作结构时触发。适用于正式研究写作。",
            "title": "学术论文写作器",
            "inputs": [
                "主题",
                "文章类型",
                "目标字数",
                "引用格式",
                "已有资料",
            ],
            "workflow": [
                "先明确研究问题。",
                "生成结构大纲。",
                "写引言、背景、方法、分析和结论。",
                "标出需要引用的位置。",
                "检查结论是否回应研究问题。",
            ],
            "output": [
                "标题建议",
                "论文结构",
                "各章节草稿",
                "引用占位",
                "待补资料清单",
            ],
            "constraints": [
                "不编造来源。",
                "需要引用的位置标 [需要引用]。",
                "不替用户伪造研究结果。",
            ],
            "tags": ["learning", "writing", "academic"],
            "pattern": "generator",
        },
        {
            "name": "flashcard-creator",
            "description": "当用户提到'记忆卡片'、'Anki'、'Quizlet'、'主动回忆'或需要从资料中提取知识点生成问答卡片时触发。适用于内部培训题库和间隔重复学习。",
            "title": "记忆卡片生成器",
            "inputs": [
                "学习材料、笔记或文档",
                "可选：主题标签、难度范围",
            ],
            "workflow": [
                "提取事实、定义、流程、对比和例子。",
                "设计具体问题。",
                "给出 1-3 行简洁答案。",
                "按主题和难度打标签。",
                "从简单到困难排序。",
            ],
            "output": [
                "编号",
                "正面问题",
                "背面答案",
                "标签",
                "难度",
            ],
            "constraints": [
                "不设计只能回答'是/否'的问题。",
                "每张卡片独立可理解。",
                "不重复同一个概念。",
            ],
            "tags": ["learning", "memory", "education"],
            "pattern": "generator",
        },
        {
            "name": "study-session-planner",
            "description": "当用户提到'学习计划'、'备考安排'、'复习日程'、'时间规划'或需要根据考试日期生成学习日程时触发。适用于学生复习、员工培训和证书备考。",
            "title": "学习时段规划器",
            "inputs": [
                "科目或主题",
                "截止日期",
                "每天可用时间",
                "难度和优先级",
            ],
            "workflow": [
                "按考试临近程度和难度排序。",
                "拆分每日学习块。",
                "安排新内容、复习和练习。",
                "加入间隔复习。",
                "保留休息和缓冲时间。",
            ],
            "output": [
                "总体计划",
                "每日安排",
                "学习块类型",
                "复习点",
                "风险提醒",
            ],
            "constraints": [
                "每天有效学习不超过 6 小时。",
                "同一主题不连续安排过久。",
                "时间不够时明确提示取舍。",
            ],
            "tags": ["learning", "planning", "time-management"],
            "pattern": "generator",
        },
    ],
    "office": [
        {
            "name": "professional-email-drafter",
            "description": "当用户提到'写邮件'、'发邮件'、'邮件草稿'、'客户沟通'或需要根据场景撰写专业邮件时触发。适用于请求、跟进、升级、说明、拒绝和客户沟通。",
            "title": "专业邮件撰写器",
            "inputs": [
                "邮件目的",
                "收件人关系",
                "背景事实",
                "期望动作",
                "语气要求",
            ],
            "workflow": [
                "判断沟通场景。",
                "选择合适语气。",
                "用简短开头交代背景。",
                "清晰提出请求或结论。",
                "给出下一步。",
            ],
            "output": [
                "邮件主题",
                "正文",
                "可选备选语气",
            ],
            "constraints": [
                "不编造事实。",
                "不写阴阳怪气或攻击性表达。",
                "不默认加入空泛寒暄。",
                "敏感邮件保持克制。",
            ],
            "tags": ["office", "communication", "email"],
            "pattern": "generator",
        },
        {
            "name": "meeting-notes-organizer",
            "description": "当用户提到'会议纪要'、'会议整理'、'会议记录'、'行动项'或将零散笔记整理成可执行纪要时触发。适用于项目会、客户会、复盘会和管理例会。",
            "title": "会议纪要组织器",
            "inputs": [
                "会议记录或转录稿",
                "可选：参会人、日期、项目名",
            ],
            "workflow": [
                "区分事实、讨论、决策和行动项。",
                "提取已经明确的结论。",
                "标出行动项、负责人和截止时间。",
                "把未决事项放到开放问题。",
                "标出缺失信息。",
            ],
            "output": [
                "会议摘要",
                "已做决策",
                "行动项：负责人 / 动作 / 截止时间",
                "开放问题",
                "风险与依赖",
            ],
            "constraints": [
                "不补造负责人和日期。",
                "不把讨论意见写成已决策。",
                "缺信息标 [缺失]。",
            ],
            "tags": ["office", "meeting", "communication"],
            "pattern": "generator",
        },
        {
            "name": "cv-linkedin-optimizer",
            "description": "当用户提到'优化简历'、'LinkedIn'、'领英'、'求职'、'内部转岗'或需要根据目标岗位优化个人资料时触发。适用于求职、内部转岗和人才包装。",
            "title": "简历与领英优化器",
            "inputs": [
                "当前简历",
                "目标岗位 JD",
                "真实经历",
                "可量化成果",
            ],
            "workflow": [
                "分析 JD 的核心能力要求。",
                "将经历映射到岗位要求。",
                "重写经历描述。",
                "加入真实量化结果。",
                "标出能力缺口和补救方式。",
            ],
            "output": [
                "职业简介",
                "工作经历改写",
                "技能关键词",
                "领英标题",
                "能力缺口",
            ],
            "constraints": [
                "不编造经历。",
                "不夸大成果。",
                "不照抄 JD 原句。",
            ],
            "tags": ["office", "career", "hr"],
            "pattern": "generator",
        },
        {
            "name": "presentation-prep-skill",
            "description": "当用户提到'做PPT'、'演示文稿'、'汇报结构'、'演讲准备'或需要将主题整理成演示结构时触发。适用于高管汇报、融资路演和技术方案评审。",
            "title": "演示文稿准备器",
            "inputs": [
                "演示主题",
                "目标听众",
                "时长",
                "已有材料",
            ],
            "workflow": [
                "明确演示目标。",
                "设计叙事线。",
                "拆成逐页结构。",
                "每页只保留一个核心观点。",
                "给出视觉建议和讲者备注。",
            ],
            "output": [
                "演示标题",
                "听众画像",
                "页码结构",
                "每页关键点",
                "视觉建议",
                "讲者备注",
            ],
            "constraints": [
                "不做纯文字堆叠。",
                "15-20 分钟不超过 20 页。",
                "每页不超过 3-4 个要点。",
            ],
            "tags": ["office", "presentation", "communication"],
            "pattern": "generator",
        },
    ],
    "research": [
        {
            "name": "deep-research-synthesizer",
            "description": "当用户提到'深度研究'、'行业研究'、'竞品调研'、'多源分析'或需要从多份材料中提炼洞察时触发。适用于行业研究、产品研究和战略分析。",
            "title": "深度研究合成器",
            "inputs": [
                "多个来源材料",
                "研究问题",
                "输出目标",
            ],
            "workflow": [
                "先按来源类型分类。",
                "提取每个来源的事实和观点。",
                "找出共识、分歧和空白。",
                "合成关键洞察。",
                "给出下一步问题。",
            ],
            "output": [
                "研究问题",
                "来源分层",
                "关键事实",
                "主要洞察",
                "分歧与风险",
                "下一步建议",
            ],
            "constraints": [
                "区分事实、推测和作者判断。",
                "不把单一来源写成行业共识。",
                "重要结论给来源依据。",
            ],
            "tags": ["research", "analysis", "strategy"],
            "pattern": "generator",
        },
        {
            "name": "source-validation-skill",
            "description": "当用户提到'验证来源'、'信息可信度'、'交叉验证'、'事实核查'或需要评估信息来源质量时触发。适用于研究、写作、投研、竞品分析和技术选型。",
            "title": "来源验证器",
            "inputs": [
                "链接、文章、报告或引用",
                "需要验证的问题",
            ],
            "workflow": [
                "检查作者、机构和发布时间。",
                "判断是否一手来源。",
                "查找交叉验证材料。",
                "标出利益相关和可能偏见。",
                "给出可信度等级。",
            ],
            "output": [
                "来源列表",
                "可信度评分",
                "可确认事实",
                "不确定信息",
                "使用建议",
            ],
            "constraints": [
                "不把营销稿当事实。",
                "不把过期资料当当前事实。",
                "无法确认时明确写'未验证'。",
            ],
            "tags": ["research", "validation", "fact-checking"],
            "pattern": "reviewer",
        },
        {
            "name": "knowledge-structuring-skill",
            "description": "当用户提到'知识整理'、'结构化知识'、'知识库'、'资料归档'或需要将非结构化材料整理成框架时触发。适用于知识库、项目资料和研究归档。",
            "title": "知识结构化器",
            "inputs": [
                "零散笔记、文章、会议材料或资料包",
                "可选：目标分类方式",
            ],
            "workflow": [
                "识别主题和实体。",
                "合并重复信息。",
                "建立层级结构。",
                "标出关系和依赖。",
                "生成可维护目录。",
            ],
            "output": [
                "总体框架",
                "分类目录",
                "核心概念",
                "关系说明",
                "待补资料",
            ],
            "constraints": [
                "不为了整齐而改写事实。",
                "不合并语义不同的概念。",
                "保留来源线索。",
            ],
            "tags": ["research", "knowledge-management", "organization"],
            "pattern": "generator",
        },
        {
            "name": "competitive-intelligence-skill",
            "description": "当用户提到'竞品分析'、'竞争情报'、'市场对比'、'产品定位'或需要比较产品/公司/方案时触发。适用于竞品分析、市场研究和产品战略。",
            "title": "竞争情报分析器",
            "inputs": [
                "竞品列表",
                "分析目标",
                "资料来源",
                "关注维度",
            ],
            "workflow": [
                "明确比较维度。",
                "提取每个对象的事实信息。",
                "做功能、定位、客户、价格和风险对比。",
                "提炼差异。",
                "给出机会和不确定性。",
            ],
            "output": [
                "对比表",
                "每个竞品摘要",
                "优势和弱点",
                "机会点",
                "风险和待验证问题",
            ],
            "constraints": [
                "不把宣传口径当真实能力。",
                "不做无来源的市场判断。",
                "区分事实和推测。",
            ],
            "tags": ["research", "competitive-analysis", "strategy"],
            "pattern": "generator",
        },
    ],
    "content-creation": [
        {
            "name": "video-script-generator",
            "description": "当用户提到'视频脚本'、'短视频'、'口播稿'、'内容传播'或需要为视频生成脚本结构时触发。适用于内容团队和产品传播。",
            "title": "视频脚本生成器",
            "inputs": [
                "主题",
                "目标观众",
                "视频时长",
                "平台",
                "核心观点",
            ],
            "workflow": [
                "设计开场钩子。",
                "拆成 3-5 个段落。",
                "每段给出画面和口播重点。",
                "控制节奏。",
                "收束到一个行动或观点。",
            ],
            "output": [
                "标题",
                "开场",
                "分段脚本",
                "画面建议",
                "结尾",
            ],
            "constraints": [
                "不为了吸引注意力夸大事实。",
                "不堆空泛口号。",
                "保持和平台时长匹配。",
            ],
            "tags": ["content", "video", "marketing"],
            "pattern": "generator",
        },
        {
            "name": "hook-generator",
            "description": "当用户提到'开场钩子'、'标题'、'吸引读者'、'开篇'或需要为内容生成开场时触发。适用于文章、视频、社交媒体或演示场景。",
            "title": "开场钩子生成器",
            "inputs": [
                "主题",
                "目标读者",
                "内容类型",
                "核心观点",
            ],
            "workflow": [
                "找到读者最关心的冲突或收益。",
                "生成多种开场路线。",
                "保持克制，不夸大。",
                "给出适用场景说明。",
            ],
            "output": [
                "判断型钩子",
                "问题型钩子",
                "场景型钩子",
                "数据型钩子",
                "最推荐版本",
            ],
            "constraints": [
                "不写标题党。",
                "不制造虚假焦虑。",
                "钩子要能被正文支撑。",
            ],
            "tags": ["content", "writing", "marketing"],
            "pattern": "generator",
        },
        {
            "name": "flowchart-decision-builder",
            "description": "当用户提到'流程图'、'决策树'、'Mermaid'、'业务流程'、'审批规则'或需要将流程/规则转成可视化结构时触发。适用于业务流程、系统流程和审批规则。",
            "title": "流程图与决策树构建器",
            "inputs": [
                "流程描述",
                "决策条件",
                "输出格式偏好",
            ],
            "workflow": [
                "提取步骤。",
                "找出判断节点。",
                "标出输入、输出和异常路径。",
                "生成流程节点。",
                "检查是否有闭环或缺口。",
            ],
            "output": [
                "节点列表",
                "条件分支",
                "Mermaid 流程图",
                "异常路径",
            ],
            "constraints": [
                "保持节点简单。",
                "不自行添加未说明的决策条件。",
                "复杂流程先分层。",
            ],
            "tags": ["content", "diagram", "process"],
            "pattern": "generator",
        },
    ],
    "engineering-foundations": [
        {
            "name": "code-documenter",
            "description": "当用户提到'生成文档'、'代码注释'、'API 文档'、'技术文档'或需要为函数/类/模块生成文档时触发。适用于技术文档补全和知识移交。",
            "title": "代码文档生成器",
            "inputs": [
                "源代码",
                "语言和框架",
                "文档格式要求",
            ],
            "workflow": [
                "阅读代码和调用上下文。",
                "识别功能、参数、返回值和副作用。",
                "生成文档块。",
                "补正常示例和边界示例。",
                "标出潜在异常。",
            ],
            "output": [
                "文档注释",
                "使用示例",
                "参数说明",
                "返回值说明",
                "边界情况",
            ],
            "constraints": [
                "不编造代码不存在的行为。",
                "不解释显而易见的废话。",
                "示例要能运行或明确是伪代码。",
            ],
            "tags": ["engineering", "documentation", "code"],
            "pattern": "generator",
        },
        {
            "name": "unit-test-generator",
            "description": "当用户提到'写测试'、'单元测试'、'补测试'、'测试覆盖'或需要为函数/模块生成单元测试时触发。适用于 Jest、Vitest、pytest、JUnit 等测试框架。",
            "title": "单元测试生成器",
            "inputs": [
                "待测代码",
                "测试框架",
                "现有测试风格",
            ],
            "workflow": [
                "分析公开行为。",
                "识别输入、输出和异常路径。",
                "生成正常场景测试。",
                "生成边界和错误测试。",
                "如有外部依赖，设计 mock。",
            ],
            "output": [
                "测试文件",
                "测试用例说明",
                "覆盖点清单",
                "未覆盖风险",
            ],
            "constraints": [
                "测行为，不测内部实现细节。",
                "每个测试独立。",
                "不依赖执行顺序。",
            ],
            "tags": ["engineering", "testing", "quality"],
            "pattern": "generator",
        },
        {
            "name": "debug-assistant",
            "description": "当用户提到'调试'、'Bug'、'报错'、'堆栈'、'线上问题'或需要根据错误信息定位问题时触发。适用于 bug 排查和线上问题复盘。",
            "title": "调试助手",
            "inputs": [
                "错误信息",
                "堆栈",
                "相关代码",
                "运行环境",
            ],
            "workflow": [
                "解释错误表面含义。",
                "定位最可能出错位置。",
                "分析变量、类型和执行流。",
                "给出最小修复。",
                "补一条预防建议。",
            ],
            "output": [
                "现象",
                "根因候选",
                "定位证据",
                "修复方案",
                "预防建议",
            ],
            "constraints": [
                "不在上下文不足时强行下结论。",
                "多个可能原因按概率排序。",
                "不重写无关代码。",
            ],
            "tags": ["engineering", "debugging", "troubleshooting"],
            "pattern": "tool-wrapper",
        },
        {
            "name": "regex-builder-explainer",
            "description": "当用户提到'正则表达式'、'regex'、'匹配规则'、'提取文本'或需要根据自然语言需求生成正则时触发。适用于文本解析和数据提取。",
            "title": "正则表达式构建与解释器",
            "inputs": [
                "想匹配或提取的内容",
                "正则引擎",
                "示例字符串",
            ],
            "workflow": [
                "明确匹配目标。",
                "生成可读正则。",
                "分段解释。",
                "给出正例和反例。",
                "说明限制。",
            ],
            "output": [
                "正则表达式",
                "分段解释",
                "3 个匹配示例",
                "2 个不匹配示例",
                "限制说明",
            ],
            "constraints": [
                "优先可读性。",
                "不必要时不使用复杂前后查找。",
                "说明适用的正则引擎。",
            ],
            "tags": ["engineering", "regex", "text-processing"],
            "pattern": "tool-wrapper",
        },
        {
            "name": "conventional-commit-generator",
            "description": "当用户提到'提交信息'、'commit message'、'Conventional Commits'、'变更说明'或需要根据 diff 生成规范提交信息时触发。适用于代码提交和变更归档。",
            "title": "规范化提交信息生成器",
            "inputs": [
                "git diff",
                "修改文件列表",
                "变更目的",
            ],
            "workflow": [
                "判断变更类型。",
                "推断作用域。",
                "生成 72 字以内首行。",
                "必要时补正文。",
                "如变更不相关，建议拆提交。",
            ],
            "output": [
                "commit message",
                "可选正文",
                "拆分建议",
            ],
            "constraints": [
                "一个提交对应一个逻辑变更。",
                "不把功能和修复混在一起。",
                "不知道作用域时用更保守描述。",
            ],
            "tags": ["engineering", "git", "workflow"],
            "pattern": "generator",
        },
        {
            "name": "code-review-skill",
            "description": "当用户提到'代码审查'、'PR Review'、'Review'、'走查'或需要审查代码变更时触发。适用于 PR Review 和交付前检查。",
            "title": "代码审查 Skill",
            "inputs": [
                "代码 diff",
                "相关文件",
                "变更目标",
                "测试结果",
            ],
            "workflow": [
                "先理解变更意图。",
                "检查正确性和边界条件。",
                "检查安全风险和输入校验。",
                "检查兼容性和可维护性。",
                "检查测试缺口。",
                "按严重程度输出发现。",
            ],
            "output": [
                "Findings：按严重程度排序",
                "文件和行号",
                "风险说明",
                "修复建议",
                "测试缺口",
            ],
            "constraints": [
                "不做泛泛表扬。",
                "没有问题就明确说没有发现。",
                "不把风格偏好写成严重问题。",
            ],
            "tags": ["engineering", "code-review", "quality"],
            "pattern": "reviewer",
        },
        {
            "name": "workflow-automation-agent",
            "description": "当用户提到'工作流'、'自动化'、'流程编排'、'Agent 任务'或需要将复杂目标拆成可执行流程时触发。适用于流程自动化和 Agent 任务编排。",
            "title": "工作流自动化智能体",
            "inputs": [
                "目标",
                "可用工具",
                "数据源",
                "风险边界",
                "期望输出",
            ],
            "workflow": [
                "明确目标和完成标准。",
                "拆分步骤。",
                "标出每步输入和输出。",
                "映射可用工具。",
                "标出人工确认点。",
                "给出执行顺序和失败处理。",
            ],
            "output": [
                "目标定义",
                "步骤清单",
                "工具映射",
                "权限边界",
                "人工确认点",
                "验收标准",
            ],
            "constraints": [
                "不默认执行高风险动作。",
                "不把模糊目标拆成自动化流程。",
                "涉及发送、删除、付款、生产变更时要求人工确认。",
            ],
            "tags": ["engineering", "workflow", "automation", "agent"],
            "pattern": "pipeline",
        },
    ],
}


def write_skill(category: str, skill: dict):
    skill_dir = SKILLS_DIR / category / skill["name"]
    skill_dir.mkdir(parents=True, exist_ok=True)

    # SKILL.md
    skill_md = skill_dir / "SKILL.md"
    lines = [
        "---",
        f'name: {skill["name"]}',
        f'description: {skill["description"]}',
        "---",
        "",
        f'# {skill["title"]}',
        "",
        "## 适用场景",
        f'- {skill["description"].split("适用于")[-1].strip("。")}' if "适用于" in skill["description"] else "- 待补充",
        "",
        "## 输入",
    ]
    for inp in skill["inputs"]:
        lines.append(f"- {inp}")
    lines.append("")
    lines.append("## 工作流程")
    for i, step in enumerate(skill["workflow"], 1):
        lines.append(f"{i}. {step}")
    lines.append("")
    lines.append("## 输出格式")
    for out in skill["output"]:
        lines.append(f"- {out}")
    lines.append("")
    lines.append("## Gotchas")
    for c in skill["constraints"]:
        lines.append(f"- {c}")
    lines.append("")

    skill_md.write_text("\n".join(lines), encoding="utf-8")

    # meta.json
    meta = {
        "name": skill["name"],
        "version": "1.0.0",
        "pattern": skill.get("pattern", "generator"),
        "tags": skill.get("tags", []),
        "platforms": ["kimi", "claude", "cursor", "codex", "gemini"],
    }
    meta_file = skill_dir / "meta.json"
    meta_file.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    return {
        "name": skill["name"],
        "path": f"skills/{category}/{skill['name']}",
        "description": skill["description"],
        "metadata": {
            "tags": ",".join(skill.get("tags", [])),
            "platforms": ",".join(meta["platforms"]),
        },
    }


def main():
    new_entries = []
    for category, skills in categories.items():
        for skill in skills:
            entry = write_skill(category, skill)
            new_entries.append(entry)
            print(f"Created: {entry['path']}")

    # Update index.json
    with INDEX_FILE.open("r", encoding="utf-8") as f:
        index = json.load(f)

    existing_names = {s["name"] for s in index["skills"]}
    for entry in new_entries:
        if entry["name"] not in existing_names:
            index["skills"].append(entry)
            existing_names.add(entry["name"])

    index["lastUpdated"] = "2026-05-29"
    with INDEX_FILE.open("w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"\nUpdated {INDEX_FILE}")
    print(f"Total new skills added: {len(new_entries)}")


if __name__ == "__main__":
    main()
