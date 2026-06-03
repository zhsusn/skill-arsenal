# skill-arsenal 项目说明

> 本文档面向 AI 编程助手。阅读前请注意：本项目为个人 AI 技能收藏库，已完成基础设施初始化与多轮技能扩充，但尚未引入构建系统、自动化测试套件或 CI/CD。

---

## 项目概览

`skill-arsenal` 是一个个人 AI **技能（skill）收藏库**，旨在系统化地收集、分类和管理面向各类 AI 编程助手（如 Kimi、Claude、Cursor、Codex、Gemini、Windsurf 等）的提示词技能（skills）与斜杠命令（slash commands）。

项目当前状态：
- ✅ 已完成目录结构、脚本、模板和初始 skills 的创建。
- ✅ 当前共包含 **19 个 skill** 和 **2 个斜杠命令**。
- ✅ 提供 `install.sh`、`validate.py`、`convert.py`、`skill-create-pattern.py` 四个核心工具脚本。
- ✅ 已生成 Cursor `.mdc` 规则文件（位于 `.cursor/rules/`）。
- ❌ 尚未引入构建系统、测试套件或 CI/CD。
- ❌ 脚本自身暂无单元测试，依赖手动验证。

---

## 当前项目结构

```
skill-arsenal/
├── README.md                       # 项目说明、快速开始、平台兼容表
├── LICENSE                         # Apache 许可证
├── AGENTS.md                       # 本文档（AI 助手上下文说明）
├── index.json                      # 机器可读的技能索引（供 skill-finder 使用）
├── .cursor/
│   └── rules/                      # 自动生成的 Cursor .mdc 规则文件
│       ├── code-review.mdc
│       ├── documentation.mdc
│       ├── git-automation.mdc
│       ├── requirement-analysis.mdc
│       └── sql-optimization.mdc
├── scripts/                        # 工具脚本
│   ├── install.sh                  # 一键安装到各平台 skill 路径
│   ├── validate.py                 # 检查 SKILL.md 格式合规性与 index.json 同步性
│   ├── convert.py                  # 跨平台格式转换（Cursor .mdc / Aider CONVENTIONS.md / VS Code Snippets）
│   ├── skill-create-pattern.py     # 带模式选择的 Skill 脚手架生成器
│   └── skill-create-pattern.txt    # skill-create-pattern.py 的使用示例
├── skills/                         # 核心技能库（按领域分类）
│   ├── sdlc/                       # 软件全生命周期（Software Development Life Cycle）
│   │   ├── brainstorming/
│   │   ├── code-review/
│   │   ├── documentation/
│   │   ├── executing-plans/
│   │   ├── finish/
│   │   ├── git-automation/
│   │   ├── prd-feature-detail/
│   │   ├── prd-system-outline/
│   │   ├── prd-trace-matrix/
│   │   ├── progress-tracker/
│   │   ├── requesting-code-review/
│   │   ├── requirement-analysis/
│   │   ├── systematic-debugging/
│   │   ├── technical-design-document-generator/
│   │   ├── test-driven-development/
│   │   ├── ai-architecture-advisor/
│   │   └── writing-plans/
│   ├── data-engineering/           # 数据工程
│   │   └── sql-optimization/
│   ├── Reverse-Engineering/        # 逆向工程与元技能治理
│   │   └── skill-based-architecture/
│   └── ...                         # 其他预留分类
├── commands/                       # 斜杠命令（快速触发）
│   ├── commit.md
│   └── review.md
├── hooks/                          # 生命周期钩子（预留，当前为空）
├── templates/                      # 项目模板
│   └── new-skill-template/         # 新建 skill 的脚手架
│       ├── SKILL.md
│       └── meta.json
└── docs/                           # 文档
    ├── skill-development-guide.md  # 如何编写高质量 skill
    ├── platform-compatibility.md   # 各平台路径对照表与格式差异说明
    └── naming-conventions.md       # 命名规范与 Frontmatter 字段约束
```

### 分类原则

