---
key: signed-rank-test-reference-2023
pathways: [probability-statistics]
version: NIST Dataplot Reference Manual, "Signed Rank Test", created 5 June 2001, last updated 11 December 2023; web page read 2026-10-18
sections: whole page (purpose, assumptions after Conover, comparison with the t and sign tests, statistic and large-sample approximation)
read:
status: draft
---

Prepared on 2026-10-18 by the inference and simulation slice from source checks, not from study: the headings that need your own reading are left empty. Search: "NIST engineering statistics handbook Wilcoxon signed rank test sign test nonparametric assumptions". A software reference, used because the e-Handbook page on the test was not found. Used for `meth:nonparametric-tests`.

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- One-sample or paired test of equal means; assumptions: symmetric differences, mutually independent, same mean, at least interval scale.
- Replaces the t test's normality by symmetry; less powerful than the t test when its assumptions hold; more powerful than the sign test but assumes more, so the sign test is preferred when symmetry is doubtful.
- W = min(W-, W+); tables for N <= 30; normal approximation with mean n(n + 1)/4 and s.d. sqrt(n(n + 1)(2n + 1)/24) for larger N.

## Limits

The sign test's exact binomial null distribution is derived in the entry, not quoted from this page.
