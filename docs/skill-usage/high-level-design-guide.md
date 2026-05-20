# high-level-design 设计与使用手册

> 本文档为内部设计参考，说明 `high-level-design` skill 的设计意图、`system_architecture` 双视图结构的由来，以及与 `functional-architecture-generator` 的协作关系。

## 一、设计意图

`high-level-design`（概要设计）是 OpenSpec 阶段 3 的核心 skill，承上启下：
- **承上**：读取已冻结的 PRD-000（`specs/01-05.md`）和竞品分析（`competitive-analysis.md`）
- **启下**：为详细设计（`detailed-design`）和任务拆解（`task-breakdown`）提供架构基线

核心约束：**严格限定为架构层（影响 ≥2 个模块）**，禁止输出接口字段、类图、DDL、算法参数等详细设计内容。任何下钻内容必须拦截并引导至下游 skill。

## 二、system_architecture 双视图结构

### 背景
在改造前，`system_architecture` 章节只产出**单一技术架构图**（C4-Model 或简单 flowchart），存在以下问题：
- **业务方看不懂**：C4 Container 图展示的是 Gateway/Service/DB，产品经理关心的是商品域/订单域/支付域
- **缺少模块划分的可视化**：`03-functional-structure.md` 的模块清单是文字表格，没有带颜色编码和依赖关系的架构图
- `functional-architecture-generator` skill 引入后，其业务功能架构能力无处安放

### 双视图设计
将 `system_architecture` 重构为**技术架构图（默认）+ 业务功能架构图（可选）**的双视图结构：

```
01-system-architecture.md
├── 架构概览
├── 分层/服务划分（技术视角表格）
├── 技术架构图（C4-Model，默认必有）
│   └── C4Context / C4Container / C4Component
├── 业务功能架构图（可选，模块≥4或多业务域时补充）
│   ├── 划分视角与分区列表
│   ├── 业务功能架构总览（Mermaid flowchart + 颜色编码）
│   ├── 模块清单表
│   └── 关键架构说明
└── 边界与 Enforcement 机制
```

### 两个视图的分工

| 维度 | 技术架构图（C4-Model） | 业务功能架构图（functional-architecture-generator） |
|------|----------------------|---------------------------------------------------|
| **视角** | 技术视角 | 业务视角 |
| **受众** | 开发团队、架构师、运维 | 产品经理、业务方、项目经理 |
| **展示内容** | Gateway / Service / DB / Cache / MQ | 商品域 / 订单域 / 支付域 / 用户域 |
| **方法论** | C4-Model（Context→Container→Component） | 五维分区划分 + 颜色编码策略 |
| **Mermaid 类型** | `C4Context` / `C4Container` / `flowchart LR` | `flowchart TB` / `flowchart LR`（按决策树） |
| **颜色策略** | C4 标准色（#08427b Person / #1168bd System / #438dd5 Container） | 同色系渐变（大域背景 vs 节点色） |
| **输出时机** | **默认必有** | 模块数 ≥ 4 或存在多业务域时**可选补充** |

## 三、与 functional-architecture-generator 的协作

### 数据流
```
prd-generation
    ↓ 产出 03-functional-structure.md（文字模块清单）
high-level-design
    ↓ Step 2: 解析 03-functional-structure.md 提取模块清单
    ↓ system_architecture
        ├─ 技术架构图：high-level-design 自身生成（C4-Model）
        └─ 业务功能架构图：调用 functional-architecture-generator 方法论
            - 分区划分（用户角色/业务域/系统层级/生命周期）
            - 颜色编码（同色系渐变）
            - 布局决策树（TB/LR/单列/双列）
            - 模块清单表 + 关键架构说明
    ↓ 01-system-architecture.md 交付
detailed-design
    ↓ 基于 01-system-architecture.md 逐模块下钻
```

### 职责边界
- `high-level-design` 负责：**何时**生成业务功能架构图（判断条件：模块数 ≥ 4 或多业务域）
- `functional-architecture-generator` 负责：**如何**生成（分区方法论、颜色策略、布局决策树、Mermaid 代码）

