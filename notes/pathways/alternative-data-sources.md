---
key: alternative-data-sources
section: ml-alternative-data
status: not started (draft entries from the migration only)
---

# Alternative data: sources, information value and market effects

Pathway outcome, from the guide: assess an alternative dataset by its coverage, timing and incremental information over consensus, test its return and fundamentals predictability, and judge how its edge decays as access spreads. Its checkpoint joins one alternative sales proxy for listed retailers with documented coverage start dates and release lags, tests it against analyst consensus in a point-in-time panel, and compares the effect before and after the data became widely sold. Its fourteen readings run from practitioner and institutional framing (`wide-kolanovic-big-data`, `rf-monk-prins-rook-2019`) through evidence on specific datasets (`rf-froot-kang-ozik-sadka-2017`, `rf-dichev-qian-2022`, `rf-kang-stice-lawrence-wong-2021`, `wide-green-employer-reviews`, `rf-chen-de-hu-hwang-2014`, `eq-da-engelberg-gao-2011`) to market effects and the economics of data (`rf-katona-painter-patatoukas-zeng-2025`, `exp-altdata-governance`, `rf-grennan-michaely-2021`, `rf-dessaint-foucault-fresard-2024`, `exp-financial-data-value`, `rf-farboodi-veldkamp-2020`).

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 16 October 2026 by migration slice 32 (`notes/migration-slices.md`), which gave this pathway the legacy taxonomy file's table, its four characteristics remarks and its fundamental-and-other-data block. The entry rests on López de Prado (`alpha-afml`, chap. 2) and Velu, Hardy and Nehren (`s3-velu`, chap. 1), neither a reading of this pathway; López de Prado takes his split of alternative data from `wide-kolanovic-big-data`, the pathway's first reading, which was not opened. The checkpoint was not attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in migration slice 32, 2026-10-16:

- `def:financial-data-types`: López de Prado's fundamental, market, analytics and alternative data, with release lags (the legacy generalised a Bloomberg example), backfilling and reinstatement, cost, crowding of analytics, and his opinions marked as opinions; Velu, Hardy and Nehren's fundamental and analyst inputs with their hedges restored, and their point that a dataset's value falls as access spreads.

Partly checked 2026-10-16, draft; human review outstanding. Artefacts: `notes/artefacts/statistical-learning-foundations/data-taxonomy.tex`.

## Related entries owned elsewhere

Cross-referenced, not owned here: `data:trading-reference-data`, `data:market-data-levels`, `data:derived-market-statistics` (`point-in-time-data`); `meth:activity-sampled-bars` (`statistical-learning-foundations`).

## Entry backlog

- ev:alternative-data-edge-decay: evidence on how an alternative dataset's predictive value falls as access spreads, and on short-horizon data crowding out long-horizon forecasting (`rf-katona-painter-patatoukas-zeng-2025`, `rf-dessaint-foucault-fresard-2024`, `rf-farboodi-veldkamp-2020`, unread).
- meth:alternative-dataset-assessment: coverage, history, release lag, vendor backfill and incremental information over consensus, as the checkpoint asks (`wide-kolanovic-big-data`, `rf-monk-prins-rook-2019`, unread).
- ev:holdings-insider-ratings-signals: whether 13F holdings changes, insider trades and rating downgrades predict returns, which Velu, Hardy and Nehren assert with hedges (no reading of this pathway covers it; source to identify).

## Legacy candidate material

Run `python3 tools/migration_status.py` for the current counts. After slice 32 no legacy file lists this pathway.

## What changed in my view or practice

## Questions carried forward

- López de Prado's "over 10TB" of FIX data a day has no source or market; is there a primary figure?
