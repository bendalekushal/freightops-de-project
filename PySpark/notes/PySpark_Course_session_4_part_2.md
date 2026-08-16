# PySpark Data Engineering Bootcamp — Session 4 Master Notes

## Session Status

**Session:** 4  
**Current stopping point:** `groupBy()` physical execution plan  
**Next topic:** `groupBy() + agg()`  
**Practical files completed/planned:**
- `04_orderBy_global_sorting.py`
- `05_sortWithinPartitions.py`
- `06_repartition.py`
- `07_coalesce.py`

---

## 1. Session Scope

This continuation started from `orderBy()` and global sorting.

Covered in this section:

1. `orderBy()` and global sorting
2. `Exchange` and range partitioning
3. `sortWithinPartitions()`
4. `repartition()`
5. `repartition(n, column)`
6. `coalesce()`
7. `groupBy()` execution and shuffle behavior

The Spark Performance Optimization section is **not yet covered**. Topics such as AQE, shuffle partition tuning, partition sizing, and skew optimization are only referenced here and will be taught later.

---

# 2. `orderBy()` — Global Sorting

## Concept

```python
df.orderBy("salary")
```

or:

```python
df.orderBy(F.col("salary").desc())
```

`orderBy()` establishes a **global ordering** of the DataFrame.

Because records can initially exist in different partitions, Spark cannot simply sort every partition independently and claim that the complete DataFrame is globally sorted.

## Why is `orderBy()` wide?

Global sorting can require records to be redistributed between partitions.

Mental model:

```text
orderBy()
   ↓
Global ordering required
   ↓
Redistribution
   ↓
Exchange
   ↓
Shuffle
   ↓
Sort
```

Therefore, `orderBy()` is a **wide transformation**.

## Practical physical plan

The actual plan observed during the practical was:

```text
AdaptiveSparkPlan
+- Sort
   +- Exchange
      +- Scan ExistingRDD
```

The important `Exchange` argument was:

```text
rangepartitioning(salary DESC NULLS LAST, 200)
```

The key lesson is that Spark uses range partitioning for the global ordering requirement.

## Important distinction

Global sorting does not mean Spark must put the complete dataset into one partition.

Instead, data can be distributed into ordered ranges across partitions.

Conceptually:

```text
Highest values
     ↓
Partition 1

Middle values
     ↓
Partition 2

Lowest values
     ↓
Partition 3
```

The partitions themselves have an ordering relationship.

---

# 3. `sortWithinPartitions()`

## Concept

```python
df.sortWithinPartitions(
    F.col("salary").desc()
)
```

`sortWithinPartitions()` sorts records **inside each existing partition**.

It does not establish global ordering.

## Global vs local sorting

```text
orderBy()
    ↓
Global sorting
    ↓
Exchange / redistribution
    ↓
Sort
```

```text
sortWithinPartitions()
    ↓
Use existing partitions
    ↓
Sort each partition independently
```

## Physical plan observed

For the initial `sortWithinPartitions()` practical, the physical plan was:

```text
Sort
+- Scan ExistingRDD
```

There was no `Exchange` caused by the sort operation itself.

## Important practical refinement

We then explicitly performed:

```python
df = df.repartition(2)
```

before:

```python
df.sortWithinPartitions(
    F.col("salary").desc()
)
```

The resulting plan contained:

```text
Scan ExistingRDD
   ↓
Exchange
   ↓
RoundRobinPartitioning(2)
   ↓
Sort
```

The `Exchange` came from `repartition(2)`, **not** from `sortWithinPartitions()`.

## Mental model

```text
sortWithinPartitions()
    ↓
Local / partition-level ordering
    ↓
No global ordering guarantee
```

A DataFrame can therefore have individually sorted partitions while the complete DataFrame is not globally sorted.

---

# 4. `repartition()`

## Concept

```python
df.repartition(2)
```

asks Spark to redistribute the DataFrame into 2 partitions.

If the original DataFrame has 12 partitions:

```text
12 partitions
      ↓
repartition(2)
      ↓
2 partitions
```

## Why does `repartition()` cause an Exchange?

