# Deflation / disinflation row of the regime map, real-time classification: protocol

Written 2026-10-17 (derivatives and empirical validation (2026-10-17) that date) after the inflation-shock row had been run on the same quarterly CPI
vintages and response series (inflation_quarterly_test.py), and before any deflation-row result was computed.
The data are therefore not new to this session; the protocol is recorded in advance of this row's results and
committed with them, so it is not a preregistration.

## Hypothesis (def:macro-regime-asset-map, "Deflation or disinflation")

"Nominal yields and breakevens down, duration rallies." Breakevens are not tested (TIPS history too short for most of
the sample); "duration rallies" is the same sign as falling nominal yields, so one response is tested.

## Regime, real time (mirror image of the inflation-shock rule)

Philadelphia Fed quarterly CPI vintages (cpiQvMd.xlsx), vintage month m the middle month of the quarter. In vintage v
with last reported month L: pi(L) = 100 ln(P_L / P_{L-12}); signal = 1 if pi(L) - pi(L-12) <= -1.0 point (a
deceleration of at least one point over a year). Threshold fixed now, not varied. Skip rules as in the inflation row.

## Response and test

- dy10 = GS10(m+3) - GS10(m), hypothesis < 0.
- Mean in signal quarters minus other quarters, Welch t; supported if the difference is negative with |t| > 2.
- Reported alongside, not part of the verdict: Newey-West t (4 lags), the number of episodes, and the slope and WTI
  responses defined as in the inflation row.
