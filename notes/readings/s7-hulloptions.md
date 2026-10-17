---
key: s7-hulloptions
pathways: [volatility-options, rates-credit-mortgages, commodity-hedging, futures-execution]
version: John C. Hull, Options, Futures, and Other Derivatives, 11th Global edition, Pearson Education Limited, Harlow, 2022 (ISBN 9781292410654; eBook 9781292410623), copyright 2022, adapted from the U.S. 11th edition (ISBN 9780136939979). Matches the catalogue entry (11th Global edition, published 2021, copyright 2022, ISBN 9781292410654), which warns that Global and U.S. paginations differ. Copy used: a local PDF outside the repository with a text layer (printed page = PDF page - 1); 881 PDF pages
sections: chap. 1 "Introduction", pp. 23-33; chap. 2 "Futures Markets and Central Counterparties", pp. 46-57 and 62-65; chap. 3 "Hedging Strategies Using Futures", pp. 70-90; chap. 4 "Interest Rates", pp. 98-119; chap. 5 "Determination of Forward and Futures Prices", pp. 124-145; chap. 6 "Interest Rate Futures", pp. 152-155. Text layer, read for migration slice 31; Figures 2.1 (p. 51) and 3.3 (p. 81) viewed as page images: the two legacy PNGs reproduce them. Author errata not checked; third batch of 2026-10-17: secs. 7.2 and 7.6, pp. 175 and 183-185 (Example 7.1 reproduced), secs. 15.6 and 15.8 with Example 15.6, and Table 19.6, for `mod:multi-curve-fra-swap-valuation` and `mod:black-scholes-merton`; fourth batch of 2026-10-17: sec. 4.9, p. 111, footnote 4 (start-settled FRA payment discounted at the fixing), for the settlement-convention correction of `mod:multi-curve-fra-swap-valuation`
read:
status: draft
---

Prepared on 2026-10-15 by migration slice 31 from source checks, not from study: the headings that need your own reading are left empty. The legacy Hull notes (`volatility-options/basic.tex` and `fwdfut.tex`) follow these chapters closely, but their edition is not recorded.

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- A call is the right to buy, a put the right to sell; options cost a premium, forwards and futures nothing beyond margin (p. 31). Forward payoff $S_T-K$ long (p. 29).
- Futures specification, price and position limits, convergence (pp. 48-51); margin accounts, maintenance margin about 75% of initial, clearing-member margin on a net basis, about 99% coverage, guaranty fund (pp. 51-54); CCPs and bilateral CSA clearing, 2016 margin rules, interest on margin, haircuts (pp. 54-57); forward against futures (pp. 64-65).
- Hedges and basis, effective price $F_1+b_2$, cross-hedge basis components, $S_2^*-F_2$ and $S_2-S_2^*$ (p. 77), all at a hedge ratio of 1.0, natural for the same asset and "not always optimal" in a cross hedge (p. 79) (pp. 70-79); minimum-variance hedge ratio $\rho\sigma_S/\sigma_F$, Example 3.3 (0.78, 37 contracts), daily settlement, tailing by 1.05 (pp. 79-83); beta hedges (pp. 84-89); stack and roll, Metallgesellschaft (pp. 89-90).
- Rate types; EFFR as a weighted average of brokered rates (p. 99; superseded since 2016, see `exp-sofr-data`); SOFR a volume-weighted median (p. 99); reference rates backward-looking (p. 101); compounding (pp. 101-104); zero rates, bond pricing, par yield, bootstrap (pp. 104-108); forward rates and instantaneous forward (pp. 109-110); FRA valued at the present value of $\tau(R_K-R_F)L$ (pp. 110-112; Example 4.3 prints 369,200, exact 369,247; the p. 111 LIBOR example reverses the payment direction: Party A, receiving fixed 3% with LIBOR at 3.5%, pays rather than receives \$125,000; errata not checked); duration, modified duration, convexity (pp. 112-117); term-structure theories (pp. 117-119).
- Investment against consumption assets; forward prices with income, yield, storage; value of a forward; forward against futures prices; index arbitrage; interest rate parity; convenience yield; cost of carry (pp. 124-144).
- U.S. day counts and quotes (pp. 152-155).

## Limits

## Implementation

## Notation map

## Connections

## Entries

`def:derivative-contracts`, `res:cost-of-carry-forward-price` (`volatility-options`); `def:interest-rate-measures`, `mod:forward-rates-fra`, `mod:duration-convexity`, `conv:us-rate-quotation`, `mech:otc-clearing-collateral` (`rates-credit-mortgages`); `def:futures-hedge-basis`, `mod:minimum-variance-hedge-ratio` (`commodity-hedging`); the slice-31 merge into `mech:futures-margin-settlement` (`futures-execution`).

## Open questions

- Hull's EFFR description is pre-2016; check the author errata and the U.S. 11th edition for other dated rate descriptions.
