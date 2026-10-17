---
key: exp-huang-lehalle-rosenbaum-queue-reactive
pathways: [market-making-lob]
version: Weibing Huang, Charles-Albert Lehalle and Mathieu Rosenbaum, "Simulating and Analyzing Order Book Data: The Queue-Reactive Model", Journal of the American Statistical Association 110(509), 107-122, 2015, as catalogued. Copy used: arXiv 1312.0563 version 2 of 3 September 2014, 29 pages, downloaded 2026-10-16 into the ignored `reading_materials/`; text layer; printed page = PDF page. The journal version was not compared
sections: secs. 2-3 (pp. 4-20): framework and Theorem 2.1, data, Model I estimation and invariant law, Models IIa-IIb, Model III and mechanical volatility, the placement application's calibration
read:
status: draft
---

Prepared on 2026-10-16 by the source follow-up of order books and order flow / dealer models and information reviews from source checks, not from study: the headings that need your own reading are left empty.

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- Ergodicity (Theorem 2.1, pp. 4-5) under a negative individual drift above a bound and bounded total insertion.
- Model I (sec. 2.3, pp. 7-10): independent birth-death queues; MLE as inverse mean waiting time by queue size times event shares; invariant law from rho(n) = lambda_L(n)/(lambda_C(n+1)+lambda_M(n+1)).
- Data (sec. 2.2, pp. 5-7): Cheuvreux records, Euronext Paris, January 2010 to March 2012, first and last hour removed; France Telecom (spread 1.43 ticks) and Alcatel-Lucent; K = 3.
- Model III (sec. 3.1, pp. 17-18): theta and theta_reinit; maximal mechanical volatility 5 bp against 14 bp observed; eta 0.08 against 0.39; calibration theta = 0.7, theta_reinit = 0.85 (p. 20).

## Limits

Model III numbers are for one stock; the arXiv text may differ from the journal's.
