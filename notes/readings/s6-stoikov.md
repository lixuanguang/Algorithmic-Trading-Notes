---
key: s6-stoikov
pathways: [market-making-lob, execution-market-making]
version: 2008 journal article, Quantitative Finance 8(3), 217-224; author-hosted journal PDF
sections: 1-3 (checked for the migration pilot); source verification (2026-10-17): secs. 2.3 and 3.1 (pp. 219-221) rechecked as page images in the same author-hosted PDF, downloaded again
read:
status: draft
---

Prepared on 2026-10-14 by the compendium migration pilot from source checks, not from study: the headings that need your own reading are left empty.

source verification (2026-10-17) (source checks, not study): the infinite-horizon reservation prices of sec. 2.3 were recomputed from the stated objective; the printed bid matches the indifference definition and the printed ask does not (it breaks symmetry at q = 0), recorded in `mod:avellaneda-stoikov` as an apparent misprint.

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- Reservation price with frozen inventory $r(s,q,t)=s-q\gamma\sigma^2(T-t)$ (sec. 2.2, eq. (8), p. 219).
- Exponential intensity $\lambda(\delta)=Ae^{-k\delta}$ from power-law order sizes and logarithmic impact, $A=\Lambda/\alpha$, $k=\alpha K$ (sec. 2.5, eq. (12), p. 220).
- Approximate quotes: spread $\gamma\sigma^2(T-t)+\frac2\gamma\ln(1+\gamma/k)$ around $r$, from an expansion in $q$ and a linearised arrival term (sec. 3.2, eqs. (29)–(30), p. 221).
- 1000 simulations, $\gamma=0.1$: inventory strategy profit 65.0 (s.d. 6.6) against symmetric 68.4 (s.d. 12.7), same average spread 1.49 (sec. 3.3, Table 1, p. 222).

## Limits

## Implementation

## Notation map

- $\sigma$ is the absolute volatility of an arithmetic Brownian midprice (house override in `mod:avellaneda-stoikov`); $\lambda^a,\lambda^b$ are execution intensities, not impact slopes.

## Connections

- Builds on Ho and Stoll (1981), which the paper says first studied this dealer problem (sec. 3.1, p. 220); `crypto-cartea` has a chapter on dynamic market making ("Market Making"), not yet checked.

## Entries

`mod:avellaneda-stoikov`.

## Open questions

## Retrieval cards

Misprint review, method validation (2026-10-17): Balakaeva and Veretennikov (arXiv:2510.15988v1, Lemma 3) print the same infinite-horizon ask without derivation; their own Lemma 2 and Definition 3 give the ask with D(q-1), so the printed form stays an apparent misprint, quoted unchanged.
