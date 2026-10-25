---
key: financial-ml-evaluation
section: ml-alternative-data
status: not started (draft entries only, not from study)
---

# Financial ML: information timing, uncertainty and portfolio tests

Pathway outcome, from the guide: assess a modern ML or language-model result using time-valid inputs, numerical checks, appropriate uncertainty and a portfolio decision after implementation costs. Its checkpoint specifies a small time-valid financial-text or market-stress experiment, recording release times, training cutoffs, tuning trials and held-out dates, and reports interval coverage by regime and after-cost loss. Its eight readings are `alpha-jansen`, `latest-levy-caution-llm`, `latest-pit-language-models`, `exp-implementable-frontier`, `latest-high-dimensional-grs`, `latest-conformal-time-dependence`, `latest-bis-market-stress-ml` and `w5-gneiting-katzfuss`.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 16 October 2026 by financial data and labels review (`notes/source-review-records.md`). The entry rests on López de Prado (`alpha-afml`), which is not a reading of this pathway; none of the pathway's eight readings has been opened, and the checkpoint was not attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in financial data and labels / source review / optimal execution / execution control reviews:

- `pit:label-weight-leakage`: what López de Prado's labels, uniqueness and attribution weights know about the future, the conditions under which he says there is no leakage, the full-sample choice of the fractional-differencing order and the same-training-set meta-labels, and a train/test checklist (the checklist is the entry's own; purging and embargo unread).

Partly checked 2026-10-16, draft; human review outstanding. Numerical checks: `trading_notes.numerical.ml_alternative_data.afml_checks`, `trading_notes.numerical.labelling_sample_weights.purged_cv_checks` and `.financial_labels_checks`.

method validation (2026-10-17):

- `meth:time-valid-ml-experiment-record`: release times, model and pretraining cutoffs, tuning trials and held-out dates for an ML or language-model result, from Kelly et al.'s point-in-time models. Partly checked 2026-10-17, draft.

## Source verification after macro markets and pricing review

method validation (2026-10-17) (audit repairs and a source-review coverage; source verification and bounded tests, not study or human review): Queue: `meth:time-valid-ml-experiment-record` resolved as a new entry in `ml-alternative-data/labelling-sample-weights.tex` from Kelly, Malamud, Schwab and Xu's point-in-time language models (NBER WP 35247, May 2026); Levy (SSRN 403) and Jansen's third edition were not read. The record is in `notes/source-review-records.md`, *method validation (2026-10-17)*.

empirical extensions (2026-10-17) (six audit repairs and a source-review coverage; source verification and bounded tests, not study or human review): `meth:time-valid-ml-experiment-record` narrowed (He, Lv, Manela and Wu's abstract merged; Levy's full text refused again (Wiley 403)). The record is in `notes/source-review-records.md`, *empirical extensions (2026-10-17)*.

derivatives and empirical validation (2026-10-17) (seven audit repairs, backlog reconciliation and a source-review coverage; source verification and bounded tests, not study or human review): the `pit:ml-leakage-taxonomy` question: Kapoor and Narayanan's leakage taxonomy merged into `meth:time-valid-ml-experiment-record`, which lacks duplicate and test-window-selection checks. The record is in `notes/source-review-records.md`, *derivatives and empirical validation (2026-10-17)*.

## Related entries owned elsewhere

Cross-referenced, not owned here: `def:label-concurrency-uniqueness`, `meth:sample-weights-attribution-decay`, `meth:meta-labelling`, `meth:triple-barrier-labelling`, `meth:fixed-width-fractional-differencing`, `meth:event-based-sampling` (`statistical-learning-foundations`); `pit:parameter-overfitting` (`backtest-inference`); `meth:strategy-production-lifecycle` (`model-governance-controls`).

## Entry backlog

- meth:time-valid-ml-experiment-record: Levy's look-ahead study (`latest-levy-caution-llm`; SSRN and Wiley refused automated retrieval on 2026-10-17) and Jansen's third edition (`alpha-jansen`). `latest-pit-language-models` and He, Lv, Manela and Wu's abstract are in the entry.

## What changed in my view or practice

## Questions carried forward

- Does López de Prado's chap. 7 purging rule cover labels whose spans start in the training set and end in the test set, and the concurrency counts that mix the two?
