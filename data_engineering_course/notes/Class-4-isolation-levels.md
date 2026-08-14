╔══════════════════════════════════════════╗
║        ISOLATION LEVELS — FINAL          ║
╚══════════════════════════════════════════╝

1. READ UNCOMMITTED
───────────────────
Weakest

Can read uncommitted data.

Dirty Read → POSSIBLE


2. READ COMMITTED
─────────────────
Reads committed data.

Dirty Read → PREVENTED

Non-Repeatable Read
→ POSSIBLE


3. REPEATABLE READ
──────────────────
Repeated reads of a row
remain consistent.

Dirty Read → PREVENTED

Non-Repeatable Read
→ PREVENTED


4. SERIALIZABLE
────────────────
Strongest standard level.

Concurrent execution should
behave as if transactions
were executed serially.

Strongest protection
        ↓
Potentially more
contention / conflicts /
waiting / retries


IMPORTANT:

Don't choose isolation
based only on DATA SIZE.

Choose based on:

→ Business correctness
→ Concurrency
→ Latency
→ Throughput
→ Database implementation
→ Workload