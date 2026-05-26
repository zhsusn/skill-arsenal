---
name: code-review-pipeline
description: 当用户提到'启动审查'、'code review'、'审查流程'、'review pipeline'、'开始审查'或代码完成、功能实现、合并前时触发。自动化代码审查编排器，融合四阶段流程与五轴质量评估，管理从代码完成到审查通过的全流程状态机。
---

# Code Review Pipeline 编排器

> 自动化代码审查编排器，融合四阶段流程与五轴质量评估。
> 管理从代码完成到审查通过的全流程状态机，包含变更大小门禁、多轮角色切换、进度追踪。
> 适配 Kimi Code 无 subagent 环境，采用会话内角色切换 + 状态机驱动。

## 状态定义与流转

| 状态 | 说明 | 触发条件 | 下一状态 |
|------|------|---------|---------|
| IDLE | 待机 | 初始 / 审查通过归档后 | SIZING |
| SIZING | 变更大小评估 | 自动/半自动/手动触发 | REQUESTING（≤300行）或 SPLITTING（>300行） |
| SPLITTING | 拆分指导 | 变更过大 | REQUESTING（拆分后） |
| REQUESTING | 准备审查材料 | 材料准备完毕 | REVIEWING_P1 |
| REVIEWING_P1 | Phase 1: 上下文收集 | 材料就绪 | REVIEWING_P2 |
| REVIEWING_P2 | Phase 2: 高层级审查 | P1 完成 | REVIEWING_P3 |
| REVIEWING_P3 | Phase 3: 逐行分析 | P2 完成 | SUMMARY |
| SUMMARY | Phase 4: 总结决策 | P3 完成 | RECEIVING（发现issue）或 DONE（零问题） |
| RECEIVING | 处理反馈 | 收到《审查意见书》 | FIXING |
| FIXING | 执行修复 | 生成《修复计划》 | VERIFYING |
| VERIFYING | 复查验证 | 修复完成 | DONE（通过）或 RECEIVING（仍有问题） |
| DONE | 审查通过 | 无遗留 blocking/important | IDLE |

## 变更大小门禁

```
~100  lines changed → Good. 直接进入审查。
~300  lines changed → Acceptable if single logical change. 进入审查。
~1000 lines changed → Too large. 强制进入 SPLITTING。
```

**拆分策略指导（当用户需要拆分时）：**

| 策略 | 适用场景 | 操作方式 |
|------|---------|---------|
| Stack | 顺序依赖 | 先提交基础变更，后续基于它 |
| By file group | 跨领域变更 | 按 reviewer expertise 分组拆分 |
| Horizontal | 分层架构 | 先提共享代码/接口，再提消费者 |
| Vertical | 功能开发 | 按小功能切片（全栈小闭环） |

**纪律：** 重构与功能开发必须分开提交。小清理（变量重命名）可酌情包含。

## 自动化触发机制

### 自动触发（零干扰）
当检测到以下信号，记录到 `openspec/changes/{变更名}/code-review/review-buffer.json`：
- 文件保存且含 `# @review` 或 `// @review` 标记
- 用户消息含"完成了"、"Task done"、"功能实现完毕"
- 连续编码 30 分钟且存在未提交 git diff

### 半自动触发（批量确认）
当满足模块完成或 30 分钟间隔：
> 【模块名】已完成，积累 N 条待审查变更：
> - 文件：src/components/UserForm.vue（+80/-5）
> - 预估复杂度：中等 | 变更大小：145 行（符合门禁）
> 启动审查流程？ [确认 / 修改范围 / 跳过]

### 手动触发
- `/review` — 审查最近 1 个 commit
- `/review HEAD~2..HEAD` — 指定范围
- `/review src/api/user.py` — 指定文件
- `启动审查` / `code review` — 完整 pipeline

## 角色编排流程

### Step 1: REQUESTING（提审者）
调用 `requesting-code-review` Skill：
1. 提取 git diff 范围与统计信息
2. 执行变更大小评估（SIZING）
3. 生成《审查请求书》（YAML）
4. 状态置为 REVIEWING_P1

### Step 2: REVIEWING（审查者）— 四阶段执行
调用 `code-reviewer` Skill，分三轮角色切换：

**Round A — Phase 1+2（上下文 + 高层级）：**
> 角色指令：你是 Staff Engineer，负责评估架构设计与性能影响。不看实现细节，只看设计选择。

