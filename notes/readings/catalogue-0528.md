---
key: catalogue-0528
pathways: [price-impact-execution, execution-market-making, market-making-lob, market-simulation, lob-deep-learning, market-structure-execution-quality]
version: Jean-Philippe Bouchaud, Julius Bonart, Jonathan Donier and Martin Gould, Trades, Quotes and Prices: Financial Markets Under the Microscope, Cambridge University Press, first published 2018 (ISBN 9781107156050; DOI 10.1017/9781316659335). The catalogue record does not establish the edition; this copy was used. Local PDF with a text layer, outside the repository (printed page = PDF page - 19)
sections: chap. 10, secs. 10.4-10.5 (p. 198); chap. 11, secs. 11.1-11.2 (pp. 208-212); chap. 12, secs. 12.2-12.5 (pp. 233-236, 240-241); chap. 13, secs. 13.1-13.2.3 (pp. 249-257); chap. 19, sec. 19.5 (pp. 361-362); page images of pp. 211, 234, 252 and 362 (checked for migration liquidity and impact / market-impact models reviews); chap. 2, secs. 2.1-2.2.2, pp. 23-31; chap. 3, pp. 43-56; chap. 4, secs. 4.1-4.2.1, pp. 58-61; chap. 7, secs. 7.1-7.2, pp. 118-120; chap. 9, pp. 163-185; chap. 10, sec. 10.1, pp. 187-189; chap. 11, sec. 11.4, pp. 222-223 (order books and order flow review); chap. 3, secs. 3.1.2-3.1.3, 3.2.2-3.2.3, pp. 45, 55-56 (order matching and fragmentation review and the order books and order flow review follow-up)
read:
status: draft
---

Prepared on 2026-10-15 by migration liquidity and impact review from source checks, not from study: the headings that need your own reading are left empty. The book is in the catalogue but on no route's required list.

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- Two readings of impact: orders forecast prices (efficient-market view, after Hasbrouck) against trading moves prices (order-flow view, Santa Fe model) (sec. 11.1, pp. 208–210).
- Reaction, observed and prediction impact, $I^{\mathrm{obs}}=I^{\mathrm{react}}+I^{\mathrm{pred}}$, with $\mathcal F_t$ implicit throughout (eqs. (11.1)–(11.4), pp. 210–211, page image of p. 211); reaction impact estimable by random trades; short-run mechanical impact similar for random and informed trades (p. 212).
- Impact decay after a metaorder: abrupt relaxation then a plateau; permanent impact mixes reaction and prediction; correlated metaorders mimic permanent impact (sec. 12.4, p. 240).
- Propagator model, eq. (13.7) (p. 252, page image); constant permanent impact with long-memory signs would make returns autocorrelated (pp. 250–251); response function eq. (13.10) (p. 253).
- Order splitting, not herding, causes the long memory of order signs (p. 198).
- Square-root law, eq. (12.6) (p. 234, page image); shortfall two-thirds of peak impact (eq. (12.11), p. 241); permanent impact = prediction + reaction, eq. (12.5) (p. 233).
- Kernel estimation $K=\mathbf C^{-1}S$ (eqs. (13.13)–(13.15), p. 254); power-law decay and the fine balance $\beta_c=(1-\gamma)/2$ (eq. (13.17), pp. 254–257).
- Absence of price manipulation in the latent-liquidity model: the cost of any closed trajectory is a non-negative quadratic form (sec. 19.5, pp. 361–362, page image).

## Limits

## Implementation

## Notation map

- $\varepsilon_n$ (market-order sign) corresponds to the compendium's trade sign $q_t$ in the spread entries.

## Connections

- `wide-webster-price-impact` quotes pp. 35–36, 210–211 and 238–239 of this book.
- `s6-hasbrouck` is the efficient-market reading the authors contrast with.

## Entries

`def:price-impact`, `mod:propagator`, `res:no-price-manipulation`, `ev:square-root-impact`.

order books and order flow review: `def:limit-order-book`, `mech:order-lifecycle`, `res:limit-order-options`, `def:queue-imbalance`, `def:order-flow-imbalance` (naming), `def:tick-size`, `ev:high-frequency-stylised-facts`, `meth:realised-variance-signature-plot`, `meth:intraday-deseasonalisation`, `def:market-clocks-durations`, `def:order-event-point-processes`, `mod:hawkes-order-flow`, `mod:queue-reactive-intensities`.

order matching and fragmentation review and the order books and order flow review follow-up: `def:limit-order-book` (their market-order event convention, p. 45), `def:order-instructions` (IOC against FOK, p. 55), `mech:order-matching-pricing` (auction price, p. 56).

## Open questions

- In eq. (11.2) as printed, observed impact conditions on execution alone, whereas (11.1) and (11.3) condition on $\mathcal F_t$; the identity (11.4) needs the conditioning throughout, which the authors say is implicit (p. 210).
- Chapter 14 (generalised propagators) and chapter 19's eq. (19.7) were not read.

## Retrieval cards
