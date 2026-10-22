---
key: wide-gneiting-raftery
pathways: [return-predictability]
version: Tilmann Gneiting and Adrian E. Raftery, "Strictly Proper Scoring Rules, Prediction, and Estimation", Journal of the American Statistical Association 102(477), March 2007, 359-378. Copy used: author-hosted PDF of the journal's typeset article (sites.stat.washington.edu/people/raftery/Research/PDF/Gneiting2007jasa.pdf, 20 pages, SHA-256 d31a0c5f...7ba2), retrieved 2026-10-22; PDF page = printed page - 358
sections: abstract and sec. 1 (pp. 359-360); sec. 2.1 (p. 360); sec. 4.1-4.2 (pp. 365-367); sec. 6 (pp. 370-371); sec. 8.2 (p. 374)
read:
status: draft
---

Prepared on 2026-10-22 by the forecast-combination and proper-scoring batch from source checks, not from study: the headings that need your own reading are left empty. Used for `meth:proper-scoring-rules`.

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- Orientation: scores are positively oriented rewards S(P, x) that the forecaster wishes to maximise (p. 359). Proper: S(Q, Q) >= S(P, Q) for all P, Q; strictly proper if equality only for P = Q (eq. (1), p. 360).
- Logarithmic score LogS(p, x) = log p(x) (eq. (19), p. 365): strictly proper relative to densities; expected score is negative Shannon entropy and the divergence is Kullback-Leibler. Every proper local score is equivalent to it; the linear score p(x) is improper and encourages overprediction at the mode (p. 366).
- CRPS (eq. (20)) = -integral of (F(y) - 1{y >= x})^2; kernel form (21) = (1/2) E|X - X'| - E|X - x|; Gaussian closed form; strictly proper for finite first moment; in negative orientation in the units of the observation and equal to the absolute error for a point forecast (p. 367).
- Energy score with beta = 2 reduces to the negative squared error of the mean, proper but not strictly proper (eq. (23), p. 367).
- Quantile scores (40)-(42); (41) is the tick or check loss in negative orientation; interval score (43), negatively oriented, (u - l) + (2/alpha)(l - x)1{x < l} + (2/alpha)(x - u)1{x > u} (p. 370).
- Bilinear process (44), intervals I, J, K (45)-(47), Table 2 (p. 371): coverage 95.01, 95.08, 94.98; width 4.00, 5.45, 3.79; interval score 4.77, 8.04, 5.32 over 100,000 forecasts. K is sharpest but the conditional interval I scores best.
- Weather case study: log score "highly sensitive to extreme cases"; CRPS less so (p. 374).

## Limits

Secs. 3, 5, 7 and 9 (categorical rules, kernel scores, Bayes factors and cross-validation, optimum score estimation) were not used. Burn-in, seed and J's unconditional quantiles are not stated for Table 2; the recomputation estimates the quantiles by simulation.
