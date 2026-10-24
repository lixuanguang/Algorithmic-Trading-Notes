# Python migration

All maintained Python moves under `src/`: the package in `src/trading_notes/`, tests in `src/tests/`, local stubs in `src/typings/`. Numerical examples move from flat modules and `notes/artefacts/` scripts into one package per compendium subsection, `src/trading_notes/numerical/<subsection>/`, holding domain modules beside `*_checks.py` entrypoints that run as `python -m trading_notes.numerical.<subsection>.<name>_checks`.

## Checklist for each migrated example

- [ ] Run the old script and save its output as the baseline.
- [ ] Move the module with `git mv` into the subsection package; split domain classes and functions from check orchestration and reporting.
- [ ] Model records as pydantic models (`trading_notes.numerical.records.Record`, or `MutableRecord` for accumulators), not dataclasses or untyped dicts.
- [ ] Share `report.CheckReport`, `report.print_versions`, `tolerance.close`, `repository.repository_root` and `option_pricing.black_scholes.BlackScholes` where the arithmetic is identical; keep independent references independent.
- [ ] Keep formulas, units, seeds and tolerances; rerun and diff against the baseline, explaining any numerical difference.
- [ ] Keep the module docstring to one purpose sentence; sources, seeds and conventions go in the `main()` docstring. No dated corrections, audit notes or migration narrative in Python.
- [ ] Read files below a `--root` repository root (default: the working directory), never relative to the working directory alone.
- [ ] Retire the `notes/artefacts/` wrapper and remove it from `[tool.mypy] files` and `notes/artefacts/ruff.toml`.
- [ ] Register the module in `src/tests/numerical/test_checks.py` with its `passed` summary and, when a run takes more than about half a second, `stand_ins` for its expensive parts; port its unit tests.
- [ ] Rewrite live references in `compendium/`, `notes/pathways/` and `notes/coverage/` to the module name; leave dated review records as written.
- [ ] Pass `make lint format-check typecheck check-compendium check-coverage test examples`.

## How the examples are tested

- `test_each_example_runs_once`: one real, isolated run of each example's entrypoint (`python -I -W error`, the module through runpy as `python -m` runs it, or its forwarding script) from an empty temporary folder. It must exit 0 with its check-line count, no failed line and its success summary, leave the primed shared generators and NumPy settings unchanged, and write nothing.
- `test_failure_reaches_status_and_runs_repeat` (one pytest item per check): `main()` in process three times, clean, with one forced failure, clean again, with expensive parts replaced by `stand_ins`. The clean runs must pass and print the same thing; the failure must reach the summary and status 1.
- `test_entrypoints_exit_with_the_status_of_main`: each module's `if __name__ == "__main__":` block, and each forwarding script, executed with `main` answering 0 and then 1.
- `VerifiersRejectBrokenExamples`: the verifiers reject a `main` that always returns 1, one that always returns 0, and a report kept across runs.
- `make examples`: each unmigrated check script once, from an empty temporary folder.

## Infrastructure moves

| Old path | New path |
| --- | --- |
| `tools/check_compendium.py` | `src/trading_notes/cli/check_compendium.py` (`python -m trading_notes.cli.check_compendium`) |
| `tools/check_coverage.py` | `src/trading_notes/cli/check_coverage.py` (`python -m trading_notes.cli.check_coverage`) |
| `tests/` | `src/tests/` |
| `typings/` | `src/typings/` |
| (new) | `src/trading_notes/numerical/repository.py`: the `--root` option of examples that read repository files |

## Retired artefact scripts

The scripts below are gone; each row names the module that replaces it and the note that owns its entries. Dated review records (`notes/log.md`, `notes/source-review-records.md`, `notes/entry-evidence.json`) still cite the old paths; read them through this table.