- **`sdlc/`**：**软件全生命周期（Software Development Life Cycle）**主目录。收敛需求、架构、设计、开发、测试、部署、运维等所有与软件交付过程直接相关的 skill。任何在 SDLC 某一阶段被调用的技能均应归入此类，确保生命周期内技能统一入口、可检索、可迭代。
- **`data-engineering/`**：数据工程专用分类，存放与数据管道、SQL 优化、数据建模等相关的 skill。
- **`Reverse-Engineering/`**：存放元技能与项目规则治理类 skill（如将项目规则重构为 skill-based architecture），不参与具体软件交付过程。
- **`engineering-foundations/`**：工程基础能力分类，存放代码文档、单元测试、调试、正则表达式、提交规范、代码审查、工作流自动化等通用工程技能。
- **`learning/`**：学习知识分类，存放结构化笔记、考试准备、学习路线、概念解释、论文写作、记忆卡片、学习规划等与知识获取相关的 skill。
- **`office/`**：办公沟通分类，存放专业邮件、会议纪要、演示文稿准备等职场沟通相关的 skill。
- **`job-hunting/`**：求职面试分类，存放简历优化、面试准备、求职策略、offer 谈判、薪资沟通等求职全周期相关的 skill。
- **`research/`**：研究决策分类，存放深度研究合成、来源验证、知识结构化、竞争情报分析等研究与分析相关的 skill。
- **`content-creation/`**：内容表达分类，存放视频脚本、开场钩子、流程图构建等内容创作相关的 skill。
- **其他预留分类**：未来可按领域横向扩展（如 `devops/`、`security/` 等），但同一 skill 不得跨分类重复存放。

### 非 Skill 的参考文件

`skills/` 目录下还存在以下非正式 skill 文件，供设计与规划参考：
- `skills/info.txt`：`progress-tracker` skill 的详细设计规格与开源调研笔记。
- `skills/kimi+OpenSpec+superpower-v1.1.md`：一套完整的「Kimi + OpenSpec + Superpowers」AI 项目落地操作手册（V2.0），涵盖从概要需求到收尾归档的 10 个阶段工作流。该文件是历史设计意图的重要参考。

---

## 技术栈与构建流程

**当前状态：无传统技术栈，无构建流程。**

- 不存在 `pyproject.toml`、`package.json`、`Cargo.toml`、`Makefile` 或其他任何构建配置文件。
- 不存在运行时依赖、虚拟环境或容器化配置。
- 脚本仅使用**标准 Python 3 库**（`validate.py`、`convert.py`、`skill-create-pattern.py`）和 **Bash**（`install.sh`）。
- 无编译、无打包、无 `npm install` / `pip install` / `cargo build` 等步骤。

---

## 代码组织与模块划分

### 单个 Skill 的内部结构

每个 skill 目录遵循 **渐进式披露（Progressive Disclosure）** 原则：

```
skills/<category>/<skill-name>/
├── SKILL.md              # 必需：核心指令（<500 行），Frontmatter 仅含 name + description
├── meta.json             # 可选：全量元数据（版本、标签、兼容平台等）
├── scripts/              # 可选：可执行脚本（Python / Bash）
├── references/           # 可选：深度参考资料（按需加载）
│   ├── REFERENCE.md      # 详细技术参考（推荐命名）
│   └── FORMS.md          # 表单模板（推荐命名）
└── assets/               # 可选：模板、示例文件
```

**`SKILL.md` 标准格式示例（Kimi Code 兼容版）：**

```markdown
---
name: code-review
description: 当用户提交代码审查请求、提到'review'、'代码走读'或重构评估时触发。执行安全性、性能和可维护性审查。
---

# Code Review

## 适用场景
- 提交前代码审查
- 重构评估

## 审查清单
1. 检查 SQL 注入和 XSS 风险
2. 验证异常处理完整性
3. 评估算法复杂度

## 输出格式
- 严重问题（阻塞）
- 建议优化（非阻塞）
- 正面反馈

## Gotchas
- 审查范围：只审查当前变更涉及的文件，不展开全局重构建议
- 误报处理：若某条规则在特定上下文不适用（如测试文件允许 magic number），明确说明原因
- 安全红线：发现硬编码密钥、SQL 拼接、XSS 漏洞时，必须标记为阻塞项
```

> **Kimi Code 兼容性提示**：Kimi Code 的 skill 加载器采用严格白名单校验，Frontmatter 中**仅允许 `name` 和 `description` 两个字段**，其他字段（如 `metadata`、`license`、`compatibility`）会导致加载报错。本项目采用**双轨制**：`SKILL.md` 保持极简（name + description），扩展元数据统一存放在同目录的 `meta.json` 中。

