---
key: systematic-equities
section: systematic-equities
status: not started (draft entries only, not from study)
---

# Systematic equities: equity securities and valuation (section overview)

A compendium section declared in `compendium/compendium.tex`. This note lists the equity-securities and valuation entries that precede the signal and portfolio sections; the guide's specialist pathways for the section (`equity-long-short-construction` and others) have their own notes. The guide pathway `equity-events-fundamentals` assumes the valuation entries listed here. Topics and objectives are in `notes/coverage/objectives.json` (topics `equity-securities-markets`, `equity-valuation-foundations`, `industry-company-analysis`, `dividend-discount-models`, `market-multiples-valuation`, `equity-research-reporting`, `free-cash-flow-valuation`, `residual-income-valuation`, `private-company-valuation`).

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Written on 20 October 2026 by the corporate-finance and equity-valuation batch: 24 entries in five sections, from Damodaran's *Investment Valuation* (2012) and *Applied Corporate Finance* (2014), IFRS 13 and IAS 1 as adopted in the EU, Porter (2008), the GICS methodology (2023), the US Merger Guidelines (2023), the CIPD PESTLE factsheet, Cooper and Lambertides (2023), Lang and Stulz (1993), FTSE Russell free-float rules (2026), FINRA Rule 11140, Delaware law and the EU Shareholder Rights Directive. That is source checking, not study.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted. No checkpoint has been set for these entries.

## Entries created or changed

Corporate-finance and equity-valuation batch (2026-10-20); numbers checked by `trading_notes.numerical.systematic_equities.equity_valuation_checks`, which reuses the Harbour valuation:

- Equity securities and markets: `def:equity-instruments`, `def:equity-rights-voting`, `def:equity-issuance-trading-liquidity`, `def:corporate-distribution-mechanics`.
- Valuation foundations: `def:price-value-indicators`, `def:valuation-model-families`, `meth:present-value-model-inputs`, `def:intrinsic-value-mispricing`, `meth:valuation-approach-choice`, `meth:valuation-price-judgement`.
- Industry and company analysis: `meth:industry-analysis`, `meth:company-position-analysis`.
- Dividend discount models: `meth:gordon-growth-model`, `meth:preferred-stock-valuation`, `meth:pvgo-justified-pe`, `meth:multistage-ddm`, `meth:sustainable-growth`.
- Multiples: `meth:multiples-valuation-basics`, `meth:peer-group-selection`, `meth:justified-multiples`, `meth:normalised-earnings`, `meth:alternative-multiples`, `meth:enterprise-value-multiples`, `meth:comparables-evaluation`.

