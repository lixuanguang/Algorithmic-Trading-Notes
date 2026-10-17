---
key: otc-fixed-income-trading
section: execution-trading-costs
status: not started (draft entries from the migration only)
---

# Fixed-income and OTC electronic trading

Pathway outcome, from the guide: measure what clients pay in bond, swap and FX dealer markets, and explain how RFQ and portfolio trading, transparency rules and dealer capacity change those costs. Its checkpoint estimates round-trip costs from TRACE data by trade size and rating before and after a transparency or electronification change, compares RFQ, portfolio-trade and voice costs where identifiable, and documents data limitations. Its fourteen readings run from OTC search theory (`wide-dgp-otc`, `wide-duffie-dark-markets`) through the fixed-income survey (`wide-bsv-fi-survey`), transparency and electronic-trading evidence (`wide-edwards-harris-piwowar`, `wide-hendershott-madhavan`, `wide-ohara-zhou-electronic`), search frictions and dealer capacity, portfolio trading (`wide-li-ohara-portfolio-trading`), investor composition, FX algorithms (`exp-fx-algos`) and relationship trading, to the 2020 liquidity crisis and quote competition.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 15 October 2026 by migration fixed-income market structure review (`notes/source-review-index.md`), which migrated the legacy fixed-income-microstructure file mapped to this pathway alone. The entries come from migration and source checking: `wide-bsv-fi-survey` in its published JFQA version, read in part; the abstracts only of `wide-edwards-harris-piwowar`, `wide-hendershott-madhavan` and `wide-ohara-zhou-electronic`; FINRA Rules 6730 and 6750 and filing pages as displayed on 15 October 2026; ESMA's statement of 10 October 2025 and transparency manual of 12 May 2026. That is not study of the readings, and the checkpoint was not attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in migration fixed-income market structure / source review / optimal execution / high-frequency strategies reviews:

- `def:fixed-income-market-structure`: segments (Treasuries, structured products and TBAs, corporate and municipal bonds) kept apart from trading protocols (runs, voice, RFQ, BWIC/OWIC), venues (interdealer platforms, RFQ platforms, all-to-all) and dealer risk-bearing (principal trading, prearranged trades, reduced capital commitment, nonbank dealers); "dealer balance sheet as venue" treated as a metaphor; electronic RFQ evidence at abstract level.
- `rule:us-eu-bond-transparency`: TRACE reporting (Rule 6730, 15-minute outer limit, the one-minute proposal and its supersession) kept apart from dissemination (Rule 6750 and its exceptions, Treasuries), the 2002–2017 phase-in history, and EU post-trade deferrals for bonds from 2 March 2026 (ESMA examples); EU pre-trade and U.K. regimes not checked. The fixed-income market structure review follow-up (same day) separated the presently effective non-member-affiliate exclusion from the member-affiliate expansion (SR-FINRA-2026-009, effective 2 August 2027, whose wording the rulebook already displays).
- `ev:bond-transparency-trading-costs`: post-trade transparency associated with lower customer costs in U.S. corporate bonds and other segments, costs falling with trade size; the survey's limits (completed trades only, large orders, optimal transparency unresolved); pre-trade transparency as an open question; what data clients can measure with, including Rule 2232's mark-up disclosure for non-institutional customer principal trades with same-day offsetting trades (follow-up).

All three: verification partly checked 2026-10-15, stability draft; human review outstanding. Their artefact is `notes/artefacts/otc-fixed-income-trading/derivations.tex`.

## Source verification after macro markets and pricing review

method validation (2026-10-17) (audit repairs and a source-review coverage; source verification and bounded tests, not study or human review): Queue: `rule:eu-mifir-bond-transparency-level1` resolved by merge into `rule:us-eu-bond-transparency` (Regulation (EU) 2024/791, Art. 1(5)-(9); Delegated Regulation (EU) 2025/1246, OJ of 3 November 2025, Art. 8a deferral maxima, applying from 2 March 2026); `ev:credit-derivative-swap-trading-structure` narrowed (17 CFR 50.4 clearing classes, 37.9 and 37.10 SEF execution and MAT; trading shares unmeasured); `rule:uk-bond-transparency` blocked (FCA 403; legislation.gov.uk empty 202). The record is in `notes/source-review-records.md`, *method validation (2026-10-17)*.

empirical extensions (2026-10-17) (six audit repairs and a source-review coverage; source verification and bounded tests, not study or human review): `ev:credit-derivative-swap-trading-structure` narrowed (the CFTC's made-available-to-trade filings and TW SEF's 2023 submission merged). The record is in `notes/source-review-records.md`, *empirical extensions (2026-10-17)*.

derivatives and empirical validation (2026-10-17) (seven audit repairs, backlog reconciliation and a source-review coverage; source verification and bounded tests, not study or human review): the `rule:uk-bond-transparency` question: FCA PS24/14's four bond deferral groups merged into `rule:us-eu-bond-transparency` from an Internet Archive capture; `rule:uk-bond-transparency` narrowed to its thresholds and Handbook text. The record is in `notes/source-review-records.md`, *derivatives and empirical validation (2026-10-17)*.

## Related entries owned elsewhere

Cross-referenced, not owned here: `def:dealer-inventory-risk`, `meth:dealer-quote-adjustment` (`market-making-lob` and `execution-market-making`), `def:spread-measures` (`execution-market-making`), `def:best-execution` (`market-structure-execution-quality`), `meth:transaction-cost-analysis` and `def:portfolio-trading` (`execution-trading-costs`), `mech:etf-creation-redemption` (`etf-index-closing-execution`, with Pan and Zeng's corporate bond ETF evidence). The dealer-capacity theory of the guide's `bond-swap-dealer-market-making` pathway (no note yet) was not drawn on beyond the survey's account. None of these establishes fixed-income facts on its own.

## Entry backlog

- ev:credit-derivative-swap-trading-structure: measured shares of dealer-to-client RFQ against order-book trading in swaps, and the swap readings. The CFTC's clearing and SEF rules, its made-available-to-trade determinations and TW SEF's 2023 submission are merged.
- rule:uk-bond-transparency: the size thresholds of PS24/14's Table 8 by issuer, issue size and maturity, and the Handbook text (MAR 11); the four deferral groups and the December 2025 start are in `rule:us-eu-bond-transparency`.

## Legacy candidate material

Run `python3 tools/check_compendium.py` for the current counts. After fixed-income market structure review no legacy file lists this pathway as its single candidate.

## What changed in my view or practice

## Questions carried forward

- Read Edwards, Harris and Piwowar, Hendershott and Madhavan, and O'Hara and Zhou in full: only abstracts were read on 2026-10-15 (SSRN and a working-paper copy returned bot or 403 pages).
- Read the FINRA approval orders for SR-FINRA-2024-004 and SR-FINRA-2025-008, and the current TRACE dissemination caps.
- Does pre-trade transparency in illiquid bonds raise dealer risk or reduce liquidity in any measured sample? Not checked.
