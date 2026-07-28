# Claim 2 — improved square-loss corruption powers

**VERIFIED.** The exact conditional-mean misspecification is `O(alpha)` under
CTL and `O(c alpha)` under LTC. An independently reconstructed time-uniform
square-loss argument squares those terms, giving `n alpha^2` and
`n c^2 alpha^2`, exactly as Lemma 3.3 states.

## Exact claim and assumptions

[Lemma 3.3](https://ar5iv.labs.arxiv.org/html/2512.23816#S3.Thmtheorem3)
assumes finite `H subset (X -> [-1,1])`, binary labels, a realizable
conditional mean, an adapted sequence, alpha-Huber replacement, and epsilon >
0 randomized response. The result is simultaneous for all horizons and all
`h` with probability at least `1-delta`.

## Independently reconstructed bound

Let `d=g-g*`, `a=g*-F`, and `eta=o-F`. Exact expansion gives

```text
loss(g)-loss(g*) = d^2 + 2 d a - 2 d eta.
```

Young's inequality controls approximation by `d^2/4+4 alpha_app^2`.
Conditional Hoeffding plus Ville at `lambda=1/(8C^2)`, followed by a finite
class union bound, controls the martingale term at every horizon. Rearranging:

```text
sum d^2 <= 2 loss_difference
           + 8 n alpha_app^2
           + 16 C^2 log(|H|/delta).
```

Substituting `C=c`, `alpha_app<=2alpha` for CTL and
`alpha_app<=2c alpha` for LTC yields the claimed dependencies.

## Old and new terms on the same scale

| Source | CTL squared error | LTC squared error |
| --- | --- | --- |
| SquareχPO Lemma 5.1 (arXiv:2505.21395) | `alpha` | `c alpha` |
| Current Lemma 3.3 | `alpha^2` | `c^2 alpha^2` |

The prior source was retrieved with an explicit User-Agent; its HTML SHA-256
is `09ea82592e3f2cdc67a426fb45ea23d7cb169bb0b8a2483e024c7837a30f39eb`.

## Reproducible evidence

- [Claim contract](../../../evidence/claim_2/claim_contract.json)
- [Primary verifier](../../../evidence/claim_2/corruption_order.py)
- [Independent checker](../../../evidence/claim_2/corruption_order_checker.py)
- [Raw results](../../../evidence/claim_2/raw_results.json)
- [Checker output](../../../evidence/claim_2/checker_output.json)
- [Failing negative control](../../../evidence/claim_2/negative_control_output.json)
- [Source audit](../../../evidence/claim_2/source_audit.md)
- [Method](../../../evidence/claim_2/method.md)
- [Limitations](../../../evidence/claim_2/limitations.md)
- [Runtime](../../../evidence/claim_2/runtime.json)
- [Fixed command](../../../evidence/claim_2/command.txt)

The checker independently enumerates 1,600 exact rational configurations. The
control deliberately applies the CTL replacement formula to LTC and exits 1.
Finite enumeration checks the implementation; the derivation establishes the
universal statement.
