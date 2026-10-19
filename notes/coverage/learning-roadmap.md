# Learning roadmap

Topics in prerequisite order, grouped by the depth most of their objectives require. Each topic builds on the topics in its *Builds on* column; a topic can sit in a later group than some of its own objectives. Objectives, their status and their entries are in [objectives.json](objectives.json); run `make check-coverage` for current coverage. Chapter keys are sections declared in `compendium/compendium.tex`.

The order is a navigation aid for subjects, not an examination sequence. Several topics in different subjects can be studied in parallel once their prerequisites are met.

## Worked journeys

Two routes have been followed end to end, from roadmap to compiled entry to source locator.

**Reusing an existing entry.** `topic:return-measurement` (Foundations) → `objective:compare-time-and-money-weighted-returns` → `def:return-measures` in the *Portfolio construction and risk* chapter, section *Performance evaluation* → its Statement cites the GIPS 2020 glossary (`wide-gips-2020`, pp. 78 and 83) and provision 1.A.35 for when money-weighted returns may be presented; the worked example in Practice gives the time- and money-weighted returns of one cash-flow history. The outline item `outline:7099c7688942:m003:b01` maps to this objective; its review is in `outline-crosswalk.json`.

**A new chapter.** `topic:cash-flow-analysis` (Foundations) → `objective:link-cash-flow-statement` → `meth:statement-linked-cash-flows` in the new *Financial statement analysis* chapter, section *Cash-flow analysis* → IAS 7 paragraphs 6, 10 and 18-20 (`eu-2023-1803-ias7`) and the IFRS 18 amendments (`eu-2026-338-ifrs18`, amended paras. 18(b), 20, 33A and 34A); the worked example is checked by `notes/artefacts/financial-statement-analysis/cash-flow-linkage-check.py`. Two outline items map to the objective (`outline:7099c7688942:m030:b01` and `:b02`); the same entry covers the line-by-line conversion and the IFRS-against-US-GAAP comparison (`objective:convert-indirect-to-direct-cash-flow`, `objective:compare-cash-flow-reporting-frameworks`).

## 1. Foundations

| Topic | Chapter | Builds on | Objectives |
| --- | --- | --- | ---: |
| `topic:time-value-of-money` Time value of money and cash-flow additivity | `common-toolkit` | — | 3 |
| `topic:return-measurement` Return measurement | `portfolio-construction-risk` | `topic:time-value-of-money` | 5 |
| `topic:market-index-construction` Market index construction | `international-equity-markets` | `topic:return-measurement` | 2 |
| `topic:descriptive-statistics` Descriptive statistics of returns | `common-toolkit` | `topic:return-measurement` | 4 |
| `topic:probability-distributions` Probability and distributions in finance | `common-toolkit` | `topic:descriptive-statistics` | 3 |
| `topic:statistical-inference` Sampling and statistical inference | `common-toolkit` | `topic:probability-distributions` | 3 |
| `topic:simulation-methods` Simulation and resampling | `common-toolkit` | `topic:probability-distributions` | 3 |
| `topic:firms-market-structure` Firms and market structure | `multi-asset-systematic-macro` | — | 3 |
| `topic:business-cycles` Business and credit cycles | `multi-asset-systematic-macro` | — | 2 |
| `topic:fiscal-policy` Fiscal policy | `multi-asset-systematic-macro` | `topic:business-cycles` | 1 |
| `topic:monetary-policy` Monetary policy | `rates-credit-mortgages` | `topic:business-cycles` | 2 |
| `topic:geopolitics-trade` Geopolitics and international trade | `multi-asset-systematic-macro` | — | 3 |
| `topic:financial-reporting-framework` Financial reporting framework and information sources | `financial-statement-analysis` | — | 3 |
| `topic:income-statement-analysis` Income statement analysis | `financial-statement-analysis` | `topic:financial-reporting-framework` | 5 |
| `topic:balance-sheet-analysis` Balance sheet analysis | `financial-statement-analysis` | `topic:financial-reporting-framework` | 3 |
| `topic:cash-flow-analysis` Cash-flow statement analysis | `financial-statement-analysis` | `topic:income-statement-analysis`, `topic:balance-sheet-analysis` | 5 |
| `topic:inventory-accounting` Inventory accounting and analysis | `financial-statement-analysis` | `topic:income-statement-analysis` | 3 |
| `topic:leases-employee-compensation` Leases, pensions and share-based compensation | `financial-statement-analysis` | `topic:balance-sheet-analysis` | 6 |
| `topic:income-tax-accounting` Income tax accounting | `financial-statement-analysis` | `topic:income-statement-analysis` | 3 |
| `topic:portfolio-risk-return` Portfolio risk and return | `portfolio-construction-risk` | `topic:descriptive-statistics` | 6 |
| `topic:asset-pricing-factor-models` CAPM and factor models | `portfolio-construction-risk` | `topic:portfolio-risk-return` | 8 |
| `topic:business-models` Business models | `corporate-finance` | — | 1 |
| `topic:equity-securities-markets` Equity securities and markets | `systematic-equities` | — | 4 |
| `topic:bond-instrument-features` Bond features, issuance and markets | `rates-credit-mortgages` | — | 5 |
| `topic:short-term-funding` Short-term funding and repurchase agreements | `portfolio-risk-financing` | `topic:bond-instrument-features` | 1 |
| `topic:bond-pricing-yields` Bond pricing and yield measures | `rates-credit-mortgages` | `topic:time-value-of-money` | 4 |
| `topic:interest-rate-risk` Interest-rate risk measures | `rates-credit-mortgages` | `topic:bond-pricing-yields` | 4 |
| `topic:securitisation` Securitisation and asset-backed securities | `securitised-structured-credit` | `topic:credit-risk-analysis` | 3 |
| `topic:derivative-instruments` Derivative instruments and markets | `volatility-options` | — | 4 |
| `topic:forward-commitment-valuation` Forward, futures and swap valuation | `volatility-options` | `topic:derivative-instruments`, `topic:term-structure` | 7 |
| `topic:investment-management-process` Investors and the investment management process | `portfolio-construction-risk` | — | 3 |
| `topic:investment-policy-planning` Investment policy and planning | `portfolio-construction-risk` | `topic:investment-management-process` | 4 |
| `topic:behavioral-finance` Behavioural finance | `portfolio-construction-risk` | — | 2 |
| `topic:risk-management-framework` Risk management framework and governance | `portfolio-construction-risk` | — | 2 |
| `topic:ethics-professionalism` Ethics, trust and professionalism | `professional-ethics` | — | 2 |
| `topic:professional-conduct-code` Code of ethics and professional conduct programme | `professional-ethics` | `topic:ethics-professionalism` | 2 |