两者不是调用关系（skill 不直接调用 skill），而是**知识引用关系**：`high-level-design` 在生成业务功能架构图时，遵循 `functional-architecture-generator` 定义的方法论和规范。

## 四、使用手册

### 触发场景
当用户要求以下操作时触发：
- "概要设计"、"high-level-design"、"HLD"
- "系统架构设计"、"技术选型"
- "基于已冻结 PRD 进入设计阶段"

### 前置依赖
| 上游 Skill | 产出物 | 用途 | 是否必需 |
|---|---|---|---|
| `prd-generation` | `specs/01-05.md` | 产品范围、模块清单、需求边界、非功能指标 | **必须** |
| `competitive-analysis` | `design/competitive-analysis.md` | 技术选型论证支撑 | **必须** |
| `detailed-requirements` | `specs/feature-*/spec.md` | 模块功能细节，用于覆盖度校验 | 建议参考 |
| `human` | `human-decisions.md` | Gate 2 签字状态 | **必须** |

### 执行步骤
1. **配置加载**：读取 `openspec/config.yaml` 中 `artifact_specs.high-level-design`
2. **上游文档解析**：解析 `03-functional-structure.md`（模块清单）、`02-requirements-list.md`（P0/P1/P2）、`05-non-functional.md`（NFR）
3. **逐项生成**：按 `required_sections` 生成 18 个章节文件
4. **system_architecture 双视图生成**：
   - 技术架构图（C4-Model）：默认生成
   - 业务功能架构图：若模块数 ≥ 4 或存在多业务域，补充生成
5. **边界自检**：每章检查是否包含字段级定义、代码片段、单模块内部细节
6. **覆盖度校验**：校验 P0 模块覆盖、技术选型溯源、全局状态机兼容
7. **触发 self-check**：校验一致性、完整性、交叉引用有效性
8. **Gate 2 人工冻结**：宣读阻塞提示，等待人工签字

### 下游消费
| 下游 Skill | 消费文档 | 衔接规则 |
|---|---|---|
| `detailed-design` | `design/*.md` | 评审通过后按模块逐一下钻 |
| `task-breakdown` | `design/*.md` + `specs/feature-*/design.md` | 基于架构分层拆解任务 |
| `monitoring-setup` | `14-operations-architecture.md` | 基于运维架构生成监控规则初稿 |
| `human` | `design/*.md` + `rollback-plan.md` | Gate 2 人工冻结确认 |

## 五、关键设计决策

### 决策 1：为什么业务功能架构图是"可选"而非"必须"？
- 小型系统（模块数 < 4）通常不需要业务功能架构图，C4 Container 图已足够表达
- 强制生成会增加不必要的文档负担，违反"按需产出"原则
- 判断条件明确：模块数 ≥ 4 **或** 存在明显多业务域时补充

### 决策 2：为什么 C4-Model 作为技术架构图的标准？
- C4-Model 是业界公认的软件架构可视化标准（Simon Brown）
- 与 `mermaid-diagrams` skill 的 C4 支持能力天然衔接
- 层级清晰（Context→Container→Component），受众覆盖面广（从高管到开发）

### 决策 3：为什么不让 functional-architecture-generator 直接替代 system_architecture？
- `high-level-design` 的 `system_architecture` 是**18 章节文档的一部分**，需要与前后章节（tech_stack、data_architecture、interface_contracts）保持一致性
- 单独调用 `functional-architecture-generator` 会破坏文档的连贯性和上下文
- 最佳实践是**知识引用**：`high-level-design` 掌握何时生成，`functional-architecture-generator` 提供如何生成的方法论

## 六、注意事项

- **正向设计，非逆向分析**：基于需求生成架构，不是扫描现有代码
- **边界红线不可越**：概要设计只定义影响 ≥2 模块的决策
- **技术选型必须溯源**：每个选型必须关联 `competitive-analysis.md` 结论
- **模块遗漏 = BLOCKER**：未覆盖 P0 模块的架构设计不得通过自查
- **图表一致性**：Mermaid 图表必须从文本架构描述自动生成，禁止图表与文字描述矛盾
- **Gate 2 必须确认 rollback-plan**：很多技术债的根源是"能上线不能回滚"
