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
- `meth:rate-bond-forward-valuation`: FRAs and their uses, SOFR futures, bond forwards, conversion factors and the cheapest to deliver. Corrected 2026-10-18 (PR #24 pass): Hull's Example 6.3 restated with its SOFR + 200 bp borrowing and quarter-year accrual, the hedge derived from rates. Corrected 2026-10-19 (second PR #24 pass): the original bond forward is built on one dated coupon calendar (Sunday coupon paid Monday, T+1 spot, act/360 repo), with a two-repo ledger and a carry identity.
- `meth:swap-valuation-replication`: interest-rate, currency and equity swaps by replication (Hull chaps. 7 and 34; Handbook chap. 64). Corrected 2026-10-18 (PR #24 pass): the next equity payment is worth N(E_t/E_0 - P(t,T_next)), 7.980133m in the example, separated from the whole equity leg and the net value; Hull's p. 778 expression and his Technical Note 19 are compared.

All partly checked 2026-10-18, draft. Examples in `notes/artefacts/forward-swap-valuation/forward-swap-checks.py`; human review is outstanding. Coverage records are editorial, not study. `def:derivative-contracts` and `res:cost-of-carry-forward-price` are extended by links, not repeated.

Written in the derivatives, portfolio and execution batch (2026-10-19):

In `option-valuation.tex` (topic `option-valuation`):

- `def:option-value-drivers`: exercise and time value and the six factors, with signs checked by bumping Hull's base case.
- `res:put-call-forward-parity`: put-call and put-call-forward parity with arbitrages and synthetic positions.
- `meth:one-period-binomial-valuation`: hedge and replication, risk neutrality and the irrelevance of the real-world probability.
- `meth:multi-period-binomial-valuation`: two-period European and American options, an option arbitrage and a caplet on the rate tree.
- `meth:black-model-rates-currencies`: the BSM call as a levered share position, Garman-Kohlhagen, and Black's model for futures options, caplets and swaptions (Hull chaps. 15, 17, 18, 29).
- `meth:greeks-delta-gamma-hedging`: Greeks, delta hedging against Hull's Table 19.4, gamma risk and implied volatility in trading.

In `option-strategies.tex` (topic `option-strategies`):

- `meth:option-replication-deltas`: replicating an asset with options and the deltas of hedged positions. Corrected 2026-10-19 (PR #25 pass): dividends carried through the identities; a fixed-strike short forward has spot delta -e^(-qT).
- `meth:covered-call-protective-put`: covered calls, protective puts and short-position hedges.
- `meth:option-spreads-volatility-strategies`: spreads, straddles, collars, calendar spreads and skew, with a summary table. Corrected 2026-10-19 (PR #25 pass): calendar-spread values and profits distinguished.
- `ex:option-strategy-selection-case`: strategy choice for a single-stock holding and option positions targeting exposures.

All partly checked 2026-10-19, draft. Examples in `notes/artefacts/option-valuation/option-valuation-checks.py` and `notes/artefacts/option-strategies/option-strategy-checks.py`; human review is outstanding. Coverage records are editorial, not study. `mod:black-scholes-merton`, `def:implied-volatility-surface` and `meth:option-payoff-profit` are linked, not repeated.

Written in library gap-filling Batch L1 (2026-10-21):

- New topic file `compendium/volatility-options/numerical-methods.tex`: `meth:finite-difference-option-pricing` (explicit and Crank-Nicolson schemes, the monotonicity condition with the discount term, upwinding, boundaries, American exercise by projection and projected SOR) and `meth:least-squares-monte-carlo` (Hull's eight-path example, a 50-date Bermudan put, in-sample against out-of-sample bias). Checks in `notes/artefacts/numerical-pricing/numerical-pricing-checks.py`.
- New topic file `compendium/volatility-options/exotic-options.tex`: `meth:digital-option-valuation` (cash and asset digitals, the call as their difference, call-spread limit, pin risk), `meth:barrier-option-valuation` (in-out parity, the down-and-out call, Brownian-bridge and discretely monitored simulation, the Broadie-Glasserman-Kou shift, vega near the barrier) and `meth:asian-option-valuation` (discrete and continuous geometric averages, a geometric control for the arithmetic average, and a negative-carry case where the Asian call exceeds the vanilla). Checks in `notes/artefacts/exotic-options/exotic-option-checks.py`.
- `compendium/volatility-options/option-valuation.tex`: new `res:delta-hedging-volatility-mismatch` (hedging with actual against implied volatility, Wilmott chap. 12, with the nonnegative-gamma condition and a cash-digital counterexample; discrete-hedging error, chap. 47), with checks in `notes/artefacts/option-valuation/volatility-mismatch-hedging-check.py`; `meth:greeks-delta-gamma-hedging` extended with vanna and volga and a link to the new entry. `meth:active-currency-strategies` (currency-markets) gained a See also link only.

Sources: Hull, *Options, Futures, and Other Derivatives*, 11th Global ed., and Wilmott, *Paul Wilmott on Quantitative Finance*, 2nd ed. (chapters listed in the record). Synthetic examples only. Partly checked 2026-10-21, draft; human review outstanding. See [record](../source-review-records.md#library-gap-filling-batch-l1-21-october-2026).

Written in library gap-filling Batch L2 (2026-10-21), decision L2-D5: `meth:multi-period-binomial-valuation` extended with known dollar dividends in a recombining tree (Hull's Example 21.5 reproduced) and dividend-motivated early exercise of an American call; `meth:black-model-rates-currencies` extended with the receiver swaption, payer-receiver parity and the callable bond as a straight bond less a receiver swaption. Checks in `notes/artefacts/option-valuation/dividend-tree-swaption-checks.py`. Partly checked 2026-10-21, draft; human review outstanding. See [record](../source-review-records.md#library-gap-filling-batch-l2-21-october-2026).

Written in library gap-filling Batch L4 (2026-10-21):

- `meth:monte-carlo-greeks` (new, `numerical-methods.tex`): resimulation with common random numbers and its bias-variance choice of step, pathwise and likelihood-ratio delta and vega (Broadie and Glasserman 1996), the digital whose pathwise delta is zero on every path, the gamma boundary term, and the strike case. Checks in `notes/artefacts/numerical-pricing/monte-carlo-greeks-check.py`.
- `meth:cross-currency-basis-swaps` (new, `forward-commitment-valuation.tex`): constant-notional cash flows by party, the dollar-leg (BIS) and foreign-leg (Du-Tepper-Verdelhan) sign conventions with annualisation, synthetic dollar funding and the principal exchanges, on overnight-rate legs. Checks in `notes/artefacts/forward-swap-valuation/cross-currency-basis-check.py`. `meth:swap-valuation-replication` gained a See also link and lost a stray comma; `meth:digital-option-valuation` gained a link.

Sources: Hull, 11th Global ed.; Broadie and Glasserman (1996); Ding, Liu and Rutkowski (arXiv v3); Borio et al. (BIS Quarterly Review, September 2016). Synthetic examples only. Partly checked 2026-10-21, draft; human review outstanding. See [record](../source-review-records.md#library-gap-filling-batch-l4-21-october-2026).

Written in library gap-filling Batch L5 (2026-10-21):

- `meth:lookback-option-valuation` (new, `exotic-options.tex`, whose section heading now names lookbacks): floating and fixed-strike payoffs, Hull's floating formulas with the extreme to date and the fixed-strike parity relation, Wilmott's state-variable formulation and jump condition, Example 26.2, seasoned contracts, and discrete against continuous monitoring on coupled grids with an exact Brownian-bridge extreme (no barrier shift transplanted). Checks in `notes/artefacts/exotic-options/lookback-option-check.py`. `meth:barrier-option-valuation` gained a See also link.
- `meth:transaction-cost-hedging` (new, `option-valuation.tex`, after `res:delta-hedging-volatility-mismatch`, which gained a link): Leland's adjusted volatilities for long and short positions (cited through Wilmott chap. 48; Leland 1985 not read), the Hoggard-Whalley-Wilmott equation and nonadditivity, the admissible domain of the long formula, fixed-interval against band rebalancing as Wilmott reports it, and a simulated comparison of hedging costs with the Leland premium. Checks in `notes/artefacts/option-valuation/transaction-cost-hedging-check.py`.
- `meth:monte-carlo-greeks`: the resimulation-bias sentence corrected (generally biased; more paths do not remove it; affine prices excepted).

Sources: Hull, 11th Global ed., sec. 26.11; Wilmott, 2nd ed., chaps. 24, 26 and 48. Synthetic examples only. Partly checked 2026-10-21, draft; human review outstanding. See [record](../source-review-records.md#library-gap-filling-batch-l5-21-october-2026).

## Source verification after macro markets and pricing review

empirical extensions (2026-10-17) (six audit repairs and a source-review coverage; source verification and bounded tests, not study or human review): `mod:black-scholes-merton` resolved (new entry `mod:black-scholes-merton`); `def:implied-volatility-surface` resolved (new entry `def:implied-volatility-surface`). The record is in `notes/source-review-records.md`, *empirical extensions (2026-10-17)*.

derivatives and empirical validation (2026-10-17) (seven audit repairs, backlog reconciliation and a source-review coverage; source verification and bounded tests, not study or human review): the `def:implied-volatility-surface` question: arXiv v1 and v2 of Gatheral and Jacquier carry the same density slip, merged into `def:implied-volatility-surface`; the `meth:leland-cost-adjusted-volatility` question (Leland 1985) blocked, no open copy. New entries for the option-pricing pathway are listed in `option-pricing-models`. The record is in `notes/source-review-records.md`, *derivatives and empirical validation (2026-10-17)*.

## Related entries owned elsewhere

Cross-referenced, not owned here: `mech:futures-margin-settlement` (`futures-execution`, extended with Hull's generic margin account); `mech:otc-clearing-collateral`, `def:interest-rate-measures`, `mod:forward-rates-fra`, `mod:duration-convexity`, `conv:us-rate-quotation` (`rates-credit-mortgages`); `def:futures-hedge-basis`, `mod:minimum-variance-hedge-ratio` (`commodity-hedging`); `res:synthetic-short-put-call` (`synthetic-equity-cfd-trs`); `def:arbitrage` (`execution-market-making`).

## Entry backlog

## What changed in my view or practice

## Questions carried forward

- Which edition of Hull did the earlier notes follow? They match the 11th Global edition's wording closely but are not dated.
