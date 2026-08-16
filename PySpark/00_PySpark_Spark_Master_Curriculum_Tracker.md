# PySpark / Apache Spark Bootcamp — Master Curriculum Tracker

**Last updated:** 15 August 2026  
**Current topic:** `orderBy()` → global sorting → `sortWithinPartitions()`  
**Environment:** PySpark 3.4.1 | Python 3.11.15 | Java 11  
**Project:** JobPulse AI / DataEngineer-Bootcamp

## Teaching Pattern

For every new topic:

```text
Concept → Beginner explanation → Deep technical explanation
→ Example → Interview perspective → Practical
→ User writes/runs code → Review output + physical plan
→ Quiz → Notes → Next topic
```

Rules:
- Concise revision for topics already known.
- Deep, beginner-friendly teaching for new/weak topics.
- Keep connecting API → logical plan → Catalyst → physical plan → partitions → tasks → shuffle.
- Prefer built-in Spark functions over UDFs when possible.
- Use JobPulse AI / realistic Data Engineering examples.
- Create professional Markdown notes after meaningful sessions.
- Do NOT mark performance optimization as completed merely because related concepts appeared in plans.

---

# 1. COMPLETED

## Spark Foundations
- Spark introduction and distributed computing
- Cluster, node, worker-node concepts
- Driver program
- Cluster manager
- Executors
- Tasks
- SparkSession
- SparkContext relationship
- Partitions
- Input splits
- Jobs, stages and tasks
- Lazy evaluation
- Lineage / DAG
- Narrow vs wide transformations

Core model:

```text
Action → Job → Stages → Tasks → Executors
```

## DataFrames / Data Sources
- DataFrame fundamentals
- DataFrame immutability
- `spark.read`
- CSV reading
- Parquet
- Headers
- `inferSchema`
- Explicit schemas
- `StructType`
- `StructField`
- Nullability
- Basic Spark data types
- `show()`
- `printSchema()`
- `dtypes`

## Execution Plans
- `explain()`
- `explain("formatted")`
- Logical vs physical plans
- `Scan ExistingRDD`
- `Scan parquet`
- `Project`
- `Filter`
- `Exchange`
- `HashAggregate`
- Basic `AdaptiveSparkPlan` awareness
- Reading physical-plan output

## DataFrame Transformations
- `select()`
- `filter()`
- `where()`
- `withColumn()`
- `when()`
- `otherwise()`
- `lit()`
- Type casting
- `groupBy()`
- `agg()`
- `count()`
- `sum()`
- `avg()`
- `min()`
- `max()`
- `dropDuplicates()`
- `distinct()`
- Basic `drop()`

## File / Scan Optimizations
- Column pruning
- Predicate pushdown
- Reading `PushedFilters`
- Reading `ReadSchema`

Mental model:

```text
select() → column pruning → fewer columns read

filter() → predicate pushdown when supported
```

## NULL Handling
- `isNull()`
- `isNotNull()`
- `fillna()`
- `dropna()`
- `coalesce()`
- NULL vs 0 / empty string / False
- Three-valued logic: TRUE / FALSE / UNKNOWN
- NULL comparison behavior in `filter()`
- `when()` / `otherwise()` with NULL

## String Functions
- `trim()`
- `lower()`
- `upper()`
- `initcap()`
- `length()`
- `split()`
- `concat()`
- `regexp_replace()`

## Date / Timestamp Functions
- Date vs timestamp
- `to_date()`
- `to_timestamp()`
- `datediff()`
- `date_add()`
- `date_sub()`
- `year()`
- `month()`
- Date typing vs strings

## Deduplication / Shuffle
- `distinct()` as a transformation
- Complete-row deduplication
- `dropDuplicates()` with keys
- Why deduplication requires redistribution
- `Exchange`
- Hash partitioning
- Partial/local aggregation
- Final/global aggregation
- Why `distinct()` appears as `HashAggregate`
- Why `dropDuplicates(["company"])` can show `first()`
- Why duplicate selection should not be assumed deterministic

---

# 2. PARTIALLY COVERED / NEEDS DEEPER PRACTICE

## Aggregations
Covered:
- `groupBy`
- `count`
- `sum`
- `avg`
- `min`
- `max`

Still needed:
- Multiple aggregations
- Conditional aggregations
- Aliases
- Physical plan analysis
- Partial/final aggregation
- Shuffle analysis

## Joins
Previously introduced:
- Join types
- Join behavior
- Broadcast joins

