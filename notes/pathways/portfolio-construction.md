---
key: portfolio-construction
section: portfolio-construction-risk
status: not started (draft entries only, not from study)
---

# Portfolio construction, estimation error and risk models

Pathway outcome, from the guide: construct a constrained portfolio from noisy forecasts with a factor risk model, shrinkage and costs, and attribute its realised risk. Its checkpoint builds mean-variance portfolios for a 500-stock universe with sample, shrunk and factor-model covariances, plus ERC and HRP, and backtests them with costs, reporting ex-ante against realised risk, transfer coefficients and turnover. Its fifteen readings run from mean-variance selection and estimation error (`s6-markowitz`, `wide-michaud-enigma`, `wide-chopra-ziemba`, `wide-kan-zhou`, `s7-demiguel`), through shrinkage, factor risk models and constrained or risk-based portfolios (`wide-ledoit-wolf-review`, `wide-connor-goldberg-korajczyk`, `wide-demiguel-norm`, `alpha-black`, `wide-maillard-roncalli-erc`, `wide-lopez-de-prado-hrp`, `w3-kelly-upsa`), to implementation with the transfer coefficient and convex optimisation with costs, single- and multi-period (`wide-clarke-transfer-coefficient`, `wide-boyd-markowitz-seventy`, `exp-boyd-multiperiod-trading`).

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 15 October 2026 by transaction-cost models review (`notes/source-review-records.md`). The overview's outcome makes costs explicit and testable in a portfolio, but its goal for constrained portfolios "with factor risk models, shrinkage and costs" names this pathway. The entry comes from source checking against `s7-narang` (third edition, 2024), which is not a reading of this pathway. Portfolio construction review checked Narang's chap. 6 and read one of the pathway's readings, Boyd et al. (`wide-boyd-markowitz-seventy`, authors' version of 5 January 2024, selected sections), for method mechanics. That is source checking, not study: no reading has been studied, and the checkpoint was not attempted. financial data and labels review (16 October 2026) added material from López de Prado's data-structures chapter, checked against `alpha-afml`, which is not a reading of this pathway.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in transaction-cost models / source review / optimal execution / high-frequency strategies reviews:

- `mod:portfolio-transaction-cost-function`: Narang's transaction cost model as an input to portfolio construction, not a cost minimiser; his flat, linear, piecewise-linear and quadratic forms written as total cost against signed size, with units, the per-unit form of each, and the square-root law as a 3/2-power total; his exhibits read as schematic against an assumed convex curve, so no general ranking of accuracy or computational cost is adopted; his note 2's conflation of per-share and total exponents recorded.

Changed in the transaction-cost models review follow-up, 2026-10-15: the entry's notation is now for one equity in shares ($q$, $V$ in shares, $P$ in currency per share), with per-share cost defined only for $q\neq0$; every form has nonnegative coefficients and $C(0)=0$; the piecewise-linear form is a convex hinge sum, equal to a maximum of lines only with matching intercepts; the 3/2-power form is written out; and the assumptions (symmetric, nonnegative, expected, one instrument and period) are stated, with contracts and notional left to their own units.

Verification partly checked 2026-10-15, stability draft; human review outstanding.

Written in portfolio construction / source review / optimal execution / high-frequency strategies reviews, from Narang's chap. 6, "Portfolio Construction Models" (`s7-narang`, third edition, pp. 99-125), with Boyd et al. for mechanics:

- `meth:rule-based-position-sizing`: the two families; equal position, equal risk, alpha-driven and decision-tree weighting; Narang's two arguments against unequal weights, placed where he puts them; Exhibit 6.1's weights shown to be inverse-variance; inverse volatility kept apart from equal risk contribution under a full covariance matrix (three-asset example computed).
- `mod:mean-variance-portfolio-optimisation`: Markowitz's two forms and their closed form (Boyd et al.), Sharpe maximisation as a separate objective, expected drawdown outside the model, the unconstrained single-asset claim corrected by Narang's own example, inputs (GARCH prevalence as his unsourced claim; correlation grouping as his two-pair illustration), constraints, costs (cross-referenced), solver claims against Boyd et al.'s Table 2, Black-Litterman acting on means not correlations, resampling described by Narang as reordering one series (which keeps that series' mean and variance; corrected in the follow-up below).
- `meth:signal-portfolio-allocation`: Narang's account of Grinold and Kahn's factor-portfolio optimisation, his 0.2% example checked, "not more than about 20" kept as his statement, Grinold and Kahn unread.

Changed in portfolio construction review: `mod:portfolio-transaction-cost-function` now cites Boyd et al. secs. 2.4 and 4.3 for its remarks on convex cost terms and nonconvex constraints.

