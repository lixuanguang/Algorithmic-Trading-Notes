---
key: rates-credit-mortgages
section: rates-credit-mortgages
status: not started (draft entries only, not from study)
---

# Rates: yield curves, term premia and derivatives (section overview)

Overview outcome, from the guide: connect a rate quote or bond position to its curve, expected policy path, term premium, collateral and hedge-contract assumptions. Its checkpoint builds a cash-flow and risk-assumption sheet for a collateralised swap hedged with SOFR futures and a Treasury note, repriced under level and slope moves, a policy surprise, a term-premium shock and a collateral or funding change. Its readings are `rt-gurkaynak-wright-2012`, `s6-brigo`, `exp-adrian-crump-moench-term-structure`, `gap-rates-sofr-futures-hedging` and `gap-gregory5`.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 15 October 2026 by derivatives and hedging review (`notes/source-review-records.md`). The pathway holds the rates, compounding, forward-rate, duration, quotation and OTC-clearing material from Hull, with time-value formulas. The entries come from source checking against Hull's 11th Global edition (not a reading of this overview), the New York Fed's reference-rate methodology (`exp-sofr-data`) and the CPSS-IOSCO principles (`exp-pfmi`); the time-value formulas are derived, not sourced. None of the overview's readings has been read; the checkpoint was not attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in derivatives and hedging / source review / optimal execution / high-frequency strategies reviews:

- `def:interest-rate-measures`: credit spread; Treasury, overnight and repo rates; EFFR and SOFR methodology (Hull's brokered-average EFFR superseded in 2016 by a volume-weighted median); compounding conversions and EAR (an "expected annual rate" reading corrected); zero rates, bond yields and par yields; annuity and perpetuity values derived, with their timing and limits.
- `mod:forward-rates-fra`: forward and instantaneous forward rates; FRA payoff against present value (discounting restored), settlement timing and the single-curve caveat; term-structure theories as conjectures.
- `mod:duration-convexity`: Macaulay and modified duration and convexity as approximations, checked at plus or minus 200 bp; yield change against parallel curve shift. derivatives and hedging review follow-up, 2026-10-16: the yield moves one for one with a parallel zero-curve shift if and only if the zero rates at all the bond's payment dates equal its yield; a flat curve is sufficient, not necessary (a zero-coupon bond on any curve); counterexamples computed in `trading_notes.numerical.interest_rates.yield_shift_checks`.
- `conv:us-rate-quotation`: U.S. day counts, Treasury bill discount quotes, bond prices in thirty-seconds, clean and dirty prices.
- `mech:otc-clearing-collateral`: CCP and bilateral ISDA/CSA clearing, variation and initial margin, interest on margin, haircuts, and the post-crisis reforms as Hull reports them; CCPs mitigate rather than eliminate counterparty risk.

All partly checked 2026-10-15, draft; human review outstanding.

Written in macro markets and pricing / source review / optimal execution / execution control reviews:

- `def:fixed-income-universe`: the fixed-income segments, Gliner's fixed-income ETF table (Table 9.5) and an unchecked size claim.

Changed in macro markets and pricing review (merges): `mod:forward-rates-fra` (FRA market notation, Gliner's fixing-date and convexity remarks corrected); `mod:duration-convexity` (DV01, a convexity formula that dropped the price corrected, and negative convexity). the topic review other rates entries are owned by `monetary-policy-curve` (`def:central-bank-policy-framework`, `mod:taylor-rule`, `rule:major-central-banks-current`, `meth:policy-path-ois-futures`), `curve-term-structure` (`meth:curve-trades-carry-rolldown`), `rates-inflation` (`def:tips-breakevens`) and `rate-derivatives` (`def:interest-rate-swaps`), all in `compendium/rates-credit-mortgages/monetary-policy-curves.tex`.

Written in empirical extensions (2026-10-17) (source verification and bounded checks, not study or human review):

- `mod:multi-curve-fra-swap-valuation`: FRA and swap valuation with separate projection and discount curves, with own checks (`trading_notes.numerical.rate_swaps_clearing.multicurve_checks`). Partly checked 2026-10-17, draft; human review outstanding.

Written in the fixed-income and derivatives batch (2026-10-18):

In `bond-instruments-markets.tex` (topic `bond-instrument-features`):

- `def:bond-features-indenture`: issuer, maturity, par, coupon, currency and seniority; indenture, trustee, affirmative and negative covenants (Handbook chaps. 1, 10, 11 and 40); the Trust Indenture Act threshold dated (\$50 million since 2015).
- `def:bond-cash-flow-contingencies`: bullet, amortising, sinking-fund, floating, step-up, deferred, PIK and index-linked structures; issuer and holder options (chaps. 1 and 10).
- `rule:bond-issuance-legal-tax`: registration and exemptions, shelf, Rule 144A, tax treatment of municipal and Treasury interest, T+1 settlement and the EU prospectus exemptions, each dated. Corrected 2026-10-19 (second PR #24 pass): exempt original-issue discount, taxable market discount and capital gains distinguished with their basis treatment (IRS Pub. 550 and 1212), with a worked example.
- `def:bond-market-segments-trading`: segments, participants, primary methods and OTC secondary trading against equity markets (chaps. 1 and 7; Bessembinder, Spatt and Venkataraman).
- `meth:corporate-funding-ig-hy`: investment-grade against high-yield funding (chap. 10).
- `def:government-agency-supranational-funding`: sovereign, local, agency and supranational funding and its contrast with corporate issuance (chaps. 1, 7, 8, 9 and 16; IBRD factsheet FY2026). Corrected 2026-10-18 (PR #24 pass): the Treasury noncompetitive limit is $10 million from 8 August 2022 (31 CFR 356.12 and 356.22; 87 FR 40438), not the Handbook's $5 million; the October 2026 amendment leaves it unchanged.

In `bond-pricing-yields.tex` (topic `bond-pricing-yields`):

- `meth:bond-price-from-yield`: full, clean and accrued prices on and between coupon dates; street against Treasury simple-stub pricing (31 CFR 356 App. B); price-yield relations.
- `meth:matrix-pricing`: IFRS 13 B7 and 79(a), with an interpolated example.
- `def:bond-yield-spread-measures`: compounding conversions, current yield, yields to call and worst, G-, I- and Z-spreads on one curve.
- `meth:floating-money-market-yields`: quoted and discount margins, Treasury FRN and bill formulas, money-market conversions. Corrected 2026-10-18 (PR #24 pass): the SOFR FRN example has a dated schedule and business-day SOFR compounding with calendar-day weights (New York Fed methodology); discount margin 96.38 bp.

In `term-structure-returns.tex` (topic `term-structure`):

- `meth:spot-par-forward-curves`: bootstrapping, pricing with spot and forward rates, comparing curves.
- `meth:forward-rates-expected-returns`: forwards as break-evens, realised against expected returns, rolling down the curve (Ilmanen, Handbook chaps. 31-32).
- `def:swap-curve-short-term-spreads`: the swap curve, swap spreads and short-term credit and liquidity spreads, dated.
- `res:term-structure-theories`: expectations (local and unbiased forms, convexity bias), liquidity preference, segmentation and preferred habitat.
- `meth:yield-curve-factor-exposures`: principal components (Hull Table 22.9; GSW month-end data 1986-2026), factor hedges, volatility term structure and economic drivers of views.

In `interest-rate-risk.tex` (topic `interest-rate-risk`):

- `meth:bond-return-decomposition`: coupons, interest on interest, pull to par and rate effect; the Macaulay-duration horizon.
- `meth:yield-duration-pvbp`: Macaulay, modified, approximate and money duration, PVBP and their drivers.
- `meth:convexity-portfolio-duration`: convexity and its scaling, the duration-convexity approximation, portfolio measures and their limits.
- `meth:curve-based-empirical-duration`: effective duration and convexity, key-rate durations, a callable bond and empirical duration. Corrected 2026-10-18 (PR #24 pass): curve and yield measures of an option-free bond are equal only on a flat curve (or for one cash flow); a sloped-curve counterexample gives 10.2186 against 11.2131.

All partly checked 2026-10-18, draft. Examples in `trading_notes.numerical.bond_pricing_yields.bond_valuation_checks` and `trading_notes.numerical.term_structure_returns.term_structure_checks`; human review is outstanding. Coverage records are editorial, not study. The existing `def:interest-rate-measures`, `conv:us-rate-quotation`, `mod:forward-rates-fra`, `mod:duration-convexity`, `meth:curve-trades-carry-rolldown`, `def:interest-rate-swaps` and `mod:multi-curve-fra-swap-valuation` are linked, not repeated; the single-curve examples are labelled and the multi-curve entry keeps the projection and discounting distinction.

Written in the derivatives, portfolio and execution batch (2026-10-19):

In `arbitrage-free-valuation.tex` (topic `arbitrage-free-bond-valuation`):

- `meth:arbitrage-free-bond-valuation`: law of one price on cash flows, spot-curve value of the Handbook's 6.5% bond and the arbitrage at another price; zero-curve against lattice pricing.
- `meth:binomial-rate-tree-calibration`: the lognormal tree, calibration date by date to par bonds, backward induction and pathwise valuation (Handbook chap. 36).
- `mod:term-structure-models-simulation`: Monte Carlo rate paths for path-dependent securities; equilibrium (Vasicek) and no-arbitrage (Ho-Lee) short-rate models.

In `embedded-option-bonds.tex` (topic `embedded-option-bonds`):

- `meth:callable-putable-bond-valuation`: embedded-option types, callable and putable values on the calibrated tree, and the effects of volatility, level and shape.
- `meth:option-adjusted-spread`: OAS against the Z-spread, option cost and the effect of assumed volatility.
- `meth:embedded-option-effective-duration`: effective, one-sided and key-rate durations and effective convexity at constant OAS. Corrected 2026-10-19 (PR #25 pass): convexities in the compendium convention (callable -77.15) beside the Handbook's half-scaled figures.
- `meth:capped-floored-floater-valuation`: capped, floored and collared floaters on the tree (Fabozzi Fixed Income Analysis 2007, chap. 9).
- `meth:convertible-bond-valuation`: convertible features, conversion measures and premiums, Hull's default-adjusted stock tree, and risk-return against the straight bond and stock. Corrected 2026-10-19 (PR #25 pass): Tesla's terms from the 2019 prospectus supplement: no issuer call, a holders' fundamental-change put, a separate make-whole adjustment.

In `fixed-income-portfolio-management.tex` (topic `fixed-income-portfolio-management`):

- `def:fixed-income-mandates-return-model`: roles of bonds, mandate types, portfolio risk measures, liquidity and an expected-return model.
- `meth:bond-leverage-taxation`: leverage through repo, futures, swaps and lending, and taxable against tax-exempt management.
- `meth:liability-matching-ladders`: liability-driven investing, cash-flow matching by linear programming and ladders. Corrected 2026-10-19 (PR #25 pass): the ladder's key-rate profile (0.13 to 0.64) and twist risk (-0.493%) replace the claim of equal key-rate durations; equal-face, equal-market-value and equal-risk allocations compared.
- `meth:immunisation-liabilities`: single- and multiple-liability immunisation, shifts and twists, implementation alternatives and risks (MIP chap. 6).
- `meth:bond-index-exposure-benchmarks`: bond indexes, passive methods and benchmark choice.
- `meth:yield-curve-positioning`: positions for market-consistent, divergent, volatility and cross-currency curve views.
- `meth:curve-strategy-evaluation`: active key-rate durations, scenario returns and expected return and tracking risk.

All partly checked 2026-10-19, draft. Examples in `trading_notes.numerical.embedded_option_bonds.rate_tree_checks` and `trading_notes.numerical.fixed_income_portfolio_management.fixed_income_portfolio_checks`; human review is outstanding. Coverage records are editorial, not study. `meth:curve-based-empirical-duration` is linked, not repeated.

Written in library gap-filling Batch L2 (2026-10-21), in `arbitrage-free-valuation.tex` (topic `arbitrage-free-bond-valuation`):

- `mod:affine-short-rate-models`: the affine bond-price form, Vasicek and CIR closed forms, the Feller condition, Hull-White's theta(t) fitted to the GSW curve of 30 September 2026, exact joint sampling of the rate and its integral, and negative rates.
- `mod:hjm-forward-rate-models`: the HJM drift condition, Ho-Lee and Hull-White as Markov special cases, the forward market model under forward and rolling spot measures, Black caplets and Hull's adjustment for backward-looking rates.
- `mod:term-structure-models-simulation` extended: fitting simulated paths by a time-dependent drift, the lognormal (Black-Karasinski) alternative and Wilmott's caution on refitting.

Partly checked 2026-10-21, draft. Checks in `trading_notes.numerical.arbitrage_free_valuation.short_rate_model_checks` (GSW curve; volatilities illustrative, not calibrated). Sources: Hull, *OFOD* 11th Global ed., chaps. 29 and 31-33; Wilmott, *PWOQF* 2nd ed., chaps. 30, 31 and 37; the Handbook, chap. 37. Human review outstanding. See [record](../source-review-records.md#library-gap-filling-batch-l2-21-october-2026).

## Source verification after macro markets and pricing review

macro markets and pricing review follow-up, 2026-10-16 (source verification, not study): `data:fixed-income-market-size` resolved (SIFMA Fact Book highlights: global fixed-income debt $160.7 trillion and equity market capitalisation $157.8 trillion in 2025; the product-group ranking found ill-posed). Entries corrected in the same follow-up are listed in `notes/source-review-records.md`, *macro markets and pricing review follow-up*.

empirical extensions (2026-10-17) (six audit repairs and a source-review coverage; source verification and bounded tests, not study or human review): `rule:otc-derivatives-reforms` narrowed (U.S. rules resolved (17 CFR 23.150-161, 43.3, 45.3) and merged into `mech:otc-clearing-collateral`; BCBS-IOSCO, prudential regulators and EMIR unread); `mod:multi-curve-fra-swap-valuation` resolved (new entry `mod:multi-curve-fra-swap-valuation` from Hull, with own checks); `ev:term-premia` resolved (Adrian, Crump and Moench and the New York Fed's file summarised and merged into `mod:forward-rates-fra`). The record is in `notes/source-review-records.md`, *empirical extensions (2026-10-17)*.

derivatives and empirical validation (2026-10-17) (seven audit repairs, backlog reconciliation and a source-review coverage; source verification and bounded tests, not study or human review): audit repairs: `mod:multi-curve-fra-swap-valuation` now separates the end-settled swaplet from the start-settled FRA, with the stochastic-valuation conditions and `trading_notes.numerical.rate_swaps_clearing.fra_settlement_checks`. The `conv:fra-rate-multicurve-measure`, `ev:term-premia` and `rule:otc-derivatives-reforms` questions: Bianchetti and Carlicchi's FRA table (end-settled form), Kim and Wright against ACM (correlation 0.86 over 441 months) and the BCBS-IOSCO margin framework merged; `rule:otc-derivatives-reforms` narrowed. The record is in `notes/source-review-records.md`, *derivatives and empirical validation (2026-10-17)*.

## Related entries owned elsewhere

Cross-referenced, not owned here: `def:derivative-contracts`, `res:cost-of-carry-forward-price`, `def:swaps-as-forward-strips`, `meth:rate-bond-forward-valuation`, `meth:swap-valuation-replication` (`volatility-options`); `mech:futures-margin-settlement` (`futures-execution`); `def:return-measures` (`performance-manager-evaluation`); `mod:minimum-variance-hedge-ratio` (`commodity-hedging`); `def:fixed-income-market-structure` (`otc-fixed-income-trading`); `mech:securities-lending-short-sale` (`money-markets-repo-lending`); `def:common-investor-contagion` (`funding-crowding`).

## Specialist pathways

The guide's pathways for this section, in its order, with the existing material or the content gap as recorded by the content migration of 22 October 2026. A pathway with related material but no note has not been opened.

Printed as numbered sections of the chapter, under the guide pinned at `8302467` (`subsection_alignment_plan.md`): `bond-pricing-rate-risk`, `curve-term-structure`, `rate-derivatives`, `monetary-policy-curve`, `bond-risk-premia`, `rates-inflation`. A pathway without entries of its own is not printed; the related material and partial treatments named below are printed under the pathway or section that owns them.

- `bond-pricing-rate-risk` (Bond instruments, pricing, yields and interest-rate risk): added by the guide revision of 22 October 2026 (`8302467`); no pathway note; its entries are in `rates-credit-mortgages/interest-rates`, `rates-credit-mortgages/bond-instruments-markets`, `rates-credit-mortgages/fixed-income-universe`, `rates-credit-mortgages/bond-pricing-yields`, `rates-credit-mortgages/interest-rate-risk`.
- `curve-term-structure` (Yield-curve construction and term-structure models): pathway note [curve-term-structure.md](curve-term-structure.md), 2 entries listed, in `rates-credit-mortgages/curve-trades`, `rates-credit-mortgages/gsw-treasury-curve`.
- `rate-derivatives` (Interest-rate derivatives, volatility and RFR conventions): pathway note [rate-derivatives.md](rate-derivatives.md), 2 entries listed, in `rates-credit-mortgages/rate-swaps-clearing`, `volatility-options/option-pricing`.
- `monetary-policy-curve` (Monetary policy, balance-sheet policy and the yield curve): pathway note [monetary-policy-curve.md](monetary-policy-curve.md), 6 entries listed, in `rates-credit-mortgages/monetary-fiscal-policy`, `rates-credit-mortgages/monetary-policy-curves`.
- `bond-risk-premia` (Bond risk premia, rates strategies and fixed-income portfolio management): no pathway note; related existing material in `rates-credit-mortgages/term-structure-returns`, `rates-credit-mortgages/fixed-income-portfolio-management`, not reviewed as a complete treatment of the pathway. Broadened by the guide revision of 22 October 2026 (`8302467`) to cover fixed-income portfolio management; its entries are in `rates-credit-mortgages/curve-trades`, `rates-credit-mortgages/fixed-income-portfolio-management`.
- `rates-inflation` (Inflation-linked bonds, real yields and breakevens): pathway note [rates-inflation.md](rates-inflation.md), 1 entries listed, in `rates-credit-mortgages/tips-breakevens`.

## Entry backlog

- rule:otc-derivatives-reforms: the U.S. prudential regulators' uncleared-margin rule and EMIR's texts, with scope and dates; the CFTC's rules and the BCBS-IOSCO framework (thresholds and phase-in) are in `mech:otc-clearing-collateral`.

## What changed in my view or practice

## Questions carried forward

- The earlier time-value notes have no recorded source; were they from a CFA curriculum reading?
