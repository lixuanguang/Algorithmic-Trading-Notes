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

## Related entries owned elsewhere

Cross-referenced, not owned here: `res:synthetic-short-put-call` (`synthetic-equity-cfd-trs`); `def:broker-agency-conflicts` (`market-structure-execution-quality`); `res:arbitrage-risks` (`execution-market-making`); `mech:futures-margin-settlement` (`futures-execution`).

## Entry backlog

- rule:us-short-sale-margin-and-price-test: current Regulation T and FINRA margin for short sales, and the current U.S. short-sale price test; DGP's 2001 description is historical.
- ev:securities-lending-fees-evidence: measured lending fees, rebates and specials (for example from institutional lending data, `catalogue-0897`), against the legacy "low or negative rebates" claim.

## Legacy candidate material

Run `python3 tools/migration_status.py` for the current counts. No legacy file names this pathway as its map candidate.

## What changed in my view or practice

## Questions carried forward

- Read the published DGP article (JFE 2002) and the ISLA handbook's current online version; the compilation read is dated 31 March 2025, with sections under review.
- Check Hu and Black's statement that Regulation T bars lending shares for voting purposes "in many circumstances".
- U.S. proxy-processing rules and other jurisdictions' short-sale rules were not checked.
