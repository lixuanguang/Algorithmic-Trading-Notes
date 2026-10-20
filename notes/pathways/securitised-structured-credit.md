---
key: securitised-structured-credit
section: securitised-structured-credit
status: not started (draft entries only, not from study)
---

# Securitised and structured credit (section overview)

A compendium section declared in `compendium/compendium.tex`. The topic and its objectives are in `notes/coverage/objectives.json` (topic `securitisation`). The guide's specialist pathways that touch structured credit have their own notes.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 20 October 2026 by the credit, time-series and valuation batch, from Fabozzi and Kothari (2008), Hull (2021, chap. 8), Fuster, Lucca and Vickery (2022), Regulation (EU) 2017/2402, Directive (EU) 2019/2162 and FHFA Advisory Bulletin 2021-02. That is source checking, not study.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Credit, time-series and valuation batch (2026-10-20); numbers checked by `notes/artefacts/corporate-credit-capital/credit-cds-securitisation-checks.py` (part 10), which rebuilds Fabozzi and Kothari's 660 million pool month by month and Hull's ABS CDO table:

- `def:securitisation-process`: definition, parties, true sale, EU risk retention, benefits and incentive costs.
- `meth:abs-structures-credit-enhancement`: covered bonds and dual recourse, credit enhancement and its sizing, revolving card ABS, CDOs and the ABS CDO.
- `meth:mortgage-securities-prepayment`: agency and non-agency MBS, CPR, SMM and PSA, sequential and PAC tranching, CMBS call protection.

Partly checked 2026-10-20, draft; human review outstanding. See [record](../source-review-records.md#credit-time-series-and-valuation-batch-20-october-2026).

## Related entries owned elsewhere

Cross-referenced, not owned here: `meth:credit-spread-term-structure` (`corporate-credit-cds`); `meth:option-adjusted-spread` (`rates-credit-mortgages`).

## Entry backlog

## What changed in my view or practice

## Questions carried forward

- Fabozzi and Kothari print an average life of 8.6 years at 165% PSA; a month-by-month rebuild gives 8.54. Which convention gives 8.6?
- Their Table 3.2 retires class B in month 97 while the text says 98, and prints balances for classes C and D (96.5m and 73m) that differ from Structure 1 as stated (159.225m and 120.45m). Is there an erratum?
- CMBS balloon and refinancing risk is stated as an interpretation; which primary source (a rating methodology or a CMBS prospectus) documents it?
