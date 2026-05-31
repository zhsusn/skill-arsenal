# Flowchart Syntax

> **v11 推荐**：统一使用 `flowchart` 关键字，不再使用 `graph`。

## Basic Structure

```mermaid
flowchart TD
  A[Client] --> B[API Gateway]
  B --> C[Auth Service]
  B --> D[Order Service]
  D --> E[(Order DB)]
  C --> F[(User DB)]

  subgraph Services
    C
    D
  end
```

## Direction

| Keyword | Direction |
|---------|-----------|
| `TD` / `TB` | Top to bottom |
| `LR` | Left to right |
| `RL` | Right to left |
| `BT` | Bottom to top |

## Node Shapes（形状语义化规范）

| Syntax | Shape | 语义用途 | 示例 |
|--------|-------|---------|------|
| `[text]` | Rectangle | 页面/界面/普通处理 | `Pg_Dashboard[项目 Dashboard]` |
| `(text)` | Rounded rectangle | 开始/结束/子流程入口 | `([开始])` `([结束])` |
| `{text}` | Diamond | 决策/判断 | `Dec_IsValid{输入合法?}` |
| `[(text)]` | Cylinder | 数据库/存储 | `[(User DB)]` |
| `[[text]]` | Subroutine | 外部调用/子系统 | `[[第三方支付]]` |
| `((text))` | Circle | 连接符/汇总点 | `(( ))` |
| `>text]` | Flag | 异步事件/信号 | `>Webhook]` |
| `{{text}}` | Hexagon | 进行中/准备步骤 | `{{St_Running{{运行中}}}}` |
| `[/text/]` | Parallelogram (右倾) | 成功/完成/输出 | `[/St_Passed[/已通关/]]` |
| `[\text\]` | Parallelogram (左倾) | 失败/阻塞/异常 | `[\St_Blocked[\已阻塞\]]` |

> **原则**：形状优先于颜色/emoj 承载语义。打印成黑白后，仅凭形状仍能区分类型。

## Arrow Types

| Syntax | Style | Use for |
|--------|-------|---------|
| `-->` | Arrow | 正向主流程 |
| `---` | Line | 连接 (无方向) |
| `-.->` | Dashed arrow | 回流/返回/重试/可选路径 |
| `==>` | Thick arrow | 重要主干/强调路径 |
| `--x` | X end | 终止 |
| `--o` | Circle end | 引用/关联 |

## Labels on Arrows

```mermaid
flowchart LR
  A -->|yes| B
  A -->|no| C
  B -->|"with quotes"| D
```

## 换行规则

```mermaid
flowchart TD
  %% ✅ 正确：使用 <br>
  A[第一行<br>第二行]

  %% ✅ 正确：使用 \n（需 htmlLabels: false）
  B["第一行\n第二行"]

  %% ❌ 错误：XML 自闭合标签在旧版渲染器中不生效
  %% C[第一行<br/>第二行]
```

## Subgraphs（阶段分组规范）

```mermaid
flowchart TD
  subgraph Phase_1["项目初始化"]
    A[新建项目] --> B{是否已存在?}
    B -->|否| C[创建目录]
    B -->|是| D[加载项目]
  end

  subgraph Phase_2["核心处理"]
    C --> E[解析配置]
    D --> E
    E --> F[执行业务逻辑]
  end

  subgraph Phase_3["完成归档"]
    F --> G[保存结果]
    G --> H([结束])
  end
```

**subgraph 规则**：
- 节点 > 10 时必须分组
- 命名格式：`Phase_XXX[阶段名]` 或 `Layer_XXX[层级名]`
- 每个 `subgraph` 必须有 `end`
- 嵌套不超过 3 层

## 样式集中声明规范

```mermaid
flowchart TD
  %% === 样式定义区（开头）===
  classDef page fill:#e1f5fe,stroke:#01579b,stroke-width:2px
  classDef decision fill:#fff3e0,stroke:#ef6c00,stroke-width:2px
  classDef state_running fill:#fffde7,stroke:#f9a825,stroke-dasharray:5 5
  classDef state_done fill:#e8f5e9,stroke:#2e7d32
  classDef state_fail fill:#ffebee,stroke:#c62828,stroke-width:3px
  classDef gate fill:#f3e5f5,stroke:#6a1b9a

  %% === 流程逻辑区 ===
  Start([开始]) --> Pg_Workbench[项目工作台]
  Pg_Workbench --> Dec_HasProject{是否已有项目?}
  Dec_HasProject -->|否| Pg_NewProject[新建项目向导]
  Dec_HasProject -->|是| Pg_Dashboard[项目 Dashboard]
  Pg_NewProject --> Pg_Dashboard

  Pg_Dashboard --> St_Running{{运行中}}
  St_Running --> Dec_Result{执行结果?}
  Dec_Result -->|成功| St_Passed[/已通关/]
  Dec_Result -->|失败| St_Blocked[\已阻塞\]

  St_Blocked -.->|重试| St_Running

  %% === 样式应用区（结尾）===
  class Pg_Workbench,Pg_Dashboard,Pg_NewProject page
  class Dec_HasProject,Dec_Result decision
  class St_Running state_running
  class St_Passed state_done
  class St_Blocked state_fail
```

## 特殊字符处理

```mermaid
flowchart LR
  %% 含冒号、括号、花括号
  A["Node: with colon"]
  B["Node (with parens)"]
  C["包含{变量}的节点"]
  D["数组 stages[]"]

  %% 含 & < > 等特殊符号
  E["A & B 协作"]
  F["1 < 2 判断"]

  %% 箭头标签含斜杠、空格
  A -->|"POST /api/v1"| B
  B -->|"4xx / 5xx"| C

  A --> B
  B --> C
  C --> D
  D --> E
  E --> F
```
