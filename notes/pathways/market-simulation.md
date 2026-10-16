---
key: market-simulation
section: execution-market-making
status: not started (draft entries from the migration only)
---

# Market simulation and counterfactual testing

Pathway outcome, from the guide: build or select a market simulator and validate it against stylised facts and counterfactual responses before using it to train or test strategies.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. This note was opened on 16 October 2026 by migration slice 33 (`notes/migration.md`), which wrote five entries for this pathway from the legacy stylised-facts, event-time and order-flow-model files, checked against Lehalle and Laruelle (`alpha-laruelle`), Bouchaud et al. (`catalogue-0528`) and Hasbrouck (`s6-hasbrouck`). None of the pathway's required readings has been read; the checkpoint has not been attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

- `ev:high-frequency-stylised-facts`: heavy tails, volatility clustering, order-sign long memory, activity clustering and intraday patterns, each with Bouchaud et al.'s sample (2011--2015).
- `meth:realised-variance-signature-plot`: realised variance and covariance, the signature plot in two forms, microstructure noise and the Epps effect.
- `meth:intraday-deseasonalisation`: Lehalle and Laruelle's additive and multiplicative decompositions, centred moving averages and volume model, with the look-ahead of two-sided averages.
- `def:market-clocks-durations`: durations; event, trade, quote, volume and business time; Hasbrouck's rule for choosing an index.
- `def:order-event-point-processes`: counting processes, intensities, the Poisson baseline and the time-change theorem (with Lehalle and Laruelle's misprinted condition corrected).

All five: partly checked 2026-10-16, draft; human review outstanding. Artefacts: `notes/artefacts/market-simulation/stylized-facts.tex` and `trade-duration-event-time.tex` (legacy files verbatim), `04-overview-original.tex` (the folder's wrapper before slice 33) and `order-flow-checks.py` (simulations for all slice-33 entries). The simulator's building blocks, Hawkes processes and queue-reactive intensities, are owned by `market-making-lob` and cross-referenced, not listed here.

Changed in the slice-33 follow-up, 2026-10-16: `meth:realised-variance-signature-plot` (limits restricted to continuous Itô processes; quadratic-variation limits with jumps and co-jumps; the noise expectation's assumptions stated as exact for the simulated driftless Brownian model; a unit-jump Poisson counterexample in `order-flow-checks.py`).

Changed in migration slice 36, 2026-10-16: `meth:intraday-deseasonalisation` (Lehalle and Laruelle's mean-against-path warning, app. A.14.1, and a simulated example), from the data-engineering file, which listed this pathway; the file's other blocks were routed by content (see `lob-deep-learning`). Partly checked, draft.

## Entry backlog

- res:time-rescaling-theorem: the half-line statement (compensator continuous and divergent) from a point-process text such as Daley and Vere-Jones; Brown et al. (2002) was read for the finite-window theorem (positive conditional intensity, finite integrated intensity) and the KS goodness-of-fit bands

## Source verification after slice 37

Source follow-up of slices 33-36 and the slice-37 audit, 2026-10-16 (source verification, not study): `meth:refresh-time-covariance` narrowed (Definition 1, Assumptions 1-2 and sec. 5.3 read; refresh-time realised covariance biased without lead-lag terms in simulation); `res:time-rescaling-theorem` narrowed (Brown, Barbieri, Ventura, Kass and Frank, Neural Computation 14(2), pp. 325-331); `ev:simulator-realism-metrics` resolved (Vyetrenko et al., arXiv v1: five groups of stylised-fact checks and ABIDES comparisons; Noble, Rosenbaum and Souilmi, arXiv v1: in-sample validation statistics on Databento data 2023-2025, a 29-microsecond inter-event mode and an impact state; the ACM version of the former not compared). The record is in `notes/migration-slices.md`, *Source follow-up of slices 33-36 and slice-37 audit corrections*.

Second source follow-up, 2026-10-16 (source verification, not study or human review): `meth:refresh-time-covariance` resolved (Hayashi and Yoshida, Bernoulli 2005, author copy: Condition C, Definition 3.1, Theorem 3.1 and Remarks 3.3-3.4; noise outside the model); `res:time-rescaling-theorem` unchanged (no new source in this batch; the gap recorded on 16 October 2026 stands). The record is in `notes/migration-slices.md`, *Second source follow-up of the slice 33-37 queue*.

## Legacy candidate material

Run `python3 tools/migration_status.py` for the current counts. Slice 36 migrated the data-engineering file and removed the legacy microstructure chapter; no legacy file now lists this pathway.

## What changed in my view or practice

## Questions carried forward

- Bouchaud et al.'s E-mini signature plot is nearly flat while Lehalle and Laruelle's Rio Tinto realised variance diverges at fine steps: is the difference the instrument, the price used (mid against trade) or the plot's units?
