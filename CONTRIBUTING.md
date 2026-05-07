# 贡献指南

感谢你对 `skill-arsenal` 的兴趣！本项目的愿景是打造一套**可扩展的 Skill 与 Spec 框架**，为软件全生命周期中的 AI 编码提供标准化、可复用的质量保障。无论你是想修复 Bug、新增 Skill，还是改进文档，我们都欢迎你的贡献。

> 如果你是第一次参与开源，可以搜索带有 [`good first issue`](https://github.com/zhsusn/skill-arsenal/labels/good%20first%20issue) 标签的 Issue 开始。

---

## 目录

- [开发环境搭建](#开发环境搭建)
- [报告 Bug](#报告-bug)
- [提议新功能](#提议新功能)
- [贡献流程](#贡献流程)
- [提交信息规范](#提交信息规范)
- [Skill 编写规范](#skill-编写规范)
- [更新文档](#更新文档)
- [审核与合并](#审核与合并)

---

## 开发环境搭建

本项目**零运行时依赖**，只需要：

- **Python 3.8+**（用于运行校验与转换脚本）
- **Bash**（用于运行安装脚本；Windows 用户建议使用 Git Bash 或 WSL）
- **Git**

无需 `pip install`、`npm install`、`make` 或 Docker。

克隆仓库后即可使用：

```bash
git clone https://github.com/zhsusn/skill-arsenal.git
cd skill-arsenal

# 验证环境
python3 scripts/validate.py
```

---

## 报告 Bug

如果你发现了问题，请通过 [Bug Report Issue 模板](https://github.com/zhsusn/skill-arsenal/issues/new?template=bug_report.md) 提交，并尽可能包含以下信息：

- 问题发生的 Skill 名称和文件路径
- 复现步骤（最小示例）
- 期望行为 vs 实际行为
- 运行环境（操作系统、Python 版本）

---

## 提议新功能

在提交大量代码前，建议先通过 [Feature Request Issue 模板](https://github.com/zhsusn/skill-arsenal/issues/new?template=feature_request.md) 讨论你的想法。这有助于：

- 确认需求与项目方向一致
- 避免重复劳动
- 获得维护者的早期反馈

---

## 贡献流程

### 1. Fork 并克隆

```bash
# 1. 在 GitHub 上 Fork 本仓库
# 2. 克隆你的 Fork
git clone https://github.com/<你的用户名>/skill-arsenal.git
cd skill-arsenal

# 3. 添加上游远程
git remote add upstream https://github.com/zhsusn/skill-arsenal.git
```

### 2. 创建功能分支

```bash
git checkout -b feat/my-new-skill
# 或
git checkout -b fix/validate-script-bug
```

分支命名建议：

| 前缀 | 用途 |
|------|------|
| `feat/` | 新增 Skill、功能 |
| `fix/` | 修复 Bug |
| `docs/` | 文档更新 |
| `refactor/` | 代码重构 |

### 3. 开发与修改

#### 如果是新增/修改 Skill：

1. 复制模板或修改现有 Skill：
   ```bash
   cp -r templates/new-skill-template skills/<category>/<skill-name>
   ```
2. 编写 `SKILL.md`（Frontmatter 仅限 `name` + `description`）
3. 编写 `meta.json`（扩展元数据）
4. 如需深度参考，创建 `references/REFERENCE.md` 或 `references/FORMS.md`
5. **运行校验**：
   ```bash
   python3 scripts/validate.py
   ```
6. **同步索引**：确保 `index.json` 包含新 Skill 的条目
7. **重新生成 Cursor 规则**（如修改了现有 Skill）：
   ```bash
   python3 scripts/convert.py --tool cursor --all --output .cursor/rules
   ```

#### 如果是修改脚本：

- 保持**标准库-only**原则（不引入第三方依赖）
- 确保修改后 `validate.py` 仍能正常运行
- 如涉及重大逻辑变更，建议在 PR 中补充测试说明

### 4. 提交

```bash
git add .
git commit -m "feat: add high-level-design skill"
```

提交信息请遵循 [Conventional Commits](https://www.conventionalcommits.org/zh-hans/v1.0.0/) 规范（详见下方）。

### 5. 推送并创建 Pull Request

```bash
git push origin feat/my-new-skill
```

然后在 GitHub 上创建 Pull Request，并确保：

- [ ] PR 标题清晰描述了变更内容
- [ ] 关联了相关的 Issue（如有）
- [ ] `validate.py` 本地校验通过
- [ ] `.cursor/rules/` 已同步更新（如涉及 Skill 修改）
- [ ] `index.json` 已同步更新（如涉及 Skill 增删）
- [ ] 文档已更新（如适用）

---

## 提交信息规范

采用 [Conventional Commits](https://www.conventionalcommits.org/zh-hans/v1.0.0/)：

```
<类型>(<可选范围>): <描述>

[可选的正文]

[可选的脚注]
```

常用类型：

| 类型 | 用途 |
|------|------|
| `feat` | 新增 Skill、功能 |
| `fix` | 修复 Bug |
| `docs` | 文档更新（README、AGENTS.md、docs/） |
| `style` | 格式调整（不影响功能） |
| `refactor` | 代码重构 |
| `chore` | 构建/工具链改动 |

示例：

```
feat(skills): add high-level-design skill for SDLC stage 3

- 支持配置驱动的 16 章节输出
- 引入严格边界红线（概要设计 vs 详细设计）
- 借鉴开源 architecture-blueprint-generator 的横切关注点框架

Closes #42
```

---

## Skill 编写规范

所有 Skill 必须遵守以下规范（详见 [`docs/skill-development-guide.md`](docs/skill-development-guide.md)）：

1. **单一职责**：一个 Skill 只做一件事
2. **Kimi Code 兼容**：`SKILL.md` Frontmatter **仅限 `name` + `description`**，其他元数据放入 `meta.json`
3. **必须包含 Gotchas**：每个 `SKILL.md` 正文必须包含 `## Gotchas` 章节
4. **触发场景描述**：`description` 必须描述用户说什么/什么情况下激活，而非功能清单
5. **目录名 kebab-case**：小写字母，单词间用 `-` 分隔，禁止连续连字符 `--`
6. **渐进式披露**：核心指令 < 500 行，深度知识放入 `references/`
7. **文档同步**：新增/修改 Skill 后，同步更新 `index.json` 和 `meta.json`

---

## 更新文档

如果你修改了以下内容，必须同步更新对应文档：

| 修改内容 | 需更新的文档 |
|----------|-------------|
| 新增/修改 Skill | `index.json`、`SKILL.md`、`meta.json`、`.cursor/rules/` |
| 新增分类 | `AGENTS.md`、本文件 (`CONTRIBUTING.md`) |
| 修改项目结构/流程 | `AGENTS.md`、`README.md` |
| 修改脚本行为 | `AGENTS.md`、相关 Skill 文档 |
| 修改平台兼容策略 | `docs/platform-compatibility.md` |

---

## 审核与合并

维护者会在收到 PR 后尽快审核。审核关注点包括：

1. **格式合规**：`validate.py` 是否通过
2. **内容质量**：Skill 是否遵循单一职责、Gotchas 是否完整
3. **文档同步**：`index.json`、`.cursor/rules/` 是否同步
4. **边界红线**：Skill 内容是否越界（如将详细设计混入概要设计）

审核通过后，维护者会执行 Squash and Merge，并清理提交信息。

---

再次感谢你的贡献！如有疑问，欢迎通过 [GitHub Discussions](https://github.com/zhsusn/skill-arsenal/discussions) 交流。