### Frontmatter 字段说明

本项目为同时兼容 **Kimi Code**（严格白名单：仅允许 `name` + `description`）和 Claude / Cursor 等平台，采用**双轨制**设计：

#### `SKILL.md` Frontmatter（极简）

- **必填**：`name`（1–64 字符，kebab-case，匹配目录名）、`description`（1–1024 字符，**建议 ≤ 200 字符**）
- **description 写法**：必须描述**触发场景**（用户说什么/什么情况下激活），而非功能清单。错误："这个 Skill 可以查询文档、创建文档"。正确："当用户提到'查询文档'、'创建文档'时触发"。
- **禁止**：`metadata`、`license`、`compatibility`、`allowed-tools` 等扩展字段（会导致 Kimi Code 报错）

#### `meta.json`（全量元数据）

在同目录下放置 `meta.json`，存放扩展信息，供外部检索工具、版本管理和转换脚本使用：

```json
{
  "name": "code-review",
  "version": "1.0.0",
  "pattern": "reviewer",
  "tags": ["development", "quality", "security"],
  "platforms": ["kimi", "claude", "cursor", "codex", "gemini"]
}
```

`meta.json` 扩展字段建议：
- `pattern`：设计模式，可选值 `tool-wrapper`、`generator`、`reviewer`、`inversion`、`pipeline`
- `domain`：领域标识（如 `fastapi`、`sql`、`react`）
- `version`、`tags`、`platforms`：版本管理与检索标签

### 斜杠命令（Slash Commands）

`commands/` 目录存放快速触发指令，其 `SKILL.md` 风格的 frontmatter 中使用 `name: /command-name` 格式：
- `commit.md`：`/commit` —— 生成 Conventional Commits 规范提交信息。
- `review.md`：`/review` —— 执行快速代码审查。

---

## 开发规范

### 命名与分类
- Skill 按领域分目录存放。当前校验脚本认可的有效分类为：`sdlc`、`data-engineering`、`Reverse-Engineering`、`engineering-foundations`、`learning`、`office`、`research`、`content-creation`、`job-hunting`。
- 每个 skill 目录名使用小写英文字母，单词间用连字符 `-` 分隔（kebab-case），**禁止连续连字符 `--`**。
- 每个 skill 必须包含 `SKILL.md`，且文件名全大写。

### 渐进式披露（三级加载）
1. **Level 1**：AI 只读取 `SKILL.md` 的 Frontmatter（`name` + `description`），用于 skill 匹配。
2. **Level 2**：匹配成功后加载 `SKILL.md` 正文，获取核心指令。
3. **Level 3**：执行时按需加载 `references/` 和 `scripts/` 中的深度知识。

### 文件引用规范
- 引用 skill 内其他文件时，使用**相对路径**。
- 保持**一级深度**，避免深层嵌套引用链（如 `../` 或 `a/b/c/`）。

### 索引与元数据维护
- 维护根目录的 `index.json`，供外部工具（如 skill-finder）快速检索。
- 每个 skill 目录下建议放置 `meta.json`，存放 `tags`、`platforms`、`version`、`pattern` 等扩展元数据。
- 新增或修改 skill 后，应同步更新 `index.json` 和 `meta.json`，并运行 `python3 scripts/validate.py` 校验。

### Skill 编写原则（核心约束速查）

> **详细规范与最佳实践**见 `docs/skill-development-guide.md`。以下仅列出 AI 助手必须遵守的核心约束：

1. **单一职责**：一个 Skill 只做一件事，复杂工作流由调用方编排多个 Skill 组合完成。
2. **不写通用知识**：只补充项目/团队特有的业务逻辑、流程约定和系统接入方式。
3. **Description 是触发器**：必须写触发场景（用户说什么 / 什么情况下激活），建议 ≤ 200 字符。禁止功能清单式描述。
4. **必须包含 Gotchas 节**：每个 `SKILL.md` 正文必须包含 `## Gotchas`（或同义章节），列出踩坑点、危险操作、特殊约束。
5. **五种设计模式**（推荐在 `meta.json` 中标注 `pattern`）：`tool-wrapper`、`generator`、`reviewer`、`inversion`、`pipeline`。
6. **不过度约束**：保留模型根据对话上下文自然调整的空间。
7. **危险操作 Hook**：删除、覆盖等破坏性操作需设计确认机制。
8. **配置外置**：API Key、Token 等通过环境变量或配置文件提供，禁止硬编码。
9. **有状态 Skill 说明存储方式**：跨对话状态需明确持久化路径。
10. **执行生命周期（强制）**：所有 `generator`、`reviewer`、`pipeline` 模式的 Skill，应遵循 `docs/skill-execution-framework.md` 中的**五阶段三检查点**框架（输入分析 → 条目整理 → 原子执行 → 覆盖验证 → 总结归档），确保输入可追溯、输出可验证。`generator` 和 `pipeline` 模式必须在 `SKILL.md` 中显式实现阶段 4 的"条目回溯"与"幻觉检测"。

