---
key: otc-fixed-income-trading
section: execution-trading-costs
status: not started (draft entries from the migration only)
---

# Fixed-income and OTC electronic trading

Pathway outcome, from the guide: measure what clients pay in bond, swap and FX dealer markets, and explain how RFQ and portfolio trading, transparency rules and dealer capacity change those costs. Its checkpoint estimates round-trip costs from TRACE data by trade size and rating before and after a transparency or electronification change, compares RFQ, portfolio-trade and voice costs where identifiable, and documents data limitations. Its fourteen readings run from OTC search theory (`wide-dgp-otc`, `wide-duffie-dark-markets`) through the fixed-income survey (`wide-bsv-fi-survey`), transparency and electronic-trading evidence (`wide-edwards-harris-piwowar`, `wide-hendershott-madhavan`, `wide-ohara-zhou-electronic`), search frictions and dealer capacity, portfolio trading (`wide-li-ohara-portfolio-trading`), investor composition, FX algorithms (`exp-fx-algos`) and relationship trading, to the 2020 liquidity crisis and quote competition.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 15 October 2026 by migration slice 22 (`notes/migration.md`), which migrated the legacy fixed-income-microstructure file mapped to this pathway alone. The entries come from migration and source checking: `wide-bsv-fi-survey` in its published JFQA version, read in part; the abstracts only of `wide-edwards-harris-piwowar`, `wide-hendershott-madhavan` and `wide-ohara-zhou-electronic`; FINRA Rules 6730 and 6750 and filing pages as displayed on 15 October 2026; ESMA's statement of 10 October 2025 and transparency manual of 12 May 2026. That is not study of the readings, and the checkpoint was not attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in migration slice 22, 2026-10-15:

- `def:fixed-income-market-structure`: segments (Treasuries, structured products and TBAs, corporate and municipal bonds) kept apart from trading protocols (runs, voice, RFQ, BWIC/OWIC), venues (interdealer platforms, RFQ platforms, all-to-all) and dealer risk-bearing (principal trading, prearranged trades, reduced capital commitment, nonbank dealers); "dealer balance sheet as venue" treated as a metaphor; electronic RFQ evidence at abstract level.
- `rule:us-eu-bond-transparency`: TRACE reporting (Rule 6730, 15-minute outer limit, the one-minute proposal and its supersession) kept apart from dissemination (Rule 6750 and its exceptions, Treasuries), the 2002–2017 phase-in history, and EU post-trade deferrals for bonds from 2 March 2026 (ESMA examples); EU pre-trade and U.K. regimes not checked.
- `ev:bond-transparency-trading-costs`: post-trade transparency associated with lower customer costs in U.S. corporate bonds and other segments, costs falling with trade size; the survey's limits (completed trades only, large orders, optimal transparency unresolved); pre-trade transparency as an open question; what data clients can measure with.

All three: verification partly checked 2026-10-15, stability draft; human review outstanding. Their artefact is `notes/artefacts/otc-fixed-income-trading/derivations.tex`.

## Related entries owned elsewhere

Cross-referenced, not owned here: `def:dealer-inventory-risk`, `meth:dealer-quote-adjustment` (`market-making-lob` and `execution-market-making`), `def:spread-measures` (`execution-market-making`), `def:best-execution` (`market-structure-execution-quality`), `meth:transaction-cost-analysis` and `def:portfolio-trading` (`execution-trading-costs`), `mech:etf-creation-redemption` (`etf-index-closing-execution`, with Pan and Zeng's corporate bond ETF evidence). The dealer-capacity theory of the guide's `bond-swap-dealer-market-making` pathway (no note yet) was not drawn on beyond the survey's account. None of these establishes fixed-income facts on its own.

## Entry backlog

- ev:credit-derivative-swap-trading-structure: how index and single-name CDS and interest rate swaps trade (central clearing, swap execution facilities, dealer mediation, RFQ on SEFs), against the legacy claims that indices trade "more centrally than bespoke risk" and swaps "remain dealer-mediated because contracts differ"; needs dated CFTC and SEF sources and the swap readings.
- rule:eu-mifir-bond-transparency-level1: the amended MiFIR text (Regulation (EU) 2024/791) on bond pre-trade transparency and deferral categories, and the Official Journal publication of the amending RTS 2; EUR-Lex returned an empty page on 2026-10-15.
- rule:uk-bond-transparency: the U.K. bond transparency regime, kept separate from the EU's; not checked.

## Legacy candidate material

Run `python3 tools/migration_status.py` for the current counts. After slice 22 no legacy file lists this pathway as its single candidate.

## What changed in my view or practice

## Questions carried forward

- Read Edwards, Harris and Piwowar, Hendershott and Madhavan, and O'Hara and Zhou in full: only abstracts were read on 2026-10-15 (SSRN and a working-paper copy returned bot or 403 pages).
- Read the FINRA approval orders for SR-FINRA-2024-004 and SR-FINRA-2025-008, and the current TRACE dissemination caps.
- Does pre-trade transparency in illiquid bonds raise dealer risk or reduce liquidity in any measured sample? Not checked.
