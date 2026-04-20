---
name: /review
description: 对当前代码（diff 或指定文件）执行快速代码审查，输出严重问题、优化建议和正面反馈。
---

# /review

当用户调用 `/review` 时：

1. 获取审查目标：
   - 如果用户指定了文件，读取文件内容
   - 否则读取当前 git diff（已暂存或未暂存）
2. 按照 `skills/development/code-review` 的审查清单执行分析
3. 输出结构化审查报告：
   - 严重问题（阻塞）：必须修复
   - 建议优化（非阻塞）：可后续处理
   - 正面反馈：肯定代码中的亮点

## 快捷模式
- `/review --security`：仅执行安全检查
- `/review --perf`：仅执行性能分析
- `/review --style`：仅检查代码风格和命名
