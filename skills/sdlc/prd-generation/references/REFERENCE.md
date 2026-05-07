# PRD-000 概要需求生成器 — 参考资料索引

本目录存放 prd-generation Skill 的深度参考资料，按渐进式披露原则按需加载。

## 文件清单

| 文件 | 用途 | 加载时机 |
|------|------|----------|
| `completeness-scoring.md` | 四层红绿灯评分算法与阻塞规则 | 每层访谈结束后 |
| `consistency-checklist.md` | 一致性校验 + 竞品对标清单 + 问题分级模板 | Layer 4 强制校验阶段 |
| `questioning-guide.md` | 三层递进式提问策略，含 JTBD 与 abeejuice 快速模式 | 各 Layer 访谈阶段 |
| `system-outline-template.md` | 五文件输出模板（01-05）与 13 章逻辑映射 | Step 5 输出阶段 |
| `jtbd-framework.md` | JTBD + 用户故事 + Component Inventory 编写指南 | Layer 1-2 需求表达阶段 |

## 开源项目融合说明

本 Skill 融合了以下开源项目的设计思想：

- **abeejuice/prd-skill**：6 题快速访谈模板、URL 审计思路、逐题确认交互模式
- **johnnychauvet/prd-skill**：JTBD 框架、原子用户故事、Component Inventory、AI Build Summary
- **cdeust/ai-prd-generator-plugin**：多文件拆分策略、原子声明分解验证、策略引擎思想
