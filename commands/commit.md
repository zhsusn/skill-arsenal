---
name: /commit
description: 根据当前代码变更生成符合 Conventional Commits 规范的提交信息，并执行提交前自检。
---

# /commit

当用户调用 `/commit` 时：

1. 读取当前工作区的变更（git diff --cached 或 git diff）
2. 分析变更内容，判断 type（feat/fix/docs/style/refactor/perf/test/chore）
3. 生成 50 字符以内的提交标题
4. 如有需要，补充 body 说明变更动机
5. 执行提交前自检清单（是否有测试、是否含敏感信息等）
6. 输出完整的 commit message，询问用户是否确认提交

## 自检清单
- [ ] 变更是否已添加到暂存区（git add）
- [ ] 是否包含敏感信息（API Key、密码）
- [ ] 测试是否通过
- [ ] 提交粒度是否合理（原子性）
