# Customized Data Engineering Roadmap

## Learning Objective

Build strong, production-oriented Data Engineering fundamentals while avoiding repeated study of topics already known.

Primary cloud ecosystem: AWS  
Primary practical domain: Logistics / Parcel / Fleet Data Platform  
Primary hands-on laboratory: Uploaded logistics datasets

## Learning Rules

- **SKIP** — Do not reteach. Use only when required as context.
- **REVISE** — Short refresher focused on Data Engineering usage.
- **LEARN** — Start from fundamentals and build progressively.
- **DEEP DIVE** — First principles, internals, implementation, failures, optimization, production design and interview questions.

| Topic | Decision | Depth |
|---|---|---|
| SQL | SKIP | Use continuously |
| Python basics | SKIP | Practical usage |
| Python OOP | REVISE | Deep revision |
| Functional Programming | REVISE | Deep revision |
| Recursion | REVISE | Deep revision |
| NumPy | REVISE | Practical |
| Pandas | REVISE | Practical |
| DBMS | LEARN | Deep |
| Data Modeling | LEARN | Very Deep |
| Data Warehousing | LEARN | Deep |
| ETL / ELT | LEARN | Very Deep |
| dbt | LEARN | Practical |
| Airflow | LEARN | Deep |
| Fivetran | REVISE | Conceptual |
| Big Data Fundamentals | LEARN | Very Deep |
| Apache Spark | ALREADY LEARNING | Do not restart; deepen engineering concepts |
| Kafka / Streaming | LEARN | Deep |
| System Design | LEARN | Very Deep |
| AWS | KNOWLEDGE EXISTS | Production-oriented deepening |
| GCP | SKIP hands-on | Conceptual mapping |
| Azure | SKIP hands-on | Conceptual mapping |
| DevOps | LEARN | Practical |
| Docker | LEARN | Practical |
| Terraform | LEARN | Practical |
| Kubernetes | LEARN | Basic / conceptual |
| DSA | LEARN | Interview-focused |
| GenAI | REVISE | Conceptual |
| RAG | REVISE | Practical |
| Agentic AI | REVISE | Conceptual |

## Teaching Method

Every major concept follows:

1. WHY — Why does it exist?
2. WHAT — What exactly is it?
3. HOW — How does it work internally?
4. VISUALIZE — Architecture / flow / handwritten-style diagram.
5. CODE — Implement it.
6. DATASET — Apply it to the logistics datasets.
7. PRODUCTION — How a real team uses it.
8. FAILURE — Failure modes and recovery.
9. OPTIMIZATION — Performance, reliability and cost.
10. INTERVIEW — How interviewers may test it.
11. HANDWRITTEN NOTES — Compact notebook-style revision notes.

## Phase 0 — Data Engineering Mental Model

**Status: START FROM BASIC**

- What is Data Engineering?
- Data Engineer responsibilities
- Source systems
- Ingestion
- Storage
- Processing
- Serving
- Batch vs Streaming
- ETL vs ELT
- Data Lake
- Data Warehouse
- Data Lakehouse
- Data Mart
- Data Pipeline
- Data Platform
- Data Quality
- Data Lineage
- Data Governance

Core flow:

```text
Business
   ↓
Source Systems
   ↓
Ingestion
   ↓
Raw / Bronze
   ↓
Transformation
   ↓
Silver / Processed
   ↓
Gold / Curated
   ↓
Serving
   ↓
Analytics / Applications / ML
```

## Phase 1 — Python for Data Engineering

**Status: TARGETED REVISION**

Skip basic Python teaching.

Revise:

- Functions
- Collections
- Modules
- Exceptions
- Iterators
- Generators
- Functional programming
- map / filter / reduce
- Lambda
- OOP
- Classes and objects
- Inheritance
- Composition
- Polymorphism
- Encapsulation
- Recursion
- Decorators
- NumPy
- Pandas

Focus on how these concepts appear in Data Engineering code.

## Phase 2 — Database Management Systems

**Status: LEARN FROM BASIC**

