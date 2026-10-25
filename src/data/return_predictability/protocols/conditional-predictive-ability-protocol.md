# Conditional predictive ability checks: protocol

Written 2026-10-22, before `conditional-predictive-ability-checks.py` existed and before any statistic below had been
computed. When it was written, both sources had been read, including the published simulation tables quoted below
(Giacomini and White's Table 1; Zhu and Timmermann's Tables 1 and 2). The annual data file had been used by the
previous batch; no rolling-window forecast or loss difference of it had been computed. The protocol is fixed in
advance within the session; it is not blind to the published numbers and is not a preregistration. It serves
`meth:conditional-predictive-ability`. The protocols, data, scripts and results of the two earlier batches in this
folder are unchanged.

## Sources and versions

- `giacomini-white-2006-wp`: R. Giacomini and H. White, "Tests of conditional predictive ability", authors' version
  "This version: April 2006" (post-referee: the acknowledgement thanks the Editor and three referees), 31 PDF pages,
  `GiacominiWhite04.pdf` from Giacomini's former UCLA page, retrieved from the Wayback Machine capture of 2006-09-20,
  SHA-256 `2d937c5c…f15a7`; printed page = PDF page. The published article (Econometrica 74(6), 2006, 1545–1578,
  catalogue `wide-giacomini-white`) could not be obtained: Wiley returned HTTP 403 on 2026-10-22 and Unpaywall and
  Semantic Scholar list only the 2003 Boston College working paper as an open copy. Nothing below is attributed to the
  journal's pages or numbering. The preprint's text refers to "Theorems 5 and 6" for tests numbered Theorems 1–4 in
  the same copy; locators use the copy's own numbering.
- `zhu-timmermann-2022-arxiv`: Y. Zhu and A. Timmermann, "Can Two Forecasts Have the Same Conditional Expected
  Accuracy?", arXiv:2006.03238v2 (submitted 19 August 2022; title page dated 22 August 2022), 30 PDF pages, SHA-256
  `afed6367…4cea`; printed page = PDF page. Version 1 (5 June 2020, SHA-256 `4f4b6627…846c`) was downloaded and its
  abstract and section list compared only: it claimed that the null "cannot be valid under a rolling window
  estimation scheme"; version 2 replaces this with a necessary and sufficient condition and constructive examples.
  Only version 2 is cited.

## Notation and definitions (fixed now)

`ΔL_{t+1} = L(y_{t+1}, f_{1,t}) − L(y_{t+1}, f_{2,t})`, forecasts made at origin t. Test function (instrument)
`h_t`, q × 1, known at t. `Z_{t+1} = h_t ΔL_{t+1}`, `Z̄ = n^{-1} Σ Z_{t+1}`.

- **One-step conditional statistic** (GW eq. (4), p. 9): `T = n Z̄' Ω̂^{-1} Z̄`, `Ω̂ = n^{-1} Σ Z_{t+1} Z_{t+1}'`
  (uncentred). Reject at level α when `T > χ²_{q,1−α}`; degrees of freedom q = number of linearly independent
  instruments.
- **τ-step conditional statistic** (GW eq. (6), p. 11): Ω̃ adds autocovariances at lags 1..τ − 1 with weights 1.
- **Unconditional statistics** (G_t trivial, h_t = 1): (a) the same T with q = 1, which equals `GW_T²` of ZT eq. (4)
  and uses the mds variance; (b) Diebold–Mariano type t with a HAC variance (GW eq. (8), p. 12); (c) the subsample t of
  ZT eq. (13), p. 14, with K blocks against Student t_{K−1}. HAC and Newey–West variances are computed from
  demeaned ΔL, as is usual for the Diebold–Mariano statistic; GW eq. (8) writes them uncentred, and under the null
  both are consistent. Every rejection is two-sided for t statistics and upper-tail for χ² statistics.
- **Standard errors of pooled simulation means** are the standard deviation of the R per-sample means divided by √R,
  so serial dependence within a sample is accounted for.
- **Singular instruments.** The implementation computes the singular values of the n × q matrix of Z / √n. If the
  smallest is below `1e-10 × max(n, q) × largest`, it raises an error naming the rank; it never silently uses a
  generalised inverse. The remedy is to drop the redundant instrument and report the reduced q.

## Part V: validation of the statistic (deterministic, plus one seeded random check)

Gated:

- V1. Hand example, n = 6, h_t = (1, a_t) with integer data fixed in the script: T by exact rational arithmetic
  (`fractions.Fraction`, 2 × 2 inverse by cofactors), by `numpy.linalg.solve`, and as n·R² of the uncentred regression
  of a vector of ones on Z' (GW comment 7, p. 10) via `numpy.linalg.lstsq`; all agree to 1e-12.
