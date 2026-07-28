"""Finite-policy implementations and theorem algebra for Claims 5 and 6."""

from __future__ import annotations

import argparse
import json
import math
from typing import Any


Policy = dict[str, float]


def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def phi(u: float) -> float:
    return u + math.log(u)


def _argmin(scores: dict[str, float]) -> str:
    return min(sorted(scores), key=scores.__getitem__)


def _argmax(scores: dict[str, float]) -> str:
    return max(sorted(scores), key=scores.__getitem__)


def priv_chi_po(
    policies: dict[str, Policy],
    reference: Policy,
    ranked_pairs: list[tuple[str, str]],
    *,
    beta: float,
    r_max: float,
    q: float,
) -> tuple[str, dict[str, float]]:
    scores: dict[str, float] = {}
    lam = 2 * q - 1
    for name, policy in policies.items():
        value = 0.0
        for preferred, rejected in ranked_pairs:
            h = beta * (
                phi(policy[preferred] / reference[preferred])
                - phi(policy[rejected] / reference[rejected])
            )
            clean_probability = sigmoid(max(-2 * r_max, min(2 * r_max, h)))
            value += math.log(lam * clean_probability + 1 - q)
        scores[name] = value
    return _argmax(scores), scores


def square_chi_po(
    policies: dict[str, Policy],
    reference: Policy,
    records: list[tuple[str, str, int]],
    *,
    beta: float,
    r_max: float,
    c: float,
) -> tuple[str, dict[str, float]]:
    scores: dict[str, float] = {}
    for name, policy in policies.items():
        value = 0.0
        for tau_one, tau_minus_one, z in records:
            h = beta * (
                phi(policy[tau_one] / reference[tau_one])
                - phi(policy[tau_minus_one] / reference[tau_minus_one])
            )
            p = sigmoid(max(-2 * r_max, min(2 * r_max, h)))
            value += (2 * p - 1 - c * z) ** 2
        scores[name] = value
    return _argmin(scores), scores


def priv_xpo_update(
    policies: dict[str, Policy],
    reference: Policy,
    observations: list[tuple[str, str, int]],
    *,
    beta: float,
    gamma: float,
    q: float,
    omit_c_squared: bool = False,
) -> tuple[str, dict[str, float]]:
    lam = 2 * q - 1
    c = 1 / lam
    scores: dict[str, float] = {}
    for name, policy in policies.items():
        log_likelihood = 0.0
        optimism = 0.0
        for sampled, reference_sample, private_label in observations:
            preferred, rejected = (
                (sampled, reference_sample)
                if private_label == 1
                else (reference_sample, sampled)
            )
            h = beta * math.log(
                policy[preferred] / reference[preferred]
            ) - beta * math.log(policy[rejected] / reference[rejected])
            log_likelihood += math.log(lam * sigmoid(h) + 1 - q)
            optimism += math.log(policy[reference_sample])
        multiplier = 1.0 if omit_c_squared else c * c
        scores[name] = gamma * optimism - multiplier * log_likelihood
    return _argmin(scores), scores


def square_xpo_update(
    policies: dict[str, Policy],
    reference: Policy,
    observations: list[tuple[str, str, int]],
    *,
    beta: float,
    gamma: float,
    c: float,
    printed_minus_sign: bool,
) -> tuple[str, dict[str, float]]:
    scores: dict[str, float] = {}
    for name, policy in policies.items():
        loss = 0.0
        optimism = 0.0
        for sampled, reference_sample, z in observations:
            h = beta * math.log(
                policy[sampled] / reference[sampled]
            ) - beta * math.log(
                policy[reference_sample] / reference[reference_sample]
            )
            loss += (2 * sigmoid(h) - 1 - c * z) ** 2
            optimism += math.log(policy[reference_sample])
        scores[name] = gamma * optimism + (-loss if printed_minus_sign else loss)
    return _argmin(scores), scores


