---
key: execution-trading-costs
section: execution-trading-costs
status: not started (draft entries only, not from study)
---

# Execution, trading costs and market structure (section overview)

Overview outcome, from the guide: plan the execution of an equity order, a futures roll and a bond trade, estimate expected cost and its uncertainty from a stated impact model, and split realised implementation shortfall into spread, impact, timing and fees under the rules in force. The overview's readings are `wide-perold-shortfall`, `alpha-almgren`, `catalogue-0504`, `ex-goyal-jegadeesh-wu-2026`, `wide-bsv-fi-survey` and `exp-fx-algos`.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 15 October 2026 by optimal execution review (`notes/source-review-index.md`) and extended by execution benchmarks / transaction-cost analysis reviews: the overview's outcome asks for a schedule and an expected cost with its uncertainty from a stated impact model, and `alpha-almgren` is one of its readings. execution benchmarks review added the execution-benchmark entries: the overview's outcome and checkpoint ask for realised implementation shortfall against arrival price, and its first reading is Perold's paper. execution algorithms review added the execution-algorithms entries: how an algorithm pursues its benchmark, how a large order is exposed and routed, and how portfolios are traded, which is the outcome's planning of a venue, mechanism and schedule. transaction-cost analysis review added the transaction-cost entries: measuring and splitting realised shortfall is the outcome's last clause; best execution and broker conflicts are owned by `market-structure-execution-quality`, and manager performance by `performance-manager-evaluation`. The entries come from source checking against Lehalle and Laruelle (`alpha-laruelle`, on no route), the Almgren–Chriss author preprint of December 2000 (`alpha-almgren`, selected passages), Harris (`alpha-harris`) and Kissell (`s7-kissellscience`, on no route). Perold's paper (`wide-perold-shortfall`) was not available and has not been read. That is not study of the readings.

Moved in by the content migration of 22 October 2026, with labels and content unchanged: from `ml-alternative-data`: `mod:cartea-jaimungal-execution`.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in optimal execution / source review / optimal execution / high-frequency strategies reviews:

- `mod:almgren-chriss-execution`: mean–variance optimal execution; the Almgren–Chriss closed form and Lehalle and Laruelle's discrete version with power-law temporary impact; expectation-only, variance-only and mean–variance schedules.
- `def:block-trade`: block trades and the four problems of arranging them (Harris).

Written in execution benchmarks / source review / optimal execution / high-frequency strategies reviews:

- `def:execution-benchmark`: benchmark prices (decision, arrival, VWAP, participation-weighted, open and close) with their timing, weighting and biases, and algorithm targets (VWAP, TWAP, POV, arrival price, implementation shortfall, liquidity seeker).
- `def:implementation-shortfall`: paper minus real portfolio; Perold's execution and opportunity components and Wagner's delay, trading and opportunity components, as given by Kissell, with Harris's estimator and the Plexus breakdown.
- `meth:algorithm-benchmark-choice`: Lehalle and Laruelle's choice of an algorithm's benchmark by region, order size, market context and hedged risk (their Table 3.1).

Written in execution algorithms / source review / optimal execution / high-frequency strategies reviews:

- `def:trading-envelope`: a trading algorithm's execution parameters, risk-control layer (trading curve and envelope) and tactics; how VWAP, TWAP, POV and implementation-shortfall algorithms pursue their benchmarks; combining benchmarks through constraints or envelopes (Lehalle and Laruelle, Kissell).
- `meth:execution-decision-support`: pre-trade analytics, monitoring and performance indicators, what-if scenarios (Lehalle and Laruelle).
- `def:order-exposure-decisions`: display, splitting, broker and market decisions; reactive against proactive traders; evasive strategies (Harris).
- `def:portfolio-trading`: program trades, the firm bid/offer market, basket algorithms and index-fund trading tactics (Harris, Kissell).
- `mech:positive-feedback-hedging`: portfolio insurance as positive-feedback hedging and its 1987 sizing (Harris), with an own feedback calculation.
- `meth:algorithm-benchmark-choice` extended with Lehalle and Laruelle's Table 3.2.

Written in transaction-cost analysis / source review / optimal execution / high-frequency strategies reviews:

- `def:transaction-costs`: explicit, implicit and missed-trade costs (Harris); Kissell's ten components; an accounting split of shortfall into delay, half-spread paid, midpoint drift, opportunity and fees (own, reconciled), not a causal impact measure.
- `meth:transaction-cost-analysis`: measuring, predicting and comparing costs; Kissell's index-adjusted cost and z-score (with a side correction); selection limits of routing tables.
- `meth:aggressiveness-tradeoff`: Harris's marginal rule balancing transaction and missed-trade costs.
- Merged into existing entries: the signed benchmark cost, benchmark list, VWAP, estimator quality and gaming (`def:execution-benchmark`); the missed-quantity formula (`def:implementation-shortfall`); pre-, live- and post-trade tools and the average-price attribution, with the (A.26) correction (`meth:execution-decision-support`); the motive audit and block reporting (`def:block-trade`).

