# Interview Prep Notes — Session 8 (Star Schema Design, Fact & Dimension Tables — Phase 5 Started)

## 1. Fact vs. Dimension — the real test, not just "big vs small"
- **Fact table** = an event, with numbers you'd actually sum up across many rows (revenue, miles, fuel used).
- **Dimension table** = descriptive context about a "thing" — attributes that don't get summed, just describe (a truck's make, a customer's name).
- **Real test for a number:** does it change every time (a fact, summable), or is it a fixed attribute of one thing (a dimension, not summable)? Example: `fuel_gallons_used` on a trip changes every trip → fact. `tank_capacity_gallons` on a truck → always the same for that truck → dimension attribute, not a fact, even though it's a number.
- **Row count is not the test.** A table can be small and still be a fact table, or large and still be a dimension. Caught myself almost using "large row count" as the test — it isn't.

## 2. Grain — what one row actually means
- Every fact table needs a clear grain: what does one single row represent? For `fact_trips`, one row = one trip.
- Tables with a different grain (like `maintenance_records`, one row = one service event) don't belong squashed into the same fact table — they're a separate fact table in their own right, at their own grain. Multiple fact tables side by side is normal, correct design, not messy.

## 3. Star vs. Snowflake — a real decision, tied back to the BRD
- `trips.csv` only has `driver_id`, `truck_id`, `trailer_id`, `load_id` — no `customer_id` or `route_id` directly. Those live in `loads`.
- **Snowflake option:** keep it as-is, join through `loads` every time you need customer/route info — matches raw structure exactly, but extra join every time.
- **Star option:** pull `customer_id` and `route_id` directly into `fact_trips` at build time — one join covers everything.
- **Decision: star**, chosen specifically because the BRD's actual KPIs (revenue per mile by customer, etc.) need customer and route info directly, and extra joins just make that harder for no benefit here.

## 4. SCD Type 1 vs Type 2 — plain explanation
- **Type 1:** overwrite in place, no history. Use for corrections/mistakes — e.g., a customer's misspelled name being fixed. Nobody needs to know the wrong version ever existed.
- **Type 2:** keep the old row, add a new one. Use for real events that actually happened at a point in time — e.g., a driver's home terminal changing.
- **The real test:** would you ever need to answer "what was true back then," or do you only ever care about "what's true right now"? If only "right now" matters, Type 1. If history matters, Type 2.
- Applied the test to `dim_customer`, `dim_route`, `dim_trailer` — none had a real recurring "event" the way driver/truck attributes did, so all three stay simple (no SCD tracking), a deliberate decision, not a shortcut.

## 5. Built Today
- **`fact_trips`**: joined Silver `trips` + `loads` on `load_id`, explicitly `.select()`'d only the agreed-on columns (not just keeping everything from the join by default — a deliberate design choice). Verified row count matched `trips` exactly (85,410) — confirming no rows lost or duplicated, consistent with the known 1:1 relationship between trips and loads from Phase 0.
- **`dim_customer`, `dim_route`, `dim_trailer`**: simple pass-through from Silver to Gold, using the same loop pattern as the Phase 4 passthrough script. Verified row counts matched known totals (200 / 58 / 180).

## 6. Real Mistakes Caught This Session
- First attempt at the remaining-dimensions script tried to read Delta tables using `format("parquet")` with a `.parquet` path suffix — wrong; Delta tables are read with `format("delta")` and no file extension in the path, since Delta stores its own folder structure with a `_delta_log`, not a single parquet file.
- Used plural naming (`dim_customers`, `dim_routes`, `dim_trailers`) inconsistent with the already-existing `dim_driver` and `dim_truck` — caught and corrected to keep naming consistent across the whole schema, since an inconsistent naming pattern is exactly the kind of thing a reviewer or interviewer would notice.
- Noted (not a bug): `.option("header")` and `.option("inferSchema")` are CSV-only options and are silently ignored when reading Delta format, since Delta already stores its own schema internally.

## Star Schema — Now Complete
- 1 fact table: `fact_trips`
- 5 dimensions: `dim_driver`, `dim_truck` (both full SCD Type 2), `dim_customer`, `dim_route`, `dim_trailer` (all simple, decision justified via the Type 1/2 test)

**Next: loading this into Redshift.**