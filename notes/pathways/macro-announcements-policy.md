---
key: macro-announcements-policy
section: multi-asset-systematic-macro
status: not started (draft entries only, not from study)
---

# Macro announcements, policy news and announcement premia

Pathway outcome, from the guide: measure how stocks, bonds and currencies respond to scheduled macro releases and FOMC decisions, explain why the responses change over the business cycle, and estimate how much of the equity premium is earned around announcements. Its 16 required readings: `wide-abdv-announcements`, `ma-andersen-bollerslev-diebold-vega-2007`, `ma-boyd-hu-jagannathan-2005`, `ma-elenev-law-song-yaron-2024`, `ma-gilbert-scotti-strasser-vega-2017`, `wide-savor-wilson-announcements`, `ma-ai-bansal-2018`, `wide-lucca-moench-drift`, `ma-cieslak-morse-vissing-jorgensen-2019`, `ma-bernanke-kuttner-2005`, `wide-gss-policy`, `wide-nakamura-steinsson`, `ma-bauer-swanson-2023`, `wide-bauer-swanson`, `ma-brusa-savor-wilson-2020`, `ma-mueller-tahbaz-salehi-vedolin-2017`. This note is for a pathway of the section `multi-asset-systematic-macro`.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 16 October 2026 by macro markets and pricing review (`notes/source-review-index.md`). The entries come from source checking against Gliner (`s7-gliner`, *Global Macro Trading*, Wiley 2014, read from a local PDF and cited by chapter, section and PDF page), the BLS, Federal Reserve and ECB pages as retrieved on 16 October 2026. That is not study of the readings: none of them has been read for this pathway, and no checkpoint was attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in macro markets and pricing / source review / optimal execution / execution control reviews:

- `data:us-macro-release-calendar`: the usual U.S. release cadence, FOMC and ECB meeting frequency ("ECB 6 per year" corrected), and agencies' calendars as the record.
- `meth:macro-event-queries`: Gliner's conditional back-tests around events (the BoE's 2012 QE example), surprises and revisions, and why six events cannot support a hit rate.

All: verification partly checked 2026-10-16, stability draft; human review outstanding.

## Source verification after macro markets and pricing review

macro markets and pricing review follow-up, 2026-10-16 (source verification, not study): `data:us-release-schedules-2026` narrowed. Entries corrected in the same follow-up are listed in `notes/source-review-records.md`, *macro markets and pricing review follow-up*.

Second macro markets and pricing review follow-up, 2026-10-16 (source verification, not study): `data:us-release-schedules-2026` narrowed (BLS CPI schedule: 10 November and 10 December 2026, 13 January 2027 at 8:30 a.m.). Entries corrected in the same follow-up are listed in `notes/source-review-records.md`, *macro markets and pricing review second follow-up*.

Source follow-up of order books and order flow / dealer models and information reviews and the macro markets and pricing review audit, 2026-10-16 (source verification, not study): `data:us-release-schedules-2026` blocked (the ISM calendar and report pages redirect to a member login, rechecked 2026-10-16). The record is in `notes/source-review-records.md`, *Source follow-up of order books and order flow / dealer models and information reviews and macro markets and pricing review audit corrections*.

Second source follow-up, 2026-10-16 (source verification, not study or human review): `data:us-release-schedules-2026` resolved (ISM 2026 calendar read from a browser export: first and third business days at 10:00 a.m.; the rule reproduces every date except January, an ISM holiday, and April's Services date, which skips Good Friday; computed in contract-specifications-statistics-checks.py, section 5). The record is in `notes/source-review-records.md`, *Second source follow-up of the order books and order flow / macro markets and pricing reviews queue*.

## Related entries owned elsewhere

Cross-referenced, not owned here: `def:central-bank-policy-framework` (`monetary-policy-curve`); `rule:major-central-banks-current` (`monetary-policy-curve`); `def:macroeconomic-indicators` (`macro-nowcasting-signals`).

## Entry backlog

None open after the second source follow-up of 2026-10-16.

## What changed in my view or practice

## Questions carried forward

- Do announcement-day returns (Savor--Wilson) survive in the post-2015 sample?
