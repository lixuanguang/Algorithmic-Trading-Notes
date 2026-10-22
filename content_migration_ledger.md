# Content migration ledger

Companion to [content_migration_plan.md](content_migration_plan.md). It records the complete M0 disposition of the compendium and the guide pathways for the migration of 22 October 2026, generated from parsed input graphs before and after the migration rather than from filenames. Paths are relative to `compendium/`.

Baseline: commit `0c5394d` (structure of `80b0fc5`), guide `343d145`. Target: guide `6c7734ed49f1c242908b86a57c4f5d1f0e349ec0`, `learning_parts` of `guide/learning_routes.json`.

## 1. Reconciled inventory

| Measure | Before (audited baseline, re-parsed) | After |
| --- | --- | --- |
| Typed entries | 697 | 697, same labels and types |
| Topic files | 169 | 179 (10 new files receive split entries; none removed) |
| Populated wrappers / declared section keys | 28 / 42 | 38 / 49 |
| Parts | none | 8 declared, 7 printed (Part VIII has no populated section) |
| Wrapper `\input`s | 169, each file once | 179, each file once |
| Nested topic `\input`s | 7 figure inputs (`.tikz`) | 7 figure inputs; two paths changed with their moved files |
| Entries changing file | — | 75; bodies byte-identical except two figure `\input` paths |
| Objectives / topics / outline items | 449 / 108 / 1,030 | 449 / 108 / 1,030; 12 topic owners changed, coverage values unchanged |

## 2. Declared structure

| Part | Section key | Title | State | Topic files | Entries |
| --- | --- | --- | --- | ---: | ---: |
| I `mathematics-statistics-numerics` | `financial-mathematics` | Financial mathematics and return measurement | populated | 2 | 4 |
| I `mathematics-statistics-numerics` | `probability-statistics` | Probability and statistical inference | populated | 5 | 13 |
| I `mathematics-statistics-numerics` | `regression-time-series` | Regression and time-series econometrics | populated | 4 | 17 |
| I `mathematics-statistics-numerics` | `stochastic-processes-calculus` | Stochastic processes and calculus | populated | 1 | 3 |
| I `mathematics-statistics-numerics` | `bayesian-inference` | Bayesian inference and parameter uncertainty | populated | 1 | 1 |
| I `mathematics-statistics-numerics` | `high-dimensional-statistics` | High-dimensional statistics and covariance estimation | populated | 1 | 2 |
| I `mathematics-statistics-numerics` | `numerical-optimisation` | Numerical methods and optimisation | populated | 1 | 1 |
| II `empirical-finance-research-governance` | `asset-pricing` | Asset pricing theory and empirical tests | populated | 1 | 7 |
| II `empirical-finance-research-governance` | `causal-inference` | Causal inference and experimental design | declared, unpopulated | 0 | 0 |
| II `empirical-finance-research-governance` | `research-engineering-validation` | Research engineering, data provenance and model validation | populated | 7 | 26 |
| II `empirical-finance-research-governance` | `professional-ethics` | Professional ethics | populated | 7 | 22 |
| II `empirical-finance-research-governance` | `ml-alternative-data` | Machine learning and alternative data | populated | 6 | 22 |
| III `public-markets` | `rates-credit-mortgages` | Rates: yield curves, term premia and derivatives | populated | 10 | 53 |
| III `public-markets` | `government-bond-markets` | Government bond markets and sovereign debt | populated | 1 | 2 |
| III `public-markets` | `financial-statement-analysis` | Financial statement analysis | populated | 16 | 56 |
| III `public-markets` | `corporate-finance` | Corporate finance | populated | 7 | 20 |
| III `public-markets` | `corporate-credit-capital` | Corporate credit, hybrids and labelled bonds | populated | 3 | 14 |
| III `public-markets` | `securitised-structured-credit` | Securitised and structured credit | populated | 2 | 5 |
| III `public-markets` | `systematic-equities` | Systematic equities | populated | 11 | 45 |
| III `public-markets` | `volatility-options` | Option pricing, volatility models and hedging | populated | 8 | 38 |
| III `public-markets` | `volatility-trading-premia` | Volatility trading, option premia and implied information | populated | 1 | 1 |
| III `public-markets` | `multi-asset-systematic-macro` | Multi-asset and systematic macro | populated | 7 | 32 |
| III `public-markets` | `currency-markets` | Currency markets: exchange rates, premia and hedging | populated | 3 | 18 |
| III `public-markets` | `international-equity-markets` | International and emerging equity markets | populated | 2 | 3 |
| III `public-markets` | `global-regional-markets` | Global and regional markets: capital flows, local bonds and market access | declared, unpopulated | 0 | 0 |
| IV `portfolio-financing-execution` | `portfolio-construction-risk` | Portfolio construction and risk | populated | 19 | 79 |
| IV `portfolio-financing-execution` | `portfolio-risk-financing` | Funding, collateral and liquidity | populated | 5 | 16 |
| IV `portfolio-financing-execution` | `execution-market-making` | Market microstructure and market making | populated | 8 | 72 |
| IV `portfolio-financing-execution` | `execution-trading-costs` | Execution, trading costs and market structure | populated | 16 | 60 |
| V `energy-commodities` | `energy-commodities` | Commodity futures: storage, curves, hedging and options | populated | 2 | 3 |
| V `energy-commodities` | `commodity-spot-markets` | Commodity spot markets: price formation, market integration and long-run prices | declared, unpopulated | 0 | 0 |
| V `energy-commodities` | `physical-commodity-markets` | Physical commodity markets: delivery, price discovery and trading | populated | 1 | 3 |
| V `energy-commodities` | `commodity-investing-premia` | Commodity risk premia and investing: factors, allocation and index products | populated | 2 | 5 |
| V `energy-commodities` | `oil-shocks-macro` | Oil-price shocks, forecasting and the macroeconomy | declared, unpopulated | 0 | 0 |
| V `energy-commodities` | `power-gas-environmental` | Gas and power markets: hubs, storage, networks and market design | populated | 1 | 1 |
| V `energy-commodities` | `environmental-markets` | Environmental markets: emissions trading, carbon credits and certificates | declared, unpopulated | 0 | 0 |
| VI `private-real-insurance` | `private-capital-allocator` | Private equity, private credit and fund structures | populated | 5 | 17 |
| VI `private-real-insurance` | `real-asset-investor` | Real estate, infrastructure and natural-resource investments | populated | 3 | 10 |
| VI `private-real-insurance` | `insurance-climate-risk` | Insurance and climate-linked risk | declared, unpopulated | 0 | 0 |
| VI `private-real-insurance` | `private-wealth-management` | Private wealth management | populated | 4 | 15 |
| VII `digital-assets` | `digital-assets-prediction-markets` | Crypto settlement, venues and derivatives | populated | 3 | 7 |
| VII `digital-assets` | `crypto-spot-markets` | Crypto spot markets: price discovery, market quality, valuation and investors | populated | 1 | 1 |
| VII `digital-assets` | `onchain-protocols` | On-chain protocols | populated | 1 | 2 |
| VII `digital-assets` | `tokenised-fractional-assets` | Fractional and tokenised assets: fractional shares, tokenised securities and real-world assets | declared, unpopulated | 0 | 0 |
| VII `digital-assets` | `crypto-market-making` | Crypto market making: order books, DEX liquidity and token market makers | declared, unpopulated | 0 | 0 |
| VII `digital-assets` | `crypto-trading-strategies` | Crypto trading strategies: factors, trend, arbitrage, sentiment and machine learning | populated | 1 | 1 |
| VIII `event-contracts` | `event-contracts-prediction-markets` | Event contracts and prediction markets | declared, unpopulated | 0 | 0 |
| VIII `event-contracts` | `event-contract-venues` | Event-contract venues, settlement and regulation | declared, unpopulated | 0 | 0 |
| VIII `event-contracts` | `event-contract-trading` | Event-contract trading: market making, derivatives and strategies | declared, unpopulated | 0 | 0 |

## 3. Topic-file dispositions

One row per topic file, in compiled order. *Subsection* is the chapter's `\section` heading; *Subsubsection* is the file's own heading when it sits inside a multi-file group. Actions: **retain** (same section and relative order, same heading level), **reorder** (same section, new position or heading level), **move** (whole file to another section, all its entries with it), **split** (file loses or gains the entries listed in section 4). The entries of a row are all those in the file after the migration; split exceptions are enumerated in section 4.