- Database and DBMS
- RDBMS
- Tables
- Primary and foreign keys
- Constraints
- Transactions
- ACID
- Database architecture
- Indexes
- Query execution
- Partitioning
- Replication
- Sharding
- RDBMS vs NoSQL
- Columnar databases
- Graph databases
- OLTP vs OLAP

Goal: understand why different database technologies exist and when a Data Engineer should use them.

## Phase 3 — Data Modeling

**Status: DEEP LEARNING**

- Business requirements
- Entities
- Attributes
- Relationships
- Cardinality
- Keys
- ER modeling
- Normalization
- Denormalization
- Analytical modeling
- Fact tables
- Dimension tables
- Grain
- Measures
- Surrogate keys
- Natural keys
- Star schema
- Snowflake schema
- SCD Type 1
- SCD Type 2
- SCD Type 3

Practice domains: Logistics, Banking, E-commerce, Cab booking, Healthcare.

Primary project: Logistics Data Model.

## Phase 4 — Data Warehousing

**Status: DEEP LEARNING**

- OLTP
- OLAP
- Warehouse architecture
- Warehouse layers
- Data marts
- Facts and dimensions
- Star and snowflake schemas
- SCD
- ELT
- Warehouse optimization
- Partitioning
- Clustering
- Analytical query patterns

AWS focus: S3, Athena and Redshift.

## Phase 5 — ETL / ELT / Data Integration

**Status: VERY DEEP**

Concepts:

- ETL and ELT
- Full load
- Incremental load
- CDC
- Watermarks
- Idempotency
- Retries
- Backfills
- Schema evolution
- Data validation
- Data quality
- Audit columns
- Error handling
- Dead-letter/error paths

Tools:

- Apache Airflow
- dbt
- AWS Glue
- AWS DMS
- AWS Lambda

Fivetran: conceptual understanding only.

## Phase 6 — Big Data Fundamentals

**Status: VERY DEEP**

- Vertical vs horizontal scaling
- Distributed storage
- Distributed computation
- Partitioning
- Parallelism
- Replication
- Fault tolerance
- Data locality
- Serialization
- Network I/O
- Shuffle
- Cluster architecture

Technology mapping:

- HDFS
- Snowflake
- BigQuery
- Databricks

AWS remains the primary hands-on ecosystem.

## Phase 7 — Apache Spark

**STATUS: ALREADY LEARNING — DO NOT RESTART**

Do not repeat beginner Spark API material unless a gap appears.

Deepen:

- Driver
- Executors
- Cluster manager
- Jobs
- Stages
- Tasks
- DAG
- Partitions
- Shuffle
- Broadcast
- Cache
- Persistence
- Serialization
- Catalyst
- Tungsten
- AQE
- Join strategies
- Partition strategies
- Memory management
- Fault tolerance
- Performance tuning
- Logical plans
- Physical plans

Use the existing PySpark learning as the starting point.

## Phase 8 — Kafka & Real-Time Processing

**STATUS: LEARN FROM BASIC**

- Producer
- Consumer
- Broker
- Topic
- Partition
- Offset
- Consumer group
- Replication
- Retention
- Ordering
- Consumer lag
- Delivery semantics
- At-most-once
- At-least-once
- Exactly-once concepts
- Idempotent consumers
- Backpressure
- Spark Structured Streaming
- Checkpoints
- Stateful processing
- Watermarks

AWS mapping: Amazon MSK and Kinesis concepts.

## Phase 9 — System Design for Data Engineering

**STATUS: VERY DEEP**

```text
Requirements
     ↓
Scale / Capacity
     ↓
Latency
     ↓
Ingestion
     ↓
Storage
     ↓
Processing
     ↓
Serving
     ↓
Reliability
     ↓
Security
     ↓
Monitoring
     ↓
Cost
```

Topics:

- Batch vs Streaming
- Lambda architecture
- Kappa architecture
- Ingest → Process → Store → Serve
- Scalability
- Availability
- Reliability
- Fault tolerance
- Durability
- Consistency
- Latency
- Throughput
- Idempotency
- Backpressure
- Partitioning
- Replication
- Caching

Design exercises:

- Logistics batch pipeline
- Near-real-time parcel tracking
- Uber-style trip pipeline
- Netflix-style data platform
- Final logistics platform

