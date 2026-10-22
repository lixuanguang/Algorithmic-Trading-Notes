# Return predictability checks: protocol

Written 2026-10-22, before `return-predictability-checks.py` was first run and before any statistic on the data
below was computed. By then the published tables being compared with had been read (Campbell and Shiller 1986,
Table 1a; Clark and West 2006, Tables 1 and 4; Welch and Goyal 2008, Table 1; Campbell and Thompson 2005,
Table 2), and the extracted data had been inspected for column names, date ranges and missing values only. The
protocol is recorded in advance within the session; it is not blind to the published numbers and is not a
preregistration. It serves `res:campbell-shiller-identity`, `meth:nested-forecast-tests` and
`meth:restricted-forecast-value`.

## Data

- `goyal-annual-1871-2025.csv` and `goyal-monthly-1871-2025.csv`, extracted by `goyal_extract.py` from the
  workbook Goyal's page labels "Original data (up to 2005) used in the paper" (SHA-256 recorded in the script and
  the CSV headers). The file served on 2026-10-22 runs to December 2025, so it is a 2026 vintage. Differences from
  the published tables may come from data revisions; they are reported, not tuned away.
- Synthetic data from fixed seeds (below), for checks where the true model must be known.

## Definitions and timing (fixed now)

- Annual simple return for year t: `CRSP_SPvw` from 1926; before 1926, `(Index_t + D12_t) / Index_{t-1} - 1`.
  Monthly simple return for month t: `CRSP_SPvw` from January 1926; before that,
  `(Index_t + D12_t / 12) / Index_{t-1} - 1`.
- Log return `r_t = log(1 + R_t)`; log dividend growth `Δd_t = log D12_t - log D12_{t-1}`; log dividend-price
  ratio `dp_t = log D12_t - log Index_t`; price-dividend ratio `pd_t = -dp_t`.
- Annual log equity premium (Welch and Goyal): `log(1 + R_t) - log(1 + Rfree_t)`. Monthly simple excess return
  (Campbell and Thompson): `R_t - Rfree_t`.
- Every forecast of the outcome in period t uses `dp_{t-1}` and parameters estimated only from pairs
  `(dp_{s-1}, y_s)` with `s <= t - 1` (recursive, expanding window). The benchmark is the mean of `y_s`, `s <= t - 1`.
- Statistics over the P forecasts: `R2_OS = 1 - MSE_A / MSE_N` (A predictive regression, N historical mean);
  `ΔRMSE = sqrt(MSE_N) - sqrt(MSE_A)` in percent per period; `MSE-F = P (MSE_N - MSE_A) / MSE_A` and
  `ENC = Σ e_N (e_N - e_A) / MSE_A` (Welch and Goyal eqs. (6)-(7) with h = 1, so `T - h + 1 = P` and
  `(T - h + 1)/T = 1`); Clark-West `f_t = e_N^2 - [e_A^2 - (ŷ_N - ŷ_A)^2]`, regressed on a constant, with the
  ordinary least-squares t statistic (one-step forecasts).
- Welch and Goyal's printed adjustment `R̄² = R² - (1 - R²)(T - k)/(T - 1)` would put an R² near zero at about
  -100 percent, which their Table 1 does not show; it is read as a misprint. The script reports the unadjusted
  `R2_OS` and the conventional `1 - (1 - R2)(T - 1)/(T - k)` with k = 2, and compares the adjusted value with
  Table 1 only as a reported number. `ΔRMSE` needs no adjustment and is the gated comparison.
- Linearisation constant: `ρ = 1 / (1 + exp(mean dp))` over the sample used, the 1988 form also used by Cochrane
  (2008, p. 1540). The working paper's point, `ρ = exp(-(mean r - mean Δd))` (Campbell and Shiller 1986, pp. 4-5),
  is reported alongside. *[Audit correction: "mean r" here was implemented as the mean log return; the paper (p. 5)
  takes the log of one plus the sample average return, `r = log(1 + mean R)`. See* Audit corrections *below.]*

## Checks and acceptance criteria

### A. Present-value identity (annual data, 1872-2025, and 1872-1986 for comparison with Campbell and Shiller)

