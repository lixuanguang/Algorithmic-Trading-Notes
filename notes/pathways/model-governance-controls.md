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

- `def:quant-strategy-risk-sources`: model risk (inapplicability, misspecification, implementation errors), regime change and exogenous shocks, kept apart from funding contagion (`funding-crowding`) and operational failure; the legacy "discretionary overrides" qualified as an ungoverned model change.
- `meth:quant-strategy-monitoring`: exposure, profit-and-loss (including how money is made and hit rate), execution and systems monitors as early warnings; execution-algorithm indicators left to the decision-support entry of `execution-trading-costs` (see below).

Both verification partly checked 2026-10-15, stability draft; human review outstanding. Their artefact is `notes/artefacts/model-governance-controls/risk-assessment.tex`, a new file beside the slice-17 `derivations.tex`. The same legacy file's contagion block was routed to `funding-crowding` (its entry is listed below, under related entries).

## Related entries owned elsewhere

Cross-referenced, not owned here: `def:automated-trading-architecture` (model accuracy checks, venue messages) and `meth:execution-decision-support` (`execution-trading-costs`); `def:floor-automated-trading-systems` (`execution-market-making`); `def:common-investor-contagion` (`funding-crowding`); `meth:backtest-evaluation-diagnostics`, `pit:parameter-overfitting` (`backtest-inference`); `res:arbitrage-risks` (`execution-market-making`).

## Entry backlog

- rule:mifid-rts6-algorithmic-controls: Commission Delegated Regulation (EU) 2017/589 (`wide-mifid-rts6`) on testing, kill functionality, pre- and post-trade controls, capacity and business continuity. EUR-Lex returned a bot challenge on 2026-10-15; retrieve the current consolidated text before stating any EU obligation.
- meth:discretionary-override-governance: who may override or switch off a model, on what evidence, with what record and review, against Narang's "discretionary overrides" for exogenous shocks (`s8-governance`, `w4-simonian-model-governance`, unread).
- ev:quant-implementation-failures: Knight Capital's August 2012 loss and AXA Rosenberg's 2007-2010 risk-model coding error as Narang reports them (pp. 195-196), to check against the regulators' orders (`wide-knight-capital`, unread; the AXA Rosenberg order is not catalogued).
- mech:order-state-reconciliation: the protocol-level evidence for reconciling order state after a failure (order status, execution reports, resend and possible-duplicate flags), from the FIX specification (`s6-fix`, a reading of the `research-engineering-validation` overview); the entry's reconciliation steps are currently a synthesis.

## Legacy candidate material

Run `python3 tools/migration_status.py` for the current counts. No legacy file lists this pathway since slice 26 migrated `sysinv/modelrisk.tex`.

## What changed in my view or practice

## Questions carried forward

- Which audit-trail and record-keeping rules (for example the U.S. consolidated audit trail, or EU order-record rules) should replace Harris's 2002 description in the entry?
- Map the entry's controls to the Knight Capital failure points (`wide-knight-capital`, unread).
