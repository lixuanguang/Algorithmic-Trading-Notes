---
key: wide-bacry-hawkes
pathways: [market-making-lob]
version: Emmanuel Bacry, Iacopo Mastromatteo and Jean-François Muzy, "Hawkes Processes in Finance", Market Microstructure and Liquidity 1(1), 1550005, 2015 (DOI 10.1142/s2382626615500057). Copy used: arXiv 1502.04592v2, 17 May 2015, 48 pages, downloaded 2026-10-16. Page numbers below are the preprint's; the journal version was not checked
sections: abstract and sec. 1 (pp. 1-3); sec. 2.1 (pp. 3-6, Definition 1, Proposition 1, Examples 1-2); secs. 2.2-2.2.4 (pp. 6-8); sec. 5.1 (p. 27, Bacry and Muzy's impact model); sec. 6.1 (pp. 29-30, Large's level-I model) (checked for order books and order flow review)
read:
status: draft
---

Prepared on 2026-10-16 by order books and order flow review from source checks, not from study: the headings that need your own reading are left empty. A required reading of `market-making-lob`; the sections above were read for one entry, the rest of the review was not.

## Question and claim

## Mechanism

## Method

## Data and timing

- Bacry and Muzy's model, as reported: EuroStoxx and Euro-Bund futures, most liquid maturity, 800 trading days, 2009-2012 (sec. 5.1, p. 27).
- Large's model, as reported: Barclays on the LSE, 22 trading days of January 2002, 1-second time stamps (sec. 6.1, p. 30).

## Key results

- Definition: non-negative, causal, integrable kernels; asymptotic stationarity when the matrix of kernel norms has spectral radius below 1 (sec. 2.1, pp. 3-4).
- Exponential kernel $\alpha\beta e^{-\beta t}$ (norm $\alpha$) and power-law kernel $\alpha\beta(1+\beta t)^{-(1+\gamma)}$ (stationary for $\alpha<\gamma$) (pp. 5-6).
- Non-linear Hawkes processes allow inhibition through negative kernels at the cost of tractability (sec. 2.2.4, p. 8); slightly negative self-kernels in the feedback of price moves on market orders in Bacry and Muzy's fit (p. 27).

## Limits

## Implementation

## Notation map

- Kernel parameterisations differ from Lehalle and Laruelle's $\alpha e^{-\beta t}$ (norm $\alpha/\beta$); see `mod:hawkes-order-flow`.

## Connections

## Entries

`mod:hawkes-order-flow`; also cited in `def:market-clocks-durations` (Further reading).

## Open questions

- The non-linear link is printed as $h(x)=1_{x\in\mathbb R^+}$ in the text layer (p. 8); read as the positive part, not checked by page image.

## Retrieval cards
