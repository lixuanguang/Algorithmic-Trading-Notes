---
key: lob-deep-learning
section: execution-market-making
status: not started (draft entries from the migration only)
---

# Deep learning on limit-order-book data

Pathway outcome, from the guide: train and evaluate an order-book prediction model with leakage-free splits, realistic benchmarks and transaction-level usefulness.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. This note was opened on 16 October 2026 by migration slice 33 (`notes/migration.md`), which wrote one entry for this pathway from the legacy order-flow-imbalance file, checked against Cont, Kukanov and Stoikov (`catalogue-0503`, arXiv version 3) and Bouchaud et al. (`catalogue-0528`). None of the pathway's required readings has been read; the checkpoint has not been attempted. That is migration and source checking, not study.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

- `def:order-flow-imbalance`: Cont, Kukanov and Stoikov's event-based OFI at the best quotes against signed trade volume (trade imbalance), with their April 2010 TAQ evidence, the naming collision with Bouchaud et al.'s "order-flow imbalance", and the legacy menu of imbalance features. It is the "linear OFI baseline" of the checkpoint, not yet implemented.

Partly checked 2026-10-16, draft; human review outstanding. Artefact: `notes/artefacts/lob-deep-learning/order-flow-imbalance.tex` (the legacy file verbatim). Related entries owned elsewhere, cross-referenced and not listed here: queue imbalance and queue-reactive intensities (`market-making-lob`), trade-sign classification (`price-impact-execution`), realised variance and intraday deseasonalisation (`market-simulation`; the latter's look-ahead warning matters for features), and the time-validity pitfall (`financial-ml-evaluation`).

## Entry backlog

- def:multi-level-ofi: multi-level OFI integrated across book depth, and cross-asset OFI, with sample, horizons and out-of-sample design, from Cont, Cucuringu and Zhang (`wide-cont-cross-impact-ofi`, a required reading, not read); the legacy "multi-level" and "cross-venue" imbalance features wait on it
- ev:ofi-forecast-horizons: how OFI-based forecasts degrade with horizon and across stocks and periods, from Kolm, Turiel and Westray (`wide-kolm-deep-ofi`) and the LOBCAST benchmark (`w2-lobcast`); the legacy caveat "imbalance is horizon-dependent" was found in neither source read and waits on these

## Legacy candidate material

Run `python3 tools/migration_status.py` for the current counts. After slice 33 the pathway's candidates are the feature-engineering file (`04_order_flow_and_empirical_microstructure/08_...`, its only exclusive file) and the data-engineering file (`09_...`, shared with `market-simulation`).

## What changed in my view or practice

## Questions carried forward

- Cont, Kukanov and Stoikov fit contemporaneous price changes; how much of the 65 percent $R^2$ survives as a forecast of the next interval, and on post-2010 data?