## 2. Analysis and valuation

| Topic | Chapter | Builds on | Objectives |
| --- | --- | --- | ---: |
| `topic:linear-regression` Linear regression | `common-toolkit` | `topic:statistical-inference` | 7 |
| `topic:time-series-models` Time-series models | `common-toolkit` | `topic:linear-regression` | 7 |
| `topic:machine-learning-methods` Machine learning methods | `ml-alternative-data` | `topic:linear-regression` | 3 |
| `topic:data-science-workflow` Financial data-science workflow | `ml-alternative-data` | `topic:machine-learning-methods` | 4 |
| `topic:exchange-rate-mechanics` Exchange-rate quotation and arithmetic | `currency-markets` | `topic:time-value-of-money` | 4 |
| `topic:exchange-rate-determination` Exchange-rate determination and policy | `currency-markets` | `topic:exchange-rate-mechanics`, `topic:monetary-policy` | 5 |
| `topic:economic-growth` Economic growth | `multi-asset-systematic-macro` | `topic:business-cycles` | 4 |
| `topic:macro-asset-valuation` Economic drivers of asset values | `multi-asset-systematic-macro` | `topic:business-cycles`, `topic:monetary-policy` | 3 |
| `topic:long-lived-asset-accounting` Long-lived assets | `financial-statement-analysis` | `topic:balance-sheet-analysis` | 2 |
| `topic:financial-reporting-quality` Financial reporting quality | `financial-statement-analysis` | `topic:cash-flow-analysis` | 7 |
| `topic:ratio-analysis` Ratio analysis and forecasting | `financial-statement-analysis` | `topic:income-statement-analysis`, `topic:balance-sheet-analysis`, `topic:cash-flow-analysis` | 4 |
| `topic:financial-statement-modelling` Financial statement modelling | `financial-statement-analysis` | `topic:ratio-analysis` | 4 |
| `topic:intercorporate-investments` Intercorporate investments and consolidation | `financial-statement-analysis` | `topic:balance-sheet-analysis` | 2 |
| `topic:foreign-currency-reporting` Foreign-currency reporting | `financial-statement-analysis` | `topic:exchange-rate-mechanics`, `topic:balance-sheet-analysis` | 3 |
| `topic:financial-institution-analysis` Analysis of banks and insurers | `financial-statement-analysis` | `topic:ratio-analysis` | 3 |
| `topic:integrated-statement-analysis` Integrated financial statement analysis | `financial-statement-analysis` | `topic:financial-reporting-quality`, `topic:ratio-analysis` | 3 |
| `topic:corporate-ownership-governance` Corporate ownership, stakeholders and governance | `corporate-finance` | — | 5 |
| `topic:working-capital-liquidity` Working capital and liquidity | `corporate-finance` | `topic:ratio-analysis` | 2 |
| `topic:capital-investment-decisions` Capital investment decisions | `corporate-finance` | `topic:time-value-of-money` | 2 |
| `topic:capital-structure-cost-of-capital` Capital structure and cost of capital | `corporate-finance` | `topic:capital-investment-decisions`, `topic:asset-pricing-factor-models` | 4 |
| `topic:payout-policy` Dividends and share repurchases | `corporate-finance` | `topic:capital-structure-cost-of-capital` | 4 |
| `topic:equity-valuation-foundations` Equity valuation foundations | `systematic-equities` | `topic:time-value-of-money` | 6 |
| `topic:market-multiples-valuation` Price and enterprise-value multiples | `systematic-equities` | `topic:equity-valuation-foundations` | 7 |
| `topic:corporate-restructuring` Corporate restructuring | `corporate-finance` | `topic:capital-structure-cost-of-capital`, `topic:market-multiples-valuation` | 2 |
| `topic:industry-company-analysis` Industry and company analysis | `systematic-equities` | `topic:ratio-analysis` | 2 |
| `topic:equity-research-reporting` Equity research reports and forecasts | `systematic-equities` | `topic:financial-statement-modelling` | 2 |
| `topic:dividend-discount-models` Dividend discount models | `systematic-equities` | `topic:equity-valuation-foundations` | 6 |
| `topic:free-cash-flow-valuation` Free cash flow valuation | `systematic-equities` | `topic:cash-flow-analysis`, `topic:dividend-discount-models` | 4 |
| `topic:residual-income-valuation` Residual income valuation | `systematic-equities` | `topic:dividend-discount-models` | 3 |
| `topic:private-company-valuation` Private company valuation | `systematic-equities` | `topic:free-cash-flow-valuation`, `topic:market-multiples-valuation` | 3 |
| `topic:term-structure` Term structure of interest rates | `rates-credit-mortgages` | `topic:bond-pricing-yields` | 6 |
| `topic:credit-risk-analysis` Credit risk and credit analysis | `corporate-credit-capital` | `topic:ratio-analysis`, `topic:bond-pricing-yields` | 2 |
| `topic:sovereign-credit-analysis` Sovereign and public-sector credit | `government-bond-markets` | `topic:credit-risk-analysis` | 1 |
| `topic:arbitrage-free-bond-valuation` Arbitrage-free bond valuation | `rates-credit-mortgages` | `topic:term-structure` | 3 |
| `topic:embedded-option-bonds` Bonds with embedded options | `rates-credit-mortgages` | `topic:arbitrage-free-bond-valuation`, `topic:interest-rate-risk` | 5 |
| `topic:credit-models` Credit valuation models | `corporate-credit-capital` | `topic:credit-risk-analysis`, `topic:arbitrage-free-bond-valuation` | 4 |
| `topic:credit-default-swaps` Credit default swaps | `corporate-credit-capital` | `topic:credit-models` | 3 |
| `topic:option-valuation` Option valuation | `volatility-options` | `topic:forward-commitment-valuation`, `topic:probability-distributions` | 6 |
| `topic:commodity-investment` Commodity investment | `commodity-investing-premia` | `topic:forward-commitment-valuation` | 4 |
| `topic:hedge-fund-strategies` Hedge funds and their strategies | `portfolio-construction-risk` | `topic:alternative-investment-structures` | 3 |
| `topic:digital-asset-investment` Digital asset investment | `digital-assets-prediction-markets` | — | 2 |
| `topic:active-management-analysis` Active management and the fundamental law | `portfolio-construction-risk` | `topic:asset-pricing-factor-models` | 3 |
| `topic:exchange-traded-funds` Exchange-traded funds | `execution-trading-costs` | `topic:equity-securities-markets` | 2 |
| `topic:market-risk-measurement` Market risk measurement and limits | `portfolio-construction-risk` | `topic:probability-distributions`, `topic:interest-rate-risk` | 3 |
| `topic:backtesting-simulation` Backtesting and scenario simulation | `research-engineering-validation` | `topic:simulation-methods` | 2 |
| `topic:performance-evaluation` Performance attribution, benchmarks and appraisal | `portfolio-construction-risk` | `topic:return-measurement`, `topic:asset-pricing-factor-models` | 7 |
| `topic:performance-presentation-standards` Performance presentation standards | `portfolio-construction-risk` | `topic:return-measurement` | 4 |

