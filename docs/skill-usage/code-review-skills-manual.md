# Code Review Skills 使用手册

> 面向开发者和 AI 助手的 code review 技能族操作手册。

---

## 一、快速开始

### 1.1 安装

本技能族已集成在 skill-arsenal 中，无需额外安装。确保你的 AI 工具已加载 `skills/sdlc/` 下的相关 skill：

```bash
# 查看可用 code review skills
ls skills/sdlc/code-review-*
ls skills/sdlc/requesting-code-review
ls skills/sdlc/receiving-code-review
ls skills/sdlc/code-reviewer
```

### 1.2 触发方式

| 触发词 | 激活的 Skill | 行为 |
|--------|------------|------|
| "启动审查" / "code review" / "review pipeline" | `code-review-pipeline` | 完整四阶段 × 五轴审查流程 |
| "审查这段代码" / "检查实现质量" / "request review" | `requesting-code-review` | 生成审查请求书并触发审查 |
| "review" / "代码走读" / "检查这段代码" | `code-reviewer` | 直接执行审查者角色 |
| "处理审查意见" / "修复 review 问题" / "复查" | `receiving-code-review` | 处理反馈并生成修复计划 |

---

## 二、完整流程演示

### 2.1 标准流程（推荐）

```
用户：完成了用户认证模块

AI：【SIZING】45 行 → Good
    【REQUESTING】生成审查请求书
    【REVIEWING_P1】上下文收集
    【REVIEWING_P2】架构 + 性能评估
    【REVIEWING_P3】逐行分析（加载 security-review-guide.md + code-quality-universal.md）
    【SUMMARY】输出审查意见书（5 issues）
    【RECEIVING】生成修复计划
    【FIXING】执行修复
    【VERIFYING】复查 → 通过
    【DONE】更新看板
```

### 2.2 分步控制

如果你想控制每一步的执行：

```
用户：进入 REVIEWING_P3，只审查 src/middleware/auth.py 的安全轴
AI：加载 security-review-guide.md，执行 Phase 3 安全专项审查

用户：生成修复计划
AI：调用 receiving-code-review，输出 fix-plan.yaml

用户：修复 B1 和 I1 后复查
AI：进入 VERIFYING，仅审查修改过的文件
```

### 2.3 跳过审查（紧急通道）

```
用户：跳过审查，hotfix 紧急修复线上崩溃
AI：记录到 docs/decisions.md：
    【跳过】task-xxx 因 hotfix 跳过审查，责任人：user，事后补审截止：24h
```

---

## 三、各 Skill 详细使用说明

### 3.1 code-review-pipeline（编排器）

**用途：** 管理从代码完成到审查通过的完整状态机。

**何时使用：**
- 任务完成后自动触发
- 用户说"启动审查流程"
- 需要追踪多轮审查进度

**关键输出：**
- `review-request.yaml` — 审查请求书
- `review-report.yaml` — 审查意见书
- `fix-plan.yaml` — 修复计划
- `docs/progress.md` — 审查看板更新
- `docs/decisions.md` — 决策日志追加

**自定义：**
- 修改状态机流转规则：编辑 SKILL.md 中"状态定义与流转"表格
- 调整变更大小门禁：修改 SIZING 阶段的阈值（默认 100/300/1000）

### 3.2 requesting-code-review（提审者）

**用途：** 准备审查材料，生成审查请求书。

**何时使用：**
- 代码已完成，需要正式提交审查
- 需要评估变更大小
- 需要检测死代码和依赖变更

**手动操作示例：**

```bash
# 1. 获取变更统计
BASE_SHA=$(git rev-parse HEAD~1)
HEAD_SHA=$(git rev-parse HEAD)
git diff --stat $BASE_SHA..$HEAD_SHA

# 2. 检查死代码
grep -r "old_function_name" src/ --include="*.py" | grep -v "new_file.py"

# 3. 检查依赖变更
git diff requirements.txt package.json
```

