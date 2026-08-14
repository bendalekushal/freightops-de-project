# PySpark Course — Session 4 Notes
## DataFrames, Execution Plans, Optimization, Expressions, NULL Handling & String Functions

**Date:** 13 August 2026  
**Environment:** PySpark 3.4.1, Python 3.11, Java 11  
**Project context:** JobPulse AI / Data Engineering Bootcamp

---

## 1. Session Objective

This session moved from Spark theory into practical PySpark DataFrame work.

We learned how to:

- Create and inspect DataFrames.
- Read and write Parquet.
- Understand `explain("formatted")`.
- Observe column pruning.
- Observe predicate pushdown.
- Use `select()`, `filter()`, and `withColumn()`.
- Understand why `withColumn()` appears as `Project`.
- Use `when()` / `otherwise()`.
- Use `lit()` and type casting.
- Understand NULL semantics and three-valued logic.
- Use `isNull()`, `isNotNull()`, `fillna()`, `dropna()`, and `coalesce()`.
- Clean string columns using Spark built-in functions.
- Connect transformations to Spark physical execution plans.

---

# 2. Spark DataFrame Basics — Practical

A Spark DataFrame is a distributed collection of data organized into named columns.

Example:

```python
data = [
    (101, "Alice", "IT", 75000),
    (102, "Bob", "HR", 55000),
    (103, "Charlie", "IT", 90000),
    (104, "David", "Finance", 65000),
]

columns = ["employee_id", "name", "department", "salary"]

df = spark.createDataFrame(data, columns)
```

Inspection:

```python
df.printSchema()
df.show()
```

---

# 3. `select()` and Physical Plan

Example:

```python
selected_df = df.select("name", "salary")

selected_df.show()
selected_df.explain("formatted")
```

Physical plan observed:

```text
Project
   ↓
Scan ExistingRDD
```

Important idea:

`select()` is a transformation and normally does not require a shuffle.

A projection in Spark means selecting/calculating the output columns.

---

# 4. Parquet Practical

We wrote the DataFrame to Parquet:

```python
df.write.mode("overwrite").parquet(
    "PySpark/session_4/data/employees"
)
```

Spark writes distributed output as files inside a directory, rather than necessarily producing one single `.parquet` file.

Reading:

```python
employees = spark.read.parquet(
    "PySpark/session_4/data/employees"
)
```

---

# 5. Column Pruning

We tested:

```python
selected_employees = employees.select(
    "name",
    "salary"
)
```

Physical plan showed:

```text
Scan parquet
Output [2]: [name, salary]

ReadSchema: struct<name:string,salary:bigint>
```

The original dataset had:

```text
employee_id
name
department
salary
```

but Spark only needed:

```text
name
salary
```

This is **column pruning**.

### Mental model

```text
Parquet
   ↓
Need only name + salary
   ↓
Read only required columns
   ↓
Less unnecessary I/O
```

If we selected:

```python
employees.select(
    "name",
    "salary",
    "department"
)
```

the `ReadSchema` changed accordingly:

```text
name
department
salary
```

`employee_id` was not read because nothing downstream required it.

---

# 6. `filter()` and Predicate Pushdown

Example:

```python
filtered_employees = (
    employees
    .filter(F.col("salary") > 60000)
    .select("name", "salary")
)
```

Physical plan contained:

```text
PushedFilters:
[
    IsNotNull(salary),
    GreaterThan(salary,60000)
]
```

This demonstrates **predicate pushdown**.

### Column pruning vs predicate pushdown

Column pruning answers:

> Which columns do I need?

Predicate pushdown answers:

> Which eligible row predicates can be pushed toward the data source?

Conceptually:

```text
Parquet
   ↓
Column pruning
   ↓
Read required columns
   ↓
Predicate pushdown
   ↓
Filter eligible data earlier
```

Important interview wording:

> Spark can push eligible predicates to a data source when the source supports predicate pushdown. The exact amount of data eliminated depends on the source and its capabilities.

Do not say predicate pushdown always happens.

---

# 7. Multiple Predicates

We tested:

```python
result = (
    employees
    .filter(
        (F.col("salary") > 60000) &
        (F.col("department") == "IT")
    )
    .select("name", "department", "salary")
)
```

Observed:

```text
PushedFilters:
[
    IsNotNull(salary),
    IsNotNull(department),
    GreaterThan(salary,60000),
    EqualTo(department,IT)
]
```

Only these columns were read:

```text
name
department
salary
```

`employee_id` was pruned.

No `Exchange` appeared.

Therefore:

```text
filter()
   ↓
narrow transformation
   ↓
no shuffle
```

---

# 8. OR Predicate

We then tested:

```python
result = (
    employees
    .filter(
        (F.col("salary") > 60000) |
        (F.col("department") == "IT")
    )
    .select("name", "department", "salary")
)
```

The physical plan showed:

```text
PushedFilters:
[
    Or(
        GreaterThan(salary,60000),
        EqualTo(department,IT)
    )
]
```

Important lesson:

Predicate pushdown is not limited to simple AND predicates. The actual pushdown depends on the source and predicate support.

---

# 9. `withColumn()`

Example:

```python
salary_band_df = employees.withColumn(
    "salary_band",
    F.when(F.col("salary") < 60000, "Low")
     .when(
         (F.col("salary") >= 60000) &
         (F.col("salary") < 80000),
         "Medium"
     )
     .otherwise("High")
)
```

Result:

```text
Alice     75000   Medium
Bob       55000   Low
Charlie   90000   High
David     65000   Medium
```

A simpler equivalent expression is:

```python
F.when(F.col("salary") < 60000, "Low") \
 .when(F.col("salary") < 80000, "Medium") \
 .otherwise("High")
```

because conditions are evaluated top-to-bottom.

### Key concept

`withColumn()` is a transformation.

It returns a new DataFrame because Spark DataFrames are immutable.

It normally does not require a shuffle.

---

# 10. Why `withColumn()` Appears as `Project`

Physical plan:

```text
Project
   ↓
ColumnarToRow
   ↓
Scan parquet
```

The Project output contained:

```text
employee_id
name
department
salary
CASE WHEN ... END AS salary_band
```

So internally:

```text
withColumn()
    ↓
new Spark expression
    ↓
Project
    ↓
existing columns + derived column
```

This is an important Spark execution-plan concept.

Also remember:

```text
select()      → Project
withColumn()  → Project
string expressions → usually part of Project
filter()      → Filter
```

---

# 11. `lit()` — Literal Values

`col()` refers to a column value:

```python
F.col("salary")
```

`lit()` creates a Spark literal/constant expression:

```python
F.lit("India")
F.lit(5000)
F.lit(0.10)
F.lit(True)
```

Example:

```python
df.withColumn(
    "country",
    F.lit("India")
)
```

Every row receives:

```text
India
```

Mental model:

```text
col()
   ↓
value from the row's column

lit()
   ↓
constant value
```

---

# 12. Type Casting

Use `.cast()` to convert a column to another data type.

Examples:

```python
F.col("salary").cast("double")

F.col("employee_id").cast("string")

F.col("application_date").cast("date")

F.col("created_at").cast("timestamp")
```

Example:

```python
employees_messy = employees.withColumn(
    "salary_string",
    F.col("salary").cast("string")
)

employees_typed = employees_messy.withColumn(
    "salary_numeric",
    F.col("salary_string").cast("double")
)
```

Observed schema:

```text
salary_string   → string
salary_numeric  → double
```

Casting is important when source data arrives with incorrect or inconsistent data types.

Invalid conversions can result in `NULL`, which makes NULL handling important.

---

# 13. NULL Semantics

Python:

```python
None
```

becomes Spark:

```text
NULL
```

Example:

```python
data = [
    (101, "Alice", 75000),
    (102, "Bob", None),
    (103, "Charlie", 55000),
    (104, "David", None),
    (105, "Eva", 90000),
]
```

Schema:

```text
employee_id: long
name: string
salary: long
```

---

# 14. Three-Valued Logic

Spark SQL uses:

```text
TRUE
FALSE
UNKNOWN
```

For:

```python
F.col("salary") > 60000
```

when salary is NULL:

```text
NULL > 60000
      ↓
UNKNOWN
```

This is not the same as FALSE.

However, `filter()` keeps only rows where the condition is TRUE.

Therefore:

```text
salary     salary > 60000     filter result
75000      TRUE               keep
55000      FALSE              remove
NULL       UNKNOWN            remove
```

This is a critical interview concept.

---

# 15. `isNull()` and `isNotNull()`

Find NULL values:

```python
df.filter(
    F.col("salary").isNull()
)
```

Find non-NULL values:

```python
df.filter(
    F.col("salary").isNotNull()
)
```

These are explicit NULL checks.

---

# 16. `when()` with NULL

Example:

```python
result = df.withColumn(
    "salary_status",
    F.when(F.col("salary") > 60000, "Above 60K")
     .otherwise("60K or Below")
)
```

For NULL salary:

```text
NULL > 60000
      ↓
UNKNOWN
      ↓
when condition is not TRUE
      ↓
otherwise()
```

Therefore NULL salaries received:

```text
60K or Below
```

---

# 17. `fillna()`

Replace NULL with a value.

```python
filled_df = df.fillna({
    "salary": 0
})
```

Result:

```text
NULL → 0
```

The row remains.

Use this when the business meaning of the replacement is valid.

Do not blindly replace every NULL with zero.

---

# 18. `dropna()`

Remove rows containing NULL in selected columns.

```python
dropped_df = df.dropna(
    subset=["salary"]
)
```

Result:

```text
NULL salary
    ↓
entire row removed
```

Whether this is correct depends on business/data-quality requirements.

---

# 19. `coalesce()`

`coalesce()` returns the first non-NULL expression.

Example:

```python
F.coalesce(
    F.col("primary_salary"),
    F.col("secondary_salary"),
    F.lit(0)
)
```

Logic:

```text
primary_salary available?
       ↓ YES
use primary_salary

       ↓ NO

secondary_salary available?
       ↓ YES
use secondary_salary

       ↓ NO

use 0
```

This is particularly useful when multiple source columns can provide the same business value.

---

# 20. NULL Mental Model

Remember:

```text
NULL ≠ 0
NULL ≠ ""
NULL ≠ False
```

NULL means missing/unknown value.

The correct treatment depends on business semantics.

---

# 21. String Functions

We created dirty job data:

```text
job_id | company       | location
101    | "  Microsoft "| "PUNE, India"
102    | "AMAZON"      | "Mumbai, INDIA"
103    | "google india"| "Bangalore, India"
104    | "  TCS"       | "PUNE, INDIA"
```

Important built-in string functions:

```python
F.trim()
F.lower()
F.upper()
F.initcap()
F.length()
F.split()
F.concat()
F.regexp_replace()
```

---

# 22. `trim()`

Removes leading/trailing whitespace.

```python
F.trim(F.col("company"))
```

Example:

```text
"  Microsoft  "
       ↓
"Microsoft"
```

It does not remove spaces inside the string.

---

# 23. `lower()` and `upper()`

```python
F.lower(F.col("company"))
```

```text
"MICROSOFT" → "microsoft"
```

and:

```python
F.upper(F.col("company"))
```

```text
"Microsoft" → "MICROSOFT"
```

Useful for normalization and consistent comparisons.

---

# 24. `initcap()`

Capitalizes the first character of each word.

```python
F.initcap(F.col("company"))
```

Example:

```text
"microsoft india"
       ↓
"Microsoft India"
```

Useful for presentation formatting.

---

# 25. `split()`

Splits a string into an array.

```python
F.split(
    F.col("location"),
    ","
)
```

For:

```text
"Pune, India"
```

result conceptually:

```text
["Pune", " India"]
```

Access the first element:

```python
F.split(
    F.col("location"),
    ","
)[0]
```

Then clean it:

```python
F.trim(
    F.split(F.col("location"), ",")[0]
)
```

---

# 26. `concat()`

Combines expressions.

Example:

```python
F.concat(
    F.col("first_name"),
    F.lit(" "),
    F.col("last_name")
)
```

`lit(" ")` supplies the literal space.

---

# 27. `regexp_replace()`

Useful for pattern-based cleaning.

Example:

```python
F.regexp_replace(
    F.col("phone"),
    "[^0-9]",
    ""
)
```

This removes every non-digit character.

Example:

```text
+91-987-654-3210
        ↓
919876543210
```

This is very useful for messy production data.

---

# 28. Practical String Cleaning Completed

We created:

```python
clean_df = df.withColumn(
    "company_clean",
    F.trim(F.lower(F.col("company")))
).withColumn(
    "city_clean",
    F.trim(
        F.lower(
            F.split(F.col("location"), ",")[0]
        )
    )
)
```

Observed:

```text
company_clean | city_clean
--------------|-----------
microsoft     | pune
amazon        | mumbai
google india  | bangalore
tcs           | pune
```

This was correct.

For presentation-oriented output, `initcap()` could be used instead of `lower()`:

```text
Pune
Mumbai
Bangalore
```

For analytical normalization, lowercase values are often useful because comparisons become consistent.

---

# 29. Physical Plan for String Cleaning

Observed:

```text
== Physical Plan ==

* Project
+- * Scan ExistingRDD
```

The Project contained expressions such as:

```text
trim(lower(company))
trim(lower(split(location, ",")[0]))
```

This demonstrates again that Spark represents many DataFrame expressions as a `Project`.

No `Exchange` appeared.

Therefore these string transformations do not require data redistribution.

---

# 30. Important Pattern Learned in Session 4

We can now connect API operations to physical plan operators:

```text
select()
    ↓
Project

withColumn()
    ↓
Project

String expressions
    ↓
Project

filter()
    ↓
Filter

groupBy(), many joins, orderBy(), etc.
    ↓
Potential Exchange
    ↓
Shuffle
```

And two major file-scan optimizations:

```text
select()
    ↓
Column Pruning
    ↓
Read only required columns
```

```text
filter()
    ↓
Predicate Pushdown
    ↓
Push eligible predicates toward data source
```

---

# 31. Interview-Level Summary

If asked:

### Why is `select()` efficient with Parquet?

Because Spark can perform column pruning and the Parquet reader can read only the required columns.

### What is predicate pushdown?

It is the optimization where Spark pushes an eligible filter predicate toward the underlying data source so unnecessary data can potentially be eliminated earlier.

### Does `filter()` cause a shuffle?

Normally no. `filter()` is a narrow transformation because each partition can evaluate the predicate independently.

### Why does `withColumn()` appear as `Project`?

Because Spark's physical projection operator can select existing columns and calculate derived expressions. `withColumn()` is represented as a projection containing the original columns plus the new expression.

### What is the difference between `col()` and `lit()`?

```text
col() → reference a DataFrame column
lit() → create a constant/literal expression
```

### What happens when comparing NULL?

A comparison involving NULL generally produces UNKNOWN under Spark SQL's three-valued logic.

`filter()` retains only TRUE rows.

### `fillna()` vs `dropna()` vs `coalesce()`

```text
fillna()
→ replace NULL values

dropna()
→ remove rows containing NULL

coalesce()
→ return the first non-NULL expression
```

---

# 32. Session 4 Practical Files

The practical work completed/started during this session includes:

```text
PySpark/
└── session_4/
    ├── data/
    │   └── employees/
    │       └── *.parquet
    │
    ├── 01_dataframes_basic.py
    ├── 02_null_handling.py
    └── 03_string_functions.py
```

The exact filenames should follow the files actually created in the project.

---

# 33. Topics Still Pending

We stopped here today.

Next session should continue with:

1. Date and timestamp functions.
2. Date parsing and formatting.
3. `to_date()` / `to_timestamp()`.
4. Date arithmetic.
5. `datediff()` and timestamp differences.
6. `drop()`.
7. `distinct()`.
8. `dropDuplicates()`.
9. More DataFrame transformations.
10. Then move toward joins and aggregations.

The next major milestone after these DataFrame fundamentals is to start applying them directly to the JobPulse AI project dataset.

---

## Session 4 Key Takeaway

The most important mental model from this session is:

```text
PySpark API
    ↓
Logical plan
    ↓
Catalyst optimization
    ↓
Physical plan
    ↓
Operators such as:
    Project
    Filter
    Scan parquet
    Exchange
    ↓
Tasks execute against partitions
```

And for Parquet:

```text
SELECT required columns
        ↓
Column Pruning
        ↓
Less data read

FILTER rows
        ↓
Predicate Pushdown
        ↓
Potentially less data processed
```

This is the bridge between writing PySpark code and understanding what Spark actually does underneath.