| Old script | New module | Owning note |
| --- | --- | --- |
| `notes/artefacts/active-management-analysis/active-management-checks.py` | `trading_notes.numerical.active_management.active_management_checks` | `compendium/portfolio-construction-risk/active-management.tex` |
| `notes/artefacts/alternatives-allocation/alternatives-allocation-checks.py` | `trading_notes.numerical.alternatives_allocation.alternatives_allocation_checks` | `compendium/portfolio-construction-risk/alternatives-allocation.tex` |
| `notes/artefacts/corporate-finance/corporate-finance-checks.py` | `trading_notes.numerical.corporate_finance.corporate_finance_checks` | corporate-finance (six subsections; most entries in corporate-ownership-governance) |
| `notes/artefacts/corporate-finance/country-risk-premium-check.py` | `trading_notes.numerical.capital_structure_cost_of_capital.country_risk_premium_checks` | `compendium/corporate-finance/capital-structure-cost-of-capital.tex` |
| `notes/artefacts/derivative-overlays/overlay-checks.py` | `trading_notes.numerical.derivative_overlays.derivative_overlays_checks` | `compendium/portfolio-construction-risk/derivative-overlays.tex` |
| `notes/artefacts/derivative-overlays/seasoned-variance-swap-check.py` | `trading_notes.numerical.derivative_overlays.seasoned_variance_swap_checks` | `compendium/portfolio-construction-risk/derivative-overlays.tex` |
| `notes/artefacts/equity-portfolio-management/equity-portfolio-checks.py` | `trading_notes.numerical.equity_portfolio_management.equity_portfolio_management_checks` | `compendium/systematic-equities/equity-portfolio-management.tex` |
| `notes/artefacts/exotic-options/exotic-option-checks.py` | `trading_notes.numerical.exotic_options.exotic_options_checks` | `compendium/volatility-options/exotic-options.tex` |
| `notes/artefacts/exotic-options/lookback-option-check.py` | `trading_notes.numerical.exotic_options.lookback_options_checks` | `compendium/volatility-options/exotic-options.tex` |
| `notes/artefacts/financial-statement-analysis/cash-flow-linkage-check.py` | `trading_notes.numerical.cash_flow_analysis.cash_flow_linkage_checks` | `compendium/financial-statement-analysis/cash-flow-analysis.tex` |
| `notes/artefacts/financial-statement-analysis/statement-analysis-checks.py` | `trading_notes.numerical.company_case.statement_analysis_checks` | financial-statement-analysis/company-case (case used across the section) |
| `notes/artefacts/firms-market-structure/market-structure-checks.py` | `trading_notes.numerical.firms_market_structure.market_structure_checks` | `compendium/systematic-equities/firms-market-structure.tex` |
| `notes/artefacts/forward-swap-valuation/cross-currency-basis-check.py` | `trading_notes.numerical.forward_commitment_valuation.cross_currency_basis_checks` | `compendium/volatility-options/forward-commitment-valuation.tex` |
| `notes/artefacts/forward-swap-valuation/forward-swap-checks.py` | `trading_notes.numerical.forward_commitment_valuation.forward_swap_valuation_checks` | `compendium/volatility-options/forward-commitment-valuation.tex` |
| `notes/artefacts/hedge-funds/hedge-fund-checks.py` | `trading_notes.numerical.hedge_fund_strategies.hedge_funds_checks` | `compendium/portfolio-construction-risk/hedge-fund-strategies.tex` |
| `notes/artefacts/investment-planning/investment-planning-checks.py` | `trading_notes.numerical.investment_process_planning.investment_planning_checks` | `compendium/portfolio-construction-risk/investment-process-planning.tex` |
| `notes/artefacts/manager-selection/manager-selection-checks.py` | `trading_notes.numerical.manager_selection.manager_selection_checks` | `compendium/portfolio-construction-risk/manager-selection.tex` |
| `notes/artefacts/market-risk-measurement/market-risk-checks.py` | `trading_notes.numerical.market_risk_measurement.market_risk_measurement_checks` | `compendium/portfolio-construction-risk/market-risk-measurement.tex` |
| `notes/artefacts/option-pricing-models/option-model-checks.py` | `trading_notes.numerical.option_pricing.option_models_checks` | `compendium/volatility-options/option-pricing.tex` |
| `notes/artefacts/option-strategies/option-strategy-checks.py` | `trading_notes.numerical.option_strategies.option_strategies_checks` | `compendium/volatility-options/option-strategies.tex` |
| `notes/artefacts/option-valuation/dividend-tree-swaption-checks.py` | `trading_notes.numerical.option_valuation.dividend_tree_swaption_checks` | `compendium/volatility-options/option-valuation.tex` |
| `notes/artefacts/option-valuation/option-valuation-checks.py` | `trading_notes.numerical.option_valuation.option_valuation_checks` | `compendium/volatility-options/option-valuation.tex` |
| `notes/artefacts/option-valuation/transaction-cost-hedging-check.py` | `trading_notes.numerical.option_hedging.transaction_cost_hedging_checks` | `compendium/volatility-options/option-hedging.tex` |
| `notes/artefacts/option-valuation/volatility-mismatch-hedging-check.py` | `trading_notes.numerical.option_hedging.volatility_mismatch_hedging_checks` | `compendium/volatility-options/option-hedging.tex` |
| `notes/artefacts/performance-evaluation/performance-evaluation-checks.py` | `trading_notes.numerical.performance_attribution_appraisal.performance_evaluation_checks` | `compendium/portfolio-construction-risk/performance-attribution-appraisal.tex` |
| `notes/artefacts/performance-presentation-standards/gips-checks.py` | `trading_notes.numerical.performance_standards.gips_checks` | `compendium/portfolio-construction-risk/performance-standards.tex` |
| `notes/artefacts/portfolio-construction/black-litterman-check.py` | `trading_notes.numerical.portfolio_construction_models.black_litterman_checks` | `compendium/portfolio-construction-risk/portfolio-construction-models.tex` |
| `notes/artefacts/portfolio-construction/erc-check.py` | `trading_notes.numerical.portfolio_construction_models.equal_risk_contribution_checks` | `compendium/portfolio-construction-risk/portfolio-construction-models.tex` |
| `notes/artefacts/portfolio-construction/erc-sharpe-check.py` | `trading_notes.numerical.portfolio_construction_models.erc_sharpe_checks` | `compendium/portfolio-construction-risk/portfolio-construction-models.tex` |
| `notes/artefacts/portfolio-construction/kelly-check.py` | `trading_notes.numerical.portfolio_construction_models.kelly_growth_checks` | `compendium/portfolio-construction-risk/portfolio-construction-models.tex` |
| `notes/artefacts/portfolio-construction/mean-cvar-check.py` | `trading_notes.numerical.portfolio_construction_models.mean_cvar_checks` | `compendium/portfolio-construction-risk/portfolio-construction-models.tex` |
| `notes/artefacts/portfolio-risk-return/portfolio-choice-checks.py` | `trading_notes.numerical.portfolio_choice.portfolio_choice_checks` | `compendium/portfolio-construction-risk/portfolio-choice.tex` |
| `notes/artefacts/portfolio-risk-return/portfolio-moments-checks.py` | `trading_notes.numerical.portfolio_moments.portfolio_moments_checks` | `compendium/portfolio-construction-risk/portfolio-moments.tex` |
| `notes/artefacts/risk-parity-vol-targeting/risk-parity-checks.py` | `trading_notes.numerical.portfolio_construction_models.risk_parity_checks` | `compendium/portfolio-construction-risk/portfolio-construction-models.tex` |
| `notes/artefacts/risk-tail-systemic/es-discrete-check.py` | `trading_notes.numerical.var_es_estimation.expected_shortfall_checks` | `compendium/portfolio-construction-risk/var-es-estimation.tex` |
| `notes/artefacts/risk-tail-systemic/var-backtest-check.py` | `trading_notes.numerical.var_es_estimation.var_backtest_checks` | `compendium/portfolio-construction-risk/var-es-estimation.tex` |
| `notes/artefacts/strategic-asset-allocation/saa-checks.py` | `trading_notes.numerical.strategic_asset_allocation.strategic_asset_allocation_checks` | `compendium/portfolio-construction-risk/strategic-asset-allocation.tex` |
| `notes/artefacts/systematic-equities/equity-fcf-ri-private-checks.py` | `trading_notes.numerical.systematic_equities.equity_fcf_ri_private_checks` | systematic-equities (free-cash-flow, residual-income and private-company valuation) |
| `notes/artefacts/systematic-equities/equity-valuation-checks.py` | `trading_notes.numerical.systematic_equities.equity_valuation_checks` | systematic-equities (market multiples, valuation foundations, dividend discount models) |
| `notes/artefacts/volatility-options/bsm-svi-checks.py` | `trading_notes.numerical.option_pricing.bsm_svi_checks` | `compendium/volatility-options/option-pricing.tex` |

