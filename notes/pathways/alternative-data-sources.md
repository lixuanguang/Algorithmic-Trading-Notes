---
key: alternative-data-sources
section: ml-alternative-data
status: not started (draft entries only, not from study)
---

# Alternative data: sources, information value and market effects

Pathway outcome, from the guide: assess an alternative dataset by its coverage, timing and incremental information over consensus, test its return and fundamentals predictability, and judge how its edge decays as access spreads. Its checkpoint joins one alternative sales proxy for listed retailers with documented coverage start dates and release lags, tests it against analyst consensus in a point-in-time panel, and compares the effect before and after the data became widely sold. Its fourteen readings run from practitioner and institutional framing (`wide-kolanovic-big-data`, `rf-monk-prins-rook-2019`) through evidence on specific datasets (`rf-froot-kang-ozik-sadka-2017`, `rf-dichev-qian-2022`, `rf-kang-stice-lawrence-wong-2021`, `wide-green-employer-reviews`, `rf-chen-de-hu-hwang-2014`, `eq-da-engelberg-gao-2011`) to market effects and the economics of data (`rf-katona-painter-patatoukas-zeng-2025`, `exp-altdata-governance`, `rf-grennan-michaely-2021`, `rf-dessaint-foucault-fresard-2024`, `exp-financial-data-value`, `rf-farboodi-veldkamp-2020`).

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 16 October 2026 by financial data and labels review (`notes/source-review-records.md`). The entry rests on López de Prado (`alpha-afml`, chap. 2) and Velu, Hardy and Nehren (`s3-velu`, chap. 1), neither a reading of this pathway; López de Prado takes his split of alternative data from `wide-kolanovic-big-data`, the pathway's first reading, which was not opened. The checkpoint was not attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in financial data and labels / source review / optimal execution / execution control reviews:

- `def:financial-data-types`: López de Prado's fundamental, market, analytics and alternative data, with release lags, backfilling and reinstatement, cost, crowding of analytics, and his opinions marked as opinions; Velu, Hardy and Nehren's fundamental and analyst inputs with their hedges restored, and their point that a dataset's value falls as access spreads.

Partly checked 2026-10-16, draft; human review outstanding.

## Source verification after macro markets and pricing review

method validation (2026-10-17) (audit repairs and a source-review coverage; source verification and bounded tests, not study or human review): Queue: `meth:alternative-dataset-assessment` unchanged and blocked: Monk, Prins and Rook (CAIA copy 404; Stanford page links SSRN, which refuses automated retrieval) and Kolanovic and Krishnamachari (no public authorised copy) not obtained. The record is in `notes/source-review-records.md`, *method validation (2026-10-17)*.

empirical extensions (2026-10-17) (six audit repairs and a source-review coverage; source verification and bounded tests, not study or human review): `ev:alternative-data-edge-decay` narrowed (Dessaint, Foucault and Frésard and Farboodi and Veldkamp read at abstract level and merged); `ev:holdings-insider-ratings-signals` narrowed (Cohen, Malloy and Pomorski (abstract and sec. I) merged). The record is in `notes/source-review-records.md`, *empirical extensions (2026-10-17)*.

derivatives and empirical validation (2026-10-17) (seven audit repairs, backlog reconciliation and a source-review coverage; source verification and bounded tests, not study or human review): the `ev:holdings-insider-ratings-signals` question: Cohen, Malloy and Pomorski's NBER working paper quantified (82 basis points a month value-weighted, $t=2.15$) in `def:financial-data-types`; `ev:holdings-insider-ratings-signals` narrowed to 13F and ratings. The record is in `notes/source-review-records.md`, *derivatives and empirical validation (2026-10-17)*.

## Related entries owned elsewhere

Cross-referenced, not owned here: `data:trading-reference-data`, `data:market-data-levels`, `data:derived-market-statistics` (`point-in-time-data`); `meth:activity-sampled-bars` (`statistical-learning-foundations`).

## Entry backlog

- ev:alternative-data-edge-decay: measured evidence (sample, period, magnitude) that a dataset's predictive value falls as access to it spreads. Katona, Painter, Patatoukas and Zeng (`rf-katona-painter-patatoukas-zeng-2025`) is unread; Dessaint, Foucault and Frésard and Farboodi and Veldkamp were read at abstract level only, and both concern short-horizon data crowding out long-horizon forecasting rather than the decay of one dataset's edge.
- meth:alternative-dataset-assessment: coverage, history, release lag, vendor backfill and incremental information over consensus, as the checkpoint asks. Neither reading has an accessible copy (`wide-kolanovic-big-data`: no authorised copy of the J.P. Morgan report; `rf-monk-prins-rook-2019`: CAIA copy HTTP 404, SSRN 403; 2026-10-17).
- ev:holdings-insider-ratings-signals: whether 13F holdings changes and rating downgrades predict returns (no source read for either); the insider result is quantified from Cohen, Malloy and Pomorski's NBER working paper in `def:financial-data-types`.

## What changed in my view or practice

## Questions carried forward

- López de Prado's "over 10TB" of FIX data a day has no source or market; is there a primary figure?
