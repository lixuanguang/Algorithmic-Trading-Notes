---
key: international-equity-markets
section: international-equity-markets
status: not started (draft entries from the migration only)
---

# International and emerging equity markets

Pathway outcome, from the guide: measure equity-market integration and diversification gains across developed, emerging and frontier markets without relying on raw correlations, in local currency and in dollars, hedged and unhedged, after survivorship, reclassification and stale-price corrections. Its 5 required readings: `gr-karolyi-stulz-2003`, `gr-jorion-goetzmann-1999`, `gr-coeurdacier-rey-2013`, `gr-bekaert-harvey-2003`, `gr-carpenter-whitelaw-2017`. This note is for the section overview.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 16 October 2026 by migration macro markets and pricing review (`notes/source-review-index.md`), which routed here the equity-index, index-construction and equity-derivative blocks of the legacy chapter; not a candidate of any legacy file (routing exception). The entries come from migration and source checking against Gliner (`s7-gliner`, *Global Macro Trading*, Wiley 2014, read from a local PDF and cited by chapter, section and PDF page). That is not study of the readings: none of them has been read for this pathway, and no checkpoint was attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in migration macro markets and pricing / source review / optimal execution / execution control reviews:

- `def:equity-indices-derivatives`: Gliner's indices by region, weighting methods, ETFs and ADRs, as of 2013.

All: verification partly checked 2026-10-16, stability draft; human review outstanding. The legacy wording is kept in `notes/artefacts/multi-asset-systematic-macro/`.

## Source verification after macro markets and pricing review

macro markets and pricing review follow-up, 2026-10-16 (source verification, not study): `data:equity-index-lists-current` narrowed. Entries corrected in the same follow-up are listed in `notes/source-review-records.md`, *macro markets and pricing review follow-up*.

Second macro markets and pricing review follow-up, 2026-10-16 (source verification, not study): `data:equity-index-lists-current` narrowed (JPX market-structure page; Moscow Exchange index page). Entries corrected in the same follow-up are listed in `notes/source-review-records.md`, *macro markets and pricing review second follow-up*.

Source follow-up of order books and order flow / dealer models and information reviews and the macro markets and pricing review audit, 2026-10-16 (source verification, not study): `data:equity-index-lists-current` narrowed (Nikkei's Nikkei 225 profile and JPX's TOPIX page). The record is in `notes/source-review-records.md`, *Source follow-up of order books and order flow / dealer models and information reviews and macro markets and pricing review audit corrections*.

Second source follow-up, 2026-10-16 (source verification, not study or human review): `data:equity-index-lists-current` narrowed further (FTSE/JSE ground rules v9.3: Top 40 the 40 most investable All Share companies, headline indices on the SWIX free float from 18 March 2024; FT Wilshire 5000: comprehensive, float-adjusted U.S. market index). The record is in `notes/source-review-records.md`, *Second source follow-up of the order books and order flow / macro markets and pricing reviews queue*.

source verification (2026-10-17) (source verification and bounded tests, not study or human review): `data:equity-index-lists-current` narrowed: NSE's methodology of September 2026 (Nifty 50, float-adjusted capitalisation-weighted) and Borsa Istanbul's ground rules of April 2020 (free-float weighting, capped variants) were read into `def:equity-indices-derivatives`. Failed routes, not repeated blindly: IDX (HTTP 403 again), S&P DJI methodologies (403, also through the fetching tool), stoxx.com (TLS certificate not verifiable; not forced), Euronext (403), and the Hang Seng address tried (404). The record is in `notes/source-review-records.md`, *source verification (2026-10-17)*.

method validation (2026-10-17) (audit repairs and a source-review coverage; source verification and bounded tests, not study or human review): Queue: `data:equity-index-lists-current` narrowed further (Hang Seng Index methodology v2.3, July 2023). The record is in `notes/source-review-records.md`, *method validation (2026-10-17)*.

empirical extensions (2026-10-17) (six audit repairs and a source-review coverage; source verification and bounded tests, not study or human review): `data:equity-index-lists-current` narrowed (DJIA, Russell 2000, FTSE 100, EURO STOXX 50 and DAX rules read and merged into `def:equity-indices-derivatives`). The record is in `notes/source-review-records.md`, *empirical extensions (2026-10-17)*.

derivatives and empirical validation (2026-10-17) (seven audit repairs, backlog reconciliation and a source-review coverage; source verification and bounded tests, not study or human review): target 44: BME's IBEX committee notice of December 2024 (free-float bands, 20 percent cap) merged into `def:equity-indices-derivatives`. The record is in `notes/source-review-records.md`, *derivatives and empirical validation (2026-10-17)*.

## Related entries owned elsewhere

Cross-referenced, not owned here: `meth:equity-index-valuation` (`cross-asset-style-premia`); `def:vix-variance-dividend-swaps` (`vix-correlation-dividends`); `mech:etf-creation-redemption` (`etf-index-closing-execution`).

## Entry backlog

- data:equity-index-lists-current: current methodologies for the Jakarta Composite, the S&P 500 and the other S&P DJI indices apart from the DJIA, CAC 40 and AEX, KOSPI, ASX 200, NZX 50, Shanghai Composite, Bovespa, Mexico IPC, Nasdaq Composite and FTSE MIB, and BME's IBEX Technical Regulations themselves; fourteen indices' rules and an IBEX committee notice are in `def:equity-indices-derivatives`.

## Legacy candidate material

None: the legacy chapters were all migrated by macro markets and pricing review.

## What changed in my view or practice

## Questions carried forward