**Round B — Phase 3（逐行分析）：**
> 角色指令：你是 Security Engineer + QA Lead，负责逐行检查逻辑正确性、安全漏洞、边界情况。

**Round C — Phase 4（总结）：**
> 角色指令：你是 Tech Lead，汇总所有发现，按严重性定级，给出合并建议。

### Step 3: RECEIVING（被审者）
调用 `receiving-code-review` Skill：
1. 读取《审查意见书》
2. 逐条执行 VERIFY → EVALUATE → RESPOND
3. 生成《修复计划》
4. 状态置为 FIXING

### Step 4: VERIFYING（复查）
修复完成后，再次调用 `code-reviewer` Skill：
- 仅审查修改过的文件（缩小范围）
- 验证修复到位 + 无回归
- 输出《复查报告》

### Step 5: DONE
- 更新 `openspec/changes/{变更名}/code-review/decisions.md`
- 回写 `progress-tracker`：`phases.code_review.status = passed`
- 清空 `openspec/changes/{变更名}/code-review/review-state.json`
- 状态置为 IDLE

## 审查速度规范

- **响应时限**：1 个工作日内必须响应（上限，非目标）
- **理想节奏**：收到请求后尽快响应，典型变更应在一天内完成多轮 review
- **优先策略**：优先快速给出个体反馈，而非追求一次性快速批准
- **大变更处理**：要求拆分，不硬审巨大 changeset

## 输出物规范

### 审查请求书 (review-request.yaml)
```yaml
# 路径：openspec/changes/{变更名}/code-review/review-request.yaml
review_request:
  task_id: "task-002"
  timestamp: "2026-05-24T06:00:00+08:00"
  description: "添加用户认证中间件"
  requirements_source: "docs/prd/auth.md"
  base_sha: "a1b2c3d"
  head_sha: "e4f5g6h"
  files_changed:
    - path: "src/middleware/auth.py"
      change_type: "新增"
      lines_added: 45
      lines_deleted: 0
      language: "python"
  total_lines_changed: 45
  sizing_assessment: "Good"
  scope: "新增 JWT 验证逻辑，影响所有受保护路由"
  test_status: "已本地测试，未写单元测试"
  known_issues: "SECRET_KEY 临时硬编码，待配置化"
```

### 审查意见书 (review-report.yaml)
```yaml
# 路径：openspec/changes/{变更名}/code-review/review-report.yaml
review_report:
  task_id: "task-002"
  overall: "Request Changes"
  summary: "JWT 逻辑正确，但密钥硬编码和缺少唯一索引需修复"
  phases:
    phase1_context: "理解无误：为 FastAPI 添加 JWT 认证，保护 admin 路由"
    phase2_high_level: "架构合理（中间件模式），但性能上缺少缓存策略"
    phase3_line_by_line: "发现 3 个实质性问题"
  issues:
    blocking:
      - id: B1
        phase: "phase3"
        axis: "security"
        file: "src/middleware/auth.py"
        line: 45
        desc: "SECRET_KEY 硬编码在源码中"
        suggest: "使用 os.environ.get('JWT_SECRET')，并在 .env.example 中添加示例值"
        rationale: "硬编码密钥一旦提交到 git，历史记录中永久存在"
    important:
      - id: I1
        phase: "phase3"
        axis: "correctness"
        file: "src/models/user.py"
        line: 12
        desc: "User.email 缺少唯一索引"
        suggest: "添加 db.Column(db.String(120), unique=True, index=True)"
    nit:
      - id: N1
        phase: "phase3"
        axis: "readability"
        file: "src/middleware/auth.py"
        line: 23
        desc: "函数名 validateToken 不符合 snake_case 规范"
        suggest: "重命名为 validate_token"
    suggestion:
      - id: S1
        phase: "phase2"
        axis: "performance"
        desc: "JWT 验证每次请求都解析 token，建议增加 Redis 缓存已验证 token"
    praise:
      - id: P1
        phase: "phase3"
        axis: "correctness"
        desc: "错误处理完整，区分了 token 过期和签名无效两种情况"
  strengths:
    - "JWT 验证逻辑清晰，错误处理完整"
    - "使用依赖注入获取配置，便于测试 mock"
  assessment: "建议：修复 B1 和 I1 后合并，N1 和 S1 可在后续迭代处理"
  dead_code_identified:
    - "formatLegacyDate() in src/utils/date.ts — 被新实现替代"
  new_dependencies:
    - name: "pyjwt"
      version: "2.8.0"
      license: "MIT"
      last_commit: "2024-01"
      audit_clean: true
```

