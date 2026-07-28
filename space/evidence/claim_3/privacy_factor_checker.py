"""Independent Decimal checker for Claim 3.

This implementation intentionally shares no functions with the primary
Fraction-based certificate.
"""

from __future__ import annotations

import json
from decimal import Decimal, getcontext


def main() -> int:
    getcontext().prec = 60
    q = Decimal(3) / Decimal(4)
    lam = Decimal(2) * q - Decimal(1)
    c = Decimal(1) / lam
    mu = Decimal(1) / Decimal(4)
    n = Decimal(64)

    observed_mean = lam * mu
    recovered_mean = c * observed_mean
    variance = (c * c - mu * mu) / n
    fisher = lam * lam / (Decimal(1) - lam * lam * mu * mu)
    cramer_rao = Decimal(1) / (n * fisher)

    # Independently exhaust a grid of rational RR probabilities and means.
    grid_failures: list[str] = []
    for q_num in range(6, 10):
        q_grid = Decimal(q_num) / Decimal(10)
        lam_grid = Decimal(2) * q_grid - Decimal(1)
        c_grid = Decimal(1) / lam_grid
        for mu_num in range(-8, 9):
            mu_grid = Decimal(mu_num) / Decimal(10)
            privatized = lam_grid * mu_grid
            if c_grid * privatized != mu_grid:
                grid_failures.append(f"q={q_grid},mu={mu_grid}")

    checks = {
        "independent_unbiasedness": recovered_mean == mu,
        "independent_cramer_rao_equality": variance == cramer_rao,
        "exact_fixture_c": c == Decimal(2),
        "exhaustive_rational_grid": not grid_failures,
    }
    payload = {
        "claim": 3,
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "grid_cases": 4 * 17,
        "grid_failures": grid_failures,
        "variance": str(variance),
        "cramer_rao": str(cramer_rao),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
