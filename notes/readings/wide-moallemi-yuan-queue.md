---
key: wide-moallemi-yuan-queue
pathways: [market-making-lob, hft-market-design]
version: Ciamac C. Moallemi and Kai Yuan, "A Model for Queue Position Valuation in a Limit Order Book", author working paper, initial version December 2016, current revision June 2017 (the copy read; the catalogue records the 2016 version), from the author's site (moallemi.com/ciamac/papers/queue-value-2016.pdf), 33 pages, retrieved 2026-10-16; printed page = PDF page
sections: abstract; sec. 1 (pp. 1-4); sec. 2, opening (p. 6); sec. 4.3 and Table 1 (pp. 18-19); sec. 5.2 and Table 3 (pp. 23-24); sec. 6 (pp. 24-25); read for dealer models and information review. Sec. 3 (the value recursion) and the remaining sections not read
read:
status: draft
---

Prepared on 2026-10-16 by dealer models and information review from source checks, not from study: the headings that need your own reading are left empty.

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- Two components of a resting order's value under price-time priority: a static one (spread against adverse selection at execution, adverse selection increasing with queue position) and a dynamic one (the option value of a locked-in position as it moves up) (abstract; pp. 1, 3-4).
- Faster orders win better positions, especially after a price change, when traders race to queue at the new price (p. 3).
- Restricted to large-tick assets (spread rarely above one tick, long queues); small-tick assets buy priority with price; pro-rata markets make position irrelevant (p. 6; n. 2, p. 2).
- BAC on Nasdaq, August 2013 (Table 1, p. 19); nine symbols backtested; front-of-queue value exceeds back-of-queue value in every symbol, the model's gap from 0.03 to 0.22 ticks (Table 3, p. 23); "comparable to the bid ask spread (>0.1 ticks)" for BAC and CSCO (p. 24).
- Queue value rewards speed; is price-time priority right for large-tick assets? (p. 25).

## Limits

## Implementation

## Notation map

## Connections

## Entries

dealer models and information review: `res:queue-position-value` (owned by `hft-market-design`; the paper contradicts the claim that queues are thin).

## Open questions

- Is there a later journal version, and which revision does the catalogue intend? Table 2 describes 21 trading days of August 2013, Table 3 averages over 30 trading days.

## Retrieval cards
