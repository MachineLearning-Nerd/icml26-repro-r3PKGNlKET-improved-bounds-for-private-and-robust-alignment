# Method

Route 1 uses exact rational arithmetic.  With randomized-response truthful
probability `q`, the observed mean is `(2q-1)mu`.  Inverting that contraction
gives `c=1/(2q-1)`, which is algebraically identical to the paper's
exponential form.  The estimator `c * mean(z)` is unbiased, has variance
`(c^2-mu^2)/n`, and attains the Cramer-Rao bound pointwise.

Route 2 does not assume unbiasedness.  It chooses the clean Bernoulli means
`+/- c/(8 sqrt(n))`, for `n >= c^2/64`.  After randomized response, their
separation no longer contains `c`.  Bounding product-distribution total
variation with KL and Pinsker, then applying Le Cam's two-point lemma, yields
minimax mean-squared error at least `K c^2/n` for a universal positive
constant `K`.

The independent checker reimplements the contraction and Fisher-information
calculation with `Decimal`, then exhausts 68 rational `(q,mu)` cases.  The
negative control replaces `c=1/(2q-1)` by `1/q`; the primary verifier must
exit nonzero.
