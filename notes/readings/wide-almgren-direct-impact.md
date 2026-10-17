---
key: wide-almgren-direct-impact
pathways: [price-impact-execution]
version: Robert Almgren, Chee Thum, Emmanuel Hauptmann and Hong Li, "Direct Estimation of Equity Market Impact", Risk 18(7), 58-62, July 2005 (catalogue record). Copy used: the authors' preprint dated 10 May 2005, 26 pages, downloaded 2026-10-15 from a Wayback Machine snapshot (8 August 2017) of www.cims.nyu.edu/~almgren/papers/costestim.pdf, because the live author link returned an error. Page numbers below are the preprint's; the published version was not compared
sections: secs. 1-4.3 (pp. 3-22), page images of pp. 19 and 21 (checked for impact estimation review)
read:
status: draft
---

Prepared on 2026-10-15 by impact estimation review from source checks, not from study: the headings that need your own reading are left empty. Distinct from `alpha-almgren` (Almgren and Chriss, the execution framework this paper fits).

## Question and claim

## Mechanism

## Method

- Pre-trade midpoint $S_0$, realised average price $\bar S$, post-trade midpoint $S_{\mathrm{post}}$ half an hour after the last fill; $I=(S_{\mathrm{post}}-S_0)/S_0$, $J=(\bar S-S_0)/S_0$ (pp. 9–10); volume time (p. 10); temporary impact $J-I/2$ (eq. (2), p. 15); fits (7)–(8) with heteroskedastic weights (p. 19, page image).

## Data and timing

- Citigroup US equity orders, December 2001 to June 2003; 682,562 orders, 29,509 after filters (S&P 500, volatility below 12.5%, no MOO/MOC/VWAP, no fills after 4:10 pm, at least two transactions, 1,000 shares and 0.25% of ADV) (pp. 5–8).

## Key results

- $\alpha=0.891\pm0.10$, $\delta=0.267\pm0.22$, $\beta=0.600\pm0.038$; square root rejected at 95%; fixed $\alpha=1$, $\delta=1/4$, $\beta=3/5$; $\gamma=0.314\pm0.041$, $\eta=0.142\pm0.0062$; $R^2$ below 1% (pp. 20–21, page image of p. 21).
- No consistent dependence on the bid–ask spread (p. 19).
- Table 3 example (p. 22), recomputed and matching to rounding.

## Limits

## Implementation

## Notation map

- The paper's $I$, $J$, $\gamma$, $\eta$ are local to `meth:almgren-impact-estimation`.

## Connections

- Linear permanent impact preferred as the only arbitrage-free form, citing Huberman and Stanzl (2004), not consulted (p. 16).

## Entries

`meth:almgren-impact-estimation`; also cited in `ev:square-root-impact`.

## Open questions

- Compare with the published Risk version, and check whether "permanent" measured half an hour after the last fill is stable to longer horizons.

## Retrieval cards
