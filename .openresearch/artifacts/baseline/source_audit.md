# Baseline source and evaluator audit

The paper source is the ar5iv HTML for arXiv:2512.23816, retrieved with the
explicit User-Agent recorded in `paper_source.json`. Its SHA-256 is
`a6f601022be169cb0651f4d4e389e233cae827109c611f79adfb7dd67fddcc0b`.

The six judge claims map to the following exact paper statements:

1. Lemma 3.1 (`#S3.Thmtheorem1`): finite conditional-density class, adapted
   sequence, realizability, randomized response with epsilon > 0, and a
   simultaneous probability-at-least-1-delta bound over n in [T] and theta.
2. Lemma 3.3 (`#S3.Thmtheorem3`): finite functions into [-1,1], adapted binary
   labels, conditional-mean realizability, alpha in [0,1/2), epsilon > 0, and
   simultaneous CTL/LTC bounds over all n and h.
3. Remark 3.2 and Section 3: the privacy contraction factor is
   c(epsilon)=(exp(epsilon)+1)/(exp(epsilon)-1), and c(epsilon)^2 is called the
   optimal estimation-error privacy cost.
4. Definition 2.4 plus Lemma 3.3: CTL and LTC are different mechanism
   compositions; the theorem-level squared bias terms are alpha^2 and
   c(epsilon)^2 alpha^2, corresponding to alpha and c(epsilon) alpha after a
   square root.
5. Algorithm 2/Theorem 4.8 and Algorithm 4/Theorem 5.3: finite policy class,
   policy realizability, bounded density ratios, coverability, proper optimism
   choice, and high-probability suboptimality bounds.
6. Algorithm 1/Theorem 4.4 and Algorithm 3/Theorem 5.2: comparator-dependent
   beta, policy realizability, bounded implicit reward differences,
   single-policy concentrability, and high-probability offline gaps.

The judged Space revision is immutable historical evidence. Its canonical
overview contains only summary assertions and references two absent files.
Consequently, every scientific claim is BLOCKED at this baseline even though
the historical-audit check itself passes.
