---
key: commodity-storage-curves
section: energy-commodities
status: not started (draft entries only, not from study)
---

# Theory of storage, convenience yield and inventories

Pathway outcome, from the guide: explain the basis and the shape of commodity forward curves from inventories, convenience yield and stock-out risk; estimate the competitive storage model; and tell when backwardation reflects scarcity rather than a risk premium. Its 11 required readings: `ec-kaldor-1939`, `ec-working-1948`, `ec-brennan-1958`, `ec-fama-french-1987`, `ec-williams-wright-1991`, `physical-deaton-laroque-storage-1992`, `ec-deaton-laroque-1996`, `cf-cafiero-2011`, `ec-ng-pirrong-1994`, `ec-pindyck-1994`, `cf-symeonidis-2012`. This note is for a pathway of the section `energy-commodities`.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 16 October 2026 by macro markets and pricing review (`notes/source-review-index.md`). The entries come from source checking against Gliner (`s7-gliner`, *Global Macro Trading*, Wiley 2014, read from a local PDF and cited by chapter, section and PDF page). That is not study of the readings: none of them has been read for this pathway, and no checkpoint was attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in macro markets and pricing / source review / optimal execution / execution control reviews:

- `def:contango-backwardation-stocks`: storage and scarcity, seasonal crop curves, ending stocks with trade, stocks-to-use, and roll yield stated carefully.

All: verification partly checked 2026-10-16, stability draft; human review outstanding.

## Source verification after macro markets and pricing review

macro markets and pricing review follow-up, 2026-10-16 (source verification, not study): `ev:backwardation-scarcity-or-premium` narrowed. Entries corrected in the same follow-up are listed in `notes/source-review-records.md`, *macro markets and pricing review follow-up*.

source verification (2026-10-17) (source verification and bounded tests, not study or human review): `ev:backwardation-scarcity-or-premium` empirically tested on two U.S. energy contracts (own bounded test, protocol fixed before computing; `trading_notes.research.commodity_curves.backwardation`, results and panel beside it, on EIA data ending 5 April 2024): backwardation rises as inventories fall below their seasonal norm for WTI (1987-2024, t = -5.9) and Henry Hub (2015-2024, t = -4.4), so scarcity is supported; the pre-specified premium test is not (WTI slope t = 0.1, OOS R^2 -2.2 percent), with an exploratory sign effect for WTI only. Written into `def:contango-backwardation-stocks`. The record is in `notes/source-review-records.md`, *source verification (2026-10-17)*.

method validation (2026-10-17) (audit repairs and a source-review coverage; source verification and bounded tests, not study or human review): `ev:backwardation-scarcity-or-premium` repaired and retested (v2; v1 recoverable with `git show 684b3a0:notes/artefacts/commodity-storage-curves/superseded-first-run/<file>`): contract identity checked under NYMEX's expiry rules with the data calendar (Henry Hub's pre-1997 roll inferred from the data), the incomplete April 2024 month excluded, price-only and inventory samples separated (gas premium test now 362 months, out-of-sample from January 2004), inventory reports dated by a conservative convention from EIA's 2025-2026 schedules (6, 7 or 11 days after the week ending), settlement-timed results labelled closing-price associations and an executable next-day variant added, and the 'dropped' message corrected. Verdicts unchanged: scarcity supported (WTI t = -5.9, gas t = -4.3), premium not supported (WTI OOS R^2 -1.8%, gas -0.8%). Focused checks: `trading_notes.numerical.commodity_curves.energy_checks`. The record is in `notes/source-review-records.md`, *method validation (2026-10-17)*.

empirical extensions (2026-10-17) (six audit repairs and a source-review coverage; source verification and bounded tests, not study or human review): `ev:backwardation-scarcity-or-premium` tested (heating oil added under a protocol recorded before the data: scarcity supported, premium not). The record is in `notes/source-review-records.md`, *empirical extensions (2026-10-17)*.

derivatives and empirical validation (2026-10-17) (seven audit repairs, backlog reconciliation and a source-review coverage; source verification and bounded tests, not study or human review): audit repairs: the heating-oil premium test rerun with the protocol's log returns (slope 0.33, $t=1.55$; OOS $R^2=-0.95$ percent), the simple-return run kept; EIA's contract definition and the sparse two-contract calendar documented. The `ev:backwardation-scarcity-or-premium` question: hedging pressure from the CFTC's Commitments of Traders tested for WTI under a protocol recorded before the data: not supported. The record is in `notes/source-review-records.md`, *derivatives and empirical validation (2026-10-17)*.

## Related entries owned elsewhere

Cross-referenced, not owned here: `res:cost-of-carry-forward-price` (`volatility-options`); `def:futures-hedge-basis` (`commodity-hedging`); `def:agricultural-markets` (`agricultural-futures-delivery`).

## Entry backlog

- ev:backwardation-scarcity-or-premium: commodities beyond the three U.S. energy contracts (metals, agriculture), and hedging pressure for gas and heating oil (tested for WTI only, not supported). Data limits that remain: inventory release schedules before 2025, NYMEX's heating-oil rule text, sparse two-contract overlap before 2007, COT release delays, and TAS availability before 2019.

## What changed in my view or practice

## Questions carried forward
