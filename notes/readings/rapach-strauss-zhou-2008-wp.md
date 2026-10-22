---
key: rapach-strauss-zhou-2008-wp
pathways: [return-predictability]
version: David E. Rapach, Jack K. Strauss and Guofu Zhou, "Out-of-Sample Equity Premium Prediction: Consistently Beating the Historical Average", working paper, first draft 23 July 2007, version of 6 February 2008 (published, retitled, as "Out-of-Sample Equity Premium Prediction: Combination Forecasts and Links to the Real Economy", Review of Financial Studies 23(2), 2010, catalogue wide-rapach-strauss-zhou, not obtained). Copy used: Zhou's former web copy (apps.olin.wustl.edu/faculty/zhou/RSZ.pdf, 404 on 2026-10-22) from the Wayback Machine capture of 2016-06-16 (38 pages, SHA-256 c8dab2ae...f909); printed page = PDF page - 1; tables on unnumbered pages at the end
sections: abstract; secs. 1-2 (pp. 1-12); sec. 3.1-3.2 (pp. 12-19); secs. 3.6 and 4 (pp. 21-23); notes to Tables 1-4 and Table 1 (PDF pp. 29-30)
read:
status: draft
---

Prepared on 2026-10-22 by the forecast-combination and proper-scoring batch from source checks, not from study: the headings that need your own reading are left empty. Used for `meth:forecast-combination`.

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- Individual model (1): r_{t+1} = alpha + beta x_{i,t} + e_{t+1}, recursive (expanding) OLS; the historical average as the benchmark (pp. 3-4; the printed benchmark formula omits the 1/t).
- Combination (2): r_c = sum_i omega_{i,t} r_i, weights formed ex ante at t; mean (1/N), median, trimmed mean (drop the extremes, 1/(N - 2) on the rest); simple schemes need no holdout (pp. 4-5). DMSPE weights (3)-(4): inverse discounted MSPE over the holdout, theta = 1 (the paper calls Bates-Granger optimal for uncorrelated forecasts) and 0.9 (p. 5). For the MSE optimum, the precise condition is unbiased, uncorrelated forecast errors, so their second-moment matrix is diagonal (Interpretation). Clusters C(K, PB), K = 2, 3, and approximate BMA by SIC or AIC (pp. 5-6). Holdout: the 60 months before each evaluation period (n. 16, p. 14).
- Restrictions: slope set to zero if its sign disagrees with the expected sign, taken from full-sample estimates (n. 9, p. 8); negative forecasts set to zero (p. 8).
- Evaluation: R2_OS (6), Clark-West MSPE-adjusted statistic (7), one-sided; n. 11 (p. 9): its behaviour for combination forecasts has not been analysed. Utility gain for gamma = 3 with weights in [0, 1.5] and a five-year rolling variance (eqs. (8)-(11), pp. 9-10). Data-mining bootstrap with maximal statistics, 200 replications (sec. 2.5, pp. 11-12).
- Data: Goyal and Welch's monthly file, 14 predictors available 1927:01-2005:12, log S&P 500 returns less the T-bill rate (pp. 12-13). Evaluation periods 1947:01, 1965:01, 1976:01 and 2000:01 to 2005:12 (pp. 13-14).
- Table 1 (1947:01-2005:12, PDF p. 30): unrestricted OLS, four of 14 predictors have a positive R2_OS, the largest 0.33 (term spread); mean combination 0.95 (MSPE-adj. p-value 0.09 percent), median 0.81, trimmed mean 0.91, DMSPE 0.95 and 0.96, clusters 0.46 and 0.42, ABMA 0.95 (text p. 16).

## Limits

The covariate-estimation results (sec. 2.3, Panels C-D) and Tables 2-6 were not used. The RFS 2010 version, which adds the "links to the real economy" and may revise the design, sample and numbers, was not obtained (HTTP 403 from doi.org, OUP and SSRN on 2026-10-22). The forecast-error covariance and diversification argument of `meth:forecast-combination` is labelled Interpretation; this working paper states only the Bates-Granger reading of DMSPE with theta = 1.
