---
key: rates-credit-mortgages
section: rates-credit-mortgages
status: not started (draft entries from the migration only)
---

# Rates: yield curves, term premia and derivatives (section overview)

Overview outcome, from the guide: connect a rate quote or bond position to its curve, expected policy path, term premium, collateral and hedge-contract assumptions. Its checkpoint builds a cash-flow and risk-assumption sheet for a collateralised swap hedged with SOFR futures and a Treasury note, repriced under level and slope moves, a policy surprise, a term-premium shock and a collateral or funding change. Its readings are `rt-gurkaynak-wright-2012`, `s6-brigo`, `exp-adrian-crump-moench-term-structure`, `gap-rates-sofr-futures-hedging` and `gap-gregory5`.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 15 October 2026 by migration slice 31 (`notes/migration-slices.md`). The rates, compounding, forward-rate, duration, quotation and OTC-clearing material of the legacy Hull notes (`volatility-options/basic.tex` and `fwdfut.tex`, mapped to the options overview and, for `fwdfut.tex`, to this overview and `commodity-hedging`) was routed here, together with the time-value formulas of the unsourced legacy file `rates-credit-mortgages/01_tvm.tex`. The entries come from source checking against Hull's 11th Global edition (not a reading of this overview), the New York Fed's reference-rate methodology (`exp-sofr-data`) and the CPSS-IOSCO principles (`exp-pfmi`); the time-value formulas are derived, not sourced. None of the overview's readings has been read; the checkpoint was not attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in migration slice 31, 2026-10-15:

- `def:interest-rate-measures`: credit spread; Treasury, overnight and repo rates; EFFR and SOFR methodology (Hull's brokered-average EFFR superseded in 2016 by a volume-weighted median); compounding conversions and EAR (the legacy "expected annual rate" corrected); zero rates, bond yields and par yields; annuity and perpetuity values derived, with their timing and limits.
- `mod:forward-rates-fra`: forward and instantaneous forward rates; FRA payoff against present value (the legacy dropped the discounting), settlement timing and the single-curve caveat; term-structure theories as conjectures.
- `mod:duration-convexity`: Macaulay and modified duration and convexity as approximations, checked at plus or minus 200 bp; yield change against parallel curve shift.
- `conv:us-rate-quotation`: U.S. day counts, Treasury bill discount quotes, bond prices in thirty-seconds, clean and dirty prices.
- `mech:otc-clearing-collateral`: CCP and bilateral ISDA/CSA clearing, variation and initial margin, interest on margin, haircuts, and the post-crisis reforms as Hull reports them; CCPs mitigate rather than eliminate counterparty risk.

All partly checked 2026-10-15, draft; human review outstanding. Artefacts: `notes/artefacts/volatility-options/hull-basics.tex`, `hull-forwards-futures.tex`, and `notes/artefacts/rates-credit-mortgages/time-value.tex`.

## Related entries owned elsewhere

Cross-referenced, not owned here: `def:derivative-contracts`, `res:cost-of-carry-forward-price` (`volatility-options`); `mech:futures-margin-settlement` (`futures-execution`); `def:return-measures` (`performance-manager-evaluation`, from the same time-value file); `mod:minimum-variance-hedge-ratio` (`commodity-hedging`); `def:fixed-income-market-structure` (`otc-fixed-income-trading`); `mech:securities-lending-short-sale` (`money-markets-repo-lending`); `def:common-investor-contagion` (`funding-crowding`).

## Entry backlog

- rule:otc-derivatives-reforms: the primary rules behind Hull's account (U.S. swap execution and clearing mandates, swap data reporting, and the uncleared-margin framework phased in from 2016), with jurisdictions, scope and dates (`gap-gregory5` and the rule texts, unread).
- mod:multi-curve-fra-swap-valuation: FRA and swap valuation with separate projection and discounting curves and backward-looking compounded SOFR, replacing the single-curve illustration (`s6-brigo`, `gap-rates-sofr-futures-hedging`, unread).
- ev:term-premia: estimates of term premia that decide between expectations and liquidity-preference accounts (`exp-adrian-crump-moench-term-structure`, unread); home pathway `curve-term-structure`.

## Legacy candidate material

Run `python3 tools/migration_status.py` for the current counts. No legacy file lists this overview alone; slice 31 migrated `rates-credit-mortgages/01_tvm.tex` and removed the legacy chapter. No legacy block now lists this overview as a candidate. That says nothing about consolidation.

## What changed in my view or practice

## Questions carried forward

- The legacy time-value file has no recorded source; was it from a CFA curriculum reading?
