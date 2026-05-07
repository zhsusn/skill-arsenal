# skill-arsenal

> **一套可扩展的 Skill 与 Spec 框架**，为软件全生命周期中的 AI 编码提供**标准化、可复用的质量保障**。
>
> *让开发行云流水，让产品超越预期。*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## 我们的目标

在 AI 编码助手日益普及的今天，提示词的质量直接决定了产出的上限。`skill-arsenal` 不仅仅是一个 Skill 收藏库，更是一套**可扩展的框架**：

- **标准化**：每个 Skill 遵循统一的 `SKILL.md` + `meta.json` 双轨制规范，配合 `validate.py` 静态校验，确保任何新增 Skill 都能被各平台正确识别与加载。
- **全生命周期覆盖**：从需求脑暴（`brainstorming`）→ 概要需求（`prd-generation`）→ 详细需求（`prd-feature-detail`）→ 概要设计（`high-level-design`）→ 详细设计（`technical-design-document-generator`）→ 编码（`code-review`、`test-driven-development`）→ 自查（`self-check`）→ 收尾（`finishing-a-development-branch`），每个阶段都有标准化的 AI 协作接口。
- **质量门控**：`self-check` 与 `progress-tracker` 贯穿全程，确保"不自查不流转"，让 AI 产出物具备可评审、可追溯、可冻结的工程质量。
- **可复用与可扩展**：通过 `config.yaml` 配置驱动输出模板，通过 `skill-create-pattern.py` 脚手架快速生成新 Skill，通过 `convert.py` 一键分发到 Kimi / Cursor / Aider / VS Code 等多平台。

无论你是个人开发者还是技术团队，都可以基于本框架快速搭建属于自己的 AI 编码质量体系。

---

## 项目概览

| 维度 | 现状 |
|------|------|
| **Skills** | **21 个**（覆盖 SDLC 全生命周期、数据工程、逆向工程） |
| **Slash Commands** | **2 个**（`/commit`、`/review`） |
| **核心工具脚本** | **4 个**（`install.sh`、`validate.py`、`convert.py`、`skill-create-pattern.py`） |
| **生成产物** | `.cursor/rules/*.mdc`（自动转换） |
| **构建依赖** | 零依赖（纯标准库 Python + Bash） |
| **自动化测试** | GitHub Actions 自动运行 `validate.py`（PR 阶段门禁） |

---

## 核心设计理念

### 1. 渐进式披露（Progressive Disclosure）

AI 只在需要时加载必要的上下文：

- **Level 1**：Frontmatter（`name` + `description`）用于 Skill 匹配
- **Level 2**：`SKILL.md` 正文提供核心指令
- **Level 3**：`references/` 与 `scripts/` 按需加载深度知识

### 2. 双轨制元数据（Kimi Code 兼容）

- `SKILL.md` Frontmatter **仅限 `name` + `description`**，避免严格白名单平台报错
- `meta.json` 存放扩展元数据（`version`、`tags`、`platforms`、`pattern`），供检索与转换使用

### 3. 配置驱动（Config-Driven）

各阶段 Skill 读取 `openspec/config.yaml` 中的 `artifact_specs` 定义，按 `required_sections` 输出，而非硬编码章节。这使得同一套 Skill 可以适应不同项目的文档规范。

### 4. 阶段门控（Phase Gate）

每个阶段完成后必须通过 `self-check` 自查，无 BLOCKER 方可进入下一阶段。概要设计评审通过前，严禁进入详细设计或编码实现。

---

## 项目结构

```
skill-arsenal/
├── README.md                       # 本文档
├── LICENSE                         # MIT 许可证
├── AGENTS.md                       # AI 助手上下文说明（面向 Agent）
├── index.json                      # 机器可读的技能索引
├── .gitignore                      # Git 忽略规则
├── .cursor/
│   └── rules/                      # 自动生成的 Cursor .mdc 规则文件
├── scripts/                        # 工具脚本
│   ├── install.sh                  # 一键安装到各平台 skill 路径
│   ├── validate.py                 # SKILL.md 格式合规性 + index.json 同步性校验
│   ├── convert.py                  # 跨平台格式转换（Cursor .mdc / Aider / VS Code）
│   ├── skill-create-pattern.py     # 带模式选择的 Skill 脚手架生成器
│   └── skill-create-pattern.txt    # 脚手架使用示例
├── skills/                         # 核心技能库（按领域分类）
│   ├── sdlc/                       # 软件全生命周期（SDLC）
│   │   ├── brainstorming/
│   │   ├── code-review/
│   │   ├── documentation/
│   │   ├── executing-plans/
│   │   ├── finishing-a-development-branch/
│   │   ├── git-automation/
│   │   ├── high-level-design/
│   │   ├── prd-feature-detail/
│   │   ├── prd-generation/
│   │   ├── prd-trace-matrix/
│   │   ├── progress-tracker/
│   │   ├── requesting-code-review/
│   │   ├── requirement-analysis/
│   │   ├── self-check/
│   │   ├── systematic-debugging/
│   │   ├── technical-design-document-generator/
│   │   ├── test-driven-development/
│   │   └── writing-plans/
│   ├── data-engineering/           # 数据工程
│   │   └── sql-optimization/
│   └── Reverse-Engineering/        # 逆向工程与元技能治理
│       └── skill-based-architecture/
├── commands/                       # 斜杠命令（快速触发）
│   ├── commit.md
│   └── review.md
├── hooks/                          # 生命周期钩子（预留）
├── templates/                      # 项目模板
│   └── new-skill-template/         # 新建 skill 的脚手架
│       ├── SKILL.md
│       └── meta.json
└── docs/                           # 文档
    ├── skill-development-guide.md      # Skill 编写完整手册
    ├── platform-compatibility.md       # 各平台路径对照表与格式差异
    ├── naming-conventions.md           # 命名规范与 Frontmatter 字段约束
    ├── high-level-design-spec.md       # high-level-design 设计规格书
    └── high-level-design-usage.md      # high-level-design 使用手册
```