Still needed deeply:
- Inner / left / right / full
- Left semi / left anti
- Join keys
- Duplicate columns
- NULL join behavior
- Join cardinality
- Broadcast hash join
- Sort-merge join
- Join strategy selection
- Physical-plan comparison

## Window Functions
Basic window concepts introduced.

Still needed:
- `partitionBy()`
- `orderBy()`
- `row_number()`
- `rank()`
- `dense_rank()`
- `lag()`
- `lead()`
- Top-N per group
- Latest record per key
- Deterministic deduplication
- Running totals
- Moving averages
- Window physical plans

## `repartition()` / `coalesce()`
Previously introduced.

Need deeper practical coverage:
- Full shuffle
- Increasing/decreasing partitions
- Hash partitioning
- Key-based repartitioning
- Reducing partitions with `coalesce()`
- When each is appropriate

## Caching / Persistence
Covered:
- `cache()`
- `persist()`
- `unpersist()`
- Lazy materialization

Still needed:
- Storage levels
- `MEMORY_ONLY`
- `MEMORY_AND_DISK`
- `DISK_ONLY`
- Cache eviction / memory pressure
- When NOT to cache

## UDFs
Basic concepts introduced.

Still needed:
- Python UDFs
- Return types
- Python/JVM boundary
- Serialization overhead
- Why UDFs can be slower
- Built-in alternatives
- Pandas UDFs
- Arrow
- When Pandas UDFs are appropriate

## Spark SQL
Basic SQL concepts introduced.

Still needed:
- Temp views
- `createOrReplaceTempView()`
- `spark.sql()`
- SQL vs DataFrame API
- Logical-plan equivalence
- Mixing SQL and DataFrame API

## Spark UI / Debugging
Basic plan reading introduced.

Still needed:
- Jobs tab
- Stages tab
- SQL tab
- Executors tab
- Storage tab
- Task distribution
- Shuffle read/write
- Input/output
- Identifying bottlenecks

## Checkpointing
Previously introduced.

Need deeper:
- `checkpoint()`
- `localCheckpoint()`
- Lineage truncation
- Reliability differences
- Long lineage
- Streaming use cases

## Structured Streaming
Basic concepts introduced:
- Streaming DataFrames
- Output modes
- Watermarks

Still needed deeply:
- `readStream`
- `writeStream`
- Triggers
- Micro-batch execution
- Streaming checkpoints
- Query lifecycle
- Append / update / complete
- Event time
- Late data
- State cleanup
- Tumbling / sliding / session windows
- Stream-static joins
- Stream-stream joins

---

# 3. CURRENT / NEXT

## `orderBy()` — CURRENT

This is the immediate next topic.

Need to cover:
- Global sorting
- Why `orderBy()` is wide
- Why global sorting requires redistribution
- `Exchange`
- Range partitioning
- Sort operators
- Physical-plan interpretation

Practical:

```python
df.orderBy(F.col("salary").desc())
```

Expected learning:

```text
Input partitions
      ↓
Exchange / redistribution
      ↓
Global sorting
      ↓
Sorted result
```

## `sortWithinPartitions()` — NEXT

Critical comparison:

```text
orderBy()
→ global ordering

sortWithinPartitions()
→ ordering only inside each partition
```

We will implement both and compare their physical plans and behavior.

---

# 4. UPCOMING CORE CURRICULUM

After sorting:

1. `drop()` deeper practical
2. Aggregations deep dive
3. Join deep dive
4. `union()` / `unionByName()` reinforcement
5. Advanced Window Functions
6. `repartition()` vs `coalesce()`
7. UDFs
8. Pandas UDFs / Arrow
9. Spark SQL
10. Spark UI / debugging
11. Checkpointing
12. Structured Streaming deep dive
13. Production Spark concepts

---

# 5. SPARK PERFORMANCE OPTIMIZATION — NOT YET COVERED

**Important: this section is NOT complete.**

These topics must be taught properly later and must not be marked complete just because they appeared incidentally in physical plans.

## Shuffle Optimization
- Shuffle mechanics
- Shuffle read/write
- Network I/O
- Disk I/O
- Spill
- Shuffle partition sizing

## `spark.sql.shuffle.partitions`
Must explicitly cover:
- What it controls
- Default behavior
- Too many partitions
- Too few partitions
- Choosing a sensible value
- Impact on shuffle

## AQE — Adaptive Query Execution
Must explicitly cover:
- Runtime statistics
- Coalescing post-shuffle partitions
- Skew join optimization
- Dynamic partition adjustments

