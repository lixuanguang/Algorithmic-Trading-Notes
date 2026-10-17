---
key: monetary-policy-curve
section: rates-credit-mortgages
status: not started (draft entries from the migration only)
---

# Monetary policy, balance-sheet policy and the yield curve

Pathway outcome, from the guide: read the expected policy path from futures, measure policy surprises at high frequency, and separate rate-path, term-premium and balance-sheet channels in long yields. Its 15 required readings: `rt-kuttner-2001`, `rt-piazzesi-swanson-2008`, `wide-gss-policy`, `rt-hanson-stein-2015`, `rt-hanson-lucca-wright-2021`, `rt-swanson-2021`, `wide-vayanos-vila`, `rt-gagnon-lsap-2011`, `rt-kvj-qe-2011`, `rt-damico-king-2013`, `rt-wu-xia-2016`, `rt-du-forbes-luzzetti-2024`, `rt-fed-balance-sheet-2025`, `latest-ashtari-tafti-liquidity-policy-2025`, `rt-bauer-rudebusch-2020`. This note is for a pathway of the section `rates-credit-mortgages`.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 16 October 2026 by migration macro markets and pricing review (`notes/source-review-index.md`), which routed here the central-bank, Taylor-rule, OIS and Eurodollar blocks of the legacy chapter; `02_transmission_maps.tex` named this pathway as a candidate, while the central-bank blocks were in `01_regimes.tex`. The entries come from migration and source checking against Gliner (`s7-gliner`, *Global Macro Trading*, Wiley 2014, read from a local PDF and cited by chapter, section and PDF page), Taylor (1993), and the Federal Reserve, ECB, Bank of England, Bank of Japan, SNB, ARRC, EMMI and CFTC (CBOT filing 23-214) texts as retrieved on 16 October 2026. That is not study of the readings: none of them has been read for this pathway, and no checkpoint was attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in migration macro markets and pricing / source review / optimal execution / execution control reviews:

- `def:central-bank-policy-framework`: mandates, tools, the money multiplier, aggregates, the ZLB, QE with Bauer's announcement-day yield changes, crisis facilities, hawks and doves.
- `mod:taylor-rule`: Taylor's 1993 equation (2 percent equilibrium real rate), the Taylor principle and Gliner's printing slip.
- `rule:major-central-banks-current`: FOMC, ECB Governing Council (27 members, decisions every six weeks), BoE MPC, BoJ Policy Board and SNB as of 16 October 2026; Gliner's 2011--2013 ECB, SNB and BoE record; TARGET2 described correctly.
- `meth:policy-path-ois-futures`: fed funds futures, OIS and meeting-dated probabilities (dilution when the period straddles the meeting), and Eurodollar futures as history: LIBOR's end and the 2023 conversion to SOFR.

All: verification partly checked 2026-10-16, stability draft; human review outstanding. The legacy wording is kept in `notes/artefacts/multi-asset-systematic-macro/`.

## Source verification after macro markets and pricing review

macro markets and pricing review follow-up, 2026-10-16 (source verification, not study): `data:eurodollar-sofr-conversion-date` narrowed; `rule:boe-minutes-publication-history` resolved (Bank of England minutes about a fortnight after each meeting until July 2015 (Warsh review; 9 and 22 July 2015), published with the Monetary Policy Summary from 6 August 2015); `ev:qe-announcement-effects` narrowed; `rule:central-bank-policy-history` narrowed; `data:fomc-communication-current` resolved (FOMC press conferences after every meeting in 2025 and 2026 so far, projections at four meetings (March, June, September, December), minutes about three weeks later). Entries corrected in the same follow-up are listed in `notes/source-review-records.md`, *macro markets and pricing review follow-up*.

