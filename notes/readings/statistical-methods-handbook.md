---
key: statistical-methods-handbook
pathways: [common-toolkit]
version: NIST/SEMATECH e-Handbook of Statistical Methods, National Institute of Standards and Technology (itl.nist.gov/div898/handbook), web edition; pages read through fetched renderings on 2026-10-18
sections: 1.3.3.4 Bootstrap Plot; 1.3.5.2 Confidence Limits for the Mean; 1.3.5.8 Chi-Square Test for the Variance; 1.3.5.9 F-Test for Equality of Two Variances; 1.3.5.10 Levene Test (inference and simulation slice); 1.3.5.1 Measures of Location; 1.3.5.6 Measures of Scale; 1.3.5.11 Measures of Skewness and Kurtosis; 7.2.6.2 Percentiles; 1.3.6.6.1 Normal, 1.3.6.6.2 Uniform, 1.3.6.6.4 t, 1.3.6.6.9 Lognormal, 1.3.6.6.18 Binomial distributions
read:
status: draft
---

Prepared on 2026-10-18 by the statistics slice from source checks, not from study: the headings that need your own reading are left empty. Used for `def:return-sample-statistics`, `def:return-shape-statistics` and `def:financial-distributions`; sec. 1.3.6.6.9 (lognormal median and mean) reread on 2026-10-18 for `meth:regression-prediction-functional-form`.

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- 1.3.5.1: mean, median (odd and even N), mode; the median is the better location estimate with extreme tail values.
- 1.3.5.6: variance and standard deviation with N - 1; range; average absolute deviation (N); median absolute deviation; interquartile range.
- 1.3.5.11: skewness g1 and kurtosis with s computed with N; adjusted G1 = sqrt(N(N-1))/(N-2) g1, which many programs compute; normal kurtosis 3; excess kurtosis subtracts 3; the convention must be checked in software.
- 7.2.6.2: the p(N+1) = k + d percentile rule with interpolation and clamping at the extremes; other rules (Hyndman and Fan R6, R7, R8) are in common use.
- Distributions: normal moments; t mean undefined for nu = 1, variance nu/(nu - 2) undefined for nu = 1, 2, skewness undefined for nu <= 3, kurtosis 3(nu - 2)/(nu - 4) undefined for nu <= 4; lognormal mean, mode, s.d., skewness and kurtosis for scale 1; binomial pmf and moments; uniform density, mean (A + B)/2, s.d. sqrt((B - A)^2/12), kurtosis 9/5.

- 1.3.5.2: in the long run about 95 % of such intervals contain the true mean; it does not mean a 95 % probability that this interval does.
- 1.3.5.8-1.3.5.9: chi-square test T = (N - 1)(s/sigma0)^2 on N - 1 d.f.; F = s1^2/s2^2 on (N1 - 1, N2 - 1) d.f.; neither page discusses non-normality. 1.3.5.10: Levene is less sensitive than Bartlett to departures from normality.
- 1.3.3.4: bootstrap subsamples with replacement estimate a statistic's sampling distribution; percentile intervals; not appropriate for all distributions and statistics (the range).
- 1.3.5.11 (reread for the correction): kurtosis measures heavy or light tails relative to a normal; high kurtosis tends to mean heavy tails, or outliers.

## Limits

Web renderings; equations reconstructed where garbled and checked numerically. The handbook's own variance definition uses N - 1 while its skewness and kurtosis use N; the entries state both.
