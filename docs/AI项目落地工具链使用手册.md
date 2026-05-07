AI项目落地工具链使用手册
工具集成方式 + 完全手动方式完整指南
版本 V2.0 | 2026年5月
目录
一、系统要求与环境准备
二、工具集成方式（MCP Server模式）
三、完全手动方式（无MCP Server）
四、常见问题与排除
一、系统要求与环境准备
1.1 必备工具
表格
工具	作用	安装方式
Kimi Code	AI 编程引擎，提供智能决策和代码生成	kimi.com/code 下载
OpenSpec	规格驱动开发框架，管理变更生命周期	npm i -g @fission-ai/openspec
Superpowers	AI 编码技能框架，提供结构化工作流	GitHub 克隆
1.2 目录结构初始化
在开始使用之前，需要创建以下目录结构：
bash
复制
# OpenSpec 核心目录
mkdir -p openspec/{specs,changes,archive,schemas/{项目名}/templates}

# Superpowers Skill 目录
mkdir -p .kimi/skills/

# AI 产出物目录
mkdir -p docs/ai-output

# 测试目录
mkdir -p tests/{unit,integration}
1.3 Skill 安装清单
安装以下 Skill，本方案共需要 18 个 Skill：
表格
Skill名称	来源	安装路径
brainstorming	Superpowers	.kimi/skills/superpowers/
writing-plans	Superpowers	.kimi/skills/superpowers/
executing-plans	Superpowers	.kimi/skills/superpowers/
tdd	Superpowers	.kimi/skills/superpowers/
systematic-debugging	Superpowers	.kimi/skills/superpowers/
requesting-code-review	Superpowers	.kimi/skills/superpowers/
finish	Superpowers	.kimi/skills/superpowers/
prd-generation	本方案	.kimi/skills/prd-generation/
progress-tracker	本方案	.kimi/skills/progress-tracker/
self-check	本方案	.kimi/skills/self-check/
二、工具集成方式（MCP Server模式）
2.1 三工具打通前提条件
工具集成方式需要满足以下前提条件：
MCP 协议支持： Kimi Code 支持 MCP Client 模式，能够通过 MCP 协议与外部服务通信。
OpenSpec MCP Server： OpenSpec 提供 MCP Server，暴露 propose、apply、archive、verify 等 tools。
Superpowers MCP Server： Superpowers 提供 MCP Server，暴露 brainstorming、writing-plans、executing-plans、tdd 等 tools。
配置文件： openspec/config.yaml 已创建并配置完毕。
2.2 完整工作流程
在工具集成模式下，整个工作流程如下：
初始化 —— 通过 progress-tracker 初始化项目目录和配置文件
变更提案 —— 使用 /opsx:propose 创建变更提案
需求探索 —— 调用 brainstorming 进行需求探索
市场定位 —— 调用 competitive-analysis mode=positioning 执行市场定位与差异化分析
概要需求 —— 调用 prd-generation 生成概要需求文档
详细需求 —— 调用 detailed-requirements 生成模块化详细需求
技术竞品分析 —— 调用 competitive-analysis mode=technical 执行技术深度对比
概要设计 —— 调用 high-level-design 生成系统架构设计
详细设计 —— 调用 detailed-design 生成模块级详细设计
接口驱动 —— 调用 interface-first-dev 定义前后端接口契约
任务拆解 —— 调用 task-breakdown 将工作拆解为≤30分钟/任务
编码实现 —— 调用 executing-plans + tdd 执行开发任务
单元测试 —— 调用 unit-test 生成并执行单元测试（覆盖率≥70%）
集成测试 —— 调用 integration-test 生成并执行集成测试
归档收尾 —— 调用 OpenSpec 的 archive + Superpowers 的 requesting-code-review
2.3 各阶段操作指令
阶段 0：初始化项目
bash
复制
# 初始化 OpenSpec 目录结构
npx @fission-ai/openspec@latest init

