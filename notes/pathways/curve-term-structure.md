---
key: curve-term-structure
section: rates-credit-mortgages
status: not started (draft entries from the migration only)
---

# Yield-curve construction and term-structure models

Pathway outcome, from the guide: build a zero curve, decompose yields into expectations and term premia, and estimate and compare affine term-structure models. Its 16 required readings: `catalogue-0233`, `wide-litterman-scheinkman`, `wide-nelson-siegel`, `wide-hagan-west-interp`, `wide-ametrano-bianchetti`, `wide-gsw-yield-curve`, `wide-diebold-li`, `s6-vasicek`, `wide-cir-1985`, `wide-hull-white`, `s6-hjm`, `wide-duffee-essentially`, `wide-jsz`, `rt-cdr-afns-2011`, `exp-adrian-crump-moench-term-structure`, `rt-kim-wright-2005`. This note is for a pathway of the section `rates-credit-mortgages`.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 16 October 2026 by migration slice 37 (`notes/migration.md`), which routed here the curve-trade, carry-and-rolldown and inversion blocks of the legacy chapter; not a candidate of any legacy file (routing exception). The entries come from migration and source checking against Gliner (`s7-gliner`, *Global Macro Trading*, Wiley 2014, read from a local PDF and cited by chapter, section and PDF page) and Estrella and Trubin (2006). That is not study of the readings: none of them has been read for this pathway, and no checkpoint was attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in migration slice 37, 2026-10-16:

- `meth:curve-trades-carry-rolldown`: DV01-neutral steepeners and flatteners, bull and bear moves, carry signs that depend on the curve and financing, rolldown defined (Gliner's definition corrected), and Estrella--Trubin's inversion record to 2005.

All: verification partly checked 2026-10-16, stability draft; human review outstanding. The legacy wording is kept in `notes/artefacts/multi-asset-systematic-macro/`.

Written in the fourth batch of 2026-10-17:

- `data:gsw-treasury-curve`: the Federal Reserve's fitted Treasury curve: the Svensson form, its parameters and an own recomputation.

## Source verification after slice 37

Slice-37 follow-up, 2026-10-16 (source verification, not study): `ev:curve-inversion-after-2005` narrowed. Entries corrected in the same follow-up are listed in `notes/migration-slices.md`, *Slice 37 follow-up*.

Second slice-37 follow-up, 2026-10-16 (source verification, not study): `ev:curve-inversion-after-2005` narrowed (Estrella and Trubin's own series rebuilt from H.15 with a reproducible script; month and episode rules tested; only the outcome-dependent revisit remains). Entries corrected in the same follow-up are listed in `notes/migration-slices.md`, *Slice 37 second follow-up*.

Source follow-up of slices 33-36 and the slice-37 audit, 2026-10-16 (source verification, not study): `ev:curve-inversion-after-2005` deferred (depends on future NBER dating; no peak after February 2020 dated as of 16 October 2026; the episode rule's hit rates are now labelled retrospective in the entry). The record is in `notes/migration-slices.md`, *Source follow-up of slices 33-36 and slice-37 audit corrections*.

Audit note of 2026-10-16 (`meth:curve-trades-carry-rolldown`): the episode rule is scored from an episode's last inverted month and ex-post NBER dates, so its hit rates describe the record and are not a prospective forecasting result; counts unchanged.

Batch of 2026-10-17 (source verification and bounded tests, not study or human review): `ev:curve-inversion-after-2005` deferral retained: NBER's chronology (data last updated 14 March 2023) still ends with the February 2020 peak and April 2020 trough, so the provisional outcomes are unchanged. The record is in `notes/migration-slices.md`, *Batch of 17 October 2026*.

Third batch of 2026-10-17 (six audit repairs and a 60-item queue; source verification and bounded tests, not study or human review): `ev:curve-inversion-after-2005` deferred (trigger review: no NBER peak after February 2020; 24 of the 27 months lie beyond the longest past announcement lag, 3 months and both episodes within it; retained). The record is in `notes/migration-slices.md`, *Third batch of 17 October 2026*.

Fourth batch of 2026-10-17 (seven audit repairs, backlog reconciliation and a 70-target batch; source verification and bounded tests, not study or human review): target 32: new entry `data:gsw-treasury-curve` (the published Svensson parameters reproduce SVENY10 on all 13,759 days to 0.00005 points). Backlog: `ev:curve-inversion-after-2005` rewritten; all 27 inverted months now have complete horizons, and only retrospective NBER dating remains, with a revisit trigger of an NBER peak announcement or April 2027. The record is in `notes/migration-slices.md`, *Fourth batch of 17 October 2026*.

## Related entries owned elsewhere

Cross-referenced, not owned here: `mod:duration-convexity` (`rates-credit-mortgages`); `mod:forward-rates-fra` (`rates-credit-mortgages`); `conv:government-bond-futures` (`futures-execution`).

## Entry backlog

- ev:curve-inversion-after-2005: retrospective NBER dating only. All 27 inverted expansion months from November 2022 (episodes 2022-11 to 2024-11 and 2025-03 to 2025-04, on H.15 data) now have complete twelve-month horizons with no recession dated; 24 lie beyond the longest past announcement lag (12 months) and 3 (2024-11, 2025-03, 2025-04) still within it. Revisit when NBER announces a business-cycle peak after February 2020, or from April 2027, when the last of the 27 months passes the longest past lag (a later dating would then need a longer lag than any before).

## Legacy candidate material

None: the legacy chapters were all migrated by slice 37.

## What changed in my view or practice

## Questions carried forward