`corporate_finance` and `systematic_equities` are named after sections, not subsections, because each of their check scripts spans several subsections of one shared case; their domain code lives in subsection packages (`capital_structure_cost_of_capital`, `company_case`).

## Former flat modules

| Old module | New modules |
| --- | --- |
| `active_management` | `active_management.fundamental_law`, `.active_management_checks` |
| `alternatives_allocation` | `alternatives_allocation.commitment_pacing`, `.alternatives_allocation_checks` |
| `black_litterman`, `equal_risk_contribution`, `erc_sharpe`, `kelly_growth`, `mean_cvar`, `risk_parity` | `portfolio_construction_models.black_litterman`, `.kelly_growth`, `.mean_cvar`, `.risk_contributions` and one `*_checks` module each |
| `bsm_svi`, `option_models` | `option_pricing.black_scholes`, `.svi`, `.stochastic_models`, `.bsm_svi_checks`, `.option_models_checks` |
| `cash_flow_linkage` | `cash_flow_analysis.statement_linkage`, `.cash_flow_linkage_checks` |
| `country_risk_premium` | `capital_structure_cost_of_capital.cost_of_capital`, `.country_risk`, `.country_risk_premium_checks` |
| `cross_currency_basis`, `forward_swap_valuation` | `forward_commitment_valuation.cross_currency`, `.swap_valuation` and their `*_checks` |
| `derivative_overlays`, `seasoned_variance_swap` | `derivative_overlays.variance_swap` and their `*_checks` |
| `dividend_tree_swaption`, `option_valuation` | `option_valuation.dividend_tree`, `.delta_hedging` and their `*_checks` |
| `equity_portfolio_management` | `equity_portfolio_management.equity_universe`, `.equity_portfolio_management_checks` |
| `exotic_options`, `lookback_options` | `exotic_options.exotic_pricing`, `.lookback` and their `*_checks` |
| `expected_shortfall`, `var_backtest` | `var_es_estimation.expected_shortfall`, `.var_backtest` and their `*_checks` |
| `gips` | `performance_standards.composite`, `.gips_checks` |
| `hedge_funds` | `hedge_fund_strategies.return_smoothing`, `.hedge_funds_checks` |
| `investment_planning` | `investment_process_planning.retirement_plan`, `.investment_planning_checks` |
| `manager_selection` | `manager_selection.manager_evaluation`, `.manager_selection_checks` |
| `market_risk_measurement` | `market_risk_measurement.market_risk`, `.market_risk_measurement_checks` |
| `market_structure` | `firms_market_structure.firm_costs`, `.market_structure_checks` |
| `option_strategies` | `option_strategies.option_strategies_checks` |
| `performance_evaluation` | `performance_attribution_appraisal.performance_measures`, `.performance_evaluation_checks` |
| `portfolio_moments` | `portfolio_moments.scenario_moments`, `.portfolio_moments_checks` |
| `statement_analysis` (`harbour_namespace()`) | `company_case.harbour` (`HarbourCase`), `.statement_analysis_checks`, `corporate_finance.corporate_finance_checks`, `systematic_equities.equity_valuation_checks`, `systematic_equities.equity_fcf_ri_private_checks` |
| `strategic_asset_allocation` | `strategic_asset_allocation.allocation`, `.strategic_asset_allocation_checks` |
| `transaction_cost_hedging`, `volatility_mismatch_hedging` | `option_hedging.leland_hedging`, `.volatility_mismatch` and their `*_checks` |
| (script only) `portfolio-choice-checks.py` | `portfolio_choice.frontier`, `.history`, `.portfolio_choice_checks` |

