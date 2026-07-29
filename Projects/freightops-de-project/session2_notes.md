# Interview Prep Notes — Session 2 (Glue Catalog, Athena, Cross-Region Debugging)

## 1. Glue Data Catalog & Crawler
- **Glue Catalog** = metadata only (table names, columns, types, S3 location) — not the data itself. Without it, Athena can't see your files as tables at all.
- **Glue Crawler** = scans S3, infers schema automatically, registers it in the catalog. Re-run periodically to catch schema evolution (new/changed columns from source systems).
- **Glue needs its own IAM role** (not your personal IAM user) — a service-linked identity, trusted specifically to be assumed by `glue.amazonaws.com`.
- **Real, verified finding:** the crawler inferred `contract_start_date` as `string`, not `date` — because the source format (`DD-MM-YYYY`) isn't standard. Numeric columns (`credit_terms_days`, `annual_revenue_potential`) inferred correctly as `bigint`. **This is concrete evidence for why date standardization has to happen in Silver, not be assumed** — a real finding, not a hypothetical.
- **Interview line:** *"My crawler inferred a date column as a string because the source format was ambiguous — that's exactly the kind of thing that has to get fixed in the Silver layer before any date-based logic can run."*

## 2. Athena
- Athena is a **query engine, not a database** — every query result gets written to an S3 location you specify; Athena doesn't store anything itself.
- **Real bug hit today: cross-region mismatch.** Data bucket was in `us-east-1` (created without an explicit `--region` flag the very first time), but Glue Catalog/CLI default region was `ap-south-1`. Crawler could still read cross-region fine — but **Athena's results bucket must be in the exact same region as the query.**
- **AWS quirk:** creating a bucket in `us-east-1` doesn't require `--create-bucket-configuration`; every other region does (e.g. `LocationConstraint=ap-south-1`). Missing this is a common real error.
- **How to check a bucket's actual region:** `aws s3api get-bucket-location --bucket <name>` — a blank/null result specifically means `us-east-1` (a known AWS quirk, not a broken command).
- **Interview line:** *"I hit a cross-region mismatch because my first bucket was created without an explicit region — good reminder that region should always be explicit from the very first resource, not assumed."*
- **Verified end-to-end today:** S3 → Glue Crawler → Glue Catalog → Athena SQL query → `SELECT COUNT(*) FROM trips` returned exactly 85,410 — matching the number from Phase 0. Real proof the whole chain works, not just individual pieces.

## 3. IAM — Least Privilege in Practice (hit twice today)
- Hit `AccessDenied` twice: once creating the Glue role (`iam:CreateRole`), once starting an Athena query (`athena:StartQueryExecution`) — both times because `freightops-dev` only had the specific permissions granted earlier, nothing more.
- **This is least privilege working correctly, not a bug** — a scoped user shouldn't silently have permissions nobody explicitly granted.
- **Real production distinction to know:** in a real company, a developer usually *can't* self-grant new IAM permissions (that's restricted to a platform/infra team or IaC). We used root once, narrowly, to bootstrap — a legitimate but deliberately limited use, not a pattern to repeat casually.
- **Interview line:** *"I hit AccessDenied errors while building this and treated them as confirmation the least-privilege setup was working — not something to just bypass with AdministratorAccess."*

## 4. Git / Environment Mistakes — Real, Concrete Lessons
| Mistake | Root Cause | Lesson |
|---|---|---|
| `.gitignore` had no effect; all 14 raw CSVs got committed | File was actually saved as `gitignore` (no leading dot) — Windows/VS Code silently dropped it | **Always verify a config file exists with the exact right name** (`cat .gitignore`, or `dir -Force` to reveal hidden/dotfiles) before assuming it's protecting anything |
| `git push` failed with HTTP 408 (timeout) | Pushing 14MB of CSVs (from the mistake above) over an unstable/slow connection | `git rm --cached` stops *future* tracking but does **not** remove already-committed data from history — the push size doesn't shrink until history itself is rewritten (`git filter-repo`, not done today — deliberately deferred, not urgent for non-sensitive synthetic data) |
| PowerShell inline JSON in AWS CLI commands kept breaking (quoting/escaping errors) | PowerShell's quote-escaping rules differ from bash | **Real, reliable fix: write JSON to a file, reference it with `file://path.json`** instead of fighting inline escaping — this is AWS's own recommended pattern, not just a workaround |
| Several commands (`attach-role-policy`, `create-database`) returned zero output | Normal — many AWS CLI write operations are silent on success | **Never assume silence = failure or success — always verify with a corresponding `get-*`/`list-*` command** |

## 5. General Engineering Habits (reinforced again today)
- Verify a fix at the source (`dir -Force` to actually see the misnamed file) rather than guessing and retrying blindly.
- A command "running without error" ≠ "did what you expected" — always confirm with an independent check (row counts, `get-table`, `get-query-results`).
- Real infra debugging is rarely one clean fix — today involved IAM permission gaps, region mismatches, and a file-naming mistake, all in one session. That's normal, not a sign of doing it wrong.