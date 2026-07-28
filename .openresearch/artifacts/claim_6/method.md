# Claim 6 method

The finite-policy conformance fixture implements the exact named objectives:
PrivChiPO ranks by the private label and maximizes the induced-private BT log
likelihood; SquareChiPO keeps the original +/-1 response ordering and
minimizes `(2P-1-cz)^2`.

The theorem checker represents rate factors as monomial exponents. Lemma 3.1
gives `c^2 log/n`; the offline meta theorem takes a square root, yielding
`c sqrt(log/n)`. Lemma 3.3 gives CTL `c^2 log/n+alpha^2` and LTC
`c^2 log/n+c^2 alpha^2`; `sqrt(a+b)<=sqrt(a)+sqrt(b)` gives the two Theorem
5.2 rates. The kappa prefactor is carried unchanged.
