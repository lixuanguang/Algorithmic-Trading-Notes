---
key: market-simulation
section: execution-market-making
status: not started (draft entries only, not from study)
---

# Market simulation and counterfactual testing

Pathway outcome, from the guide: build or select a market simulator and validate it against stylised facts and counterfactual responses before using it to train or test strategies.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. This note was opened on 16 October 2026 by order books and order flow review (`notes/source-review-index.md`). (`catalogue-0528`) and Hasbrouck (`s6-hasbrouck`). None of the pathway's required readings has been read; the checkpoint has not been attempted.

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

All five: partly checked 2026-10-16, draft; human review outstanding. Checks: `order-flow-checks.py`. The simulator's building blocks, Hawkes processes and queue-reactive intensities, are owned by `market-making-lob` and cross-referenced, not listed here.

Changed in the order books and order flow review follow-up, 2026-10-16: `meth:realised-variance-signature-plot` (limits restricted to continuous Itô processes; quadratic-variation limits with jumps and co-jumps; the noise expectation's assumptions stated as exact for the simulated driftless Brownian model; a unit-jump Poisson counterexample in `order-flow-checks.py`).

Changed in dealer models and information / source review / optimal execution / execution control reviews: `meth:intraday-deseasonalisation` (Lehalle and Laruelle's mean-against-path warning, app. A.14.1, and a simulated example). Partly checked, draft.

## Entry backlog

Empty after the source verification (2026-10-17); new stubs go here.

## Source verification after macro markets and pricing review

Source follow-up of order books and order flow / dealer models and information reviews and the macro markets and pricing review audit, 2026-10-16 (source verification, not study): `meth:refresh-time-covariance` narrowed (Definition 1, Assumptions 1-2 and sec. 5.3 read; refresh-time realised covariance biased without lead-lag terms in simulation); `res:time-rescaling-theorem` narrowed (Brown, Barbieri, Ventura, Kass and Frank, Neural Computation 14(2), pp. 325-331); `ev:simulator-realism-metrics` resolved (Vyetrenko et al., arXiv v1: five groups of stylised-fact checks and ABIDES comparisons; Noble, Rosenbaum and Souilmi, arXiv v1: in-sample validation statistics on Databento data 2023-2025, a 29-microsecond inter-event mode and an impact state; the ACM version of the former not compared). The record is in `notes/source-review-records.md`, *Source follow-up of order books and order flow / dealer models and information reviews and macro markets and pricing review audit corrections*.

Second source follow-up, 2026-10-16 (source verification, not study or human review): `meth:refresh-time-covariance` resolved (Hayashi and Yoshida, Bernoulli 2005, author copy: Condition C, Definition 3.1, Theorem 3.1 and Remarks 3.3-3.4; noise outside the model); `res:time-rescaling-theorem` unchanged (no new source in this batch; the gap recorded on 16 October 2026 stands). The record is in `notes/source-review-records.md`, *Second source follow-up of the order books and order flow / macro markets and pricing reviews queue*.

source verification (2026-10-17) (source verification and bounded tests, not study or human review): `res:time-rescaling-theorem` resolved with a caveat by merge into `def:order-event-point-processes`: Laub, Taimre and Pollett (arXiv v1, 2015, Theorem 5, p. 18) restate Daley and Vere-Jones's Proposition 7.4.IV for the half-line, with a monotonic continuous compensator diverging almost surely; Daley and Vere-Jones's own text was not read. The record is in `notes/source-review-records.md`, *source verification (2026-10-17)*.

derivatives and empirical validation (2026-10-17) (seven audit repairs, backlog reconciliation and a source-review coverage; source verification and bounded tests, not study or human review): the `ev:high-frequency-stylised-facts` question: Ratliff-Crain et al.'s retest of Cont's eleven facts (eight supported intraday, three not) merged into `ev:high-frequency-stylised-facts`. The record is in `notes/source-review-records.md`, *derivatives and empirical validation (2026-10-17)*.

## What changed in my view or practice

## Questions carried forward

- Bouchaud et al.'s E-mini signature plot is nearly flat while Lehalle and Laruelle's Rio Tinto realised variance diverges at fine steps: is the difference the instrument, the price used (mid against trade) or the plot's units?
