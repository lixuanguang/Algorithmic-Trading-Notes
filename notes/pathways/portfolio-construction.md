---
key: portfolio-construction
section: portfolio-construction-risk
status: not started (draft entries from the migration only)
---

# Portfolio construction, estimation error and risk models

Pathway outcome, from the guide: construct a constrained portfolio from noisy forecasts with a factor risk model, shrinkage and costs, and attribute its realised risk. Its checkpoint builds mean-variance portfolios for a 500-stock universe with sample, shrunk and factor-model covariances, plus ERC and HRP, and backtests them with costs, reporting ex-ante against realised risk, transfer coefficients and turnover. Its fifteen readings run from mean-variance selection and estimation error (`s6-markowitz`, `wide-michaud-enigma`, `wide-chopra-ziemba`, `wide-kan-zhou`, `s7-demiguel`), through shrinkage, factor risk models and constrained or risk-based portfolios (`wide-ledoit-wolf-review`, `wide-connor-goldberg-korajczyk`, `wide-demiguel-norm`, `alpha-black`, `wide-maillard-roncalli-erc`, `wide-lopez-de-prado-hrp`, `w3-kelly-upsa`), to implementation with the transfer coefficient and convex optimisation with costs, single- and multi-period (`wide-clarke-transfer-coefficient`, `wide-boyd-markowitz-seventy`, `exp-boyd-multiperiod-trading`).

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 15 October 2026 by migration slice 27 (`notes/migration-slices.md`). That slice routed the introduction and the *Types of Transaction Cost Models* block of the legacy transaction-cost-models file (`sysinv/txncostmod.tex`, Narang's systematic-investing notes) here, against the file's map candidate, the section overview `portfolio-construction-risk`. The overview's outcome makes costs explicit and testable in a portfolio, but its goal for constrained portfolios "with factor risk models, shrinkage and costs" names this pathway. The entry comes from source checking against `s7-narang` (third edition, 2024), which is not a reading of this pathway. Slice 28 migrated the file mapped to this pathway alone (`sysinv/portconstmod.tex`), checking it against Narang's chap. 6 and reading one of the pathway's readings, Boyd et al. (`wide-boyd-markowitz-seventy`, authors' version of 5 January 2024, selected sections), for method mechanics. That is source checking, not study: no reading has been studied, and the checkpoint was not attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in migration slice 27, 2026-10-15:

- `mod:portfolio-transaction-cost-function`: Narang's transaction cost model as an input to portfolio construction, not a cost minimiser; his flat, linear, piecewise-linear and quadratic forms written as total cost against signed size, with units, the per-unit form of each, and the square-root law as a 3/2-power total; his exhibits read as schematic against an assumed convex curve, so no general ranking of accuracy or computational cost is adopted; his note 2's conflation of per-share and total exponents recorded.

Changed in the slice-27 follow-up, 2026-10-15: the entry's notation is now for one equity in shares ($q$, $V$ in shares, $P$ in currency per share), with per-share cost defined only for $q\neq0$; every form has nonnegative coefficients and $C(0)=0$; the piecewise-linear form is a convex hinge sum, equal to a maximum of lines only with matching intercepts; the 3/2-power form is written out; and the assumptions (symmetric, nonnegative, expected, one instrument and period) are stated, with contracts and notional left to their own units.

Verification partly checked 2026-10-15, stability draft; human review outstanding. Its artefact is `notes/artefacts/portfolio-construction-risk/transaction-cost-models.tex` (under the map candidate, keeping the file whole).

Written in migration slice 28, 2026-10-15, from Narang's chap. 6, "Portfolio Construction Models" (`s7-narang`, third edition, pp. 99-125), with Boyd et al. for mechanics:

- `meth:rule-based-position-sizing`: the two families; equal position, equal risk, alpha-driven and decision-tree weighting; Narang's two arguments against unequal weights, placed where he puts them (the legacy filed the second under equal weighting); Exhibit 6.1's weights shown to be inverse-variance; inverse volatility kept apart from equal risk contribution under a full covariance matrix (three-asset example computed).
- `mod:mean-variance-portfolio-optimisation`: Markowitz's two forms and their closed form (Boyd et al.), Sharpe maximisation as a separate objective, expected drawdown outside the model, the unconstrained single-asset claim corrected by Narang's own example, inputs (GARCH prevalence as his unsourced claim; correlation grouping as his two-pair illustration), constraints, costs (cross-referenced), solver claims against Boyd et al.'s Table 2, Black-Litterman acting on means not correlations, resampling by reordering unable to change the sample moments, and the legacy data-mining item not adopted.
- `meth:signal-portfolio-allocation`: Narang's account of Grinold and Kahn's factor-portfolio optimisation, his 0.2% example checked, "not more than about 20" kept as his statement, Grinold and Kahn unread.

Changed in slice 28: `mod:portfolio-transaction-cost-function` now cites Boyd et al. secs. 2.4 and 4.3 for its remarks on convex cost terms and nonconvex constraints.

All three new entries partly checked 2026-10-15, draft; human review outstanding. Their artefact is `notes/artefacts/portfolio-construction-risk/portfolio-construction-models.tex`, a new file beside slice 27's.

## Related entries owned elsewhere

Cross-referenced, not owned here: `def:transaction-costs` and `meth:transaction-cost-analysis` (`execution-trading-costs`; the same legacy file's cost-components block was merged into the first, and is listed in that note); `mod:almgren-chriss-execution` (`execution-trading-costs`); `ev:square-root-impact` and `meth:almgren-impact-estimation` (`price-impact-execution`; the empirical shape of costs, not changed); `pit:backtest-cost-short-assumptions` (`backtest-inference`; the effect of misestimated costs, not changed); from slice 28, `pit:parameter-overfitting` and `meth:backtest-evaluation-diagnostics` (`backtest-inference`) and `def:common-investor-contagion` (`funding-crowding`), cross-referenced and not changed.

## Entry backlog

- meth:convex-cost-portfolio-optimisation: linear, quadratic and 3/2-power cost terms in a convex single- and multi-period portfolio problem, and what each form demands of the solver, to replace the entry's interpretation of computational cost (`wide-boyd-markowitz-seventy` read in part in slice 28, secs. 2.4 and 4.3; `exp-boyd-multiperiod-trading` unread).
- res:no-trade-region: proportional costs create a region around the target in which not trading is optimal (`w2-davis-norman`, an optional branch, unread).
- mod:black-litterman: equilibrium (market-implied) returns combined with views and their confidence into posterior expected returns, to check Narang's description and the legacy claim about correlations (`alpha-black`, unread).
- meth:resampled-efficiency: what Michaud's resampling draws, what it averages, and whether it improves out-of-sample results (Michaud's book, not catalogued; `wide-michaud-enigma` for the estimation-error critique; unread).
- meth:portfolio-covariance-estimation: factor models and shrinkage for large covariance matrices, against Narang's grouping of similar instruments (`wide-ledoit-wolf-review`, `wide-connor-goldberg-korajczyk`, unread; EWMA and DCC as listed by Boyd et al., sec. 3.4).
- meth:equal-risk-contribution: equal contributions to portfolio risk under a full covariance matrix, against inverse-volatility weights (`wide-maillard-roncalli-erc`, unread); home pathway `risk-parity-vol-targeting`.
- mod:garch-volatility-forecast: GARCH and EWMA volatility forecasts and their comparative accuracy, against Narang's prevalence claim (`s7-bollerslev`, unread); home pathway `time-series-volatility`.

## Legacy candidate material

Run `python3 tools/migration_status.py` for the current counts. The legacy file still mapped to this pathway is `sysinv/riskmod.tex`; slice 28 migrated `sysinv/portconstmod.tex`.

## What changed in my view or practice

## Questions carried forward

- Narang's note 2 (p. 97) reports square-root cost per share for U.S. equities as better supported than a quadratic total but cites nothing; which form should a portfolio's cost term take for the checkpoint's 500-stock universe, given the impact evidence owned by `price-impact-execution`?
- Narang's Exhibit 6.1 labels inverse-variance weights "volatility-adjusted"; which rule did the third edition intend, and does any earlier edition differ?