# 初始化项目配置
/skill:progress-tracker 初始化项目目录
阶段 1：创建变更提案
bash
复制
/opsx:propose "描述你的变更需求"
产出：openspec/changes/{变更名}/proposal.md
阶段 1：需求探索
bash
复制
# 调用 Superpowers 的 brainstorming
/skill:brainstorming 请读取变更提案：@openspec/changes/{变更名}/proposal.md
在此基础上进行需求探索。资料来源：自动搜索网络 + 读取本地项目文档
阶段 1.5：市场定位分析（可选但推荐）
bash
复制
# 调用 competitive-analysis 的 positioning 模式
/skill:competitive-analysis mode=positioning 请基于需求探索结果，执行市场定位竞品分析。

分析目标：{基于需求草案中的模块初分}
问题类型：market_entry | positioning
参考文档：@openspec/changes/{变更名}/brainstorming/requirement-draft.md

产出：openspec/changes/{变更名}/brainstorming/market-positioning.md
阶段 2：生成概要需求
bash
复制
# 调用 prd-generation
/skill:prd-generation 基于 brainstorming 结果，生成概要需求。
参考文档：@openspec/changes/{变更名}/proposal.md
产出：specs/ 目录下的 5 个 Markdown 文件：01-product-overview.md、02-requirements-list.md、03-functional-structure.md、04-business-rules.md、05-non-functional.md
阶段 2.5：生成详细需求
bash
复制
# 调用 detailed-requirements
/skill:detailed-requirements 基于概要需求，按模块独立输出详细需求。
从 P0 模块开始，逐个模块输出。
阶段 3 前置：技术竞品分析
bash
复制
# 调用 competitive-analysis 的 technical 模式
/skill:competitive-analysis mode=technical 请自动搜索相关竞品，执行技术深度对比分析。

分析维度：角色数据模型设计、核心功能流程、技术选型、集成方式
参考文档：@openspec/changes/{变更名}/specs/

产出：openspec/changes/{变更名}/design/competitive-analysis.md
openspec/changes/{变更名}/design/design-input.md
阶段 3：概要设计
bash
复制
# 调用 high-level-design 生成概要设计
/skill:high-level-design 生成概要设计。
参考文档：@openspec/changes/{变更名}/specs/
@openspec/changes/{变更名}/design/competitive-analysis.md
@openspec/changes/{变更名}/design/design-input.md
阶段 4：详细设计
bash
复制
/skill:detailed-design 按模块输出详细设计。
参考文档：@openspec/changes/{变更名}/design/
@openspec/changes/{变更名}/specs/feature-*/
阶段 5：接口驱动开发
bash
复制
/skill:interface-first-dev 基于详细设计定义前后端接口契约。
生成：OpenAPI/Swagger + Mock数据 + 并行开发计划
阶段 6：任务拆解
bash
复制
/skill:task-breakdown 基于详细设计和接口契约，生成开发任务清单。
原则：每个任务 ≤ 30 分钟
阶段 7：编码实现
bash
复制
/skill:executing-plans 按 tasks.md 逐个执行任务。
约束：符合项目编码规范 + 包含异常处理 + 完成后自测
阶段 8：单元测试
bash
复制
/skill:unit-test 为已完成的模块生成单元测试。
要求：覆盖率 ≥ 70%，独立运行
阶段 9：集成测试
bash
复制
/skill:integration-test 生成集成测试，覆盖端到端主链路场景。
阶段 10：归档收尾
bash
复制
# 代码审查
/skill:requesting-code-review

# 归档变更
/opsx:archive

# 最终自查
/skill:self-check
三、完全手动方式（无MCP Server）
3.1 手动方式说明
当 MCP Server 不可用时（网络不通、服务未部署或权限不足），可以通过手动方式按顺序执行命令。手动方式的核心原则是：
每个命令按固定顺序执行，不能跳过或并行
每个命令的输出作为下一个命令的输入
每个阶段完成后需要人工确认后才能进入下一阶段
自查环节必不可少，确保产出物质量
3.2 完整命令执行流程
表格
步骤	命令	说明	产出物
0	progress-tracker	初始化目录结构	config.yaml
1	/opsx:propose	创建变更提案	proposal.md
1	brainstorming	需求探索	探索记录
1.5	competitive-analysis	市场定位分析（可选）	market-positioning.md
2	prd-generation	生成概要需求	01-05.md
2.5	detailed-requirements	生成详细需求	feature-*/
3 前置	competitive-analysis	技术竞品分析	competitive-analysis.md + design-input.md
3	high-level-design	概要设计	design/*.md
4	detailed-design	详细设计	feature-*/design.md
5	interface-first-dev	接口驱动	openapi.yaml
6	task-breakdown	任务拆解	tasks.md
7	executing-plans	编码实现	代码文件
8	unit-test	单元测试	tests/unit/
9	integration-test	集成测试	tests/integration/
10	archive	归档收尾	archive/
3.3 各阶段详细命令列表
步骤 0：初始化变更目录
bash
复制
# 1. 创建目录结构
mkdir -p openspec/{specs,changes,archive}
mkdir -p openspec/changes/{变更名}/{specs,design}
mkdir -p .kimi/skills/
mkdir -p docs/ai-output
mkdir -p tests/{unit,integration}

