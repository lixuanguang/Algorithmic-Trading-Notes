---
key: wide-budish-cramton-shim
pathways: [hft-market-design]
version: Eric Budish, Peter Cramton and John Shim, "The High-Frequency Trading Arms Race: Frequent Batch Auctions as a Market Design Response", Quarterly Journal of Economics 130(4), 1547-1621, 2015 (DOI 10.1093/qje/qjv027), matching the catalogue. Copy used: the published open-access (CC BY-NC-ND) PDF hosted by the University of Maryland economics department, downloaded 2026-10-15; text layer, printed page = PDF page + 1546
sections: abstract and sec. I (pp. 1547-1556); sec. VI.A-VI.E (pp. 1576-1592), with page images of pp. 1589-1590 (checked for migration slice 15). Secs. II-V (data and empirical analysis) and VII-VIII (frequent batch auctions) not read
read:
status: draft
---

Prepared on 2026-10-15 by migration slice 15 from source checks, not from study: the headings that need your own reading are left empty.

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- Model (sec. VI.A, pp. 1576–1579): value of $x$ perfectly correlated with a public signal $y$ (compound Poisson jumps, rate $\lambda_{\mathrm{jump}}$, absolute size $J$); costless liquidation; investors arrive at rate $\lambda_{\mathrm{invest}}$ with unit demand; risk-neutral trading firms; simultaneous messages processed serially in random order.
- Exogenous entry (sec. VI.B, Proposition 1, pp. 1579–1583): one liquidity provider and $N-1$ snipers; the provider is sniped with probability $(N-1)/N$; eq. (3) $\lambda_{\mathrm{invest}}s/2=\lambda_{\mathrm{jump}}\Pr(J>s/2)\mathbb E[J-s/2\mid J>s/2]$, independent of $N$.
- Thin markets (Proposition 2, pp. 1583–1585): spreads rise with each unit of depth, under the assumption that investors trade their whole quantity at once.
- Endogenous speed investment (sec. VI.D, Proposition 3, pp. 1588–1591): zero-profit conditions eqs. (5)–(6); eq. (7) $\lambda_{\mathrm{invest}}s^*/2=N^*c_{\mathrm{speed}}$ (rederived: (5) plus $N-1$ times (6)); heterogeneous speed costs leave inframarginal firms positive profits (n. 27). Prisoner's dilemma (Proposition 4, p. 1591); comparative statics of the prize (Proposition 5, p. 1592).
- Evidence as summarised in sec. I (pp. 1552–1553): ES–SPY, 2005–2011; median correlation 0.1016 at 10 ms and 0.0080 at 1 ms; median arbitrage duration 97 ms (2005) to 7 ms (2011); median profit about 0.08 index points per unit, roughly constant; frequency driven by volatility; prize about \$75 million a year.
- The authors do not claim markets are less liquid than before HFT (n. 5, pp. 1554–1555).

## Limits

## Implementation

## Notation map

- $\lambda_{\mathrm{jump}},\lambda_{\mathrm{invest}}$ are arrival rates, declared in the notation overrides; $s$ is the full spread.

## Connections

- `alpha-laruelle` sec. 2.4.2 (pp. 161–162) describes competition among high-frequency market makers pushing them into less liquid stocks.

## Entries

`res:latency-arbitrage-arms-race`.
