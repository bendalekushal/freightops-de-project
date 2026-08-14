# Interview Prep Notes — Session 6 (Partitioning, Skew, Salting)

## 1. Partitions — the basics
- Spark splits data into chunks called partitions, spread across workers to run in parallel.
- Checked with: `df.rdd.getNumPartitions()`
- On our `trips` table: 2 partitions, split purely by file size (not by any column), so counts were nearly even (42,834 / 42,576).

## 2. Skew — what it actually is, shown with real data
- Skew = one partition ends up with way more data than the others. The job's total time is however long the biggest partition takes — other workers just sit idle once they're done.
- **Made it happen on purpose:** repartitioned `trips` by `trip_status`, a column where every single row has the same value ("Completed"). Result: all 85,410 rows landed in ONE partition; the other 3 didn't even show up in the results (an empty partition has nothing to count, so it's just missing from the output, not shown as 0).
- Real interview-ready example: "I created skew on purpose by partitioning on a column with only one value, and saw 100% of the data land in a single partition while three sat empty."

## 3. Fixing skew — three real approaches
1. **Salting** — add a random extra column to force spreading (details below). Used when you need manual control or an older Spark version.
2. **Broadcast join** — for skew that shows up during a join specifically, when one side is small. Already used this earlier for `customers` + `loads`.
3. **Adaptive Query Execution (AQE)** — Spark's built-in automatic fix, on by default since Spark 3.0. Detects and splits oversized partitions on its own, no extra code needed.
- **Real-world order of preference:** AQE first (free, automatic), salting when AQE isn't enough or on older Spark, broadcast specifically for skewed joins.

## 4. Salting — implemented and verified
- Added a random column: `F.rand() * N`, cast to int — this is the "salt."
- Repartitioned using both the skewed column AND the salt column together.
- **First attempt failed:** used only 4 possible salt values (0-3) for 4 partitions — got uneven results (one partition with double the data, another with zero). Fixed by increasing to 20 possible salt values — result came out roughly even across all 4 partitions.

## 5. How hashing and "divide, take the remainder" actually works — plain explanation
- Spark needs to decide, for every row, which of the 4 partitions it goes into.
- Step 1: it runs the row's values (in our case, `trip_status` + `salt`) through a **hash function** — this just means turning any input into some number. Same input always gives the same number, every time.
- Step 2: it takes that number and divides it by however many partitions you asked for (4, here) and looks at the **remainder** — the leftover after dividing evenly. A remainder after dividing by 4 is always 0, 1, 2, or 3.
- That remainder is literally which partition number the row goes into.
- **Why few salt values caused problems:** with only 4 different salt values, you only get 4 different hash numbers. It's possible for two totally different numbers to happen to leave the *same* remainder when divided by 4 — like 17 and 9 both leaving remainder 1. That's a collision — two different values landing in the same partition by coincidence, leaving another partition empty.
- **Why more salt values fixed it:** with 20 different salt values instead of 4, you get about 20 different hash numbers going through the "divide by 4, take the remainder" step. Spread across only 4 possible remainders, they average out much more evenly — same 4 buckets, just less chance of an unlucky pile-up.
- **One-line version to remember:** more variety going in makes the divide-and-remainder trick land more evenly across the buckets you have — same number of buckets, just fewer coincidental collisions.