| Part | Section | Subsection | Subsubsection | File | Source | Action | Entries | Figures |
| --- | --- | --- | --- | --- | --- | --- | ---: | --- |
| I | `financial-mathematics` | Time value, required returns and present value |  | `time-value.tex` | `common-toolkit/time-value.tex` | move | 3 |  |
| I | `financial-mathematics` | Return measurement |  | `return-measurement.tex` | entries from `portfolio-construction-risk/performance-evaluation.tex` | split (new file) | 1 |  |
| I | `probability-statistics` | Descriptive statistics of returns |  | `descriptive-statistics.tex` | `common-toolkit/descriptive-statistics.tex` | move | 4 |  |
| I | `probability-statistics` | Probability and distributions in finance |  | `probability.tex` | `common-toolkit/probability.tex` | move; split (loses `meth:bayesian-updating`) | 2 |  |
| I | `probability-statistics` | Sampling and statistical inference |  | `statistical-inference.tex` | `common-toolkit/statistical-inference.tex` | move | 4 |  |
| I | `probability-statistics` | Historical simulation and resampling |  | `resampling.tex` | `common-toolkit/simulation-methods.tex` | move; split (loses `meth:monte-carlo-simulation`) | 2 |  |
| I | `probability-statistics` | Heavy tails and extreme values |  | `extreme-values.tex` | entries from `portfolio-construction-risk/risk-models.tex` | split (new file) | 1 |  |
| I | `regression-time-series` | Simple linear regression |  | `regression.tex` | `common-toolkit/regression.tex` | move | 3 |  |
| I | `regression-time-series` | Multiple regression |  | `multiple-regression.tex` | `common-toolkit/multiple-regression.tex` | move | 4 |  |
| I | `regression-time-series` | Time-series models |  | `time-series-models.tex` | `common-toolkit/time-series-models.tex` | move | 7 |  |
| I | `regression-time-series` | Volatility forecasts, forecast evaluation and structural breaks |  | `volatility-forecasting.tex` | entries from `portfolio-construction-risk/risk-models.tex` | split (new file) | 3 |  |
| I | `stochastic-processes-calculus` | Stochastic calculus for asset prices |  | `stochastic-calculus.tex` | `common-toolkit/stochastic-calculus.tex` | move | 3 |  |
| I | `bayesian-inference` | Posterior updating and prediction |  | `bayesian-updating.tex` | entries from `probability-statistics/probability.tex` | split (new file) | 1 |  |
| I | `high-dimensional-statistics` | Large covariance matrices: shrinkage and random-matrix noise |  | `covariance-estimation.tex` | entries from `portfolio-construction-risk/risk-models.tex` | split (new file) | 2 |  |
| I | `numerical-optimisation` | Monte Carlo simulation |  | `monte-carlo-simulation.tex` | entries from `probability-statistics/resampling.tex` | split (new file) | 1 |  |
| II | `asset-pricing` | Systematic risk, the CAPM and factor models |  | `asset-pricing-models.tex` | `portfolio-construction-risk/asset-pricing-models.tex` | move | 7 | `asset-pricing/figures/security-market-line.tikz` (moved; path in `asset-pricing-checks.py` updated) |
| II | `research-engineering-validation` | The structure of a quant strategy and its alpha models |  | `quant-strategy-structure.tex` | `portfolio-construction-risk/quant-strategy-structure.tex` | move | 3 | `research-engineering-validation/figures/strategystructure.tikz` (moved) |
| II | `research-engineering-validation` | Backtests and simulation | Strategy research and backtest evaluation | `backtest-evaluation.tex` | (in place) | reorder | 8 |  |
| II | `research-engineering-validation` | Backtests and simulation | Scenarios, simulation and sensitivity | `scenario-simulation.tex` | (in place) | reorder | 1 |  |
| II | `research-engineering-validation` | Point-in-time reference and market data |  | `point-in-time-data.tex` | (in place) | retain | 5 |  |
| II | `research-engineering-validation` | Controls, strategy risk and production | Operational controls for automated trading | `trading-controls.tex` | (in place) | reorder | 4 |  |
| II | `research-engineering-validation` | Controls, strategy risk and production | Sources of strategy risk and their monitoring | `strategy-risk.tex` | (in place) | reorder | 2 |  |
| II | `research-engineering-validation` | Controls, strategy risk and production | The research and production chain of a strategy | `strategy-production.tex` | (in place) | reorder | 3 |  |
| II | `professional-ethics` | Ethics, trust and decision-making |  | `ethics-trust-framework.tex` | (in place) | retain | 2 |  |
| II | `professional-ethics` | The Code, the Standards and their enforcement |  | `code-standards-enforcement.tex` | (in place) | retain | 2 |  |
| II | `professional-ethics` | Applying the Standards | Professionalism and the integrity of capital markets | `standards-professionalism-markets.tex` | (in place) | reorder | 4 |  |
| II | `professional-ethics` | Applying the Standards | Duties to clients and to employers | `standards-clients-employers.tex` | (in place) | reorder | 4 |  |
| II | `professional-ethics` | Applying the Standards | Investment analysis, conflicts and responsibilities as a member | `standards-analysis-conflicts-members.tex` | (in place) | reorder | 6 |  |
| II | `professional-ethics` | Evaluating conduct and manager selection |  | `conduct-cases.tex` | (in place) | retain | 2 |  |
| II | `professional-ethics` | The Asset Manager Code |  | `asset-manager-code.tex` | (in place) | retain | 2 |  |
| II | `ml-alternative-data` | Financial data and the data-science workflow | Types of financial data | `financial-data-types.tex` | (in place) | reorder | 1 |  |
| II | `ml-alternative-data` | Financial data and the data-science workflow | The data-science workflow | `data-science-workflow.tex` | (in place) | reorder | 4 |  |
| II | `ml-alternative-data` | Machine learning methods |  | `machine-learning-methods.tex` | (in place) | reorder | 3 |  |
| II | `ml-alternative-data` | Financial data structures, labels and features | Financial data structures: bars, multi-product series and event sampling | `financial-data-structures.tex` | (in place) | reorder | 4 |  |
| II | `ml-alternative-data` | Financial data structures, labels and features | Labels and sample weights for overlapping financial outcomes | `labelling-sample-weights.tex` | (in place) | reorder | 8 |  |
| II | `ml-alternative-data` | Financial data structures, labels and features | Fractionally differentiated features | `fractional-differentiation.tex` | (in place) | reorder | 2 |  |
| III | `rates-credit-mortgages` | Bonds, yields and discounting | Interest rates, discounting and rate risk | `interest-rates.tex` | (in place) | reorder | 7 |  |
| III | `rates-credit-mortgages` | Bonds, yields and discounting | Bonds: features, legal terms, markets and issuers | `bond-instruments-markets.tex` | (in place) | reorder | 6 |  |
| III | `rates-credit-mortgages` | Bonds, yields and discounting | Bond prices, yields and spreads | `bond-pricing-yields.tex` | (in place) | reorder | 4 |  |
| III | `rates-credit-mortgages` | Term structure and interest-rate risk | The term structure: curves, forwards, returns and curve risk | `term-structure-returns.tex` | (in place) | reorder | 5 |  |
| III | `rates-credit-mortgages` | Term structure and interest-rate risk | Bond returns and interest-rate risk | `interest-rate-risk.tex` | (in place) | reorder | 4 |  |
| III | `rates-credit-mortgages` | Arbitrage-free valuation and embedded options | Arbitrage-free bond valuation and interest-rate trees | `arbitrage-free-valuation.tex` | (in place) | reorder | 5 |  |
| III | `rates-credit-mortgages` | Arbitrage-free valuation and embedded options | Bonds with embedded options | `embedded-option-bonds.tex` | (in place) | reorder | 5 |  |
| III | `rates-credit-mortgages` | Monetary policy and the curve | Monetary policy and its interaction with fiscal policy | `monetary-fiscal-policy.tex` | (in place) | reorder | 2 |  |
| III | `rates-credit-mortgages` | Monetary policy and the curve | Central banks, the policy path and the curve | `monetary-policy-curves.tex` | (in place) | reorder | 8 |  |
| III | `rates-credit-mortgages` | Fixed-income portfolio management |  | `fixed-income-portfolio-management.tex` | (in place) | reorder | 7 |  |
| III | `government-bond-markets` | Sovereign credit |  | `sovereign-credit.tex` | (in place) | retain | 2 |  |
| III | `financial-statement-analysis` | Reporting and the statements | Reporting framework and information sources | `financial-reporting-framework.tex` | (in place) | reorder | 3 |  |
| III | `financial-statement-analysis` | Reporting and the statements | Income-statement analysis | `income-statement-analysis.tex` | (in place) | reorder | 5 |  |
| III | `financial-statement-analysis` | Reporting and the statements | Balance-sheet analysis | `balance-sheet-analysis.tex` | (in place) | reorder | 3 |  |
| III | `financial-statement-analysis` | Reporting and the statements | Cash-flow analysis | `cash-flow-analysis.tex` | (in place) | reorder | 3 |  |
| III | `financial-statement-analysis` | Reporting and the statements | A reconciled company case | `company-case.tex` | (in place) | reorder | 1 |  |
| III | `financial-statement-analysis` | Accounting measurement | Inventories | `inventory-accounting.tex` | (in place) | reorder | 3 |  |
| III | `financial-statement-analysis` | Accounting measurement | Long-lived assets | `long-lived-asset-accounting.tex` | (in place) | reorder | 2 |  |
| III | `financial-statement-analysis` | Accounting measurement | Leases and employee compensation | `leases-employee-compensation.tex` | (in place) | reorder | 6 |  |
| III | `financial-statement-analysis` | Accounting measurement | Income taxes | `income-tax-accounting.tex` | (in place) | reorder | 3 |  |
| III | `financial-statement-analysis` | Group and international reporting | Intercorporate investments | `intercorporate-investments.tex` | (in place) | reorder | 2 |  |
| III | `financial-statement-analysis` | Group and international reporting | Foreign currency in financial statements | `foreign-currency-reporting.tex` | (in place) | reorder | 3 |  |
| III | `financial-statement-analysis` | Analytical ratios and reporting quality | Ratio analysis | `ratio-analysis.tex` | (in place) | reorder | 4 |  |
| III | `financial-statement-analysis` | Analytical ratios and reporting quality | Financial reporting quality | `financial-reporting-quality.tex` | (in place) | reorder | 7 |  |
| III | `financial-statement-analysis` | Analytical ratios and reporting quality | Banks and insurers | `financial-institution-analysis.tex` | (in place) | reorder | 4 |  |
| III | `financial-statement-analysis` | Forecasting and integrated analysis | Financial statement modelling | `financial-statement-modelling.tex` | (in place) | reorder | 4 |  |
| III | `financial-statement-analysis` | Forecasting and integrated analysis | Integrated analysis | `integrated-statement-analysis.tex` | (in place) | reorder | 3 |  |
| III | `corporate-finance` | Ownership, governance and business models | Corporate issuers, ownership and governance | `corporate-ownership-governance.tex` | (in place) | reorder | 5 |  |
| III | `corporate-finance` | Ownership, governance and business models | Business models | `business-models.tex` | (in place) | reorder | 1 |  |
| III | `corporate-finance` | Working capital and liquidity |  | `working-capital-liquidity.tex` | (in place) | retain | 2 |  |
| III | `corporate-finance` | Capital investment and allocation |  | `capital-investment.tex` | (in place) | retain | 2 |  |
| III | `corporate-finance` | Capital structure and the cost of capital |  | `capital-structure-cost-of-capital.tex` | (in place) | retain | 4 |  |
| III | `corporate-finance` | Payout policy |  | `payout-policy.tex` | (in place) | retain | 4 |  |
| III | `corporate-finance` | Corporate restructuring |  | `corporate-restructuring.tex` | (in place) | retain | 2 |  |
| III | `corporate-credit-capital` | Credit risk and credit analysis |  | `credit-risk-analysis.tex` | (in place) | retain | 6 |  |
| III | `corporate-credit-capital` | Credit default swaps |  | `credit-default-swaps.tex` | (in place) | retain | 4 |  |
| III | `corporate-credit-capital` | Credit portfolio management |  | `credit-portfolio-management.tex` | (in place) | retain | 4 |  |
| III | `securitised-structured-credit` | Securitisation |  | `securitisation.tex` | (in place) | retain | 3 |  |
| III | `securitised-structured-credit` | Default correlation and tranche valuation |  | `default-correlation.tex` | (in place) | retain | 2 |  |
| III | `systematic-equities` | Equity securities and fundamental analysis | Equity securities and markets | `equity-securities-markets.tex` | (in place) | reorder | 4 |  |
| III | `systematic-equities` | Equity securities and fundamental analysis | Industry and company analysis | `industry-company-analysis.tex` | (in place) | reorder | 2 |  |
| III | `systematic-equities` | Equity securities and fundamental analysis | Equity research and forecast models | `equity-research-reporting.tex` | (in place) | reorder | 2 |  |
| III | `systematic-equities` | Equity valuation | Equity valuation foundations | `equity-valuation-foundations.tex` | (in place) | reorder | 6 |  |
| III | `systematic-equities` | Equity valuation | Dividend discount models | `dividend-discount-models.tex` | (in place) | reorder | 5 |  |
| III | `systematic-equities` | Equity valuation | Price and enterprise-value multiples | `market-multiples.tex` | (in place) | reorder | 7 |  |
| III | `systematic-equities` | Equity valuation | Free cash flow valuation | `free-cash-flow-valuation.tex` | (in place) | reorder | 4 |  |
| III | `systematic-equities` | Equity valuation | Residual income valuation | `residual-income-valuation.tex` | (in place) | reorder | 3 |  |
| III | `systematic-equities` | Equity valuation | Private company valuation | `private-company-valuation.tex` | (in place) | reorder | 3 |  |
| III | `systematic-equities` | Signals and equity portfolios | Combining alpha signals | `signal-combination.tex` | (in place) | reorder | 2 |  |
| III | `systematic-equities` | Signals and equity portfolios | Equity portfolio management | `equity-portfolio-management.tex` | (in place) | reorder | 7 |  |
| III | `volatility-options` | Derivative contracts and markets | Forwards, futures and options, and the cost of carry | `derivative-contracts.tex` | (in place) | reorder | 2 | `volatility-options/figures/futures-convergence.tikz` (unchanged) |
| III | `volatility-options` | Derivative contracts and markets | Derivative markets, types, payoffs and uses | `derivative-markets-uses.tex` | (in place) | reorder | 4 |  |
| III | `volatility-options` | Pricing and valuing forward commitments |  | `forward-commitment-valuation.tex` | (in place) | retain | 8 |  |
| III | `volatility-options` | Option valuation and the volatility surface | Option valuation: value drivers, parity, binomial trees, Black's model and the Greeks | `option-valuation.tex` | (in place) | reorder | 8 |  |
| III | `volatility-options` | Option valuation and the volatility surface | Option pricing and the implied volatility surface | `option-pricing.tex` | (in place) | reorder | 5 |  |
| III | `volatility-options` | Option strategies |  | `option-strategies.tex` | (in place) | reorder | 4 |  |
| III | `volatility-options` | Numerical option pricing: finite differences, least-squares Monte Carlo and simulated Greeks |  | `numerical-methods.tex` | (in place) | retain | 3 |  |
| III | `volatility-options` | Digital, barrier, lookback and Asian options |  | `exotic-options.tex` | (in place) | retain | 4 |  |
| III | `volatility-trading-premia` | VIX, variance swaps and dividend swaps |  | `vix-variance-dividends.tex` | (in place) | retain | 1 |  |
| III | `multi-asset-systematic-macro` | Economic foundations | Firms and market structure | `firms-market-structure.tex` | (in place) | reorder | 3 |  |
| III | `multi-asset-systematic-macro` | Economic foundations | Business cycles, fiscal policy, trade and geopolitics | `business-cycles-policy.tex` | (in place) | reorder | 6 |  |
| III | `multi-asset-systematic-macro` | Economic foundations | Economic growth and its investment implications | `economic-growth.tex` | (in place) | reorder | 4 |  |
| III | `multi-asset-systematic-macro` | Asset valuation and capital-market expectations | The economy and asset values | `macro-asset-valuation.tex` | (in place) | reorder | 3 |  |
| III | `multi-asset-systematic-macro` | Asset valuation and capital-market expectations | Capital market expectations | `capital-market-expectations.tex` | (in place) | reorder | 6 |  |
| III | `multi-asset-systematic-macro` | Macro strategies, regimes and data | Global macro: strategy, record, risk and practitioners | `global-macro.tex` | (in place) | reorder | 4 |  |
| III | `multi-asset-systematic-macro` | Macro strategies, regimes and data | Regimes, indicators, releases and valuation | `macro-regimes-data.tex` | (in place) | reorder | 6 |  |
| III | `currency-markets` | Exchange-rate mechanics, parity and determination |  | `fx-mechanics-parity.tex` | (in place) | retain | 9 |  |
| III | `currency-markets` | Currencies in global macro |  | `macro-fx.tex` | (in place) | retain | 5 |  |
| III | `currency-markets` | Currency management |  | `currency-management.tex` | (in place) | retain | 4 |  |
| III | `international-equity-markets` | Index construction: weights, divisors, returns and index types |  | `index-construction.tex` | (in place) | reorder | 2 |  |
| III | `international-equity-markets` | Equity indices and instruments for macro |  | `equity-indices.tex` | (in place) | reorder | 1 |  |
| IV | `portfolio-construction-risk` | Investors and the investment process | Investors, the investment process and investment policy | `investment-process-planning.tex` | (in place) | reorder | 6 |  |
| IV | `portfolio-construction-risk` | Investors and the investment process | Behavioural finance: biases and market behaviour | `behavioural-finance.tex` | (in place) | reorder | 2 |  |
| IV | `portfolio-construction-risk` | Portfolio risk, return and choice | Portfolio return and risk: moments and diversification | `portfolio-moments.tex` | (in place) | reorder | 2 |  |
| IV | `portfolio-construction-risk` | Portfolio risk, return and choice | Portfolio choice: asset classes, risk aversion and efficient portfolios | `portfolio-choice.tex` | (in place) | reorder | 4 | `portfolio-construction-risk/figures/mean-sd-frontier.tikz` (unchanged) |
| IV | `portfolio-construction-risk` | Allocation and construction | Strategic asset allocation | `strategic-asset-allocation.tex` | `multi-asset-systematic-macro/strategic-asset-allocation.tex` | move | 11 |  |
| IV | `portfolio-construction-risk` | Allocation and construction | Portfolio construction models: rules and optimisers | `portfolio-construction-models.tex` | (in place) | reorder | 10 |  |
| IV | `portfolio-construction-risk` | Allocation and construction | Transaction cost models as inputs to portfolio construction | `transaction-cost-models.tex` | (in place) | reorder | 1 |  |
| IV | `portfolio-construction-risk` | Risk management, risk models and overlays | Risk management framework and governance | `risk-governance.tex` | (in place) | reorder | 2 |  |
| IV | `portfolio-construction-risk` | Risk management, risk models and overlays | Risk models: factor exposures and their control | `risk-models.tex` | (in place) | reorder; split (loses `meth:portfolio-covariance-estimation`, `ev:correlation-matrix-noise`, `mod:garch-volatility-forecast`, `meth:volatility-forecast-loss`, `meth:structural-break-tests`, `meth:extreme-value-tail-estimation`) | 2 |  |
| IV | `portfolio-construction-risk` | Risk management, risk models and overlays | Market risk measurement and limits | `market-risk-measurement.tex` | (in place) | reorder | 3 |  |
| IV | `portfolio-construction-risk` | Risk management, risk models and overlays | Derivative overlays for portfolio exposures | `derivative-overlays.tex` | (in place) | reorder | 4 |  |
| IV | `portfolio-construction-risk` | Performance and manager evaluation | Performance evaluation | `performance-evaluation.tex` | (in place) | reorder; split (loses `def:return-measures`) | 3 |  |
| IV | `portfolio-construction-risk` | Performance and manager evaluation | Performance attribution, benchmarks and appraisal | `performance-attribution-appraisal.tex` | (in place) | reorder | 7 |  |
| IV | `portfolio-construction-risk` | Performance and manager evaluation | Active management: value added, the information ratio and the fundamental law | `active-management.tex` | (in place) | reorder | 3 |  |
| IV | `portfolio-construction-risk` | Performance and manager evaluation | Investment manager selection | `manager-selection.tex` | (in place) | reorder | 4 |  |
| IV | `portfolio-construction-risk` | Performance and manager evaluation | Performance presentation standards | `performance-standards.tex` | (in place) | reorder | 4 |  |
| IV | `portfolio-construction-risk` | Alternatives and institutional portfolios | Hedge funds | `hedge-fund-strategies.tex` | (in place) | reorder | 3 |  |
| IV | `portfolio-construction-risk` | Alternatives and institutional portfolios | Allocating to alternative investments | `alternatives-allocation.tex` | (in place) | reorder | 2 |  |
| IV | `portfolio-construction-risk` | Alternatives and institutional portfolios | Institutional investor portfolios | `institutional-portfolios.tex` | (in place) | reorder | 6 |  |
| IV | `portfolio-risk-financing` | Money markets and reference rates |  | `money-markets.tex` | (in place) | reorder | 3 |  |
| IV | `portfolio-risk-financing` | Securities lending and short selling |  | `securities-lending.tex` | (in place) | retain | 4 |  |
| IV | `portfolio-risk-financing` | Crowding, contagion and liquidity spirals |  | `crowding-contagion.tex` | (in place) | reorder; split (gains `mod:liquidity-spirals`) | 3 |  |
| IV | `portfolio-risk-financing` | Counterparty exposure and valuation adjustments |  | `counterparty-xva.tex` | `corporate-credit-capital/counterparty-xva.tex` | move | 4 |  |
| IV | `portfolio-risk-financing` | Synthetic short positions |  | `synthetic-shorts.tex` | (in place) | retain | 2 |  |
| IV | `execution-market-making` | Markets, trading systems and orders | Markets, traders and venues | `market-organisation.tex` | (in place) | reorder | 9 |  |
| IV | `execution-market-making` | Markets, trading systems and orders | Floor and automated trading systems | `trading-systems.tex` | (in place) | reorder | 1 |  |
| IV | `execution-market-making` | Markets, trading systems and orders | Orders, limit order books and queues | `order-books.tex` | (in place) | reorder | 8 |  |
| IV | `execution-market-making` | Order flow and dealer models | Order flow in time: stylised facts, clocks and point processes | `order-flow-statistics.tex` | (in place) | reorder | 6 |  |
| IV | `execution-market-making` | Order flow and dealer models | Inventory and quoting (with three inner groups over its nine former headings, now subsubsections) | `market-making-models.tex` | (in place) | reorder | 35 | `execution-market-making/figures/grossman_miller_trading.tikz`, `limit_order_market_making.tikz` (unchanged) |
| IV | `execution-market-making` | Options and FX dealing | Options dealing: market-maker spreads, cost measurement and retail routing | `options-dealing.tex` | (in place) | reorder | 3 |  |
| IV | `execution-market-making` | Options and FX dealing | Spot FX dealing: market structure, internalisation and last look | `fx-dealing.tex` | (in place) | reorder | 3 |  |
| IV | `execution-market-making` | High-frequency trading: strategies, speed races and the costs of other traders |  | `high-frequency-trading.tex` | (in place) | reorder | 7 |  |
| IV | `execution-trading-costs` | Benchmarks and trade measurement | Execution benchmarks and implementation shortfall | `execution-benchmarks.tex` | (in place) | reorder | 3 |  |
| IV | `execution-trading-costs` | Benchmarks and trade measurement | Signing trades | `trade-signing.tex` | (in place) | reorder | 1 |  |
| IV | `execution-trading-costs` | Price impact |  | `impact-models.tex` | (in place) | reorder | 9 |  |
| IV | `execution-trading-costs` | Optimal execution and scheduling | Execution scheduling and block orders | `execution-scheduling.tex` | (in place) | reorder | 2 |  |
| IV | `execution-trading-costs` | Optimal execution and scheduling | Optimal execution as stochastic control: the benchmark for learned policies | `execution-control.tex` | `ml-alternative-data/execution-control.tex` | move | 1 |  |
| IV | `execution-trading-costs` | Algorithms, routing and venues | Execution algorithms, order exposure and portfolio trading | `execution-algorithms.tex` | (in place) | reorder | 6 |  |
| IV | `execution-trading-costs` | Algorithms, routing and venues | Smart order routing across fragmented venues | `smart-order-routing.tex` | (in place) | reorder | 3 |  |
| IV | `execution-trading-costs` | Algorithms, routing and venues | Dark trading and fragmentation | `dark-trading-fragmentation.tex` | (in place) | reorder | 5 |  |
| IV | `execution-trading-costs` | Transaction cost analysis and execution quality | Transaction costs and transaction cost analysis | `transaction-cost-analysis.tex` | (in place) | reorder | 3 |  |
| IV | `execution-trading-costs` | Transaction cost analysis and execution quality | Best execution and broker conflicts | `execution-quality.tex` | (in place) | reorder | 2 |  |
| IV | `execution-trading-costs` | Execution by instrument | Exchange-traded funds and index products | `etf-mechanics.tex` | (in place) | reorder | 3 |  |
| IV | `execution-trading-costs` | Execution by instrument | Futures: venue conventions, off-exchange trades, margin and price discovery | `futures-execution.tex` | (in place) | reorder | 5 |  |
| IV | `execution-trading-costs` | Execution by instrument | Fixed-income and OTC trading | `fixed-income-trading.tex` | (in place) | reorder | 3 |  |
| IV | `execution-trading-costs` | Regulation and execution governance | Market regulation, venue competition and circuit breakers | `market-regulation.tex` | (in place) | reorder | 6 |  |
| IV | `execution-trading-costs` | Regulation and execution governance | Tick size | `tick-size.tex` | (in place) | reorder | 3 |  |
| IV | `execution-trading-costs` | Regulation and execution governance | Trade strategy, implementation across markets and execution governance | `trade-strategy-governance.tex` | (in place) | reorder | 5 |  |
| V | `energy-commodities` | Curves and inventories |  | `commodity-curves.tex` | (in place) | reorder | 1 |  |
| V | `energy-commodities` | Hedging with futures |  | `futures-hedging.tex` | (in place) | reorder | 2 | `energy-commodities/figures/hedge-variance.tikz` (unchanged) |
| V | `physical-commodity-markets` | Crude oil, metals and agricultural markets |  | `physical-markets.tex` | (in place) | retain | 3 |  |
| V | `commodity-investing-premia` | Commodity futures as investments |  | `commodity-futures-investing.tex` | (in place) | reorder | 4 |  |
| V | `commodity-investing-premia` | Commodity indices |  | `commodity-indices.tex` | (in place) | reorder | 1 |  |
| V | `power-gas-environmental` | Natural gas |  | `natural-gas.tex` | (in place) | retain | 1 |  |
| VI | `private-capital-allocator` | Alternative investment structures, fees and returns |  | `alternative-investment-structures.tex` | (in place) | retain | 3 |  |
| VI | `private-capital-allocator` | Private equity and private debt |  | `private-capital-foundations.tex` | (in place) | retain | 3 |  |
| VI | `private-capital-allocator` | Private-market structures, performance and the investment process |  | `private-market-programmes.tex` | (in place) | retain | 5 |  |
| VI | `private-capital-allocator` | Private equity strategies, valuation and allocation |  | `private-equity-strategies.tex` | (in place) | retain | 3 |  |
| VI | `private-capital-allocator` | Private debt and special situations |  | `private-debt-special-situations.tex` | (in place) | retain | 3 |  |
| VI | `real-asset-investor` | Real estate |  | `real-estate.tex` | (in place) | retain | 6 |  |
| VI | `real-asset-investor` | Infrastructure |  | `infrastructure.tex` | (in place) | retain | 3 |  |
| VI | `real-asset-investor` | Land, timberland and farmland |  | `land-timber-farmland.tex` | (in place) | retain | 1 |  |
| VI | `private-wealth-management` | Private clients and the wealth management industry |  | `clients-industry.tex` | (in place) | retain | 5 |  |
| VI | `private-wealth-management` | Wealth and investment planning |  | `wealth-planning.tex` | (in place) | retain | 5 |  |
| VI | `private-wealth-management` | Preserving wealth |  | `wealth-preservation.tex` | (in place) | retain | 2 |  |
| VI | `private-wealth-management` | Advising the wealthy and transferring wealth |  | `wealth-transfer.tex` | (in place) | retain | 3 |  |
| VII | `digital-assets-prediction-markets` | Distributed ledgers and their financial applications |  | `distributed-ledgers.tex` | entries from `crypto-spot-markets/digital-asset-investing.tex` | split (new file) | 1 |  |
| VII | `digital-assets-prediction-markets` | Stablecoins: runs and international standards |  | `stablecoins.tex` | entries from `digital-assets-prediction-markets/crypto-venues-perpetuals.tex` | split (new file) | 2 |  |
| VII | `digital-assets-prediction-markets` | Crypto venues, perpetuals and trading risk |  | `crypto-venues-perpetuals.tex` | (in place) | retain; split (loses `def:amm-pool-mechanics`, `mech:defi-lending-liquidation`, `ev:crypto-dated-futures-carry`, `mod:liquidity-spirals`, `ev:stablecoin-runs`, `rule:stablecoin-standards`) | 4 |  |
| VII | `crypto-spot-markets` | Digital-asset investing |  | `digital-asset-investing.tex` | `digital-assets-prediction-markets/digital-asset-investing.tex` | move; split (loses `def:distributed-ledger-applications`) | 1 |  |
| VII | `onchain-protocols` | Automated market makers and lending protocols |  | `amm-lending.tex` | entries from `digital-assets-prediction-markets/crypto-venues-perpetuals.tex` | split (new file) | 2 |  |
| VII | `crypto-trading-strategies` | Carry on dated crypto futures |  | `crypto-carry.tex` | entries from `digital-assets-prediction-markets/crypto-venues-perpetuals.tex` | split (new file) | 1 |  |

