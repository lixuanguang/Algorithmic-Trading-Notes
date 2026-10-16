---
key: s3-velu
pathways: [point-in-time-data, alternative-data-sources]
version: Raja Velu, Maxence Hardy and Daniel Nehren, Algorithmic Trading and Quantitative Strategies, Chapman & Hall/CRC Financial Mathematics Series, CRC Press, Boca Raton, ISBN 9781498737166 (hbk), 9780429183942 (ebk). The copyright page of the local copy reads "(c) 2020 Taylor & Francis Group"; the catalogue records a 2020 release and 2021 copyright. Copy used: a local PDF outside the repository with a text layer (printed page = PDF page - 17 in chap. 1)
sections: chap. 1, sec. 1.4 "Taxonomy of Data Used in Algorithmic Trading" (pp. 26-44), text layer, with Table 1.10 (p. 37) by page image, read for migration slice 32; nothing else read; slice 36: chap. 11, sec. 11.1 (pp. 383-386), text layer
read:
status: draft
---

Prepared on 2026-10-16 by migration slice 32 from source checks, not from study: the headings that need your own reading are left empty. The legacy ML data-taxonomy file's five definitions (reference data, market data feed, binned data, granular intraday activity, fundamental and other data) follow this section closely without naming it; the book is cited in the compendium's preface. No route checked here names it as a required reading.

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- Reference data, "the key foundation of a robust quantitative strategy development": universe, symbology needing "a bi-temporal data structure", ticker changes, corporate actions, static data and quote factors, exchange data whose historic values must be kept "in order to run realistic historical backtests", condition codes, special days ("model normal days first"), futures and options reference data (E-mini front month about 1.5 million contracts a day against 30,000 before the roll), event calendars, related tickers, composite assets, latency tables (sec. 1.4.1, pp. 26-35).
- Market data Level I, II and III; matching-engine against reception time; full book once messages are "consolidated into one single dataset ordered by timestamp"; Table 1.10, a U.S. Level III record, price "Divide by 10000"; special order types (sec. 1.4.2, pp. 35-39).
- Derived statistics: daily activity, intraday microstructure, pre-computed aggregates, which "need to fully support the peculiarities described in the Reference Data section"; binned data, profiles "rarely built with a granularity finer than one minute" (sec. 1.4.3, pp. 39-42).
- Fundamental and other data: key ratios, analyst recommendations, earnings, holders (13F) that "might indicate changes in sentiment", insiders "thought to be an indicator", ratings downgrades that "generally have a negative impact"; alternative data whose value falls as more investors get access (sec. 1.4.4, pp. 42-44).

## Limits

## Implementation

## Notation map

## Connections

## Entries

`data:trading-reference-data`, `data:market-data-levels`, `data:derived-market-statistics` (`point-in-time-data`); `def:financial-data-types` (`alternative-data-sources`, with `alpha-afml`).

Slice 36: `data:market-data-levels` (the order path from client to venue: FIX, the order management system, gateways and native protocols, acknowledgements and executions, clearing and settlement; chap. 11, sec. 11.1, pp. 383-386), merged from the legacy data-engineering file.

## Open questions

- The legacy "divide by 1000" and the mislabelled "Binned Data" heading were the notes' slips, not the book's; were the notes made from another printing?
- The 13F, 13D and Form 4 thresholds and deadlines in the footnotes (p. 43) are not checked against the rules.
