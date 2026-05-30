---
name: project-size-estimate
description: 当用户提到'估算项目规模'、'size-estimate'、'工作量评估'、'项目多大'、'开发周期预估'或需要量化项目复杂度时触发。基于模块、接口、页面、复杂度与风险五维度输出乐观/预期/保守三档得分与流程裁剪建议。
---

# Project Size Estimate

## 适用场景
- 项目启动前快速规模预判
- PRD 导入后首次量化评估
- 敏捷迭代前判断应采用何种流程模板
- 用户主动提供需求文本，要求估算工作量或开发周期

## 输入规范
优先从用户输入中提取以下字段；缺失时由解析引擎推断。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| requirement_text | string | 是 | 自然语言需求描述（PRD 摘要或原始描述） |
| known_module_count | int | 否 | 已知模块数 |
| known_api_count | int | 否 | 已知接口数 |
| known_page_count | int | 否 | 已知页面数 |
| tech_complexity | int (1-5) | 否 | 技术复杂度 |
| risk_level | int (1-5) | 否 | 风险等级 |
| project_type | enum | 否 | web / app / ai / data / infra，用于类比库匹配 |
| historical_velocity | float | 否 | 团队历史速率（故事点/人天），用于校准建议 |

## 解析引擎（推断规则）
当字段缺失时，基于 `requirement_text` 进行模式匹配与类比推断。

### 维度推断
| 维度 | 关键词/模式 | 推断规则 |
|------|-------------|----------|
| 模块数 | 用户系统、订单、支付、权限、内容管理、商品、库存、消息、营销 | 1 业务域 ≈ 1 模块；出现"等"上浮 20%；出现"平台/中台"默认 +2 |
| 接口数 | 对接、调用、API、同步、回调、推送、Webhook、RPC、OpenAPI | 2 模块交互 ≈ 3-5 接口；涉及开放平台/外部系统 ×2；纯内部后台 ×1 |
| 页面数 | 后台、管理端、H5、小程序、大屏、报表、配置页、列表页 | 每模块 1-3 页；含报表/大屏 +2；含复杂表单流程 +1 |
| 技术复杂度 | 微服务、高并发、AI、分布式、实时计算、区块链、联邦学习 | 1 无 / 2 低 / 3 中 / 4 高 / 5 极高；多关键词取最高 |
| 风险等级 | 支付、资金、隐私、医疗、监管、合规、审计、安全等级保护 | 1 无 / 2 低 / 3 中 / 4 高 / 5 极高；涉及资金流转默认 ≥3 |

### 类比库（文本极模糊时 fallback）
按 `project_type` 匹配基准值：
- web: { module: 4, api: 8, page: 6, complexity: 2, risk: 1 }
- app: { module: 5, api: 10, page: 10, complexity: 3, risk: 2 }
- ai: { module: 3, api: 6, page: 4, complexity: 4, risk: 3 }
- data: { module: 3, api: 12, page: 5, complexity: 3, risk: 2 }
- infra: { module: 2, api: 15, page: 3, complexity: 4, risk: 3 }

## 计算引擎
### 维度换算
| 维度 | 换算公式 | 权重 |
|------|----------|------|
| 模块数 | 原始值 × 1.0 | 30% |
| 接口数 | 原始值 × 0.8 | 20% |
| 页面数 | 原始值 × 0.4 | 15% |
| 技术复杂度 | 原始值 × 2.5 | 20% |
| 风险等级 | 原始值 × 1.5 | 15% |

### 三档得分
```
基础分 = (模块数 × 1.0) + (接口数 × 0.8) + (页面数 × 0.4) + (技术复杂度 × 2.5) + (风险等级 × 1.5)
乐观得分 = ROUND(基础分 × 0.72)
预期得分 = ROUND(基础分)
保守得分 = ROUND(基础分 × 1.25)
```

