---
key: s7-kissellscience
pathways: [execution-trading-costs, market-structure-execution-quality]
version: Robert Kissell, The Science of Algorithmic Trading and Portfolio Management, Academic Press (Elsevier), copyright 2014, ISBN 978-0-12-401689-7; the catalogue cites it as 2013. Local PDF with a text layer, outside the repository (printed page = PDF page - 19); identity checked from the title page, copyright page and ISBN, not the file name
sections: chap. 1, pp. 16-19 (algorithm classes and types, basket algorithms and the risk-aversion parameter; pp. 18-19 for execution algorithms review); chap. 3, pp. 87-96 (best execution, ten cost components, classification, pre-, intra- and post-trade analysis; transaction-cost analysis review), pp. 110-113 (index-adjusted cost and z-scores, page image of p. 112; transaction-cost analysis review), pp. 97-108 (cost conventions, implementation shortfall, arrival cost, benchmark, VWAP and participation-weighted price performance), page images of pp. 100, 103 and 105 (checked for migration execution benchmarks / transaction-cost analysis reviews)
read:
status: draft
---

Prepared on 2026-10-15 by migration execution benchmarks review from source checks, not from study: the headings that need your own reading are left empty. The book is in the catalogue but on no route's required list; it was used because Perold's paper (`wide-perold-shortfall`) was not available.

## Question and claim

## Mechanism

## Method

- Implementation shortfall as paper minus actual return (eqs. (3.1)–(3.4), pp. 97–99); complete execution; Perold's execution and opportunity costs (pp. 100–101); Wagner's expanded form with delay, trading and opportunity parts, and the market-activity form (eqs. (3.5)–(3.8), pp. 101–104); arrival cost in currency and basis points with signed quantities (eqs. (3.9)–(3.11), p. 105).
- Benchmark, VWAP (full day, interval, to end of day) and participation-weighted price performance (eqs. (3.12)–(3.16), pp. 105–108).

## Data and timing

## Key results

- Worked examples recomputed with exact arithmetic: \$2,600 for a complete fill; \$3,080 for a partial fill, split as 2,000 execution, 1,000 opportunity and 80 fees (Perold) or 1,250 delay, 1,000 trading, 750 opportunity and 80 fees (Wagner) (pp. 99–103).
- Ten unbundled cost components and their classification (Tables 3.1–3.2, pp. 89–95); market impact as an unobservable counterfactual (pp. 91–92); cost measure against forecast; VWAP comparison as performance, close as tracking error (pp. 95–96); best execution as a process judged on the information available at the start (p. 88).
- Index-adjusted cost (3.21)–(3.22) and z-scores (3.23)–(3.24), tested by order size and strategy on shares traded, with the investor's own pre-trade model (pp. 110–113).
- Basket algorithms manage cost against total basket risk, with cash-balancing, self-financing and participation constraints; brokers scale the risk-aversion parameter differently (pp. 18–19).
- Algorithm types: VWAP follows the volume curve, TWAP trades evenly in time, POV trades a fixed fraction of volume without guaranteed completion; arrival-price and implementation-shortfall algorithms are cost–risk optimisations whose meaning varies across brokers (chap. 1, pp. 16–18).

## Limits

- Own checks: the intermediate actual return for a partial fill adds fees instead of subtracting them (p. 100); eq. (3.10) divides by the signed $(\sum s_j)P_0$ and so reverses the sign for sells, unlike (3.11); eq. (3.16) has no side factor. Eq. (3.22) leaves the index cost unsigned by side, which mis-adjusts sells; "Index VWAP = 1/2 R_m" approximates the index cost, not the index VWAP (p. 112). TWAP is described as "a constant participation rate" but means a constant rate in time (p. 17).

## Implementation

## Notation map

- $S$, $s_j$, $p_j$, $P_d$, $P_0$, $P_n$, $\bar P$ (the book's $P_{avg}$) as in `def:implementation-shortfall`.

## Connections

- Attributes the execution-and-opportunity formula to Perold (1988) and the expanded form to Wagner (1975, 1991) and Wagner and Edwards (1993), none consulted.

## Entries

`def:implementation-shortfall`, `def:execution-benchmark`, `def:transaction-costs`, `meth:transaction-cost-analysis`; also cited in `def:trading-envelope`, `def:portfolio-trading`, `def:best-execution` and `def:broker-agency-conflicts`.

## Open questions

- Are the sign slips in (3.10) and on p. 100 corrected in `wide-kissell-methods` (2021)?

## Retrieval cards