1. The exact identity `r_t = Δd_t - pd_{t-1} + log(1 + exp(pd_t))` holds to 1e-12 for every year. (Algebra and
   timing check.) *[Audit correction: the first run checked 1872-1925 only, because the return defined above is
   CRSP's from 1926; parts A1-A4 now use one return built from `Index` and `D12` in every year.]*
2. The linear approximation `r_t ≈ k + ρ pd_t - pd_{t-1} + Δd_t` has error variance below 0.5 percent of the
   variance of `r_t` and correlation above 0.99 with `r_t`. Campbell and Shiller report 0.0008 and 0.9996 for
   real returns 1871-1986 (Table 1a, column ii); their series and deflator differ, so only the order is compared.
3. Iterating the approximate identity J = 1, 5, 10 and 20 years forward reproduces `pd_t` exactly once the
   approximation errors and the terminal term `ρ^J pd_{t+J}` are kept (to 1e-10); the terminal term's weight
   `ρ^J` is reported.
4. In-sample OLS on `dp_{t-1}` over 1927-2004 and 1872-2025: `b_r - b_d + ρ φ = 1 + b_ε` holds to 1e-10, where
   `b_ε` is the slope of the approximation error `ε_t = r_t - (k + ρ pd_t - pd_{t-1} + Δd_t)`. Cochrane reports, for real CRSP data 1927-2004,
   `b_r ≈ 0.10`, `b_d ≈ 0`, `φ ≈ 0.94` and `ρ = 0.9638` (pp. 1540-1541); the S&P series here differs, so these
   are reported, not gated.

### B. Nested forecast comparison

1. Hand example: eight declared observations; recursive forecasts by explicit formulas agree with
   `numpy.linalg.lstsq` to 1e-12; `mean(f) = MSE_N - (MSE_A - adj)` and `mean(f) = 2 mean(e_N (e_N - e_A))`
   (Clark-West eqs. (2.1), (3.9)-(3.10), (4.1)); `ENC = P mean(f) / (2 MSE_A)` to 1e-12.
2. Timing: changing every observation after period t leaves every forecast for periods up to t + 1 unchanged.
3. Monte Carlo, Clark and West's DGP 1 (eq. (6.1)): `y_t = 0.5 + γ z_{t-1} + e_t`,
   `z_t = 0.15 + 0.95 z_{t-1} + v_t`, var(e) = 18, var(v) = 0.025, corr(e, v) = -0.75, initial z drawn from its
   stationary distribution; recursive forecasts, R = 120, P = 120 and 240; 5,000 replications; seed 20261022.
   Under γ = 0:
   - the mean of `MSE_N - MSE_A` is negative with Monte Carlo t below -5 for both P;
   - Clark-West one-sided rejection at 1.282 lies in [0.04, 0.11] and within 0.02 of Clark and West's Table 1,
     panel B1 (0.085 for P = 120, 0.070 for P = 240);
   - the unadjusted ("MSPE-normal") test rejects in less than 0.03 of replications (their 0.028 and 0.012).
   Under γ = 0.35 (P = 240, same seed stream continued): Clark-West rejects more often than the unadjusted test.
4. Welch and Goyal's annual dividend-price row (data 1872-2005; first forecast for 1892, after 20 regression
   observations; and from 1965): the in-sample adjusted R² within 0.25 points of 0.49; ΔRMSE within 0.05 points of
   -0.11 (from 1892) and -0.09 (from 1965). R2_OS, the adjusted value, MSE-F, ENC and the Clark-West t are reported.
   A miss is recorded as a failed reproduction with the vintage caveat, not corrected by changing definitions.
5. Start-date sensitivity, reported only: R2_OS and Clark-West t for evaluation from 1892, 1927, 1947, 1965 and
   1985, ending 2005 and ending 2025.

### C. Restricted forecasts and economic value (monthly)

1. Hand example: three declared months; the weight `w = clip(μ̂ / (γ σ̂²), 0, 1.5)`, the portfolio return
   `R_f + w (R - R_f)` and the utility `mean(R_p) - (γ/2) var(R_p)` agree with explicit arithmetic.
2. Campbell and Thompson's dividend-price comparison: monthly, regression data from February 1871, forecasts
   January 1927 to December 2003, γ = 3, weights in [0, 1.5], variance from all excess returns observed before
   the month. Forecasts: historical mean; unrestricted regression; restricted (slope set to zero, so the forecast
   is the historical mean, when it is negative; then any negative forecast set to zero; the historical-mean
   forecast is floored at zero too). The expected sign is fixed in advance as positive, from theory, not from the
   full-sample estimate. Reported: R2_OS for each, the historical-mean investor's utility (Table 2: 0.501 percent
   a month), and the utility changes (Table 2: -0.016 unrestricted, -0.024 restricted). Gated: the utility level
   within 0.05 points of 0.501, and both changes within 0.05 points of zero, the range Table 2 shows for this
   predictor. Their signs are reported, not gated.
