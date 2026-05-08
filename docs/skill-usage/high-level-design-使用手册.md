# high-level-design（概要设计生成器）使用手册

**版本**: V2.1  
**最后更新**: 2026-05-08  
**适用对象**: 架构师、技术负责人、项目经理、开发者

---

## 1. 这是什么？

`high-level-design`（简称 HLD Skill）是一个**自动生成系统概要设计文档**的 AI 技能。

它能帮你把 PRD（需求文档）和竞品分析报告，快速转化为一份结构严谨、图表完备、可直接归档或评审的架构设计文档。核心就一句话：**告诉它你要做什么，它帮你画出系统怎么搭**。

### 一句话定位
> 影响 ≥2 个模块的架构决策，必须在写代码之前，用 HLD Skill 显性化、文档化、评审通过。

---

## 2. 适用场景

| 场景 | 示例 |
|------|------|
| 🏗️ 新系统立项 | 公司要做一个新的订单中台，需要输出架构设计文档给技术委员会评审 |
| 🔀 大规模重构 | 单体应用拆微服务，涉及多个模块边界重新划分 |
| 📊 技术选型 | 要在 Kafka vs RabbitMQ、MySQL vs TiDB 之间做决策，需要记录决策理由 |
| 🚀 跨团队协作 | 前端、后端、运维、测试都要看同一份架构蓝图，避免各自理解不一致 |
| 🛡️ 运维左移 | V2.1 新增——在设计阶段就把监控、告警、回滚方案一起考虑进去 |

**不适用的情况**：
- 只改一个接口的字段类型 → 用不到 HLD，直接写详细设计或代码即可。
- 纯 UI 页面调整，不涉及后端架构变更 → 不需要出 HLD。

---

## 3. 核心功能

### 3.1 自动生成 18 章标准化文档

从系统概述到附录，全覆盖。V2.1 特别新增了运维架构和回滚方案两章，让设计文档直接对接生产运维。

### 3.2 配置驱动，想写几章就写几章

通过 `config.yaml` 里的 `required_sections` 列表，自由裁剪。小项目可以只生成 8 章，大项目 18 章全拉满。

### 3.3 图表全自动生成

不需要你打开 Draw.io 画画。所有架构图、ER 图、时序图、部署拓扑图，都由 Skill 自动生成 **Mermaid** 代码，贴在文档里直接看。

### 3.4 Gate 2 设计冻结把关

生成完不是立刻能往下走。必须等人工审批（Gate 2）通过后，文档才算「冻结」，下游的详细设计和任务拆解才能开始。没通过？Skill 会明确提示你被阻塞了。

### 3.5 回滚方案双写（V2.1 新增）

回滚方案不再只藏在某次变更目录里，Skill 会自动同时写到项目级 `ops/rollback-plan.md`，让运维同学随时能找到最新有效的回滚指南。

---

## 4. 使用方式

### 4.1 前置准备

使用 HLD Skill 之前，请确保你已经准备好了以下材料：

1. ✅ **PRD 文档**（由 `prd-generation` Skill 生成或手写）
2. ✅ **竞品分析报告**（由 `competitive-analysis` Skill 生成或手写）
3. ✅ **`config.yaml`** 配置文件（项目根目录下）
4. ✅ **Gate 2 评审人**（需要一位架构师或技术负责人审批）

### 4.2 配置 `config.yaml`

在你的项目根目录创建或编辑 `config.yaml`：

```yaml
# ========== 必填项 ==========
project_name: order-platform        # 项目英文名，只能用小写字母、数字、连字符
domain: ecommerce                   # 领域：ecommerce / fintech / saas / iot / gaming / enterprise

# ========== 章节配置 ==========
required_sections:
  - 01-overview
  - 02-architecture-principles
  - 03-system-context
  - 04-functional-architecture
  - 05-technical-architecture
  - 06-data-architecture
  - 07-interface-design
  - 08-deployment-topology
  - 14-operations-architecture      # V2.1 新增：运维架构
  - 15-rollback-plan              # V2.1 新增：回滚方案
  - 16-disaster-recovery
  - 18-appendix

skip_sections:
  - 09-non-functional-requirements  # 当前项目暂不涉及
  - 17-cost-estimation              # 暂不评估成本

# ========== 可选配置 ==========
gate2_approver: "arch-lead@company.com"
operations:
  dual_write_rollback: true         # 开启回滚方案双写（推荐）
  generate_mermaid: true            # 自动生成 Mermaid 图表（推荐）
```

