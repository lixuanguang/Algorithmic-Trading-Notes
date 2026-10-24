---
key: macro-regimes-stock-bond
section: multi-asset-systematic-macro
status: not started (draft entries only, not from study)
---

# Macro regimes, inflation and the stock–bond correlation

Pathway outcome, from the guide: identify growth, inflation and volatility regimes with information available at the time, measure how asset classes and styles behave in each, model the stock–bond correlation, and test whether regime-aware allocation beats a static mix out of sample. Its 15 required readings: `wide-ang-timmermann-regimes`, `ma-ang-bekaert-2002`, `ma-guidolin-timmermann-2007`, `ma-kritzman-page-turkington-2012`, `ma-ilmanen-maloney-ross-2014`, `s16-regimes`, `ma-neville-draaisma-funnell-harvey-van-hemert-2021`, `ma-bekaert-wang-2010`, `w3-fang-liu-roussanov-inflation`, `ma-connolly-stivers-sun-2005`, `ma-baele-bekaert-inghelbrecht-2010`, `rt-cpv-2020`, `ma-brixton-2023`, `ma-molenaar-2024`, `w4-stamos-stock-bond-corr`. This note is for a pathway of the section `multi-asset-systematic-macro`.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 16 October 2026 by macro markets and pricing review (`notes/source-review-index.md`). The entries come from source checking against Gliner (`s7-gliner`, *Global Macro Trading*, Wiley 2014, read from a local PDF and cited by chapter, section and PDF page). That is not study of the readings: none of them has been read for this pathway, and no checkpoint was attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in macro markets and pricing / source review / optimal execution / execution control reviews:

- `def:macro-regime-asset-map`: a map of asset and sector responses to growth, recession, inflation, deflation, liquidity and geopolitical shocks, kept as hypotheses, with Gliner's risk-on/risk-off and sector-rotation passages.

All: verification partly checked 2026-10-16, stability draft; human review outstanding.

## Source verification after macro markets and pricing review

macro markets and pricing review follow-up, 2026-10-16 (source verification, not study): `ev:regime-asset-responses-tested` narrowed. Entries corrected in the same follow-up are listed in `notes/source-review-records.md`, *macro markets and pricing review follow-up*.

source verification (2026-10-17) (source verification and bounded tests, not study or human review): `ev:regime-asset-responses-tested` empirically tested for the recession row only (own bounded test, protocol fixed before computing; `trading_notes.research.macro_regimes_data.regime_recession`, results and panel beside it): on a Sahm-type rule applied to each quarterly vintage of the Philadelphia Fed's real-time unemployment data, 1965-2025 (241 vintages, 53 signal quarters; the 2026 vintages skipped because October 2025 is missing in them), none of the five recession signs holds over the next three months at |t| > 2, and equities and defensives move against the map; inside ex-post NBER windows the signs match the map but are not significant. Written into `def:macro-regime-asset-map`. The record is in `notes/source-review-records.md`, *source verification (2026-10-17)*.

method validation (2026-10-17) (audit repairs and a source-review coverage; source verification and bounded tests, not study or human review): `ev:regime-asset-responses-tested` repaired (v2; v1 kept): the ex-post NBER window is stated as any overlap (v1) with an all-months sensitivity; the dollar is tested on the goods-only index to 2019 (primary) and on the goods-and-services index from 2006, the v1 splice reported with its definition break; real-time and ex-post blocks separated; Newey-West (4) t and episode counts added. Real time: no sign passes (goods-only dollar +1.1%, t = 1.98). Ex post: on all-months windows the yield and Baa-spread signs pass Welch |t| > 2, so 'no ex-post sign reaches the threshold' now holds only for any-overlap windows with Welch t. Focused checks: `trading_notes.numerical.macro_regimes_data.regime_checks`. The record is in `notes/source-review-records.md`, *method validation (2026-10-17)*.

empirical extensions (2026-10-17) (six audit repairs and a source-review coverage; source verification and bounded tests, not study or human review): `ev:regime-asset-responses-tested` tested (the inflation-shock row tested on real-time CPI vintages under a protocol with two recorded deviations: no response supported). The record is in `notes/source-review-records.md`, *empirical extensions (2026-10-17)*.

derivatives and empirical validation (2026-10-17) (seven audit repairs, backlog reconciliation and a source-review coverage; source verification and bounded tests, not study or human review): audit repairs: the inflation-shock row rerun on the quarterly CPI vintages the protocol named (`cpiQvMd.xlsx`; 128 vintages, 34 signals in 13 episodes; no sign supported), the monthly-vintage run kept as a timing sensitivity. The `ev:regime-asset-responses-tested` question: the deflation row tested on the same vintages under a recorded protocol: not supported. The record is in `notes/source-review-records.md`, *derivatives and empirical validation (2026-10-17)*.

## Related entries owned elsewhere

Cross-referenced, not owned here: `def:global-macro-strategy` (`multi-asset-systematic-macro`); `def:macroeconomic-indicators` (`macro-nowcasting-signals`); `def:tips-breakevens` (`rates-inflation`).

## Entry backlog

- ev:regime-asset-responses-tested: the map's growth, liquidity and geopolitical rows and Gliner's Figure 8.3 sector phases on real-time classifications, and other rules, horizons and non-U.S. assets for the rows tested. The recession, inflation-shock and deflation rows are tested on real-time vintages: no hypothesised sign is supported.

## What changed in my view or practice

## Questions carried forward

- Which regime classification (growth/inflation quadrants, volatility states, Markov switching) do the readings recommend, and with what real-time data?
