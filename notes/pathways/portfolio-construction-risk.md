---
key: portfolio-construction-risk
section: portfolio-construction-risk
status: not started (draft entries only, not from study)
---

# Portfolio construction and risk (section overview)

Overview outcome, from the guide: construct and evaluate a portfolio whose forecasts, risk model, constraints, costs and tail measures are explicit and testable. Its checkpoint builds a long-only and a long-short portfolio from the same forecasts and risk model, reports ex-ante and realised risk, turnover, costs and the largest tail-loss contributors, and reruns with a shrunk covariance estimate. Its readings are `s7-meucci`, `alpha-grinold` and `s7-qrm`.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 15 October 2026 by systematic-investing architecture review (`notes/source-review-records.md`). This overview keeps the parts about the structure of a quant strategy and its forecasts: the black-box components and Narang's alpha taxonomy and strategy specification. Signal combination went to `equity-long-short-construction`, the production chain to `model-governance-controls`, and the execution and HFT material was merged into existing entries of `execution-trading-costs` and `hft-market-design`. The entries come from source checking against `s7-narang` (third edition, 2024), which is not one of the overview's readings; none of those has been read, and the checkpoint was not attempted.

Moved out by the content migration of 22 October 2026, with labels and content unchanged: to `asset-pricing`: `mech:systematic-risk-pricing`, `mod:return-generating-models`, `mod:capm-sml`, `meth:capm-regression`, `meth:required-return-on-equity`, `mod:multifactor-apt`, `def:factor-model-types`; to `financial-mathematics`: `def:return-measures`; to `high-dimensional-statistics`: `meth:portfolio-covariance-estimation`, `ev:correlation-matrix-noise`; to `probability-statistics`: `meth:extreme-value-tail-estimation`; to `regression-time-series`: `mod:garch-volatility-forecast`, `meth:volatility-forecast-loss`, `meth:structural-break-tests`; to `research-engineering-validation`: `def:quant-strategy-components`, `def:alpha-model-taxonomy`, `meth:alpha-strategy-specification`. Moved in: from `multi-asset-systematic-macro`: `def:investment-governance-allocation`, `meth:economic-balance-sheet-allocation`, `def:allocation-approaches-risk`, `meth:asset-class-factor-specification`, `meth:asset-only-allocation-mvo`, `meth:allocation-implementation-rebalancing`, `meth:allocation-robustness-liquidity-risk-budget`, `meth:liability-relative-allocation`, `meth:goals-based-allocation-heuristics`, `meth:allocation-constraints-taxes-revision`, `meth:tactical-shifts-behavioural-biases`.

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
- `ex:investment-planning-case`: a fictional surgeon's case: a stated tax basis, a required real after-tax return of 2.81 percent including the gains tax on a staged sale, three candidate allocations scored after tax, a funding gap resolved by changing the plan, IPS provisions, and an index-futures hedge of the retained concentrated stock tested against the loss limit.

In `behavioural-finance.tex` (topic `behavioral-finance`):

- `def:behavioural-biases`: beliefs and preferences (Barberis and Thaler, NBER w9222, secs. 3.1-3.2, pp. 12-21); Statman's cognitive and emotional shortcuts and errors (2019, chaps. 1, 3 and 4); effects on decisions and remedies, including Kahneman's decorrelation and premortem.
- `mech:biases-market-anomalies`: limits to arbitrage (pp. 3-6); size, reversal, value, momentum and drift with the BSV account (pp. 33-34 and 38-39); closed-end fund discounts (p. 44); home bias, naive diversification, excessive trading and the disposition effect (pp. 47-50).

In `risk-governance.tex` (topic `risk-management-framework`):

- `def:risk-management-framework`: definition, process, governance and ERM, risk tolerance, risk budgeting and limits (MIP chap. 9, pp. 579-584 and 634-635); Damodaran's risk hedging against risk management (2008, pp. 303-304).
- `meth:risk-identification-modification`: financial and non-financial risks (chap. 9, pp. 585-586, 596 and 623); Damodaran's alternatives for reducing exposure (chap. 10, pp. 331-335); the case's transition hedge, which shifts market risk but leaves the stock's specific risk.

