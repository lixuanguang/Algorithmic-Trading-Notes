---
key: portfolio-construction-risk
section: portfolio-construction-risk
status: not started (draft entries only, not from study)
---

# Portfolio construction and risk (section overview)

Overview outcome, from the guide: construct and evaluate a portfolio whose forecasts, risk model, constraints, costs and tail measures are explicit and testable. Its checkpoint builds a long-only and a long-short portfolio from the same forecasts and risk model, reports ex-ante and realised risk, turnover, costs and the largest tail-loss contributors, and reruns with a shrunk covariance estimate. Its readings are `s7-meucci`, `alpha-grinold` and `s7-qrm`.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 15 October 2026 by systematic-investing architecture review (`notes/source-review-records.md`). This overview keeps the parts about the structure of a quant strategy and its forecasts: the black-box components and Narang's alpha taxonomy and strategy specification. Signal combination went to `equity-long-short-construction`, the production chain to `model-governance-controls`, and the execution and HFT material was merged into existing entries of `execution-trading-costs` and `hft-market-design`. The entries come from source checking against `s7-narang` (third edition, 2024), which is not one of the overview's readings; none of those has been read, and the checkpoint was not attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in systematic-investing architecture / source review / optimal execution / high-frequency strategies reviews:

- `def:quant-strategy-components`: Narang's alpha, risk and transaction cost models feeding portfolio construction, which interacts with execution, with data and research around them (chap. 2, pp. 16-19); the diagram, in this chapter's figures, has the return arrow of his Exhibit 2.1.
- `def:alpha-model-taxonomy`: alpha as skill in timing selection and sizing; theory-driven against data-driven; Narang's eight theory-driven classes by input; the trend follower's return-to-downside claim restored to its subject; carry kept apart from value as interpretation.
- `meth:alpha-strategy-specification`: forecast target, horizon, bet structure, universe, model specification, conditioning variables and run frequency; forecast strength tied to size only through calibration and the portfolio decision; Narang's claim that machine learning tests specifications "without overfitting" not adopted.

All three partly checked 2026-10-15, draft; human review outstanding.

Written in the portfolio moments and diversification slice (2026-10-18), owned here as the chapter's foundations:

- `meth:portfolio-return-moments`: one-period arithmetic portfolio return from beginning-of-period value weights (units, horizon, base currency, no intra-period cash flows); expected return, variance, standard deviation, covariance and correlation of portfolios in expanded and matrix form (Markowitz 1952, pp. 80-81; covariance of weighted sums); model moments against historical estimates and their denominators; rebalanced against buy-and-hold weights.
- `mech:diversification-correlation`: portfolio standard deviation against correlation for long-only weights; zero variance at a correlation of -1 only; reduction relative to the weighted average of volatilities, not a guarantee of beating the safer asset; Markowitz's "Diversification cannot eliminate all variance" with the equal-weight floor; Longin and Solnik on conditional and bear-market correlation.

Both partly checked 2026-10-18, draft; examples in `notes/artefacts/portfolio-risk-return/portfolio-moments-checks.py`; human review outstanding. Coverage records are editorial, not study.

Audit correction (2026-10-18): `mech:diversification-correlation` now qualifies the equal-correlation limit: a positive floor for a fixed positive correlation, sigma^2/N for zero correlation, and no fixed negative correlation as N grows, because an equicorrelation matrix needs -1/(N-1) <= rho <= 1. The boundary cases are checked in the same script.

Written in the portfolio choice and asset pricing batch (2026-10-18), in `portfolio-choice.tex`:

- `def:asset-class-characteristics`: what distinguishes cash, government and corporate bonds, equities, property and gold (SEC investor guide, pp. 1-3). Dated US table for 1928-2025 from Damodaran's January 2026 workbook (arithmetic and geometric means reproduced; standard deviations, real means and worst years computed). Historical averages against forward-looking expected returns; the stock-bond correlation by subperiod.
- `def:risk-aversion-utility`: concavity, the certainty equivalent and the Arrow-Pratt coefficient (Gollier, Hammitt and Treich 2013); Markowitz's U(E, V) and fair bets (p. 90). E - A sigma^2/2 exact under CARA-normal (Ross 1976, eq. (9)), with its units and gamma = A/2.
- `meth:efficient-frontier`: Markowitz pp. 82-89 and Fama-French Fig. 1. Closed forms under a budget constraint and their conditions; GMV; a three-fund example with a long-only boundary solution, an infeasible target and dominated portfolios. Figure `figures/mean-sd-frontier.tikz`.
- `meth:capital-allocation-line`: CAL, tangency and separation (Fama-French pp. 27-28; Sharpe pp. 432-435); y* for A = 2, 4, 8; a higher borrowing rate; the tangency condition r_f below the GMV mean; CAL against CML and the equilibrium assumptions.

