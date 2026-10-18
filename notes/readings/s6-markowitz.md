---
key: s6-markowitz
pathways: [portfolio-construction, portfolio-construction-risk]
version: Harry Markowitz, "Portfolio Selection", The Journal of Finance 7(1), March 1952, pp. 77-91; the catalogue's link (finance.martinsewell.com/capm/Markowitz1952.pdf), a 16-page scanned image PDF without a text layer, retrieved 2026-10-18 (SHA-256 0af6b760bbb18cc5543c17a9c3449fa69feeda270748507f490310544650e473; PDF page = printed page - 76); not stored in the repository
sections: pp. 77-81 read as rendered page images in the portfolio moments and diversification slice (2026-10-18); p. 77 had been cited earlier from another reading, see mod:mean-variance-portfolio-optimisation
read:
status: draft
---

Prepared on 2026-10-18 by the portfolio moments and diversification slice from source checks, not from study: the headings that need your own reading are left empty. Used for `meth:portfolio-return-moments` and `mech:diversification-correlation`.

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- p. 78: the discounted-return rule never implies diversification; with X_i >= 0 and sum X_i = 1 the portfolio return is a weighted average of the securities' returns; n. 4, with short sales an infinite amount would go to the security with the highest r.
- p. 79: the law of large numbers cannot make a portfolio's actual yield almost the expected yield: "The returns from securities are too intercorrelated. Diversification cannot eliminate all variance." Limitations stated: static probability beliefs; results presented geometrically for 3 and 4 securities.
- p. 80: E = sum p_i y_i; V = sum p_i (y_i - E)^2; sigma = sqrt(V); coefficient of variation sigma/E; the expected value of a weighted sum is the weighted sum of expected values; covariance sigma_ij = E{[R_i - E(R_i)][R_j - E(R_j)]} = rho_ij sigma_i sigma_j.
- p. 81: variance of a weighted sum; R = sum R_i X_i with X_i "the percentage of the investor's assets which are allocated to the i-th security", fixed by the investor, sum X_i = 1, X_i >= 0 (short sales excluded); E = sum X_i mu_i and V = sum_i sum_j sigma_ij X_i X_j. n. 7: probability beliefs are the investor's, possibly subjective; the paper does not consider how beliefs are formed.

## Limits

Printing slips on p. 81 as scanned: the first double sum's inner index reads "i>1" where j>i is meant, and the final V formula prints "X_i X" without the subscript j. The entries use the intended forms. The paper has no estimation from data and no denominators; those come from the descriptive-statistics entries. Pages 82-91 (geometry of efficient sets) were not read in this slice.