- V2. Random data (seed 20261109), n = 500, q = 3: solve route and n·R² route agree to 1e-10.
- V3. q = 1, h = 1: T equals `(Σ ΔL)² / Σ ΔL²`, the square of ZT eq. (4), to 1e-12.
- V4. χ²₂ upper tail equals `exp(−x/2)` (closed form) at x = 1, 4, 5.991, 10 to 1e-14; the 5 percent critical values
  are 3.841 (q = 1) and 5.991 (q = 2) at three decimals.
- V5. Singular instruments: (a) a duplicated column (q = 3, rank 2) and (b) h = (1, 2) raise the error; (c) the
  Moore–Penrose statistic with the duplicated column equals the statistic with the column dropped, to 1e-10, so the
  generalised inverse gives a χ² with rank, not q, degrees of freedom.
- V6. Ω̃ with τ = 2 and unit weights equals a hand double loop to 1e-12; with τ = 1 it equals Ω̂.
- V7. Scalar long-run variance with uniform weights at lags 1..L equals Ω̃ with τ = L + 1 and h = 1; Newey–West
  (Bartlett) equals a hand loop; the subsample t on a 12-value example equals a hand calculation; all to 1e-12.

## Part H: same average accuracy, different conditional accuracy (DGP simulation)

Design (Interpretation, built for this entry). State `S_t ∈ {0, 1}` i.i.d. with probability 1/2, observed at t.
`y_{t+1} = +1 + ε` if `S_t = 1`, `−1 + ε` if `S_t = 0`, ε ~ N(0, 1). Method A forecasts +1 and method B −1 at every
origin (no estimation). Squared loss.

Derived now: `E[L_A | S=1] = 1`, `E[L_A | S=0] = 5`, B the mirror image; `E[ΔL | S=1] = −4`, `E[ΔL | S=0] = +4`,
`E ΔL = 0`. Here `ΔL_{t+1} = −4 y_{t+1}`, which is i.i.d., so the unconditional null holds and the mds variance is
valid for it; the conditional null fails because `E[y_{t+1} | F_t] ≠ (f_A + f_B)/2 = 0` (ZT Proposition 1).

Simulation: R = 10,000 samples of n = 120, seed 20261110. Tests at 5 percent: unconditional T (h = 1, χ²₁) and
conditional T with h = (1, S_t) (χ²₂). Gated: the four conditional expectations exactly (Fractions); pooled
`E[ΔL | S]` within 3 standard errors of ∓4; unconditional rejection rate in [0.035, 0.070]; conditional rejection rate
≥ 0.99. Monte Carlo standard errors `√(p(1 − p)/R)` reported.

## Part N: a design in which the conditional null holds by construction (DGP simulation)

Design (after ZT Example 2, p. 6). Two signals `x_{i,t} = 0.9 x_{i,t−1} + u_{i,t}`, u ~ N(0, 1), independent,
burn-in 200. Each method forecasts with the m = 12 period moving average of its own signal,
`f_{i,t} = (1/12) Σ_{s=0}^{11} x_{i,t−s}` (a fixed rolling window). The outcome is
`y_{t+1} = (f_{1,t} + f_{2,t})/2 + ε_{t+1}`, ε ~ N(0, 1) i.i.d.

Derived now: `ΔL_{t+1} = 2 ε_{t+1} (f_{2,t} − f_{1,t})`, so `E[ΔL_{t+1} | F_t] = 0` and {ΔL} is an mds. The null
holds because the DGP's conditional mean is defined as the average of the two forecasts; it is a construction, not a
property of two misspecified methods in general (ZT Proposition 1).

Simulation: R = 10,000, n ∈ {120, 1000}, seed 20261111. Instruments (i) h = (1, ΔL_t), the choice in GW's application
(p. 19), first usable origin one period later; (ii) h = (1, f_{1,t} − f_{2,t}). One-step mds covariance, χ²₂.
Gated: pooled sample means of both components of Z for (i) within 3 standard errors of 0 at n = 1000; rejection rate
of (i) at n = 1000 within 0.015 of 0.05. Reported: all other rates with Monte Carlo standard errors.

## Part U: the unconditional null holds, the conditional null fails (DGP simulation)

Design: ZT Example 4 (p. 13) with Gaussian errors. `y_{t+1} = c + ε_{t+1}`, ε ~ N(0, 1) i.i.d.; method 1 forecasts
with the mean of the last m = 4 outcomes, method 2 forecasts 0; c = m^{-1/2} = 1/2.

