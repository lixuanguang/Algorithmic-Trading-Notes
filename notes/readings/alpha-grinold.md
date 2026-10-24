---
key: alpha-grinold
pathways: [portfolio-construction-risk, equity-long-short-construction]
version: Richard C. Grinold and Ronald N. Kahn, Active Portfolio Management, second edition, McGraw-Hill (1999 copyright), as catalogued. Copy used: a local PDF outside the repository with a text layer; printed pages from the running heads
sections: chap. 10, "Forecasting Basics", pp. 261-271, with pp. 265-266 as page images; performance and planning batch (2026-10-18): chap. 3, pp. 49-50, 67 and 76-78 (active and residual risk, marginal contributions, risk decomposition and attribution); chap. 4, p. 90 (active beta and residual variance); chap. 5, pp. 109-124 and Technical Appendix pp. 136-137 (information ratio, Tables 5.1 and 5.3); chap. 6, pp. 147-163 (fundamental law). Printed page = PDF page - 8; equations are images, so formulas were confirmed from the surrounding text, tables and worked numbers; derivatives, portfolio and execution batch (2026-10-19), read in a second local copy of the same 1999 edition (SHA-256 5c2e3efad6032e6b8965835fdbc2ff99a1cdbd8b57b2984752161975ec1c13b8, printed page = PDF page - 4, cited by running-head pages): chap. 14, pp. 393-396 and 408-409 (four construction procedures, screens, stratification, summary); chap. 15, pp. 419-420 (long/short and the long-only constraint); chap. 16, p. 456 (turnover)
read:
status: draft
---

Prepared on 2026-10-17 by the source verification (2026-10-17) from source checks, not from study: the headings that need your own reading are left empty. Used for `meth:forecast-scaling-ic`.

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- Basic forecasting formula and refined forecast (eqs. 10.1-10.2, pp. 262-263).
- Rule of thumb: refined forecast = volatility x IC x score (eq. 10.11, p. 266); binary-model example IC = 0.0833, multiplier 0.75.
- Two forecasts: weights 0.1467 and 0.1307, combined IC 0.1090 (pp. 269-271); Table 10.1 (p. 269).

## Key results (performance and planning batch, 2026-10-18)

- Ex post and ex ante IR; top-quartile IR about 0.5 (Table 5.1, p. 114); IR independent of aggressiveness, proportional to sqrt(horizon) (pp. 115-117); omega* = IR/(2 lambda), Table 5.3 reproduced (p. 123).
- IR = IC sqrt(BR), assumptions, additivity, combined correlated sources, not the law of large numbers, binary example (IR 1.157 against 1.155), transaction-cost footnote (pp. 147-163).
- Active variance split into factor and specific (pp. 76-77) and into active beta and residual (p. 90). Used for `meth:active-return-information-ratio`, `res:fundamental-law-active-management`, `meth:active-risk-decomposition` and `meth:return-attribution`.

## Limits

Chaps. 3-6 and 10 read in part as listed; chaps. 11-12 not read.

Audit repair, method validation (2026-10-17): n. 1 (p. 263) uses E{r|g} "somewhat loosely"; the Technical Appendix proves the best linear estimate (Proposition 1, pp. 287-288) and the conditional expectation only under joint normality (Proposition 2, p. 289). Own checks: `trading_notes.numerical.signal_combination.linear_projection_checks`.
