---
key: wide-bacry-life-cycle
pathways: [price-impact-execution]
version: Emmanuel Bacry, Adrian Iuga, Matthieu Lasnier and Charles-Albert Lehalle, "Market Impacts and the Life Cycle of Investors Orders", Market Microstructure and Liquidity 1(2), 1550009, 2015 (DOI 10.1142/s2382626615500094). Copy used: arXiv 1412.0217, printed 9 December 2014, 30 pages, downloaded 2026-10-15. Page numbers below are the preprint's; the journal version was not checked
sections: abstract (p. 1); sec. 2.2 (pp. 3-4); sec. 3 (pp. 5-8, page image of p. 8, impact estimation review); secs. 7-8 (pp. 19-22); page image of p. 21 (checked for market-impact models / impact estimation reviews)
read:
status: draft
---

Prepared on 2026-10-15 by market-impact models review from source checks, not from study: the headings that need your own reading are left empty.

## Question and claim

## Mechanism

## Method

## Data and timing

- About 400,000 metaorders traded electronically by one broker on European markets in 2010 (abstract, p. 1; sec. 2.3, p. 3).

## Key results

- Impact defined by $\epsilon\Delta P_t=\eta_t+\epsilon\Delta W_t$; temporary (end of execution), transient (during), decay (after) and permanent (long after) impact (sec. 2.2, eq. (1), p. 3); estimation needs $\mathbb E[\epsilon\Delta W]=0$ (p. 4).
- Direct regressions of the signed end-of-execution move (Table 2, p. 8): daily participation 0.54–0.59 with duration −0.23 to −0.35; trading rate 0.37–0.56 with duration +0.15 to +0.24; spread 0.28 and volatility 0.96 in log-log fits.
- Square-root temporary impact in daily participation (abstract); smaller exponents with robust direct regressions than with log-log regressions (sec. 8, p. 22).
- Mechanical against informational views of permanent impact, held as a duality (sec. 7.1, pp. 19–20).
- Debiasing for autocorrelated metaorder flow with a square-root model, after Waelbroeck and Gomes (2013); CAPM-like decomposition, eq. (21), with beta over $D-20$ to $D+20$; after debiasing the idiosyncratic profile returns to its initial level within 20 days, the remaining permanent impact is systematic (secs. 7.2–7.3, pp. 20–22, page image of p. 21).

## Limits

## Implementation

## Notation map

- Their index $\mathcal I_d$ is not the compendium's impact $I$; their $\eta_t$ is the impact curve.

## Connections

- `catalogue-0528` p. 240 makes the same point that correlated metaorders mimic permanent impact.

## Entries

`meth:post-execution-impact-profile`, `ev:square-root-impact`, `ev:intraday-impact-profile`; also cited in `def:price-impact`.

## Open questions

- The beta is estimated over a window that includes the execution and the following days (Interpretation: in-sample, can absorb the event). Lehalle and Laruelle's 2018 restatement (`alpha-laruelle`, pp. 213–215) keeps the same window and least-squares beta, so the question stands; the journal version itself was not compared.

## Retrieval cards
