---
key: lob-deep-learning
section: execution-market-making
status: not started (draft entries only, not from study)
---

# Deep learning on limit-order-book data

Pathway outcome, from the guide: train and evaluate an order-book prediction model with leakage-free splits, realistic benchmarks and transaction-level usefulness.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. This note was opened on 16 October 2026 by order books and order flow review (`notes/source-review-index.md`). (`catalogue-0528`). At order books and order flow review none of the pathway's required readings had been read. Correction of 2026-10-17, superseding that sentence for the current state: specified sections of Briola, Bartolucci and Aste (arXiv v4, secs. 4-7, pp. 7-8 and 22-25), LOBCAST (arXiv v2, pp. 1-10), Kolm, Turiel and Westray (SSRN 6 August 2021, PDF pp. 1-31) and Cont, Cucuringu and Zhang (arXiv v4) were source-checked on 16 October 2026 against the entries that cite them. That is source checking, not study: no reading has been studied in full, the LOBCAST supplemental material (SUP, which holds its trading simulation) and Briola et al.'s Appendices A-C (in the same arXiv PDF) are unread, and the checkpoint, including a costed test of an order-book signal of ours, has not been attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

- `def:order-flow-imbalance`: Cont, Kukanov and Stoikov's event-based OFI at the best quotes against signed trade volume (trade imbalance), with their April 2010 TAQ evidence, the naming collision with Bouchaud et al.'s "order-flow imbalance". It is the "linear OFI baseline" of the checkpoint, not yet implemented.

Partly checked 2026-10-16, draft; human review outstanding. Related entries owned elsewhere, cross-referenced and not listed here: queue imbalance and queue-reactive intensities (`market-making-lob`), trade-sign classification (`price-impact-execution`), realised variance and intraday deseasonalisation (`market-simulation`; the latter's look-ahead warning matters for features), and the time-validity pitfall (`financial-ml-evaluation`).

## Source verification after macro markets and pricing review

Second macro markets and pricing review follow-up, 2026-10-16, working source gaps of dealer models and information review (source verification, not study): `def:multi-level-ofi` resolved. Entries corrected in the same follow-up are listed in `notes/source-review-records.md`, *macro markets and pricing review second follow-up*.

Source follow-up of order books and order flow / dealer models and information reviews and the macro markets and pricing review audit, 2026-10-16 (source verification, not study): `ev:ofi-forecast-horizons` narrowed (LOBCAST: F1 48-61 percent on 2021-22 LOBSTER data, horizon effects not monotone; Kolm et al. blocked); `meth:lob-signal-transaction-usefulness` narrowed (Briola, Bartolucci and Aste, arXiv v4: p_T = CT/(PT + TT - CT) is an assumption-free overlap of predicted and realised round trips, not profit after spread or fees; validation days inside the training window; the checklist itself is still without a source, and no signal of ours has been costed). The record is in `notes/source-review-records.md`, *Source follow-up of order books and order flow / dealer models and information reviews and macro markets and pricing review audit corrections*.

Audit correction of 2026-10-16 (`def:order-flow-imbalance`): Cont, Cucuringu and Zhang selected their 100 stocks by market capitalisation on 31 December 2019 (n. 3, p. 5), the end of their 2017-2019 sample; the entry now states that universe-selection look-ahead, separates it from their rolling train/test design, and does not call the reported calculations invalid.

Second source follow-up, 2026-10-16 (source verification, not study or human review): `ev:ofi-forecast-horizons` resolved in the working-paper version (Kolm, Turiel and Westray, SSRN 6 August 2021: 115 Nasdaq stocks 2019-2020, stock-specific horizons, order-flow inputs beat book states for most stocks, out-of-sample R^2 peaks near two average price changes, no costs; the Mathematical Finance version not compared); `meth:lob-signal-transaction-usefulness` unchanged (no new source in this batch; the gap recorded on 16 October 2026 stands). The record is in `notes/source-review-records.md`, *Second source follow-up of the order books and order flow / macro markets and pricing reviews queue*.

source verification (2026-10-17) (source verification and bounded tests, not study or human review): Audit corrections: the Kolm, Turiel and Westray summary in `def:order-flow-imbalance` and `notes/readings/wide-kolm-deep-ofi.md` no longer says the CNN-LSTM did better with book inputs for 23-45 stocks; Table 3's entries are net counts (significantly favouring OF minus significantly favouring LOB; CNN-LSTM 70-93), the source's wording is ambiguous and no exact count is stated; the decline beyond two average price changes is cited to Fig. 8 (PDF p. 28), not Fig. 2. The Status paragraph above is corrected: specified sections were source-checked, while full study, the LOBCAST supplement (SUP sec. 7), Briola et al.'s Appendices A-C and a costed checkpoint remain incomplete. `meth:lob-signal-transaction-usefulness` narrowed: the checklist's tradability, latency and tick-size items now have sources (Briola et al. sec. 7, pp. 22-23, and Table 7; LOBCAST; Kolm et al.; Gould and Bonart; Moallemi and Saglam), and a costed test is specified in `def:order-flow-imbalance` but not run (LOBSTER's free samples now need a request and accepted terms); capacity and crowding remain unsourced. The record is in `notes/source-review-records.md`, *source verification (2026-10-17)*.

method validation (2026-10-17) (audit repairs and a source-review coverage; source verification and bounded tests, not study or human review): Queue: `meth:lob-signal-transaction-usefulness` unchanged (licensed message data still required). The record is in `notes/source-review-records.md`, *method validation (2026-10-17)*.

derivatives and empirical validation (2026-10-17) (seven audit repairs, backlog reconciliation and a source-review coverage; source verification and bounded tests, not study or human review): backlog reconciliation only: the backlog lines below were rewritten to state the remaining gap alone, removing stacked dated status prefixes and claims that material was unread or not obtained where earlier batches had read it. The record is in `notes/source-review-records.md`, *derivatives and empirical validation (2026-10-17)*.

## Related entries owned elsewhere

dealer models and information / source review / optimal execution / execution control reviews; the data-engineering file's to `data:market-data-levels` and `data:trading-reference-data` (`point-in-time-data`), `meth:venue-market-share`, `meth:spread-volatility-regression`, `meth:intraday-deseasonalisation` and the new `meth:skill-luck-significance-tests` (`performance-manager-evaluation`). Transaction-level usefulness is a backlog stub (below). Multilevel and cross-asset OFI results wait on the stubs already here.

## Entry backlog

- meth:lob-signal-transaction-usefulness: a source for the capacity and crowding items, and the costed test specified in the entry, which needs licensed message data (LOBSTER samples now require a request and accepted terms). Briola et al.'s backtest assumptions and clock-time horizons, LOBCAST's and Kolm et al.'s cost cautions, Gould and Bonart's out-of-sample scores and Moallemi and Saglam's latency cost are in `def:order-flow-imbalance`.

## What changed in my view or practice

## Questions carried forward

- Cont, Kukanov and Stoikov fit contemporaneous price changes; how much of the 65 percent $R^2$ survives as a forecast of the next interval, and on post-2010 data?
