我仔细审阅了这两份文档，从项目周期覆盖度、人工参与节点、功能验证机制、高风险环节四个维度进行系统检查。以下是完整分析：
一、项目周期覆盖度检查
1.1 当前覆盖的阶段
表格
阶段	文档中的对应环节	覆盖状态
需求	变更提案 → brainstorming → 竞品分析 → 概要需求 → 详细需求	✅ 完整
设计	概要设计 → 详细设计 → 接口契约	✅ 完整
开发	任务拆解 → 编码实现（TDD）	✅ 完整
测试	单元测试 → 集成测试	⚠️ 部分缺失
交付	代码审查 → 归档	❌ 严重不足
运维	无	❌ 完全缺失
1.2 明显缺失的环节
（1）用户验收测试（UAT）
文档中的"集成测试"是技术层面的端到端测试，但缺少业务层面的用户验收。即：产品经理/业务方是否认可这个功能？是否满足实际业务场景？
（2）预发布与灰度验证
没有部署到预发布环境（Staging）进行真实业务流程走通的环节。集成测试通过 ≠ 生产环境可用。
（3）上线与回滚机制
没有发布流程、没有回滚方案。如果上线后发现问题，工具链到此中断。
（4）监控与告警
没有线上监控、错误追踪、性能观测的闭环。
（5）迭代反馈与需求回溯
归档后即结束，没有从用户真实使用数据反哺下一版需求的机制。
二、人工参与节点分析
2.1 文档中明确的人工参与点
设计文档提到：
"人工只需在关键决策点（如需求确认、评审签字）进行干预"
使用手册中分散提到的确认点：
概要需求评审签字
详细需求确认
架构评审
代码审查
2.2 各阶段人工参与深度评估
表格
阶段	当前文档要求	建议的人工参与方式	参与深度
需求探索	AI自主brainstorming	人工提供业务背景、确认核心痛点、校准用户画像	🔶 中度
概要需求	AI生成5个md文件	人工必须评审并签字确认，这是后续所有工作的基准	🔴 深度
详细需求	AI按模块输出	人工逐模块确认原型图、边界条件、异常流程	🔴 深度
概要设计	AI生成架构	人工评审技术选型、数据流、安全方案	🔴 深度
接口契约	AI生成OpenAPI	前后端负责人共同确认字段、状态码、鉴权方式	🔴 深度
任务拆解	AI生成≤30分钟任务	人工调整优先级、识别依赖盲区、评估工时合理性	🔶 中度
编码实现	AI自主TDD执行	人工Review关键算法、安全相关代码	🟢 轻度
单元/集成测试	AI生成并执行	人工抽查覆盖率报告、补充边界Case	🟢 轻度
页面功能验证	❌ 文档未提及	人工必须走完整业务流程，点击每个按钮、验证每条数据流	🔴 深度
上线发布	❌ 文档未提及	人工确认发布窗口、监控大盘、回滚预案	🔴 深度
2.3 关键问题：何时做"页面功能验证"？
文档中没有专门的功能验证（Function Verification）或业务流程走通（E2E Business Flow）环节。
建议插入位置：在"集成测试"之后、"归档收尾"之前，增加一个 UAT & 业务流程验证 阶段：
bash
复制
# 建议补充的命令
/skill:uat-verification 基于详细需求中的用户故事，执行业务流程验证。
验证清单：@openspec/changes/{变更名}/specs/feature-*/user-stories.md
环境：staging / preview部署

# 人工操作：在预览环境手动走通核心业务流程
# 产出：uat-report.md（通过/不通过，遗留问题清单）
三、高风险环节识别
3.1 风险矩阵
表格
环节	风险等级	风险描述	为什么需要人工严格把关
概要需求确认	🔴 极高	AI生成的需求与真实业务意图偏差	这是整个项目的"锚点"，一旦偏差，后续所有工作都是错的。AI容易过度推断或遗漏隐性需求。
接口契约定义	🔴 极高	字段设计不合理导致前后端返工	接口是前后端的分界线，AI可能忽略鉴权、分页、批量操作、幂等性等工程细节。
详细需求原型	🟠 高	页面交互逻辑与用户体验脱节	AI生成的原型是"逻辑正确"但"体验可能糟糕"，缺少真实用户的操作体感。
概要设计评审	🟠 高	技术选型不当或架构扩展性不足	AI倾向于使用常见方案，可能忽略团队现有技术债、性能瓶颈、安全合规要求。
业务流程验证	🟠 高（文档缺失）	功能可用但业务走不通	集成测试验证的是接口连通性，不是业务规则正确性。例如：订单状态机流转、退款逆向流程。
任务拆解	🟡 中	任务粒度不合理或依赖遗漏	可能导致开发中断或并行开发时出现阻塞。
代码生成	🟡 中	AI生成"看起来对"但有隐患的代码	通过TDD和Code Review可大幅降低风险。
3.2 最需要人工严格把关的三个环节
环节1：概要需求评审（Gate 1）
为什么风险最大：
文档中 /skill:prd-generation 直接产出5个md文件，然后进入下一阶段
没有明确的人工"冻结"机制
AI可能将用户的模糊意图过度具体化，或者遗漏核心业务规则
把关方式：
plain
复制
/skill:prd-generation 生成概要需求
→ 人工评审会议（必须）
→ 在 openspec/changes/{变更名}/specs/ 下签字确认
→ /skill:self-check 概要需求  ← 这个自查不能替代人工评审
→ 只有确认后才允许进入 detailed-requirements
检查清单：
[ ] 目标用户画像是否准确？
[ ] 核心功能列表是否覆盖业务闭环？
[ ] 边界条件（如空状态、超限、权限）是否定义？
[ ] 非功能性需求（性能、安全）是否量化？
环节2：接口契约确认（Gate 2）
为什么风险大：
文档中 /skill:interface-first-dev 生成OpenAPI后即进入开发
接口一旦开始开发，变更成本指数级上升
把关方式：
前后端负责人必须在 openapi.yaml 上共同签字
使用Swagger UI可视化预览，人工点击每个接口检查
特别关注：错误码设计、分页参数、文件上传、WebSocket、鉴权头
环节3：业务流程走通（Gate 3，文档缺失）
为什么必须新增：
单元测试和集成测试是"白盒验证"，UAT是"黑盒验证"
AI可能实现了一个"逻辑正确"但"业务错误"的功能（如优惠券叠加规则理解错误）
把关方式：
plain
复制
新增阶段：UAT & 业务验证
├── 部署到预览环境（Vercel Preview / 测试服务器）
├── 人工按用户故事逐个操作
├── 验证正向流程 + 异常分支 + 边界条件
├── 产出 uat-report.md
└── 不通过则退回 executing-plans 修复
四、改进建议
4.1 补充缺失的环节
建议在工具链中增加以下阶段：
表格
新增阶段	插入位置	负责方	产出物
UAT & 业务验证	集成测试之后	产品经理/业务方 + 开发	uat-report.md
预发布部署	UAT之后	运维/开发	staging-deployment.md
上线发布	归档之前	运维负责人	release-notes.md
线上监控	归档之后	运维 + 开发	monitoring-dashboard.md
4.2 明确人工参与的三道闸门
建议在文档中显式定义三个不可跳过的人工闸门（Human Gates）：
plain
复制
Gate 1: 需求冻结闸 —— 概要需求评审签字后方可进入设计
Gate 2: 设计冻结闸 —— 接口契约 + 概要设计评审签字后方可进入开发  
Gate 3: 发布冻结闸 —— UAT通过 + 代码审查通过后方可归档上线
4.3 页面功能验证的具体操作建议
对于"走一个完整业务流程"，建议在使用手册中补充：
bash
复制
# 阶段 9.5：UAT 与业务流程验证（人工主导）

