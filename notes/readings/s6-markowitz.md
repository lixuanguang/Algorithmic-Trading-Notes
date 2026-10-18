---
key: s6-markowitz
pathways: [portfolio-construction, portfolio-construction-risk]
version: Harry Markowitz, "Portfolio Selection", The Journal of Finance 7(1), March 1952, pp. 77-91; the catalogue's link (finance.martinsewell.com/capm/Markowitz1952.pdf), a 16-page scanned image PDF without a text layer, retrieved 2026-10-18 (SHA-256 0af6b760bbb18cc5543c17a9c3449fa69feeda270748507f490310544650e473). One-based PDF page 1 is a JSTOR cover sheet, so the article's printed pp. 77-91 are PDF pp. 2-16 and one-based PDF page = printed page - 75 (printed p. 81 is PDF p. 6; corrected 2026-10-18 from an earlier "- 76"). Not stored in the repository; a git-ignored local copy with the same hash is at reading_materials/derivatives-validation/src/Markowitz1952.pdf
sections: pp. 77-81 read as rendered page images in the portfolio moments and diversification slice (2026-10-18); pp. 82-91 (PDF pp. 7-16) read as page images in the portfolio choice and asset pricing batch (2026-10-18); p. 77 had been cited earlier from another reading, see mod:mean-variance-portfolio-optimisation
read:
status: draft
---

Prepared on 2026-10-18 by the portfolio moments and diversification slice from source checks, not from study: the headings that need your own reading are left empty. Used for `meth:portfolio-return-moments` and `mech:diversification-correlation`; from 2026-10-18 also for `def:asset-class-characteristics`, `def:risk-aversion-utility`, `meth:efficient-frontier` and `mod:return-generating-models`.

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- p. 78: the discounted-return rule never implies diversification; with X_i >= 0 and sum X_i = 1 the portfolio return is a weighted average of the securities' returns; n. 4, with short sales an infinite amount would go to the security with the highest r.
- p. 79: the law of large numbers cannot make a portfolio's actual yield almost the expected yield: "The returns from securities are too intercorrelated. Diversification cannot eliminate all variance." Limitations stated: static probability beliefs; results presented geometrically for 3 and 4 securities.
- p. 80: E = sum p_i y_i; V = sum p_i (y_i - E)^2; sigma = sqrt(V); coefficient of variation sigma/E; the expected value of a weighted sum is the weighted sum of expected values; covariance sigma_ij = E{[R_i - E(R_i)][R_j - E(R_j)]} = rho_ij sigma_i sigma_j.
- p. 81: variance of a weighted sum; R = sum R_i X_i with X_i "the percentage of the investor's assets which are allocated to the i-th security", fixed by the investor, sum X_i = 1, X_i >= 0 (short sales excluded); E = sum X_i mu_i and V = sum_i sum_j sigma_ij X_i X_j. n. 7: probability beliefs are the investor's, possibly subjective; the paper does not consider how beliefs are formed.
- p. 82, Fig. 1: attainable (E, V) combinations; the E-V rule selects those "with minimum V for given E or more and maximum E for given V or less". Fig. 1 has E horizontal and V vertical.
- pp. 83-85, Fig. 2: three securities with sum X_i = 1 and X_i >= 0 reduced to two dimensions; isomean lines parallel, isovariance curves concentric ellipses; the critical line; the efficient set from the minimum-variance point to the maximum-E point (n. 8: V in X_1, X_2; n. 9 on equal means).
- p. 87 and n. 10: the efficient set (in weights) is a series of connected line segments; V against E for efficient portfolios gives connected parabola segments, for any number of securities.
- p. 89: the E-V rule implies diversification for a wide range of beliefs, and the right kind (across industries, which have lower covariances); using sigma or sigma/E instead of V leaves the choice in the efficient set; n. 12: combining two portfolios of equal variance never increases variance and lowers it unless their returns are perfectly correlated.
- pp. 90-91: an investor with U(E, V), dU/dE > 0 and dU/dV < 0 "will never accept an actuarially fair bet"; the third moment linked to a propensity to gamble; E-V efficiency "reasonable as a working hypothesis" for institutions; X_i may represent aggregates such as bonds, stocks and real estate (n. 15: care with aggregates); estimates should combine statistics and judgement; the paper treats only the second stage, not the formation of beliefs.

## Limits

Printing slips on p. 81 as scanned: the first double sum's inner index reads "i>1" where j>i is meant, and the final V formula prints "X_i X" without the subscript j. The entries use the intended forms. The paper has no estimation from data and no denominators; those come from the descriptive-statistics entries. Pages 82-91 were read in the later portfolio choice batch (2026-10-18).
