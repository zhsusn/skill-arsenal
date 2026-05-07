# Self-Check Skill 设计规格书

> 本文档面向 Skill 实现者与维护者，描述 `self-check` 的完整技术架构、检查流水线、Agent 分工及与外部系统的集成协议。

---

## 1. 功能定位

| 维度 | 说明 |
|------|------|
| 核心职责 | 产出物自查：内容一致性 + 内容完整性 + 交叉引用有效性 + 无内部矛盾 + 阶段特定检查 |
| 所属阶段 | 贯穿软件全生命周期（每个阶段完成后自动触发） |
| 执行方式 | 内联执行（不生成独立持久化文件，输出自查报告到对话） |
| 设计模式 | `reviewer`（审查员模式） |
| 开源对标 | spellbook 的 `auditing-green-mirage` / `fact-checking` / `verifying-hunches`（部分满足，需改造） |

---

## 2. 总体架构

```
┌─────────────────────────────────────────────────────────────┐
│                    self-check Skill                          │
├─────────────────────────────────────────────────────────────┤
│  触发方式：阶段完成后自动触发 / 手动触发                       │
│  执行模式：内联执行（对话输出，不持久化文件）                   │
│  架构模式：主控 Agent + 5 个并行检查子 Agent                  │
│  复用来源：spellbook fact-checking + auditing-green-mirage   │
└─────────────────────────────────────────────────────────────┘
```

### 2.1 核心原则（复用 spellbook 验证哲学）

1. **零信任原则**：不假设产出物正确，每个结论必须有证据。
2. **证据溯源**：每个检查结果必须标注证据位置（`文件:行号` 或 `章节`）。
3. **原子化验证**：将复合声明拆分为独立可验证单元（复用 fact-checking 原子分解）。
4. **测试必须能失败**：覆盖率检查不仅看数字，还要看测试是否真正验证行为（复用 auditing-green-mirage）。

---

## 3. 六大检查项

| 检查项 | 说明 | 通用阶段 | 编码阶段 | 测试阶段 |
|--------|------|----------|----------|----------|
| **内容一致性** | 与上游文档（概要需求/设计）对比，无矛盾 | ✅ | ✅ | ✅ |
| **内容完整性** | 对照 `config.yaml` 的 `required_sections`，无遗漏 | ✅ | ✅ | — |
| **交叉引用有效性** | 文档间 `@引用` 是否可解析 | ✅ | ✅ | — |
| **无内部矛盾** | 同一文档内无逻辑冲突 | ✅ | ✅ | — |
| **接口一致性** | 代码与 `api-spec.md` / `openapi.yaml` 对比 | — | ✅ | — |
| **覆盖率/测试有效性** | 单元测试覆盖率 ≥ 70%，且无 Green Mirage | — | — | ✅ |

---

## 4. 处理逻辑

### 4.1 主控流程

```
Step 1: 识别当前阶段 + 变更名
    ↓
Step 2: 读取 config.yaml 中该阶段的 required_sections
    ↓
Step 3: 加载 checklist-map（阶段文件清单与上游依赖）
    ↓
Step 4: 并行检查（5 个子 Agent 同时执行）
    ├── Agent 1: 内容一致性
    ├── Agent 2: 内容完整性
    ├── Agent 3: 交叉引用有效性
    ├── Agent 4: 无内部矛盾
    └── Agent 5: 阶段特定检查（编码/测试阶段）
    ↓
Step 5: 结果聚合与门控判断
    ├── 无 BLOCKER → 允许进入下一阶段
    └── 有 BLOCKER → 要求修复后重新自查
    ↓
Step 6: 输出结构化自查报告
```

### 4.2 Agent 1: 内容一致性检查（Consistency Agent）

**复用来源**：spellbook `fact-checking`（Claim Verification Pipeline）

**方法**：
1. **提取上游关键声明**：读取上游文档，识别所有事实性声明（如"系统面向 C 端用户"、"响应时间 < 2s"），输出声明清单 `[{id, claim, source_file, source_line}]`。
2. **定位对应表述**：扫描当前产出物，搜索语义对应，标记：一致 / 矛盾 / 缺失 / 需澄清。
3. **生成一致性报告**：输出映射表 `[{claim_id, current_location, status, evidence}]`。

**输出格式**：