## 前置条件
- 代码已部署到预览环境
- 集成测试全部通过

## 人工操作步骤
1. 打开预览环境地址
2. 按 user-stories.md 逐个执行：
   - 正向流程：注册 → 登录 → 创建角色 → 生成剧本 → 保存 → 导出
   - 异常分支：重复名称、超长输入、网络中断恢复
   - 权限验证：未登录访问、越权操作
3. 记录问题到 uat-issues.md
4. 严重问题 → 退回开发；轻微问题 → 记入下一迭代

/skill:progress-tracker 请更新进度
/skill:self-check UAT验证
五、总结
表格
维度	评估结论
周期覆盖	覆盖了需求→设计→开发→技术测试，但缺失UAT、部署、上线、监控四个关键阶段
人工参与	文档提到了"关键决策点"，但没有明确哪几个点是强制人工闸门，容易流于形式
功能验证	缺少专门的页面功能验证和业务流程走通环节，集成测试不能替代人工UAT
最大风险	概要需求偏差（一错全错）> 接口契约缺陷（返工成本高）> 业务流程未走通（上线即故障）
核心建议：在现有工具链基础上，增加 Gate 1/2/3 三道人工强制闸门，补充 UAT 与上线发布环节，否则这个工具链是一个"开发完成"的工具链，而不是一个"项目交付"的工具链。
再细化下新增的这结果环节的输入和输出，输入数据来自哪里？从外部系统提供还是手工录入还是其他来源？  通过什么处理？人工处理还是skill出来还是其他工具，需要明确处理单元； 输出是什么，输出的数据给谁用，怎么用？  另外，因为以上环节没有页面原型，是不是风险较大，页面开发完成后需要人工确认下，另外详细需求中是否描述了每个按钮点击后的动作和页面变化呢？
编辑
复制
分享
监控工具自动采集分析与原型完善
基于文档现有内容和你的追问，我从输入-处理-输出（IPO）维度细化四个新增环节，并回答页面原型与交互细节的关键风险。
一、新增环节 IPO 详细设计
1. UAT & 业务流程验证（新增阶段 9.5）
表格
维度	详细说明
输入	① 测试清单源：feature-*/user-stories.md（需从详细需求中提取用户故事）
② 功能入口：预览环境 URL（Staging/Preview）
③ 基准规格：specs/03-functional-structure.md + feature-*/spec.md（功能清单）
④ 接口契约：openapi.yaml（用于验证前后端数据一致性）
⑤ 集成测试报告：tests/integration/ 通过记录（准入门槛）
数据来源	user-stories.md 由 /skill:detailed-requirements 生成时自动提取；预览环境由 CI/CD 或 人工部署；接口契约来自上游阶段产物
处理单元	人工主导（产品经理/业务方/你本人）+ AI辅助
• 人工：逐条执行用户故事，点击每个按钮，观察页面状态变化
• AI辅助：/skill:uat-verification 可自动生成测试清单模板和问题记录格式，但不能替代人工点击
输出	uat-report.md（包含：通过项/不通过项/遗留问题/严重级别）
给谁用	① 开发负责人：根据不通过项安排修复
② 项目经理：决定是否进入发布阶段
③ 归档留存：作为变更审计材料存入 openspec/changes/{变更名}/uat/
怎么用	严重问题（P0/P1）→ 退回 /skill:executing-plans 修复；轻微问题（P2）→ 记入 tasks.md 下一迭代处理；报告签字后触发上线流程
2. 预发布部署（新增阶段 9.6）
表格
维度	详细说明
输入	① 代码源：通过代码审查的 Git 分支/commit SHA
② 环境配置：ops/staging-config.yaml（数据库连接、第三方API Key、域名）
③ 部署脚本：ops/deploy-staging.sh（由项目初始化时创建或 /skill:executing-plans 生成）
④ UAT准入单：uat-report.md（必须已通过）
数据来源	代码来自 Git；环境配置由 运维/开发人工录入 或继承自项目模板；部署脚本可由 skill 生成初稿，人工审核后使用
处理单元	CI/CD 工具自动处理为主 + 人工触发
• 推荐：GitHub Actions / Vercel Preview / Docker Compose
• 人工：在 Kimi Code 中执行 /skill:deploy-staging（如果未来封装此 skill），或在命令行执行脚本
• 关键：部署完成后人工确认服务健康检查通过
输出	staging-deployment.md（环境地址、部署时间、版本号、已知问题清单）
给谁用	① UAT 测试人员：获得可访问的预览地址
② 客户/业务方：提前体验功能（如 reelforge 的剧本生成效果）
③ 开发团队：用于线上问题复现前的预验证
怎么用	部署报告贴在项目群/飞书文档；预览地址发给业务方进行体验确认；如部署失败，自动回滚并告警
3. 上线发布（新增阶段 10.5）
表格
维度	详细说明
输入	① 发布审批单：uat-report.md（通过）+ code-review-report.md（通过）
② 发布清单：release-checklist.md（数据库迁移、配置变更、第三方依赖检查）
③ 回滚方案：rollback-plan.md（由 /skill:high-level-design 阶段预留）
④ 制品包：Docker 镜像/静态文件包 + 版本 Tag
数据来源	审批单来自上游阶段；发布清单由 /skill:release-management（建议新增）基于详细设计生成初稿，运维负责人人工补充；回滚方案来自概要设计阶段的运维架构设计
处理单元	人工主导（运维/技术负责人）+ 工具执行
• 人工：确认发布窗口、执行发布清单逐项检查、决策是否发布
• 工具：ArgoCD / Jenkins / 云厂商 CLI 执行实际部署
• 严禁 AI 自动执行生产发布，必须人工最终确认
输出	release-notes.md（版本说明、变更点、兼容性影响）+ 生产环境部署确认单
给谁用	① 运营/客服团队：了解新功能，准备用户答疑
② 用户：通过公告获知更新
③ 运维：留存发布记录，用于事后审计
怎么用	发布完成后在监控群通告；release-notes.md 同步到项目文档站点；如发布失败，立即执行 rollback-plan.md
4. 线上监控与反馈（新增阶段 11）
表格
维度	详细说明
输入	① 运行时数据：应用日志（Error/Warning）、性能指标（QPS/延迟/内存）、业务指标（订单转化率/功能使用率）
② 告警规则：monitoring-rules.yaml（阈值配置，如错误率>1%触发告警）
③ 用户反馈：客服工单、应用商店评论、埋点数据
数据来源	运行时数据来自 Sentry / Prometheus / 云监控 等外部系统自动采集；用户反馈来自 客服系统/埋点平台；告警规则由 /skill:monitoring-setup（建议新增）生成初稿，人工调整阈值
处理单元	监控工具自动处理 + 人工响应
• 自动：错误采集、性能图表生成、告警通知（飞书/钉钉/邮件）
• 人工：On-call 工程师响应 P0 告警；产品经理定期Review埋点数据
• AI辅助：/skill:monitoring-analysis 可每周生成异常摘要报告，但不处理告警
输出	monitoring-dashboard.md（周度健康报告）+ 告警通知单 + feedback-loop.md（用户反馈汇总）
给谁用	① 开发团队：根据错误日志修复线上 Bug
② 产品经理：根据功能使用率数据，调整下一版需求优先级
③ 项目Owner（你）：判断项目健康度，决定资源投入
怎么用	告警 → 立即响应；周度报告 → 在需求评审会上作为数据支撑；用户反馈 → 输入到下一变更的 brainstorming 阶段，形成闭环
二、页面原型与交互细节的关键风险
2.1 文档中关于原型的现状
从设计文档和使用手册看，/skill:detailed-requirements 的输出包含：
plain
复制
feature-XX-{模块名}/
├── spec.md          # 功能规格
├── prototype.md     # 页面原型 ← 这个文件存在
├── io-table.md      # 输入输出表
└── logic.md         # 业务逻辑
但是，文档没有明确 prototype.md 的粒度标准——它到底是：
A) 只有页面布局线框图（Wireframe）？
B) 还是包含每个按钮的交互状态机（点击前/点击后/加载中/错误态）？
2.2 当前风险：prototype.md 可能不够细
对于 reelforge（短剧生成系统）这类强交互型产品，如果只是文字描述原型，风险极高：
表格
风险点	具体表现	后果
按钮级交互缺失	AI生成"点击生成按钮，系统生成剧本"，但没描述：按钮是立即响应还是异步？加载动画是什么？生成失败后按钮状态？	前端开发凭经验猜测，上线后用户体验不一致
页面状态流转缺失	角色工厂页面：空态（无角色）→ 创建中 → 创建成功 → 编辑态。AI可能只描述了成功态	空态和异常态遗漏，用户看到空白页面
表单校验规则缺失	剧本名称输入框：最大长度？特殊字符限制？实时校验还是提交校验？	前后端校验不一致，用户提交后报错
多设备适配缺失	分镜工作室的拖拽操作在移动端如何降级？	移动端功能不可用
2.3 建议：增加原型评审闸门（Gate 2.5）
在详细需求阶段后、概要设计前，强制插入人工原型确认：
bash
复制
# 新增阶段：原型评审（人工闸门 Gate 2.5）

