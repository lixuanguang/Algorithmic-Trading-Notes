---
key: back-transformed-forecast-mean-2014
pathways: [common-toolkit]
version: Rob J Hyndman, "The forecast mean after back-transformation", Hyndsight blog, 25 February 2014 (robjhyndman.com/hyndsight/backtransforming/); live page read 2026-10-18
sections: whole post: opening paragraph; Taylor-series mean; Box-Cox transformations; scaled logistic transformation skimmed
read:
status: draft
---

Prepared on 2026-10-18 by the regression correction pass from source checks, not from study: the headings that need your own reading are left empty. Used for `meth:regression-prediction-functional-form`.

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- Back-transformed point forecasts "can be considered the median of the forecast densities (assuming the forecast densities on the transformed scale are symmetric)"; medians do not aggregate but means do (opening paragraph).
- Mean on the original scale from the first three Taylor terms: f(mu) + sigma^2 f''(mu)/2; for the log case (lambda = 0) e^mu (1 + sigma^2/2) (Box-Cox transformations).

## Limits

A blog post, not a primary reference. The mean adjustment is a second-order approximation, not the exact lognormal mean e^(mu + sigma^2/2); the entry uses the exact normal-theory factor from Duan and NIST and cites this post only for the symmetry condition on the median. The post does not discuss geometric means; the geometric-mean reading in the entry is derivation.