| 上游结论 | 当前文档位置 | 状态 | 证据 |
|----------|--------------|------|------|
| 角色最大 100 个 | `spec.md:45` | ❌ 矛盾 | 详细需求写 50 个 |

### 4.3 Agent 2: 内容完整性检查（Completeness Agent）

**复用来源**：自建（spellbook 无直接对应）

**方法**：
1. 读取 `config.yaml` 中 `artifact_specs.{phase}.required_sections`。
2. 扫描产出物 Markdown 标题结构（H1/H2），建立标题索引。
3. 逐项匹配：`system_architecture` → 匹配到 "系统架构" ✅；`data_architecture` → 未找到 ❌。
4. 内容非空检查：匹配到的章节正文长度 > 100 字（或包含 Mermaid 图表）。
5. Mermaid 语法检查（可选）：提取 ` ```mermaid ` 代码块，检查基本语法。

**输出格式**：

| required_section | 对应章节 | 状态 | 缺失内容 |
|------------------|----------|------|----------|
| io_table | 输入输出表 | ❌ | feature-02-模块B 缺少 io-table.md |

### 4.4 Agent 3: 交叉引用有效性检查（Reference Agent）

**复用来源**：自建（spellbook 无直接对应）

**方法**：
1. **扫描 `@引用`**：正则 `@([^\s]+)`，如 `@openspec/changes/{change}/specs/01-product-overview.md`。
2. **文件存在性验证**：解析相对路径（基于项目根目录），检查文件系统是否存在。
3. **锚点验证**：若引用包含 `#锚点`，读取目标文件扫描对应标题。
4. **Markdown 链接验证**：扫描 `[text](path)`，检查相对路径文件是否存在。

**输出格式**：

| 引用路径 | 所在文件 | 状态 | 修复建议 |
|----------|----------|------|----------|
| `@specs/03-functional-structure.md` | `design.md:12` | ❌ | 文件不存在，请补充或修正路径 |

### 4.5 Agent 4: 无内部矛盾检查（Conflict Agent）

**复用来源**：spellbook `fact-checking`（原子声明分解思想）

**方法**：
1. **术语表提取**：扫描"术语：定义"模式，检测同一术语的不同定义。
2. **数值约束提取**：扫描数值表达式，标记潜在数值冲突（如"最大支持 100 个" vs "批量创建上限 50 个"）。
3. **状态机冲突检测**：提取 Mermaid `stateDiagram`，检查不可达状态、死循环、转换条件互斥性。
4. **权限矩阵矛盾**：提取 RBAC 矩阵，检查同一角色对同一资源的冲突权限、权限继承循环。

**输出格式**：

| 矛盾点 | 位置 A | 位置 B | 冲突描述 | 建议 |
|--------|--------|--------|----------|------|
| 角色定义 | `spec.md:23` | `spec.md:78` | 术语"角色"在两处定义不同 | 统一术语表 |

### 4.6 Agent 5: 阶段特定检查（Phase-specific Agent）

#### 4.6.1 编码阶段：接口一致性

**复用来源**：spellbook `fact-checking`（代码声明验证）

**输入**：代码文件 + `api-spec.md` + `openapi.yaml`

**方法**：
1. 提取代码接口定义（后端：`@app.get/@app.post` 装饰器；前端：API 调用函数）。
2. 提取 spec 接口定义（`api-spec.md` 表格 / `openapi.yaml` paths）。
3. 对比矩阵：接口路径、HTTP 方法、请求参数、响应结构、异常码。
4. 异常处理覆盖：读取 `design.md` 异常处理章节，检查代码中 `try/except` 或错误处理中间件。

#### 4.6.2 测试阶段：测试有效性

**复用来源**：spellbook `auditing-green-mirage`（反模式检测）

**输入**：测试代码 + 覆盖率报告

**方法**：
1. **覆盖率门控**：运行 `pytest --cov={module} --cov-report=term-missing`，判断 ≥ 70%。
2. **反模式检测（Green Mirage Audit）**：
   - 空断言：`assert True` / `assert None is None`
   - 同义反复：`assert len(list) == len(list)`
   - 过度 mock：mock 了被测对象本身的核心逻辑
   - 检查实现而非行为：`assert obj._internal_state == x`
   - 无法失败：测试路径无 assert 或无条件通过
