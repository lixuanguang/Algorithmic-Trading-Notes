---
key: rate-derivatives
section: rates-credit-mortgages
status: not started (draft entries from the migration only)
---

# Interest-rate derivatives, volatility and RFR conventions

Pathway outcome, from the guide: price caps, swaptions and SOFR futures with a calibrated model and explain smile, convexity and convention effects. Its 16 required readings: `s6-brigo`, `wide-bgm-lmm`, `rt-lss-2001`, `wide-hagan-sabr`, `rt-arbitrage-free-sabr-2014`, `gap-rates-multicurve-sabr`, `wide-trolle-schwartz-usv`, `rt-cdg-usv-2002`, `rt-hanson-convexity-2014`, `rt-schrimpf-sushko-rfr-2019`, `gap-rates-backward-term-rates`, `exp-sofr-data`, `wide-mercurio-sofr`, `wide-skov-skovmand-sofr`, `gap-rates-isda-definitions`, `catalogue-0235`. This note is for a pathway of the section `rates-credit-mortgages`.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 16 October 2026 by migration macro markets and pricing review (`notes/source-review-index.md`), which routed here the interest-rate-swap block of the legacy chapter; not a candidate of any legacy file (routing exception). The entries come from migration and source checking against Gliner (`s7-gliner`, *Global Macro Trading*, Wiley 2014, read from a local PDF and cited by chapter, section and PDF page). That is not study of the readings: none of them has been read for this pathway, and no checkpoint was attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in migration macro markets and pricing / source review / optimal execution / execution control reviews:

- `def:interest-rate-swaps`: fixed for floating, payer and receiver, SOFR in place of LIBOR, clearing rather than "exchange-traded".

All: verification partly checked 2026-10-16, stability draft; human review outstanding. The legacy wording is kept in `notes/artefacts/multi-asset-systematic-macro/`.

Written in derivatives and empirical validation (2026-10-17):

- `mod:sabr-smile`: the SABR expansion in single- and multiple-curve form, with an own Monte Carlo check.

## Source verification after macro markets and pricing review

macro markets and pricing review follow-up, 2026-10-16 (source verification, not study): `data:irs-notional-share` narrowed. Entries corrected in the same follow-up are listed in `notes/source-review-records.md`, *macro markets and pricing review follow-up*.

Second macro markets and pricing review follow-up, 2026-10-16 (source verification, not study): `data:irs-notional-share` resolved (BIS OTC derivatives bulk data: at end-December 2025 interest rate swaps $545.0 trillion, 81.4 percent of $669.5 trillion interest rate derivatives; FRAs 10.7, options 7.9 percent; end-June 2024 swaps 81.1 percent of $578.8 trillion). Entries corrected in the same follow-up are listed in `notes/source-review-records.md`, *macro markets and pricing review second follow-up*.

derivatives and empirical validation (2026-10-17) (seven audit repairs, backlog reconciliation and a source-review coverage; source verification and bounded tests, not study or human review): target 29: new entry `mod:sabr-smile` (SABR expansion in single- and multiple-curve form, with an own Monte Carlo check); targets 34-35 (Schrimpf and Sushko; the SOFR calculation and revision rule) merged into `def:money-market-reference-rates`. The record is in `notes/source-review-records.md`, *derivatives and empirical validation (2026-10-17)*.

## Related entries owned elsewhere

Cross-referenced, not owned here: `meth:policy-path-ois-futures` (`monetary-policy-curve`); `mech:otc-clearing-collateral` (`rates-credit-mortgages`).

## Entry backlog


## Legacy candidate material

None: the legacy chapters were all migrated by macro markets and pricing review.

## What changed in my view or practice

## Questions carried forward
