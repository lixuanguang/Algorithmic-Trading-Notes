---
key: asset-pricing
section: asset-pricing
status: not started (draft entries only, not from study)
---

# Asset pricing theory and empirical tests (section overview)

A compendium section in Part II, *Empirical finance, machine learning and research governance*, declared in `compendium/compendium.tex`. Overview outcome, from the guide: For a published return anomaly, record the claim, sample, data vintage and test, reproduce a headline estimate, and say which risk-based or mispricing explanations the evidence cannot separate.

Its checkpoint, from the guide: Take one published return anomaly. Record the claim, sample, data vintage and test; reproduce a headline estimate from public data; then state which risk-based or mispricing explanations the evidence cannot rule out and what further test would separate them. Keep apart the question whether the variable predicts returns and the question whether a pricing model explains them.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Entry histories and source-review references are in [portfolio-construction-risk.md](portfolio-construction-risk.md).

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries

By pathway, in compiled order: each printed pathway is a numbered section of the chapter, and a pathway with several topic files prints each as a subsection.

- `asset-pricing-theory` (Asset-pricing theory: stochastic discount factors, CAPM and factor pricing; `asset-pricing-models.tex`): `mech:systematic-risk-pricing`, `mod:return-generating-models`, `mod:capm-sml`, `meth:required-return-on-equity`, `mod:multifactor-apt`.
- `empirical-asset-pricing` (Empirical asset pricing: factor models and tests; `factor-model-tests.tex`): `meth:capm-regression`, `def:factor-model-types`.
- `return-predictability` (Return predictability and forecast evaluation; `return-predictability.tex`): `res:campbell-shiller-identity`, `meth:nested-forecast-tests`, `meth:restricted-forecast-value`, `meth:forecast-combination`, `meth:proper-scoring-rules`, `meth:conditional-predictive-ability`.

## Specialist pathways

The guide's pathways for this section, in its order, with the existing material, partial treatment or content gap. A pathway with related material but no note has not been opened. A partial treatment names the existing entries that treat some of the pathway's subtopics, wherever they sit, and the subtopics with nothing written.

Printed as numbered sections of the chapter, under the guide pinned at `8302467`: `asset-pricing-theory`, `empirical-asset-pricing`, and, from the return-predictability content batch of 22 October 2026, `return-predictability`. A pathway without entries of its own is not printed; the related material and partial treatments named below are printed under the pathway or section that owns them.

- `asset-pricing-theory` (Asset-pricing theory: stochastic discount factors, CAPM and factor pricing): no pathway note; related existing material in `asset-pricing/asset-pricing-models`, not reviewed as a complete treatment of the pathway.
- `standard-errors-inference` (Standard errors, clustering and weak instruments): no pathway note; partial treatment in existing entries, not reviewed as complete: heteroskedasticity-robust and Newey–West standard errors (`meth:regression-misspecification` in `regression-time-series/multiple-regression`); Sharpe-ratio standard errors under serial correlation (`meth:sharpe-ratio-standard-error` in `research-engineering-validation/backtest-evaluation`); tests with overlapping observations (`meth:correlation-independence-tests` in `probability-statistics/statistical-inference`). Not written: clustered and panel standard errors; weak instruments and IV inference.
- `empirical-asset-pricing` (Empirical asset pricing: factor models and tests): no pathway note; related existing material in `asset-pricing/factor-model-tests`, not reviewed as a complete treatment of the pathway.
- `return-predictability` (Return predictability and forecast evaluation): pathway note [return-predictability.md](return-predictability.md), opened 22 October 2026 with three entries in `asset-pricing/return-predictability` (the present-value identity, nested forecast tests, restricted forecasts and their economic value), and extended the same day with two more (forecast combination; proper scoring of predictive distributions and intervals) and then a sixth (conditional predictive ability of forecasting methods). Related material elsewhere, cross-referenced: `meth:forecast-accuracy-evaluation` (`regression-time-series/time-series-models`); `meth:backtest-evaluation-diagnostics` (`research-engineering-validation/backtest-evaluation`); applications of the Clark–West test in `def:contango-backwardation-stocks` (`energy-commodities/commodity-curves`) and `meth:fx-valuation-signals` (`currency-markets/macro-fx`). Not written: predictive-regression bias and long-horizon inference (deferred to `standard-errors-inference`); option-implied premium bounds.
- `event-studies` (Event studies and long-run abnormal returns): no pathway note; partial treatment in existing entries, not reviewed as complete: an announcement-window event study and the limits of its window choice (`def:central-bank-policy-framework` in `rates-credit-mortgages/monetary-policy-curves`); the market model separating market-related from residual returns (`mod:return-generating-models` in `asset-pricing/asset-pricing-models`). Not written: estimation- and event-window design; abnormal-return test statistics; long-run abnormal returns.

## Entry backlog

## What changed in my view or practice

## Questions carried forward
