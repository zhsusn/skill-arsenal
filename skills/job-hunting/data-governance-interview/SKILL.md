---
name: data-governance-interview
description: 当用户明确要求生成数据治理领域的面试练习题，或提到'数据治理面试题'、'data governance interview'、'DAMA面试'、'数据治理练习'时触发。生成覆盖数据标准、数据质量、元数据、数据血缘、主数据管理（MDM）、数据安全六大核心域的结构化面试题，支持概念框架、场景设计、合规案例、技术工具四种题型。
---

# Data Governance Interview

## Purpose

Generate structured data governance interview practice questions in a multi-part format. Covers the six core governance domains: Data Standards, Data Quality, Metadata, Data Lineage, Master Data Management (MDM), and Data Security.

## Workflow

### 1) Scan Existing Content First

Before generating anything:

1. List repository files and relevant subdirectories.
2. Review markdown files that look like prior data governance interview questions, attempts, or solutions.
3. For each discovered question, note:
   - Domain/scenario
   - Whether it includes a reference answer
   - Whether it is a full solution vs skeleton/partial
4. Treat all discovered scenarios as completed and avoid duplicates.

Also treat these as already completed:

- Financial supply-chain customer MDM design
- Banking regulatory reporting lineage audit
- GDPR cross-border data classification matrix
- Healthcare PHI de-identification strategy
- Retail product catalog data quality framework
- Telecom subscriber data retention policy
- Insurance claim data steward RACI design

### 2) Ask Exactly Two Questions

Ask the user only these two questions, then wait for answers:

1. What style of interview should this be?
   - Concept & Framework (definitions, DAMA-DMBOK, DCAM, policy design)
   - Scenario Design (architecture, implementation, trade-offs)
   - Compliance & Case (regulatory conflicts, incident response, audit)
   - Mixed
2. What difficulty level?
   - Junior (analyst/associate, execution-focused)
   - Senior (manager/architect, design + stakeholder management)
   - Principal/Director (strategy, org design, multi-domain governance)

### 3) Generate One Markdown Interview

Create a single markdown file in the repository with a descriptive name (for example, `dg_mdm_finance_interview.md`).

Use this interview structure:

- **Part 1 (~15 min): Concept & Framework** — core definitions, framework selection, policy drafting. Foundation for everything that follows.
- **Part 2 (~20 min): Scenario Design** — architecture or process design that stresses Part 1 concepts. Must include realistic constraints (budget, legacy systems, org politics).
- **Part 3 (~15 min): Compliance & Case Analysis** — regulatory requirement or incident case. Requires risk assessment, stakeholder negotiation, and trade-off justification.
- **Part 4 (~10 min): Deep Dive Discussion** — 3-4 open-ended questions on scaling, failure modes, or emerging trends (AI governance, privacy-preserving compute, federated governance).

## Design Constraints

**Do this:**

- Real enterprise or regulatory framing, not academic exercises.
- Include at least one cross-functional stakeholder conflict (IT vs Business, Compliance vs Product, HQ vs Regional).
- Include at least one quantifiable target (e.g., "reduce data quality issues by 40%", "achieve 99.9% lineage coverage").
- Deep dives should have genuine trade-offs with no single "right" answer.
- Tailor complexity to the stated seniority level.
- Ground questions in real regulatory frameworks where applicable (GDPR, CCPA, HIPAA, 银保监会数据治理指引, EAST, SOX).

**Avoid:**

- Questions that hinge purely on memorizing DAMA-DMBOK chapter numbers.
- Overly broad scenarios that cannot be scoped in the given time.
- Questions where the "answer" is just listing tools without reasoning.
- Trivial Part 1 with all difficulty deferred to later parts.
- Fake company names that sound like real ones (use clearly fictional names).

## Domain Coverage Rotation

For each generated interview, privately ensure balanced coverage across the six governance domains:

| Domain | Sample Focus Areas |
|--------|-------------------|
| **Data Standards** | Naming conventions, business glossary, data dictionary, value domain constraints |
| **Data Quality** | Dimensions (completeness, accuracy, consistency, timeliness, uniqueness, validity), DQ rules, scoring cards |
| **Metadata Management** | Technical/business/operational metadata, data catalog design, impact analysis |
| **Data Lineage** | Field-level lineage, ETL pipeline traceability, upstream change impact, audit trail |
| **Master Data Management** | Golden record design, match/merge/survivorship, federation vs centralization, data stewardship |
| **Data Security** | Classification levels, static/dynamic masking, encryption, access control, privacy-enhancing technologies |

Rotate the primary domain of Part 2 and Part 3 across interviews to ensure variety.

## Seniority-Level Adjustments

**Junior:**
- Focus on execution: writing DQ rules, cataloging metadata, running lineage extraction scripts.
- Provide more scaffolding in the prompt (suggest tables, give partial RACI).
- Expect concrete tool knowledge (SQL, Python, Great Expectations, Atlas, dbt).

**Senior:**
- Focus on design and trade-offs: selecting MDM architecture mode, defining quality SLAs, balancing security vs usability.
- Less scaffolding, more ambiguity by design.
- Expect cross-domain integration (e.g., how data quality rules affect lineage accuracy).

**Principal/Director:**
- Focus on organizational transformation: building governance committees, funding models, change management, multi-year roadmaps.
- Include board-level or regulatory-examiner stakeholder perspectives.
- Expect quantified business cases and risk-adjusted ROI.

## Required Output Format

The generated markdown must include:

1. **Title and metadata** (duration, difficulty, primary domains, regulatory context).
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

- Designing a data governance operating model for a post-merger bank
- Implementing field-level lineage for a 500-table data warehouse migration
- Building a customer golden record across CRM, ERP, and e-commerce platforms
- Responding to a regulatory finding on data quality for risk-weighted asset calculations
- Creating a cross-border data classification policy for a multinational SaaS company
- Establishing data stewardship for a self-service analytics program
- Designing PII detection and masking for a ML training pipeline
- Reconciling conflicting data definitions between finance and operations
- Architecting a data catalog for a hybrid cloud (on-prem + Snowflake + Databricks) environment
- Creating retention and deletion policies for a healthcare IoT platform
- Implementing DQ monitoring for real-time streaming data pipelines
- Designing federated MDM for a conglomerate with autonomous business units

## Gotchas

- **Regulatory accuracy**: When referencing specific regulations (e.g., 银保监会指引 Article X), verify the article exists or frame as "per regulatory guidance" rather than citing fake articles.
- **Tool neutrality**: Avoid questions that assume a single vendor stack. Candidates should be evaluated on principles, not product certifications.
- **Ambiguity is intentional**: The best scenario questions are deliberately under-specified to test the candidate's ability to ask clarifying questions.
- **No real companies**: Use fictional but realistic company names to avoid confusion or misrepresentation.
- **Domain depth**: Do not let the interview drift into pure data engineering or pure compliance law. Keep the focus on *governance*—policy, process, stewardship, and cross-functional orchestration.