3. Same calculation extended to December 2025, reported only.
4. Synthetic check of the mechanism: DGP 1 rescaled to monthly decimals (y in percent divided by 100), γ = 0.35,
   R = 240, P = 480, 1,000 replications, seed 20261023. Reported: mean utility gain of the unrestricted and the
   restricted forecast over the historical mean; gated only that the gain is computed from out-of-sample
   forecasts (timing check as in B2).

No other specification is part of a verdict. After the first run the observed values are added to the script as
regression checks, and any change to this protocol after that run is recorded below with its reason.

## Changes after the first run

First run, 2026-10-22: every gated check in A, B and C1-C3 passed; the script then stopped in C4 with a NumPy
`RuntimeWarning` (run under `-W error`) because the running variance was computed for the first outcome too
(division by n - 1 = 0) before the unused column was sliced away. No reported number depended on that column.

1. Harness correction (C4): the running variance is computed only for the forecast months. Results unchanged.
2. Diagnostic (C4): the share of months whose weight sits at the 1.5 cap. It shows a design flaw in this
   protocol: DGP 1's mean excess return, 0.5 + 0.35 x 3 = 1.55 percent a month against a variance of 18 percent
   squared, asks for a weight near 2.9, so the cap binds in nearly every month (100 percent for the historical
   mean, 97.7 percent for the regression) and the synthetic check cannot show the value of a forecast. C4's
   numbers are kept and reported as they are.
3. Supplement (C5, not part of any verdict): the same design with the intercept lowered by 1.05 so that the mean
   excess return is 0.5 percent a month, seed 20261024, and the known-parameter conditional utility gain
   `(1/(2γ)) (R2/(1 - R2)) (1 + S2)` as a reference (half the expected-return gain of Campbell and Thompson's
   eq. (8)). A units slip in the first version of that reference line (an extra division by 100) was corrected
   before the values were recorded.
4. Recorded values: the observed numbers of A2, B3, B4, C2, C3 and C5 are asserted at their printed rounding, to
   detect drift. No tolerance in this protocol was changed.

Outcome against the protocol: A1-A4, B1-B4 and C1-C2 pass. Two results sit inside their tolerances but are worth
stating. The Clark-West sizes, 0.069 (P = 120) and 0.059 (P = 240), are 0.016 and 0.011 below Clark and West's
0.085 and 0.070, more than the Monte Carlo standard error (about 0.004); the cause was not identified. The
in-sample adjusted R2, 0.32 against 0.49, and ΔRMSE from 1965, -0.13 against -0.09, differ from Welch and Goyal's
by more than rounding, which is consistent with, but not shown to be caused by, the 2026 data vintage.

## Audit corrections (22 October 2026, after the record above)

An audit of the uncommitted batch, the same day, found two calculation errors in part A and an under-qualified size
statement in part B. Each was checked against the local source PDFs (Campbell and Shiller, NBER WP 2100, printed
pp. 4-5 and Table 1a, as page images; Clark and West, NBER Technical WP 326, pp. 8-10, 15-16 and Table 1). The first
run's script, output and this protocol as it then stood are kept unchanged in `superseded-first-run/`. The text above
is unchanged apart from the two bracketed notes. No seed, specification or tolerance of the protocol was changed.

1. **Working-paper linearisation point (A2).** The paper linearises around `Δd = g` and
   `δ = log(exp(r - g) - 1)`, with `ρ = exp(-(r - g))`, and takes "the log of one plus the sample average real return
   on stocks, less the sample average change in log dividends" (p. 5). The first run used the mean log return (and
   CRSP returns from 1926), giving ρ 0.9498 (1872-1986) and 0.9501 (1872-2025). With `r = log(1 + mean R)` of the
   Index-and-D12 return the values are 0.9348 and 0.9364; the gap is mostly the Jensen term `log(1 + mean R) - mean
   log(1 + R)`. Timing: the paper's `R_t = (P_{t+1} - P_t + D_t)/P_t` with `δ_t = d_{t-1} - p_t` dates prices at the
   start of the period; with Goyal's end-of-year `Index` and trailing `D12` the same return is
   `(Index_t + D12_t)/Index_{t-1}`, and `δ_t` is the end-of-year dividend yield, so the conventions agree. The paper
   uses real (PPI-deflated, 1871-1986) data; the extracted columns contain no deflator, so the rows here are a nominal
   illustration, not a reproduction of Table 1a. For a given expansion point the remainder is the same in real and
   nominal data (inflation cancels from `r - Δd`), but the variance of `r` and the working-paper point itself differ.
