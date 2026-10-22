---
key: probability-statistics-random-processes
pathways: [probability-statistics, bayesian-inference]
version: Hossein Pishro-Nik, Introduction to Probability, Statistics, and Random Processes, Kappa Research; online edition at probabilitycourse.com read through fetched renderings on 2026-10-18 (edition not stated on the pages)
sections: 1.4.3 Bayes' Rule; 7.1.2 Central Limit Theorem; 8.3.3 Confidence Intervals for Normal Samples; 8.4.3 Hypothesis Testing for the Mean; 8.4.4 P-Values (inference and simulation slice); 5.1.5 Conditional Expectation (Revisited) and Conditional Variance; 5.3.1 Covariance and Correlation; 8.2.2 Point Estimators for Mean and Variance
read:
status: draft
---

Prepared on 2026-10-18 by the statistics slice from source checks, not from study: the headings that need your own reading are left empty. Searched for after the free edition of Blitzstein and Hwang proved non-downloadable. Used for `def:return-sample-statistics`, `def:return-dependence`, `def:conditional-moments` and `meth:bayesian-updating`.

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- 1.4.3: Bayes' rule with the law of total probability in the denominator; the rare-condition test example (posterior about 0.0049).
- 5.1.5: discrete conditional expectation and variance; E[X] = E[E[X|Y]]; Var(X) = E[Var(X|Y)] + Var(E[X|Y]); Example 5.11 verifies both on a 2 x 2 table.
- 5.3.1: Cov = E[XY] - EX EY; correlation in [-1, 1]; independence implies zero covariance, not conversely (uniform point in the unit disc); correlation invariant to positive affine maps; variance of a sum.
- 5.3.1, reread 2026-10-18 (portfolio moments slice, fetched rendering; the direct download was refused with HTTP 406): Lemma 5.3, item 7, Cov(sum_i a_i X_i, sum_j b_j Y_j) = sum_i sum_j a_i b_j Cov(X_i, Y_j); eq. (5.21), Var(aX + bY) = a^2 Var X + b^2 Var Y + 2ab Cov(X, Y). Used for `meth:portfolio-return-moments` (covariance of two portfolios).
- 8.2.2: the 1/n variance estimator has bias -sigma^2/n; S^2 with n - 1 is unbiased; S is biased for sigma.

- 7.1.2: CLT for i.i.d. variables with finite mean and positive finite variance; a limit, with n >= 30 a rule of thumb.
- 8.3.3: T = (Xbar - mu)/(S/sqrt n) ~ t(n - 1) and (n - 1)S^2/sigma^2 ~ chi-square(n - 1) for normal samples, any n; the t and chi-square intervals.
- 8.4.3: one- and two-sided hypotheses; Type I (alpha) and Type II (beta(mu)) errors; z and t tests, exact for normal data, approximate for large non-normal samples; two-sided test equivalent to the interval.
- 8.4.4: p-value as the lowest alpha that rejects; 60 heads in 100, p about 0.023.
- 8.2.2 reread (correction): the unbiasedness of S^2 uses a random sample (i.i.d.).

## Limits

The author and title are inferred from the site's links, not stated on each page. The law of total covariance used in the entry is derived, not quoted.
