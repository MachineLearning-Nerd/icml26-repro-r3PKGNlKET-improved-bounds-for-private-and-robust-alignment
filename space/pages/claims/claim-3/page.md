# Claim 3 — privacy factor and optimality

**VERIFIED.** For binary randomized response,
`c(epsilon)=(exp(epsilon)+1)/(exp(epsilon)-1)` is exactly the inverse
contraction of the clean Bernoulli mean. Both an attainable estimator and an
estimator-independent two-point lower bound have the
`c(epsilon)^2/n` mean-squared-error scale.

## Exact claim and assumptions

The exact source is [Lemma 3.1 and Remark
3.2](https://ar5iv.labs.arxiv.org/html/2512.23816#S3.Thmtheorem1).
The source assumes epsilon > 0, binary epsilon-LDP randomized response, a
finite realizable class, and an adapted sequence. The optimality statement is
about order, not the hidden constant.

## Direct numerical certificate

| Quantity | Exact result |
| --- | ---: |
| truthful RR probability `q` | 3/4 |
| `exp(epsilon)` | 3 |
| contraction `lambda=2q-1` | 1/2 |
| `c=1/lambda` | 2 |
| clean mean `mu`; samples `n` | 1/4; 64 |
| unbiased-estimator variance | 63/1024 |
| inverse Fisher information / `n` | 63/1024 |
| Le Cam output pair | Bernoulli(33/64), Bernoulli(31/64) |

The identity is general: `q=exp(epsilon)/(1+exp(epsilon))`, hence
`1/(2q-1)=(exp(epsilon)+1)/(exp(epsilon)-1)=1/tanh(epsilon/2)`.

## Why this tests optimality

The first route proves that `c mean(z)` is unbiased and attains the
Cramer-Rao variance `(c^2-mu^2)/n`. The independent route selects clean means
`+/-c/(8 sqrt(n))`; randomized response removes `c` from their output
separation. KL, Pinsker, and Le Cam then give minimax MSE
`Omega(c^2/n)` for any estimator when `n >= c^2/64`. The sample count is not
chosen from a desired pass tolerance, and no empirical slope is used as proof.

## Reproducible evidence

- [Claim contract](../../../evidence/claim_3/claim_contract.json)
- [Primary verifier](../../../evidence/claim_3/privacy_factor.py)
- [Independent checker](../../../evidence/claim_3/privacy_factor_checker.py)
- [Raw results](../../../evidence/claim_3/raw_results.json)
- [Checker output](../../../evidence/claim_3/checker_output.json)
- [Negative control](../../../evidence/claim_3/negative_control_output.json)
- [Method](../../../evidence/claim_3/method.md)
- [Limitations](../../../evidence/claim_3/limitations.md)
- [Runtime record](../../../evidence/claim_3/runtime.json)
- [Exact fixed command](../../../evidence/claim_3/command.txt)
- [Pinned project metadata](../../../environment/pyproject.toml)
- [Pinned uv lockfile](../../../environment/uv.lock)

The independent checker passes 68 rational cases. The negative control uses
the wrong factor `1/q`; it fails the contraction, identity, unbiasedness, and
Cramer-Rao checks and exits nonzero.
