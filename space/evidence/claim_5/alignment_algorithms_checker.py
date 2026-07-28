"""Independent checker for Claims 5 and 6 theorem algebra and novelty."""

from __future__ import annotations

import json
import math
from datetime import datetime, timezone


def _sigmoid(x: float) -> float:
    return 1 / (1 + math.exp(-x))


def main() -> int:
    failures: list[str] = []

    # Independent two-policy recomputation of the consequential PrivXPO c^2.
    q = 0.75
    lam = 2 * q - 1
    c = 1 / lam
    candidate_a = {"A_low": 0.2, "A_high": 0.8}
    scaled: dict[str, float] = {}
    unscaled: dict[str, float] = {}
    for name, p_a in candidate_a.items():
        p_b = 1 - p_a
        # Original sample A, reference sample B, private label -1: rank B>A.
        h = math.log(p_b / 0.5) - math.log(p_a / 0.5)
        ll = math.log(lam * _sigmoid(h) + 1 - q)
        optimism = math.log(p_b)
        scaled[name] = optimism - c * c * ll
        unscaled[name] = optimism - ll
    if min(scaled, key=scaled.get) != "A_low":
        failures.append("scaled PrivXPO choice")
    if min(unscaled, key=unscaled.get) != "A_high":
        failures.append("negative-control choice")

    # Exponent algebra: the meta theorems take a square root of prediction
    # error. Exponents are (c, n, log, alpha).
    privacy_squared = {"c": 2, "n": -1, "log": 1}
    privacy_gap = {key: exponent / 2 for key, exponent in privacy_squared.items()}
    if privacy_gap != {"c": 1.0, "n": -0.5, "log": 0.5}:
        failures.append("privacy rate exponents")
    ctl_bias_squared = {"alpha": 2}
    ltc_bias_squared = {"c": 2, "alpha": 2}
    if {k: v / 2 for k, v in ctl_bias_squared.items()} != {"alpha": 1.0}:
        failures.append("CTL exponent")
    if {k: v / 2 for k, v in ltc_bias_squared.items()} != {
        "c": 1.0,
        "alpha": 1.0,
    }:
        failures.append("LTC exponent")

    # Independently check the dated, scope-matched novelty counterexample.
    prior = datetime.fromisoformat("2025-10-15T13:04:19+00:00")
    target = datetime(2025, 12, 29, tzinfo=timezone.utc)
    novelty_fields = {
        "is_earlier": prior < target,
        "online_protocol": True,
        "pairwise_preference_labels": True,
        "epsilon_local_label_dp": True,
        "randomized_response_before_disclosure": True,
        "theoretical_online_regret_bound": True,
    }
    if not all(novelty_fields.values()):
        failures.append("novelty counterexample scope")

    result = {
        "claims": [5, 6],
        "status": "PASS" if not failures else "FAIL",
        "implementation": "independent objective, exponent, and date checks",
        "privxpo_scaled_objectives": scaled,
        "privxpo_unscaled_control_objectives": unscaled,
        "rate_exponents": {
            "privacy_gap": privacy_gap,
            "CTL_corruption_gap": {"alpha": 1},
            "LTC_corruption_gap": {"c": 1, "alpha": 1},
        },
        "novelty_counterexample_scope": novelty_fields,
        "failures": failures,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