Derived now (Interpretation; v_t = f_{1,t} − c ~ N(0, 1/m)): `E ΔL = 1/m − c² = 0`;
`E[ΔL_{t+1} | F_t] = v_t² − c²`, not zero, so the conditional null fails; `E ΔL² = 8/m + 2/m² = 2.125`;
`E[f_1 ΔL] = c(1/m − c²) = 0`; `E[f_1² ΔL] = 2/m² = 0.125`. ΔL_{t+1} depends on ε_{t−m+1}, …, ε_{t+1}, so it is
m-dependent: autocorrelation is possible at lags 1..m and zero beyond.

Simulation: R = 10,000, n ∈ {120, 1000}, seed 20261112. Tests at 5 percent:

- U-a the mds-variance unconditional statistic (h = 1); reported, with the sample variance of the signed statistic
  `GW_T` compared with ZT Proposition 6's `V_m = (4m² − 4m^{3/2}κ₁ + m(κ₂ + 3))/(8m² + κ₂ − 1)` at κ₁ = 0, κ₂ = 3,
  that is 88/130 = 0.677 (reported only);
- U-b HAC with uniform weights at lags 1..m (the dependence order derived above); if the estimate is not positive,
  Bartlett weights at the same lag are used and the count reported;
- U-c Newey–West (Bartlett) with lag ⌊0.75 n^{1/3}⌋ (ZT n. 10); reported;
- U-d subsample t, K = 4 blocks, t₃ critical value;
- U-e conditional statistic with h = (1, f_{1,t}) and with h = (1, f_{1,t}²), χ²₂; reported.

Gated: pooled mean of ΔL within 3 standard errors of 0; pooled mean of ΔL² within 3 standard errors of 2.125; pooled
means of f_1 ΔL and f_1² ΔL within 3 standard errors of 0 and 0.125; rejection rates of U-b and U-d at n = 1000 within
0.02 of 0.05.

## Part C: equal population models, unequal forecasting methods (DGP simulation)

Design: `y_{t+1} = 0.5 + ε_{t+1}`, ε ~ N(0, 1); predictor `x_t = 0.9 x_{t−1} + u_t`, u ~ N(0, 1), independent of ε
(true slope zero). Method M: mean of the last m = 20 outcomes. Method D: OLS of y_{s+1} on (1, x_s) over the last 20
pairs, evaluated at x_t. Both population models give E[y | F] = 0.5, so the null of equal model accuracy at
population parameters (GW eq. (1)) holds.

Derived now (Interpretation): with `ȳ` the window mean, `b̂` the window slope and `d_t = x_t − x̄`,
`ΔL = L_M − L_D` has `E[ΔL | F_t] = 2(0.5 − ȳ) b̂ d_t − b̂² d_t²` and `E ΔL = −E[b̂² d_t²] < 0`, because
`E[(0.5 − ȳ) b̂ d_t] = 0` when x is independent of ε. So the method null fails unconditionally, in favour of M.

Simulation: R = 2,000, n = 1000, seed 20261113. Gated: pooled mean of ΔL negative by more than 3 standard errors;
pooled mean of `2(0.5 − ȳ) b̂ d_t` within 3 standard errors of 0. Reported: rejection rates of the conditional test
with h = (1, ΔL_t) and of the subsample t (K = 4).

## Part X: an expanding window (DGP simulation)

Design: ZT Example 5 (p. 16): y_t = ε_t i.i.d. N(0, 1); method 1 forecasts with the expanding mean of all outcomes
through t, method 2 with `t^{-1/2}`; first origin m = λT. Under squared loss E ΔL = 0 but E[ΔL | F_t] ≠ 0.
Statistic: GW_T of ZT eq. (4) (h = 1, mds variance) against ±1.96.

Simulation: T = 2000, λ ∈ {0.25, 0.5}, R = 10,000, seed 20261114. Gated: both rejection rates exceed 0.10. Reported
against ZT Table 2 (p. 18; asymptotic sizes 0.196 and 0.158).

## Part E: empirical illustration with a fixed rolling window (existing data)

Data: `goyal-annual-predictors-1871-2025.csv` (unchanged; extracted in the previous batch from Goyal's workbook,
SHA-256 `8d210b77…be872`, a 2026 vintage running to 2025). Outcome `y_t = log(1 + CRSP_SPvw_t) − log(1 + Rfree_t)`,
predictor `dp_{t−1} = log D12 − log Index` dated t − 1, outcomes from 1927, exactly as in parts F of the previous
batch. Predictor years are calendar-indexed; publication lags and data revisions are not modelled, so the exercise
does not establish point-in-time availability or a real-time investable backtest.

