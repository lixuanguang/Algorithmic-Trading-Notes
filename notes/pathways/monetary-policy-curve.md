---
key: monetary-policy-curve
section: rates-credit-mortgages
status: not started (draft entries from the migration only)
---

# Monetary policy, balance-sheet policy and the yield curve

Pathway outcome, from the guide: read the expected policy path from futures, measure policy surprises at high frequency, and separate rate-path, term-premium and balance-sheet channels in long yields. Its 15 required readings: `rt-kuttner-2001`, `rt-piazzesi-swanson-2008`, `wide-gss-policy`, `rt-hanson-stein-2015`, `rt-hanson-lucca-wright-2021`, `rt-swanson-2021`, `wide-vayanos-vila`, `rt-gagnon-lsap-2011`, `rt-kvj-qe-2011`, `rt-damico-king-2013`, `rt-wu-xia-2016`, `rt-du-forbes-luzzetti-2024`, `rt-fed-balance-sheet-2025`, `latest-ashtari-tafti-liquidity-policy-2025`, `rt-bauer-rudebusch-2020`. This note is for a pathway of the section `rates-credit-mortgages`.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 16 October 2026 by migration slice 37 (`notes/migration.md`), which routed here the central-bank, Taylor-rule, OIS and Eurodollar blocks of the legacy chapter; `02_transmission_maps.tex` named this pathway as a candidate, while the central-bank blocks were in `01_regimes.tex`. The entries come from migration and source checking against Gliner (`s7-gliner`, *Global Macro Trading*, Wiley 2014, read from a local PDF and cited by chapter, section and PDF page), Taylor (1993), and the Federal Reserve, ECB, Bank of England, Bank of Japan, SNB, ARRC, EMMI and CFTC (CBOT filing 23-214) texts as retrieved on 16 October 2026. That is not study of the readings: none of them has been read for this pathway, and no checkpoint was attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in migration slice 37, 2026-10-16:

- `def:central-bank-policy-framework`: mandates, tools, the money multiplier, aggregates, the ZLB, QE with Bauer's announcement-day yield changes, crisis facilities, hawks and doves.
- `mod:taylor-rule`: Taylor's 1993 equation (2 percent equilibrium real rate), the Taylor principle and Gliner's printing slip.
- `rule:major-central-banks-current`: FOMC, ECB Governing Council (27 members, decisions every six weeks), BoE MPC, BoJ Policy Board and SNB as of 16 October 2026; Gliner's 2011--2013 ECB, SNB and BoE record; TARGET2 described correctly.
- `meth:policy-path-ois-futures`: fed funds futures, OIS and meeting-dated probabilities (dilution when the period straddles the meeting), and Eurodollar futures as history: LIBOR's end and the 2023 conversion to SOFR.

All: verification partly checked 2026-10-16, stability draft; human review outstanding. The legacy wording is kept in `notes/artefacts/multi-asset-systematic-macro/`.

## Source verification after slice 37

Slice-37 follow-up, 2026-10-16 (source verification, not study): `data:eurodollar-sofr-conversion-date` narrowed; `rule:boe-minutes-publication-history` resolved (Bank of England minutes about a fortnight after each meeting until July 2015 (Warsh review; 9 and 22 July 2015), published with the Monetary Policy Summary from 6 August 2015); `ev:qe-announcement-effects` narrowed; `rule:central-bank-policy-history` narrowed; `data:fomc-communication-current` resolved (FOMC press conferences after every meeting in 2025 and 2026 so far, projections at four meetings (March, June, September, December), minutes about three weeks later). Entries corrected in the same follow-up are listed in `notes/migration-slices.md`, *Slice 37 follow-up*.

## Related entries owned elsewhere

Cross-referenced, not owned here: `def:money-market-reference-rates` (`money-markets-repo-lending`); `def:currency-regimes-intervention` (`em-currencies-intervention`); `meth:macro-event-queries` (`macro-announcements-policy`).

## Entry backlog

- data:eurodollar-sofr-conversion-date: the text of CME Clearing Advisories 23-082 and 23-121, which refused automated access with a terms-of-use message on 2026-10-16; search listings give the conversion as effective after the close of Friday 14 April 2023 (trade date 17 April), against the CBOT filing's "April 23, 2023".
- ev:qe-announcement-effects: Gagnon, Raskin, Remache and Sack (2011), whose IJCB PDF link returned an HTML page on 2026-10-16; Bauer's 2012 letter was read and matches Gliner's Table 11.4.
- rule:central-bank-policy-history: an ECB statement on whether OMT was ever activated (the 2022 TPI release only says it remains in the toolkit), TLTRO terms, the PBOC's band and reserve-requirement history, and the Bank of England's first published inflation forecast; the BoJ's March 2024 exit, the SNB's January 2015 decision and the APP's history were checked on 2026-10-16.

## Legacy candidate material

None: the legacy chapters were all migrated by slice 37.

## What changed in my view or practice

## Questions carried forward

- Measure policy surprises at high frequency (Kuttner) before reading OIS-implied probabilities.
