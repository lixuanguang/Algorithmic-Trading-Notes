---
key: crypto-perpetuals
section: digital-assets-prediction-markets
status: not started (draft entries from the migration only)
---

# Crypto perpetuals and cross-venue basis

Pathway outcome, from the guide: reconcile spot, perpetual and dated-futures basis with feasible financing, transfer, margin and liquidation paths across fragmented venues. Its checkpoint builds an hourly spot-perpetual ledger with mark, continuously accrued funding, fees, borrow, collateral and settlement, applies Deribit's selected rulebook and instrument-specific funding formula, and builds an executable price band from account-specific financing. Its thirteen readings run from settlement foundations (`crypto-narayanan`) and cross-venue arbitrage (`s6-makarov`), through carry (`roadmap-carry`), crypto factors, perpetual pricing (`roadmap-perpetual-pricing`, `roadmap-perpetual-fundamentals`), implied yield curves and basis risk (`s11-r15`), to option pricing on futures, venue documentation (`s11-r29`, `gapclose-deribit-rules`), data problems and portfolio construction.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 15 October 2026 by migration slice 24 (`notes/migration.md`), which routed all four blocks of the legacy crypto-market-microstructure file here, an exception to the file's map candidate `crypto-mm-microstructure`, whose outcome is the fee, impact, latency and adverse-selection terms of quoting one venue's order book; the blocks concern cross-venue structure, funding, margin and settlement. The entries come from migration and source checking against `s6-makarov` (2018 discussion paper), `roadmap-perpetual-pricing` (arXiv v2), `roadmap-perpetual-fundamentals` (arXiv v7, abstract only) and `gapclose-deribit-rules` (rulebook v2.0 and funding specification, retrieved 15 October 2026). That is not study of the readings, and the checkpoint was not attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in migration slice 24, 2026-10-15:

- `def:crypto-venue-instrument-structure`: executable venue prices, reference prices, fair-value models and legal best execution kept apart; Makarov–Schoar's 2017–2018 cross-country spreads and capital controls; spot, dated futures, perpetuals (linear, inverse, quanto, after Ackerer–Hugonnier–Jermann) and Deribit's European cash-settled options; on-chain pools not checked.
- `mech:perpetual-funding`: premium and interest terms and the long's cash flow (Ackerer–Hugonnier–Jermann); anchoring as a model result, no guaranteed convergence (He et al.); Deribit's sign convention, premium rate, damper, caps by currency, continuous accrual quoted per 8 hours, settlement-currency units, and 08:00 UTC cash settlement; worked examples recomputed by script.
- `def:crypto-trading-risk-layers`: Deribit's liquidation process, insurance fund, socialised loss and auto-deleveraging, and custody arrangements, kept apart from venue insolvency and from stablecoin, network and bridge risk (unchecked).
  Corrected 2026-10-15 (slice-24 follow-up): socialised loss is triggered at Deribit's absolute discretion when the fund is depleted in all currencies, or in the bankrupt account's currency when Deribit decides not to convert others (Rule 10.8); converting other currencies is itself discretionary (Rule 10.7).

All three: verification partly checked 2026-10-15, stability draft; human review outstanding. The artefact is `notes/artefacts/crypto-mm-microstructure/derivations.tex` (under the map candidate, keeping the file whole), with `funding_checks.py` beside it.

Written in the third batch of 2026-10-17 (source verification and bounded checks, not study or human review):

- `ev:crypto-dated-futures-carry`: dated-futures carry and its drivers, from BIS WP 1087 (archived copy). Partly checked 2026-10-17, draft; human review outstanding.
- `def:amm-pool-mechanics`: constant-product and concentrated-liquidity pools, with own checks (`batch60-amm-checks.py`). Partly checked 2026-10-17, draft; human review outstanding.

## Source verification after slice 37

Third batch of 2026-10-17 (six audit repairs and a 60-item queue; source verification and bounded tests, not study or human review): `ev:crypto-funding-crowding` narrowed (BIS WP 1087's dated-futures evidence and its restatements merged; a direct funding-rate study unread); `ev:crypto-dated-futures-carry` resolved (new entry `ev:crypto-dated-futures-carry` from BIS WP 1087 (archived copy)); `def:crypto-options-venue-structure` narrowed (a one-day Deribit API snapshot (inverse against USDC-settled listings, open-interest concentration) merged into `def:crypto-venue-instrument-structure`; other venues unread); `def:amm-pool-mechanics` narrowed (new entry `def:amm-pool-mechanics` from the Uniswap v2 and v3 papers; gas costs not covered); `ev:stablecoin-network-settlement-risk` narrowed (the Federal Reserve's FEDS Note on USDC and SVB merged into `def:crypto-trading-risk-layers`). The record is in `notes/migration-slices.md`, *Third batch of 17 October 2026*.

## Related entries owned elsewhere

Cross-referenced, not owned here: `def:best-execution`, `def:smart-order-routing` (`market-structure-execution-quality`); `def:fx-market-structure` (`fx-dealer-market-making`); `res:arbitrage-risks` (`execution-market-making`); `mech:futures-margin-settlement` (`futures-execution`); `def:securities-lending-fee-rebate` (`money-markets-repo-lending`). None of them is crypto evidence.

## Entry backlog

- ev:crypto-funding-crowding: (narrowed in the third batch of 2026-10-17) whether funding rates measure crowding or leverage demand, against the legacy claim; needs empirical evidence (for example `s11-r15` or `roadmap-carry`, unread).
- def:crypto-options-venue-structure: (narrowed in the third batch of 2026-10-17) crypto option venues, strike concentration and inverse payoffs, against the legacy "fewer venues and strikes"; belongs to `crypto-options-numeraire`.
- def:amm-pool-mechanics: (narrowed in the third batch of 2026-10-17) constant-function pools, inventory curves and gas costs; belongs to `amm-lending`.
- ev:stablecoin-network-settlement-risk: (narrowed in the third batch of 2026-10-17) stablecoin redemption and depeg, chain congestion, reorganisations and bridge or transfer delay; belongs to `stablecoin-pegs-runs` and the section overview.

## Legacy candidate material

Run `python3 tools/migration_status.py` for the current counts. No legacy file lists this pathway.

## What changed in my view or practice

## Questions carried forward

- Read Deribit's Exchange Membership Terms, clause 12, for the full liquidation waterfall and the Liquidity Support Program.
- Read Gornall, Rinaldi and Xiao (`s11-r15`) and the BIS carry paper in full; neither was retrieved.
- Check other venues' funding cadence, interest term and clamps before generalising.
