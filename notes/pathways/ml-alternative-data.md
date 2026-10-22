---
key: ml-alternative-data
section: ml-alternative-data
status: not started (draft entries only, not from study)
---

# Machine learning and alternative data (section overview)

A compendium section in Part II, *Empirical finance, machine learning and research governance*, declared in `compendium/compendium.tex`. Overview outcome, from the guide: Test whether a filing-text feature adds decision-time predictive value beyond a dictionary measure and a simple market baseline, reporting coverage, missingness, the full model search and loss uncertainty.

Its checkpoint, from the guide: Create a filing-text feature with a documented release-time join and coverage history. Compare a dictionary, finance-language model and simple market baseline on untouched chronological data; report missingness, the complete model search and loss uncertainty before any portfolio claim.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Populated before this note existed; the content migration of 22 October 2026 added this overview without changing the entries' verification, coverage or mastery state. Entry histories and source-review references are in [alternative-data-sources.md](alternative-data-sources.md), [financial-ml-evaluation.md](financial-ml-evaluation.md), [statistical-learning-foundations.md](statistical-learning-foundations.md).

Moved out by the content migration of 22 October 2026, with labels and content unchanged: to `execution-trading-costs`: `mod:cartea-jaimungal-execution`.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries

By pathway, in compiled order: each printed pathway is a numbered section of the chapter, and a pathway with several topic files prints each as a subsection.

- `statistical-learning-foundations` (Statistical learning foundations and time-series validation):
  - *The data-science workflow* (`data-science-workflow.tex`): `def:financial-data-science-uses`, `meth:data-analysis-project`, `meth:ml-model-training-evaluation`.
  - *Machine learning methods* (`machine-learning-methods.tex`): `def:learning-methods-overfitting`, `meth:supervised-algorithm-selection`, `meth:unsupervised-algorithm-selection`.
  - *Financial data structures: bars, multi-product series and event sampling* (`financial-data-structures.tex`): `meth:activity-sampled-bars`, `meth:information-driven-bars`, `meth:etf-trick`, `meth:event-based-sampling`.
  - *Labels and sample weights for overlapping financial outcomes* (`labelling-sample-weights.tex`): `meth:triple-barrier-labelling`, `meth:meta-labelling`, `def:label-concurrency-uniqueness`, `meth:sequential-bootstrap`, `meth:sample-weights-attribution-decay`, `meth:purged-embargoed-cross-validation`.
  - *Fractionally differentiated features* (`fractional-differentiation.tex`): `mod:fractional-differencing-weights`, `meth:fixed-width-fractional-differencing`.
- `financial-ml-evaluation` (Financial ML: information timing, uncertainty and portfolio tests; `ml-time-validity.tex`): `pit:label-weight-leakage`, `meth:time-valid-ml-experiment-record`.
- `text-llm-agents` (Text, language models and agent evaluation; `text-features.tex`): `meth:text-feature-engineering`.
- `alternative-data-sources` (Alternative data: sources, information value and market effects; `financial-data-types.tex`): `def:financial-data-types`.

## Specialist pathways

The guide's pathways for this section, in its order, with the existing material, partial treatment or content gap as recorded by the content migration of 22 October 2026 and its closeout review. A pathway with related material but no note has not been opened. A partial treatment names the existing entries that treat some of the pathway's subtopics, wherever they sit, and the subtopics with nothing written.

Printed as numbered sections of the chapter, under the guide pinned at `8302467` (`subsection_alignment_plan.md`): `statistical-learning-foundations`, `financial-ml-evaluation`, `text-llm-agents`, `alternative-data-sources`. A pathway without entries of its own is not printed; the related material and partial treatments named below are printed under the pathway or section that owns them.

- `statistical-learning-foundations` (Statistical learning foundations and time-series validation): pathway note [statistical-learning-foundations.md](statistical-learning-foundations.md), 19 entries listed, in `ml-alternative-data/data-science-workflow`, `ml-alternative-data/financial-data-structures`, `ml-alternative-data/fractional-differentiation`, `ml-alternative-data/labelling-sample-weights`, `ml-alternative-data/machine-learning-methods`, `ml-alternative-data/text-features`.
- `ml-asset-pricing` (ML return prediction and asset pricing): no pathway note; partial treatment in existing entries, not reviewed as complete: deep-learning short-horizon return forecasts from order-book data (`def:order-flow-imbalance` in `execution-market-making/order-flow-imbalance`). Not written: cross-sectional ML return prediction; ML asset-pricing and latent-factor models.
- `financial-ml-evaluation` (Financial ML: information timing, uncertainty and portfolio tests): pathway note [financial-ml-evaluation.md](financial-ml-evaluation.md), 2 entries listed, in `ml-alternative-data/ml-time-validity`.
- `forecasting-generative-rl` (Deep forecasting and generative scenarios): no pathway note; partial treatment in existing entries, not reviewed as complete: deep sequence models for order-book forecasting, their horizons and transfer (`def:order-flow-imbalance` in `execution-market-making/order-flow-imbalance`). Not written: deep forecasting beyond the order book; generative scenario models.
- `reinforcement-learning-trading` (Reinforcement learning for trading, hedging and execution): pathway note [reinforcement-learning-trading.md](reinforcement-learning-trading.md), 1 entries listed, in `execution-trading-costs/execution-control`.
- `text-llm-agents` (Text, language models and agent evaluation): no pathway note; related existing material in `ml-alternative-data/text-features`, not reviewed as a complete treatment of the pathway.
- `alternative-data-sources` (Alternative data: sources, information value and market effects): pathway note [alternative-data-sources.md](alternative-data-sources.md), 1 entries listed, in `ml-alternative-data/financial-data-types`.

## Entry backlog

## What changed in my view or practice

## Questions carried forward
