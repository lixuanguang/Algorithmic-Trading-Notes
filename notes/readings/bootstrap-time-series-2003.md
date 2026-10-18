---
key: bootstrap-time-series-2003
pathways: [common-toolkit]
version: Dimitris N. Politis, "The Impact of Bootstrap Methods on Time Series Analysis", Statistical Science 18(2) (2003), 219-230, doi 10.1214/ss/1063994977. Copy used: author's PDF from mathweb.ucsd.edu retrieved 2026-10-18, SHA-256 80c1b1332fe3a7982930b6be541b9ee62b6cdcaecb8cc28ba9accea8e3c9a61f, 12 PDF pages, in the git-ignored `reading_materials/coverage-pilots/` (printed page = PDF page + 218)
sections: abstract; sec. 2 Block resampling and subsampling (pp. 221-222); sec. 2.3 Block size choice (p. 223)
read:
status: draft
---

Prepared on 2026-10-18 by the inference and simulation slice from source checks, not from study: the headings that need your own reading are left empty. Searched for after Kunsch (1989) on Project Euclid returned an empty page to the fetcher. Used for `meth:bootstrap-resampling`.

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- The i.i.d. bootstrap applied to dependent data is inconsistent (Singh 1981): it scrambles the data, loses all dependence information, and its variance estimate converges to gamma(0) instead of the long-run variance sum of gamma(s) (p. 221).
- Kunsch's (1989) block bootstrap joins k blocks of b consecutive observations drawn with replacement from all n - b + 1 blocks and recomputes the statistic on the pseudo-series (p. 222); circular and stationary variants follow.
- Choosing b is like bandwidth choice in smoothing; cross-validation and plug-in approaches (p. 223).

## Limits

The entry's AR(1) figures are exact expectations computed for this record, not results from the paper. Kunsch (1989) itself was not read.
