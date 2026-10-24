---
key: zhu-timmermann-2022-arxiv
pathways: [return-predictability]
version: Yinchu Zhu and Allan Timmermann, "Can Two Forecasts Have the Same Conditional Expected Accuracy?", arXiv:2006.03238v2 [stat.ME], submitted 19 August 2022 (title page dated 22 August 2022); 30 pages, SHA-256 afed6367...4cea, retrieved 2026-10-22; printed page = PDF page. Version 1 (5 June 2020, SHA-256 4f4b6627...846c) compared for its abstract and section list only
sections: secs. 1-5 (pp. 1-19); proofs of Propositions 1-2, Lemma 1 and Proposition 5 (pp. 19-21); proofs of Propositions 6 and 8 (pp. 24-28), read as page images on 2026-10-23
read:
status: draft
---

Prepared on 2026-10-22 for the conditional predictive ability entry from source checks, not from study: the headings that need your own reading are left empty. Used for `meth:conditional-predictive-ability` as a methodological qualification of `giacomini-white-2006-wp`.

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- Proposition 1 (p. 5): under squared loss, if f1 != f2 a.s., E[dL | F_t] = 0 a.s. iff E[y_{t+1} | F_t] = (f1 + f2)/2. Examples 1-2 (pp. 5-6) construct cases where it holds.
- Proposition 2 (p. 6): with forecasts measurable on the last m observations, the null fails unless the conditional mean depends only on those observations (rules out MA, ARMA, state-space, GARCH-in-mean).
- Lemma 1 (p. 8): AR(q) with estimated coefficients; the null fails if Var(beta1 + beta2 | Y_{t-q:t}) > 0 with positive probability.
- Proposition 3 (p. 8): nested models with c chosen so that average losses are equal; dL is still not an mds, for rolling and expanding windows. Proposition 4 (p. 9): the same for non-nested models.
- Sec. 3 (pp. 9-12): the null is equivalent to E[xi | F_t] = 0 for the equal-weight forecast error; the J test can have more power than the GW test for the same instrument (Proposition 5, Figure 1); inflation and GDP application.
- Sec. 4 (pp. 13-18): for the unconditional null with a rolling window, the mds variance gives N(0, V_m) (Example 4, Proposition 6, p. 14); remedies: Newey-West (Remark 1) or the subsample t with K blocks and t_{K-1} (Remark 2, eq. (13), Proposition 7); Table 1 (p. 16) sizes for lognormal-skewed errors; expanding window Example 5 and Proposition 8 (pp. 16-17), Table 2 (p. 18).

## Limits

Checked numerically for this entry (trading_notes.numerical.return_predictability.conditional_predictive_ability_checks, parts U, X and P), with two discrepancies. (1) For Example 4 with Gaussian errors (kappa1 = 0, kappa2 = 3) the autocovariances of dL give V_m = (2m + 1)/(3m), 0.75 at m = 4, confirmed by simulation (0.755); Proposition 6's formula gives 0.677 and tends to 1/2 rather than 2/3. The two agree at m = 1. (2) For Example 5, the GW statistic at T = 2000 rejects 5.7 and 5.4 percent at 1.96 (lambda = 0.25, 0.5), matching the limit derived here with a plus sign on the stochastic-integral term; eq. (14) prints a minus sign, and Table 2 gives 19.6 and 15.8 percent, which neither form reproduces (the printed form gives 14.9 and 11.7). Also noted: the proof of Proposition 5 writes Z = -2 y_t eps and E Y^2 where dL h = c T^{-1/2} y^3 - y^2 eps gives E Y^4, as in the proposition's statement. Table 1 (skewed errors) and the empirical application of sec. 3.2 were not re-computed.

### Source audit of the two discrepancies (23 October 2026)

Read as page images from the cached copy (`reading_materials/conditional-predictive-ability/src/ZhuTimmermann_arXiv2006.03238v2.pdf`, SHA-256 re-checked `afed6367...4cea`).