3. **边界条件覆盖**：读取 `logic.md` 边界定义，检查空输入、最大值、异常值、并发场景。

---

## 5. 输入输出规格

### 5.1 输入数据

| 输入项 | 类型 | 来源 | 说明 |
|--------|------|------|------|
| 当前阶段标识 | 字符串 | 用户指令或上下文推断 | 如 `high-level-requirements` |
| 变更名 | 字符串 | 当前会话上下文 | 如 `feature-role-factory` |
| 产出物文件列表 | 文件路径数组 | 自动扫描阶段对应目录 | 根据 checklist-map 匹配 |
| 上游依赖文档 | 文件路径数组 | checklist-map 定义 | 前一阶段产出物 |
| `config.yaml` | YAML 文件 | `openspec/config.yaml` | 提取 `artifact_specs` 和 `rules` |
| 代码文件（编码阶段） | 文件路径数组 | 用户指定或自动扫描 | 如 `src/**/*.py` |
| 测试报告（测试阶段） | 文本/JSON | 工具生成 | `pytest --cov` 输出 |

### 5.2 输出数据

| 输出项 | 类型 | 格式 | 说明 |
|--------|------|------|------|
| 自查报告 | Markdown | 对话内联输出 | 含汇总表 + 阻塞/警告/通过明细 |
| 状态信号 | 结构化数据 | 内部传递 progress-tracker | `{stage, status, blockers[], warnings[]}` |

---

## 6. 门控与严重级别

| 级别 | 含义 | 流程影响 |
|------|------|----------|
| 🔴 **BLOCKER** | 必须修复 | **禁止进入下一阶段** |
| 🟡 **WARNING** | 建议修复 | 允许进入，但 progress-tracker 记录风险 |
| 🟢 **INFO** | 优化建议 | 不影响流程 |

**门控规则**：
- 存在 BLOCKER → 阶段状态锁定，输出"请修复以上阻塞问题后，重新执行 self-check"。
- 无 BLOCKER，存在 WARNING → 输出"可进入下一阶段，但需关注风险"。
- 全部通过 → 输出"自查通过，进入下一阶段"。

---

## 7. 与 Progress-Tracker 的集成协议

self-check 完成后，向 progress-tracker 发送状态更新：

```yaml
self_check_result:
  change_name: "{变更名}"
  stage: "{阶段名}"
  timestamp: "YYYY-MM-DD HH:mm"
  overall_status: "passed" | "warning" | "blocked"
  summary:
    total_checks: 24
    passed: 20
    warnings: 3
    blockers: 1
  blockers:
    - check_item: "content_consistency"
      file: "specs/feature-01/spec.md"
      line: 45
      description: "概要需求定义角色最大100个，详细需求写50个"
      severity: "high"
  warnings:
    - check_item: "cross_reference_valid"
      file: "design/01-system-architecture.md"
      line: 12
      description: "@specs/03-functional-structure.md 文件不存在"
      severity: "medium"
  next_action:
    blocked: "修复阻塞问题后重新执行 self-check"
    warning: "可进入下一阶段，但需关注风险"
    passed: "阶段完成，进入下一阶段"
```

> **注意**：self-check **只读** `progress.md`，不直接修改；通过状态信号传递结果。

---

## 8. 开源复用分析

### 8.1 能力映射

| self-check 检查项 | 可对标的 spellbook Skill | 复用度 | 差距分析 |
|-------------------|--------------------------|--------|----------|
| 内容一致性 | `fact-checking` | ⚠️ 部分 | fact-checking 聚焦代码/注释声明验证，self-check 需扩展到文档间一致性 |
| 内容完整性 | 无直接对应 | ❌ 不满足 | spellbook 无"章节完整性检查"能力，需自建 |
| 交叉引用有效性 | 无直接对应 | ❌ 不满足 | spellbook 无文件引用解析能力，需自建 |
| 无内部矛盾 | `fact-checking`（原子声明分解） | ⚠️ 部分 | 可借鉴原子声明分解，但需适配文档级矛盾检测 |
| 接口一致性 | `fact-checking` | ✅ 高 | 直接复用：提取接口声明 → 对照代码验证 |
| 覆盖率达标 | `auditing-green-mirage` | ✅ 高 | 直接复用：审计测试有效性 + 覆盖率检查 |

