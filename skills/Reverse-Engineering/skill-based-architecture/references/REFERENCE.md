# Reference Materials

深度参考资料索引。按主题拆分，按需加载。

## 结构与设计

| 文件 | 内容 | 何时阅读 |
|------|------|----------|
| [layout.md](layout.md) | 推荐目录布局、`SKILL.md` 模板、项目边界、多 Skill 共存、Prompt/Context/Harness 定位 | 新建 Skill 或决定内容归属时 |
| [skill-composition.md](skill-composition.md) | Skill 组合模式、多 Skill 路由策略、命名空间隔离 | 设计多 Skill 协作方案时 |
| [multi-skill-routing.md](multi-skill-routing.md) | 多 Skill 环境下的路由与激活优先级 | 调试 Skill 冲突或激活失败时 |

## 工具集成

| 文件 | 内容 | 何时阅读 |
|------|------|----------|
| [thin-shells.md](thin-shells.md) | `.cursor` 注册入口、通用薄壳体、各工具薄壳模板、兼容性矩阵、SessionStart Hook | 将 Skill 接入新工具或调试静默激活时 |

## 流程与协议

| 文件 | 内容 | 何时阅读 |
|------|------|----------|
| [protocols.md](protocols.md) | 元工作流模板、任务闭环协议、记录阈值（2/3 规则）、泛化规则、激活验证 | 设计自我演进机制或诊断规则未触发时 |
| [conventions.md](conventions.md) | 按项目类型的规则文件集、决策指南、反模式、故障排查、文件大小指南、命名规范 | 迁移决策、容量诊断或 Skill 损坏排查时 |

## 迁移与案例

| 文件 | 内容 | 何时阅读 |
|------|------|----------|
| [migration.md](migration.md) | 将现有文档迁移到 Skill 架构的模式：超大 SKILL.md、分散规则、薄壳重写、拆分/合并标准 | 开始迁移或面对庞大/碎片化的规则集时 |
| [project-types.md](project-types.md) | Java/Spring Boot、Python CLI/数据、多 Skill 全栈、以及"小到单文件即可"的典型案例 | 从零开始选型或判断完整架构是否过度时 |
| [self-evolution.md](self-evolution.md) | 行动后复盘、从错误中学习、记录阈值、激活优于存储、描述触发失败、压力下的任务闭环协议 | 长期维护 Skill 或诊断"写了但从未触发"时 |
| [behavior-failures.md](behavior-failures.md) | 行为层 ❌/✅ 场景——Agent 合理化表述的前后对比（AAR 跳过、被动摘要描述、同会话路由跳过） | Skill 纸面正确但实践中仍漂移时 |