Rows by first action: move 15, reorder 114, retain 40, split 10. The former wrapper `common-toolkit/section.tex` was removed after all nine inputs moved; no input remains assigned to it.

## 4. Entry-level split exceptions

Every other entry moves, or stays, with its whole file in section 3.

| Label | Type | Source file (after any whole-file move) | Destination file | Destination section |
| --- | --- | --- | --- | --- |
| `meth:bayesian-updating` | method | `probability-statistics/probability.tex` | `bayesian-inference/bayesian-updating.tex` | `bayesian-inference` |
| `meth:monte-carlo-simulation` | method | `probability-statistics/resampling.tex` | `numerical-optimisation/monte-carlo-simulation.tex` | `numerical-optimisation` |
| `def:return-measures` | definition | `portfolio-construction-risk/performance-evaluation.tex` | `financial-mathematics/return-measurement.tex` | `financial-mathematics` |
| `meth:portfolio-covariance-estimation` | method | `portfolio-construction-risk/risk-models.tex` | `high-dimensional-statistics/covariance-estimation.tex` | `high-dimensional-statistics` |
| `ev:correlation-matrix-noise` | evidence | `portfolio-construction-risk/risk-models.tex` | `high-dimensional-statistics/covariance-estimation.tex` | `high-dimensional-statistics` |
| `mod:garch-volatility-forecast` | model | `portfolio-construction-risk/risk-models.tex` | `regression-time-series/volatility-forecasting.tex` | `regression-time-series` |
| `meth:volatility-forecast-loss` | method | `portfolio-construction-risk/risk-models.tex` | `regression-time-series/volatility-forecasting.tex` | `regression-time-series` |
| `meth:structural-break-tests` | method | `portfolio-construction-risk/risk-models.tex` | `regression-time-series/volatility-forecasting.tex` | `regression-time-series` |
| `meth:extreme-value-tail-estimation` | method | `portfolio-construction-risk/risk-models.tex` | `probability-statistics/extreme-values.tex` | `probability-statistics` |
| `def:amm-pool-mechanics` | definition | `digital-assets-prediction-markets/crypto-venues-perpetuals.tex` | `onchain-protocols/amm-lending.tex` | `onchain-protocols` |
| `mech:defi-lending-liquidation` | mechanism | `digital-assets-prediction-markets/crypto-venues-perpetuals.tex` | `onchain-protocols/amm-lending.tex` | `onchain-protocols` |
| `ev:crypto-dated-futures-carry` | evidence | `digital-assets-prediction-markets/crypto-venues-perpetuals.tex` | `crypto-trading-strategies/crypto-carry.tex` | `crypto-trading-strategies` |
| `mod:liquidity-spirals` | model | `digital-assets-prediction-markets/crypto-venues-perpetuals.tex` | `portfolio-risk-financing/crowding-contagion.tex` | `portfolio-risk-financing` |
| `ev:stablecoin-runs` | evidence | `digital-assets-prediction-markets/crypto-venues-perpetuals.tex` | `digital-assets-prediction-markets/stablecoins.tex` | `digital-assets-prediction-markets` |
| `rule:stablecoin-standards` | rule | `digital-assets-prediction-markets/crypto-venues-perpetuals.tex` | `digital-assets-prediction-markets/stablecoins.tex` | `digital-assets-prediction-markets` |
| `def:distributed-ledger-applications` | definition | `crypto-spot-markets/digital-asset-investing.tex` | `digital-assets-prediction-markets/distributed-ledgers.tex` | `digital-assets-prediction-markets` |