### 修复计划 (fix-plan.yaml)
```yaml
# 路径：openspec/changes/{变更名}/code-review/fix-plan.yaml
fix_plan:
  task_id: "task-002"
  total_issues: 5
  blocking: 1
  important: 1
  nit: 1
  suggestion: 1
  items:
    - id: B1
      severity: blocking
      action: "fix"
      approach: "使用 os.environ.get('JWT_SECRET')，添加 .env.example，更新 docker-compose.yml"
      files: ["src/middleware/auth.py", ".env.example", "docker-compose.yml"]
      test_required: true
      estimated_time: "10min"
    - id: S1
      severity: suggestion
      action: "defer"
      defer_reason: "需要引入 Redis，超出本次范围"
      follow_up_task: "task-005"
  execution_order: ["B1", "I1", "N1"]
  defer_items:
    - id: S1
      reason: "需要引入 Redis，超出本次范围，已记录到 code-review/decisions.md"
```

## 进度追踪集成

**openspec/changes/{变更名}/code-review/decisions.md**
```markdown
## 审查看板

| 任务 | 模块 | 状态 | 变更大小 | 发现 | 已修复 | 待验证 | 已通过 | 归档 |
|------|------|------|---------|------|--------|--------|--------|------|
| task-003 | 分镜工作室 | REQUESTING | 120 行 | - | - | - | - | - |
| task-002 | 用户认证 | VERIFYING | 45 行 | 5 | 3 | 0 | - | - |
| task-001 | 角色工厂 | DONE | 200 行 | 2 | 2 | 0 | ✅ | 2026-05-22 |

## 阻塞项
- task-002: B1 密钥硬编码（修复中，预计 10min）

## 下一步
1. 完成 task-002 复查
2. 启动 task-003 Phase 1
```

**openspec/changes/{变更名}/code-review/decisions.md**
```markdown
## 2026-05-24 task-002 审查决策
- B1 密钥管理：接受 reviewer 建议，采用环境变量方案。理由：硬编码密钥在 git 历史中永久存在。
- I1 唯一索引：接受建议。额外检查：现有数据无重复 email。
- S1 Redis 缓存：延期处理。理由：本次仅做基础认证，缓存优化在 task-005 性能专项中处理。
- N1 命名规范：接受建议。
- 死代码清理：确认移除 formatLegacyDate()，无剩余引用。
- 复查结果：2026-05-24 07:15 复查通过，无回归。
```

## 使用方式

### 完整流程
```
用户：完成了用户认证模块
AI：【SIZING】45 行 → Good
    【REQUESTING】生成审查请求书
    【REVIEWING_P1】上下文收集
    【REVIEWING_P2】架构 + 性能评估
    【REVIEWING_P3】逐行分析（加载 python.md + security-review-guide.md）
    【SUMMARY】输出审查意见书（5 issues）
    【RECEIVING】生成修复计划
    【FIXING】执行修复
    【VERIFYING】复查 → 通过
    【DONE】更新看板
```

### 单步调试
```
用户：进入 REVIEWING_P3，只审查 src/middleware/auth.py 的安全轴
AI：加载 security-review-guide.md + python.md，执行 Phase 3 安全专项审查
```

### 跳过审查（紧急通道）
```
用户：跳过审查，hotfix 紧急修复线上崩溃
AI：记录到 openspec/changes/{变更名}/code-review/decisions.md：【跳过】task-xxx 因 hotfix 跳过审查，责任人：user，事后补审截止：24h
```

## Gotchas

- **无 subagent 环境**：通过同一会话内角色轮替模拟多模型审查，每轮之间必须执行角色重置。
- **变更大小门禁是强制性的**：>300 行必须给出拆分建议，不接受"这次例外"。
- **审查者严格隔离**：不要携带实现者视角进入审查阶段，角色切换时必须声明"你现在不是代码作者"。
- **输出物不是可选的**：即使零问题通过，也必须输出审查意见书（praise 和 strengths 不能省略）。
- **阻塞性问题必须清零**：DONE 状态的前置条件是所有 blocking 和 important 已修复或明确延期。
- **进度追踪双向写入**：pipeline 负责更新 openspec/changes/{变更名}/code-review/decisions.md 并回写 progress-tracker，skill 不负责。
- **复查范围缩小**：VERIFYING 阶段只审查修改过的文件，不重新全量审查。
- **热修复通道**：允许跳过审查，但必须在 decisions.md 留下审计痕迹和补审截止时间。
