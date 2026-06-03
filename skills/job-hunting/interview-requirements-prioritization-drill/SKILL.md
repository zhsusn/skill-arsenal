---
name: interview-requirements-prioritization-drill
description: Runs a rapid system design drill focused on clarification questions and requirement prioritization before architecture work. Use when the user wants to practice follow-up questions, requirement scoping, or turning an ambiguous prompt into a small set of prioritized functional and non-functional requirements.
---

# Requirements Prioritization Drill

## Purpose

Train the user on the first 5-10 minutes of a system design interview:

- parsing an ambiguous prompt
- asking strong follow-up questions
- compressing the problem into a few prioritized requirements

This drill is interactive and ephemeral. Do not save generated problems, notes, or solutions to disk unless the user explicitly asks.

## When To Use

Use this skill when the user asks to:

- practice system design follow-up questions
- get better at requirements gathering
- improve prioritization or scoping
- run a quick drill before the main design

## Drill Rules

1. Keep each round fast. The target is a short reps-based exercise, not a full interview.
2. Generate a new problem description in chat only. Do not create files.
3. Privately prepare three things before starting the round:
   - a small set of ideal follow-up questions
   - concise ideal answers to those questions
   - a strong target set of prioritized requirements
4. Do not reveal the ideal answers immediately.
5. Stay in interviewer mode until the user submits a block of functional and non-functional requirements or explicitly asks for feedback.
6. Keep the scope on requirements and prioritization. Do not drift into entities, APIs, or architecture unless the user explicitly asks to extend the round.

## Round Structure

### 1. Generate Problem

Generate a realistic but ambiguous system design prompt:

- 1-3 sentences
- product or infrastructure flavored
- enough ambiguity to require clarification
- one clear scaling or consistency tension
- no niche domain knowledge required

Avoid:

- overused canonical prompts with canned answers
- prompts that are so broad they cannot be scoped quickly
- prompts that closely copy existing repository scenarios

When useful, include a short setup line such as:

- duration: `5-minute requirements drill`
- target level: `senior`

### 2. Invite Clarifying Questions

Ask the user to drive with follow-up questions.

Do not dump all helpful questions up front. Let the user practice.

If the user stalls or asks for help, offer up to three suggested question directions, not the full answer. Good categories:

- users and use cases
- scope boundaries
- scale and traffic shape
- latency and durability expectations
- consistency and failure tolerance
- operational or compliance constraints

### 3. Answer As Interviewer

Answer each question like a real interviewer:

- be concise
- be consistent with the scenario
- confirm reasonable assumptions
- avoid over-specifying the problem
- give enough detail to support prioritization

If the user asks low-value or premature questions, gently redirect toward requirements-level concerns.

### 4. Wait For Requirements

Continue until the user sends a block of text containing:

- functional requirements
- non-functional requirements

If the user starts designing too early, redirect:

`Pause there. Before architecture, give me your prioritized functional and non-functional requirements.`

### 5. Provide Feedback

Once the user submits requirements, respond with four sections:

1. `What was strong`
2. `What to tighten`
3. `Suggested improved requirement set`
4. `Ideal follow-up questions I was hoping to hear`

Feedback should focus on:

- whether they found the product's core loop
- whether they kept the list small enough
- whether the NFRs actually force design choices
- whether they separated primary requirements from deferable concerns

### 6. Repeat

Offer another round immediately after feedback.

If the user wants to continue, generate a fresh problem and repeat from step 1.

## Prioritization Heuristics

Apply these heuristics while evaluating the user:

1. Find the core value loop first.
   Usually this is one end-to-end path, not the full product surface.
2. Prefer 3 functional requirements and 3 non-functional requirements.
   Four is acceptable. More than that usually needs pruning.
3. Keep only requirements that change the design.
   If a requirement does not materially affect the system shape, treat it as secondary.
4. Defer standard platform concerns unless central.
   Auth, admin tooling, dashboards, billing, and analytics are often assumptions unless the prompt makes them primary.
5. Quantify non-functional requirements.
   Avoid vague items like "it should scale" or "it should be reliable."
6. Tie each non-functional requirement to a hotspot.
   Example: low-latency reads, bursty writes, strict consistency on promotion, durable audit logs.

For deeper guidance and evaluation language, read [reference.md](reference.md).

## Problem Generation Pattern

For each round, privately sketch:

- scenario
- likely user
- likely core loop
- likely trap or distractor
- ideal top 3 functional requirements
- ideal top 3 non-functional requirements

Use that private sketch to answer questions and grade the user, but do not expose it before the feedback step.

## Feedback Standard

Keep feedback concrete. Prefer comments like:

- `You identified too many features and missed the core loop around X.`
- `Your NFRs are reasonable, but only one of them would actually change the architecture.`
- `You included auth and analytics too early; those are secondary for this round.`

Avoid generic praise or generic criticism.

## Example Prompt Types

Rotate across:

- operational tooling
- data pipelines
- marketplace workflows
- notification and messaging
- search and ranking
- collaboration
- release and deployment systems

Keep the domain broad enough that the exercise tests prioritization, not domain trivia.

## Gotchas
- **不要替用户生成“标准答案”后再让用户背诵**：演练的价值在于用户自己思考追问，如果提前 dump 理想答案，就变成记忆训练而非能力训练。
- **避免生成过于宽泛、无法在 5 分钟内收敛的题目**：如果 prompt 涉及“设计一个电商平台”而没有明确边界，用户会陷入功能罗列，无法练习 prioritization。
- **不要过早泄露 CAP 立场或具体技术选型**：在 requirements 阶段就告诉用户“这里应该用 eventual consistency”会破坏练习目标，技术决策应留到架构阶段。
- **反馈必须具体，禁止空泛评价**：像“还不错”或“需要改进”这样的反馈对提升毫无帮助，必须指出具体哪个 requirement 改变了架构选择、哪个是冗余的。