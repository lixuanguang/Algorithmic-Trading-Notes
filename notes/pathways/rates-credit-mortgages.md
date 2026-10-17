---
key: rates-credit-mortgages
section: rates-credit-mortgages
status: not started (draft entries from the migration only)
---

# Rates: yield curves, term premia and derivatives (section overview)

Overview outcome, from the guide: connect a rate quote or bond position to its curve, expected policy path, term premium, collateral and hedge-contract assumptions. Its checkpoint builds a cash-flow and risk-assumption sheet for a collateralised swap hedged with SOFR futures and a Treasury note, repriced under level and slope moves, a policy surprise, a term-premium shock and a collateral or funding change. Its readings are `rt-gurkaynak-wright-2012`, `s6-brigo`, `exp-adrian-crump-moench-term-structure`, `gap-rates-sofr-futures-hedging` and `gap-gregory5`.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 15 October 2026 by migration derivatives and hedging review (`notes/source-review-records.md`). The rates, compounding, forward-rate, duration, quotation and OTC-clearing material of the legacy Hull notes (`volatility-options/basic.tex` and `fwdfut.tex`, mapped to the options overview and, for `fwdfut.tex`, to this overview and `commodity-hedging`) was routed here, together with the time-value formulas of the unsourced legacy file `rates-credit-mortgages/01_tvm.tex`. The entries come from source checking against Hull's 11th Global edition (not a reading of this overview), the New York Fed's reference-rate methodology (`exp-sofr-data`) and the CPSS-IOSCO principles (`exp-pfmi`); the time-value formulas are derived, not sourced. None of the overview's readings has been read; the checkpoint was not attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in migration derivatives and hedging / source review / optimal execution / high-frequency strategies reviews:

- `def:interest-rate-measures`: credit spread; Treasury, overnight and repo rates; EFFR and SOFR methodology (Hull's brokered-average EFFR superseded in 2016 by a volume-weighted median); compounding conversions and EAR (the legacy "expected annual rate" corrected); zero rates, bond yields and par yields; annuity and perpetuity values derived, with their timing and limits.
- `mod:forward-rates-fra`: forward and instantaneous forward rates; FRA payoff against present value (the legacy dropped the discounting), settlement timing and the single-curve caveat; term-structure theories as conjectures.
- `mod:duration-convexity`: Macaulay and modified duration and convexity as approximations, checked at plus or minus 200 bp; yield change against parallel curve shift. derivatives and hedging review follow-up, 2026-10-16: the yield moves one for one with a parallel zero-curve shift if and only if the zero rates at all the bond's payment dates equal its yield; a flat curve is sufficient, not necessary (a zero-coupon bond on any curve); counterexamples computed in `notes/artefacts/rates-credit-mortgages/yield-shift-check.py`.
- `conv:us-rate-quotation`: U.S. day counts, Treasury bill discount quotes, bond prices in thirty-seconds, clean and dirty prices.
- `mech:otc-clearing-collateral`: CCP and bilateral ISDA/CSA clearing, variation and initial margin, interest on margin, haircuts, and the post-crisis reforms as Hull reports them; CCPs mitigate rather than eliminate counterparty risk.

All partly checked 2026-10-15, draft; human review outstanding. Artefacts: `notes/artefacts/volatility-options/hull-basics.tex`, `hull-forwards-futures.tex`, and `notes/artefacts/rates-credit-mortgages/time-value.tex`.

Written in migration macro markets and pricing / source review / optimal execution / execution control reviews, from the legacy macro chapter:

- `def:fixed-income-universe`: the fixed-income segments, Gliner's fixed-income ETF table (Table 9.5) and the legacy's unchecked size claim.

Changed in macro markets and pricing review (merges): `mod:forward-rates-fra` (FRA market notation, Gliner's fixing-date and convexity remarks corrected); `mod:duration-convexity` (DV01, the legacy convexity formula, which dropped the price, and negative convexity). the topic review other rates entries are owned by `monetary-policy-curve` (`def:central-bank-policy-framework`, `mod:taylor-rule`, `rule:major-central-banks-current`, `meth:policy-path-ois-futures`), `curve-term-structure` (`meth:curve-trades-carry-rolldown`), `rates-inflation` (`def:tips-breakevens`) and `rate-derivatives` (`def:interest-rate-swaps`), all in `compendium/rates-credit-mortgages/monetary-policy-curves.tex`.

Written in empirical extensions (2026-10-17) (source verification and bounded checks, not study or human review):

- `mod:multi-curve-fra-swap-valuation`: FRA and swap valuation with separate projection and discount curves, with own checks (`multicurve-check.py`). Partly checked 2026-10-17, draft; human review outstanding.

## Source verification after macro markets and pricing review

macro markets and pricing review follow-up, 2026-10-16 (source verification, not study): `data:fixed-income-market-size` resolved (SIFMA Fact Book highlights: global fixed-income debt $160.7 trillion and equity market capitalisation $157.8 trillion in 2025; the legacy's ranking found ill-posed). Entries corrected in the same follow-up are listed in `notes/source-review-records.md`, *macro markets and pricing review follow-up*.

empirical extensions (2026-10-17) (six audit repairs and a source-review coverage; source verification and bounded tests, not study or human review): `rule:otc-derivatives-reforms` narrowed (U.S. rules resolved (17 CFR 23.150-161, 43.3, 45.3) and merged into `mech:otc-clearing-collateral`; BCBS-IOSCO, prudential regulators and EMIR unread); `mod:multi-curve-fra-swap-valuation` resolved (new entry `mod:multi-curve-fra-swap-valuation` from Hull, with own checks); `ev:term-premia` resolved (Adrian, Crump and Moench and the New York Fed's file summarised and merged into `mod:forward-rates-fra`). The record is in `notes/source-review-records.md`, *empirical extensions (2026-10-17)*.

derivatives and empirical validation (2026-10-17) (seven audit repairs, backlog reconciliation and a source-review coverage; source verification and bounded tests, not study or human review): Stage 1: `mod:multi-curve-fra-swap-valuation` now separates the end-settled swaplet from the start-settled FRA, with the stochastic-valuation conditions and `fra-settlement-check.py`. Targets 31, 33 and 39: Bianchetti and Carlicchi's FRA table (end-settled form), Kim and Wright against ACM (correlation 0.86 over 441 months) and the BCBS-IOSCO margin framework merged; `rule:otc-derivatives-reforms` narrowed. The record is in `notes/source-review-records.md`, *derivatives and empirical validation (2026-10-17)*.

## Related entries owned elsewhere

Cross-referenced, not owned here: `def:derivative-contracts`, `res:cost-of-carry-forward-price` (`volatility-options`); `mech:futures-margin-settlement` (`futures-execution`); `def:return-measures` (`performance-manager-evaluation`, from the same time-value file); `mod:minimum-variance-hedge-ratio` (`commodity-hedging`); `def:fixed-income-market-structure` (`otc-fixed-income-trading`); `mech:securities-lending-short-sale` (`money-markets-repo-lending`); `def:common-investor-contagion` (`funding-crowding`).

## Entry backlog

- rule:otc-derivatives-reforms: the U.S. prudential regulators' uncleared-margin rule and EMIR's texts, with scope and dates; the CFTC's rules and the BCBS-IOSCO framework (thresholds and phase-in) are in `mech:otc-clearing-collateral`.

## Legacy candidate material

Run `python3 tools/check_compendium.py` for the current counts. No legacy file lists this overview alone; derivatives and hedging review migrated `rates-credit-mortgages/01_tvm.tex` and removed the legacy chapter. No legacy block now lists this overview as a candidate. That says nothing about consolidation.

## What changed in my view or practice

## Questions carried forward

- The legacy time-value file has no recorded source; was it from a CFA curriculum reading?
