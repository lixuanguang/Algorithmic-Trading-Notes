---
key: wide-boyd-markowitz-seventy
pathways: [portfolio-construction]
version: Stephen Boyd, Kasper Johansson, Ronald Kahn, Philipp Schiele and Thomas Schmelzer, "Markowitz Portfolio Construction at Seventy", Journal of Portfolio Management 50(8), 117-160, July 2024. Copy used: the authors' version dated 5 January 2024, 53 pages, linked from the authors' page in the catalogue (web.stanford.edu/~boyd/papers/markowitz.html), downloaded 2026-10-15 and read through its text layer; journal pagination not checked
sections: secs. 1.1-1.4 (pp. 3-10), 2.4 trading cost (p. 17), 3.2 (pp. 19-20), 3.4 (pp. 21-22), 4.3 (pp. 27-28), 5.6 and Table 2 (pp. 39-40), read for migration slice 28; secs. 3.3 factor model (pp. 20-21) and 4.2 softening constraints (pp. 25-27), read for slice 29; the rest not read; third batch of 2026-10-17: arXiv v1 (2401.05080) sec. 3.4, pp. 21-22, again, and the backtest's covariance paragraph, pp. 31-32, for `meth:portfolio-covariance-estimation`
read:
status: draft
---

Prepared on 2026-10-15 by migration slice 28 from source checks, not from study: the headings that need your own reading are left empty. Only the sections listed were read, to check method mechanics in `mod:mean-variance-portfolio-optimisation`.

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- Markowitz's problem in two forms, maximum return under a volatility target and maximum risk-adjusted return $\mu^\top w-\gamma w^\top\Sigma w$, each with a budget constraint; both have closed forms involving $\Sigma^{-1}$; long-only makes the second a QP (sec. 1.1, pp. 4-5). Sharpe-ratio maximisation is a further objective, convex "at least when the constraints are simple" (sec. 3.2, p. 20).
- The alleged deficiencies (sensitivity to inputs, symmetric risk, expected utility, higher moments, greediness) and the authors' replies (sec. 1.2, pp. 5-8); robust optimisation and regularisation: long-only and leverage limits, Black-Litterman regularising the mean toward market-implied returns, covariance shrinkage (sec. 1.3, pp. 8-9; sec. 3.4, p. 22).
- EWMA, DCC and iterated EWMA as covariance estimators that work well in practice (sec. 3.4, p. 22).
- Trading cost $(\kappa^{\mathrm{spread}})^\top|z|+(\kappa^{\mathrm{impact}})^\top|z|^{3/2}$ as a fraction of portfolio value, with $\kappa^{\mathrm{impact}}_i=a s_i v_i^{-1/2}$ (sec. 2.4, eq. (10), p. 17).
- Factor model $r=Ff+\epsilon$, $f$ and $\epsilon$ uncorrelated, $D$ diagonal, $\Sigma=F\Sigma_fF^\top+D$; economic factors interpretable, PCA factors less so after the first; factor neutrality as zero covariance with a factor, $(\Sigma_fF^\top w)_i=0$; better large-covariance estimates and $O(nk^2)$ solves (sec. 3.3, pp. 20-21).
- Soft constraints: remove $f\le f_{\max}$ and subtract $\gamma(f-f_{\max})_+$; preserves convexity; strict or mandated limits stay hard; priorities from quantiles of Lagrange multipliers (sec. 4.2, pp. 25-27).
- Integer shares, cardinality and minimum-position constraints are nonconvex; mixed-integer solvers are much slower (sec. 4.3, pp. 27-28).
- Solve times with a factor model: 0.65 s for 10,000 assets and 50 factors, 0.89 s with 100 factors, MOSEK (Table 2, p. 40).

## Limits

## Implementation

## Notation map

## Connections

## Entries

`mod:mean-variance-portfolio-optimisation`, `mod:factor-risk-model`; cited in `mod:portfolio-transaction-cost-function`.

## Open questions