**💡 小贴士**：
- `project_name` 一旦确定就不要随便改，它会作为文件路径和文档标题的一部分。
- `required_sections` 至少保留 5 章，最多 18 章。不确定就选默认的 12 章。

### 4.3 触发 Skill

在 AI 对话中，用自然语言触发即可：

**示例 1：标准触发**
> "请为当前项目生成概要设计文档。PRD 在 `docs/prd/PRD-001.md`，竞品分析在 `docs/competitive-analysis.md`，配置用根目录的 `config.yaml`。

**示例 2：指定输出目录**
> "生成 HLD，输出到 `design/change-2026-q2-order-refactor/` 目录下。"

**示例 3：带 Gate 2 状态**
> "先生成 HLD 草稿，Gate 2 还在评审中，记得加上冻结阻塞提示。"

### 4.4 完整示例：从 0 到冻结

假设你是一个电商平台的技术负责人，正在规划「订单履约拆分」项目：

**Step 1：准备输入文件**

```
my-project/
├── docs/
│   ├── prd/
│   │   └── PRD-007-order-fulfillment.md
│   └── competitive-analysis.md
├── config.yaml
└── design/                    <-- HLD 将输出到这里
```

**Step 2：AI 对话触发**

> "我需要为订单履约拆分项目生成概要设计。请读取 `docs/prd/PRD-007-order-fulfillment.md` 和 `docs/competitive-analysis.md`，按照 `config.yaml` 的章节配置，输出到 `design/change-007/`。"

**Step 3：AI 执行过程**

1. 校验输入文件是否存在。
2. 读取 `config.yaml`，确定要生成哪些章节。
3. 逐章生成内容，嵌入 Mermaid 图表。
4. 生成 `15-rollback-plan.md`，并双写到 `ops/rollback-plan.md`。
5. 因为 Gate 2 还未审批，在 `DESIGN.md` 首页加上 **⚠️ 设计冻结阻塞提示**。
6. 输出完成，告诉你生成了哪些文件。

**Step 4：人工评审 Gate 2**

你把生成的 `design/change-007/DESIGN.md` 发给架构师评审。架构师确认没问题后，把 `design/change-007/.gate2-status` 文件内容改为 `approved`。

**Step 5：重新触发冻结**

> "Gate 2 已通过，请冻结当前 HLD 并广播给下游。"

AI 会：
- 在文档首页盖上 **"DESIGN FROZEN"** 水印。
- 创建 `.frozen` 令牌文件。
- 通知下游 Skill（详细设计、任务拆解、监控配置）可以开始工作。

---

## 5. 输出产物说明

生成完成后，你会在输出目录看到以下文件：

```
design/change-007/
├── DESIGN.md                          # 📄 汇总页，带目录，先看这个
├── 01-overview.md                     # 项目背景、目标、范围
├── 02-architecture-principles.md      # 架构原则（如：高内聚低耦合）
├── 03-system-context.md               # 系统与外部依赖的边界
├── 04-functional-architecture.md      # 功能模块划分
├── 05-technical-architecture.md       # 技术栈与分层
├── 06-data-architecture.md            # 数据模型与 ER 图
├── 07-interface-design.md             # 模块间接口契约
├── 08-deployment-topology.md          # 部署拓扑图
├── 14-operations-architecture.md      # 🆕 V2.1：监控、日志、链路追踪架构
├── 15-rollback-plan.md                # 🆕 V2.1：回滚触发条件与步骤
├── 16-disaster-recovery.md            # 灾备方案
├── 18-appendix.md                     # 术语表、参考资料
├── .frozen                            # 冻结令牌（Gate 2 后出现）
└── .hld-log.json                      # 生成日志（审计用）
```

同时，项目根目录会多出一个运维资产：

```
ops/
└── rollback-plan.md                   # 项目级最新回滚方案（由 15-rollback-plan.md 双写而来）
```

---

## 6. 常见问题（FAQ）

