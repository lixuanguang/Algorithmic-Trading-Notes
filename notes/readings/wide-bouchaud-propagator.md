---
key: wide-bouchaud-propagator
pathways: [price-impact-execution]
version: Jean-Philippe Bouchaud, Yuval Gefen, Marc Potters and Matteo Wyart, "Fluctuations and response in financial markets: the subtle nature of 'random' price changes", Quantitative Finance 4(2), 176-190, 2004 (DOI 10.1080/14697680400000022). Copy used: arXiv cond-mat/0307332v2 (25 August 2003), 30 pages, downloaded 2026-10-15. Page numbers below are the preprint's; the journal version was not checked
sections: sec. 3.1 (pp. 14-16); sec. 3.2 (pp. 16-17); page image of p. 14 (checked for migration market-impact models review)
read:
status: draft
---

Prepared on 2026-10-15 by migration market-impact models review from source checks, not from study: the headings that need your own reading are left empty.

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- Trade superposition model: $p_n=\sum_{n'<n}G_0(n-n')\varepsilon_{n'}\ln V_{n'}+\sum_{n'<n}\eta_{n'}$, $G_0$ the bare propagator, $\eta$ independent of signs and uncorrelated (eq. (12), p. 14, page image); $G_0$ measurable in principle with random trades (p. 14).
- A constant $G_0$ with power-law sign correlations would make the response grow like $\ell^{1-\gamma}$, so $G_0$ must decay (p. 16); power-law ansatz eq. (22) and $2H=2-2\beta-\gamma$ (pp. 16–17).

## Limits

## Implementation

## Notation map

- Their $p_n$ and $\eta_n$ correspond to the book's $m_t$ and $\xi_n$ (`catalogue-0528`, eq. (13.7)); the book's simple model drops the $\ln V$ weight.

## Connections

- `catalogue-0528` chap. 13 restates the model without the volume weight.

## Entries

`mod:propagator`.

## Open questions

- Check the journal version against the arXiv v2 equations.

## Retrieval cards
