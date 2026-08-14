╔══════════════════════════════════════════╗
║        LOCKING — SHARED vs EXCLUSIVE     ║
╚══════════════════════════════════════════╝


SHARED LOCK
───────────

S = Shared

Usually associated with READ.

Multiple readers can share
the resource.

S + S
  ↓
 ✓


EXCLUSIVE LOCK
──────────────

X = Exclusive

Used for WRITE / UPDATE.

Conflicts with:

S + X → ✗
X + S → ✗
X + X → ✗


LOCK MATRIX

          Existing
          S      X

Request S  ✓      ✗
Request X  ✗      ✗


MEMORY:

S = Share reading

X = Exclusive modification


Example:

T1 → S LOCK → READ P001
T2 → S LOCK → READ P001

       ✓


T1 → X LOCK → UPDATE P001
T2 → X LOCK → UPDATE P001

       ✗
       ↓
     WAIT


LOCKING
   ↓
Concurrency Control
   ↓
Prevents unsafe conflicts


But:

Too much locking
      ↓
Blocking
      ↓
Deadlocks
      ↓
Performance problems

╔══════════════════════════════════════════╗
║        LOCKING — CHECKPOINT              ║
╚══════════════════════════════════════════╝

T1:
X LOCK → P001


A. T2 READ P001
   S + X
      ↓
   ❌ conflict
   → traditional model: WAIT


B. T2 UPDATE P001
   X + X
      ↓
   ❌ conflict
   → WAIT / conflict


C. T2 UPDATE P002
   X(P001) + X(P002)
      ↓
   ✓ different rows
   → can proceed


D. T3 READ P001
   S + X
      ↓
   ❌ conflict
   → traditional model: WAIT


IMPORTANT:

Locking model ≠ MVCC

Traditional:
X lock can block S lock

MVCC:
Reader may read an older/
appropriate committed version
without waiting for writer.