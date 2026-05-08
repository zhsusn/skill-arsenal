# Detailed Requirements 详细需求生成器 — 使用手册

> **Skill 版本**：V2.1  
> **适用阶段**：OpenSpec 阶段 2.5（模块级详细需求）  
> **前置依赖**：`prd-generation` 已冻结且 🚪 Gate 1 签字通过  
> **关联 Skill**：`prd-generation`、`high-level-design`、`self-check`、`human`、`progress-tracker`  
> **更新日期**：2026-05-08

---

## 一、这是什么

**detailed-requirements** 是你的「模块拆解工程师」。

当概要需求（PRD-000）已经冻结、你知道了系统有哪些模块之后，这个 Skill 会**逐个模块**帮你写出标准化的详细规格。每个模块产出 **5 个文件**：需求追溯、原型结构、数据契约、业务逻辑、交互状态机。

如果说 prd-generation 是在地图上画出「有哪些省」，detailed-requirements 就是在画出「每个省里有哪些市、每条路的交通规则、每个红绿灯的切换逻辑」。

> 💡 **一句话理解**：prd-generation 定「做什么」，detailed-requirements 定「每个功能具体怎么做、数据怎么流、按钮点了会发生什么」。

---

## 二、适用场景

### ✅ 什么时候用它

- **概要需求已冻结**："PRD-000 已经确认了，帮我按模块拆详细需求"
- **批量模块拆解**："系统有 5 个模块，帮我逐个写出详细规格"
- **补齐设计输入**："概要设计前需要模块级的接口定义和状态机"
- **强交互产品**："这个产品有大量前端页面，我需要精确的按钮级交互定义"

### ❌ 什么时候不用它

- **概要需求还没冻结**："先写详细需求，概要后面补" → **绝对不行**，必须先冻结 Gate 1
- **只需要深挖一个模块**："帮我详细分析一下支付模块的所有边界情况" → 用 `prd-feature-detail` 单模块深度模式
- **直接写代码**："别写文档了，直接帮我写登录接口" → 这不是本 Skill 的职责范围

---

## 三、核心功能

| 功能 | 说明 | 对你意味着什么 |
|------|------|--------------|
| **解析模块清单** | 自动读取 `03-functional-structure.md` 提取所有模块 | 你不需要手动列清单，AI 直接从冻结的概要需求里读 |
| **串行逐模块生成** | 一个模块一个模块地输出，不并行 | 每个模块都能得到充分的上下文关注，不会漏掉细节 |
| **五文件标准化输出** | 每个模块固定产出 spec / prototype / io-table / logic / interaction-spec | 不管是哪个模块，文档结构都一样，开发和测试读起来不费劲 |
| **按钮级交互状态机**（V2.1 新增） | 每个按钮、输入框、下拉框都有完整的「点击前→点击中→点击后」定义 | 开发不会再来问你"这个按钮报错时文案是什么" |
| **模块间一致性校验** | 自动检查 6 个维度：字段/状态/接口/规则/覆盖/交互规格 | 模块 A 和模块 B 不会定义同一个字段为不同类型 |
| **🚪 Gate 2.5 原型冻结**（V2.1 新增） | 全部生成后 AI 宣读阻塞提示，等你逐页确认交互规格 | 上线后不会因为"这个页面的报错状态和那个页面不一样"被用户吐槽 |

---

## 四、使用方式

### 4.1 启动方式

**方式一：自然语言触发（推荐）**

```
💫 PRD-000 已经冻结了，帮我按模块拆详细需求
```

```
💫 基于已冻结的概要需求，生成所有模块的详细规格
参考文档：@openspec/changes/{变更名}/specs/03-functional-structure.md
```

**方式二：斜杠命令触发**

```
/skill:detailed-requirements 为 reelforge 变更生成模块详细需求
```

**前置检查（AI 会自动执行）**：

```
Kimi：正在检查前置条件...
✅ 01-product-overview.md      存在
✅ 02-requirements-list.md     存在
✅ 03-functional-structure.md  存在
✅ 04-business-rules.md        存在
✅ 05-non-functional.md        存在
✅ Gate 1 状态：passed（human-decisions.md 已确认）

所有前置条件满足，开始生成。
```

> ⚠️ 如果 Gate 1 未通过，AI 会阻断并提示："请先完成 prd-generation 并确认 Gate 1 冻结。"

### 4.2 完整示例：AI 短剧生成平台

假设 `03-functional-structure.md` 中定义了以下模块：

