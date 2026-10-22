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

Written in library gap-filling Batch L2 (2026-10-21), new topic file `compendium/securitised-structured-credit/default-correlation.tex`:

- `mod:gaussian-copula-default-correlation`: copulas, the one-factor Gaussian copula for default times, conditional binomial defaults, Vasicek's worst-case default rate, and the Basel IRB risk-weight function (CRE31, in force from 1 January 2023, retrieved 2026-10-21) reproducing CRE99's illustrative risk weights.
- `meth:tranche-loss-base-correlation`: tranche loss, Hull's Example 25.2 reproduced, large against exact finite pools and simulation, compound and base correlation, and their failures on a synthetic two-correlation market.

Partly checked 2026-10-21, draft. Checks in `notes/artefacts/default-correlation/default-correlation-checks.py`. Sources: Hull, *OFOD* 11th Global ed., secs. 24.8 and 25.8-25.11; Hull, *RMFI* 6th ed., secs. 9.5-9.6; Basel Framework CRE31 and CRE99. Human review outstanding. See [record](../source-review-records.md#library-gap-filling-batch-l2-21-october-2026).

## Related entries owned elsewhere

Cross-referenced, not owned here: `meth:credit-spread-term-structure` (`corporate-credit-cds`); `meth:option-adjusted-spread` (`rates-credit-mortgages`).

## Specialist pathways

The guide's pathways for this section, in its order, with the existing material, partial treatment or content gap as recorded by the content migration of 22 October 2026 and its closeout review. A pathway with related material but no note has not been opened. A partial treatment names the existing entries that treat some of the pathway's subtopics, wherever they sit, and the subtopics with nothing written.

Printed as numbered sections of the chapter, under the guide pinned at `8302467` (`subsection_alignment_plan.md`): `mortgages-abs-clo`, `synthetic-risk-transfer`. A pathway without entries of its own is not printed; the related material and partial treatments named below are printed under the pathway or section that owns them.

- `covered-bonds` (Covered bonds and extendable maturity): no pathway note; partial treatment in existing entries, not reviewed as complete: dual recourse and covered bonds against securitisation (`meth:abs-structures-credit-enhancement` in `securitised-structured-credit/securitisation`, `meth:credit-cds-international-structured` in `corporate-credit-capital/credit-portfolio-management`). Not written: extendable maturities; covered-bond spreads and regulatory treatment.
- `sukuk` (Sukuk: ownership, recourse and relative value): content gap; no entry written.
- `mortgages-abs-clo` (Mortgages, ABS and CLO waterfalls): no pathway note; related existing material in `securitised-structured-credit/securitisation`, not reviewed as a complete treatment of the pathway.
- `synthetic-risk-transfer` (Synthetic risk transfer and credit-linked notes): no pathway note; related existing material in `securitised-structured-credit/default-correlation`, not reviewed as a complete treatment of the pathway.
- `cmbs-workouts` (CMBS, servicing and property workouts): no pathway note; partial treatment in existing entries, not reviewed as complete: CMBS call protection, the special servicer as B-piece holder and balloon risk (`meth:mortgage-securities-prepayment` in `securitised-structured-credit/securitisation`). Not written: servicing standards; modification and foreclosure outcomes; loss severities.

## Entry backlog

## What changed in my view or practice

## Questions carried forward

- Fabozzi and Kothari print an average life of 8.6 years at 165% PSA; a month-by-month rebuild gives 8.54. Which convention gives 8.6?
- Their Table 3.2 retires class B in month 97 while the text says 98, and prints balances for classes C and D (96.5m and 73m) that differ from Structure 1 as stated (159.225m and 120.45m). Is there an erratum?
- CMBS balloon and refinancing risk is stated as an interpretation; which primary source (a rating methodology or a CMBS prospectus) documents it?
