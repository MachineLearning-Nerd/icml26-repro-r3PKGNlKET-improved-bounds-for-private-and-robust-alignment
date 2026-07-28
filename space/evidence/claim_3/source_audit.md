# Claim 3 source audit

Primary source: arXiv:2512.23816 via
`https://ar5iv.labs.arxiv.org/html/2512.23816`, retrieved
2026-07-28T17:44:34Z, SHA-256
`a6f601022be169cb0651f4d4e389e233cae827109c611f79adfb7dd67fddcc0b`.

Lemma 3.1 (`#S3.Thmtheorem1`) defines
`c(epsilon)=(exp(epsilon)+1)/(exp(epsilon)-1)=1/(2 sigma(epsilon)-1)`.
Remark 3.2 says the MLE estimation error has order
`c(epsilon)^2 log(|Theta|)` and calls `c(epsilon)^2` the optimal privacy
cost. The statement assumes binary randomized response, epsilon > 0, a finite
realizable conditional-density class, and an adapted sequence; it is a
high-probability uniform-convergence result.

The certificate isolates the information-theoretic part of the optimality
claim. For a clean +/-1 Bernoulli mean `mu`, randomized response contracts the
mean by `lambda=2q-1=1/c`. This creates both an attainable variance of order
`c^2/n` and a two-point minimax lower bound of the same order.
