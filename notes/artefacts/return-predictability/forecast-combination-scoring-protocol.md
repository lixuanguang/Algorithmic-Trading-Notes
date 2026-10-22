# Forecast combination and proper scoring checks: protocol

Written 2026-10-22, before `forecast-combination-scoring-checks.py` existed and before any statistic of the
predictors below had been computed. When it was written, the published tables compared with below had already been
read: Rapach, Strauss and Zhou's working paper of February 2008, Table 1, and Gneiting and Raftery (2007),
Table 2. The workbook had been inspected for column names and date ranges only. The protocol is fixed in advance
within the session; it is not blind to the published numbers and is not a preregistration. It serves
`meth:forecast-combination` and `meth:proper-scoring-rules`. The earlier batch's protocol, data, script and results
in this folder are unchanged.

## Sources and versions

- `rapach-strauss-zhou-2008-wp`: D. E. Rapach, J. K. Strauss and G. Zhou, "Out-of-Sample Equity Premium Prediction:
  Consistently Beating the Historical Average", working paper, first draft 23 July 2007, version of 6 February 2008,
  38 PDF pages. Zhou's copy (`apps.olin.wustl.edu/faculty/zhou/RSZ.pdf`, now 404) was retrieved from the Wayback Machine
  (capture 2016-06-16, the same digest as the 2014-12-22 capture), SHA-256 `c8dab2ae…f909`. Printed page = PDF page
  − 1 in the text; the tables are on unnumbered PDF pages 30–35. This paper is the precursor of the catalogue's
  `wide-rapach-strauss-zhou` (RFS 23(2), 2010). The RFS version could not be obtained (doi.org, OUP and SSRN returned
  HTTP 403 on 2026-10-22), so nothing below is attributed to it.
- `wide-gneiting-raftery`: JASA 102(477), March 2007, pp. 359–378, author-hosted copy
  (`sites.stat.washington.edu/people/raftery/Research/PDF/Gneiting2007jasa.pdf`), SHA-256 `d31a0c5f…7ba2`, 20 pages,
  the journal's typeset version; PDF page = printed page − 358.

## Data

- `goyal-annual-predictors-1871-2025.csv`, extracted by `goyal_extract_predictors.py` from the same workbook as the
  earlier batch (Goyal's page, "Original data (up to 2005) used in the paper", SHA-256 `8d210b77…be872`, retrieved
  2026-10-22), Annual sheet, columns `yyyy, Index, D12, E12, tbl, AAA, BAA, lty, Rfree, CRSP_SPvw`, as printed. The
  workbook runs to 2025, so it is a 2026 vintage. It is not the file behind either paper's tables. The earlier CSVs are
  not modified.
- Synthetic data from the fixed seeds below.

## Part F: forecast combination (annual)

Fixed now, before any result:

- **Outcome.** The annual log equity premium `y_t = log(1 + CRSP_SPvw_t) - log(1 + Rfree_t)`, outcomes 1927–2025. This
  is the definition used for Welch and Goyal's row in the earlier batch.
- **Predictors** (N = 4, dated t - 1, as printed in the workbook, no other transformation):
  `dp = log D12 - log Index`, `ep = log E12 - log Index`, `tms = lty - tbl`, `dfy = BAA - AAA`. They were chosen for
  being among the working paper's 14 (listed on p. 13, PDF p. 14) and for being definable from the extracted
  columns without lags or release adjustments. Two are valuation ratios and two are bond-market spreads, chosen in
  advance so that the forecast errors would include correlated and less-correlated pairs. No other predictor set is
  run.
- **Forecasts.** Recursive OLS of `y_s` on a constant and `x_{i,s-1}` over outcomes 1927 to t - 1. The benchmark is the
  mean of `y_s` over the same outcomes. First forecast 1947 (R = 20 regression observations, 1927–1946); evaluation
  1947–2025 (P = 79). Second window reported: 1947–2005 (P = 59), the working paper's long period. The combination is
  the equal-weight mean of the four regression forecasts (working paper eq. (2) with `ω = 1/N`). No restrictions, no
  holdout, no estimated weights.
