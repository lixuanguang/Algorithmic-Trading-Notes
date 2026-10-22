---
key: smearing-retransformation-1983
pathways: [regression-time-series]
version: Naihua Duan, "Smearing Estimate: A Nonparametric Retransformation Method", Journal of the American Statistical Association 78(383), September 1983, pp. 605-610 (JSTOR stable 2288126); local copy reading_materials/Smearing.pdf (git-ignored), SHA-256 7525fc608bce0cf8b0e9b6e060bbf5f3ce434b859de03f53b2c9198e36118885, text layer
sections: abstract; 1 Introduction; 2 The retransformation problem; 3 The smearing estimate (pp. 605-606); sec. 4 (p. 607), Lemma 1 and Theorem 1 with the moment condition, read 2026-10-18 in the second correction pass
read:
status: draft
---

Prepared on 2026-10-18 by the regression slice from source checks, not from study: the headings that need your own reading are left empty. Used for `meth:regression-prediction-functional-form`.

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- Retransformation bias: E Y0 = E h(x0 beta + eps) differs from h(x0 beta) for nonlinear h (sec. 2, p. 606).
- With a log transformation and normal errors, E Y0 = exp(x0 beta + sigma^2/2); the naive estimate exp(x0 b + s^2/2) is consistent for that quantity but not for E Y0 when errors are not normal: a normal mixture gives E Y0 = 2.79 exp(x0 beta) against 1.65, a 41 percent asymptotic bias (sec. 2, p. 606).
- Reread 2026-10-18 (correction pass), sec. 2, p. 606: "Whether the true error distribution is normal or not, the above estimate is consistent for exp(x0 beta + sigma^2/2); however, it might not be consistent for E Y0." Normality is therefore sufficient, not necessary, for the naive estimate to target E Y0. The same page: for the regression coefficients, least squares "is consistent and minimum variance linear unbiased" whether or not the errors are normal; non-normality "affects only the efficiency".
- Second correction pass 2026-10-18: the coefficient-consistency sentence on p. 606 is conditional: beta-hat and x0 beta-hat "are unbiased and also consistent if the design matrix is asymptotically nondegenerate"; errors are i.i.d. with mean 0 and variance sigma^2 (p. 605). Theorem 1 (sec. 4, p. 607): the smearing estimate is weakly consistent if (i) h is continuously differentiable, (ii) X contains the intercept, (iii) X'X/n tends to a positive-definite matrix, (iv) E sup_{|t|<=M} [h'(x0 beta + eps + t)]^2 is finite for all M; for the log transformation (iv) reduces to E exp(2 eps) < infinity. Duan notes (iii) is "much stronger than we need".
- Smearing estimate: replace the error distribution F by the empirical cdf of the least squares residuals, giving (1/n) sum h(x0 b + e_i), eq. (3.1); errors are assumed i.i.d. with mean zero and constant variance (secs. 2-3).

## Limits

Section 4 (consistency) was read on 2026-10-18; sections 5-6 (efficiency, the Health Insurance Study application) were not read in full; heteroscedastic retransformation is outside what was read.
