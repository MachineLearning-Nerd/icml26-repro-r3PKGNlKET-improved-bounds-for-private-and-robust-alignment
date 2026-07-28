# Current verification

This page supersedes the one-line assertions in the **Historical rejected
baseline**. Current evidence is additive and uses the fixed command:

```text
uv run --frozen python -m reproduction.runner
```

| Claim | Canonical page | Status |
| --- | --- | --- |
| 1 | [Standard private MLE log loss](../claims/claim-1/page.md) | VERIFIED |
| 2 | [Improved square-loss corruption powers](../claims/claim-2/page.md) | VERIFIED |
| 3 | [Privacy factor and optimality](../claims/claim-3/page.md) | VERIFIED |
| 4 | [Corruption/privacy ordering](../claims/claim-4/page.md) | VERIFIED |
| 5 | [Online algorithms and PrivXPO rate](../claims/claim-5/page.md) | FALSIFIED |
| 6 | [Offline PrivChiPO and SquareChiPO rates](../claims/claim-6/page.md) | VERIFIED |

The pinned environment is Python 3.12 with `pyproject.toml` and `uv.lock`.

[Historical rejected baseline](#/overview) is preserved unchanged and is not
the current verifier.

- [Release report and score forecast](../../release/release_report.md)
- [Evaluator-blind red-team record](../../release/red_team.md)
- [Upload allowlist](../../release/upload_allowlist.txt)
- [SHA-256 upload manifest](../../release/upload_manifest.sha256)

## Evaluator-visible evidence matrix

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [Standard private MLE log loss](#/claim-1) | yes | yes | yes | yes | yes | yes | VERIFIED |
| 2 | [Improved square-loss corruption powers](#/claim-2) | yes | yes | yes | yes | yes | yes | VERIFIED |
| 3 | [Privacy factor and optimality](#/claim-3) | yes | yes | yes | yes | yes | yes | VERIFIED |
| 4 | [Corruption/privacy ordering](#/claim-4) | yes | yes | yes | yes | yes | yes | VERIFIED |
| 5 | [Online algorithms and PrivXPO rate](#/claim-5) | yes | yes | yes | yes | yes | yes | FALSIFIED |
| 6 | [Offline PrivChiPO and SquareChiPO rates](#/claim-6) | yes | yes | yes | yes | yes | yes | VERIFIED |

The matrix is also available as
[machine-readable JSON](../../release/visibility_matrix.json).
