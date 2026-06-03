---
name: interview-system-design
description: Generates systems design interview practice (prompt + solution files), acts as an interactive interviewer, and reviews whiteboard designs via Excalidraw. Use when the user asks to create, practice, or get feedback on a system design interview.
---

# System Design Interview

## Purpose

Generate, facilitate, and review systems design interview practice sessions. Operates in three modes depending on what the user asks for.

## Mode 1: Generate Interview

Triggered when the user asks to create or generate a new system design interview.

### 1) Scan Existing Content First

Before generating anything:

1. List repository files and subdirectories.
2. Look for existing `sd_*_interview.md` and `sd_*_solution.md` files.
3. For each discovered interview, note the topic/scenario.
4. Treat all discovered scenarios as completed and avoid duplicates.

Also treat these as already completed:

- Ticketmaster (event ticketing / seat reservation)
- Tinder
- Bit.ly

### 2) Ask Three Questions

Ask the user these three questions, then wait for answers:

1. How long is the interview?
   - 30 minutes (focused, single deep dive)
   - 45 minutes (standard)
   - 60 minutes (full loop, multiple deep dives)
2. What company or style of company?
   - FAANG / Big Tech (breadth + depth, structured rubric)
   - Growth-stage startup (pragmatic, real constraints, scrappy)
   - Infrastructure / platform company (deep infra knowledge)
   - Custom (user provides description)
3. Any specific domain, constraints, or focus areas? (optional free text)

### 3) Research

Before generating, fetch relevant guides to ground the question in real interview patterns:

- Fetch the hellointerview.com delivery framework: `https://www.hellointerview.com/learn/system-design/in-a-hurry/delivery`
- If the chosen topic maps to a known problem, attempt to fetch its breakdown from `https://www.hellointerview.com/learn/system-design/problem-breakdowns/{topic}`
- Reference core concepts (CAP theorem, consistency models, key technologies) to produce realistic non-functional requirements.

### 4) Generate Two Files

Produce two markdown files saved to the repository root.

#### File 1: `sd_{name}_interview.md` (clean prompt, no answers)

This is what the candidate works from. It must contain NO hints, NO answers, and NO reference material.

Structure:

```
# {Problem Name}

**Duration:** {30/45/60} min
**Level:** {mid / senior / staff}
**Focus areas:** {e.g., real-time, pub/sub, horizontal scaling}

## Problem Statement

{Realistic, ambiguous prompt as an interviewer would deliver it. 1-3 sentences. Under-specified by design.}

## Time Allocation

| Phase | Time |
|---|---|
| Requirements | ~5 min |
| Core Entities | ~2 min |
| API Design | ~5 min |
| High-Level Design | ~{10-15} min |
| Deep Dives | ~{10-15} min |

## Whiteboard

Create your diagram at: `~/notes/Excalidraw/sd_{name}.excalidraw.md`

---

## My Requirements

### Functional Requirements

(fill in)

### Non-Functional Requirements

(fill in)

## My Core Entities

(fill in)

## My API Design

(fill in)

## My High-Level Design

(notes here; whiteboard in Excalidraw)

## My Deep Dives

(fill in)
```

#### File 2: `sd_{name}_solution.md` (reference answer)

This is the answer key. The candidate should NOT read this until after attempting the interview or requesting review.

Structure:

1. **Title and Metadata** -- same as prompt file header.

2. **Expected Functional Requirements** -- 3-5 prioritized requirements the candidate should surface, phrased as "Users/Clients should be able to..." statements.

3. **Expected Non-Functional Requirements** -- 3-5 with quantified targets (e.g., "feed render latency < 200ms", "scale to 50M DAU"). Include CAP theorem stance.

4. **Capacity Estimation** -- only if it materially influences the design. State when and why to do the math.

5. **Expected Core Entities** -- entity list with key fields (not exhaustive, only design-relevant columns).

6. **Expected API Design** -- REST endpoints (default) or appropriate protocol with rationale. Include auth notes.

7. **Reference High-Level Design** -- component list (services, databases, caches, queues, CDN, etc.), data flow description for each core endpoint, key schema fields next to the relevant component, and a mermaid diagram of the target architecture.

8. **Deep Dive Areas** -- 2-3 areas scaled by interview duration (1 for 30 min, 2 for 45 min, 3 for 60 min). Each deep dive includes:
   - The bottleneck or problem to address
   - Key trade-offs to discuss (with pros/cons)
   - Expected technologies and patterns
   - What a strong answer looks like
   - What a weak answer looks like

9. **Curveball / Follow-up Questions** -- 2-3 interviewer probes that test edge cases, failure modes, or alternative approaches. Include what a good response covers.

10. **Evaluation Rubric** -- table with four dimensions:

| Dimension            | Does Not Meet | Meets | Exceeds |
| -------------------- | ------------- | ----- | ------- |
| Problem Navigation   | ...           | ...   | ...     |
| Solution Design      | ...           | ...   | ...     |
| Technical Excellence | ...           | ...   | ...     |
| Communication        | ...           | ...   | ...     |

Fill each cell with specific, problem-relevant criteria (not generic).

