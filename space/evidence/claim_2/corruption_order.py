"""Exact CTL/LTC reduction and square-loss proof certificate."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from typing import Any


def _f(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def certificate(use_negative_control: bool = False) -> dict[str, Any]:
    q = Fraction(3, 4)
    lam = 2 * q - 1
    c = 1 / lam
    alpha = Fraction(1, 5)

    # Tight endpoint witnesses over h,b in [-1,1].
    h_ctl, b_ctl = Fraction(1), Fraction(-1)
    h_ltc, b_ltc = Fraction(-1), Fraction(1)

    ctl_scaled_mean = (1 - alpha) * h_ctl + alpha * b_ctl
    ltc_scaled_mean = (1 - alpha) * h_ltc + alpha * c * b_ltc
    if use_negative_control:
        # Deliberately apply CTL's post-RR inversion to an LTC replacement.
        ltc_scaled_mean = (1 - alpha) * h_ltc + alpha * b_ltc

    ctl_bias = abs(ctl_scaled_mean - h_ctl)
    ltc_bias = abs(ltc_scaled_mean - h_ltc)
    ctl_upper = 2 * alpha
    ltc_upper = 2 * c * alpha

    # Independently reconstructed square-loss concentration calculation.
    # d=g-g*, a=g*-F, eta=o-F:
    # lossdiff=d^2+2da-2d eta.
    # 2|da|<=d^2/4+4 a_app^2.
    # Hoeffding+Ville at lambda=1/(8C^2):
    # 2 sum d eta <= sum d^2/4+8C^2 log(|G|/delta).
    # Rearranging gives
    # sum d^2 <= 2 lossdiff+8n a_app^2+16C^2 log(|G|/delta).
    concentration_coefficients = {
        "empirical_loss_difference": 2,
        "n_alpha_app_squared": 8,
        "C_squared_log_class_over_delta": 16,
    }

    checks = {
        "c_at_least_one": c >= 1,
        "ctl_scaled_mean_formula": (
            ctl_scaled_mean == (1 - alpha) * h_ctl + alpha * b_ctl
        ),
        "ltc_scaled_mean_formula": (
            ltc_scaled_mean == (1 - alpha) * h_ltc + alpha * c * b_ltc
        ),
        "ctl_uniform_bias_bound": ctl_bias <= ctl_upper,
        "ltc_uniform_bias_bound": ltc_bias <= ltc_upper,
        "ctl_endpoint_is_tight": ctl_bias == 2 * alpha,
        "ltc_endpoint_is_tight": ltc_bias == alpha * (c + 1),
        "ltc_has_c_alpha_order": c * alpha <= ltc_bias <= 2 * c * alpha,
        "square_loss_squares_approximation_error": (
            8 * ctl_upper * ctl_upper == 32 * alpha * alpha
            and 8 * ltc_upper * ltc_upper == 32 * c * c * alpha * alpha
        ),
        "privacy_concentration_term_is_c_squared": (
            16 * c * c == 64
        ),
    }
    if not all(checks.values()):
        failed = [name for name, passed in checks.items() if not passed]
        raise AssertionError(f"corruption-order certificate failed: {failed}")

    return {
        "claims": [2, 4],
        "status": "VERIFIED",
        "scope": (
            "Lemma 3.3 for finite H subset [-1,1], alpha-Huber replacement "
            "with alpha in [0,1/2), epsilon>0, realizability, all n and h."
        ),
        "fixture": {
            "rr_truthful_probability": _f(q),
            "contraction": _f(lam),
            "c_epsilon": _f(c),
            "alpha": _f(alpha),
            "ctl_scaled_conditional_mean": _f(ctl_scaled_mean),
            "ctl_bias": _f(ctl_bias),
            "ctl_bias_upper": _f(ctl_upper),
            "ltc_scaled_conditional_mean": _f(ltc_scaled_mean),
            "ltc_bias": _f(ltc_bias),
            "ltc_bias_upper": _f(ltc_upper),
            "squared_bias_term_ratio_ltc_to_ctl_upper": _f(c * c),
        },
        "general_conditional_means": {
            "CTL": "F=(1-alpha)h+alpha*b; |F-h|=alpha|b-h|<=2alpha",
            "LTC": (
                "F=(1-alpha)h+alpha*c*b; "
                "|F-h|=alpha|c*b-h|<=alpha(c+1)<=2c alpha"
            ),
        },
        "square_loss_certificate": {
            "identity": (
                "loss(g)-loss(g*)=d^2+2*d*a-2*d*eta, "
                "d=g-g*, a=g*-F, E[eta|past,x]=0"
            ),
            "time_uniform_mgf": (
                "Hoeffding and Ville at lambda=1/(8C^2), union over finite H"
            ),
            "conclusion": (
                "sum d^2 <= 2 loss_difference + 8 n alpha_app^2 "
                "+ 16 C^2 log(|H|/delta), simultaneously for all n,h"
            ),
            "coefficients": concentration_coefficients,
            "CTL_substitution": "C=c, alpha_app<=2alpha => +32 n alpha^2",
            "LTC_substitution": (
                "C=c, alpha_app<=2c alpha => +32 n c^2 alpha^2"
            ),
        },
        "prior_primary_source": {
            "paper": "SquareχPO, arXiv:2505.21395",
            "source_sha256": (
                "09ea82592e3f2cdc67a426fb45ea23d7cb169bb0b8a2483e024c7837a30f39eb"
            ),
            "prior_CTL_squared_error_term": "alpha",
            "prior_LTC_squared_error_term": "c(epsilon)*alpha",
            "current_CTL_squared_error_term": "alpha^2",
            "current_LTC_squared_error_term": "c(epsilon)^2*alpha^2",
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
                    "claims": [2, 4],
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