## 3. Portfolio and client decisions

| Topic | Chapter | Builds on | Objectives |
| --- | --- | --- | ---: |
| `topic:option-strategies` Option strategies | `volatility-options` | `topic:option-valuation` | 4 |
| `topic:derivative-overlay-strategies` Derivative overlays for portfolio exposures | `portfolio-construction-risk` | `topic:forward-commitment-valuation`, `topic:interest-rate-risk` | 4 |
| `topic:currency-management` Currency management | `currency-markets` | `topic:exchange-rate-determination`, `topic:derivative-overlay-strategies` | 4 |
| `topic:capital-market-expectations` Capital market expectations | `multi-asset-systematic-macro` | `topic:macro-asset-valuation`, `topic:economic-growth` | 6 |
| `topic:strategic-asset-allocation` Asset allocation | `multi-asset-systematic-macro` | `topic:capital-market-expectations`, `topic:investment-policy-planning` | 11 |
| `topic:equity-portfolio-management` Equity portfolio management | `systematic-equities` | `topic:asset-pricing-factor-models`, `topic:active-management-analysis` | 7 |
| `topic:fixed-income-portfolio-management` Fixed-income portfolio management | `rates-credit-mortgages` | `topic:interest-rate-risk`, `topic:term-structure` | 7 |
| `topic:credit-portfolio-strategies` Active credit strategies | `corporate-credit-capital` | `topic:credit-models`, `topic:fixed-income-portfolio-management` | 4 |
| `topic:alternatives-allocation` Allocating to alternative investments | `portfolio-construction-risk` | `topic:strategic-asset-allocation`, `topic:alternative-investment-structures` | 2 |
| `topic:institutional-portfolios` Institutional investor portfolios | `portfolio-construction-risk` | `topic:strategic-asset-allocation` | 6 |
| `topic:trade-execution` Trading costs and trade execution | `execution-trading-costs` | — | 5 |
| `topic:manager-selection` Investment manager selection | `portfolio-construction-risk` | `topic:performance-evaluation` | 3 |
| `topic:professional-conduct-standards` Application of professional conduct standards | `professional-ethics` | `topic:professional-conduct-code` | 16 |
| `topic:asset-manager-conduct` Asset manager code of conduct | `professional-ethics` | `topic:professional-conduct-code` | 2 |

