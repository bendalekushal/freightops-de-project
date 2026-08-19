╔══════════════════════════════════════════╗
║             B-TREE INDEX                 ║
╚══════════════════════════════════════════╝

B-TREE
──────

Balanced
+
Ordered
+
Tree structure

        ↓

Efficient key searching


CONCEPTUAL:

             ROOT
              │
       ┌──────┴──────┐
       ↓             ↓
   INTERNAL       INTERNAL
       │             │
       ↓             ↓
     LEAF          LEAF

LEAF
→ sorted index entries


GOOD FOR:

=
<
>
<=
>=
BETWEEN
ORDER BY


WHY?

B-tree maintains
ordered keys.


SEARCH:

Query
 ↓
Root
 ↓
Branch
 ↓
Leaf
 ↓
Index entry
 ↓
Table tuple


B-TREE vs HASH

B-Tree
→ equality
→ range
→ ordering

Hash
→ equality-oriented


IMPORTANT:

Index ≠ table

Index contains
indexed key + row reference
(conceptually)


B-TREE ≠ MAGIC

Planner may still choose:

Sequential Scan

if that is estimated
to be cheaper.

╔══════════════════════════════════════════╗
║        B-TREE — CHECKPOINT               ║
╚══════════════════════════════════════════╝

WHY B-TREE?

Sequential Scan
      ↓
Many rows examined

B-Tree
      ↓
Navigate tree
      ↓
Reduce search space
      ↓
Find relevant key


RANGE QUERY
───────────

Find starting key
      ↓
Traverse ordered leaves
      ↓
Read relevant range
      ↓
Stop


LOW CARDINALITY
───────────────

5 unique values
+
10M rows

        ↓

Predicate may match
large portion of table

        ↓

Many index entries
+
Many table fetches

        ↓

Sequential Scan may be cheaper


IMPORTANT:

B-Tree itself isn't
necessarily "slow".

The issue is often:
LOW SELECTIVITY
+
HIGH ROW FETCH COST


LEAF LEVEL
──────────

Bottom level

Contains:
→ indexed keys
→ tuple references


INDEX ENTRY ≠ FULL ROW

Index Scan:

B-Tree
 ↓
Index entry
 ↓
Table tuple
 ↓
Full row


Index Only Scan:

B-Tree
 ↓
Required data available
from index
 ↓
Potentially no table fetch