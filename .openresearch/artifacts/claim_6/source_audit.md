# Claim 6 source audit

Primary source: arXiv:2512.23816, Algorithm 1/Theorem 4.4
(`#S4.Thmtheorem4`) and Algorithm 3/Theorem 5.2
(`#S5.Thmtheorem2`). Retrieved 2026-07-28 with explicit User-Agent; HTML
SHA-256
`a6f601022be169cb0651f4d4e389e233cae827109c611f79adfb7dd67fddcc0b`.

Both theorems require policy realizability (Assumption 4.1), bounded implicit
reward differences (Assumption 4.2), finite policy class, the stated
single-policy concentrability, and a suitable beta. Their high-probability
bounds retain `kappa(pi*)`; it is not set to one in this reproduction.

Theorem 4.4 gives `kappa*c*sqrt(log(|Pi|/delta)/n)`. Theorem 5.2 gives under
CTL `kappa*(c*sqrt(log(|Pi|/delta)/n)+alpha)` and under LTC the final term is
`c*alpha`.
