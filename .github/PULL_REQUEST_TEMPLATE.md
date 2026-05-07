## 关联 Issue

<!-- 如有相关 Issue，请使用 Fixes #123 或 Closes #456 自动关闭 -->

Fixes #

## 变更类型

<!-- 请在符合的选项前打 [x] -->

- [ ] `feat` — 新增功能（Skill、脚本、能力）
- [ ] `fix` — Bug 修复
- [ ] `docs` — 文档更新
- [ ] `style` — 代码格式调整（不影响功能）
- [ ] `refactor` — 代码重构
- [ ] `chore` — 构建/工具链改动

## 变更描述

<!-- 清晰描述本次 PR 做了什么、为什么做 -->

## 测试说明

<!-- 描述你如何验证这些变更 -->

- [ ] 本地运行 `python3 scripts/validate.py` 通过
- [ ] 如涉及 Skill 修改，已重新生成 `.cursor/rules/`：`python3 scripts/convert.py --tool cursor --all --output .cursor/rules`
- [ ] `index.json` 已同步更新
- [ ] 文档已同步更新（README.md / AGENTS.md / docs/）

## 自查清单

<!-- 提交前请确认 -->

- [ ] 我的代码遵循了项目的代码风格
- [ ] 我已阅读并遵守 [CONTRIBUTING.md](../CONTRIBUTING.md)
- [ ] 我对本次变更做了充分的本地验证
- [ ] 本次变更不引入破坏性修改（如有请在描述中说明）
