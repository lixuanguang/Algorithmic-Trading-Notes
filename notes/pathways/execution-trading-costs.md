---
key: execution-trading-costs
section: execution-trading-costs
status: not started (draft entries from the migration only)
---

# Execution, trading costs and market structure (section overview)

Overview outcome, from the guide: plan the execution of an equity order, a futures roll and a bond trade, estimate expected cost and its uncertainty from a stated impact model, and split realised implementation shortfall into spread, impact, timing and fees under the rules in force. The overview's readings are `wide-perold-shortfall`, `alpha-almgren`, `catalogue-0504`, `ex-goyal-jegadeesh-wu-2026`, `wide-bsv-fi-survey` and `exp-fx-algos`.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 15 October 2026 by migration slice 10 (`notes/migration.md`) and extended by slices 11 and 12, because the guide runs one study loop per section overview and the optimal-execution blocks of the legacy notes belong to this overview rather than to a specialist pathway: its outcome asks for a schedule and an expected cost with its uncertainty from a stated impact model, and `alpha-almgren` is one of its readings. Slice 11 added the execution-benchmark blocks: the overview's outcome and checkpoint ask for realised implementation shortfall against arrival price, and its first reading is Perold's paper. Slice 12 added the execution-algorithms blocks: how an algorithm pursues its benchmark, how a large order is exposed and routed, and how portfolios are traded, which is the outcome's planning of a venue, mechanism and schedule. The entries come from migration and source checking against Lehalle and Laruelle (`alpha-laruelle`, on no route), the Almgren–Chriss author preprint of December 2000 (`alpha-almgren`, selected passages), Harris (`alpha-harris`) and Kissell (`s7-kissellscience`, on no route). Perold's paper (`wide-perold-shortfall`) was not available and has not been read. That is not study of the readings.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in migration slice 10, 2026-10-15:

- `mod:almgren-chriss-execution`: mean–variance optimal execution; the Almgren–Chriss closed form and Lehalle and Laruelle's discrete version with power-law temporary impact; expectation-only, variance-only and mean–variance schedules.
- `def:block-trade`: block trades and the four problems of arranging them (Harris).

Written in migration slice 11, 2026-10-15:

- `def:execution-benchmark`: benchmark prices (decision, arrival, VWAP, participation-weighted, open and close) with their timing, weighting and biases, and algorithm targets (VWAP, TWAP, POV, arrival price, implementation shortfall, liquidity seeker).
- `def:implementation-shortfall`: paper minus real portfolio; Perold's execution and opportunity components and Wagner's delay, trading and opportunity components, as given by Kissell, with Harris's estimator and the Plexus breakdown.
- `meth:algorithm-benchmark-choice`: Lehalle and Laruelle's choice of an algorithm's benchmark by region, order size, market context and hedged risk (their Table 3.1).

Written in migration slice 12, 2026-10-15:

- `def:trading-envelope`: a trading algorithm's execution parameters, risk-control layer (trading curve and envelope) and tactics; how VWAP, TWAP, POV and implementation-shortfall algorithms pursue their benchmarks; combining benchmarks through constraints or envelopes (Lehalle and Laruelle, Kissell).
- `meth:execution-decision-support`: pre-trade analytics, monitoring and performance indicators, what-if scenarios (Lehalle and Laruelle).
- `def:order-exposure-decisions`: display, splitting, broker and market decisions; reactive against proactive traders; evasive strategies (Harris).
- `def:portfolio-trading`: program trades, the firm bid/offer market, basket algorithms and index-fund trading tactics (Harris, Kissell).
- `mech:positive-feedback-hedging`: portfolio insurance as positive-feedback hedging and its 1987 sizing (Harris), with an own feedback calculation.
- `meth:algorithm-benchmark-choice` extended with Lehalle and Laruelle's Table 3.2.

All ten: verification partly checked 2026-10-15, stability draft; human review outstanding. Their derivations artefact is `notes/artefacts/market-making-lob/derivations.tex`. The impact concepts they use (price impact and its empirical estimation) are owned by `price-impact-execution` and are cross-referenced from the entries, not listed here; so is the 1987-crash mechanism owned by `execution-market-making`.

## Entry backlog

## Legacy candidate material

Run `python3 tools/migration_status.py` for the current counts. The rest of `compendium/legacy/execution-trading-costs/01_execution_and_algorithmic_trading/` is shared between this overview and its specialist pathways; decide each block's owner when its file is migrated.

## What changed in my view or practice

## Questions carried forward

- Lehalle and Laruelle's appendix mixes two timing conventions (price step (A.16) against the terminal conditions (A.27)); the entry uses the Almgren–Chriss convention. Is the book's Figure A.11 computed under either?
- The journal version of Almgren and Chriss (2001) has not been compared with the December 2000 preprint.
- What denominator should a participation rate use: market volume with or without the order's own fills, and with or without auctions? Neither Kissell nor Lehalle and Laruelle says (slice 12).
- Perold (1988) has not been read; the formula called Perold's, and the expanded form called Wagner's, are attributed by Kissell. Does Perold's paper define the opportunity cost at the end of trading or at a later horizon, and does it include fees?
- How should realised shortfall be split into spread, impact, timing and fees, as the checkpoint asks? None of the sources checked splits the trading-related part into spread and impact.
