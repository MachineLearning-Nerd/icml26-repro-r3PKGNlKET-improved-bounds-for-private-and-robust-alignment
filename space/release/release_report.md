# Release report

- Previous live judged score: `0/12`
- Conservative projected score range after the proposed change: `8/12–12/12`
- Best-supported possible new score: `12/12` (**forecast, not a judge result**)

## Claim summary

| Claim | Current points | Possible points | Confidence | Evidence status | Basis and remaining risk |
| --- | ---: | ---: | --- | --- | --- |
| 1 | 0 | 2 | HIGH | VERIFIED | Universal likelihood-ratio certificate, independent Decimal checker, and consequential failing control. |
| 2 | 0 | 2 | HIGH | VERIFIED | Universal square-loss derivation, exact prior comparison, and 1,600-case independent checker. |
| 3 | 0 | 2 | HIGH | VERIFIED | Matching attainable variance and estimator-independent Le Cam lower bound. |
| 4 | 0 | 2 | HIGH | VERIFIED | Exact CTL/LTC expectations and endpoint witnesses over the full stated scalar domain. |
| 5 | 0 | 2 | MEDIUM | FALSIFIED | Rate verifies; dated online locally-private RLHF counterexample falsifies the broad novelty conjunct. Narrow joint-robust novelty remains uncontradicted. |
| 6 | 0 | 2 | HIGH | VERIFIED | Named algorithms and exact theorem exponent substitutions; independent checker and failing control. |

Current total score: `0/12`. Conservative projected total score range:
`8/12–12/12`. Best-supported possible total score: `12/12`, strictly a
forecast. All six claims changed from the prior INCONCLUSIVE verdict. No claim
is BLOCKED.

Before upload, the publication action is to commit only the files in
`upload_allowlist.txt` through the Hugging Face text API to the existing Space
`DineshAI/r3PKGNlKET`. No second Space will be created.

## Frozen provenance

- Paper: arXiv:2512.23816.
- Paper HTML: `https://ar5iv.labs.arxiv.org/html/2512.23816`.
- Retrieved: `2026-07-28T17:44:34Z` with an explicit browser User-Agent.
- Paper HTML SHA-256:
  `a6f601022be169cb0651f4d4e389e233cae827109c611f79adfb7dd67fddcc0b`.
- Judged HF revision:
  `340d714e1848fb38fa63552937f6a1467560c61c`.
- Judge head: `340d714e1848fb38fa63552937f6a1467560c61c`.
- Validated baseline SHA:
  `adf154897e750dbd7a6b0e34c6c957c1ad411b44`.
- Winning scientific branch:
  `orx/named-offline-and-online-alignment-algorithm-cer`.
- Winning scientific SHA:
  `d440faf10c0884d98aa143afc167e0947f8acfdc`.
- Fixed command: `uv run --frozen python -m reproduction.runner`.
- Environment: Python `>=3.12,<3.13`, `pyproject.toml`, and `uv.lock`.
- Seeds: none; all certificates are deterministic.

## Experiment tree

1. Historical judged baseline audit — local, exact evidence-gap regression.
2. Privacy-factor and lower-bound certificate — Claim 3, local.
3. Uniform-convergence and corruption-order certificate — Claims 1, 2, 4,
   local.
4. Named online/offline algorithms and novelty audit — Claims 5, 6, Hugging
   Face `cpu-upgrade`.
5. Evaluator-visible release candidate and red-team gates — cumulative local
   regression.

## Compute and cost

The local runs were pre-estimated at one required core and under 30 seconds;
their recorded cumulative runner wall times were 0.10 and 0.30 seconds.
They incurred no external compute charge.

The Claims 5–6 suite had uncertain runtime and was routed to Hugging Face
`cpu-upgrade` as required. It requested that flavor, saw 64 logical CPUs and
an 8-core cgroup quota, and used 0.418512719 runner wall seconds and
0.041141898 process CPU seconds. The successful orchestration duration was 10
seconds. At the documented $0.0005/minute price, the successful job’s
estimated billed cost is $0.0005; exact invoice data was not exposed. One
earlier 10-second setup attempt failed before the verifier because the default
image lacked `uv`; no scientific evidence came from it.

## Historical safety and evaluator visibility

The judged 13-path manifest was recorded before modification. The historical
page is preserved byte-for-byte with SHA-256
`7612f7a7d8d7b9451b88dbf5504aac20e01a5b030a895b62e076e3c6c52f6def`
and is labeled exactly **Historical rejected baseline**. The current page and
verifiers appear first. A fresh-clone subset check and evaluator-blind
traversal are recorded in `subset_check.json` and `red_team.md`.

Every claim page directly exposes: source quantifiers and assumptions;
executable code; the fixed command and pinned environment; inline numerical
results; linked raw JSON; independent checker output; negative-control output;
limitations; Git SHA; seeds; CPU allocation; and runtime. The machine-readable
matrix is in `visibility_matrix.json`.

## Exact command ledger

Research orchestration:

```text
orx projects --json
orx runs 377abc95-d259-4aea-b6b8-2be63389c7d5
orx paper 2512.23816 --full
orx exp run 2c2e2d2e-fbe9-4d0c-b4a7-ab32c84ea205 --backend local
orx exp run 76ee44bf-83e7-4f00-ba5c-fd5cf6f1314e --backend local
orx exp run 093a8635-cc50-45fa-980d-d032bc79b0be --backend local
orx exp run 985504cc-3588-4c07-b30e-6b0a854c7ea4 --backend hf --flavor cpu-upgrade --image ghcr.io/astral-sh/uv:python3.12-bookworm
orx exp run e52f53b2-8fae-4e79-b0b1-f5b318b848e9 --backend local
```

Fixed reproduction and presentation checks:

```text
uv sync --frozen
uv run --frozen python -m reproduction.runner
uv run marimo check notebooks/reproduction.py
rsvg-convert reports/reproduction/images/claim-outcomes.svg
rsvg-convert reports/reproduction/images/privacy-contraction.svg
rsvg-convert reports/reproduction/images/corruption-order.svg
rsvg-convert reports/reproduction/images/algorithm-objectives.svg
```

Exact evidence paths are `evidence/claim_1/` through `evidence/claim_6/`.
The exact upload list and content hashes are in `upload_allowlist.txt` and
`upload_manifest.sha256`.
