# Limitations and deviations

- The certificate verifies the binary randomized-response information cost
  underlying the paper's optimality statement. It does not claim the hidden
  constant in Lemma 3.1.
- The Cramer-Rao route alone covers unbiased regular estimators; the separate
  Le Cam route supplies the estimator-independent minimax order argument.
- No neural language model is trained. This is deliberate: Claim 3 is a
  mathematical mechanism and lower-bound claim, for which a finite training
  curve would be weaker and potentially circular evidence.
- The paper cites prior mean-estimation lower bounds for broader CTL/LTC
  settings. This claim page does not re-prove those broader corruption lower
  bounds; they belong to Claim 4.