## Phase 10 — AWS Data Engineering

**STATUS: PRODUCTION-ORIENTED DEEPENING**

Core services:

- S3
- RDS
- Glue
- DMS
- Lambda
- EMR
- Athena
- Redshift
- IAM
- KMS
- CloudWatch
- CloudTrail

Focus on architecture decisions, service selection, security, reliability, failure handling, monitoring, cost and integration.

Do not spend time relearning basic service definitions.

GCP and Azure are only mapped conceptually to AWS equivalents.

## Phase 11 — DevOps for Data Engineering

**STATUS: PRACTICAL**

- Git
- GitHub
- Branching
- Pull Requests
- Code Review
- CI/CD
- Docker
- Dockerfile
- Images
- Containers
- Environment variables
- Terraform
- Providers
- Resources
- Variables
- Outputs
- State

Kubernetes: conceptual architecture and basic operational understanding.

## Phase 12 — DSA

**STATUS: INTERVIEW TRACK**

High priority:

- Time complexity
- Space complexity
- Arrays
- Strings
- Hashing
- Sorting
- Binary Search
- Two Pointers
- Stacks
- Queues
- Recursion
- Linked Lists
- Trees
- Graphs
- Heap / Priority Queue

Lower priority:

- Backtracking
- Bit manipulation
- Advanced DP
- Advanced graph algorithms

Goal: choose appropriate data structures and algorithms and explain complexity during Data Engineering interviews.

## Phase 13 — GenAI / RAG / Agentic AI

**STATUS: REVISION**

GenAI:

- LLM basics
- APIs
- Tokens
- Context
- Cost
- Prompt engineering
- Structured output
- Function calling

RAG:

```text
Documents
   ↓
Chunking
   ↓
Embeddings
   ↓
Vector Database
   ↓
Retrieval
   ↓
LLM
   ↓
Answer
```

Agentic AI:

```text
Agent
  ↓
Reason
  ↓
Choose tool
  ↓
Retrieve data
  ↓
Execute action
  ↓
Return result
```

Focus on the Data Engineer's role in AI data systems.

# Final Capstone — Logistics Data Platform

```text
                    DATA SOURCES
                         │
            ┌────────────┼────────────┐
            ↓            ↓            ↓
          CSV           API       Event Stream
            │            │            │
            └────────────┼────────────┘
                         ↓
                  S3 RAW / BRONZE
                         ↓
                     AIRFLOW
                   ORCHESTRATION
                         ↓
                  GLUE / SPARK
                    PROCESSING
                         ↓
                ┌────────┴────────┐
                ↓                 ↓
            S3 SILVER          S3 GOLD
                │                 │
                └────────┬────────┘
                         ↓
                  ATHENA / REDSHIFT
                         ↓
                    BI / REPORTING
```

Later add Kafka/MSK + Spark Structured Streaming for real-time parcel tracking.

Infrastructure track:

```text
GitHub
   ↓
CI/CD
   ↓
Docker
   ↓
Terraform
   ↓
AWS Infrastructure
```

# Learning Notebook Standard

Each completed topic gets handwritten-style revision notes.

Example:

```text
╔══════════════════════════════════════╗
║       DATA ENGINEERING              ║
╚══════════════════════════════════════╝

DE = BUILD SYSTEMS FOR DATA

SOURCE
  ↓
INGEST
  ↓
STORE
  ↓
PROCESS
  ↓
SERVE
  ↓
ANALYTICS / ML / APPLICATION

Remember:
Raw data should be preserved.

Why?
→ Audit
→ Debug
→ Replay
→ Backfill
→ Reprocess
```

# Course Progress

```text
Phase 0   █░░░░░░░░░░  STARTING NOW
Phase 1   ░░░░░░░░░░░  Python Revision
Phase 2   ░░░░░░░░░░░  DBMS
Phase 3   ░░░░░░░░░░░  Data Modeling
Phase 4   ░░░░░░░░░░░  Warehousing
Phase 5   ░░░░░░░░░░░  ETL / ELT
Phase 6   ░░░░░░░░░░░  Big Data
Phase 7   ░░░░░░░░░░░  Spark Deepening
Phase 8   ░░░░░░░░░░░  Kafka / Streaming
Phase 9   ░░░░░░░░░░░  System Design
Phase 10  ░░░░░░░░░░░  AWS
Phase 11  ░░░░░░░░░░░  DevOps
Phase 12  ░░░░░░░░░░░  DSA
Phase 13  ░░░░░░░░░░░  GenAI / RAG
Capstone  ░░░░░░░░░░░  Logistics Platform
```