## 输入
/skill:detailed-requirements 生成的 feature-*/prototype.md
参考：@openspec/changes/{变更名}/specs/03-functional-structure.md

## 人工处理（必须）
1. 打开 prototype.md，检查每个页面是否包含：
   - [ ] 页面布局图（手绘/截图/ASCII均可）
   - [ ] 每个可交互元素的说明（按钮、输入框、下拉框）
   - [ ] 交互状态机：点击前 → 点击中（loading） → 点击后（成功/失败）
   - [ ] 异常分支：网络中断、权限不足、数据为空时的页面表现
   - [ ] 页面间跳转关系（从角色工厂到剧本工坊的流转）

2. 如有缺失，要求 AI 补充：
/skill:detailed-requirements 补充 feature-01-角色工厂 的按钮交互细节。
重点：创建角色按钮的加载态和错误态。

## 输出
feature-*/prototype.md（已确认版本）
feature-*/interaction-spec.md（新增：交互规格说明书）

## 给谁用
前端开发：按 interaction-spec.md 实现精确交互
测试人员：按 interaction-spec.md 验证每个状态
2.4 detailed-requirements 应补充的交互规格
建议强制要求 detailed-requirements 在生成 prototype.md 时，必须包含以下按钮级交互模板：
markdown
复制
### 交互元素：{按钮名称}

| 属性 | 说明 |
|------|------|
| 触发方式 | 点击 / 悬停 / 拖拽 / 键盘快捷键 |
| 前置条件 | 用户已登录 / 已选择角色 / 表单校验通过 |
| 立即反馈 | 按钮置灰 + 显示 Spinner / 显示 Toast "生成中..." |
| 成功结果 | 页面跳转至 /script-studio / 弹窗显示结果 / 列表自动刷新 |
| 失败结果 | 按钮恢复可点击 + 错误提示（位置：按钮下方/顶部Toast/弹窗） |
| 异常分支 | 网络超时：重试按钮 / 服务端500：联系客服链接 |
| 埋点事件 | click_generate_script / generate_script_success / generate_script_fail |
三、修正后的完整流程（含人工闸门与原型确认）
Mermaid
复制
代码
预览
graph TD
    A[变更提案] --> B[需求探索]
    B --> C[概要需求]
    C -->|Gate 1: 人工评审签字| D[详细需求]
    D --> E[原型与交互规格]
    E -->|Gate 2.5: 人工逐页确认按钮交互| F[概要设计]
    F -->|Gate 2: 人工评审架构| G[详细设计]
    G --> H[接口契约]
    H -->|Gate 2: 前后端共同签字| I[任务拆解]
    I --> J[编码实现]
    J --> K[单元/集成测试]
    K --> L[UAT & 业务流程验证]
    L -->|Gate 3: 人工走通每个页面| M[预发布部署]
    M --> N[上线发布]
    N --> O[线上监控]
    O -->|反馈闭环| B
