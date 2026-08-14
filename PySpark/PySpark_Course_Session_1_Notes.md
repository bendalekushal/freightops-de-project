# PySpark Course Notes

## Session 1: Introduction to Big Data & Why Apache Spark?

**Course Version:** v1.0\
**Project:** JobPulse AI\
**Duration:** Session 1

------------------------------------------------------------------------

# Learning Objectives

By the end of this session, you should understand:

-   What Big Data is.
-   Why traditional tools fail with large datasets.
-   The Five Vs of Big Data.
-   Distributed Computing.
-   Why Apache Spark was developed.

------------------------------------------------------------------------

# 1. What is Data?

Data is a collection of raw facts that can be processed to generate
meaningful insights.

Example:

``` text
Candidate_ID | Skills | Experience
101          | Python | 4 Years
102          | SQL    | 2 Years
```

# 2. What is Big Data?

**Definition**

Big Data is data that cannot be efficiently processed using traditional
tools or a single machine because of its size, speed, or complexity.

Big Data is not just about large file sizes.

# 3. Five Vs of Big Data

## Volume

Amount of data (GB, TB, PB, EB).

## Velocity

The speed at which data is generated and arrives.

Examples: - Stock market - IoT devices - GPS tracking - Banking
transactions - Job postings

## Variety

Different data formats: - CSV - JSON - XML - Parquet - Images - Videos -
PDFs - Logs - Audio

## Veracity

Quality and reliability of data: - Missing values - Duplicate records -
Incorrect values - Typographical errors - Invalid data

## Value

Business insights extracted from raw data.

# 4. Why Traditional Tools Fail

Example:

-   Laptop RAM: **16 GB**
-   Dataset: **1 TB**

Problems: - Insufficient memory - Slow processing - Limited CPU
resources - Limited storage - Single point of failure

# 5. Distributed Computing

Instead of processing everything on one computer, distribute the
workload across multiple machines.

Example:

``` text
160 GB Dataset

↓

Machine 1 → 16 GB
Machine 2 → 16 GB
Machine 3 → 16 GB
...
Machine 10 → 16 GB
```

Each machine processes its partition in parallel.

# 6. Advantages of Distributed Computing

-   Memory optimization
-   Parallel processing
-   Better CPU utilization
-   Faster execution
-   Fault tolerance
-   Horizontal scalability
-   High availability
-   Cost efficiency

# 7. Why Apache Spark?

Apache Spark is a distributed data processing engine designed to process
large datasets efficiently across multiple machines.

Key features: - In-memory processing - Fault tolerance - Scalability -
Batch and streaming support - APIs for Python, Scala, Java, and R

# 8. Where Does PySpark Fit?

``` text
Python Code
      ↓
PySpark API
      ↓
Apache Spark Engine (JVM)
      ↓
Cluster
```

# 9. JobPulse AI Connection

``` text
Job APIs
    ↓
Raw JSON
    ↓
PySpark Cleaning
    ↓
Validation
    ↓
Business Rules
    ↓
Parquet Files
    ↓
Analytics
    ↓
Dashboard
```

# Interview Revision

### What is Big Data?

Big Data is data that cannot be processed efficiently using traditional
tools or a single machine due to its size, speed, variety, and
complexity.

### Why was Apache Spark introduced?

To process massive datasets using distributed computing with high
performance, scalability, and fault tolerance.

### What is Distributed Computing?

A computing model where data and computation are distributed across
multiple machines that work simultaneously.

# Common Mistakes

-   Thinking Big Data only means large files.
-   Confusing Veracity with raw data.
-   Ignoring parallel processing.
-   Assuming Spark stores all data on one machine.

# Key Terms

  Term                    Meaning
  ----------------------- ---------------------------------------------------
  Big Data                Data too large/complex for traditional processing
  Volume                  Amount of data
  Velocity                Speed of data generation
  Variety                 Different data formats
  Veracity                Data quality
  Value                   Business insight
  Distributed Computing   Multiple machines working together
  Apache Spark            Distributed processing engine
  PySpark                 Python API for Spark

# Revision Tracker

  Session        Topic                              Status
  -------------- ---------------------------------- -----------
  ✅ Session 1   Introduction to Big Data           Completed
  ⏳ Session 2   Spark Architecture                 Pending
  ⏳ Session 3   Spark Installation & Environment   Pending
  ⏳ Session 4   SparkSession & SparkContext        Pending
  ⏳ Session 5   RDD Fundamentals                   Pending
