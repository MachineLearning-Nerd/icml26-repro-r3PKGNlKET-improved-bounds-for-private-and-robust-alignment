"""Independent exhaustive checker for CTL and LTC conditional means."""

from __future__ import annotations

import json
from fractions import Fraction


def main() -> int:
    qs = [Fraction(3, 5), Fraction(2, 3), Fraction(3, 4), Fraction(4, 5)]
    alphas = [Fraction(0), Fraction(1, 20), Fraction(1, 5), Fraction(2, 5)]
    values = [
        Fraction(-1),
        Fraction(-3, 4),
        Fraction(-1, 2),
        Fraction(-1, 4),
        Fraction(0),
        Fraction(1, 5),
        Fraction(1, 4),
        Fraction(1, 2),
        Fraction(3, 4),
        Fraction(1),
    ]
    failures: list[str] = []
    checked = 0
    for q in qs:
        c = 1 / (2 * q - 1)
        for alpha in alphas:
            for h in values:
                for b in values:
                    ctl = (1 - alpha) * h + alpha * b
                    ltc = (1 - alpha) * h + alpha * c * b
                    if abs(ctl - h) > 2 * alpha:
                        failures.append("CTL bias")
                    if abs(ltc - h) > 2 * c * alpha:
                        failures.append("LTC bias")
                    # Exact expectation obtained by enumerating clean label,
                    # Huber replacement, and RR output.
                    clean_plus = (1 + h) / 2
                    bad_plus = (1 + b) / 2
                    corrupt_plus = (1 - alpha) * clean_plus + alpha * bad_plus
                    ctl_z_plus = q * corrupt_plus + (1 - q) * (1 - corrupt_plus)
                    ctl_enum = c * (2 * ctl_z_plus - 1)
                    rr_clean_plus = q * clean_plus + (1 - q) * (1 - clean_plus)
                    ltc_z_plus = (1 - alpha) * rr_clean_plus + alpha * bad_plus
                    ltc_enum = c * (2 * ltc_z_plus - 1)
                    if ctl_enum != ctl:
                        failures.append("CTL enumeration")
                    if ltc_enum != ltc:
                        failures.append("LTC enumeration")
                    checked += 1
    result = {
        "claims": [2, 4],
        "status": "PASS" if not failures else "FAIL",
        "implementation": "independent exhaustive Fraction enumeration",
        "cases_checked": checked,
        "failures": sorted(set(failures)),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
