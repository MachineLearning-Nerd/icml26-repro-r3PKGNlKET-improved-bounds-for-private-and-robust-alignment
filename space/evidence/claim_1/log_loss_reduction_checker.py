"""Independent Decimal checker for the Lemma 3.1 reduction."""

from __future__ import annotations

import json
from decimal import Decimal, getcontext
from fractions import Fraction


getcontext().prec = 70


def _d(value: Fraction) -> Decimal:
    return Decimal(value.numerator) / Decimal(value.denominator)


def main() -> int:
    qs = [Fraction(3, 5), Fraction(2, 3), Fraction(3, 4), Fraction(4, 5)]
    ps = [Fraction(k, 8) for k in range(1, 8)]
    checked = 0
    failures: list[str] = []
    for q in qs:
        lam = 2 * q - 1
        c = 1 / lam
        for p in ps:
            for r in ps:
                if p == r:
                    continue
                pt = lam * p + 1 - q
                rt = lam * r + 1 - q
                clean_tv = abs(p - r)
                private_tv = abs(pt - rt)
                hp = _d(pt).sqrt()
                hr = _d(rt).sqrt()
                hq = (Decimal(1) - _d(pt)).sqrt()
                hs = (Decimal(1) - _d(rt)).sqrt()
                h2 = (hp - hr) ** 2 + (hq - hs) ** 2
                affinity = hp * hr + hq * hs
                if private_tv != lam * clean_tv:
                    failures.append("TV contraction")
                if c * c * private_tv * private_tv != clean_tv * clean_tv:
                    failures.append("c^2 rescaling")
                if abs(affinity - (Decimal(1) - h2 / 2)) > Decimal("1e-60"):
                    failures.append("affinity identity")
                if _d(private_tv * private_tv) > h2:
                    failures.append("TV/Hellinger")
                checked += 1
    result = {
        "claim": 1,
        "status": "PASS" if not failures else "FAIL",
        "implementation": "independent Decimal arithmetic; no primary imports",
        "cases_checked": checked,
        "precision_digits": getcontext().prec,
        "failures": sorted(set(failures)),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
