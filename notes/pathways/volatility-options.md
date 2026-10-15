---
key: volatility-options
section: volatility-options
status: not started (draft entries from the migration only)
---

# Option pricing, volatility models and hedging (section overview)

Overview outcome, from the guide: fit an arbitrage-free volatility surface to an option chain and compare delta and delta-vega hedges of one position on profit and loss, costs and tail losses under observed and stressed smile moves. Its readings are `s7-hulloptions`, `s6-blackscholes`, `p2-merton`, `s6-surface`, `exp-lee-wings`, `exp-gatheral-jacquier-svi` and `s6-glasserman`.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 15 October 2026 by migration slice 31 (`notes/migration-slices.md`), which migrated the legacy Hull notes. Only the derivatives basics and forward pricing are owned here; the rest of those notes went to `rates-credit-mortgages`, `commodity-hedging` and `futures-execution`. The entries come from source checking against Hull's 11th Global edition (`s7-hulloptions`, chaps. 1, 2 and 5), the overview's first reading, but that is not study of it: no option-pricing, volatility-surface or hedging material has been written, and the checkpoint was not attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in migration slice 31, 2026-10-15:

- `def:derivative-contracts`: spot, forward, futures and options; payoffs, rights and obligations (the legacy reversed call and put rights), payoff against profit and premium, exercise styles, futures specification, price limits and convergence (redrawn figure); notional against market value.
- `res:cost-of-carry-forward-price`: no-arbitrage forward prices with income, yield and storage; the value of an existing forward; index arbitrage and interest rate parity; investment against consumption assets (only an upper bound for the latter) and convenience yield; when forward and futures prices are equal.

Both partly checked 2026-10-15, draft; human review outstanding. Artefacts: `notes/artefacts/volatility-options/hull-basics.tex` and `hull-forwards-futures.tex`, with the original figures.

## Related entries owned elsewhere

Cross-referenced, not owned here: `mech:futures-margin-settlement` (`futures-execution`, extended with Hull's generic margin account); `mech:otc-clearing-collateral`, `def:interest-rate-measures`, `mod:forward-rates-fra`, `mod:duration-convexity`, `conv:us-rate-quotation` (`rates-credit-mortgages`); `def:futures-hedge-basis`, `mod:minimum-variance-hedge-ratio` (`commodity-hedging`); `res:synthetic-short-put-call` (`synthetic-equity-cfd-trs`); `def:arbitrage` (`execution-market-making`).

## Entry backlog

- mod:black-scholes-merton: the Black-Scholes-Merton model, its assumptions and Greeks, toward the overview's hedging checkpoint (`s6-blackscholes`, `p2-merton`, Hull chaps. 15 and 19, unread).
- def:implied-volatility-surface: implied volatility, the smile and arbitrage-free surfaces (`s6-surface`, `exp-gatheral-jacquier-svi`, unread).

## Legacy candidate material

Run `python3 tools/migration_status.py` for the current counts. No legacy file lists this overview: slice 31 migrated `volatility-options/basic.tex` and removed the legacy chapter. That says nothing about consolidation.

## What changed in my view or practice

## Questions carried forward

- Which edition of Hull did the legacy notes follow? They match the 11th Global edition's wording closely but are not dated.