| 编号 | 模块名称 | 优先级 |
|------|----------|--------|
| feature-01 | 剧本工坊 | P0 |
| feature-02 | 角色工厂 | P0 |
| feature-03 | 分镜工作室 | P0 |
| feature-04 | 渲染中心 | P1 |
| feature-05 | 系统设置 | P1 |

---

**Phase 1：模块识别**

```
Kimi：【Phase 1：模块识别】

已从 03-functional-structure.md 提取 5 个模块：
- feature-01-script-workshop（P0）
- feature-02-character-factory（P0）
- feature-03-storyboard-studio（P0）
- feature-04-render-center（P1）
- feature-05-system-settings（P1）

按优先级排序：P0 模块先生成。
```

---

**Phase 2：逐模块生成（以 feature-01-script-workshop 为例）**

```
Kimi：【Phase 2：生成 feature-01-script-workshop】

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
模块：剧本工坊（feature-01-script-workshop）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

上游追溯：
- US-001-001：Given 用户有剧本创意 When 进入剧本工坊 Then 可创建新剧本
- US-001-002：Given 用户编辑剧本 When 使用 AI 辅助 Then 获得续写建议

正在生成 5 个文件...
✅ _index.md        已保存
✅ spec.md          已保存（含 8 条 AC：3B/1NB/1N/2E/1D）
✅ prototype.md     已保存（4 个页面：/workshop, /workshop/edit, /workshop/ai-assist, /workshop/export）
✅ io-table.md      已保存（12 个输入字段，8 个输出字段）
✅ logic.md         已保存（3 个业务流程 + 剧本状态机）
✅ interaction-spec.md  已保存（18 个可交互元素）

保存路径：openspec/changes/ai-short-drama-platform-v1/specs/feature-01-script-workshop/
```

**interaction-spec.md 片段示例**：

```markdown
## 页面：剧本编辑页 /workshop/edit

### 元素：AI 续写按钮（#btn-ai-continue）
| 属性 | 说明 |
|------|------|
| 触发方式 | click |
| 前置条件 | 剧本内容非空，且光标位于段落末尾 |
| 立即反馈 | 按钮显示 loading spinner，编辑区置灰不可编辑 |
| 成功结果 | 在光标位置插入 AI 生成的续写内容，编辑区恢复可编辑，显示"续写完成"toast |
| 失败结果 | 按钮恢复可点击，编辑区恢复可编辑，显示红色 toast"生成失败，请重试" |
| 异常分支 | 网络中断 → 显示"网络异常，已保存本地草稿"；超时(10s) → 同失败结果处理 |
| 埋点事件 | `ai_continue_click`，携带参数：{script_id, cursor_position, word_count} |

### 页面跳转图
```mermaid
graph LR
    A[/workshop] -->|点击新建| B[/workshop/edit]
    B -->|点击 AI 续写| B
    B -->|点击导出| C[/workshop/export]
    B -->|点击返回| A
```
```

---

**继续生成其他模块...**

```
Kimi：【feature-02-character-factory】生成完毕 ✅
Kimi：【feature-03-storyboard-studio】生成完毕 ✅
Kimi：【feature-04-render-center】生成完毕 ✅
Kimi：【feature-05-system-settings】生成完毕 ✅
```

---

**Phase 3：模块间一致性校验**

```
Kimi：【Phase 3：一致性校验】正在扫描所有模块...

维度 1：字段一致性          ✅ 通过
维度 2：状态枚举一致性        ⚠️ 发现 Warning
  → feature-01 中剧本状态为 "draft/published/archived"
  → feature-03 中剧本状态为 "draft/submitted/approved"
  → 建议统一为 "draft/published/archived"

维度 3：接口依赖闭环          ✅ 通过
维度 4：业务规则冲突          ✅ 通过
维度 5：需求覆盖完整性        ✅ 通过（100% P0 需求已覆盖）
维度 6：交互规格冲突（V2.1）  ✅ 通过

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
校验结果：0 Error / 1 Warning / 5 ✅
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Warning 已写入 _consistency-report.md，建议确认状态枚举统一方案。
用户：统一为 draft/published/archived

Kimi：已更新 feature-03 的 logic.md。重新校验...
✅ 全部通过，进入 Gate 2.5
```

---

**Phase 4：🚪 Gate 2.5 原型冻结**

