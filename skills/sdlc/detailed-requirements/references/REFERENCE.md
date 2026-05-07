# Detailed Requirements 参考资料索引

> 本目录为 `detailed-requirements` Skill 的深度参考资料，按需加载。

---

## 文件清单

| 文件 | 用途 | 加载时机 |
|------|------|----------|
| `SINGLE_MODULE_GUIDE.md` | 单模块深度模式完整指南（何时使用、执行步骤、输出格式） | 当模块数 ≤3 或需要穷尽式人工协作时 |
| `module-interview-guide.md` | 深度访谈提问技巧和边界探测方法 | 执行单模块深度模式 Step 3 时 |
| `feature-template.md` | 单文档 PRD-00X 完整模板（11 章节） | 执行单模块深度模式输出时 |
| `acceptance-criteria-patterns.md` | Given-When-Then 规范与模糊语言检测清单 | 编写验收标准时 |
| `business-logic-spec.md` | 业务逻辑四要素（输入/处理/输出/副作用）编写规范 | 编写 logic.md 或 PRD-00X 第 4 章时 |

---

## 模式选择速查

| 项目特征 | 推荐模式 | 参考文件 |
|----------|----------|----------|
| 模块数 ≥4，需要标准化批量输出 | **默认模式**（4 文件目录） | 无需加载参考，直接按 SKILL.md 执行 |
| 模块数 ≤3，或仅 1 个核心模块需深挖 | **单模块深度模式** | `SINGLE_MODULE_GUIDE.md` + `module-interview-guide.md` |
| 需要输出传统 PRD-00X 单文档 | **单模块深度模式** | `feature-template.md` |
| 验收标准质量不达标 | 两种模式均适用 | `acceptance-criteria-patterns.md` |
| 业务逻辑描述有歧义 | 两种模式均适用 | `business-logic-spec.md` |
