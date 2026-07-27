# Project Roadmap — FreightOps Analytics Platform
**Mentee:** Kushal Bendale | **Pace:** 5–8 hrs/week | **Target:** 1–3 months (~40–70 hrs)
**Domain:** Truckload carrier fleet & logistics operations (matches your TCS background)

Status legend: ⬜ not started · 🔶 in progress · ✅ complete

---

## Phase 0 — Business Understanding & Documentation (~4–5 hrs)
⬜ Business domain, problem statement, stakeholders, pain points
⬜ KPIs & success metrics
⬜ Functional / non-functional requirements, assumptions, risks
⬜ Mini-BRD + Project Charter (real artifact you'll keep)
**Interview outcome:** Can frame *why* the project exists before any tech talk — this is what separates "I used Spark" from "I solved a business problem with Spark."

## Phase 1 — SQL Deep Dive on Real Data (~8–10 hrs)
⬜ Joins, window functions, CTEs, recursive CTEs on trips/loads/routes
⬜ Query optimization, execution plans, indexing concepts
⬜ Build 10+ analytical queries answering real ops questions (on-time %, deadhead miles, driver utilization)
**Interview outcome:** Confidently whiteboard SQL under pressure — highest-weight skill for your target companies.

## Phase 2 — Python for Data Engineering (~6–8 hrs)
⬜ Pandas data cleaning on the messy fields (mixed date formats, nulls in fuel_purchases, dup detection)
⬜ OOP + config-driven pipeline structure, logging, exception handling
⬜ Data quality/validation framework + unit tests (pytest)
**Interview outcome:** Explain a real data-quality framework you built, not just "I used Pandas."

## Phase 3 — AWS Core (S3, Glue, Athena, Lambda, IAM) (~8–10 hrs)
⬜ S3 bucket structure (raw/bronze/silver/gold), IAM least-privilege roles
⬜ Glue Crawler + Glue Job (PySpark) on this data, Athena views
⬜ Lambda-based transformation, EventBridge trigger
⬜ Secrets Manager, cost/security discussion
**Interview outcome:** Match and *exceed* your resume's AWS bullet points with real, explainable implementation.

## Phase 4 — PySpark & Distributed Processing (~8–10 hrs)
⬜ DataFrame API, partitioning, broadcast join, skew handling
⬜ Catalyst/Tungsten/shuffle — conceptual depth, Spark UI reading
⬜ Medallion architecture (Bronze/Silver/Gold) implementation on this dataset
**Interview outcome:** Debug a skewed join or explain a Spark UI stage graph live.

## Phase 5 — Data Warehousing & Modeling (~6–8 hrs)
⬜ Star schema design for this data (fact_trips, dim_driver, dim_truck, dim_route...)
⬜ SCD Type 1 & 2 (drivers/trucks change over time — real use case here)
⬜ Kimball vs Inmon, grain, surrogate keys
**Interview outcome:** Design a schema on a whiteboard and defend grain/SCD choices.

## Phase 6 — Orchestration, Idempotency & Monitoring (~4–6 hrs)
⬜ Step Functions design (conceptual + one real implementation), retries, DLQ
⬜ Idempotency, checkpointing, watermarking for late data
⬜ CloudWatch logging/alerting, SLA/SLO framing
**Interview outcome:** Answer "what happens when your pipeline fails at 2am" with a real, specific story.

## Phase 7 — Power BI Dashboard (~4–6 hrs)
⬜ Power Query, data modeling/relationships, core DAX
⬜ One polished dashboard on fleet KPIs (on-time %, cost per mile, maintenance spend)
**Interview outcome:** Walk through a dashboard you built and the DAX behind it.

## Phase 8 — Git, Testing, CI/CD, Interview Narrative (~6–8 hrs)
⬜ Branching/PR workflow, code review practice
⬜ GitHub Actions pipeline (lint + test on push)
⬜ Final documentation pass + STAR-format project narrative for interviews
**Interview outcome:** A GitHub repo + narrative you can walk any interviewer through end-to-end.

---
**Total: ~50–65 hrs.** We complete each phase's hands-on exercise and review before moving to the next — no skipping ahead.
