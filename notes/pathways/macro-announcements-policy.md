---
key: macro-announcements-policy
section: multi-asset-systematic-macro
status: not started (draft entries from the migration only)
---

# Macro announcements, policy news and announcement premia

Pathway outcome, from the guide: measure how stocks, bonds and currencies respond to scheduled macro releases and FOMC decisions, explain why the responses change over the business cycle, and estimate how much of the equity premium is earned around announcements. Its 16 required readings: `wide-abdv-announcements`, `ma-andersen-bollerslev-diebold-vega-2007`, `ma-boyd-hu-jagannathan-2005`, `ma-elenev-law-song-yaron-2024`, `ma-gilbert-scotti-strasser-vega-2017`, `wide-savor-wilson-announcements`, `ma-ai-bansal-2018`, `wide-lucca-moench-drift`, `ma-cieslak-morse-vissing-jorgensen-2019`, `ma-bernanke-kuttner-2005`, `wide-gss-policy`, `wide-nakamura-steinsson`, `ma-bauer-swanson-2023`, `wide-bauer-swanson`, `ma-brusa-savor-wilson-2020`, `ma-mueller-tahbaz-salehi-vedolin-2017`. This note is for a pathway of the section `multi-asset-systematic-macro`.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 16 October 2026 by migration slice 37 (`notes/migration.md`), which routed here the data-release, query and calendar blocks of the legacy chapter; `02_transmission_maps.tex` named this pathway as a candidate, while the blocks themselves were in `01_regimes.tex`. The entries come from migration and source checking against Gliner (`s7-gliner`, *Global Macro Trading*, Wiley 2014, read from a local PDF and cited by chapter, section and PDF page), the BLS, Federal Reserve and ECB pages as retrieved on 16 October 2026. That is not study of the readings: none of them has been read for this pathway, and no checkpoint was attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in migration slice 37, 2026-10-16:

- `data:us-macro-release-calendar`: the usual U.S. release cadence, FOMC and ECB meeting frequency (the legacy's "ECB 6 per year" corrected), and agencies' calendars as the record.
- `meth:macro-event-queries`: Gliner's conditional back-tests around events (the BoE's 2012 QE example), surprises and revisions, and why six events cannot support a hit rate.

All: verification partly checked 2026-10-16, stability draft; human review outstanding. The legacy wording is kept in `notes/artefacts/multi-asset-systematic-macro/`.

## Source verification after slice 37

Slice-37 follow-up, 2026-10-16 (source verification, not study): `data:us-release-schedules-2026` narrowed. Entries corrected in the same follow-up are listed in `notes/migration-slices.md`, *Slice 37 follow-up*.

## Related entries owned elsewhere

Cross-referenced, not owned here: `def:central-bank-policy-framework` (`monetary-policy-curve`); `rule:major-central-banks-current` (`monetary-policy-curve`); `def:macroeconomic-indicators` (`macro-nowcasting-signals`).

## Entry backlog

- data:us-release-schedules-2026: the BLS CPI release calendar and the ISM's report calendar (first and third business days), whose pages refused automated access; the BEA, Census and Federal Reserve G.17 calendars were read on 2026-10-16 and match the legacy cadence.

## Legacy candidate material

None: the legacy chapters were all migrated by slice 37.

## What changed in my view or practice

## Questions carried forward

- Do announcement-day returns (Savor--Wilson) survive in the post-2015 sample?
