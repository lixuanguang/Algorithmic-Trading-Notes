---
key: fx-dealer-market-making
section: execution-market-making
status: not started (draft entries from the migration only)
---

# FX dealing: internalisation, last look and hedging

Pathway outcome, from the guide: price a spot FX client franchise, choose between internalising and hedging inventory across currency pairs, and evaluate aggregator and last-look practices against fill and markout evidence. Its checkpoint sets spreads and an inventory skew for one pair, compares internalising only, hedging immediately and a mixed policy, then adds a last-look window and reports fill rates, reject rates and client markouts, stating which results depend on latency and client mix. Its twelve readings run from the King–Osler–Rime survey through FX order-flow evidence to internalisation (`cfd-butz-oomen-2019`), multi-currency skewing and hedging, and last look and aggregators (`dm-oomen-aggregator-2017`, `dm-oomen-last-look-2017`, `dm-cartea-jaimungal-walton-2019`).

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 15 October 2026 by migration slice 20 (`notes/migration.md`), which migrated the legacy FX-market-microstructure file mapped to this pathway alone. The entries come from migration and source checking against the BIS Markets Committee's 2020 report (`exp-fx-algos`), the FX Global Code of December 2024 (`exp-fx-code`), one provider's 2025 disclosure, and two of this pathway's readings in open versions (`cfd-butz-oomen-2019` accepted manuscript; `dm-cartea-jaimungal-walton-2019` arXiv v1). That is not study of the readings, and the checkpoint was not attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in migration slice 20, 2026-10-15:

- `def:fx-market-structure`: fragmentation without a consolidated tape; venues and access channels, RFQ/RFS risk transfer, firm and non-firm liquidity, principal and franchise liquidity; internalisation as a dealer choice; transaction cost analysis metrics including reject ratios.
- `mod:fx-internalisation-horizon`: Butz and Oomen's queue model: conditional horizon $L/\lambda$ of a risk-increasing trade, all-trade average $W=L/(2\lambda)\approx(R/\lambda_0)c_R/\sqrt{2\pi}$ with $\lambda_0$ the baseline intensity; EUR/USD calibration recomputed (all-trade 1.39 minutes, conditional about 2.78) and the costs of position skewing.
- `mech:fx-last-look`: the FX Global Code's Principle 17 (voluntary, December 2024) with all three cover-and-deal conditions, one provider's disclosed terms (September 2025; spot price check up to 10 ms, no additional hold), decision time against check time and additional hold, firm against conditional quotes, price against validity rejections and technical failures, and the Cartea–Jaimungal–Walton model prediction.

All three: verification partly checked 2026-10-15, stability draft; human review outstanding. Their artefact is `notes/artefacts/fx-dealer-market-making/derivations.tex`.

## Related entries owned elsewhere

Cross-referenced, not owned here: `def:dealer-inventory-risk`, `meth:dealer-quote-adjustment`, `mod:inventory-based-quotes` (`market-making-lob` and `execution-market-making`); `def:smart-order-routing`, `def:best-execution` (`market-structure-execution-quality`); `res:latency-arbitrage-arms-race` (`hft-market-design`). None of them is FX evidence.

Slice 36, 2026-10-16: cyclic (triangular) currency arbitrage is in `def:arbitrage` (owned by `execution-market-making`): the no-arbitrage band with bid and ask quotes, derived and checked, and Harris's three-legged currency box recomputed. It concerns cross-pair pricing, which bears on this pathway's choice between internalising and hedging across currency pairs, but it is Harris's arbitrage material, so it was not written as an entry here.

Slice 37, 2026-10-16: the legacy macro chapter's FX market-structure block was merged into `def:fx-market-structure` (Gliner's $4 trillion and trading hours, the BIS's $9.6 trillion for April 2025, and the legacy's "5.5 days" corrected). The dollar, the dollar index and the SDR are in `def:us-dollar-dxy-sdr` (`currency-markets`).

Slice-36 follow-up, 2026-10-16: `def:arbitrage` now states the triangular equality only for frictionless quotes; with spreads, cross-rate midpoints may differ while no executable cycle profits (EUR/USD, USD/JPY, EUR/JPY example recomputed).

## Entry backlog

- ev:fx-last-look-fill-reject-evidence: measured fill rates, reject rates, hold times and client markouts under last look against firm liquidity, with benchmarks, horizons and selection effects; Oomen's last-look and aggregator papers (unread) and empirical FX studies are needed before such an entry.

## Legacy candidate material

Run `python3 tools/migration_status.py` for the current counts. After slice 20 no legacy file lists this pathway.

## What changed in my view or practice

## Questions carried forward

- Read Oomen (2017) on last look and on aggregators; no open copy was found on 2026-10-15.
- Read King, Osler and Rime (2013) for FX market structure.
- Fixing windows were left to `fx-funding-settlement`; prime-broker access was not checked.