Changed in the portfolio construction review follow-up, 2026-10-15: `mod:mean-variance-portfolio-optimisation` now states the closed form's conditions (positive-definite $\Sigma$, $\gamma>0$, a feasible volatility target), defines $\nu^\star$ as the budget constraint's multiplier, says a singular $\Sigma$ needs separate treatment rather than a pseudoinverse by default, and adds that ignoring risk without bounds can make the problem unbounded; its resampling passage now separates one series, a common row permutation (covariance kept) and independent permutations (covariance changed); and its machine-learning passage separates forecasting, learning allocation weights and optimisation. `meth:rule-based-position-sizing` now gives the ERC weights as about 29.93, 29.93 and 40.15 percent (40.2 was a rounding slip) and requires positive portfolio variance for normalised risk contributions. `mod:portfolio-transaction-cost-function` now says which pathway reading was read.

All three new entries partly checked 2026-10-15, draft; human review outstanding.

Written in risk models / source review / optimal execution / high-frequency strategies reviews, from Narang's chap. 4, "Risk Models" (`s7-narang`, third edition, pp. 71-84), with Boyd et al. secs. 3.3 and 4.2:

- `mod:factor-risk-model`: risk as an unforecast exposure and the risk model as an input to the portfolio decision, not the decision; the factor model $r=Ff+\epsilon$ with $\Sigma=F\Sigma_fF^\top+D$ and its assumptions; diversification of residual risk under stated correlation conditions (computed; corrected in the risk models review follow-up); economic against PCA factors, whose labels are after-the-fact; exposure limits and neutrality, with zero covariance kept apart from zero exposure (computed); a market, size, value and momentum list, not in Narang's chapter, read as roles that depend on the strategy; "unintended" not the same as "uncompensated"; updating not evidence of better forecasts.
- Merged into `mod:mean-variance-portfolio-optimisation`: hard limits against penalties, with Boyd et al.'s softening (a penalty replaces a limit; mandated limits stay hard); limit levels from theory or data; where limits apply; volatility and dispersion read as parts of one covariance model, with Narang's dispersion inference and VaR description not adopted.

Changed in the risk models review follow-up, 2026-10-15: `mod:factor-risk-model` now treats a diagonal residual covariance as sufficient, not necessary, for residual diversification (constant equicorrelation leaves a floor; correlation within disjoint pairs gives $0.108/n$ and still diversifies); the CVX-XOM pair is an approximate hedge that Narang says "substantially eliminated" market risk, exact only with equal betas; and his rule is quoted as no expectation of being compensated *sufficiently*, not of earning nothing.

Both partly checked 2026-10-15, draft; human review outstanding.

Written in financial data and labels / source review / optimal execution / execution control reviews:

- `mod:pca-risk-distribution-weights`: López de Prado's weights that deliver a chosen distribution of risk across principal components (`alpha-afml`, chap. 2, sec. 2.4.2, pp. 35-36), with two formula slips corrected, the positive-eigenvalue requirement, the sign indeterminacy ($2^k$ allocations per risk distribution, $k$ the components given risk, when eigenvalues are distinct) and the estimation-error caveat for the smallest eigenvalues.

Partly checked 2026-10-16, draft; human review outstanding. Checks: `afml-checks.py`.

method validation (2026-10-17):

- `mod:black-litterman`: equilibrium returns, views and the posterior mean, with numerical checks; a claim that it adjusts correlations corrected. Partly checked 2026-10-17, draft.
- `meth:portfolio-covariance-estimation`: linear and nonlinear shrinkage of large covariance matrices, with an own simulation. Partly checked 2026-10-17, draft.

Written in empirical extensions (2026-10-17) (source verification and bounded checks, not study or human review):

- `meth:equal-risk-contribution`: ERC against inverse-volatility weights, with own checks (`erc-check.py`). Partly checked 2026-10-17, draft; human review outstanding.
- `mod:garch-volatility-forecast`: GARCH(1,1) against EWMA, with own synthetic checks (`garch-ewma-check.py`). Partly checked 2026-10-17, draft; human review outstanding.
- `meth:resampled-efficiency`: Michaud resampling: what is drawn and averaged, and the proponents' simulation evidence. Partly checked 2026-10-17, draft; human review outstanding.

## Source verification after macro markets and pricing review

source verification (2026-10-17) (source verification and bounded tests, not study or human review): `meth:convex-cost-portfolio-optimisation` resolved by merge into `mod:portfolio-transaction-cost-function` (Boyd et al., *Multi-Period Trading via Convex Optimization*, 2017, author-hosted PDF, secs. 2.3, 4.7 and 5.3): the a|x| + b sigma |x|^{3/2}/V^{1/2} + cx cost, convexity of the common variants and nonconvexity of fixed fees, interior-point cost O(nk^2) 'even for ... the 3/2 power transaction costs', a coefficient near 2 for purely quadratic problems, and multi-period effort linear in the horizon; the piecewise-linear reformulation remains our interpretation. The record is in `notes/source-review-records.md`, *source verification (2026-10-17)*.