All thirteen: verification partly checked 2026-10-15, stability draft; human review outstanding. The impact concepts they use (price impact and its empirical estimation) are owned by `price-impact-execution` and are cross-referenced from the entries, not listed here; so is the 1987-crash mechanism owned by `execution-market-making`.

Written in trading infrastructure / source review / optimal execution / high-frequency strategies reviews:

- `def:automated-trading-architecture`: Lehalle and Laruelle's architecture (Figure 3.1) and the inputs of trading tools: market data with fast analytics, two-way venue connections, historical data with recorded messages and context, and models with an accuracy check.
- Merged: indicator publication into `meth:execution-decision-support` (pp. 200–202; the book calls trading algorithms "stateless agents").

Both partly checked 2026-10-15, draft. The operational controls and the floor-against-automated comparison are owned by `model-governance-controls` and `execution-market-making` and are not listed here.

Changed in equity market structure / source review / optimal execution / high-frequency strategies reviews:

- Merged: Harris's 2002 block-print and size-precedence rule into `def:block-trade` (sec. 15.6.1), with reporting, execution priority and trade-through protection kept apart; Harris's three reasons for cheap index trading into `def:portfolio-trading` (sec. 23.4).

Both partly checked 2026-10-15, draft.

Changed in the equity market structure review follow-up, 2026-10-15: `def:portfolio-trading` now gives index arbitrage as about 9 percent of reported program-trade volume (about 2.4 percent of NYSE volume), and `def:block-trade` limits the 2002 print requirement to brokers and dealers who were exchange members.

Changed in transaction-cost models / source review / optimal execution / high-frequency strategies reviews:

- Merged: Narang's three cost components into `def:transaction-costs` (`s7-narang`, third edition, chap. 5, pp. 85-91). His slippage (decision to arrival) is mapped to the delay term, and his market impact (arrival to fill) to the trading-related part of shortfall, not to causal impact. His claim that impact is known once the trade is complete is corrected: the unaffected price is never observed. His trend-following, mean-reversion, latency and volatility claims are kept as conditional statements about the drift over the delay. His clearing and settlement descriptions are reported as his, beside the CPSS-IOSCO principles' DvP and central-counterparty paragraphs (`exp-pfmi`, paras 1.12-1.13); no clearing definition is adopted.

Partly checked 2026-10-15, draft; human review outstanding.

Changed in the transaction-cost models review follow-up, 2026-10-15: `def:transaction-costs` no longer says that Narang's selling order "did not raise the price"; his example shows a negative arrival-to-fill cost against a benchmark, which does not identify the order's own effect. The cost-function entry is owned by `portfolio-construction`.

Changed in systematic-investing architecture / source review / optimal execution / high-frequency strategies reviews:

- `def:order-exposure-decisions`: Narang's execution-algorithm choices (aggressive against passive, side-dependent; rebates and inverted fees; signal strength and strategy type; the inside-spread middle ground; micro price; hidden orders and icebergs; order sizing; footprints), chap. 7, pp. 127-137; cancel-and-replace without intent to execute kept as an unresolved pitfall, with the U.S. futures spoofing clause (7 U.S.C. 6c(a)(5)(C)).
- `def:portfolio-trading`: Narang's portfolio bid (p. 128).
- `def:automated-trading-architecture`: Narang's DMA, colocation, FIX and hardware (pp. 138-141); sponsored access referred to Rule 15c3-5.

Partly checked 2026-10-15, draft.

Changed in the systematic-investing architecture review follow-up, 2026-10-15: `def:order-exposure-decisions` no longer says hidden orders "reveal nothing"; they remove the pre-trade display, while executions and pinging (SEC 2010 release, p. 47, n. 69) still leak information. Its Currency field and that of `def:automated-trading-architecture` now date the 2024 U.S. Code passage and Narang's 2024 account.

Changed in order matching and fragmentation / source review / optimal execution / execution control reviews: `def:order-exposure-decisions` (benefits and costs of exposure, parasitic and defensive traders, display instructions and display precedence; Harris pp. 84-85, 117, 382-384) and `def:block-trade` (sunshine trading, pp. 327-328). Partly checked 2026-10-16, draft.