2. **One coherent return for the identity (A1-A4).** Part A now uses `R_t = (Index_t + D12_t)/Index_{t-1} - 1` in
   every year. A1 is checked over 1872-2025 (1.9e-15). The CRSP log return less this return, 1926-2025, is reported
   separately: mean +0.00002, standard deviation 0.0103, largest 0.0675 (1931). A2 now checks that the approximation
   error is exactly the Taylor remainder `log(1 + e^{pd}) - [log(1 + e^{pd-bar}) + ρ (pd - pd-bar)]`, non-negative by
   convexity and at most `(pd - pd-bar)^2 / 8` (since the second derivative is `ρ(1 - ρ) <= 1/4`), to 1e-12, at both
   points. Variance ratios of the pure remainder: 0.00021 (1872-1986) and 0.00077 (1872-2025) at the mean-pd point,
   the protocol's gated point (gate unchanged, passes); 0.00089 and 0.00728 at the corrected working-paper point
   (reported only; the second is above the 0.005 gate, which never applied to that point). The first run's 0.0023 and
   0.0025 were mostly the CRSP mismatch: with CRSP returns from 1926 the same calculation gives 0.00229 and 0.00248.
   A3 is exact as before. A4, 1927-2004: `b_r` 0.066 (was 0.064), `b_d` -0.067, `φ` 0.896, `b_ε` -0.0029 (was
   -0.0052), long-run shares 0.49 and 0.49; 1872-2025: `b_r` 0.024, `b_ε` -0.0032, shares 0.21 and 0.76. The slope of
   CRSP log returns is reported beside `b_r`. Parts B and C keep their own return definitions (CRSP from 1926, as Welch
   and Goyal and Campbell and Thompson use), and their output is unchanged.
3. **Clark-West size (B3).** The comparison with Table 1 now counts the simulation error of both runs (5,000
   replications each, p. 15): 0.069 against 0.085 is -0.016 with a standard error of 0.0053 (-3.0), and 0.059 against
   0.070 is -0.011 with 0.0049 (-2.3). The gates are unchanged and still pass. The first record's "simulation error
   about 0.004" counted one side only.
4. **Bounded investigation (B3b, reported only, seed 20261104 chosen for it).** Before the recorded run, exploratory
   runs in the session (other seeds, 5,000 or 50,000 replications, not recorded in the script) gave recursive sizes of
   0.070-0.081 (P = 120) and 0.059-0.066 (P = 240); with 50,000 replications of the protocol's design, 0.0727 and
   0.0642. B3b follows the source's design (p. 15): one path of R + 720 observations shared by every P; the first
   observation drawn from the stationary distribution (the protocol's draw of the lagged z gives the same joint law);
   no observed lag for `y_1`, so the regression starts at observation 2; recursive and rolling schemes; 20,000
   replications; the ordinary t statistic. Recursive: 0.0722, 0.0657, 0.0551 for P = 120, 240, 720 against 0.085,
   0.070, 0.054 (-2.9, -1.1 and +0.3 standard errors). Rolling: 0.0722, 0.0730, 0.0856 against 0.085, 0.078, 0.091
   (-3.0, -1.2, -1.2). The means Clark and West quote for rolling, R = 120, P = 720 (p. 16: MSPE difference -0.24,
   adjusted 0.01, squared forecast difference 0.25) come out at -0.247, +0.005 and 0.252, so the DGP and the statistic
   agree with theirs. In exploratory runs on common random numbers, starting the regression at observation 1 or 2
   moved the sizes by at most 0.0003 (20,000 replications), and dividing the variance of `f` by P instead of P - 1 by
   at most 0.0004 (5,000 replications). **Unresolved:** the recomputed sizes at P = 120 are about 0.013 below Table 1 in both schemes (about three
   standard errors); at P = 240 and 720 they agree within about one. Not identified, and not tested: the authors'
   random-number generator and code, and any detail of the t statistic not stated in the paper.
5. **Recorded values.** The part A drift check was replaced by the corrected values (its label keeps the old ones);
   drift checks for A4 and B3b were added, with hand checks A0 (the working-paper point on three declared returns,
   and the steady state in which both points agree). Final: 47 checks pass.