## Inventory of Python outside `src/`

Counted on 2026-10-24 with `git ls-files -co --exclude-standard '*.py' '*.pyi'`: 121 files outside `src/` (248 inside it).

| Kind | Files | Disposition |
| --- | --- | --- |
| Forwarding wrappers in `notes/artefacts/` (`from trading_notes.numerical ... import main`) | 77 | Retired one by one as their 77 flat modules move into subsection packages. |
| Unmigrated check implementations in `notes/artefacts/` (run by `make examples`) | 13 | Migrate into subsection packages. |
| Research and data scripts in `notes/artefacts/`: extracts, empirical reruns, exchange snapshots | 22 | Migrate into `src/trading_notes/research/<topic>/` with `--root` data paths; the data and outputs they read and write stay in `notes/artefacts/`. Scripts that need network access or the `empirical` dependency group keep that requirement and are not run by `make check`. |
| Historical runs in `notes/artefacts/**/superseded-*/` | 8 | Archived, not maintained: kept byte for byte as the code that produced the superseded results cited by `notes/source-review-records.md`, excluded from lint and type checks, never executed. To be removed from the working tree in one batch once those records cite them as `git show <commit>:<path>`; their data files stay. |
| `guide/refresh_views.py` | 1 | Migrate into `src/trading_notes/guide/refresh_views.py`, run as `python -m trading_notes.guide.refresh_views --root guide`, with the vendored guide keeping only its data and outputs; `guide/README.md` and `subsection_alignment_plan.md` then point to the module. |

