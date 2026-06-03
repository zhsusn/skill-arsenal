---
name: java-backend-interview
description: 当用户明确要求生成Java后端/高并发领域的面试练习题，或提到'Java后端面试题'、'高并发面试'、'Spring Boot面试'、'JVM面试'、'Redis面试'时触发。生成覆盖Spring Boot、高并发系统设计、Redis深度应用、JVM调优、异步队列、限流熔断、分布式锁七大核心域的结构化面试题，支持概念框架、场景设计、源码分析、调优案例四种题型。
---

# Java Backend & High-Concurrency Interview

## Purpose

Generate structured Java backend and high-concurrency interview practice questions in a multi-part format. Covers the seven core domains: Spring Boot & Microservices, High-Concurrency System Design, Redis Deep Dive, JVM Tuning, Async Messaging, Rate Limiting & Circuit Breaker, Distributed Locking.

## Workflow

### 1) Scan Existing Content First

Before generating anything:

1. List repository files and relevant subdirectories.
2. Review markdown files that look like prior Java backend interview questions, attempts, or solutions.
3. For each discovered question, note:
   - Domain/scenario
   - Whether it includes a reference answer
   - Whether it is a full solution vs skeleton/partial
4. Treat all discovered scenarios as completed and avoid duplicates.

Also treat these as already completed:

- UBS high-concurrency write architecture (QPS 100K+)
- Redis user-profile cache consistency design
- JVM Full GC / OOM troubleshooting case
- Spring Boot @Async vs custom thread pool comparison
- Sentinel rate-limiting & circuit breaker design
- MyBatis SQL injection prevention & batch optimization
- Distributed locking with Redisson & RedLock debate
- Kafka consumer rebalancing & exactly-once semantics

### 2) Ask Exactly Two Questions

Ask the user only these two questions, then wait for answers:

1. What style of interview should this be?
   - Concept & Framework (Spring IoC, JVM memory model, Redis data structures, GC algorithms)
   - Scenario Design (high-concurrency architecture, cache consistency, async processing, degradation)
   - Source Code & Tuning (Spring Boot auto-config, JVM GC log analysis, Redis persistence, thread pool optimization)
   - Mixed
2. What difficulty level?
   - Junior (execution-focused, concrete tool knowledge: Spring Boot, MyBatis, Redis, Maven)
   - Senior (design + performance tuning: async queues, batching, JVM tuning, distributed locking)
   - Principal/Director (strategic: microservice governance, multi-language migration, platform evolution)

### 3) Generate One Markdown Interview

Create a single markdown file in the repository with a descriptive name (for example, `java_ubs_high_concurrency_interview.md`).

Use this interview structure:

- **Part 1 (~15 min): Concept & Framework** — core definitions, Spring IoC lifecycle, JVM memory model, Redis persistence, transaction propagation. Foundation for everything that follows.
- **Part 2 (~20 min): Scenario Design** — high-concurrency architecture or cache consistency design that stresses Part 1 concepts. Must include realistic constraints (QPS target, latency SLA, existing tech stack).
- **Part 3 (~15 min): Source Code & Tuning** — GC log analysis, thread pool deadlock, Redis slow query, or Spring Boot startup optimization. Requires hands-on experience and tool knowledge.
- **Part 4 (~10 min): Deep Dive Discussion** — 3-4 open-ended questions on scaling, failure modes, or emerging trends (Project Loom, GraalVM native image, Spring Boot 3.x native, virtual threads).

## Design Constraints

**Do this:**

- Real enterprise or e-commerce/fintech framing, not academic exercises.
- Include at least one cross-functional stakeholder conflict (Backend vs SRE, Business vs Stability, Monolith vs Microservice migration).
- Include at least one quantifiable target (e.g., "reduce P99 latency to <50ms", "support 100K+ QPS", "reduce Full GC frequency to <1 per day").
- Deep dives should have genuine trade-offs with no single "right" answer.
- Tailor complexity to the stated seniority level.
- Ground questions in real frameworks and versions where applicable (Spring Boot 2.x/3.x, JDK 8/11/17, Redis 6/7, JVM G1/ZGC).

**Avoid:**

- Questions that hinge purely on memorizing Spring annotation names.
- Overly broad scenarios that cannot be scoped in the given time.
- Questions where the "answer" is just listing tools without reasoning.
- Trivial Part 1 with all difficulty deferred to later parts.
- Fake company names that sound like real ones (use clearly fictional names).

## Domain Coverage Rotation

For each generated interview, privately ensure balanced coverage across the seven backend domains:

| Domain | Sample Focus Areas |
|--------|-------------------|
| **Spring Boot & Microservices** | Auto-configuration, Bean lifecycle, AOP proxy, transaction propagation, circular dependency, Spring Boot 3.x native image |
| **High-Concurrency System Design** | Async queues (Disruptor/BlockingQueue), batching, connection pool (HikariCP), thread pool isolation, load balancing, degradation |
| **Redis Deep Dive** | Data structures, cache penetration/breakdown/avalanche, distributed locking, persistence (RDB/AOF), Cluster/Sentinel, Pipeline |
| **JVM Tuning** | Memory model, GC algorithms (G1/ZGC/CMS), GC log analysis, OOM troubleshooting (MAT/jstack), JIT compilation, escape analysis |
| **Async Messaging** | Kafka/RabbitMQ/RocketMQ, exactly-once semantics, consumer rebalancing, message deduplication, dead-letter queue |
| **Rate Limiting & Circuit Breaker** | Token bucket / leaky bucket, Sentinel/Resilience4j, degradation strategy, fallback design |
| **Distributed Locking** | Redis SET NX EX, Redisson watchdog, RedLock debate, ZooKeeper/etcd locking, lock granularity |

Rotate the primary domain of Part 2 and Part 3 across interviews to ensure variety.

## Seniority-Level Adjustments

**Junior:**
- Focus on execution: writing CRUD with MyBatis, configuring RedisTemplate, setting up Spring Boot starters, basic JVM parameters.
- Provide more scaffolding in the prompt (suggest thread pool sizes, give partial configuration).
- Expect concrete tool knowledge (Spring Boot, MyBatis-Plus, Redis, Maven/Gradle, JUnit).

**Senior:**
- Focus on design and trade-offs: choosing between JDK proxy and CGLIB, designing cache consistency, tuning G1 for large heap, handling Kafka consumer lag.
- Less scaffolding, more ambiguity by design.
- Expect cross-domain integration (e.g., how Redis cache strategy affects database connection pool sizing).

**Principal/Director:**
- Focus on platform evolution: migrating from monolith to microservices, multi-language stack (Java + Go), service mesh adoption, backend platform standardization.
- Include CTO-level or SRE-team stakeholder perspectives.
- Expect quantified business cases and risk-adjusted ROI for platform investments.

## Required Output Format

The generated markdown must include:

1. **Title and metadata** (duration, difficulty, primary domains, tech stack context).
2. **Background** with enterprise context, existing tech stack, and organizational constraints.
3. **Parts 1-4**, each with behavioral spec and candidate response area.
4. **An evaluation criteria table** at the end with four dimensions:

| Dimension | Does Not Meet | Meets | Exceeds |
|-----------|--------------|-------|---------|
| Domain Knowledge | ... | ... | ... |
| Structured Thinking | ... | ... | ... |
| Stakeholder Navigation | ... | ... | ... |
| Practical Rigor | ... | ... | ... |

Fill each cell with specific, problem-relevant criteria (not generic).

## Scenario Inspiration

- Designing a high-concurrency event tracking service (100K+ QPS) with Spring Boot + Kafka + Flink
- Implementing cache consistency for user-profile data across Redis Cluster and MySQL
- Troubleshooting a production Full GC storm in a 32GB-heap Java service
- Migrating from Spring Boot 2.x to 3.x with GraalVM native image constraints
- Building a distributed idempotency layer for payment callbacks
- Architecting a multi-tenant SaaS backend with tenant-level resource isolation
- Optimizing MyBatis batch insert for 10M+ rows daily sync
- Designing a rate-limiting gateway for flash-sale e-commerce traffic
- Handling Redis Cluster failover without cache avalanche during peak traffic
- Evaluating virtual threads (Project Loom) vs traditional thread pools for I/O-heavy services

## Gotchas

- **Version accuracy**: When referencing specific JDK versions or Spring Boot features, verify the version exists (e.g., ZGC is production-ready since JDK 15, Shenandoah since JDK 12). Frame as "per JDK 17 documentation" if uncertain.
- **Tool neutrality**: Avoid questions that assume a single vendor stack. Candidates should be evaluated on principles, not product certifications.
- **Ambiguity is intentional**: The best scenario questions are deliberately under-specified to test the candidate's ability to ask clarifying questions.
- **No real companies**: Use fictional but realistic company names to avoid confusion or misrepresentation.
- **Domain depth**: Do not let the interview drift into pure frontend or pure DevOps. Keep the focus on *backend engineering*—concurrency, performance, stability, and cross-system integration.