```
Kimi：【Phase 4：🚪 Gate 2.5 原型冻结】

全部 5 个模块已生成，一致性校验通过。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚪 Gate 2.5: 原型冻结 —— 等待人工逐页确认
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

产出物已保存至：openspec/changes/ai-short-drama-platform-v1/specs/feature-*/interaction-spec.md

请按以下清单逐页检查每个模块：

1. 📋 每个可交互元素的说明是否完整（按钮、输入框、下拉框）
2. 🔄 交互状态机是否覆盖：点击前 → 点击中（loading） → 点击后（成功/失败）
3. ⚠️ 异常分支是否完整：网络中断、权限不足、数据为空时的页面表现
4. 🔗 页面间跳转关系是否与 prototype.md 一致
5. 📊 埋点事件是否覆盖所有关键操作

建议检查顺序（按优先级）：
→ feature-01-script-workshop（P0）
→ feature-02-character-factory（P0）
→ feature-03-storyboard-studio（P0）
→ feature-04-render-center（P1）
→ feature-05-system-settings（P1）

确认后执行：/skill:human gate=Gate2.5 action=sign-off
⚠️ 未获得人工确认前，禁止进入 high-level-design 阶段。

用户：确认

Kimi：✅ Gate 2.5 已签字
   📋 更新 _modules-index.md：所有模块状态 → "原型已冻结"
   📊 调用 self-check 执行最终校验...
   📈 更新 progress-tracker：阶段 2.5 → 已完成
```

---

### 4.3 各阶段配合要点

| 阶段 | 你需要做什么 | 不要做什么 |
|------|-------------|-----------|
| **Phase 1** | 确认模块清单是否正确 | 不要临时加模块（应回溯修改 PRD-000） |
| **Phase 2** | 每模块生成后快速浏览，确认核心页面和功能无遗漏 | 不要要求 AI 一次生成所有模块（串行是设计特性） |
| **Phase 3** | 认真看一致性校验报告，特别是 Warning | 不要忽略 Warning（虽然不阻塞，但可能埋坑） |
| **Gate 2.5** | 逐模块打开 interaction-spec.md，检查关键交互路径 | 不要一句话不看就确认（交互遗漏是上线后 bug 主因） |

---

## 五、输出产物说明

### 5.1 模块级文件总览

每个模块目录下有 5 个标准文件：

| 文件 | 通俗解释 | 谁会读 | 什么时候读 |
|------|---------|--------|-----------|
| `spec.md` | 「这个模块做什么、不做什么、怎么算验收通过」 | 测试、项目经理、开发 | 开发前确认范围 |
| `prototype.md` | 「这个模块有哪些页面、页面怎么跳转、大概长什么样」 | UI 设计师、前端开发、产品经理 | 设计阶段 |
| `io-table.md` | 「这个模块有哪些数据字段、什么类型、从哪来到哪去」 | 后端开发、接口设计 | 接口设计阶段 |
| `logic.md` | 「这个模块的业务流程怎么走、状态怎么变、出错怎么办」 | 后端开发、架构师 | 技术设计阶段 |
| `interaction-spec.md` | 「每个按钮点了会发生什么、报错时页面怎么表现」 | 前端开发、产品经理 | 前端开发阶段 |

### 5.2 全局索引与报告

| 文件 | 内容 | 用途 |
|------|------|------|
| `_modules-index.md` | 所有模块的清单、状态、追溯关系 | 项目经理快速了解「哪些模块做完了、哪些有问题」 |
| `_consistency-report.md` | 一致性校验的完整报告 | 架构师审查「模块间有没有冲突」 |

### 5.3 输出路径示例

```
openspec/changes/ai-short-drama-platform-v1/specs/
├── feature-01-script-workshop/
│   ├── _index.md
│   ├── spec.md
│   ├── prototype.md
│   ├── io-table.md
│   ├── logic.md
│   └── interaction-spec.md
├── feature-02-character-factory/
│   └── ...
├── feature-03-storyboard-studio/
│   └── ...
├── feature-04-render-center/
│   └── ...
├── feature-05-system-settings/
│   └── ...
├── _modules-index.md
└── _consistency-report.md
```

---

## 六、常见问题

**Q1：为什么不能跳过概要需求直接写详细需求？**
> 详细需求的每个模块都严格继承自 `03-functional-structure.md` 的模块清单。如果概要没冻结，模块边界可能还在变——今天拆成 5 个模块，明天可能变成 7 个。详细需求写了一半再改模块清单，返工成本极高。

**Q2：为什么必须串行生成，不能一次性把所有模块都生成？**
> 两个原因：一是上下文窗口限制，并行生成会导致每个模块分到的注意力不足；二是编号和命名一致性，串行生成可以确保模块间的字段名、状态值、接口定义保持一致。如果并行，模块 A 可能把"剧本状态"定义为 `draft/published`，模块 B 定义为 `draft/submitted`——这种冲突后期修起来很头疼。

