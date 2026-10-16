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

## Source verification after slice 37

Second slice-37 follow-up, 2026-10-16, working source gaps of slice 36 (source verification, not study): `def:multi-level-ofi` resolved (Cont, Cucuringu and Zhang, arXiv v4 of 13 June 2023: ten levels, PCA-integrated OFI explaining 89 percent of the levels' variance, LOBSTER 2017-2019 top 100 S&P 500 stocks, 30-minute windows; integrated OFI lifts contemporaneous out-of-sample R^2 from 64.6 to 83.8 percent, cross-asset terms add little contemporaneously, and one-minute forecasts have negative out-of-sample R^2; their per-level flow uses the new size where Cont, Kukanov and Stoikov use the old; the legacy's cross-venue pressure remains an unsourced construction). Entries corrected in the same follow-up are listed in `notes/migration-slices.md`, *Slice 37 second follow-up*.

Source follow-up of slices 33-36 and the slice-37 audit, 2026-10-16 (source verification, not study): `ev:ofi-forecast-horizons` narrowed (LOBCAST: F1 48-61 percent on 2021-22 LOBSTER data, horizon effects not monotone; Kolm et al. blocked); `meth:lob-signal-transaction-usefulness` narrowed (Briola, Bartolucci and Aste, arXiv v4: p_T = CT/(PT + TT - CT) is an assumption-free overlap of predicted and realised round trips, not profit after spread or fees; validation days inside the training window; the checklist itself is still without a source, and no signal of ours has been costed). The record is in `notes/migration-slices.md`, *Source follow-up of slices 33-36 and slice-37 audit corrections*.

Audit correction of 2026-10-16 (`def:order-flow-imbalance`): Cont, Cucuringu and Zhang selected their 100 stocks by market capitalisation on 31 December 2019 (n. 3, p. 5), the end of their 2017-2019 sample; the entry now states that universe-selection look-ahead, separates it from their rolling train/test design, and does not call the reported calculations invalid.

Second source follow-up, 2026-10-16 (source verification, not study or human review): `ev:ofi-forecast-horizons` resolved in the working-paper version (Kolm, Turiel and Westray, SSRN 6 August 2021: 115 Nasdaq stocks 2019-2020, stock-specific horizons, order-flow inputs beat book states for most stocks, out-of-sample R^2 peaks near two average price changes, no costs; the Mathematical Finance version not compared); `meth:lob-signal-transaction-usefulness` unchanged (no new source in this batch; the gap recorded on 16 October 2026 stands). The record is in `notes/migration-slices.md`, *Second source follow-up of the slice 33-37 queue*.

## Related entries owned elsewhere

Slice 36, 2026-10-16, migrated this pathway's two remaining candidate files, but by content most of their blocks went elsewhere (routing exceptions recorded in `notes/migration-slices.md`): the feature-engineering file's blocks concern relative-value arbitrage, not order-book prediction, and went to `res:arbitrage-risks`, `def:trader-motives` and `meth:triple-barrier-labelling`; the data-engineering file's to `data:market-data-levels` and `data:trading-reference-data` (`point-in-time-data`), `meth:venue-market-share`, `meth:spread-volatility-regression`, `meth:intraday-deseasonalisation` and the new `meth:skill-luck-significance-tests` (`performance-manager-evaluation`). The one block on transaction-level usefulness became a backlog stub (below). No block of either file asserts a multilevel or cross-asset OFI result; those wait on the stubs already here. Artefacts: `notes/artefacts/lob-deep-learning/feature-engineering-microstructure-alpha.tex` and `microstructure-data-engineering.tex`.

## Entry backlog

- meth:lob-signal-transaction-usefulness: how to judge an order-book signal by what it is worth after trading: forecast target (mid-price, spread, fill, volatility), tradability (spread, queue loss, fees, access), capacity, stability across tick size, latency and participants, and crowding; the legacy evaluation list (slice 36) is a checklist without a source, and the checkpoint's "probability of profitable round trips after spread" (Briola et al., `w2-briola-lob-guide`; LOBCAST, `w2-lobcast`) is unread

## Legacy candidate material

Run `python3 tools/migration_status.py` for the current counts. Slice 36 migrated both remaining candidate files and removed the legacy microstructure chapter; no legacy file now lists this pathway.

## What changed in my view or practice

## Questions carried forward

- Cont, Kukanov and Stoikov fit contemporaneous price changes; how much of the 65 percent $R^2$ survives as a forecast of the next interval, and on post-2010 data?