### 分类原则

- **`sdlc/`**：收敛软件全生命周期内所有与软件交付过程直接相关的 skill（需求、架构、设计、开发、测试、部署、运维）。同一 skill 不得跨分类重复存放。
- **`data-engineering/`**：数据工程专用分类（SQL 优化、数据管道、数据建模等）。
- **`Reverse-Engineering/`**：元技能与项目规则治理类 skill（如将项目规则重构为 skill-based architecture），不参与具体软件交付过程。

---

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/zhsusn/skill-arsenal.git
cd skill-arsenal
```

### 2. 安装 Skill 到本地 AI 工具

```bash
# 安装全部 skills 到 Kimi Code 全局目录
./scripts/install.sh --tool kimi --all

# 安装单个 skill 到当前项目
./scripts/install.sh --tool claude --skill skills/sdlc/code-review --target .

# 查看支持的参数
./scripts/install.sh --help
```

### 3. 校验格式合规性

```bash
# 校验所有 skill + index.json 同步性
python3 scripts/validate.py

# 仅校验索引
python3 scripts/validate.py --index

# 校验单个 skill
python3 scripts/validate.py --skill skills/sdlc/high-level-design
```

### 4. 跨平台转换

```bash
# 生成 Cursor .mdc 规则文件（产物位于 .cursor/rules/）
python3 scripts/convert.py --tool cursor --all --output .cursor/rules

