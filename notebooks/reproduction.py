import marimo

__generated_with = "0.23.15"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md(r"""
    # Private and robust alignment: an executable guide

    **Evidence first.** Five evaluator-selected claims are verified and one
    is falsified as written. Claim 5's PrivXPO rate verifies, but its broad
    novelty conjunct has a dated counterexample. These are reproduction
    verdicts, not a new live judge score.

    | Claim | Evidence verdict | Decisive certificate |
    | --- | --- | --- |
    | 1 | VERIFIED | likelihood-ratio supermartingale + exact RR contraction |
    | 2 | VERIFIED | square-loss martingale + squared misspecification |
    | 3 | VERIFIED | attainable estimator + Le Cam lower bound |
    | 4 | VERIFIED | exact CTL/LTC expectation and endpoint witnesses |
    | 5 | FALSIFIED | rate verified; prior online private RLHF paper |
    | 6 | VERIFIED | named algorithms + exact theorem exponent map |

    The formal evidence used the fixed command
    `uv run --frozen python -m reproduction.runner`. This notebook embeds
    the accepted results so opening it never launches an expensive run.
    """)
    return


@app.cell
def _(mo):
    epsilon = mo.ui.slider(
        start=0.1,
        stop=5.0,
        step=0.1,
        value=1.1,
        label="Privacy ε",
    )
    epsilon
    return (epsilon,)


@app.cell
def _(epsilon, mo):
    import math

    eps = float(epsilon.value)
    c_eps = (math.exp(eps) + 1.0) / (math.exp(eps) - 1.0)
    contraction = 1.0 / c_eps
    mo.md(
        rf"""
        ## The mechanism behind Claims 1 and 3

        Binary randomized response multiplies every clean Bernoulli mean and
        every pairwise total-variation distance by

        \[
        \lambda=\tanh(\varepsilon/2)=1/c(\varepsilon).
        \]

        At **ε = {eps:.1f}**, `c(ε) = {c_eps:.4f}` and the contraction is
        `{contraction:.4f}`. Undoing that contraction multiplies variance by
        `c(ε)² = {c_eps**2:.4f}`. The certificate proves both attainability
        (an unbiased estimator reaches this scale) and necessity (a two-point
        Le Cam argument gives the same minimax order).
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Why corruption order matters

    Write `h` for the clean label mean and `b` for an adversarial
    replacement mean. After de-privatizing the observed label:

    \[
    F_{\mathrm{CTL}}=(1-\alpha)h+\alpha b,\qquad
    F_{\mathrm{LTC}}=(1-\alpha)h+\alpha c b.
    \]

    Therefore CTL has bias at most `2α`, while LTC has bias at most
    `2cα`. Endpoint adversaries attain those orders. Claim 2 then uses a
    square-loss argument, so the approximation contributions are
    `α²` and `c²α²`, not `α` and `cα`.
    """)
    return


@app.cell
def _(mo):
    fixture = [
        {
            "algorithm": "PrivχPO",
            "A_high": -0.6709814418,
            "A_low": -2.5104419617,
            "rule": "maximize",
            "selected": "A_high",
        },
        {
            "algorithm": "SquareχPO",
            "A_high": 16.3586115830,
            "A_low": 2.5994345513,
            "rule": "minimize",
            "selected": "A_low",
        },
        {
            "algorithm": "PrivXPO",
            "A_high": 2.5898505856,
            "A_low": 1.4999881131,
            "rule": "minimize",
            "selected": "A_low",
        },
    ]
    mo.ui.table(fixture, selection=None)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## The novelty falsification

    The target appeared on arXiv on 2025-12-29. arXiv:2510.13512 appeared
    on 2025-10-15 and contains an online KL-regularized RLHF algorithm over
    pairwise preferences, with ε-local randomized response applied before
    disclosure to the learner and a theorem-level online regret bound.
    That is a counterexample to the broad “first online private alignment
    algorithm” conjunct. We did **not** find a prior algorithm jointly
    handling privacy and adversarial corruption, so the narrower novelty
    reading remains uncontradicted.

    ## What this reproduction does not claim

    Finite fixtures only test implementations. The universal results rest
    on independently reconstructed symbolic derivations or a dated
    assumption-matched counterexample. We did not use empirical slopes to
    certify asymptotic theorems, did not run a GPU, and do not claim that
    the live score changed before the evaluator records a new revision.
    """)
    return


if __name__ == "__main__":
    app.run()
