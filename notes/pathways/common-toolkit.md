---
key: common-toolkit
section: retired guide overview (compatibility bridge)
status: retired; history kept below
---

# Common toolkit (retired guide overview: bridge to Part I)

The guide retired this overview in its eight-Part edition (`guide/learning_routes.json`, `retired_overviews`). It is no longer a compendium section. Its nine former topic files are now in the seven sections of Part I, *Financial mathematics, statistics and numerical methods*:

| Successor section | Former files and entries |
| --- | --- |
| `financial-mathematics` ([overview](financial-mathematics.md)) | `time-value.tex`; with `def:return-measures` from portfolio performance |
| `probability-statistics` ([overview](probability-statistics.md)) | `descriptive-statistics.tex`, `statistical-inference.tex`; `probability.tex` without Bayesian updating; `simulation-methods.tex` as `resampling.tex` without Monte Carlo |
| `regression-time-series` ([overview](regression-time-series.md)) | `regression.tex`, `multiple-regression.tex`, `time-series-models.tex` |
| `stochastic-processes-calculus` ([overview](stochastic-processes-calculus.md)) | `stochastic-calculus.tex` |
| `bayesian-inference` ([overview](bayesian-inference.md)) | `meth:bayesian-updating`, from `probability.tex` |
| `high-dimensional-statistics` ([overview](high-dimensional-statistics.md)) | none from this chapter; its covariance entries came from portfolio risk |
| `numerical-optimisation` ([overview](numerical-optimisation.md)) | `meth:monte-carlo-simulation`, from `simulation-methods.tex` |

The guide moved this overview's research-record checkpoint to `research-engineering-validation` ([overview](research-engineering-validation.md)). The history below records the work done while the chapter existed; its file paths are historical.

## Former overview

Overview outcome, from the guide: write a reproducible research record for a simple signal: decision-time data, an economic mechanism, the uncertainty of the headline estimate, a portfolio decision and the evidence that would reject it. Its checkpoint is a one-page research record for a public-data signal, rebuilt from the recorded inputs. Its readings are `prob-wasserman`, `s15-campbell`, `s6-cochrane`, `alpha-boyd`, `s7-meucci`, `s6-pbo` and `s8-bitemporal`.

The chapter also held the time-value foundations that the subject objectives in `notes/coverage/objectives.json` place under `topic:time-value-of-money` and part of `topic:return-measurement`. Those entries come from the foundation slice of 18 October 2026, not from this overview's readings.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 18 October 2026 by the first foundation slice (`notes/source-review-records.md`, *Return measurement and present value: first foundation slice*). The entries come from source checking against an open finance textbook, Hull and a Federal Reserve note, none of them this overview's readings. That is not study, and the checkpoint was not attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in the first foundation slice (2026-10-18):

- `def:required-return-components`: the Fisher relation, exact and approximate; nominal yield as real yield plus expected inflation plus an inflation risk premium, and the inflation-indexed liquidity premium, from the Federal Reserve staff decomposition; credit and other premia as a decomposition by convention.
- `meth:instrument-present-value`: present values of zero-coupon and coupon bonds (single yield and zero rates), preferred stock, constant and two-stage dividend growth; implied yield, required return and growth.
- `res:cash-flow-additivity`: the law of one price and additivity of dated cash flows; implied forward rates, covered interest parity and a one-period replicated option with put-call parity.

All three partly checked 2026-10-18, draft; numerical examples in `trading_notes.numerical.financial_mathematics.time_value_returns_checks`; human review outstanding.

Corrections of 2026-10-18: `res:cash-flow-additivity` now shows the dated cash flows of forward lending and borrowing and separates them from refinancing at a later, unknown rate; `def:required-return-components` separates the realised (ex post) Fisher identity and the ex ante relation (Mankiw, chap. 5, sec. 5-3) from the expected real return under uncertain inflation; `meth:instrument-present-value` distinguishes nominal annual yields compounded semiannually from effective annual yields.

Written in the statistics slice (2026-10-18):