Inside `src/trading_notes/numerical/`: 77 flat example modules still to move into subsection packages, and six support modules (`__init__`, `newey_west`, `records`, `report`, `repository`, `tolerance`).

## Remaining work

- 77 flat example modules and their 77 wrappers, the 13 unmigrated check scripts, the 22 research and data scripts and `guide/refresh_views.py`: 113 implementations.
- The eight historical runs: rewrite their citations, then remove them from the working tree.

## Next batch

Statistics, backtest inference, rates, funding, credit and execution: the 35 flat modules `backtest_design`, `drawdown_resampling`, `multiple_testing`, `sharpe_statistics`, `sharpe_conditions`, `sharpe_zero`, `statistics_probability`, `correlation_independence`, `inference_simulation`, `linear_regression`, `extreme_value`, `stochastic_calculus`, `bond_valuation_risk`, `fixed_income_portfolio`, `rate_tree_embedded_options`, `fra_settlement`, `multicurve`, `yield_shift`, `funding_repo`, `margin_purchase`, `credit_cds_securitisation`, `credit_portfolios`, `counterparty_capital`, `counterparty_xva`, `default_correlation`, `cme_allocation`, `commodity_latency`, `contract_statistics`, `dealer_queue_information`, `liquidity_market_design`, `market_estimators_rules`, `lob_models`, `lob_model_derivations`, `order_flow`, `trade_execution`, and the scripts `backtest-inference/scenario-simulation-checks.py`, `linear-regression/multiple-regression-checks.py`, `time-series-models/time-series-checks.py`, `short-rate-models/short-rate-model-checks.py`, `term-structure-dynamics/term-structure-checks.py` (40 implementations).
