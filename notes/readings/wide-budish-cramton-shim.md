---
key: wide-budish-cramton-shim
pathways: [hft-market-design]
version: Eric Budish, Peter Cramton and John Shim, "The High-Frequency Trading Arms Race: Frequent Batch Auctions as a Market Design Response", Quarterly Journal of Economics 130(4), 1547-1621, 2015 (DOI 10.1093/qje/qjv027), matching the catalogue. Copy used: the published open-access (CC BY-NC-ND) PDF hosted by the University of Maryland economics department, downloaded 2026-10-15; text layer, printed page = PDF page + 1546
sections: abstract and sec. I (pp. 1547-1556); sec. VI.A-VI.E (pp. 1576-1592), with page images of pp. 1589-1590 (checked for migration high-frequency strategies review). Secs. VII-VIII (frequent batch auctions and alternatives, pp. 1594-1611) read in the source follow-up of 2026-10-16, with the September 2013 NBER conference version's sec. 7.1 and n. 33 for comparison; secs. II-V (data and empirical analysis) not read
read:
status: draft
---

Prepared on 2026-10-15 by migration high-frequency strategies review from source checks, not from study: the headings that need your own reading are left empty.

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- Model (sec. VI.A, pp. 1576–1579): value of $x$ perfectly correlated with a public signal $y$ (compound Poisson jumps, rate $\lambda_{\mathrm{jump}}$, absolute size $J$); costless liquidation; investors arrive at rate $\lambda_{\mathrm{invest}}$ with unit demand; risk-neutral trading firms; simultaneous messages processed serially in random order.
- Exogenous entry (sec. VI.B, Proposition 1, pp. 1579–1583): exactly one unit quoted at each of $y\pm s/2$, the bid and ask belonging to one firm or to two (Proposition 1(i), p. 1583); the authors let one firm play liquidity provider for simplicity, with equivalent equilibria in which the role rotates (pp. 1579–1580); a stale quote is sniped with probability $(N-1)/N$ (Proposition 1(iii)); eq. (3) $\lambda_{\mathrm{invest}}s/2=\lambda_{\mathrm{jump}}\Pr(J>s/2)\mathbb E[J-s/2\mid J>s/2]$, independent of $N$.
- Thin markets (Proposition 2, pp. 1583–1585): spreads rise with each unit of depth, under the assumption that investors trade their whole quantity at once.
- Endogenous speed investment (sec. VI.D, Proposition 3, pp. 1588–1591): zero-profit conditions eqs. (5)–(6); eq. (7) $\lambda_{\mathrm{invest}}s^*/2=N^*c_{\mathrm{speed}}$ (rederived: (5) plus $N-1$ times (6)); heterogeneous speed costs leave inframarginal firms positive profits (n. 27). Prisoner's dilemma (Proposition 4, p. 1591); comparative statics of the prize (Proposition 5, p. 1592).
- Evidence as summarised in sec. I (pp. 1552–1553): ES–SPY, 2005–2011; median correlation 0.1016 at 10 ms and 0.0080 at 1 ms; median arbitrage duration 97 ms (2005) to 7 ms (2011); median profit about 0.08 index points per unit, roughly constant; frequency driven by volatility; prize about \$75 million a year.
- The authors do not claim markets are less liquid than before HFT (n. 5, pp. 1554–1555).
- Batch auctions (sec. VII.A, p. 1596): rationing at the clearing price by whole batch intervals outstanding; within a batch, same priority and random (pro rata) tie-breaks. The 2013 working paper: earlier batches first, pro rata within the last, "Time priority is only relevant across batch intervals" (n. 33).
- Speed advantage (sec. VII.B, pp. 1597-1598): relevant only for jumps in a window of length delta, a fraction delta/tau (1/1000 for 100 microseconds and a 100 ms batch); symmetric liquidity providers not sniped; epsilon/(2 tau) with random latency (n. 34). Calibration of tau 10-100 ms or 100 ms-1 s (p. 1606, from an online appendix not read).
- Alternatives (sec. VIII): Tobin taxes, message ratios and resting times, random delays (which do not address sniping), asymmetric delays.

## Limits

## Implementation

## Notation map

- $\lambda_{\mathrm{jump}},\lambda_{\mathrm{invest}}$ are arrival rates, declared in the notation overrides; $s$ is the full spread.

## Connections

- `alpha-laruelle` sec. 2.4.2 (pp. 161–162) describes competition among high-frequency market makers pushing them into less liquid stocks.

## Entries

`res:latency-arbitrage-arms-race`.
