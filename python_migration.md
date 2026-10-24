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
- `make examples`: each unmigrated check script once, from an empty temporary folder. None remain after the macro-to-wealth batch; the target says so explicitly and still runs any such script that is added.

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
| `notes/artefacts/asset-pricing-factor-models/asset-pricing-checks.py` | `trading_notes.numerical.asset_pricing_models.asset_pricing_checks` | `compendium/asset-pricing/asset-pricing-models.tex` (also factor-model-tests.tex) |
| `notes/artefacts/backtest-inference/backtest-design-checks.py` | `trading_notes.numerical.backtest_evaluation.backtest_design_checks` | `compendium/research-engineering-validation/backtest-evaluation.tex` |
| `notes/artefacts/backtest-inference/drawdown-resampling-checks.py` | `trading_notes.numerical.backtest_evaluation.drawdown_resampling_checks` | `compendium/research-engineering-validation/backtest-evaluation.tex` |
| `notes/artefacts/backtest-inference/multiple-testing-checks.py` | `trading_notes.numerical.backtest_evaluation.multiple_testing_checks` | `compendium/research-engineering-validation/backtest-evaluation.tex` |
| `notes/artefacts/backtest-inference/scenario-simulation-checks.py` | `trading_notes.numerical.scenario_simulation.scenario_simulation_checks` | `compendium/research-engineering-validation/scenario-simulation.tex` |
| `notes/artefacts/backtest-inference/sharpe-checks.py` | `trading_notes.numerical.backtest_evaluation.sharpe_statistics_checks` | `compendium/research-engineering-validation/backtest-evaluation.tex` |
| `notes/artefacts/backtest-inference/sharpe-conditions-checks.py` | `trading_notes.numerical.backtest_evaluation.sharpe_conditions_checks` | `compendium/research-engineering-validation/backtest-evaluation.tex` |
| `notes/artefacts/backtest-inference/sharpe-zero-check.py` | `trading_notes.numerical.backtest_evaluation.sharpe_zero_checks` | `compendium/research-engineering-validation/backtest-evaluation.tex` |
| `notes/artefacts/bond-valuation-risk/bond-valuation-checks.py` | `trading_notes.numerical.bond_pricing_yields.bond_valuation_checks` | `compendium/rates-credit-mortgages/bond-pricing-yields.tex` (parts 1-5 and 10); parts 6-9 serve `interest-rate-risk.tex` |
| `notes/artefacts/capital-market-expectations/cme-checks.py` | `trading_notes.numerical.capital_market_expectations.capital_market_expectations_checks` | `compendium/multi-asset-systematic-macro/capital-market-expectations.tex` |
| `notes/artefacts/commodity-investment/commodity-return-checks.py` | `trading_notes.numerical.commodity_futures_investing.commodity_returns_checks` | `compendium/commodity-investing-premia/commodity-futures-investing.tex` (also commodity-return-components.tex and commodity-indices.tex) |
| `notes/artefacts/commodity-storage-curves/energy-checks.py` | `trading_notes.numerical.commodity_curves.energy_checks` | `compendium/energy-commodities/commodity-curves.tex` |
| `notes/artefacts/corporate-credit-capital/credit-cds-securitisation-checks.py` | `trading_notes.numerical.credit_risk_analysis.credit_cds_securitisation_checks` | `compendium/corporate-credit-capital/credit-risk-analysis.tex`; also cited by `credit-default-swaps.tex`, `government-bond-markets/sovereign-credit.tex` and `securitised-structured-credit/securitisation.tex` |
| `notes/artefacts/corporate-finance/corporate-finance-checks.py` | `trading_notes.numerical.corporate_finance.corporate_finance_checks` | corporate-finance (six subsections; most entries in corporate-ownership-governance) |
| `notes/artefacts/corporate-finance/country-risk-premium-check.py` | `trading_notes.numerical.capital_structure_cost_of_capital.country_risk_premium_checks` | `compendium/corporate-finance/capital-structure-cost-of-capital.tex` |
| `notes/artefacts/counterparty-xva/counterparty-capital-check.py` | `trading_notes.numerical.counterparty_xva.counterparty_capital_checks` | `compendium/portfolio-risk-financing/counterparty-xva.tex` |
| `notes/artefacts/counterparty-xva/counterparty-xva-checks.py` | `trading_notes.numerical.counterparty_xva.counterparty_xva_checks` | `compendium/portfolio-risk-financing/counterparty-xva.tex` |
| `notes/artefacts/credit-portfolios/credit-portfolio-checks.py` | `trading_notes.numerical.credit_portfolio_management.credit_portfolios_checks` | `compendium/corporate-credit-capital/credit-portfolio-management.tex` |
| `notes/artefacts/crypto-mm-microstructure/funding_checks.py` | `trading_notes.numerical.crypto_venues_perpetuals.perpetual_funding_checks` | `compendium/digital-assets-prediction-markets/crypto-venues-perpetuals.tex` |
| `notes/artefacts/crypto-perpetuals/amm-checks.py` | `trading_notes.numerical.amm_lending.amm_pool_checks` | `compendium/onchain-protocols/amm-lending.tex` |
| `notes/artefacts/currency-management/currency-management-checks.py` | `trading_notes.numerical.currency_management.currency_management_checks` | `compendium/currency-markets/currency-management.tex` |
| `notes/artefacts/default-correlation/default-correlation-checks.py` | `trading_notes.numerical.default_correlation.default_correlation_checks` | `compendium/securitised-structured-credit/default-correlation.tex` |
| `notes/artefacts/derivative-overlays/overlay-checks.py` | `trading_notes.numerical.derivative_overlays.derivative_overlays_checks` | `compendium/portfolio-construction-risk/derivative-overlays.tex` |
| `notes/artefacts/derivative-overlays/seasoned-variance-swap-check.py` | `trading_notes.numerical.derivative_overlays.seasoned_variance_swap_checks` | `compendium/portfolio-construction-risk/derivative-overlays.tex` |
| `notes/artefacts/descriptive-probability/statistics-probability-checks.py` | `trading_notes.numerical.descriptive_statistics.statistics_probability_checks` | `compendium/probability-statistics/descriptive-statistics.tex` |
| `notes/artefacts/digital-assets/digital-asset-checks.py` | `trading_notes.numerical.distributed_ledgers.digital_assets_checks` | `compendium/digital-assets-prediction-markets/distributed-ledgers.tex` (parts 5-7 serve crypto-spot-markets/digital-asset-investing.tex) |
| `notes/artefacts/economic-growth/growth-checks.py` | `trading_notes.numerical.economic_growth.economic_growth_checks` | `compendium/multi-asset-systematic-macro/economic-growth.tex` |
| `notes/artefacts/equity-long-short-construction/forecast-checks.py` | `trading_notes.numerical.signal_combination.forecast_scaling_checks` | `compendium/systematic-equities/signal-combination.tex` |
| `notes/artefacts/equity-long-short-construction/projection-checks.py` | `trading_notes.numerical.signal_combination.linear_projection_checks` | `compendium/systematic-equities/signal-combination.tex` |
| `notes/artefacts/equity-portfolio-management/equity-portfolio-checks.py` | `trading_notes.numerical.equity_portfolio_management.equity_portfolio_management_checks` | `compendium/systematic-equities/equity-portfolio-management.tex` |
| `notes/artefacts/etf-mechanics/etf-checks.py` | `trading_notes.numerical.etf_mechanics.etf_mechanics_checks` | `compendium/execution-trading-costs/etf-mechanics.tex` |
| `notes/artefacts/execution-market-making/cme-allocation-checks.py` | `trading_notes.numerical.order_books.cme_allocation_checks` | `compendium/execution-market-making/order-books.tex` |
| `notes/artefacts/execution-market-making/commodity-production-latency-checks.py` | `trading_notes.numerical.order_books.commodity_latency_checks` | `compendium/execution-market-making/order-books.tex` (by content; no live note cites it) |
| `notes/artefacts/execution-market-making/contract-specifications-statistics-checks.py` | `trading_notes.numerical.futures_execution.contract_statistics_checks` | `compendium/execution-trading-costs/futures-execution.tex`; also cited by `notes/pathways/macro-announcements-policy.md` |
| `notes/artefacts/execution-market-making/dealer-queue-information-checks.py` | `trading_notes.numerical.high_frequency_trading.dealer_queue_information_checks` | `compendium/execution-market-making/high-frequency-trading.tex` |
| `notes/artefacts/execution-market-making/liquidity-market-design-checks.py` | `trading_notes.numerical.market_organisation.liquidity_market_design_checks` | `compendium/execution-market-making/market-organisation.tex` |
| `notes/artefacts/execution-market-making/market-estimators-rules-checks.py` | `trading_notes.numerical.order_flow_statistics.market_estimators_rules_checks` | `compendium/execution-market-making/order-flow-statistics.tex` |
| `notes/artefacts/exotic-options/exotic-option-checks.py` | `trading_notes.numerical.exotic_options.exotic_options_checks` | `compendium/volatility-options/exotic-options.tex` |
| `notes/artefacts/exotic-options/lookback-option-check.py` | `trading_notes.numerical.exotic_options.lookback_options_checks` | `compendium/volatility-options/exotic-options.tex` |
| `notes/artefacts/extreme-value/extreme-value-checks.py` | `trading_notes.numerical.extreme_values.extreme_value_checks` | `compendium/probability-statistics/extreme-values.tex` |
| `notes/artefacts/financial-ml-methods/ml-methods-checks.py` | `trading_notes.numerical.machine_learning_methods.financial_ml_methods_checks` | `compendium/ml-alternative-data/machine-learning-methods.tex` (also data-science-workflow.tex and text-features.tex) |
| `notes/artefacts/financial-statement-analysis/cash-flow-linkage-check.py` | `trading_notes.numerical.cash_flow_analysis.cash_flow_linkage_checks` | `compendium/financial-statement-analysis/cash-flow-analysis.tex` |
| `notes/artefacts/financial-statement-analysis/statement-analysis-checks.py` | `trading_notes.numerical.company_case.statement_analysis_checks` | financial-statement-analysis/company-case (case used across the section) |
| `notes/artefacts/firms-market-structure/market-structure-checks.py` | `trading_notes.numerical.firms_market_structure.market_structure_checks` | `compendium/systematic-equities/firms-market-structure.tex` |
| `notes/artefacts/fixed-income-portfolio/fixed-income-portfolio-checks.py` | `trading_notes.numerical.fixed_income_portfolio_management.fixed_income_portfolio_checks` | `compendium/rates-credit-mortgages/fixed-income-portfolio-management.tex`; also cited by `portfolio-risk-financing/liability-matching.tex` |
| `notes/artefacts/forward-swap-valuation/cross-currency-basis-check.py` | `trading_notes.numerical.forward_commitment_valuation.cross_currency_basis_checks` | `compendium/volatility-options/forward-commitment-valuation.tex` |
| `notes/artefacts/forward-swap-valuation/forward-swap-checks.py` | `trading_notes.numerical.forward_commitment_valuation.forward_swap_valuation_checks` | `compendium/volatility-options/forward-commitment-valuation.tex` |
| `notes/artefacts/fx-determination-forecasting/fx-checks.py` | `trading_notes.numerical.macro_fx.fx_checks` | `compendium/currency-markets/macro-fx.tex` |
| `notes/artefacts/fx-determination-forecasting/fx-panel-inference-check.py` | `trading_notes.numerical.macro_fx.fx_panel_inference_checks` | `compendium/currency-markets/macro-fx.tex` |
| `notes/artefacts/fx-mechanics-determination/fx-checks.py` | `trading_notes.numerical.fx_mechanics_parity.fx_mechanics_checks` | `compendium/currency-markets/fx-mechanics-parity.tex` (also fx-market.tex, fx-quotes-forwards.tex and currency-carry.tex) |
| `notes/artefacts/hedge-funds/hedge-fund-checks.py` | `trading_notes.numerical.hedge_fund_strategies.hedge_funds_checks` | `compendium/portfolio-construction-risk/hedge-fund-strategies.tex` |
| `notes/artefacts/high-dimensional-estimation/covariance-volatility-checks.py` | `trading_notes.numerical.covariance_estimation.covariance_volatility_checks` | `compendium/high-dimensional-statistics/covariance-estimation.tex` (parts 3-4 serve regression-time-series/volatility-forecasting.tex) |
| `notes/artefacts/inference-simulation/correlation-independence-checks.py` | `trading_notes.numerical.statistical_inference.correlation_independence_checks` | `compendium/probability-statistics/statistical-inference.tex` |
| `notes/artefacts/inference-simulation/inference-simulation-checks.py` | `trading_notes.numerical.statistical_inference.inference_simulation_checks` | `compendium/probability-statistics/statistical-inference.tex` |
| `notes/artefacts/institutional-portfolios/institutional-checks.py` | `trading_notes.numerical.institutional_portfolios.institutional_portfolios_checks` | `compendium/portfolio-risk-financing/institutional-portfolios.tex` (also portfolio-construction-risk/esg-integration.tex) |
| `notes/artefacts/investment-planning/investment-planning-checks.py` | `trading_notes.numerical.investment_process_planning.investment_planning_checks` | `compendium/portfolio-construction-risk/investment-process-planning.tex` |
| `notes/artefacts/linear-regression/multiple-regression-checks.py` | `trading_notes.numerical.multiple_regression.multiple_regression_checks` | `compendium/regression-time-series/multiple-regression.tex` |
| `notes/artefacts/linear-regression/regression-checks.py` | `trading_notes.numerical.regression.linear_regression_checks` | `compendium/regression-time-series/regression.tex` |
| `notes/artefacts/macro-asset-valuation/macro-valuation-checks.py` | `trading_notes.numerical.macro_asset_valuation.macro_valuation_checks` | `compendium/multi-asset-systematic-macro/macro-asset-valuation.tex` |
| `notes/artefacts/macro-policy-trade/macro-policy-trade-checks.py` | `trading_notes.numerical.business_cycles_policy.macro_policy_trade_checks` | `compendium/multi-asset-systematic-macro/business-cycles-policy.tex` (also rates-credit-mortgages/monetary-fiscal-policy.tex) |
| `notes/artefacts/macro-regimes-stock-bond/regime-checks.py` | `trading_notes.numerical.macro_regimes_data.regime_checks` | `compendium/multi-asset-systematic-macro/macro-regimes-data.tex` |
| `notes/artefacts/manager-selection/manager-selection-checks.py` | `trading_notes.numerical.manager_selection.manager_selection_checks` | `compendium/portfolio-construction-risk/manager-selection.tex` |
| `notes/artefacts/market-index-construction/index-construction-checks.py` | `trading_notes.numerical.index_construction.index_construction_checks` | `compendium/international-equity-markets/index-construction.tex` |
| `notes/artefacts/market-making-lob/model-checks.py` | `trading_notes.numerical.market_making_models.lob_models_checks` | `compendium/execution-market-making/market-making-models.tex` |
| `notes/artefacts/market-making-lob/model-derivations-checks.py` | `trading_notes.numerical.market_making_models.lob_model_derivations_checks` | `compendium/execution-market-making/market-making-models.tex` |
| `notes/artefacts/market-risk-measurement/market-risk-checks.py` | `trading_notes.numerical.market_risk_measurement.market_risk_measurement_checks` | `compendium/portfolio-construction-risk/market-risk-measurement.tex` |
| `notes/artefacts/market-simulation/order-flow-checks.py` | `trading_notes.numerical.order_flow_statistics.order_flow_checks` | `compendium/execution-market-making/order-flow-statistics.tex` |
| `notes/artefacts/multi-asset-systematic-macro/carry-market-statistics-checks.py` | `trading_notes.numerical.multi_asset_systematic_macro.carry_market_statistics_checks` | multi-asset-systematic-macro (currency-markets/macro-fx.tex, rates-credit-mortgages/interest-rates.tex and monetary-policy-curves.tex, macro-regimes-data.tex, execution-market-making/order-books.tex and high-frequency-trading.tex) |
| `notes/artefacts/multi-asset-systematic-macro/convexity-curve-signals-checks.py` | `trading_notes.numerical.multi_asset_systematic_macro.convexity_curve_signals_checks` | multi-asset-systematic-macro (rates-credit-mortgages/interest-rates.tex, business-cycles-policy.tex, global-macro.tex, physical commodities, currency-markets/currency-carry.tex) |
| `notes/artefacts/multi-asset-systematic-macro/macro-pricing-risk-checks.py` | `trading_notes.numerical.global_macro.macro_pricing_risk_checks` | `compendium/multi-asset-systematic-macro/global-macro.tex` (parts also serve rates-credit-mortgages/monetary-policy-curves.tex and execution-trading-costs/futures-execution.tex) |
| `notes/artefacts/numerical-pricing/monte-carlo-greeks-check.py` | `trading_notes.numerical.monte_carlo_simulation.monte_carlo_greeks_checks` | `compendium/numerical-optimisation/monte-carlo-simulation.tex` |
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
| `notes/artefacts/portfolio-construction/shrinkage-check.py` | `trading_notes.numerical.covariance_estimation.covariance_shrinkage_checks` | `compendium/high-dimensional-statistics/covariance-estimation.tex` |
| `notes/artefacts/portfolio-risk-return/portfolio-choice-checks.py` | `trading_notes.numerical.portfolio_choice.portfolio_choice_checks` | `compendium/portfolio-construction-risk/portfolio-choice.tex` |
| `notes/artefacts/portfolio-risk-return/portfolio-moments-checks.py` | `trading_notes.numerical.portfolio_moments.portfolio_moments_checks` | `compendium/portfolio-construction-risk/portfolio-moments.tex` |
| `notes/artefacts/private-capital/private-capital-checks.py` | `trading_notes.numerical.private_capital_allocator.private_capital_checks` | private-capital-allocator (alternative-investment-structures.tex, private-fund-structures.tex, private-market-programmes.tex, private-equity-strategies.tex, private-debt-special-situations.tex) |
| `notes/artefacts/private-wealth/concentrated-position-check.py` | `trading_notes.numerical.wealth_transfer.concentrated_position_checks` | `compendium/private-wealth-management/wealth-transfer.tex` (the collar serves volatility-options/option-strategies.tex) |
| `notes/artefacts/private-wealth/private-wealth-checks.py` | `trading_notes.numerical.private_wealth_management.private_wealth_checks` | private-wealth-management (clients-industry.tex parts 1, 3-4; wealth-planning.tex parts 3, 5, 6, 8-10; wealth-preservation.tex parts 2, 7, 10; wealth-transfer.tex parts 11-13) |
| `notes/artefacts/rate-tree-embedded-options/rate-tree-checks.py` | `trading_notes.numerical.embedded_option_bonds.rate_tree_checks` | `compendium/rates-credit-mortgages/embedded-option-bonds.tex`; also cited by `arbitrage-free-valuation.tex` and `volatility-options/convertible-bonds.tex` |
| `notes/artefacts/rates-credit-mortgages/fra-settlement-check.py` | `trading_notes.numerical.rate_swaps_clearing.fra_settlement_checks` | `compendium/rates-credit-mortgages/rate-swaps-clearing.tex` |
| `notes/artefacts/rates-credit-mortgages/multicurve-check.py` | `trading_notes.numerical.rate_swaps_clearing.multicurve_checks` | `compendium/rates-credit-mortgages/rate-swaps-clearing.tex` |
| `notes/artefacts/rates-credit-mortgages/yield-shift-check.py` | `trading_notes.numerical.interest_rates.yield_shift_checks` | `compendium/rates-credit-mortgages/interest-rates.tex` |
| `notes/artefacts/real-assets/real-asset-checks.py` | `trading_notes.numerical.real_asset_investor.real_assets_checks` | real-asset-investor (real-estate.tex parts 1-4, infrastructure.tex part 5, land-timber-farmland.tex part 6) |
| `notes/artefacts/reinforcement-learning-trading/cartea_jaimungal_checks.py` | `trading_notes.numerical.execution_control.cartea_jaimungal_checks` | `compendium/execution-trading-costs/execution-control.tex` |
| `notes/artefacts/return-predictability/conditional-predictive-ability-checks.py` | `trading_notes.numerical.return_predictability.conditional_predictive_ability_checks` | `compendium/asset-pricing/return-predictability.tex` |
| `notes/artefacts/return-predictability/forecast-combination-scoring-checks.py` | `trading_notes.numerical.return_predictability.forecast_combination_scoring_checks` | `compendium/asset-pricing/return-predictability.tex` |
| `notes/artefacts/return-predictability/return-predictability-checks.py` | `trading_notes.numerical.return_predictability.return_predictability_checks` | `compendium/asset-pricing/return-predictability.tex` |
| `notes/artefacts/risk-parity-vol-targeting/risk-parity-checks.py` | `trading_notes.numerical.portfolio_construction_models.risk_parity_checks` | `compendium/portfolio-construction-risk/portfolio-construction-models.tex` |
| `notes/artefacts/risk-tail-systemic/es-discrete-check.py` | `trading_notes.numerical.var_es_estimation.expected_shortfall_checks` | `compendium/portfolio-construction-risk/var-es-estimation.tex` |
| `notes/artefacts/risk-tail-systemic/garch-ewma-check.py` | `trading_notes.numerical.volatility_forecasting.garch_ewma_checks` | `compendium/regression-time-series/volatility-forecasting.tex` |
| `notes/artefacts/risk-tail-systemic/var-backtest-check.py` | `trading_notes.numerical.var_es_estimation.var_backtest_checks` | `compendium/portfolio-construction-risk/var-es-estimation.tex` |
| `notes/artefacts/short-rate-models/short-rate-model-checks.py` | `trading_notes.numerical.arbitrage_free_valuation.short_rate_model_checks` | `compendium/rates-credit-mortgages/arbitrage-free-valuation.tex` |
| `notes/artefacts/short-term-funding/funding-repo-checks.py` | `trading_notes.numerical.money_markets.funding_repo_checks` | `compendium/portfolio-risk-financing/money-markets.tex` |
| `notes/artefacts/short-term-funding/margin-purchase-check.py` | `trading_notes.numerical.securities_lending.margin_purchase_checks` | `compendium/portfolio-risk-financing/securities-lending.tex` |
| `notes/artefacts/statistical-learning-foundations/afml-checks.py` | `trading_notes.numerical.ml_alternative_data.afml_checks` | ml-alternative-data (financial-data-structures.tex, labelling-sample-weights.tex, fractional-differentiation.tex) |
| `notes/artefacts/statistical-learning-foundations/cv-checks.py` | `trading_notes.numerical.labelling_sample_weights.purged_cv_checks` | `compendium/ml-alternative-data/labelling-sample-weights.tex` |
| `notes/artefacts/statistical-learning-foundations/financial-labels-capital-checks.py` | `trading_notes.numerical.labelling_sample_weights.financial_labels_checks` | `compendium/ml-alternative-data/labelling-sample-weights.tex` (the ETF-trick parts serve financial-data-structures.tex) |
| `notes/artefacts/stochastic-calculus/stochastic-calculus-checks.py` | `trading_notes.numerical.stochastic_calculus.stochastic_calculus_checks` | `compendium/stochastic-processes-calculus/stochastic-calculus.tex` |
| `notes/artefacts/strategic-asset-allocation/saa-checks.py` | `trading_notes.numerical.strategic_asset_allocation.strategic_asset_allocation_checks` | `compendium/portfolio-construction-risk/strategic-asset-allocation.tex` |
| `notes/artefacts/synthetic-equity-cfd-trs/synthetic_short_checks.py` | `trading_notes.numerical.synthetic_shorts.synthetic_short_checks` | `compendium/portfolio-risk-financing/synthetic-shorts.tex` |
| `notes/artefacts/systematic-equities/equity-fcf-ri-private-checks.py` | `trading_notes.numerical.systematic_equities.equity_fcf_ri_private_checks` | systematic-equities (free-cash-flow, residual-income and private-company valuation) |
| `notes/artefacts/systematic-equities/equity-valuation-checks.py` | `trading_notes.numerical.systematic_equities.equity_valuation_checks` | systematic-equities (market multiples, valuation foundations, dividend discount models) |
| `notes/artefacts/term-structure-dynamics/term-structure-checks.py` | `trading_notes.numerical.term_structure_returns.term_structure_checks` | `compendium/rates-credit-mortgages/term-structure-returns.tex` |
| `notes/artefacts/time-series-models/time-series-checks.py` | `trading_notes.numerical.time_series_models.time_series_checks` | `compendium/regression-time-series/time-series-models.tex` |
| `notes/artefacts/trade-execution/trade-execution-checks.py` | `trading_notes.numerical.trade_strategy_governance.trade_execution_checks` | `compendium/execution-trading-costs/trade-strategy-governance.tex` |
| `notes/artefacts/volatility-options/bsm-svi-checks.py` | `trading_notes.numerical.option_pricing.bsm_svi_checks` | `compendium/volatility-options/option-pricing.tex` |

