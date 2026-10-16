---
key: s6-hasbrouck
pathways: [execution-market-making, market-making-lob, price-impact-execution, market-simulation]
version: Joel Hasbrouck, Empirical Market Microstructure: The Institutions, Economics, and Econometrics of Securities Trading, Oxford University Press, 2007 (ISBN 978-0-19-530164-9); local PDF with a text layer, outside the repository (printed page = PDF page - 11)
sections: secs. 3.2, 3.4, 4.4-4.5, 9.6-9.8.1 (pp. 87-92, page image of p. 91; slice 9), 5.4.2, 5.5, 8.1-8.7, chap. 11, secs. 14.2.2 and 14.3.3 (pp. 24-27, 29-30, 38-39, 49, 53, 67-75, 106-117, 148, 150-151; checked for migration slices 3 to 5); sec. 9.7, pp. 89-90; sec. 15.2.3, pp. 163-164; note 1 to chap. 4 and note 1 to chap. 9, p. 180 (slice 33); slice 35: chap. 1, secs. 1.1-1.3 (pp. 3-6), chap. 2, sec. 2.4 (pp. 17-19); slice 36: chap. 10, secs. 10.2-10.3 and the data discussion that follows (pp. 99-105)
read:
status: draft
---

Prepared on 2026-10-15 by migration slice 3 from source checks, not from study: the headings that need your own reading are left empty. The book is a required reading of the section overview route `execution-market-making`, not of `market-making-lob`. A second local file under Hasbrouck's name is his 2004 lecture-notes draft, not this book, and was not used.

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- Fundamental value or efficient price: the expectation of the payoff conditional on all public information, a martingale with respect to those information sets; trade prices usually are not martingales (sec. 3.2, pp. 25–26).
- Roll model: $p_t=m_t+cq_t$, $\gamma_0=2c^2+\sigma_u^2$, $\gamma_1=-c^2$, $c=\sqrt{-\gamma_1}$ (sec. 3.4, eqs. (3.3)–(3.5), pp. 29–30); PCO example and violated assumptions (p. 30).
- Biases: autocorrelated signs bias $\hat c$ down, signs correlated with $u_t$ bias it up (Exercises 4.2–4.3, pp. 38–39); positive sample autocovariances are not uncommon (sec. 4.5, p. 39).
- Sequential trade with a cost $c$: $A=\mathbb{E}[V\mid\text{buy}]+c$, $B=\mathbb{E}[V\mid\text{sell}]-c$; quotes martingales, trade prices not (sec. 5.4.2, p. 49).
- Generalized Roll model: spread $2(c+\lambda)$, $\gamma_0=c^2+(c+\lambda)^2+\sigma_u^2$, $\gamma_1=-c(c+\lambda)$; prices alone do not identify $\lambda$ and $c$, only $\lambda^2+\sigma_u^2$ (secs. 8.2–8.3, pp. 67–69).
- Random-walk decomposition $p_t=m_t+s_t$: only $\sigma_w^2=\theta(1)^2\sigma_\varepsilon^2$ is identified, the pricing-error variance has a lower bound (sec. 8.6, eqs. (8.8)–(8.13), pp. 72–74); long-horizon variance per unit time approximates $\sigma_w^2$ (p. 69); variance ratios (sec. 8.7, eq. (8.14), pp. 74–75); lagged adjustment gives positive autocorrelation (Exercise 8.2, p. 74).
- Stoll's CARA dealer bid $B=\mu_X-(2n+1)\alpha\sigma_X^2/2$, and $P-\alpha\sigma_X^2/2$ at the optimum; two-security version (sec. 11.2, eqs. (11.2)–(11.3), pp. 110–111). Garman ruin and Amihud–Mendelson quotes (secs. 11.1.1–11.1.2, pp. 107–109).
- Inventory versus information: same short-run response, information permanent; NYSE specialist inventories explain little of quote dynamics (sec. 11.4, p. 115).
- Effective cost $p_t-m_t$ = realised cost $p_t-m_{t+5}$ + $(m_{t+5}-m_t)$ for a buy, Rule 605 (sec. 14.2.2, eq. (14.2), p. 148); time-stamp and sign-inference problems (sec. 14.3.3, pp. 150–151).

## Limits

## Implementation

## Notation map

- $c\to S/2$ (per-side cost, half the spread); $q_t\to Q_t$ (trade sign); risk aversion $\alpha\to\gamma$ in `mod:inventory-based-quotes`; $\lambda$ here is the information cost per trade, not a Poisson intensity.

## Connections

- `alpha-harris` gives the practitioner account of the same spread components, measures and Roll estimator; `catalogue-0496` gives the Ho–Stoll account that chap. 11 omits.

## Entries

`def:spread-measures`, `res:roll-spread-estimator`, `res:spread-component-identification`, `mod:inventory-based-quotes`, `def:volatility-components`; also cited in `res:adverse-selection-spread-component`, `def:fundamental-value` and `meth:order-flow-impact-regression` (contrast with Harris's fundamental value).

Slice 33: `meth:trade-sign-classification`, `def:market-clocks-durations`, `ev:high-frequency-stylised-facts` (intraday seasonality note).

Slice 35: `def:market-functions` (Walrasian price, p. 4), `def:liquidity-dimensions` (depth, breadth and resiliency, pp. 4-5; breadth as many participants, unlike Harris's width), `def:trader-motives` (reversible liquidity roles, p. 5), `mech:venue-competition-fragmentation` (the liquidity externality as a network externality, p. 5), `def:trading-sessions-execution-systems` (auctions, fixings, random stops and deadlines, pp. 17-18), `meth:venue-market-share` (uses of closing prices, p. 18).

Slice 36: `mech:venue-competition-fragmentation` (price discovery across venues, the VECM and information shares, chap. 10, pp. 99-102) and `data:market-data-levels` (time aggregation, timestamp quality and sequencing across markets, the public-awareness time, pp. 104-105).

## Open questions

## Retrieval cards
