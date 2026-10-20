---
key: s7-hulloptions
pathways: [volatility-options, rates-credit-mortgages, commodity-hedging, futures-execution, common-toolkit]
version: John C. Hull, Options, Futures, and Other Derivatives, 11th Global edition, Pearson Education Limited, Harlow, 2022 (ISBN 9781292410654; eBook 9781292410623), copyright 2022, adapted from the U.S. 11th edition (ISBN 9780136939979). Matches the catalogue entry (11th Global edition, published 2021, copyright 2022, ISBN 9781292410654), which warns that Global and U.S. paginations differ. Copy used: a local PDF outside the repository with a text layer (printed page = PDF page - 1); 881 PDF pages
sections: chap. 1 "Introduction", pp. 23-33; chap. 2 "Futures Markets and Central Counterparties", pp. 46-57 and 62-65; chap. 3 "Hedging Strategies Using Futures", pp. 70-90; chap. 4 "Interest Rates", pp. 98-119; chap. 5 "Determination of Forward and Futures Prices", pp. 124-145; chap. 6 "Interest Rate Futures", pp. 152-155. Text layer, read for derivatives and hedging review; Figures 2.1 (p. 51) and 3.3 (p. 81) viewed as page images. Author errata not checked; empirical extensions (2026-10-17): secs. 7.2 and 7.6, pp. 175 and 183-185 (Example 7.1 reproduced), secs. 15.6 and 15.8 with Example 15.6, and Table 19.6, for `mod:multi-curve-fra-swap-valuation` and `mod:black-scholes-merton`; derivatives and empirical validation (2026-10-17): sec. 4.9, p. 111, footnote 4 (start-settled FRA payment discounted at the fixing), for the settlement-convention correction of `mod:multi-curve-fra-swap-valuation`; first foundation slice (2026-10-18): sec. 4.8, pp. 109-110 (forward rates and locking them in), sec. 11.4, pp. 255-256 (put-call parity, eq. (11.6)), sec. 13.1, pp. 288-290 (one-step binomial replication) read in a second local copy of the same Global 11th edition outside the repository (SHA-256 36748bb660c075cad059b3f6ca2b648b185ecbc866a3291e30cca272a345ba8e, printed page = PDF page - 1); time-value correction (2026-10-18): sec. 4.8, p. 110 and Business Snapshot 4.1, p. 111 reread (dated forward lending and borrowing; rolling short borrowing as a yield-curve play); statistics slice (2026-10-18): sec. 15.1, pp. 339-340 (lognormal property, eqs. (15.4)-(15.5), Example 15.2); inference and simulation slice (2026-10-18): sec. 21.6, pp. 489-494 (Monte Carlo simulation, standard error, Examples 21.7-21.8), sec. 22.2, pp. 517-521 (historical simulation, scenario formula, weighting observations); regression slice correction (2026-10-18): chap. 22, sec. 22.2, p. 517 with n. 2 (fifth-highest loss and its alternatives), p. 520 (historical-simulation ES) and p. 521 (weighting observations) reread; fixed-income and derivatives batch (2026-10-18), second local copy: chap. 1, secs. 1.1-1.10, pp. 23-41 (exchange and OTC markets, reforms, market size, hedgers, speculators, arbitrageurs, dangers, Business Snapshots 1.1-1.4); secs. 4.6-4.7, pp. 105-108; secs. 5.4-5.9, pp. 127-137 (Examples 5.1-5.4; sec. 5.8 forward against futures prices, p. 135); chap. 6, pp. 154-167 (cash and quoted bond prices, conversion factors, cheapest to deliver, Examples 6.1-6.3, SOFR futures, convexity adjustment); chap. 7, pp. 172-200 (reasons for swaps, valuation, value through time and Figure 7.9, currency swaps and Examples 7.2-7.3, credit risk, CDS, Business Snapshot 7.2); sec. 8.2, p. 209; secs. 10.1-10.7, pp. 227-238 (option positions, moneyness, intrinsic and time value, naked-option margin); secs. 11.3-11.4, pp. 252-257; sec. 13.2, pp. 292-293; sec. 22.9, pp. 534-537 (principal components of rate moves, Table 22.9); sec. 25.1, pp. 587-591; sec. 34.4, pp. 777-778 (equity swaps). Slips found: Example 6.3 subtracts \$197,000 for \$197,500 and computes \$102,250 for \$102,500; Examples 7.2-7.3 print 0.9629 where Hull's own inputs give 0.9628; the PCA standard deviation 25.45 matches neither the printed (25.40) nor the unrounded (25.50) loadings; correction pass on PR #24 (2026-10-18), same second copy: sec. 6.3, pp. 162-163 reread (Example 6.3 borrows at three-month SOFR plus 200 basis points for three months from 16 December 2021, accrues 0.25 of a year, and locks 2.01 percent from the 99.990 quote); sec. 34.4, pp. 777-778 reread (p. 778 gives the value of the next equity cash flow as L(E - E0)/E0, which omits discounting of the notional; Technical Note 19, read as `hull-tn19`, gives the swap value L E/E0 - L(1 + R0 tau0)/(1 + R tau), whose equity part is L E/E0 - L/(1 + R tau)); derivatives, portfolio and execution batch (2026-10-19), second local copy: chap. 3, sec. 3.5, pp. 85-88 (beta hedge and changing beta); chap. 6, sec. 6.1, pp. 152-153 (day counts), sec. 6.4, pp. 166-167 (duration-based hedge, Example 6.5); chap. 11, pp. 247-264 (value drivers, bounds, put-call parity and Table 11.3, American bounds); chap. 12, pp. 269-284 (covered call, protective put, spreads, calendar spreads, straddles); chap. 13, pp. 288-303 (one- and two-step trees, American puts; Hull's 4.1923 and 5.0894 use p rounded, exact 4.1927 and 5.0896); chap. 15, sec. 15.11, pp. 358-359 (implied volatility, VIX futures Example 15.8); chap. 17, secs. 17.2 and 17.5, pp. 387-388 and 394-395 (range forward, currency options); chap. 18, pp. 405-409 (futures-option parity, Black's model, Examples 18.5-18.7); chap. 19, pp. 421-438 (delta hedging, Tables 19.2-19.4, gamma, vega; the simulated performance measure falls as the square root of the rebalancing interval below Hull's 0.16 and 0.13 at half- and quarter-week intervals); chap. 20, sec. 20.3, pp. 456-458 (equity skew); chap. 26, sec. 26.1, p. 615 and sec. 26.16, pp. 629-632 (zero-cost collar, variance and volatility swaps, Examples 26.4-26.5); chap. 27, sec. 27.4, pp. 650-653 (convertible tree, 107.44); chap. 29, pp. 694-702 (caplet Example 29.3, swaption Example 29.4, cap-floor parity); chap. 31, secs. 31.1-31.2, pp. 719-725 (short-rate models, Example 31.1); chap. 32, sec. 32.1, pp. 732-736 (no-arbitrage models); credit, time-series and valuation batch (2026-10-20): chap. 8 pp. 201-206 (securitisation, ABS waterfall, ABS CDO, Table 8.1); chap. 25 pp. 587-598 (CDS, implied hazard, binary CDS, indices, fixed coupons, Example 25.1)
read:
status: draft
---

