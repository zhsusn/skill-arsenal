# skill-arsenal

> 个人 AI 技能（Skill）收藏库 —— 系统化收集、分类和管理面向各类 AI 编程助手的提示词技能与斜杠命令。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## 项目简介

`skill-arsenal` 是一个面向中文开发者的个人 AI Skill 仓库，遵循 [Agent Skills Specification](https://agentskills.io) 标准设计，支持渐进式披露（Progressive Disclosure），确保 AI 只在需要时加载必要的上下文。

本项目灵感主要来自：
- [anthropics/skills](https://github.com/anthropics/skills) —— 官方 Skill 格式标准与渐进式披露架构
- [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) —— 跨平台安装与转换机制
- [awesome-ai-agent-skills](https://github.com/seb1n/awesome-ai-agent-skills) —— 平台无关的通用能力库理念

## 支持的 AI 工具

| 平台 | 项目级路径 | 全局路径 | 状态 |
|------|-----------|---------|------|
| Kimi Code | `.kimi/skills/` | `~/.kimi/skills/` | ✅ 原生支持 |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` | ✅ 原生支持 |
| Cursor | `.cursor/skills/` | `~/.cursor/skills/` | ⚙️ 需转换 |
| OpenAI Codex | `.codex/skills/` | `~/.codex/skills/` | ✅ 原生支持 |
| Gemini CLI | `.gemini/skills/` | `~/.gemini/skills/` | ✅ 原生支持 |

> 详细兼容表见 [`docs/platform-compatibility.md`](docs/platform-compatibility.md)。

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/zhsusn/skill-arsenal.git
cd skill-arsenal
```

### 2. 安装 Skill 到本地

```bash
# 安装全部 skills 到 Kimi Code 全局目录
./scripts/install.sh --tool kimi --all

# 安装单个 skill 到当前项目
./scripts/install.sh --tool claude --skill skills/development/code-review --target .

# 查看支持的参数
./scripts/install.sh --help
```

### 3. 创建新 Skill

复制模板并修改：

```bash
cp -r templates/new-skill-template skills/<category>/my-new-skill
```

更多编写规范见 [`docs/skill-development-guide.md`](docs/skill-development-guide.md)。

## 项目结构

```
skill-arsenal/
├── README.md                       # 项目说明
├── LICENSE                         # MIT 许可证
├── index.json                      # 机器可读的技能索引
├── AGENTS.md                       # AI 助手上下文说明
├── scripts/                        # 工具脚本
│   ├── install.sh                  # 一键安装到各平台 skill 路径
│   ├── validate.py                 # 检查 SKILL.md 格式合规性
│   └── convert.py                  # 跨平台格式转换（如转 Cursor rules）
├── skills/                         # 核心技能库（按领域分类）
│   ├── core-deliverables/          # 核心交付物：需求、架构、设计、开发、测试、部署等过程文档
│   ├── development/                # 开发辅助工具与提效技能
│   ├── data-engineering/           # 数据工程
│   ├── architecture/               # 架构设计（通用方法论）
│   ├── writing/                    # 技术写作与通用文档
│   ├── analysis/                   # 分析类（非研发过程专属）
│   └── tools/                      # 工具集成与外部系统对接
├── commands/                       # 斜杠命令（快速触发）
│   ├── commit.md
│   └── review.md
├── hooks/                          # 生命周期钩子（预留）
├── templates/                      # 项目模板
│   └── new-skill-template/         # 新建 skill 的脚手架
│       ├── SKILL.md
│       └── scripts/
└── docs/                           # 文档
    ├── skill-development-guide.md
    ├── platform-compatibility.md
    └── naming-conventions.md
```

### 分类原则

- **`core-deliverables/`**：专门收敛软件生命周期各阶段的过程文档类 skill（需求、架构、设计、开发、测试、部署），确保核心交付物受控、可迭代。
- **`development/` / `tools/` / `writing/`**：存放工具类、辅助提效类 skill，不参与核心交付物管控。

## 单个 Skill 的结构

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

## 校验与质量门禁

```bash
# 检查所有 skill 的格式合规性
python3 scripts/validate.py

# 检查特定 skill
python3 scripts/validate.py --skill skills/development/code-review

# 转换所有 skill 为 Cursor 规则
python3 scripts/convert.py --tool cursor --output ./cursor-rules
```

## 现有 Skill 列表

| Skill | 分类 | 描述 | 支持平台 |
|-------|------|------|---------|
| `code-review` | development | 执行代码审查，检查安全性、性能和可维护性问题 | all |
| `git-automation` | development | Git 工作流自动化，生成规范提交信息 | all |
| `sql-optimization` | data-engineering | SQL 查询性能分析与优化建议 | all |
| `documentation` | writing | 技术文档编写与结构优化 | all |
| `requirement-analysis` | analysis | 需求分析与用户故事拆分 | all |

完整列表见 [`index.json`](index.json)。

## 贡献

目前为个人技能库，暂不开放外部贡献。如果你有任何建议，欢迎通过 Issue 讨论。

## 许可

[MIT](LICENSE) © 2026 zhsusn
