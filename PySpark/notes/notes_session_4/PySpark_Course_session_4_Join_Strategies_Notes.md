# Session 4 --- PySpark Join Strategies

## Session focus

Understand why joins can cause data movement, how Spark chooses physical
join strategies, and how to read `Exchange`, `BroadcastExchange`,
`Sort`, `BuildLeft`, and `BuildRight`.

## 1. Join fundamentals

An inner join can be a wide operation because matching join keys may
exist in different partitions.

``` text
Left input                    Right input
    |                              |
    +--------- join key -----------+
                  |
        Matching keys must be
        co-located / compatible
                  |
               Exchange
```

Interview wording:

> Spark may redistribute both join inputs according to the join keys so
> that matching keys are co-located in compatible partitions.

Do not say every join always shuffles: broadcast strategies can avoid
the normal repartitioning of the large side.

------------------------------------------------------------------------

## 2. SortMergeJoin

Observed plan:

``` text
SortMergeJoin Inner
├── Sort
│   └── Exchange
│       └── Filter
│           └── Scan
└── Sort
    └── Exchange
        └── Filter
            └── Scan
```

Execution:

``` text
Left  → Exchange(hashpartitioning(key)) → Sort ┐
                                               ├→ SortMergeJoin
Right → Exchange(hashpartitioning(key)) → Sort ┘
```

Why Exchange? Matching keys need compatible partitioning.

Why Sort? The inputs are sorted by the join key so Spark can merge
matching sorted streams.

Spark also inserted `isnotnull(join_key)` filters before the shuffle for
the inner equality join.

Mental model:

``` text
Exchange → Sort → Merge
```

Interview answer:

> SortMergeJoin is a common strategy for large equi-joins. Spark
> typically shuffles both inputs by the join key, sorts them, and merges
> matching sorted keys.

------------------------------------------------------------------------

## 3. BroadcastHashJoin

Example:

``` python
from pyspark.sql.functions import broadcast

result = employees.join(
    broadcast(departments),
    employees.department == departments.department,
    "inner"
)
```

Observed plan:

``` text
BroadcastHashJoin Inner BuildRight
├── Filter
│   └── Scan
└── BroadcastExchange
    └── Filter
        └── Scan
```

No normal hash-partitioning Exchange on the large side and no Sort
operators.

Execution:

``` text
Small side
    ↓
BroadcastExchange
    ↓
Build hash relation
    ↓
Distributed to executors

Large-side rows
    ↓
Probe local hash relation
```

`BuildRight` means the right input is the build/broadcast side.

If the broadcast side is on the left, Spark can show `BuildLeft`.

Important distinction:

``` text
Exchange          → shuffle / redistribute data
BroadcastExchange → distribute a small relation
```

Interview answer:

> BroadcastHashJoin broadcasts a small build-side relation, builds an
> in-memory hash relation using the join key, and probes it with rows
> from the other side.

------------------------------------------------------------------------

## 4. BroadcastNestedLoopJoin

We tested a non-equi/range condition:

``` python
result = employees.join(
    broadcast(salary_bands),
    (employees.salary >= salary_bands.min_salary) &
    (employees.salary <= salary_bands.max_salary),
    "inner"
)
```

Observed plan:

``` text
BroadcastNestedLoopJoin Inner BuildRight
├── Filter
│   └── Scan
└── BroadcastExchange
    └── Filter
        └── Scan
```

The condition was:

``` text
salary >= min_salary
AND salary <= max_salary
```

This is not a simple equality-key lookup, so the normal
BroadcastHashJoin pattern does not apply.

Mental model:

``` text
Small side
    ↓
Broadcast
    ↓
Large-side row
    ↓
Evaluate general / non-equi condition
```

Do not oversimplify this as "every large row is always compared with
every small row"; exact execution depends on the condition and
optimizations.

Interview answer:

> BroadcastNestedLoopJoin broadcasts one side and evaluates a general
> join condition against the broadcasted relation. It can support
> non-equi conditions but can become expensive as the broadcast-side
> cardinality grows.

------------------------------------------------------------------------

## 5. ShuffledHashJoin

Conceptual execution:

``` text
Left  → Exchange ┐
                ├→ ShuffledHashJoin
Right → Exchange ┘
```

Unlike SortMergeJoin, it does not require Sort operators.

``` text
SortMergeJoin
→ Exchange → Sort → Merge

ShuffledHashJoin
→ Exchange → Build hash table → Probe
```

Terminology:

``` text
Build side → creates hash relation
Probe side → looks up keys in hash relation
```

We attempted to influence the strategy with:

``` python
spark.conf.set(
    "spark.sql.join.preferSortMergeJoin",
    "false"
)
```

but Spark still selected `SortMergeJoin` for the tiny test DataFrames.

Lesson:

> A configuration preference does not guarantee a particular physical
> join strategy. Spark considers additional planning conditions,
> statistics, relation sizes, join characteristics, and constraints.

------------------------------------------------------------------------

## 6. Strategy comparison

  -----------------------------------------------------------------------------------------
  Strategy                  Shuffle        Sort           Hash relation  Typical use
  ------------------------- -------------- -------------- -------------- ------------------
  SortMergeJoin             Yes, typically Yes            No             Large-large
                            both sides                                   equi-joins

  BroadcastHashJoin         No normal      No             Yes            Small + large
                            shuffle of                                   equi-join
                            large side                                   

  BroadcastNestedLoopJoin   No normal      No             No hash lookup Broadcastable
                            shuffle of                                   non-equi/general
                            large side                                   condition

  ShuffledHashJoin          Yes, typically No             Yes            Suitable shuffled
                            both sides                                   hash join
  -----------------------------------------------------------------------------------------

