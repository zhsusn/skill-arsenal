---
name: documentation
description: 技术文档编写与结构优化，支持 README、API 文档、架构决策记录（ADR）等类型。适用于项目文档初始化、现有文档重构和技术写作辅助。
metadata:
  tags: "writing,documentation,communication"
  platforms: "kimi,claude,cursor,codex,gemini"
---

# Documentation

## 适用场景
- 新项目 README 初始化
- API 接口文档编写（OpenAPI / Markdown）
- 架构决策记录（ADR）撰写
- 操作手册（Runbook）和部署指南
- 现有文档的结构优化和可读性提升

## 核心职责
1. 根据项目信息生成清晰、完整的技术文档
2. 优化文档结构，确保逻辑递进、易于导航
3. 统一术语和风格，保持全文一致
4. 补充缺失的关键信息（如安装步骤、配置示例、故障排查）

## 文档类型模板

### README.md
标准结构：
1. 项目标题与一句话描述
2. 徽章（License、Build、Version）
3. 功能特性（Features）
4. 快速开始（Quick Start）
5. 安装说明（Installation）
6. 使用示例（Usage / Examples）
7. 项目结构（Project Structure）
8. 贡献指南（Contributing）
9. 许可证（License）

### API 文档
- 每个端点包含：描述、请求方法、URL、参数、请求示例、响应示例、错误码
- 使用表格呈现参数（名称、类型、必填、说明）

### ADR（Architecture Decision Record）
采用轻量级格式：
- 标题与日期
- 背景（Context）
- 决策（Decision）
- 后果（Consequences）
- 替代方案（Alternatives Considered）

## 写作原则

1. **读者优先**：明确目标读者（新手/资深/运维），调整技术深度
2. **示例驱动**：每个概念配一个最小可运行示例
3. **层次分明**：使用标题层级（## / ### / ####）构建信息架构
4. **简洁准确**：删除冗余修饰词，用主动语态
5. **可验证**：安装步骤、代码示例应可复现

## 输出格式

根据用户请求的文档类型，输出完整的 Markdown 内容。如有必要，提供改进建议对比（Before / After）。

## 示例

### 示例 1：优化现有 README

**输入片段**：
```markdown
# MyProject
This is a project. It can do many things. You need to install it first.
```

**优化输出**：
```markdown
# MyProject

> 一句话描述项目的核心价值。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## 功能特性
- 特性一：解决了什么问题
- 特性二：核心优势

## 快速开始

```bash
git clone https://github.com/user/repo.git
cd repo
pip install -r requirements.txt
python main.py
```

## 项目结构
```
repo/
├── src/          # 源代码
├── tests/        # 测试
└── docs/         # 文档
```
```

## 注意事项
- 不要替用户编造不存在的功能或参数
- 如果信息不足，列出需要用户补充的内容清单
- 保持 Markdown 格式规范（代码块标注语言、表格对齐等）

## 变更日志

- 2026-04-20: 初始版本