# Class 1 — Data Engineering Mental Model

## Core idea

A company continuously generates data from many sources:

```text
Customers
Parcels
Drivers
Trucks
Trailers
Trips
Sorting Centers
Transport Centers
Parcel Events
Maintenance
Delivery Performance
```

This information does not naturally exist as one clean table.

A Data Engineer builds systems that make this data available, reliable, clean, consistent, scalable and usable.

Core flow:

```text
SOURCE
  ↓
INGESTION
  ↓
STORAGE
  ↓
PROCESSING
  ↓
SERVING
  ↓
CONSUMERS
```

Consumers can be:

- BI
- Analytics
- Applications
- Data Science
- Machine Learning
- GenAI

## Why do we need each layer?

### Source

Where original data is generated.

Examples:

- Application database
- CSV
- API
- IoT device
- Kafka event
- External system

### Ingestion

Moves data from the source into the Data Platform.

Examples:

- AWS DMS
- AWS Glue
- Lambda
- Kafka
- Kinesis
- Airflow

### Storage

Where data is persisted.

Examples:

- S3
- RDS
- Redshift

### Processing

Where data is cleaned, validated and transformed.

Examples:

- PySpark
- Spark
- AWS Glue
- dbt
- SQL

### Serving

Makes processed data available to consumers.

Examples:

- Athena
- Redshift
- APIs
- BI tools
- Data marts

## The important mental model

```text
             DATA PLATFORM

SOURCE
  │
  │ Extract
  ↓
INGESTION
  │
  │ Store raw
  ↓
BRONZE / RAW
  │
  │ Transform
  ↓
SILVER / CLEAN
  │
  │ Business logic
  ↓
GOLD / CURATED
  │
  ↓
SERVING
  │
  ├── BI
  ├── Analytics
  ├── ML
  └── Applications
```

## Why preserve raw data?

Raw data represents what actually arrived from the source.

If a source sends an incorrect value, we should not immediately overwrite the original record.

Instead:

```text
SOURCE
  ↓
RAW
  ↓
VALIDATE
  ↓
CORRECT / TRANSFORM
  ↓
PROCESSED
```

Keeping the original enables:

- Debugging
- Auditing
- Reprocessing
- Backfills
- Data quality investigations
- Recovery

# Handwritten Notes — Class 1

```text
╔══════════════════════════════════════╗
║       CLASS 1 — DATA ENGINEERING     ║
╚══════════════════════════════════════╝

DE = BUILD SYSTEMS FOR DATA

SOURCE
  ↓
INGEST
  ↓
STORE
  ↓
PROCESS
  ↓
SERVE
  ↓
CONSUMER

Source
──────
Where data is CREATED.

Ingestion
─────────
How data enters our platform.

Storage
───────
Where data is PERSISTED.

Processing
──────────
Where data is CLEANED /
VALIDATED / TRANSFORMED.

Serving
───────
Where processed data becomes
AVAILABLE to consumers.

IMPORTANT
─────────
Keep RAW data.

Why?
→ Audit
→ Debug
→ Replay
→ Backfill
→ Reprocess

Remember:

Raw ≠ useless

Raw = source of truth
for what actually arrived.
```

# Class 1 Checkpoint

Answer these in your own words before moving to DBMS:

1. What is a source system in our logistics project?
2. What is the difference between a source and an ingestion layer?
3. Why do we preserve raw data?
4. What is the purpose of the silver/processed layer?
5. Give three possible consumers of our processed logistics data.
6. If `parcel_events.csv` contains 1,000 duplicate events, at which layer would you detect and handle duplicates, and why?

The instructor will review the answers before Class 2: **Data → Database → DBMS → RDBMS**.
