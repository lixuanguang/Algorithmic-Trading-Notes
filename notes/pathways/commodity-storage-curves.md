---
key: commodity-storage-curves
section: energy-commodities
status: not started (draft entries from the migration only)
---

# Theory of storage, convenience yield and inventories

Pathway outcome, from the guide: explain the basis and the shape of commodity forward curves from inventories, convenience yield and stock-out risk; estimate the competitive storage model; and tell when backwardation reflects scarcity rather than a risk premium. Its 11 required readings: `ec-kaldor-1939`, `ec-working-1948`, `ec-brennan-1958`, `ec-fama-french-1987`, `ec-williams-wright-1991`, `physical-deaton-laroque-storage-1992`, `ec-deaton-laroque-1996`, `cf-cafiero-2011`, `ec-ng-pirrong-1994`, `ec-pindyck-1994`, `cf-symeonidis-2012`. This note is for a pathway of the section `energy-commodities`.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 16 October 2026 by migration slice 37 (`notes/migration.md`), which routed here the contango, backwardation and ending-stocks blocks and the commodities introduction of the legacy chapter; not a candidate of any legacy file (routing exception). The entries come from migration and source checking against Gliner (`s7-gliner`, *Global Macro Trading*, Wiley 2014, read from a local PDF and cited by chapter, section and PDF page). That is not study of the readings: none of them has been read for this pathway, and no checkpoint was attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in migration slice 37, 2026-10-16:

- `def:contango-backwardation-stocks`: storage and scarcity, seasonal crop curves, ending stocks with trade, stocks-to-use, and roll yield stated carefully.

All: verification partly checked 2026-10-16, stability draft; human review outstanding. The legacy wording is kept in `notes/artefacts/multi-asset-systematic-macro/`.

## Source verification after slice 37

Slice-37 follow-up, 2026-10-16 (source verification, not study): `ev:backwardation-scarcity-or-premium` narrowed. Entries corrected in the same follow-up are listed in `notes/migration-slices.md`, *Slice 37 follow-up*.

Batch of 2026-10-17 (source verification and bounded tests, not study or human review): `ev:backwardation-scarcity-or-premium` empirically tested on two U.S. energy contracts (own bounded test, protocol fixed before computing; `notes/artefacts/commodity-storage-curves/backwardation_test.py`, results and panel beside it, on EIA data ending 5 April 2024): backwardation rises as inventories fall below their seasonal norm for WTI (1987-2024, t = -5.9) and Henry Hub (2015-2024, t = -4.4), so scarcity is supported; the pre-specified premium test is not (WTI slope t = 0.1, OOS R^2 -2.2 percent), with an exploratory sign effect for WTI only. Written into `def:contango-backwardation-stocks`. The record is in `notes/migration-slices.md`, *Batch of 17 October 2026*.

## Related entries owned elsewhere

Cross-referenced, not owned here: `res:cost-of-carry-forward-price` (`volatility-options`); `def:futures-hedge-basis` (`commodity-hedging`); `def:agricultural-markets` (`agricultural-futures-delivery`).

## Entry backlog

- ev:backwardation-scarcity-or-premium: extend the 2026-10-17 test (scarcity supported, linear premium not supported, for WTI and Henry Hub) to other commodities and to the pathway's readings on hedging pressure and the storage model (for example Gorton, Hayashi and Rouwenhorst), which were not read; EIA's futures series end on 5 April 2024

## Legacy candidate material

None: the legacy chapters were all migrated by slice 37.

## What changed in my view or practice

## Questions carried forward
