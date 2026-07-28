# Claim 6 — offline PrivChiPO and SquareChiPO rates

**VERIFIED.** Exact finite-policy implementations match Algorithms 1 and 3,
and independent theorem algebra maps the proof-level uniform errors to the
stated offline suboptimality rates.

## Exact claims and assumptions

[Theorem 4.4](https://ar5iv.labs.arxiv.org/html/2512.23816#S4.Thmtheorem4)
and [Theorem 5.2](https://ar5iv.labs.arxiv.org/html/2512.23816#S5.Thmtheorem2)
assume policy realizability, bounded implicit reward differences, finite
policy class, single-policy L1 concentrability, a suitable beta, and
probability at least `1-delta`. The prefactor `kappa(pi*)` is retained:

| Algorithm / setting | Verified rate |
| --- | --- |
| PrivChiPO | `kappa*c*sqrt(log(|Pi|/delta)/n)` |
| SquareChiPO, CTL | `kappa*(c*sqrt(log(|Pi|/delta)/n)+alpha)` |
| SquareChiPO, LTC cumulative check | `kappa*(c*sqrt(log(|Pi|/delta)/n)+c*alpha)` |

## Named algorithm implementations

PrivChiPO ranks the responses using the private label, evaluates
`phi(u)=u+log(u)`, clips the implicit reward difference, and maximizes the
ordinary likelihood of the induced private BT probability. SquareChiPO keeps
the original `+1/-1` response ordering and minimizes
`(2P-1-c(epsilon)z)^2`; it does not rank by the observed label.

On the fixed two-policy fixture:

| Algorithm | Selected policy | Why |
| --- | --- | --- |
| PrivChiPO | `A_high` | highest induced-private log likelihood |
| SquareChiPO | `A_low` | lowest unranked private square loss for `z=-1` |

## Rate certificate

The offline meta theorem takes a square root of prediction error. Therefore:

```text
sqrt(c^2 log/n)                         = c sqrt(log/n)
sqrt(c^2 log/n + alpha^2)              <= c sqrt(log/n) + alpha
sqrt(c^2 log/n + c^2 alpha^2)          <= c sqrt(log/n) + c alpha.
```

This is symbolic theorem instantiation, not an empirical slope. The cumulative
suite first reruns the independently reconstructed Lemmas 3.1 and 3.3.

## Reproducible evidence

- [Claim contract](../../../evidence/claim_6/claim_contract.json)
- [Algorithm verifier](../../../evidence/claim_6/alignment_algorithms.py)
- [Independent checker](../../../evidence/claim_6/alignment_algorithms_checker.py)
- [Raw results](../../../evidence/claim_6/raw_results.json)
- [Checker output](../../../evidence/claim_6/checker_output.json)
- [Failing control](../../../evidence/claim_6/negative_control_output.json)
- [Source audit](../../../evidence/claim_6/source_audit.md)
- [Method](../../../evidence/claim_6/method.md)
- [Limitations](../../../evidence/claim_6/limitations.md)
- [Runtime](../../../evidence/claim_6/runtime.json)
- [Fixed command](../../../evidence/claim_6/command.txt)

The independent checker shares no primary code. It recomputes the
consequential PrivXPO objective fixture, checks rate monomial exponents, and
checks the dated novelty-counterexample fields. Its negative control exits 1.
