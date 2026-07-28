# Claim 1 — standard private MLE log loss

**VERIFIED.** Lemma 3.1 follows from a reconstructed time-uniform
likelihood-ratio certificate plus exact binary randomized-response
contraction. The tested objective is ordinary negative log likelihood of the
induced private density; it contains no de-biasing correction.

## Exact claim and assumptions

[Lemma 3.1](https://ar5iv.labs.arxiv.org/html/2512.23816#S3.Thmtheorem1)
assumes a finite conditional-density class, binary labels, epsilon > 0
randomized response, an adapted sequence, and realizability. With probability
at least `1-delta`, the statement is simultaneous for every horizon `n in
[T]` and candidate `theta`.

## Proof certificate

For private truth `P` and candidate `Q`,

```text
E_P exp(-(ell_Q-ell_P)/2)
  = sum_o sqrt(P(o) Q(o))
  = 1 - H^2(P,Q)/2
  <= exp(-H^2(P,Q)/2).
```

The resulting nonnegative supermartingale, Ville's inequality, and a union
bound over the finite class give

```text
sum H_t^2 <= sum (ell_theta,t-ell_theta*,t) + 2 log(|Theta|/delta)
```

simultaneously for all horizons and candidates. For binary randomized
response, `TV(P_tilde,Q_tilde)=lambda TV(P,Q)` exactly, where
`lambda=2q-1=1/c(epsilon)`. Since `TV^2<=H^2`, this is precisely the claimed
`c(epsilon)^2` reduction.

## Inline raw fixture

| Quantity | Exact value |
| --- | ---: |
| RR truthful probability `q` | 3/4 |
| contraction `lambda`; `c` | 1/2; 2 |
| clean truth / candidate `P(+1)` | 3/4; 1/4 |
| private truth / candidate `P(+1)` | 5/8; 3/8 |
| clean TV / private TV | 1/2; 1/4 |
| private squared Hellinger | 0.06350832689629149 |
| independent cases | 168 |

## Reproducible evidence

- [Claim contract](../../../evidence/claim_1/claim_contract.json)
- [Primary verifier](../../../evidence/claim_1/log_loss_reduction.py)
- [Independent checker](../../../evidence/claim_1/log_loss_reduction_checker.py)
- [Raw results](../../../evidence/claim_1/raw_results.json)
- [Checker output](../../../evidence/claim_1/checker_output.json)
- [Failing negative control](../../../evidence/claim_1/negative_control_output.json)
- [Source audit](../../../evidence/claim_1/source_audit.md)
- [Method](../../../evidence/claim_1/method.md)
- [Limitations](../../../evidence/claim_1/limitations.md)
- [Runtime](../../../evidence/claim_1/runtime.json)
- [Fixed command](../../../evidence/claim_1/command.txt)

The independent checker shares no primary implementation and uses 70-digit
Decimal arithmetic. The negative control applies the raw density to private
labels; it exits 1 because the contraction and rescaling identities fail.

## Limitation

The rational sweep is only an implementation cross-check. The universal
evidence is the symbolic supermartingale derivation above. The historical
empirical slope assertion is rejected and unused.
