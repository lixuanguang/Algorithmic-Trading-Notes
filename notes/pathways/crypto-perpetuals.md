---
key: crypto-perpetuals
section: digital-assets-prediction-markets
status: not started (draft entries only, not from study)
---

# Crypto perpetuals and cross-venue basis

Pathway outcome, from the guide: reconcile spot, perpetual and dated-futures basis with feasible financing, transfer, margin and liquidation paths across fragmented venues. Its checkpoint builds an hourly spot-perpetual ledger with mark, continuously accrued funding, fees, borrow, collateral and settlement, applies Deribit's selected rulebook and instrument-specific funding formula, and builds an executable price band from account-specific financing. Its thirteen readings run from settlement foundations (`crypto-narayanan`) and cross-venue arbitrage (`s6-makarov`), through carry (`roadmap-carry`), crypto factors, perpetual pricing (`roadmap-perpetual-pricing`, `roadmap-perpetual-fundamentals`), implied yield curves and basis risk (`s11-r15`), to option pricing on futures, venue documentation (`s11-r29`, `gapclose-deribit-rules`), data problems and portfolio construction.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 15 October 2026 by crypto market structure review (`notes/source-review-index.md`). The entries come from source checking against `s6-makarov` (2018 discussion paper), `roadmap-perpetual-pricing` (arXiv v2), `roadmap-perpetual-fundamentals` (arXiv v7, abstract only) and `gapclose-deribit-rules` (rulebook v2.0 and funding specification, retrieved 15 October 2026). That is not study of the readings, and the checkpoint was not attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in crypto market structure / source review / optimal execution / high-frequency strategies reviews:

- `def:crypto-venue-instrument-structure`: executable venue prices, reference prices, fair-value models and legal best execution kept apart; Makarov–Schoar's 2017–2018 cross-country spreads and capital controls; spot, dated futures, perpetuals (linear, inverse, quanto, after Ackerer–Hugonnier–Jermann) and Deribit's European cash-settled options; on-chain pools not checked.
- `mech:perpetual-funding`: premium and interest terms and the long's cash flow (Ackerer–Hugonnier–Jermann); anchoring as a model result, no guaranteed convergence (He et al.); Deribit's sign convention, premium rate, damper, caps by currency, continuous accrual quoted per 8 hours, settlement-currency units, and 08:00 UTC cash settlement; worked examples recomputed by script.
- `def:crypto-trading-risk-layers`: Deribit's liquidation process, insurance fund, socialised loss and auto-deleveraging, and custody arrangements, kept apart from venue insolvency and from stablecoin, network and bridge risk (unchecked).
  Corrected 2026-10-15 (crypto market structure review follow-up): socialised loss is triggered at Deribit's absolute discretion when the fund is depleted in all currencies, or in the bankrupt account's currency when Deribit decides not to convert others (Rule 10.8); converting other currencies is itself discretionary (Rule 10.7).

All three: verification partly checked 2026-10-15, stability draft; human review outstanding. Checks: `funding_checks.py`.

Written in empirical extensions (2026-10-17) (source verification and bounded checks, not study or human review):

- `ev:crypto-dated-futures-carry`: dated-futures carry and its drivers, from BIS WP 1087 (archived copy). Partly checked 2026-10-17, draft; human review outstanding.
- `def:amm-pool-mechanics`: constant-product and concentrated-liquidity pools, with own checks (`amm-checks.py`). Partly checked 2026-10-17, draft; human review outstanding.

## Source verification after macro markets and pricing review

empirical extensions (2026-10-17) (six audit repairs and a source-review coverage; source verification and bounded tests, not study or human review): `ev:crypto-funding-crowding` narrowed (BIS WP 1087's dated-futures evidence and its restatements merged; a direct funding-rate study unread); `ev:crypto-dated-futures-carry` resolved (new entry `ev:crypto-dated-futures-carry` from BIS WP 1087 (archived copy)); `def:crypto-options-venue-structure` narrowed (a one-day Deribit API snapshot (inverse against USDC-settled listings, open-interest concentration) merged into `def:crypto-venue-instrument-structure`; other venues unread); `def:amm-pool-mechanics` narrowed (new entry `def:amm-pool-mechanics` from the Uniswap v2 and v3 papers; gas costs not covered); `ev:stablecoin-network-settlement-risk` narrowed (the Federal Reserve's FEDS Note on USDC and SVB merged into `def:crypto-trading-risk-layers`). The record is in `notes/source-review-records.md`, *empirical extensions (2026-10-17)*.

