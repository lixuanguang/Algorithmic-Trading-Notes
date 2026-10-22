---
key: nist-dataplot-rank-correlation
pathways: [probability-statistics]
version: National Institute of Standards and Technology, Dataplot Reference Manual, "RANK CORRELATION INDEPENDENCE TEST" (https://itl.nist.gov/div898/software/dataplot/refman1/auxillar/rankcorr.htm), date created 8 March 2013, last updated 11 December 2023; a fetched rendering read 2026-10-21 (summarised by the fetch tool)
sections: whole page: purpose, definition of Spearman's rho via average ranks, critical values (Conover Table A10 for n <= 30 without ties; normal approximation z_p / sqrt(n - 1) otherwise), two-sided p-value, reference to Conover (1999), pp. 319-327
read:
status: draft
---

Prepared on 2026-10-21 by library gap-filling Batch L2 from source checks, not from study: the headings that need your own reading are left empty. Used for `meth:correlation-independence-tests` (`probability-statistics`).

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- Spearman's rho is the Pearson correlation of the ranks, ties given average ranks; the test of independence uses tabulated quantiles for n <= 30 without ties, and z_p / sqrt(n - 1) for larger n or many ties.

## Limits

- Software documentation, not a textbook derivation; the d_i shortcut is not given. Conover (1999) was not read.

## Implementation

## Notation map

## Connections

## Entries

`meth:correlation-independence-tests` (`probability-statistics`).

## Open questions
