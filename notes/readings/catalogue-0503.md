---
key: catalogue-0503
pathways: [lob-deep-learning]
version: Rama Cont, Arseniy Kukanov and Sasha Stoikov, "The Price Impact of Order Book Events", Journal of Financial Econometrics 12(1), 47-88, 2014 (DOI 10.1093/jjfinec/nbt003). Copy used: arXiv 1011.6402v3, dated March 2011 (arXiv stamp 13 April 2011), 26 pages, downloaded 2026-10-16. Page numbers below are the preprint's; the journal version was not checked
sections: abstract (p. 1); sec. 2.1 (pp. 3-4, definition of e_n and OFI); sec. 3.1 (p. 8, data and time grid); sec. 4.1 (p. 16, trade imbalance against OFI, Table 4) (checked for migration order books and order flow review)
read:
status: draft
---

Prepared on 2026-10-16 by migration order books and order flow review from source checks, not from study: the headings that need your own reading are left empty. The paper is in the catalogue and is not on `lob-deep-learning`'s required list, whose readings build on it.

## Question and claim

## Mechanism

## Method

## Data and timing

- One calendar month (April 2010) of consolidated NYSE TAQ quotes and trades for 50 S&P 500 stocks drawn at random; timestamps rounded to the second; best quotes aggregated into an NBBO; about 40 quote updates per trade (sec. 3.1, p. 8).
- A 10-second grid, regressions per half-hour (273 per stock); robustness over intervals from 10 quote updates to 10 minutes on a subsample (p. 8).

## Key results

- $e_n$ and $\mathrm{OFI}_k$ as in `def:order-flow-imbalance` (sec. 2.1, p. 4).
- Average $R^2$ 65 percent for OFI against 32 percent for trade imbalance; with both, trade imbalance significant in 31 percent of subsamples (sec. 4.1, Table 4, p. 16).
- Slope inversely proportional to depth (abstract).

## Limits

## Implementation

## Notation map

- Their trade imbalance $\mathrm{TI}_k$ is what Bouchaud et al. (`catalogue-0528`, p. 222) call "order-flow imbalance".

## Connections

## Entries

`def:order-flow-imbalance`.

## Open questions

- The fits are contemporaneous; the forecasting use the legacy notes implied was not tested in the passages read.

## Retrieval cards
