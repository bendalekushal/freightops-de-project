╔════════════════════════════════════════════╗
║            ACID PROPERTIES                 ║
╚════════════════════════════════════════════╝


ACID
────

A → Atomicity
C → Consistency
I → Isolation
D → Durability


══════════════════════════════════════════════

A — ATOMICITY
─────────────

"ALL OR NOTHING"

Transaction:

  Step 1 ✓
      ↓
  Step 2 ✓
      ↓
  Step 3 ✓
      ↓
    COMMIT


If any step fails:

  Step 1 ✓
      ↓
  Step 2 ✓
      ↓
  Step 3 ✗
      ↓
   ROLLBACK
      ↓
  No partial commit


Think:

Transaction completeness


══════════════════════════════════════════════

C — CONSISTENCY
───────────────

"VALID → VALID"

Before transaction
       ↓
   VALID STATE
       ↓
  TRANSACTION
       ↓
   VALID STATE


Database rules must remain valid.

Examples:

→ Primary Key
→ Foreign Key
→ NOT NULL
→ UNIQUE
→ CHECK
→ Data types
→ Business rules


Think:

Database integrity


══════════════════════════════════════════════

I — ISOLATION
─────────────

"CONCURRENT TRANSACTIONS"

Transaction A
      │
      ↓
   DATABASE
      ↑
      │
Transaction B


Transactions should not
interfere in an unsafe way.

Later:

→ Dirty Read
→ Non-repeatable Read
→ Phantom Read

Isolation levels:

→ Read Uncommitted
→ Read Committed
→ Repeatable Read
→ Serializable


Think:

Concurrent transaction behavior


══════════════════════════════════════════════

D — DURABILITY
──────────────

"COMMITTED = SURVIVES FAILURE"

Transaction
     ↓
   COMMIT ✓
     ↓
System crashes
     ↓
   RECOVERY
     ↓
Committed data remains ✓


Usually supported by:

→ Transaction logs
→ Recovery mechanisms
→ Persistent storage


Think:

Committed data is recoverable


══════════════════════════════════════════════

QUICK MEMORY TRICK
──────────────────

A → All or Nothing

C → Correct / Valid State

I → Independent Concurrent Transactions

D → Doesn't disappear after COMMIT

The safest interview definitions are:

A → All-or-nothing transaction
C → Preserve database validity/integrity
I → Control concurrent transaction interaction
D → Preserve committed changes after failure

╔══════════════════════════════════════════╗
║     CONCURRENCY ANOMALIES — FINAL        ║
╚══════════════════════════════════════════╝


1. DIRTY READ
─────────────

T1 → UPDATE
      ↓
   NOT COMMITTED
      ↓
T2 → READ
      ↓
❌ Reads UNCOMMITTED data


KEY:
UNCOMMITTED VALUE


────────────────────────────────────────────


2. NON-REPEATABLE READ
───────────────────────

T2 → READ P001
      ↓
  IN_TRANSIT

T1 → UPDATE P001
      ↓
    COMMIT

T2 → READ P001
      ↓
   DELIVERED


KEY:
SAME ROW
DIFFERENT VALUE


────────────────────────────────────────────


3. PHANTOM READ
───────────────

T2 → QUERY
      ↓
  P001, P002

T1 → INSERT P003
      ↓
    COMMIT

T2 → SAME QUERY
      ↓
  P001, P002, P003


KEY:
DIFFERENT ROW SET


════════════════════════════════════════════

MEMORY:

DIRTY
  → UNCOMMITTED DATA

NON-REPEATABLE
  → SAME ROW
    DIFFERENT VALUE

PHANTOM
  → DIFFERENT ROW SET