╔══════════════════════════════════════════╗
║        MVCC — MULTI-VERSION             ║
║        CONCURRENCY CONTROL               ║
╚══════════════════════════════════════════╝


MVCC
────

Multiple Versions
       +
Visibility Rules
       +
Transaction/Snapshot
       ↓
Concurrent access


Example:

P001

Version 1
─────────
IN_TRANSIT
   ↑
   │
T2 can see old
committed version


Version 2
─────────
DELIVERED
   ↑
   │
T1 is modifying
newer version


T1 → newer version
T2 → visible committed version


KEY IDEA:

Reader does not always
need to wait for writer.


MVCC ≠ No Locks

Real databases may use:

MVCC + LOCKS


Think:

LOCKING
→ Who can access/change?


MVCC
→ Which version can
  this transaction see?


  ╔══════════════════════════════════════════╗
║        LOCKING vs MVCC                   ║
╚══════════════════════════════════════════╝

LOCKING
────────

Question:

"Can this transaction
access/change this resource?"

Uses:
→ Shared locks
→ Exclusive locks
→ Lock compatibility
→ Blocking
→ Deadlock handling


MVCC
────

Question:

"Which VERSION of this data
can this transaction see?"

Uses:
→ Multiple row versions
→ Visibility rules
→ Snapshots
→ Transaction information


IMPORTANT:

MVCC ≠ No Locks

Real databases may use:

        MVCC
          +
        LOCKS
          ↓
   Concurrency Control