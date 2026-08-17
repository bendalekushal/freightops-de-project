╔══════════════════════════════════════════╗
║         LOCK GRANULARITY                 ║
╚══════════════════════════════════════════╝

Meaning:

SIZE / SCOPE of the
resource being locked.


HIERARCHY:

DATABASE
   ↓
TABLE
   ↓
PAGE / BLOCK
   ↓
ROW


COARSE
──────

DATABASE
TABLE

Large lock
   ↓
Few locks
   ↓
Less overhead
   ↓
More blocking
   ↓
Less concurrency


FINE
────

ROW

Small lock
   ↓
More locks
   ↓
More management overhead
   ↓
Less unnecessary blocking
   ↓
More concurrency


KEY TRADE-OFF:

Coarse
→ less overhead
→ more contention


Fine
→ more overhead
→ less contention
→ higher concurrency

╔══════════════════════════════════════════╗
║      LOCK GRANULARITY — REVISION         ║
╚══════════════════════════════════════════╝

COARSE
──────

DATABASE / TABLE

✓ Fewer locks
✓ Less management overhead

❌ More contention
❌ More blocking
❌ Lower concurrency


FINE
────

PAGE / ROW

✓ More precise
✓ Less unnecessary contention
✓ Higher concurrency

❌ More locks
❌ More management overhead


KEY:

T1 → P001
T2 → P005

ROW LOCK
   ↓
Both can potentially proceed ✓


T1 → P001
T2 → P001

X + X
  ↓
❌ Conflict
  ↓
T2 waits / conflict


LOCK ESCALATION
───────────────

Many fine-grained locks
        ↓
Too much management
        ↓
Larger/coarser lock
        ↓
Fewer locks
        ↓
Potentially more contention