四、总结与行动建议
表格
问题	结论	立即行动
新增环节 IPO	已细化四个环节的输入来源、处理单元（人工 vs 工具）、输出物及消费方	将上表纳入《使用手册》第3.4节
页面原型风险	文档虽有 prototype.md，但未规定按钮级交互粒度，对 reelforge 这类交互密集型产品风险大	强制增加 Gate 2.5：详细需求产出后，人工逐页确认每个按钮的前置条件、点击反馈、成功/失败态
交互细节缺失	detailed-requirements 需补充 interaction-spec.md，强制使用按钮交互模板	修改 /skill:detailed-requirements 的 SKILL.md，在输出规范中增加交互元素表格
数据来源	UAT清单来自详细需求；部署配置来自人工录入+模板继承；监控数据来自外部系统自动采集	在项目初始化时（progress-tracker阶段）就创建 ops/ 目录模板，包含 staging-config.yaml 和 monitoring-rules.yaml 骨架
最关键的一句话：对于 reelforge，页面开发完成后的"人工点击确认"不可替代。AI 可以生成 90% 的代码，但按钮点下去后用户的心理预期（如"生成剧本"按钮是 2 秒出结果还是 20 秒？需不需要进度条？）必须由你作为产品 Owner 亲自体验并确认。建议在工具链中把这一步设为硬性阻塞环节，不签字不能进入发布。
总结下，需要新增哪些skill，这些skill的输入和输出和现有的哪个衔接？  需要修改哪些skill，修改要点有哪些
编辑
复制
分享
集成修改、ops目录创建与页面确认节点
基于前面的 IPO 分析，以下是需要新增的 Skill和需要修改的 Skill的完整清单，包含输入输出衔接关系。
一、需要新增的 Skill（4 个）
表格
Skill 名称	输入（来源）	处理单元	输出	衔接上游	衔接下游	说明
uat-verification	① tests/integration/ 通过记录
② feature-*/user-stories.md（从详细需求提取）
③ openapi.yaml（接口基准）
④ 预览环境 URL（人工/CI 提供）	人工主导点击验证 + AI 辅助生成测试清单模板和问题记录格式	uat-report.md（通过/不通过/遗留问题/严重级别）	integration-test	requesting-code-review + release-management	这是 Gate 3 的核心载体，AI 不能替代人工点击页面，但可生成检查清单
release-management	① uat-report.md（UAT 通过）
② code-review-report.md（来自 requesting-code-review）
③ rollback-plan.md（来自 high-level-design）
④ 代码分支/commit SHA	人工最终决策 + AI 辅助生成发布清单和 Release Notes	release-notes.md + release-checklist.md + 生产部署确认单	requesting-code-review + uat-verification	opsx:archive	严禁 AI 自动执行生产发布，AI 只负责生成文档和检查项，上线按钮必须由人按
monitoring-setup	① high-level-design 中的运维架构章节
② 项目技术栈（FastAPI/Vue3 等）
③ 告警渠道配置（人工录入飞书/钉钉 Webhook）	AI 生成初稿 + 人工调整阈值	monitoring-rules.yaml + alert-channels.md	high-level-design	monitoring-analysis（长期运行）	项目初始化时一次性执行，建议在 progress-tracker 阶段触发
monitoring-analysis	① 运行时日志/告警（Sentry/Prometheus 等外部系统）
② 埋点数据
③ monitoring-rules.yaml	监控工具自动采集 + AI 辅助生成周度摘要报告	monitoring-dashboard.md + feedback-loop.md	release-management（上线后）	brainstorming（下一变更迭代）	周期性运行，将线上反馈数据反哺到下一版需求
新增 Skill 在流程中的位置
Mermaid
复制
代码
预览
graph LR
    A[integration-test] --> B[uat-verification]
    B --> C[requesting-code-review]
    C --> D[release-management]
    D --> E[opsx:archive]
    D --> F[monitoring-setup<br/>一次性]
    F --> G[monitoring-analysis<br/>周期性]
    G -->|feedback-loop.md| H[brainstorming]
二、需要修改的 Skill（6 个）
表格
Skill 名称	修改要点	修改原因	输出物变化
detailed-requirements	强制增加交互规格输出：在 feature-*/prototype.md 基础上，新增 feature-*/interaction-spec.md，要求每个按钮必须包含：触发方式、前置条件、立即反馈、成功/失败结果、异常分支、埋点事件	当前 prototype.md 粒度未知，reelforge 作为强交互产品，按钮级状态机缺失会导致前端实现偏差	新增 interaction-spec.md（按钮级交互状态机）
progress-tracker	初始化时增加运维基础设施目录：创建 ops/ 目录并生成 staging-config.yaml 骨架、rollback-plan.md 模板、monitoring-rules.yaml 骨架	当前初始化缺少预发布和监控的配置载体，导致后续 deploy/monitoring 无据可依	初始化产出增加 ops/ 目录及三个配置文件骨架
high-level-design	增加运维架构章节：在 16 个设计文档中增加部署架构、回滚策略、监控大盘设计；独立输出 rollback-plan.md	当前设计只关注功能实现，缺少上线后的回滚和运维方案，release-management 无输入可用	新增 rollback-plan.md（回滚步骤、数据库回滚脚本清单、灰度策略）
integration-test	增加用户故事检查清单：输出 user-stories-checklist.md，将详细需求中的用户故事转为可勾选的测试项，供 UAT 使用	当前集成测试是技术端到端验证，缺少面向业务人员的 UAT 检查清单	新增 user-stories-checklist.md
self-check	增加两个检查维度：
① 交互规格完整性检查（按钮状态机是否覆盖空态/加载态/错误态）
② UAT 报告质量检查（遗留问题是否分级、严重问题是否已修复）	当前 self-check 只覆盖概要需求/概要设计/详细设计/接口/编码/测试，缺少对交互和 UAT 的把关	检查清单增加 interaction-spec 和 uat-report 两个 target
requesting-code-review	明确输出 code-review-report.md：记录通过/有条件通过/不通过结论，以及阻塞性问题清单	当前只是"进行审查"，没有结构化输出，release-management 无法判断代码质量是否准入	新增 code-review-report.md（签字确认格式）
三、关键衔接关系汇总
3.1 数据流总图（新增 + 修改后的完整链路）
plain
复制
阶段 2.5 详细需求
    │
    ├──→ detailed-requirements 输出：prototype.md + interaction-spec.md（新增）
    │
    ├──→ Gate 2.5：人工逐页确认按钮交互（阻塞）
    │
    ▼
