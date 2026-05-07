# 概要设计边界红线

本文档定义 `high-level-design` Skill 的严格边界：什么必须留在概要设计层，什么必须留给详细设计层。

## 核心判定原则

> **变更影响 ≥2 个模块 → 概要设计**
> **变更影响 ≤1 个模块 → 详细设计**

---

## must_be_here（必须在概要设计层定义）

以下内容影响范围跨模块或改变系统整体结构，必须在概要设计阶段锁定：

1. **新增/删除微服务或模块**
   - 理由：影响团队分工、接口契约、部署拓扑
   
2. **更换技术栈**
   - 语言、框架、数据库类型、AI 模型基座
   - 理由：影响招聘、学习成本、长期维护
   
3. **调整核心数据流**
   - 如同步改异步队列、引入事件总线
   - 理由：影响一致性模型、故障模式、监控策略
   
4. **修改全局状态机**
   - 状态数量变更、状态流转路径新增/删除
   - 理由：影响多个模块的业务逻辑和数据库设计
   
5. **变更认证/授权方案**
   - 如从 Session 改 JWT、从 RBAC 改 ABAC
   - 理由：影响所有服务的安全模型
   
6. **数据库选型变更**
   - 如从 MySQL 改 PostgreSQL、引入向量数据库
   - 理由：影响数据迁移、运维、成本
   
7. **引入新的中间件/基础设施**
   - 如新增消息队列、搜索引擎、对象存储
   - 理由：影响部署架构、运维复杂度、成本

---

## must_not_be_here（禁止出现在概要设计层）

以下内容是单模块内部实现细节，必须留给 `detailed-design`：

1. **接口字段级校验规则**
   - 如 `varchar(64)`、`@NotNull`、`@Size(min=1, max=100)`
   - 归宿：`detailed-design/api-spec.md`
   
2. **物理表字段/索引/DDL**
   - 如字段类型、长度、索引名称、分区键
   - 归宿：`detailed-design/db-schema.md`
   
3. **算法流程和参数调优**
   - 如 Prompt 模板、温度参数、采样策略、模型微调参数
   - 归宿：`detailed-design/algorithm.md`
   
4. **单接口异常码和补偿事务**
   - 如 `ERR_001`、`TCC` 流程、`Saga` 步骤
   - 归宿：`detailed-design/exception-handling.md`
   
5. **类图和函数签名**
   - 如 `class UserService { createUser(...) }`
   - 归宿：`detailed-design/design.md`
   
6. **模块内部调用链**
   - 如 `Controller → Service → Repository → Mapper`
   - 归宿：`detailed-design/design.md`
   
7. **单测用例和 Mock 策略**
   - 如 `test_create_user_success`、`@patch('redis.Redis')`
   - 归宿：`detailed-design/test-plan.md`
   
8. **缓存 Key 设计和过期策略**
   - 如 `user:profile:{user_id}`、TTL=3600
   - 归宿：`detailed-design/design.md`
   
9. **具体配置文件内容**
   - 如 `application.yml` 中的连接池参数
   - 归宿：`detailed-design/design.md`

---

## 边界检查清单（生成时自测）

每生成一个章节后，扫描以下内容：

- [ ] 是否出现 SQL/DDL（CREATE TABLE、ALTER、INDEX）
- [ ] 是否出现字段类型声明（varchar、int、JSONB 等）
- [ ] 是否出现编程语言关键字（class、def、function、interface、type）
- [ ] 是否出现框架注解（@RequestBody、@Entity、@Component）
- [ ] 是否出现具体异常码（ERR_XXX、CODE_XXX）
- [ ] 是否出现 Prompt 模板或算法参数
- [ ] 是否出现模块内部三层调用链（Controller/Service/DAO）
- [ ] 是否出现测试断言（assert、expect、mock）

若命中 ≥1 项，标记为**内容下钻**，必须提升抽象层级后重新输出。

---

## 设计锁定原则（阶段门控）

```yaml
phase_transitions:
  - from: high-level-design
    to: detailed-design
    gate: "概要设计架构评审通过（用户签字确认）"
    red_flags:
      - "禁止在概要设计评审通过前写详细设计"
      - "禁止概要设计未定就进入编码实现"
      - "禁止绕过 self-check 直接进入下一阶段"
      
lock_rules:
  freeze_after_review: true
  change_requires: "架构评审会重新评审"
  forbidden_before_review:
    - detailed-design
    - task-breakdown
    - implementation
```

---

## 需求追溯规则

概要设计的每个决策必须能向上追溯：

1. **每个模块** → 必须对应 `03-functional-structure.md` 中的模块
2. **每个技术选型** → 必须在 `competitive-analysis.md` 中有结论支撑
3. **每个全局状态** → 必须能追溯到 `02-requirements-list.md` 或 `04-business-rules.md` 中的业务规则
4. **每个非功能策略** → 必须对应 `05-non-functional.md` 中的指标

追溯断裂时，标记为 WARNING 并要求补充依据。
