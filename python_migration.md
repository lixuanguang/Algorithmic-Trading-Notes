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
| `notes/artefacts/backtest-inference/backtest-design-checks.py` | `trading_notes.numerical.backtest_evaluation.backtest_design_checks` | `compendium/research-engineering-validation/backtest-evaluation.tex` |
| `notes/artefacts/backtest-inference/drawdown-resampling-checks.py` | `trading_notes.numerical.backtest_evaluation.drawdown_resampling_checks` | `compendium/research-engineering-validation/backtest-evaluation.tex` |
| `notes/artefacts/backtest-inference/multiple-testing-checks.py` | `trading_notes.numerical.backtest_evaluation.multiple_testing_checks` | `compendium/research-engineering-validation/backtest-evaluation.tex` |
| `notes/artefacts/backtest-inference/scenario-simulation-checks.py` | `trading_notes.numerical.scenario_simulation.scenario_simulation_checks` | `compendium/research-engineering-validation/scenario-simulation.tex` |
| `notes/artefacts/backtest-inference/sharpe-checks.py` | `trading_notes.numerical.backtest_evaluation.sharpe_statistics_checks` | `compendium/research-engineering-validation/backtest-evaluation.tex` |
| `notes/artefacts/backtest-inference/sharpe-conditions-checks.py` | `trading_notes.numerical.backtest_evaluation.sharpe_conditions_checks` | `compendium/research-engineering-validation/backtest-evaluation.tex` |
| `notes/artefacts/backtest-inference/sharpe-zero-check.py` | `trading_notes.numerical.backtest_evaluation.sharpe_zero_checks` | `compendium/research-engineering-validation/backtest-evaluation.tex` |
| `notes/artefacts/bond-valuation-risk/bond-valuation-checks.py` | `trading_notes.numerical.bond_pricing_yields.bond_valuation_checks` | `compendium/rates-credit-mortgages/bond-pricing-yields.tex` (parts 1-5 and 10); parts 6-9 serve `interest-rate-risk.tex` |
| `notes/artefacts/corporate-credit-capital/credit-cds-securitisation-checks.py` | `trading_notes.numerical.credit_risk_analysis.credit_cds_securitisation_checks` | `compendium/corporate-credit-capital/credit-risk-analysis.tex`; also cited by `credit-default-swaps.tex`, `government-bond-markets/sovereign-credit.tex` and `securitised-structured-credit/securitisation.tex` |
| `notes/artefacts/corporate-finance/corporate-finance-checks.py` | `trading_notes.numerical.corporate_finance.corporate_finance_checks` | corporate-finance (six subsections; most entries in corporate-ownership-governance) |
| `notes/artefacts/corporate-finance/country-risk-premium-check.py` | `trading_notes.numerical.capital_structure_cost_of_capital.country_risk_premium_checks` | `compendium/corporate-finance/capital-structure-cost-of-capital.tex` |
| `notes/artefacts/counterparty-xva/counterparty-capital-check.py` | `trading_notes.numerical.counterparty_xva.counterparty_capital_checks` | `compendium/portfolio-risk-financing/counterparty-xva.tex` |
| `notes/artefacts/counterparty-xva/counterparty-xva-checks.py` | `trading_notes.numerical.counterparty_xva.counterparty_xva_checks` | `compendium/portfolio-risk-financing/counterparty-xva.tex` |
| `notes/artefacts/credit-portfolios/credit-portfolio-checks.py` | `trading_notes.numerical.credit_portfolio_management.credit_portfolios_checks` | `compendium/corporate-credit-capital/credit-portfolio-management.tex` |
| `notes/artefacts/default-correlation/default-correlation-checks.py` | `trading_notes.numerical.default_correlation.default_correlation_checks` | `compendium/securitised-structured-credit/default-correlation.tex` |
| `notes/artefacts/derivative-overlays/overlay-checks.py` | `trading_notes.numerical.derivative_overlays.derivative_overlays_checks` | `compendium/portfolio-construction-risk/derivative-overlays.tex` |
| `notes/artefacts/derivative-overlays/seasoned-variance-swap-check.py` | `trading_notes.numerical.derivative_overlays.seasoned_variance_swap_checks` | `compendium/portfolio-construction-risk/derivative-overlays.tex` |
| `notes/artefacts/descriptive-probability/statistics-probability-checks.py` | `trading_notes.numerical.descriptive_statistics.statistics_probability_checks` | `compendium/probability-statistics/descriptive-statistics.tex` |
| `notes/artefacts/equity-portfolio-management/equity-portfolio-checks.py` | `trading_notes.numerical.equity_portfolio_management.equity_portfolio_management_checks` | `compendium/systematic-equities/equity-portfolio-management.tex` |
| `notes/artefacts/execution-market-making/cme-allocation-checks.py` | `trading_notes.numerical.order_books.cme_allocation_checks` | `compendium/execution-market-making/order-books.tex` |
| `notes/artefacts/execution-market-making/commodity-production-latency-checks.py` | `trading_notes.numerical.order_books.commodity_latency_checks` | `compendium/execution-market-making/order-books.tex` (by content; no live note cites it) |
| `notes/artefacts/execution-market-making/contract-specifications-statistics-checks.py` | `trading_notes.numerical.futures_execution.contract_statistics_checks` | `compendium/execution-trading-costs/futures-execution.tex`; also cited by `notes/pathways/macro-announcements-policy.md` |
| `notes/artefacts/execution-market-making/dealer-queue-information-checks.py` | `trading_notes.numerical.high_frequency_trading.dealer_queue_information_checks` | `compendium/execution-market-making/high-frequency-trading.tex` |
| `notes/artefacts/execution-market-making/liquidity-market-design-checks.py` | `trading_notes.numerical.market_organisation.liquidity_market_design_checks` | `compendium/execution-market-making/market-organisation.tex` |
| `notes/artefacts/execution-market-making/market-estimators-rules-checks.py` | `trading_notes.numerical.order_flow_statistics.market_estimators_rules_checks` | `compendium/execution-market-making/order-flow-statistics.tex` |
| `notes/artefacts/exotic-options/exotic-option-checks.py` | `trading_notes.numerical.exotic_options.exotic_options_checks` | `compendium/volatility-options/exotic-options.tex` |
| `notes/artefacts/exotic-options/lookback-option-check.py` | `trading_notes.numerical.exotic_options.lookback_options_checks` | `compendium/volatility-options/exotic-options.tex` |
| `notes/artefacts/extreme-value/extreme-value-checks.py` | `trading_notes.numerical.extreme_values.extreme_value_checks` | `compendium/probability-statistics/extreme-values.tex` |
| `notes/artefacts/financial-statement-analysis/cash-flow-linkage-check.py` | `trading_notes.numerical.cash_flow_analysis.cash_flow_linkage_checks` | `compendium/financial-statement-analysis/cash-flow-analysis.tex` |
| `notes/artefacts/financial-statement-analysis/statement-analysis-checks.py` | `trading_notes.numerical.company_case.statement_analysis_checks` | financial-statement-analysis/company-case (case used across the section) |
| `notes/artefacts/firms-market-structure/market-structure-checks.py` | `trading_notes.numerical.firms_market_structure.market_structure_checks` | `compendium/systematic-equities/firms-market-structure.tex` |
| `notes/artefacts/fixed-income-portfolio/fixed-income-portfolio-checks.py` | `trading_notes.numerical.fixed_income_portfolio_management.fixed_income_portfolio_checks` | `compendium/rates-credit-mortgages/fixed-income-portfolio-management.tex`; also cited by `portfolio-risk-financing/liability-matching.tex` |
| `notes/artefacts/forward-swap-valuation/cross-currency-basis-check.py` | `trading_notes.numerical.forward_commitment_valuation.cross_currency_basis_checks` | `compendium/volatility-options/forward-commitment-valuation.tex` |
| `notes/artefacts/forward-swap-valuation/forward-swap-checks.py` | `trading_notes.numerical.forward_commitment_valuation.forward_swap_valuation_checks` | `compendium/volatility-options/forward-commitment-valuation.tex` |
| `notes/artefacts/hedge-funds/hedge-fund-checks.py` | `trading_notes.numerical.hedge_fund_strategies.hedge_funds_checks` | `compendium/portfolio-construction-risk/hedge-fund-strategies.tex` |
| `notes/artefacts/inference-simulation/correlation-independence-checks.py` | `trading_notes.numerical.statistical_inference.correlation_independence_checks` | `compendium/probability-statistics/statistical-inference.tex` |
| `notes/artefacts/inference-simulation/inference-simulation-checks.py` | `trading_notes.numerical.statistical_inference.inference_simulation_checks` | `compendium/probability-statistics/statistical-inference.tex` |
| `notes/artefacts/investment-planning/investment-planning-checks.py` | `trading_notes.numerical.investment_process_planning.investment_planning_checks` | `compendium/portfolio-construction-risk/investment-process-planning.tex` |
| `notes/artefacts/linear-regression/multiple-regression-checks.py` | `trading_notes.numerical.multiple_regression.multiple_regression_checks` | `compendium/regression-time-series/multiple-regression.tex` |
| `notes/artefacts/linear-regression/regression-checks.py` | `trading_notes.numerical.regression.linear_regression_checks` | `compendium/regression-time-series/regression.tex` |
| `notes/artefacts/manager-selection/manager-selection-checks.py` | `trading_notes.numerical.manager_selection.manager_selection_checks` | `compendium/portfolio-construction-risk/manager-selection.tex` |
| `notes/artefacts/market-making-lob/model-checks.py` | `trading_notes.numerical.market_making_models.lob_models_checks` | `compendium/execution-market-making/market-making-models.tex` |
| `notes/artefacts/market-making-lob/model-derivations-checks.py` | `trading_notes.numerical.market_making_models.lob_model_derivations_checks` | `compendium/execution-market-making/market-making-models.tex` |
| `notes/artefacts/market-risk-measurement/market-risk-checks.py` | `trading_notes.numerical.market_risk_measurement.market_risk_measurement_checks` | `compendium/portfolio-construction-risk/market-risk-measurement.tex` |
| `notes/artefacts/market-simulation/order-flow-checks.py` | `trading_notes.numerical.order_flow_statistics.order_flow_checks` | `compendium/execution-market-making/order-flow-statistics.tex` |
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
| `notes/artefacts/rate-tree-embedded-options/rate-tree-checks.py` | `trading_notes.numerical.embedded_option_bonds.rate_tree_checks` | `compendium/rates-credit-mortgages/embedded-option-bonds.tex`; also cited by `arbitrage-free-valuation.tex` and `volatility-options/convertible-bonds.tex` |
| `notes/artefacts/rates-credit-mortgages/fra-settlement-check.py` | `trading_notes.numerical.rate_swaps_clearing.fra_settlement_checks` | `compendium/rates-credit-mortgages/rate-swaps-clearing.tex` |
| `notes/artefacts/rates-credit-mortgages/multicurve-check.py` | `trading_notes.numerical.rate_swaps_clearing.multicurve_checks` | `compendium/rates-credit-mortgages/rate-swaps-clearing.tex` |
| `notes/artefacts/rates-credit-mortgages/yield-shift-check.py` | `trading_notes.numerical.interest_rates.yield_shift_checks` | `compendium/rates-credit-mortgages/interest-rates.tex` |
| `notes/artefacts/risk-parity-vol-targeting/risk-parity-checks.py` | `trading_notes.numerical.portfolio_construction_models.risk_parity_checks` | `compendium/portfolio-construction-risk/portfolio-construction-models.tex` |
| `notes/artefacts/risk-tail-systemic/es-discrete-check.py` | `trading_notes.numerical.var_es_estimation.expected_shortfall_checks` | `compendium/portfolio-construction-risk/var-es-estimation.tex` |
| `notes/artefacts/risk-tail-systemic/var-backtest-check.py` | `trading_notes.numerical.var_es_estimation.var_backtest_checks` | `compendium/portfolio-construction-risk/var-es-estimation.tex` |
| `notes/artefacts/short-rate-models/short-rate-model-checks.py` | `trading_notes.numerical.arbitrage_free_valuation.short_rate_model_checks` | `compendium/rates-credit-mortgages/arbitrage-free-valuation.tex` |
| `notes/artefacts/short-term-funding/funding-repo-checks.py` | `trading_notes.numerical.money_markets.funding_repo_checks` | `compendium/portfolio-risk-financing/money-markets.tex` |
| `notes/artefacts/short-term-funding/margin-purchase-check.py` | `trading_notes.numerical.securities_lending.margin_purchase_checks` | `compendium/portfolio-risk-financing/securities-lending.tex` |
| `notes/artefacts/stochastic-calculus/stochastic-calculus-checks.py` | `trading_notes.numerical.stochastic_calculus.stochastic_calculus_checks` | `compendium/stochastic-processes-calculus/stochastic-calculus.tex` |
| `notes/artefacts/strategic-asset-allocation/saa-checks.py` | `trading_notes.numerical.strategic_asset_allocation.strategic_asset_allocation_checks` | `compendium/portfolio-construction-risk/strategic-asset-allocation.tex` |
| `notes/artefacts/systematic-equities/equity-fcf-ri-private-checks.py` | `trading_notes.numerical.systematic_equities.equity_fcf_ri_private_checks` | systematic-equities (free-cash-flow, residual-income and private-company valuation) |
| `notes/artefacts/systematic-equities/equity-valuation-checks.py` | `trading_notes.numerical.systematic_equities.equity_valuation_checks` | systematic-equities (market multiples, valuation foundations, dividend discount models) |
| `notes/artefacts/term-structure-dynamics/term-structure-checks.py` | `trading_notes.numerical.term_structure_returns.term_structure_checks` | `compendium/rates-credit-mortgages/term-structure-returns.tex` |
| `notes/artefacts/time-series-models/time-series-checks.py` | `trading_notes.numerical.time_series_models.time_series_checks` | `compendium/regression-time-series/time-series-models.tex` |
| `notes/artefacts/trade-execution/trade-execution-checks.py` | `trading_notes.numerical.trade_strategy_governance.trade_execution_checks` | `compendium/execution-trading-costs/trade-strategy-governance.tex` |
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
| `backtest_design`, `drawdown_resampling`, `multiple_testing`, `sharpe_statistics`, `sharpe_conditions`, `sharpe_zero` | `backtest_evaluation.backtest_book`, `.drawdown_bootstrap`, `.familywise_tests`, `.sharpe_inference` and one `*_checks` module each |
| `bond_valuation_risk` | `bond_pricing_yields.fixed_rate_bonds`, `.sofr_notes`, `.bond_valuation_checks` |
| `cme_allocation`, `commodity_latency` | `order_books.matching_allocation`, `.latency_calibration` and their `*_checks` |
| `contract_statistics` | `futures_execution.contract_statistics_checks` |
| `correlation_independence`, `inference_simulation` | `statistical_inference.correlation_tests`, `.sample_inference` and their `*_checks` |
| `counterparty_capital`, `counterparty_xva` | `counterparty_xva.regulatory_capital`, `.swap_exposure`, `.tree_cva` and their `*_checks`; the GSW curve and Hull-White model in `arbitrage_free_valuation.short_rate_models` |
| `credit_cds_securitisation` | `credit_risk_analysis.credit_instruments`, `.credit_cds_securitisation_checks` |
| `credit_portfolios` | `credit_portfolio_management.structured_claims`, `.credit_portfolios_checks`; Vasicek's model from `default_correlation.factor_model` |
| `dealer_queue_information` | `high_frequency_trading.speed_race`, `.dealer_queue_information_checks` |
| `default_correlation` | `default_correlation.factor_model`, `.tranche_pricing`, `.default_correlation_checks` |
| `extreme_value` | `extreme_values.tail_estimation`, `.extreme_value_checks` |
| `fixed_income_portfolio` | `fixed_income_portfolio_management.curve_exposures`, `.fixed_income_portfolio_checks` |
| `fra_settlement`, `multicurve` | `rate_swaps_clearing.fra_valuation` and their `*_checks` |
| `funding_repo` | `money_markets.money_market_instruments`, `.funding_repo_checks` |
| `linear_regression` | `regression.simple_regression`, `.linear_regression_checks` |
| `liquidity_market_design` | `market_organisation.liquidity_models`, `.liquidity_market_design_checks` |
| `lob_models`, `lob_model_derivations` | `market_making_models.inventory_models`, `.microstructure_models` and their `*_checks` |
| `margin_purchase` | `securities_lending.margin_accounts`, `.margin_purchase_checks` |
| `market_estimators_rules`, `order_flow` | `order_flow_statistics.point_processes`, `.trade_classification`, `.covariance_estimators` and their `*_checks` |
| `rate_tree_embedded_options` | `embedded_option_bonds.binomial_tree`, `.rate_tree_checks` |
| `statistics_probability` | `descriptive_statistics.return_statistics`, `.statistics_probability_checks` |
| `stochastic_calculus` | `stochastic_calculus.geometric_brownian_motion`, `.stochastic_calculus_checks` |
| `trade_execution` | `trade_strategy_governance.almgren_chriss`, `.trade_execution_checks` |
| `yield_shift` | `interest_rates.continuous_cash_flows`, `.yield_shift_checks` |
| (script only) `scenario-simulation-checks.py` | `scenario_simulation.return_simulation`, `.scenario_simulation_checks`; the history reader in `portfolio_choice.history` |
| (script only) `multiple-regression-checks.py` | `multiple_regression.least_squares`, `.multiple_regression_checks` |
| (script only) `time-series-checks.py` | `time_series_models.forecasting_models`, `.time_series_checks` |
| (script only) `short-rate-model-checks.py` | `arbitrage_free_valuation.short_rate_models`, `.short_rate_model_checks` |
| (script only) `term-structure-checks.py` | `term_structure_returns.curve_bootstrap`, `.term_structure_checks` |
| (new) | `us_calendar`: weekday arithmetic and federal holidays shared by the order-book, futures and SOFR examples |

