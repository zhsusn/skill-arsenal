# skill-arsenal 项目说明

> 本文档面向 AI 编程助手。阅读前请注意：本项目目前已完成基础设施初始化，包含示例 skills、工具脚本和文档，但尚未引入构建系统或测试套件。

---

## 项目概览

`skill-arsenal` 是一个个人 AI **技能（skill）收藏库**，旨在系统化地收集、分类和管理面向各类 AI 编程助手（如 Kimi、Claude、Cursor、Codex 等）的提示词技能（skills）与斜杠命令（slash commands）。

项目当前状态：
- ✅ 已完成目录结构、脚本、模板和初始 skills 的创建。
- ✅ 包含 5 个示例 skill 和 2 个斜杠命令。
- ✅ 提供 `install.sh`、`validate.py`、`convert.py` 三个核心工具脚本。
- ❌ 尚未引入构建系统、测试套件或 CI/CD。

---

## 当前项目结构

```
skill-arsenal/
├── README.md                       # 项目说明、快速开始、平台兼容表
├── LICENSE                         # MIT 许可证
├── index.json                      # 机器可读的技能索引（供 skill-finder 使用）
├── AGENTS.md                       # 本文档
├── scripts/                        # 工具脚本
│   ├── install.sh                  # 一键安装到各平台 skill 路径
│   ├── convert.py                  # 跨平台格式转换（如转 Cursor rules）
│   └── validate.py                 # 检查 SKILL.md 格式合规性
├── skills/                         # 核心技能库（按领域分类）
│   ├── core-deliverables/          # 核心交付物：需求、架构、设计、开发、测试、部署等过程文档
│   ├── development/                # 开发辅助工具与提效技能
│   │   ├── code-review/
│   │   └── git-automation/
│   ├── data-engineering/           # 数据工程
│   │   └── sql-optimization/
│   ├── architecture/               # 架构设计（通用方法论，预留）
│   ├── writing/                    # 技术写作与通用文档
│   │   └── documentation/
│   ├── analysis/                   # 分析类（非研发过程专属）
│   │   └── requirement-analysis/
│   └── tools/                      # 工具集成与外部系统对接（预留）
├── commands/                       # 斜杠命令（快速触发）
│   ├── commit.md
│   └── review.md
├── hooks/                          # 生命周期钩子（预留）
├── templates/                      # 项目模板
│   └── new-skill-template/         # 新建 skill 的脚手架
│       ├── SKILL.md
│       └── scripts/
└── docs/                           # 文档
    ├── skill-development-guide.md  # 如何编写高质量 skill
    ├── platform-compatibility.md   # 各平台路径对照表
    └── naming-conventions.md       # 命名规范
```

### 分类原则

- **`core-deliverables/`**：专门收敛软件生命周期各阶段的过程文档类 skill（需求、架构、设计、开发、测试、部署），确保核心交付物受控、可迭代。
- **`development/` / `tools/` / `writing/`**：存放工具类、辅助提效类 skill，不参与核心交付物管控。

---

## 技术栈与构建流程

**当前状态：无技术栈。**

- 不存在 `pyproject.toml`、`package.json`、`Cargo.toml`、`Makefile` 或其他任何构建配置文件。
- 不存在运行时依赖、虚拟环境或容器化配置。
- 脚本使用标准 Python 库（`validate.py`、`convert.py`）和 Bash（`install.sh`）。

---

## 代码组织与模块划分

### 单个 Skill 的内部结构

每个 skill 目录遵循 **渐进式披露（Progressive Disclosure）** 原则：

```
skills/<category>/<skill-name>/
├── SKILL.md              # 必需：Frontmatter 元数据 + 核心指令（<500 行）
├── scripts/              # 可选：可执行脚本（Python / Bash）
├── references/           # 可选：深度参考资料（按需加载）
│   ├── REFERENCE.md      # 详细技术参考（推荐命名）
│   └── FORMS.md          # 表单模板（推荐命名）
└── assets/               # 可选：模板、示例文件
```

**`SKILL.md` 标准格式示例（符合 Agent Skills Spec）：**

```markdown
---
name: code-review
description: 执行代码审查，检查安全性、性能和可维护性问题
metadata:
  tags: "development,quality,security"
  platforms: "claude,kimi,cursor"
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
```

