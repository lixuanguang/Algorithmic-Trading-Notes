---
key: wide-lo-sharpe
pathways: [backtest-inference]
version: Andrew W. Lo, "The Statistics of Sharpe Ratios", Financial Analysts Journal 58(4), 36-52, 2002, as catalogued. Copy used: the published article (AIMR copyright line, journal pagination) hosted on a Berkeley student-organisation site, provenance not established, downloaded 2026-10-17; text layer, pp. 38, 40 and 41 checked as page images
sections: pp. 36-41 (IID, non-IID and time-aggregation sections, Tables 1-2); Appendix A only for the Newey-West reference
read:
status: draft
---

Prepared on 2026-10-17 by the source verification (2026-10-17) from source checks, not from study: the headings that need your own reading are left empty. Used for `meth:sharpe-ratio-standard-error`.

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- IID: SE(SR) = sqrt((1 + SR^2/2)/T) (eq. 9, p. 38); 0.188 at SR 1.50 and 0.303 at 3.00 for T = 60, recomputed.
- Non-IID: GMM variance under stationarity (eqs. 13-15, pp. 39-40).
- Time aggregation: SR(q) = eta(q) SR, eta(q) = q / sqrt(q + 2 sum (q-k) rho_k) (eq. 20, p. 40); AR(1) closed form eq. 22 and Table 2 (p. 41) recomputed.

## Limits

Asymptotic; the empirical sections and Appendix A were not checked.

Audit repair, method validation (2026-10-17): eq. (5) (p. 38, page image) asserts Var(sigma-hat^2) -> 2 sigma^4 under "finite mean and variance", which needs normal fourth moments; recorded as an overstatement in the source, not edited. Eqs. (25)-(26) (p. 42) give the nu_3, nu_4 form and the normal special case; eq. (16) and note 7 (pp. 40, 51) define additive q-period returns. Own checks: `trading_notes.numerical.backtest_evaluation.sharpe_conditions_checks`.