Proposition 6 (statement p. 14; proof pp. 24-27). With eps-bar_t the mean of the last m errors, dL_{t+1} = eps-bar_t^2 - c^2 - 2 eps_{t+1}(c + eps-bar_t), c^2 = 1/m, and the proof computes gamma_d for 1 <= d <= m - 1 (eqs. (22)-(26)), d = m (eq. (27)) and d = 0 (eq. (28)). Here kappa1 = E eps^3 and kappa2 = E eps^4 (so kappa2 = 3 for Gaussian errors).
- Eq. (23), p. 25: for xi_2, a sum of k = m - d independent errors, the proof writes E xi_2^4 = sum_{s1 != s2} E eps^2 E eps^2 + sum_s E eps^4 = k(k - 1) + k kappa2. The ordered pairs s1 != s2 can be matched to the four factors in three ways ({1,2}{3,4}, {1,3}{2,4}, {1,4}{2,3}), so E xi^4 = 3k(k - 1) + k kappa2 (3k^2 for Gaussian errors). The step before eq. (28), p. 26, has the same omission: E eps-bar^4 = m^{-3}(m - 1 + kappa2) where m^{-3}(3(m - 1) + kappa2) is correct.
- With the factor 3, eq. (23) becomes E eps-bar_{t+d}^2 eps-bar_t^2 = m^{-4}(2dm - d^2 + 3k(k - 1) + k kappa2), so E eps-bar_{t+d}^2 eps-bar_t^2 - c^4 = m^{-4}(2k^2 + k(kappa2 - 3)); eqs. (24)-(25) are unaffected. So gamma_d = m^{-4}[2(m - d)^2 + (m - d)(kappa2 - 3)] - 2c m^{-2} kappa1 - 4 m^{-3}(m - d), gamma_m = -2c m^{-2} kappa1 as printed, and gamma_0 = m^{-3}(8m^2 + 2m + kappa2 - 3).
- Gaussian case: gamma_0 = 8/m + 2/m^2, gamma_d = 2(m - d)^2/m^4 - 4(m - d)/m^3, and the long-run variance over gamma_0 is V_m = (2m + 1)/(3m): 3/4 at m = 4, tending to 2/3. The printed steps give the printed formula, 88/130 at m = 4, tending to 1/2. Both agree at m = 1, where no pairings arise.
- General iid errors (derived here; symbolic check with sympy in a scratch session, not part of the repository's checks): V_m = (16m^2 - 12 kappa1 m^{3/2} + 3m(kappa2 + 1) + 2) / (3(8m^2 + 2m + kappa2 - 3)). A scratch Monte Carlo with centred exponential errors (kappa1 = 2, kappa2 = 9, m = 4, 4 million draws) gave 0.437 against 0.437 from this form and 0.353 from Proposition 6. Exploratory only: neither the symbolic check nor this Monte Carlo is saved or rerun by the repository, so the general form is not repository-verified evidence. Not used in the entry; ZT's skewed-error Table 1 was not re-simulated, so its numbers are neither confirmed nor refuted.
- Recorded checks: trading_notes.numerical.return_predictability.conditional_predictive_ability_checks P1 (exact 3/4; simulated 0.7552, se 0.0107; implied rejection 0.0236 against 0.0237; and the printed proof steps in exact arithmetic giving 88/130 with the printed pairing count and 3/4 with the factor 3).

Proposition 8 (statement eq. (14), p. 17; proof pp. 27-28). Eq. (29) defines dL_{t+1} = (eps_{t+1} - f_{1,t})^2 - (eps_{t+1} - t^{-1/2})^2 with f_{1,t} the expanding mean, the ordering the script implements. Eq. (30), p. 28: sum dL -> int (u^{-2}B^2 - u^{-1}) du - 2 int (u^{-1}B - u^{-1/2}) dB = A + 2N, with N = int (u^{-1/2} - u^{-1}B) dB; and A_{2,T} -> 4I, I = int (u^{-1/2} - u^{-1}B)^2 du, with A_{1,T} = o_P(1). The limit of sum dL / sqrt(sum dL^2) is therefore A/(2 sqrt I) + N/sqrt I. Eq. (14) prints A/(2 sqrt I) - N/sqrt I. Because A and N are correlated, the sign matters; reversing the loss ordering would flip both terms together and leave the two-sided rate unchanged, so the ordering cannot reconcile them. The proof's form agrees with the finite-T simulation (0.0567/0.0538 at T = 2000; grid limit 0.054/0.053). The printed form gives 0.149/0.117. Table 2 (0.196/0.158, p. 18) matches neither. Not explained here: the table may come from a different design, grid or statistic, which the paper does not state.