method validation (2026-10-17) (audit repairs and a source-review coverage; source verification and bounded tests, not study or human review): Queue: `mod:black-litterman` resolved as a new entry (Black and Litterman's October 1991 Goldman Sachs paper, appendix formula by page image; the 1992 FAJ article not compared); `meth:portfolio-covariance-estimation` narrowed with a new entry (Ledoit and Wolf's review, UZH WP 323; factor-model estimation unread); `res:no-trade-region` narrowed (Guasoni and Muhle-Karbe's survey restates Davis and Norman and the epsilon^(1/3) width; merged into `mod:portfolio-transaction-cost-function`). The record is in `notes/source-review-records.md`, *method validation (2026-10-17)*.

empirical extensions (2026-10-17) (six audit repairs and a source-review coverage; source verification and bounded tests, not study or human review): `res:no-trade-region` blocked (Davis and Norman (1990) has no open copy (arXiv and OpenAlex searched)); `meth:portfolio-covariance-estimation` narrowed (Boyd et al. sec. 3.4 and their backtest's normalised EWMA (half-life 125 days) merged into `meth:portfolio-covariance-estimation`; factor-model estimation and DCC unread); `meth:resampled-efficiency` narrowed (new entry `meth:resampled-efficiency` from the Michauds' authors' version (2007): what is drawn and averaged; out-of-sample evidence only the proponents' simulation); `meth:equal-risk-contribution` resolved (new entry `meth:equal-risk-contribution` from Maillard, Roncalli and Teïletche); `mod:garch-volatility-forecast` resolved (new entry `mod:garch-volatility-forecast` from Christoffersen and Hansen and Lunde). The record is in `notes/source-review-records.md`, *empirical extensions (2026-10-17)*.

derivatives and empirical validation (2026-10-17) (seven audit repairs, backlog reconciliation and a source-review coverage; source verification and bounded tests, not study or human review): audit repairs: `meth:equal-risk-contribution`'s maximum-Sharpe statement qualified (positive common Sharpe ratio needed; counterexample with Sharpe $-\sqrt2$). The `meth:portfolio-covariance-estimation`, `meth:constant-correlation-shrinkage`, `meth:poet-covariance` and `meth:shrinkage-estimator-choice` questions (DCC, the constant-correlation shrinkage intensity, POET and the 2022 review) into `meth:portfolio-covariance-estimation`; 15-16 (Markowitz 1952 and DeMiguel, Garlappi and Uppal) into `mod:mean-variance-portfolio-optimisation`; 17 (multi-period optimisation) into `mod:portfolio-transaction-cost-function`; 18-19 (Qian; Maillard, Roncalli and Teiletche's backtests) into `meth:equal-risk-contribution`; 68 (Shreve and Soner) narrowed `res:no-trade-region`. The record is in `notes/source-review-records.md`, *derivatives and empirical validation (2026-10-17)*.

## Related entries owned elsewhere

Cross-referenced, not owned here: `def:transaction-costs` and `meth:transaction-cost-analysis` (`execution-trading-costs`; the cost components are in the first, listed in that note); `mod:almgren-chriss-execution` (`execution-trading-costs`); `ev:square-root-impact` and `meth:almgren-impact-estimation` (`price-impact-execution`; the empirical shape of costs, not changed); `pit:backtest-cost-short-assumptions` (`backtest-inference`; the effect of misestimated costs, not changed); from portfolio construction review, `pit:parameter-overfitting` and `meth:backtest-evaluation-diagnostics` (`backtest-inference`) and `def:common-investor-contagion` (`funding-crowding`), cross-referenced and not changed; from risk models review, `def:quant-strategy-risk-sources` (`model-governance-controls`), cross-referenced and not changed, and the stub `meth:var-es-estimation-methods` in `risk-tail-systemic`, which holds this pathway's statistical-methods item.

## Entry backlog

- res:no-trade-region: Davis and Norman's (1990) own paper (`w2-davis-norman`): no open copy; Shreve and Soner's account of it and their wealth-independent no-trade interval are in `mod:portfolio-transaction-cost-function`.
- meth:resampled-efficiency: independent out-of-sample evidence on resampled efficiency (the entry's only evidence is the proponents' simulation) and the estimation-error critique of `wide-michaud-enigma`.
- meth:portfolio-covariance-estimation: estimating a factor model's loadings, factor covariance and residual variances (`wide-connor-goldberg-korajczyk`), the nonlinear-shrinkage formula itself, and Engle's 2002 DCC paper (Engle and Sheppard's account is read). Shrinkage targets and intensity, POET, DCC's equations and the 2022 review's recommendations are in the entry.

## What changed in my view or practice

## Questions carried forward

- Narang's note 2 (p. 97) reports square-root cost per share for U.S. equities as better supported than a quadratic total but cites nothing; which form should a portfolio's cost term take for the checkpoint's 500-stock universe, given the impact evidence owned by `price-impact-execution`?
- Narang's Exhibit 6.1 labels inverse-variance weights "volatility-adjusted"; which rule did the third edition intend, and does any earlier edition differ?