- `def:return-sample-statistics`: mean, median, mode; range, absolute deviations, variance and standard deviation with $N$ and $N-1$; the $p(N+1)$ percentile rule and the interquartile range.
- `def:return-shape-statistics`: moment skewness and kurtosis with $N$ denominators, bias-adjusted versions, kurtosis against excess kurtosis.
- `def:return-dependence`: covariance and correlation, units, denominators, linearity and other limits.
- `def:downside-relative-dispersion`: semi-deviation about a target with its three denominator conventions; the coefficient of variation and why it fails for returns near or below zero.
- `def:conditional-moments`: unconditional and conditional expectation, variance and covariance, with the laws of total expectation, variance and covariance on a probability table.
- `def:financial-distributions`: normal, lognormal, Student $t$ and binomial moments and when they exist; the lognormal price model.
- `meth:bayesian-updating`: a discrete prior updated by binomial likelihoods, with normalisation and the predictive probability.

All seven partly checked 2026-10-18, draft; examples in `trading_notes.numerical.descriptive_statistics.statistics_probability_checks`; human review outstanding.

Corrections of 2026-10-18: sampling assumptions for the unbiased sample variance; kurtosis read as tail and outlier sensitivity, not central mass; finite sample moments distinguished from nonexistent population moments, with the Student-t thresholds for real degrees of freedom; GBM drift against mean log return; conditional independence in the Bayesian example; the check-script path removed from the printed text.

Written in the inference and simulation slice (2026-10-18):

- `meth:confidence-intervals`: estimand and sampling design; the central limit theorem and its assumptions; exact $t$ and chi-square intervals against normal approximations; the repeated-sampling meaning; failure under serial dependence.
- `meth:hypothesis-testing`: null and alternative, $p$-values, Type I and II errors, power by the noncentral $t$; chi-square and $F$ tests for variances and their normality dependence.
- `meth:nonparametric-tests`: sign and signed-rank tests against the $t$ test, their assumptions and relative power.
- `meth:historical-simulation`: scenario construction from past changes, equal and age weights, and what the window assumes.
- `meth:bootstrap-resampling`: the bootstrap's sampling unit, its ideal value, and the failure of i.i.d. resampling for dependent data against moving blocks.
- `meth:monte-carlo-simulation`: target, seed, standard error and the square-root rule against a closed-form benchmark.

All six partly checked 2026-10-18, draft; examples in `trading_notes.numerical.statistical_inference.inference_simulation_checks`; human review outstanding.

Corrections of 2026-10-18: `meth:historical-simulation` now uses the lower loss quantile and exact-tail-mass ES of `meth:var-es-estimation-methods` for both weightings (VaR 8,400 in both; ES 15,700 equal-weighted and about 14,000 age-weighted), with Hull's equal-weight rank attributed as an alternative; `meth:hypothesis-testing` states the independent-samples condition of the variance-ratio F test and uses an independently drawn second sample, with a correlated-sample counterexample.

Written in the regression slice (2026-10-18):

- `meth:simple-regression-estimation`: population and estimated lines, the least squares criterion and formulas, fitted values and residuals, coefficient units, association against causation.
- `meth:regression-diagnostics-anova`: the LINE conditions and how sensitive inference is to each, residual plots and standardised residuals, the standard error of estimate, $R^2$ and its cautions, coefficient $t$ tests, the ANOVA table and $F=t^2$.
- `meth:regression-prediction-functional-form`: predictions, the interval for the mean against the prediction interval, extrapolation, log functional forms and retransformation to medians and means (normal theory and smearing).

All three partly checked 2026-10-18, draft; examples in `trading_notes.numerical.regression.linear_regression_checks`; human review outstanding. Multiple regression, misspecification, time-series regression and the CAPM regression are not written; `topic:linear-regression` is therefore only partly covered.

Correction pass of 2026-10-18: `meth:simple-regression-estimation` states when the estimates exist (finite data, $S_{xx}>0$); `meth:regression-diagnostics-anova` separates the assumptions for computing, unbiasedness, conventional variances and exact $t$/$F$ inference, requires $n>2$, and restricts $F=t^2$ to the zero-slope null; `meth:regression-prediction-functional-form` treats the back-transformed log prediction as a geometric mean (a median only under a median-zero log error), qualifies Duan's consistency statement and corrects the log--log percentage rule; the ES pitfall of `meth:historical-simulation` now matches the canonical VaR of 8,400.

