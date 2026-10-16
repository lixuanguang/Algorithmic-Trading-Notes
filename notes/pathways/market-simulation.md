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

## Entry backlog

- meth:refresh-time-covariance: covariance estimators for asynchronous prices (refresh-time sampling, Hayashi--Yoshida), with their conditions; named by the legacy notes and by Lehalle and Laruelle (p. 318), none read; the slice-33 check shows previous-tick sampling itself produces an Epps effect
- res:time-rescaling-theorem: the time-change theorem with its exact conditions (compensator continuous and divergent) from a point-process text such as Daley and Vere-Jones; Lehalle and Laruelle print the condition as $\int_0^\infty\lambda=1$ (p. 308)
- ev:simulator-realism-metrics: the stylised-fact metrics a simulator is scored on, from Vyetrenko et al. (`w2-vyetrenko-realism`) and the reality-gap tests of Noble, Rosenbaum and Souilmi (`exp-noble-rosenbaum-souilmi-reality-gap`), required readings not read

## Legacy candidate material

Run `python3 tools/migration_status.py` for the current counts. After slice 33 the pathway's remaining candidate is the data-engineering file (`04_order_flow_and_empirical_microstructure/09_...`, shared with `lob-deep-learning`).

## What changed in my view or practice

## Questions carried forward

- Bouchaud et al.'s E-mini signature plot is nearly flat while Lehalle and Laruelle's Rio Tinto realised variance diverges at fine steps: is the difference the instrument, the price used (mid against trade) or the plot's units?