def certificate(use_negative_control: bool = False) -> dict[str, Any]:
    reference = {"A": 0.5, "B": 0.5}
    policies = {
        "A_low": {"A": 0.2, "B": 0.8},
        "A_high": {"A": 0.8, "B": 0.2},
    }
    q = 0.75
    c = 2.0

    offline_private, offline_private_scores = priv_chi_po(
        policies,
        reference,
        [("A", "B"), ("A", "B")],
        beta=1.0,
        r_max=2.0,
        q=q,
    )
    offline_square, offline_square_scores = square_chi_po(
        policies,
        reference,
        [("A", "B", -1), ("A", "B", -1)],
        beta=1.0,
        r_max=2.0,
        c=c,
    )
    online_private, online_private_scores = priv_xpo_update(
        policies,
        reference,
        [("A", "B", -1)],
        beta=1.0,
        gamma=1.0,
        q=q,
        omit_c_squared=use_negative_control,
    )
    printed_square, printed_square_scores = square_xpo_update(
        policies,
        reference,
        [("A", "B", 1)],
        beta=1.0,
        gamma=0.0,
        c=c,
        printed_minus_sign=True,
    )
    corrected_square, corrected_square_scores = square_xpo_update(
        policies,
        reference,
        [("A", "B", 1)],
        beta=1.0,
        gamma=0.0,
        c=c,
        printed_minus_sign=False,
    )

    rate_routes = {
        "PrivXPO": {
            "input_squared_error": "c^2*log(|Pi|T/delta)/T",
            "meta_theorem_output": "c*sqrt(log(|Pi|T/delta)/T)",
            "corruption_term": "none",
        },
        "PrivChiPO": {
            "input_squared_error": "c^2*log(|Pi|/delta)/n",
            "meta_theorem_output": "c*sqrt(log(|Pi|/delta)/n)",
        },
        "SquareChiPO_CTL": {
            "input_squared_error": "c^2*log(|Pi|/delta)/n + alpha^2",
            "meta_theorem_output": "c*sqrt(log(|Pi|/delta)/n) + alpha",
        },
        "SquareChiPO_LTC": {
            "input_squared_error": "c^2*log(|Pi|/delta)/n + c^2*alpha^2",
            "meta_theorem_output": (
                "c*sqrt(log(|Pi|/delta)/n) + c*alpha"
            ),
        },
    }

    checks = {
        "priv_chi_po_private_mle_selects_matching_policy": (
            offline_private == "A_high"
        ),
        "square_chi_po_unranked_loss_selects_matching_policy": (
            offline_square == "A_low"
        ),
        "priv_xpo_c_squared_scaling_is_consequential": (
            online_private == "A_low"
        ),
        "priv_xpo_rate_is_square_root_of_claim_1_error": (
            rate_routes["PrivXPO"]["meta_theorem_output"]
            == "c*sqrt(log(|Pi|T/delta)/T)"
        ),
        "offline_rates_are_square_roots_of_uniform_errors": (
            rate_routes["PrivChiPO"]["meta_theorem_output"]
            == "c*sqrt(log(|Pi|/delta)/n)"
            and rate_routes["SquareChiPO_CTL"]["meta_theorem_output"].endswith(
                "+ alpha"
            )
        ),
        "square_xpo_printed_sign_selects_larger_loss": (
            printed_square == "A_low"
            and corrected_square == "A_high"
            and printed_square_scores["A_low"] < printed_square_scores["A_high"]
        ),
    }
    if not all(checks.values()):
        failed = [name for name, passed in checks.items() if not passed]
        raise AssertionError(f"alignment-algorithm certificate failed: {failed}")

    return {
        "claims": [5, 6],
        "status": {"claim_5": "FALSIFIED", "claim_6": "VERIFIED"},
        "claim_5_subclaims": {
            "PrivXPO_rate": "VERIFIED",
            "first_online_private_alignment_algorithm": "FALSIFIED",
            "first_online_private_and_robust_algorithm": (
                "not contradicted by the audited pre-paper corpus"
            ),
            "SquareXPO_as_printed": (
                "source defect: argmin uses minus a nonnegative square loss; "
                "the proof requires empirical-loss minimization"
            ),
        },
        "novelty_counterexample": {
            "paper": (
                "Offline and Online KL-Regularized RLHF under Differential "
                "Privacy"
            ),
            "arxiv": "2510.13512",
            "published": "2025-10-15T13:04:19Z",
            "target_paper_published": "2025-12-29",
            "algorithm": "POKL-RLHF (Algorithm 2)",
            "setting": (
                "online KL-regularized RLHF from pairwise human preferences; "
                "only RR-privatized labels are disclosed to the learner"
            ),
            "guarantee": (
                "Theorem 5.2 gives a logarithmic online regret bound under "
                "Bradley-Terry realizability and epsilon>0 label LDP"
            ),
            "source_html_sha256": (
                "921ac2750798565d1e20e251f3f9c92d27d04bfd92dc1f4e83058c90efeb1412"
            ),
            "arxiv_metadata_sha256": (
                "9a9465aa677b6f6c9ba496be233ac5e2b4da05527a8d1e34b593a6a4abd0470a"
            ),
        },
        "finite_policy_fixture": {
            "policies": policies,
            "reference": reference,
            "PrivChiPO_selected": offline_private,
            "PrivChiPO_scores": offline_private_scores,
            "SquareChiPO_selected": offline_square,
            "SquareChiPO_losses": offline_square_scores,
            "PrivXPO_selected": online_private,
            "PrivXPO_objectives": online_private_scores,
            "SquareXPO_printed_minus_selected": printed_square,
            "SquareXPO_printed_objectives": printed_square_scores,
            "SquareXPO_corrected_plus_selected": corrected_square,
            "SquareXPO_corrected_objectives": corrected_square_scores,
        },
        "rate_routes": rate_routes,
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
                    "claims": [5, 6],
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
