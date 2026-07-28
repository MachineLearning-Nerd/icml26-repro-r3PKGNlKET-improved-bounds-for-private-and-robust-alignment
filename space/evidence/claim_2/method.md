# Claim 2 method

Write `d=g-g*`, `a=g*-F`, and `eta=o-F`. Exact expansion gives
`loss(g)-loss(g*)=d^2+2da-2d eta`. Young's inequality controls approximation
by `d^2/4+4 alpha_app^2`. Conditional Hoeffding, Ville's inequality, and a
finite-class union bound at `lambda=1/(8C^2)` control the martingale term by
`sum d^2/4+8C^2 log(|H|/delta)`, for all horizons. Rearrangement yields

`sum d^2 <= 2 loss_difference + 8n alpha_app^2 + 16C^2 log(|H|/delta)`.

For CTL, `C=c` and `alpha_app<=2alpha`. For LTC,
`alpha_app<=2c alpha`. Substitution yields the exact claimed orders.
