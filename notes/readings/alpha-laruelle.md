---
key: alpha-laruelle
pathways: [execution-market-making, hft-market-design]
version: Charles-Albert Lehalle and Sophie Laruelle (eds.), Market Microstructure in Practice, 2nd ed., World Scientific, 2018 (ISBN 9789813231122; DOI 10.1142/10739); local PDF with a text layer, outside the repository (printed page = PDF page - 27)
sections: chap. 2, secs. 2.2, 2.3.1, 2.5-2.5.2 (pp. 143-151, 169-184); app. A, secs. A.5 and A.10 (pp. 261-266, 292-298); page images for p. 172 and pp. 262-266 (checked for migration slice 4)
read:
status: draft
---

Prepared on 2026-10-15 by migration slice 4 from source checks, not from study: the headings that need your own reading are left empty. `notes/log.md` records the book as completed before the study method; it is in the catalogue but on no route's required list.

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- Four liquidity variables: volume, spread, volatility, book size; their intraday seasonality, high after the open (Figure 2.12, pp. 145–148); at a one-tick spread, book size adjusts instead of the spread (p. 148).
- Cross-sectional spread relation $\psi_i=a+b\sigma_i/\sqrt{N_i}$ for small-tick instruments, with a bounce term $\eta=N_c/(2N_a)$ for large-tick ones (eq. (2.1), pp. 144–145).
- Daily spread rises with daily volatility (Figure 2.13, pp. 150–151); spread on volatility in levels and logs, with the log-normal back-transformation (app. A.10.2, pp. 295–298; Rio Tinto, $R^2$ 0.24, 0.16, 0.11).
- Garman–Klass volatility normalised by the average price (p. 172, page image); used for seasonality and for the FTSE 100 / IBEX 35 comparison, which found no significant effect of UK fragmentation on intraday volatility (pp. 146–147, 172–174).
- Number of trades per day as a proxy for HFT activity (Figure 2.25, p. 171).
- Flash Crash account: volume-following sell algorithm, hot-potato trading between futures and equities, paused orders, internalised retail flow routed to the market, NYSE LRPs, post-crash rules (sec. 2.5.2, pp. 177–183).
- Toy model of the Flash Crash: overflow $r_t=F_t-\bar F$, impact $I=1/D$ with $dI_t/I_t=\sigma_IdW_t+r_tdt$ (A.12), price $dP=\sigma_PdW^P+I^+dR^+-I^-dR^-$ (A.13), hot-potato rate $r_t\simeq(1-\rho^t)r_0/(1-\rho)$; the explicit solution (A.14) has a $t^2$ exponent that does not follow from $R_t\simeq tr_0/(1-\rho)$ (own check, open) (app. A.5, pp. 261–266).

## Limits

## Implementation

## Notation map

- $\psi\to\psi$ (spread); open, high, low, close $\to p^O,p^H,p^L,p^C$ (the compendium's $C$ is the transaction-cost component).

## Connections

- `alpha-harris` chaps. 14 and 20 give the theory behind the spread–volatility relation and the fundamental/transitory split; `s6-hasbrouck` chap. 8 gives the econometrics.
- The Flash Crash material leads to `w5-kirilenko-flash-crash` and `w5-menkveld-yueshen-flash` (`hft-market-design`), which the book cites.

## Entries

`meth:garman-klass-volatility`, `meth:spread-volatility-regression`; also cited in `res:spread-determinants`.

## Open questions

- Is (A.14) a misprint for an exponent linear in $t$, or does the model intend $dI_t/I_t$ to depend on $R_t$ rather than $r_t$?

## Retrieval cards