**Q3：如果发现某个模块粒度太大，可以拆成两个吗？**
> 不可以在这里拆。模块拆分必须在 `prd-generation` 阶段完成，通过修改 `03-functional-structure.md` 并重新冻结 Gate 1。detailed-requirements 的职责是「按给定模块输出规格」，不是「重新规划模块」。

**Q4：interaction-spec.md 看起来好繁琐，每个按钮都要写吗？**
> 是的，每个**可交互元素**都要写。但「纯展示元素」（如静态文本、只读图片）不需要。这个文件的存在意义是消除前端开发中的「灰色地带」——比如"这个按钮 loading 时能不能点""报错时错误文案显示在哪""网络断了要不要自动重试"——这些细节如果不在需求阶段定义清楚，开发阶段会来回确认，反而更浪费时间。

**Q5：模块没有前端页面（比如纯后台任务调度），也要写 interaction-spec.md 吗？**
> 要写，但内容可以是：「本模块无用户交互界面，交互规格 N/A」。这是为了统一五文件结构，让下游工具和开发人员知道「这个模块没有前端交互」是经过确认的，而不是遗漏了。

**Q6：一致性校验发现 Error 怎么办？**
> Error 必须修。AI 会指出具体是哪个模块、哪个字段/状态/交互元素冲突了，并给出修复建议。修复后 AI 会重新执行一致性校验，直到 Error = 0 才能进入 Gate 2.5。

**Q7：Gate 2.5 可以只检查 P0 模块，P1 后面再说吗？**
> 不建议。虽然技术上你可以分批次确认，但 Gate 2.5 的设计意图是「在开始进入技术设计前，确保所有交互规格都经过人工审查」。如果 P1 模块不检查，后续 high-level-design 可能会基于不完整的交互假设做技术方案。

**Q8：和 `prd-feature-detail` 有什么区别？**
> `detailed-requirements` 是**批量标准化**模式：读取模块清单，按统一模板为所有模块生成五文件。适合「模块已经清晰，需要快速补齐全部详细规格」的场景。
> `prd-feature-detail` 是**单模块深度**模式：针对一个模块进行穷尽式访谈和多轮澄清，适合「某个核心模块特别复杂，需要深度挖掘所有边界情况」的场景。

---

## 七、快速参考卡

### 7.1 指令速查

| 你想让 Kimi 做... | 发送的指令 |
|-------------------|-----------|
| 开始生成详细需求 | "PRD-000 已冻结，帮我按模块拆详细需求" |
| 指定参考文档 | "参考文档：@openspec/changes/{变更名}/specs/03-functional-structure.md" |
| 查看某模块产物 | "打开 feature-01-script-workshop 的 interaction-spec.md" |
| 修复一致性 Error | "请修复字段一致性冲突：feature-01 和 feature-03 的状态枚举统一为 draft/published/archived" |
| 确认 Gate 2.5 | "确认" 或 `/skill:human gate=Gate2.5 action=sign-off` |
| 冻结后提出修改 | "我需要修改 feature-02 的登录交互流程" → AI 会启动变更流程 |

### 7.2 下游接力指南

```
detailed-requirements (产出 feature-XX-*/)
    ├──→ [high-level-design] 读取 logic.md + io-table.md 做概要设计
    ├──→ [self-check] 读取全部模块文件执行最终校验
    └──→ [human] Gate 2.5 签字记录
```

### 7.3 Gate 2.5 逐页检查清单

检查每个模块的 interaction-spec.md 时，重点关注：

- [ ] **完整性**：每个按钮、输入框、下拉框、链接、开关都有定义
- [ ] **状态机闭环**：点击前（可点）→ 点击中（loading/禁用）→ 点击后（成功/失败）
- [ ] **异常分支**：网络中断、权限不足、数据为空、超时 —— 每种情况都有页面反馈
- [ ] **页面跳转**：prototype.md 里的页面流转图和 interaction-spec.md 里的跳转定义一致
- [ ] **埋点覆盖**：每个关键操作（提交、导出、删除、切换）都有埋点事件定义

---

## 八、版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| V2.1 | 2026-05-08 | 新增 `interaction-spec.md`（按钮级交互状态机）；新增交互规格冲突校验（Error 等级）；新增 🚪 Gate 2.5 原型冻结阻塞提示；强化串行生成与模块边界约束。 |
| V1.1 | 2026-05-07 | 初始版本。基于 prd-generation 五文件，按模块串行生成 spec/prototype/io-table/logic 四文件；执行模块间一致性校验。 |