In `active-management.tex` (topic `active-management-analysis`):

- `meth:active-return-information-ratio`: value added from active weights (MIP chap. 12, p. 743); ex post and ex ante IR, Table 5.1 and Table 5.3 (Grinold and Kahn, chap. 5, pp. 110-123); Bacon's tracking error and IR conventions (pp. 167-169); Sharpe's (1994) differential-return ratio; optimal active risk and SR_P^2 = SR_B^2 + IR^2, derived.
- `res:fundamental-law-active-management`: IR = IC sqrt(BR), assumptions, additivity and examples (chap. 6, pp. 147-162); the transfer coefficient (Grinold and Kahn 2020, pp. 23 and 27-29); a constrained five-stock check of IR_P = TC x IR_Q.
- `meth:active-risk-decomposition`: factor and specific active variance (chap. 3, pp. 76-77), active beta and residual risk (chap. 4, p. 90), marginal contributions (p. 67).

All partly checked 2026-10-18, draft. Examples in `notes/artefacts/investment-planning/investment-planning-checks.py` and `notes/artefacts/active-management-analysis/active-management-checks.py`; human review is outstanding. Coverage records are editorial, not study.

Written in the derivatives, portfolio and execution batch (2026-10-19):

In `market-risk-measurement.tex` (topic `market-risk-measurement`):

