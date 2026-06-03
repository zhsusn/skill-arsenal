---
name: resume-ats-formatter
description: 当用户提到'ATS优化'、'简历格式'、'简历排版'、'机器筛选'或需要确保简历通过ATS系统时触发。提供格式兼容性检查、关键词匹配度分析与ATS友好排版建议。
---

# Resume ATS Formatter

## 适用场景

- 优化简历以通过 Applicant Tracking Systems (ATS)
- 检查简历格式是否会被机器解析错误
- 分析简历与职位描述的关键词匹配度
- 排版混乱、难以阅读，需要专业格式整理
- 用户提及："ATS"、"简历优化"、"机器筛选"、"简历格式"、"简历排版"

## 核心能力

- ATS 格式兼容性检查（文件格式、字体、布局、解析风险）
- 关键词提取与匹配度评分
- ATS 安全排版规则与布局建议
- 提供修改前后的对比与重评分

## ATS 兼容性检查

### 文件格式

- ✅ 使用 `.docx` 或文本型 `.pdf`（非扫描件）
- ❌ 避免 `.pages`、`.odt`、图片型 PDF
- ✅ 文件名：`FirstName_LastName_Resume.pdf`
- ❌ 避免：`resume_final_v2_FINAL.docx`

### 字体与排版

- ✅ 标准字体：Arial、Calibri、Georgia、Times New Roman、Helvetica、Verdana
- ✅ 字号：正文 10–12pt，标题 12–14pt，姓名 16–20pt
- ✅ 行距 1.0–1.15，段后间距 6–12pt，章节间距 12–16pt
- ❌ 禁用文本框、表格、多栏布局、页眉页脚
- ❌ 禁用图片、图表、技能条、进度指示器、表情符号

### 章节标题

使用 ATS 可识别的标准标题：

- `PROFESSIONAL EXPERIENCE` / `WORK EXPERIENCE`
- `EDUCATION`
- `SKILLS` / `TECHNICAL SKILLS`
- `PROFESSIONAL SUMMARY` / `SUMMARY`
- `CERTIFICATIONS`
- `PROJECTS`

❌ 避免创意标题：`My Journey`、`What I Bring to the Table`

### 联系方式布局

```
JOHN SMITH
john.smith@email.com | (555) 123-4567 | linkedin.com/in/johnsmith
San Francisco, CA
```

- ✅ 放在正文，不要放在页眉/页脚
- ✅ 包含：姓名、邮箱、电话、城市/州、LinkedIn
- ❌ 排除：完整街道地址、照片、出生日期、婚姻状况、多个电话

## ATS 安全布局规则

### 页面与边距

- **初级（0–5 年）：** 1 页
- **中级（5–15 年）：** 1–2 页
- **高级/高管（15+ 年）：** 2 页（高管最多 3 页）
- **边距：** 0.5"–1"，四边一致

### 视觉层级

1. **姓名** — 最大、最醒目
2. **章节标题** — 清晰分隔
3. **职位/公司名** — 易于扫描
4. **项目符号** — 细节内容

- 用字号大小建立层级
- 用 **粗体** 强调（姓名、职位、标题）
- 用全大写表示章节标题
- 保持间距一致

### 工作经历格式

```
COMPANY NAME | City, ST
Job Title | Month Year - Month Year

• Achievement bullet with metrics and results
• Achievement bullet with metrics and results
```

- 日期格式统一：`Jan 2020 - Present` 或 `MM/YYYY`
- 项目符号长度 1–2 行，以动词开头、结果结尾
- 每段经历 3–6 条 bullet（近期多写，早期少写）

### 技能章节格式

**推荐：简单列表**
```
SKILLS
Python, JavaScript, SQL, React, Node.js, AWS, Docker, Git, Agile, JIRA
```

**可选：分类列表**
```
TECHNICAL SKILLS
Languages: Python, JavaScript, TypeScript, SQL
Frameworks: React, Node.js, Django
Tools: AWS, Docker, Kubernetes, Git
```

⚠️ 多栏技能布局可能导致 ATS 解析错误，慎用。

### 教育章节格式

```
EDUCATION
Bachelor of Science in Computer Science
University of California, Berkeley | 2018
GPA: 3.8/4.0（3.5+ 可写）
```

## 关键词匹配度分析

### Step 1：提取职位描述关键词

分类三类关键词：

**硬技能（技术）**
- 编程语言（Python、Java、SQL）
- 工具与平台（Salesforce、AWS、Excel）
- 认证（PMP、CPA、CFA）
- 方法论（Agile、Six Sigma、SDLC）

**软技能**
- 领导力、协作、沟通
- 问题解决、分析思维
- 项目管理、利益相关者管理

**行业术语**
- B2B、SaaS、e-commerce
- Enterprise、SMB
- ARR、MRR、churn rate

### Step 2：匹配分析

对每个职位关键词：
1. 检查简历中是否有完全匹配的短语
2. 检查同义词或变体
3. 统计出现频率
4. 记录所在位置（Summary、Experience、Skills）

### Step 3：计算匹配分数

```
Match Score = (Keywords Matched / Total Required Keywords) × 100

目标：80%+ 为强匹配
```

### Step 4：关键词放置策略

**优先级 1：Professional Summary（简历顶部）**
- 包含 5–8 个最重要的关键词
- 自然融入 3–4 句话
- 示例："Data Scientist with 5+ years using Python, SQL, and machine learning..."

**优先级 2：Skills Section**
- 明确列出关键词
- 使用职位描述中的确切措辞

