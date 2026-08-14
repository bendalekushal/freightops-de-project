# Interview Prep Notes — Session 7 (Trucks SCD Type 2, Caching, Spark UI — Phase 4 Complete)

## 1. SCD Type 2 for Trucks — built independently, same pattern as Drivers
- Applied the exact same two-file pattern from `dim_driver` to `dim_truck`, with very little guidance needed this time — good sign the concept actually stuck, not just followed along.
- Tracked field: `status` (Active/Maintenance) — a real business-driven change, same category as `home_terminal` on drivers.
- **Real catch during review, not a bug but a good habit:** test data used lowercase `"maintenance"` while the real column used `"Maintenance"`. Didn't break the logic (still correctly registered as a change), but flagged as a reminder — sloppy test data with inconsistent casing can hide the exact kind of real-world data-quality issue this project is supposed to be practicing catching.
- Verified result: `TRK00001` correctly produced two rows — old (`Active`, `is_current: false`, closed out today) and new (`Maintenance`, `is_current: true`, empty end date) — same shape as the drivers result, confirmed independently.

## 2. Caching
- `.cache()` tells Spark to keep a DataFrame's result in memory after first computing it, instead of recalculating it from scratch every time it's reused.
- **Real rule:** only cache something you'll actually use more than once. Caching something used only once wastes memory for no benefit — caching isn't automatically "faster," it's a tradeoff.
- Applied to `joined_df` in `gold_revenue_per_mile.py`, reused for two different aggregations: revenue-per-mile (`result_df`) and average distance per customer (`avg_df`).
- Small good habit applied on our own: `.avg('actual_distance_miles')` produces an awkward auto-named column (`avg(actual_distance_miles)`), renamed cleanly with `.withColumnRenamed(...)`.

## 3. Reading the Spark UI
- Available while a script is actively running, at `http://localhost:4040` — closes once `spark.stop()` runs. Used `input("Press Enter...")` to pause a script long enough to view it live.
- **Jobs tab:**
  - Saw an actual `broadcast exchange` job — real, direct proof the broadcast join genuinely happened, not just assumed from the code. Without `F.broadcast(...)`, this would instead show a heavier "shuffle exchange" step.
  - Saw tasks marked "skipped" (e.g., "1/1 (2 skipped)") on later jobs — this is caching visible in action: Spark recognized it already computed that result and reused it instead of redoing the join.
- **SQL/DataFrame tab:** lists every actual query run, including Delta's own "filtering files for query" bookkeeping steps (Delta checking its transaction log to know which physical files it needs).
- **Real, practical use:** this is the actual tool to check *why* something is slow in production — confirm a broadcast really happened, check which stages got skipped vs. fully recomputed, see real per-stage timing — instead of guessing.

## Phase 4 — Now Fully Complete
- Silver layer: all 14 tables, 2 real date-type fixes, 2 real missing-ID flags, all verified.
- PySpark joins with broadcast, verified against an earlier SQL result (Phase 1) — same answer, two tools.
- Partitioning and skew: created real skew on purpose, fixed it with salting, understood the hash/remainder mechanism underneath.
- SCD Type 2: built twice (drivers, then trucks independently) using Delta MERGE in two separate passes — close-out then insert.
- Caching and the Spark UI: used correctly, and confirmed with visual, direct evidence rather than just trusting the code ran without error.

**Next: Phase 5 — Redshift, star schema, and the rest of the Gold layer.**