## Inventory of Python outside `src/`

Counted on 2026-10-24 with `git ls-files -co --exclude-standard '*.py' '*.pyi'`: 81 files outside `src/` (331 inside it).

| Kind | Files | Disposition |
| --- | --- | --- |
| Forwarding wrappers in `notes/artefacts/` (`from trading_notes.numerical ... import main`) | 42 | Retired one by one as their 42 flat modules move into subsection packages. |
| Unmigrated check implementations in `notes/artefacts/` (run by `make examples`) | 8 | Migrate into subsection packages. |
| Research and data scripts in `notes/artefacts/`: extracts, empirical reruns, exchange snapshots | 22 | Migrate into `src/trading_notes/research/<topic>/` with `--root` data paths; the data and outputs they read and write stay in `notes/artefacts/`. Scripts that need network access or the `empirical` dependency group keep that requirement and are not run by `make check`. |
| Historical runs in `notes/artefacts/**/superseded-*/` | 8 | Archived, not maintained: kept byte for byte as the code that produced the superseded results cited by `notes/source-review-records.md`, excluded from lint and type checks, never executed. To be removed from the working tree in one batch once those records cite them as `git show <commit>:<path>`; their data files stay. |
| `guide/refresh_views.py` | 1 | Migrate into `src/trading_notes/guide/refresh_views.py`, run as `python -m trading_notes.guide.refresh_views --root guide`, with the vendored guide keeping only its data and outputs; `guide/README.md` and `subsection_alignment_plan.md` then point to the module. |

