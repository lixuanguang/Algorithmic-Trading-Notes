---
key: private-wealth-management
section: private-wealth-management
status: not started (draft entries only, not from study)
---

# Private wealth management (section overview)

A compendium section declared in `compendium/compendium.tex`. Its topics and neutral objectives are in `notes/coverage/objectives.json` (topics whose section is `private-wealth-management`), and the learning order is in `notes/coverage/learning-roadmap.md`: private clients and the industry, then wealth planning, then preservation, then advising complex clients and transferring wealth.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 20 October 2026 by the completion batch: 15 entries in four sections. Jurisdictions: United States federal law for tax year 2026 and the United Kingdom (outside Scotland) for 2026 to 2027, chosen because they contrast citizenship- with residence-based taxation, estate with inheritance tax and two pension designs; Singapore appears only for its residence rule. Sources: Rev. Proc. 2025-32, Notice 2025-67, Title 26 sections and SEC rules (LII), GOV.UK and HMRC guidance, the UK--US treaty, IRAS, ESMA's suitability guidelines, MiFID II, the SEC's adviser interpretation, the Federal Reserve's 2022 SCF bulletin, Ibbotson, Milevsky, Chen and Zhu (2007), Gennaioli, Shleifer and Vishny (NBER WP 18174) and Campbell, Serfaty-de Medeiros and Viceira (NBER WP 13088). That is source checking, not study. All clients are hypothetical; nothing here is personal tax advice.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Completion batch (2026-10-20). Numbers are checked by `notes/artefacts/private-wealth/private-wealth-checks.py`:

- Clients and the industry: `meth:individual-wealth-capital`, `meth:private-client-tax-inflation`, `meth:private-client-ips`, `def:wealth-management-industry`, `meth:advising-families`.
- Planning: `meth:goals-based-financial-plan`, `meth:lifetime-exposures`, `meth:tax-in-planning`, `meth:private-client-allocation-review`, `meth:retirement-across-jurisdictions`.
- Preservation: `meth:human-capital-risks`, `meth:purchasing-power-fx`.
- Advising the wealthy and transfers: `meth:residency-citizenship`, `meth:complex-client-situations`, `meth:wealth-transfer-strategies`.

Related existing entries: `meth:goals-based-allocation-heuristics`, `meth:economic-balance-sheet-allocation`, `meth:allocation-constraints-taxes-revision`, `meth:investment-policy-statement`, `def:tips-breakevens`, `meth:currency-hedging-programme`.

Partly checked 2026-10-20, draft; human review outstanding. See [record](../source-review-records.md#completion-batch-20-october-2026).

Final audit correction pass (2026-10-20): the Okafor case reconciled (reserve outside the policy portfolio, retirement at 62, one set of savings, education dates and tax assumptions), asset location under one convention, UK residence band taper and the gift-and-estate chronology. See [record](../source-review-records.md#final-audit-correction-pass-20-october-2026).

PR #33 correction pass (2026-10-21): the Okafors' 2026 federal tax specified and computed by stacking (42,500 of dividends and gains at 15 percent, 23,500 at 20 percent, NIIT 2,599.20) instead of a 15 percent rate inferred from the 35 percent band. See [record](../source-review-records.md#pr-33-correction-pass-21-october-2026).

## Specialist pathways

The guide's pathways for this section, in its order, with the existing material or the content gap as recorded by the content migration of 22 October 2026. A pathway with related material but no note has not been opened.

- `household-finance-lifecycle` (Household finance, human capital and lifecycle investment planning): no pathway note; related existing material in `private-wealth-management/clients-industry`, `private-wealth-management/wealth-planning`, not reviewed as a complete treatment of the pathway.
- `tax-aware-wealth-preservation` (Taxes, asset location and concentrated positions): no pathway note; related existing material in `private-wealth-management/wealth-preservation`, not reviewed as a complete treatment of the pathway.
- `wealth-transfer-succession` (Estate planning, intergenerational transfers and family-business succession): no pathway note; related existing material in `private-wealth-management/wealth-transfer`, not reviewed as a complete treatment of the pathway.

## Entry backlog

## What changed in my view or practice


Written in library gap-filling Batch L6 (2026-10-21): `meth:complex-client-situations` extended with concentrated single-stock positions (sale, staged diversification, completion portfolios, collars and prepaid forwards, exchange funds, charitable remainder trusts), from *Portfolio Management in Practice*, Vol. 1, chap. 16, sec. 6, and *Managing Investment Portfolios*, Example 11-3, with US federal tax mechanics verified in 26 U.S.C. 1259, 721, 351(e), 704(c), 737 and 664, Treas. Reg. 1.351-1 and Rev. Rul. 2003-7 (retrieved 2026-10-21). Checks in `notes/artefacts/private-wealth/concentrated-position-check.py`. Partly checked 2026-10-21, draft; human review outstanding. See [record](../source-review-records.md#library-gap-filling-batch-l6-21-october-2026).

## Questions carried forward

- State taxes, Scottish rates, the UK Finance Act 2025 text on the four-year regime, US Treasury regulations and case law, and national succession law are outside the sources; each would change specific numbers.
- Mortality uses an illustrative Gompertz law; the SSA period life table could not be retrieved (HTTP 403).
