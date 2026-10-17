---
key: portfolio-construction-risk
section: portfolio-construction-risk
status: not started (draft entries from the migration only)
---

# Portfolio construction and risk (section overview)

Overview outcome, from the guide: construct and evaluate a portfolio whose forecasts, risk model, constraints, costs and tail measures are explicit and testable. Its checkpoint builds a long-only and a long-short portfolio from the same forecasts and risk model, reports ex-ante and realised risk, turnover, costs and the largest tail-loss contributors, and reruns with a shrunk covariance estimate. Its readings are `s7-meucci`, `alpha-grinold` and `s7-qrm`.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 15 October 2026 by migration slice 30 (`notes/migration-slices.md`), which migrated the last three files of Narang's systematic-investing notes, all mapped to this overview. This overview keeps the parts about the structure of a quant strategy and its forecasts: the black-box components and Narang's alpha taxonomy and strategy specification. Signal combination went to `equity-long-short-construction`, the production chain to `model-governance-controls`, and the execution and HFT material was merged into existing entries of `execution-trading-costs` and `hft-market-design`. The entries come from source checking against `s7-narang` (third edition, 2024), which is not one of the overview's readings; none of those has been read, and the checkpoint was not attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in migration slice 30, 2026-10-15:

- `def:quant-strategy-components`: Narang's alpha, risk and transaction cost models feeding portfolio construction, which interacts with execution, with data and research around them (chap. 2, pp. 16-19); the legacy diagram, moved to this chapter's figures, now has the return arrow of his Exhibit 2.1.
- `def:alpha-model-taxonomy`: alpha as skill in timing selection and sizing; theory-driven against data-driven; Narang's eight theory-driven classes by input (the legacy listed five); the trend follower's return-to-downside claim restored to its subject; carry kept apart from value as interpretation.
- `meth:alpha-strategy-specification`: forecast target, horizon, bet structure, universe, model specification, conditioning variables (omitted by the legacy) and run frequency; forecast strength tied to size only through calibration and the portfolio decision; Narang's claim that machine learning tests specifications "without overfitting" not adopted.

All three partly checked 2026-10-15, draft; human review outstanding. Their artefacts are `notes/artefacts/portfolio-construction-risk/systematic-investing-overview.tex` (with exact copies of the legacy overview, chapter wrapper and diagram) and `alpha-models.tex`.

## Source verification after slice 37

Second batch of 2026-10-17 (audit repairs and a 50-item queue; source verification and bounded tests, not study or human review): Queue: `ev:trend-following-evidence` resolved by merge into `def:alpha-model-taxonomy`'s pitfalls (Moskowitz, Ooi and Pedersen's abstract; Hurst, Ooi and Pedersen's 1880-2016 Exhibit 1: 7.3 percent net, 9.7 percent volatility, Sharpe 0.76, drawdowns up to 25 percent). The record is in `notes/migration-slices.md`, *Second batch of 17 October 2026*.

Third batch of 2026-10-17 (six audit repairs and a 60-item queue; source verification and bounded tests, not study or human review): `meth:residual-reversion-strategy` narrowed (Avellaneda and Lee and Gatev et al. merged into the alpha taxonomy); `ev:value-carry-premia` resolved (Koijen et al., Asness, Moskowitz and Pedersen and the QMJ paper merged into `def:alpha-model-taxonomy`). The record is in `notes/migration-slices.md`, *Third batch of 17 October 2026*.

Fourth batch of 2026-10-17 (seven audit repairs, backlog reconciliation and a 70-target batch; source verification and bounded tests, not study or human review): targets 21, 22 and 24: Lo and MacKinlay's decomposition of contrarian profits, Avellaneda and Lee's s-score thresholds (chosen inside their backtest period) and Moskowitz, Ooi and Pedersen's position sizing merged into `def:alpha-model-taxonomy`; `meth:residual-reversion-strategy` narrowed. The record is in `notes/migration-slices.md`, *Fourth batch of 17 October 2026*.

## Related entries owned elsewhere

Cross-referenced, not owned here: from the same legacy files, `meth:alpha-signal-combination` (`equity-long-short-construction`), `meth:strategy-production-lifecycle` (`model-governance-controls`), and the merges into `def:order-exposure-decisions`, `def:portfolio-trading`, `def:automated-trading-architecture` (`execution-trading-costs`) and `def:hft-strategies` (`hft-market-design`); also `mod:factor-risk-model`, `meth:rule-based-position-sizing`, `mod:mean-variance-portfolio-optimisation` and `mod:portfolio-transaction-cost-function` (`portfolio-construction`), and `meth:hypothesis-driven-strategy-research` and `pit:parameter-overfitting` (`backtest-inference`).

## Entry backlog

- meth:residual-reversion-strategy: after-cost capacity and crowding evidence for residual reversal at scale; Khandani and Lo give the August 2007 paths only as figures. Avellaneda and Lee's s-score rule, Lo and MacKinlay's decomposition and Gatev et al. are in `def:alpha-model-taxonomy`. Home pathway `statistical-arbitrage`.

## Legacy candidate material

Run `python3 tools/migration_status.py` for the current counts. No legacy file now lists this overview: slice 30 migrated the last three and removed the legacy chapter. That says nothing about consolidation: the backlog is open and no reading has been studied.

## What changed in my view or practice

## Questions carried forward

- Narang's eight classes and Exhibit 3.2 are a practitioner's framework; does `alpha-grinold`'s account of forecasts and information coefficients organise them differently?