Inside `src/trading_notes/numerical/`: 42 flat example modules still to move into subsection packages, and seven support modules (`__init__`, `newey_west`, `records`, `report`, `repository`, `tolerance`, `us_calendar`).

## Completed batches

| Batch | Implementations | Evidence |
| --- | --- | --- |
| Statistics, backtest inference, rates, funding, credit and execution | 40: the 35 flat modules and 5 scripts in the tables above, from `backtest-design-checks.py` to `trade-execution-checks.py` | Each module's output diffed against its pre-migration run: identical except six intended wording changes that removed history text: the backtest-design "earlier rule/peak" labels, the statistics header "corrections of 2026-10-18" (now "counterexamples"), the extreme-value "freeze reproduction" line, the liquidity "market design review" sampler (now "naive sampler"), the municipal-discount header's "(correction of 2026-10-19)" and the short-rate parameters "written in this script" (now "in the module"). Class-based migration completed by the audit repairs below. After them `make source-check` passed on 2026-10-24: lock check, lint, format, strict mypy (352 files), compendium and coverage checkers with 0 problems, 418 tests and 944 subtests, `make examples` 8 check scripts; `make verify-outlines` 0 problems. |

### Audit repairs of the statistics-to-execution batch

An audit of that batch found that moving a module and adding records had not finished the class-based migration in five domain modules, and found three contract defects. The repairs:

| Finding | Repair | Validation |
| --- | --- | --- |
| `PrincipalComponents.of` signed three components by default and raised IndexError on a matrix of two maturities | `signed=None` signs every available component; an explicit count outside 0..maturities, or input that is not a matrix of at least two dates, raises ValueError | `test_rates_and_order_flow_models.PrincipalComponentCounts`: two maturities, one maturity, five maturities (leading three equal to `signed=3`), invalid counts and shapes; the term-structure example's output is unchanged |
| `HullWhite.path_discount` declared an array but returned `np.float64` for a scalar integral; `tranche_payoff` had the same mismatch | Overloads: a scalar gives `float`, an array gives an array of its shape; the redundant `float(...)` calls in their consumers are gone | `HullWhiteDiscount`: runtime types and element-by-element equality of the scalar and array results |
| `counterparty_xva.tree_cva`, `embedded_option_bonds.binomial_tree`, `order_books.matching_allocation`, `order_flow_statistics.covariance_estimators`, `order_flow_statistics.trade_classification` were functions only | `ShortRateTree` (calibration, state prices, bond, swap and floater values and CVAs) with `DefaultRisk` (hazard and recovery); `LognormalTree` (calibration, node rates, backward induction with options and coupon functions); `RestingOrders` (Pro Rata, Leveling, FIFO; `split_fifo` stays a pure helper); `ObservedPrices` (previous-tick sampling, Hayashi-Yoshida; `refresh_times` stays a function across series); `Quote` (Lee-Ready, EMO, CLNV with strict Decimal prices; `tick_test` stays a function of the trade history). The two binomial trees stay independent implementations | `RateTrees`, `TradeSigning` (float prices rejected), `AsynchronousCovariance`, the rewritten `CmeAllocation` tests; outputs of the five consuming examples identical |
| Identical `check(failed, name, cond)` helpers in three modules and `section`/`head` helpers in five | `report.require` and `report.section`, used by `dealer_queue_information_checks`, `liquidity_market_design_checks`, `order_flow_checks`, `market_estimators_rules_checks` and `contract_statistics_checks`; each keeps its own end-of-run output | `FailureOnlyReporting`; outputs identical |