# 生成 Aider CONVENTIONS.md
python3 scripts/convert.py --tool aider --all --output .
```

### 5. 创建新 Skill

使用脚手架按设计模式生成：

```bash
python3 scripts/skill-create-pattern.py my-skill "My Skill Description" --pattern reviewer --dir ./skills/sdlc
```

内置模式：`tool-wrapper`、`generator`、`reviewer`、`inversion`、`pipeline`。

> ⚠️ 生成后请手动检查：若 `SKILL.md` Frontmatter 中包含 `metadata:` 字段，需移除并移至 `meta.json`（Kimi Code 兼容性要求）。

更多编写规范见 [`docs/skill-development-guide.md`](docs/skill-development-guide.md)。

---

## 平台兼容性

| 平台 | 项目级路径 | 全局路径 | 原生格式 | 备注 |
|------|-----------|---------|---------|------|
| **Kimi Code** | `.kimi/skills/` | `~/.kimi/skills/` | Skill 目录 | Frontmatter 严格白名单（仅 `name` + `description`） |
| **Claude Code** | `.claude/skills/` | `~/.claude/skills/` | Skill 目录 | 支持扩展 Frontmatter |
| **Cursor** | `.cursor/skills/` | `~/.cursor/skills/` | `.mdc` 规则 | 安装时自动调用 `convert.py` 转换 |
| **OpenAI Codex** | `.codex/skills/` | `~/.codex/skills/` | Skill 目录 | - |
| **Gemini CLI** | `.gemini/skills/` | `~/.gemini/skills/` | Skill 目录 | - |
| **Windsurf** | `.windsurf/skills/` | `~/.windsurf/skills/` | Skill 目录 | - |
| **Aider** | - | 项目根目录 | `CONVENTIONS.md` | 通过 `convert.py --tool aider` 生成 |
| **VS Code** | `.vscode/` | - | `.code-snippets` | 通过 `convert.py --tool vscode` 生成 |

> 详细路径对照与格式差异说明见 [`docs/platform-compatibility.md`](docs/platform-compatibility.md)。

---

## 现有 Skill 速览

### SDLC 全生命周期（`skills/sdlc/`）

| Skill | 触发场景 | 阶段 |
|-------|---------|------|
| `brainstorming` | 新功能探索、思路梳理、需求模糊时 | 阶段 0 |
| `requirement-analysis` | 需求澄清、用户故事拆分 | 阶段 1 辅助 |
| `prd-generation` | 从零写 PRD-000 概要需求 | **阶段 1** |
| `prd-feature-detail` | 基于冻结 PRD 生成单模块详细需求 | **阶段 2** |
| `prd-trace-matrix` | 需求追溯、变更影响分析 | 贯穿 |
| `high-level-design` | 系统架构设计、技术选型 | **阶段 3** |
| `technical-design-document-generator` | 基于 PRD 生成 SDD 详细设计 | **阶段 4** |
| `code-review` | 代码审查、重构评估 | 开发阶段 |
| `test-driven-development` | 编码前写测试 | 开发阶段 |
| `executing-plans` | 按已有计划执行多步骤任务 | 开发阶段 |
| `writing-plans` | 有需求后先写实施计划 | 开发阶段 |
| `requesting-code-review` | 完成任务后请求评审 | 开发阶段 |
| `finishing-a-development-branch` | 开发分支收尾、合并决策 | 开发阶段 |
| `systematic-debugging` | 遇到 Bug 时系统排查 | 开发阶段 |
| `git-automation` | 生成规范提交信息 | 开发阶段 |
| `documentation` | 编写技术文档、ADR、README | 贯穿 |
| `self-check` | 阶段完成后门控自查 | 贯穿 |
| `progress-tracker` | 跟踪项目进度、驱动阶段流转 | 贯穿 |
| `ai-architecture-advisor` | AI 项目架构选型、Agent 设计 | 架构咨询 |

### 数据工程（`skills/data-engineering/`）

| Skill | 触发场景 |
|-------|---------|
| `sql-optimization` | SQL 慢查询、索引、执行计划分析 |

### 逆向工程（`skills/Reverse-Engineering/`）

| Skill | 触发场景 |
|-------|---------|
| `skill-based-architecture` | 整理项目规则、重构为 skill 体系 |

### 斜杠命令（`commands/`）

| 命令 | 功能 |
|------|------|
| `/commit` | 生成 Conventional Commits 规范提交信息 |
| `/review` | 执行快速代码审查 |

完整列表与元数据见 [`index.json`](index.json)。

---

## 核心工具脚本

| 脚本 | 功能 | 技术栈 |
|------|------|--------|
| `install.sh` | 一键安装 skill 到各平台本地路径；支持 `--all`、`--skill`、`--target`、`--force` | Bash |
| `validate.py` | 校验目录名 kebab-case、SKILL.md Frontmatter 白名单、Gotchas 章节、index.json 同步性 | Python 3（标准库） |
| `convert.py` | 生成 Cursor `.mdc`、Aider `CONVENTIONS.md`、VS Code `.code-snippets` | Python 3（标准库） |
| `skill-create-pattern.py` | 交互式 Skill 脚手架，支持 5 种设计模式选择 | Python 3（标准库） |

---

## 文档索引

| 文档 | 面向读者 | 内容 |
|------|---------|------|
| [`AGENTS.md`](AGENTS.md) | AI 编程助手 | 项目结构、开发规范、Kimi Code 兼容性要求、工具脚本详解 |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | 贡献者 | 开发环境搭建、贡献流程、PR 规范、提交信息规范 |
| [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) | 所有参与者 | 社区行为准则（Contributor Covenant） |
| [`docs/skill-development-guide.md`](docs/skill-development-guide.md) | Skill 作者 | 如何编写高质量 skill：设计模式、Gotchas 要求、触发场景写法、渐进式披露 |
| [`docs/platform-compatibility.md`](docs/platform-compatibility.md) | 使用者 | 各平台路径对照表与格式差异说明 |
| [`docs/naming-conventions.md`](docs/naming-conventions.md) | Skill 作者 | 命名规范与 Frontmatter 字段约束 |
| [`docs/high-level-design-spec.md`](docs/high-level-design-spec.md) | 维护者 | high-level-design Skill 的设计规格书与开源复用分析 |
| [`docs/high-level-design-usage.md`](docs/high-level-design-usage.md) | 终端用户 | high-level-design Skill 的使用手册与 FAQ |

---

## 贡献

我们欢迎所有形式的贡献！无论是修复 Bug、新增 Skill、改进文档，还是提出想法。

- 请阅读 [`CONTRIBUTING.md`](CONTRIBUTING.md) 了解贡献流程与规范
- 参与前请先阅读 [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md)
- 新手指南：搜索带有 [`good first issue`](https://github.com/zhsusn/skill-arsenal/labels/good%20first%20issue) 标签的 Issue 开始

---

## 许可

[MIT](LICENSE) © 2026 zhsusn
