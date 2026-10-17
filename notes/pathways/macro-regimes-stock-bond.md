---
key: macro-regimes-stock-bond
section: multi-asset-systematic-macro
status: not started (draft entries from the migration only)
---

# Macro regimes, inflation and the stock–bond correlation

Pathway outcome, from the guide: identify growth, inflation and volatility regimes with information available at the time, measure how asset classes and styles behave in each, model the stock–bond correlation, and test whether regime-aware allocation beats a static mix out of sample. Its 15 required readings: `wide-ang-timmermann-regimes`, `ma-ang-bekaert-2002`, `ma-guidolin-timmermann-2007`, `ma-kritzman-page-turkington-2012`, `ma-ilmanen-maloney-ross-2014`, `s16-regimes`, `ma-neville-draaisma-funnell-harvey-van-hemert-2021`, `ma-bekaert-wang-2010`, `w3-fang-liu-roussanov-inflation`, `ma-connolly-stivers-sun-2005`, `ma-baele-bekaert-inghelbrecht-2010`, `rt-cpv-2020`, `ma-brixton-2023`, `ma-molenaar-2024`, `w4-stamos-stock-bond-corr`. This note is for a pathway of the section `multi-asset-systematic-macro`.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 16 October 2026 by migration slice 37 (`notes/migration.md`), which routed here the regime-response blocks of the legacy chapter (relationship between assets, sector rotation, fixed income and commodities in regimes); `01_regimes.tex` named this pathway as a candidate, the others came from `02_transmission_maps.tex`. The entries come from migration and source checking against Gliner (`s7-gliner`, *Global Macro Trading*, Wiley 2014, read from a local PDF and cited by chapter, section and PDF page). That is not study of the readings: none of them has been read for this pathway, and no checkpoint was attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in migration slice 37, 2026-10-16:

- `def:macro-regime-asset-map`: the legacy's map of asset and sector responses to growth, recession, inflation, deflation, liquidity and geopolitical shocks, kept as hypotheses, with Gliner's risk-on/risk-off and sector-rotation passages.

All: verification partly checked 2026-10-16, stability draft; human review outstanding. The legacy wording is kept in `notes/artefacts/multi-asset-systematic-macro/`.

## Source verification after slice 37

Slice-37 follow-up, 2026-10-16 (source verification, not study): `ev:regime-asset-responses-tested` narrowed. Entries corrected in the same follow-up are listed in `notes/migration-slices.md`, *Slice 37 follow-up*.

Batch of 2026-10-17 (source verification and bounded tests, not study or human review): `ev:regime-asset-responses-tested` empirically tested for the recession row only (own bounded test, protocol fixed before computing; `notes/artefacts/macro-regimes-stock-bond/regime_recession_test.py`, results and panel beside it): on a Sahm-type rule applied to each quarterly vintage of the Philadelphia Fed's real-time unemployment data, 1965-2025 (241 vintages, 53 signal quarters; the 2026 vintages skipped because October 2025 is missing in them), none of the five recession signs holds over the next three months at |t| > 2, and equities and defensives move against the map; inside ex-post NBER windows the signs match the map but are not significant. Written into `def:macro-regime-asset-map`. The record is in `notes/migration-slices.md`, *Batch of 17 October 2026*.

Second batch of 2026-10-17 (audit repairs and a 50-item queue; source verification and bounded tests, not study or human review): `ev:regime-asset-responses-tested` repaired (v2; v1 kept): the ex-post NBER window is stated as any overlap (v1) with an all-months sensitivity; the dollar is tested on the goods-only index to 2019 (primary) and on the goods-and-services index from 2006, the v1 splice reported with its definition break; real-time and ex-post blocks separated; Newey-West (4) t and episode counts added. Real time: no sign passes (goods-only dollar +1.1%, t = 1.98). Ex post: on all-months windows the yield and Baa-spread signs pass Welch |t| > 2, so 'no ex-post sign reaches the threshold' now holds only for any-overlap windows with Welch t. Focused checks: `batch50-regime-checks.py`. The record is in `notes/migration-slices.md`, *Second batch of 17 October 2026*.

Third batch of 2026-10-17 (six audit repairs and a 60-item queue; source verification and bounded tests, not study or human review): `ev:regime-asset-responses-tested` tested (the inflation-shock row tested on real-time CPI vintages under a protocol with two recorded deviations: no response supported). The record is in `notes/migration-slices.md`, *Third batch of 17 October 2026*.

## Related entries owned elsewhere

Cross-referenced, not owned here: `def:global-macro-strategy` (`multi-asset-systematic-macro`); `def:macroeconomic-indicators` (`macro-nowcasting-signals`); `def:tips-breakevens` (`rates-inflation`).

## Entry backlog

- ev:regime-asset-responses-tested: (tested within stated bounds in the third batch of 2026-10-17) test the other rows of the regime map (growth, inflation, deflation, liquidity, geopolitical) and Gliner's Figure 8.3 sector phases on regimes classified with real-time data, and the recession row with other real-time rules, horizons, commodities and non-U.S. assets; the recession row was tested on 2026-10-17 with a real-time Sahm-type rule (no sign supported; `def:macro-regime-asset-map`)

## Legacy candidate material

None: the legacy chapters were all migrated by slice 37.

## What changed in my view or practice

## Questions carried forward

- Which regime classification (growth/inflation quadrants, volatility states, Markov switching) do the readings recommend, and with what real-time data?
