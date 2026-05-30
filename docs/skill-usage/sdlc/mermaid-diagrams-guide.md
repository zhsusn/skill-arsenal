# mermaid-diagrams 设计与使用手册

> 本文档为内部设计参考，说明 `mermaid-diagrams` skill 的设计意图、外部来源适配、与 `mermaid-diagram-patterns` 的融合方案，以及使用方式。

## 一、设计意图

在 AI 辅助编程工作流中，**可视化是降低认知负载的关键手段**。但 Mermaid 作为纯文本图表工具，存在以下痛点：
- AI 生成的 Mermaid 代码常有语法错误，直接导出会导致空白图或渲染失败
- 不同图表类型（ERD、Sequence、Flowchart）的语法细节容易混淆
- 缺乏系统化的校验-导出工作流（生成 → 校验 → 导出 → 报告）

本 skill 提供端到端的 Mermaid 工具链：**生成 → 校验 → 导出 → 报告**。

## 二、外部来源与适配

### 来源
本 skill 核心内容源自开源项目 [Agents365-ai/mermaid-skill](https://github.com/Agents365-ai/mermaid-skill)（MIT 许可证）。

### 适配改造
将外部 skill 引入 `skill-arsenal` 时，做了以下适配：

| 适配项 | 原始版本 | 改造后 |
|--------|---------|--------|
| Frontmatter | 含 `homepage`、`metadata`（Kimi Code 不兼容） | 精简为仅 `name` + `description`，扩展信息移至 `meta.json` |
| 描述风格 | 功能清单式（"Generate Mermaid diagrams..."） | 触发场景式（"当用户提到'画图'、'流程图'...时触发"） |
| 语言 | 英文为主 | 中文为主，保留 Mermaid 代码示例原样 |
| 校验环节 | 作为工作流步骤 | 强化为**必填环节**，增加常见校验错误说明 |
| references | 仅语法参考（FLOWCHART/SEQUENCE/CLASS-ER/OTHER-TYPES） | **融合 mermaid-diagram-patterns**，新增场景化模式速查 |

## 三、mermaid-diagram-patterns 融合方案

### 为什么融合？
原始 `mermaid-skill` 的 references 是**纯语法速查表**（类似字典），而 `mermaid-diagram-patterns`（smithery.ai）提供的是**场景化完整模板**（类似作文范文）。两者互补：
- **字典**：查询语法细节（箭头类型、节点形状、类关系）
- **范文**：按场景（ERD/Sequence/Flowchart/Architecture/State）提供可直接复用的完整示例

### 融合方式
不新建独立 skill，而是将 patterns 作为 `mermaid-diagrams` 的 **Level 3 参考资料**：

| 文件 | 类型 | 内容 |
|------|------|------|
| `references/FLOWCHART.md` | 语法速查 | 方向、节点形状、箭头类型、子图、特殊字符 |
| `references/SEQUENCE.md` | 语法速查 | 参与者声明、箭头类型、激活框、循环与条件、并行执行 |
| `references/CLASS-ER.md` | 语法速查 | 可见性修饰符、关系、基数、属性标记 |
| `references/OTHER-TYPES.md` | 语法速查 | 状态图、Git 图、甘特图、饼图、思维导图、C4 上下文 |
| `references/PATTERNS.md`（新增） | **场景化模式** | ERD/Sequence/Flowchart/Architecture/State 完整示例 + 约定表 + 样式指南 + Quality Checklist |
| `references/REFERENCE.md`（新增） | 索引 | 所有 references 的导航页 |

### SKILL.md 的联动增强
- **语法参考节**：新增指向 `references/PATTERNS.md` 的链接
- **质量检查清单**（新增章节）：9 项检查项（图表类型选择、标签清晰度、箭头方向、ERD 基数、激活条、决策点、subgraph 分组、注释、对比度）

## 四、使用手册

### 触发场景
当用户提到以下关键词时触发：
- "画图"、"流程图"、"时序图"、"架构图"
- "类图"、"ER图"、"状态机"
- "导出图片"、"生成 Mermaid"、"可视化"

### 工作流程
1. **检查依赖**：尝试 `mmdc --version`，不可用则回退到 Kroki API
2. **选择图表类型**：从 11+ 类型中选择（流程图、时序图、类图、ER 图、状态图、甘特图、饼图、Git 图、C4 上下文、思维导图）
3. **生成**：将 `.mmd` 文件写入磁盘
4. **校验（必填）**：`mmdc -i diagram.mmd -o /tmp/test.png 2>&1`
5. **导出**：使用 `mmdc` 或 Kroki API 生成 PNG/SVG/PDF
6. **报告**：告知用户输出文件路径

### 双通道导出
| 方式 | 命令 | 适用场景 |
|------|------|---------|
| **本地 mmdc** | `mmdc -i diagram.mmd -o diagram.png -w 2048 --backgroundColor white` | 离线环境、高质量输出、需要主题控制 |
| **Kroki API** | `curl -X POST ... https://kroki.io/mermaid/png -o diagram.png` | 无 Node.js、快速一次性图表、CI/CD 流水线 |

### 与上游 skill 的衔接
| 上游 | 衔接点 |
|------|--------|
| `functional-architecture-generator` | 生成的业务功能架构 `.mmd` 需要校验和导出时，调用本 skill |
| `high-level-design` | HLD 产出的 C4 架构图、ER 图、时序图、状态图需要校验和导出时，调用本 skill |
| `detailed-design` | 详细设计中的类图、时序图需要导出时，调用本 skill |

## 五、注意事项

- **校验先行**：禁止跳过校验直接导出，否则会生成损坏的图片文件
- **路径安全**：生成 `.mmd` 文件时优先使用当前工作目录，避免写入 skill 目录内部
- **网络依赖**：Kroki 需要外网访问，离线环境必须提前安装 `mmdc`
- **主题一致性**：同一文档中的多个图表建议统一主题（default/dark/neutral/forest/base）
