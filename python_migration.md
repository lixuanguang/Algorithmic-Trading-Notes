# Python migration

All maintained Python is under `src/`: the package in `src/trading_notes/`, tests in `src/tests/`, local stubs in `src/typings/`. The migration is complete: no Python file is left outside `src/`, and no module defines a dataclass. Numerical examples move from flat modules and `notes/artefacts/` scripts into one package per compendium subsection, `src/trading_notes/numerical/<subsection>/`, holding domain modules beside `*_checks.py` entrypoints that run as `python -m trading_notes.numerical.<subsection>.<name>_checks`.

## Checklist for each migrated example

- [ ] Run the old script and save its output as the baseline.
- [ ] Move the module with `git mv` into the subsection package; split domain classes and functions from check orchestration and reporting.
- [ ] Model records as pydantic models (`trading_notes.records.Record`, or `MutableRecord` for accumulators), not dataclasses or untyped dicts. A record is iterable over its fields, so never unpack or splat one as if it were a tuple; mypy does not catch it.
- [ ] Share `report.CheckReport`, `report.print_versions`, `tolerance.close`, `repository.repository_root` and `option_pricing.black_scholes.BlackScholes` where the arithmetic is identical; keep independent references independent.
- [ ] Keep formulas, units, seeds and tolerances; rerun and diff against the baseline, explaining any numerical difference.
- [ ] Keep the module docstring to one purpose sentence; sources, seeds and conventions go in the `main()` docstring. No dated corrections, audit notes or migration narrative in Python.
- [ ] Read files below a `--root` repository root (default: the working directory), never relative to the working directory alone.
- [ ] Register the module in `src/tests/numerical/test_checks.py` with its `passed` summary and, when a run takes more than about half a second, `stand_ins` for its expensive parts; port its unit tests.
- [ ] Rewrite live references in `compendium/`, `notes/pathways/` and `notes/coverage/` to the module name; leave dated review records as written.
- [ ] Pass `make lint format-check typecheck check-compendium check-coverage test`.

## How the examples are tested

- `test_each_example_runs_once`: one real, isolated run of each example's entrypoint (`python -I -W error`, the module through runpy as `python -m` runs it) from an empty temporary folder. It must exit 0 with its check-line count, no failed line and its success summary, leave the primed shared generators and NumPy settings unchanged, and write nothing.
- `test_failure_reaches_status_and_runs_repeat` (one pytest item per check): `main()` in process three times, clean, with one forced failure, clean again, with expensive parts replaced by `stand_ins`. The clean runs must pass and print the same thing; the failure must reach the summary and status 1.
- `test_entrypoints_exit_with_the_status_of_main`: each module's `if __name__ == "__main__":` block, executed with `main` answering 0 and then 1.
- `VerifiersRejectBrokenExamples`: the verifiers reject a `main` that always returns 1, one that always returns 0, and a report kept across runs.
- `src/tests/research/test_workflows.py`: the research workflows' arguments, side-effect-free imports, shared readers and shared records (`RandomWalkComparison`, `TimingRule`, `IndexMonths`, the H.15 and Treasury extract readers, the jet-fuel weekly changes); the H.15, Treasury and inversion workflows against their committed outputs; and, when the git-ignored `reading_materials/` is present, every other workflow replayed (`python -I -W error`) into a temporary folder from an unrelated directory and compared with its retained outputs byte for byte, after the explicit `RELABELLED` mapping of reworded labels, each with its exact occurrence count (skipped otherwise, as in CI).
- `src/tests/structure/test_cli.py::RuntimeCheck`: the CI runtime check's version, implementation, GIL and machine rules, and its exit status as a process.
- `src/tests/guide/test_refresh_views.py`: the guide generator, run on the vendored guide into a temporary folder, writes exactly the committed guide source, HTML notes and recency export; its route and TeX rules on broken inputs.

## Infrastructure moves

