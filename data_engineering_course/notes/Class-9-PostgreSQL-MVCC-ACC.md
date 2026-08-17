╔══════════════════════════════════════════════╗
║     POSTGRESQL + MVCC + CONCURRENCY          ║
╚══════════════════════════════════════════════╝


POSTGRESQL
──────────

Primary concurrency model:

MVCC

        ↓

Multiple versions
        +
Visibility rules
        +
Snapshots


NORMAL SELECT
─────────────

T1 → UPDATE P001
        ↓
new version

T2 → SELECT P001
        ↓
MVCC visibility
        ↓
appropriate committed version

Reader does NOT simply
wait for writer.


EXPLICIT LOCK
─────────────

SELECT ... FOR UPDATE

        ↓

Explicit row-level conflict
        ↓
May WAIT


MVCC COST
─────────

UPDATE
  ↓
New version
  ↓
Old version retained
  ↓
Dead tuples
  ↓
VACUUM / AUTOVACUUM
  ↓
Cleanup


ACC
───

Adaptive Concurrency Control

Question:

"How much concurrent work
should we allow RIGHT NOW?"


Healthy
  ↓
Increase concurrency


Contention
  ↓
Reduce concurrency


ACC ≠ MVCC

MVCC
→ Which version can I see?

ACC
→ How much concurrent work
  should I allow?


OCC
───

Optimistic Concurrency Control

Proceed optimistically
       ↓
Check conflicts
       ↓
At commit
       ↓
Conflict?
       ↓
Abort + Retry

╔════════════════════════════════════════════╗
║   MVCC + OCC + ACC — FINAL REVISION       ║
╚════════════════════════════════════════════╝


MVCC
────

Multi-Version Concurrency Control

Question:

"Which version of this data
can my transaction see?"

        ↓

Multiple versions
        +
Visibility / Snapshot
        ↓
Appropriate committed version


NORMAL SELECT
─────────────

T1 → UPDATE
     ↓
new version
     ↓
uncommitted

T2 → SELECT
     ↓
MVCC visibility
     ↓
old committed version


IMPORTANT:

MVCC ≠ No Locks

MVCC reduces unnecessary
reader/writer blocking.

Writers can still conflict.


SELECT FOR UPDATE
─────────────────

Explicit row lock

SELECT ... FOR UPDATE

        ↓

Transaction wants
the row + lock

        ↓

Can WAIT if another
transaction holds conflict.


OCC
───

Optimistic Concurrency Control

Proceed optimistically
        ↓
Check conflicts
        ↓
Conflict?
   ↓
Abort / Retry


ACC
───

Adaptive Concurrency Control

Observe system
        ↓
Contention / load
        ↓
Adjust concurrency
        ↓
More or less concurrent work


MEMORY:

MVCC
→ Which VERSION can I see?

OCC
→ What if transactions CONFLICT?

ACC
→ How much CONCURRENCY should
  I allow right now?