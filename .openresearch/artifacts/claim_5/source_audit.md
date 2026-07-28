# Claim 5 source audit

Target source: arXiv:2512.23816, Algorithm 2 and Theorem 4.8
(`#S4.Thmtheorem8`), plus Algorithm 4 in Section 5.2. HTML retrieved
2026-07-28 with explicit User-Agent; SHA-256
`a6f601022be169cb0651f4d4e389e233cae827109c611f79adfb7dd67fddcc0b`.

The rate subclaim assumes policy realizability, bounded density ratios, finite
policy class, trajectory-level coverability, epsilon > 0, any beta > 0 and
integer horizon T, with a suitable optimism gamma. It is high-probability and
contains `c(epsilon)*sqrt(log(|Pi|T/delta)/T)`, multiplied by the stated
coverability term.

Novelty counterexample: *Offline and Online KL-Regularized RLHF under
Differential Privacy*, arXiv:2510.13512. Its v1 metadata gives
2025-10-15T13:04:19Z, before the target's 2025-12-29T19:20:35Z arXiv date.
The target metadata snapshot SHA-256 is
`fefe71a75289e1b5d5c98c983333f67431441e5bc09a750432c9cfe3792e593b`.
Algorithm 2
is an online pairwise-preference RLHF method where RR privatizes each label
before learner access; Theorem 5.2 supplies an online regret bound under
Bradley-Terry realizability and epsilon-local label DP.

- Primary HTML:
  `https://ar5iv.labs.arxiv.org/html/2510.13512`
- Algorithm anchor: `#alg2`
- Theorem anchor: `#S5.Thmtheorem2`
- HTML SHA-256:
  `921ac2750798565d1e20e251f3f9c92d27d04bfd92dc1f4e83058c90efeb1412`
- arXiv API metadata SHA-256:
  `9a9465aa677b6f6c9ba496be233ac5e2b4da05527a8d1e34b593a6a4abd0470a`

Three `orx lit` searches covered online private preference alignment, online
RLHF plus local privacy/corruption, and private robust alignment. The
counterexample appeared in the latter searches. This establishes a concrete
contradiction to the private-online “first” subclaim; it does not contradict
the narrower private-plus-corruption novelty subclaim.

Source defect noted separately: target Algorithm 4 defines a nonnegative
square loss but minimizes `optimism - square_loss`; its proof needs empirical
loss minimization. The exact source tar confirms the minus sign and also uses
an undefined `[n]` in that online update. This defect is not needed for the
novelty falsification.
