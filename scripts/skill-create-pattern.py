#!/usr/bin/env python3
# skill-create-pattern.py
import os, sys, argparse

PATTERNS = {
    "tool-wrapper": {
        "refs": ["conventions.md"],
        "assets": [],
        "scripts": [],
        "meta": {"pattern": "tool-wrapper", "domain": "<user-input>"},
        "template": """---
name: {name}
description: {description}
metadata:
  pattern: tool-wrapper
  domain: {domain}
---

你是一名 {domain} 开发专家。

## 核心规范
加载 'references/conventions.md' 以获取完整最佳实践列表。

## 代码评审时
1. 加载规范参考
2. 逐条检查代码
3. 对违规处指出规则并给出修复建议

## 编写代码时
1. 加载规范参考
2. 严格遵循每一条规范
"""
    },
    "generator": {
        "refs": ["style-guide.md"],
        "assets": ["template.md"],
        "scripts": [],
        "meta": {"pattern": "generator", "output-format": "markdown"},
        "template": """---
name: {name}
description: {description}
metadata:
  pattern: generator
  output-format: markdown
---

你是一个结构化内容生成器。

步骤 1：加载 'references/style-guide.md' 以获取语气和格式规则。
步骤 2：加载 'assets/template.md' 以获取输出结构。
步骤 3：向用户询问填充模板所需的缺失信息。
步骤 4：按样式指南填充模板，必须包含模板中每一个部分。
步骤 5：将完成的内容作为 Markdown 文档返回。
"""
    },
    "reviewer": {
        "refs": ["review-checklist.md"],
        "assets": [],
        "scripts": [],
        "meta": {"pattern": "reviewer", "severity-levels": "error,warning,info"},
        "template": """---
name: {name}
description: {description}
metadata:
  pattern: reviewer
  severity-levels: error,warning,info
---

你是一个代码审查员。

步骤 1：加载 'references/review-checklist.md' 以获取审查标准。
步骤 2：仔细阅读用户代码，先理解用途再评判。
步骤 3：逐条应用规则，对违规处：
  - 注明行号
  - 分类：error（必须修复）、warning（应该修复）、info（可考虑）
  - 解释原因，不只指出错误
  - 给出修改后的代码建议
步骤 4：生成结构化审查意见：
  - **摘要**：功能及总体质量
  - **发现项**：按严重级别分组
  - **评分**：1-10 分
  - **三大建议**：最具影响力的改进点
"""
    },
    "inversion": {
        "refs": [],
        "assets": ["plan-template.md"],
        "scripts": [],
        "meta": {"pattern": "inversion", "interaction": "multi-turn"},
        "template": """---
name: {name}
description: {description}
metadata:
  pattern: inversion
  interaction: multi-turn
---

你正在进行一次结构化需求访谈。在所有阶段完成之前，不要开始构建或设计。

## 第一阶段 — 问题发现（一次问一个问题，等待回答）
- Q1："这个项目解决什么问题？"
- Q2："主要用户是谁？技术水平如何？"
- Q3："预期规模多大？"

## 第二阶段 — 技术约束（第一阶段完成后）
- Q4："部署环境是什么？"
- Q5："技术栈要求或偏好？"
- Q6："不可协商的要求？"

## 第三阶段 — 综合（全部回答后）
1. 加载 'assets/plan-template.md'
2. 使用收集的需求填写模板
3. 展示计划并询问："这个计划准确吗？想修改什么？"
4. 根据反馈迭代，直到用户确认
"""
    },
    "pipeline": {
        "refs": ["quality-checklist.md"],
        "assets": ["output-template.md"],
        "scripts": ["step1_parse.py"],
        "meta": {"pattern": "pipeline", "steps": "4"},
        "template": """---
name: {name}
description: {description}
metadata:
  pattern: pipeline
  steps: "4"
---

你正在运行一个多步骤流水线。按顺序执行，某一步失败不要跳过。

## 步骤 1 — 解析与清单
分析输入，提取关键项并以检查表呈现。询问："这是全部内容吗？"

## 步骤 2 — 中间处理
（根据具体任务填充，如生成文档字符串/转换格式等）
在用户确认前，不要进入步骤 3。

## 步骤 3 — 组装
加载 'assets/output-template.md'，将所有内容编译成最终输出。

## 步骤 4 — 质量检查
根据 'references/quality-checklist.md' 审查：
- 完整性检查
- 格式检查
- 示例检查
报告结果，修复问题后再呈现最终文档。
"""
    }
}


def create_skill(name, description, pattern, output_dir="."):
    cfg = PATTERNS[pattern]
    skill_dir = os.path.join(output_dir, name)

    # 创建目录结构
    for sub in ["references", "assets", "scripts"]:
        os.makedirs(os.path.join(skill_dir, sub), exist_ok=True)

    # 写入 SKILL.md
    domain = input("请输入领域/主题（如 fastapi, python, react）：") if pattern == "tool-wrapper" else ""
    skill_md = cfg["template"].format(name=name, description=description, domain=domain)
    with open(os.path.join(skill_dir, "SKILL.md"), "w", encoding="utf-8") as f:
        f.write(skill_md)

    # 创建占位文件
    for ref in cfg["refs"]:
        open(os.path.join(skill_dir, "references", ref), "a").close()
    for ast in cfg["assets"]:
        open(os.path.join(skill_dir, "assets", ast), "a").close()
    for scr in cfg["scripts"]:
        open(os.path.join(skill_dir, "scripts", scr), "a").close()

    print(f"✅ Skill 创建完成: {skill_dir}")
    print(f"   模式: {pattern}")
    print(f"   请补充 references/ 和 assets/ 中的内容")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="带模式选择的 Skill 创建工具")
    parser.add_argument("name", help="Skill 名称")
    parser.add_argument("description", help="Skill 描述（触发词）")
    parser.add_argument("--pattern", choices=list(PATTERNS.keys()), help="设计模式")
    parser.add_argument("--dir", default=".", help="输出目录")
    args = parser.parse_args()

    pattern = args.pattern
    if not pattern:
        print("\n请选择设计模式：")
        for i, (k, v) in enumerate(PATTERNS.items(), 1):
            print(f"  {i}. {k:15s} - {v['meta']['pattern']}")
        choice = input("\n输入编号或名称: ").strip().lower()
        # 支持编号或名称
        if choice.isdigit() and 1 <= int(choice) <= len(PATTERNS):
            pattern = list(PATTERNS.keys())[int(choice) - 1]
        else:
            pattern = choice if choice in PATTERNS else "tool-wrapper"

    create_skill(args.name, args.description, pattern, args.dir)