**输出模板：**
```yaml
review_request:
  task_id: "task-002"
  timestamp: "2026-05-24T06:00:00+08:00"
  description: "添加用户认证中间件"
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
  new_dependencies: []
```

### 3.3 code-reviewer（审查者）

**用途：** 执行结构化代码审查。

**何时使用：**
- 收到审查请求书后
- 用户直接要求审查某段代码
- 需要专项审查（安全/性能/架构）

**四阶段执行：**

| 阶段 | 输入 | 输出 | 角色 |
|------|------|------|------|
| Phase 1 | 审查请求书 | 上下文理解摘要 | — |
| Phase 2 | 代码 + 架构/性能指南 | blocking/important/suggestion/praise | Staff Engineer |
| Phase 3 | 代码 + 安全/质量指南 | 逐文件 issues | Security Engineer + QA Lead |
| Phase 4 | 所有发现汇总 | 审查意见书 + 合并决策 | Tech Lead |

**专项审查指令：**

```
"只审查安全轴" → 加载 security-review-guide.md，跳过其他轴
"只审查性能" → 加载 performance-review-guide.md，聚焦 Phase 2
"架构审查" → 加载 architecture-review-guide.md，执行 Phase 2
```

**输出格式：**
必须严格输出 YAML，禁止插入解释性文字。

```yaml
review_report:
  task_id: "task-002"
  overall: "Request Changes"
  summary: "JWT 逻辑正确，但密钥硬编码需修复"
  issues:
    blocking:
      - id: B1
        phase: "phase3"
        axis: "security"
        file: "src/middleware/auth.py"
        line: 45
        desc: "SECRET_KEY 硬编码在源码中"
        suggest: "使用 os.environ.get('JWT_SECRET')"
        rationale: "硬编码密钥在 git 历史中永久存在"
  strengths:
    - "错误处理完整，区分了 token 过期和签名无效"
  assessment: "建议：修复 B1 后合并"
```

### 3.4 receiving-code-review（被审者）

**用途：** 处理审查反馈，生成修复计划。

**何时使用：**
- 收到审查意见书后
- 需要按优先级修复问题
- 修复完成后需要复查

**处理流程：**

1. **分类与澄清**
   - 逐条理解 issue
   - 有任何不理解立即 STOP 并 ASK
   - 不要部分修复

2. **生成修复计划**
   ```yaml
   fix_plan:
     task_id: "task-002"
     items:
       - id: B1
         severity: blocking
         action: "fix"
         approach: "使用 os.environ.get('JWT_SECRET')"
         files: ["src/middleware/auth.py"]
         test_required: true
         estimated_time: "10min"
     execution_order: ["B1", "I1", "N1"]
   ```

3. **执行修复**
   - 一次只改一项
   - 改完测完再改下一项
   - 引入新问题立即停止，重新审查

4. **状态回写**
   - 修复完成后自动进入 VERIFYING
   - 再次调用 code-reviewer 复查

**禁止行为：**
- "You're absolutely right!"（表演式认同）
- "I'll fix it later"（延期清理）
- 未完全理解就实施修复

---

## 四、参考指南使用说明

### 4.1 通用参考指南

| 指南 | 路径 | 触发条件 | 内容 |
|------|------|---------|------|
| 安全审查 | `code-reviewer/reference/security-review-guide.md` | 涉及认证/支付/上传/隐私 | 输入验证、授权、注入防护、XSS、敏感数据 |
| 性能审查 | `code-reviewer/reference/performance-review-guide.md` | 变更>200行或涉及DB/缓存 | N+1查询、复杂度、内存、并发、前端性能 |
| 架构审查 | `code-reviewer/reference/architecture-review-guide.md` | 新增模块/接口变更/重构 | SOLID、耦合、分层、API设计、扩展性 |
| 通用质量 | `code-reviewer/reference/code-quality-universal.md` | 默认加载 | 复用审计、参数膨胀、TOCTOU、魔法数字 |

### 4.2 按需加载示例

```
审查范围：src/api/user.py, src/models/user.py（Python）
加载指南：
  1. code-quality-universal.md（默认）
  2. security-review-guide.md（涉及用户数据）
  3. performance-review-guide.md（涉及数据库）
  4. python.md（预留，待实现）
```