## Data Skew
- Hot keys
- Symptoms
- Detection
- Salting
- Broadcast alternatives
- AQE skew handling

## Partition Optimization
- Partition sizing
- Small-file problem
- Too many / too few partitions
- Output partition count
- Parallelism

## Join Optimization
- Broadcast strategy
- Sort-merge strategy
- Join order
- Filter before join
- Column pruning before join
- Avoiding unnecessary shuffle

## Cache Optimization
- When to cache
- When not to cache
- Storage levels
- Memory pressure
- Unpersisting

## File Optimization
- Small files
- Parquet
- Compression
- Partitioned output
- File sizing

## Code Optimization
- Built-in functions vs UDFs
- Avoiding unnecessary transformations
- Avoiding repeated scans
- Avoiding repeated actions
- Avoiding unnecessary `collect()`

---

# 6. PRODUCTION SPARK TOPICS — UPCOMING

- Data-quality validation
- Schema validation
- Bad-record handling
- `PERMISSIVE`
- `DROPMALFORMED`
- `FAILFAST`
- Error handling
- Logging
- Spark configuration
- Driver memory
- Executor memory
- Executor cores
- Resource allocation
- Serialization
- Python/JVM boundary
- Arrow
- Production failure scenarios
- Monitoring

Important configurations to cover later:

```text
spark.sql.shuffle.partitions
spark.sql.adaptive.enabled
spark.sql.autoBroadcastJoinThreshold
spark.executor.memory
spark.executor.cores
spark.driver.memory
```

---

# 7. JOBPULSE AI PROJECT APPLICATION

The eventual project progression should be:

```text
Raw job data
     ↓
Schema validation
     ↓
Data cleaning
     ↓
NULL handling
     ↓
String normalization
     ↓
Date/timestamp parsing
     ↓
Deduplication
     ↓
Filtering / projections
     ↓
Joins
     ↓
Aggregations
     ↓
Window functions
     ↓
Data quality
     ↓
Performance optimization
     ↓
Analytics-ready datasets
```

Project implementation should reinforce Spark concepts rather than replace the theory.

---

# 8. MASTER SPARK MENTAL MODEL

```text
SOURCE DATA
    ↓
DataFrameReader
    ↓
Schema
    ↓
DataFrame API
    ↓
Transformations
    ↓
Logical Plan
    ↓
Catalyst Optimizer
    ↓
Optimized Logical Plan
    ↓
Physical Planning
    ↓
Physical Plan
    ↓
Partitions
    ↓
Narrow / Wide Dependencies
    ↓
Exchange / Shuffle where required
    ↓
Stages
    ↓
Tasks
    ↓
Executors
    ↓
Result
```

Performance thinking:

```text
Data volume
    ↓
Partitions
    ↓
Parallelism
    ↓
Shuffle
    ↓
Network / Disk / Memory
    ↓
Execution time
```

---

# 9. COMPLETION STANDARD

A topic should be marked **Completed** only when I can:

1. Explain it in my own words.
2. Write basic PySpark code without copying.
3. Predict its broad execution behavior.
4. Read the relevant physical-plan operator.
5. Explain shuffle behavior when relevant.
6. Answer basic interview questions.
7. Apply it to a realistic Data Engineering scenario.

A topic that was only introduced should remain **Partially Covered**, not Completed.

---

# 10. NEW-CHAT HANDOFF PROMPT

Copy this into a new chat:

> Continue my PySpark / Apache Spark Data Engineering Bootcamp using my Master Curriculum Tracker.
>
> Current topic: `orderBy()` → global sorting → `sortWithinPartitions()`.
>
> Follow the established pattern:
> concept → beginner explanation → deep technical explanation → example → interview perspective → practical coding → I run the code → review my output/physical plan → quiz → next topic.
>
> Do not repeat mastered topics deeply. Go deep on new/weak topics.
>
> Keep practical work inside my existing `freightops` / `DataEngineer-Bootcamp` project and create Markdown notes at meaningful session boundaries.
>
> Important: Spark Performance Optimization has NOT been formally covered yet. Do not mark AQE, `spark.sql.shuffle.partitions`, data skew, shuffle tuning, partition sizing, or related optimization topics as completed just because they appeared in physical-plan explanations.
>
> Immediate next exercise: `orderBy()` and its physical plan, followed by `sortWithinPartitions()` and a practical comparison.
