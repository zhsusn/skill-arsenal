---
name: resume-jd-optimizer
description: 当用户拿到目标岗位JD、需要分析匹配度并据此优化简历时触发。执行JD分析→匹配评分→定向改写→关键词植入的端到端流程。
---

# Resume-JD Optimizer

## 适用场景

- 用户拿到目标岗位 JD，需要分析匹配度并优化简历
- 用户问"这个岗位我合适吗""帮我改简历投这个岗位"
- 用户需要计算与目标岗位的匹配分数
- 用户想针对特定 JD 定制简历版本

## 端到端流程

```
JD 文本输入 → 提取要求 & 关键词 → 计算匹配分 & 识别 Red Flags
                                              ↓
                                    生成优化策略
                                              ↓
简历输入 → 定向改写（Reorder / Reword / 关键词植入）→ 输出定制简历 + 变更摘要
```

### 阶段1：JD 分析

#### 1.1 需求分类提取

将 JD 拆分为三类要求：

| 类型 | 说明 | 示例 |
|------|------|------|
| **Required（必须）** | 不满足则直接过滤 | 学历、年限、特定技术栈、证书 |
| **Preferred（加分）** | 提升竞争力 | 高级证书、领域经验、特定工具 |
| **Soft/Culture（文化）** | 决定面试通过后的适配 | 沟通风格、团队结构、公司价值观 |

**识别 Required 的语言信号：**
- "Must have..."、"Required: X years..."、"Essential qualifications"
- 在 JD 中出现 3 次以上

**识别 Preferred 的语言信号：**
- "Nice to have..."、"Bonus if..."、"A plus if..."
- 在 JD 中仅出现 1-2 次

#### 1.2 关键词提取

识别三类关键词：

- **Hard Skills**：工具（Python, AWS, Salesforce）、方法论（Agile, Six Sigma）、证书（PMP, CPA）
- **Soft Skills**：领导力、沟通、问题解决、适应性
- **Domain Knowledge**：B2B SaaS、医疗、金融科技、合规（HIPAA, GDPR）

#### 1.3 Red Flags 检测

扫描 JD 中的警告信号：

| 类别 | Red Flags | 含义 |
|------|-----------|------|
| **工作负荷** | "Wear many hats"、"Hit the ground running"、"Self-starter in ambiguous situations" | 职责边界模糊、可能加班 |
| **文化问题** | "Rockstar/Ninja/Guru"、"We work hard, play hard"、"Like a family" | 过度加班文化、不专业管理 |
| **薪酬不透明** | "Competitive salary" 无范围、"Equity-heavy" 无底薪、仅写 "DOE" | 可能压低薪资 |

**正向信号：**
- JD 描述详细、结构化 → 公司目标清晰
- 提及具体工具（JIRA, Amplitude）→ 运营成熟
- 提到混合办公/弹性工作 → 现代管理

### 阶段2：匹配评分

#### 2.1 计算逻辑

```
Required Skills 匹配率：8/10 = 80%
Preferred Skills 匹配率：3/5 = 60%

Overall Match = Required × 0.7 + Preferred × 0.3
              = 80% × 0.7 + 60% × 0.3 = 74%
```

#### 2.2 匹配分解读

| 分数区间 | 含义 | 建议 |
|----------|------|------|
| 90-100% | 过度匹配（可能被当做过高资历） | 可投，但简历中适当降级表述 |
| 75-89% | 优秀匹配 | **立即投递**，优先级最高 |
| 60-74% | 良好匹配 | 投递，用 Cover Letter 弥补 gaps |
| 50-59% | 有挑战性 | 仅当非常感兴趣时投递 |
| <50% | 明显不匹配 | 建议跳过，除非 dream job |

#### 2.3 Gap 分析

对每项缺失要求分类：

- **Critical Gap**：一票否决项（无医疗执照、无安全许可）→ **不建议投递**
- **Major Gap**：显著但可解释（缺少 SQL 经验）→ 在 Cover Letter 中主动说明
- **Minor Gap**：容易补齐或不影响核心（缺移动端经验）→ 忽略或在面试中转移话题

### 阶段3：简历定向改写

**核心原则：** 不编造、不撒谎——只**突出**与目标岗位最相关的真实经历。

#### 3.1 专业总结（Professional Summary）定制

按目标角色重写"电梯演讲"，直接回应 JD 的核心要求。

**错误示例（通用）：**
> Results-driven professional with 5 years of experience in business operations. Strong analytical and communication skills.

**正确示例（投运营经理岗）：**
> Operations Manager with 5 years optimizing supply chain processes and reducing costs by 25%. Expertise in Lean Six Sigma, vendor management, and cross-functional team leadership.

**正确示例（投项目经理岗，同一个人）：**
> Project Manager with 5 years leading cross-functional initiatives from concept to delivery. PMP-certified with expertise in Agile methodology, stakeholder management, and budget oversight.

#### 3.2 经历重新排序（Reorder）

按**与目标岗位的相关性**排序，而非时间顺序。

**示例：** 申请数据岗，但最近一份是市场协调员：
- 排序前：1. Marketing Coordinator（当前） → 2. Data Analyst（过往）
- 排序后：1. Data Analyst（移至顶部，标注日期） → 2. Marketing Coordinator（次要）

#### 3.3 Bullet 点调整

**策略 A：调整 bullet 顺序**
- 投管理岗 → 先放 "Led team of 12..."、"Managed budget of $2M..."
- 投技术岗 → 先放 "Developed automated system..."、"Analyzed 500K+ data points..."

