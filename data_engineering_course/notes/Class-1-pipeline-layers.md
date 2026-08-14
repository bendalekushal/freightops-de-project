╔══════════════════════════════════════════╗
║       CLASS 1 — PIPELINE LAYERS          ║
╚══════════════════════════════════════════╝


SOURCE
──────
Where data is generated / maintained.

Ex:
DB | API | CSV | IoT | Kafka


        ↓


INGESTION
─────────
How data MOVES from source
into our data platform.

Ex:
DMS | Glue | Kafka | Lambda


        ↓


BRONZE / RAW
─────────────
Keep source representation.

Why?
→ Audit
→ Replay
→ Backfill
→ Debug
→ Reprocess


        ↓


SILVER
──────
Make data technically CLEAN
and CONSISTENT.

→ Validate
→ Clean
→ Standardize
→ Deduplicate
→ Resolve data-quality issues


        ↓


GOLD
────
Make data BUSINESS READY.

→ KPIs
→ Metrics
→ Aggregations
→ Business rules


        ↓


SERVING
───────
Expose data to:

→ BI
→ Analysts
→ Applications
→ ML
→ Business