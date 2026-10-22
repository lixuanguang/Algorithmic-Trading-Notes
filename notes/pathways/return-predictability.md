---
key: return-predictability
section: asset-pricing
status: not started (draft entries only, not from study)
---

# Return predictability and forecast evaluation

Pathway outcome, from the guide: judge an aggregate return predictor with present-value logic, out-of-sample tests for nested models and proper scoring. Its 11 required readings: `wide-campbell-shiller-1988`, `wide-cochrane-dog`, `s7-welch`, `wide-goyal-welch-zafirov`, `wide-campbell-thompson`, `wide-rapach-strauss-zhou`, `wide-clark-west`, `wide-giacomini-white`, `wide-gneiting-raftery`, `wide-martin-svix`, `w3-cakici-pockets-replication`. Prerequisite pathways: `time-series-volatility`, `empirical-asset-pricing`. This note is for a pathway of the section `asset-pricing`.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 22 October 2026 by the return-predictability content batch (`content_development_plan.md`; review record in `notes/source-review-records.md`, *Return-predictability content batch (22 October 2026)*). The three entries come from source checking, not study: of the required readings, `wide-cochrane-dog` (author-hosted copy of the published article) and `s7-welch` (journal copy) were read at the locators cited, and `wide-campbell-shiller-1988`, `wide-clark-west` and `wide-campbell-thompson` only in working-paper versions, registered as `campbell-shiller-1986-nber`, `clark-west-2006-nber` and `campbell-thompson-2005-nber`. The other six were not read then. The forecast-combination and proper-scoring batch (22 October 2026; `content_development_plan.md`, section 10; review record *Forecast-combination and proper-scoring batch (22 October 2026)*) added two entries, again from source checking, not study: `wide-gneiting-raftery` was read in the author-hosted copy of the journal article, and `wide-rapach-strauss-zhou` only in its February 2008 working-paper precursor, registered as `rapach-strauss-zhou-2008-wp`; the RFS version could not be obtained. `wide-giacomini-white`, `wide-goyal-welch-zafirov`, `wide-martin-svix` and `w3-cakici-pockets-replication` remain unread. The checkpoint was not attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted. The checkpoint asks for five predictors, a combination forecast and Clark-West tests. The first batch's numerical checks use one predictor (the dividend-price ratio); the second adds an annual equal-weight combination of four predictors (dp, ep, tms, dfy), fixed in advance, with descriptive Clark-West statistics. That is an editorial worked example, not the checkpoint.

## Entries created or changed

Written in the return-predictability content batch, 22 October 2026 (`asset-pricing/return-predictability.tex`, the pathway's only topic file):

- `res:campbell-shiller-identity`: the exact and log-linear return identities, the working paper's and Cochrane's choices of rho, the forward solution and the coefficient restriction b_r = 1 - rho phi + b_d, with an S&P 500 worked example.
- `meth:nested-forecast-tests`: recursive design, R2_OS and Delta RMSE, MSE-F and ENC, the nested-model MSPE bias and the Clark-West test; Monte Carlo size, Welch and Goyal's dividend-price row and start-date sensitivity.
- `meth:restricted-forecast-value`: Campbell and Thompson's sign restrictions, bounded mean-variance weights and the utility gain; their dividend-price row recomputed and a synthetic experiment.

Navigation only (no claim changed): links to `meth:nested-forecast-tests` from `def:contango-backwardation-stocks` and `meth:fx-valuation-signals` where the Clark-West statistic is named, and See also links from `meth:forecast-accuracy-evaluation` and `meth:backtest-evaluation-diagnostics`.

Written in the forecast-combination and proper-scoring batch, 22 October 2026 (same file):

- `meth:forecast-combination`: combination schemes of the 2008 working paper (mean, median, trimmed mean, discounted MSPE), the error-covariance and ambiguity identities and the diversification floor; an annual four-predictor example, 1947-2025 and 1947-2005.
- `meth:proper-scoring-rules`: propriety, the log score, CRPS and interval score with sign conventions and units; same-mean forecasts with different spreads, propriety by quadrature, Gneiting and Raftery's Table 2 by simulation, and a linear pool against an averaged point forecast.

Navigation only (no claim changed): See also links to `meth:forecast-combination` from `meth:nested-forecast-tests` and to `meth:proper-scoring-rules` from `meth:forecast-accuracy-evaluation`.

All five: stability draft; editorial review only, human review outstanding. Numerical evidence: `notes/artefacts/return-predictability/` (for each batch a protocol, extraction script, derived data, check script and recorded output; the second batch's files are prefixed `forecast-combination-scoring` and `goyal_extract_predictors`).

## Related entries owned elsewhere

Cross-referenced, not owned here: `meth:forecast-accuracy-evaluation` and `meth:autoregressive-forecasting` (`stationarity-cointegration`); `meth:backtest-evaluation-diagnostics`, which keeps Welch and Goyal's Table 1 magnitudes and Campbell and Thompson's R2/S2 rule (`backtest-inference`); `meth:gordon-growth-model` (`equity-events-fundamentals`); `def:risk-aversion-utility` and `meth:capital-allocation-line` (`portfolio-construction`); `meth:correlation-independence-tests` and `meth:hypothesis-testing` (`probability-statistical-inference`); for the second batch, `meth:alpha-signal-combination` (signal combination in equities), `meth:volatility-forecast-loss` (robust losses for variance forecasts) and `meth:var-es-estimation-methods` (VaR as a quantile forecast).

## Entry backlog

- Forecast combination: the RFS 2010 version of `wide-rapach-strauss-zhou` (403 from the publisher and SSRN on 22 October 2026) and the optional `wide-timmermann-combinations` were not obtained; locators of `meth:forecast-combination` are the 2008 working paper's. The real-economy links of the published version are not covered.
- The updated predictor set and sample (`wide-goyal-welch-zafirov`): the 2026 data file was used, the paper was not read.
- Conditional predictive ability with rolling windows (`wide-giacomini-white`): not started. Proper scoring is now written (`meth:proper-scoring-rules`), but tests of equal average scores and conditional tests are not, so `objective:score-and-combine-return-forecasts` stays partial.
- Density combination beyond the linear-pool example, calibration (PIT) diagnostics, and scoring of real return density forecasts: not started.
- Option-implied premium bound (`wide-martin-svix`) and the real-time kernel check (`w3-cakici-pockets-replication`): not started.
- Predictive-regression bias and long-horizon inference (`rf-stambaugh-1999`, `rf-hodrick-1992`): deferred to `standard-errors-inference`.
- Checkpoint replication with five predictors, a combination forecast and evaluation-start sensitivity.
- The Clark-West sizes recomputed here (0.069 and 0.059) are below the published 0.085 and 0.070 by 3.0 and 2.3 standard errors, counting both simulations. A rerun in the source's design confines the gap to P = 120 (about three standard errors); its cause is unresolved.

## What changed in my view or practice

## Questions carried forward
