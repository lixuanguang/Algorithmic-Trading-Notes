---
key: sovereign-municipal
section: government-bond-markets
status: not started (draft entries only, not from study)
---

# Sovereign default, restructuring and local-currency debt

Pathway outcome, from the guide: distinguish local-currency sovereign risk, default incentives, restructuring terms and litigation risk, and compare market-implied recovery with historical outcomes. Its 11 required readings: `gap-sovereign-local-currency`, `rt-arellano-2008`, `rt-dps-portfolios-2020`, `rt-hss-em-premia-2020`, `gap-sovereign-restructuring-playbook`, `gap-sovereign-imf-srdsf`, `gap-sovereign-haircuts`, `rt-hebert-schreger-2017`, `rt-ste-court-2021`, `gap-sovereign-worldbank-ids`, `latest-avdjiev-sovereign-nbfi-nexus-2026`. This note is for a pathway of the section `government-bond-markets`.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 16 October 2026 by macro markets and pricing review (`notes/source-review-index.md`). The entries come from source checking against Gliner (`s7-gliner`, *Global Macro Trading*, Wiley 2014, read from a local PDF and cited by chapter, section and PDF page) and the Moody's 1983--2006 table he reproduces. That is not study of the readings: none of them has been read for this pathway, and no checkpoint was attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in macro markets and pricing / source review / optimal execution / execution control reviews:

- `def:sovereign-credit-defaults`: ISDA's sovereign definition, reference entities, inverted credit curves, the 40 percent recovery convention against Moody's 55 percent mean (the test depends on n), and the 1998--2006 default record.

All: verification partly checked 2026-10-16, stability draft; human review outstanding.

Credit, time-series and valuation batch (2026-10-20); numbers checked by `notes/artefacts/corporate-credit-capital/credit-cds-securitisation-checks.py` (part 9):

- `meth:sovereign-credit-analysis`: indicators, debt dynamics and the debt-stabilising primary balance (Fabozzi handbook eqs. 17-1 to 17-3, verified against a nominal roll-forward), debt structure, gross financing needs, local- against foreign-currency debt, and US general obligation against revenue bonds.

Written for the curriculum objective; the pathway's 11 required readings were not read for it. Partly checked 2026-10-20, draft; human review outstanding. See [record](../source-review-records.md#credit-time-series-and-valuation-batch-20-october-2026).

## Source verification after macro markets and pricing review

macro markets and pricing review follow-up, 2026-10-16 (source verification, not study): `ev:isda-greece-2012-determination` resolved (ISDA EMEA Determinations Committee: Restructuring Credit Event for the Hellenic Republic, unanimous, 9 March 2012, after the collective action clauses; auction held 19 March 2012 (final price not read in a primary document)); `ev:sovereign-restructurings-after-2006` narrowed. Entries corrected in the same follow-up are listed in `notes/source-review-records.md`, *macro markets and pricing review follow-up*.

Second macro markets and pricing review follow-up, 2026-10-16 (source verification, not study): `ev:sovereign-restructurings-after-2006` narrowed (Greece: EUR 197 billion exchanged, 53.5 percent nominal haircut, NPV loss 70-75 percent, EUR 106 billion written off; Argentina: US$82 billion restructured, US$65.5 billion of it foreign-law, recovery about 52 percent). Entries corrected in the same follow-up are listed in `notes/source-review-records.md`, *macro markets and pricing review second follow-up*.

Source follow-up of order books and order flow / dealer models and information reviews and the macro markets and pricing review audit, 2026-10-16 (source verification, not study): `ev:sovereign-restructurings-after-2006` blocked for now (no named dataset with a dated Argentine default count obtained: Reinhart's data page lists no static download link and the BoC-BoE database counts amounts in default from 1960, not episodes since independence). The record is in `notes/source-review-records.md`, *Source follow-up of order books and order flow / dealer models and information reviews and macro markets and pricing review audit corrections*.

Second source follow-up, 2026-10-16 (source verification, not study or human review): `ev:sovereign-restructurings-after-2006` resolved as attributed counts (CRS IF10991 v6: nine external defaults since 1816, May 2020 the ninth; Reinhart's 2010 chartbook: seven external and five domestic episodes to 2009; Fitch's 2020 study: rating defaults in 2001, 2014, 2019 and 2020; kept apart, not merged). The record is in `notes/source-review-records.md`, *Second source follow-up of the order books and order flow / macro markets and pricing reviews queue*.

## Related entries owned elsewhere

Cross-referenced, not owned here: `mech:cds-contract-credit-events` (`corporate-credit-cds`); `meth:curve-trades-carry-rolldown` (`curve-term-structure`).

## Entry backlog

None open after the second source follow-up of 2026-10-16.

## What changed in my view or practice

## Questions carried forward
- The IMF's sovereign risk and debt sustainability framework guidance refused access on 2026-10-20; how does its fan-chart approach change the single-year debt-dynamics calculation?
