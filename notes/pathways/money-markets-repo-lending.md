---
key: money-markets-repo-lending
section: portfolio-risk-financing
status: not started (draft entries from the migration only)
---

# Money markets, repo and securities lending

Pathway outcome, from the guide: price short-term cash and collateral financing, distinguish repo from securities lending, and test funding-liquidity exposure with dated benchmark, fund and transaction evidence. Its thirteen readings run from commercial paper and CDs through the ICMA repo FAQ (`al-icma`), the New York Fed reference rates, repo-rate evidence, Duffie–Gârleanu–Pedersen on securities lending (`al-duffie`), the ISLA best-practice handbook (`al-isla`) and institutional lending mandates, to money-fund data, reforms and runs, funding liquidity, repo premia and special repo rates.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 15 October 2026 by migration slice 23 (`notes/migration.md`), which routed the lending blocks of the legacy securities-lending-and-synthetic-shorts file here, an exception to the file's map candidate `synthetic-equity-cfd-trs`: their subject is the lending market itself, which this pathway's outcome and readings cover. The entries come from migration and source checking against Harris (`alpha-harris`, chap. 7), `al-duffie` in its September 2001 working paper, `al-icma` and `al-isla` as retrieved, Regulation SHO on eCFR (October 2026) and Hu–Black's working paper. That is not study of the readings, and no checkpoint was attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in migration slice 23, 2026-10-15:

- `def:street-name-beneficial-ownership`: registration, beneficial ownership, custody and permission to lend kept apart; votes follow record holdings, lent shares carry votes to the borrower, brokers vote record shares in proportion to instructions (Harris); recall to vote; record-date capture through borrowing (Hu–Black), kept apart from swap-based decoupling and disclosure.
- `mech:securities-lending-short-sale`: locate, borrow, delivery, recall, replacement borrow and buy-in (DGP, 2001); Regulation SHO's locate (Rule 203(b)) and close-out (Rule 204(a)) as current U.S. law; ISLA's recall-to-buy-in practice; broker–customer arrangements against the institutional loan; availability against operational risks.
- `def:securities-lending-fee-rebate`: fee against non-cash collateral, rebate against cash collateral with the fee implicit; 102 percent collateral and rebate accrual (DGP); general collateral and specials; broker rebate spreads; retail short proceeds and customer margin kept apart from loan collateral.

All three: verification partly checked 2026-10-15, stability draft; human review outstanding. Their legacy wording is kept, with the rest of the file, in `notes/artefacts/synthetic-equity-cfd-trs/derivations.tex`.

Written in migration slice 37, 2026-10-16, from the legacy macro chapter:

- `def:money-market-reference-rates`: money-market instruments as Gliner describes them; fed funds, SOFR and the EFFR; LIBOR's end (panel after 30 June 2023, synthetic settings to 30 September 2024); EONIA discontinued on 3 January 2022 and €STR published since 2 October 2019; the LIBOR--OIS spread as a historical stress gauge. Verification partly checked 2026-10-16, stability draft.

## Source verification after slice 37

Slice-37 follow-up, 2026-10-16 (source verification, not study): `data:post-libor-funding-stress-measures` narrowed; `data:treasury-bill-offering-schedule` resolved (TreasuryDirect: bills of 4 to 52 weeks; 4-, 6-, 8-, 13-, 17- and 26-week weekly, 52-week every four weeks, plus cash management bills). Entries corrected in the same follow-up are listed in `notes/migration-slices.md`, *Slice 37 follow-up*.

Second slice-37 follow-up, 2026-10-16 (source verification, not study): `data:post-libor-funding-stress-measures` narrowed (OFR FSI: 3-month CP minus SOFR OIS replaces LIBOR-OIS, CP minus 3-month Treasury replaces TED, from 1 January 2022; funding contribution 9.58 on 10 October 2008, 0.96 on 30 March 2020, -0.16 on 13 October 2026). Entries corrected in the same follow-up are listed in `notes/migration-slices.md`, *Slice 37 second follow-up*.

Source follow-up of slices 33-36 and the slice-37 audit, 2026-10-16 (source verification, not study): `data:post-libor-funding-stress-measures` deferred (a dated CP minus SOFR OIS series needs SOFR OIS swap rates, which were not found in public data; no study replacing LIBOR-OIS was read in this batch). The record is in `notes/migration-slices.md`, *Source follow-up of slices 33-36 and slice-37 audit corrections*.

## Related entries owned elsewhere

Cross-referenced, not owned here: `res:synthetic-short-put-call` (`synthetic-equity-cfd-trs`); `def:broker-agency-conflicts` (`market-structure-execution-quality`); `res:arbitrage-risks` (`execution-market-making`); `mech:futures-margin-settlement` (`futures-execution`).

## Entry backlog

- rule:us-short-sale-margin-and-price-test: current Regulation T and FINRA margin for short sales, and the current U.S. short-sale price test; DGP's 2001 description is historical.
- ev:securities-lending-fees-evidence: measured lending fees, rebates and specials (for example from institutional lending data, `catalogue-0897`), against the legacy "low or negative rebates" claim.
- data:post-libor-funding-stress-measures: which spreads research studies, beyond the OFR's index, use in LIBOR-OIS's place, and a dated series of the 3-month commercial paper minus SOFR OIS spread itself; the OFR's June 2023 replacement of its funding variables, its daily index and the Fed's May 2026 Financial Stability Report were read on 2026-10-16

## Legacy candidate material

Run `python3 tools/migration_status.py` for the current counts. No legacy file names this pathway as its map candidate.

## What changed in my view or practice

## Questions carried forward

- Read the published DGP article (JFE 2002) and the ISLA handbook's current online version; the compilation read is dated 31 March 2025, with sections under review.
- Check Hu and Black's statement that Regulation T bars lending shares for voting purposes "in many circumstances".
- U.S. proxy-processing rules and other jurisdictions' short-sale rules were not checked.