Fixed now, before any result:

- **Window.** m = 20 years, rolling and fixed. The forecast for year t uses outcomes t − 20, …, t − 1 and predictor
  values dated t − 21, …, t − 2, then dp dated t − 1. m = 20 is the size of the first estimation sample of the earlier
  recursive experiments, so the 1947 forecasts coincide with theirs; no other window is run.
- **Methods.** M: the window mean. D: window OLS of y on (1, dp lagged).
- **Evaluation.** Forecasts 1947–2025 (n = 79); second window 1947–2005 (n = 59). No other sample is run.
- **Losses.** Squared error. CRPS of a Gaussian predictive density N(f, s²), with s² the window sample variance
  (ddof 1) for M and the residual variance (ddof 2) for D; the Gaussian form is an assumption. ΔL = L_M − L_D, so a
  positive mean favours D.
- **Tests.** Unconditional: Diebold–Mariano t with Newey–West (Bartlett) lag ⌊0.75 n^{1/3}⌋ (3 and 2), two-sided normal
  p-value; the mds-variance version is also reported. Conditional: h = (1, ΔL_t), one-step mds covariance, χ²₂,
  evaluated from 1948 (n = 78 and 58). Reported: R2_OS of D against M, means of ΔL, statistics and p-values. No result
  is required to be significant, and no other instrument, window, predictor or loss is tried.

Gated (correctness only): E1 rolling OLS in closed form equals `lstsq` per window to 1e-10; E2 overwriting all rows
after t (t = 1970, 2000) leaves every forecast through t + 1 unchanged; E3 the 1947 forecasts equal the earlier
recursive ones from the same 20 observations to 1e-12; E4 the Gaussian CRPS closed form equals quadrature for the
first forecast to 1e-7; E5 Ω̂ passes the rank check.

## General rules

No specification, seed, sample or tolerance is changed to obtain a significant result or to match a published
number. Monte Carlo standard errors are reported with every simulated rate. After the first run, observed values are
added as recorded-value checks at their printed rounding. Any change to this protocol after the first run is
recorded below with its reason.

## Changes after the first run

First run, 2026-10-22 (script SHA-256 `e6ad1125…ed21`; output kept unchanged as
`conditional-predictive-ability-first-run.txt`): 41 checks, 39 passed. Before it, two coding slips were corrected
without any statistic having been computed: the rank message for stacked matrices, and a window-sum helper. Every
gated check in V, H, N, U, C and E passed. **Both gates of part X failed**: the rejection rates of GW_T against
1.96 were 0.0567 (λ = 0.25) and 0.0538 (λ = 0.5), mc se 0.0023, not above 0.10. ZT Table 2 gives 0.196 and 0.158.

1. **Part X, investigation.** The design follows Example 5 as printed (p. 17). Writing
   `ΔL = (f₁² − f₂²) + 2y(f₂ − f₁)` gives the limit `A/(2√I) + N/√I`, with A, I and N the integrals of eq. (14). Eq.
   (14) prints the second term with a minus sign, and the two terms are correlated, so the sign matters. A grid
   simulation of both (part P2, seed 20261115; post-run, not part of a verdict) gives 0.054 and 0.053 for the derived
   form, agreeing with the T = 2000 simulation within Monte Carlo error. The printed form gives 0.149 and 0.117,
   still below Table 2. Our conclusion: for Example 5 as stated, the distortion of the mds-variance statistic is
   small, and Table 2 is not reproduced; we cannot tell whether the table reflects a different design. The gate is
   not loosened. It now prints as a failed reproduction, and the observed rates are recorded values.
