# 命名与分类规范

## Skill 目录命名

- 使用 **小写英文字母**，单词间用连字符 `-` 分隔（kebab-case）。
- 不允许空格、下划线或大写字母。
- **禁止连续连字符**（`--`），且不得以连字符开头或结尾。

✅ 正确示例：
- `code-review`
- `sql-optimization`
- `api-documentation`
- `requirement-analysis`

❌ 错误示例：
- `CodeReview`（含大写）
- `code_review`（含下划线）
- `api documentation`（含空格）
- `api--doc`（连续连字符）
- `-api-doc`（以连字符开头）

## 分类目录

Skill 按领域存放在 `skills/` 下的固定分类中：

| 分类目录 | 说明 | 示例 |
|---------|------|------|
| `core-deliverables/` | **核心交付物**：需求、架构、设计、开发、测试、部署等研发过程输出文档 | 需求分析、架构设计、测试方案、部署手册 |
| `development/` | 开发辅助工具与提效技能 | 代码生成、Git 自动化、Lint 配置、重构辅助 |
| `data-engineering/` | 数据工程 | ETL 管道、SQL 优化、数据建模 |
| `architecture/` | 架构设计（通用方法论） | 技术选型、容量规划、ADR 模板 |
| `writing/` | 技术写作与通用文档 | 博客撰写、README 优化、文案润色 |
| `analysis/` | 分析类（非研发过程专属） | 数据分析、竞品分析、用户画像 |
| `tools/` | 工具集成与外部系统对接 | FFmpeg 工作流、Docker 助手、CI/CD 脚本 |

> **原则**：`core-deliverables/` 专门收敛软件生命周期各阶段的过程文档类 skill，确保核心交付物受控、可迭代。工具类、辅助提效类 skill 应归入 `development/`、`tools/` 等其他目录。

## 文件命名

| 文件/目录 | 命名规范 | 说明 |
|-----------|---------|------|
| `SKILL.md` | 全大写 | Skill 核心文件，必须存在 |
| `scripts/` | 全小写 | 可执行脚本目录 |
| `references/` | 全小写 | 参考资料目录 |
| `assets/` | 全小写 | 静态资源目录 |
| 脚本文件 | kebab-case | 如 `analyze-diff.py`、`security-check.sh` |
| 参考资料 | kebab-case | 如 `performance-rules.md` |

## Frontmatter 规范

`SKILL.md` 的 YAML frontmatter 必须遵循 [Agent Skills Specification](https://agentskills.io/specification)。

### 必填字段

```yaml
---
name: code-review                    # 唯一标识符，与目录名一致
description: 执行代码审查...          # 描述技能作用和触发场景（≤1024 字符）
---
```

### 可选标准字段

```yaml
---
name: code-review
description: 执行代码审查...
license: MIT                          # 许可证名称或许可证文件名
compatibility: "需要 Python 3.9+"      # 环境要求（≤500 字符）
metadata:                             # 自定义键值对，用于扩展属性
  tags: "development,quality"
  platforms: "kimi,claude,cursor"
allowed-tools: "Read Bash Grep"       # 实验性：预批准的工具列表（空格分隔）
---
```

### 字段约束

- `name`：
  - 长度 1–64 字符
  - 仅允许小写字母 `a-z`、数字和连字符 `-`
  - 不得以连字符开头或结尾
  - **不得包含连续连字符 `--`**
  - 必须与父目录名完全一致

- `description`：
  - 长度 1–1024 字符
  - 必须非空
  - 明确说明「做什么」和「何时用」
  - 包含触发关键词，帮助 AI 识别相关任务

- `license`：
  - 建议简短（许可证名或捆绑的许可证文件名）

- `compatibility`：
  - 若提供，长度 ≤500 字符
  - 说明环境要求（目标产品、系统包、网络访问等）

- `metadata`：
  - 键值均为字符串的映射
  - 建议键名具有一定唯一性，避免冲突
  - 本项目约定使用 `tags`（逗号分隔）、`platforms`（逗号分隔）存放分类和平台信息

- `allowed-tools`：
  - 实验性字段，支持情况因平台而异
  - 空格分隔的工具名列表

## 版本与变更

Skill 的变更通过 Git 版本控制追踪，不单独维护版本号。如需标记重要变更，可在 `SKILL.md` 末尾添加：

```markdown
## 变更日志

- 2026-04-20: 初始版本
```
