---
key: portfolio-construction
section: portfolio-construction-risk
status: not started (draft entries from the migration only)
---

# Portfolio construction, estimation error and risk models

Pathway outcome, from the guide: construct a constrained portfolio from noisy forecasts with a factor risk model, shrinkage and costs, and attribute its realised risk. Its checkpoint builds mean-variance portfolios for a 500-stock universe with sample, shrunk and factor-model covariances, plus ERC and HRP, and backtests them with costs, reporting ex-ante against realised risk, transfer coefficients and turnover. Its fifteen readings run from mean-variance selection and estimation error (`s6-markowitz`, `wide-michaud-enigma`, `wide-chopra-ziemba`, `wide-kan-zhou`, `s7-demiguel`), through shrinkage, factor risk models and constrained or risk-based portfolios (`wide-ledoit-wolf-review`, `wide-connor-goldberg-korajczyk`, `wide-demiguel-norm`, `alpha-black`, `wide-maillard-roncalli-erc`, `wide-lopez-de-prado-hrp`, `w3-kelly-upsa`), to implementation with the transfer coefficient and convex optimisation with costs, single- and multi-period (`wide-clarke-transfer-coefficient`, `wide-boyd-markowitz-seventy`, `exp-boyd-multiperiod-trading`).

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 15 October 2026 by migration slice 27 (`notes/migration-slices.md`). That slice routed the introduction and the *Types of Transaction Cost Models* block of the legacy transaction-cost-models file (`sysinv/txncostmod.tex`, Narang's systematic-investing notes) here, against the file's map candidate, the section overview `portfolio-construction-risk`. The overview's outcome makes costs explicit and testable in a portfolio, but its goal for constrained portfolios "with factor risk models, shrinkage and costs" names this pathway. The entry comes from source checking against `s7-narang` (third edition, 2024), which is not a reading of this pathway. None of the pathway's readings has been read, and the checkpoint was not attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in migration slice 27, 2026-10-15:

- `mod:portfolio-transaction-cost-function`: Narang's transaction cost model as an input to portfolio construction, not a cost minimiser; his flat, linear, piecewise-linear and quadratic forms written as total cost against signed size, with units, the per-unit form of each, and the square-root law as a 3/2-power total; his exhibits read as schematic against an assumed convex curve, so no general ranking of accuracy or computational cost is adopted; his note 2's conflation of per-share and total exponents recorded.

Verification partly checked 2026-10-15, stability draft; human review outstanding. Its artefact is `notes/artefacts/portfolio-construction-risk/transaction-cost-models.tex` (under the map candidate, keeping the file whole).

## Related entries owned elsewhere

Cross-referenced, not owned here: `def:transaction-costs` and `meth:transaction-cost-analysis` (`execution-trading-costs`; the same legacy file's cost-components block was merged into the first, and is listed in that note); `mod:almgren-chriss-execution` (`execution-trading-costs`); `ev:square-root-impact` and `meth:almgren-impact-estimation` (`price-impact-execution`; the empirical shape of costs, not changed); `pit:backtest-cost-short-assumptions` (`backtest-inference`; the effect of misestimated costs, not changed).

## Entry backlog

- meth:convex-cost-portfolio-optimisation: linear, quadratic and 3/2-power cost terms in a convex single- and multi-period portfolio problem, and what each form demands of the solver, to replace the entry's interpretation of computational cost (`wide-boyd-markowitz-seventy`, `exp-boyd-multiperiod-trading`, unread).
- res:no-trade-region: proportional costs create a region around the target in which not trading is optimal (`w2-davis-norman`, an optional branch, unread).

## Legacy candidate material

Run `python3 tools/migration_status.py` for the current counts. The legacy files mapped to this pathway are `sysinv/portconstmod.tex` and `sysinv/riskmod.tex`.

## What changed in my view or practice

## Questions carried forward

- Narang's note 2 (p. 97) reports square-root cost per share for U.S. equities as better supported than a quadratic total but cites nothing; which form should a portfolio's cost term take for the checkpoint's 500-stock universe, given the impact evidence owned by `price-impact-execution`?
