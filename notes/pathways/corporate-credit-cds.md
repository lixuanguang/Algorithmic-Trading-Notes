---
key: corporate-credit-cds
section: corporate-credit-capital
status: not started (draft entries only, not from study)
---

# Corporate bonds and credit derivatives

Pathway outcome, from the guide: reconcile a cash-bond spread, a CDS model value and competing bond-return evidence. Its 14 required readings: `s6-duffie`, `catalogue-0238`, `add-cds-contract`, `add-cds-model`, `add-cds-rfr2026`, `add-bond-factor`, `add-bond-counterevidence`, `gapclose-openbond-corrected-factors`, `catalogue-0239`, `exp-trace`, `exp-bao-pan-wang-bond-illiquidity`, `gap-credit-cdx-hy-spec`, `w5-hull-white-cds`, `w5-augustin-cds-survey`. This note is for a pathway of the section `corporate-credit-capital`.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 16 October 2026 by macro markets and pricing review (`notes/source-review-index.md`). The entries come from source checking against Gliner (`s7-gliner`, *Global Macro Trading*, Wiley 2014, read from a local PDF and cited by chapter, section and PDF page). That is not study of the readings: none of them has been read for this pathway, and no checkpoint was attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in macro markets and pricing / source review / optimal execution / execution control reviews:

- `mech:cds-contract-credit-events`: premium leg, physical settlement against par and its cash equivalent, credit events, Gliner's "unlimited upside" corrected, and the post-2009 standard contract flagged as unchecked.

All: verification partly checked 2026-10-16, stability draft; human review outstanding.

Credit, time-series and valuation batch (2026-10-20); numbers checked by `notes/artefacts/corporate-credit-capital/credit-cds-securitisation-checks.py`, which reproduces Hull's (2023) Examples 17.1-17.4, Tables 17.1-17.5 and 19.1-19.2 and Appendix K, and Hull's (2021) Example 25.1:

- Credit risk and credit analysis: `def:credit-risk-components`, `meth:corporate-credit-analysis`, `meth:risky-bond-cva`, `meth:rating-migration-returns`, `mod:structural-reduced-form-credit`, `meth:credit-spread-term-structure`.
- Credit default swaps: `def:cds-contract-features`, `meth:cds-pricing`, `meth:cds-strategies` (with Berd, Mashal and Wang 2004 on curve steepeners).

These entries serve the curriculum objectives of the section; none of the pathway's 14 required readings was read for them. Partly checked 2026-10-20, draft; human review outstanding. See [record](../source-review-records.md#credit-time-series-and-valuation-batch-20-october-2026).

Alternatives batch (2026-10-20), in `credit-portfolio-management.tex`:

- `meth:credit-spread-portfolio-risk`: risks of spread portfolios, spread duration and DTS, and the spread measures with the case for OAS.
- `meth:credit-selection-positioning`: bottom-up (excess spread to peers) and top-down (cycle, sectors, equity momentum) approaches, and positioning by DTS, curve, quality and instrument.
- `meth:credit-liquidity-tail-risk`: liquidity cost scores, liquidity management, credit VaR (Vasicek), stress tests and issuer limits by downgrade risk or DTS.
- `meth:credit-cds-international-structured`: CDS overlays and replication, international credit, structured instruments against corporates (tranching, CLO tests) and analytical tools.

Sources: Ben Dor et al. (2012, 2021), Hull (2023) chap. 19, Larreur (2021). Examples in `notes/artefacts/credit-portfolios/credit-portfolio-checks.py`. Partly checked 2026-10-20, draft; human review outstanding; none of the pathway's required readings was read for them.

## Source verification after macro markets and pricing review

macro markets and pricing review follow-up, 2026-10-16 (source verification, not study): `conv:cds-standard-contract` narrowed. Entries corrected in the same follow-up are listed in `notes/source-review-records.md`, *macro markets and pricing review follow-up*.

Second macro markets and pricing review follow-up, 2026-10-16 (source verification, not study): `conv:cds-standard-contract` narrowed (the Big Bang FAQ read for contract coverage, Determinations Committee requests, the 60-day look-back and the fixed coupons). Entries corrected in the same follow-up are listed in `notes/source-review-records.md`, *macro markets and pricing review second follow-up*.

Source follow-up of order books and order flow / dealer models and information reviews and the macro markets and pricing review audit, 2026-10-16 (source verification, not study): `conv:cds-standard-contract` blocked (the 2014 ISDA Credit Derivatives Definitions are sold by ISDA; no licensed copy). The record is in `notes/source-review-records.md`, *Source follow-up of order books and order flow / dealer models and information reviews and macro markets and pricing review audit corrections*.

Second source follow-up, 2026-10-16 (source verification, not study or human review): `conv:cds-standard-contract` still blocked (ISDA's 21 February 2014 release read: bail-in credit event, sovereign asset-package delivery, standard reference obligation, implementation from the September 2014 roll by reference or protocol; the Definitions themselves are sold by ISDA and were not read). The record is in `notes/source-review-records.md`, *Second source follow-up of the order books and order flow / macro markets and pricing reviews queue*.

source verification (2026-10-17) (source verification and bounded tests, not study or human review): `conv:cds-standard-contract` still blocked: ISDA's 2014 Definitions Protocol (published 21 August 2014) and its web page were read into `mech:cds-contract-credit-events` (Implementation Date the later of 22 September 2014 and the business day after any cut-off date; effectiveness condition met on 17 September 2014), but the Definitions' operative wording is sold by ISDA and was not read. The record is in `notes/source-review-records.md`, *source verification (2026-10-17)*.

method validation (2026-10-17) (audit repairs and a source-review coverage; source verification and bounded tests, not study or human review): Queue: `conv:cds-standard-contract` still blocked (the 2014 ISDA Definitions are sold). The record is in `notes/source-review-records.md`, *method validation (2026-10-17)*.

derivatives and empirical validation (2026-10-17) (seven audit repairs, backlog reconciliation and a source-review coverage; source verification and bounded tests, not study or human review): backlog reconciliation only: the backlog lines below were rewritten to state the remaining gap alone, removing stacked dated status prefixes and claims that material was unread or not obtained where earlier batches had read it. The record is in `notes/source-review-records.md`, *derivatives and empirical validation (2026-10-17)*.

## Related entries owned elsewhere

Cross-referenced, not owned here: `def:sovereign-credit-defaults` and `meth:sovereign-credit-analysis` (`sovereign-municipal`); `def:securitisation-process`, `meth:abs-structures-credit-enhancement`, `meth:mortgage-securities-prepayment` (`securitised-structured-credit`); `meth:equity-macro-leading-indicators` (`macro-nowcasting-signals`).

## Entry backlog

- conv:cds-standard-contract: the 2014 ISDA Credit Derivatives Definitions themselves (sold by ISDA, not read), for the current credit-event and deliverable-obligation terms. The Big Bang Protocol page and FAQ, ISDA's release of 21 February 2014 and the 2014 Definitions Protocol of 21 August 2014 were read.

## What changed in my view or practice

## Questions carried forward
- Hull's Table K.1 prints the year-4 survival probability as 0.9321 against 0.9231 in Table K.2; is it in the author's errata for the 6th edition?
- The CDS-bond basis is described from Hull; how large has it been since 2020 for European investment-grade names?