## 4. Private markets and private wealth

| Topic | Chapter | Builds on | Objectives |
| --- | --- | --- | ---: |
| `topic:alternative-investment-structures` Alternative investment structures, fees and returns | `private-capital-allocator` | `topic:return-measurement` | 3 |
| `topic:private-capital` Private equity, private debt and special situations | `private-capital-allocator` | `topic:alternative-investment-structures` | 9 |
| `topic:private-market-programmes` Private-market structures, performance and investment process | `private-capital-allocator` | `topic:alternative-investment-structures` | 5 |
| `topic:real-estate-investment` Real estate investment | `real-asset-investor` | `topic:alternative-investment-structures` | 6 |
| `topic:infrastructure-investment` Infrastructure investment | `real-asset-investor` | `topic:alternative-investment-structures` | 3 |
| `topic:natural-resource-investment` Land, timberland and farmland | `real-asset-investor` | `topic:alternative-investment-structures` | 1 |
| `topic:private-wealth-clients` Private clients and the wealth management industry | `private-wealth-management` | `topic:investment-policy-planning` | 5 |
| `topic:wealth-planning` Goals-based wealth and investment planning | `private-wealth-management` | `topic:private-wealth-clients`, `topic:strategic-asset-allocation` | 5 |
| `topic:wealth-preservation` Human-capital and purchasing-power protection | `private-wealth-management` | `topic:wealth-planning` | 2 |
| `topic:wealth-transfer-advice` Advising complex families and transferring wealth | `private-wealth-management` | `topic:wealth-planning` | 3 |

### Accounting expansion,19 October2026

The45-objective accounting slice follows framework → income/balance/cash-flow analysis → inventory/long-lived assets → leases/compensation/taxes → quality → ratios → integrated forecast and credit decision. Existing three cash-flow objectives remain prerequisites, not newly counted. See the [semantic review](../source-review-records.md#accounting-and-statement-analysis-45-objectives-19-october-2026) for all operations and depth. These are editorial completions, not learner mastery; the remaining financial-statement topics are not silently promoted.