Spark must physically redistribute records to create the requested partition layout.

Therefore:

```text
repartition()
    ↓
Redistribution
    ↓
Exchange
    ↓
Shuffle
```

`repartition()` is a **wide transformation**.

## Number-based repartitioning

For:

```python
df.repartition(2)
```

the physical plan showed:

```text
Exchange
Arguments:
RoundRobinPartitioning(2), REPARTITION_BY_NUM
```

### Meaning

- `2` = number of output partitions
- `RoundRobinPartitioning` = records are distributed across the requested partitions in a round-robin style
- `REPARTITION_BY_NUM` = the repartition request was based on an explicit partition count

---

# 5. `repartition(n, column)`

We then tested:

```python
df.repartition(
    2,
    "department"
)
```

The physical plan showed:

```text
Exchange
Arguments:
hashpartitioning(department, 2), REPARTITION_BY_NUM
```

## Meaning

```text
2
↓
Number of output partitions

department
↓
Partitioning expression used to distribute records
```

This is different from:

```python
df.repartition(2)
```

which produced:

```text
RoundRobinPartitioning(2)
```

The key-based version uses hash partitioning on the specified expression.

## Important warning

Do not assume:

```text
IT → Partition 1
HR → Partition 2
```

The actual partition assignment is determined by Spark's hash-partitioning mechanism. The important guarantee is that records are distributed according to the partitioning expression.

---

# 6. `coalesce()`

## Concept

```python
df.coalesce(2)
```

is primarily used to reduce the number of partitions without a full shuffle.

If the DataFrame has 12 partitions:

```text
12 partitions
      ↓
coalesce(2)
      ↓
2 partitions
```

## Physical plan observed

The actual plan was:

```text
Coalesce
+- Scan ExistingRDD
```

There was no `Exchange`.

This directly contrasted with:

```python
df.repartition(2)
```

which produced an `Exchange`.

## Why can `coalesce()` avoid a full shuffle?

Conceptually, Spark can combine existing partition dependencies into fewer partitions rather than fully redistributing every record.

```text
Existing partitions
       ↓
Combine partition structure
       ↓
Fewer partitions
```

This is associated with a **narrow dependency** for the normal partition-reduction use case.

## Important limitation

`coalesce()` is primarily for reducing partitions.

For increasing partitions, use:

```python
df.repartition(20)
```

rather than relying on `coalesce()`.

## Trade-off

Because `coalesce()` avoids a full redistribution, resulting partitions can potentially be less evenly balanced.

Do not memorize the oversimplified statement:

> "coalesce never shuffles."

The more accurate statement is:

> `coalesce()` can reduce partitions without a full shuffle in the normal reduction use case.

Partition balance and performance optimization will be covered later.

---

# 7. `repartition()` vs `coalesce()`

| Feature | `repartition()` | `coalesce()` |
|---|---|---|
| Main purpose | Redistribute data | Reduce partitions |
| Shuffle | Yes, for normal repartitioning | No full shuffle for normal reduction |
| Exchange | Usually present | Not present for normal reduction |
| Can increase partitions | Yes | Not the intended use |
| Can decrease partitions | Yes | Yes |
| Redistribution quality | Full redistribution | Can be less balanced |
| Typical physical operator | `Exchange` | `Coalesce` |

Mental model:

```text
Need a new distribution?
        ↓
repartition()
        ↓
Exchange / Shuffle
```

```text
Just need fewer partitions?
        ↓
coalesce()
        ↓
Combine existing partition structure
```

---

# 8. `groupBy()` — Connecting Partitioning to Aggregation

We then moved from partition APIs into physical execution of aggregation.

Example:

```python
result = df.groupBy("department").count()
```

Output:

```text
+----------+-----+
|department|count|
+----------+-----+
|IT        |3    |
|HR        |2    |
|Finance   |1    |
+----------+-----+
```

## Why is `groupBy()` wide?

Records with the same grouping key may initially be located in different partitions.

Example:

```text
Partition 1       Partition 2

IT                IT
HR                HR
```

Spark needs records belonging to the same grouping key to reach the appropriate target partition so the aggregation can be completed correctly.

Therefore:

```text
groupBy()
   ↓
Need same key together
   ↓
Exchange / Shuffle
```

## Actual physical plan observed

```text
AdaptiveSparkPlan
+- HashAggregate
   +- Exchange
      +- HashAggregate
         +- Project
            +- Scan ExistingRDD
```

This is a major Spark execution pattern.

---

# 9. Partial and Final Aggregation

The first `HashAggregate` contained:

```text
partial_count(1)
```

This means Spark performs a **partial/local aggregation before the shuffle**.

Conceptually:

```text
Input partition
      ↓
Partial HashAggregate
      ↓
Smaller intermediate result
```

For example:

```text
Partition 1:
IT
IT
HR

↓

IT = 2
HR = 1
```

Then Spark performs the shuffle.

The physical plan showed:

```text
Exchange
Arguments:
hashpartitioning(department, 200)
```

After the shuffle, the second `HashAggregate` performs the final aggregation.

Conceptually:

```text
Partial HashAggregate
        ↓
Exchange / Shuffle
        ↓
Final HashAggregate
```

For example:

```text
IT = 2
IT = 1

↓

IT = 3
```

## Why partial aggregation is useful

Spark can reduce the amount of data that needs to cross the shuffle boundary.

Instead of shuffling every raw row:

```text
IT
IT
IT
IT
IT
```

it may shuffle partial results:

```text
IT → partial count
```

This is an important distributed-aggregation pattern.

---

# 10. `groupBy()` and Hash Partitioning

The observed Exchange was:

```text
hashpartitioning(department, 200)
```

This means Spark is redistributing partial aggregation results according to the grouping key.

This connects directly to the previous practical:

```python
df.repartition(2, "department")
```

which produced:

```text
hashpartitioning(department, 2)
```

The difference is that `groupBy()` itself requires the necessary partitioning for the aggregation, whereas `repartition()` explicitly requests a new physical distribution.

---

# 11. Physical Plan Reading Skill

A major goal of this Session 4 section is learning to read `Exchange` instead of merely noticing that it exists.

When you see:

```text
Exchange
```

ask:

> Why does Spark need to move this data?

Examples learned:

### `orderBy()`

```text
Exchange
↓
rangepartitioning(salary DESC, ...)
```

Reason:

> Global sorting.

### `repartition(2)`

```text
Exchange
↓
RoundRobinPartitioning(2)
```

Reason:

> Redistribute into 2 partitions.

### `repartition(2, "department")`

```text
Exchange
↓
hashpartitioning(department, 2)
```

Reason:

> Redistribute according to `department` into 2 partitions.

### `groupBy("department")`

```text
Partial HashAggregate
↓
Exchange
↓
hashpartitioning(department, ...)
↓
Final HashAggregate
```

Reason:

> Bring the same grouping keys together for final aggregation.

---

# 12. Narrow vs Wide Mental Model

### Narrow

```text
select()
filter()
withColumn()
sortWithinPartitions()
coalesce()   # normal partition reduction
```

Generally, each output partition can be computed from a limited set of parent partitions without a full redistribution.

### Wide

```text
distinct()
dropDuplicates()
groupBy()
orderBy()
repartition()
many joins
```

Data may need to move between partitions.

Typical physical-plan signal:

```text
Exchange
```

---

# 13. Common Mistakes

### Mistake 1

> `orderBy()` just sorts every partition.

Incorrect.

`orderBy()` establishes global ordering and can require redistribution.

### Mistake 2

> `sortWithinPartitions()` gives a globally sorted DataFrame.

Incorrect.

It only sorts within existing partitions.

### Mistake 3

> Any `Exchange` near `sortWithinPartitions()` was caused by `sortWithinPartitions()`.

Incorrect.

In our practical:

```text
repartition(2)
    ↓
Exchange
    ↓
sortWithinPartitions()
```

The Exchange came from `repartition(2)`.

### Mistake 4

> `repartition(2)` means split every partition into 2.

Incorrect.

It means the resulting DataFrame has 2 partitions after redistribution.

### Mistake 5

> `repartition(2, "department")` means IT always goes to partition 1.

Incorrect.