### Frontmatter 字段说明

遵循 [agentskills.io](https://agentskills.io/specification) 标准：

- **必填**：`name`（1–64 字符，kebab-case，匹配目录名）、`description`（1–1024 字符）
- **可选标准字段**：
  - `license`：许可证名称或文件名
  - `compatibility`：环境要求（≤500 字符）
  - `metadata`：自定义键值对映射（字符串→字符串），本项目约定存放 `tags`、`platforms`
  - `allowed-tools`：实验性字段，空格分隔的预批准工具列表

---

## 开发规范

### 命名与分类
- Skill 按领域分目录存放：`core-deliverables/`、`development/`、`data-engineering/`、`architecture/`、`writing/`、`analysis/`、`tools/`。
- 每个 skill 目录名使用小写英文字母，单词间用连字符 `-` 分隔（kebab-case），**禁止连续连字符 `--`**。
- 每个 skill 必须包含 `SKILL.md`，且文件名全大写。

### 渐进式披露（三级加载）
1. **Level 1**：AI 只读取 `SKILL.md` 的 Frontmatter（`name` + `description`），用于 skill 匹配。
2. **Level 2**：匹配成功后加载 `SKILL.md` 正文，获取核心指令。
3. **Level 3**：执行时按需加载 `references/` 和 `scripts/` 中的深度知识。

### 文件引用规范
- 引用 skill 内其他文件时，使用**相对路径**。
- 保持**一级深度**，避免深层嵌套引用链。

### 索引维护
- 维护根目录的 `index.json`，供外部工具（如 skill-finder）快速检索。
- 新增或修改 skill 后，应同步更新 `index.json` 并运行 `python3 scripts/validate.py` 校验。

---

## 测试策略

**当前状态：无测试。**

规划中建议引入：
- `scripts/validate.py`：对 `SKILL.md` 的 Frontmatter、目录结构、必填字段进行静态校验。
- GitHub Actions：在 PR 阶段自动运行校验脚本，确保索引与目录同步。

---

## 部署与发布

**当前状态：无部署流程。**

规划中建议：
- 通过 `scripts/install.sh` 将技能安装到本地 AI 工具目录（如 `~/.kimi/skills/`、`.claude/skills/`、`.cursor/skills/` 等）。
- 未来可考虑发布为 MCP Server，实现工具级集成。

---

## 安全注意事项

- Skill 中的 `scripts/` 目录可能包含可执行代码（Python / Bash）。在引入或执行任何脚本前，必须审查其内容，避免运行未经审核的命令。
- 避免在 `SKILL.md` 或脚本中硬编码 API Key、Token 或其他敏感凭证。
- 由于本仓库是个人技能库，若后续接受外部贡献，需对 PR 中的脚本和指令进行安全审计，防止提示词注入（Prompt Injection）或恶意代码执行。

---

## 实施路线

| 阶段 | 目标 | 状态 |
|------|------|------|
| **Phase 1：基础设施** | 建立目录结构和 `SKILL.md` 模板；编写 `index.json` 和 `scripts/install.sh`；迁移 5–10 个最常用的个人 skill。 | ✅ 已完成 |
| **Phase 2：工具化** | 添加 `validate.py` 检查格式合规；实现 `convert.py` 生成 Cursor rules / VS Code snippets；集成 GitHub Actions 自动更新索引。 | ⚙️ 部分完成 |
| **Phase 3：生态** | 编写贡献指南，接受 PR；发布到 awesome-agent-skills 等导航站；考虑打包为 MCP Server。 | ⏳ 未开始 |

---

## 对 AI 助手的提示

- **不要假设存在任何构建工具或包管理器**。当前项目没有 `npm install`、`pip install`、`cargo build` 等步骤。
- **优先阅读 `docs/tmp.txt`**。该文件是目前唯一包含项目设计意图的文档（历史参考）。
- **所有新增代码或脚本** 应遵循上述规划中的目录结构和命名规范。
- **语言**：项目文档和注释主要使用**中文**。
- 修改 skill 后，务必同步更新 `index.json` 并运行 `python3 scripts/validate.py`。
