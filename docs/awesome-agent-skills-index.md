# Awesome Agent Skills 开源项目索引

> 本文档收录 GitHub 上公开可访问的 Agent Skills 相关开源项目，按类别整理，便于快速定位和参考。
> 
> 📅 数据收集时间：2026-05-26 | ⭐ Star 数量为近似值，随时间变化，请以 GitHub 页面为准

---

## 📑 目录

- [一、Awesome 聚合索引](#一awesome-聚合索引)
- [二、生产级 Skill 套件](#二生产级-skill-套件)
- [三、平台与厂商官方 Skills](#三平台与厂商官方-skills)
- [四、专项 Skills](#四专项-skills)
- [五、工具与安装器](#五工具与安装器)

---

## 一、Awesome 聚合索引

> 汇总和索引多个 Agent Skills 的 Awesome List 或策展仓库，适合作为生态入口。

| skill项目 | 来源URL | star数量 | 备注 |
|---|---|---|---|
| **VoltAgent/awesome-agent-skills** | https://github.com/VoltAgent/awesome-agent-skills | ⭐ 22,000+ | 最严格的策展仓库。1000+ skills，来自 Anthropic、Microsoft、Sentry、Trail of Bits 等官方团队。强调 "hand-picked, not AI-slop"。兼容 Claude Code / Codex / Gemini CLI / Cursor / Copilot / Windsurf 等 |
| **ComposioHQ/awesome-claude-skills** | https://github.com/ComposioHQ/awesome-claude-skills | ⭐ 39,000+ | Claude Skills 质量合集，覆盖开发、数据分析、商业等领域 |
| **gmh5225/awesome-skills** | https://github.com/gmh5225/awesome-skills | - | 社区 curated list，汇集 skills 仓库、资源和工具链接，覆盖多平台 |
| **ai-boost/awesome-prompts** | https://github.com/ai-boost/awesome-prompts | ⭐ 7,000+ | 从 GPT Store 顶级 GPT 提取的 prompts + Prompt Engineering 论文。含 Agent Skills 相关资源 |
| **skillcreatorai/Awesome-Agent-Skills** | https://github.com/skillcreatorai/Awesome-Agent-Skills | - | 通用 skills 策展列表，提供 `npx ai-agent-skills` CLI 一键安装 |
| **Bosh-Kuo/awesome-agent-toolkit** | https://github.com/Bosh-Kuo/awesome-agent-toolkit | - | 聚合 MCP configs + agent skills + prompts + tools |

---

## 二、生产级 Skill 套件

> 面向完整 SDLC 或真实工程工作流的 Skill 集合，可直接用于生产环境。

| skill项目 | 来源URL | star数量 | 备注 |
|---|---|---|---|
| **obra/superpowers** | https://github.com/obra/superpowers | ⭐ 190,000+ | 目前最火的 Agentic Skills 框架。20+ 核心 skills，覆盖 brainstorm / write-plan / execute-plan / TDD / debug / review 等完整工作流。支持 Claude Code / Cursor / Codex / Gemini / Copilot / OpenCode |
| **mattpocock/skills** | https://github.com/mattpocock/skills | ⭐ 97,000+ | TypeScript 讲师 Matt Pocock 的真实 `.claude` 目录开源。17+ dev workflow skills：PRD 写作、TDD、架构分析、Git guardrails、issue triage、refactoring。上线即霸榜 GitHub Trending #1 |
| **addyosmani/agent-skills** | https://github.com/addyosmani/agent-skills | ⭐ 42,000+ | Google 前工程师 Addy Osmani 创建。23 个生产级工程 skills，覆盖 spec → plan → build → test → review → ship 全生命周期。7 条 slash 命令驱动。融入 Google 工程文化最佳实践 |
| **anthropics/skills** | https://github.com/anthropics/skills | ⭐ 136,000+ | Anthropic 官方 Agent Skills 仓库。定义 SKILL.md 规范（渐进式披露），含 docx/pdf/pptx/xlsx 文档 skills + skill-creator + 模板。全平台覆盖：Claude Code / Claude.ai / Claude API |
| **gsd-build/get-shit-done** | https://github.com/gsd-build/get-shit-done | ⭐ 22,800+ | 轻量级元提示、上下文工程和规格驱动开发系统。面向 Claude Code 和 OpenCode |
| **datawhalechina/hello-agents** | https://github.com/datawhalechina/hello-agents | ⭐ 23,800+ | DataWhale 中文社区出品的 Agent 学习仓库 |

---

## 三、平台与厂商官方 Skills

> 各大技术公司和平台官方发布的 Agent Skills，通常与其产品生态深度整合。

| skill项目 | 来源URL | star数量 | 备注 |
|---|---|---|---|
| **github/awesome-copilot** | https://github.com/github/awesome-copilot | ⭐ 33,400+ | GitHub Copilot 官方技能仓库。含 instructions、agents、skills 和配置。支持 `gh skills install` 安装 |
| **huggingface/skills** | https://github.com/huggingface/skills | ⭐ 7,700+ | Hugging Face 官方 skills，覆盖 ML 工作流 |
| **openai/skills** | https://github.com/openai/skills | - | OpenAI 官方 skills，覆盖文档处理等场景 |
| **microsoft/* (Azure AI Foundry)** | https://github.com/microsoft/ | - | Microsoft Azure AI Foundry 官方发布 133+ skills，覆盖 .NET / Java / Python / Rust / TypeScript 等 6 种语言 |
| **vercel-labs/agent-skills** | https://github.com/vercel-labs/agent-skills | - | Vercel 官方 skills |
| **stripe/agent-skills** | https://github.com/stripe/ | - | Stripe 官方 skills（支付集成） |
| **cloudflare/agent-skills** | https://github.com/cloudflare/ | - | Cloudflare 官方 skills（Workers / 边缘计算） |
| **netlify/agent-skills** | https://github.com/netlify/ | - | Netlify 官方 skills |
| **sentry/skills** | https://github.com/sentry/ | - | Sentry 官方 skills，覆盖 20+ 平台 SDK 接入 |
| **figma/skills** | https://github.com/figma/ | - | Figma 官方 skills（设计到代码转换） |
| **mongodb/skills** | https://github.com/mongodb/ | - | MongoDB 官方 skills |
| **redis/skills** | https://github.com/redis/ | - | Redis 官方 skills |
| **auth0/skills** | https://github.com/auth0/ | - | Auth0 官方 skills（身份认证） |
| **apollo/skills** | https://github.com/apollographql/ | - | Apollo GraphQL 官方 skills |
| **hashicorp/skills** | https://github.com/hashicorp/ | - | HashiCorp 官方 skills |
| **notion/skills** | https://github.com/makenotion/ | - | Notion 官方 skills（知识捕获、会议智能、spec-to-task） |
| **expo/skills** | https://github.com/expo/ | - | Expo 官方 skills（React Native） |
| **trailofbits/skills** | https://github.com/trailofbits/ | - | Trail of Bits 安全审计官方 skills |
| **google-labs/skills** | https://github.com/google-labs/ | - | Google Labs (Stitch) 官方 skills |
| **brave/skills** | https://github.com/brave/ | - | Brave 浏览器官方 skills |
| **browserbase/skills** | https://github.com/browserbase/ | - | Browserbase 官方 skills |
| **binance/skills** | https://github.com/binance/ | - | Binance 官方 skills |
| **wordpress/skills** | https://github.com/WordPress/ | - | WordPress 官方 skills |
| **venice.ai/skills** | https://github.com/veniceai/ | - | Venice.ai 官方 skills |
| **resend/skills** | https://github.com/resend/ | - | Resend 官方 skills（邮件发送 / React Email） |
| **neon/skills** | https://github.com/neondatabase/ | - | Neon 数据库官方 skills |

---

## 四、专项 Skills

> 聚焦特定领域或单一能力的 Skills，可作为上述套件的补充。

| skill项目 | 来源URL | star数量 | 备注 |
|---|---|---|---|
| **awesome-skills/code-review-skill** | https://github.com/awesome-skills/code-review-skill | ⭐ 229 | 17+ 语言代码审查 skill。覆盖 React 19 / Vue 3 / Rust / TypeScript / TanStack Query / Java / Go 等，含安全审查、架构审查、性能审查指南 |
| **NeoLabHQ/code-review** | https://github.com/NeoLabHQ/code-review | - | 综合 PR 代码审查。使用专项 agent：bug-hunter / security-auditor / code-quality-reviewer / contracts-reviewer / historical-context-reviewer / test-coverage-reviewer |
| **NeoLabHQ/sdd** | https://github.com/NeoLabHQ/sdd | - | Spec-Driven Development 工作流。将 prompt 转化为生产级实现，含结构化规划、架构设计、LLM-as-a-Judge 质量门禁 |
| **NeoLabHQ/ddd** | https://github.com/NeoLabHQ/ddd | - | 领域驱动开发 skill。含 Clean Architecture、SOLID 原则、设计模式 |
| **NeoLabHQ/reflexion** | https://github.com/NeoLabHQ/reflexion | - | 自反思循环 skill。强制 LLM 反思先前输出并自我修正 |
| **NeoLabHQ/sadd** | https://github.com/NeoLabHQ/sadd | - | SubAgent-Driven Development。独立子 agent 分发任务，迭代间含代码审查检查点 |
| **NeoLabHQ/kaizen** | https://github.com/NeoLabHQ/kaizen | - | 持续改进方法论 skill。基于日本 Kaizen 哲学和精益方法 |
| **NeoLabHQ/prompt-engineering** | https://github.com/NeoLabHQ/prompt-engineering | - | 提示工程技术与模式，含 Anthropic 最佳实践和 agent persuasion 原则 |
| **hamelsmu/eval-audit** | https://github.com/hamelsmu/eval-audit | - | 审计 LLM eval pipeline，暴露问题 |
| **hamelsmu/error-analysis** | https://github.com/hamelsmu/error-analysis | - | 系统性识别 LLM pipeline 中的失败模式 |
| **hamelsmu/generate-synthetic-data** | https://github.com/hamelsmu/generate-synthetic-data | - | 为 LLM eval 创建多样化合成测试输入 |
| **hamelsmu/write-judge-prompt** | https://github.com/hamelsmu/write-judge-prompt | - | 为主观标准设计 LLM-as-a-Judge evaluator |
| **hamelsmu/validate-evaluator** | https://github.com/hamelsmu/validate-evaluator | - | 将 LLM judge 与人类标注校准 |
| **hamelsmu/evaluate-rag** | https://github.com/hamelsmu/evaluate-rag | - | 评估 RAG 检索和生成质量 |
| **hamelsmu/build-review-interface** | https://github.com/hamelsmu/build-review-interface | - | 构建 LLM trace 审查的标注界面 |
| **anombyte93/atlas-ai-skills** | https://github.com/anombyte93/atlas-ai-skills | - | Atlas AI 开发工具包。5 个 skills：PRD 生成 / Session 管理 / Research 前置 / Skill 优化 / Accomplish 日志 |
| **muratcankoylan/context-engineering-kit** | https://github.com/muratcankoylan/context-engineering-kit | ⭐ 401 | 上下文工程综合技能集：上下文基础 / 退化识别 / 压缩策略 / 优化 / 多 agent 模式 / 记忆系统 / 工具设计 / 评估框架 |
| **jherrodthomas/automotive-skills-suite** | https://github.com/jherrodthomas/automotive-skills-suite | - | 152 个汽车工程 skills。覆盖 ISO 26262 / ISO/SAE 21434 / ISO 21448 SOTIF / ASPICE / AUTOSAR |
| **sanbir/solidity-auditor-skills** | https://github.com/sanbir/solidity-auditor-skills | - | Solidity 安全审计 skill。210 个攻击向量，5-7 并行 agent，DeFi 协议检查清单 |
| **sanbir/solana-auditor-skills** | https://github.com/sanbir/solana-auditor-skills | - | Solana/Rust 安全审计 skill。105 个攻击向量，Anchor/native Rust/Pinocchio |
| **sanbir/ton-auditor-skills** | https://github.com/sanbir/ton-auditor-skills | - | TON/FunC/Tact 安全审计 skill。120 个攻击向量 |
| **sanbir/sui-auditor-skills** | https://github.com/sanbir/sui-auditor-skills | - | Sui Move 安全审计 skill。143 个攻击向量 |
| **rameerez/claude-code-startup-skills** | https://github.com/rameerez/claude-code-startup-skills | - | 构建和运营软件创业公司、App 和 SaaS 的 skills |
| **testdino-hq/playwright-skill** | https://github.com/testdino-hq/playwright-skill | - | 70+ 生产级 Playwright 自动化测试模式：E2E / POM / CI/CD / 迁移 / CLI |
| **Leonxlnx/taste-skill** | https://github.com/Leonxlnx/taste-skill | - | 高 agency 前端 skill。可调整的设计方差、动效强度、视觉密度，防止通用 UI slop |
| **zscole/model-hierarchy-skill** | https://github.com/zscole/model-hierarchy-skill | - | 基于任务复杂度的成本优化模型路由 skill |
| **uucz/moyu** | https://github.com/uucz/moyu | - | 反过度工程 skill。5 种变体，10 平台支持 |
| **affaan-m/everything-claude-code** | https://github.com/affaan-m/everything-claude-code | ⭐ 46,500+ | Claude Code 综合安全审查 skill。含认证 / 输入处理 / secrets / API 的全面检查清单 |
| **jakedahn/pomodoro-system** | https://github.com/jakedahn/pomodoro-system | - | 番茄工作法系统 skill。含任务管理、时间追踪、休息提醒 |
| **meodai/skill.color-expert** | https://github.com/meodai/skill.color-expert | - | 色彩科学专家 skill。286K 词参考资料，覆盖 OKLCH/OKLAB / 调色板生成 / 无障碍 / 色彩命名 |
| **deusyu/translate-book** | https://github.com/deusyu/translate-book | - | 书籍翻译 skill。PDF/DOCX/EPUB 并行子 agent 翻译，支持断点续传 |
| **CloudAI-X/threejs-skills** | https://github.com/CloudAI-X/threejs-skills | - | Three.js 3D 元素和交互体验创建 skills |

---

## 五、工具与安装器

> 辅助安装、管理、生成 Agent Skills 的工具和 CLI。

| skill项目 | 来源URL | star数量 | 备注 |
|---|---|---|---|
| **numman-ali/openskills** | https://github.com/numman-ali/openskills | ⭐ 7,200+ | Skills 通用安装器。将 Anthropic Skills 系统赋能给所有 AI 编程智能体，支持从本地路径或私有 Git 仓库加载 skill |
| **skillcreatorai/ai-agent-skills** (npm) | https://github.com/skillcreatorai/Ai-Agent-Skills | - | `npx ai-agent-skills install <skill>` 一键安装到各 agent 原生目录。支持 Claude Code / Cursor / VS Code / Amp 等 |
| **dmgrok/mcp_mother_skills** | https://github.com/dmgrok/mcp_mother_skills | - | MCP 服务器，基于项目上下文动态提供 agent skills。聚合 112 个 skills（Anthropic / GitHub / OpenAI / HuggingFace / Vercel / SkillCreator.ai） |
| **Cake-Agentic-AI-Workflows/cake-workflow-builder** | https://github.com/Cake-Agentic-AI-Workflows/cake-workflow-builder | - | 可视化 workflow builder，无需写 markdown 即可生成 SKILL.md 文件 |
| **SkillCreator.ai** | https://skillcreator.ai/ | - | 在线 skill 生成器。从自然语言描述生成 skill，30 秒完成 |

---

## 🔖 使用建议

| 场景 | 推荐入口 |
|---|---|
| 快速了解生态全貌 | `VoltAgent/awesome-agent-skills` |
| 需要完整 SDLC 工程纪律 | `obra/superpowers` / `addyosmani/agent-skills` |
| 需要真实工程师日常 workflow | `mattpocock/skills` |
| 需要了解 SKILL.md 规范 | `anthropics/skills` |
| 需要特定工具/平台整合 | `VoltAgent/awesome-agent-skills` 中按厂商筛选 |
| 需要代码审查专项能力 | `awesome-skills/code-review-skill` / `NeoLabHQ/code-review` |
| 需要上下文工程/多 agent 架构 | `muratcankoylan/context-engineering-kit` |
| 需要安全审计 | `sanbir/*` 系列 |
| 需要一键安装 skills | `npx ai-agent-skills` / `openskills` |

---

## 📝 贡献与更新

本索引为手工整理，可能存在遗漏或数据滞后。欢迎通过以下方式补充：

1. **发现新的开源 Skills 项目**：提交 PR 补充到对应分类
2. **Star 数量更新**：各项目 star 数增长迅速，可在使用时核对 GitHub 实际数据
3. **分类调整**：若某项目定位与当前分类不符，可建议调整

---

*本索引由 skill-arsenal 项目维护，旨在为国内 AI 开发者提供 Agent Skills 生态的一站式导航。*
