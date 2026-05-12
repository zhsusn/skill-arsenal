---
name: documentation
description: 当用户要求编写README、创建架构决策记录（ADR）、编写操作手册/Runbook/部署指南，或需要重构、优化现有技术文档时触发。不负责需求/设计/接口契约等阶段产出物。
---

# Documentation

## 本文档 Skill 不负责（请使用对应阶段 Skill）

为避免与 SDLC 阶段 skill 的职责重叠，以下文档类型**不在本 skill 范围内**：

| 文档类型 | 正确 Skill | 说明 |
|---------|-----------|------|
| 概要/详细需求文档 | `prd-generation` / `detailed-requirements` | OpenSpec 规范需求 |
| 概要/详细设计文档 | `high-level-design` / `detailed-design` | 架构与模块级技术设计 |
| 接口契约 / OpenAPI | `interface-first-dev` | 前后端接口契约与 Mock |
| 实现计划 / 任务拆解 | `writing-plans` / `task-breakdown` | 开发路线图与可执行任务 |
| 代码审查报告 | `code-review` / `requesting-code-review` | 代码质量审查 |
| CHANGELOG / 发布说明 | `finish` / `release-management` | 变更归档与发布 |

## 适用场景
- 新项目 README 初始化
- 架构决策记录（ADR）撰写
- 操作手册（Runbook）和部署指南编写
- 已有技术文档的结构优化和可读性提升
- API 消费者文档（含请求/响应示例，面向调用方）编写

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

### ADR（Architecture Decision Record）
采用轻量级格式：
- 标题与日期
- 背景（Context）
- 决策（Decision）
- 后果（Consequences）
- 替代方案（Alternatives Considered）

### Runbook / 部署指南
标准结构：
- 环境要求与前置依赖
- 部署步骤（逐条、可复现）
- 配置参数说明（表格）
- 健康检查与验证命令
- 故障排查（常见问题 + 解决命令）
- 回滚步骤

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

## Gotchas

- 不要替用户编造不存在的功能或参数
- 如果信息不足，列出需要用户补充的内容清单
- 保持 Markdown 格式规范（代码块标注语言、表格对齐等）
- **设计/需求/接口契约文档请走对应阶段 Skill**：本 skill 触发词中的"API 文档"仅指面向调用方的**消费者文档**（含请求/响应示例），而非 `api-spec.md` 或 `openapi.yaml` 等技术规格
- **ADR 与 HLD 的关系**：`high-level-design` 负责产出架构决策本身，本 skill 仅负责将决策整理为轻量级 ADR 文档格式；若用户处于设计阶段，优先触发 `high-level-design`

## 变更日志

- 2026-05-12: 重构边界，增加免责声明，明确与阶段 Skill 的职责划分，迁移至 `engineering-foundations` 分类
- 2026-04-20: 初始版本