阶段 3 概要设计
    │
    ├──→ high-level-design 输出：design/*.md + rollback-plan.md（新增）
    │
    ├──→ monitoring-setup 消费运维架构 → 输出 monitoring-rules.yaml（新增）
    │
    ▼
阶段 5 接口契约
    │
    ▼
阶段 6 任务拆解
    │
    ▼
阶段 7 编码实现
    │
    ▼
阶段 8 单元/集成测试
    │
    ├──→ integration-test 输出：tests/integration/ + user-stories-checklist.md（新增）
    │
    ▼
阶段 9.5 UAT（新增）
    │
    ├──→ uat-verification 消费 user-stories-checklist.md + 预览环境
    │
    ├──→ 人工点击走通业务流程（阻塞）
    │
    ├──→ 输出：uat-report.md
    │
    ▼
阶段 9.6 预发布部署（人工执行脚本）
    │
    ▼
阶段 10 代码审查
    │
    ├──→ requesting-code-review 输出：code-review-report.md（新增）
    │
    ▼
阶段 10.5 上线发布（新增）
    │
    ├──→ release-management 消费：
    │       uat-report.md（通过）
    │       code-review-report.md（通过）
    │       rollback-plan.md（来自阶段3）
    │
    ├──→ 人工最终确认发布窗口
    │
    ├──→ 输出：release-notes.md + release-checklist.md
    │
    ▼
阶段 11 归档
    │
    ├──→ opsx:archive 归档范围扩大：纳入 uat-report + release-notes
    │
    ▼
阶段 12 线上监控（新增）
    │
    ├──→ monitoring-analysis 周期性运行
    │
    ├──→ 输出：monitoring-dashboard.md + feedback-loop.md
    │
    └──→ feedback-loop.md 输入到下一变更的 brainstorming（闭环）
3.2 人工阻塞闸门与 Skill 的对应关系
表格
闸门	对应 Skill	人工动作	Skill 辅助动作
Gate 1 需求冻结	prd-generation	评审并签字 specs/01-05.md	self-check 概要需求 预检
Gate 2.5 原型冻结	detailed-requirements	逐页确认 interaction-spec.md 中每个按钮的交互状态机	AI 生成交互规格模板
Gate 2 设计冻结	high-level-design	评审架构 + 确认 rollback-plan.md	self-check 概要设计 预检
Gate 3 发布冻结	uat-verification + release-management	在预览环境走通完整业务流程，确认 uat-report.md	AI 生成 UAT 检查清单和发布清单
四、实施优先级建议
表格
优先级	Skill	理由
P0	修改 detailed-requirements（增加 interaction-spec.md）	reelforge 是交互密集型产品，按钮级交互缺失是当前最大风险
P0	新增 uat-verification	文档完全缺失业务验证环节，上线后极易出现"功能可用但流程走不通"
P1	修改 progress-tracker（增加 ops/ 目录）	为后续 deploy/monitoring 提供基础设施载体，一次性投入
P1	修改 high-level-design（增加 rollback-plan.md）	发布管理的前置依赖，没有回滚方案不能上线
P1	新增 release-management	补齐"开发完成 → 上线交付"的最后一公里
P2	新增 monitoring-setup + monitoring-analysis	长期价值大，但短期内不影响 reelforge MVP 上线
P2	修改 self-check + requesting-code-review	质量加固，可在使用过程中逐步迭代
五、一句话总结
新增 4 个 Skill 补齐"UAT → 发布 → 监控"的交付后链路；修改 6 个 Skill 解决"按钮交互规格缺失"和"回滚/运维方案空白"的隐患。最关键的改动是：detailed-requirements 必须输出按钮级交互状态机，uat-verification 必须成为人工阻塞闸门。
人工处理的环节中整个流程中怎样体现？
编辑
复制
分享
文档落点定位与Gate流程说明及执行责任
在现有工具链中，人工参与目前只是模糊地描述为"关键决策点进行干预"。要让它显性化、可落地、可追溯，需要在流程、文档、命令三个层面同步改造。
一、人工参与的三层显性化方案
1.1 流程层：用「人工闸门（Human Gate）」标记阻塞点
将人工参与从"建议性"改为阻塞性——AI 执行到此处暂停，必须获得人工信号才能继续。
Mermaid
全屏 
下载 
复制
代码
预览
AI产出

人工签字

AI产出

人工逐页确认

AI产出

人工签字

AI产出

人工点击走通

人工最终决策

brainstorming
prd-generation
🚪 Gate 1: 需求冻结
detailed-requirements
🚪 Gate 2.5: 原型冻结
high-level-design
🚪 Gate 2: 设计冻结
detailed-design
interface-first-dev
task-breakdown
executing-plans
unit-test +integration-test
🚪 Gate 3: UAT冻结
release-management
opsx:archive
关键规则：每个 🚪 闸门处，AI 必须暂停并等待人工输入，不能自动进入下一阶段。
1.2 文档层：用「签字文件（Sign-off）」固化责任
每个 Gate 对应一份不可篡改的签字文件，记录"谁、在什么时候、以什么结论、通过了什么"。
表格
Gate	签字文件路径	格式要求	签字人
Gate 1 需求冻结	openspec/changes/{变更名}/sign-off/01-requirements.md	包含：评审意见、遗留问题、通过/有条件通过/不通过、签字人、日期	产品负责人（你）
Gate 2.5 原型冻结	openspec/changes/{变更名}/sign-off/02.5-prototype.md	包含：逐页确认清单、按钮交互检查、签字	产品负责人 + 前端负责人
Gate 2 设计冻结	openspec/changes/{变更名}/sign-off/02-design.md	包含：架构评审意见、回滚方案确认、签字	技术负责人（你）
Gate 3 发布冻结	openspec/changes/{变更名}/sign-off/03-release.md	包含：UAT结果、代码审查结论、发布窗口确认、签字	产品负责人 + 技术负责人
签字文件模板（以 Gate 1 为例）：
Markdown
复制
代码
预览
# 需求冻结签字单

## 变更信息
- 变更名：reelforge-v1.2-角色工厂重构
- 版本：2026-05-08-v2
- 评审日期：2026-05-08

## 评审对象
- `specs/01-product-overview.md`
- `specs/02-requirements-list.md`
- `specs/03-functional-structure.md`
- `specs/04-business-rules.md`
- `specs/05-non-functional.md`

## 评审结论
□ 通过（可直接进入详细需求）
□ 有条件通过（遗留问题需在详细需求阶段修复）
□ 不通过（需重新生成概要需求）

## 遗留问题（如选"有条件通过"）
1. [P1] 角色工厂中"批量导入"功能的边界条件未定义
2. [P2] 非功能性需求中缺少并发用户数指标

## 签字
- 产品负责人：___________ 日期：___________
- 技术负责人：___________ 日期：___________
1.3 命令层：用「/human 指令」显式触发人工介入
在 Kimi Code 的交互中，人工参与不是被动的"AI 停下来等你"，而是通过显式命令触发人工任务：
bash
复制
# AI 执行到 Gate 1 时，自动输出：
========================================
🚪 Gate 1: 需求冻结 —— 等待人工评审
========================================
产出物已保存至：@openspec/changes/{变更名}/specs/
请执行以下操作：
1. 阅读 5 个 spec 文件
2. 如有修改意见，直接编辑文件或在对话中提出
3. 确认无误后，输入指令：

/human:sign-off 需求冻结 结论=通过 遗留="批量导入边界待补充"

# 只有收到 /human:sign-off 后，AI 才允许执行下一阶段：
/skill:detailed-requirements
建议定义的人工指令集：
表格
指令	作用	使用场景
/human:sign-off {gate} 结论={通过/有条件通过/不通过} 遗留={问题清单}	人工确认通过某个 Gate	每个 Gate 结束时
/human:reject {gate} 原因={} 范围={}	人工打回重做	发现严重偏差时
/human:pause 原因={}	临时暂停流程	需要等待外部资源（如设计师出图）
/human:resume	恢复暂停的流程	外部资源到位后
/human:hotfix 问题={} 优先级={P0/P1/P2}	线上紧急修复	监控阶段发现问题
二、各阶段人工参与的具体体现
2.1 需求阶段：人工是「校准者」
表格
AI 动作	人工动作	体现形式
/skill:brainstorming 生成需求草案	人工提供业务背景、纠正用户画像偏差	在对话中直接回复："角色工厂的目标用户不是专业编剧，是短视频运营，请修正"
/skill:prd-generation 生成 5 个 spec	Gate 1：人工逐条阅读，确认核心功能列表覆盖业务闭环	sign-off/01-requirements.md 签字
/skill:detailed-requirements 生成交互规格	Gate 2.5：人工打开 prototype.md，想象自己点击每个按钮	sign-off/02.5-prototype.md 逐页勾选
关键：需求阶段人工不替代 AI 写文档，而是做"意图校准"——AI 负责穷尽可能性，人工负责删减和聚焦。
2.2 设计阶段：人工是「约束施加者」
表格
AI 动作	人工动作	体现形式
/skill:high-level-design 生成架构	Gate 2：人工评审技术选型是否符合现有技术债	在 sign-off/02-design.md 中注明："禁止使用 GraphQL，团队熟悉 REST"
AI 生成 rollback-plan.md	人工确认回滚步骤是否可操作	在签字单中注明："数据库回滚脚本需单独测试"
关键：设计阶段人工不画架构图，而是施加约束——告诉 AI 什么不能做、什么必须做。
2.3 开发阶段：人工是「抽查者」
表格
AI 动作	人工动作	体现形式
/skill:executing-plans 按任务编码	人工抽查关键算法和安全相关代码	在对话中：@src/core/script-generator.ts 检查这段生成逻辑是否有并发问题
/skill:tdd 执行红绿重构	人工抽查测试用例是否覆盖边界	查看覆盖率报告，要求补充："角色名称超过 50 字符的测试缺失"
关键：开发阶段人工不做 Code Review 的全部工作，而是抽查高风险点——AI 负责 90% 的审查，人工负责 10% 的关键风险。
2.4 测试/UAT 阶段：人工是「体验者」
表格
AI 动作	人工动作	体现形式
/skill:integration-test 通过接口测试	Gate 3：人工在预览环境点击每个页面	uat-report.md 中记录："角色创建按钮在移动端无法点击"
AI 生成 user-stories-checklist.md	人工按清单逐项勾选，走完整业务流程	在签字单中确认："所有 P0 用户故事已验证通过"
关键：UAT 阶段必须人工亲自点击，AI 只能生成检查清单，不能替代手指操作。
2.5 发布阶段：人工是「最终决策人」
表格
AI 动作	人工动作	体现形式
/skill:release-management 生成发布清单	人工确认发布窗口、检查回滚方案	sign-off/03-release.md 签字
CI/CD 工具执行部署脚本	人工点击"确认发布"按钮	在运维平台或命令行执行最终命令
关键：发布阶段 AI 负责"准备"，人工负责按下最终按钮——这是安全底线。
三、人工参与在进度追踪中的体现
progress-tracker 需要增加人工状态字段，让项目看板一眼看出"谁在等谁"：
markdown
复制
# tasks.md 中增加人工状态列

| 阶段 | 任务 | 负责人 | AI状态 | 人工状态 | 阻塞原因 |
|------|------|--------|--------|----------|----------|
| 需求 | 概要需求生成 | AI | ✅ 完成 | 🚪 待签字 | 等待 Gate 1 评审 |
| 设计 | 接口契约定义 | AI | ✅ 完成 | 🚪 待签字 | 等待前后端负责人确认 |
| UAT | 业务流程验证 | 人工 | ⏸️ 未开始 | 🚪 进行中 | 等待预览环境部署 |
| 发布 | 上线发布 | 人工 | ⏸️ 未开始 | 🚪 待决策 | 等待 UAT 报告签字 |
当人工状态为"待签字"时，AI 不得自动开始下一阶段任务。
四、总结：人工参与的三条铁律
表格
铁律	说明	在文档中的体现
1. 阻塞性	人工不通过，AI 不继续	每个 Gate 后有 🚪 标记，AI 等待 /human:sign-off
2. 可追溯	每个决策都有记录、有签字、有日期	sign-off/ 目录下的 Markdown 签字单
3. 分层性	不同阶段人工角色不同（校准者→约束者→抽查者→体验者→决策人）	使用手册中明确定义每个阶段的人工职责和指令
最终建议：在《AI项目落地工具链使用手册》中新增第 3.5 节"人工参与规范"，包含：
五个 Gate 的签字单模板
/human:* 指令集说明
各阶段人工职责对照表
进度看板中的人工状态字段规范
这样，人工参与不再是"想起来就看一下"，而是嵌入流程的、有记录、有阻塞、有责任的正式环节。
/human:*  是一个skill吗
编辑
复制
分享
Kimi Code人工阻塞实现方案
不是。 /human:* 不是 Kimi Code 的原生命令，也不是某个开源 skill。这是我刚才提出的流程设计概念，但用错了表达方式，让你产生了误解。
一、澄清：Kimi Code 中实际有什么
表格
命令格式	来源	说明
/skill:skill-name	Kimi Code 原生	调用 .kimi/skills/ 下的 skill
/opsx:propose	OpenSpec（如集成）	OpenSpec 的变更提案命令
/flow:xxx	你之前尝试过的	未知命令，提示不可用
Kimi Code 没有 /human:sign-off 这种命令。 如果你现在去输入，它会报 Unknown slash command。
二、那"人工阻塞"怎么落地？
既然没有原生命令，要在现有工具链中实现"人工参与显性化"，有三种务实方案：
方案 A：在 Skill 的 SKILL.md 中定义"人工确认节点"（推荐）
实现方式：修改每个需要人工把关的 skill（如 prd-generation、high-level-design），在其 SKILL.md 的 ## 执行流程 中增加一个伪步骤：
Markdown
复制
代码
预览
## 执行流程

1. 读取上游文档
2. 生成产出物并保存到指定路径
3. **人工确认节点** ← 新增
   - 输出提示语："概要需求已生成，请阅读 @openspec/changes/{变更名}/specs/ 下的 5 个文件"
   - 输出检查清单："请确认：①核心功能覆盖业务闭环 ②边界条件已定义 ③非功能性需求已量化"
   - 等待用户回复"确认"或"修改：{具体意见}"
4. 只有在收到"确认"后，才允许进入下一阶段
效果：AI 执行完步骤 2 后，会主动停下来输出一段提示，等你回复。你回复"确认"后，AI 继续；你说"修改"，AI 回到步骤 2 重修。
优点：零开发成本，只改 SKILL.md 文本。
方案 B：用 progress-tracker 作为人工状态机
实现方式：把 progress-tracker 改造成流程控制器：
bash
复制
# 用户输入
/skill:progress-tracker 状态=Gate1 动作=等待人工确认

# AI 输出
========================================
🚪 Gate 1: 需求冻结 —— 当前状态：等待人工确认
========================================
产出物路径：@openspec/changes/{变更名}/specs/
请阅读后，输入以下指令之一：
- "确认通过" → 解锁下一阶段
- "有条件通过，遗留：{问题}" → 解锁但标记遗留
- "不通过，原因：{原因}" → 退回重做

# 用户输入
确认通过

# AI 输出
Gate 1 已通过。现在可以执行：
/skill:detailed-requirements
优点：统一入口，看板清晰。
方案 C：纯约定式，不靠技术约束（最简单）
实现方式：在《使用手册》中写明"此处必须人工确认"，但不改任何 skill。靠人和 AI 的对话节奏自然阻塞：
bash
复制
你：/skill:prd-generation 生成概要需求

Kimi：已生成 5 个 spec 文件...（等待你下一步输入）

你：（阅读文件后）确认通过，进入详细需求

Kimi：收到，执行 /skill:detailed-requirements...
缺点：没有强制阻塞，如果你不小心发了下一条命令，AI 不会阻止。
三、修正后的建议
既然 /human:* 不是真实命令，我修正之前的建议：
表格
原建议	修正为
定义 /human:sign-off 指令集	在 progress-tracker 的 SKILL.md 中增加"人工确认"子流程，用自然语言指令替代
签字文件自动创建	在相关 skill（如 prd-generation）的输出规范中，要求生成 sign-off/ 目录和模板，但签字动作由人手动完成
AI 收到指令后才继续	靠对话上下文自然阻塞，AI 输出确认提示后，等待用户下一条消息
四、实际可落地的最小改动
如果你现在就要改，只需做两件事：
改 prd-generation/SKILL.md：在输出步骤后增加：
"生成完成后，输出提示：'概要需求已生成，请阅读并确认。确认后输入"通过"以继续。'"
改 progress-tracker/SKILL.md：增加状态枚举：
人工状态：待确认 | 已确认 | 已驳回
在《使用手册》中增加一节：写明每个 Gate 的人工检查清单和确认话术（如"通过"、"驳回"）。
不需要开发新命令，不需要装新 skill。 靠 SKILL.md 的文本描述 + 对话节奏即可实现。
总结：/human:* 是我提出的流程概念，不是真实 skill。在 Kimi Code 中，"人工阻塞"靠修改现有 skill 的 SKILL.md 增加确认提示来实现，而不是靠注册新命令。
增加一个human skill怎样呢？统一记录人工决策历史和环节
编辑
复制
分享
Gate 3 状态记录技能设计
这个思路非常对。一个专门的 human skill 能把分散在各处的人工决策集中化、可追溯、可查询，比让每个 skill 自己处理人工状态要优雅得多。
以下是完整设计方案：
一、human skill 定位
表格
属性	说明
定位	人工决策的"审计日志 + 状态闸门"
职责	① 记录每个 Gate 的人工结论 ② 控制阶段流转权限 ③ 提供决策历史查询
不做什么	不替代人工做判断、不自动生成决策内容、不修改产出物
类比	像 Git 的 commit + status——记录快照 + 显示当前状态
二、功能要求
2.1 核心能力
表格
能力	说明
决策记录	对每次人工确认生成结构化记录，包含：Gate、时间、结论、遗留问题、决策人
状态控制	根据最新决策判断当前变更是否允许进入下一阶段
历史追溯	支持查询某个变更的全部决策链，或跨变更的决策统计
阻塞提示	当用户试图跳过未通过的 Gate 时，主动拦截并提示
2.2 决策类型
表格
类型	含义	后续动作
sign-off	签字通过	解锁下一阶段，记录遗留问题（如有）
conditional	有条件通过	解锁下一阶段，但遗留问题必须记入下一阶段的 tasks.md
reject	驳回重做	锁定当前阶段，必须修复后才能再次 sign-off
pause	暂停流程	标记为阻塞状态，等待外部资源
resume	恢复流程	解除暂停，回到 pause 前状态
hotfix	紧急修复	在已归档变更上记录紧急补丁决策
三、使用方法
3.1 标准调用格式
bash
复制
# 格式
/skill:human gate={Gate名称} action={决策类型} [result={结论}] [issues={遗留问题}] [reason={驳回原因}]

# 示例 1：Gate 1 通过
/skill:human gate=Gate1 action=sign-off result=passed issues="P1: 批量导入边界条件待补充"

# 示例 2：Gate 2.5 有条件通过
/skill:human gate=Gate2.5 action=conditional result=passed issues="P1: 角色创建按钮的loading态需细化；P2: 移动端适配方案下一迭代处理"

# 示例 3：Gate 3 驳回
/skill:human gate=Gate3 action=reject reason="UAT发现角色工厂在Safari浏览器下无法保存，需修复后重新验证"

# 示例 4：查询当前变更的决策历史
/skill:human action=history

# 示例 5：查询当前变更状态
/skill:human action=status
3.2 在流程中的插入位置
Mermaid
全屏 
下载 
复制
代码
预览
四、配置
4.1 目录结构
plain
复制
.kimi/skills/human/
├── SKILL.md
├── config.yaml          # 决策模板和校验规则
└── templates/
    ├── decision-record.md   # 单条决策记录模板
    └── status-report.md     # 状态查询输出模板
4.2 config.yaml
yaml
复制
# human skill 配置
gates:
  - id: Gate1
    name: 需求冻结
    required_outputs:
      - specs/01-product-overview.md
      - specs/02-requirements-list.md
      - specs/03-functional-structure.md
      - specs/04-business-rules.md
      - specs/05-non-functional.md
    next_stage: detailed-requirements

  - id: Gate2.5
    name: 原型冻结
    required_outputs:
      - feature-*/prototype.md
      - feature-*/interaction-spec.md
    next_stage: high-level-design

  - id: Gate2
    name: 设计冻结
    required_outputs:
      - design/*.md
      - rollback-plan.md
    next_stage: detailed-design

  - id: Gate3
    name: 发布冻结
    required_outputs:
      - uat-report.md
      - code-review-report.md
    next_stage: release-management

# 决策权限（默认只有用户本人）
sign_off_authority:
  - user  # 由 Kimi Code 会话中的当前用户自动填充

# 阻塞规则
blocking_rules:
  - rule: 前一 Gate 未通过，禁止进入下一 Gate
  - rule: Gate3 未通过，禁止执行 opsx:archive
五、输入
表格
输入项	来源	必填
gate	用户指定（Gate1/Gate2.5/Gate2/Gate3）	是（action 非 history/status 时）
action	用户指定	是
result	用户指定（passed/failed）	sign-off/conditional 时必填
issues	用户输入或 AI 辅助整理	否
reason	用户输入	reject 时必填
change_name	自动从当前会话上下文读取	自动
timestamp	自动生成	自动
user_id	Kimi Code 会话标识	自动
六、处理逻辑
plain
复制
1. 读取当前变更名（从 openspec/changes/ 最新目录或会话上下文）
2. 读取该变更已有的 human-decisions.md
3. 校验：
   a. 指定的 gate 是否存在
   b. 前一 gate 是否已通过（如 Gate2 要求 Gate1 已通过）
   c. 产出物是否已生成（检查 required_outputs 文件是否存在）
4. 生成决策记录
5. 如果是 sign-off/conditional → 更新 progress-tracker 状态为"已确认"
   如果是 reject → 更新 progress-tracker 状态为"已驳回"，并生成修复任务
   如果是 pause → 标记阻塞原因
   如果是 history/status → 读取并格式化输出
6. 保存到 openspec/changes/{变更名}/human-decisions.md
7. 返回下一步可操作指令（如"现在可以执行 /skill:detailed-requirements"）
七、输出
7.1 主输出：human-decisions.md
Markdown
复制
代码
预览
# 人工决策日志

## 变更：reelforge-v1.2-角色工厂重构

| 序号 | Gate | 决策类型 | 结论 | 决策人 | 时间 | 遗留问题 | 驳回原因 |
|------|------|----------|------|--------|------|----------|----------|
| 1 | Gate1 | sign-off | passed | zhsusn | 2026-05-08 18:00 | P1: 批量导入边界条件待补充 | - |
| 2 | Gate2.5 | conditional | passed | zhsusn | 2026-05-08 19:30 | P1: 创建角色按钮loading态细化；P2: 移动端适配下一迭代 | - |
| 3 | Gate2 | sign-off | passed | zhsusn | 2026-05-08 21:00 | - | - |

## 当前状态
✅ 已解锁至：detailed-design  
⏸️ 下一 Gate：Gate3（等待 integration-test 完成）

## 阻塞记录
无
7.2 状态查询输出
bash
复制
/skill:human action=status
输出：
plain
复制
========================================
变更：reelforge-v1.2-角色工厂重构
========================================
已通过：Gate1(需求冻结) → Gate2.5(原型冻结) → Gate2(设计冻结)
当前阶段：detailed-design（进行中）
下一 Gate：Gate3（发布冻结）
状态：🟢 正常推进

⚠️ 注意：Gate2.5 为"有条件通过"，存在遗留问题：
  - P1: 创建角色按钮loading态细化（应在 detailed-design 阶段修复）
  - P2: 移动端适配（记入下一迭代 tasks.md）

可操作指令：
- /skill:detailed-design
- /skill:human action=history
7.3 驳回后的修复任务
bash
复制
/skill:human gate=Gate3 action=reject reason="Safari下无法保存"
自动触发：
Markdown
复制
代码
预览
<!-- 生成到 openspec/changes/{变更名}/rework-tasks.md -->
# Gate3 驳回修复任务

## 驳回原因
Safari下无法保存

## 修复任务
- [ ] [P0] 排查角色工厂在 Safari 浏览器的保存逻辑
- [ ] [P0] 修复后重新执行 UAT 验证
- [ ] [P0] 重新申请 Gate3 sign-off
八、与现有 Skill 的衔接修改
表格
现有 Skill	修改要点	与 human skill 的衔接
prd-generation	生成 5 个 spec 后，末尾增加提示："请阅读产出物，确认后执行 /skill:human gate=Gate1 action=sign-off"	human 记录 Gate1 决策
detailed-requirements	生成 prototype + interaction-spec 后，提示执行 /skill:human gate=Gate2.5	human 记录 Gate2.5 决策
high-level-design	生成设计文档 + rollback-plan 后，提示执行 /skill:human gate=Gate2	human 记录 Gate2 决策
integration-test	生成测试报告后，提示执行 /skill:human gate=Gate3	human 记录 Gate3 决策
progress-tracker	增加 human_status 字段，从 human-decisions.md 读取	human 更新 progress-tracker 状态
self-check	增加检查项："当前 Gate 是否已通过 human skill 确认？"	self-check 调用 human 状态做准入校验
九、使用示例（完整走一遍）
bash
复制
# 1. 生成概要需求
/skill:prd-generation
# AI产出5个spec，并提示：
# "产出物已保存至 specs/。请阅读后执行：/skill:human gate=Gate1 action=sign-off"

# 2. 人工阅读后，确认通过
/skill:human gate=Gate1 action=sign-off result=passed issues="P1: 批量导入边界待补充"
# AI返回：
# "Gate1 已记录。遗留问题已标记。现在可以执行：/skill:detailed-requirements"

# 3. 生成详细需求
/skill:detailed-requirements
# AI产出prototype，提示执行 Gate2.5

# 4. 人工逐页确认原型
/skill:human gate=Gate2.5 action=conditional result=passed issues="P1: loading态细化；P2: 移动端适配"
# AI返回：
# "Gate2.5 有条件通过。P1 请在 detailed-design 阶段修复，P2 记入下一迭代。现在可执行：/skill:high-level-design"

# 5. 查询状态（随时）
/skill:human action=status
# 查看当前变更卡在哪个 Gate，有什么遗留问题
十、总结
表格
维度	设计要点
本质	不是让人工"少做"，而是让人工决策"被记录、被追踪、成闭环"
核心文件	human-decisions.md——变更级的人工审计日志
阻塞机制	靠 SKILL.md 中的校验规则 + progress-tracker 状态联动实现
查询能力	action=history 查决策链，action=status 查当前阻塞点
与现有流程关系	插入在各阶段之间，作为"人工闸门"的统一载体，替代之前分散的确认提示
这个 skill 做好后，你的工具链就真正形成了 "AI 执行 → 人工确认 → AI 再执行" 的闭环，而且每一步确认都有据可查。建议作为 P0 优先级 实现。