One printed wording changed: the counterparty-xva discount-factor check's detail says "opposite sign" instead of "previous sign". Every other example's output is byte-identical to its run before the repairs. `regulatory_capital` (one class, seven functions of the SA-CCR and capital formulas) was not part of the audit findings and is left as it is.

## Remaining work

- 42 flat example modules and their 42 wrappers, the 8 unmigrated check scripts, the 22 research and data scripts and `guide/refresh_views.py`: 73 implementations.
- Twelve of the 42 flat modules still define dataclasses (`bitemporal`, `covariance_shrinkage`, `digital_assets`, `economic_growth`, `filing_timestamps`, `garch_ewma`, `index_construction`, `linear_projection`, `monte_carlo_greeks`, `order_reconciliation`, `private_capital`, `time_value_returns`); they become pydantic records as they migrate. The structural checkers (`structure/compendium.py`, `compendium_check.py`, `coverage_check.py`) also use dataclasses and are outside the numerical migration.
- The eight historical runs: rewrite their citations, then remove them from the working tree.

## Next batch

Macro, FX, commodities, return predictability, covariance and machine learning, wealth and market structure: the 8 unmigrated check scripts `commodity-storage-curves/energy-checks.py`, `fx-determination-forecasting/fx-checks.py`, `macro-regimes-stock-bond/regime-checks.py`, `multi-asset-systematic-macro/carry-market-statistics-checks.py`, `multi-asset-systematic-macro/convexity-curve-signals-checks.py`, `return-predictability/conditional-predictive-ability-checks.py`, `return-predictability/forecast-combination-scoring-checks.py`, `return-predictability/return-predictability-checks.py`, and the 32 flat modules `fx_mechanics`, `fx_panel_inference`, `currency_management`, `macro_policy_trade`, `macro_pricing_risk`, `macro_valuation`, `economic_growth`, `capital_market_expectations`, `commodity_returns`, `real_assets`, `forecast_scaling`, `asset_pricing_factor_models`, `covariance_shrinkage`, `covariance_volatility`, `garch_ewma`, `linear_projection`, `purged_cv`, `afml`, `financial_labels`, `financial_ml_methods`, `cartea_jaimungal`, `institutional_portfolios`, `private_capital`, `private_wealth`, `concentrated_position`, `index_construction`, `etf_mechanics`, `digital_assets`, `amm_pool`, `perpetual_funding`, `synthetic_short`, `monte_carlo_greeks` (40 implementations). The batch after it: the ten flat modules left (`bitemporal`, `filing_deadlines`, `filing_timestamps`, `intercorporate_fx_institutions`, `margin_spiral`, `negative_hedge_ratio`, `numerical_pricing`, `order_reconciliation`, `order_routing_fragmentation`, `time_value_returns`), the 22 research scripts and `guide/refresh_views.py`.