Partly checked 2026-10-20, draft; human review outstanding. See [record](../source-review-records.md#corporate-finance-and-equity-valuation-batch-20-october-2026).

Credit, time-series and valuation batch (2026-10-20); numbers checked by `trading_notes.numerical.systematic_equities.equity_fcf_ri_private_checks`, which rebuilds the Harbour value from its forecast:

- Equity research and forecast models: `meth:forecast-model-valuation`, `def:research-report-evaluation`.
- Free cash flow valuation: `meth:fcff-fcfe-derivation`, `meth:fcf-forecasting`, `meth:fcf-valuation-models`, `meth:cash-flow-proxies`.
- Residual income: `def:residual-income-eva`, `meth:residual-income-valuation`, `meth:residual-income-comparison`.
- Private companies: `meth:private-earnings-normalisation`, `meth:private-discount-rate`, `meth:private-company-valuation`.

Partly checked 2026-10-20, draft; human review outstanding. See [record](../source-review-records.md#credit-time-series-and-valuation-batch-20-october-2026).

## Specialist pathways

The guide's pathways for this section, in its order, with the existing material, partial treatment or content gap as recorded by the content migration of 22 October 2026 and its closeout review. A pathway with related material but no note has not been opened. A partial treatment names the existing entries that treat some of the pathway's subtopics, wherever they sit, and the subtopics with nothing written.

Printed as numbered sections of the chapter, under the guide pinned at `8302467` (`subsection_alignment_plan.md`): `equity-events-fundamentals`, `equity-long-short-construction`, `equity-event-driven`. A pathway without entries of its own is not printed; the related material and partial treatments named below are printed under the pathway or section that owns them.

- `equity-factor-premia` (Equity factor premia, crashes and timing): no pathway note; partial treatment in existing entries, not reviewed as complete: value, momentum, quality and carry premia across markets (`def:alpha-model-taxonomy` in `research-engineering-validation/quant-strategy-structure`); size, value, momentum and reversal anomalies with behavioural explanations (`mech:biases-market-anomalies` in `portfolio-construction-risk/behavioural-finance`); factor timing by volatility scaling (`ev:volatility-managed-portfolios` in `portfolio-construction-risk/portfolio-construction-models`); factor (smart-beta) indexes (`def:cap-weighted-factor-indexing` in `systematic-equities/equity-portfolio-management`). Not written: factor crashes; valuation- and momentum-based factor timing; post-publication decay.
- `statistical-arbitrage` (Statistical arbitrage and short-horizon equity strategies): no pathway note; partial treatment in existing entries, not reviewed as complete: residual mean reversion (Avellaneda–Lee), distance pairs (Gatev et al.) and the Lo–MacKinlay contrarian decomposition (`def:alpha-model-taxonomy` in `research-engineering-validation/quant-strategy-structure`); pairs trading as an active equity strategy (`def:active-equity-strategies` in `systematic-equities/equity-portfolio-management`); cointegration of a pairs spread (`meth:cointegration-testing` in `regression-time-series/time-series-models`); the August 2007 quant unwind (`def:common-investor-contagion` in `portfolio-risk-financing/crowding-contagion`). Not written: short-horizon reversal evidence net of costs; capacity and implementation at scale.
- `demand-flows-passive` (Demand-based asset pricing, flows and passive investing): no pathway note; partial treatment in existing entries, not reviewed as complete: price pressure from index-fund trading at reconstitution (`ev:index-reconstitution-impact` in `execution-trading-costs/etf-mechanics`); index funds' timing of index changes (`meth:index-equity-portfolio-construction` in `systematic-equities/equity-portfolio-management`). Not written: demand-system asset pricing and inelastic markets; fund-flow effects; effects of rising passive ownership.
- `equity-events-fundamentals` (Fundamental valuation and accounting signals): no pathway note; related existing material in `systematic-equities/industry-company-analysis`, `systematic-equities/equity-research-reporting`, `systematic-equities/equity-valuation-foundations`, `systematic-equities/dividend-discount-models`, `systematic-equities/market-multiples`, `systematic-equities/free-cash-flow-valuation`, `systematic-equities/residual-income-valuation`, `systematic-equities/private-company-valuation`, not reviewed as a complete treatment of the pathway.
- `equity-trader-signals` (Short-selling, option, insider and retail-flow signals): no pathway note; partial treatment in existing entries, not reviewed as complete: insider-trade signals, opportunistic against routine insiders (`def:financial-data-types` in `ml-alternative-data/financial-data-types`); filing deadlines for insider and holdings data (`data:holdings-insider-filing-lags` in `research-engineering-validation/point-in-time-data`). Not written: short-interest and lending-fee signals; option-implied signals; retail-flow signals.
- `equity-long-short-construction` (Equity portfolio construction: mandates, indexing, signal combination and long–short portfolios): pathway note [equity-long-short-construction.md](equity-long-short-construction.md), 9 entries listed, in `systematic-equities/equity-portfolio-management`, `systematic-equities/signal-combination`. Broadened by the guide revision of 22 October 2026 (`8302467`) to cover equity mandates and indexing; its entries are in `systematic-equities/signal-combination`, `systematic-equities/equity-portfolio-management`.
- `equity-event-driven` (Equity securities, corporate actions, earnings events and merger arbitrage): no pathway note; partial treatment in existing entries, not reviewed as complete: merger arbitrage among event-driven strategies (`meth:hedge-fund-strategy-classification` in `portfolio-construction-risk/hedge-fund-strategies`); activist returns around Schedule 13D filings (`def:active-equity-strategies` in `systematic-equities/equity-portfolio-management`, `def:equity-portfolio-roles-mandate` in `systematic-equities/equity-portfolio-management`); post-earnings drift and accrual returns around announcements (`mech:biases-market-anomalies` in `portfolio-construction-risk/behavioural-finance`, `meth:earnings-quality-persistence` in `financial-statement-analysis/financial-reporting-quality`). Not written: earnings-announcement return measurement; merger-arbitrage returns and deal-failure risk. Broadened by the guide revision of 22 October 2026 (`8302467`) to cover equity securities and corporate actions; its entries are in `systematic-equities/equity-securities-markets`.

## Entry backlog

## What changed in my view or practice

## Questions carried forward

- The peer table for Harbour is hypothetical; would a real peer set of listed tool makers change the conclusion that comparables controlled for growth point to overvaluation?
- Fair market value is described without the US tax authority's definition (Rev. Rul. 59-60 and the estate-tax regulations), which was not consulted.
- Ohlson (1995) was not read; the persistence factor in the residual-income entry is stated as a derivation. Would Ohlson's linear information dynamics change the Harbour continuing value?
- Cooper and Lambertides select peers on expected growth with US data; does the ten-firm result hold for European mid-caps?
