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

- `data:holdings-insider-filing-lags`: Form 13F, Schedules 13D and 13G, Forms 3 and 4 deadlines in force on 15 October 2026, their 2024 change and what they imply for decision-time panels. Partly checked 2026-10-17, draft.

Second batch of 2026-10-17:

- `meth:bitemporal-reference-tables`: actual (valid) against record (transaction) time for identifiers, corporate actions and vendor corrections, from Fowler, with an own synthetic split-correction check. Partly checked 2026-10-17, draft.

## Source verification after slice 37

Second slice-37 follow-up, 2026-10-16, working source gaps of slice 36 (source verification, not study): `data:trade-correction-records` narrowed (Daily TAQ v4.0: 01 records carry corrected data at the original time, 12 records the correction time and the original data; decision-time handling stated in the entry). Entries corrected in the same follow-up are listed in `notes/migration-slices.md`, *Slice 37 second follow-up*.

Source follow-up of slices 33-36 and the slice-37 audit, 2026-10-16 (source verification, not study): `data:trade-correction-records` blocked (Holden and Jacobsen: journal behind a subscription, SSRN HTTP 403, SMU record without a file, Holden's former Indiana page 401/404; Daily TAQ v4.0 field 8 rechecked: it does not state which time the 10 and 11 records carry). The record is in `notes/migration-slices.md`, *Source follow-up of slices 33-36 and slice-37 audit corrections*.

Second source follow-up, 2026-10-16 (source verification, not study or human review): `data:trade-correction-records` narrowed from blocked (Holden and Jacobsen, JF 2014, published version: sample, quote screens, n. 12 on the blank Quote Cancel/Correction field, Interpolated Time eq. (16) and its look-ahead, n. 29). The record is in `notes/migration-slices.md`, *Second source follow-up of the slice 33-37 queue*.

Batch of 2026-10-17 (source verification and bounded tests, not study or human review): `data:holdings-insider-filing-lags` resolved as a new entry in `research-engineering-validation/point-in-time-data.tex`: 17 CFR 240.13f-1, 13d-1, 13d-2, 16a-3 and 0-3 (eCFR, 15 October 2026), 15 U.S.C. 78p(a)(2) and the 2023 beneficial-ownership release (88 FR 76896), against Velu, Hardy and Nehren's pre-2024 footnotes; deadline arithmetic in `notes/artefacts/point-in-time-data/batch40-filing-checks.py`. `data:trade-correction-records` narrowed: Holden and Jacobsen's Internet Appendix (author-hosted) prints their July 2013 MTAQ program, which keeps only trades with correction code 00 and a positive price; their DTAQ code link returned 404 and the TAQ 10/11 record time is still unstated. The record is in `notes/migration-slices.md`, *Batch of 17 October 2026*.

Second batch of 2026-10-17 (audit repairs and a 50-item queue; source verification and bounded tests, not study or human review): Audit repair: `data:holdings-insider-filing-lags` now keeps EDGAR acceptance, the official filing date (17 CFR 232.13: 5:30 p.m., 10 p.m. for Forms 3-5, 144, 13D, 13G), public dissemination and first-observed time apart, assumes no fixed post-acceptance delay, and keeps separate timestamps for amendments and later-released confidential information (15 U.S.C. 78m(f)(4); Rule 24b-2) (`batch50-filing-timestamp-checks.py`). Queue: `meth:bitemporal-reference-tables` resolved as a new entry (Fowler, 2021; own synthetic check); `ev:delisting-survivorship-rewriting` narrowed (Shumway's abstract from the BYU record; full text 403); `data:trade-correction-records` narrowed further (NYSE Daily TAQ spec v4.0: correction codes 00-12 and what records 01 and 12 carry). The record is in `notes/migration-slices.md`, *Second batch of 17 October 2026*.

Third batch of 2026-10-17 (six audit repairs and a 60-item queue; source verification and bounded tests, not study or human review): `data:trade-correction-records` narrowed (three earlier Daily TAQ specifications define the correction records alike and give no time for them; Holden and Jacobsen's code archive returns 404); `ev:delisting-survivorship-rewriting` narrowed (Shumway and Warther's abstract (a $-55$ percent substitute delisting return; no Nasdaq size effect after correction) merged into `data:trading-reference-data`; Shumway's full text still refused). The record is in `notes/migration-slices.md`, *Third batch of 17 October 2026*.

Fourth batch of 2026-10-17 (seven audit repairs, backlog reconciliation and a 70-target batch; source verification and bounded tests, not study or human review): backlog reconciliation only: the backlog lines below were rewritten to state the remaining gap alone, removing stacked dated status prefixes and claims that material was unread or not obtained where earlier batches had read it. The record is in `notes/migration-slices.md`, *Fourth batch of 17 October 2026*.

## Related entries owned elsewhere

Cross-referenced, not owned here: `def:financial-data-types` (`alternative-data-sources`, including López de Prado's release lags, backfilling and reinstatement of fundamental data); `meth:etf-trick` (`statistical-learning-foundations`); `pit:label-weight-leakage` (`financial-ml-evaluation`); `pit:backtest-cost-short-assumptions` (`backtest-inference`).

## Entry backlog

- ev:delisting-survivorship-rewriting: Shumway's full text (BYU repository HTTP 403), Elton, Gruber and Blake, and Ljungqvist, Malloy and Marston (no open copy; the CEPR version is restricted). Shumway's and Shumway and Warther's abstracts are in `data:trading-reference-data`.
- data:trade-correction-records: the time carried by correction records 10 and 11, which none of the four Daily TAQ specifications read states, and Holden and Jacobsen's DTAQ code (link 404).

## Legacy candidate material

Run `python3 tools/migration_status.py` for the current counts. No legacy file lists this pathway; its entries and changes came by routing (slices 32 and 36).

## What changed in my view or practice

## Questions carried forward

- Review the routing: should the market-data entries belong to `market-structure-execution-quality` or `lob-deep-learning` instead?
