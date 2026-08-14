# PySpark Course Notes

# Session 3 – SparkSession, SparkContext & Reading Data

## Status
Completed (Parts 1–5)

## Topics Covered
- SparkSession
- SparkContext
- SparkSession vs SparkContext
- Spark DataFrame
- Immutability
- Schema
- DataFrameReader
- Reading CSV, JSON & Parquet
- Explicit Schema
- StructType & StructField

---

## SparkSession

- Unified entry point to Spark
- Creates or reuses SparkContext
- Used for DataFrames, SQL and reading/writing data

```python
from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("JobPulse AI")
    .getOrCreate()
)
```

---

## SparkSession vs SparkContext

SparkSession
↓
SparkContext
↓
Driver
↓
Cluster
↓
Executors

SparkSession = High-level API

SparkContext = Low-level execution engine

---

## Spark DataFrame

Definition:
An immutable distributed collection of data organized into named columns.

Characteristics:
- Distributed
- Immutable
- Schema-based
- Parallel Processing
- Catalyst Optimized

---

## Schema

Schema contains:
- Column Names
- Data Types
- Nullability
- Metadata

---

## DataFrameReader

spark.read is a DataFrameReader object.

Supports:
- CSV
- JSON
- Parquet
- ORC
- JDBC

Example:

```python
df = (
    spark.read
    .option("header","true")
    .option("inferSchema","true")
    .csv("employees.csv")
)
```

---

## Lazy Evaluation

spark.read.csv()

↓

Logical Plan

↓

DataFrame

↓

No Execution

↓

show()

↓

Execution Starts

---

## CSV vs Parquet

CSV
- Values only
- Schema inference required

Parquet
- Stores values
- Stores schema
- Stores metadata
- Faster

---

## Explicit Schema

```python
from pyspark.sql.types import *

employee_schema = StructType([
    StructField("employee_id", IntegerType(), False),
    StructField("name", StringType(), False),
    StructField("salary", DoubleType(), True),
    StructField("joining_date", DateType(), True)
])
```

Reading:

```python
df = (
    spark.read
    .option("header","true")
    .schema(employee_schema)
    .csv("employees.csv")
)
```

---

## StructType vs StructField

StructType = Complete schema

StructField = Single column

---

## Common Data Types

- StringType
- IntegerType
- LongType
- DoubleType
- BooleanType
- DateType
- TimestampType
- DecimalType

---

## Production Best Practices

- Use explicit schema
- Avoid inferSchema on production
- Prefer Parquet
- Use meaningful app names

---

## Interview Quick Revision

- SparkSession = Entry Point
- SparkContext = Low-level Engine
- spark.read = DataFrameReader
- DataFrame = Immutable
- StructType = Full Schema
- StructField = One Column
- Explicit Schema > inferSchema

---

## Next Session

- printSchema()
- show()
- schema
- columns
- dtypes
- count()
- describe()
- summary()
- explain()
