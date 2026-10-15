---
key: financial-ml-evaluation
section: ml-alternative-data
status: not started (draft entries from the migration only)
---

# Financial ML: information timing, uncertainty and portfolio tests

Pathway outcome, from the guide: assess a modern ML or language-model result using time-valid inputs, numerical checks, appropriate uncertainty and a portfolio decision after implementation costs. Its checkpoint specifies a small time-valid financial-text or market-stress experiment, recording release times, training cutoffs, tuning trials and held-out dates, and reports interval coverage by regime and after-cost loss. Its eight readings are `alpha-jansen`, `latest-levy-caution-llm`, `latest-pit-language-models`, `exp-implementable-frontier`, `latest-high-dimensional-grs`, `latest-conformal-time-dependence`, `latest-bis-market-stress-ml` and `w5-gneiting-katzfuss`.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 16 October 2026 by migration slice 32 (`notes/migration-slices.md`), which gave this pathway the time-validity consequences of the legacy AFML labelling, sample-weight and fractional-differencing notes, one of the files' three map candidates. The entry rests on López de Prado (`alpha-afml`), which is not a reading of this pathway; none of the pathway's eight readings has been opened, and the checkpoint was not attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in migration slice 32, 2026-10-16:

- `pit:label-weight-leakage`: what López de Prado's labels, uniqueness and attribution weights know about the future, the conditions under which he says there is no leakage, the full-sample choice of the fractional-differencing order and the same-training-set meta-labels, and a train/test checklist (the checklist is the entry's own; purging and embargo unread).

Partly checked 2026-10-16, draft; human review outstanding. Artefacts: `notes/artefacts/statistical-learning-foundations/`.

## Related entries owned elsewhere

Cross-referenced, not owned here: `def:label-concurrency-uniqueness`, `meth:sample-weights-attribution-decay`, `meth:meta-labelling`, `meth:triple-barrier-labelling`, `meth:fixed-width-fractional-differencing`, `meth:event-based-sampling` (`statistical-learning-foundations`); `pit:parameter-overfitting` (`backtest-inference`); `meth:strategy-production-lifecycle` (`model-governance-controls`).

## Entry backlog

- meth:time-valid-ml-experiment-record: recording release times, model-training cutoffs, tuning trials and held-out dates for an ML or language-model result, as the checkpoint asks (`alpha-jansen`, `latest-pit-language-models`, `latest-levy-caution-llm`, unread).

## Legacy candidate material

Run `python3 tools/migration_status.py` for the current counts. After slice 32 no legacy file lists this pathway.

## What changed in my view or practice

## Questions carried forward

- Does López de Prado's chap. 7 purging rule cover labels whose spans start in the training set and end in the test set, and the concurrency counts that mix the two?