**策略 B：改写 bullet 语言**
在保持真实的前提下，引入 JD 关键词。

| JD 原文 | 原 bullet | 优化后 bullet |
|---------|-----------|---------------|
| stakeholder management | Worked with various teams | Managed stakeholder relationships across 5 departments, ensuring alignment on project priorities |

**策略 C：量化增强**
将模糊表述改为数据驱动：

- 优化前："Led product roadmap"
- 优化后："Defined product roadmap based on analysis of 50+ customer interviews and usage data from 100K+ users"

### 阶段4：关键词植入与验证

#### 4.1 技能区重排与补全

**示例：** JD 强调 Data analysis, SQL, Python, Stakeholder communication

- 优化前：`Microsoft Office, Communication, Project Management, Python, SQL, Data Visualization, Leadership`
- 优化后：`SQL, Python, Data Analysis, Data Visualization, Stakeholder Communication, Project Management, Microsoft Office`

#### 4.2 关键词植入规则

**DO：**
- 仅在真实掌握的技能上使用 JD 关键词
- 使用 JD 中的**精确措辞**（如果准确）
- 将关键词自然嵌入上下文
- 在多个区域重复关键关键词（总结、技能、经历）

**DON'T：**
- 添加不具备的技能
- 关键词堆砌（同一词重复 10 次）
- 改变实际经历的真实含义
- 为关键词密度牺牲可读性

#### 4.3 可接受 vs 不可接受的边界

| ✅ 可接受 | ❌ 不可接受（撒谎） |
|-----------|---------------------|
| 重新排序真实信息 | 添加不具备的技能 |
| 强调相关经历 | 修改数字或指标 |
| 使用行业标准术语 | 编造虚假经历 |
| 为模糊表述增加上下文 | 声称未担任过的职位 |
| 匹配 JD 的语言风格 | 声称未获得的证书 |

## 输出格式

完成分析+优化后，输出以下结构：

```markdown
# JD 分析与简历优化报告

## 目标岗位：[职位] @ [公司]

### 一、匹配评分
- **Overall Match**: X%
- **Required**: X/Y ✅/❌
- **Preferred**: X/Y ✅/❌
- **建议**: [立即投递 / 可投递 / 不建议]

### 二、Red Flags 扫描
- [列出检测到的 red flags 或 "无重大风险"]

### 三、Gaps 分析
- **Critical**: [无 / 具体项]
- **Major**: [具体项 + 应对策略]
- **Minor**: [具体项 + 应对策略]

### 四、简历优化摘要

#### 专业总结
- **Before**: [原文]
- **After**: [优化版]
- **植入关键词**: [列表]

#### 经历调整
- **[公司] - [职位]**
  - 排序变化：[移至顶部 / 保持]
  - Bullet 调整：[具体修改]
  - 新增关键词：[列表]

#### 技能区
- **新排序**: [列表]
- **新增**: [从 JD 提取的关键词]
- **移除**: [如需腾空间]

### 五、投递前检查清单
- [ ] 总结中提到了目标职位关键词
- [ ] Top 5 技能与 JD Top 5 要求对齐
- [ ] 最相关经历排在首位
- [ ] 每段经历的第一个 bullet 回应 JD 核心要求
- [ ] JD 关键词自然分布在全文
- [ ] 所有声明均为真实
- [ ] 文件名已规范命名（例：Smith_Resume_PM_TechCorp_2024.pdf）
```

## Gotchas

1. **不要帮用户撒谎**：可以重新排序、强调、换词，但绝不能编造经历、技能、证书或数据。用户要对自己的简历真实性负全责。

2. **JD 分析≠阅读理解**：不要机械地逐句翻译 JD，而要识别出真正的筛选标准（Required vs Preferred），避免用户因"看到 10 条要求就放弃"而错失机会。

3. **匹配分仅供参考**：70% 的匹配分不代表 70% 的概率拿到 offer。投递时机、内推、Cover Letter 质量同样关键。不要让用户过度依赖分数做决策。

4. **避免关键词堆砌到可读性崩塌**：ATS 扫描只是第一道关卡，最终简历要过的是 HR 和用人经理的眼睛。保留自然语言流畅度。

5. **版本管理是用户的事**：AI 只能输出"优化后的版本"，用户需要自己保存 Master Resume（完整版源文件）和各定向版本。建议命名格式：`[LastName]_Resume_[Role]_[Company]_[Date].pdf`。

6. **Vague JD 的处理**：如果 JD 极其模糊（如只写"负责相关工作"），标记为 Red Flag，建议用户在投递前通过 LinkedIn 或招聘方确认具体职责，避免入职后职责不符。

7. **覆盖验证**：输出优化版后，必须回溯 JD 中的核心关键词，确认每一项都在简历中至少出现一次（除用户确实不具备的技能外）。这一步防止 AI 幻觉性遗漏。

8. **有状态场景**：如果用户需要针对同一 JD 反复迭代多轮优化，建议用户保存 tailoring notes（记录每次改了什么），用于后续面试准备。

9. **多个 JD 同时优化**：优先让用户选 1-2 个最匹配的岗位深度定制，而非对 10+ 个岗位泛泛修改。质量 > 数量。

10. **Cover Letter 不是本 Skill 的核心职责**：本 Skill 输出"简历优化"为主。如用户需要 Cover Letter，可在简历优化完成后提供 2-3 个 talking points 作为附加输出，但不应展开完整撰写。
