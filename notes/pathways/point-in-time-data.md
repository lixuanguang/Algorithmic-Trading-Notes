---
key: point-in-time-data
section: research-engineering-validation
status: not started (draft entries from the migration only)
---

# Point-in-time data, vendor files and bias control

Pathway outcome, from the guide: construct a research panel whose every field is available at decision time, with documented vintages, corrections and survivorship controls. Its checkpoint builds a monthly stock panel with delisting returns, point-in-time fundamentals with reporting lags and identifiers, documents each vendor vintage, and shows how a published anomaly changes with and without delisting and survivorship corrections. Its fourteen readings run from bitemporal history (`s8-bitemporal`) and vendor files (`exp-crsp-ciz`, `exp-trace`, `wide-dick-nielsen-trace`, `wide-holden-jacobsen`, `wide-sec-13f-nport`, `exp-gleif`) to bias evidence (`wide-shumway-delisting`, `wide-ljungqvist-rewriting`, `wide-elton-gruber-blake-survivorship`, `wide-aggarwal-jorion`, `w4-akey-noisy-ff-factors`, `w5-croushore-stark`) and missing data (`exp-missing-financial-data`).

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 16 October 2026 by migration slice 32 (`notes/migration-slices.md`), which routed the legacy taxonomy file's reference-data, market-data-feed, binned-data and intraday-activity blocks here, outside the file's map candidates (`statistical-learning-foundations`, `financial-ml-evaluation`, `alternative-data-sources`): their content is the reference and market data from which a decision-time panel is built. The legacy notes did not name their source; it is Velu, Hardy and Nehren (`s3-velu`, chap. 1, sec. 1.4), which is not a reading of this pathway. None of the pathway's readings has been opened, and the checkpoint was not attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in migration slice 32, 2026-10-16:

- `data:trading-reference-data`: universe, symbology with bitemporal as-of mapping, ticker changes, corporate actions, static data and quote factors, exchange data with rule histories, condition codes, special days, futures and options reference data, event calendars, related and composite instruments, latency tables; the legacy's dividend conflation corrected.
- `data:market-data-levels`: Level I, II and III data, matching-engine against reception time, the U.S. Level III record (prices divided by 10,000, not 1,000), special order types.
- `data:derived-market-statistics`: daily activity data, intraday microstructure statistics, pre-computed aggregates and binned data, with the reference-data caveat and the availability time of each field; the legacy's "Binned Data" heading corrected.

All partly checked 2026-10-16, draft; human review outstanding. Artefact: `notes/artefacts/statistical-learning-foundations/data-taxonomy.tex`.

Changed in migration slice 36, 2026-10-16 (a routing exception from the microstructure data-engineering file, whose candidates are `lob-deep-learning` and `market-simulation`; the blocks concern what a record means and when it was known): `data:market-data-levels` (timestamp quality and sequencing across markets and the public-awareness time, Hasbrouck p. 105; three times for a feature's availability; corrections arriving as later records; the legacy feed levels and message layers against Velu, Hardy and Nehren chap. 11) and `data:trading-reference-data` (the ticker caveat: identifiers with validity dates). Partly checked, draft.

## Related entries owned elsewhere

Cross-referenced, not owned here: `def:financial-data-types` (`alternative-data-sources`, including López de Prado's release lags, backfilling and reinstatement of fundamental data); `meth:etf-trick` (`statistical-learning-foundations`); `pit:label-weight-leakage` (`financial-ml-evaluation`); `pit:backtest-cost-short-assumptions` (`backtest-inference`).

## Entry backlog

- meth:bitemporal-reference-tables: valid time against transaction time for identifiers, corporate actions and vendor corrections (`s8-bitemporal`, unread).
- data:holdings-insider-filing-lags: Form 13F, 13D, 3 and 4 filing deadlines and their use in a decision-time panel (`wide-sec-13f-nport`; Velu, Hardy and Nehren give the 13F threshold and the 13D and Form 4 deadlines in footnotes, p. 43, unchecked against the rules).
- ev:delisting-survivorship-rewriting: delisting returns, survivorship and vendor history rewriting (`wide-shumway-delisting`, `wide-elton-gruber-blake-survivorship`, `wide-ljungqvist-rewriting`, unread).
- data:trade-correction-records: how consolidated U.S. trade data mark cancellations, corrections and late reports, and how a decision-time panel should apply them (`wide-holden-jacobsen` and the TAQ documentation, unread); slice 36 stated the principle only

## Legacy candidate material

Run `python3 tools/migration_status.py` for the current counts. No legacy file lists this pathway; its entries and changes came by routing (slices 32 and 36).

## What changed in my view or practice

## Questions carried forward

- Review the routing: should the market-data entries belong to `market-structure-execution-quality` or `lob-deep-learning` instead?
