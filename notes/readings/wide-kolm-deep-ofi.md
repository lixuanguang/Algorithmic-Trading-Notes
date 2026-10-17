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

- Pairwise OF-against-LOB tests: each Table 3 entry is, per model and horizon, the number of stocks with a significantly positive t-statistic (1 percent) minus the number with a significantly negative one (sec. 4.1.2, PDF p. 19; caption, PDF p. 21). CNN-LSTM row: 70 to 93 (Avg 89); LSTM rows 114-115. These are net counts: neither they nor 115 minus them are counts of winning or losing stocks, and the raw counts are not reported.
- Source ambiguity, recorded rather than resolved: the caption and text also read an entry X as OF outperforming "for X stocks"; the caption tests a "loss difference" where the text tests a difference in R^2_OS; and the text's "about 40 stocks for which the CNN-LSTM with LOB inputs perform better" at shorter horizons (PDF p. 20) cannot be derived from the net counts. No exact count of LOB-favoured stocks is stated.
- Out-of-sample R^2 rises up to about two average price changes (Fig. 2, PDF p. 18, whose horizons stop at two). The decline beyond two rests on Fig. 8 (PDF p. 28): read from the plot, CNN-LSTM peaks near 1.5 percent at about two and falls to roughly 0.64 at ten; the text on it says R^2_OS "plateaus at around two average price changes" (sec. 4.3, PDF p. 27).

Correction of 2026-10-17: the earlier bullet here said the CNN-LSTM did better with LOB inputs "for 23 to 45 stocks", obtained by subtracting Table 3's entries from 115, and cited Fig. 2 for the decline; both were wrong for the reasons above (rechecked on PDF pp. 18-21 and 27-28 as page images).

## Limits

No transaction costs: "proper modeling of transaction costs and application of an appropriate execution strategy is critical to their profitability" (PDF p. 31). Working-paper version.
