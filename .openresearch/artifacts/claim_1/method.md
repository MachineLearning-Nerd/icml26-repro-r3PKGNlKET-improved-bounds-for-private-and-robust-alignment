# Claim 1 method

For a candidate private density `Q` and realizable truth `P`, the conditional
expectation of the square-root likelihood ratio is their Hellinger affinity:

`E_P exp(-(ell_Q-ell_P)/2) = sum_o sqrt(P(o)Q(o)) = 1-H^2(P,Q)/2`.

The inequality `1-u <= exp(-u)` therefore constructs a nonnegative
supermartingale. Ville's inequality makes the bound simultaneous in time, and
a union bound makes it simultaneous over the finite class. Binary randomized
response contracts TV exactly by `lambda=2q-1=1/c(epsilon)`, so rescaling
produces the claimed `c(epsilon)^2` factor.

The objective is exactly `sum -log P_tilde_theta(private_label|x)`. The
negative control evaluates private labels under the raw density and fails the
contraction certificate.
