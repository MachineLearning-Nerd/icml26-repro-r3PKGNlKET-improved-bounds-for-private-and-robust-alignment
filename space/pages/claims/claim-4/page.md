# Claim 4 — corruption/privacy ordering

**VERIFIED.** Exact expectation calculation gives an `alpha`-order CTL bias
and a `c(epsilon) alpha`-order LTC bias. Endpoint adversaries show both orders
are attained up to universal constants.

## Exact definitions and quantifiers

[Definition 2.4](https://ar5iv.labs.arxiv.org/html/2512.23816#S2.Thmtheorem4)
defines CTL as Huber replacement followed by randomized response, and LTC in
the reverse order. The result applies for every clean conditional mean
`h in [-1,1]`, adversarial replacement mean `b in [-1,1]`,
`alpha in [0,1/2)`, and epsilon > 0.

After multiplying the observed label by `c=1/(2q-1)`:

```text
CTL: F=(1-alpha)h+alpha b
     |F-h|=alpha|b-h| <= 2 alpha.

LTC: F=(1-alpha)h+alpha c b
     |F-h|=alpha|c b-h| <= alpha(c+1) <= 2c alpha.
```

Choosing `(h,b)=(1,-1)` attains `2alpha` for CTL. Choosing
`(h,b)=(-1,1)` attains `(c+1)alpha` for LTC, which lies between `c alpha`
and `2c alpha`.

## Inline exact fixture

| Quantity | Exact value |
| --- | ---: |
| `q`; contraction; `c` | 3/4; 1/2; 2 |
| `alpha` | 1/5 |
| tight CTL bias / upper | 2/5; 2/5 |
| tight LTC bias / upper | 3/5; 4/5 |
| ratio of squared upper terms | 4 |
| independent cases | 1,600 |

The unexplained historical ratio near `c^2` conflated squared error with
conditional-mean bias. The table distinguishes them.

## Reproducible evidence

- [Claim contract](../../../evidence/claim_4/claim_contract.json)
- [Primary verifier](../../../evidence/claim_4/corruption_order.py)
- [Independent checker](../../../evidence/claim_4/corruption_order_checker.py)
- [Raw results](../../../evidence/claim_4/raw_results.json)
- [Checker output](../../../evidence/claim_4/checker_output.json)
- [Failing negative control](../../../evidence/claim_4/negative_control_output.json)
- [Source audit](../../../evidence/claim_4/source_audit.md)
- [Method](../../../evidence/claim_4/method.md)
- [Limitations](../../../evidence/claim_4/limitations.md)
- [Runtime](../../../evidence/claim_4/runtime.json)
- [Fixed command](../../../evidence/claim_4/command.txt)

The independent checker enumerates both generative processes from their label
distributions using exact Fraction arithmetic. It imports no primary
functions. The swapped-order control exits 1.