| Old path | New path |
| --- | --- |
| `tools/check_compendium.py` | `src/trading_notes/cli/check_compendium.py` (`python -m trading_notes.cli.check_compendium`) |
| `tools/check_coverage.py` | `src/trading_notes/cli/check_coverage.py` (`python -m trading_notes.cli.check_coverage`) |
| `tests/` | `src/tests/` |
| `typings/` | `src/typings/` |
| (new) | `src/trading_notes/numerical/repository.py`: the `--root` option of examples that read repository files |
| `src/trading_notes/numerical/records.py` | `src/trading_notes/records.py`: the `Record` and `MutableRecord` bases, shared by every package |
| `guide/refresh_views.py` | `src/trading_notes/guide/` (`python -m trading_notes.guide.refresh_views --root <repo>`): `refresh_views`, `routes`, `catalogue`, `charts`, `tex_text` and the verbatim templates as package data in `templates/` |
| `notes/artefacts/ruff.toml`, `make examples` | removed: nothing outside `src/` is linted, type-checked or run |
| the inline Python of CI's "Verify supported Python runtime" step | `src/trading_notes/cli/check_runtime.py` (`python -m trading_notes.cli.check_runtime`): `Runtime` checks CPython, the `.python-version` release, the GIL and the x86_64 machine |
| (new) | `src/trading_notes/research/`: the research workflows, with `workflow.WorkflowArguments` (`--root`, `--output`), `fred`, `spreadsheets` and `regressions` |
| `notes/artefacts/<topic>/` data, results and protocols | `src/data/<subsection>/{inputs,results,protocols}/`, read through `trading_notes.data_folders.DataFolder`; see [Research data and the model reference](#research-data-and-the-model-reference) |
| `notes/artefacts/market-making-lob/model-derivations.tex` | `model-derivations/model-reference.tex` and one file per model (`make model-reference`) |

## Retired artefact scripts

The scripts below are gone; each row names the module that replaces it and the note that owns its entries. Dated records still cite the old paths: the review records (`notes/log.md`, `notes/source-review-records.md`, `notes/entry-evidence.json`), the protocols written before their runs (now in `src/data/<subsection>/protocols/`) and the superseded runs' notes (removed with their runs; see the relocation table below). Read them through this table.

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
| `notes/artefacts/commodity-hedging/jet_fuel_hedge_test.py` | `trading_notes.research.futures_hedging.jet_fuel_hedge` | `compendium/energy-commodities/futures-hedging.tex` |
| `notes/artefacts/commodity-investment/commodity-return-checks.py` | `trading_notes.numerical.commodity_futures_investing.commodity_returns_checks` | `compendium/commodity-investing-premia/commodity-futures-investing.tex` (also commodity-return-components.tex and commodity-indices.tex) |
| `notes/artefacts/commodity-storage-curves/backwardation_test.py` | `trading_notes.research.commodity_curves.backwardation` | `compendium/energy-commodities/commodity-curves.tex` |
| `notes/artefacts/commodity-storage-curves/energy-checks.py` | `trading_notes.numerical.commodity_curves.energy_checks` | `compendium/energy-commodities/commodity-curves.tex` |
| `notes/artefacts/commodity-storage-curves/heating_oil_test.py` | `trading_notes.research.commodity_curves.heating_oil` | `compendium/energy-commodities/commodity-curves.tex` |
| `notes/artefacts/commodity-storage-curves/hedging_pressure_test.py` | `trading_notes.research.commodity_curves.hedging_pressure` | `compendium/energy-commodities/commodity-curves.tex` |
| `notes/artefacts/corporate-credit-capital/credit-cds-securitisation-checks.py` | `trading_notes.numerical.credit_risk_analysis.credit_cds_securitisation_checks` | `compendium/corporate-credit-capital/credit-risk-analysis.tex`; also cited by `credit-default-swaps.tex`, `government-bond-markets/sovereign-credit.tex` and `securitised-structured-credit/securitisation.tex` |
| `notes/artefacts/corporate-finance/corporate-finance-checks.py` | `trading_notes.numerical.corporate_finance.corporate_finance_checks` | corporate-finance (six subsections; most entries in corporate-ownership-governance) |
| `notes/artefacts/corporate-finance/country-risk-premium-check.py` | `trading_notes.numerical.capital_structure_cost_of_capital.country_risk_premium_checks` | `compendium/corporate-finance/capital-structure-cost-of-capital.tex` |
| `notes/artefacts/counterparty-xva/counterparty-capital-check.py` | `trading_notes.numerical.counterparty_xva.counterparty_capital_checks` | `compendium/portfolio-risk-financing/counterparty-xva.tex` |
| `notes/artefacts/counterparty-xva/counterparty-xva-checks.py` | `trading_notes.numerical.counterparty_xva.counterparty_xva_checks` | `compendium/portfolio-risk-financing/counterparty-xva.tex` |
| `notes/artefacts/credit-portfolios/credit-portfolio-checks.py` | `trading_notes.numerical.credit_portfolio_management.credit_portfolios_checks` | `compendium/corporate-credit-capital/credit-portfolio-management.tex` |
| `notes/artefacts/crypto-mm-microstructure/funding_checks.py` | `trading_notes.numerical.crypto_venues_perpetuals.perpetual_funding_checks` | `compendium/digital-assets-prediction-markets/crypto-venues-perpetuals.tex` |
| `notes/artefacts/crypto-perpetuals/amm-checks.py` | `trading_notes.numerical.amm_lending.amm_pool_checks` | `compendium/onchain-protocols/amm-lending.tex` |
| `notes/artefacts/crypto-perpetuals/deribit-options-snapshot.py` | `trading_notes.research.crypto_venues_perpetuals.deribit_options` | `compendium/digital-assets-prediction-markets/crypto-venues-perpetuals.tex` |
| `notes/artefacts/crypto-perpetuals/okx-options-snapshot.py` | `trading_notes.research.crypto_venues_perpetuals.okx_options` | `compendium/digital-assets-prediction-markets/crypto-venues-perpetuals.tex` |
| `notes/artefacts/currency-management/currency-management-checks.py` | `trading_notes.numerical.currency_management.currency_management_checks` | `compendium/currency-markets/currency-management.tex` |
| `notes/artefacts/curve-term-structure/gsw-kw-acm.py` | `trading_notes.research.gsw_treasury_curve.curve_checks` | `compendium/rates-credit-mortgages/gsw-treasury-curve.tex` |
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
| `notes/artefacts/financial-statement-analysis/intercorporate-fx-institutions-checks.py` | `trading_notes.numerical.financial_statement_analysis.intercorporate_fx_institutions_checks` | `compendium/financial-statement-analysis/intercorporate-investments.tex` (also foreign-currency-reporting.tex and financial-institution-analysis.tex) |
| `notes/artefacts/financial-statement-analysis/statement-analysis-checks.py` | `trading_notes.numerical.company_case.statement_analysis_checks` | financial-statement-analysis/company-case (case used across the section) |
| `notes/artefacts/firms-market-structure/market-structure-checks.py` | `trading_notes.numerical.firms_market_structure.market_structure_checks` | `compendium/systematic-equities/firms-market-structure.tex` |
| `notes/artefacts/fixed-income-portfolio/fixed-income-portfolio-checks.py` | `trading_notes.numerical.fixed_income_portfolio_management.fixed_income_portfolio_checks` | `compendium/rates-credit-mortgages/fixed-income-portfolio-management.tex`; also cited by `portfolio-risk-financing/liability-matching.tex` |
| `notes/artefacts/forward-swap-valuation/cross-currency-basis-check.py` | `trading_notes.numerical.forward_commitment_valuation.cross_currency_basis_checks` | `compendium/volatility-options/forward-commitment-valuation.tex` |
| `notes/artefacts/forward-swap-valuation/forward-swap-checks.py` | `trading_notes.numerical.forward_commitment_valuation.forward_swap_valuation_checks` | `compendium/volatility-options/forward-commitment-valuation.tex` |
| `notes/artefacts/funding-crowding/spiral-checks.py` | `trading_notes.numerical.crowding_contagion.margin_spiral_checks` | `compendium/portfolio-risk-financing/crowding-contagion.tex` |
| `notes/artefacts/fx-determination-forecasting/fx-checks.py` | `trading_notes.numerical.macro_fx.fx_checks` | `compendium/currency-markets/macro-fx.tex` |
| `notes/artefacts/fx-determination-forecasting/fx-panel-inference-check.py` | `trading_notes.numerical.macro_fx.fx_panel_inference_checks` | `compendium/currency-markets/macro-fx.tex` |
| `notes/artefacts/fx-determination-forecasting/fx_carry_test.py` | `trading_notes.research.macro_fx.carry_out_of_sample` | `compendium/currency-markets/macro-fx.tex` |
| `notes/artefacts/fx-determination-forecasting/fx_ppp_oos_test.py` | `trading_notes.research.macro_fx.ppp_out_of_sample` | `compendium/currency-markets/macro-fx.tex` |
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
| `notes/artefacts/macro-regimes-stock-bond/deflation_row_test.py` | `trading_notes.research.macro_regimes_data.deflation_row` | `compendium/multi-asset-systematic-macro/macro-regimes-data.tex` |
| `notes/artefacts/macro-regimes-stock-bond/inflation_quarterly_test.py` | `trading_notes.research.macro_regimes_data.inflation_quarterly` | `compendium/multi-asset-systematic-macro/macro-regimes-data.tex` |
| `notes/artefacts/macro-regimes-stock-bond/inflation_regime_test.py` | `trading_notes.research.macro_regimes_data.inflation_regime` | `compendium/multi-asset-systematic-macro/macro-regimes-data.tex` |
| `notes/artefacts/macro-regimes-stock-bond/regime-checks.py` | `trading_notes.numerical.macro_regimes_data.regime_checks` | `compendium/multi-asset-systematic-macro/macro-regimes-data.tex` |
| `notes/artefacts/macro-regimes-stock-bond/regime_recession_test.py` | `trading_notes.research.macro_regimes_data.regime_recession` | `compendium/multi-asset-systematic-macro/macro-regimes-data.tex` |
| `notes/artefacts/manager-selection/manager-selection-checks.py` | `trading_notes.numerical.manager_selection.manager_selection_checks` | `compendium/portfolio-construction-risk/manager-selection.tex` |
| `notes/artefacts/market-index-construction/index-construction-checks.py` | `trading_notes.numerical.index_construction.index_construction_checks` | `compendium/international-equity-markets/index-construction.tex` |
| `notes/artefacts/market-making-lob/model-checks.py` | `trading_notes.numerical.market_making_models.lob_models_checks` | `compendium/execution-market-making/market-making-models.tex` |
| `notes/artefacts/market-making-lob/model-derivations-checks.py` | `trading_notes.numerical.market_making_models.lob_model_derivations_checks` | `compendium/execution-market-making/market-making-models.tex` |
| `notes/artefacts/market-risk-measurement/market-risk-checks.py` | `trading_notes.numerical.market_risk_measurement.market_risk_measurement_checks` | `compendium/portfolio-construction-risk/market-risk-measurement.tex` |
| `notes/artefacts/market-simulation/order-flow-checks.py` | `trading_notes.numerical.order_flow_statistics.order_flow_checks` | `compendium/execution-market-making/order-flow-statistics.tex` |
| `notes/artefacts/market-structure-execution-quality/order-routing-fragmentation-checks.py` | `trading_notes.numerical.dark_trading_fragmentation.order_routing_fragmentation_checks` | `compendium/execution-trading-costs/dark-trading-fragmentation.tex` |
| `notes/artefacts/model-governance-controls/reconciliation-check.py` | `trading_notes.numerical.trading_controls.order_reconciliation_checks` | `compendium/research-engineering-validation/trading-controls.tex` |
| `notes/artefacts/multi-asset-systematic-macro/carry-market-statistics-checks.py` | `trading_notes.numerical.multi_asset_systematic_macro.carry_market_statistics_checks` | multi-asset-systematic-macro (currency-markets/macro-fx.tex, rates-credit-mortgages/interest-rates.tex and monetary-policy-curves.tex, macro-regimes-data.tex, execution-market-making/order-books.tex and high-frequency-trading.tex) |
| `notes/artefacts/multi-asset-systematic-macro/convexity-curve-signals-checks.py` | `trading_notes.numerical.multi_asset_systematic_macro.convexity_curve_signals_checks` | multi-asset-systematic-macro (rates-credit-mortgages/interest-rates.tex, business-cycles-policy.tex, global-macro.tex, physical commodities, currency-markets/currency-carry.tex) |
| `notes/artefacts/multi-asset-systematic-macro/global_macro_down_months_2014_test.py` | `trading_notes.research.global_macro.down_months_2014` | `compendium/multi-asset-systematic-macro/global-macro.tex` |
| `notes/artefacts/multi-asset-systematic-macro/global_macro_down_months_test.py` | `trading_notes.research.global_macro.down_months` | `compendium/multi-asset-systematic-macro/global-macro.tex` |
| `notes/artefacts/multi-asset-systematic-macro/h15_monthly.py` | `trading_notes.research.business_cycles_policy.h15_spread` | `compendium/multi-asset-systematic-macro/business-cycles-policy.tex` |
| `notes/artefacts/multi-asset-systematic-macro/inversion-horizons.py` | `trading_notes.research.business_cycles_policy.inversion_horizons` | `compendium/multi-asset-systematic-macro/business-cycles-policy.tex` |
| `notes/artefacts/multi-asset-systematic-macro/macro-pricing-risk-checks.py` | `trading_notes.numerical.global_macro.macro_pricing_risk_checks` | `compendium/multi-asset-systematic-macro/global-macro.tex` (parts also serve rates-credit-mortgages/monetary-policy-curves.tex and execution-trading-costs/futures-execution.tex) |
| `notes/artefacts/multi-asset-systematic-macro/ust_monthly.py` | `trading_notes.research.business_cycles_policy.treasury_spread` | `compendium/multi-asset-systematic-macro/business-cycles-policy.tex` |
| `notes/artefacts/numerical-pricing/monte-carlo-greeks-check.py` | `trading_notes.numerical.monte_carlo_simulation.monte_carlo_greeks_checks` | `compendium/numerical-optimisation/monte-carlo-simulation.tex` |
| `notes/artefacts/numerical-pricing/numerical-pricing-checks.py` | `trading_notes.numerical.numerical_methods.numerical_pricing_checks` | `compendium/numerical-optimisation/numerical-methods.tex` |
| `notes/artefacts/option-pricing-models/option-model-checks.py` | `trading_notes.numerical.option_pricing.option_models_checks` | `compendium/volatility-options/option-pricing.tex` |
| `notes/artefacts/option-strategies/option-strategy-checks.py` | `trading_notes.numerical.option_strategies.option_strategies_checks` | `compendium/volatility-options/option-strategies.tex` |
| `notes/artefacts/option-valuation/dividend-tree-swaption-checks.py` | `trading_notes.numerical.option_valuation.dividend_tree_swaption_checks` | `compendium/volatility-options/option-valuation.tex` |
| `notes/artefacts/option-valuation/option-valuation-checks.py` | `trading_notes.numerical.option_valuation.option_valuation_checks` | `compendium/volatility-options/option-valuation.tex` |
| `notes/artefacts/option-valuation/transaction-cost-hedging-check.py` | `trading_notes.numerical.option_hedging.transaction_cost_hedging_checks` | `compendium/volatility-options/option-hedging.tex` |
| `notes/artefacts/option-valuation/volatility-mismatch-hedging-check.py` | `trading_notes.numerical.option_hedging.volatility_mismatch_hedging_checks` | `compendium/volatility-options/option-hedging.tex` |
| `notes/artefacts/performance-evaluation/performance-evaluation-checks.py` | `trading_notes.numerical.performance_attribution_appraisal.performance_evaluation_checks` | `compendium/portfolio-construction-risk/performance-attribution-appraisal.tex` |
| `notes/artefacts/performance-presentation-standards/gips-checks.py` | `trading_notes.numerical.performance_standards.gips_checks` | `compendium/portfolio-construction-risk/performance-standards.tex` |
| `notes/artefacts/point-in-time-data/bitemporal-check.py` | `trading_notes.numerical.point_in_time_data.bitemporal_checks` | `compendium/research-engineering-validation/point-in-time-data.tex` |
| `notes/artefacts/point-in-time-data/filing-checks.py` | `trading_notes.numerical.point_in_time_data.filing_deadlines_checks` | `compendium/research-engineering-validation/point-in-time-data.tex` |
| `notes/artefacts/point-in-time-data/filing-timestamp-checks.py` | `trading_notes.numerical.point_in_time_data.filing_timestamps_checks` | `compendium/research-engineering-validation/point-in-time-data.tex` |
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
| `notes/artefacts/rates-credit-mortgages/acm-term-premium-summary.py` | `trading_notes.research.gsw_treasury_curve.acm_term_premium` | `compendium/rates-credit-mortgages/gsw-treasury-curve.tex` |
| `notes/artefacts/rates-credit-mortgages/fra-settlement-check.py` | `trading_notes.numerical.rate_swaps_clearing.fra_settlement_checks` | `compendium/rates-credit-mortgages/rate-swaps-clearing.tex` |
| `notes/artefacts/rates-credit-mortgages/multicurve-check.py` | `trading_notes.numerical.rate_swaps_clearing.multicurve_checks` | `compendium/rates-credit-mortgages/rate-swaps-clearing.tex` |
| `notes/artefacts/rates-credit-mortgages/yield-shift-check.py` | `trading_notes.numerical.interest_rates.yield_shift_checks` | `compendium/rates-credit-mortgages/interest-rates.tex` |
| `notes/artefacts/real-assets/real-asset-checks.py` | `trading_notes.numerical.real_asset_investor.real_assets_checks` | real-asset-investor (real-estate.tex parts 1-4, infrastructure.tex part 5, land-timber-farmland.tex part 6) |
| `notes/artefacts/reinforcement-learning-trading/cartea_jaimungal_checks.py` | `trading_notes.numerical.execution_control.cartea_jaimungal_checks` | `compendium/execution-trading-costs/execution-control.tex` |
| `notes/artefacts/return-predictability/conditional-predictive-ability-checks.py` | `trading_notes.numerical.return_predictability.conditional_predictive_ability_checks` | `compendium/asset-pricing/return-predictability.tex` |
| `notes/artefacts/return-predictability/forecast-combination-scoring-checks.py` | `trading_notes.numerical.return_predictability.forecast_combination_scoring_checks` | `compendium/asset-pricing/return-predictability.tex` |
| `notes/artefacts/return-predictability/goyal_extract.py` | `trading_notes.research.return_predictability.goyal_extract` | `compendium/asset-pricing/return-predictability.tex` |
| `notes/artefacts/return-predictability/goyal_extract_predictors.py` | `trading_notes.research.return_predictability.goyal_extract_predictors` | `compendium/asset-pricing/return-predictability.tex` |
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
| `notes/artefacts/term-structure-dynamics/gsw-month-end-extract.py` | `trading_notes.research.term_structure_returns.gsw_month_end` | `compendium/rates-credit-mortgages/term-structure-returns.tex` |
| `notes/artefacts/term-structure-dynamics/term-structure-checks.py` | `trading_notes.numerical.term_structure_returns.term_structure_checks` | `compendium/rates-credit-mortgages/term-structure-returns.tex` |
| `notes/artefacts/time-series-models/time-series-checks.py` | `trading_notes.numerical.time_series_models.time_series_checks` | `compendium/regression-time-series/time-series-models.tex` |
| `notes/artefacts/time-value-returns/time-value-return-checks.py` | `trading_notes.numerical.financial_mathematics.time_value_returns_checks` | `compendium/financial-mathematics/time-value.tex` (also return-measurement.tex) |
| `notes/artefacts/trade-execution/trade-execution-checks.py` | `trading_notes.numerical.trade_strategy_governance.trade_execution_checks` | `compendium/execution-trading-costs/trade-strategy-governance.tex` |
| `notes/artefacts/volatility-options/bsm-svi-checks.py` | `trading_notes.numerical.option_pricing.bsm_svi_checks` | `compendium/volatility-options/option-pricing.tex` |
| `notes/artefacts/volatility-options/negative-hedge-ratio-check.py` | `trading_notes.numerical.futures_hedging.negative_hedge_ratio_checks` | `compendium/energy-commodities/futures-hedging.tex` |

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
| (script only) `energy-checks.py` | `commodity_curves.nymex_contracts` (now also used by the commodity research workflows, with heating oil as a third market), `commodity_curves.energy_checks` |
| (script only) `fx-checks.py` | `macro_fx.ppp_forecasts` (also imported by `research.macro_fx.ppp_out_of_sample`), `macro_fx.fx_checks` |
| `financial_ml_methods` | `machine_learning_methods.learners`, `machine_learning_methods.financial_ml_methods_checks` |
| `institutional_portfolios` | `institutional_portfolios.plan_rules`, `institutional_portfolios.institutional_portfolios_checks` |
| `private_capital` | `alternative_investment_structures.hedge_fund_fees`, `private_fund_structures.waterfalls`, `private_equity_strategies.leveraged_buyout`, `private_debt_special_situations.restructuring`, `internal_rate` (new support module), `private_capital_allocator.private_capital_checks` |
| `private_wealth` | `wealth_planning.household_plan`, `wealth_preservation.us_income_tax`, `wealth_preservation.tax_drag`, `wealth_transfer.transfer_rules`, `private_wealth_management.private_wealth_checks` |
| (new) | `us_calendar`: weekday arithmetic and federal holidays shared by the order-book, futures and SOFR examples |
| (new) | `internal_rate`: the IRR (Brent's method on a fixed bracket) shared by the real-asset and private-capital examples |

## Inventory of Python outside `src/`

Counted on 2026-10-25 with `git ls-files -co --exclude-standard '*.py' '*.pyi'` on the final working tree: 0 files outside `src/`, 528 inside it: 505 modules, all checked by mypy, and 23 `.pyi` stubs in `src/typings/`, read through `mypy_path`. No configuration file or script holds a Python program: the CI runtime check was the last one.

| Kind | Before the final batch | Now |
| --- | --- | --- |
| Forwarding wrappers in `notes/artefacts/` | 10 | 0: deleted; their flat modules moved into subsection packages |
| Research and data scripts in `notes/artefacts/` | 22 | 0: `src/trading_notes/research/<topic>/` |
| Historical runs in `notes/artefacts/**/superseded-*/` | 8 | 0: removed after checking that `git show <commit>:<path>` gives each byte for byte; each superseded folder's README named the commit and the command. The folders' remaining data files and READMEs were removed in the research-data migration and are recoverable at `684b3a0` |
| `guide/refresh_views.py` | 1 | 0: `src/trading_notes/guide/` |
| Flat example modules in `src/trading_notes/numerical/` | 10 | 0 |

The support modules left directly in `src/trading_notes/numerical/` are `__init__`, `internal_rate`, `newey_west`, `report`, `repository`, `tolerance` and `us_calendar`.

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

### The final batch: flat modules, research workflows, the guide generator and cleanup

| Part | What moved | Evidence |
| --- | --- | --- |
| Ten flat modules | `bitemporal`, `filing_deadlines`, `filing_timestamps` into `point_in_time_data` (`split_history`, `edgar_filings`, three `*_checks`); `margin_spiral` into `crowding_contagion` (`liquidity_spiral`, `margin_spiral_checks`); `negative_hedge_ratio` into `futures_hedging` (`hedge_ratio`); `numerical_pricing` into `numerical_methods` (`put_pricing`, `least_squares_monte_carlo`); `order_reconciliation` into `trading_controls` (`order_state`); `order_routing_fragmentation` into `dark_trading_fragmentation` (`venue_shares`), with `order_books.order_instructions` and `smart_order_routing.venue_allocation`; `time_value_returns` into `financial_mathematics` with `time_value.cash_flows`; `intercorporate_fx_institutions` into `financial_statement_analysis` with `intercorporate_investments`, `foreign_currency_reporting` and `financial_institution_analysis`. Their four dataclass modules became records; `us_calendar` gained the business-day rules they share | Every entrypoint's output, run from an empty folder, byte-identical to its pre-migration run except four headings of the order-routing example that lose "(corrected 2026-10-16)" |
| Research scripts | The 22 scripts as 22 workflows in 10 topic packages; each takes `--root` and `--output` and its inputs as arguments, and writes to its artefact folder unless `--output` is given. `heating_oil` no longer patches the backwardation script's globals: `nymex_contracts` has heating oil as a market | Replayed from an unrelated folder into a scratch folder (before the repairs below reworded nine labels): every stdout and output file equals the retained evidence, except `regime_quarters.csv`, whose retained copy prints one zero as `-0.000` where the original script and the workflow print `0.000`, and five stdouts never retained (H.15, Treasury, both Goyal extracts and the GSW month-end extract), which equal the original scripts' runs. The jet-fuel hedge, broken at `fe1da20` when the heating-oil patch stopped being imported, reproduces its retained results again |
| Guide generator | `guide/refresh_views.py` as `src/trading_notes/guide/`, pydantic records for the route file (`extra="forbid"`), typed throughout | Guide source, HTML notes and recency export byte-identical to the committed files; the copied `guide/` tree equals the reading-list commit's tree less `refresh_views.py` |
| Structure and records | The structural checkers' dataclasses became records; `records.py` moved to `trading_notes.records` | Compendium and coverage reports identical, text and JSON |
| Domain classes left from earlier batches | `regulatory_capital` (SA-CCR and BA-CVA records); `bond_pricing_yields.FixedRateBond` in place of five bond functions; `fixed_income_portfolio_management.CashFlows` in place of `(amounts, times)` tuples; `company_case`: the FCFF routes as `YearForecast` methods and `VestedOptions`; `capital_structure_cost_of_capital.RatingSchedule`; one `annuity` factor in `time_value.cash_flows` instead of three copies, and `CashFlowStream.npv` instead of a second `npv`; `CovarianceModel.long_only_minimum_variance`. Six `typing.cast` calls replaced by typed conversions | All 130 entrypoints byte-identical before and after |
| Repository | `make examples`, `notes/artefacts/ruff.toml`, the E501 and mypy file lists and every lint or type exemption removed; Makefile, pre-commit, pyproject, README and the installation test updated; module docstrings cut to one purpose sentence; 103 live references in `compendium/`, `notes/pathways/`, `notes/readings/` and `notes/coverage/` rewritten to module names, and the compendium's module names set with `\nolinkurl` so that they break (the PDF has no overfull boxes) | See validation below |

### Repairs of the final batch

An audit of the uncommitted final batch found one contract defect, research workflows whose domain logic was still procedural beside an `Arguments` record, process-history wording in printed labels, and a Python program inside the CI workflow.

| Finding | Origin | Repair | Validation |
| --- | --- | --- | --- |
| `ContractCalendar.same_contract` compared optional delivery months directly, and `jet_fuel_hedge.WeeklyChanges.of` compared `calendar.delivery(a)` with `calendar.delivery(b)`, so two unknown months (None == None) counted as one contract. On weekdays from 1 January to 23 October 2026, the WTI front month is unknown on 16 and 23 October, yet `same_contract` returned True and the week was kept | pre-existing in `same_contract` (the backwardation script); the jet-fuel comparison was its own copy | `same_contract` holds only when every identity rule gives a known delivery month on both dates and the months agree; `WeeklyChanges.of` calls it instead of comparing months itself, so both callers drop unknown identities. The market rules are unchanged: gas needs offsets 3, 5 and 6, crude and heating oil one rule | Reproduced before the fix with the 2026 calendar. `test_nymex_contracts.UnknownIdentity` (both unknown, one unknown in either order, known match, known roll) and `test_gas_identity_needs_every_offset`; `test_workflows.JetFuelWeeks` (the roll week, both unknown-identity weeks dropped, 42 weeks in all). With the old comparison patched back in, `test_both_unknown` fails. No retained number changes: in the retained EIA data, the jet-fuel weeks end on 5 April 2024, the futures' last day, and no backwardation, heating-oil or jet-fuel pair has an unknown delivery month under any rule (counted: 0 for WTI, NG, HO and both hedges) |
| Research workflows kept their domain logic in module functions | incomplete extraction | `business_cycles_policy`: `H15Release` (SDMX parsing, daily extract), `ParYieldFiles`, `DailyRows.months`, `.complete` and `.write_monthly` in place of `check_consecutive` and `complete`, and `SpreadArguments`, the `--extract` option both spreads share; `inversion_horizons.Inversions`. `global_macro`: `IndexMonths` (the monthly table, its statistics, subsets and verdict, shared by both down-month workflows) and `IndexWorkbook` (in place of `barclay_workbook`, with its window and revision check). `gsw_treasury_curve`: `SvenssonCurve`, `RecomputedYields`, `TermPremia`, `TenYearPremium`. `term_structure_returns.MonthEndYields`. `return_predictability`: `GoyalWorkbook` and `GoyalArguments`, shared by both extracts. `crypto_venues_perpetuals`: `Instruments.listings`, `OptionBook`, `OptionSnapshot`. `commodity_curves`: `CurvePanel.build` returns a `CurveSample` (exclusions, scarcity fits, the executable rule, the WTI and gas report), `CurvePanel.print_roll_check`, and `TimingRule`, shared by the settlement and executable variants of both markets and by heating oil; `HeatingOilSample`, `HedgingSample`. `futures_hedging`: `WeeklyChanges.report`. `macro_fx`: `CarryPanel`, `PppPanel`, and `RandomWalkComparison` and `turnover` in `currencies`, shared by both. `macro_regimes_data`: `VintageQuarters` and `ResponseDifference`, shared by the three vintage rows, `VintageLabels`, `RegimeQuarters`. Each `main` parses its arguments, builds these records and prints. Small pure helpers remain where a class adds nothing: the FRED, spreadsheet and French readers, `bond_equivalent`, `mean_spread`, `ols_h`, `largest`, `below_zero`, `summarise_returns`, `log_change`, `welch_t`, `indicator_slope`, `episodes` | Every workflow, run old and new from an unrelated folder with `-W error` into scratch folders: identical stdout and files except the reworded labels below, including the five stdouts never retained and `regime_quarters.csv` (which differs from its retained copy only by the known `-0.000`). New unit tests: `SharedStatistics`, `test_daily_extracts`, the rewritten `test_month_coverage` |
| Printed labels and one CSV column described earlier runs and reviews | carried over from the scripts, and kept deliberately by the final batch | Neutral labels, every number unchanged: "superseded row-stacked t" -> "row-stacked t" (PPP and carry, twice each); "superseded simple-return P" -> "simple-return P" and the column `r_simple_superseded` -> `r_simple` (heating oil); "the v2 executable rule" -> "the executable rule"; "roll weeks dropped" -> "weeks excluded (roll or unknown contract)" (jet fuel, twice: `WeeklyChanges.of` also excludes weeks whose contract 1 is unknown); "exploratory (added after the v1 run, not pre-specified)" -> "exploratory (not pre-specified)" (backwardation, twice); "the audited snapshot" -> "the recorded snapshot" and "method validation (2026-10-17)'s page values" -> "the index page's values of 2026-10-17" (2014 down months; the 55 months are now counted, not written); "empirical extensions (2026-10-17) used 111 monthly vintages" -> "the monthly-vintage test uses 111 vintages" (quarterly inflation row); the 2014 workflow's docstring names `down_months` instead of "the page run"; a test comment that dated an audit. The retained outputs are evidence the notes cite and stay unchanged; the replay test maps each reworded label explicitly, with its occurrence count, and compares everything else byte for byte | `RetainedEvidence.test_replays` with `RELABELLED`; `test_relabelled_files_are_replayed` |
| CI's "Verify supported Python runtime" step ran an inline Python program | final batch | `trading_notes.cli.check_runtime`: the `Runtime` record and `main`, run by CI as `uv run --frozen --no-editable python -m trading_notes.cli.check_runtime`. It keeps the checks: CPython, the version in `.python-version`, the GIL enabled and not a free-threaded build, and the x86_64 machine; a failure is named on stderr with status 1 instead of an AssertionError. No other configuration file or script holds Python | `test_cli.RuntimeCheck`; the import side-effect test covers the new module. Locally (macOS arm64) it exits 1 by design and 0 with `--machine arm64` |

Kept as written: the recession row's "usd (v1 splice; ...)" and "ANY OVERLAP (v1 definition)" labels and its `usd_splice_v1` column name the protocol-defined series that `notes/pathways/macro-regimes-stock-bond.md` cites and that `macro_regimes_data.regime_checks` reads from the retained results; the checks that verify the retained first runs (`energy_checks`, `fx_checks`, `regime_checks`) still name them, because those runs are their subject; and "retrieved" dates, input paths such as `source-verification/empirical/` and the coverage checker's "source verification" problems, which name sources, folders and a check rather than review history.

## Research data and the model reference

The last batch moved the research data out of `notes/artefacts/` and turned the market-making derivations into a separate model reference. It started from `684b3a0bb3ee45cfb22ff41e4ea4ab98eee58734` (checked unchanged: local and remote `main` both at it, clean tree), whose `notes/artefacts/` held 72 tracked files of 2,028,614 bytes: 27 CSV, 28 TXT, 16 Markdown and one LaTeX file. Every file's SHA-256 was recorded before any change.

### Layout

```
compendium/            compendium.tex, compendium.pdf, sections, preamble.tex, house.tex
model-derivations/     README.md, model-reference.tex, model-reference.pdf
  front/               notation.tex, model-index.tex
  execution-market-making/market-making-models/
                       grossman-miller.tex, kyle-single-auction.tex,
                       static-limit-order-depth.tex, roll-spread-estimator.tex
src/
  trading_notes/       the package; data_folders.py holds DataFolder
  tests/, typings/
  data/<subsection>/   inputs/, results/, protocols/ (retained, tracked)
                       runs/local/inputs/, runs/local/results/ (written by workflows, ignored)
```

`src/data/` now holds 52 retained files in 14 subsection folders: `business_cycles_policy`, `commodity_curves`, `crypto_venues_perpetuals`, `currency_intervention`, `futures_hedging`, `global_macro`, `gsw_treasury_curve`, `macro_fx`, `macro_indicators`, `macro_regimes_data`, `portfolio_choice`, `rate_swaps_clearing`, `return_predictability` and `term_structure_returns`. Folders exist only where files do; there is no `archive/` folder, because every historical run was removed (below). The data is outside the installed package: the wheel holds only `src/trading_notes/`, and code finds the data below `--root`.

A file's role decided its folder, not its extension: source extracts (Goyal, GSW month-end, the H.15 and Treasury daily extracts, the BIS, UN and IRR extracts, the Damodaran transcription) are inputs; calculated panels, printed results and snapshots are results, even when another workflow reads them (`backwardation_monthly.csv`, `global_macro_monthly.csv`, `h15-spread-monthly.csv`); protocols are protocols. Each dataset has one owner, and consumers in other subsections read it there: `regime_inputs` reads the H.15 daily extract from `business_cycles_policy/inputs/`, `carry_market_statistics_checks` the BIS and UN extracts from `rate_swaps_clearing` and `macro_indicators`, `convexity_curve_signals_checks` the monthly spreads from `business_cycles_policy/results/`. File names are unchanged; no collision required a rename.

### Reading and writing data

- `trading_notes.data_folders.DataFolder(subsection=...)` gives a subsection's `inputs`, `results`, `run_inputs` and `run_results` paths relative to the root; numerical checks and research workflows use it in place of the former `notes/artefacts` constants (`ARTEFACTS`, the checks' `DATA` and `FOLDER`, `H15_DAILY`).
- `WorkflowArguments.folder` is a `DataFolder`. `retained_inputs` and `retained_results` are read by default; `output_folder` (new results) and `extract_folder` (rebuilt extracts) default to `runs/local/results/` and `runs/local/inputs/` and are created on use; `--output` sends every written file to one folder instead. The Goyal and GSW extract workflows write to `extract_folder`, as does `--extract` in the H.15 and Treasury spread workflows. Normal runs cannot overwrite a retained file.
- `WorkflowArguments.upstream(requested, retained)` reads another workflow's output: the retained file, or a requested generated file or run folder holding it under the same name. A requested file that does not exist raises `FileNotFoundError: requested input not found: <path>` before anything is printed or written, with no fallback. Options: `--spreads` (`inversion_horizons`), `--backwardation` (`hedging_pressure`), `--page-months` (`down_months_2014`), `--h15-daily` (`deflation_row`, `inflation_quarterly`, `inflation_regime`, which now share `regime_inputs.RowArguments`).
- `.gitignore` ignores `/src/data/*/runs/` only; retained files and sources stay visible.

### Relocation and removal

52 files moved with `git mv` and match their recorded hashes byte for byte. While the batch was in progress the owner asked for the historical runs of `commodity_curves`, `macro_fx`, `macro_regimes_data` and `return_predictability` to be removed rather than archived: those 19 files (the six `superseded-*` folders and `conditional-predictive-ability-first-run.txt`) are deleted and recoverable with `git show 684b3a0:notes/artefacts/<old path>`. The LaTeX file became the model reference. The retained files of other subsections, including protocols that cite their first runs or old paths, are unchanged; read such citations through this table. Old paths are relative to `notes/artefacts/`, new paths to `src/data/`.

| Old path | New path or outcome | SHA-256 at `684b3a0` |
| --- | --- | --- |
| `commodity-hedging/jet-fuel-hedge-protocol.md` | `futures_hedging/protocols/jet-fuel-hedge-protocol.md` | `36bda2c56a3da561ef75e57c7c8a74d8e308963c21f876c272bf068e6b0b0bd2` |
| `commodity-hedging/jet_fuel_hedge_results.txt` | `futures_hedging/results/jet_fuel_hedge_results.txt` | `debb5152d004b4cfbf9aec79236a127e462b25c235f357567be2158809a3c004` |
| `commodity-storage-curves/backwardation_monthly.csv` | `commodity_curves/results/backwardation_monthly.csv` | `2eab519ec517c89feaa25642a65d3599c30214c7149bbe01e750f085b5b312da` |
| `commodity-storage-curves/backwardation_results.txt` | `commodity_curves/results/backwardation_results.txt` | `a197c5e718db7d3d1fc34e0d264031db4fd06d68b3c13a5570126cb756875836` |
| `commodity-storage-curves/heating-oil-protocol.md` | `commodity_curves/protocols/heating-oil-protocol.md` | `76ef8ce2143ba72ff087c29b0ca17d43e411b93a4236a549556747d95912b2f0` |
| `commodity-storage-curves/heating_oil_monthly.csv` | `commodity_curves/results/heating_oil_monthly.csv` | `f6d19401cec854298842ba693aefbafe22d8185b46a89395734f4e549811e656` |
| `commodity-storage-curves/heating_oil_results.txt` | `commodity_curves/results/heating_oil_results.txt` | `5b8385467551f24df04b6c22d4652b1acdad4b272c386ca9b2fe473aa255c764` |
| `commodity-storage-curves/hedging-pressure-protocol.md` | `commodity_curves/protocols/hedging-pressure-protocol.md` | `afc54afcecfc7fd81b962dba04e288f28829f72a059bfec28d2ff48f862eb741` |
| `commodity-storage-curves/hedging_pressure_monthly.csv` | `commodity_curves/results/hedging_pressure_monthly.csv` | `89485d4c53ced2eb9b068710b79b48100eba733f932afe6bd1b2a5826e05ced7` |
| `commodity-storage-curves/hedging_pressure_results.txt` | `commodity_curves/results/hedging_pressure_results.txt` | `f2dda56e91f70f934968aa0a9290d406f315c3d43fb10aa08c2c9378986eb6b1` |
| `commodity-storage-curves/superseded-first-run/README.md` | removed (archive) | `721d914e5f3e6fd5e232a0b8fa1a31842aedfba710166a0870d17c1bca91929b` |
| `commodity-storage-curves/superseded-first-run/backwardation_monthly.csv` | removed (archive) | `6953ecd1f92fab4038994cacfca96cca867e8e8b6196b59e809f93c77a3d8c2e` |
| `commodity-storage-curves/superseded-first-run/backwardation_results.txt` | removed (archive) | `9783f4c4e65bfed4dd6398029cd0800cd45e808968d099655a38ff78a445dd7b` |
| `commodity-storage-curves/superseded-simple-return-run/README.md` | removed (archive) | `e1bed3753a4b899d9a685974f0e32af76c682f492274c92fd4fd23b45826a001` |
| `commodity-storage-curves/superseded-simple-return-run/heating_oil_monthly.csv` | removed (archive) | `2352697797d0bcf85b731d5a3c66d16953863b70f1c13e8cf826549ca5b29f7f` |
| `commodity-storage-curves/superseded-simple-return-run/heating_oil_results.txt` | removed (archive) | `3e963fcdf9f504ea14018176967c89a69e6edaa304c562a3ffc06ed073534e69` |
| `crypto-perpetuals/deribit-options-snapshot.txt` | `crypto_venues_perpetuals/results/deribit-options-snapshot.txt` | `e99a6a95dbfdbbeca05d00da490e241173fba0321ba7df1f327926221d7bf95c` |
| `crypto-perpetuals/okx-options-snapshot.txt` | `crypto_venues_perpetuals/results/okx-options-snapshot.txt` | `508677befe300d600d0c1531990d9add861426d355e5395587196ae9f7dc52e1` |
| `curve-term-structure/gsw-kw-acm.txt` | `gsw_treasury_curve/results/gsw-kw-acm.txt` | `2ff9aaa2b9e4eb144e17f3a152500cd2a6ebe5db506dcee2ec9ac34ca795693c` |
| `fx-determination-forecasting/fx-carry-protocol.md` | `macro_fx/protocols/fx-carry-protocol.md` | `c6b27f2c3414e05a446e70847e74adb06dc40c9b7fdefdc91d11fc4492b3ab4d` |
| `fx-determination-forecasting/fx_carry_monthly.csv` | `macro_fx/results/fx_carry_monthly.csv` | `da23b9e5dc6f1bc9bd2ac8bea4bab1cec7f59a77afdf17244008f5d42630b686` |
| `fx-determination-forecasting/fx_carry_results.txt` | `macro_fx/results/fx_carry_results.txt` | `aec365546462404b637924cef41c0215342a2a1d83c5a2633ee360129049ae3f` |
| `fx-determination-forecasting/fx_ppp_monthly.csv` | `macro_fx/results/fx_ppp_monthly.csv` | `2379a3a395851b3237a1e4a95089659ac6d15e6dd42c77712004d7d7d420def8` |
| `fx-determination-forecasting/fx_ppp_results.txt` | `macro_fx/results/fx_ppp_results.txt` | `fd948eae8cb4010036972d1b4283f88998bd713559a82a4e6c29f4a015c9b3ec` |
| `fx-determination-forecasting/superseded-first-run/README.md` | removed (archive) | `dced194ecd67aa838db2d7b12c345204c3e75733f1aad797faee7b4411cb8bc1` |
| `fx-determination-forecasting/superseded-first-run/fx_ppp_monthly.csv` | removed (archive) | `da1bb9d4d7a54df875e73d485a1a806f5e782b780dc77fd61972aeff670b1461` |
| `fx-determination-forecasting/superseded-first-run/fx_ppp_results.txt` | removed (archive) | `4c5f66c66b8ca6e884383860956e847b0b8f4566c9ec44eca9433c6b6df51f4b` |
| `fx-determination-forecasting/superseded-row-lag-inference/README.md` | removed (archive) | `acb0efaf45a85ed51f0a6df15cf73f5f59ecb0593f36ae1e6c3cab2724c1abcd` |
| `fx-determination-forecasting/superseded-row-lag-inference/fx_carry_results.txt` | removed (archive) | `cc512c368c17f882324b8602560dc25c46a4d835801b597382dfeccac1d44522` |
| `fx-determination-forecasting/superseded-row-lag-inference/fx_ppp_results.txt` | removed (archive) | `40cfe1a2cfcb258d5f8f17138105aa40c61c5d713841e8253da284c39377e971` |
| `macro-regimes-stock-bond/deflation-row-protocol.md` | `macro_regimes_data/protocols/deflation-row-protocol.md` | `5153fb80e142a39ef915bfe795f9f335c4ee6379f7cbf4dfa47a0f9b94aecd93` |
| `macro-regimes-stock-bond/deflation_quarters.csv` | `macro_regimes_data/results/deflation_quarters.csv` | `e73e6e1d49663cdbd3269553068b8fda36b47bee92720412ffea87f6588e3466` |
| `macro-regimes-stock-bond/deflation_results.txt` | `macro_regimes_data/results/deflation_results.txt` | `b1519ba2a20d1c0ab402c375e1023cc8451c44088736c623697a331d65e962c9` |
| `macro-regimes-stock-bond/inflation-row-protocol.md` | `macro_regimes_data/protocols/inflation-row-protocol.md` | `55ba56045352104a8c90390b6f9a6456cb326652bd4328602dcf1c6aaab1f26e` |
| `macro-regimes-stock-bond/inflation_monthly_vintage_quarters.csv` | `macro_regimes_data/results/inflation_monthly_vintage_quarters.csv` | `4419a9332fcd252612826e8ff573f346263012e8d8cfca22b2d965f1b158c389` |
| `macro-regimes-stock-bond/inflation_quarterly_results.txt` | `macro_regimes_data/results/inflation_quarterly_results.txt` | `c5a093d32c002542867a683343f774094c84bbdd1e131aee04a96137874f88ef` |
| `macro-regimes-stock-bond/inflation_quarterly_vintage_quarters.csv` | `macro_regimes_data/results/inflation_quarterly_vintage_quarters.csv` | `36194924fc12840f5ac074458d38a7c0a656bf644d0d9f4ee64f8a3137930745` |
| `macro-regimes-stock-bond/inflation_results.txt` | `macro_regimes_data/results/inflation_results.txt` | `6753551fc98eb80a70ef97ddf40f018d7783dff282f87aeefe37621e1a2021a5` |
| `macro-regimes-stock-bond/regime_quarters.csv` | `macro_regimes_data/results/regime_quarters.csv` | `294292e291f9d3c42a23d8a2721df2943cc97a17b64ba415f205e39a5c4ce6e7` |
| `macro-regimes-stock-bond/regime_recession_results.txt` | `macro_regimes_data/results/regime_recession_results.txt` | `b4533843d0c1250899f9620a0eea59faa32ec89c4e0cd2be639b7eabdd956a8b` |
| `macro-regimes-stock-bond/superseded-first-run/README.md` | removed (archive) | `aab51ff66c9af73ab8b54c233e7522cc120b8dde2765219aee0e3dc95f4d079d` |
| `macro-regimes-stock-bond/superseded-first-run/regime_quarters.csv` | removed (archive) | `82ce2b9749b75ece95ea7e2d7375d5ca47e6b60af0989b42d7f7014a85b28d85` |
| `macro-regimes-stock-bond/superseded-first-run/regime_recession_results.txt` | removed (archive) | `ef85345a0a29d707806395ffc8b1123d6dda703a65ce28de9e61c01c15f28d16` |
| `multi-asset-systematic-macro/bis-otc-ird-instruments.csv` | `rate_swaps_clearing/inputs/bis-otc-ird-instruments.csv` | `5c72733be1d75f92ebac819131a3f6e7fb17a7a22c1ad60d2178bcc05ad84585` |
| `multi-asset-systematic-macro/global_macro_monthly.csv` | `global_macro/results/global_macro_monthly.csv` | `dbbd954447e8d0871c14f809a8046261708b88cd8b8305d61c2aa4915ca69862` |
| `multi-asset-systematic-macro/global_macro_monthly_2014.csv` | `global_macro/results/global_macro_monthly_2014.csv` | `7fc107bc7e3b46c26e0465fd739271286b9ec9f0206d391132bca225b8e7cd88` |
| `multi-asset-systematic-macro/global_macro_results.txt` | `global_macro/results/global_macro_results.txt` | `7db11fe654acb4a4f31daf6e48ad204876cb684d0b76e57e23d4cac621c61b92` |
| `multi-asset-systematic-macro/global_macro_results_2014.txt` | `global_macro/results/global_macro_results_2014.txt` | `29f2e0dd3d25e95f432431b93d42d5e692137a6e9a15de8946a5909a9330147f` |
| `multi-asset-systematic-macro/h15-daily-3m-10y.csv` | `business_cycles_policy/inputs/h15-daily-3m-10y.csv` | `5a60c4f9c5ad8b1a79ec99eb9d4038225e1a71ccc3d6c68414d593a3cb4037c4` |
| `multi-asset-systematic-macro/h15-spread-monthly.csv` | `business_cycles_policy/results/h15-spread-monthly.csv` | `8878ee2d68b68efaf9614615876997244c71407b1f366c4a3113562dcdae20d8` |
| `multi-asset-systematic-macro/inversion-horizons.txt` | `business_cycles_policy/results/inversion-horizons.txt` | `b25d8895fa1ee7136d3f7dc8b500926643432e9b268ec8941f76d31192cd58db` |
| `multi-asset-systematic-macro/irr-fine-codes-gliner-currencies.csv` | `currency_intervention/inputs/irr-fine-codes-gliner-currencies.csv` | `2fa45ba042e13e38a93aeee5014d058527d1dd3caeec8f48232f0dedd71645bc` |
| `multi-asset-systematic-macro/ust-10y3m-monthly.csv` | `business_cycles_policy/results/ust-10y3m-monthly.csv` | `acd26d0156b43dc7471c6ec3d633517660208d6fddcdeeafdc895b925633f5ad` |
| `multi-asset-systematic-macro/ust-daily-3m-2y-10y.csv` | `business_cycles_policy/inputs/ust-daily-3m-2y-10y.csv` | `ca37e881d31ec627e6d84d3dc10313d9860fef54cb0ac8a7b871f3e6fd8303ad` |
| `multi-asset-systematic-macro/wpp2024-working-prime-age.csv` | `macro_indicators/inputs/wpp2024-working-prime-age.csv` | `c731b85edd0bb849d53fea4538001da8552987e3d0b5d563267faf085c8fea31` |
| `portfolio-risk-return/us-asset-class-returns-1928-2025.csv` | `portfolio_choice/inputs/us-asset-class-returns-1928-2025.csv` | `494a0a694977b2aac7d7e220ee3a4294a4234824a3e5365622ee44d91c9f3a2a` |
| `rates-credit-mortgages/acm-term-premium-summary.txt` | `gsw_treasury_curve/results/acm-term-premium-summary.txt` | `bc9fc049b34fe4d617698cabc170a783e7ad686ecd36d44a53a7c38263414d98` |
| `return-predictability/conditional-predictive-ability-first-run.txt` | removed (archive) | `c46e1ba701d4da9dbe01f2bcb9691742d47873be7f3aa1c4d7f370911d919235` |
| `return-predictability/conditional-predictive-ability-protocol.md` | `return_predictability/protocols/conditional-predictive-ability-protocol.md` | `c12b8eea91add33463e5184759b47024e3802e6fc757f19aa859eea9992ff816` |
| `return-predictability/conditional-predictive-ability-results.txt` | `return_predictability/results/conditional-predictive-ability-results.txt` | `a4d501e3142e0f2aeb7786c895085e6a1c41fb78b083f69a317065ec1923f0db` |
| `return-predictability/forecast-combination-scoring-protocol.md` | `return_predictability/protocols/forecast-combination-scoring-protocol.md` | `61d22d232f32f1812377d25ce3b83d1d012a295152e027e67624a88bf89a14c5` |
| `return-predictability/forecast-combination-scoring-results.txt` | `return_predictability/results/forecast-combination-scoring-results.txt` | `4e5731e985c1190e38c62d60e5aad91f28fe56be1c84aae19b79e231f914890e` |
| `return-predictability/goyal-annual-1871-2025.csv` | `return_predictability/inputs/goyal-annual-1871-2025.csv` | `296a21275877ccb8c31b2dcb451deaa7228ec4e992d5d81c0735dfe7fc983fae` |
| `return-predictability/goyal-annual-predictors-1871-2025.csv` | `return_predictability/inputs/goyal-annual-predictors-1871-2025.csv` | `794ed8148aa0c84ee7aa38b500ce834fa2a3c19772d4a121b02f0f5e5c4210f3` |
| `return-predictability/goyal-monthly-1871-2025.csv` | `return_predictability/inputs/goyal-monthly-1871-2025.csv` | `9dcf8e17d6329ac9ea0bbb0bffde93467d940914571374b3a4d05108dd5def26` |
| `return-predictability/return-predictability-protocol.md` | `return_predictability/protocols/return-predictability-protocol.md` | `4d417b5be128d6d80c3e19d57129e2e85a2c551bb55ff1f27ee9007256ed4627` |
| `return-predictability/return-predictability-results.txt` | `return_predictability/results/return-predictability-results.txt` | `adf6fd50201973ed0479b74c9d04be76931249335b1bfc3648af6a50acbb59a5` |
| `return-predictability/superseded-first-run/README.md` | removed (archive) | `5a249bc1b6d84c1cae91bd75e5991125fbecc1c2cff5dec9494219e304c5ebe2` |
| `return-predictability/superseded-first-run/return-predictability-protocol.md` | removed (archive) | `08ab32b02377ef82346942e1c783f6fb57b62f4bca47de71fc029b1521403d4b` |
| `return-predictability/superseded-first-run/return-predictability-results.txt` | removed (archive) | `27cd827231b30288ae9f623a69d835d4642fd01e2fb83580314ab883277c6755` |
| `term-structure-dynamics/gsw-month-end-zero.csv` | `term_structure_returns/inputs/gsw-month-end-zero.csv` | `a3c38c3574d67869b4ea86f4c38aca47b7e45ff3c94a188572df663cce66f86c` |
| `market-making-lob/model-derivations.tex` | split into `model-derivations/` (not byte-preserved) | `a8c58f9b05a754804f167393e60ad3534c5ad0a7ee9f5df2e986f326062ef55b` |

Three checks read the removed runs. `energy_checks` and `fx_checks` lose their "v1 panel preserved (SHA-256 prefix)" line (22 to 21 and 15 to 14 check lines); `regime_checks` loses that line (13 to 12) but keeps its five "v1 any-overlap result preserved" assertions, now against the first run's printed values (regime mean, difference, t for `dy10`, `dcred`, `eq`, `dfn` and the dollar splice) written as constants from `regime_recession_results.txt` of the removed run. Every other output line of the three checks is unchanged.

### Model reference

`model-derivations/model-reference.tex` is the single entrypoint, built with `make model-reference` (or `latexmk -lualatex model-reference.tex` in `model-derivations/`); `make check` builds it after the compendium, and the two builds are independent. It inputs `../compendium/preamble.tex` and `house.tex`, so there is no second preamble: `preamble.tex` runs `\qfcompendiumdir typography.lua`, with `\qfcompendiumdir` empty for the compendium and `../compendium/` for the reference, and loads hyperref with `destlabel`, so PDF destinations are named after labels. `house.tex` adds `\qfentrylink{label}` (reference to compendium) and `\qfderivation{label}` (compendium to reference), relative links of the form `file.pdf#label`; catalogue links (`../guide/...`) work unchanged from both folders. `model-reference.pdf` is committed beside its source under a `.gitignore` exception; LaTeX intermediates stay ignored, and the old document's local `.aux`, `.log`, `.fls`, `.fdb_latexmk`, `.out` and PDF were deleted, not moved.

The original document was split into four model files under `execution-market-making/market-making-models/`, with labels `drv:grossman-miller` (and `drv:grossman-miller-trading-fees`, `drv:grossman-miller-liquidity-measures`), `drv:kyle-single-auction`, `drv:static-limit-order-depth` and `drv:roll-spread-estimator`; compendium labels are unchanged. Each file gives the purpose, sources and implementation, the assumptions with variables, units, timing and information sets, the derivation, the results with interpretation and limiting cases, and the limitations. Its header comments became the notation chapter's closing paragraph. The front matter adds a notation table and the model index (model, compendium entry, derivation, implementation and check part, with the checks' parameters, seeds and tolerances). The six compendium proof sketches link to their derivations. Roll's estimator is an entry of the `market-organisation-liquidity` pathway (`spread-measurement.tex`) but keeps the original grouping with the three market-making models; the index records its compendium home.

