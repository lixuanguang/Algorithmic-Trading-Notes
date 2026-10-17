---
key: w2-briola-lob-guide
pathways: [lob-deep-learning]
version: Antonio Briola, Silvia Bartolucci and Tomaso Aste, "Deep limit order book forecasting: a microstructural guide", Quantitative Finance 25(7), 2025, as catalogued. Copy used: arXiv 2403.09267 version 4 of 4 June 2024, 43 pages, downloaded 2026-10-16; text layer. The journal version was not compared
sections: secs. 4-5 (pp. 7-8), sec. 6 (tick classes) and sec. 7 (pp. 22-25); source verification (2026-10-17): sec. 7, pp. 22-23 (the four backtest assumptions), and Table 7 with its text, pp. 16-17
read:
status: draft
---

Prepared on 2026-10-16 by the source follow-up of order books and order flow / dealer models and information reviews from source checks, not from study: the headings that need your own reading are left empty.

source verification (2026-10-17) (source checks, not study): the four assumptions a history-only backtest must make and the clock-time distribution of tick-time horizons were read for `def:order-flow-imbalance`; Appendices A-C remain unread.

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- Fifteen large- and mega-cap NASDAQ stocks, LOBSTER 2017-2019; 45 training days, 5 validation days drawn from the training period, 10 test days per year; horizons of 10, 50 and 100 book updates against one tick.
- p_T = CT/(PT + TT - CT), an overlap of predicted and realised round trips, "assumption-free" (no costs or fills).

## Limits

Validation days inside the training window; universe chosen on 2017-2019 capitalisation.
