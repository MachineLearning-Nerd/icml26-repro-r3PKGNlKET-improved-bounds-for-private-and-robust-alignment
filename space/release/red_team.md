# Evaluator-blind red-team review

## Review A — candidate before release metadata fixes

The reviewer was given only a fresh checkout of the judged Space overlaid with
the candidate text and the evaluator rubric. No repository, OpenResearch
logs, dashboard, or storage hints were supplied.

Files opened, in order:

1. `README.md`
2. `logbook.json`
3. `pages/current/page.md`
4. `pages/claims/claim-1/page.md` through
   `pages/claims/claim-6/page.md`
5. linked `evidence/claim_*/` files

The reviewer located every current verifier and could decide all six claims.
It nevertheless rejected release readiness for two discoverability gaps:
Claims 5–6 runtime files contained a placeholder instead of the actual HF
allocation/runtime, and no canonical release page exposed the score forecast,
protected-tree subset result, or exact upload manifest.

Fixes applied: actual HF run allocation and timings were inserted; objective
values were placed inline; a release-report navigation node, score forecast,
visibility JSON, protected subset record, upload allowlist, and SHA-256
manifest were added.

## Review B — repeated after fixes

The second reviewer again started at `README.md`, then opened
`pages/current/page.md`, all six claim pages, every linked contract/source
audit/method/verifier/raw/checker/control/limitation/runtime/command file, and
finally `release/release_report.md`, `release/visibility_matrix.json`,
`release/subset_check.json`, `release/upload_allowlist.txt`, and
`release/upload_manifest.sha256`.

Results:

- The current verifier is unambiguous and precedes the historical page.
- All exact claims, domains, assumptions, and quantifiers are visible.
- All six verdicts can be reached without repository or dashboard knowledge.
- Raw values appear inline and match linked JSON.
- Every checker passes; every deliberately defective control reports FAIL and
  exits nonzero.
- The fixed command, lockfile, Git SHAs, seeds, compute, and runtime are
  visible.
- Claim 5 clearly separates the verified rate, falsified broad novelty
  conjunct, and uncontradicted narrower joint-robust interpretation.
- The historical page remains reachable and is explicitly labeled
  **Historical rejected baseline**.
- No conclusion remained unverifiable from the candidate alone.

Reviewer verdicts: Claims 1, 2, 3, 4, and 6 VERIFIED; Claim 5 FALSIFIED.
All cells in the evaluator-visible visibility matrix are complete.