Mental models:

``` text
SortMergeJoin
→ Exchange + Sort + Merge

BroadcastHashJoin
→ Broadcast + Hash + Probe

BroadcastNestedLoopJoin
→ Broadcast + General condition

ShuffledHashJoin
→ Exchange + Hash + Probe
```

------------------------------------------------------------------------

## 7. Broadcast decision

Do not use:

``` text
Smaller table = broadcast
```

Use:

``` text
Safely small enough?
        ↓
Executor memory comfortable?
        ↓
Replication/network cost acceptable?
        ↓
Broadcast candidate
```

Example:

``` text
500 GB fact + 20 MB dimension
→ BroadcastHashJoin is a strong candidate.
```

But:

``` text
500 GB fact + 50 GB dimension
→ Do not casually broadcast.
→ Consider shuffle-based strategies.
```

And:

``` text
1 TB fact + 800 MB dimension
→ Do not automatically broadcast.
→ Check statistics, executor memory, serialized size,
  replication/network cost, and workload.
```

Important correction:

> The key concern is not simply whether the table fits in driver memory.
> A broadcast relation is distributed to executors and must be safely
> held and replicated there.

------------------------------------------------------------------------

## 8. Physical-plan reading checklist

When reading a join plan, ask:

1.  What join operator was selected?
2.  Is there an `Exchange`?
3.  What partitioning does the Exchange use?
4.  Are there `Sort` operators?
5.  Is there a `BroadcastExchange`?
6.  Is it `BuildLeft` or `BuildRight`?
7.  What is the join condition?
8.  Why did Spark need each operator?

Examples:

``` text
hashpartitioning(department, 200)
→ redistribute by department

BuildRight
→ right input builds hash relation

BroadcastExchange
→ small relation is being distributed

Sort
→ required by the SortMergeJoin path
```

------------------------------------------------------------------------

## 9. Interview questions

### Why can an inner join cause a shuffle?

Matching join keys may be distributed across different partitions, so
Spark may redistribute the inputs to make matching keys co-located.

### Why does SortMergeJoin have Sort operators?

The shuffled inputs must be sorted by the join key so Spark can merge
matching sorted streams.

### What is the advantage of BroadcastHashJoin?

It can avoid shuffling the large input by broadcasting a small
build-side relation.

### What does BuildRight mean?

The right input is used to build the hash relation.

### Exchange vs BroadcastExchange?

`Exchange` represents redistribution/shuffle. `BroadcastExchange`
distributes a small relation for broadcast use.

### Difference between SortMergeJoin and ShuffledHashJoin?

Both can shuffle the inputs. SortMergeJoin sorts and merges them;
ShuffledHashJoin builds a hash relation and probes it.

### Is the smaller table always broadcast?

No. It must be safely broadcastable considering size, statistics,
executor memory, replication cost, and workload.

### Does `spark.sql.join.preferSortMergeJoin=false` guarantee ShuffledHashJoin?

No. It is a preference, not a guarantee.

------------------------------------------------------------------------

## 10. Common mistakes

``` text
❌ Every join always shuffles.
✓ Broadcast strategies can avoid normal large-side shuffle.

❌ Smaller table always means broadcast.
✓ It must be safely broadcastable and operationally suitable.

❌ Build side probes.
✓ Build side creates the hash relation; probe side looks it up.

❌ Broadcast join has no Exchange.
✓ It can contain BroadcastExchange.

❌ ShuffledHashJoin means no shuffle.
✓ It is a shuffle-based strategy.

❌ Turning off preferSortMergeJoin forces ShuffledHashJoin.
✓ It does not guarantee that strategy.
```

------------------------------------------------------------------------

## 11. Session 4 revision card

``` text
Exchange
→ data movement / shuffle

SortMergeJoin
→ Exchange + Sort + Merge

BroadcastHashJoin
→ BroadcastExchange + Hash + Probe

BroadcastNestedLoopJoin
→ Broadcast + general condition

ShuffledHashJoin
→ Exchange + Hash + Probe

Build side
→ creates hash relation

Probe side
→ searches hash relation

Broadcast suitability
→ size + executor memory + statistics + replication cost
```

## 12. Session state

Covered in practice:

-   `orderBy()` / global sorting
-   `sortWithinPartitions()`
-   `repartition(n)`
-   `repartition(n, column)`
-   Round-robin partitioning
-   Hash partitioning
-   `coalesce()`
-   `groupBy()` and shuffle behavior
-   Partial/final aggregation
-   Multiple aggregations
-   Filter before/after aggregation
-   `select()` / Project
-   `withColumn()`
-   Multiple `withColumn()` calls
-   `drop()`
-   `distinct()`
-   `dropDuplicates()`
-   Duplicate-group identification
-   `union()`
-   `unionByName()`
-   `unionByName(..., allowMissingColumns=True)`
-   `SortMergeJoin`
-   `BroadcastHashJoin`
-   `BroadcastNestedLoopJoin`
-   `ShuffledHashJoin` conceptual comparison
-   Join-strategy selection

Deferred:

-   Window-function implementation of Pandas-style `duplicated()`
-   Dedicated Spark Performance Optimization
-   Deeper Window Functions
-   Further production join tuning beyond the current Session 4 scope

## Final mental model

> The key Session 4 skill is not memorizing operator names. When reading
> a physical plan, ask: **Why did Spark place this operator here?**
