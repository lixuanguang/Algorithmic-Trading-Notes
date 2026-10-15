---
key: funding-crowding
section: portfolio-risk-financing
status: not started (draft entries from the migration only)
---

# Funding, leverage and crowding

Pathway outcome, from the guide: trace how margin, leverage, funding runs and crowded positions turn small shocks into forced liquidations. Its checkpoint picks one deleveraging episode (2007, 2008, 2020 or 2024), documents the funding trigger, margin changes, crowded positions and price impact, and estimates how much an overlap-based crowding measure would have warned in advance. Its twelve readings run from liquidity spirals, limits of arbitrage and margin-based pricing (`exp-brunnermeier-pedersen-liquidity`, `wide-shleifer-vishny-limits`, `wide-garleanu-pedersen-margin`), through leverage, repo runs and intermediary capital (`wide-adrian-shin-leverage`, `wide-gorton-metrick-repo`, `wide-he-kelly-manela`), to episodes: the 2007 quant meltdown (`exp-khandani-lo-quant-meltdown`), merger-arbitrage crashes, crowded exits (`wide-pedersen-exit`), Archegos, the August 2024 carry unwind and segmented arbitrage.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 15 October 2026 by migration slice 26 (`notes/migration-slices.md`). That slice routed the *Contagion Risk* block of the legacy risk-assessment file (`sysinv/modelrisk.tex`, Narang's systematic-investing notes) here, against the file's map candidate `model-governance-controls`. That pathway's outcome is model inventories, validation and pre-trade controls; the block concerns crowded positions, cross-collateralisation, volatility targeting and forced exits, which is this pathway's outcome. The entry comes from source checking against `s7-narang` (third edition, 2024), which is not a reading of this pathway. None of the pathway's readings has been read, and the checkpoint was not attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in migration slice 26, 2026-10-15:

- `def:common-investor-contagion`: Narang's contagion or common-investor risk, split into crowding (common positions) and the ATM effect (common funding: losses elsewhere force the sale of a liquid strategy). It gives his four drivers of August 2007 (crowding, weak prior returns, cross-collateralisation, volatility targeting) as a practitioner's explanation without data, and his August 1998 LTCM example. The Pulte Homes illustration does not support his "about half" and "about 20 times", and his "quadratic" impact does not match the square-root law.

Verification partly checked 2026-10-15, stability draft; human review outstanding. Its artefact is `notes/artefacts/model-governance-controls/risk-assessment.tex` (under the map candidate, keeping the file whole).

## Related entries owned elsewhere

Cross-referenced, not owned here and not changed: `res:arbitrage-risks` (`execution-market-making`; staying power under leverage, LTCM); `def:quant-strategy-risk-sources` (`model-governance-controls`); `ev:square-root-impact` (`price-impact-execution`); `mech:futures-margin-settlement` (`futures-execution`); `def:securities-lending-fee-rebate` (`money-markets-repo-lending`). Kept distinct: the `backtest-inference` stub `ev:signal-decay-crowding`, which asks whether delayed-signal decay identifies crowding, a question that common positions and forced liquidation do not answer.

## Entry backlog

- ev:august-2007-quant-unwind: the August 2007 quant liquidation measured with data (losses, timing, the unwind hypothesis), to test Narang's four drivers (`exp-khandani-lo-quant-meltdown`, unread).
- mod:margin-liquidity-spiral: how margins and funding liquidity turn losses into forced sales and wider margins (`exp-brunnermeier-pedersen-liquidity`, unread).
- mod:volatility-targeting-deleveraging: leverage set inversely to measured volatility and correlation, raised as volatility falls and cut by many holders at once when it jumps, against Narang's 1.5-2 times estimate (no source checked; `risk-parity-vol-targeting` readings, unread).
- meth:overlap-crowding-measure: a crowding measure from the overlap of holdings, as the checkpoint asks (`wide-pedersen-exit`, `w4-chincarini-crowded-anomalies`, unread).

## Legacy candidate material

Run `python3 tools/migration_status.py` for the current counts. No legacy file lists this pathway; its slice-26 material came from a file mapped to `model-governance-controls`.

## What changed in my view or practice

## Questions carried forward

- Do Khandani and Lo's data support Narang's sequence (multi-strategy deleveraging first, then statistical arbitrage), and his claim that the losses were "solely the result of market impact"?
