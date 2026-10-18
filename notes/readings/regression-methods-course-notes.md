---
key: regression-methods-course-notes
pathways: [common-toolkit]
version: Penn State Eberly College of Science, STAT 501 Regression Methods, online course notes (online.stat.psu.edu/stat501); read 2026-10-18 through Internet Archive captures dated 16 December 2025 to 12 May 2026, because the live site's TLS certificate chain could not be verified from this environment
sections: 1.2 Best fitting line; 1.3 The simple linear regression model; 1.4 Common error variance; 1.5 Coefficient of determination; 1.8 R-squared cautions; 2.1 Inference for intercept and slope; 2.3 Sums of squares; 2.6 ANOVA table and F-test; 2.7 Example (t squared equals F); 2.8 Equivalent linear relationship tests; 3.2 Confidence interval for the mean response; 3.3 Prediction interval for a new response; 4.1 Background; 4.2 Residuals vs. fits; 4.4 Identifying problems with residual plots; 4.5 Residuals vs. order; 4.6 Normal probability plot; 9.1-9.3 Log transformations
read:
status: draft
---

Prepared on 2026-10-18 by the regression slice from source checks, not from study: the headings that need your own reading are left empty. Used for `meth:simple-regression-estimation`, `meth:regression-diagnostics-anova` and `meth:regression-prediction-functional-form`.

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- Least squares minimises Q = sum of squared prediction errors; b1 = Sxy/Sxx, b0 = ybar - b1 xbar (1.2). The population line E(Y) = beta0 + beta1 x; LINE conditions (1.3, 4.1).
- MSE = SSE/(n-2) estimates sigma^2; S = sqrt(MSE) (1.4). SSTO = SSR + SSE; R^2 = SSR/SSTO; "association is not causation" (1.5). Seven R^2 cautions, including curvature with R^2 = 0, high R^2 without good fit, one influential point, causation, ecological correlation, significance without practical size, wide intervals despite high R^2 (1.8).
- Slope t test and interval on n-2 d.f. (2.1); ANOVA with MSR/MSE ~ F(1, n-2) (2.6); (t*)^2 = F*, equivalent two-sided tests, only t for one-sided alternatives (2.7); regressing in the two directions gives different equations (2.8).
- Mean-response interval and prediction interval differ by an extra MSE term; use within the scope of the model; the prediction interval depends strongly on normality (3.2-3.3).
- Tests and intervals very sensitive to dependence, sensitive to unequal variance, slope inference fairly robust to non-normality, prediction intervals quite sensitive to non-normality (4.1). Residual plots and their patterns; standardised residuals beyond +/-2 flagged, not removed; order plots only with known collection order (4.2-4.6).
- Transform x for non-linearity alone, y for non-normality or unequal variance; exponentiated log predictions are medians; factors e^b1 (log-level) and k^b1 (log-log) (9.1-9.3).

## Limits

Course notes with Minitab output, not a primary reference; read as archived renderings, so figures and some tables were not visible. No mean retransformation (smearing or lognormal correction) is given; Duan (1983) is used for that. Correction pass 2026-10-18: the notes' reading of an exponentiated log prediction as the median is approximate; exactly it is the conditional geometric mean, and the median only when the log error has median zero (Hyndman 2014 for the symmetry condition). Their (t*)^2 = F* example (2.7) is for the zero-slope null only.
