# Claim-by-claim reproduction: private and robust alignment

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/MachineLearning-Nerd/icml26-repro-r3PKGNlKET-improved-bounds-for-private-and-robust-alignment/blob/main/notebooks/reproduction.py)

We audited all six claims selected by the evaluator for
[*Improved Bounds for Private and Robust Alignment*](https://arxiv.org/abs/2512.23816).
Five are **VERIFIED** by proof-level executable certificates. Claim 5 is
**FALSIFIED as written**: its `c(epsilon)/sqrt(T)` PrivXPO rate verifies, but
arXiv:2510.13512 described an online locally-private preference-alignment
algorithm before this paper, contradicting the claim’s broad “first online”
conjunct. This is a forecast, not a new judge score; the previous live score
remains **0/12** until the evaluator assesses the published revision.

The central observed numbers are exact rather than fitted slopes:
randomized response contracts total variation by `1/c(epsilon)`; at
`exp(epsilon)=3`, `c=2`, CTL bias is `2 alpha`, and the exhibited LTC bias is
`3 alpha` (bounded by `4 alpha`). The offline theorem algebra gives
`c sqrt(log|Pi|/n)` and `c sqrt(log|Pi|/n)+alpha`. No GPU was used. Short
symbolic checks ran locally on one core; the uncertain-runtime named-algorithm
suite ran on Hugging Face `cpu-upgrade` (8 vCPU allocation, 0.42 s runner
wall time). Finite fixtures are implementation checks, not substitutes for
the universal derivations.

- [Illustrated technical report](reports/reproduction/report.md)
- [Self-contained tutorial notebook](notebooks/reproduction.py)
- [Evaluator-visible evidence surface](space/pages/current/page.md)

## Experiment log

Every experiment inherited the exact command
`uv run --frozen python -m reproduction.runner`.

| Branch / experiment | Purpose or change | Exact run command | Assessment / outcome | Compute |
| --- | --- | --- | --- | --- |
| [`orx/historical-judged-baseline-audit`](https://github.com/MachineLearning-Nerd/icml26-repro-r3PKGNlKET-improved-bounds-for-private-and-robust-alignment/tree/orx/historical-judged-baseline-audit) | Freeze and audit the judged 0/12 artifact | `uv run --frozen python -m reproduction.runner` | Historical evidence gate correctly fails; no scientific claim inferred | local CPU, 1 core |
| [`orx/exact-privacy-factor-and-lower-bound-certificate`](https://github.com/MachineLearning-Nerd/icml26-repro-r3PKGNlKET-improved-bounds-for-private-and-robust-alignment/tree/orx/exact-privacy-factor-and-lower-bound-certificate) | Claim 3 identity, estimator, and minimax certificate | `uv run --frozen python -m reproduction.runner` | Claim 3 VERIFIED | local CPU, 1 core, 0.10 s |
| [`orx/exact-uniform-convergence-and-corruption-order-c`](https://github.com/MachineLearning-Nerd/icml26-repro-r3PKGNlKET-improved-bounds-for-private-and-robust-alignment/tree/orx/exact-uniform-convergence-and-corruption-order-c) | Claims 1, 2, and 4 symbolic certificates | `uv run --frozen python -m reproduction.runner` | Claims 1, 2, and 4 VERIFIED | local CPU, 1 core, 0.30 s |
| [`orx/named-offline-and-online-alignment-algorithm-cer`](https://github.com/MachineLearning-Nerd/icml26-repro-r3PKGNlKET-improved-bounds-for-private-and-robust-alignment/tree/orx/named-offline-and-online-alignment-algorithm-cer) | Claims 5 and 6 named algorithms, rates, and novelty audit | `uv run --frozen python -m reproduction.runner` | Claim 5 FALSIFIED; Claim 6 VERIFIED | HF `cpu-upgrade`, 8 vCPU, 0.42 s |
| [`orx/evaluator-visible-release-candidate-and-red-team`](https://github.com/MachineLearning-Nerd/icml26-repro-r3PKGNlKET-improved-bounds-for-private-and-robust-alignment/tree/orx/evaluator-visible-release-candidate-and-red-team) | Cumulative regression and evaluator-blind release gates | `uv run --frozen python -m reproduction.runner` | Candidate release surface | local CPU, 1 core |
| `main` | Publication surface | Not run as an experiment (publication surface) | README, report, notebook, and exact published text mirror | none |

## Reproduce locally

Install [uv](https://docs.astral.sh/uv/), then run:

```bash
uv sync --frozen
uv run --frozen python -m reproduction.runner
uv run marimo check notebooks/reproduction.py
```

The runner exits nonzero if a certificate, independent checker, negative
control, raw-data consistency check, or release-surface gate fails.

---

# Upstream workspace

ICML 2026 agent reproduction workspace for r3PKGNlKET.