### 8.2 可复用组件

| 复用组件 | 来源 Skill | 复用方式 |
|----------|------------|----------|
| 声明提取引擎 | `fact-checking` | 改造为 Markdown 文档声明提取器 |
| 并行验证代理 | `fact-checking` | 复用子代理分派模式，每个检查项独立分派 |
| 分级信任报告 | `fact-checking` | 复用报告格式，增加 BLOCKER/WARNING/INFO 三级 |
| 反模式检测 | `auditing-green-mirage` | 改造为文档反模式（空章节、循环引用）+ 测试反模式 |
| 测试有效性审计 | `auditing-green-mirage` | 直接复用 Green Mirage 检测逻辑 |
| 假设验证框架 | `verifying-hunches` | 改造为文档假设验证（如"模块 A 依赖模块 B"是否成立） |

### 8.3 需自建的能力

| 能力 | 说明 | 实现建议 |
|------|------|----------|
| `required_sections` 对照检查 | 读取 config.yaml 章节定义，检查当前文档覆盖 | 读取 YAML → 扫描 Markdown 标题 → 生成缺失清单 |
| `@引用` 解析器 | 扫描文档中的 `@文件路径` 引用，验证文件是否存在 | 正则提取 `@路径` → 文件系统检查 |
| 文档间一致性比对 | 对比概要需求与详细需求中的同名概念定义 | 提取关键术语表 → 跨文档比对定义 |
| 阶段门控集成 | 将 self-check 结果作为阶段切换的必要条件 | 与 progress-tracker 联动，未通过则锁定阶段状态 |

---

## 9. 实施优先级

| 优先级 | 模块 | 说明 |
|--------|------|------|
| **P0** | Agent 2 完整性检查 + Agent 3 交叉引用 | 最基础能力，直接影响文档质量 |
| **P0** | 报告模板 + 门控集成 | 与 progress-tracker 联动，形成闭环 |
| **P1** | Agent 1 内容一致性 | 复用 fact-checking，实现文档级声明验证 |
| **P1** | Agent 5 编码/测试阶段检查 | 接口一致性 + 覆盖率门控，开发阶段刚需 |
| **P2** | Agent 4 内部矛盾检测 | 术语表 + 数值约束 + 状态机冲突 |
| **P2** | Mermaid 语法检查 | 增强图表可靠性 |
| **P3** | 自动化触发（阶段完成后自动执行） | 减少人工触发成本 |

---

## 10. 风险与规避

| 风险 | 规避方法 |
|------|----------|
| 大文档上下文溢出 | 子 Agent 只读取相关章节，不加载全文 |
| 误报率高 | 引入"需澄清"中间状态，人工确认后再定级 |
| 检查耗时过长 | 5 个 Agent 并行执行，单 Agent 超时 30 秒 |
| 与 progress-tracker 循环依赖 | self-check 只读 `progress.md`，不直接修改；通过状态信号传递 |

---

## 11. 附录：Checklist-Map 示例

```yaml
# 各阶段检查清单映射
high-level-requirements:
  files:
    - "openspec/changes/{change}/specs/01-product-overview.md"
    - "openspec/changes/{change}/specs/02-requirements-list.md"
    - "openspec/changes/{change}/specs/03-functional-structure.md"
    - "openspec/changes/{change}/specs/04-business-rules.md"
    - "openspec/changes/{change}/specs/05-non-functional.md"
  upstream:
    - "openspec/changes/{change}/proposal.md"

detailed-requirements:
  module_structure: "feature-{序号}-{模块名}/"
  files_pattern: "openspec/changes/{change}/specs/feature-*/"
  upstream:
    - "openspec/changes/{change}/specs/01-product-overview.md"
    - "openspec/changes/{change}/specs/03-functional-structure.md"

implementation:
  checks: [interface_consistency, exception_coverage]
  upstream:
    - "openspec/changes/{change}/specs/feature-*/api-spec.md"
    - "openspec/changes/{change}/specs/feature-*/design.md"

unit-test:
  checks: [coverage_threshold, test_validity]
  coverage_threshold: 70
  upstream:
    - "openspec/changes/{change}/specs/feature-*/test-plan.md"
    - "openspec/changes/{change}/specs/feature-*/logic.md"
```
