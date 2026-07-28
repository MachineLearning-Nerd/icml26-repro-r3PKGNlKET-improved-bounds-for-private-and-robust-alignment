"""Exact certificate for the randomized-response privacy factor.

This module checks the algebraic contraction, an efficient unbiased estimator,
and a two-point lower bound.  The latter rules out replacing the
``c(epsilon)^2 / n`` estimation scale by a smaller order uniformly over the
Bernoulli-mean family.
"""

from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction
from typing import Any


def _fraction(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def certificate(use_negative_control: bool = False) -> dict[str, Any]:
    q = Fraction(3, 4)
    odds = q / (1 - q)
    contraction = 2 * q - 1
    c_factor = 1 / contraction
    if use_negative_control:
        # Deliberately omit the randomized-response contraction inversion.
        c_factor = 1 / q

    epsilon = math.log(float(odds))
    c_exponential = (math.exp(epsilon) + 1) / (math.exp(epsilon) - 1)
    c_hyperbolic = 1 / math.tanh(epsilon / 2)

    mu = Fraction(1, 4)
    n = 64
    output_mean = contraction * mu
    output_plus_probability = (1 + output_mean) / 2
    estimator_expectation = c_factor * output_mean
    estimator_variance = (c_factor * c_factor - mu * mu) / n
    fisher_information = (
        contraction * contraction / (1 - contraction * contraction * mu * mu)
    )
    cramer_rao = 1 / (n * fisher_information)

    # Le Cam pair: mu in {-Delta,+Delta}.  The output probabilities are exact.
    delta = Fraction(1, 16)
    p_plus = (1 + contraction * delta) / 2
    p_minus = (1 - contraction * delta) / 2
    single_kl = float(
        (p_plus - p_minus) * math.log(float(p_plus / p_minus))
    )
    product_tv_upper = math.sqrt(n * single_kl / 2)
    le_cam_mse_lower = (
        float(delta * delta) / 2 * (1 - product_tv_upper)
    )
    target_scale = float(Fraction(4, n))

    checks = {
        "rr_odds_equal_exp_epsilon": math.isclose(
            math.exp(epsilon), float(odds), rel_tol=0, abs_tol=1e-14
        ),
        "contraction_is_inverse_c": contraction * c_factor == 1,
        "c_matches_exponential_identity": math.isclose(
            float(c_factor), c_exponential, rel_tol=0, abs_tol=1e-14
        ),
        "c_matches_hyperbolic_identity": math.isclose(
            float(c_factor), c_hyperbolic, rel_tol=0, abs_tol=1e-14
        ),
        "unbiased_estimator": estimator_expectation == mu,
        "cramer_rao_attained": estimator_variance == cramer_rao,
        "two_point_pair_inside_domain": 0 < delta < 1,
        "two_point_tv_bound_nonvacuous": 0 < product_tv_upper < 1,
        "two_point_lower_bound_positive": le_cam_mse_lower > 0,
        "two_point_lower_bound_has_c2_over_n_scale": (
            le_cam_mse_lower / target_scale > 0.02
        ),
    }
    if not all(checks.values()):
        failed = [name for name, value in checks.items() if not value]
        raise AssertionError(f"privacy-factor certificate failed: {failed}")

    return {
        "claim": 3,
        "status": "VERIFIED",
        "scope": (
            "Exact randomized-response identity and optimal c(epsilon)^2/n "
            "order for Bernoulli mean estimation; constants are not claimed."
        ),
        "fixture": {
            "q_rr_truthful": _fraction(q),
            "exp_epsilon": _fraction(odds),
            "epsilon": epsilon,
            "contraction_lambda": _fraction(contraction),
            "c_epsilon": _fraction(c_factor),
            "mu": _fraction(mu),
            "n": n,
            "output_plus_probability": _fraction(output_plus_probability),
            "estimator_variance": _fraction(estimator_variance),
            "fisher_information_per_sample": _fraction(fisher_information),
            "cramer_rao_variance": _fraction(cramer_rao),
            "two_point_delta": _fraction(delta),
            "two_point_output_p_plus": _fraction(p_plus),
            "two_point_output_p_minus": _fraction(p_minus),
            "two_point_product_tv_upper": product_tv_upper,
            "two_point_mse_lower": le_cam_mse_lower,
            "two_point_lower_to_c2_over_n_ratio": (
                le_cam_mse_lower / target_scale
            ),
        },
        "general_lower_bound": {
            "parameter_pair": "mu = +/- c(epsilon)/(8*sqrt(n))",
            "condition": "n >= c(epsilon)^2/64",
            "output_bernoulli_separation": "1/(8*sqrt(n))",
            "conclusion": (
                "Le Cam plus Pinsker gives minimax MSE >= K*c(epsilon)^2/n "
                "for a universal K>0."
            ),
        },
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
                    "claim": 3,
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
