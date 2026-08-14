# Interview Prep Notes — Sessions 4 & 5 Combined (Silver Completed, PySpark Joins)

## From Session 4 (short session)
- Standing practices locked in: plain language everywhere, explain each hands-on step as it happens, end-of-session interview questions.
- `silver_trips.py` built and verified: driver/truck/trailer missing-ID flags, counts matched Phase 0 (1714/1672/1680).
- Real mistake caught: first attempt used a wrong column (`customer_id`, which doesn't exist in `trips.csv`) instead of `trailer_id` — caught by checking the real file instead of trusting memory.
- Delta overwrite doesn't delete old files right away — it just updates the table's pointer to the new version. Cleanup is a separate step (`VACUUM`), not covered in depth yet.
- Log noise: `setLogLevel("ERROR")` helps but doesn't remove everything (ivy/jar messages happen before Spark starts; Windows shutdown errors are a separate OS-level thing). Practical fix for now: redirect output to a file and search it.
- Found 10 tables with date-like columns needing a check.

## From Session 5 (today)

### Date audit — closed out
- Wrote one script (`check_date_schemas.py`) to check 8 tables' schemas at once, using a Python dictionary + for loop, instead of writing 8 separate scripts.
- Result: only 2 of 14 tables actually had a real date problem — `customers.contract_start_date` and `trucks.acquisition_date`. The other 8 were already fine, because their raw dates were in standard `YYYY-MM-DD` format.
- **Real lesson:** the problem was never "dates are hard" — it's specifically non-standard formats. Spark parses standard formats correctly on its own.
- Fixed `trucks.acquisition_date` the same way as `customers` — checked the real raw value first (`27-04-2017`) before assuming the format, confirmed `dd-MM-yyyy` was correct, applied `to_date()`, verified with before/after schema and real output values.

### Missing-ID flag — closed out
- Found (from session 1 notes) that `fuel_purchases.driver_id` also had ~2% missing, same as `trips`. Built `silver_fuel_purchases.py` using the same `when().otherwise()` pattern. Verified: 3,988 missing out of ~196,000 rows, matching the known 2.03%.

### All 14 tables passed through to Silver
- Realized partway through that only 4 of 14 tables had actually been written to Silver — the rest were only schema-checked, never written.
- Wrote the remaining 10 in one script using a loop (same dictionary + for-loop pattern as the schema check), instead of repeating near-identical code 10 times.
- Verified all 14 folders exist under `data/silver/` with real row counts matching known totals (loads: 85410, delivery_events: 170820, etc.).
- **Real lesson:** it's easy to feel "almost done" after fixing the two interesting bugs and forget the plain, repetitive table-by-table work still has to happen. Both kinds of work count.

### PySpark Joins — new topic, first real attempt
- `df1.join(df2, on="key", how="inner")` — same idea as SQL join, matching rows on a shared column.
- **Broadcast join:** `F.broadcast(small_df)` — used when one side of a join is small enough to fit in memory (our case: `customers` at 200 rows vs `loads`/`trips` at 85,000+). Spark skips shuffling data across machines and just copies the small table everywhere instead. Real, correct use here — not "always broadcast," but "broadcast because the size gap actually justified it."
- `groupBy("col").agg(F.sum("col").alias("name"))` — same as SQL's `GROUP BY` + `SUM(...) AS name`.
- Using `from pyspark.sql import functions as F` and calling `F.sum(...)`, `F.col(...)` avoids accidentally overwriting Python's built-in `sum()` function — a real, common gotcha avoided by good habit.
- **Verified result matched Phase 1's SQL answer exactly** — same top customer (CUST00123), same revenue, same miles, same per-mile figure (2.21) — same question, same answer, two different tools. Real proof the join logic is correct.
- Floating-point display quirk noticed and fixed: `1390786.8100000003` is normal decimal rounding behavior in Spark (and most languages) when summing many decimals — not a bug. Fixed by wrapping in `F.round(...)`, same as was already done for the per-mile figure.

## Real Habits Reinforced Again
- Check the actual file/column before assuming a name or format — caught two real mistakes this way across both sessions.
- Verify a fix with before/after evidence (schema, row counts, matching known numbers) — every single fix today was confirmed this way, not assumed.
- When the same operation needs to run across many similar files, write one loop instead of many near-identical scripts.