# 2. 创建配置文件 openspec/config.yaml
cat > openspec/config.yaml << 'EOF'
schema: {项目名}-sdd
version: "1.0"
context: |
  项目：{项目名称}
  技术栈：{前端框架} + {后端框架} + {数据库}
  规范：所有变更必须通过概要评审和详细评审
EOF

# 3. 初始化进度跟踪
/skill:progress-tracker 初始化{项目名}项目目录
步骤 1：创建变更提案
bash
复制
/opsx:propose "{变更描述}"
说明：创建 openspec/changes/{变更名}/proposal.md，包含变更背景、目标、范围、关联模块等信息。
步骤 1：需求探索
bash
复制
/skill:brainstorming 帮我脑暴一下，打算做个{产品描述}，
本地资料：@docs/ref/*.md

/skill:progress-tracker 请更新进度
说明：进行苏格拉底式提问，理清核心需求。输出为需求探索记录。
步骤 1.5：市场定位分析（可选但推荐）
bash
复制
/skill:competitive-analysis mode=positioning 请基于需求探索结果，执行市场定位竞品分析。

分析目标：{基于需求草案中的模块初分}
问题类型：market_entry | positioning
参考文档：@openspec/changes/{变更名}/brainstorming/requirement-draft.md

/skill:progress-tracker 请更新进度
说明：从 JTBD、Blue Ocean、颠覆向量等维度分析竞争格局与差异化空间。
输出：openspec/changes/{变更名}/brainstorming/market-positioning.md
步骤 2：生成概要需求
bash
复制
/skill:prd-generation 基于 brainstorming 结果生成概要需求。
参考文档：@openspec/changes/*/proposal.md @docs/*/*

/skill:progress-tracker 请更新进度

/skill:self-check 概要需求
输出：specs/ 目录下的 5 个 Markdown 文件。
步骤 2.5：生成详细需求
bash
复制
/skill:detailed-requirements 基于概要需求，按模块输出详细需求。
参考文档：@openspec/changes/{变更名}/specs/01-*.md
@openspec/changes/{变更名}/specs/03-*.md

/skill:progress-tracker 请更新进度
输出：每个模块一个独立目录 feature-XX-{模块名}/，包含 spec.md、prototype.md、io-table.md、logic.md。
步骤 3 前置：技术竞品分析
bash
复制
/skill:competitive-analysis mode=technical 请自动搜索相关竞品，执行技术深度对比分析。

分析维度：角色数据模型设计、核心功能流程、技术选型、集成方式
参考文档：@openspec/changes/{变更名}/specs/
@openspec/changes/{变更名}/brainstorming/market-positioning.md（如有）

/skill:progress-tracker 请更新进度
说明：按四维模型执行结构化技术对比，输出 competitive-analysis.md 和 design-input.md。
输出：openspec/changes/{变更名}/design/competitive-analysis.md
openspec/changes/{变更名}/design/design-input.md
步骤 3：概要设计
bash
复制
/skill:high-level-design 生成概要设计。
参考：@openspec/changes/{变更名}/specs/
@openspec/changes/{变更名}/design/competitive-analysis.md
@openspec/changes/{变更名}/design/design-input.md

/skill:self-check 概要设计
输出：design/ 目录下的 16 个 Markdown 文件（按 required_sections 配置）。
步骤 4：详细设计
bash
复制
/skill:detailed-design 按模块输出详细设计。
参考：@openspec/changes/{变更名}/design/
@openspec/changes/{变更名}/specs/feature-*/

