---
key: money-markets-repo-lending
section: portfolio-risk-financing
status: not started (draft entries only, not from study)
---

# Money markets, repo and securities lending

Pathway outcome, from the guide: price short-term cash and collateral financing, distinguish repo from securities lending, and test funding-liquidity exposure with dated benchmark, fund and transaction evidence. Its thirteen readings run from commercial paper and CDs through the ICMA repo FAQ (`al-icma`), the New York Fed reference rates, repo-rate evidence, Duffie–Gârleanu–Pedersen on securities lending (`al-duffie`), the ISLA best-practice handbook (`al-isla`) and institutional lending mandates, to money-fund data, reforms and runs, funding liquidity, repo premia and special repo rates.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 15 October 2026 by securities lending and synthetic shorts review (`notes/source-review-index.md`). The entries come from source checking against Harris (`alpha-harris`, chap. 7), `al-duffie` in its September 2001 working paper, `al-icma` and `al-isla` as retrieved, Regulation SHO on eCFR (October 2026) and Hu–Black's working paper. That is not study of the readings, and no checkpoint was attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in securities lending and synthetic shorts / source review / optimal execution / high-frequency strategies reviews:

- `def:street-name-beneficial-ownership`: registration, beneficial ownership, custody and permission to lend kept apart; votes follow record holdings, lent shares carry votes to the borrower, brokers vote record shares in proportion to instructions (Harris); recall to vote; record-date capture through borrowing (Hu–Black), kept apart from swap-based decoupling and disclosure.
- `mech:securities-lending-short-sale`: locate, borrow, delivery, recall, replacement borrow and buy-in (DGP, 2001); Regulation SHO's locate (Rule 203(b)) and close-out (Rule 204(a)) as current U.S. law; ISLA's recall-to-buy-in practice; broker–customer arrangements against the institutional loan; availability against operational risks.
- `def:securities-lending-fee-rebate`: fee against non-cash collateral, rebate against cash collateral with the fee implicit; 102 percent collateral and rebate accrual (DGP); general collateral and specials; broker rebate spreads; retail short proceeds and customer margin kept apart from loan collateral.

All three: verification partly checked 2026-10-15, stability draft; human review outstanding.

Written in macro markets and pricing / source review / optimal execution / execution control reviews:

- `def:money-market-reference-rates`: money-market instruments as Gliner describes them; fed funds, SOFR and the EFFR; LIBOR's end (panel after 30 June 2023, synthetic settings to 30 September 2024); EONIA discontinued on 3 January 2022 and €STR published since 2 October 2019; the LIBOR--OIS spread as a historical stress gauge. Verification partly checked 2026-10-16, stability draft.

Written in derivatives and empirical validation (2026-10-17):

- `ev:money-fund-runs`: March 2020 prime-fund runs, institutional against retail (Cipriani and La Spada).

## Source verification after macro markets and pricing review

macro markets and pricing review follow-up, 2026-10-16 (source verification, not study): `data:post-libor-funding-stress-measures` narrowed; `data:treasury-bill-offering-schedule` resolved (TreasuryDirect: bills of 4 to 52 weeks; 4-, 6-, 8-, 13-, 17- and 26-week weekly, 52-week every four weeks, plus cash management bills). Entries corrected in the same follow-up are listed in `notes/source-review-records.md`, *macro markets and pricing review follow-up*.

Second macro markets and pricing review follow-up, 2026-10-16 (source verification, not study): `data:post-libor-funding-stress-measures` narrowed (OFR FSI: 3-month CP minus SOFR OIS replaces LIBOR-OIS, CP minus 3-month Treasury replaces TED, from 1 January 2022; funding contribution 9.58 on 10 October 2008, 0.96 on 30 March 2020, -0.16 on 13 October 2026). Entries corrected in the same follow-up are listed in `notes/source-review-records.md`, *macro markets and pricing review second follow-up*.

Source follow-up of order books and order flow / dealer models and information reviews and the macro markets and pricing review audit, 2026-10-16 (source verification, not study): `data:post-libor-funding-stress-measures` deferred (a dated CP minus SOFR OIS series needs SOFR OIS swap rates, which were not found in public data; no study replacing LIBOR-OIS was read in this batch). The record is in `notes/source-review-records.md`, *Source follow-up of order books and order flow / dealer models and information reviews and macro markets and pricing review audit corrections*.

source verification (2026-10-17) (source verification and bounded tests, not study or human review): `data:post-libor-funding-stress-measures` deferral retained: no public, dated SOFR OIS series was obtained, so the CP minus SOFR OIS spread still cannot be built. The record is in `notes/source-review-records.md`, *source verification (2026-10-17)*.

method validation (2026-10-17) (audit repairs and a source-review coverage; source verification and bounded tests, not study or human review): Queue: `rule:us-short-sale-margin-and-price-test` resolved by merge into `mech:securities-lending-short-sale` (12 CFR 220.12(c): 150 percent; FINRA Rule 4210(c)(2)-(3); Rule 201's 10 percent trigger and NBB restriction for the day and the next); `ev:securities-lending-fees-evidence` resolved by merge into `def:securities-lending-fee-rebate` (Sikorskaya, author version of 27 April 2026, Table 1: general collateral 0.39 percent, specials 5.61 percent mean near the Russell cutoff, 2006-2018). The record is in `notes/source-review-records.md`, *method validation (2026-10-17)*.

empirical extensions (2026-10-17) (six audit repairs and a source-review coverage; source verification and bounded tests, not study or human review): `data:post-libor-funding-stress-measures` deferred (trigger review: still no free official dated SOFR OIS series; retained). The record is in `notes/source-review-records.md`, *empirical extensions (2026-10-17)*.

derivatives and empirical validation (2026-10-17) (seven audit repairs, backlog reconciliation and a source-review coverage; source verification and bounded tests, not study or human review): the `def:money-market-reference-rates` and `ev:money-fund-runs` questions: new entry `ev:money-fund-runs` (Cipriani and La Spada); CP maturities (the BIS primer contradicts Gliner's 90-270 days), the SOFR calculation and revision rule, Schrimpf and Sushko and Copeland and Engbretson merged into `def:money-market-reference-rates`. The record is in `notes/source-review-records.md`, *derivatives and empirical validation (2026-10-17)*.

## Related entries owned elsewhere

Cross-referenced, not owned here: `res:synthetic-short-put-call` (`synthetic-equity-cfd-trs`); `def:broker-agency-conflicts` (`market-structure-execution-quality`); `res:arbitrage-risks` (`execution-market-making`); `mech:futures-margin-settlement` (`futures-execution`).

## Entry backlog

- data:post-libor-funding-stress-measures: a free, dated, official series for the 3-month commercial paper minus SOFR OIS spread (no free official SOFR OIS series, rechecked 2026-10-17), and which spreads research uses in LIBOR-OIS's place beyond the OFR's index. Deferred: revisit when an official term SOFR OIS series becomes freely available.

## What changed in my view or practice

## Questions carried forward

- Read the published DGP article (JFE 2002) and the ISLA handbook's current online version; the compilation read is dated 31 March 2025, with sections under review.
- Check Hu and Black's statement that Regulation T bars lending shares for voting purposes "in many circumstances".
- U.S. proxy-processing rules and other jurisdictions' short-sale rules were not checked.
