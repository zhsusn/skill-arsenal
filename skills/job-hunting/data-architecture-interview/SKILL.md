---
name: data-architecture-interview
description: 当用户明确要求生成大数据/数据架构领域的面试练习题，或提到'数据架构面试题'、'大数据架构师面试'、'数仓架构面试'、'Lakehouse面试'、'实时数仓面试'时触发。生成覆盖实时/离线架构、湖仓一体、OLAP引擎、高并发数据服务、OneID/用户画像、数据治理、可观测性七大核心域的结构化面试题，支持概念框架、架构设计、性能调优、跨域治理四种题型。
---

# Data Architecture Interview

## Purpose

Generate structured data architecture and big data platform interview practice questions in a multi-part format. Covers the seven core domains: Real-time & Offline Architecture, Lakehouse, OLAP Engine, High-Concurrency Data Service, OneID / User Profile, Data Governance, and Observability.

## Workflow

### 1) Scan Existing Content First

Before generating anything:

1. List repository files and relevant subdirectories.
2. Review markdown files that look like prior data architecture interview questions, attempts, or solutions.
3. For each discovered question, note:
   - Domain/scenario
   - Whether it includes a reference answer
   - Whether it is a full solution vs skeleton/partial
4. Treat all discovered scenarios as completed and avoid duplicates.

Also treat these as already completed:

- Lakehouse platform with Flink + Paimon (7000+ offline / 1000+ real-time tasks)
- High-concurrency UBS data gateway (200B logs/day, QPS 100K+, P99<50ms)
- Frontend observability system (Java Agent + StarRocks, P99<3s)
- OneID generation with distributed ID + graph computing
- StarRocks OLAP optimization with Bitmap index
- Data governance system for 500+ tables (lineage, quality, security)
- CDC real-time sync with Debezium + Hudi (minute-level, <5min delay)
- Cross-border data federation for SEA business units

### 2) Ask Exactly Two Questions

Ask the user only these two questions, then wait for answers:

1. What style of interview should this be?
   - Concept & Framework (Lakehouse principles, Lambda vs Kappa, data modeling, OLAP storage formats)
   - Scenario Design (platform architecture, real-time pipeline, cost optimization, cross-region deployment)
   - Performance Tuning & Troubleshooting (Flink backpressure, StarRocks query slow, Kafka consumer lag, GC in data services)
   - Mixed
2. What difficulty level?
   - Junior (execution-focused: writing Flink SQL, configuring Kafka topics, StarRocks table design, data ingestion pipelines)
   - Senior (design + tuning: choosing storage engine, balancing cost vs latency, data governance integration, platform evolution)
   - Principal/Director (strategic: multi-business-line platform, data asset valuation, cloud vs on-premise, AI-data convergence)

### 3) Generate One Markdown Interview

Create a single markdown file in the repository with a descriptive name (for example, `da_lakehouse_fintech_interview.md`).

Use this interview structure:

- **Part 1 (~15 min): Concept & Framework** — core definitions, Lakehouse vs Data Warehouse vs Data Lake, data modeling (dimensional vs Data Vault), OLAP indexing, exactly-once semantics. Foundation for everything that follows.
- **Part 2 (~20 min): Scenario Design** — platform architecture or pipeline design that stresses Part 1 concepts. Must include realistic constraints (PB-scale data, multi-region, budget limit, existing tech stack).
- **Part 3 (~15 min): Performance Tuning & Troubleshooting** — Flink backpressure, StarRocks query optimization, Kafka rebalancing, or data service OOM. Requires hands-on tuning experience.
- **Part 4 (~10 min): Deep Dive Discussion** — 3-4 open-ended questions on scaling, failure modes, or emerging trends (AI-ready data platform, real-time governance, data mesh, data asset accounting).

## Design Constraints

**Do this:**

- Real enterprise or fintech/e-commerce framing, not academic exercises.
- Include at least one cross-functional stakeholder conflict (Data Team vs Backend Team, Finance vs Engineering, HQ vs Regional Office).
- Include at least one quantifiable target (e.g., "reduce data latency from T+1 to minute-level", "support 200B events/day", "reduce cloud cost by 20%").
- Deep dives should have genuine trade-offs with no single "right" answer.
- Tailor complexity to the stated seniority level.
- Ground questions in real frameworks and versions where applicable (Flink 1.17+, Paimon 0.6+, StarRocks 3.x, Kafka 3.x, K8s 1.28+).

**Avoid:**

