# Skill 开发指南

> 本文档面向 skill 作者，提供编写高质量 AI Skill 的最佳实践。

## 核心原则：渐进式披露

Skill 的设计遵循 **三级加载** 架构，确保 AI 上下文窗口高效利用：

| 级别 | 内容 | 大小 | 加载时机 |
|------|------|------|---------|
| **Level 1 — 元数据** | Frontmatter（`name` + `description`） | ~100 tokens | 始终加载，用于匹配 |
| **Level 2 — 指令** | `SKILL.md` 正文 | < 5000 tokens（推荐 < 500 行） | 匹配成功后加载 |
| **Level 3 — 资源** | `references/`、`scripts/`、`assets/` | 无限制 | 执行时按需读取 |

**关键 implication**：`description` 决定了 skill 是否被触发。描述必须清晰、具体，包含「做什么」和「何时用」。

## 编写 `description` 的黄金法则

`description` 是 skill 的触发器，其质量直接决定 AI 能否在正确场景调用该 skill。

### ✅ 好的描述

```yaml
description: 执行代码审查，检查安全性、性能和可维护性问题。适用于提交前代码审查、重构评估和代码走读场景。
```

特点：
- 明确功能（做什么）
- 明确场景（何时用）
- 包含触发关键词（代码审查、提交前、重构）

### ❌ 差的描述

```yaml
description: 一个关于代码的 skill。
```

问题：
- 过于笼统
- 没有触发场景
- AI 无法判断是否应激活

## `SKILL.md` 正文结构

建议采用以下模块化结构：

```markdown
---
name: skill-name
description: 清晰描述...
metadata:
  tags: "tag1,tag2"
---

# Skill 标题

## 适用场景
- 场景 1
- 场景 2

## 核心职责
1. 职责 1
2. 职责 2

## 执行步骤
1. 步骤 1
2. 步骤 2

## 输出格式
- 输出项 1
- 输出项 2

## 注意事项
- 注意 1
- 注意 2

## 示例

### 示例 1：XXX 场景
```
输入...
```

预期输出...
```
```

### 设计建议

1. **解释「为什么」而非仅下达「必须」命令**
   - 避免：`MUST always check for SQL injection`
   - 推荐：`Check for SQL injection because user inputs may contain malicious payloads`

2. **使用示例驱动**
   - 提供 1–2 个完整的输入/输出示例，比抽象规则更有效。

3. **限制行数**
   - `SKILL.md` 正文控制在 **500 行以内**（官方推荐 < 5000 tokens）。
   - 详细内容移至 `references/` 目录。

4. **避免冗余上下文**
   - 不要重复常识（如「Python 是一种编程语言」）。
   - 聚焦该 skill 特有的知识、流程或约束。

## 目录与文件规范

```
skills/<category>/<skill-name>/
├── SKILL.md              # 必需
├── scripts/              # 可选：可执行脚本
├── references/           # 可选：深度参考资料
└── assets/               # 可选：模板与示例
```

### `scripts/` 目录

存放可执行脚本（Python、Bash 等）。脚本应：
- **自包含或明确文档化依赖**：优先使用标准库；若需第三方库，在 `compatibility` 字段或脚本注释中说明。
- 包含 `--help` 参数说明用法。
- 不硬编码 API Key、Token 等敏感信息。
- 优雅处理边界情况，提供有用的错误信息。

示例：
```python
#!/usr/bin/env python3
"""分析代码差异并输出审查要点。"""
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="分析代码差异")
    parser.add_argument("diff_file", help="差异文件路径")
    args = parser.parse_args()
    # ...

if __name__ == "__main__":
    main()
```

### `references/` 目录

存放深度参考资料，按需加载。官方规范推荐以下命名：
- `REFERENCE.md` —— 详细技术参考
- `FORMS.md` —— 表单模板或结构化数据格式
- 领域特定文件（如 `security-checklist.md`、`performance-rules.md`）

保持单个参考文件聚焦，文件越小，AI 按需加载时消耗的上下文越少。

### `assets/` 目录

存放静态资源：
- 文档模板（`report-template.md`）
- 配置文件示例
- 图片或数据文件

## 文件引用规范

在 `SKILL.md` 中引用其他文件时，必须使用**相对于 skill 根目录的相对路径**，且保持**一级深度**，避免深层嵌套引用链：

✅ 正确示例：
```markdown
See [the reference guide](references/REFERENCE.md) for details.

Run the extraction script:
scripts/extract.py
```

❌ 错误示例：
```markdown
See [deeply nested](../other/references/nested/thing.md)
```

## 测试 Skill

在提交新 skill 前，建议进行以下验证：

```bash
# 1. 格式校验
python3 scripts/validate.py --skill skills/<category>/<skill-name>

# 2. 手动测试：将 skill 安装到本地 AI 工具
./scripts/install.sh --tool kimi --skill skills/<category>/<skill-name> --target .

# 3. 触发测试：向 AI 提出该 skill 覆盖场景的问题，观察是否正确激活
```

## 提交前检查清单

- [ ] 目录名使用 kebab-case，无连续连字符 `--`
- [ ] `SKILL.md` 文件名全大写
- [ ] Frontmatter 包含 `name` 和 `description`
- [ ] `name` 与目录名一致，符合命名约束（1–64 字符，小写+数字+连字符）
- [ ] `description` ≤1024 字符，明确说明功能和场景
- [ ] `SKILL.md` 正文不超过 500 行
- [ ] 文件引用使用相对路径且保持一级深度
- [ ] 无敏感信息（API Key、Token、密码）
- [ ] 已更新 `index.json`
- [ ] `scripts/validate.py` 校验通过
