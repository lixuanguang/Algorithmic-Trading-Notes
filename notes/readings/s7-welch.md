---
key: s7-welch
pathways: [backtest-inference, return-predictability]
version: Ivo Welch and Amit Goyal, "A Comprehensive Look at the Empirical Performance of Equity Premium Prediction", RFS 21(4), 2008, as catalogued. Copy used: journal copy on Welch's site (ivo-welch.info), text layer; Table 1 (p. 1470) read as a page image
sections: abstract (p. 1455); data, p. 1457; OOS statistics, eqs. (6)-(7), pp. 1461-1462; estimation periods, p. 1464; Table 1 (annual forecasts)
read:
status: draft
---

Prepared on 2026-10-17 by method validation (2026-10-17) from source checks, not from study: the headings that need your own reading are left empty. Used for `meth:backtest-evaluation-diagnostics` (the R^2 of 0.05).

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- Annual OOS adjusted R^2 negative for every variable in Table 1 with forecasts beginning twenty years into the sample (e.g. d/p IS 0.49, OOS -2.06; e/p 1.08, -1.78; term spread 0.16, -2.42).
- Abstract: the models "predicted poorly both in-sample (IS) and out-of-sample (OOS) for 30 years".

## Source checks for return-predictability (2026-10-22)

- Equity premium: continuously compounded S&P 500 return including dividends less the short rate; d/p = log D12 - log P (p. 1457). Forecasts use only data available at the forecast date (p. 1461); three evaluation periods (p. 1464).
- R^2, Delta RMSE and MSE-F, eq. (6), p. 1461; ENC, eq. (7), p. 1462; MSE-F and ENC nonstandard for nested models, critical values bootstrapped; n. 3: the tests are "ultimately tests of whether beta is equal to zero" (p. 1462).
- The adjusted-R^2 formula printed with eq. (6) gives about -100 percent for R^2 near zero, which Table 1 does not show; read as a misprint.
- Table 1, d/p row (page image, rotated, 220 dpi): IS 0.49; from 20 years: OOS -2.06, Delta RMSE -0.11; from 1965: -3.69, -0.09.

## Limits

Monthly and other horizons, and later tables, not read.