Credit, time-series and valuation batch (2026-10-20), on annual US data for 1928-2025 and seeded simulations:

- Multiple regression (`trading_notes.numerical.multiple_regression.multiple_regression_checks`): `meth:multiple-regression-formulation`, `meth:multiple-regression-fit-tests`, `meth:regression-misspecification`, `meth:regression-extensions`, built on a regression of Baa corporate bond excess returns on Treasury and equity excess returns.
- Time-series models (`trading_notes.numerical.time_series_models.time_series_checks`): `meth:trend-models`, `def:stationarity-unit-roots`, `meth:autoregressive-forecasting`, `meth:forecast-accuracy-evaluation`, `mod:arch-conditional-variance`, `meth:cointegration-testing`, `meth:time-series-model-selection`, built mainly on US inflation.

Sources: STAT 501 lessons 5-8 and 10-14 (Internet Archive copies), Tsay (2010, 3rd ed.) chaps. 2, 3 and 8, Hyndman and Athanasopoulos (FPP3) secs. 5.8, 5.10, 7.4, 7.5 and 9.1. Partly checked 2026-10-20, draft; human review outstanding. See [record](../source-review-records.md#credit-time-series-and-valuation-batch-20-october-2026).

Written in library gap-filling Batch L1 (2026-10-21), new topic file `compendium/common-toolkit/stochastic-calculus.tex`:

- `def:brownian-motion-quadratic-variation`: Brownian motion from its increments and as the limit of a scaled random walk; quadratic variation $[W]_T=T$, the mean-square argument behind $dW^2=dt$, left-point stochastic integrals.
- `res:ito-lemma-geometric-brownian-motion`: Itô's lemma in one dimension; the GBM solution; mean against median of the terminal price; $E[S_T^2]$ by Itô; Euler discretisation error kept separate from sampling error.
- `res:risk-neutral-pricing-feynman-kac`: market price of risk and Girsanov's change of drift (with the density $Z_T$ as a checked calculation); money-market numeraire; Wilmott's backward-Kolmogorov route from an expectation to the pricing equation.

Sources: Hull, *Options, Futures, and Other Derivatives*, 11th Global ed., chaps. 14, 15 and 28; Wilmott, *Paul Wilmott on Quantitative Finance*, 2nd ed., chaps. 4 and 10. Synthetic examples in `trading_notes.numerical.stochastic_calculus.stochastic_calculus_checks`. Partly checked 2026-10-21, draft; human review outstanding. See [record](../source-review-records.md#library-gap-filling-batch-l1-21-october-2026).

The same batch extended `meth:monte-carlo-simulation` with control variates and the separation of discretisation bias from sampling error (`trading_notes.numerical.statistical_inference.inference_simulation_checks`).

Written in library gap-filling Batch L2 (2026-10-21), in `statistical-inference.tex`:

- `meth:correlation-independence-tests`: the t test of zero correlation, Spearman's rank correlation with midranks and its transform properties, the chi-square test of independence, and the information coefficient with overlapping returns.

Partly checked 2026-10-21, draft. Checks in `trading_notes.numerical.statistical_inference.correlation_independence_checks`. Sources: OpenStax, *Introductory Statistics* 2e, secs. 11.3 and 12.4; NIST Dataplot, "Rank Correlation Independence Test". Human review outstanding. See [record](../source-review-records.md#library-gap-filling-batch-l2-21-october-2026).

## Entry backlog

## What changed in my view or practice

## Questions carried forward

- The equity-risk-premium and credit-spread figures in the required-return example are illustrative; which estimates should replace them, and from what data?
- Newey-West standard errors and the Engle-Granger critical values are used from statsmodels without having read Newey and West (1987) or Engle and Granger (1987); which textbook treatment should be read to state their conditions?
- Does the AR(1) preference over AR(4) for US inflation survive a test of equal predictive accuracy (Diebold-Mariano) rather than a comparison of RMSEs?