In `asset-pricing-models.tex`, owned by `topic:asset-pricing-factor-models` and printed in this chapter:

- `mech:systematic-risk-pricing`: Sharpe's systematic and unsystematic components (pp. 438-440); the model-dependent pricing claim.
- `mod:return-generating-models`: the market and single-index models and multifactor return-generating models against pricing restrictions; uses.
- `mod:capm-sml`: assumptions, beta and the SML against the CML; the Black version; applications; Fama and French's evidence. Figure `figures/security-market-line.tikz`.
- `meth:capm-regression`: a declared twelve-month synthetic regression; raw against excess returns; uncertainty; alpha is not skill.
- `meth:required-return-on-equity`: inputs for 1 October 2026 (Damodaran's implied ERP 4.20 percent with a 5.29 percent Treasury rate; an assumed beta of 1.15); sensitivity; the difference from a historical average return.
- `mod:multifactor-apt`: Ross's argument and Theorem I; Huberman and Wang's exact and approximate forms; an original arbitrage among well-diversified portfolios and its residual-risk version.
- `def:factor-model-types`: Connor's three types (1995) and Huberman and Wang's three identification approaches; output interpretation and several risk dimensions.

Correction pass (2026-10-18, PR #22): `meth:efficient-frontier` no longer says constrained solutions must have zero weights, and `meth:required-return-on-equity` treats a historical premium with the current 10-year yield as a legitimate estimate with its own assumption and uncertainty (Damodaran's corporate finance project notes).

All partly checked 2026-10-18, draft. The examples are in `notes/artefacts/portfolio-risk-return/portfolio-choice-checks.py` and `notes/artefacts/asset-pricing-factor-models/asset-pricing-checks.py`; human review is outstanding.


Written in the performance and planning batch (2026-10-18):

In `investment-process-planning.tex` (topics `investment-management-process` and `investment-policy-planning`):

- `def:portfolio-management-process`: the portfolio perspective and the planning, execution and feedback steps (Maginn, Tuttle, McLeavey and Pinto, *Managing Investment Portfolios*, 3rd ed., 2007, chap. 1, pp. 2-10).
- `def:investor-types-needs`: individual and institutional investors; DB against DC plans, funded status and surplus risk (chap. 3, pp. 64-66 and 79-80); Exhibit 1-3's requirements and tolerances; Ang (2014) on sovereign funds, pension pillars, the US 5 percent foundation payout and individuals (chap. 1).
- `def:asset-management-industry`: fee economics and roles (MIP chap. 1, pp. 2-4); the four US registered fund types, disclosure, leverage limits and fulcrum fees (Ang chap. 16, pp. 523-527); hedge fund fees (chap. 17, pp. 581-582); separate accounts; ICI 2026 Fact Book figures for year-end 2025.
- `meth:investment-policy-statement`: purpose and components, risk objective with willingness and ability, return objective and required return, constraints (chap. 1, pp. 2, 5-7 and 11-17); Maginn's required-return examples reproduced.
- `meth:asset-class-portfolio-construction`: strategic allocation with ranges and asset-class criteria (chap. 5, pp. 231-232 and 248-249); risk budgeting; harmonised ESG approach definitions (GSIA 2022, p. 7) and Ang's view of exclusions as costed constraints (chap. 3, pp. 110-112).
- `ex:investment-planning-case`: a fictional surgeon's case: required real return 2.70 percent, three candidate allocations, IPS provisions, a concentrated holding and a futures overlay.

In `behavioural-finance.tex` (topic `behavioral-finance`):

- `def:behavioural-biases`: beliefs and preferences (Barberis and Thaler, NBER w9222, secs. 3.1-3.2, pp. 12-21); Statman's cognitive and emotional shortcuts and errors (2019, chaps. 1, 3 and 4); effects on decisions and remedies, including Kahneman's decorrelation and premortem.
- `mech:biases-market-anomalies`: limits to arbitrage (pp. 3-6); size, reversal, value, momentum and drift with the BSV account (pp. 33-34 and 38-39); closed-end fund discounts (p. 44); home bias, naive diversification, excessive trading and the disposition effect (pp. 47-50).

In `risk-governance.tex` (topic `risk-management-framework`):

- `def:risk-management-framework`: definition, process, governance and ERM, risk tolerance, risk budgeting and limits (MIP chap. 9, pp. 579-584 and 634-635); Damodaran's risk hedging against risk management (2008, pp. 303-304).
- `meth:risk-identification-modification`: financial and non-financial risks (chap. 9, pp. 585-586, 596 and 623); Damodaran's alternatives for reducing exposure (chap. 10, pp. 331-335); the case's overlay.

In `active-management.tex` (topic `active-management-analysis`):

- `meth:active-return-information-ratio`: value added from active weights (MIP chap. 12, p. 743); ex post and ex ante IR, Table 5.1 and Table 5.3 (Grinold and Kahn, chap. 5, pp. 110-123); Bacon's tracking error and IR conventions (pp. 167-169); Sharpe's (1994) differential-return ratio; optimal active risk and SR_P^2 = SR_B^2 + IR^2, derived.
- `res:fundamental-law-active-management`: IR = IC sqrt(BR), assumptions, additivity and examples (chap. 6, pp. 147-162); the transfer coefficient (Grinold and Kahn 2020, pp. 23 and 27-29); a constrained five-stock check of IR_P = TC x IR_Q.
- `meth:active-risk-decomposition`: factor and specific active variance (chap. 3, pp. 76-77), active beta and residual risk (chap. 4, p. 90), marginal contributions (p. 67).

All partly checked 2026-10-18, draft. Examples in `notes/artefacts/investment-planning/investment-planning-checks.py` and `notes/artefacts/active-management-analysis/active-management-checks.py`; human review is outstanding. Coverage records are editorial, not study.

## Source verification after macro markets and pricing review

method validation (2026-10-17) (audit repairs and a source-review coverage; source verification and bounded tests, not study or human review): Queue: `ev:trend-following-evidence` resolved by merge into `def:alpha-model-taxonomy`'s pitfalls (Moskowitz, Ooi and Pedersen's abstract; Hurst, Ooi and Pedersen's 1880-2016 Exhibit 1: 7.3 percent net, 9.7 percent volatility, Sharpe 0.76, drawdowns up to 25 percent). The record is in `notes/source-review-records.md`, *method validation (2026-10-17)*.

empirical extensions (2026-10-17) (six audit repairs and a source-review coverage; source verification and bounded tests, not study or human review): `meth:residual-reversion-strategy` narrowed (Avellaneda and Lee and Gatev et al. merged into the alpha taxonomy); `ev:value-carry-premia` resolved (Koijen et al., Asness, Moskowitz and Pedersen and the QMJ paper merged into `def:alpha-model-taxonomy`). The record is in `notes/source-review-records.md`, *empirical extensions (2026-10-17)*.

derivatives and empirical validation (2026-10-17) (seven audit repairs, backlog reconciliation and a source-review coverage; source verification and bounded tests, not study or human review): the `def:alpha-model-taxonomy` and `meth:s-score-residual-trading` questions: Lo and MacKinlay's decomposition of contrarian profits, Avellaneda and Lee's s-score thresholds (chosen inside their backtest period) and Moskowitz, Ooi and Pedersen's position sizing merged into `def:alpha-model-taxonomy`; `meth:residual-reversion-strategy` narrowed. The record is in `notes/source-review-records.md`, *derivatives and empirical validation (2026-10-17)*.

## Related entries owned elsewhere

Cross-referenced, not owned here: `meth:alpha-signal-combination` (`equity-long-short-construction`), `meth:strategy-production-lifecycle` (`model-governance-controls`), and the merges into `def:order-exposure-decisions`, `def:portfolio-trading`, `def:automated-trading-architecture` (`execution-trading-costs`) and `def:hft-strategies` (`hft-market-design`); also `mod:factor-risk-model`, `meth:rule-based-position-sizing`, `mod:mean-variance-portfolio-optimisation` and `mod:portfolio-transaction-cost-function` (`portfolio-construction`), and `meth:hypothesis-driven-strategy-research` and `pit:parameter-overfitting` (`backtest-inference`).

## Entry backlog

- meth:residual-reversion-strategy: after-cost capacity and crowding evidence for residual reversal at scale; Khandani and Lo give the August 2007 paths only as figures. Avellaneda and Lee's s-score rule, Lo and MacKinlay's decomposition and Gatev et al. are in `def:alpha-model-taxonomy`. Home pathway `statistical-arbitrage`.

## What changed in my view or practice

## Questions carried forward

- Narang's eight classes and Exhibit 3.2 are a practitioner's framework; does `alpha-grinold`'s account of forecasts and information coefficients organise them differently?