- `meth:portfolio-var-methods-decomposition`: parametric, historical and Monte Carlo VaR on one portfolio, ES and VaR decompositions (RMFI 6th ed.). Corrected 2026-10-19 (PR #25 pass): one zero-mean convention throughout; components sum to the reported 1,729,125.
- `meth:sensitivity-scenario-risk-measures`: beta, duration, convexity and option Greeks as risk measures; historical, hypothetical and reverse stress tests. Corrected 2026-10-19 (PR #25 pass): each stress and VaR comparison names the book it covers.
- `meth:market-risk-limits-capital`: risk budgets and limits, capital allocation with RAROC, and measures by institution type. Corrected 2026-10-19 (PR #25 pass): the stop-loss comparison names the book and convention (1.16 times VaR). Corrected 2026-10-21 (Batch L3): FRTB stated as the Basel standard (effective 1 January 2023) with its different EU, UK and US implementation.

In `derivative-overlays.tex` (topic `derivative-overlay-strategies`):

- `meth:forward-commitment-risk-overlays`: futures and swaps for duration, currency forwards and swaps, and equity futures, forwards and swaps for beta.
- `meth:volatility-derivative-applications`: variance and volatility swaps and VIX futures. Extended 2026-10-21 (Batch L4): a seasoned variance swap valued from observation-weighted realised and remaining variance (a labelled derivation), with the exact discrete remaining strike under GBM kept apart from the continuous approximation; checks in `notes/artefacts/derivative-overlays/seasoned-variance-swap-check.py`.
- `meth:derivative-overlay-allocation`: targeting equity and rate exposure together, rebalancing, and expectations inferred from derivative prices.
- `ex:endowment-derivative-overlay-case`: cash against futures for rebalancing and a tactical tilt (illustrative).

All partly checked 2026-10-19, draft. Examples in `notes/artefacts/market-risk-measurement/market-risk-checks.py` and `notes/artefacts/derivative-overlays/overlay-checks.py`; human review is outstanding. Coverage records are editorial, not study. `meth:var-es-estimation-methods` and `def:vix-variance-dividend-swaps` are linked, not repeated.

Written in the alternatives batch (2026-10-20):

In `hedge-fund-strategies.tex`:

- `def:hedge-fund-features`: features against other asset classes, vehicles (single funds, funds of funds, managed accounts, registered funds), data biases, performance, smoothing, and fee layers in a fund of funds.
- `meth:hedge-fund-strategy-classification`: classification and the equity-related, event-driven, relative value, opportunistic, specialist and multi-manager families, with merger, long/short and convertible arithmetic.
- `meth:hedge-fund-factor-exposures`: factor models with lagged factors for smoothing, and the Sharpe-ratio test for adding a fund to a 60/40 portfolio on reported and de-smoothed statistics.

In `alternatives-allocation.tex`:

- `def:alternatives-roles-opportunity-set`: roles of alternatives, alternatives against bonds as equity risk mitigators, and label-based against factor-based opportunity sets.
- `meth:alternatives-allocation-approaches`: considerations by type, suitability, allocation approaches, commitment pacing (Takahashi-Alexander and Luxenberg et al.), overcommitment, the denominator effect, liquidity reserves and monitoring.

Sources: Ang (2014) chaps. 13, 14 and 17; Jaeger (2008); Getmansky, Lo and Makarov (NBER WP 9571); Demaria et al. (2021); Luxenberg et al. (arXiv 2207.07767). Examples in `notes/artefacts/hedge-funds/hedge-fund-checks.py` and `notes/artefacts/alternatives-allocation/alternatives-allocation-checks.py`. Partly checked 2026-10-20, draft; human review outstanding. Coverage records are editorial, not study.

## Source verification after macro markets and pricing review

method validation (2026-10-17) (audit repairs and a source-review coverage; source verification and bounded tests, not study or human review): Queue: `ev:trend-following-evidence` resolved by merge into `def:alpha-model-taxonomy`'s pitfalls (Moskowitz, Ooi and Pedersen's abstract; Hurst, Ooi and Pedersen's 1880-2016 Exhibit 1: 7.3 percent net, 9.7 percent volatility, Sharpe 0.76, drawdowns up to 25 percent). The record is in `notes/source-review-records.md`, *method validation (2026-10-17)*.

empirical extensions (2026-10-17) (six audit repairs and a source-review coverage; source verification and bounded tests, not study or human review): `meth:residual-reversion-strategy` narrowed (Avellaneda and Lee and Gatev et al. merged into the alpha taxonomy); `ev:value-carry-premia` resolved (Koijen et al., Asness, Moskowitz and Pedersen and the QMJ paper merged into `def:alpha-model-taxonomy`). The record is in `notes/source-review-records.md`, *empirical extensions (2026-10-17)*.

derivatives and empirical validation (2026-10-17) (seven audit repairs, backlog reconciliation and a source-review coverage; source verification and bounded tests, not study or human review): the `def:alpha-model-taxonomy` and `meth:s-score-residual-trading` questions: Lo and MacKinlay's decomposition of contrarian profits, Avellaneda and Lee's s-score thresholds (chosen inside their backtest period) and Moskowitz, Ooi and Pedersen's position sizing merged into `def:alpha-model-taxonomy`; `meth:residual-reversion-strategy` narrowed. The record is in `notes/source-review-records.md`, *derivatives and empirical validation (2026-10-17)*.

## Entries created by the completion batch (2026-10-20)

Institutional investor portfolios, in `institutional-portfolios.tex`, checked by `notes/artefacts/institutional-portfolios/institutional-checks.py`: `def:institutional-investor-characteristics`, `meth:db-pension-risk`, `meth:institutional-ips-portfolios`, `meth:swf-risk-case`, `meth:endowment-liquidity-allocation`, `meth:institutional-esg-integration`. Sources: Ang (2014) chap. 1, 3 and 13, NBIM's GPFG pages (2026), the Santiago Principles, Lerner, Schoar and Wang (NBER WP 14341), Title 26 ss. 430 and 4942, IRS Notice 2021-48, New York NPC s. 553 and the GSIA review; existing bank, insurer, ESG and allocation entries are cross-referenced. Partly checked 2026-10-20, draft; human review outstanding. The records are in `notes/source-review-records.md`, *Completion batch, 20 October 2026*, and *Final audit correction pass, 20 October 2026* (pension funding law, New York endowment spending law, endowment liquidity).

PR #33 correction pass (2026-10-21): Harlow's 2026 statutory base nets the present value of installments on open bases (IRC 430(c)(3); 96.8m, not 400m) and the full minimum contribution is computed with its timing (151.91m at the valuation date); Elmsworth's pure spending rule is tested against its own quarterly history (peak 5.24 percent, not 5.25). See [record](../source-review-records.md#pr-33-correction-pass-21-october-2026).

## Related entries owned elsewhere

Cross-referenced, not owned here: `meth:alpha-signal-combination` (`equity-long-short-construction`), `meth:strategy-production-lifecycle` (`model-governance-controls`), and the merges into `def:order-exposure-decisions`, `def:portfolio-trading`, `def:automated-trading-architecture` (`execution-trading-costs`) and `def:hft-strategies` (`hft-market-design`); also `mod:factor-risk-model`, `meth:rule-based-position-sizing`, `mod:mean-variance-portfolio-optimisation` and `mod:portfolio-transaction-cost-function` (`portfolio-construction`), and `meth:hypothesis-driven-strategy-research` and `pit:parameter-overfitting` (`backtest-inference`).

## Specialist pathways

The guide's pathways for this section, in its order, with the existing material, partial treatment or content gap as recorded by the content migration of 22 October 2026 and its closeout review. A pathway with related material but no note has not been opened. A partial treatment names the existing entries that treat some of the pathway's subtopics, wherever they sit, and the subtopics with nothing written.

Printed as numbered sections of the chapter, under the guide pinned at `8302467` (`subsection_alignment_plan.md`): `portfolio-construction`, `risk-tail-systemic`, `performance-manager-evaluation`, `climate-sustainable`, `investment-policy-allocation`. A pathway without entries of its own is not printed; the related material and partial treatments named below are printed under the pathway or section that owns them.

- `portfolio-construction` (Portfolio construction, estimation error and risk models): pathway note [portfolio-construction.md](portfolio-construction.md), 13 entries listed, in `high-dimensional-statistics/covariance-estimation`, `portfolio-construction-risk/portfolio-construction-models`, `portfolio-construction-risk/risk-models`, `portfolio-construction-risk/transaction-cost-models`, `regression-time-series/volatility-forecasting`.
- `risk-tail-systemic` (Market risk, tail hedging and systemic stress): pathway note [risk-tail-systemic.md](risk-tail-systemic.md), 2 entries listed, in `portfolio-construction-risk/var-es-estimation`, `probability-statistics/extreme-values`.
- `performance-manager-evaluation` (Performance attribution and manager evaluation): pathway note [performance-manager-evaluation.md](performance-manager-evaluation.md), 19 entries listed, in `financial-mathematics/return-measurement`, `portfolio-construction-risk/manager-selection`, `portfolio-construction-risk/performance-attribution-appraisal`, `portfolio-construction-risk/performance-evaluation`, `portfolio-construction-risk/performance-standards`.
- `climate-sustainable` (Climate risk and sustainable portfolios): no pathway note; partial treatment in existing entries, not reviewed as complete: ESG approaches, climate risk and carbon-intensity against tracking-error trade-offs (`meth:institutional-esg-integration` in `portfolio-construction-risk/esg-integration`); climate scenarios in a sovereign fund's risk management (`meth:swf-risk-case` in `portfolio-risk-financing/institutional-portfolios`); evaluating issuers' ESG exposures (`meth:esg-exposure-evaluation` in `corporate-finance/corporate-ownership-governance`). Not written: evidence on climate-risk pricing; climate benchmark construction.
- `investment-policy-allocation` (Investment policy and strategic asset allocation, with alternatives and derivative overlays): added by the guide revision of 22 October 2026 (`8302467`); no pathway note; its entries are in `portfolio-construction-risk/investment-process-planning`, `portfolio-construction-risk/behavioural-finance`, `portfolio-construction-risk/strategic-asset-allocation`, `portfolio-construction-risk/derivative-overlays`, `portfolio-construction-risk/hedge-fund-strategies`, `portfolio-construction-risk/alternatives-allocation`.

## Entry backlog

- meth:residual-reversion-strategy: after-cost capacity and crowding evidence for residual reversal at scale; Khandani and Lo give the August 2007 paths only as figures. Avellaneda and Lee's s-score rule, Lo and MacKinlay's decomposition and Gatev et al. are in `def:alpha-model-taxonomy`. Home pathway `statistical-arbitrage`.

## What changed in my view or practice

## Questions carried forward

- Narang's eight classes and Exhibit 3.2 are a practitioner's framework; does `alpha-grinold`'s account of forecasts and information coefficients organise them differently?
