---
key: model-governance-controls
section: research-engineering-validation
status: not started (draft entries from the migration only)
---

# Model governance, AI risk and trading controls

Pathway outcome, from the guide: design a model inventory, validation and change process, and the pre-trade and kill-switch controls an algorithmic strategy needs before production. Its checkpoint is a two-page control specification for deploying a new execution algorithm (inventory entry, validation evidence, change approval, pre-trade limits, kill switch, monitoring and incident playbook), mapping each control to the relevant rule or principle and to the Knight Capital failure points. Its fourteen readings include U.S., U.K. and EU model-risk and algorithmic-trading rules (`s8-governance`, `wide-pra-ss123`, `wide-mifid-rts6`, `wide-sec-15c3-5`, `w2-pra-ss518`, `wide-dora`), operational-resilience principles (`wide-bcbs-opres`), industry controls (`w2-fia-automated-controls`) and the Knight Capital order (`wide-knight-capital`).

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 15 October 2026 by migration slice 17 (`notes/migration.md`), which migrated the legacy production-considerations file mapped to this pathway. Only its reliability, network-failure and audit-trail blocks were routed here; its architecture, indicator, floor-against-automated and brokerage blocks went elsewhere or were deleted. The entry comes from migration and source checking against Harris (`alpha-harris`, 2002) and the current eCFR text of Rule 15c3-5, whose adopting release (`wide-sec-15c3-5`) is a reading of this pathway but was not itself read. That is not study of the readings: none has been studied, and the EU rule (`wide-mifid-rts6`) could not be retrieved.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in migration slice 17, 2026-10-15:

- `meth:automated-trading-operational-controls`: Harris's reliability, security and audit-trail practice (2002); the network-failure examples, with unknown order state, unknown fill state, reconciliation, retry, cancellation and recovery kept apart (synthesis marked as Interpretation); and the U.S. market-access rule, 17 CFR 240.15c3-5, in its current text (duplicative-order rejection, access restriction, post-trade execution reports, annual review).

Verification partly checked 2026-10-15, stability draft; human review outstanding. Its artefact is `notes/artefacts/model-governance-controls/derivations.tex`.

Written in migration slice 26, 2026-10-15, from Narang's chapter "Risks Inherent to Quant Strategies" (`s7-narang`, third edition, 2024, not a reading of this pathway):

- `def:quant-strategy-risk-sources`: model risk (inapplicability, misspecification, implementation errors), regime change and exogenous shocks, kept apart from funding contagion (`funding-crowding`) and operational failure; the legacy "discretionary overrides" qualified by separating ad hoc intervention outside the validated design, in effect an unvalidated model change, from approved and tested contingency responses (de-risking rules, limits, kill switches), which are part of the design.
- `meth:quant-strategy-monitoring`: exposure, profit-and-loss (including how money is made and hit rate), execution and systems monitors as early warnings; execution-algorithm indicators left to the decision-support entry of `execution-trading-costs` (see below).

Changed in the slice-26 follow-up, 2026-10-15: `def:quant-strategy-risk-sources` no longer calls every override an unvalidated model change; operational controls are described as mitigating failure, not guaranteeing its prevention; and the five causes are presented as overlapping questions rather than exclusive categories.

Both verification partly checked 2026-10-15, stability draft; human review outstanding. Their artefact is `notes/artefacts/model-governance-controls/risk-assessment.tex`, a new file beside the slice-17 `derivations.tex`. The same legacy file's contagion block was routed to `funding-crowding` (its entry is listed below, under related entries).

Written in migration slice 30, 2026-10-15, from López de Prado (`alpha-afml`, 2018, chap. 1, pp. 5-9), through the *Chains of Production for Alpha Signals* block of Narang's legacy overview file and one item of the alpha-models file (both mapped to the overview `portfolio-construction-risk`; a routing exception, since promotion, allocation and decommission are model-governance decisions):

- `meth:strategy-production-lifecycle`: the meta-strategy paradigm, the research stations, and the embargo, paper-trading, graduation, re-allocation and decommission stages, as one author's prescription without quantitative criteria; his decommission condition and "in general" on concave allocation restored; "microscopic alpha" kept as opinion.