Changed in market design and liquidity / source review / optimal execution / execution control reviews: `def:block-trade` (Harris's block dealers against block brokers in the upstairs market, pp. 328--330) and `def:order-exposure-decisions` (how markets protect exposure: time precedence with a meaningful tick, undisclosed orders, audit trails, delayed reporting, p. 389). Partly checked 2026-10-16, draft; human review outstanding.

Written in the derivatives, portfolio and execution batch (2026-10-19):

In `trade-strategy-governance.tex` (topic `trade-execution`):

- `meth:execution-cost-measures`: effective spread, VWAP cost and implementation shortfall with MIP chap. 10's examples.
- `def:electronic-trading-environment`: drivers, fragmentation, trader types, systems, latency, risks, mitigations and abuses.
- `meth:trade-strategy-selection`: motives, inputs, benchmarks, strategies for three orders and algorithm classes.
- `def:trade-implementation-by-market`: implementation in equities, fixed income, listed and OTC derivatives and spot FX.
- `meth:trade-execution-evaluation-governance`: cost measurement, statistical evaluation and procedures under FINRA Rule 5310 and MiFID II article 27.

All partly checked 2026-10-19, draft. Examples in `notes/artefacts/trade-execution/trade-execution-checks.py`; human review is outstanding. Coverage records are editorial, not study. `def:transaction-costs`, `def:implementation-shortfall`, `def:spread-measures`, `def:execution-benchmark` and `mech:venue-competition-fragmentation` are linked, not repeated.

## Source verification after macro markets and pricing review

source verification (2026-10-17) (source verification and bounded tests, not study or human review): `def:clearing-settlement` resolved by merge into `def:transaction-costs` (its clearing-and-settlement item): the CPSS-IOSCO principles' Annex H definitions of clearing, final settlement, delivery versus payment, principal risk, central counterparty, novation and open offer (pp. 174-178, BIS PDF). The CPMI's online glossary page renders its terms by script and was not compared; the CPSS glossary of 2003 was not read. The record is in `notes/source-review-records.md`, *source verification (2026-10-17)*.

## Specialist pathways

The guide's pathways for this section, in its order, with the existing material or the content gap as recorded by the content migration of 22 October 2026. A pathway with related material but no note has not been opened.

- `price-impact-execution` (Price impact, optimal execution and TCA): pathway note [price-impact-execution.md](price-impact-execution.md), 10 entries listed, in `execution-trading-costs/impact-models`, `execution-trading-costs/trade-signing`.
- `market-structure-execution-quality` (Market structure rules, fees and execution quality): pathway note [market-structure-execution-quality.md](market-structure-execution-quality.md), 19 entries listed, in `execution-trading-costs/dark-trading-fragmentation`, `execution-trading-costs/execution-quality`, `execution-trading-costs/market-regulation`, `execution-trading-costs/smart-order-routing`, `execution-trading-costs/tick-size`.
- `otc-fixed-income-trading` (Fixed-income and OTC electronic trading): pathway note [otc-fixed-income-trading.md](otc-fixed-income-trading.md), 3 entries listed, in `execution-trading-costs/fixed-income-trading`.
- `etf-index-closing-execution` (ETFs, index events and closing auctions): pathway note [etf-index-closing-execution.md](etf-index-closing-execution.md), 3 entries listed, in `execution-trading-costs/etf-mechanics`.
- `futures-execution` (Futures execution: matching, rolls and settlement): pathway note [futures-execution.md](futures-execution.md), 5 entries listed, in `execution-trading-costs/futures-execution`.
- `retail-cfd-brokers` (Retail CFDs: leverage limits, broker risk and client outcomes): content gap; no entry written.

## Entry backlog

Empty after the source verification (2026-10-17); new stubs go here.

## What changed in my view or practice

## Questions carried forward

- Lehalle and Laruelle's appendix mixes two timing conventions (price step (A.16) against the terminal conditions (A.27)); the entry uses the Almgren–Chriss convention. Is the book's Figure A.11 computed under either?
- The journal version of Almgren and Chriss (2001) has not been compared with the December 2000 preprint.
- The checkpoint's split into spread, impact, timing and fees: transaction-cost analysis review gives an accounting split (delay, half-spread paid, midpoint drift, opportunity, fees) that reconciles exactly, but none of the sources checked turns the midpoint drift into causal impact; a market-adjusted residual is impact only under the model that removes the rest. Which source or design would identify impact here, and how do the tick, fee and reporting rules in force change the split?
- What denominator should a participation rate use: market volume with or without the order's own fills, and with or without auctions? Neither Kissell nor Lehalle and Laruelle says (execution algorithms review).
- Perold (1988) has not been read; the formula called Perold's, and the expanded form called Wagner's, are attributed by Kissell. Does Perold's paper define the opportunity cost at the end of trading or at a later horizon, and does it include fees?
- How should realised shortfall be split into spread, impact, timing and fees, as the checkpoint asks? None of the sources checked splits the trading-related part into spread and impact.
