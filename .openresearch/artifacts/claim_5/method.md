# Claim 5 method

Route 1 is exact implementation conformance. A two-policy finite instance
implements Algorithm 2's ranking, BT probability, induced private likelihood,
`c(epsilon)^2` scaling, and global-optimism term. Removing `c^2` reverses the
selected policy, so the control tests a consequential detail.

Route 2 is theorem algebra. Lemma 3.1 supplies squared prediction error
`c^2 log(|Pi|T/delta)/T`; the XPO meta theorem takes its square root, yielding
the exact `c sqrt(log/T)` term. Coverability and paper constants remain
symbolic rather than being silently set to one.

Route 3 is a dated primary-source novelty test. arXiv:2510.13512 predates the
target and meets every scope field: online, pairwise human preferences,
RR-localized labels, learner sees only private labels, and a theorem-level
online regret result. One false conjunct makes the imported compound claim
false even though the PrivXPO rate subclaim verifies.
