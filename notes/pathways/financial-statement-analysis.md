---
key: financial-statement-analysis
section: financial-statement-analysis
status: not started (draft entries only, not from study)
---

# Financial statement analysis (section overview)

A compendium section declared in `compendium/compendium.tex`. The pinned guide has no section for accounting and statement analysis, although its `equity-events-fundamentals` pathway assumes them. The section's topics and neutral objectives are in `notes/coverage/objectives.json` (topics whose owner is `financial-statement-analysis`), and the learning order is in `notes/coverage/learning-roadmap.md`. There is no guide outcome, checkpoint or reading list for this section.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 18 October 2026 by the coverage pilot. Expanded on 20 October 2026 by the accounting and statement-analysis batch: 46 new entries in thirteen sections, from primary IFRS (EU-adopted) and FASB texts, SEC rules, the EU audit regulation, Subramanyam and Wild (2009), Damodaran (2012), Porter (2008), Sloan (1996) and Kahneman (2011). That is source checking, not study.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted. No checkpoint has been set for this section.

## Entries created or changed

Written in the coverage pilot (2026-10-18):

- `meth:statement-linked-cash-flows`: IAS 7 classification and the direct and indirect methods; account roll-forwards that turn the income statement and two balance sheets into a cash-flow statement; the IFRS 18 change of starting point to operating profit and the fixed classification of interest and dividends from 2027; an original worked example reconciled three ways (`notes/artefacts/financial-statement-analysis/cash-flow-linkage-check.py`).

Partly checked 2026-10-18, draft; human review outstanding.

Cash-flow slice (2026-10-18): the example now includes a prepaid expense and an accrued expense, the Notation gives the line-by-line direct conversion, and the Conditions compare IFRS before and after IFRS 18 with US GAAP Topic 230 (ASU 2016-15's reprint of the Codification paragraphs, Deloitte's quotation of 230-10-45-28 to 45-30, FASB staff papers of 2025-2026). Rechecked by `cash-flow-linkage-check.py`. Partly checked, draft; human review outstanding.

Accounting and statement-analysis batch (2026-10-20), one shared case and 45 objective entries; numbers checked by `notes/artefacts/financial-statement-analysis/statement-analysis-checks.py`:

- Framework and sources: `def:statement-analysis-framework`, `def:filings-disclosures-information-sources`, `def:ifrs-us-gaap-reporting-systems`.
- Company case: `ex:harbour-tools-statements` (ledger-built statements; direct = indirect cash flow; equity roll-forward).
- Income statement: `meth:revenue-recognition-analysis`, `meth:expense-recognition-capitalisation`, `meth:non-recurring-items`, `meth:earnings-per-share`, `meth:income-statement-ratios`.
- Balance sheet: `meth:intangibles-goodwill-reporting`, `meth:financial-instruments-liabilities`, `meth:balance-sheet-ratios`.
- Cash flows: `meth:cash-flow-interpretation`, `meth:free-cash-flow-coverage`.
- Inventories: `meth:inventory-measurement-nrv`, `meth:inventory-cost-formulas`, `meth:inventory-disclosure-analysis`.
- Long-lived assets: `meth:intangible-acquisition-routes`, `meth:impairment-derecognition`.
- Leases and compensation: `meth:lease-reporting`, `meth:post-employment-benefit-reporting`, `meth:share-based-compensation-reporting`, `def:long-term-liability-compensation-disclosures`, `meth:share-based-compensation-modelling`, `meth:post-employment-benefit-modelling`.
- Income taxes: `def:accounting-taxable-profit-differences`, `meth:deferred-tax-analysis`, `meth:tax-rate-measures`.
- Reporting quality: `def:reporting-results-quality`, `def:reporting-incentives-discipline`, `meth:earnings-management-presentation`, `meth:reporting-warning-signs`, `meth:report-quality-evaluation`, `meth:earnings-quality-persistence`, `meth:cash-flow-balance-sheet-quality`.
- Ratios: `meth:financial-ratio-families`, `meth:ratio-based-evaluation`, `meth:return-on-equity-decomposition`, `meth:ratio-based-earnings-forecast`.
- Modelling: `ex:harbour-pro-forma-model`, `meth:forecast-biases-remedies`, `meth:competition-inflation-forecasting`, `meth:forecast-horizon-steady-state`.
- Integrated analysis: `ex:integrated-credit-decision`, `meth:accounting-analysis-adjustments`, `meth:accounting-change-effects`.

Partly checked 2026-10-20, draft; human review outstanding. See [record](../source-review-records.md#accounting-and-statement-analysis-batch-20-october-2026).

## Entry backlog

## What changed in my view or practice

## Questions carried forward

- The current FASB Codification was not accessible; is any Topic 230 paragraph cited in the entry amended after 2016 beyond the finance-lease item?
- How did reported operating cash flows of non-financial issuers change on adopting IFRS 18 in 2027? A real filing would test the interest reclassification shown in the synthetic example.
- Which current Codification paragraphs replace the pre-Codification Statements cited (FAS 2, 86, 87, 109, 141R, 142, 144, 158), and have any been amended in ways that change the entries?
- Does the PCAOB critical-audit-matter requirement (AS 3101) change what a US auditor's report adds for analysis? The PCAOB site refused access on 2026-10-20.
- How did real issuers' operating cash flows and covenant definitions change on adopting IFRS 18 in 2027, against the Harbour illustration?
- Read Beneish (1999) and Richardson, Tuna and Wysocki (2010) to test the warning-sign and accrual entries against the detection and post-publication evidence.
