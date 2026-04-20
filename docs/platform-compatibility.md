# 平台兼容对照表

本文档记录各 AI 编程助手对 Skill 的支持情况、安装路径和格式差异。

## 路径对照表

| 平台 | 项目级路径 | 全局（用户级）路径 | 格式 |
|------|-----------|-------------------|------|
| **Kimi Code** | `.kimi/skills/` | `~/.kimi/skills/` | `SKILL.md` + 渐进式披露 |
| **Claude Code** | `.claude/skills/` | `~/.claude/skills/` | `SKILL.md` + 渐进式披露 |
| **Cursor** | `.cursor/skills/` | `~/.cursor/skills/` | `.mdc` 规则文件 |
| **OpenAI Codex** | `.codex/skills/` | `~/.codex/skills/` | `SKILL.md` + 渐进式披露 |
| **Gemini CLI** | `.gemini/skills/` | `~/.gemini/skills/` | `SKILL.md` + 渐进式披露 |
| **Aider** | — | — | `CONVENTIONS.md` |
| **Windsurf** | `.windsurf/skills/` | — | `SKILL.md` |

> **注意**：Windows 系统中 `~` 对应 `%USERPROFILE%`（如 `C:\Users\<用户名>`）。

## 安装方式

### Kimi Code

```bash
# 全局安装
./scripts/install.sh --tool kimi --all

# 项目级安装
./scripts/install.sh --tool kimi --skill skills/development/code-review --target .
```

### Claude Code

```bash
# 全局安装
./scripts/install.sh --tool claude --all

# 或使用 Claude Code 内置插件
/plugin marketplace add zhsusn/skill-arsenal
```

### Cursor

Cursor 使用 `.mdc` 规则格式，需先转换：

```bash
python3 scripts/convert.py --tool cursor --output .cursor/rules
```

### Codex CLI

```bash
./scripts/install.sh --tool codex --all
```

### Gemini CLI

```bash
./scripts/install.sh --tool gemini --all
```

## 格式差异说明

### 原生 `SKILL.md` 格式（Kimi / Claude / Codex / Gemini）

直接使用本仓库的 `SKILL.md` 文件，支持三级渐进式加载：
1. Frontmatter（`name` + `description`）用于匹配
2. `SKILL.md` 正文提供核心指令
3. `references/` 和 `scripts/` 按需加载

### Cursor `.mdc` 格式

Cursor 的规则文件采用以下结构：

```markdown
---
description: 规则的描述
globs: 适用的文件 glob 模式（如 *.py, *.ts）
alwaysApply: true/false
---

# 规则标题

规则内容...
```

转换脚本会自动将 `SKILL.md` 的 frontmatter 映射为 `.mdc` 格式。

### Aider `CONVENTIONS.md` 格式

Aider 将 skill 内容合并为单个 `CONVENTIONS.md` 文件，放置在项目根目录。

## 平台特有 Frontmatter 扩展

部分平台支持额外的 frontmatter 字段：

| 字段 | 平台 | 说明 | 标准状态 |
|------|------|------|---------|
| `argument-hint` | Claude Code | 斜杠命令参数提示 | 平台扩展 |
| `allowed-tools` | Claude Code / 部分平台 | 预批准的工具列表（空格分隔） | **Agent Skills 标准（实验性）** |
| `model` | Claude Code | 覆盖默认模型（haiku / sonnet / opus） | 平台扩展 |
| `globs` | Cursor | 规则适用的文件模式 | 平台扩展 |
| `alwaysApply` | Cursor | 是否始终应用 | 平台扩展 |

> 为保持跨平台兼容，建议仅在 `SKILL.md` 中使用标准字段（`name`、`description`、`license`、`compatibility`、`metadata`、`allowed-tools`），平台特有字段可通过转换脚本自动注入。

## `metadata` 字段的跨平台使用

`metadata` 是 Agent Skills 标准定义的扩展字段（键值对映射），可用于存放平台无关的自定义属性。本项目约定：

```yaml
metadata:
  tags: "development,quality"           # 逗号分隔的分类标签
  platforms: "kimi,claude,cursor"       # 逗号分隔的支持平台
```

不同平台对 `metadata` 的支持程度可能不同，但均会保留该字段供读取。
