# Hedging pressure in WTI: protocol (ev:backwardation-scarcity-or-premium, the untested half)

Written 2026-10-17 (fourth batch of that date) before any Commitments of Traders file was downloaded and before any
result was computed. It is committed together with the results, so it is a protocol recorded in advance within the
session, not a preregistration. The WTI held-contract returns come from the v2 panel already computed and seen
(backwardation_monthly.csv); only the hedging-pressure series is new.

## Question

The backlog's remaining half: does commercial (hedger) positioning predict WTI futures returns, as the hedging-pressure
view (Keynes, Hicks; Cootner) says? Net short hedging should require a premium to long speculators, so higher
hedging pressure should predict higher returns on a long futures position.

## Data

- CFTC Commitments of Traders, legacy report, futures only, historical compressed files (deacot1986_2016.zip and the
  annual files for 2017 onward), market "CRUDE OIL, LIGHT SWEET - NEW YORK MERCANTILE EXCHANGE" (CFTC contract market
  code 067651). If the code or name changes inside the sample, that is reported and the series is spliced only where
  CFTC's code is unchanged.
- Returns: the v2 WTI panel (backwardation_monthly.csv, column r: the simple return of holding contract 2 from month-end
  t to month-end t+1, with contract identity checked), as defined by the WTI protocol; its return definition is not
  changed here.

## Definitions and timing (fixed now)

- HP_t = (commercial short - commercial long) / (commercial short + commercial long), from the latest report whose
  positions date (Tuesday) R satisfies R + 3 calendar days <= t, the month-end settlement date of the panel (the report
  is normally released on the Friday after R at 3:30 p.m. ET; delayed releases, as in government shutdowns, are not
  modelled and are a stated limitation).
- Sample: every month of the WTI panel with a usable HP_t.

## Hypothesis and acceptance

- H: beta > 0 in r_{t+1} = a + beta HP_t + u_{t+1}; supported if the Newey-West (12 lags) t > 2 AND the expanding
  out-of-sample R^2 (from month 121, against the expanding mean) is positive with a Clark-West t above 1.65 — the same
  rule as the premium test P of the v2 protocol.
- Reported alongside, not part of the verdict: the full-sample correlation of HP_t with the basis B_t; the regression
  of r on both B_t and HP_t.
