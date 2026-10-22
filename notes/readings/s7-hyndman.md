---
key: s7-hyndman
pathways: [regression-time-series]
version: Rob J. Hyndman and George Athanasopoulos, Forecasting: Principles and Practice, 3rd ed., online text (otexts.com/fpp3), chapters 5, 7 and 9 retrieved 2026-10-20 (copies in reading_materials/corp-credit-ts-20261020/fpp3-ch5.html, -ch7.html, -ch9.html)
sections: secs. 5.2 (simple methods as benchmarks), 5.8 (training and test sets; MAE, RMSE), 5.10 (time-series cross-validation), 7.4 (trend, dummy and seasonal dummy predictors), 7.5 (selecting predictors; adjusted R2, CV, AIC, AICc, BIC; spurious regression), 9.1 (stationarity, differencing, random walk, KPSS)
read:
status: draft
---

Prepared on 2026-10-20 by the credit, time-series and valuation batch (2026-10-20) from source checks, not from study: the headings that need your own reading are left empty. Used for `meth:multiple-regression-formulation`, `meth:regression-extensions`, `meth:trend-models`, `def:stationarity-unit-roots`, `meth:autoregressive-forecasting`, `meth:forecast-accuracy-evaluation`, `meth:cointegration-testing`, `meth:time-series-model-selection`.

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- Accuracy only from data not used in fitting; RMSE favours the mean, MAE the median (sec. 5.8); time-series cross-validation uses only earlier observations (sec. 5.10).
- Scatterplot screening and dropping insignificant predictors are invalid selection methods (sec. 7.5); high R2 with autocorrelated residuals signals spurious regression (sec. 7.5).
- KPSS null is stationarity; small p-values suggest differencing (sec. 9.1).

## Limits

Online text that changes; chapter 10 (dynamic regression) and chapter 9's ARIMA estimation were not read.