`corporate_finance` and `systematic_equities` are named after sections, not subsections, because each of their check scripts spans several subsections of one shared case; their domain code lives in subsection packages (`capital_structure_cost_of_capital`, `company_case`).

`real_asset_investor`, `private_capital_allocator`, `private_wealth_management`, `ml_alternative_data` and `multi_asset_systematic_macro` are named after sections for the same reason; their domain code lives in the subsection packages listed below.

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
| `forecast_scaling` | `signal_combination.forecast_refinement`, `signal_combination.forecast_scaling_checks` |
| `linear_projection` | `signal_combination.projection`, `signal_combination.linear_projection_checks` |
| `covariance_shrinkage` | `covariance_estimation.oracle_shrinkage`, `covariance_estimation.covariance_shrinkage_checks` |
| `covariance_volatility` | `covariance_estimation.constant_correlation`, `covariance_estimation.har_model`, `covariance_estimation.covariance_volatility_checks` |
| `garch_ewma` | `volatility_forecasting.garch`, `volatility_forecasting.garch_ewma_checks` |
| `purged_cv` | `labelling_sample_weights.cross_validation`, `labelling_sample_weights.purged_cv_checks` |
| `financial_labels` | `labelling_sample_weights.labels`, `financial_data_structures.etf_trick`, `labelling_sample_weights.financial_labels_checks` |
| `afml` | `financial_data_structures.bar_sampling`, `financial_data_structures.etf_trick`, `labelling_sample_weights.labels`, `fractional_differentiation.fractional_weights`, `ml_alternative_data.afml_checks` |
| `amm_pool` | `amm_lending.liquidity_pools`, `amm_lending.amm_pool_checks` |
| `perpetual_funding` | `crypto_venues_perpetuals.funding_rates`, `crypto_venues_perpetuals.perpetual_funding_checks` |
| `synthetic_short` | `synthetic_shorts.replication`, `synthetic_shorts.synthetic_short_checks` |
| `digital_assets` | `distributed_ledgers.ledger`, `distributed_ledgers.digital_assets_checks` |
| `monte_carlo_greeks` | `monte_carlo_simulation.greek_estimators`, `monte_carlo_simulation.monte_carlo_greeks_checks` |
| `concentrated_position` | `wealth_transfer.concentrated_stock`, `wealth_transfer.concentrated_position_checks` |
| `index_construction` | `index_construction.index_mathematics`, `index_construction.index_construction_checks` |
| `etf_mechanics` | `etf_mechanics.etf_trading`, `etf_mechanics.etf_mechanics_checks` |
| `commodity_returns` | `commodity_futures_investing.futures_returns`, `commodity_futures_investing.commodity_returns_checks` |
| `cartea_jaimungal` | `execution_control.optimal_liquidation`, `execution_control.cartea_jaimungal_checks` |
| `fx_panel_inference` | `newey_west` (support module, unchanged), `macro_fx.fx_panel_inference_checks` |
| `currency_management` | `currency_management.currency_hedging`, `currency_management.currency_management_checks` |
| `fx_mechanics` | `fx_mechanics_parity.fx_quotes`, `fx_mechanics_parity.fx_mechanics_checks` |
| `macro_valuation` | `macro_asset_valuation.valuation_models`, `macro_asset_valuation.macro_valuation_checks` |
| `economic_growth` | `economic_growth.solow`, `economic_growth.economic_growth_checks` |
| `capital_market_expectations` | `capital_market_expectations.regimes`, `capital_market_expectations.capital_market_expectations_checks` |
| `macro_policy_trade` | `business_cycles_policy.policy_models`, `business_cycles_policy.macro_policy_trade_checks` |
| `macro_pricing_risk` | `global_macro.rates_arithmetic`, `global_macro.macro_pricing_risk_checks` |
| `real_assets` | `real_estate.property_cash_flows`, `infrastructure.sculpted_debt`, `land_timber_farmland.timber`, `real_asset_investor.real_assets_checks` |
| `asset_pricing_factor_models` | `asset_pricing_models.capm`, `asset_pricing_models.asset_pricing_checks` |
| (script only) `regime-checks.py` | `macro_regimes_data.regime_panel`, `macro_regimes_data.regime_checks` |
| (script only) `carry-market-statistics-checks.py` | `currency_carry.funded_carry`, `multi_asset_systematic_macro.market_statistics`, `multi_asset_systematic_macro.carry_market_statistics_checks` |
| (script only) `convexity-curve-signals-checks.py` | `business_cycles_policy.recession_signals`, `multi_asset_systematic_macro.convexity_curve_signals_checks` |
| (script only) `forecast-combination-scoring-checks.py` | `return_predictability.labelled_table`, `return_predictability.forecast_evaluation`, `return_predictability.scoring_rules`, `return_predictability.forecast_combination_scoring_checks` |
| (script only) `return-predictability-checks.py` | `return_predictability.present_value`, `return_predictability.forecast_evaluation`, `return_predictability.labelled_table`, `return_predictability.return_predictability_checks` |
| (script only) `conditional-predictive-ability-checks.py` | `return_predictability.conditional_ability`, `return_predictability.scoring_rules`, `return_predictability.labelled_table`, `return_predictability.conditional_predictive_ability_checks` |
| (script only) `energy-checks.py` | `commodity_curves.nymex_contracts` (copied from `backwardation_test.py`, which keeps its own; pinned by `test_nymex_contracts`), `commodity_curves.energy_checks` |
| (script only) `fx-checks.py` | `macro_fx.ppp_forecasts` (also imported by `fx_ppp_oos_test.py`), `macro_fx.fx_checks` |
| `financial_ml_methods` | `machine_learning_methods.learners`, `machine_learning_methods.financial_ml_methods_checks` |
| `institutional_portfolios` | `institutional_portfolios.plan_rules`, `institutional_portfolios.institutional_portfolios_checks` |
| `private_capital` | `alternative_investment_structures.hedge_fund_fees`, `private_fund_structures.waterfalls`, `private_equity_strategies.leveraged_buyout`, `private_debt_special_situations.restructuring`, `internal_rate` (new support module), `private_capital_allocator.private_capital_checks` |
| `private_wealth` | `wealth_planning.household_plan`, `wealth_preservation.us_income_tax`, `wealth_preservation.tax_drag`, `wealth_transfer.transfer_rules`, `private_wealth_management.private_wealth_checks` |
| (new) | `us_calendar`: weekday arithmetic and federal holidays shared by the order-book, futures and SOFR examples |
| (new) | `internal_rate`: the IRR (Brent's method on a fixed bracket) shared by the real-asset and private-capital examples |

## Inventory of Python outside `src/`

Counted on 2026-10-24 with `git ls-files -co --exclude-standard '*.py' '*.pyi'`, with the macro-to-wealth batch in the working tree: 41 files outside `src/` (439 inside it).

| Kind | Files | Disposition |
| --- | --- | --- |
| Forwarding wrappers in `notes/artefacts/` (`from trading_notes.numerical ... import main`) | 10 | Retired as their 10 flat modules move into subsection packages. |
| Unmigrated check implementations in `notes/artefacts/` (run by `make examples`) | 0 | None remain. |
| Research and data scripts in `notes/artefacts/`: extracts, empirical reruns, exchange snapshots | 22 | Migrate into `src/trading_notes/research/<topic>/` with `--root` data paths; the data and outputs they read and write stay in `notes/artefacts/`. Scripts that need network access or the `empirical` dependency group keep that requirement and are not run by `make check`. Coupled to the package: `fx_ppp_oos_test.py` imports `macro_fx.ppp_forecasts` and `newey_west` (and `fx_carry_test.py` uses them through it); `backwardation_test.py` keeps its own NYMEX helpers, because `heating_oil_test.py` patches its module globals, and `test_nymex_contracts` pins `commodity_curves.nymex_contracts` to them. |
| Historical runs in `notes/artefacts/**/superseded-*/` | 8 | Archived, not maintained: kept byte for byte as the code that produced the superseded results cited by `notes/source-review-records.md`, excluded from lint and type checks, never executed. To be removed from the working tree in one batch once those records cite them as `git show <commit>:<path>`; their data files stay. |
| `guide/refresh_views.py` | 1 | Migrate into `src/trading_notes/guide/refresh_views.py`, run as `python -m trading_notes.guide.refresh_views --root guide`, with the vendored guide keeping only its data and outputs; `guide/README.md` and `subsection_alignment_plan.md` then point to the module. |

Inside `src/trading_notes/numerical/`: 10 flat example modules still to move into subsection packages, and eight support modules (`__init__`, `internal_rate`, `newey_west`, `records`, `report`, `repository`, `tolerance`, `us_calendar`).

## Completed batches

| Batch | Implementations | Evidence |
| --- | --- | --- |
| Statistics, backtest inference, rates, funding, credit and execution | 40: the 35 flat modules and 5 scripts in the tables above, from `backtest-design-checks.py` to `trade-execution-checks.py` | Each module's output diffed against its pre-migration run: identical except six intended wording changes that removed history text: the backtest-design "earlier rule/peak" labels, the statistics header "corrections of 2026-10-18" (now "counterexamples"), the extreme-value "freeze reproduction" line, the liquidity "market design review" sampler (now "naive sampler"), the municipal-discount header's "(correction of 2026-10-19)" and the short-rate parameters "written in this script" (now "in the module"). Class-based migration completed by the audit repairs below. After them `make source-check` passed on 2026-10-24: lock check, lint, format, strict mypy (352 files), compendium and coverage checkers with 0 problems, 418 tests and 944 subtests, `make examples` 8 check scripts; `make verify-outlines` 0 problems. Committed and pushed as `a07387728cd92b9ec2ffa0eff41fd3da3fe57235`. |
| Macro, FX, commodities, return predictability, covariance and machine learning, wealth and market structure | 40: the 32 flat modules and 8 check scripts in the tables above, from `forecast_scaling` to `private_wealth` | Each entrypoint's output, run from an empty folder with `--root`, diffed against its pre-migration run: byte-identical for 36; four intended wording changes that removed process text, with every number unchanged: the Cartea-Jaimungal heading "follow-up checks (2026-10-15)" (now "wealth identity, feedback policies and the unbounded counterexample"); the convexity script's final line "all follow-up checks passed" (now "all checks passed"); nine return-predictability lines that carried "added in the audit" or similar labels; and the conditional-predictive-ability check E3 "the recursive ones of the previous batches" (now "of the forecast-combination check"). One behaviour change: the convexity script's `assert` statements became failure-only checks, so a failure prints a `BAD` line and exits 1 instead of raising AssertionError. The 32 wrappers are deleted and removed from `[tool.mypy] files`, `notes/artefacts/ruff.toml` and the E501 list; the 8 scripts moved with `git mv`. `fx_ppp_oos_test.py` now imports `StaleDataRule`, `ExpandingForecast` and the Newey-West helpers; rerun on the local FRED files it and `fx_carry_test.py` reproduce `fx_ppp_monthly.csv`, `fx_ppp_results.txt`, `fx_carry_monthly.csv` and `fx_carry_results.txt` byte for byte, and `test_newey_west` now keeps the script's former helpers as the reference. `backwardation_test.py` is unchanged (rerun: its panel and results reproduce; the heating-oil spreadsheet is not available locally, so `heating_oil_test.py`, also unchanged, was not rerun). `make source-check` passed on 2026-10-24: lock check, lint, format (480 files), strict mypy (428 files), compendium and coverage checkers with 0 problems, 448 tests and 8280 subtests, `make examples` reporting no unmigrated scripts; `make verify-outlines` 0 problems, `make pre-commit` passed, `make pdf` rebuilt. Completed by the audit repairs below. |

### Audit repairs of the macro-to-wealth batch

An audit of the second batch found three boundary defects, two of them introduced when pandas gave way to the NumPy-backed `LabelledTable`, and found that the scoring rules and several other domain modules had kept function-only APIs. "Pre-existing" means the defect was already in the original script or flat module; "regression" means the migration introduced it.

| Finding | Origin | Repair | Validation |
| --- | --- | --- | --- |
| `FractionalDifference.fixed_width` took `argmax(abs(w) < thr)`, which is 0 when no weight qualifies, and then returned `len(series) + 1` zeros from empty dot products (order 0.4, `thr=1e-12`: six zeros for five observations) | pre-existing (`afml.py`'s `ffd`) | `width(thr, max_width)` returns the number of weights kept and raises ValueError when no weight among the first `max_width` falls below `thr` (including `thr <= 0`) or when `thr` exceeds the leading weight 1; a series shorter than the window gives an empty float64 array; no zero is ever fabricated | `test_financial_labels.FractionalWeights`: unreached and invalid cutoffs, a short history (empty) and one exactly a window long (one value), d = 0.5 at `thr=0.2` by hand, and the identities for d = 0, 1, 2 (series, first and second difference) |
| `LabelledTable.first_valid` returned the first label for an all-NaN column, where pandas' `first_valid_index()` returned None | regression | Returns `int \| None`: None for an all-NaN or empty column; an unknown column is a KeyError. `return_predictability_checks` raises ValueError if an extract has no CRSP return instead of printing a wrong year | `test_return_predictability.FirstValid` |
| `lagged(x, 0)` raised a broadcasting error (`x[:-0]` is empty), where pandas' `shift(0)` returned the column | regression | k = 0 returns an unchanged copy; k at or beyond the length gives all NaN; a negative k raises ValueError (no caller needs a lead) | `test_return_predictability.Shifts` |
| `tick_rule` and `ImbalanceBars.bar_ends` built their results without a dtype, so empty results were float64 and could not index arrays; a burn-in without buys or sells warned "Mean of empty slice" | pre-existing (`afml.py`) | Both return int64 arrays, empty ones included; a flow of at most the 100-tick burn-in returns an empty array at once; side volumes of an absent side are NaN without a warning, and volume runs bars, the only rule that uses them, raise ValueError on such a burn-in; signs and volumes of different lengths raise ValueError | `test_financial_labels.Bars`: empty and no-bar results as indices under `warnings` as errors, a one-sided burn-in |
| `scoring_rules` was five functions | incomplete extraction | `NormalForecast` (log score, CRPS, central interval), `CentralInterval` (interval score, its two quantile forecasts) and `QuantileForecast` (quantile score), generic in a float or float64 array with one private shaping helper, so scalars give `float` and arrays elementwise arrays; `crps_quadrature` stays a function of a CDF alone, the independent reference | `test_return_predictability.NormalScores` and `IntervalAndQuantileScores`: hand values (N(0, 1) at 0, interval and quantile scores), the quadrature reference, return types and the quantile decomposition |
| Other function-only domain APIs in the batch | incomplete extraction | `machine_learning_methods.learners`: `RidgeRegression`, `LassoRegression`, `NearestNeighbours`, and `Leaf.predict`/`Split.predict` in place of `ridge`, `lasso_cd`, `knn_pred` and `_predict`; `return_predictability.forecast_evaluation`: `RecursiveForecasts` in place of the tuple-returning `recursive_forecasts` (`lstsq_forecasts` stays the independent reference); `wealth_transfer.transfer_rules`: `PresenceDays`, `TradingPlan`, `EstateTax`; `private_debt_special_situations.restructuring`: `ClassVote`, `PlanConfirmation`; `distributed_ledgers.ledger`: `MerkleBranch` returned by `MerkleTree.branch` | the consuming examples' outputs; `test_digital_assets` |

Every one of the 130 example entrypoints, run from an empty folder before and after the repairs, printed byte-identical output and exited 0: no valid-case number changed. Small pure helpers remain where a class would add nothing (`tick_rule`, `lagged`, `mean_t`, `ols_slope`, `frob`, `gmv_var`, the simulation helpers `ar1` and `moving_average`, and the two independent variance routes of `optimal_liquidation`).

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

- 10 flat example modules and their 10 wrappers, the 22 research and data scripts and `guide/refresh_views.py`: 33 implementations.
- Four of the 10 flat modules still define dataclasses (`bitemporal`, `filing_timestamps`, `order_reconciliation`, `time_value_returns`); they become pydantic records as they migrate. The structural checkers (`structure/compendium.py`, `compendium_check.py`, `coverage_check.py`) also use dataclasses and are outside the numerical migration.
- `counterparty_xva.regulatory_capital` keeps its function-based form (outside the audit findings).
- The eight historical runs: rewrite their citations, then remove them from the working tree.
- When the commodity research scripts migrate, `backwardation_test.py` and `heating_oil_test.py` should use `commodity_curves.nymex_contracts` (the heating-oil rule as a third market rather than patched globals) and `test_nymex_contracts` should then test the package alone.

## Next batch

The ten flat modules left (`bitemporal`, `filing_deadlines`, `filing_timestamps`, `intercorporate_fx_institutions`, `margin_spiral`, `negative_hedge_ratio`, `numerical_pricing`, `order_reconciliation`, `order_routing_fragmentation`, `time_value_returns`), the 22 research scripts and `guide/refresh_views.py`.
