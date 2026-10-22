---
key: linear-regression-lectures
pathways: [regression-time-series]
version: Marco Taboga, Lectures on probability theory and mathematical statistics, online edition (statlect.com), lectures "Normal linear regression model", "Linear regression - Hypothesis testing" and "Gauss Markov theorem"; live pages read 2026-10-18 (HTML text, with the assumption formulas of the Gauss Markov lecture read from its equation-image sprite)
sections: Normal linear regression model - Setting, Assumptions, Distribution of the OLS estimator, Estimation of the variance of the error terms; Linear regression - Hypothesis testing - Normal vs non-normal model, Tests of hypothesis in the normal linear regression model (t test; F test), Tests of hypothesis when the OLS estimator is asymptotically normal (z test; Chi-square test); Gauss Markov theorem - Assumptions, OLS is linear and unbiased, The covariance matrix of the OLS estimator; Gamma distribution - Caveat, Definition (parameterisation only, read 2026-10-18 in the second correction pass)
read:
status: draft
---

Prepared on 2026-10-18 by the regression correction pass from source checks, not from study: the headings that need your own reading are left empty. Used for `meth:simple-regression-estimation` and `meth:regression-diagnostics-anova`.

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- OLS minimises the sum of squared residuals and, "if the design matrix X has full rank", has the closed form (X'X)^-1 X'y (Normal linear regression model, Setting). No distributional assumption enters the definition.
- Gauss Markov assumptions: X full rank, E[eps|X] = 0, Var[eps|X] = sigma^2 I (formulas read from the page images); under them OLS is linear, unbiased conditionally and unconditionally, and BLUE, with conditional covariance sigma^2 (X'X)^-1. Normality is not among these assumptions.
- Normal linear regression model: adds conditional multivariate normality of the errors; then OLS is conditionally normal, the adjusted residual variance (N-K divisor) is unbiased, has a Gamma distribution with parameters N-K and sigma^2, and is independent of the OLS estimator. These are StatLect's degrees-of-freedom and mean parameters ("Gamma distribution" lecture, Caveat and Definition, read 2026-10-18: parameters n, degrees of freedom, and h, the mean), not shape and scale: the statement says E[s^2] = sigma^2 and (N-K) s^2 / sigma^2 is chi-square with N-K d.f. In shape/scale form the same law is Gamma(shape (N-K)/2, scale 2 sigma^2/(N-K)) (conversion derived here, not quoted).
- Hypothesis testing: in the normal model the t statistic for beta_k = q (any q) has a Student's t distribution with N-K d.f.; the F statistic for R beta = q has an F distribution with L and N-K d.f. When normality holds only asymptotically, the z and Chi-square tests are large-sample versions.

## Limits

Most formulas are images; the prose and the Gauss Markov assumption images were read, other formula images were not individually transcribed. The lectures do not state that a single-restriction F equals the squared t for the same q; that step is algebra in the entry. Consistency without normality is taken from Duan (1983, p. 606), not these lectures.
