---
key: synthetic-equity-cfd-trs
section: portfolio-risk-financing
status: not started (draft entry from the migration only)
---

# CFDs, total return swaps and synthetic equity financing

Pathway outcome, from the guide: price a CFD or equity total return swap from its financing, dividend, borrow and margin terms; compare it with futures, listed total return futures and cash financing; and identify the counterparty, disclosure and tax exposures it creates. Its fourteen readings run from Hull's swap chapters (`s7-hulloptions`) and CFD pricing, through borrow fees (`al-duffie`), financing benchmarks and basis evidence, listed total return futures, uncleared-margin rules, the Archegos reports and the Lehman prime-brokerage evidence, to empty voting and hidden ownership (`cfd-hu-black-2007`), the 2023 SEC beneficial-ownership rule and U.S. dividend-equivalent withholding.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 15 October 2026 by migration slice 23 (`notes/migration.md`), which migrated the legacy securities-lending-and-synthetic-shorts file mapped to this pathway alone. Only the synthetic-short block stayed here; the lending blocks were routed to `money-markets-repo-lending`. The entry comes from migration, Harris (2002), Hu–Black's working paper and an own derivation checked numerically; Hull was not available. That is not study of the readings, and the checkpoint was not attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in migration slice 23, 2026-10-15:

- `res:synthetic-short-put-call`: long put plus short call pays $K-S_T$, a short forward at $K$; $P-C=e^{-rT}(K-F)$ with dividends; with a short bond repaying $K$ the payoff is $-S_T$, equivalent to short stock when $q=0$ (Harris's p. 157 "long bond" wording recorded as a discrepancy, since a long bond gives $2K-S_T$); with $q=0$ the financed package ends with $S_0e^{rT}-S_T$ against $S_0e^{r_bT}-S_T$ for a short sale with rebate $r_b$; matching terms; American early exercise and assignment; no guaranteed access to scarce borrow. Corrected in the slice-23 follow-up (same day), with reproducible checks in `notes/artefacts/synthetic-equity-cfd-trs/synthetic_short_checks.py`.

Verification partly checked 2026-10-15, stability draft; human review outstanding. The numerical checks are `synthetic_short_checks.py` beside the artefact, which is `notes/artefacts/synthetic-equity-cfd-trs/derivations.tex`, which keeps the whole legacy file, including the blocks routed to `money-markets-repo-lending`.

## Related entries owned elsewhere

Cross-referenced, not owned here: `mech:securities-lending-short-sale`, `def:securities-lending-fee-rebate`, `def:street-name-beneficial-ownership` (`money-markets-repo-lending`); `res:option-market-maker-spreads`, `meth:option-spread-measurement` (`options-execution`); `def:arbitrage`, `res:arbitrage-risks` (`execution-market-making`).

## Entry backlog

- ev:empty-voting-equity-derivatives: decoupling of votes from economic ownership through equity swaps and options (Hu–Black), and beneficial-ownership disclosure of cash-settled derivatives under the 2023 SEC rule (`cfd-sec-13d-2023`); kept apart from securities-lending vote transfer.
- ev:option-implied-borrow-cost: whether and how scarce borrow is priced into put–call parity deviations; needs an empirical source.

## Legacy candidate material

Run `python3 tools/migration_status.py` for the current counts. After slice 23 no legacy file lists this pathway.

## What changed in my view or practice

## Questions carried forward

- Read Hull's put–call parity and swap chapters (`s7-hulloptions`, 11th Global edition); no copy was available on 2026-10-15.
- Check listed U.S. equity option exercise style, settlement and multiplier against OCC or exchange documents.
