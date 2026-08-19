╔══════════════════════════════════════════╗
║       SQL INDEXING — FUNDAMENTALS        ║
╚══════════════════════════════════════════╝

WHY INDEX?

Without index:

Query
  ↓
Sequential Scan
  ↓
Check many rows
  ↓
Find match


With useful index:

Query
  ↓
INDEX
  ↓
Locate matching entry
  ↓
Find table row


INDEX
─────
Separate data structure
used to speed up access
to table data.


IMPORTANT:

Index ≠ Table

Index helps locate data.


DEFAULT POSTGRESQL INDEX
─────────────────────────

B-Tree


Useful for:

=
<
>
<=
>=
BETWEEN
ORDER BY


INDEX TRADE-OFF
────────────────

Reads
  ↓
Often faster ✓

BUT

INSERT
UPDATE
DELETE
  ↓
Indexes may need maintenance

Therefore:

More indexes
→ More storage
→ More write overhead
→ More maintenance


SELECTIVITY
───────────

High selectivity
→ small number of
  matching rows
→ index often useful


Low selectivity
→ large number of
  matching rows
→ index may be less useful


KEY MEMORY:

INDEX
→ Faster READS

INDEX
→ More WRITE COST


INDEX EXISTS
≠
INDEX WILL ALWAYS BE USED

╔══════════════════════════════════════╗
║ CARDINALITY vs SELECTIVITY           ║
╚══════════════════════════════════════╝

CARDINALITY
→ DISTINCTNESS of the column

parcel_id
→ 10M distinct
→ High cardinality

status
→ 3 distinct
→ Low cardinality


SELECTIVITY
→ How much a QUERY FILTER
  narrows the rows

WHERE parcel_id = P001
→ ~1 row
→ High selectivity

WHERE status = DELIVERED
→ 60% rows
→ Low selectivity