Partly checked 2026-10-15, draft; human review outstanding. Its artefacts are `notes/artefacts/portfolio-construction-risk/systematic-investing-overview.tex` and `alpha-models.tex`.

Changed in the slice-30 follow-up, 2026-10-15: embargo and paper trading are placed after deployment and before live-capital trading (graduation), as in AFML pp. 8-9, not "before production".

- `rule:mifid-rts6-algorithmic-controls`: EU RTS 6: testing and deployment limits, annual self-assessment and stress tests, kill functionality, business continuity, pre-trade controls, real-time monitoring and real-time reconciliation. Partly checked 2026-10-17, draft.
- `mech:order-state-reconciliation`: FIX OrderStatusRequest, OrderMassStatusRequest, ExecutionReport states, ResendRequest, SequenceReset and possible-duplicate flags, arranged as a documented method; offline illustration only. Partly checked 2026-10-17, draft.
- `ev:quant-implementation-failures`: Knight Capital (2012) and AXA Rosenberg (2007-2010) from the SEC orders, with the differences from Narang's account. Partly checked 2026-10-17, draft.

## Source verification after slice 37

Batch of 2026-10-17 (source verification and bounded tests, not study or human review): Three stubs resolved as new entries in `research-engineering-validation/trading-controls.tex`. `rule:mifid-rts6-algorithmic-controls`: Delegated Regulation 2017/589 through CELLAR (Arts. 5-17 and 29; no amending act, one German-only corrigendum); `meth:automated-trading-operational-controls` now says so in place of its 'EU text could not be retrieved'. `ev:quant-implementation-failures`: the SEC's Knight (34-70694) and AXA Rosenberg (33-9181) orders, read in Internet Archive captures because sec.gov refused automated retrieval, against Narang's account (his 30 minutes and $400 million against the order's 45 minutes and over $460 million). `mech:order-state-reconciliation`: FIX status requests, execution reports and resend flags from the FIX Trading Community's Orchestra files (FIX Latest EP312, FIXT EP247, commit cd24169), RTS 6 Art. 17(3), with an offline illustration in `notes/artefacts/model-governance-controls/batch40-reconciliation-check.py`. The record is in `notes/migration-slices.md`, *Batch of 17 October 2026*.

Second batch of 2026-10-17 (audit repairs and a 50-item queue; source verification and bounded tests, not study or human review): Audit repair: `mech:order-state-reconciliation` and `batch40-reconciliation-check.py` corrected: a fully filled order is no longer a resubmission candidate. Reconciled state, remaining authorised quantity and a valid intent are separate, with cases for a filled order, a partially filled cancelled order (valid and withdrawn intent), Pending Cancel, duplicate reports and a missing execution; still an offline synthetic illustration. The record is in `notes/migration-slices.md`, *Second batch of 17 October 2026*.

## Related entries owned elsewhere

Cross-referenced, not owned here: `def:automated-trading-architecture` (model accuracy checks, venue messages) and `meth:execution-decision-support` (`execution-trading-costs`); `def:floor-automated-trading-systems` (`execution-market-making`); `def:common-investor-contagion` (`funding-crowding`); `meth:backtest-evaluation-diagnostics`, `pit:parameter-overfitting` (`backtest-inference`); `res:arbitrage-risks` (`execution-market-making`).

## Entry backlog

- meth:strategy-promotion-criteria: evidence, owners and records for promoting a strategy from backtest to embargo, paper trading and production, for re-allocating and for decommissioning, against López de Prado's unquantified stages (`s8-governance`, `wide-pra-ss123`, unread).

- meth:discretionary-override-governance: who may override or switch off a model, on what evidence, with what record and review, against Narang's "discretionary overrides" for exogenous shocks (`s8-governance`, `w4-simonian-model-governance`, unread).

## Legacy candidate material

Run `python3 tools/migration_status.py` for the current counts. No legacy file lists this pathway since slice 26 migrated `sysinv/modelrisk.tex`.

## What changed in my view or practice

## Questions carried forward

- Which audit-trail and record-keeping rules (for example the U.S. consolidated audit trail, or EU order-record rules) should replace Harris's 2002 description in the entry?
- Map the entry's controls to the Knight Capital failure points (`wide-knight-capital`, unread).