Partition assignment comes from the hash-partitioning mechanism.

### Mistake 6

> `coalesce()` never shuffles under every circumstance.

Too absolute.

For normal reduction, `coalesce()` can reduce partitions without a full shuffle.

### Mistake 7

> `groupBy()` has only one aggregation stage.

Incorrect.

The observed physical plan had:

```text
Partial HashAggregate
↓
Exchange
↓
Final HashAggregate
```

---

# 14. Interview Questions

### Q1. Why is `orderBy()` a wide transformation?

Because global sorting may require redistribution of records between partitions, introducing an Exchange/shuffle boundary.

### Q2. Difference between `orderBy()` and `sortWithinPartitions()`?

`orderBy()` establishes global ordering; `sortWithinPartitions()` sorts records independently inside existing partitions.

### Q3. Why does `repartition()` cause a shuffle?

Because Spark must redistribute records to create the requested partition layout.

### Q4. What does `repartition(2)` mean?

The resulting DataFrame has 2 partitions, with records redistributed across them.

### Q5. What is `RoundRobinPartitioning(2)`?

A partitioning strategy used when Spark is redistributing data across 2 partitions without a specific partitioning key.

### Q6. What does `repartition(2, "department")` do?

It creates 2 partitions and distributes records according to the `department` partitioning expression.

### Q7. Difference between `repartition()` and `coalesce()`?

`repartition()` performs redistribution/shuffle and can increase or decrease partition count. `coalesce()` is primarily used to reduce partitions without a full shuffle.

### Q8. Why does `groupBy()` require a shuffle?

Because records for the same grouping key can exist in different partitions and need to reach the appropriate partition for final aggregation.

### Q9. Why are there two `HashAggregate` operators?

Spark can perform a partial/local aggregation before the shuffle and a final aggregation after the shuffle.

### Q10. What does `Exchange` tell you?

It indicates a physical redistribution boundary. You should inspect its partitioning arguments to understand why Spark is moving the data.

---

# 15. Interview Cheat Card

```text
orderBy()
→ Global sort
→ Wide
→ Exchange
→ Range partitioning
→ Sort

sortWithinPartitions()
→ Local partition sort
→ No global ordering
→ No shuffle caused by the sort itself

repartition(n)
→ Change partition distribution
→ Exchange
→ Shuffle
→ RoundRobinPartitioning(n)

repartition(n, key)
→ Change distribution using key
→ Exchange
→ HashPartitioning(key, n)

coalesce(n)
→ Reduce partitions
→ No full shuffle in normal reduction
→ Coalesce operator

groupBy(key)
→ Same key must reach same target partition
→ Partial HashAggregate
→ Exchange
→ Final HashAggregate
```

---

# 16. Session Progress

Completed:

- [x] `orderBy()` and global sorting
- [x] `Exchange` in global sorting
- [x] Range partitioning
- [x] `sortWithinPartitions()`
- [x] `repartition(n)`
- [x] `RoundRobinPartitioning`
- [x] `repartition(n, column)`
- [x] `HashPartitioning`
- [x] `coalesce()`
- [x] Physical-plan comparison
- [x] `groupBy()` shuffle behavior
- [x] Partial vs final aggregation

Next:

- [ ] `groupBy() + agg()`
- [ ] Physical plans for `sum`, `avg`, `min`, `max`, `count`
- [ ] Continue Session 4 progression

Future section — **not yet covered**:

- [ ] Spark Performance Optimization
- [ ] `spark.sql.shuffle.partitions`
- [ ] AQE
- [ ] Partition sizing
- [ ] Data skew
- [ ] Other optimization techniques

---

# 17. Current Stop Point

We stopped after successfully analyzing:

```text
groupBy("department").count()

Scan ExistingRDD
      ↓
Project
      ↓
Partial HashAggregate
      ↓
Exchange
      ↓
Final HashAggregate
```

Next session continuation:

```text
groupBy()
   ↓
agg()
   ↓
Multiple aggregate functions
   ↓
Physical plan analysis
```

Do not restart from `orderBy()`, `repartition()`, or `coalesce()` unless revision is specifically requested.
