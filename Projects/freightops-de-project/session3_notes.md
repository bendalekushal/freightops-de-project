# Interview Prep Notes — Session 3 (PySpark + Delta Lake Setup, Silver Layer)

## 1. Why PySpark Needs What It Needs (the full chain, Windows-specific)
- PySpark is a Python wrapper around Spark, which runs on the **JVM** — no Java, no Spark, regardless of Python code.
- On Windows specifically, Spark also needs **Hadoop's Windows compatibility layer** (`winutils.exe` + `hadoop.dll`) — Linux/Mac don't need this; it's a Windows-only requirement worth naming as such in an interview.
- `hadoop.dll` needs to be discoverable in **two places**: on PATH (`HADOOP_HOME`) *and* copied into `C:\Windows\System32` — Windows' native file-permission checks specifically look in System32, not just PATH.
- **`PYSPARK_PYTHON` / `PYSPARK_DRIVER_PYTHON`** must be set explicitly — otherwise Spark can launch a non-functional Python stub (e.g., the Microsoft Store placeholder) instead of your real environment's Python, causing a silent worker-connection failure.
- **Interview line:** *"On Windows, PySpark needs Java, a Hadoop-Windows compatibility shim, and an explicit Python path — none of which are needed on Linux/Mac. I hit and resolved all of these directly."*

## 2. Delta Lake Setup
- Delta isn't automatically known to Spark — must configure it explicitly via `configure_spark_with_delta_pip(builder)` plus two `.config(...)` calls (`spark.sql.extensions`, `spark.sql.catalog.spark_catalog`) *before* `.getOrCreate()`. Skipping this gives `Failed to find the data source: delta`.
- Mixing `conda install` and `pip install` in one environment is fine when installing genuinely new, independent packages (like we did with PySpark via conda, Delta via pip) — the real risk is only when both try to manage versions of *the same* package.

## 3. PySpark Fundamentals (first real hands-on today)
- `SparkSession.builder...getOrCreate()` — the mandatory entry point; nothing runs without it.
- **DataFrame** = Spark's version of a SQL table — rows + named columns, distributed under the hood.
- `spark.read.format("csv").option("header","true").option("inferSchema","true").load(...)` — reading data; `inferSchema` behaves like the Glue Crawler (can misjudge ambiguous formats, e.g. non-ISO dates as strings).
- **`to_date(col("x"), "dd-MM-yyyy")`** — Spark's equivalent of Pandas' `to_datetime()`, but requires an **explicit format string** (Spark won't guess) — a deliberate safety choice for large-scale automated pipelines. Common gotcha: capital `MM` = month, lowercase `mm` = minutes.
- **`withColumn("x", ...)`** — adds or replaces a column.
- **`when(condition, value).otherwise(other)`** — Spark's equivalent of SQL's `CASE WHEN` (directly reusable knowledge from Phase 1 SQL work).
- `.write.format("delta").mode("overwrite").save(path)` — writes a Delta table (creates a `_delta_log` folder + Parquet data files — verified both exist after writing, not just assumed).
- **Real, verified result today:** `contract_start_date` confirmed flipped from `string` → `date` via `printSchema()` before/after — proof, not assumption.

## 4. Data Quality Decision: Missing IDs — Flag, Don't Exclude
- Reasoning: a trip missing `driver_id` may still have valid `distance`/`fuel` data usable for other purposes (e.g., total fleet mileage) — dropping the whole row destroys still-usable information.
- Exclude only if a row is *entirely* null across the board (a different, more extreme case).
- **Flag at the column level** (`driver_id_missing`, `truck_id_missing`, `trailer_id_missing` — separate booleans), not one combined flag — since we proved most missing IDs are independent (only 114 of 4,952 affected rows had 2+ missing together). A single combined flag would force analysts to over-exclude data irrelevant to their specific question.
- **Interview line:** *"I flag data-quality issues at the column level, not with one blanket flag, because different downstream analyses have different tolerance for what's usable — collapsing that loses precision."*

## 5. Real Debugging Habits Reinforced Again
- A schema/type change is only *proven* by checking before/after (`printSchema()`), not by assuming a transformation worked because it didn't error.
- Errors that appear **after** your actual expected output has already printed correctly are often harmless cleanup/shutdown noise (confirmed today: Spark's temp-file deletion failing due to a Windows file-lock quirk) — not a real failure. Always check *where* in the output an error appears relative to your expected results.