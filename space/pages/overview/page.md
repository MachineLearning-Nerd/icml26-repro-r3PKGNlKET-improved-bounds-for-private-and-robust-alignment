# overview


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_735df14ae899", "created_at": "2026-07-28T09:05:48+00:00", "title": "Overview"}
-->
# Private & Robust Alignment Bounds (r3PKGNlKET)

**arXiv 2512.23816** · Weng/He/Zhou · ICML 2026
**Score: 12 / 12 — 6 of 6 claims VERIFIED** (numpy, CPU).

| # | Claim | Result |
|---|-------|--------|
| C0 | Lemma 3.1 log-loss MLE under LDP optimal | error ~c(ε)²/n (slope −1.00), no de-biasing |
| C1 | Lemma 3.3 square-loss CTL bias | excess risk = α² (ratio ≈1) |
| C2 | c(ε)=(eᵋ+1)/(eᵋ−1) optimal privacy cost | =1/tanh(ε/2); MLE var = Cramér-Rao bound |
| C3 | CTL vs LTC ordering | LTC/CTL bias ratio ≈ c(ε)²=4.68 |
| C4 | Thm 4.4 online gap ~c(ε)/√n | slope −1/2 (log loss, no α) |
| C5 | Thm 5.2 offline/square gap ~c(ε)/√n+α | slope −1/2 + α floor |

See outputs/verdict.json, outputs/gate.json.
