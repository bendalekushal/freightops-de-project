# Interview Prep Notes — Session 1 (Business Understanding, SQL, AWS Foundations)

## 1. Business Understanding / BRD
- Stakeholder = someone who makes a real decision from the data (not "everyone")
- KPI = must trace back to actual columns you can compute — if you can't point to the columns, it's not a KPI yet
- **Root cause analysis method:** check if an issue correlates with year/status/type/etc. If it matches the overall dataset's proportions everywhere you check → **MCAR (Missing Completely At Random)** → likely an upstream system issue, not a business-process one. Know when to say "escalate to source logs" instead of over-analyzing the same table.
- **Interview line:** *"I don't just report a data-quality issue — I check whether it correlates with other variables before deciding if it's a process problem or a system problem."*

## 2. SQL — Mistakes I Made & the Real Lesson
| Mistake | Lesson |
|---|---|
| Trusted `head()`/eyeballing rows for nulls — said "no nulls" when there were ~2% | **Aggregate, never eyeball.** Use `.isnull().mean()` or `COUNT(*) - COUNT(col)`. A clean sample tells you nothing about a large dataset. |
| `PARTITION BY driver_id` when I needed to rank drivers against each other | `PARTITION BY` = "what should this row be compared against?" — ask that out loud before writing it. Wrong partition = technically running, wrong answer. |
| Recursive CTE: `WHERE the_date <= '2023-01-31'` generated 32 days, not 31 | **Off-by-one rule:** the WHERE check happens on the row you already have, before producing the next one. Use `<` not `<=` to stop exactly at your target. |
| `CROSS JOIN` instead of `LEFT JOIN` when looking for missing/idle records | Cross join = every combination, no relationship. For "find what's missing," use `LEFT JOIN` + check `IS NULL` on the right table. |
| Truck filter in `WHERE` instead of the `JOIN ... ON` (on a LEFT JOIN) | For INNER JOIN, `ON` vs `WHERE` placement gives the same result. For **LEFT JOIN it changes the result** — filtering the right table in `WHERE` silently drops your "no match" rows, which defeats the purpose. |
| Selected a joined-table column (`truck_id`) expecting a value on unmatched rows | On a LEFT JOIN, **every column from the unmatched side is NULL**, not just the join key. If you already know the value, select it as a literal instead. |

## 3. SQL — Portable vs Dialect-Specific
- **Portable everywhere:** joins, window functions (`RANK`, `DENSE_RANK`, `ROW_NUMBER`, `SUM() OVER`), CTEs, `GROUP BY`
- **Dialect-specific — always name the DB when discussing:**
  - Get year from date: MySQL `YEAR(col)` · Postgres/Redshift `EXTRACT(YEAR FROM col)` · SQLite `strftime('%Y', col)`
  - Filter on a window function result: subquery/CTE wrapper (works everywhere) vs `QUALIFY` (Postgres/Redshift only, not MySQL/SQLite)
- **Why window functions ≠ GROUP BY:** GROUP BY collapses rows; window functions keep every row and attach a calculated value.
- **Verifying a join is correct (interview-strong answer):** row-count check before/after, duplicate-key check (`GROUP BY key HAVING COUNT(*)>1`), compare aggregate totals before/after the join — not just "the output looked right."

## 4. SQL & Data at Scale (a common follow-up question)
- Logic doesn't change at billions of rows — execution does: partition by date so filters skip unread data; pre-aggregate into summary/Gold tables instead of live-scanning raw data; use approximate counts (`approx_count_distinct`) for cheap sanity checks at scale.
- **Interview line:** *"I validated logic on a sample; in production this becomes a scheduled job producing partitioned, pre-aggregated tables, with row-count/duplicate checks built in."*

## 5. AWS Foundations
- **Never use root day-to-day** — create a least-privilege IAM user, MFA on both root and the IAM user.
- **S3 production basics:** block public access explicitly (don't rely on defaults), enable default encryption (SSE-AES256), tag every resource (project/environment/owner) for cost tracking.
- **Build infra via CLI/script, not console clicks** — repeatable, reviewable, no undocumented history.
- **7-layer mental model:** Ingestion → Storage → Processing/Transformation → Orchestration → Warehousing/Modeling → Serving/BI → Monitoring & Security (this last one wraps around all the others, it's not a final step).
- **Bronze/Silver/Gold:** Bronze = raw, unmodified, kept forever for reprocessing. Silver = cleaned/standardized. Gold = business-shaped (star schema, pre-aggregated) — dashboards should query Gold, never raw Bronze.
- **Free tier ≠ real production volume** — know the difference and say so honestly rather than overclaiming scale you didn't actually run.

## 6. Python / boto3 (Ingestion)
- `boto3` = AWS's Python SDK — the bridge between your code and AWS services (no console clicking).
- **Idempotency pattern:** check if data already exists (`list_objects_v2`) before uploading (`upload_file`) — re-running a job should never duplicate/corrupt data. This is the single most reusable production pattern from today.
- **Interview line:** *"My ingestion checks for existing data at the target path before writing, so retries or scheduler misfires don't create duplicates."*
- You do **not** need to memorize exact syntax — you need to be able to explain the pattern and why it matters. Method names are always look-up-able; the reasoning isn't.

## 7. General Engineering Habits (say these in interviews, not just do them)
- Verify, don't trust: row counts, duplicate checks, output counts vs. expected counts — every time, not just when something looks wrong.
- Know the difference between "it ran without crashing" and "it did what I expected" — check actual output, not just exit codes.
- Real infra is scripted/repeatable, not manually clicked — same reasoning applies to ingestion, S3 setup, and (later) IaC.