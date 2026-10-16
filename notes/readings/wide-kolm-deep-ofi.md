---
key: wide-kolm-deep-ofi
pathways: [lob-deep-learning]
version: Petter N. Kolm, Jeremy Turiel and Nicholas Westray, "Deep order flow imbalance: Extracting alpha at multiple horizons from the limit order book", Mathematical Finance 33(4), 2023, as catalogued. Copy used: SSRN working paper 3900141, dated 6 August 2021, 43 pages, downloaded through a browser 2026-10-16; text layer, Fig. 8 read as an image. The journal version was not compared
sections: secs. 1-4 and the conclusion (PDF pp. 1-31)
read:
status: draft
---

Prepared on 2026-10-16 by the second source follow-up from source checks, not from study: the headings that need your own reading are left empty.

## Question and claim

## Mechanism

## Method

- One network per stock; inputs are ten-level book states (LOB) or order flows (OF); horizons h_k = k Delta t / 5, k = 1..10, with Delta t = 2.34e7 ms / N and N the average daily number of non-zero mid-price changes; ten-millisecond latency buffer (secs. 2-3, PDF pp. 5-7 and 14).
- Rolling windows: one validation week, four training weeks, one test week, stepped by three weeks, 18 windows (PDF p. 15).

## Data and timing

- LOBSTER, 115 stocks that were Nasdaq-100 members at some time from 1 January 2019 to 31 January 2020, with at least 260 trading days and no corporate actions (PDF p. 12): a selection that conditions on the whole period.

## Key results

- OF inputs beat LOB inputs for most stocks in pairwise tests, though the CNN-LSTM did better with LOB for 23 to 45 stocks depending on the horizon (Table 3, PDF pp. 19-23).
- Out-of-sample R^2 rises to about two average price changes and declines after; read from Fig. 8, CNN-LSTM peaks near 1.5 percent and falls to about 0.65 at ten (PDF pp. 18 and 28).

## Limits

No transaction costs: "proper modeling of transaction costs and application of an appropriate execution strategy is critical to their profitability" (PDF p. 31). Working-paper version.