**优先级 3：Experience Bullets**
- 将关键词融入成就陈述
- 不要生硬堆砌

**关键词密度指南：**
- 核心关键词：出现 2–4 次
- 重要关键词：出现 1–2 次
- 保持自然，避免 keyword stuffing

## 分析报告输出格式

```markdown
# ATS 兼容性分析报告

## 综合评分：[X]/100

### 文件格式检查 ✅/❌
- 格式：[DOCX/PDF]
- 文本提取：[成功/失败]
- 文件大小：[X KB/MB]

### 格式问题
✅ 未检测到表格或分栏
❌ 联系方式在页眉（请移至正文）
⚠️ 技能章节混用两种字号

### 关键词分析

**关键关键词（必须包含）：**
✅ Project Management — 出现 3 次
✅ Agile/Scrum — 出现 2 次
❌ Stakeholder Management — 缺失（JD 中出现 5 次）

**重要关键词：**
✅ Cross-functional teams — 出现 1 次
⚠️ "Risk management" — 你写的是 "risk mitigation"（接近但不完全匹配）

**匹配分数：65%**
建议目标：80%+

### 修改建议

**1. 补充缺失关键词：**
在 Professional Summary 中：
"Experienced project manager with proven track record in stakeholder management and budget oversight..."

在 Experience 中添加：
"Managed stakeholder communication across 3 departments"
"Directed budget management for $2.5M project portfolio"

**2. 修复格式问题：**
- 将联系方式从页眉移至正文
- 统一技能章节的字号

**3. 强化现有关键词：**
将 "risk mitigation" 改为 "risk management" 以达成精确匹配

### 预计优化后匹配分数：85%
```

## 常见排版错误

| 错误 | 问题 | 解决方案 |
|------|------|----------|
| 文字墙 | 密集段落无 bullet | 使用 bullet，段落简短 |
| 格式不统一 | 不同字体、字号混用 | 选定一种格式并坚持 |
| 过度设计 | 花哨设计破坏 ATS | 创意留给作品集，简历保持简洁 |
| 信息过载 | 强行塞满一页 | 无情删减，优先相关性 |
| 信息不足 | 半页简历+巨大边距 | 补充细节，边距减至 0.5" |
| 表格排版 | ATS 无法解析 | 使用简单 bullet 和纯文本 |
| 多栏布局 | 解析顺序错乱 | 单栏布局 |

## 行业特定建议

### 技术岗位
- 强调编程语言和框架
- GitHub、作品集链接放在 Skills 区（非页眉）
- 认证和在线课程权重高

### 商业/金融
- 强调软件熟练度（Excel、SAP、Salesforce）
- 认证关键（CPA、CFA、PMP）
- 行业关键词（P&L、ROI、KPI）

### 医疗
- 执照和认证必须列出
- 特定系统（Epic、Cerner、MEDITECH）
- 合规关键词（HIPAA、Joint Commission）

### 市场营销
- 平台专长（HubSpot、Google Analytics）
- 渠道关键词（SEO、PPC、email marketing）
- 结果导向的语言

## 特殊情况处理

### 转行者
- 聚焦可迁移技能
- 使用目标行业的关键词
- 可能需要两份 ATS 版本

### 应届毕业生
- 教育章节成为关键词重点
- 包含相关课程和项目
- 实习经验算工作经历

### 就业空窗期
- 可仅写年份（省略月份）
- 用自由职业/咨询填补并嵌入关键词
- 志愿工作也可包含相关关键词

## 实施检查清单

1. ✅ 扫描当前简历的 ATS 兼容性问题
2. ✅ 分析职位描述中的必要关键词
3. ✅ 计算当前匹配分数
4. ✅ 识别具体缺失的关键词
5. ✅ 建议关键词的精确放置位置
6. ✅ 标记格式问题
7. ✅ 提供修改前后对比示例
8. ✅ 重新评分预估
9. ✅ 确认文件格式和命名
10. ✅ 用 ATS 模拟器测试（如可用）

## Gotchas

- **双受众陷阱**：简历必须同时满足 ATS 机器解析和人类快速扫描。不要为了追求美观而牺牲解析正确性。
- **PDF 不是万能的**：很多 ATS 对 PDF 的解析效果不如 DOCX。除非职位明确要求 PDF，否则优先提交 `.docx`。
- **精确匹配 > 同义词**：ATS 通常搜索精确短语。如果 JD 写 "project management"，写 "project coordination" 可能匹配失败。
- **多栏灾难**：多栏布局在视觉上节省空间，但 ATS 可能按错误顺序读取内容（如先读左栏所有行，再读右栏），导致工作经历顺序混乱。
- **页眉页脚隐形**：放在页眉/页脚的联系方式、页码、日期等关键信息，许多 ATS 会直接丢弃，导致联系不上候选人。
- **表格的暧昧**：即使 "简单表格" 也存在风险。有些 ATS 能解析表格，有些会跳过或打乱顺序。最安全的做法是避免任何表格结构。
- **关键词堆砌惩罚**：过度重复同一关键词会被一些高级 ATS 标记为 spam，并可能触发人工审核的负面印象。保持自然语言。
- **格式与内容冲突**：当优化格式（如调整 bullet 长度）与嵌入关键词冲突时，优先确保关键词的自然出现，其次才是视觉完美。
- **不同 ATS 差异大**：Workday、Greenhouse、Lever 等系统解析能力不同。没有绝对 "100% 通过" 的简历，只能最大化兼容性。
