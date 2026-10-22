---
key: corporate-finance
section: corporate-finance
status: not started (draft entries only, not from study)
---

# Corporate finance (section overview)

A compendium section declared in `compendium/compendium.tex`. The pinned guide has no pathway for corporate finance; its `equity-events-fundamentals` and `corporate-hybrids-preferred` pathways assume it. The section's topics and neutral objectives are in `notes/coverage/objectives.json` (topics whose section is `corporate-finance`), and the learning order is in `notes/coverage/learning-roadmap.md`. There is no guide outcome, checkpoint or reading list for this section.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 20 October 2026 by the corporate-finance and equity-valuation batch: 20 entries in seven sections, from Damodaran's *Applied Corporate Finance* (2014) and *Investment Valuation* (2012), Modigliani and Miller (1958), the G20/OECD Principles (2023), the OECD ownership study (2019), the simplified ESRS (2026), Berg, Kölbel and Rigobon (2022), OpenStax *Principles of Finance* (2nd ed.), Subramanyam and Wild (2009), Delaware and EU company law, SEC and FINRA rules, and Lang and Stulz (1993). That is source checking, not study.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted. No checkpoint has been set for this section.

## Entries created or changed

Corporate-finance and equity-valuation batch (2026-10-20). Harbour Tools plc, the case of the statement-analysis section, is reused for the cost of capital, payout and the bolt-on acquisition; numbers are checked by `notes/artefacts/corporate-finance/corporate-finance-checks.py`:

- Issuers, ownership and governance: `def:organisational-forms-issuers`, `def:stakeholder-claims`, `meth:corporate-governance-evaluation`, `def:global-ownership-structures`, `meth:esg-exposure-evaluation`.
- Business models: `def:business-model-features-types`.
- Working capital: `meth:cash-conversion-cycle`, `meth:working-capital-policy`.
- Capital investment: `meth:capital-project-evaluation`, `meth:capital-allocation-principles`.
- Capital structure and the cost of capital: `meth:wacc-calculation`, `mod:capital-structure-theory`, `meth:cost-of-debt-equity-estimation`, `meth:capital-structure-benchmarking`.
- Payout policy: `meth:distribution-effects`, `meth:dividend-policy-evaluation`, `meth:payout-policy-comparison`, `meth:dividend-sustainability`.
- Restructuring: `meth:restructuring-evaluation`, `ex:restructuring-valuation-effects`.

Partly checked 2026-10-20, draft; human review outstanding. See [record](../source-review-records.md#corporate-finance-and-equity-valuation-batch-20-october-2026).

## Specialist pathways

The guide's pathways for this section, in its order, with the existing material or the content gap as recorded by the content migration of 22 October 2026. A pathway with related material but no note has not been opened.

Printed as numbered sections of the chapter, under the guide pinned at `8302467` (`subsection_alignment_plan.md`): `capital-budgeting-investment`, `capital-structure-payout`, `corporate-governance-restructuring`. A pathway without entries of its own is not printed; the related material and partial treatments named below are printed under the pathway or section that owns them.

- `capital-budgeting-investment` (Capital budgeting, project valuation and working capital): no pathway note; related existing material in `corporate-finance/capital-investment`, `corporate-finance/working-capital-liquidity`, not reviewed as a complete treatment of the pathway.
- `capital-structure-payout` (Capital structure, cost of capital and payout policy): no pathway note; related existing material in `corporate-finance/capital-structure-cost-of-capital`, `corporate-finance/payout-policy`, not reviewed as a complete treatment of the pathway.
- `corporate-governance-restructuring` (Business models, ownership, corporate governance, mergers and restructuring): no pathway note; related existing material in `corporate-finance/corporate-ownership-governance`, `corporate-finance/business-models`, `corporate-finance/corporate-restructuring`, not reviewed as a complete treatment of the pathway. Broadened by the guide revision of 22 October 2026 (`8302467`) to cover business models and ESG exposures; its entries are in `corporate-finance/business-models`, `corporate-finance/corporate-ownership-governance`, `corporate-finance/corporate-restructuring`.

## Entry backlog

## What changed in my view or practice


Written in library gap-filling Batch L6 (2026-10-21): `meth:cost-of-debt-equity-estimation` extended with country risk premiums (default-spread, relative-volatility and melded methods; beta-scaled against additive use; revenue weights with production caveats; local risk-free rates net of the default spread; currency translation by inflation differential) from Damodaran, *Applied Corporate Finance*, pp. 89-93, 98-107 and 133-135, with an original example and its zero limit. Checks in `notes/artefacts/corporate-finance/country-risk-premium-check.py`. Partly checked 2026-10-21, draft; human review outstanding. See [record](../source-review-records.md#library-gap-filling-batch-l6-21-october-2026).

## Questions carried forward

- The rating-to-spread schedule in `meth:capital-structure-benchmarking` is illustrative; a current published schedule (for example Damodaran's annual ratings table) would test whether Harbour's optimum near 20 percent debt is robust.
- Applied Corporate Finance describes dividend tax systems and imputation countries as of 2013-2014; which have changed since?
- The ESRS cited are the 2026 simplified standards; how do the ISSB's IFRS S1 and S2, which were not accessible, differ for an investor's materiality assessment?
- Are the acquisition-return studies summarised in Investment Valuation (1970s-1990s US deals) borne out by recent evidence?
