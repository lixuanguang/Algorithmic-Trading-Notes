---
key: research-engineering-validation
section: research-engineering-validation
status: not started (draft entries only, not from study)
---

# Research engineering, data provenance and model validation (section overview)

A compendium section in Part II, *Empirical finance, machine learning and research governance*, declared in `compendium/compendium.tex`. Overview outcome, from the guide: Specify a strategy as a research record (decision timestamp, data vintages, candidate family, economic hypothesis and the evidence that would reject it) and reconstruct a research decision and its eventual trade from versioned identities, data events, experiments and control records.

Its checkpoint, from the guide: Write a one-page research record for a simple public-data signal: the decision timestamp, data vintages, candidate family, economic hypothesis, estimation window, the uncertainty of the headline estimate, risk limits and the evidence that would reject it. Then take one signal decision through raw source, normalised identity, historical revision, model run, order and final position, and produce a replay package that reproduces the decision and P&L after a corrected input arrives, including the failed run and reconciliation differences.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Populated on 22 October 2026 by the content migration, which moved existing draft entries here (3 from `portfolio-construction-risk`). A move changes no source verification, coverage, study or mastery state. Entry histories and source-review references are in [backtest-inference.md](backtest-inference.md), [model-governance-controls.md](model-governance-controls.md), [point-in-time-data.md](point-in-time-data.md), [portfolio-construction-risk.md](portfolio-construction-risk.md).

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries

By pathway, in compiled order: each printed pathway is a numbered section of the chapter, and a pathway with several topic files prints each as a subsection.

- `backtest-inference` (Strategy specification, backtest inference, multiple testing and Sharpe-ratio statistics):
  - *The structure of a quant strategy and its alpha models* (`quant-strategy-structure.tex`): `def:quant-strategy-components`, `def:alpha-model-taxonomy`, `meth:alpha-strategy-specification`.
  - *Strategy research and backtest evaluation* (`backtest-evaluation.tex`): `meth:hypothesis-driven-strategy-research`, `meth:backtest-evaluation-diagnostics`, `pit:parameter-overfitting`, `pit:backtest-cost-short-assumptions`, `meth:backtest-design-evaluation`, `meth:sharpe-ratio-standard-error`, `meth:deflated-sharpe-ratio`, `meth:multiple-testing-control`.
  - *Scenarios, simulation and sensitivity* (`scenario-simulation.tex`): `meth:scenario-simulation-analysis`.
- `point-in-time-data` (Point-in-time data, vendor files and bias control; `point-in-time-data.tex`): `data:trading-reference-data`, `data:market-data-levels`, `data:derived-market-statistics`, `data:holdings-insider-filing-lags`, `meth:bitemporal-reference-tables`.
- `model-governance-controls` (Model governance, AI risk and trading controls):
  - *Operational controls for automated trading* (`trading-controls.tex`): `meth:automated-trading-operational-controls`, `rule:mifid-rts6-algorithmic-controls`, `mech:order-state-reconciliation`, `ev:quant-implementation-failures`.
  - *Sources of strategy risk and their monitoring* (`strategy-risk.tex`): `def:quant-strategy-risk-sources`, `meth:quant-strategy-monitoring`.
  - *The research and production chain of a strategy* (`strategy-production.tex`): `meth:strategy-production-lifecycle`, `meth:strategy-promotion-criteria`, `meth:discretionary-override-governance`.

## Specialist pathways

The guide's pathways for this section, in its order, with the existing material or the content gap as recorded by the content migration of 22 October 2026. A pathway with related material but no note has not been opened.

Printed as numbered sections of the chapter, under the guide pinned at `8302467` (`subsection_alignment_plan.md`): `backtest-inference`, `point-in-time-data`, `model-governance-controls`. A pathway without entries of its own is not printed; the related material and partial treatments named below are printed under the pathway or section that owns them.

- `backtest-inference` (Strategy specification, backtest inference, multiple testing and Sharpe-ratio statistics): pathway note [backtest-inference.md](backtest-inference.md), 9 entries listed, in `research-engineering-validation/backtest-evaluation`, `research-engineering-validation/scenario-simulation`. Broadened by the guide revision of 22 October 2026 (`8302467`) to cover strategy specification; its entries are in `research-engineering-validation/quant-strategy-structure`, `research-engineering-validation/backtest-evaluation`, `research-engineering-validation/scenario-simulation`.
- `point-in-time-data` (Point-in-time data, vendor files and bias control): pathway note [point-in-time-data.md](point-in-time-data.md), 5 entries listed, in `research-engineering-validation/point-in-time-data`.
- `model-governance-controls` (Model governance, AI risk and trading controls): pathway note [model-governance-controls.md](model-governance-controls.md), 9 entries listed, in `research-engineering-validation/strategy-production`, `research-engineering-validation/strategy-risk`, `research-engineering-validation/trading-controls`.
- `reproducible-research-code` (Reproducible research code, data validation and ML systems): no pathway note; related existing material in `research-engineering-validation/strategy-production`, not reviewed as a complete treatment of the pathway.

## Entry backlog

## What changed in my view or practice

## Questions carried forward
