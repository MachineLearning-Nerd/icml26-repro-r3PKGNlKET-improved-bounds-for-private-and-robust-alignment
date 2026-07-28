# Claim 5 — online algorithms and PrivXPO rate

**FALSIFIED.** The PrivXPO rate subclaim verifies, but the compound claim's
broad “first online private alignment algorithm” subclaim has a dated,
scope-matched counterexample.

## Exact target and split verdict

[Theorem 4.8](https://ar5iv.labs.arxiv.org/html/2512.23816#S4.Thmtheorem8)
assumes policy realizability, bounded density ratios, finite `Pi`,
trajectory-level coverability, epsilon > 0, any beta > 0, and integer `T`,
with a suitable optimism parameter. Its high-probability term is

```text
kappa_cov(Pi) * c(epsilon) * sqrt(log(|Pi|T/delta)/T).
```

| Subclaim | Result |
| --- | --- |
| PrivXPO has the stated rate | VERIFIED |
| first online algorithm for private preference alignment | FALSIFIED |
| first online algorithm jointly handling privacy and corruption | not contradicted in the audited pre-target corpus |

One false conjunct makes the imported compound claim false.

## Assumption-satisfying novelty counterexample

[*Offline and Online KL-Regularized RLHF under Differential
Privacy*](https://ar5iv.labs.arxiv.org/html/2510.13512), arXiv:2510.13512,
was published 2025-10-15T13:04:19Z, before the target's
2025-12-29T19:20:35Z arXiv date. Its
[Algorithm 2](https://ar5iv.labs.arxiv.org/html/2510.13512#alg2):

- is an online KL-regularized RLHF protocol over pairwise human preferences;
- uses epsilon-local randomized response on each preference label;
- discloses only the private label to the learner;
- has a theorem-level online regret guarantee under Bradley-Terry
  realizability ([Theorem 5.2](https://ar5iv.labs.arxiv.org/html/2510.13512#S5.Thmtheorem2)).

The source HTML SHA-256 is
`921ac2750798565d1e20e251f3f9c92d27d04bfd92dc1f4e83058c90efeb1412`;
the arXiv metadata snapshot SHA-256 is
`9a9465aa677b6f6c9ba496be233ac5e2b4da05527a8d1e34b593a6a4abd0470a`.
The target arXiv metadata snapshot SHA-256 is
`fefe71a75289e1b5d5c98c983333f67431441e5bc09a750432c9cfe3792e593b`.

## Why the PrivXPO rate still verifies

The executable implements Algorithm 2's ranking, private BT likelihood,
`c(epsilon)^2` scaling, and optimism on a finite policy class. Removing `c^2`
reverses the selected policy, so the control is consequential. Independently,
Lemma 3.1 supplies

```text
c^2 log(|Pi|T/delta)/T
```

as squared prediction error. The XPO meta theorem takes its square root,
producing the displayed `c sqrt(log/T)` term while retaining `kappa_cov`.

## Inline conformance results

| Check | Result |
| --- | --- |
| exact PrivXPO fixture selection | `A_low` |
| omit-`c^2` control selection | `A_high` (control exits 1) |
| online-private counterexample predates target | yes |
| counterexample meets all five scope fields | yes |

## SquareXPO source defect

The exact target source defines a nonnegative square loss but prints
`argmin { optimism - square_loss }`; the proof requires minimizing empirical
loss. On the fixture, the printed minus sign selects `A_low`, the policy with
larger square loss, while the corrected plus sign selects `A_high`. The source
also uses undefined `[n]` in that online update. This is reported as a
limitation and is not needed for the novelty falsification.

## Reproducible evidence

- [Claim contract](../../../evidence/claim_5/claim_contract.json)
- [Algorithm verifier](../../../evidence/claim_5/alignment_algorithms.py)
- [Independent checker](../../../evidence/claim_5/alignment_algorithms_checker.py)
- [Raw results](../../../evidence/claim_5/raw_results.json)
- [Literature search record](../../../evidence/claim_5/novelty_search.json)
- [Checker output](../../../evidence/claim_5/checker_output.json)
- [Failing control](../../../evidence/claim_5/negative_control_output.json)
- [Source audit](../../../evidence/claim_5/source_audit.md)
- [Method](../../../evidence/claim_5/method.md)
- [Limitations](../../../evidence/claim_5/limitations.md)
- [Runtime](../../../evidence/claim_5/runtime.json)
- [Fixed command](../../../evidence/claim_5/command.txt)
