# Interest-differential (carry) factor for ev:fx-valuation-factors-oos: protocol

Written 2026-10-17 (empirical extensions (2026-10-17) that date) before any carry-factor result was computed. The data are the FRED files
already retained for the v2 relative-PPP test (spot rates, CPI and three-month interbank rates); they were seen in that
test, which reported a portfolio using the same interest rates as its carry leg, so this protocol is recorded in
advance within the session but is not blind to the data and is not a preregistration. The v2 PPP test and its outputs
are unchanged.

## Question

Gliner's carry indicators are the short-rate differentials (policy-rate or LIBOR differentials; chap. 7, pp. 206-208).
Does the three-month interbank rate differential against the dollar forecast dollar exchange rates out of sample,
better than a random walk, for the nine v2 currencies (JPY, GBP, CHF, CAD, AUD, NZD, SEK, NOK, DKK)?

## Definitions and timing (fixed now)

- s_t: log USD per unit of foreign currency, monthly average (FRED H.10/G.5), as in v2.
- Predictor x_t = (i_fx - i_us) for month t - 1, in percent per year, from the OECD MEI series IR3TIB01 (monthly
  averages). Month t - 1 is used because a monthly average is complete only after its month ends; the daily rates
  behind it are observable then, so the lag is one month (an assumption about observability, not a publication date).
- Outcome: ds_{t,t+h} = s_{t+h} - s_t for h = 1 and h = 12.
- Model: ds = a + b x_t + e, estimated by expanding OLS pooled across currencies on pairs whose outcome month
  t' + h <= t (no look-ahead), from START = 1985-01 with at least 60 pooled observations; forecasts from 1995-01.
- Random walk benchmark: zero change.

## Hypotheses and acceptance criteria

- Statistical (primary): the pooled h = 12 out-of-sample R^2 against the random walk is positive and the Clark-West t
  exceeds 1.65. The h = 1 result is reported alongside but is not the verdict.
- Sign: uncovered interest parity predicts b = -h/12 (high-rate currencies depreciate by the differential); the
  forward-premium puzzle literature reports b above that. The estimated b is reported; it is not part of the verdict.
- Economic: an equal-weighted monthly portfolio long currencies with x_t above the cross-sectional median and short
  those below, earning ds over one month plus the one-month accrual of the interest differential (i_fx - i_us)/1200 of
  month t, less 5 bp per unit of turnover (the v2 cost assumption). Supported if the mean net return is positive with
  Newey-West (12 lags) t > 2. This is a statistical return on monthly-average prices and interbank rates, not an
  executable trade (no forwards, no funding spread), as in v2.
- No other specification is part of the verdict.