---

## 工具脚本详解

### `scripts/validate.py`
SKILL.md 格式合规性静态校验工具，完全基于标准库。

功能：
- 校验目录名是否为合法 kebab-case（不含连续连字符）。
- 校验 `SKILL.md` 是否存在、行数是否超过 500 行。
- 校验 YAML Frontmatter 是否存在，以及是否仅包含 `name` + `description`（对 Kimi 兼容性发出警告）。
- 校验 `name` 是否与目录名一致，长度是否在 1–64 字符之间。
- 校验 `description` 是否非空且不超过 1024 字符；**超过 300 字符时发出警告**（推荐触发场景式描述，≤ 200 字符）。
- 校验 skill 所属分类是否在允许列表中。
- 校验 `references/` 目录下是否包含推荐文件（`REFERENCE.md` 或 `FORMS.md`）。
- **校验 `SKILL.md` 正文是否包含 Gotchas / 注意事项 / 踩坑点 / Red Flags 章节（缺失时发出警告）**。
- 若存在 `meta.json`，校验其 JSON 格式及 `tags`、`platforms` 是否为字符串数组。
- 校验 `index.json` 与磁盘目录的一致性（索引中有但磁盘无，或磁盘有但索引无）。

使用方式：
```bash
python3 scripts/validate.py                  # 校验所有 skill + index.json
python3 scripts/validate.py --skill skills/development/code-review
python3 scripts/validate.py --index          # 仅校验索引
```

### `scripts/convert.py`
跨平台格式转换工具，完全基于标准库。

支持输出格式：
- `cursor`：生成 `.mdc` 规则文件（frontmatter 映射为 `description` + `globs` + `alwaysApply`）。
- `aider`：追加到 `CONVENTIONS.md`。
- `vscode`：生成 `.code-snippets` JSON 文件。

使用方式：
```bash
python3 scripts/convert.py --tool cursor --input skills/development/code-review --output .cursor/rules
python3 scripts/convert.py --tool cursor --all --output .cursor/rules
python3 scripts/convert.py --tool aider --all --output .
```

> **注意**：`.cursor/rules/*.mdc` 是由本脚本生成的产物。若 skill 内容更新，应重新运行转换脚本以同步规则文件，而非直接手动修改 `.mdc` 文件。

### `scripts/install.sh`
Bash 安装脚本，支持将 skill 安装到多种 AI 工具的本地 skill 目录。

支持平台：`kimi`、`claude`、`cursor`、`codex`、`gemini`、`windsurf`。

行为：
- 默认安装到用户全局路径（如 `~/.kimi/skills`）。
- 支持 `--target <path>` 安装到项目级路径（如 `./.kimi/skills`）。
- 安装到 Cursor 时会**自动调用 `convert.py`** 转换为 `.mdc` 格式。
- 支持 `--all` 批量安装和 `--force` 强制覆盖。

使用方式：
```bash
./scripts/install.sh --tool kimi --all
./scripts/install.sh --tool claude --skill skills/development/code-review --target .
```

### `scripts/skill-create-pattern.py`
带模式选择的 Skill 脚手架生成器，支持交互式选择。

内置模式：
- `tool-wrapper`：领域规范包装器。
- `generator`：结构化内容生成器。
- `reviewer`：代码/文档审查员。
- `inversion`：结构化需求访谈（多轮对话）。
- `pipeline`：多步骤流水线。

使用方式：
```bash
python3 scripts/skill-create-pattern.py api-expert "FastAPI 开发最佳实践"
python3 scripts/skill-create-pattern.py doc-pipeline "文档生成流水线" --pattern pipeline --dir ./skills
```

