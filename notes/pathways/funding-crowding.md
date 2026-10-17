---
key: funding-crowding
section: portfolio-risk-financing
status: not started (draft entries from the migration only)
---

# Funding, leverage and crowding

Pathway outcome, from the guide: trace how margin, leverage, funding runs and crowded positions turn small shocks into forced liquidations. Its checkpoint picks one deleveraging episode (2007, 2008, 2020 or 2024), documents the funding trigger, margin changes, crowded positions and price impact, and estimates how much an overlap-based crowding measure would have warned in advance. Its twelve readings run from liquidity spirals, limits of arbitrage and margin-based pricing (`exp-brunnermeier-pedersen-liquidity`, `wide-shleifer-vishny-limits`, `wide-garleanu-pedersen-margin`), through leverage, repo runs and intermediary capital (`wide-adrian-shin-leverage`, `wide-gorton-metrick-repo`, `wide-he-kelly-manela`), to episodes: the 2007 quant meltdown (`exp-khandani-lo-quant-meltdown`), merger-arbitrage crashes, crowded exits (`wide-pedersen-exit`), Archegos, the August 2024 carry unwind and segmented arbitrage.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 15 October 2026 by migration model risk and contagion review (`notes/source-review-records.md`). the topic review routed the *Contagion Risk* block of the legacy risk-assessment file (`sysinv/modelrisk.tex`, Narang's systematic-investing notes) here, against the file's map candidate `model-governance-controls`. That pathway's outcome is model inventories, validation and pre-trade controls; the block concerns crowded positions, cross-collateralisation, volatility targeting and forced exits, which is this pathway's outcome. The entry comes from source checking against `s7-narang` (third edition, 2024), which is not a reading of this pathway. None of the pathway's readings has been read, and the checkpoint was not attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in migration model risk and contagion / source review / optimal execution / high-frequency strategies reviews:

- `def:common-investor-contagion`: Narang's contagion or common-investor risk, split into crowding (common positions) and the ATM effect (common funding: losses elsewhere force the sale of a liquid strategy). It gives his four drivers of August 2007 (crowding, weak prior returns, cross-collateralisation, volatility targeting) as a practitioner's explanation without data, and his August 1998 LTCM example. The Pulte Homes illustration does not support his "about half" and "about 20 times". Changed in the model risk and contagion review follow-up, 2026-10-15: the entry no longer says the illustration contradicts square-root metaorder impact. Aggregate crisis-period returns and volume do not identify a metaorder impact exponent, so the table bears neither for his "quadratic" nor against the square-root law; his account remains distinct from causal evidence.

Verification partly checked 2026-10-15, stability draft; human review outstanding. Its artefact is `notes/artefacts/model-governance-controls/risk-assessment.tex` (under the map candidate, keeping the file whole).

- `mod:margin-liquidity-spiral`: Brunnermeier and Pedersen's funding constraint and liquidity spirals. Partly checked 2026-10-17, draft.

## Source verification after macro markets and pricing review

source verification (2026-10-17) (source verification and bounded tests, not study or human review): `mod:margin-liquidity-spiral` resolved as a new entry in `portfolio-risk-financing/crowding-contagion.tex` from Brunnermeier and Pedersen's RFS Advance Access version (10 December 2008, princeton.edu): the margin constraint, VaR margins, destabilising margins, and the margin and loss spirals of Proposition 5 (eq. (24)); an illustration of the spiral expansion and its super-additivity in `notes/artefacts/funding-crowding/spiral-checks.py`. The issue pagination and Appendix A were not compared. The record is in `notes/source-review-records.md`, *source verification (2026-10-17)*.

method validation (2026-10-17) (audit repairs and a source-review coverage; source verification and bounded tests, not study or human review): Queue: `ev:august-2007-quant-unwind` resolved by merge into `def:common-investor-contagion` (Khandani and Lo, NBER WP 14465: July-December unwinding, the 1 and 6 August unwinds, market-making losses in the week of 6 August, reversal on 10 August); `mod:volatility-targeting-deleveraging` narrowed (Moreira and Muir's volatility-managed portfolios and Pedersen's risk-management spiral merged; Narang's 1.5-2 times estimate unverified); `meth:overlap-crowding-measure` narrowed (Pedersen gives overlap as mechanism, no measure; Chincarini et al. not obtained). The record is in `notes/source-review-records.md`, *method validation (2026-10-17)*.

empirical extensions (2026-10-17) (six audit repairs and a source-review coverage; source verification and bounded tests, not study or human review): `mod:volatility-targeting-deleveraging` narrowed (the ECB's May 2020 box on volatility-targeting strategies merged into `def:common-investor-contagion`); `meth:overlap-crowding-measure` narrowed (Chincarini, Lazo-Paz and Moneta's abstract (open access, but the publisher refused automated retrieval) merged into `def:common-investor-contagion`; their holdings measure unread). The record is in `notes/source-review-records.md`, *empirical extensions (2026-10-17)*.

derivatives and empirical validation (2026-10-17) (seven audit repairs, backlog reconciliation and a source-review coverage; source verification and bounded tests, not study or human review): the `mod:volatility-targeting-deleveraging` and `meth:residual-reversion-strategy` questions: Moreira and Muir's leverage distribution (new entry `ev:volatility-managed-portfolios`, owned by `risk-parity-vol-targeting`) narrows `mod:volatility-targeting-deleveraging`; Khandani and Lo's market-making path of August 2007 merged into `def:common-investor-contagion`. The record is in `notes/source-review-records.md`, *derivatives and empirical validation (2026-10-17)*.

## Related entries owned elsewhere

Cross-referenced, not owned here and not changed: `res:arbitrage-risks` (`execution-market-making`; staying power under leverage, LTCM); `def:quant-strategy-risk-sources` (`model-governance-controls`); `ev:square-root-impact` (`price-impact-execution`); `mech:futures-margin-settlement` (`futures-execution`); `def:securities-lending-fee-rebate` (`money-markets-repo-lending`). Kept distinct: the `backtest-inference` stub `ev:signal-decay-crowding`, which asks whether delayed-signal decay identifies crowding, a question that common positions and forced liquidation do not answer.

## Entry backlog

- mod:volatility-targeting-deleveraging: measured volatility-targeted assets and how much of them deleveraged together, and a source for Narang's 1.5-2 times leverage estimate; one strategy's leverage distribution (Moreira and Muir) and the real-time evidence (Cederburg et al.) are in `ev:volatility-managed-portfolios`.
- meth:overlap-crowding-measure: a holdings-overlap measure itself: Chincarini, Lazo-Paz and Moneta's (`w4-chincarini-crowded-anomalies`; abstract read, full text refused) or one built from 13F filings with the data-set structure in `wide-sec-13f-nport`.

## Legacy candidate material

Run `python3 tools/check_compendium.py` for the current counts. No legacy file lists this pathway; its model risk and contagion review material came from a file mapped to `model-governance-controls`.

## What changed in my view or practice

## Questions carried forward

- Do Khandani and Lo's data support Narang's sequence (multi-strategy deleveraging first, then statistical arbitrage), and his claim that the losses were "solely the result of market impact"?
