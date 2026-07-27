# FreightOps Analytics Platform

End-to-end data engineering project: a logistics/fleet analytics pipeline built on a
synthetic trucking dataset, designed and implemented following production-grade
practices (partitioned data lake, dimensional warehouse, orchestrated pipeline,
monitoring, and BI layer).

**Note:** This is a personal practice/learning project built on a synthetic dataset —
not real client or employer data. Architecture and engineering practices are designed
to production standards; data volume is intentionally scaled down for cost reasons
(see `docs/01-architecture/` for the full reasoning).

## Project Structure
```
docs/
  00-business/       → BRD, stakeholders, KPIs, requirements
  01-architecture/    → roadmap, architecture decisions, AWS tool mapping
  02-runbooks/        → operational runbooks, deployment guides (added in later phases)
sql/                  → SQL exercises and production queries by topic
src/
  ingestion/          → scripts that land data into Bronze
  transformation/     → Silver/Gold transformation logic (Python/PySpark)
  utils/              → shared helpers (logging, config, validation)
infra/                → Infrastructure-as-Code (Terraform, added in Phase 8)
tests/                → unit and data-quality tests
```

## Architecture
See `docs/01-architecture/roadmap.md` for the phased build plan and
`docs/01-architecture/7_layers_aws_tools_reference.md` for the full AWS tool mapping.

## Status
Currently in progress — see roadmap for phase-by-phase status.