Comparison with the original source: all 27 display equations, all 132 inline formulas and all 9 citations with their locators are present (checked by extracting each from both). The changes are structural (headings, labels, links instead of `\texttt` label names), stated units and information sets, and short limitation paragraphs drawn from the stated assumptions.

### Validation

- Hashes: the 52 relocated files equal their recorded SHA-256; the 72 original files are each accounted for once (52 relocated, 19 removed, 1 split).
- The 14 numerical checks that read data, run from an empty folder with `--root` before and after: byte-identical output except the three removed hash lines.
- Research replays (reading materials present) in temporary roots holding a copy of `src/data/`: every compared output equals its retained file after the existing `RELABELLED` mappings, every compared output lands in the subsection's run folder (`results/`, or `inputs/` for the extracts), and the copy's retained files are unchanged. `regime_quarters.csv` is written but, as before, not compared.
- Installed commands from an unrelated folder against the repository: the H.15 spread, backwardation, hedging pressure (reading the backwardation run), Goyal extract (to `runs/local/inputs/`), deflation row (explicit `--h15-daily`), down months and 2014 down months (reading the down-months run) reproduce the retained files, the 2014 stdout differing only by its two `RELABELLED` labels; `--spreads` on a missing file exits 1 with the message and no output; retained hashes were unchanged afterwards; run files were ignored by Git and deleted after the check.
- New tests: `Arguments.test_runs_write_to_the_local_run`, `test_upstream_files`, `CommittedInputs.test_rebuilt_extract_goes_to_the_run_inputs`, `test_missing_requested_input_fails`; `test_spreads_and_inversions` and `RetainedEvidence.test_replays` now run in temporary roots.
- `make source-check` passed: lock, lint, format (538 files), strict mypy (506 files), compendium and coverage checkers with 0 problems, 522 tests and 8995 subtests. `make verify-outlines`: 0 problems. `make pre-commit`: all hooks passed, no file changed. `make pdf` and `make model-reference`: no undefined references or citations, no overfull boxes; in both PDFs every cross-document link resolves to a named destination of the other, and the reference's catalogue keys exist in the guide PDF. The nine reference pages were inspected as rendered images.

## Remaining work

None. Known limitations:

- The research replays need the git-ignored `reading_materials/`; CI skips them, and the tests that need only committed extracts run everywhere. The external collections were not moved, copied or committed.
- The removed historical runs are only in Git history (`684b3a0`); `inflation-row-protocol.md`, `heating-oil-protocol.md` and `conditional-predictive-ability-protocol.md` still cite them, or old paths, as written.
- Cross-document links are relative, so they resolve only while both PDFs sit in their folders of one checkout.
- The H.15 SDMX XML and Treasury's yearly CSV files are not kept locally, so the `--extract` steps that rebuild the committed daily extracts were not replayed on real data; the monthly steps were, and both readers are tested on small hand-made files.
- `regime_quarters.csv` keeps its retained `-0.000`; the workflow writes `0.000`.
- The retained outputs keep their original labels; a run prints the reworded ones listed in the repairs above, and the replay test maps them explicitly.