> **已知注意事项**：`skill-create-pattern.py` 的部分模板在生成的 `SKILL.md` frontmatter 中包含了 `metadata:` 字段。根据本项目 Kimi Code 兼容性规范，**应在生成后手动移除 frontmatter 中的 `metadata`，并将该信息移至 `meta.json`**。

---

## 测试策略

**当前状态：已引入 CI 基础门禁，脚本自身仍无单元测试。**

现有质量门禁：
- `scripts/validate.py`：对 `SKILL.md` 的 Frontmatter、目录结构、必填字段、索引一致性进行静态校验。
- **GitHub Actions**：在 PR 阶段自动运行 `validate.py` 与 `index.json` 语法检查，确保索引与目录同步。
- 手动测试：将 skill 安装到本地 AI 工具（`install.sh`），通过实际对话触发以验证行为。

规划中建议引入：
- 对 `validate.py` 和 `convert.py` 引入单元测试（当前无）。
- 集成测试：验证 `install.sh` 在各平台的安装行为。

---

## 部署与发布

**当前状态：无自动化部署流程。**

现有发布手段：
- 通过 `scripts/install.sh` 将技能安装到本地 AI 工具目录（全局或项目级）。
- 通过 `scripts/convert.py` 生成 Cursor / Aider / VS Code 兼容格式后手动分发。
- 未来可考虑发布为 MCP Server，实现工具级集成。

---

## 安全注意事项

- Skill 中的 `scripts/` 目录可能包含可执行代码（Python / Bash）。在引入或执行任何脚本前，必须审查其内容，避免运行未经审核的命令。
- 避免在 `SKILL.md` 或脚本中硬编码 API Key、Token 或其他敏感凭证。
- 本仓库已开放外部贡献。所有 PR 中的脚本和指令均需经过安全审计，防止提示词注入（Prompt Injection）或恶意代码执行。具体安全审查流程见 `CONTRIBUTING.md`。

---

## 实施路线

| 阶段 | 目标 | 状态 |
|------|------|------|
| **Phase 1：基础设施** | 建立目录结构和 `SKILL.md` 模板；编写 `index.json` 和 `scripts/install.sh`；迁移最常用的个人 skill。 | ✅ 已完成 |
| **Phase 2：工具化** | 添加 `validate.py` 检查格式合规；实现 `convert.py` 生成 Cursor rules / VS Code snippets / Aider 格式；扩充核心交付物与架构类 skill；生成 `.cursor/rules`。 | ⚙️ 部分完成 |
| **Phase 3：生态** | 编写贡献指南，接受 PR；发布到 awesome-agent-skills 等导航站；考虑打包为 MCP Server；引入自动化测试与 CI/CD。 | ⚙️ 进行中 |

---

## 对 AI 助手的提示

- **不要假设存在任何构建工具或包管理器**。当前项目没有 `npm install`、`pip install`、`cargo build` 等步骤。
- **所有新增代码或脚本** 应遵循上述规划中的目录结构和命名规范。
- **语言**：项目文档、注释和 skill 内容主要使用**中文**。
- **Kimi Code 兼容性**：新增或修改 skill 时，`SKILL.md` 的 Frontmatter **仅限 `name` + `description`**，其他元数据请放入 `meta.json`。
- **关于 `meta.json` 的说明**：`meta.json` 不是冗余文件，而是为兼容 Kimi Code CLI 严格白名单（仅允许 `name` + `description`）而采用的双轨制设计。部分 skill 检查工具（如 skill-creator）可能将其标记为"无关辅助文件"，这是误报——如果将元数据移回 Frontmatter，Kimi Code CLI 会直接拒绝加载该 skill。
- **修改 skill 后**，务必同步更新 `index.json`、`meta.json`，并运行 `python3 scripts/validate.py`。
- **`.cursor/rules/` 是生成产物**：若修改了 `skills/` 下的 skill 内容，应使用 `convert.py` 重新生成 `.mdc` 文件，而不是直接编辑 `.cursor/rules/` 下的文件。
- **编写规范权威文档**：`docs/skill-development-guide.md` 是人类贡献者的 skill 编写完整手册（含设计模式、Gotchas 要求、触发场景写法等）。AI 助手在协助编写 skill 时，应同时参考该文档和本 AGENTS.md 中的核心约束。