## Mode 2: Interview (Interactive)

Triggered when the user says they want to practice, start an interview session, or references an existing `sd_*_interview.md` file.

### Behavior

1. Read the prompt file to know the problem.
2. Read the solution file privately. Never reveal its contents.
3. Deliver the problem statement exactly as written in the prompt file.
4. Act as the interviewer for the remainder of the session:
   - Respond to clarification questions as an interviewer would: confirm valid assumptions, gently redirect off-track questions, give small nudges without revealing answers.
   - Do NOT volunteer information. Let the candidate drive.
   - When the candidate asks "what do you think?" or similar, give brief directional feedback (e.g., "You're missing a key non-functional requirement around consistency" -- not "the answer is strong consistency with Raft").
   - Match the company style if one was specified (e.g., a FAANG interviewer is more structured; a startup interviewer is more conversational and cares about pragmatism).
5. If the candidate gets stuck for an extended period, offer a single gentle nudge related to the current phase. Do not give multiple hints unprompted.
6. Keep track of which phase the candidate is in (requirements, entities, API, HLD, deep dives) based on what they're discussing.

### What NOT to do

- Never dump the solution or large parts of it.
- Never say "the answer is X" -- always frame as questions or observations.
- Never rush the candidate through phases.
- Never break character as interviewer unless the user explicitly asks to end the session.

## Mode 3: Review / Feedback

Triggered when the user asks for feedback, review, or critique of their work on an existing interview.

### Gathering Context

1. Read the candidate's filled-in sections from the `sd_*_interview.md` file (the `## My ...` sections).
2. Read the whiteboard via one or both of:
   - A screenshot the user shares (image attachment).
   - The Excalidraw file at `~/notes/Excalidraw/sd_{name}.excalidraw.md`. The Obsidian Excalidraw plugin stores diagrams as markdown with a `## Text Elements` section containing all box labels, service names, schemas, and annotations in plain text.
3. Read the solution file (`sd_{name}_solution.md`) as the reference.

### Providing Feedback

Structure feedback as:

1. **What was done well** -- specific strengths, not generic praise.
2. **What was missed or could be stronger** -- gaps compared to the reference, with explanation of why it matters.
3. **Specific suggestions** -- actionable improvements (e.g., "Adding a Redis cache in front of user-profile reads would address the latency NFR you identified" -- not just "add a cache").
4. **Rubric scores** -- rate each of the four evaluation dimensions (Problem Navigation, Solution Design, Technical Excellence, Communication) as does-not-meet / meets / exceeds, with a sentence explaining why.

### What NOT to do

- Never just dump the solution file as "here's what you should have done."
- Frame everything as coaching, not grading.
- Acknowledge valid alternative approaches that differ from the reference solution.

## Design Constraints for Generated Questions

**Do this:**

- Real product or infrastructure framing, not academic exercises.
- Ambiguous enough to require clarification -- the best system design questions are deliberately under-specified.
- Include at least one interesting scaling challenge.
- Include at least one interesting consistency/availability trade-off.
- Deep dives should have genuine trade-offs with no single "right" answer.
- Tailor complexity to the stated time frame.
- Tailor depth expectations to the company style.

**Avoid:**

- Overused canonical problems with well-known single answers (URL shortener, parking lot, TinyURL).
- Questions that require extremely niche domain knowledge.
- Questions where the "answer" is just listing technologies without reasoning.
- Overly broad questions that cannot be meaningfully scoped in the given time frame.

## Scenario Inspiration (not exhaustive)

- Collaborative document editing (like Google Docs)
- Live sports score / event streaming platform
- Food delivery order matching and tracking
- Content moderation pipeline at scale
- Feature flag / experimentation platform
- Multi-region chat system with offline support
- Distributed job scheduler (like Airflow)
- Payments processing system
- Inventory management for flash sales
- Notification delivery system (push, email, SMS)
- Social media feed ranking and delivery
- Video transcoding pipeline
- Ride-sharing matching and ETA system
- Search autocomplete / typeahead
- Distributed file storage (like Dropbox sync)
- Ad serving and auction system
- Collaborative whiteboard (like Figma multiplayer)
- IoT telemetry ingestion and alerting
- E-commerce product search with faceted filtering

## Gotchas
- **Prompt 文件中严禁包含任何答案、提示或参考材料**：candidate 可能会在练习前误读 prompt 文件，任何内嵌的 hint 都会破坏面试的公平性。
- **避免使用 URL Shortener、Parking Lot 等过度使用的经典题目**：这些题目有大量现成答案，无法有效区分候选人的真实水平，应优先选择业务场景题。
- **作为面试官时绝不要主动泄露 solution 文件内容**：即使候选人卡壳，也只能给出方向性提示（如“你漏了一个一致性相关的 NFR”），不能说出“这里应该用 Raft”。
- **Excalidraw 白板路径必须与候选人实际环境一致**：如果推荐的保存路径 `~/notes/Excalidraw/` 在候选人机器上不存在，会导致白板文件丢失，面试 review 时无法读取。
- Deployment pipeline with canary releases