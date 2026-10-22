---
key: clark-west-2006-nber
pathways: [return-predictability]
version: Todd E. Clark and Kenneth D. West, "Approximately Normal Tests for Equal Predictive Accuracy in Nested Models", NBER Technical Working Paper 326, August 2006 (journal version Journal of Econometrics 138(1), 2007, catalogue wide-clark-west, not read). Copy used: PDF from nber.org (40 pages, SHA-256 69d6c6c9...0362); printed page = PDF page - 2; tables on unnumbered pages at the end
sections: abstract; secs. 1-4 (pp. 1-12); secs. 6.1-6.2 (pp. 13-17); sec. 7 (pp. 19-20); Table 1 (PDF p. 36); results table (PDF p. 40)
read:
status: draft
---

Prepared on 2026-10-22 by the return-predictability content batch from source checks, not from study: the headings that need your own reading are left empty. Used for `meth:nested-forecast-tests`.

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- MSPE-adjusted: f = (y - yhat_1)^2 - [(y - yhat_2)^2 - (yhat_1 - yhat_2)^2], regressed on a constant, one-sided at 1.282 or 1.645 (eq. (2.1), p. 4).
- Decomposition of the MSPE difference and its negative noise term (eq. (3.8), p. 7); MSPE-adjusted = 2 P^-1 sum e_1 (e_1 - e_2) (eq. (4.1), p. 8).
- Regime (p. 8): R -> infinity, P -> infinity, P/R -> finite nonzero constant; least squares; direct multistep forecasts. For one-step, conditionally homoskedastic forecasts the limit depends only on dim(Z), lim P/R and the scheme; Clark-McCracken's numerically computed tables cover dim(Z) <= 20 and P/R from 0.1 to 20.
- Eq. (4.2), p. 9: 0.90 quantile <= 1.282 <= 0.95 quantile "apart from a couple of exceptions": all 400 recursive entries obey both; 396 of 400 rolling entries obey the lower bound, the other four have a 0.90 quantile of 1.29 (pp. 9-10). Hence nominal 0.10 tests with actual size "somewhere between .05 and .10" for P and R large; "no formal proof", not asserted to be "literally true", further cases possible (p. 9).
- Eq. (4.3), p. 10: 1.645 gives size between 0.01 and 0.05; the lower bound fails in 1 recursive and 14 rolling entries (0.95 quantile 1.65 or 1.66). With dim(Z) = 1 the quantiles also apply under conditional heteroskedasticity and to multistep forecasts (p. 10); otherwise simulated critical values (p. 12).
- DGP 1 (eq. (6.1), p. 13); design (p. 15): R + 720 observations per replication, initial (y, z) drawn from the unconditional distribution, forecasts for R + 1, ..., R + 720 estimated on observations 1, ..., t - 1 (recursive) or t - R, ..., t - 1 (rolling), each P evaluated on R + 1, ..., R + P; 5,000 replications. Table 1, panel B1, recursive, R = 120: MSPE-adjusted 0.085, 0.070, 0.062, 0.054 and MSPE-normal 0.028, 0.012, 0.009, 0.003 for P = 120, 240, 360, 720; panel A1, rolling: 0.085, 0.078, 0.080, 0.091 and 0.018, 0.006, 0.001, 0.000.
- Rolling, R = 120, P = 720, means over 5,000 replications: MSPE difference -0.24, adjusted 0.01, squared forecast difference 0.25 (p. 16).
- Simulation summary: all 48 one-step entries (Tables 1-2) between 0.05 and 0.10, median 0.080; MSPE-normal median 0.008; at 1.645, sizes 0.027-0.059, three outside 0.01-0.05 (pp. 2, 15-17).
- Stock-return example, recursive, 1964-2004: MSPEs 18.91 and 19.14, adjustment 0.68, t 1.17 (pp. 19-20; the results table is printed as "Table 4", the text calls it Table 7).

## Limits

Sec. 5 (other statistics), the multistep appendix and the power tables were not read for this batch. Recomputed sizes for DGP 1 (0.069, 0.059, 5,000 replications) fall below Table 1 by 3.0 and 2.3 standard errors counting both simulations. In the source's own design (20,000 replications, audit of 22 October 2026) the gap is confined to P = 120 (about 0.013, three standard errors, recursive and rolling), while the p. 16 means are reproduced; the cause is unresolved.
