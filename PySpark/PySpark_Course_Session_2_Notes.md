# PySpark Course Notes

# Session 2 -- Apache Spark Architecture

## Topics Covered

-   Cluster, Master Node, Worker Node
-   Driver Program
-   Cluster Manager
-   Executors
-   Partitions
-   Input Splits
-   Lazy Evaluation
-   DAG
-   Jobs, Stages & Tasks
-   Shuffle
-   Narrow vs Wide Transformations
-   Catalyst Optimizer
-   Logical / Optimized Logical / Physical Plan
-   DAG Scheduler & Task Scheduler

## Architecture

``` text
PySpark Code
    ↓
Driver Program
    ↓
Logical Plan
    ↓
Catalyst Optimizer
    ↓
Optimized Logical Plan
    ↓
Physical Plan
    ↓
DAG Scheduler
    ↓
Job
    ↓
Stage(s)
    ↓
Task(s)
    ↓
Task Scheduler
    ↓
Executors
    ↓
Worker Nodes
```

## Key Definitions

### Cluster

A group of connected computers working as one logical system.

### Driver Program

Reads code, creates logical plans, DAG, Jobs, Stages and Tasks.

### Cluster Manager

Allocates cluster resources and launches Executors.

### Executor

JVM process that executes Tasks.

### Partition

Logical chunk of data processed independently.

**Rule:** One Partition = One Task.

### Input Split

Logical reading unit used while reading files.

Flow:

File → Input Split → Partition → Task → Executor

### Lazy Evaluation

Transformations are recorded and executed only when an Action is called.

### Transformations

filter, select, withColumn, join, groupBy, orderBy

### Actions

show, count, collect, first, take, write

### DAG

Directed Acyclic Graph representing transformations.

### Job

Created for every Action.

### Stage

Group of Tasks separated by Shuffle boundaries.

### Task

Smallest execution unit that processes one Partition.

### Shuffle

Redistribution of data across partitions.

### Narrow Transformation

No shuffle. Examples: - filter - select - withColumn - drop - sample

### Wide Transformation

Requires shuffle. Examples: - groupBy - orderBy - distinct -
repartition - most joins

### Catalyst Optimizer

Optimizes Spark SQL queries using: - Column Pruning - Predicate
Pushdown - Join Selection

### DAG Scheduler

Creates Jobs and Stages.

### Task Scheduler

Assigns Tasks to Executors.

## Interview Rules

-   One Action = One Job
-   Shuffle = New Stage
-   One Partition = One Task
-   Narrow = No Shuffle
-   Wide = Shuffle
-   Driver plans execution
-   Executors process data
-   Cluster Manager allocates resources

## Revision Tracker

-   Session 1 ✅ Big Data
-   Session 2 ✅ Spark Architecture
-   Session 3 ⏳ SparkSession & First PySpark Program