`probability-statistics/resampling.tex` is `common-toolkit/simulation-methods.tex` after the move; `crypto-spot-markets/digital-asset-investing.tex` was moved whole and then lost the distributed-ledger entry back to the opening crypto section. Kept in place by decision: `mod:factor-risk-model` and `meth:var-es-estimation-methods` in `portfolio-construction-risk/risk-models.tex`; the venue, perpetual-funding, risk-layer and auto-deleveraging entries in `digital-assets-prediction-markets/crypto-venues-perpetuals.tex`.

## 5. Entry destination check

All 697 labels have exactly one destination file, and each destination file is input exactly once (`make check-compendium`: no repeated input, cycle or unreachable entry). Entries by destination section: `asset-pricing` 7, `bayesian-inference` 1, `commodity-investing-premia` 5, `corporate-credit-capital` 14, `corporate-finance` 20, `crypto-spot-markets` 1, `crypto-trading-strategies` 1, `currency-markets` 18, `digital-assets-prediction-markets` 7, `energy-commodities` 3, `execution-market-making` 72, `execution-trading-costs` 60, `financial-mathematics` 4, `financial-statement-analysis` 56, `government-bond-markets` 2, `high-dimensional-statistics` 2, `international-equity-markets` 3, `ml-alternative-data` 22, `multi-asset-systematic-macro` 32, `numerical-optimisation` 1, `onchain-protocols` 2, `physical-commodity-markets` 3, `portfolio-construction-risk` 79, `portfolio-risk-financing` 16, `power-gas-environmental` 1, `private-capital-allocator` 17, `private-wealth-management` 15, `probability-statistics` 13, `professional-ethics` 22, `rates-credit-mortgages` 53, `real-asset-investor` 10, `regression-time-series` 17, `research-engineering-validation` 26, `securitised-structured-credit` 5, `stochastic-processes-calculus` 3, `systematic-equities` 45, `volatility-options` 38, `volatility-trading-premia` 1.

## 6. Coverage ownership and navigation

| Topic | Former owner | Owner |
| --- | --- | --- |
| `topic:time-value-of-money` | `common-toolkit` | `financial-mathematics` |
| `topic:return-measurement` | `portfolio-construction-risk` | `financial-mathematics` |
| `topic:descriptive-statistics` | `common-toolkit` | `probability-statistics` |
| `topic:probability-distributions` | `common-toolkit` | `probability-statistics` |
| `topic:stochastic-calculus` | `common-toolkit` | `stochastic-processes-calculus` |
| `topic:statistical-inference` | `common-toolkit` | `probability-statistics` |
| `topic:simulation-methods` | `common-toolkit` | `probability-statistics` |
| `topic:linear-regression` | `common-toolkit` | `regression-time-series` |
| `topic:time-series-models` | `common-toolkit` | `regression-time-series` |
| `topic:asset-pricing-factor-models` | `portfolio-construction-risk` | `asset-pricing` |
| `topic:digital-asset-investment` | `digital-assets-prediction-markets` | `crypto-spot-markets` |
| `topic:strategic-asset-allocation` | `multi-asset-systematic-macro` | `portfolio-construction-risk` |

Other navigation changes: 75 `source` paths in `notes/entry-evidence.json` follow their entries (review texts unchanged); the learning roadmap's chapter column follows the owners and gains the missing `topic:stochastic-calculus` row; 22 new section overview notes; specialist-pathway lists in all 38 overview notes; `common-toolkit.md` rewritten as a bridge above its kept history and `empirical-causal-research.md` added as a bridge; two specialist notes (`high-dimensional-estimation`, `time-series-volatility`) and 22 reading notes point to the successor sections. Historical review records, the coverage log rows and dated notes keep their original paths.

## 7. Guide pathway dispositions

All 222 pathways of the pinned guide, by section. **Note**: a pathway note exists and lists the entries shown. **Related**: no pathway note; the files listed hold existing entries on the subject, not reviewed as a complete treatment. **Partial**: no pathway note; the entries listed, wherever they sit, treat some of the pathway's subtopics, and the subtopics after *Not written* have no entry; not reviewed as a complete treatment. **Gap**: no entry treats the pathway's subject; a passing mention or a general method elsewhere is recorded where the closeout review found one, and is not a treatment. The migration does not create explanations for Partial or Gap pathways.

The Partial state and the Gap annotations come from the closeout review of 22 October 2026, which compared every row first recorded as Gap with all 697 entry titles and bodies by subject terms, then read the candidate entries. A shared citation alone was not counted as coverage.