/skill:self-check 详细设计
输出：每个模块目录下增加 design.md、api-spec.md、db-schema.md、state-machine.md、test-plan.md。
步骤 5：接口驱动开发
bash
复制
/skill:interface-first-dev 基于详细设计定义前后端接口契约。
参考：@openspec/changes/{变更名}/specs/feature-*/api-spec.md
@openspec/changes/{变更名}/specs/feature-*/db-schema.md

/skill:self-check 接口契约
输出：interface-contracts/ 目录下的 openapi.yaml、mock-data.json、mock-server-config.md、parallel-dev-plan.md。
步骤 6：任务拆解
bash
复制
/skill:task-breakdown 基于详细设计和接口契约，生成开发任务清单。
参考：@openspec/changes/{变更名}/specs/feature-*/design.md
@openspec/changes/{变更名}/interface-contracts/openapi.yaml
输出：openspec/changes/{变更名}/tasks.md，按 Phase 组织，每个任务 ≤ 30 分钟。
步骤 7：编码实现
bash
复制
# 对每个任务执行：
/skill:executing-plans 执行任务 {任务ID}。
参考：@openspec/changes/{变更名}/tasks.md
@openspec/changes/{变更名}/specs/feature-*/design.md
@openspec/changes/{变更名}/specs/feature-*/api-spec.md
约束：符合项目编码规范 + 包含异常处理 + 完成后自测

# 每个任务完成后：
/skill:self-check 编码任务
说明：逐个执行 tasks.md 中的任务，每个任务完成后必须自测通过。
步骤 8：单元测试
bash
复制
/skill:unit-test 为已完成的模块生成单元测试。
参考：@openspec/changes/{变更名}/specs/feature-*/test-plan.md
@openspec/changes/{变更名}/specs/feature-*/logic.md

# 运行单元测试
pytest tests/unit/ -v --cov={模块路径} --cov-report=term-missing

/skill:self-check 单元测试
要求：覆盖率 ≥ 70%，测试独立运行。
步骤 9：集成测试
bash
复制
/skill:integration-test 生成集成测试。
参考：@openspec/changes/{变更名}/specs/feature-*/spec.md
@openspec/changes/{变更名}/interface-contracts/openapi.yaml

/skill:self-check 集成测试
要求：覆盖端到端主链路场景。
步骤 12：归档收尾
bash
复制
/skill:requesting-code-review 对已完成的代码进行审查。
参考：@openspec/changes/{变更名}/tasks.md

/opsx:archive

# 最终自查
/skill:self-check 最终自查
说明：归档变更目录到 archive/，更新 specs/ 目录。
四、常见问题与排除
4.1 工具集成方式常见问题
Q1：MCP Server 连接失败怎么办？
A：检查网络连接，确认 MCP Server 已启动。可以使用命令 mcp inspector 进行诊断。如果仍然不能解决，切换到完全手动方式。
Q2：Skill 识别不到怎么办？
A：检查 Skill 目录是否正确，确认 SKILL.md 文件存在。尝试重启 Kimi Code 或重新加载 Skill。
Q3：产出物保存路径错误怎么办？
A：检查 openspec/config.yaml 中的 auto_save.base_path 配置，确认目录权限正确。
4.2 手动方式常见问题
Q1：可以跳过某些阶段吗？
A：不建议。每个阶段的产出物都是下一个阶段的输入，跳过会导致产出物质量下降。特殊情况下可以简化某个阶段，但不建议完全跳过。
Q2：自查失败怎么办？
A：根据自查报告修复问题，修复后重新执行自查。如果是内容不一致问题，需要回到上游阶段修复。
Q3：多个变更可以并行进行吗？
A：不建议。手动方式下应该一次只处理一个变更，避免上下文混淆。
4.3 通用问题
Q1：如何切换两种方式？
A：在工具集成方式下，如果 MCP Server 不可用，系统会自动提示切换到手动方式。也可以通过命令 /mode:manual 手动切换。
Q2：两种方式的产出物兼容吗？
A：兼容。两种方式产生的文档格式和目录结构完全一致，可以在任何时候切换。
Q3：需要多少人工干预？
A：主要在以下节点需要人工确认：概要需求评审签字、详细需求确认、架构评审、代码审查。其他环节由 AI 自主完成。
AI项目落地工具链 | V2.0