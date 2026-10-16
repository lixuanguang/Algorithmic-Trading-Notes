---
key: macro-nowcasting-signals
section: multi-asset-systematic-macro
status: not started (draft entries from the migration only)
---

# Nowcasting, real-time macro data and macro trading signals

Pathway outcome, from the guide: build a real-time nowcast and surprise index from data vintages and release calendars, compare factor, mixed-frequency, text and machine-learning methods, and turn macro trends into a tradable signal without look-ahead. Its 15 required readings: `w5-croushore-stark`, `w2-mccracken-ng-fredmd`, `ma-stock-watson-2002`, `wide-giannone-nowcasting`, `wide-banbura-nowcasting`, `ma-aruoba-diebold-scotti-2009`, `ma-andreou-ghysels-kourtellos-2013`, `ma-scotti-2016`, `ma-beber-brandt-luisi-2015`, `ma-thorsrud-2020`, `ma-giannone-lenza-primiceri-2021`, `ma-goulet-coulombe-2022`, `ma-dahlquist-hasseltoft-2020`, `gap-global-macro-database`, `s16-r11`. This note is for a pathway of the section `multi-asset-systematic-macro`.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 16 October 2026 by migration slice 37 (`notes/migration.md`), which routed here the indicator blocks of the legacy chapter (growth, inflation, employment, external, fiscal, consumption, housing, business, demographics) and Gliner's equity leading indicators; `02_transmission_maps.tex` named this pathway as a candidate. The entries come from migration and source checking against Gliner (`s7-gliner`, *Global Macro Trading*, Wiley 2014, read from a local PDF and cited by chapter, section and PDF page), the FOMC's Statement on Longer-Run Goals and the BLS program page as retrieved on 16 October 2026. That is not study of the readings: none of them has been read for this pathway, and no checkpoint was attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in migration slice 37, 2026-10-16:

- `def:macroeconomic-indicators`: Gliner's indicator families, the FOMC's headline-PCE goal (Gliner's "core PCE" corrected) and his demographic table read column by column.
- `meth:equity-macro-leading-indicators`: commodity prices, CDX HY, ISM, the Baltic Dry Index, consumer confidence and AUD implied volatility as Gliner's equity indicators, untested.

All: verification partly checked 2026-10-16, stability draft; human review outstanding. The legacy wording is kept in `notes/artefacts/multi-asset-systematic-macro/`.

## Related entries owned elsewhere

Cross-referenced, not owned here: `data:us-macro-release-calendar` (`macro-announcements-policy`); `meth:macro-event-queries` (`macro-announcements-policy`); `def:tips-breakevens` (`rates-inflation`).

## Entry backlog

- data:bls-ces-scope: CES coverage and exclusions from the BLS Handbook of Methods (the page was not retrievable on 2026-10-16); the legacy excluded nonprofits.
- data:demographic-projections-current: current working-age and prime-saving-age peak years (Census or UN) to replace Gliner's c.~2013 Table 12.2.

## Legacy candidate material

None: the legacy chapters were all migrated by slice 37.

## What changed in my view or practice

## Questions carried forward

- Build a release-vintage panel for payrolls, CPI and ISM before testing any of Gliner's indicators.
