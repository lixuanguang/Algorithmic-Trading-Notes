---
key: s6-stoikov
pathways: [market-making-lob, execution-market-making]
version: 2008 journal article, Quantitative Finance 8(3), 217-224; author-hosted journal PDF
sections: 1-3 (checked for the migration pilot)
read:
status: draft
---

Prepared on 2026-10-14 by the compendium migration pilot from source checks, not from study: the headings that need your own reading are left empty.

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
