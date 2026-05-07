# Skill 开发指南

> 本文档面向 skill 作者，提供编写高质量 AI Skill 的完整规范与最佳实践。
> 
> 规范来源：本项目 `AGENTS.md` + 外部最佳实践参考（Anthropic 官方设计原则、TRAE 团队经验）。

---

## 目录

1. [核心原则](#核心原则)
2. [目录与文件规范](#目录与文件规范)
3. [Frontmatter 规范](#frontmatter-规范)
4. [SKILL.md 正文规范](#skillmd-正文规范)
5. [五种设计模式](#五种设计模式)
6. [测试与验证](#测试与验证)
7. [提交前检查清单](#提交前检查清单)

---

## 核心原则

### 1. 渐进式披露（三级加载）

Skill 的设计遵循 **三级加载** 架构，确保 AI 上下文窗口高效利用：

| 级别 | 内容 | 大小 | 加载时机 |
|------|------|------|---------|
| **Level 1 — 元数据** | Frontmatter（`name` + `description`） | ~100 tokens | 始终加载，用于匹配 |
| **Level 2 — 指令** | `SKILL.md` 正文 | < 5000 tokens（推荐 < 500 行） | 匹配成功后加载 |
| **Level 3 — 资源** | `references/`、`scripts/`、`assets/` | 无限制 | 执行时按需读取 |

**关键 implication**：`description` 决定了 skill 是否被触发。描述必须清晰、具体，写**触发场景**而非功能清单。

### 2. 单一职责

每个 Skill 只做一件事。多个简单 Skill 由调用方（Agent 或工作流）编排组合，而非把多个功能塞进一个 Skill。

**反面例子**：一个 Skill 既能"查询数据库"又能"发送邮件"还能"生成报告"。
**正面例子**：三个独立 Skill —— `query-database`、`send-email`、`generate-report`，由工作流按顺序调用。

### 3. 不写通用知识，只写团队特有逻辑

模型本身已具备通用能力（写代码、查文档、搜索等）。Skill 的价值在于补充**项目特有的业务逻辑、流程约定和系统接入方式**。

- **不要写**："HTTP 请求需要包含 Authorization header"（通用常识）
- **要写**："EAC-UGate Token 的缓存机制在哪里、有效期多久、过期后怎么刷新"（团队特有）

### 4. Description 是触发器，不是说明书

`description` 必须描述**触发场景**（用户说了什么 / 什么情况下激活），而非功能清单。模型通过 description 判断"该不该调用这个 Skill"。

#### ✅ 好的描述（触发场景式）

```yaml
description: 当用户提交代码审查请求、提到'review'、'代码走读'或重构评估时触发。执行安全性、性能和可维护性审查。
```

特点：
- 明确触发条件（用户说什么/做什么时激活）
- 包含触发关键词（review、代码走读、重构）
- 模型一看就知道何时调用

#### ❌ 差的描述（功能清单式）

```yaml
description: 这个 Skill 可以查询知识库文档、创建文档、修改权限。
```

问题：
- 没有说明什么时候应该用它
- 模型会困惑："用户想操作知识库了，但我不确定这是不是最佳方式"

### 5. 不过度约束，给模型灵活性

Skill 指令不等于程序代码。AI 需要一定的灵活性来适应用户的具体语境。

- **好**："通常按 A → B → C 顺序执行，但如果用户明确指定了顺序，按用户意图优先。"
- **差**："必须严格按以下顺序：第一步...第二步...第三步..."

---

## 目录与文件规范

```
skills/<category>/<skill-name>/
├── SKILL.md              # 必需：核心指令（< 500 行）
├── meta.json             # 可选：全量元数据（版本、标签、设计模式等）
├── scripts/              # 可选：可执行脚本（Python / Bash）
├── references/           # 可选：深度参考资料（按需加载）
│   ├── REFERENCE.md      # 详细技术参考（推荐命名）
│   └── FORMS.md          # 表单模板（推荐命名）
└── assets/               # 可选：模板、示例文件（Generator 模式核心）
```

### `scripts/` 目录

存放可执行脚本。脚本应：
- **自包含或明确文档化依赖**：优先使用标准库
- 包含 `--help` 参数说明用法
- 不硬编码 API Key、Token 等敏感信息
- 重复使用的命令片段应抽到 `scripts/`，避免在 `SKILL.md` 中写死具体实现

### `references/` 目录

存放深度参考资料，按需加载。推荐命名：
- `REFERENCE.md` —— 详细技术参考
- `FORMS.md` —— 表单模板或结构化数据格式
- 领域特定文件（如 `security-checklist.md`、`performance-rules.md`）

保持单个参考文件聚焦，文件越小，AI 按需加载时消耗的上下文越少。

### `assets/` 目录

专门存放**结构化模板**（Generator / Pipeline 模式核心）：
- 文档模板（`report-template.md`）
- 代码脚手架
- 配置文件示例

---

## Frontmatter 规范

### Kimi Code 兼容性（强制）

Kimi Code 的 skill 加载器采用严格白名单校验，Frontmatter 中**仅允许 `name` 和 `description` 两个字段**。其他字段（如 `metadata`、`license`、`compatibility`）会导致加载报错。

```markdown
---
name: code-review
description: 当用户提交代码审查请求时触发...
---
```

### 字段约束

| 字段 | 约束 | 说明 |
|------|------|------|
| `name` | 1–64 字符，kebab-case，匹配目录名 | 必填 |
| `description` | 1–1024 字符，**建议 ≤ 200 字符** | 必填，必须写触发场景 |

### 扩展元数据（`meta.json`）

扩展信息统一存放在同目录的 `meta.json` 中：

```json
{
  "name": "code-review",
  "version": "1.0.0",
  "pattern": "reviewer",
  "domain": "python",
  "tags": ["development", "quality", "security"],
  "platforms": ["kimi", "claude", "cursor", "codex", "gemini"]
}
```

`meta.json` 扩展字段：
- `pattern`：设计模式，可选值 `tool-wrapper`、`generator`、`reviewer`、`inversion`、`pipeline`
- `domain`：领域标识（如 `fastapi`、`sql`、`react`）
- `version`、`tags`、`platforms`：版本管理与检索标签

---

## SKILL.md 正文规范

### 正文结构推荐

```markdown
# Skill 标题

## 适用场景
- 场景 1
- 场景 2

## 核心职责 / 执行步骤
1. 步骤 1
2. 步骤 2

## 输出格式
- 输出项 1
- 输出项 2

## Gotchas
- 踩坑点 1
- 踩坑点 2

## 示例
### 示例 1：XXX 场景
```

### 强制要求：必须包含 Gotchas 节

每个 `SKILL.md` 正文**必须**包含 `## Gotchas`（或 `## 注意事项` / `## 踩坑点` / `## Red Flags`）章节，列出：

- 认证信息过期后的处理方式
- 哪些操作是不可逆的（删除、取消、覆盖等）
- 特殊参数格式要求
- 常见误用场景与规避方法
- 调用频率限制或性能边界

**示例**：

```markdown
## Gotchas
- 审查范围：只审查当前变更涉及的文件，不展开全局重构建议
- 误报处理：若某条规则在特定上下文不适用，明确说明原因
- 安全红线：发现硬编码密钥、SQL 拼接、XSS 漏洞时，必须标记为阻塞项
```

### 设计建议

1. **解释「为什么」而非仅下达「必须」命令**
   - 避免：`MUST always check for SQL injection`
   - 推荐：`Check for SQL injection because user inputs may contain malicious payloads`

2. **使用示例驱动**
   - 提供 1–2 个完整的输入/输出示例，比抽象规则更有效

3. **限制行数**
   - `SKILL.md` 正文控制在 **500 行以内**
   - 详细内容移至 `references/` 目录

4. **避免冗余上下文**
   - 不要重复常识
   - 聚焦该 skill 特有的知识、流程或约束

### 危险操作 Hook（可选最佳实践）

对于删除文件、取消订单、覆盖数据等**破坏性操作**，在 `SKILL.md` 中设计 Hook 机制：

```markdown
## 危险操作 Hook
执行以下操作前，必须先获得用户明确确认：
- 删除文档
- 修改权限
- 导出数据

确认模板：
1. 列出受影响的对象
2. 询问："确认执行 {operation} 吗？（是/否）"
3. 只有用户回复"是"才继续
```

### 配置外置

需要用户提供配置（如 API Key、Token）的 Skill，应在 `SKILL.md` 中写清楚环境变量或配置文件位置，而不是每次要求手动输入。

### 有状态 Skill 需说明存储方式

如果 Skill 需要跨对话记住状态（用户偏好、Token 有效期等），在 `SKILL.md` 中说明状态存储路径（如 `~/.skill_prefs.json`）。

---

## 五种设计模式

新建 Skill 时，在 `meta.json` 中标注 `pattern`，并在 `SKILL.md` 中体现对应模式特征。

| 模式 | 适用场景 | 核心特征 |
|------|----------|----------|
| **tool-wrapper** | 需要注入专业知识 | 按需加载 `references/` 中的领域规范 |
| **generator** | 输出结构不稳定 | 从 `assets/` 加载模板，严格填充 |
| **reviewer** | 需要自动质量检查 | 从 `references/` 加载 checklist，逐条检查 |
| **inversion** | 需求不清晰 | 先提问收集信息，完整理解后再生成 |
| **pipeline** | 复杂任务易出错 | 强制分步骤执行，每步设检查点 |

**模式可以组合**：
- Pipeline 最后接 Reviewer 做质量校验
- Generator 前面加 Inversion 先收集信息
- Tool Wrapper 嵌入 Pipeline 每一步都加载专业知识

### 如何选择模式？

| 遇到的问题 | 推荐模式 |
|-----------|----------|
| 需要专业知识注入 | Tool Wrapper |
| 输出结构不稳定 | Generator |
| 需要自动评审 | Reviewer |
| 需求不清晰 | Inversion |
| 任务复杂易出错 | Pipeline |

---

## 测试与验证

在提交新 skill 前，进行以下验证：

```bash
# 1. 格式校验
python3 scripts/validate.py --skill skills/<category>/<skill-name>

# 2. 手动测试：将 skill 安装到本地 AI 工具
./scripts/install.sh --tool kimi --skill skills/<category>/<skill-name> --target .

# 3. 触发测试：向 AI 提出该 skill 覆盖场景的问题，观察是否正确激活
```

---

## 提交前检查清单

- [ ] 目录名使用 kebab-case，无连续连字符 `--`
- [ ] `SKILL.md` 文件名全大写
- [ ] Frontmatter **仅包含 `name` 和 `description`**（Kimi Code 兼容性要求）
- [ ] `name` 与目录名一致，符合命名约束（1–64 字符，小写+数字+连字符）
- [ ] `description` 写**触发场景**（用户说什么时激活），建议 ≤ 200 字符
- [ ] `description` ≤ 1024 字符
- [ ] `SKILL.md` 正文不超过 500 行
- [ ] `SKILL.md` 正文**包含 Gotchas 节**
- [ ] 同目录下已放置 `meta.json`（含 `tags`、`platforms`、`version`，建议含 `pattern`）
- [ ] 文件引用使用相对路径且保持一级深度
- [ ] 无敏感信息（API Key、Token、密码）
- [ ] 已更新 `index.json`
- [ ] `scripts/validate.py` 校验通过