### Q1：生成的文档可以直接给老板/客户看吗？

**可以，但建议先过一遍。** Skill 生成的是「技术架构视角」的文档，如果你的老板更关心商业价值，建议在 `01-overview.md` 里补充业务背景段落。

### Q2：Mermaid 图表在某些编辑器里显示不出来怎么办？

- **GitHub / GitLab**：原生支持 Mermaid，直接推送即可渲染。
- **VS Code**：安装「Markdown Preview Mermaid Support」插件。
- **Typora**：偏好设置 → Markdown → 开启 Mermaid 图表。
- **其他编辑器**：可以复制 Mermaid 代码到 [Mermaid Live Editor](https://mermaid.live) 查看。

### Q3：我不想生成那么多章节，怎么精简？

编辑 `config.yaml` 的 `required_sections`，只保留你需要的章节编号。例如一个小工具类项目：

```yaml
required_sections:
  - 01-overview
  - 03-system-context
  - 05-technical-architecture
  - 07-interface-design
  - 08-deployment-topology
```

### Q4：Gate 2 是谁来审批？怎么审批？

由项目指定的架构师或技术负责人审批。审批方式目前为**人工操作**：评审人阅读 `DESIGN.md` 后，手动修改 `.gate2-status` 文件内容为 `approved`。未来可能接入 CI/CD 门禁。

### Q5：HLD 生成后需求变了怎么办？

如果 PRD 或 `config.yaml` 发生实质性变更，需要：
1. 重新触发 HLD Skill 生成新版文档。
2. 重新走 Gate 2 审批。
3. 旧版会被标记为 `SUPERSEDED` 并归档。

**注意**：Skill 有严格边界，不会自动帮你同步变更。一旦检测到输入变更，旧 `.frozen` 令牌会失效。

### Q6：回滚方案双写是什么意思？为什么要双写？

- **变更级**：`design/change-007/15-rollback-plan.md` 记录的是「这次变更」的回滚步骤。
- **项目级**：`ops/rollback-plan.md` 记录的是「整个项目当前最新有效」的回滚方案。

双写的目的是让运维同学不需要翻历史变更目录，直接去 `ops/` 就能找到最新回滚指南。

### Q7：为什么禁止下钻到详细设计？

概要设计的职责是**定边界、定接口、定拓扑**。如果往下写到「这个类有几个字段、那个函数怎么实现」，文档会迅速膨胀且难以维护。详细设计请交给下游的 `detailed-design` Skill。

---

## 7. 快速参考卡

### 7.1 触发口令速查

| 你想做什么 | 这样说 |
|-----------|--------|
| 生成完整 HLD | "请生成概要设计文档" |
| 生成草稿（Gate 2 未过） | "生成 HLD 草稿，加上冻结阻塞提示" |
| 指定输出目录 | "输出到 `design/change-xxx/`" |
| 冻结设计 | "Gate 2 已通过，冻结当前 HLD" |
| 只生成特定章节 | "只生成 01、05、08 三章" |

### 7.2 章节速查表

| 编号 | 章节 | 什么时候必须写 |
|------|------|--------------|
| 01 | 概述 |  always |
| 05 | 技术架构 |  always |
| 06 | 数据架构 |  涉及数据库变更 |
| 07 | 接口设计 |  涉及跨服务调用 |
| 08 | 部署拓扑 |  涉及环境变更 |
| 14 | 运维架构 |  V2.1 推荐 always |
| 15 | 回滚方案 |  涉及生产发布 |

### 7.3 文件检查清单

在告诉 AI "我准备好了" 之前，先确认：

- [ ] `config.yaml` 已在项目根目录
- [ ] `project_name` 和 `domain` 已填写
- [ ] `required_sections` 已按需配置
- [ ] PRD 文档路径正确且文件存在
- [ ] 竞品分析报告路径正确且文件存在
- [ ] 已指定 Gate 2 评审人

---

## 8. 版本变更记录

| 版本 | 日期 | 变更内容 |
|------|------|---------|
| V2.0 | — | 初始版本，支持 16 个标准章节生成 |
| **V2.1** | 2026-05-08 | 新增 14-operations-architecture、15-rollback-plan；新增 Gate 2 冻结阻塞提示；新增回滚方案双写规则 |