2. **Part U, post-run derivation (P1).** U-a's variance of the signed statistic, 0.755 (se 0.011), is not ZT
   Proposition 6's 0.677 at κ₁ = 0, κ₂ = 3. With Gaussian errors the autocovariances of ΔL are
   `γ₀ = 2/m² + 8/m` and `γ_k = 2(m − k)²/m⁴ − 4(m − k)/m³` for 1 ≤ k ≤ m − 1, zero beyond, so the exact ratio is
   `V_m = (2m + 1)/(3m)`: 3/4 at m = 4, 1 at m = 1 (where Proposition 6 agrees) and 2/3 as m grows, not 1/2. It
   implies a rejection rate of 0.0236 against the simulated 0.0237. The direction of Proposition 6's conclusion for
   Gaussian errors, an undersized mds-variance test, is confirmed; its formula is not. Skewed errors (ZT's Table 1)
   were not simulated.
3. **Recorded values (part R).** The observed numbers of V1, H, N, U, C, X and E are asserted at their printed
   rounding to detect drift. No tolerance, seed, design, window or instrument was changed. Final: 52 checks.

Outcome, reported and not gated. **H:** with equal average losses the unconditional test rejects 5.2 percent of the
time, the conditional test with h = (1, S) always. **N:** with the null true by construction, the conditional test
rejects 4.7 percent (h = (1, ΔL_t)) and 5.1 percent (h = (1, f₁ − f₂)) at n = 1000, 4.2 and 4.4 percent at n = 120.
**U:** at n = 1000 the mds-variance unconditional test rejects 2.4 percent, uniform HAC at lag m 5.5, Newey–West
4.4 and the subsample t 4.6. At n = 120 the uniform HAC rejects 9.3 percent, in 34 samples with a non-positive
variance (Bartlett used). With h = (1, f₁) the conditional test rejects 4.4 percent although the conditional null is
false, since `E[f₁ ΔL] = 0`; with h = (1, f₁²) it rejects 78.8 percent. **C:** the mean of `L_M − L_D` is −0.097
(se 0.0004), and both tests reject in more than 98 percent of samples, in favour of the rolling mean. **E:** see
the results file. Over 1947–2025 the rolling regression on dp has R2_OS 3.40 percent against the rolling mean, but
no unconditional or conditional p-value is below 0.2 for either loss.

## Amendment, 23 October 2026 (correction and final-validation pass)

Appended after the first run and after the changes above; nothing above this heading is altered. No seed, threshold,
design, window, instrument or observation was changed, and the first-run output
(`conditional-predictive-ability-first-run.txt`, SHA-256 `c46e1ba7…9235`) is unchanged.

1. **Verdict accounting.** The first run executed 41 checks; 39 passed, and the two part X gates ("rejection
   exceeds 0.10", expecting ZT Table 2) failed. That verdict stands: under this protocol's criteria, ZT Table 2 was not
   reproduced. The script previously printed those gates as text and then reported "52 checks, 0 failed", which read
   as though every protocol criterion had been met. It now reports two separate tallies: (a) *correctness and
   regression checks*, 53 run and 0 failed: the protocol's 39 gated checks in parts V–E, 6 post-run supplements (P) and
   8 recorded values (R); (b) *historical reproduction gates*, the two part X gates with their original criterion
   and threshold, evaluated every run, not counted in (a), and both NOT MET (0.0567 and 0.0538). Tally (a) measures
   whether the code is correct and its outputs stable; it says nothing about agreement with ZT Table 2.
2. **One check added to part P1.** It runs ZT's printed proof steps for Proposition 6 (eqs. (22)–(28), pp. 24–26) in
   exact arithmetic at m = 4, κ₁ = 0, κ₂ = 3. The printed fourth moment of a sum of k errors,
   `E ξ⁴ = k(k − 1) + k κ₂` (eq. (23), p. 25, and the step before eq. (28), p. 26), reproduces 88/130 exactly; with the
   pairing count `3k(k − 1)` the same steps give 3/4, the value derived in item 2 above. So 52 becomes 53. Every
   numerical line of the recorded output is unchanged.
3. **Eq. (14) against the proof.** ZT's proof of Proposition 8 (eq. (30), p. 28) gives
   `Σ ΔL = A − 2∫(u⁻¹B − u^{−1/2}) dB = A + 2N` and `Σ ΔL² → 4I`, so the limit is `A/(2√I) + N/√I`, the form P2
   simulates as "derived". Eq. (14) on p. 17 prints a minus sign on the second term, so it disagrees with the
   proof. The loss ordering matches the proof's eq. (29): `ΔL = (y − f₁)² − (y − f₂)²`, f₁ the expanding mean,
   f₂ = t^{−1/2}. Neither sign gives Table 2 (0.054/0.053 as in the proof, 0.149/0.117 as printed, against 0.196/0.158).
   The table remains unreproduced and unexplained.
4. **Singular instruments (clarification, no code change).** V5(b), h = (1, 2), is singular because the second
   constant duplicates the intercept: Z = hΔL has rank 1 < q = 2. A single constant h = 1 is valid (V3; part U-a and
   part X use it), since Ω̂ is then the mean of ΔL², positive unless every ΔL is zero. The entry's earlier wording,
   "or one is constant over the sample", was wrong and has been corrected.
