---
key: demeterfi-varswaps-gs-1999
pathways: [portfolio-construction-risk, volatility-options]
version: Kresimir Demeterfi, Emanuel Derman, Michael Kamal and Joseph Zou, "More Than You Ever Wanted To Know About Volatility Swaps", Goldman Sachs Quantitative Strategies Research Notes, March 1999. Copy: emanuelderman.com/wp-content/uploads/1999/02/gs-volatility_swaps.pdf, 56 PDF pages with a text layer; SHA-256 ad289770b42f89cd0046f1e20ae42e4ecc2f15c419e1cd2705576739f762223e; git-ignored copy in reading_materials/library-gap-l4-20261021/; retrieved 2026-10-21; printed page = PDF page - 4. The catalogue key wide-demeterfi-varswaps is the Journal of Derivatives 6(4) 1999 version ("A Guide to Volatility and Variance Swaps"), whose pages differ; it was not read
sections: pp. 1-3 (EQ 1-2, quoting, contract terms: price source and frequency, annualisation factor with 260 business days as an example, zero mean preferred); pp. 12-13 (imperfect strikes; variance vega with an ideal strip decreases linearly with time to expiry, "as expected for a swap whose value is proportional to the remaining variance"); p. 15 (EQ 13-16: continuous realised variance, value e^{-rT}E[V - K_var], fair strike K_var = E[V]); pp. 18-19 (EQ 26, the strip); pp. 29-30 (EQ 35-37: daily accumulation of log payoffs, "variance is additive", a single jump's contribution)
read:
status: draft
---

Prepared on 2026-10-21 by library gap-filling Batch L4 from source checks, not from study: the headings that need your own reading are left empty.

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- Realised variance in the replication argument is the continuous integral (1/T) int sigma^2 dt (EQ 14, p. 15); discrete sampling and jumps are treated as departures (pp. 29-30).
- Contract terms must specify source, frequency, annualisation and mean convention (pp. 1-2).
- No mid-life valuation formula is printed. The seasoned value in `meth:volatility-derivative-applications` is a labelled derivation from EQ 14-16 and additivity (decision L4-D2).

## Limits

Goldman Sachs note, not the journal version. Under GBM, sampled squared log returns have expectation sigma^2 + (r - q - sigma^2/2)^2/A per annualised unit, a term the continuous strip omits; computed in the check script, not in the source.

## Implementation

## Notation map

## Connections

## Entries

`meth:volatility-derivative-applications`

## Open questions
