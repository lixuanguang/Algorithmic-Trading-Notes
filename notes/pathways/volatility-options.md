---
key: volatility-options
section: volatility-options
status: not started (draft entries only, not from study)
---

# Option pricing, volatility models and hedging (section overview)

Overview outcome, from the guide: fit an arbitrage-free volatility surface to an option chain and compare delta and delta-vega hedges of one position on profit and loss, costs and tail losses under observed and stressed smile moves. Its readings are `s7-hulloptions`, `s6-blackscholes`, `p2-merton`, `s6-surface`, `exp-lee-wings`, `exp-gatheral-jacquier-svi` and `s6-glasserman`.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 15 October 2026 by derivatives and hedging review (`notes/source-review-records.md`). Only the derivatives basics and forward pricing are owned here; the rest of those notes went to `rates-credit-mortgages`, `commodity-hedging` and `futures-execution`. The entries come from source checking against Hull's 11th Global edition (`s7-hulloptions`, chaps. 1, 2 and 5), the overview's first reading, but that is not study of it: no option-pricing, volatility-surface or hedging material has been written, and the checkpoint was not attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in derivatives and hedging / source review / optimal execution / high-frequency strategies reviews:

- `def:derivative-contracts`: spot, forward, futures and options; payoffs, rights and obligations, payoff against profit and premium, exercise styles, futures specification, price limits and convergence (redrawn figure); notional against market value.
- `res:cost-of-carry-forward-price`: no-arbitrage forward prices with income, yield and storage; the value of an existing forward; index arbitrage and interest rate parity; investment against consumption assets (only an upper bound for the latter) and convenience yield; when forward and futures prices are equal.

Both partly checked 2026-10-15, draft; human review outstanding.

Written in empirical extensions (2026-10-17) (source verification and bounded checks, not study or human review):

- `mod:black-scholes-merton`: the model, its PDE, Greeks and Merton's no-early-exercise result, with own checks (`bsm-svi-checks.py`). Partly checked 2026-10-17, draft; human review outstanding.
- `def:implied-volatility-surface`: implied volatility, static-arbitrage conditions, SVI and Lee's wing formula, with a recorded source discrepancy. Partly checked 2026-10-17, draft; human review outstanding.

Written in the fixed-income and derivatives batch (2026-10-18):

In `derivative-markets-uses.tex` (topic `derivative-instruments`):

- `def:derivative-markets-otc-exchange`: exchange and OTC markets, clearing house and CCP, reforms as Hull states them in 2021, size (Hull chap. 1); the Handbook's SEF wording corrected.
- `def:derivative-types-commitments-contingent`: forwards, futures and swaps against options and CDS; linear and non-linear payoffs.
- `meth:option-payoff-profit`: payoffs, profits, break-evens, moneyness, intrinsic and time value (Hull chap. 10).
- `def:derivative-uses-risks`: hedgers, speculators and arbitrageurs; issuer and investor uses; leverage, counterparty, operational, legal and systemic risks (Hull chaps. 1 and 7).

In `forward-commitment-valuation.tex` (topic `forward-commitment-valuation`):

- `meth:arbitrage-replication-carry`: arbitrage, replication, forward against expected spot, carry; commitments against contingent claims.
- `meth:forward-price-value-lifecycle`: price against value at inception, during the life and at expiry.
- `res:forward-futures-price-difference`: equality with known rates and the correlation argument, with a two-period tree (Hull sec. 5.8).
- `def:swaps-as-forward-strips`: swaps as strips of off-market forwards and as bond packages; swap price against value.
- `meth:equity-forward-futures-valuation`: dividends, yields, index futures and the value of an existing contract. Corrected 2026-10-18 (PR #24 pass): the discrete-dividend replication borrows the full spot and repays the loan with each dividend (debt 101.020320 at maturity).
- `meth:rate-bond-forward-valuation`: FRAs and their uses, SOFR futures, bond forwards, conversion factors and the cheapest to deliver. Corrected 2026-10-18 (PR #24 pass): Hull's Example 6.3 restated with its SOFR + 200 bp borrowing and quarter-year accrual, the hedge derived from rates.
- `meth:swap-valuation-replication`: interest-rate, currency and equity swaps by replication (Hull chaps. 7 and 34; Handbook chap. 64). Corrected 2026-10-18 (PR #24 pass): the next equity payment is worth N(E_t/E_0 - P(t,T_next)), 7.980133m in the example, separated from the whole equity leg and the net value; Hull's p. 778 expression and his Technical Note 19 are compared.

All partly checked 2026-10-18, draft. Examples in `notes/artefacts/forward-swap-valuation/forward-swap-checks.py`; human review is outstanding. Coverage records are editorial, not study. `def:derivative-contracts` and `res:cost-of-carry-forward-price` are extended by links, not repeated.

## Source verification after macro markets and pricing review

empirical extensions (2026-10-17) (six audit repairs and a source-review coverage; source verification and bounded tests, not study or human review): `mod:black-scholes-merton` resolved (new entry `mod:black-scholes-merton`); `def:implied-volatility-surface` resolved (new entry `def:implied-volatility-surface`). The record is in `notes/source-review-records.md`, *empirical extensions (2026-10-17)*.

derivatives and empirical validation (2026-10-17) (seven audit repairs, backlog reconciliation and a source-review coverage; source verification and bounded tests, not study or human review): the `def:implied-volatility-surface` question: arXiv v1 and v2 of Gatheral and Jacquier carry the same density slip, merged into `def:implied-volatility-surface`; the `meth:leland-cost-adjusted-volatility` question (Leland 1985) blocked, no open copy. New entries for the option-pricing pathway are listed in `option-pricing-models`. The record is in `notes/source-review-records.md`, *derivatives and empirical validation (2026-10-17)*.

## Related entries owned elsewhere

Cross-referenced, not owned here: `mech:futures-margin-settlement` (`futures-execution`, extended with Hull's generic margin account); `mech:otc-clearing-collateral`, `def:interest-rate-measures`, `mod:forward-rates-fra`, `mod:duration-convexity`, `conv:us-rate-quotation` (`rates-credit-mortgages`); `def:futures-hedge-basis`, `mod:minimum-variance-hedge-ratio` (`commodity-hedging`); `res:synthetic-short-put-call` (`synthetic-equity-cfd-trs`); `def:arbitrage` (`execution-market-making`).

## Entry backlog

## What changed in my view or practice

## Questions carried forward

- Which edition of Hull did the earlier notes follow? They match the 11th Global edition's wording closely but are not dated.
