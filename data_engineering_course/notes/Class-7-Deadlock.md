╔══════════════════════════════════════════╗
║              DEADLOCK                    ║
╚══════════════════════════════════════════╝

DEADLOCK
────────

Two or more transactions
wait for each other.

Example:

T1:
LOCK P001
  ↓
WANTS P002
  ↓
WAIT


T2:
LOCK P002
  ↓
WANTS P001
  ↓
WAIT


T1 → waits for T2
T2 → waits for T1

       ↓

      CYCLE
       ↓

   DEADLOCK


BLOCKING ≠ DEADLOCK

Blocking:
T2 waits for T1
T1 finishes
T2 continues


Deadlock:
T1 waits for T2
T2 waits for T1
Neither can continue


HOW TO REDUCE:

→ Consistent lock order
→ Short transactions
→ Avoid unnecessary locks
→ Appropriate lock granularity
→ Retry with backoff
→ Deadlock detection

The most important diagram

              LOCKING
                 │
       ┌─────────┴─────────┐
       ↓                   ↓
    BLOCKING            DEADLOCK
       │                   │
       ↓                   ↓
T2 waits for T1       T1 waits for T2
       │                   ↑
       ↓                   │
T1 finishes            T2 waits for T1
       │                   │
       ↓                   │
T2 continues           ❌ CYCLE