derivatives and empirical validation (2026-10-17) (seven audit repairs, backlog reconciliation and a source-review coverage; source verification and bounded tests, not study or human review): audit repairs: the BIS WP 1087 liquidation scale corrected from Table 7 (2.22 percentage points of open interest per standard deviation of carry, intercept 10.84 percent). The `ev:crypto-funding-crowding`, `ev:crypto-dated-futures-carry`, `def:crypto-options-venue-structure`, `def:amm-pool-mechanics`, `res:cfmm-reported-price`, `ev:uniswap-reference-tracking`, `meth:cfmm-convex-multi-asset-trade`, `mech:uniswap-v4-hooks`, `mech:auction-managed-amm` and `ev:stablecoin-network-settlement-risk` questions: perpetual-futures deviations (He et al.) into `mech:perpetual-funding`; Table 5 checked; an OKX snapshot beside Deribit; AMM fees, gas, reported prices, convex trades, Uniswap v4 and am-AMM into `def:amm-pool-mechanics`; CPMI-IOSCO finality into `def:crypto-trading-risk-layers`. New entries for DeFi lending, stablecoins and leverage are listed in their own pathway notes. The record is in `notes/source-review-records.md`, *derivatives and empirical validation (2026-10-17)*.

## Entries created by the completion batch (2026-10-20)

Distributed ledgers and digital-asset investing, in `digital-assets-prediction-markets/digital-asset-investing.tex`, checked by `notes/artefacts/digital-assets/digital-asset-checks.py`: `def:distributed-ledger-applications`, `meth:digital-asset-investment-analysis`. Sources: Nakamoto's white paper, the BIS Annual Economic Report 2018 chap. V, Narayanan et al. (draft of 9 February 2016), ethereum.org's proof-of-stake and Merge pages, Liu and Tsyvinski (NBER WP 24877) and the SEC's January 2024 spot bitcoin ETP order. Partly checked 2026-10-20, draft; human review outstanding. The record is in `notes/source-review-records.md`, *Completion batch, 20 October 2026*.

## Related entries owned elsewhere

Cross-referenced, not owned here: `def:best-execution`, `def:smart-order-routing` (`market-structure-execution-quality`); `def:fx-market-structure` (`fx-dealer-market-making`); `res:arbitrage-risks` (`execution-market-making`); `mech:futures-margin-settlement` (`futures-execution`); `def:securities-lending-fee-rebate` (`money-markets-repo-lending`). None of them is crypto evidence.

## Entry backlog

- ev:crypto-funding-crowding: whether funding measures positioning concentration (crowding) as distinct from leverage demand: He, Manela, Ross and von Wachter (arXiv v7, in `mech:perpetual-funding`) attribute the perpetual-spot gap to end users' leverage demand against limited arbitrage capital; `s11-r15` is unread and no position-level evidence has been read.
- def:crypto-options-venue-structure: venues beyond Deribit and OKX (both one-day API snapshots of 17 October 2026, in `def:crypto-venue-instrument-structure`) and whether the inverse-contract dominance and expiry concentration persist across days. Belongs to `crypto-options-numeraire`.
- def:amm-pool-mechanics: measured gas and execution costs for swaps and liquidity provision, and designs beyond Uniswap (Curve's stableswap); fee and gas theory (Milionis, Moallemi and Roughgarden), reported-price and convex-trade results (Angeris et al.), Uniswap v4 hooks and the am-AMM proposal are in the entry. Belongs to `amm-lending`.
- ev:stablecoin-network-settlement-risk: measured incidents of chain congestion, reorganisation and bridge or transfer delay; CPMI-IOSCO's settlement-finality and money-settlement guidance (July 2022) is in `def:crypto-trading-risk-layers` and redemption and depeg in `ev:stablecoin-runs`. Belongs to `stablecoin-pegs-runs` and the section overview.

## What changed in my view or practice

## Questions carried forward

- Read Deribit's Exchange Membership Terms, clause 12, for the full liquidation waterfall and the Liquidity Support Program.
- Read Gornall, Rinaldi and Xiao (`s11-r15`) and the BIS carry paper in full; neither was retrieved.
- Check other venues' funding cadence, interest term and clamps before generalising.
