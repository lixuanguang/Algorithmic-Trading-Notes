---
key: s7-tsay
pathways: [common-toolkit]
version: Ruey S. Tsay, Analysis of Financial Time Series, 3rd ed., Wiley, 2010 (ISBN 978-0-470-41435-4); owner's local PDF outside the repository (SHA-256 749e5738733cb1aca6e2c224f650de4401e55c268d216dcf26275cb84f65d7a2), printed page = PDF page - 27. The catalogue entry does not establish an edition; the 3rd edition was used
sections: chap. 2: pp. 30-31 (stationarity), 37-47 (AR models, PACF, information criteria), 53-56 (goodness of fit, forecasting, half-life), 71-78 (unit-root nonstationarity, Dickey-Fuller and ADF); chap. 3: pp. 114-117 (ARCH effects and model); chap. 8: pp. 428-431 (cointegration)
read:
status: draft
---

Prepared on 2026-10-20 by the credit, time-series and valuation batch (2026-10-20) from source checks, not from study: the headings that need your own reading are left empty. Used for `meth:trend-models`, `def:stationarity-unit-roots`, `meth:autoregressive-forecasting`, `mod:arch-conditional-variance`, `meth:cointegration-testing`, `meth:time-series-model-selection`.

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- Half-life of an AR(1): ln(0.5)/ln|phi1| (p. 56); R2 of an AR(1) fit tends to one for a unit-root series (p. 54).
- Dickey-Fuller t ratio and the ADF regression (pp. 76-77); random walk p_t = p_{t-1} + a_t (p. 72).
- ARCH effects tested by Ljung-Box on squared residuals or Engle's LM regression (p. 114); ARCH(m) model (pp. 115-116).
- Cointegration: both series unit-root nonstationary with a stationary linear combination (p. 430); tests can overlook scaling effects (pp. 430-431).

## Limits

Engle and Granger (1987) and Newey-West were not read; the Engle-Granger procedure and HAC errors are stated as interpretation.
