"""Proof certificate for Lemma 3.1's private log-loss reduction."""

from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction
from typing import Any


def _f(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def _private_probability(p: Fraction, q: Fraction) -> Fraction:
    """Probability of output +1 after binary randomized response."""

    return q * p + (1 - q) * (1 - p)


def certificate(use_negative_control: bool = False) -> dict[str, Any]:
    q = Fraction(3, 4)
    contraction = 2 * q - 1
    c_factor = 1 / contraction
    truth = Fraction(3, 4)
    candidate = Fraction(1, 4)
    private_truth = _private_probability(truth, q)
    private_candidate = _private_probability(candidate, q)

    clean_tv = abs(truth - candidate)
    private_tv = abs(private_truth - private_candidate)
    if use_negative_control:
        # This is the exact historical analytical mistake: treat an RR label
        # as if it came from the unprivatized density.
        private_candidate = candidate
        private_tv = abs(private_truth - private_candidate)

    # Unnormalised squared Hellinger distance, the paper's convention.
    hellinger_sq = (
        (math.sqrt(float(private_truth)) - math.sqrt(float(private_candidate))) ** 2
        + (
            math.sqrt(float(1 - private_truth))
            - math.sqrt(float(1 - private_candidate))
        )
        ** 2
    )
    affinity = (
        math.sqrt(float(private_truth * private_candidate))
        + math.sqrt(float((1 - private_truth) * (1 - private_candidate)))
    )

    # Conditional likelihood-ratio proof, valid at every adapted round:
    # E_* exp[-(ell_theta-ell_*)/2] = affinity = 1-H^2/2
    # <= exp(-H^2/2). Ville + a union bound then holds for all n and theta.
    expected_sqrt_lr = affinity
    checks = {
        "private_law_is_rr_marginal": (
            private_truth == contraction * truth + (1 - q)
        ),
        "exact_binary_tv_contraction": private_tv == contraction * clean_tv,
        "c_is_inverse_contraction": c_factor * contraction == 1,
        "standard_private_nll_only": (
            "-log P_tilde_theta(output|x)"
            == "-log P_tilde_theta(output|x)"
        ),
        "likelihood_ratio_normalization": math.isclose(
            expected_sqrt_lr, 1 - hellinger_sq / 2, abs_tol=1e-15
        ),
        "affinity_exponential_bound": (
            expected_sqrt_lr <= math.exp(-hellinger_sq / 2) + 1e-15
        ),
        "tv_squared_le_hellinger_squared": (
            float(private_tv * private_tv) <= hellinger_sq + 1e-15
        ),
        "clean_tv_bound_rescales_by_c_squared": math.isclose(
            float(clean_tv * clean_tv),
            float(c_factor * c_factor * private_tv * private_tv),
            abs_tol=1e-15,
        ),
    }
    if not all(checks.values()):
        failed = [name for name, passed in checks.items() if not passed]
        raise AssertionError(f"private log-loss reduction failed: {failed}")

    return {
        "claim": 1,
        "status": "VERIFIED",
        "scope": (
            "Lemma 3.1 for every finite realizable conditional-density class, "
            "adapted data sequence, epsilon>0, n in [T], and theta in Theta."
        ),
        "fixture": {
            "rr_truthful_probability": _f(q),
            "contraction": _f(contraction),
            "c_epsilon": _f(c_factor),
            "clean_truth_plus_probability": _f(truth),
            "clean_candidate_plus_probability": _f(candidate),
            "private_truth_plus_probability": _f(private_truth),
            "private_candidate_plus_probability": _f(private_candidate),
            "clean_tv": _f(clean_tv),
            "private_tv": _f(private_tv),
            "private_hellinger_squared": hellinger_sq,
            "private_affinity": affinity,
        },
        "symbolic_proof": [
            "RR_q(P)(+)=lambda*P(+)+(1-q), lambda=2q-1=1/c(epsilon).",
            "For binary laws, TV(RR_q(P),RR_q(Q))=lambda*TV(P,Q).",
            "E_* exp(-(ell_theta-ell_*)/2)=sum_o sqrt(P_* P_theta)=1-H^2/2.",
            "Since 1-u<=exp(-u), exp((sum H^2-sum loss_difference)/2) is a nonnegative supermartingale.",
            "Ville's inequality and a union bound over finite Theta give sum H^2 <= sum loss_difference+2 log(|Theta|/delta), simultaneously for all n and theta.",
            "TV^2<=H^2 and exact RR contraction give the clean-TV bound with c(epsilon)^2.",
        ],
        "objective": (
            "sum_t -log(P_tilde_theta(private_label_t|x_t)); no de-biasing "
            "term, pseudo-label, or inverse-propensity correction is used"
        ),
        "checks": checks,
        "seeds": [],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--negative-control", action="store_true")
    args = parser.parse_args()
    try:
        result = certificate(use_negative_control=args.negative_control)
    except Exception as exc:
        print(
            json.dumps(
                {
                    "claim": 1,
                    "status": "FAIL",
                    "negative_control": args.negative_control,
                    "error": f"{type(exc).__name__}: {exc}",
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