Second macro markets and pricing review follow-up, 2026-10-16 (source verification, not study): `data:eurodollar-sofr-conversion-date` resolved (CME Clearing Advisory 23-082 of 15 March 2023, from a user-supplied browser export: conversion at 1:1 after the close of Friday 14 April 2023 for trade date 17 April, Eurodollar futures and options from September 2023 and the E0, E2-E5 mid-curves; ARRC minutes of 9 March 2023 and the CFTC chairman's keynote agree; CME Submission 24-271 shows the CBOT filing's "April 23" to be the date of CME's press release on the 7.5 million converted contracts); `ev:qe-announcement-effects` resolved (NY Fed Staff Report 441, March 2010, the working-paper version: eight events, 10-year Treasury -91 bp, agency -156, MBS -113; yields up nearly 100 bp on other days; term premium down 50-100 bp in the time-series estimate, 30-100 bp overall; the IJCB version itself not obtained); `rule:central-bank-policy-history` narrowed (ECB TLTRO page: series of 5 June 2014, 10 March 2016 and 7 March 2019; PBOC Announcement [2014] No. 5: band 1 to 2 percent from 17 March 2014). Entries corrected in the same follow-up are listed in `notes/source-review-records.md`, *macro markets and pricing review second follow-up*.

Source follow-up of order books and order flow / dealer models and information reviews and the macro markets and pricing review audit, 2026-10-16 (source verification, not study): `rule:central-bank-policy-history` narrowed (Gauweiler judgment para. 84 and Press Release 70/15 via CELLAR and curia; PBC central-parity statement as reproduced by NAFMII; Bank of England Quarterly Bulletin, February 1998, pp. 30-31). The record is in `notes/source-review-records.md`, *Source follow-up of order books and order flow / dealer models and information reviews and macro markets and pricing review audit corrections*.

Correction of 2026-10-16 to the second follow-up paragraph above: CME's press release on the conversion is dated 24 April 2023 (read in a dated reprint; CME's page refused automated access), so the CBOT filing's "April 23" is not the press release's date; the filings do not explain that date. The conversion trade date, 17 April 2023, stands.

Second source follow-up, 2026-10-16 (source verification, not study or human review): `rule:central-bank-policy-history` unchanged (no new source in this batch; the gap recorded on 16 October 2026 stands). The record is in `notes/source-review-records.md`, *Second source follow-up of the order books and order flow / macro markets and pricing reviews queue*.

source verification (2026-10-17) (source verification and bounded tests, not study or human review): `rule:central-bank-policy-history` reviewed, unchanged: no new primary source. A BIS-hosted 2018 speech by an RBNZ assistant governor dates the Reserve Bank of New Zealand Act to February 1990 but not its first published inflation forecast; secondary sources say the RBNZ's early Monetary Policy Statements are not on its website; PBOC pages on the current band and reserve-requirement history were not found. The record is in `notes/source-review-records.md`, *source verification (2026-10-17)*.

method validation (2026-10-17) (audit repairs and a source-review coverage; source verification and bounded tests, not study or human review): Queue: `rule:central-bank-policy-history` narrowed (PBOC English regime and required-reserves pages; RRR cuts of 27 September 2024 and 15 May 2025). The record is in `notes/source-review-records.md`, *method validation (2026-10-17)*.

empirical extensions (2026-10-17) (six audit repairs and a source-review coverage; source verification and bounded tests, not study or human review): `rule:central-bank-policy-history` unchanged (only a route was found (RBNZ's pre-1997 statements reposted on a former official's blog); the PBOC band and the full reserve-requirement history were not obtained). The record is in `notes/source-review-records.md`, *empirical extensions (2026-10-17)*.

derivatives and empirical validation (2026-10-17) (seven audit repairs, backlog reconciliation and a source-review coverage; source verification and bounded tests, not study or human review): backlog reconciliation only: the backlog lines below were rewritten to state the remaining gap alone, removing stacked dated status prefixes and claims that material was unread or not obtained where earlier batches had read it. The record is in `notes/source-review-records.md`, *derivatives and empirical validation (2026-10-17)*.

## Related entries owned elsewhere

Cross-referenced, not owned here: `def:money-market-reference-rates` (`money-markets-repo-lending`); `def:currency-regimes-intervention` (`em-currencies-intervention`); `meth:macro-event-queries` (`macro-announcements-policy`).

## Entry backlog

- rule:central-bank-policy-history: whether the PBOC's 2 percent band of March 2014 has changed since (its English regime page states a managed float without a band), the reserve-requirement history before 2021 (the English pages list cuts from 2021; the 2024 and 2025 cuts were read), and dated evidence for 'first major central bank to publish inflation forecasts' (RBNZ pages HTTP 403; only a repost of RBNZ's pre-1997 statements on a former official's blog was found).

## Legacy candidate material

None: the legacy chapters were all migrated by macro markets and pricing review.

## What changed in my view or practice

## Questions carried forward

- Measure policy surprises at high frequency (Kuttner) before reading OIS-implied probabilities.