---

## 五、进度追踪

### 5.1 docs/progress.md

pipeline 自动维护的审查看板：

```markdown
## 审查看板

| 任务 | 模块 | 状态 | 变更大小 | 发现 | 已修复 | 待验证 | 已通过 | 归档 |
|------|------|------|---------|------|--------|--------|--------|------|
| task-002 | 用户认证 | VERIFYING | 45 行 | 5 | 3 | 0 | - | - |
| task-001 | 角色工厂 | DONE | 200 行 | 2 | 2 | 0 | ✅ | 2026-05-22 |

## 阻塞项
- task-002: B1 密钥硬编码（修复中，预计 10min）

## 下一步
1. 完成 task-002 复查
2. 启动 task-003 Phase 1
```

### 5.2 docs/decisions.md

审查决策的审计日志：

```markdown
## 2026-05-24 task-002 审查决策
- B1 密钥管理：接受 reviewer 建议，采用环境变量方案。
- S1 Redis 缓存：延期至 task-005。
- 复查结果：2026-05-24 07:15 复查通过，无回归。
```

---

## 六、常见问题

### Q1: 没有 subagent 怎么保证审查客观性？

通过**三轮角色轮替**：
1. Round A: correctness + architecture（Staff Engineer）
2. Round B: security + performance（Security Engineer）
3. Round C: readability + summary（Tech Lead）

每轮之间执行**角色重置声明**，模拟独立 reviewer。

### Q2: 变更超过 300 行怎么办？

强制进入 SPLITTING 状态，选择拆分策略：
- **Stack**：顺序依赖，先基础后实现
- **By file group**：按领域分组
- **Horizontal**：分层，先接口后消费者
- **Vertical**：按功能切片

### Q3: 可以跳过审查吗？

可以，但**必须记录**：
```markdown
## 2026-05-24 task-xxx 审查决策
- 【跳过】因 hotfix 紧急修复线上崩溃跳过审查
- 责任人：user
- 事后补审截止：24h
```

### Q4: 审查报告中的 praise 是必需的吗？

**是。** 至少 1-2 条具体 praise。没有 praise 的报告会被视为刻薄，降低可信度。

### Q5: 如何审查 AI 生成的代码？

**标准不降反升。** AI 代码往往自信且合理，即使在错误时也是如此。必须：
- 更严格地检查边界情况
- 验证测试是否真正测试了行为
- 确认没有"看起来对但实际上错"的实现

### Q6: 语言指南只有 4 个通用的，没有 Python/Vue 专项怎么办？

当前版本已实现 4 个跨语言通用指南。Python/Vue 等专项指南标记为**预留（P1）**，可按需补充到 `code-reviewer/reference/` 目录。

---

## 七、进阶自定义

### 7.1 添加项目定制层

在项目级 skills 目录创建覆盖层：

```yaml
# .kimi/skills/my-project-review-rules/SKILL.md
---
name: my-project-review-rules
description: 本项目特定的代码审查规范覆盖层
---

## 前端（Vue 3.5 + TypeScript）
- 强制 Composition API
- Props 必须定义接口，禁止 any
- 加载 code-reviewer/reference/vue.md + typescript.md

## 后端（Python + FastAPI）
- Pydantic 模型必须含 Field 描述
- 数据库操作必须使用异步 session
- 加载 code-reviewer/reference/python.md
```

### 7.2 调整严重性阈值

编辑 `code-reviewer/SKILL.md` 中的严重性标记体系表格，根据团队约定调整 blocking/important 的定义。

### 7.3 集成到 CI/CD

```yaml
# .github/workflows/review.yml
- name: Validate Review Artifacts
  run: |
    python scripts/validate.py --skill skills/sdlc/code-reviewer
    # 检查 review-request.yaml / review-report.yaml 格式
```

---

## 八、版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-05-26 | 初始版本：4 核心 skill + 4 通用 reference 指南 |