- Questions that hinge purely on memorizing Flink API method names.
- Overly broad scenarios that cannot be scoped in the given time.
- Questions where the "answer" is just listing tools without reasoning.
- Trivial Part 1 with all difficulty deferred to later parts.
- Fake company names that sound like real ones (use clearly fictional names).

## Domain Coverage Rotation

For each generated interview, privately ensure balanced coverage across the seven architecture domains:

| Domain | Sample Focus Areas |
|--------|-------------------|
| **Real-time & Offline Architecture** | Lambda vs Kappa, stream-batch unification, Flink SQL vs DataStream, Watermark & late data, checkpoint mechanism |
| **Lakehouse** | Paimon/Iceberg/Hudi, ACID on object storage, time travel, schema evolution, compaction strategy, Flink + Lakehouse integration |
| **OLAP Engine** | StarRocks/ClickHouse/Doris, MPP architecture, Bitmap index, materialized view, federated query, short-circuit optimization |
| **High-Concurrency Data Service** | Data API gateway, async ingestion, batch vs streaming write, connection pool, QPS/latency SLA, degradation |
| **OneID / User Profile** | Distributed ID, graph computing, device fingerprinting, identity resolution, real-time label updates, RTA advertising |
| **Data Governance** | Metadata management, lineage (static + dynamic), data quality rules, cost optimization, cold/hot tiering, data asset catalog |
| **Observability** | Java Agent byte-code enhancement, OpenTelemetry, full-link tracing, metrics/logs/traces correlation, anomaly detection |

Rotate the primary domain of Part 2 and Part 3 across interviews to ensure variety.

## Seniority-Level Adjustments

**Junior:**
- Focus on execution: writing Flink SQL, creating StarRocks tables, configuring Kafka producers, building data pipelines.
- Provide more scaffolding in the prompt (suggest table schemas, give partial Flink job DAG).
- Expect concrete tool knowledge (Flink, Kafka, StarRocks, Paimon, Hive, Spark SQL).

**Senior:**
- Focus on design and trade-offs: choosing Lakehouse format, balancing real-time vs cost, designing OLAP indexing, integrating governance with pipelines.
- Less scaffolding, more ambiguity by design.
- Expect cross-domain integration (e.g., how data quality rules affect lineage accuracy, how governance impacts query performance).

**Principal/Director:**
- Focus on platform strategy: building multi-business-line data platforms, data mesh vs centralization, data asset valuation and accounting, AI-data convergence, multi-cloud strategy.
- Include CTO-level or business-unit-head stakeholder perspectives.
- Expect quantified business cases and risk-adjusted ROI for platform investments.

## Required Output Format

The generated markdown must include:

1. **Title and metadata** (duration, difficulty, primary domains, tech stack context).
2. **Background** with enterprise context, existing data landscape, and organizational constraints.
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

- Designing a PB-scale Lakehouse platform for a fintech company with 20+ business lines
- Building a real-time user behavior analysis system (200B events/day, QPS 100K+)
- Optimizing StarRocks query performance for sub-second ad-hoc analytics on 10TB+ daily data
- Architecting a cross-region data platform for domestic + SEA business (data sovereignty compliance)
- Implementing OneID with graph computing across 10+ applications and 5+ data sources
- Building an observability system with Java Agent + OpenTelemetry for 200+ microservices
- Migrating from Hive-only to Flink + Paimon Lakehouse with zero downtime
- Designing a data API gateway for real-time label queries (RTA advertising, P99<50ms)
- Handling Flink backpressure during peak traffic (double 11 / loan promotion events)
- Evaluating data mesh vs centralized data platform for a conglomerate with autonomous BUs
- Building an AI-ready data foundation for LLM training and RAG knowledge base

## Gotchas

- **Version accuracy**: When referencing specific Flink/StarRocks/Paimon features, verify the version exists. Frame as "per Flink 1.17 documentation" if uncertain.
- **Tool neutrality**: Avoid questions that assume a single vendor stack (e.g., only Alibaba Cloud). Candidates should be evaluated on principles, not cloud certifications.
- **Ambiguity is intentional**: The best scenario questions are deliberately under-specified to test the candidate's ability to ask clarifying questions.
- **No real companies**: Use fictional but realistic company names to avoid confusion or misrepresentation.
- **Domain depth**: Do not let the interview drift into pure data engineering or pure business analysis. Keep the focus on *data architecture*—platform design, storage engine selection, pipeline orchestration, and cross-system integration.
