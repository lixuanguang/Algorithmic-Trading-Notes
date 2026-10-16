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

## Related entries owned elsewhere

Slice 36, 2026-10-16, migrated this pathway's two remaining candidate files, but by content most of their blocks went elsewhere (routing exceptions recorded in `notes/migration-slices.md`): the feature-engineering file's blocks concern relative-value arbitrage, not order-book prediction, and went to `res:arbitrage-risks`, `def:trader-motives` and `meth:triple-barrier-labelling`; the data-engineering file's to `data:market-data-levels` and `data:trading-reference-data` (`point-in-time-data`), `meth:venue-market-share`, `meth:spread-volatility-regression`, `meth:intraday-deseasonalisation` and the new `meth:skill-luck-significance-tests` (`performance-manager-evaluation`). The one block on transaction-level usefulness became a backlog stub (below). No block of either file asserts a multilevel or cross-asset OFI result; those wait on the stubs already here. Artefacts: `notes/artefacts/lob-deep-learning/feature-engineering-microstructure-alpha.tex` and `microstructure-data-engineering.tex`.

## Entry backlog

- def:multi-level-ofi: multi-level OFI integrated across book depth, and cross-asset OFI, with sample, horizons and out-of-sample design, from Cont, Cucuringu and Zhang (`wide-cont-cross-impact-ofi`, a required reading, not read); the legacy "multi-level" and "cross-venue" imbalance features wait on it
- ev:ofi-forecast-horizons: how OFI-based forecasts degrade with horizon and across stocks and periods, from Kolm, Turiel and Westray (`wide-kolm-deep-ofi`) and the LOBCAST benchmark (`w2-lobcast`); the legacy caveat "imbalance is horizon-dependent" was found in neither source read and waits on these
- meth:lob-signal-transaction-usefulness: how to judge an order-book signal by what it is worth after trading: forecast target (mid-price, spread, fill, volatility), tradability (spread, queue loss, fees, access), capacity, stability across tick size, latency and participants, and crowding; the legacy evaluation list (slice 36) is a checklist without a source, and the checkpoint's "probability of profitable round trips after spread" (Briola et al., `w2-briola-lob-guide`; LOBCAST, `w2-lobcast`) is unread

## Legacy candidate material

Run `python3 tools/migration_status.py` for the current counts. Slice 36 migrated both remaining candidate files and removed the legacy microstructure chapter; no legacy file now lists this pathway.

## What changed in my view or practice

## Questions carried forward

- Cont, Kukanov and Stoikov fit contemporaneous price changes; how much of the 65 percent $R^2$ survives as a forecast of the next interval, and on post-2010 data?