### 规模分级（以保守得分定级）
| 规模 | 保守得分 | 典型描述 | 流程模板 | 里程碑组合 |
|------|----------|----------|----------|------------|
| XS | ≤ 10 | 改按钮、调超时、文案替换 | 极简 | Clarify(合并)→Build→Release |
| S | 11~22 | 内部小工具、单模块后台、报表配置 | 快速 | Clarify→Align(合并)→Build→Verify→Release |
| M | 23~40 | 订单模块、权限 CMS、标准 SaaS 功能 | 标准 | Clarify→Align→Contract→Build→Verify→Release |
| L | 41~70 | 核心链路重构、AI 平台多子系统 | 完整 | 标准 + 预研阶段 |
| XL | > 70 | 新一代核心系统、中台改造 | 专项 | 强制拆分为多个 M 级子项目 |

> 边界跨级规则：保守得分跨级时，以保守得分所在区间定级。

## 置信度判定
### 单维度置信度
- **High**：用户提供已知指标，或文本中有明确数量词（如"3 个系统"）
- **Medium**：由关键词推断，或已知指标与推断值偏差 ≤ 30%
- **Low**：纯类比推断，或已知指标与推断值偏差 > 30%，或文本极模糊

### 总置信度（短板效应）
```
总置信度 = MIN(各维度置信度)
```
- 任一维度为 Low → 总置信度 Low
- 无 Low 且存在 Medium → 总置信度 Medium
- 全 High → 总置信度 High

## 输出格式
输出必须为结构化 JSON，示例如下：

```json
{
  "skill": "project-size-estimate",
  "version": "1.0",
  "project_id": "proj_xxx",
  "timestamp": "2026-05-30T19:10:00Z",
  "optimistic_score": 20,
  "expected_score": 28,
  "conservative_score": 35,
  "level": "M",
  "confidence": "Medium",
  "dimension_details": [
    {"name": "模块数", "value": 5, "inferred": false, "conf": "High", "weight": "30%", "score": 5.0},
    {"name": "接口数", "value": 12, "inferred": false, "conf": "Medium", "weight": "20%", "score": 9.6},
    {"name": "页面数", "value": 8, "inferred": false, "conf": "Medium", "weight": "15%", "score": 3.2},
    {"name": "技术复杂度", "value": 3, "inferred": true, "conf": "High", "weight": "20%", "score": 7.5},
    {"name": "风险等级", "value": 2, "inferred": true, "conf": "High", "weight": "15%", "score": 3.0}
  ],
  "suggestion": "建议 M 级。若 Clarify 后模块数减少 30%（降至 3-4 个），可降级为 S 级并采用快速流程模板。",
  "process_template": "标准",
  "milestones": ["Clarify", "Align", "Contract", "Build", "Verify", "Release"],
  "calibration": {
    "needed": false,
    "reason": "首次估算，无历史数据"
  }
}
```

## 执行步骤
1. **收集输入**：提取用户提供的 `requirement_text` 及已知指标；缺失字段标记为待推断。
2. **维度推断**：按"解析引擎"规则补全缺失值；若文本极模糊，使用类比库 fallback。
3. **偏差校验**：若已知指标与推断值偏差 > 30%，将对应维度置信度降为 Medium/Low。
4. **计算得分**：执行五维度换算，输出乐观/预期/保守三档得分。
5. **规模定级**：以保守得分查分级矩阵，确定 XS/S/M/L/XL 级别。
6. **流程裁剪**：根据级别推荐流程模板与里程碑组合。
7. **生成建议**：给出"精修后可降级"的具体条件（如减少模块数、降低复杂度）。
8. **输出 JSON**：严格按"输出格式"返回结构化结果，拒绝自然语言模糊表述。

## Gotchas
- **不过度承诺**：本 Skill 仅输出规模得分与流程建议，不直接输出人天或排期；人天换算需结合团队速率与资源投入另行计算。
- **边界跨级**：保守得分若恰落在分级边界（如 22 与 23 之间），按保守原则归入更高一级（如 23 归为 M）。
- **降级陷阱**：输出中必须包含 `suggestion` 字段，明确说明"当前级别可通过哪些条件降级"，防止用户误判为不可变更。
- **类比库局限**：类比库仅用于文本极模糊场景，若用户已提供部分已知指标，不得用类比库覆盖已知值。
- **校准触发**：项目完结后应对比实际规模与估算规模；若偏差 > 30%，需修正系数并记录 calibration_log，下次同类项目优先使用修正后系数。
- **不硬编码团队数据**：`historical_velocity` 等团队敏感数据通过输入传入，禁止在 Skill 中写死任何团队或公司私有基准。