Prepared on 2026-10-15 by derivatives and hedging review from source checks, not from study: the headings that need your own reading are left empty.

Also used by the credit, time-series and valuation batch (2026-10-20) for `def:cds-contract-features`, `meth:cds-pricing`, `def:securitisation-process`, `meth:abs-structures-credit-enhancement`.

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

- Example 25.1 reproduced: hazard 0.572% (Hull 0.5717%), duration 4.447, price 100.27; implied hazard 1.63% for 100 bp; binary CDS 205 bp (pp. 594-596).
- Table 8.1 reproduced: ABS CDO senior loses 28.2% at 13% asset losses and 69.2% at 17% (p. 205).

## Limits

## Implementation

## Notation map

## Connections

## Entries

`def:derivative-contracts`, `res:cost-of-carry-forward-price` (`volatility-options`); `def:interest-rate-measures`, `mod:forward-rates-fra`, `mod:duration-convexity`, `conv:us-rate-quotation`, `mech:otc-clearing-collateral` (`rates-credit-mortgages`); `def:futures-hedge-basis`, `mod:minimum-variance-hedge-ratio` (`commodity-hedging`); the derivatives and hedging review merge into `mech:futures-margin-settlement` (`futures-execution`).

## Open questions

- Hull's EFFR description is pre-2016; check the author errata and the U.S. 11th edition for other dated rate descriptions.