- **Rows printed in the entry**, fixed now: forecasts for 1947, 1970, 1990, 2010 and 2025.
- **Reported (no gate on their values):** for each predictor and the combination, the MSFE, `R2_OS` (percent),
  `ΔRMSE` (percentage points) and the Clark–West t statistic. The Clark-West statistic is a reported number, since an
  average of four regressions is not a nested linear model (the working paper's n. 11, PDF p. 10). Also reported: the
  correlation matrix of the four forecast errors and of the four deviations `f_i - f_bar`, and the decomposition below.
  Nothing is required to beat the benchmark. The working paper's Table 1 (monthly, 14 predictors, 1947:01–2005:12) is
  quoted as context, not compared numerically.

Gated checks (correctness only):

- F1. Recursive forecasts by running sums agree with `numpy.linalg.lstsq` refitted at each origin to 1e-10.
- F2. Chronological indexing: overwriting every outcome and predictor after year t leaves every forecast for years up
  to t + 1 unchanged (t = 1970 and 2000). This does not model publication lags, data revisions or point-in-time
  availability.
- F3. The combination's error is the mean of the four errors, to 1e-12, and
  `MSE_c = (1/N^2) 1' S 1`, where `S` is the matrix of mean products of errors (no demeaning), to 1e-12. Also
  `MSE_c = mean_i MSE_i - mean_i mean_t (f_i - f_c)^2`, the ambiguity decomposition (Interpretation), to 1e-12; so
  `MSE_c <= mean_i MSE_i`.
- F4. Synthetic diversification limit (seed 20261105): N = 4 errors with unit variance, common correlation
  `ρ ∈ {0, 0.5, 0.9, 0.99}`, 200,000 draws. The MSE of the average lies within 0.01 of `ρ + (1 - ρ)/N`.
- F5. With unbiased forecast errors and a diagonal covariance (hence diagonal second-moment matrix), the minimum-MSE
  weights `Σ^{-1}1 / 1'Σ^{-1}1` equal inverse-MSE weights to 1e-12. This is the precise MSE-optimality condition behind
  the working paper's shorthand that the forecasts are uncorrelated (p. 5; Interpretation). With the sample error
  covariance of the four predictors (1947–2025, ex post) the two weight vectors are reported only.

## Part S: proper scoring (synthetic, units stated)

Sign convention for every number: **negatively oriented losses** (smaller is better), the negatives of Gneiting and
Raftery's positively oriented scores. The units are percentage points of annual excess return unless a line says
otherwise.

- S1. Hand example: forecasts `A = N(5, 10^2)` and `B = N(5, 20^2)` (same mean, different spread), outcomes
  `x ∈ {5, -15, -40}`. Reported: squared error of the mean, `-log f(x)` (nats, with x in percent; and the same with x in
  decimals), CRPS, and the 90 percent central interval score (α = 0.1). Gated:
  - CRPS from the closed form for the normal agrees with quadrature of eq. (20) to 1e-7 and with the kernel form
    eq. (21) by Monte Carlo (seed 20261106, 10^6 pairs) within 4 Monte Carlo standard errors;
  - the interval score (43) equals (2/α) times the sum of the two quantile scores (41) at levels α/2 and 1 - α/2
    (negatively oriented, `(1{x <= r} - α')(r - x)`) to 1e-12;
  - the log scores in percent and in decimals differ by exactly `log 100`, and the A–B difference is unit-free.
- S2. Propriety by quadrature: truth `Q = N(5, 15^2)`; forecasts `N(5, s^2)`, s = 5.0, 5.5, …, 30.0. The expected log
  score, CRPS and 90 percent interval score are each smallest at s = 15. The expected linear score
  `E_Q[f(x)]` (positively oriented, an improper rule, p. 366) is largest at the smallest s on the grid. Gated.
- S3. Gneiting and Raftery's Table 2 (p. 371) in their design: the bilinear process (44), one path of 100,001
  observations after a burn-in of 1,000 (seed 20261107; the burn-in is not in the paper), one-step 95 percent intervals
  I (45), J (46) and K (47) for t = 1, …, 100,000. J's unconditional quantiles are not given in the paper. They are
  estimated from a separate path of 10^7 observations (seed 20261108). Gated: coverage within 0.5 percentage points
  of the table, average width within 2 percent and average interval score within 3 percent of the table; the order
  by average interval score is I < K < J, as published. Batch-means standard errors (100 batches) are reported.
- S4. Averaging point forecasts is not combining densities (Interpretation). Two forecasts `N(0, 10^2)` and
  `N(8, 10^2)`. The equal-weight linear pool is the mixture, with mean 4 and variance `100 + 16 = 116`. The Gaussian
  centred on the averaged point forecast is `N(4, 10^2)`. Gated: the mixture's variance by quadrature equals 116
  to 1e-8; with the pool as the truth, its expected log score and CRPS (quadrature) are below those of `N(4, 10^2)`,
  as strict propriety requires. Reported: both forecasts' scores at x = -15, 4 and 20.

No other specification is part of a verdict. After the first run, the observed values are added to the script as
regression checks at their printed rounding. Any later change to this protocol is recorded below with its reason.

## Changes after the first run

First run, 2026-10-22: all 55 gated checks passed (F1–F5, S1–S4). No definition, seed or tolerance was changed.

1. Recorded values (part R of the script): the reported R2_OS of both windows, the combination's Clark–West t, the
   ambiguity terms, S2's expected scores at s = 15, S3's average interval scores and S4's expected scores are asserted
   at their printed rounding, to detect drift. Final: 62 checks.

2. Audit corrections (22 October 2026, after the first run): the equicorrelation formula is stated for unbiased errors;
   with individual error biases it includes the squared average bias. Two exact deterministic checks (F6) use
   nonzero member biases to verify `MSE = variance + mean bias squared` and preserve both the general second-moment and
   ambiguity identities. The predictor years are calendar-indexed: release lags and revisions are not modeled,
   especially for E12, so the exercise does not establish point-in-time availability or an investable real-time
   backtest. The comparison normal in S4 is identified as a chosen distribution with the average component variance;
   point forecasts alone determine neither a variance nor a predictive distribution. No data, seeds, or reported
   forecast/scoring results changed. Current total: 64 checks.

Outcome, reported and not gated. **Part F, 1947–2025:** every single-predictor forecast has a higher MSFE than the
historical mean (R2_OS −1.83, −2.28, −3.60 and −0.83 percent for dp, ep, tms and dfy). The equal-weight combination
has R2_OS +2.56 percent (ΔRMSE +0.21 points), with a Clark–West t of 1.44. That t is a descriptive number, because an
average of four regressions is not a nested linear model. **Part F, 1947–2005:** dp and ep beat the mean (+1.34, +4.61);
the combination gives +5.82. The forecast errors are correlated between 0.89 and 0.98, because all four share the
unpredictable part of the return. Their deviations from the historical mean are correlated between −0.30 and 0.82.
The combination's gain over the average individual MSFE is exactly the mean squared spread of the forecasts about
their average: 0.1277 against 2.7777 (both × 100).

**Part S3:** I, J and K give coverages of 94.98, 94.91 and 94.94 percent, widths of 4.00, 5.46 and 3.79, and average
interval scores of 4.76, 8.03 and 5.29, against the published 95.01/95.08/94.98, 4.00/5.45/3.79 and 4.77/8.04/5.32.
This is a reproduction in the source's design, apart from the unstated burn-in, the seed and J's quantiles
(estimated here as −2.040 and 3.419).