| Section | Pathway | State | Material |
| --- | --- | --- | --- |
| `financial-mathematics` | `time-value-cash-flows` Time value of money, discounting and cash-flow valuation | Related | `financial-mathematics/time-value` |
| `financial-mathematics` | `return-measurement` Return measurement: holding-period, time-weighted and money-weighted returns | Related | `financial-mathematics/return-measurement` |
| `probability-statistics` | `probability-statistical-inference` Probability, statistical inference and resampling | Related | `probability-statistics/descriptive-statistics`, `probability-statistics/probability`, `probability-statistics/statistical-inference`, `probability-statistics/resampling` |
| `probability-statistics` | `heavy-tails-extremes` Heavy tails, extreme values and dependence | Related | `probability-statistics/extreme-values` |
| `regression-time-series` | `regression-econometrics` Linear regression, GMM and econometric inference | Related | `regression-time-series/regression`, `regression-time-series/multiple-regression` |
| `regression-time-series` | `stationarity-cointegration` Stationarity, ARMA and VAR models, unit roots and cointegration | Related | `regression-time-series/time-series-models` |
| `regression-time-series` | `time-series-volatility` Volatility forecasting, regimes and structural breaks | Note | 2 entries: `regression-time-series/volatility-forecasting` |
| `stochastic-processes-calculus` | `stochastic-calculus-control` Stochastic calculus and continuous-time control | Related | `stochastic-processes-calculus/stochastic-calculus` |
| `bayesian-inference` | `bayesian-parameter-uncertainty` Bayesian inference, shrinkage and parameter uncertainty | Related | `bayesian-inference/bayesian-updating` |
| `high-dimensional-statistics` | `high-dimensional-estimation` High-dimensional estimation: covariance shrinkage, random matrices and factor models | Note | 1 entries: `high-dimensional-statistics/covariance-estimation` |
| `numerical-optimisation` | `numerical-methods-optimisation` Optimisation and numerical methods for pricing and portfolios | Related | `numerical-optimisation/monte-carlo-simulation`, `volatility-options/numerical-methods` |
| `asset-pricing` | `asset-pricing-theory` Asset-pricing theory: stochastic discount factors, CAPM and factor pricing | Related | `asset-pricing/asset-pricing-models` |
| `asset-pricing` | `standard-errors-inference` Standard errors, clustering and weak instruments | Partial | Treated: heteroskedasticity-robust and Newey–West standard errors: `meth:regression-misspecification` (`regression-time-series/multiple-regression`); Sharpe-ratio standard errors under serial correlation: `meth:sharpe-ratio-standard-error` (`research-engineering-validation/backtest-evaluation`); tests with overlapping observations: `meth:correlation-independence-tests` (`probability-statistics/statistical-inference`). Not written: clustered and panel standard errors; weak instruments and IV inference |
| `asset-pricing` | `empirical-asset-pricing` Empirical asset pricing: factor models and tests | Related | `asset-pricing/asset-pricing-models` |
| `asset-pricing` | `return-predictability` Return predictability and forecast evaluation | Partial | Treated: out-of-sample forecast evaluation against benchmarks: `meth:forecast-accuracy-evaluation` (`regression-time-series/time-series-models`); Welch and Goyal's in- and out-of-sample equity-premium predictability: `meth:backtest-evaluation-diagnostics` (`research-engineering-validation/backtest-evaluation`); own predictive tests with Clark–West statistics: `def:contango-backwardation-stocks` (`energy-commodities/commodity-curves`), `meth:fx-valuation-signals` (`currency-markets/macro-fx`). Not written: predictive-regression bias and long-horizon inference; economic value of return forecasts |
| `asset-pricing` | `event-studies` Event studies and long-run abnormal returns | Partial | Treated: an announcement-window event study and the limits of its window choice: `def:central-bank-policy-framework` (`rates-credit-mortgages/monetary-policy-curves`); the market model separating market-related from residual returns: `mod:return-generating-models` (`asset-pricing/asset-pricing-models`). Not written: estimation- and event-window design; abnormal-return test statistics; long-run abnormal returns |
| `causal-inference` | `causal-research-designs` Causal research designs: DiD, synthetic control and RD | Gap |  |
| `causal-inference` | `causal-policy-evaluation` Causal ML and financial policy evaluation | Gap |  |
| `causal-inference` | `controlled-experiments` Controlled experiments: A/B tests, switchbacks and sequential monitoring | Gap |  |
| `research-engineering-validation` | `backtest-inference` Backtest inference, multiple testing and Sharpe-ratio statistics | Note | 9 entries: `research-engineering-validation/backtest-evaluation`, `research-engineering-validation/scenario-simulation` |
| `research-engineering-validation` | `point-in-time-data` Point-in-time data, vendor files and bias control | Note | 5 entries: `research-engineering-validation/point-in-time-data` |
| `research-engineering-validation` | `model-governance-controls` Model governance, AI risk and trading controls | Note | 9 entries: `research-engineering-validation/strategy-production`, `research-engineering-validation/strategy-risk`, `research-engineering-validation/trading-controls` |
| `research-engineering-validation` | `reproducible-research-code` Reproducible research code, data validation and ML systems | Related | `research-engineering-validation/strategy-production` |
| `professional-ethics` | `ethics-code-standards` Codes of ethics, professional standards and enforcement | Related | `professional-ethics/ethics-trust-framework`, `professional-ethics/code-standards-enforcement`, `professional-ethics/standards-professionalism-markets` |
| `professional-ethics` | `fiduciary-duties-conflicts` Duties to clients, conflicts of interest and asset-manager responsibilities | Related | `professional-ethics/standards-clients-employers`, `professional-ethics/standards-analysis-conflicts-members`, `professional-ethics/conduct-cases`, `professional-ethics/asset-manager-code` |
| `ml-alternative-data` | `statistical-learning-foundations` Statistical learning foundations and time-series validation | Note | 19 entries: `ml-alternative-data/data-science-workflow`, `ml-alternative-data/financial-data-structures`, `ml-alternative-data/fractional-differentiation`, `ml-alternative-data/labelling-sample-weights`, `ml-alternative-data/machine-learning-methods` |
| `ml-alternative-data` | `ml-asset-pricing` ML return prediction and asset pricing | Partial | Treated: deep-learning short-horizon return forecasts from order-book data: `def:order-flow-imbalance` (`execution-market-making/order-books`). Not written: cross-sectional ML return prediction; ML asset-pricing and latent-factor models |
| `ml-alternative-data` | `financial-ml-evaluation` Financial ML: information timing, uncertainty and portfolio tests | Note | 2 entries: `ml-alternative-data/labelling-sample-weights` |
| `ml-alternative-data` | `forecasting-generative-rl` Deep forecasting and generative scenarios | Partial | Treated: deep sequence models for order-book forecasting, their horizons and transfer: `def:order-flow-imbalance` (`execution-market-making/order-books`). Not written: deep forecasting beyond the order book; generative scenario models |
| `ml-alternative-data` | `reinforcement-learning-trading` Reinforcement learning for trading, hedging and execution | Note | 1 entries: `execution-trading-costs/execution-control` |
| `ml-alternative-data` | `text-llm-agents` Text, language models and agent evaluation | Related | `ml-alternative-data/data-science-workflow` |
| `ml-alternative-data` | `alternative-data-sources` Alternative data: sources, information value and market effects | Note | 1 entries: `ml-alternative-data/financial-data-types` |
| `rates-credit-mortgages` | `curve-term-structure` Yield-curve construction and term-structure models | Note | 2 entries: `rates-credit-mortgages/interest-rates`, `rates-credit-mortgages/monetary-policy-curves` |
| `rates-credit-mortgages` | `rate-derivatives` Interest-rate derivatives, volatility and RFR conventions | Note | 2 entries: `rates-credit-mortgages/monetary-policy-curves`, `volatility-options/option-pricing` |
| `rates-credit-mortgages` | `monetary-policy-curve` Monetary policy, balance-sheet policy and the yield curve | Note | 6 entries: `rates-credit-mortgages/monetary-fiscal-policy`, `rates-credit-mortgages/monetary-policy-curves` |
| `rates-credit-mortgages` | `bond-risk-premia` Bond risk premia, predictability and systematic rates strategies | Related | `rates-credit-mortgages/term-structure-returns`, `rates-credit-mortgages/fixed-income-portfolio-management` |
| `rates-credit-mortgages` | `rates-inflation` Inflation-linked bonds, real yields and breakevens | Note | 1 entries: `rates-credit-mortgages/monetary-policy-curves` |
| `government-bond-markets` | `treasury-market-functioning` Treasury market structure, basis trades and dealer capacity | Partial | Treated: Treasury trading protocols, interdealer venues and dealer risk-bearing: `def:fixed-income-market-structure` (`execution-trading-costs/fixed-income-trading`); Treasury futures delivery, cheapest-to-deliver and futures below the bond: `conv:government-bond-futures` (`execution-trading-costs/futures-execution`). Not written: basis-trade financing and leverage; dealer balance-sheet capacity and stress episodes |
| `government-bond-markets` | `treasury-issuance-demand` Government debt issuance, auctions and investor demand | Partial | Treated: Treasury instruments and single-price auctions on a pre-announced calendar: `def:government-agency-supranational-funding` (`rates-credit-mortgages/bond-instruments-markets`); yield effects of central-bank purchases: `def:central-bank-policy-framework` (`rates-credit-mortgages/monetary-policy-curves`). Not written: auction outcomes and investor demand; supply effects of issuance on yields |
| `government-bond-markets` | `sovereign-municipal` Sovereign default, restructuring and local-currency debt | Note | 2 entries: `government-bond-markets/sovereign-credit` |
| `government-bond-markets` | `municipal-bonds` Municipal bonds: pledges, taxes, trading costs and climate risk | Partial | Treated: general-obligation against revenue pledges: `def:government-agency-supranational-funding` (`rates-credit-mortgages/bond-instruments-markets`), `meth:sovereign-credit-analysis` (`government-bond-markets/sovereign-credit`); municipal tax treatment and tax-exempt portfolios: `rule:bond-issuance-legal-tax` (`rates-credit-mortgages/bond-instruments-markets`), `meth:bond-leverage-taxation` (`rates-credit-mortgages/fixed-income-portfolio-management`); fragmentation of municipal trading: `def:fixed-income-market-structure` (`execution-trading-costs/fixed-income-trading`). Not written: municipal trading-cost evidence; climate risk |
| `government-bond-markets` | `dm-sovereign-bonds` Euro-area, UK and Japanese government bond markets | Gap | Mention only, not a treatment: `conv:government-bond-futures` (`execution-trading-costs/futures-execution`) (German Schatz, Bobl and Bund futures maturities) |
| `financial-statement-analysis` | `financial-reporting-statements` Financial reporting frameworks and the three financial statements | Related | `financial-statement-analysis/financial-reporting-framework`, `financial-statement-analysis/income-statement-analysis`, `financial-statement-analysis/balance-sheet-analysis`, `financial-statement-analysis/cash-flow-analysis`, `financial-statement-analysis/company-case` |
| `financial-statement-analysis` | `accounting-measurement` Accounting measurement: revenue, inventories, long-lived assets, leases, employee benefits and income taxes | Related | `financial-statement-analysis/inventory-accounting`, `financial-statement-analysis/long-lived-asset-accounting`, `financial-statement-analysis/leases-employee-compensation`, `financial-statement-analysis/income-tax-accounting` |
| `financial-statement-analysis` | `group-international-reporting` Group accounts, intercorporate investments and foreign-currency reporting | Related | `financial-statement-analysis/intercorporate-investments`, `financial-statement-analysis/foreign-currency-reporting` |
| `financial-statement-analysis` | `financial-ratio-quality` Financial ratio analysis, earnings quality and misstatement detection | Related | `financial-statement-analysis/ratio-analysis`, `financial-statement-analysis/financial-reporting-quality`, `financial-statement-analysis/financial-institution-analysis` |
| `financial-statement-analysis` | `financial-statement-forecasting` Financial statement forecasting and integrated company analysis | Related | `financial-statement-analysis/financial-statement-modelling`, `financial-statement-analysis/integrated-statement-analysis` |
| `corporate-finance` | `capital-budgeting-investment` Capital budgeting, project valuation and working capital | Related | `corporate-finance/capital-investment`, `corporate-finance/working-capital-liquidity` |
| `corporate-finance` | `capital-structure-payout` Capital structure, cost of capital and payout policy | Related | `corporate-finance/capital-structure-cost-of-capital`, `corporate-finance/payout-policy` |
| `corporate-finance` | `corporate-governance-restructuring` Ownership, corporate governance, mergers and restructuring | Related | `corporate-finance/corporate-ownership-governance`, `corporate-finance/business-models`, `corporate-finance/corporate-restructuring` |
| `corporate-credit-capital` | `credit-models-default` Credit models, default prediction and credit portfolios | Related | `corporate-credit-capital/credit-risk-analysis`, `corporate-credit-capital/credit-portfolio-management` |
| `corporate-credit-capital` | `corporate-credit-cds` Corporate bonds and credit derivatives | Note | 18 entries: `corporate-credit-capital/credit-default-swaps`, `corporate-credit-capital/credit-portfolio-management`, `corporate-credit-capital/credit-risk-analysis`, `portfolio-risk-financing/counterparty-xva` |
| `corporate-credit-capital` | `bank-capital` Bank capital, AT1, CoCos and Tier 2 | Partial | Treated: Basel risk-based capital and leverage requirements: `def:financial-institution-features` (`financial-statement-analysis/financial-institution-analysis`); capital ratios in bank analysis: `meth:bank-camels-analysis` (`financial-statement-analysis/financial-institution-analysis`). Not written: AT1, CoCo and Tier 2 instrument terms, triggers, loss absorption and pricing |
| `corporate-credit-capital` | `corporate-hybrids-preferred` Corporate hybrids and preferred shares | Partial | Treated: preferred-stock valuation with call, put, conversion and floating-rate features: `meth:preferred-stock-valuation` (`systematic-equities/dividend-discount-models`); preferred stock among equity instruments: `def:equity-instruments` (`systematic-equities/equity-securities-markets`). Not written: corporate hybrid bonds: subordination, coupon deferral, rating-agency equity credit, calls and step-ups |
| `corporate-credit-capital` | `sustainable-bonds` Green, transition and sustainability-linked bonds | Gap |  |
| `securitised-structured-credit` | `covered-bonds` Covered bonds and extendable maturity | Partial | Treated: dual recourse and covered bonds against securitisation: `meth:abs-structures-credit-enhancement` (`securitised-structured-credit/securitisation`), `meth:credit-cds-international-structured` (`corporate-credit-capital/credit-portfolio-management`). Not written: extendable maturities; covered-bond spreads and regulatory treatment |
| `securitised-structured-credit` | `sukuk` Sukuk: ownership, recourse and relative value | Gap |  |
| `securitised-structured-credit` | `mortgages-abs-clo` Mortgages, ABS and CLO waterfalls | Related | `securitised-structured-credit/securitisation` |
| `securitised-structured-credit` | `synthetic-risk-transfer` Synthetic risk transfer and credit-linked notes | Related | `securitised-structured-credit/default-correlation` |
| `securitised-structured-credit` | `cmbs-workouts` CMBS, servicing and property workouts | Partial | Treated: CMBS call protection, the special servicer as B-piece holder and balloon risk: `meth:mortgage-securities-prepayment` (`securitised-structured-credit/securitisation`). Not written: servicing standards; modification and foreclosure outcomes; loss severities |
| `systematic-equities` | `equity-factor-premia` Equity factor premia, crashes and timing | Partial | Treated: value, momentum, quality and carry premia across markets: `def:alpha-model-taxonomy` (`research-engineering-validation/quant-strategy-structure`); size, value, momentum and reversal anomalies with behavioural explanations: `mech:biases-market-anomalies` (`portfolio-construction-risk/behavioural-finance`); factor timing by volatility scaling: `ev:volatility-managed-portfolios` (`portfolio-construction-risk/portfolio-construction-models`); factor (smart-beta) indexes: `def:cap-weighted-factor-indexing` (`systematic-equities/equity-portfolio-management`). Not written: factor crashes; valuation- and momentum-based factor timing; post-publication decay |
| `systematic-equities` | `statistical-arbitrage` Statistical arbitrage and short-horizon equity strategies | Partial | Treated: residual mean reversion (Avellaneda–Lee), distance pairs (Gatev et al.) and the Lo–MacKinlay contrarian decomposition: `def:alpha-model-taxonomy` (`research-engineering-validation/quant-strategy-structure`); pairs trading as an active equity strategy: `def:active-equity-strategies` (`systematic-equities/equity-portfolio-management`); cointegration of a pairs spread: `meth:cointegration-testing` (`regression-time-series/time-series-models`); the August 2007 quant unwind: `def:common-investor-contagion` (`portfolio-risk-financing/crowding-contagion`). Not written: short-horizon reversal evidence net of costs; capacity and implementation at scale |
| `systematic-equities` | `demand-flows-passive` Demand-based asset pricing, flows and passive investing | Partial | Treated: price pressure from index-fund trading at reconstitution: `ev:index-reconstitution-impact` (`execution-trading-costs/impact-models`); index funds' timing of index changes: `meth:index-equity-portfolio-construction` (`systematic-equities/equity-portfolio-management`). Not written: demand-system asset pricing and inelastic markets; fund-flow effects; effects of rising passive ownership |
| `systematic-equities` | `equity-events-fundamentals` Fundamental valuation and accounting signals | Related | `systematic-equities/industry-company-analysis`, `systematic-equities/equity-research-reporting`, `systematic-equities/equity-valuation-foundations`, `systematic-equities/dividend-discount-models`, `systematic-equities/market-multiples`, `systematic-equities/free-cash-flow-valuation`, `systematic-equities/residual-income-valuation`, `systematic-equities/private-company-valuation` |
| `systematic-equities` | `equity-trader-signals` Short-selling, option, insider and retail-flow signals | Partial | Treated: insider-trade signals, opportunistic against routine insiders: `def:financial-data-types` (`ml-alternative-data/financial-data-types`); filing deadlines for insider and holdings data: `data:holdings-insider-filing-lags` (`research-engineering-validation/point-in-time-data`). Not written: short-interest and lending-fee signals; option-implied signals; retail-flow signals |
| `systematic-equities` | `equity-long-short-construction` Equity signal combination, risk models and long–short portfolios | Note | 9 entries: `systematic-equities/equity-portfolio-management`, `systematic-equities/signal-combination` |
| `systematic-equities` | `equity-event-driven` Earnings, corporate events and merger arbitrage | Partial | Treated: merger arbitrage among event-driven strategies: `meth:hedge-fund-strategy-classification` (`portfolio-construction-risk/hedge-fund-strategies`); activist returns around Schedule 13D filings: `def:active-equity-strategies` (`systematic-equities/equity-portfolio-management`), `def:equity-portfolio-roles-mandate` (`systematic-equities/equity-portfolio-management`); post-earnings drift and accrual returns around announcements: `mech:biases-market-anomalies` (`portfolio-construction-risk/behavioural-finance`), `meth:earnings-quality-persistence` (`financial-statement-analysis/financial-reporting-quality`). Not written: earnings-announcement return measurement; merger-arbitrage returns and deal-failure risk |
| `volatility-options` | `option-pricing-models` Stochastic, local and jump volatility models | Note | 2 entries: `volatility-options/option-pricing` |
| `volatility-options` | `convertible-bonds` Convertible bonds and credit-equity hedging | Related | `rates-credit-mortgages/embedded-option-bonds` |
| `volatility-options` | `volatility-models` Rough and path-dependent volatility | Gap | General models only, not a treatment: `mod:heston-stochastic-volatility` (`volatility-options/option-pricing`), `mod:sabr-smile` (`volatility-options/option-pricing`) (classical stochastic volatility; no rough or path-dependent model) |
| `volatility-options` | `option-hedging-smile` Option hedging: delta, vega, smile dynamics and transaction costs | Related | `volatility-options/option-valuation`, `volatility-options/option-strategies` |
| `volatility-options` | `learning-pricing-model-risk` Learning-based pricing, calibration and model risk | Gap | General governance only, not a treatment: `meth:strategy-promotion-criteria` (`research-engineering-validation/strategy-production`) (supervisory model-risk guidance applied to strategy models) |
| `volatility-options` | `exotics-structured-products` Exotic options, autocallables and structured products | Related | `volatility-options/exotic-options` |
| `volatility-trading-premia` | `option-premia-dealers` Option returns, variance premia and dealer hedging | Partial | Treated: the variance risk premium in variance-swap strikes and selling variance: `def:vix-variance-dividend-swaps` (`volatility-trading-premia/vix-variance-dividends`), `meth:volatility-derivative-applications` (`portfolio-construction-risk/derivative-overlays`); hedged-option profit when implied and realised volatility differ: `res:delta-hedging-volatility-mismatch` (`volatility-options/option-valuation`); dealers' hedging and inventory risk in option spreads: `res:option-market-maker-spreads` (`execution-market-making/options-dealing`). Not written: option-return evidence; dealer gamma positioning and its effect on the underlying |
| `volatility-trading-premia` | `option-implied-information` Option-implied densities, tail risk and expected returns | Partial | Treated: the butterfly condition as a non-negative implied density: `def:implied-volatility-surface` (`volatility-options/option-pricing`); risk-neutral probabilities from call spreads: `meth:derivative-overlay-allocation` (`portfolio-construction-risk/derivative-overlays`). Not written: density extraction; tail-risk and implied-moment measures; their return predictability |
| `volatility-trading-premia` | `equity-option-returns` Single-stock option returns: volatility mispricing, characteristics and factors | Gap |  |
| `volatility-trading-premia` | `vix-correlation-dividends` VIX, correlation and dividend derivatives | Note | 1 entries: `volatility-trading-premia/vix-variance-dividends` |
| `volatility-trading-premia` | `short-dated-retail-options` Short-dated options, 0DTE and retail option trading | Partial | Treated: retail option routing, payment for order flow and wholesaler internalisation: `mech:options-retail-wholesaler-routing` (`execution-market-making/options-dealing`). Not written: 0DTE options; retail option returns and behaviour |
| `multi-asset-systematic-macro` | `cross-asset-style-premia` Cross-asset style premia: value, momentum, carry and defensive | Note | 1 entries: `multi-asset-systematic-macro/macro-regimes-data` |
| `multi-asset-systematic-macro` | `trend-following` Trend following and managed futures | Partial | Treated: time-series momentum construction and century-long evidence: `def:alpha-model-taxonomy` (`research-engineering-validation/quant-strategy-structure`); CTAs and managed futures as diversifiers: `meth:hedge-fund-strategy-classification` (`portfolio-construction-risk/hedge-fund-strategies`), `def:alternatives-roles-opportunity-set` (`portfolio-construction-risk/alternatives-allocation`), `def:global-macro-strategy` (`multi-asset-systematic-macro/global-macro`); Turtle-style volatility sizing: `meth:macro-position-sizing-risk` (`multi-asset-systematic-macro/global-macro`); trend followers' win rates and drawdowns: `meth:alpha-strategy-specification` (`research-engineering-validation/quant-strategy-structure`), `meth:rule-based-position-sizing` (`portfolio-construction-risk/portfolio-construction-models`). Not written: trend-signal design and horizon choice; managed-futures fees, capacity and replication |
| `multi-asset-systematic-macro` | `risk-parity-vol-targeting` Risk parity, leverage and volatility targeting | Note | 1 entries: `portfolio-construction-risk/portfolio-construction-models` |
| `multi-asset-systematic-macro` | `macro-announcements-policy` Macro announcements, policy news and announcement premia | Note | 2 entries: `multi-asset-systematic-macro/macro-regimes-data` |
| `multi-asset-systematic-macro` | `macro-regimes-stock-bond` Macro regimes, inflation and the stock–bond correlation | Note | 1 entries: `multi-asset-systematic-macro/macro-regimes-data` |
| `multi-asset-systematic-macro` | `macro-nowcasting-signals` Nowcasting, real-time macro data and macro trading signals | Note | 2 entries: `multi-asset-systematic-macro/macro-regimes-data` |
| `currency-markets` | `fx-determination-forecasting` Exchange-rate determination, forecasting and order flow | Note | 1 entries: `currency-markets/macro-fx` |
| `currency-markets` | `fx-funding-settlement` FX forwards, options, fixes and settlement | Related | `currency-markets/fx-mechanics-parity` |
| `currency-markets` | `fx-premia` Currency premia: carry, momentum, value and the dollar | Note | 1 entries: `currency-markets/macro-fx` |
| `currency-markets` | `fx-cip-dollar-funding` Covered interest parity, the cross-currency basis and dollar funding | Note | 2 entries: `currency-markets/macro-fx`, `volatility-options/forward-commitment-valuation` |
| `currency-markets` | `fx-volatility-crash-risk` FX volatility, skew and crash risk | Partial | Treated: carry crash risk and negative skew: `meth:carry-trade-uip` (`currency-markets/fx-mechanics-parity`), `mod:fx-carry-trade` (`currency-markets/macro-fx`); FX volatility trading with straddles and risk reversals: `meth:active-currency-strategies` (`currency-markets/currency-management`); option structures for currency hedging: `meth:currency-hedge-cost-reduction` (`currency-markets/currency-management`). Not written: FX volatility-surface quoting conventions; FX volatility and skew premia |
| `currency-markets` | `currency-hedging` Currency hedging for international portfolios | Related | `currency-markets/currency-management` |
| `currency-markets` | `em-currencies-intervention` Emerging-market currencies: regimes, intervention and the global financial cycle | Note | 1 entries: `currency-markets/macro-fx` |
| `international-equity-markets` | `intl-equity-integration` Equity index construction, international integration, diversification and home bias | Related | `international-equity-markets/index-construction`, `international-equity-markets/equity-indices` |
| `international-equity-markets` | `global-equity-factors` Global equity factors, country selection and return predictability | Partial | Treated: country and sector selection by valuation: `meth:equity-index-valuation` (`multi-asset-systematic-macro/macro-regimes-data`); integration-weighted equity premia: `meth:asset-class-return-forecasts` (`multi-asset-systematic-macro/capital-market-expectations`); value and momentum across countries and asset classes: `def:alpha-model-taxonomy` (`research-engineering-validation/quant-strategy-structure`). Not written: global factor models; country-level return predictability |
| `international-equity-markets` | `em-frontier-equities` Emerging and frontier equity markets: liberalisation, foreign investors and liquidity | Partial | Treated: emerging-market equity premia under partial integration, and governance risks: `meth:asset-class-return-forecasts` (`multi-asset-systematic-macro/capital-market-expectations`). Not written: liberalisation effects; foreign investors and flows; frontier-market liquidity |
| `international-equity-markets` | `cross-listing-global-trading` Cross-listings, ADRs and asynchronous global trading | Partial | Treated: ADR mechanics and currency exposure: `def:equity-indices-derivatives` (`international-equity-markets/equity-indices`). Not written: cross-listing motives and valuation effects; ADR parity and arbitrage; asynchronous trading across time zones |
| `international-equity-markets` | `china-em-equities` China's stock market: factors, retail trading, intervention and access | Gap |  |
| `global-regional-markets` | `em-capital-flows` Capital flows, global investors and benchmark effects | Partial | Treated: capital flows, sudden reversals, intervention and capital controls: `def:flows-policy-exchange-rates` (`currency-markets/fx-mechanics-parity`), `def:exchange-rate-regimes-capital-flows` (`currency-markets/fx-mechanics-parity`). Not written: global investors and benchmark-driven flows |
| `global-regional-markets` | `em-local-currency-bonds` Emerging-market local-currency government bonds: original sin, foreign holders and index inclusion | Partial | Treated: local- against foreign-currency sovereign debt for foreign holders: `meth:sovereign-credit-analysis` (`government-bond-markets/sovereign-credit`); emerging-market debt return expectations: `meth:asset-class-return-forecasts` (`multi-asset-systematic-macro/capital-market-expectations`). Not written: original sin; foreign holdings and index inclusion |
| `global-regional-markets` | `regional-local-market-access` Regional local-market access and settlement | Gap |  |
| `portfolio-construction-risk` | `portfolio-construction` Portfolio construction, estimation error and risk models | Note | 13 entries: `high-dimensional-statistics/covariance-estimation`, `portfolio-construction-risk/portfolio-construction-models`, `portfolio-construction-risk/risk-models`, `portfolio-construction-risk/transaction-cost-models`, `regression-time-series/volatility-forecasting` |
| `portfolio-construction-risk` | `risk-tail-systemic` Market risk, tail hedging and systemic stress | Note | 2 entries: `portfolio-construction-risk/risk-models`, `probability-statistics/extreme-values` |
| `portfolio-construction-risk` | `performance-manager-evaluation` Performance attribution and manager evaluation | Note | 19 entries: `financial-mathematics/return-measurement`, `portfolio-construction-risk/manager-selection`, `portfolio-construction-risk/performance-attribution-appraisal`, `portfolio-construction-risk/performance-evaluation`, `portfolio-construction-risk/performance-standards` |
| `portfolio-construction-risk` | `climate-sustainable` Climate risk and sustainable portfolios | Partial | Treated: ESG approaches, climate risk and carbon-intensity against tracking-error trade-offs: `meth:institutional-esg-integration` (`portfolio-construction-risk/institutional-portfolios`); climate scenarios in a sovereign fund's risk management: `meth:swf-risk-case` (`portfolio-construction-risk/institutional-portfolios`); evaluating issuers' ESG exposures: `meth:esg-exposure-evaluation` (`corporate-finance/corporate-ownership-governance`). Not written: evidence on climate-risk pricing; climate benchmark construction |
| `portfolio-risk-financing` | `funding-crowding` Funding liquidity, crowding and arbitrage capital | Note | 2 entries: `portfolio-risk-financing/crowding-contagion` |
| `portfolio-risk-financing` | `money-markets-repo-lending` Money markets, repo and securities lending | Note | 7 entries: `portfolio-risk-financing/money-markets`, `portfolio-risk-financing/securities-lending` |
| `portfolio-risk-financing` | `collateral-xva` Collateral, counterparty risk and xVA | Related | `portfolio-risk-financing/counterparty-xva` |
| `portfolio-risk-financing` | `alm-liquidity` Asset-liability management, institutional investment policy and liquidity | Related | `portfolio-construction-risk/institutional-portfolios` |
| `portfolio-risk-financing` | `synthetic-equity-cfd-trs` CFDs, total return swaps and synthetic equity financing | Note | 2 entries: `portfolio-risk-financing/synthetic-shorts` |
| `execution-market-making` | `market-making-lob` Market making, queues and limit-order-book models | Note | 16 entries: `execution-market-making/market-making-models`, `execution-market-making/order-books`, `execution-market-making/order-flow-statistics` |
| `execution-market-making` | `lob-deep-learning` Deep learning on limit-order-book data | Note | 1 entries: `execution-market-making/order-books` |
| `execution-market-making` | `options-execution` Options market making and execution costs | Note | 3 entries: `execution-market-making/options-dealing` |
| `execution-market-making` | `bond-swap-dealer-market-making` Bond and swap dealing: RFQs, inventory and balance-sheet capacity | Partial | Treated: RFQ protocols, venues and dealer risk-bearing in fixed income: `def:fixed-income-market-structure` (`execution-trading-costs/fixed-income-trading`); OTC derivative execution by RFQ: `def:trade-implementation-by-market` (`execution-trading-costs/trade-strategy-governance`). Not written: RFQ quoting and inventory models for bonds and swaps; balance-sheet capacity constraints |
| `execution-market-making` | `market-simulation` Market simulation and counterfactual testing | Note | 5 entries: `execution-market-making/order-flow-statistics` |
| `execution-market-making` | `fx-dealer-market-making` FX dealing: internalisation, last look and hedging | Note | 3 entries: `execution-market-making/fx-dealing` |
| `execution-market-making` | `hft-market-design` High-frequency trading, speed and adverse selection | Note | 7 entries: `execution-market-making/high-frequency-trading` |
| `execution-trading-costs` | `price-impact-execution` Price impact, optimal execution and TCA | Note | 10 entries: `execution-trading-costs/impact-models`, `execution-trading-costs/trade-signing` |
| `execution-trading-costs` | `market-structure-execution-quality` Market structure rules, fees and execution quality | Note | 19 entries: `execution-trading-costs/dark-trading-fragmentation`, `execution-trading-costs/execution-quality`, `execution-trading-costs/market-regulation`, `execution-trading-costs/smart-order-routing`, `execution-trading-costs/tick-size` |
| `execution-trading-costs` | `otc-fixed-income-trading` Fixed-income and OTC electronic trading | Note | 3 entries: `execution-trading-costs/fixed-income-trading` |
| `execution-trading-costs` | `etf-index-closing-execution` ETFs, index events and closing auctions | Note | 3 entries: `execution-trading-costs/etf-mechanics` |
| `execution-trading-costs` | `futures-execution` Futures execution: matching, rolls and settlement | Note | 5 entries: `execution-trading-costs/futures-execution` |
| `execution-trading-costs` | `retail-cfd-brokers` Retail CFDs: leverage limits, broker risk and client outcomes | Gap | General mechanism only, not a treatment: `mod:fx-internalisation-horizon` (`execution-market-making/fx-dealing`) (a dealer internalising client risk) |
| `energy-commodities` | `commodity-storage-curves` Theory of storage, convenience yield and inventories | Note | 1 entries: `energy-commodities/commodity-curves` |
| `energy-commodities` | `commodity-curve-models` Commodity term-structure models: factor, seasonal and jump models | Gap | Foundations only, not a treatment: `def:contango-backwardation-stocks` (`energy-commodities/commodity-curves`) (storage and curve shapes; no factor, seasonal or jump model) |
| `energy-commodities` | `commodity-hedging` Commodity hedging: hedge ratios, rolling hedges and corporate risk management | Note | 2 entries: `energy-commodities/futures-hedging` |
| `energy-commodities` | `commodity-options-real-options` Commodity options, spread options and real options | Partial | Treated: real options to delay, expand and abandon: `meth:capital-allocation-principles` (`corporate-finance/capital-investment`). Not written: commodity option and spread-option valuation; real-option valuation of commodity assets |
| `commodity-spot-markets` | `commodity-spot-benchmarks` Spot price assessment and benchmarks: price reporting agencies, auctions and contract pricing | Partial | Treated: WTI and Brent as crude benchmarks: `def:crude-oil-markets` (`physical-commodity-markets/physical-markets`). Not written: price-reporting-agency assessment; auctions and contract pricing |
| `commodity-spot-markets` | `commodity-spatial-arbitrage` Spatial arbitrage and market integration: transport costs, pipelines and information | Gap | Mention only, not a treatment: `def:crude-oil-markets` (`physical-commodity-markets/physical-markets`) (the Brent premium over WTI and Cushing pipeline constraints) |
| `commodity-spot-markets` | `commodity-price-cycles` Commodity price cycles, comovement and macro drivers | Gap |  |
| `commodity-spot-markets` | `commodity-stabilisation-trade-policy` Price stabilisation, public stocks and export restrictions | Gap |  |
| `commodity-spot-markets` | `commodity-long-run-prices` Long-run commodity prices: exhaustibility, secular trends and supercycles | Gap |  |
| `physical-commodity-markets` | `futures-delivery-manipulation` Futures contract design, delivery options, convergence and manipulation | Related | `physical-commodity-markets/physical-markets` |
| `physical-commodity-markets` | `metals-storage-delivery` Precious and base metals: storage, lending and delivery | Note | 1 entries: `physical-commodity-markets/physical-markets` |
| `physical-commodity-markets` | `agricultural-futures-delivery` Agricultural futures, crop balance and delivery | Note | 1 entries: `physical-commodity-markets/physical-markets` |
| `physical-commodity-markets` | `crude-oil-products` Crude oil and refined products: benchmarks, spreads and price reporting | Note | 1 entries: `physical-commodity-markets/physical-markets` |
| `physical-commodity-markets` | `commodity-information-discovery` Price discovery and fundamental information: crop and inventory reports, analysts and satellites | Partial | Treated: inventory data as a return predictor (own bounded test) and the WASDE balance: `def:contango-backwardation-stocks` (`energy-commodities/commodity-curves`). Not written: announcement effects of crop and inventory reports; analysts and satellite data |
| `physical-commodity-markets` | `freight-forward-hedging` Freight markets, Baltic benchmarks and FFAs | Gap | Mention only, not a treatment: `meth:equity-macro-leading-indicators` (`multi-asset-systematic-macro/macro-regimes-data`) (the Baltic Dry Index and FFA settlement) |
| `physical-commodity-markets` | `commodity-trading-finance` Commodity trading firms, financing and margin stress | Gap |  |
| `commodity-investing-premia` | `commodity-premia` Commodity risk premia: hedging pressure, inventories and the basis | Related | `commodity-investing-premia/commodity-futures-investing` |
| `commodity-investing-premia` | `commodity-factor-strategies` Commodity factor strategies: carry, momentum, trend, curve and skewness | Partial | Treated: commodity carry and time-series momentum evidence: `def:alpha-model-taxonomy` (`research-engineering-validation/quant-strategy-structure`); roll return: `meth:commodity-futures-return-components` (`commodity-investing-premia/commodity-futures-investing`); backwardation as a return predictor (own bounded test): `def:contango-backwardation-stocks` (`energy-commodities/commodity-curves`). Not written: cross-sectional momentum, curve and skewness strategies |
| `commodity-investing-premia` | `commodity-financialisation` Financialisation, speculation and index investing in commodity markets | Gap | Index products only, not a treatment: `def:commodity-indices-risk-return` (`commodity-investing-premia/commodity-indices`), `meth:commodity-swaps-index-construction` (`commodity-investing-premia/commodity-futures-investing`) (no treatment of price effects) |
| `commodity-investing-premia` | `commodity-allocation-inflation` Commodities in multi-asset portfolios: diversification and inflation hedging | Related | `commodity-investing-premia/commodity-futures-investing` |
| `commodity-investing-premia` | `commodity-index-products` Commodity index products: index rules, roll costs, ETFs and flow effects | Note | 5 entries: `commodity-investing-premia/commodity-futures-investing`, `commodity-investing-premia/commodity-indices` |
| `oil-shocks-macro` | `oil-price-shocks` Oil supply and demand shocks: structural identification and elasticities | Gap | Mention only, not a treatment: `def:crude-oil-markets` (`physical-commodity-markets/physical-markets`) (OPEC spare capacity) |
| `oil-shocks-macro` | `oil-price-forecasting` Forecasting the real price of oil: futures, VARs and forecast combinations | Gap |  |
| `oil-shocks-macro` | `oil-shocks-inflation-policy` Oil shocks, inflation and monetary policy | Gap |  |
| `oil-shocks-macro` | `oil-asset-prices` Oil shocks and asset prices: equities, oil risk factors and currencies | Gap |  |
| `power-gas-environmental` | `gas-hub-pricing` Natural gas markets: hub pricing, oil indexation, market integration and supply shocks | Note | 1 entries: `power-gas-environmental/natural-gas` |
| `power-gas-environmental` | `physical-lng` Natural gas storage, transport and LNG optionality | Gap | Mention only, not a treatment: `def:natural-gas-market` (`power-gas-environmental/natural-gas`) (LNG and the Henry Hub contract) |
| `power-gas-environmental` | `power-ftr` Power, storage and transmission rights | Gap |  |
| `power-gas-environmental` | `power-market-design` Electricity market design: scarcity pricing, capacity and market power | Gap |  |
| `power-gas-environmental` | `renewables-ppa-value` Renewable value, cannibalisation and PPA risk | Gap | Mention only, not a treatment: `meth:infrastructure-underwriting` (`real-asset-investor/infrastructure`) (yieldcos, merchant risk and offtaker credit) |
| `power-gas-environmental` | `power-price-forecasting` Electricity price modelling and forecasting | Gap | Mention only, not a treatment: `meth:commodity-sectors-participants` (`commodity-investing-premia/commodity-futures-investing`) (non-storable electricity and price spikes) |
| `power-gas-environmental` | `power-short-term-flexibility` Short-term power markets: intraday trading, balancing, negative prices and storage arbitrage | Gap |  |
| `environmental-markets` | `carbon-compliance-markets` Emissions trading: cap-and-trade design, banking and supply control | Gap |  |
| `environmental-markets` | `carbon-allowance-derivatives` Carbon allowance prices: drivers, derivatives, participants and hedging | Gap |  |
| `environmental-markets` | `carbon-pass-through-leakage` Carbon costs in power and industry: pass-through, leakage and border adjustment | Gap |  |
| `environmental-markets` | `voluntary-carbon-credits` Voluntary carbon and biodiversity credits: integrity, pricing and Article 6 | Gap |  |
| `environmental-markets` | `environmental-instruments` Renewable energy certificates and low-carbon fuel credits: RECs, RINs and LCFS | Gap |  |
| `private-capital-allocator` | `pe-performance-measurement` Private-market performance measurement and replication | Related | `private-capital-allocator/alternative-investment-structures`, `private-capital-allocator/private-market-programmes` |
| `private-capital-allocator` | `private-equity-vc` Private equity and venture security design | Related | `private-capital-allocator/private-capital-foundations`, `private-capital-allocator/private-equity-strategies` |
| `private-capital-allocator` | `private-credit-workouts` Private credit and workouts | Related | `private-capital-allocator/private-debt-special-situations` |
| `private-capital-allocator` | `trade-receivables` Trade finance and purchased receivables | Gap |  |
| `private-capital-allocator` | `royalty-rights` Music and pharmaceutical royalties | Gap |  |
| `private-capital-allocator` | `litigation-finance-claims` Litigation claims and legal-finance cash flows | Gap |  |
| `private-capital-allocator` | `fund-liquidity` Private-fund liquidity and evergreen vehicles | Related | `private-capital-allocator/private-market-programmes` |
| `real-asset-investor` | `property-valuation` Property valuation and listed real estate | Related | `real-asset-investor/real-estate` |
| `real-asset-investor` | `infrastructure-regulated-assets` Infrastructure and regulated assets | Related | `real-asset-investor/infrastructure` |
| `real-asset-investor` | `equipment-aircraft-leasing` Equipment and aircraft leasing | Gap | Accounting only, not a treatment: `meth:lease-reporting` (`financial-statement-analysis/leases-employee-compensation`) (lessor reporting) |
| `real-asset-investor` | `natural-resource-rights` Timber, farmland, mineral and water rights | Related | `real-asset-investor/land-timber-farmland` |
| `real-asset-investor` | `collectibles-valuation` Collectibles: auction evidence and investable returns | Gap |  |
| `insurance-climate-risk` | `catastrophe-cyber` Catastrophe and cyber insurance-linked risk | Gap | Mention only, not a treatment: `meth:insurer-analysis` (`financial-statement-analysis/financial-institution-analysis`) (catastrophe exposure in insurer analysis) |
| `insurance-climate-risk` | `longevity-risk` Mortality and longevity claims | Partial | Treated: mortality and longevity shocks in an insurer's solvency capital: `meth:life-insurer-analysis` (`financial-statement-analysis/financial-institution-analysis`); individuals' longevity risk and annuities: `meth:lifetime-exposures` (`private-wealth-management/wealth-planning`). Not written: longevity-linked securities and mortality claims as investments |
| `insurance-climate-risk` | `weather-derivatives` Weather exposure and temperature derivatives | Gap |  |
| `insurance-climate-risk` | `sidecar-capital` Sidecars, collateral release and alternative life capital | Gap |  |
| `private-wealth-management` | `household-finance-lifecycle` Household finance, human capital and lifecycle investment planning | Related | `private-wealth-management/clients-industry`, `private-wealth-management/wealth-planning` |
| `private-wealth-management` | `tax-aware-wealth-preservation` Taxes, asset location and concentrated positions | Related | `private-wealth-management/wealth-preservation` |
| `private-wealth-management` | `wealth-transfer-succession` Estate planning, intergenerational transfers and family-business succession | Related | `private-wealth-management/wealth-transfer` |
| `digital-assets-prediction-markets` | `stablecoin-tokenisation` Stablecoins and tokenised bonds | Related | `digital-assets-prediction-markets/stablecoins`, `digital-assets-prediction-markets/distributed-ledgers` |
| `digital-assets-prediction-markets` | `crypto-perpetuals` Crypto perpetuals and cross-venue basis | Note | 7 entries: `crypto-spot-markets/digital-asset-investing`, `crypto-trading-strategies/crypto-carry`, `digital-assets-prediction-markets/crypto-venues-perpetuals`, `digital-assets-prediction-markets/distributed-ledgers`, `onchain-protocols/amm-lending` |
| `digital-assets-prediction-markets` | `stablecoin-pegs-runs` Stablecoin pegs, runs and reserve assets | Note | 2 entries: `digital-assets-prediction-markets/stablecoins` |
| `digital-assets-prediction-markets` | `crypto-options-numeraire` Crypto options, inverse payoffs and margin | Related | `digital-assets-prediction-markets/crypto-venues-perpetuals` |
| `digital-assets-prediction-markets` | `crypto-leverage-liquidations` Crypto leverage, liquidations and centralised lenders | Note | 2 entries: `digital-assets-prediction-markets/crypto-venues-perpetuals`, `portfolio-risk-financing/crowding-contagion` |
| `digital-assets-prediction-markets` | `crypto-option-markets` Crypto option markets: implied volatility, smiles and risk premia | Gap | Mention only, not a treatment: `def:crypto-venue-instrument-structure` (`digital-assets-prediction-markets/crypto-venues-perpetuals`) (options as a venue instrument) |
| `crypto-spot-markets` | `crypto-price-discovery` Crypto price discovery: cross-exchange arbitrage, futures, spot ETFs and reference rates | Partial | Treated: fragmented executable prices and reference prices across venues: `def:crypto-venue-instrument-structure` (`digital-assets-prediction-markets/crypto-venues-perpetuals`); spot ETP approval and CME surveillance sharing: `meth:digital-asset-investment-analysis` (`crypto-spot-markets/digital-asset-investing`). Not written: cross-exchange arbitrage evidence; spot, futures and ETF lead–lag |
| `crypto-spot-markets` | `crypto-exchange-market-quality` Crypto exchange market quality: liquidity, fake volume and manipulation | Gap |  |
| `crypto-spot-markets` | `crypto-valuation-adoption` Bitcoin and token valuation: monetary models, adoption, mining and equilibrium prices | Gap | Mention only, not a treatment: `meth:digital-asset-investment-analysis` (`crypto-spot-markets/digital-asset-investing`), `def:distributed-ledger-applications` (`digital-assets-prediction-markets/distributed-ledgers`) (no cash flows; adoption and scarcity arguments; fixed supply) |
| `crypto-spot-markets` | `crypto-investors-etfs` Crypto investors and access: retail trading, spot ETFs and bank custody | Related | `crypto-spot-markets/digital-asset-investing` |
| `crypto-spot-markets` | `crypto-exchange-failures-regulation` Crypto exchange failures, customer assets and market regulation | Partial | Treated: custody and venue-insolvency risk: `meth:digital-asset-investment-analysis` (`crypto-spot-markets/digital-asset-investing`), `def:crypto-trading-risk-layers` (`digital-assets-prediction-markets/crypto-venues-perpetuals`). Not written: exchange-failure cases and customer-asset outcomes; market regulation |
| `crypto-spot-markets` | `crypto-return-dynamics` Crypto return dynamics: volatility, bubbles, efficiency and links to other assets | Partial | Treated: return moments, factor exposures and diversification evidence: `meth:digital-asset-investment-analysis` (`crypto-spot-markets/digital-asset-investing`). Not written: volatility dynamics; bubbles; efficiency tests |
| `onchain-protocols` | `amm-lending` Automated market makers: pricing, routing and liquidity-provider returns | Related | `onchain-protocols/amm-lending` |
| `onchain-protocols` | `mev-block-building` Transaction ordering, MEV and block building | Gap |  |
| `onchain-protocols` | `staking-restaking` Staking, liquid staking and restaking | Partial | Treated: proof-of-stake validation, stake deposits and slashing: `def:distributed-ledger-applications` (`digital-assets-prediction-markets/distributed-ledgers`). Not written: staking yields; liquid staking and restaking |
| `onchain-protocols` | `defi-lending-liquidations` DeFi lending, liquidations and price oracles | Note | 1 entries: `onchain-protocols/amm-lending` |
| `onchain-protocols` | `onchain-solvers-execution` On-chain solver auctions and cross-domain execution | Gap |  |
| `onchain-protocols` | `protocol-risk-governance` Protocol risk and governance: exploits, bridges, layer two and DAOs | Gap |  |
| `onchain-protocols` | `crypto-signals` Crypto signals and on-chain evidence | Gap |  |
| `tokenised-fractional-assets` | `fractional-shares-contracts` Fractional shares, odd lots and smaller contracts: retail access and market data | Partial | Treated: round-lot and odd-lot market-data definitions: `rule:us-equity-market-structure` (`execution-trading-costs/market-regulation`). Not written: fractional-share mechanics and retail access; smaller contracts |
| `tokenised-fractional-assets` | `tokenised-securities` Tokenised securities and funds: legal form, trading venues and settlement | Gap | Mention only, not a treatment: `def:distributed-ledger-applications` (`digital-assets-prediction-markets/distributed-ledgers`) (tokenisation of assets) |
| `tokenised-fractional-assets` | `tokenised-real-assets` Token offerings and tokenised real assets: ICOs, security tokens, real estate, art and NFTs | Gap | Mention only, not a treatment: `def:distributed-ledger-applications` (`digital-assets-prediction-markets/distributed-ledgers`) (token offerings) |
| `crypto-market-making` | `crypto-dealer-rfq` Crypto order-book dealing and RFQ | Gap |  |
| `crypto-market-making` | `crypto-mm-microstructure` Crypto order-book microstructure for market makers: fees, impact, latency and order flow | Gap |  |
| `crypto-market-making` | `token-market-makers` Token market makers: issuer agreements, listings and manipulation | Gap |  |
| `crypto-market-making` | `dex-liquidity-provision` DEX liquidity provision strategies: fee tiers, repositioning and just-in-time liquidity | Partial | Treated: concentrated-liquidity positions and the cost of providing liquidity: `def:amm-pool-mechanics` (`onchain-protocols/amm-lending`). Not written: fee-tier choice; repositioning; just-in-time liquidity |
| `crypto-market-making` | `crypto-mm-strategies` Crypto market-making strategies: inventory control, learning agents and backtests | Gap | General method only, not a treatment: `mod:avellaneda-stoikov` (`execution-market-making/market-making-models`) (inventory-aware quoting) |
| `crypto-trading-strategies` | `crypto-cross-section` Cross-sectional crypto strategies: size, momentum, reversal, value and factor momentum | Gap | Mention only, not a treatment: `meth:digital-asset-investment-analysis` (`crypto-spot-markets/digital-asset-investing`) (crypto momentum predictability, one sentence) |
| `crypto-trading-strategies` | `crypto-trend-technical` Crypto trend following, intraday momentum, technical rules and calendar effects | Gap |  |
| `crypto-trading-strategies` | `crypto-stat-arb` Crypto statistical arbitrage and pairs trading | Gap |  |
| `crypto-trading-strategies` | `crypto-ml-prediction` Machine-learning crypto return prediction and backtest pitfalls | Gap |  |
| `crypto-trading-strategies` | `crypto-arbitrage-carry` Crypto arbitrage and carry: cross-exchange, triangular, funding basis and DeFi yields | Related | `crypto-trading-strategies/crypto-carry` |
| `crypto-trading-strategies` | `crypto-sentiment-events` Attention, sentiment and event-driven crypto strategies | Gap | Mention only, not a treatment: `meth:digital-asset-investment-analysis` (`crypto-spot-markets/digital-asset-investing`) (attention predictability, one sentence) |
| `event-contracts-prediction-markets` | `prediction-forecast-evidence` Event prices as forecasts: accuracy, calibration and bias | Gap |  |
| `event-contracts-prediction-markets` | `prediction-price-theory` Price theory: beliefs, wealth and belief dynamics | Gap |  |
| `event-contracts-prediction-markets` | `prediction-wagering` Wagering markets: bookmakers, exchanges and the favourite–longshot bias | Gap |  |
| `event-contracts-prediction-markets` | `prediction-decision-markets` Decision, corporate and scientific markets | Gap |  |
| `event-contract-venues` | `prediction-settlement` Contract resolution, disputes and settlement data | Gap |  |
| `event-contract-venues` | `prediction-outcome-tokens` Outcome tokens, fractional contracts and cross-venue identity | Gap |  |
| `event-contract-venues` | `prediction-integrity` Insider trading, manipulation and wash trading | Gap |  |
| `event-contract-venues` | `prediction-regulation` Regulation and litigation: the CFTC, states and sports contracts | Gap |  |
| `event-contract-trading` | `prediction-market-design` Automated market makers and scoring rules | Gap | General method only, not a treatment: `def:amm-pool-mechanics` (`onchain-protocols/amm-lending`) (constant-product AMMs) |
| `event-contract-trading` | `prediction-order-book-mm` Order-book market making: spreads, adverse selection and who earns | Gap | General method only, not a treatment: `mod:glosten-milgrom` (`execution-market-making/market-making-models`), `res:glosten-milgrom-half-spreads` (`execution-market-making/market-making-models`) (adverse-selection spreads) |
| `event-contract-trading` | `prediction-event-derivatives` Event derivatives: binary options, parimutuel auctions, combos and belief volatility | Partial | Treated: binary (digital) option valuation and pin risk: `meth:digital-option-valuation` (`volatility-options/exotic-options`). Not written: parimutuel auctions; combinations; belief volatility |
| `event-contract-trading` | `prediction-trading-strategies` Trading strategies: longshots, arbitrage and stake sizing | Partial | Treated: Kelly stake sizing for discrete bets: `res:kelly-growth-optimal-fraction` (`portfolio-construction-risk/portfolio-construction-models`). Not written: longshot strategies; cross-venue arbitrage |

Totals: Note 55, Related 54, Partial 42, Gap 71 (222 pathways).
