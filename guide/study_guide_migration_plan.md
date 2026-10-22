# Study-guide migration plan

Status: implemented and validated on 22 October 2026, then corrected the same day after two audits (sections 12 and 13); changes are uncommitted on branch `study-guide-eight-part-migration` for review. This file is the single migration record for reorganising the
learning guide into the companion compendium's eight-Part, 49-section structure and
for filling the guide's genuine content gaps. It is updated as work proceeds; section 9
records what was actually done and how it was checked.

Prepared 22 October 2026. Target structure: the compendium's
`content_migration_plan.md` (sections 3.4, 3.5 and 4), read in the sibling
`Algorithmic-Trading-Notes` repository and not modified by this work.

## 1. Audited revision and baseline

| Measure | Baseline |
| --- | --- |
| Repository revision | `343d145909ba5384202b50604bf5ebe7e5b6ed86` (branch `main`, clean tree) |
| `learning_routes.json` SHA-256 | `a2aeb67ca658ddf617e803d5bdd8c5030faa2e6d606762765d827503793d1268` (equal to the compendium plan's pinned copy) |
| Guide | 7 Parts, 38 overview sections, 203 specialist pathways, 2,563 selected readings |
| Overviews with capstone checkpoints | 12 |
| Catalogue | 3,893 entries, 23 chapters, 4 catalogue parts; 760 extended notes |
| Generator | `python3 refresh_views.py` reproduces the committed guide source, HTML and JSON byte for byte |

There is no `AGENTS.md` in this repository; [README.md](README.md),
[structural_mapping.md](structural_mapping.md),
[bibliographic_audit.md](bibliographic_audit.md),
[editorial_backlog.md](editorial_backlog.md) and [removal_plan.md](removal_plan.md)
are the maintenance documentation. Their rules apply: catalogue identifiers never
change, each catalogue command stays on one line, version records state what was
inspected, and generated files are never edited by hand.

## 2. Target structure

Eight Parts and 49 overview sections, with section counts 7, 5, 13, 4, 7, 4, 6 and 3.
Keys are exactly the compendium plan's. "New" marks an overview that does not exist
in the baseline guide.

| Part | Key | Sections (key — displayed title) |
| --- | --- | --- |
| I. Financial mathematics, statistics and numerical methods | `mathematics-statistics-numerics` | `financial-mathematics` — Financial mathematics and return measurement (new); `probability-statistics` — Probability and statistical inference (new); `regression-time-series` — Regression and time-series econometrics (new); `stochastic-processes-calculus` — Stochastic processes and calculus (new); `bayesian-inference` — Bayesian inference and parameter uncertainty (new); `high-dimensional-statistics` — High-dimensional statistics and covariance estimation (new); `numerical-optimisation` — Numerical methods and optimisation (new) |
| II. Empirical finance, machine learning and research governance | `empirical-finance-research-governance` | `asset-pricing` — Asset pricing theory and empirical tests (new); `causal-inference` — Causal inference and experimental design (new); `research-engineering-validation` — Research engineering, data provenance and model validation; `professional-ethics` — Professional ethics (new); `ml-alternative-data` — Machine learning and alternative data |
| III. Public markets and pricing | `public-markets` | `rates-credit-mortgages`; `government-bond-markets`; `financial-statement-analysis` — Financial statement analysis (new); `corporate-finance` — Corporate finance (new); `corporate-credit-capital`; `securitised-structured-credit`; `systematic-equities`; `volatility-options`; `volatility-trading-premia`; `multi-asset-systematic-macro`; `currency-markets`; `international-equity-markets`; `global-regional-markets` |
| IV. Portfolio financing and execution | `portfolio-financing-execution` | `portfolio-construction-risk`; `portfolio-risk-financing`; `execution-market-making`; `execution-trading-costs` |
| V. Energy and commodities | `energy-commodities` | `energy-commodities`; `commodity-spot-markets`; `physical-commodity-markets`; `commodity-investing-premia`; `oil-shocks-macro`; `power-gas-environmental`; `environmental-markets` |
| VI. Private capital, real assets and insurance | `private-real-insurance` | `private-capital-allocator` — Private equity, private credit and fund structures; `real-asset-investor` — Real estate, infrastructure and natural-resource investments; `insurance-climate-risk`; `private-wealth-management` — Private wealth management (new) |
| VII. Digital assets | `digital-assets` | `digital-assets-prediction-markets`; `crypto-spot-markets`; `onchain-protocols`; `tokenised-fractional-assets`; `crypto-market-making`; `crypto-trading-strategies` |
| VIII. Event contracts and prediction markets | `event-contracts` | `event-contracts-prediction-markets`; `event-contract-venues`; `event-contract-trading` |

Unlisted titles keep their baseline guide names, which already name a discipline or
financial object. The four renamed overviews replace a role label ("allocator",
"investor"), an abbreviation ("ML") or an incomplete subject name.

## 3. Old-to-new mapping

### 3.1 Parts

| Baseline guide Part | Target Part(s) |
| --- | --- |
| `foundations` — Research foundations (4 sections) | `mathematics-statistics-numerics` (Part I) and `empirical-finance-research-governance` (Part II) |
| `public-markets` | Part III, adding `financial-statement-analysis` and `corporate-finance` after `government-bond-markets` |
| `portfolio-financing-execution` | Part IV, unchanged membership |
| `energy-commodities` | Part V, unchanged |
| `private-real-insurance` | Part VI, followed by `private-wealth-management` |
| `digital-assets` | Part VII, unchanged |
| `event-contracts` | Part VIII, unchanged |

The baseline Part key `foundations` is retired; no remaining Part uses it. The
other six Part keys are kept, so `part-<key>` labels for them still resolve.

### 3.2 Overview sections

| Baseline overview | Disposition | Target |
| --- | --- | --- |
| `common-toolkit` (Common toolkit, `route-1`) | Split; identity retired to a navigation bridge | The seven Part I sections. Its readings are redistributed: `prob-wasserman` to `probability-statistics`; `s15-campbell` to `regression-time-series`; `s6-cochrane` to `asset-pricing-theory`; `alpha-boyd` to `numerical-optimisation`; `s7-meucci` remains in `portfolio-construction-risk`; `s6-pbo` moves to the `research-engineering-validation` overview with the research-record checkpoint; `s8-bitemporal` remains in `research-engineering-validation` |
| `empirical-causal-research` (Empirical asset pricing and causal inference, `route-16`) | Split; identity retired to a navigation bridge | `asset-pricing` (anomaly reproduction, pricing restrictions) and `causal-inference` (policy effects, identification). Its checkpoint's two halves become the two overview checkpoints |
| `research-engineering-validation` | Move to Part II; rename; revise overview to open with strategy specification | Same key |
| `ml-alternative-data` | Move to Part II; rename | Same key |
| `private-capital-allocator`, `real-asset-investor` | Rename | Same keys |
| `multi-asset-systematic-macro` | Revise: add a macroeconomics reading for economic foundations | Same key |
| `corporate-credit-capital` | Revise prerequisites: statement analysis before credit | Same key |
| 32 other overviews | Retain; prerequisites remapped where they named a retired overview; prose section numbers become route references | Same keys |
| (none) | New | `financial-mathematics`, `probability-statistics`, `regression-time-series`, `stochastic-processes-calculus`, `bayesian-inference`, `high-dimensional-statistics`, `numerical-optimisation`, `asset-pricing`, `causal-inference`, `professional-ethics`, `financial-statement-analysis`, `corporate-finance`, `private-wealth-management` |

### 3.3 Specialist pathways moved between sections

| Pathway | Baseline section | Target section |
| --- | --- | --- |
| `probability-statistical-inference` | `common-toolkit` | `probability-statistics` |
| `time-series-volatility` | `common-toolkit` | `regression-time-series` |
| `stochastic-calculus-control` | `common-toolkit` | `stochastic-processes-calculus` |
| `bayesian-parameter-uncertainty` | `common-toolkit` | `bayesian-inference` |
| `high-dimensional-estimation` | `common-toolkit` | `high-dimensional-statistics` |
| `numerical-methods-optimisation` | `common-toolkit` | `numerical-optimisation` |
| `standard-errors-inference`, `empirical-asset-pricing`, `return-predictability`, `event-studies` | `empirical-causal-research` | `asset-pricing` |
| `causal-research-designs`, `causal-policy-evaluation`, `controlled-experiments` | `empirical-causal-research` | `causal-inference` |

All other pathways keep their section. The full per-pathway ledger is in section 11.

## 4. Findings

| # | Finding | Evidence | Remedy |
| --- | --- | --- | --- |
| F1 | The guide has no financial-mathematics or return-measurement route. Discounting, compounding, IRR and time- versus money-weighted returns are assumed by 15 overviews' prose prerequisites ("discount factors", "discounted cash flows", "fund cash flows", "portfolio-return accounting") but taught nowhere; the catalogue has no introductory time-value text | `rates-credit-mortgages`, `private-capital-allocator`, `real-asset-investor` and `financial-ml-evaluation` prerequisites in `learning_routes.json`; catalogue chapter 1 has no such section. Supporting entries exist: `wide-bacon-attribution`, `wide-gips-2020`, `catalogue-0233`, `s15-campbell`, `wide-dimson-marsh-staunton` | New section with two pathways; add an introductory text and money-weighted-return evidence to the catalogue |
| F2 | `common-toolkit` combines six disciplines under a generic container; its own outcome (a research record) is a research-governance task, not a mathematical one | `routes[0]` outcome, readings (`s6-pbo`, `s8-bitemporal`) and six section goals | Split into seven Part I sections; move the research-record outcome to `research-engineering-validation` |
| F3 | `probability-statistical-inference` mixes probability and mathematical statistics with graduate econometrics (`wide-hayashi-econometrics`, `wide-hansen-econometrics`); no route teaches linear and multiple regression, diagnostics or GMM as a skill, although `standard-errors-inference` assumes "OLS, IV and panel regression" | Readings and prerequisites of those two pathways | New `regression-econometrics` pathway receives the two texts; probability pathway narrowed |
| F4 | No route's checkpoint tests stationarity, unit roots, VARs or cointegration, though at least eight pathways assume cointegration (`gas-hub-pricing`, `commodity-spatial-arbitrage`, `crypto-price-discovery`, `crypto-stat-arb` and others); `time-series-volatility` mentions them only in one reading's rationale | `time-series-volatility` checkpoint and `s7-hamilton` reason; dependants' prose prerequisites | New `stationarity-cointegration` pathway, made a prerequisite of `time-series-volatility` so dependants inherit it |
| F5 | General tail and dependence estimation (`wide-cont-stylized-facts`, `wide-embrechts-extremal`, `wide-joe-copulas`) sits inside the high-dimensional covariance pathway, contrary to the target's boundary (heavy tails in probability, covariance in high-dimensional statistics) | `high-dimensional-estimation` readings and checkpoint | Split into `heavy-tails-extremes` (Probability) and a narrowed covariance pathway |
| F6 | Asset-pricing theory has no route: Cochrane's *Asset Pricing* is only an orientation reading of `common-toolkit`; no checkpoint derives the CAPM or a stochastic-discount-factor restriction; Sharpe (1964), Ross (1976) and Mehra–Prescott (1985) are not catalogued | `routes[0]` readings; catalogue section 2.1 holds theory texts but not the classic papers | New `asset-pricing-theory` pathway; add the classic papers |
| F7 | `empirical-causal-research` combines pricing tests with causal identification, and its checkpoint pairs an anomaly with a policy effect | `routes[1]` outcome, goals and checkpoint | Split into `asset-pricing` and `causal-inference`; keep prediction, pricing tests and identification distinct in outcomes and checkpoints |
| F8 | Causal inference is a guide gap only at overview level: the catalogue's chapter 4 is extensive and three pathways are complete, but no overview states estimands and identification, and `causal-research-designs` does not list the clustered-inference pathway it relies on | Catalogue chapter 4; `causal-research-designs` readings include `rf-bertrand-duflo-mullainathan-2004` only via `standard-errors-inference` | New overview from existing entries (no new catalogue entries); add the prerequisite edge |
| F9 | Professional ethics is missing from the guide and almost entirely from the catalogue (only `wide-gips-2020`) | Catalogue search for ethics, fiduciary, conflicts of interest and codes of conduct | New section, two pathways; add CFA Institute standards and procedures, SEC and EU conduct rules, and conduct evidence |
| F10 | Financial statement analysis is missing as a subject. `equity-events-fundamentals` uses statements for valuation signals but assumes statement literacy; no route teaches reporting frameworks, measurement, group or foreign-currency reporting, ratio analysis or forecasting; the catalogue holds valuation texts (`w5-penman-fsa`, `wide-koller-valuation`, `gap-damodaran4`) and signal papers but no reporting standard or reporting text | `equity-events-fundamentals` readings; catalogue section 10.2 | New section, five pathways; add the IFRS text as endorsed in the EU, the IASB's Conceptual Framework and IFRS 18, a statement-analysis text and reporting-quality research |
| F11 | Corporate finance is missing as a subject. Fragments appear in `private-equity-vc` (LBO models), `credit-models-default` (Leland), `equity-event-driven` (mergers) and `gap-credit-distress-book` (restructuring); capital budgeting, capital structure, cost of capital, payout and governance have no route, and Modigliani–Miller, Jensen–Meckling and Myers are not catalogued | Those routes' readings; catalogue search | New section, three pathways; add a text and the founding papers |
| F12 | Private wealth management is missing from the guide and catalogue apart from `wide-merton-1969` and `wide-merton-1971` | Catalogue search for household finance, lifecycle, retirement, estate and tax-aware investing | New section, three pathways; jurisdiction-dated rule sources for tax and transfer |
| F13 | 105 prose fields hard-code 183 section or Part numbers ("(20.1)", "Section 18", "Part III"); every one becomes wrong when 13 sections are inserted | Search of `prerequisites`, `learning_note`, `checkpoint` and branch reasons | Add a `[[route-id]]` and `[[part:part-id]]` reference syntax that the generator resolves to live numbers, and convert every numeric reference; validation rejects a bare numeric section reference |
| F14 | The generator hard-codes the old structure: "Start with the common toolkit", "Part VI" for digital assets, the study-method link to `route-common-toolkit`, and the assumption that every overview has a `legacy_label` | `refresh_views.py` lines 481, 857, 863, 945 and the `'legacy_label' in r` tests | Compute these from the route file; make `legacy_label` optional for new overviews; add retired-overview bridges |
| F15 | Smaller target subsections are combined or missing. Credit portfolios sit with default models; forward commitments appear only in the options overview's Hull reading; macroeconomic foundations are in no reading of the macro section. The original record also called three subjects combined coverage, which overstated it (corrected in section 12): no route taught or assessed index construction (`demand-flows-passive` and `etf-index-closing-execution` cover demand effects and execution), institutional investment policy (`alm-liquidity` covers pension and insurer liability hedging and funding stress) or tranche valuation (`credit-models-default` builds a pool-loss distribution and `synthetic-risk-transfer` allocates realised losses, with no link between them) | Route readings and checkpoints | Credit portfolios stay combined with default models. Forward pricing by carry is added to the time-value pathway checkpoint; a macroeconomics text is added to the macro overview. The three gaps are closed by extending existing pathways (section 12) |

### 4.1 Target-subject classification

"Guide gap" means the guide lacks a usable route; "compendium gap" means the
compendium lacks a compiled home. The compendium plan lists 11 unpopulated
compendium sections (for example `causal-inference`, `onchain-protocols`,
`event-contract-trading`); all except `causal-inference` already have complete
guide routes, so they are compendium gaps only.

| Section | Adequately covered | Covered but combined or misplaced | Partial | Missing (guide gap) |
| --- | --- | --- | --- | --- |
| `financial-mathematics` | | | Required returns (implicit in valuation routes) | Discounting and compounding; present value and cash-flow additivity; holding-period, time-weighted and money-weighted returns |
| `probability-statistics` | Random variables and distributions; sampling and estimation; hypothesis tests; resampling | Heavy tails and extreme values (inside the covariance pathway) | Descriptive statistics; conditional moments and dependence (copulas inside covariance pathway) | |
| `regression-time-series` | Volatility models; forecast evaluation and structural breaks | | Linear and multiple regression; diagnostics (texts listed in the probability pathway, never tested) | Stationarity and unit roots; autoregression and cointegration (no checkpoint) |
| `stochastic-processes-calculus` | All five subsections (`stochastic-calculus-control`) | | | |
| `bayesian-inference` | All four (`bayesian-parameter-uncertainty`) | | | |
| `high-dimensional-statistics` | Covariance estimation; random-matrix noise; shrinkage; factor estimation | | Regularisation (sparse regression only as a reading rationale) | |
| `numerical-optimisation` | Monte Carlo and variance reduction; constrained and convex optimisation | Discretisation error (in the stochastic-calculus checkpoint) | Root finding and linear algebra (optional branches only) | |
| `asset-pricing` | Robust standard errors; factor-model tests; predictability; event studies | | | Systematic risk, CAPM and factor pricing theory |
| `causal-inference` | DiD, synthetic control, RD; causal ML; experiments; sequential monitoring | | Causal estimands and identification (overview level only) | |
| `research-engineering-validation` | Backtest inference; point-in-time data; governance; reproducibility | Strategy anatomy and research specification (in `common-toolkit`'s outcome) | | |
| `professional-ethics` | | | | All five subsections |
| `ml-alternative-data` | All seven subsections | | | |
| `rates-credit-mortgages`, `government-bond-markets` | All subsections | | | |
| `financial-statement-analysis` | | Statement use for valuation signals (`equity-events-fundamentals`) | | Reporting and statements; measurement; group and international reporting; ratios and reporting quality; forecasting |
| `corporate-finance` | | Restructuring (`gap-credit-distress-book` in credit) | Payout and issuance evidence (equity events) | Ownership and business models; working capital; capital investment; capital structure and funding costs |
| `corporate-credit-capital` | Bonds and CDS; bank capital; hybrids; labelled bonds | Credit analysis, default models and credit portfolios (one pathway) | | |
| `securitised-structured-credit` | Structures; waterfalls; risk transfer; workouts; default dependence and tranche valuation (`synthetic-risk-transfer`, after `credit-models-default`, since the correction pass) | | | Originally recorded as combined; in fact no route valued a tranche (section 12) |
| `systematic-equities`, `volatility-trading-premia`, `currency-markets`, `global-regional-markets` | All subsections | | | |
| `volatility-options` | Valuation; surfaces; hedging; numerical pricing; exotics | | Contract foundations and forward commitments (overview reading only) | |
| `multi-asset-systematic-macro` | Macro data and policy; cross-asset strategies; regimes and nowcasting | Asset valuation and expectations (overview) | Economic foundations | |
| `international-equity-markets` | Integration; global factors; EM; cross-listings; index construction (`intl-equity-integration`, since the correction pass) | | | Originally recorded as combined; in fact no route taught index construction (section 12) |
| Part IV sections | All subsections, including institutional investment policy (`alm-liquidity`, since the correction pass) | Optimal execution with TCA (one pathway) | | Institutional portfolios were originally recorded as combined; in fact only liability hedging and funding stress were taught (section 12) |
| Part V sections | All subsections | | | |
| `private-capital-allocator`, `real-asset-investor`, `insurance-climate-risk` | All subsections | | | |
| `private-wealth-management` | | | Lifecycle portfolio choice (Merton, in stochastic control) | Client circumstances; wealth and investment planning; preservation and concentrated exposures; succession and transfer |
| Parts VII and VIII | All subsections | | | |

## 5. Gaps and readings needed

Each new pathway follows the existing format: outcome, prose prerequisites,
prerequisite routes, staged readings with reasons, checkpoint and optional branches.
Existing catalogue entries are preferred; a new entry is added only after its
identity, edition or version and availability are checked, with the scope of the
check recorded in its version record.

| Gap | New routes | Existing entries used | New catalogue entries needed |
| --- | --- | --- | --- |
| F1 | Overview `financial-mathematics`; `time-value-cash-flows`; `return-measurement` | `catalogue-0233`, `s7-hulloptions`, `wide-bacon-attribution`, `wide-gips-2020`, `s15-campbell`, `wide-dimson-marsh-staunton` | OpenStax *Principles of Finance* (2e, 2026); Berk–DeMarzo *Corporate Finance* (6th ed.), shared with F11; Dichev (2007) on dollar-weighted returns. Luenberger's *Investment Science* was considered but not added (section 10) |
| F3 | `regression-econometrics` | `s15-wooldridge`, `s15-greene`, `wide-hansen-econometrics`, `wide-hayashi-econometrics` | Hausman (1978) specification test |
| F4 | `stationarity-cointegration` | `s7-hamilton`, `wide-lutkepohl-mts` | Dickey–Fuller (1979); Sims (1980); Engle–Granger (1987); Johansen (1991) |
| F5 | `heavy-tails-extremes` | `wide-cont-stylized-facts`, `wide-embrechts-extremal`, `wide-joe-copulas`, `w2-mcneil-frey`, `w2-longin-solnik` | None |
| F6 | `asset-pricing-theory` | `s6-cochrane`, `w2-pennacchi`, `wide-harrison-kreps`, `wide-hansen-jagannathan-bounds` | Sharpe (1964); Ross (1976); Mehra–Prescott (1985) |
| F7, F8 | Overviews `asset-pricing`, `causal-inference` | `wide-cochrane-discount-rates`, `w2-welch-reproducing`, `wide-campbell-fdm`, `w5-athey-imbens-jep`, `s3-imbens`, `al-hernan` | None |
| F9 | Overview `professional-ethics`; `ethics-code-standards`; `fiduciary-duties-conflicts` | `wide-gips-2020` | CFA Institute *Standards of Practice Handbook* (12th ed., 2024) and Rules of Procedure; CFA Institute Asset Manager Code; SEC adviser-conduct interpretation and Regulation Best Interest (2019); ESMA MiFID II suitability guidelines; EU Market Abuse Regulation; conduct evidence (Egan–Matvos–Seru; Gennaioli–Shleifer–Vishny; Zingales) |
| F10 | Overview `financial-statement-analysis`; `financial-reporting-statements`; `accounting-measurement`; `group-international-reporting`; `financial-ratio-quality`; `financial-statement-forecasting` | `w5-penman-fsa`, `wide-koller-valuation`, `wide-sloan-accruals`, `exp-edgar` | EU-endorsed IFRS text; IASB Conceptual Framework and IFRS 18; a statement-analysis text; Nissim–Penman (2001); Dechow–Ge–Schrand (2010); Dechow et al. (2011); Fama–French (2000) on profitability forecasts |
| F11 | Overview `corporate-finance`; `capital-budgeting-investment`; `capital-structure-payout`; `corporate-governance-restructuring` | `wide-koller-valuation`, `wide-leland-1994`, `gap-credit-distress-book` | A corporate-finance text; Modigliani–Miller (1958, 1961); Jensen–Meckling (1976); Myers (1984); Myers–Majluf (1984); Graham–Harvey (2001); Fama–French (2001); Shleifer–Vishny (1997); Andrade–Mitchell–Stafford (2001); OECD Principles of Corporate Governance (2023) |
| F12 | Overview `private-wealth-management`; `household-finance-lifecycle`; `tax-aware-wealth-preservation`; `wealth-transfer-succession` | `wide-merton-1969` | Campbell (2006); Ibbotson et al. (2007); Bodie–Merton–Samuelson (1992); Cocco–Gomes–Maenhout (2005); Yaari (1965); Constantinides (1983); Dammon–Spatt–Zhang (2004); Meulbroek (2005); Bessembinder (2018); dated US and UK tax and transfer rules; succession evidence |
| F15 | Revised `multi-asset-systematic-macro` overview; in the correction pass, extended `intl-equity-integration`, `alm-liquidity` and `synthetic-risk-transfer` | `depth-alm-novy-marx-rauh-2011`, `depth-alm-endowment-brown-2014`, `wide-swensen-pioneering`, `depth-alm-imf-salm-2014`, `w4-elkamhi-lee-tpa`, `depth-alm-bis-pension-2026`, `s6-duffie`, `catalogue-0238` | OpenStax *Principles of Macroeconomics* (3e, 2022); Mankiw's *Macroeconomics* was considered but not added (section 10). Correction pass: MSCI *Global Investable Market Indexes Methodology* (March 2026) and *Index Calculation Methodology* (June 2026) |

Rules, tax and reporting sources state their jurisdiction and effective date in the
catalogue entry and in the route text.

## 6. Identifier compatibility and prerequisites

- **Kept identifiers.** All 203 baseline pathway keys and 36 baseline overview keys
  are kept, with their `legacy_label` values (`route-2` … `route-38`). Catalogue
  keys never change.
- **Retired overview keys.** `common-toolkit` and `empirical-causal-research` stop
  being sections. A new top-level `retired_overviews` record keeps their names,
  legacy labels and successor sections. The generator places a short navigation
  bridge on the opening page of the Part holding the first successor, carrying
  `route-common-toolkit`, `route-1`, `route-empirical-causal-research` and
  `route-16`, so old links resolve without a duplicate umbrella section. The
  generator rejects a retired key used as a live route or prerequisite.
- **New overviews** have no `legacy_label`; the generator distinguishes overviews by
  membership, not by that field.
- **Prose references.** `[[route-id]]` prints the route's current number and
  `[[part:part-id]]` the Part's Roman numeral, so prose survives renumbering.
- **Prerequisite remapping.** Every `prerequisite_routes` entry naming a retired
  overview is replaced by the most specific new route its prose names:

| Route | Baseline | Target |
| --- | --- | --- |
| Overviews `rates-credit-mortgages`, `energy-commodities`, `real-asset-investor`, `digital-assets-prediction-markets` | `common-toolkit` | `financial-mathematics` |
| `systematic-equities`, `multi-asset-systematic-macro` | `common-toolkit` | `asset-pricing` |
| `volatility-options`, `execution-market-making` | `common-toolkit` | `stochastic-processes-calculus` |
| `portfolio-construction-risk` | `common-toolkit` | `asset-pricing`, `high-dimensional-statistics`, `numerical-optimisation` |
| `research-engineering-validation`, `insurance-climate-risk`, `event-contracts-prediction-markets` | `common-toolkit` | `probability-statistics` |
| `ml-alternative-data` | `common-toolkit` | `regression-time-series` |
| `private-capital-allocator` | `common-toolkit` | `financial-mathematics`, `corporate-finance` |
| `corporate-credit-capital` | `rates-credit-mortgages` | adds `financial-statement-analysis` |
| `backtest-inference` | `common-toolkit` | `probability-statistical-inference` |
| `financial-ml-evaluation`, `crypto-signals` | `common-toolkit` | `return-measurement` |
| `standard-errors-inference` | `empirical-causal-research` | `asset-pricing`, `regression-econometrics` |
| `empirical-asset-pricing`, `event-studies` | `empirical-causal-research` | `asset-pricing` (and `asset-pricing-theory` for the former) |
| `causal-research-designs`, `causal-policy-evaluation`, `controlled-experiments` | `empirical-causal-research` | `causal-inference` (plus `standard-errors-inference` for the first) |
| `prediction-forecast-evidence` | `empirical-causal-research` | `causal-inference` |
| Six moved Part I pathways | `common-toolkit` | their new overview |
| Correction pass (section 12): `capital-budgeting-investment`, `financial-statement-forecasting`, `tax-aware-wealth-preservation`, `prediction-price-theory`, `synthetic-risk-transfer`; overview `corporate-finance` | as migrated | add `accounting-measurement`; `time-value-cash-flows`; `return-measurement`; `asset-pricing-theory` and `probability-statistical-inference`; `credit-models-default`; `asset-pricing-theory` replaces `asset-pricing` |

The generator's existing check that every prerequisite resolves and precedes its
dependant guards all of these.

## 7. Implementation stages

1. **Generator.** Optional `legacy_label`; `retired_overviews` bridges and checks;
   route and Part reference tokens with validation; computed front-matter text;
   unchanged output for an unchanged route file except where text was structural.
2. **Restructure.** Parts, overview membership, renames, prerequisite remapping,
   prose conversion, `chart_rows` for Part III, then regenerate and resolve every
   validation message.
3. **Catalogue.** Add and verify the new resources in existing catalogue chapters
   (new sections in chapters 1, 2, 6, 10 and 22, so that chapter numbers and
   labels do not shift); rebuild the catalogue PDF.
4. **Content.** Write the 13 new overviews and 19 new pathways, revise the split
   pathways and the two revised overviews, and set section goals, capstones and
   specialist order.
5. **Validate and rebuild.** Catalogue, generator and guide builds; structural
   checks; log checks; link and page-number checks; rendered-PDF inspection.
6. **Records.** Update README, structural mapping, bibliographic audit and this
   plan's evidence.

## 8. Acceptance criteria

- Exactly 8 Parts and 49 overview sections with the target keys, order and Part
  membership; section counts 7, 5, 13, 4, 7, 4, 6, 3.
- Every baseline pathway present with its key; every new pathway has a complete
  route; no placeholder or unverified reading list is described as complete.
- Every reading and branch resolves to a catalogue entry or label; every
  prerequisite resolves and precedes its dependant; no retired key is live.
- Section goals map exactly the section's pathways; capstones name their pathways;
  `specialist_order` matches each section DAG.
- No bare numeric section reference in prose; generated contents, bookmarks and
  DAGs show the eight Parts.
- Both LaTeX logs free of undefined references; guide free of overfull boxes; every
  guide link resolves to a named destination in the catalogue PDF; printed page
  numbers match the catalogue `.aux`.

## 9. Progress and evidence

| Stage | State | Evidence |
| --- | --- | --- |
| Audit and plan | Complete | Sections 1–6; baseline output reproduced byte for byte |
| 1. Generator | Complete | `refresh_views.py`: overviews detected by `specialist_order`, `legacy_label` optional; `retired_overviews` validated and rendered as bridges carrying `route-common-toolkit`, `route-1`, `route-empirical-causal-research` and `route-16`; `[[route-id]]` and `[[part:part-id]]` prose references resolved and validated; bare section or part numbers rejected outside reading selections; front-matter references computed from the route file; cross-part applications line computed; whole-guide DAG continues on a second page when the parts exceed one page. Run on the unchanged baseline route file (with only the new bare-number check disabled), the generator changed only the intended front-matter lines |
| 2. Restructure | Complete | 8 Parts, 49 overviews; section counts 7, 5, 13, 4, 7, 4, 6, 3; Part III `chart_rows` updated; 183 numeric references in 105 fields converted to route keys; 4 overviews renamed; prerequisites remapped as in section 6 |
| 3. Catalogue | Complete | 62 entries added in new sections at the ends of chapters 1, 6, 10 (two) and 22, new subsections at the ends of sections 2.1 and 2.2, and one entry in section 13.1, so no existing chapter or section number moved; catalogue then 3,955 entries. The correction pass removed one of the 62 as a duplicate and added two, giving 63 additions and 3,956 entries (section 12). Every DOI was resolved on Crossref with title and authors matched (four first-guess DOIs were wrong and were replaced); abstracts from Crossref, OpenAlex, Semantic Scholar, RePEc/IDEAS or the publisher; rules from the Federal Register API, EU Cellar metadata, GOV.UK content API and issuer PDFs; books from publisher pages. Each version record states its scope |
| 4. Content | Complete | 13 new overviews and 19 new pathways (section 11); 3 pathways split and revised; 10 moved; 6 retained pathways given new prerequisites; `research-engineering-validation` and `multi-asset-systematic-macro` overviews revised. All 222 pathways and 49 overviews have an outcome, prerequisites, ordered readings with reasons, a checkpoint and branches where useful |
| 5. Validate and rebuild | Complete | See section 9.1 |
| 6. Records | Complete | README, [structural_mapping.md](structural_mapping.md), [bibliographic_audit.md](bibliographic_audit.md) and [editorial_backlog.md](editorial_backlog.md) updated |

### 9.1 Validation evidence (22 October 2026)

These are the first validation's results. Section 12.3 gives the results after the correction pass, which supersede the counts below.

Commands, in the README's order: `latexmk -pdf institutional_quantitative_finance_reading_list.tex`, `python3 refresh_views.py`, `latexmk -pdf institutional_quantitative_finance_learning_guide.tex`.

- Generator: "Refreshed 49 overview routes and 222 specialist pathways, 2674 selected readings, 760 extended notes and 3955 recency records." Its checks passed: unique identifiers; every overview placed once; every pathway placed once; every reading and branch resolves to a catalogue entry or label; every prerequisite resolves and precedes its dependant; section goals map exactly each section's pathways; capstones name only their own pathways; every `specialist_order` equals its section DAG's row order; every prose reference resolves; no bare numeric reference; retired keys not live.
- Structure: Part sizes 7, 5, 13, 4, 7, 4, 6, 3 with the target keys in order. Mapping the nine replacement sections back to `common-toolkit` and `empirical-causal-research`, removing the four additions and collapsing the two expansions reproduces the baseline's 38-section order exactly. All 203 baseline pathway keys and all 36 retained `legacy_label` values are present; no live route names `common-toolkit`, `empirical-causal-research`, the Part key `foundations`, a pre-rename overview name or a literal Part numeral.
- Logs: catalogue 0 undefined references, 0 multiply defined labels, 20 overfull boxes, the same number as the baseline build (one new 0.14pt box was removed by rewording an entry); guide 0 undefined references, 0 multiply defined labels, 0 overfull boxes. The HTML-link mode (`catalogue_link_target: html`) also generates.
- Links: all 3,896 catalogue links in the guide (3,420 distinct) resolve to named destinations in the catalogue PDF, and all 3,896 printed catalogue page numbers equal the destination's page in that PDF.
- Navigation: PDF bookmarks list the study method, the DAG and Parts I–VIII at the top level, with sections and pathways beneath; the printed contents show the same hierarchy.
- Rendered pages inspected (Ghostscript at 70–75 dpi): contents; both whole-guide DAG pages; Part I and Part II openers with their former-section bridges; the financial-mathematics overview; the asset-pricing, financial-statement, corporate-finance and private-wealth section DAGs with their first pathways; the crypto-trading-strategies overview, whose converted references print current numbers. The first DAG page is dense but within the margins. Guide length rose from 311 to 345 pages.

These checks show that the documents build and link correctly. They do not establish the sources' claims.

## 10. Remaining limitations

- **Readings checked to metadata or abstract level only.** Like the existing catalogue, the new entries were verified for identity and version, not read in full. Eight annotations rest on the title and standard result because no abstract was retrievable (listed in [editorial_backlog.md](editorial_backlog.md)); Modigliani–Miller (1958) metadata come from a secondary index.
- **EU and IASB texts.** EUR-Lex refused automated access; the EU regulations were identified from Cellar metadata and the IASB pages were read, not the standards' text. Each record links the original act as published; the amending acts and the latest consolidated version (8 March 2026 for Regulation 2023/1803; 5 June 2026 for the Market Abuse Regulation) are identified from metadata only, and no consolidated text was read. Book chapter selections are topic selections, as elsewhere in the guide.
- **Jurisdiction-dated material.** Tax and transfer readings state US federal rules for calendar or tax year 2026 (Revenue Procedure 2025-32; Publication 550 for 2025 returns) and UK inheritance-tax thresholds as published on 6 April 2026; conduct rules are US (2019 releases) and EU (MAR, ESMA guidelines). They need annual review, and other jurisdictions are not covered.
- **Not added.** Luenberger's *Investment Science* (publisher page unreadable) and Mankiw's *Macroeconomics* (library records only); OpenStax and Berk–DeMarzo cover the same subjects.
- **Combined coverage.** Credit portfolios remain combined with default models in `credit-models-default`. Index construction, institutional investment policy and tranche valuation, first recorded here as combined, were not taught; the correction pass added required readings and assessed exercises for each inside existing pathways (section 12). Those exercises use stated synthetic or public inputs; they teach the mechanics, not a provider's production process or a live transaction.
- **Index methodologies.** The two MSCI documents were read only in the sections the pathway selects (recorded in each version record). MSCI's methodology page did not render for automated retrieval, so an edition later than March 2026 (construction) or June 2026 (calculation) was not ruled out. S&P Dow Jones Indices refused automated access, so its index-mathematics methodology was not added.
- **Tranche readings.** O'Kane's chapters are identified from Crossref chapter records and Duffie–Singleton's from the author-hosted table of contents; neither text was read. Both predate post-crisis conventions, which the exercise does not assume.
- **Compendium and vendored copy untouched.** The compendium repository and its `guide/` copy were not modified; adopting this edition there is separate work, and note keys for the two retired overviews will need the bridges described in the compendium plan.

## 11. Pathway ledger

Generated from the baseline (`343d145`) and migrated route files: every baseline pathway with its old and new number and section, and the 19 new pathways. "Retain unchanged" means the route record is identical; "prose references converted" means only numeric references or renamed section names in its text changed.

| Baseline | New | Pathway | Baseline section | New section | Disposition |
| --- | --- | --- | --- | --- | --- |
| new | 1.1 | `time-value-cash-flows` | | `financial-mathematics` | New pathway |
| new | 1.2 | `return-measurement` | | `financial-mathematics` | New pathway |
| 1.1 | 2.1 | `probability-statistical-inference` | `common-toolkit` | `probability-statistics` | Revise and split: renamed; econometrics texts moved to `regression-econometrics`; checkpoint uses autocorrelation instead of an OLS slope |
| new | 2.2 | `heavy-tails-extremes` | | `probability-statistics` | New pathway |
| new | 3.1 | `regression-econometrics` | | `regression-time-series` | New pathway |
| new | 3.2 | `stationarity-cointegration` | | `regression-time-series` | New pathway. Corrected 22 October 2026 (section 12): empirical assessment made conditional on unit-root and rank evidence |
| 1.4 | 3.3 | `time-series-volatility` | `common-toolkit` | `regression-time-series` | Move and split: renamed; ARMA, VAR, unit-root and cointegration foundations moved to `stationarity-cointegration`, now its prerequisite |
| 1.2 | 4.1 | `stochastic-calculus-control` | `common-toolkit` | `stochastic-processes-calculus` | Move; prerequisites now its overview and `probability-statistical-inference` |
| 1.5 | 5.1 | `bayesian-parameter-uncertainty` | `common-toolkit` | `bayesian-inference` | Move; prerequisites remapped; two branches became overview readings. Corrected 22 October 2026 (section 12): checkpoint prior restated as the zero-intercept restriction, supplied locally; no forward dependency |
| 1.3 | 6.1 | `high-dimensional-estimation` | `common-toolkit` | `high-dimensional-statistics` | Revise and split: renamed; tail, extreme-value and copula readings moved to `heavy-tails-extremes`; checkpoint adds factor-number selection |
| 1.6 | 7.1 | `numerical-methods-optimisation` | `common-toolkit` | `numerical-optimisation` | Move; prerequisites remapped; one branch became an overview reading |
| new | 8.1 | `asset-pricing-theory` | | `asset-pricing` | New pathway |
| 2.1 | 8.2 | `standard-errors-inference` | `empirical-causal-research` | `asset-pricing` | Move; prerequisites now `asset-pricing` and `regression-econometrics` |
| 2.3 | 8.3 | `empirical-asset-pricing` | `empirical-causal-research` | `asset-pricing` | Move; adds `asset-pricing-theory` prerequisite |
| 2.6 | 8.4 | `return-predictability` | `empirical-causal-research` | `asset-pricing` | Move; prose updated |
| 2.7 | 8.5 | `event-studies` | `empirical-causal-research` | `asset-pricing` | Move; prerequisite remapped |
| 2.2 | 9.1 | `causal-research-designs` | `empirical-causal-research` | `causal-inference` | Move; adds `standard-errors-inference` prerequisite |
| 2.4 | 9.2 | `causal-policy-evaluation` | `empirical-causal-research` | `causal-inference` | Move; prerequisites remapped |
| 2.5 | 9.3 | `controlled-experiments` | `empirical-causal-research` | `causal-inference` | Move; prerequisites remapped |
| 3.1 | 10.1 | `backtest-inference` | `research-engineering-validation` | `research-engineering-validation` | Retain; retired-overview prerequisite replaced by `probability-statistical-inference` |
| 3.2 | 10.2 | `point-in-time-data` | `research-engineering-validation` | `research-engineering-validation` | Retain; prose references converted to route keys |
| 3.3 | 10.3 | `model-governance-controls` | `research-engineering-validation` | `research-engineering-validation` | Retain; prose references converted to route keys |
| 3.4 | 10.4 | `reproducible-research-code` | `research-engineering-validation` | `research-engineering-validation` | Retain; prose references converted to route keys |
| new | 11.1 | `ethics-code-standards` | | `professional-ethics` | New pathway |
| new | 11.2 | `fiduciary-duties-conflicts` | | `professional-ethics` | New pathway |
| 4.1 | 12.1 | `statistical-learning-foundations` | `ml-alternative-data` | `ml-alternative-data` | Retain; prose references converted to route keys |
| 4.2 | 12.2 | `ml-asset-pricing` | `ml-alternative-data` | `ml-alternative-data` | Retain; prose references converted to route keys |
| 4.3 | 12.3 | `financial-ml-evaluation` | `ml-alternative-data` | `ml-alternative-data` | Retain; retired-overview prerequisite replaced by `return-measurement` |
| 4.4 | 12.4 | `forecasting-generative-rl` | `ml-alternative-data` | `ml-alternative-data` | Retain; prose references converted to route keys |
| 4.5 | 12.5 | `reinforcement-learning-trading` | `ml-alternative-data` | `ml-alternative-data` | Retain; prose references converted to route keys |
| 4.6 | 12.6 | `text-llm-agents` | `ml-alternative-data` | `ml-alternative-data` | Retain; prose references converted to route keys |
| 4.7 | 12.7 | `alternative-data-sources` | `ml-alternative-data` | `ml-alternative-data` | Retain; prose references converted to route keys |
| 5.1 | 13.1 | `curve-term-structure` | `rates-credit-mortgages` | `rates-credit-mortgages` | Retain unchanged |
| 5.2 | 13.2 | `rate-derivatives` | `rates-credit-mortgages` | `rates-credit-mortgages` | Retain unchanged |
| 5.3 | 13.3 | `monetary-policy-curve` | `rates-credit-mortgages` | `rates-credit-mortgages` | Retain unchanged |
| 5.4 | 13.4 | `bond-risk-premia` | `rates-credit-mortgages` | `rates-credit-mortgages` | Retain unchanged |
| 5.5 | 13.5 | `rates-inflation` | `rates-credit-mortgages` | `rates-credit-mortgages` | Retain unchanged |
| 6.1 | 14.1 | `treasury-market-functioning` | `government-bond-markets` | `government-bond-markets` | Retain unchanged |
| 6.2 | 14.2 | `treasury-issuance-demand` | `government-bond-markets` | `government-bond-markets` | Retain unchanged |
| 6.3 | 14.3 | `sovereign-municipal` | `government-bond-markets` | `government-bond-markets` | Retain unchanged |
| 6.4 | 14.4 | `municipal-bonds` | `government-bond-markets` | `government-bond-markets` | Retain unchanged |
| 6.5 | 14.5 | `dm-sovereign-bonds` | `government-bond-markets` | `government-bond-markets` | Retain unchanged |
| new | 15.1 | `financial-reporting-statements` | | `financial-statement-analysis` | New pathway. Corrected 22 October 2026 (section 12): the EU regulation is to be read in its current consolidated version |
| new | 15.2 | `accounting-measurement` | | `financial-statement-analysis` | New pathway |
| new | 15.3 | `group-international-reporting` | | `financial-statement-analysis` | New pathway. Corrected 22 October 2026 (section 12): forward mention of `currency-markets` marked as not needed |
| new | 15.4 | `financial-ratio-quality` | | `financial-statement-analysis` | New pathway |
| new | 15.5 | `financial-statement-forecasting` | | `financial-statement-analysis` | New pathway. Corrected 22 October 2026 (section 12): `time-value-cash-flows` added to its prerequisites |
| new | 16.1 | `capital-budgeting-investment` | | `corporate-finance` | New pathway. Corrected 22 October 2026 (section 12): `accounting-measurement` added to its prerequisites |
| new | 16.2 | `capital-structure-payout` | | `corporate-finance` | New pathway |
| new | 16.3 | `corporate-governance-restructuring` | | `corporate-finance` | New pathway |
| 7.1 | 17.1 | `credit-models-default` | `corporate-credit-capital` | `corporate-credit-capital` | Retain unchanged |
| 7.2 | 17.2 | `corporate-credit-cds` | `corporate-credit-capital` | `corporate-credit-capital` | Retain unchanged |
| 7.3 | 17.3 | `bank-capital` | `corporate-credit-capital` | `corporate-credit-capital` | Retain unchanged |
| 7.4 | 17.4 | `corporate-hybrids-preferred` | `corporate-credit-capital` | `corporate-credit-capital` | Retain unchanged |
| 7.5 | 17.5 | `sustainable-bonds` | `corporate-credit-capital` | `corporate-credit-capital` | Retain unchanged |
| 8.1 | 18.1 | `covered-bonds` | `securitised-structured-credit` | `securitised-structured-credit` | Retain unchanged |
| 8.2 | 18.2 | `sukuk` | `securitised-structured-credit` | `securitised-structured-credit` | Retain unchanged |
| 8.3 | 18.3 | `mortgages-abs-clo` | `securitised-structured-credit` | `securitised-structured-credit` | Retain unchanged |
| 8.4 | 18.4 | `synthetic-risk-transfer` | `securitised-structured-credit` | `securitised-structured-credit` | Revise: Corrected 22 October 2026 (section 12): `credit-models-default` added as a prerequisite; Duffie–Singleton and O'Kane readings; tranche-valuation exercise with physical and risk-neutral assumptions |
| 8.5 | 18.5 | `cmbs-workouts` | `securitised-structured-credit` | `securitised-structured-credit` | Retain unchanged |
| 9.1 | 19.1 | `equity-factor-premia` | `systematic-equities` | `systematic-equities` | Retain unchanged |
| 9.2 | 19.2 | `statistical-arbitrage` | `systematic-equities` | `systematic-equities` | Retain unchanged |
| 9.3 | 19.3 | `demand-flows-passive` | `systematic-equities` | `systematic-equities` | Retain unchanged |
| 9.4 | 19.4 | `equity-events-fundamentals` | `systematic-equities` | `systematic-equities` | Retain; adds `financial-ratio-quality` prerequisite |
| 9.5 | 19.5 | `equity-trader-signals` | `systematic-equities` | `systematic-equities` | Retain unchanged |
| 9.6 | 19.6 | `equity-long-short-construction` | `systematic-equities` | `systematic-equities` | Retain; prose references converted to route keys |
| 9.7 | 19.7 | `equity-event-driven` | `systematic-equities` | `systematic-equities` | Retain unchanged |
| 10.1 | 20.1 | `option-pricing-models` | `volatility-options` | `volatility-options` | Retain unchanged |
| 10.2 | 20.2 | `convertible-bonds` | `volatility-options` | `volatility-options` | Retain unchanged |
| 10.3 | 20.3 | `volatility-models` | `volatility-options` | `volatility-options` | Retain unchanged |
| 10.4 | 20.4 | `option-hedging-smile` | `volatility-options` | `volatility-options` | Retain unchanged |
| 10.5 | 20.5 | `learning-pricing-model-risk` | `volatility-options` | `volatility-options` | Retain unchanged |
| 10.6 | 20.6 | `exotics-structured-products` | `volatility-options` | `volatility-options` | Retain unchanged |
| 11.1 | 21.1 | `option-premia-dealers` | `volatility-trading-premia` | `volatility-trading-premia` | Retain unchanged |
| 11.2 | 21.2 | `option-implied-information` | `volatility-trading-premia` | `volatility-trading-premia` | Retain unchanged |
| 11.3 | 21.3 | `equity-option-returns` | `volatility-trading-premia` | `volatility-trading-premia` | Retain unchanged |
| 11.4 | 21.4 | `vix-correlation-dividends` | `volatility-trading-premia` | `volatility-trading-premia` | Retain unchanged |
| 11.5 | 21.5 | `short-dated-retail-options` | `volatility-trading-premia` | `volatility-trading-premia` | Retain unchanged |
| 12.1 | 22.1 | `cross-asset-style-premia` | `multi-asset-systematic-macro` | `multi-asset-systematic-macro` | Retain unchanged |
| 12.2 | 22.2 | `trend-following` | `multi-asset-systematic-macro` | `multi-asset-systematic-macro` | Retain unchanged |
| 12.3 | 22.3 | `risk-parity-vol-targeting` | `multi-asset-systematic-macro` | `multi-asset-systematic-macro` | Retain; prose references converted to route keys |
| 12.4 | 22.4 | `macro-announcements-policy` | `multi-asset-systematic-macro` | `multi-asset-systematic-macro` | Retain unchanged |
| 12.5 | 22.5 | `macro-regimes-stock-bond` | `multi-asset-systematic-macro` | `multi-asset-systematic-macro` | Retain unchanged |
| 12.6 | 22.6 | `macro-nowcasting-signals` | `multi-asset-systematic-macro` | `multi-asset-systematic-macro` | Retain unchanged |
| 13.1 | 23.1 | `fx-determination-forecasting` | `currency-markets` | `currency-markets` | Retain unchanged |
| 13.2 | 23.2 | `fx-funding-settlement` | `currency-markets` | `currency-markets` | Retain unchanged |
| 13.3 | 23.3 | `fx-premia` | `currency-markets` | `currency-markets` | Retain unchanged |
| 13.4 | 23.4 | `fx-cip-dollar-funding` | `currency-markets` | `currency-markets` | Retain; prose references converted to route keys |
| 13.5 | 23.5 | `fx-volatility-crash-risk` | `currency-markets` | `currency-markets` | Retain unchanged |
| 13.6 | 23.6 | `currency-hedging` | `currency-markets` | `currency-markets` | Retain unchanged |
| 13.7 | 23.7 | `em-currencies-intervention` | `currency-markets` | `currency-markets` | Retain unchanged |
| 14.1 | 24.1 | `intl-equity-integration` | `international-equity-markets` | `international-equity-markets` | Revise: Corrected 22 October 2026 (section 12): renamed; two MSCI methodology readings and an index-construction exercise |
| 14.2 | 24.2 | `global-equity-factors` | `international-equity-markets` | `international-equity-markets` | Retain unchanged |
| 14.3 | 24.3 | `em-frontier-equities` | `international-equity-markets` | `international-equity-markets` | Retain unchanged |
| 14.4 | 24.4 | `cross-listing-global-trading` | `international-equity-markets` | `international-equity-markets` | Retain; prose references converted to route keys |
| 14.5 | 24.5 | `china-em-equities` | `international-equity-markets` | `international-equity-markets` | Retain unchanged |
| 15.1 | 25.1 | `em-capital-flows` | `global-regional-markets` | `global-regional-markets` | Retain unchanged |
| 15.2 | 25.2 | `em-local-currency-bonds` | `global-regional-markets` | `global-regional-markets` | Retain unchanged |
| 15.3 | 25.3 | `regional-local-market-access` | `global-regional-markets` | `global-regional-markets` | Retain unchanged |
| 16.1 | 26.1 | `portfolio-construction` | `portfolio-construction-risk` | `portfolio-construction-risk` | Retain unchanged |
| 16.2 | 26.2 | `risk-tail-systemic` | `portfolio-construction-risk` | `portfolio-construction-risk` | Retain; adds `heavy-tails-extremes` prerequisite |
| 16.3 | 26.3 | `performance-manager-evaluation` | `portfolio-construction-risk` | `portfolio-construction-risk` | Retain unchanged |
| 16.4 | 26.4 | `climate-sustainable` | `portfolio-construction-risk` | `portfolio-construction-risk` | Retain unchanged |
| 17.1 | 27.1 | `funding-crowding` | `portfolio-risk-financing` | `portfolio-risk-financing` | Retain unchanged |
| 17.2 | 27.2 | `money-markets-repo-lending` | `portfolio-risk-financing` | `portfolio-risk-financing` | Retain unchanged |
| 17.3 | 27.3 | `collateral-xva` | `portfolio-risk-financing` | `portfolio-risk-financing` | Retain unchanged |
| 17.4 | 27.4 | `alm-liquidity` | `portfolio-risk-financing` | `portfolio-risk-financing` | Revise: Corrected 22 October 2026 (section 12): renamed; six institutional-policy readings (Swensen moved from branch to reading) and an investment-policy comparison |
| 17.5 | 27.5 | `synthetic-equity-cfd-trs` | `portfolio-risk-financing` | `portfolio-risk-financing` | Retain unchanged |
| 18.1 | 28.1 | `market-making-lob` | `execution-market-making` | `execution-market-making` | Retain unchanged |
| 18.2 | 28.2 | `lob-deep-learning` | `execution-market-making` | `execution-market-making` | Retain; prose references converted to route keys |
| 18.3 | 28.3 | `options-execution` | `execution-market-making` | `execution-market-making` | Retain unchanged |
| 18.4 | 28.4 | `bond-swap-dealer-market-making` | `execution-market-making` | `execution-market-making` | Retain unchanged |
| 18.5 | 28.5 | `market-simulation` | `execution-market-making` | `execution-market-making` | Retain unchanged |
| 18.6 | 28.6 | `fx-dealer-market-making` | `execution-market-making` | `execution-market-making` | Retain unchanged |
| 18.7 | 28.7 | `hft-market-design` | `execution-market-making` | `execution-market-making` | Retain unchanged |
| 19.1 | 29.1 | `price-impact-execution` | `execution-trading-costs` | `execution-trading-costs` | Retain unchanged |
| 19.2 | 29.2 | `market-structure-execution-quality` | `execution-trading-costs` | `execution-trading-costs` | Retain unchanged |
| 19.3 | 29.3 | `otc-fixed-income-trading` | `execution-trading-costs` | `execution-trading-costs` | Retain unchanged |
| 19.4 | 29.4 | `etf-index-closing-execution` | `execution-trading-costs` | `execution-trading-costs` | Retain unchanged |
| 19.5 | 29.5 | `futures-execution` | `execution-trading-costs` | `execution-trading-costs` | Retain unchanged |
| 19.6 | 29.6 | `retail-cfd-brokers` | `execution-trading-costs` | `execution-trading-costs` | Retain unchanged |
| 20.1 | 30.1 | `commodity-storage-curves` | `energy-commodities` | `energy-commodities` | Retain; prose references converted to route keys |
| 20.2 | 30.2 | `commodity-curve-models` | `energy-commodities` | `energy-commodities` | Retain; prose references converted to route keys |
| 20.3 | 30.3 | `commodity-hedging` | `energy-commodities` | `energy-commodities` | Retain; prose references converted to route keys |
| 20.4 | 30.4 | `commodity-options-real-options` | `energy-commodities` | `energy-commodities` | Retain; prose references converted to route keys |
| 21.1 | 31.1 | `commodity-spot-benchmarks` | `commodity-spot-markets` | `commodity-spot-markets` | Retain; prose references converted to route keys |
| 21.2 | 31.2 | `commodity-spatial-arbitrage` | `commodity-spot-markets` | `commodity-spot-markets` | Retain; prose references converted to route keys |
| 21.3 | 31.3 | `commodity-price-cycles` | `commodity-spot-markets` | `commodity-spot-markets` | Retain; prose references converted to route keys |
| 21.4 | 31.4 | `commodity-stabilisation-trade-policy` | `commodity-spot-markets` | `commodity-spot-markets` | Retain; prose references converted to route keys |
| 21.5 | 31.5 | `commodity-long-run-prices` | `commodity-spot-markets` | `commodity-spot-markets` | Retain; prose references converted to route keys |
| 22.1 | 32.1 | `futures-delivery-manipulation` | `physical-commodity-markets` | `physical-commodity-markets` | Retain; prose references converted to route keys |
| 22.2 | 32.2 | `metals-storage-delivery` | `physical-commodity-markets` | `physical-commodity-markets` | Retain; prose references converted to route keys |
| 22.3 | 32.3 | `agricultural-futures-delivery` | `physical-commodity-markets` | `physical-commodity-markets` | Retain; prose references converted to route keys |
| 22.4 | 32.4 | `crude-oil-products` | `physical-commodity-markets` | `physical-commodity-markets` | Retain; prose references converted to route keys |
| 22.5 | 32.5 | `commodity-information-discovery` | `physical-commodity-markets` | `physical-commodity-markets` | Retain; prose references converted to route keys |
| 22.6 | 32.6 | `freight-forward-hedging` | `physical-commodity-markets` | `physical-commodity-markets` | Retain; prose references converted to route keys |
| 22.7 | 32.7 | `commodity-trading-finance` | `physical-commodity-markets` | `physical-commodity-markets` | Retain; prose references converted to route keys |
| 23.1 | 33.1 | `commodity-premia` | `commodity-investing-premia` | `commodity-investing-premia` | Retain; prose references converted to route keys |
| 23.2 | 33.2 | `commodity-factor-strategies` | `commodity-investing-premia` | `commodity-investing-premia` | Retain unchanged |
| 23.3 | 33.3 | `commodity-financialisation` | `commodity-investing-premia` | `commodity-investing-premia` | Retain unchanged |
| 23.4 | 33.4 | `commodity-allocation-inflation` | `commodity-investing-premia` | `commodity-investing-premia` | Retain; prose references converted to route keys |
| 23.5 | 33.5 | `commodity-index-products` | `commodity-investing-premia` | `commodity-investing-premia` | Retain; prose references converted to route keys |
| 24.1 | 34.1 | `oil-price-shocks` | `oil-shocks-macro` | `oil-shocks-macro` | Retain unchanged |
| 24.2 | 34.2 | `oil-price-forecasting` | `oil-shocks-macro` | `oil-shocks-macro` | Retain; prose references converted to route keys |
| 24.3 | 34.3 | `oil-shocks-inflation-policy` | `oil-shocks-macro` | `oil-shocks-macro` | Retain; prose references converted to route keys |
| 24.4 | 34.4 | `oil-asset-prices` | `oil-shocks-macro` | `oil-shocks-macro` | Retain; prose references converted to route keys |
| 25.1 | 35.1 | `gas-hub-pricing` | `power-gas-environmental` | `power-gas-environmental` | Retain; prose references converted to route keys |
| 25.2 | 35.2 | `physical-lng` | `power-gas-environmental` | `power-gas-environmental` | Retain unchanged |
| 25.3 | 35.3 | `power-ftr` | `power-gas-environmental` | `power-gas-environmental` | Retain unchanged |
| 25.4 | 35.4 | `power-market-design` | `power-gas-environmental` | `power-gas-environmental` | Retain unchanged |
| 25.5 | 35.5 | `renewables-ppa-value` | `power-gas-environmental` | `power-gas-environmental` | Retain unchanged |
| 25.6 | 35.6 | `power-price-forecasting` | `power-gas-environmental` | `power-gas-environmental` | Retain unchanged |
| 25.7 | 35.7 | `power-short-term-flexibility` | `power-gas-environmental` | `power-gas-environmental` | Retain; prose references converted to route keys |
| 26.1 | 36.1 | `carbon-compliance-markets` | `environmental-markets` | `environmental-markets` | Retain unchanged |
| 26.2 | 36.2 | `carbon-allowance-derivatives` | `environmental-markets` | `environmental-markets` | Retain unchanged |
| 26.3 | 36.3 | `carbon-pass-through-leakage` | `environmental-markets` | `environmental-markets` | Retain; prose references converted to route keys |
| 26.4 | 36.4 | `voluntary-carbon-credits` | `environmental-markets` | `environmental-markets` | Retain unchanged |
| 26.5 | 36.5 | `environmental-instruments` | `environmental-markets` | `environmental-markets` | Retain unchanged |
| 27.1 | 37.1 | `pe-performance-measurement` | `private-capital-allocator` | `private-capital-allocator` | Retain; prose references converted to route keys |
| 27.2 | 37.2 | `private-equity-vc` | `private-capital-allocator` | `private-capital-allocator` | Retain; prose references converted to route keys |
| 27.3 | 37.3 | `private-credit-workouts` | `private-capital-allocator` | `private-capital-allocator` | Retain; prose references converted to route keys |
| 27.4 | 37.4 | `trade-receivables` | `private-capital-allocator` | `private-capital-allocator` | Retain; prose references converted to route keys |
| 27.5 | 37.5 | `royalty-rights` | `private-capital-allocator` | `private-capital-allocator` | Retain; prose references converted to route keys |
| 27.6 | 37.6 | `litigation-finance-claims` | `private-capital-allocator` | `private-capital-allocator` | Retain; prose references converted to route keys |
| 27.7 | 37.7 | `fund-liquidity` | `private-capital-allocator` | `private-capital-allocator` | Retain; prose references converted to route keys |
| 28.1 | 38.1 | `property-valuation` | `real-asset-investor` | `real-asset-investor` | Retain; prose references converted to route keys |
| 28.2 | 38.2 | `infrastructure-regulated-assets` | `real-asset-investor` | `real-asset-investor` | Retain; prose references converted to route keys |
| 28.3 | 38.3 | `equipment-aircraft-leasing` | `real-asset-investor` | `real-asset-investor` | Retain; prose references converted to route keys |
| 28.4 | 38.4 | `natural-resource-rights` | `real-asset-investor` | `real-asset-investor` | Retain; prose references converted to route keys |
| 28.5 | 38.5 | `collectibles-valuation` | `real-asset-investor` | `real-asset-investor` | Retain; prose references converted to route keys |
| 29.1 | 39.1 | `catastrophe-cyber` | `insurance-climate-risk` | `insurance-climate-risk` | Retain unchanged |
| 29.2 | 39.2 | `longevity-risk` | `insurance-climate-risk` | `insurance-climate-risk` | Retain unchanged |
| 29.3 | 39.3 | `weather-derivatives` | `insurance-climate-risk` | `insurance-climate-risk` | Retain unchanged |
| 29.4 | 39.4 | `sidecar-capital` | `insurance-climate-risk` | `insurance-climate-risk` | Retain unchanged |
| new | 40.1 | `household-finance-lifecycle` | | `private-wealth-management` | New pathway. Corrected 22 October 2026 (section 12): Campbell–Viceira reading now cites the existing entry `s16-r09` |
| new | 40.2 | `tax-aware-wealth-preservation` | | `private-wealth-management` | New pathway. Corrected 22 October 2026 (section 12): `return-measurement` added to its prerequisites |
| new | 40.3 | `wealth-transfer-succession` | | `private-wealth-management` | New pathway |
| 30.1 | 41.1 | `stablecoin-tokenisation` | `digital-assets-prediction-markets` | `digital-assets-prediction-markets` | Retain unchanged |
| 30.2 | 41.2 | `crypto-perpetuals` | `digital-assets-prediction-markets` | `digital-assets-prediction-markets` | Retain; prose references converted to route keys |
| 30.3 | 41.3 | `stablecoin-pegs-runs` | `digital-assets-prediction-markets` | `digital-assets-prediction-markets` | Retain; prose references converted to route keys |
| 30.4 | 41.4 | `crypto-options-numeraire` | `digital-assets-prediction-markets` | `digital-assets-prediction-markets` | Retain unchanged |
| 30.5 | 41.5 | `crypto-leverage-liquidations` | `digital-assets-prediction-markets` | `digital-assets-prediction-markets` | Retain; prose references converted to route keys |
| 30.6 | 41.6 | `crypto-option-markets` | `digital-assets-prediction-markets` | `digital-assets-prediction-markets` | Retain; prose references converted to route keys |
| 31.1 | 42.1 | `crypto-price-discovery` | `crypto-spot-markets` | `crypto-spot-markets` | Retain; prose references converted to route keys |
| 31.2 | 42.2 | `crypto-exchange-market-quality` | `crypto-spot-markets` | `crypto-spot-markets` | Retain unchanged |
| 31.3 | 42.3 | `crypto-valuation-adoption` | `crypto-spot-markets` | `crypto-spot-markets` | Retain unchanged |
| 31.4 | 42.4 | `crypto-investors-etfs` | `crypto-spot-markets` | `crypto-spot-markets` | Retain; prose references converted to route keys |
| 31.5 | 42.5 | `crypto-exchange-failures-regulation` | `crypto-spot-markets` | `crypto-spot-markets` | Retain; prose references converted to route keys |
| 31.6 | 42.6 | `crypto-return-dynamics` | `crypto-spot-markets` | `crypto-spot-markets` | Retain; prose references converted to route keys |
| 32.1 | 43.1 | `amm-lending` | `onchain-protocols` | `onchain-protocols` | Retain unchanged |
| 32.2 | 43.2 | `mev-block-building` | `onchain-protocols` | `onchain-protocols` | Retain unchanged |
| 32.3 | 43.3 | `staking-restaking` | `onchain-protocols` | `onchain-protocols` | Retain unchanged |
| 32.4 | 43.4 | `defi-lending-liquidations` | `onchain-protocols` | `onchain-protocols` | Retain; prose references converted to route keys |
| 32.5 | 43.5 | `onchain-solvers-execution` | `onchain-protocols` | `onchain-protocols` | Retain; prose references converted to route keys |
| 32.6 | 43.6 | `protocol-risk-governance` | `onchain-protocols` | `onchain-protocols` | Retain; prose references converted to route keys |
| 32.7 | 43.7 | `crypto-signals` | `onchain-protocols` | `onchain-protocols` | Retain; retired-overview prerequisite replaced by `return-measurement` |
| 33.1 | 44.1 | `fractional-shares-contracts` | `tokenised-fractional-assets` | `tokenised-fractional-assets` | Retain unchanged |
| 33.2 | 44.2 | `tokenised-securities` | `tokenised-fractional-assets` | `tokenised-fractional-assets` | Retain; prose references converted to route keys |
| 33.3 | 44.3 | `tokenised-real-assets` | `tokenised-fractional-assets` | `tokenised-fractional-assets` | Retain; prose references converted to route keys |
| 34.1 | 45.1 | `crypto-dealer-rfq` | `crypto-market-making` | `crypto-market-making` | Retain unchanged |
| 34.2 | 45.2 | `crypto-mm-microstructure` | `crypto-market-making` | `crypto-market-making` | Retain; prose references converted to route keys |
| 34.3 | 45.3 | `token-market-makers` | `crypto-market-making` | `crypto-market-making` | Retain; prose references converted to route keys |
| 34.4 | 45.4 | `dex-liquidity-provision` | `crypto-market-making` | `crypto-market-making` | Retain; prose references converted to route keys |
| 34.5 | 45.5 | `crypto-mm-strategies` | `crypto-market-making` | `crypto-market-making` | Retain; prose references converted to route keys |
| 35.1 | 46.1 | `crypto-cross-section` | `crypto-trading-strategies` | `crypto-trading-strategies` | Retain; prose references converted to route keys |
| 35.2 | 46.2 | `crypto-trend-technical` | `crypto-trading-strategies` | `crypto-trading-strategies` | Retain; prose references converted to route keys |
| 35.3 | 46.3 | `crypto-stat-arb` | `crypto-trading-strategies` | `crypto-trading-strategies` | Retain; prose references converted to route keys |
| 35.4 | 46.4 | `crypto-ml-prediction` | `crypto-trading-strategies` | `crypto-trading-strategies` | Retain; prose references converted to route keys |
| 35.5 | 46.5 | `crypto-arbitrage-carry` | `crypto-trading-strategies` | `crypto-trading-strategies` | Retain; prose references converted to route keys |
| 35.6 | 46.6 | `crypto-sentiment-events` | `crypto-trading-strategies` | `crypto-trading-strategies` | Retain; prose references converted to route keys |
| 36.1 | 47.1 | `prediction-forecast-evidence` | `event-contracts-prediction-markets` | `event-contracts-prediction-markets` | Retain; retired-overview prerequisite replaced by `causal-inference` |
| 36.2 | 47.2 | `prediction-price-theory` | `event-contracts-prediction-markets` | `event-contracts-prediction-markets` | Retain; prose names its new foundations. Corrected 22 October 2026 (section 12): those foundations added to its prerequisites |
| 36.3 | 47.3 | `prediction-wagering` | `event-contracts-prediction-markets` | `event-contracts-prediction-markets` | Retain unchanged |
| 36.4 | 47.4 | `prediction-decision-markets` | `event-contracts-prediction-markets` | `event-contracts-prediction-markets` | Retain unchanged |
| 37.1 | 48.1 | `prediction-settlement` | `event-contract-venues` | `event-contract-venues` | Retain unchanged |
| 37.2 | 48.2 | `prediction-outcome-tokens` | `event-contract-venues` | `event-contract-venues` | Retain; prose references converted to route keys |
| 37.3 | 48.3 | `prediction-integrity` | `event-contract-venues` | `event-contract-venues` | Retain unchanged |
| 37.4 | 48.4 | `prediction-regulation` | `event-contract-venues` | `event-contract-venues` | Retain unchanged |
| 38.1 | 49.1 | `prediction-market-design` | `event-contract-trading` | `event-contract-trading` | Retain unchanged |
| 38.2 | 49.2 | `prediction-order-book-mm` | `event-contract-trading` | `event-contract-trading` | Retain unchanged |
| 38.3 | 49.3 | `prediction-event-derivatives` | `event-contract-trading` | `event-contract-trading` | Retain; prose references converted to route keys |
| 38.4 | 49.4 | `prediction-trading-strategies` | `event-contract-trading` | `event-contract-trading` | Retain; prose references converted to route keys |

## 12. Correction pass (22 October 2026)

An audit of the migrated guide found that some coverage claims overstated what is taught and assessed, one duplicate catalogue identity, prerequisite inconsistencies, an assessment that rewarded test shopping, imprecise bridge metadata, three validator gaps and imprecise EU version wording. The 8-Part, 49-section structure, the section order and all identifiers were kept; existing pathways were extended rather than new ones created.

### 12.1 Findings

| # | Finding | Evidence |
| --- | --- | --- |
| A1 | Index construction was not taught: `demand-flows-passive` and `etf-index-closing-execution` study demand effects and execution, not constituent selection, free float, divisors, corporate actions or price versus total-return series | Their readings and checkpoints; the catalogue held no equity-index methodology (only BCOM, VIX and other non-equity methodologies) |
| A2 | Institutional investment policy was not taught: `alm-liquidity` covers pension and insurer liability hedging and funding stress; endowment, foundation and sovereign-fund policy, governance and constraints appeared only in an optional branch (Swensen) | Its readings and checkpoint; catalogue section 6.5 already held suitable entries |
| A3 | Tranche valuation was not connected: `credit-models-default` builds a Vasicek pool-loss distribution and `synthetic-risk-transfer` allocates realised losses, with no prerequisite link and no exercise computing tranche expected losses, legs or spreads, or separating physical from risk-neutral assumptions | Both routes' prerequisites and checkpoints; existing entries `catalogue-0238` (O'Kane) and `s6-duffie` were unused for this |
| A4 | `pw-campbell-viceira-2002` duplicated `s16-r09` (same DOI, 10.1093/0198296940.001.0001); the new record also gave the print date as an online date | DOI, ISBN and title scan of all 62 additions against the catalogue; an author-and-year scan found no other duplicate |
| A5 | `bayesian-parameter-uncertainty` assessed a CAPM-centred prior that is derived only later, in `asset-pricing-theory` (Part II), and pointed forward to `high-dimensional-estimation` as help | Route prose and checkpoint; positions 13, 15 and 19 in study order (Bayesian pathway, high-dimensional estimation, asset-pricing theory) |
| A6 | `capital-budgeting-investment` required `accounting-measurement` in prose but not in `prerequisite_routes`. Checking its neighbours and the other migrated routes found the same gap in `financial-statement-forecasting` (`time-value-cash-flows`), `tax-aware-wealth-preservation` (`return-measurement`) and `prediction-price-theory` (`asset-pricing-theory`, `probability-statistical-inference`); the `corporate-finance` overview named the `asset-pricing` overview for the CAPM, which `asset-pricing-theory` teaches; `causal-inference` and `group-international-reporting` named routes without marking them optional or later | A scan of every `[[route]]` in prerequisite prose against the transitive prerequisite graph. Mentions of later or sibling routes that describe what follows or what helps ("builds on this one", "gives the baseline"), mostly inherited from the baseline, were left as they are |
| A7 | `stationarity-cointegration` required an ECM, half-life and VECM for any chosen empirical pair, whatever the unit-root and cointegration evidence, which rewards switching pairs until a test passes | Its checkpoint |
| A8 | The `route-16` bridge recorded the preceding section's title (numerical methods) as its `\nameref` text while `\ref` printed the Part numeral; `route-1` had an empty title | Guide `.aux` entries for `route-1`, `route-16` and their key aliases |
| A9 | The validator accepted (a) a part key with characters the prose parser does not read, leaving literal `[[part:...]]` text in the guide (8 occurrences in a test); (b) the deletion of an inherited `legacy_label`; (c) TeX-spaced hard-coded references such as `Part~VI`, `Section~12` and `and~3.2` | Reproduced in scratch copies: each mutation generated without error |
| A10 | The two EU records called the selected version "consolidated" although they link the original act (ELI `/oj`), and no consolidation date was identified | Catalogue records `fsa-eu-ifrs-2023-1803` and `eth-eu-market-abuse-regulation` |

### 12.2 Corrections

- **A1.** Added two catalogue entries, verified by reading the selected sections of each PDF: MSCI *Global Investable Market Indexes Methodology* (March 2026; `gr-msci-gimi-2026`) and MSCI *Index Calculation Methodology* (June 2026; `gr-msci-index-calculation-2026`), at the end of catalogue section 13 "International equity integration". `intl-equity-integration` (renamed "Equity index construction, international integration, diversification and home bias") now opens with both as required readings and its checkpoint begins with a hand-built eight-stock index: size and liquidity screens, foreign inclusion factors with MSCI's rounding rule, divisor-method levels through a split, a rights issue, a cash dividend and a replacement, and price, gross total-return and net total-return series with a stated withholding rate (the dividend treatment was corrected in section 13: the first version wrongly required all levels to stay unchanged through the dividend); the integration panel must then state which return variant it uses. Its outcome and section goal say so.
- **A2.** `alm-liquidity` (renamed "Asset-liability management, institutional investment policy and liquidity") gained six required readings from existing entries: Novy-Marx–Rauh (public pension liabilities), Brown et al. (endowment spending), Swensen (moved from branch), the IMF sovereign ALM guidance, Elkamhi–Lee (total portfolio approach) and the BIS pension-allocation paper; IFRS 17 was already required. Its checkpoint now begins with an investment-policy comparison of a defined-benefit plan, a life insurer, an endowment or foundation and a sovereign fund: objective, liability or spending rule, governance, liquidity needs and constraints, each sourced, with jurisdiction, and the allocation consequences. The liability-hedge exercise follows unchanged.
- **A3.** `synthetic-risk-transfer` now requires `credit-models-default` and two existing readings: Duffie–Singleton (section 5.2 on risk-neutral versus actual probabilities; chapters 10–11) and O'Kane (chapters 12, 13, 16 and 18). Its checkpoint adds a tranche valuation under explicit assumptions: a 100-name homogeneous pool, 40% recovery, the one-factor Gaussian model, expected losses for 0–3%, 3–7% and 7–15% tranches at three correlations, once with physical default probabilities for loss analysis and once with a risk-neutral intensity calibrated to a stated spread for the premium and protection legs and break-even spread, with the difference explained.
- **A4.** Removed `pw-campbell-viceira-2002`; `household-finance-lifecycle` now cites `s16-r09`. The `s16-r09` record keeps its inherited dates and evidence, adds the 22 October 2026 Crossref check (book and seven chapter records, ISBNs; full text not inspected), records that it absorbed the duplicate, and takes the duplicate's fuller annotation and its Advanced level.
- **A5.** The prose now states the one relation the prior needs (a zero intercept in the excess-return regression on the market) and cites Pástor (2000), already in the pathway, as the source of the model-centred prior; `asset-pricing-theory` and `high-dimensional-estimation` are named as later and not needed. The checkpoint describes the prior as that restriction. No dependency or Part order changed.
- **A6.** Added the missing `prerequisite_routes` listed in A6; `corporate-finance` now depends on `asset-pricing-theory`; the `causal-inference` mention is marked "helps" and the `group-international-reporting` one "later; not needed here". The generator's ordering check confirms every new edge points backwards.
- **A7.** The checkpoint now fixes the pair and test settings in advance, runs cointegration tests only if both series appear I(1), estimates the ECM, half-life and VECM only if a cointegrating relation is supported, accepts "cointegration not supported" as a complete empirical answer, forbids switching pairs, and moves the ECM and VECM calculations to a simulated cointegrated pair with known parameters. The outcome says the same.
- **A8.** Bridges now use a `\BridgeLabel` macro: `\ref` prints the Part that holds the first successor (intended: the old section number no longer exists, and the Part is where the bridge sits) and `\nameref` prints "<retired name> (former section)". Both key and legacy aliases keep their hyperlink anchor on the bridge; no umbrella section was recreated.
- **A9.** Part keys must match `[a-z0-9-]+`, and prose rendering stops on any `[[` left unparsed; the union of live and retired legacy labels must be exactly `route-1` … `route-38` (the numbered scheme is closed; section 13 tightens this to each label's original overview key); the bare-reference pattern accepts a TeX tie (`~`) as well as a space.
- **A10.** Both records now say the link is the original act and list, from Publications Office metadata, the amending regulations (nine for 2023/1803, ending with 2026/338; five for the Market Abuse Regulation) and the latest consolidated version (CELEX 02023R1803-20260308 of 8 March 2026; 02014R0596-20260605 of 5 June 2026), stating that no text was read. `financial-reporting-statements` tells the reader to use the current consolidated version.

### 12.3 Commands and results

- Validator gaps reproduced before the fix and re-run after it, each on a scratch copy of the sources: part key `portfolio_financing_execution` (before: generated, 8 literal tokens; after: stops), deletion of `route-20` (before: generated; after: stops naming `route-20`), `Part~VI` and `Section~12 … and~3.2` (before: generated; after: stops naming them). An unmodified copy and the HTML-link mode (`catalogue_link_target: html`) generate.
- Build, in the README's order: `latexmk -pdf institutional_quantitative_finance_reading_list.tex`; `python3 refresh_views.py` ("Refreshed 49 overview routes and 222 specialist pathways, 2684 selected readings, 760 extended notes and 3956 recency records."); `latexmk -pdf institutional_quantitative_finance_learning_guide.tex`. A second `refresh_views.py` run reproduces the guide source, HTML and JSON byte for byte.
- Structure: 8 Parts with 7, 5, 13, 4, 7, 4, 6 and 3 sections (49 overviews); 222 pathways, all 203 baseline keys present, 19 new; 36 live legacy labels and 2 on bridges, `route-1` to `route-38` complete. Catalogue: 3,956 entries, all identifiers unique, 63 added since baseline and none removed; 3,956 version records, 760 extended notes.
- Logs: catalogue 0 undefined references, 0 multiply defined labels, 20 overfull boxes (unchanged); guide 0, 0 and 0. Guide 345 pages, catalogue 561.
- Links: all 3,905 catalogue links in the guide source (3,425 distinct) resolve to named destinations in the catalogue PDF, and every printed catalogue page number equals its destination's page; every link annotation in the built guide resolves except the deliberate whole-file link to the catalogue's first page. `route-1`, `route-16`, `route-common-toolkit` and `route-empirical-causal-research` resolve in the `.aux` to their Part numeral and "(former section)" names.
- Pages inspected (Ghostscript, 70 dpi): both whole-guide DAG pages; the Part I and Part II openers with their bridges; the international-equity overview, section DAG and pathway (pp. 158–160); the securitised-credit section DAG, which now lists `credit-models-default` under "Bring these foundations with you", and the synthetic-risk-transfer pathway (pp. 106, 109–110); the funding section DAG and the ALM pathway (pp. 181, 184–185); the Bayesian pathway (p. 35); the volatility pathway (p. 32). PDF bookmarks list the study method, the DAG and Parts I–VIII at the top level and carry the renamed pathways.
- Audit counts, recomputed from the final files: 3,057 entries with a new source inspection, 573 with inherited evidence, 326 not established; 2,712 entries linked by DOI and 2,730 version records saying full text was not inspected. The figures first recorded for the 3,955-entry catalogue (2,715 and 2,736) did not match this method, which reproduces the baseline's 2,672 and 2,683; they are replaced.

### 12.4 Remaining limitations

See section 10. In short: the new methodology and tranche readings were read only to the extent recorded; the exercises use stated synthetic or public inputs; the EU texts were identified from metadata only; and prose mentions of later or sibling routes that describe what follows, rather than what is required, were not converted into prerequisites.

## 13. Final correction pass (22 October 2026)

A narrow pass on three points from a further review. Structure, identifiers, catalogue records and the section 12 corrections are unchanged except as stated.

### 13.1 Findings

| # | Finding | Evidence |
| --- | --- | --- |
| B1 | The `intl-equity-integration` checkpoint treated a cash dividend as a maintenance event: it required the index level not to jump through a split, a rights issue, a cash dividend and a constituent replacement, and asked for price, gross and net total-return series as if all stayed level. An ordinary dividend is a return: the price index falls ex-dividend and only the total-return indices reinvest it | Checkpoint and outcome text. The MSCI *Index Calculation Methodology* (June 2026), section 2.2 (pages 27–28), states that regular cash dividends are not considered in the price indexes and are reinvested on the ex-date in the daily total-return indexes, whatever their size, while special cash dividends of 5% or more of the price are applied through a price adjustment factor to the price, gross and net indexes |
| B2 | The `synthetic-risk-transfer` checkpoint asked learners to explain why correlation moves equity and senior tranche values in opposite directions. The 7–15% tranche need not behave like a remote senior tranche | Reproduced counterexample below |
| B3 | The validator checked that `route-1` … `route-38` all exist, so swapping two labels between retained overview keys passed | Reproduced: swapping `route-2` and `route-3` between `systematic-equities` and `multi-asset-systematic-macro` generated without error under the set-only check |

### 13.2 Corrections

- **B1.** The checkpoint now separates maintenance from returns. A split, a rights issue and a constituent replacement are processed with the divisor and shown to leave the level unchanged when valued at the adjustment prices (the theoretical ex-rights price for the rights issue). An ordinary cash dividend leaves the price-index divisor unchanged, so the price index falls with the ex-dividend price; the dividend is reinvested on the ex-date in a gross total-return index (full dividend) and a net total-return index (less withholding at a stated rate), as in MSCI's daily total-return indexes, and the learner says how MSCI treats a special dividend of 5% or more instead. The checkpoint includes a check case. The outcome says the same.
- **B2.** The final instruction now asks for each tranche's expected loss and value at each correlation and an explanation of the sensitivity found at the learner's own default probability, recovery and correlations. It warns that the 7–15% tranche may move in the same direction as the equity tranche, or non-monotonically. The separation of physical-measure loss analysis from risk-neutral pricing, and of expected tranche losses from premium and protection legs and the break-even spread, is unchanged.
- **B3.** `refresh_views.py` now holds the 38 overview-key-to-label pairs taken from `learning_routes.json` at commit `343d145909ba5384202b50604bf5ebe7e5b6ed86`, including `common-toolkit` → `route-1` and `empirical-causal-research` → `route-16` on the retired bridges. Validation requires the live and retired labels to match that mapping exactly. New overviews without labels are unaffected.

### 13.3 Verification

- Dividend check case, computed directly: a stock at 100 pays an ordinary dividend of 2 and trades at 98 ex-dividend, with no other price change; with bases of 100 and 15% withholding the price index is 100 × 98/100 = 98, the gross total-return index 100 × (98 + 2)/100 = 100 and the net total-return index 100 × (98 + 2 × 0.85)/100 = 99.7. These figures appear in the generated checkpoint.
- Tranche counterexample, by finite-pool conditional binomial integration over the Gaussian factor (100 equal exposures, 40% recovery, five-year default probability 20%, tranche loss min(max(L − a, 0), d − a), 4,001-point grid on ±10 standard deviations). Expected losses in pool-notional units at asset correlations of 10% and 50%: 0–3% tranche 0.0297606361 and 0.0233146034; 3–7% tranche 0.0358173276 and 0.0230565710; 7–15% tranche 0.0417213666 and 0.0313597106. All three tranches' expected losses fall as correlation rises, so the 7–15% tranche moves in the same direction as the equity tranche here. This is a synthetic model check, not empirical evidence or a general pricing result.
- Validator regressions on scratch copies: swapping `route-2` and `route-3` between two retained overviews now stops naming both keys (the previous set-only check accepted it); swapping `route-16` on the retired bridge with `route-17` stops; deleting `route-20`, a part key with an underscore and `Part~VI` still stop; an unmodified copy and the HTML-link mode generate.
- Build, in the README's order: catalogue `latexmk`; `python3 refresh_views.py` ("Refreshed 49 overview routes and 222 specialist pathways, 2684 selected readings, 760 extended notes and 3956 recency records."); guide `latexmk`. A second generator run reproduces the guide source, HTML and JSON byte for byte.
- Structure: Parts, sections and pathway order identical to the section 12 state; 8 Parts (7, 5, 13, 4, 7, 4, 6, 3), 49 overviews, 222 pathways with all 203 baseline keys; legacy mapping equal to the baseline's.
- Logs: catalogue 0 undefined references, 0 multiply defined labels, 20 overfull boxes (unchanged); guide 0, 0 and 0; guide 345 pages. Links: all 3,905 catalogue links (3,425 distinct) resolve to named destinations and every printed page number matches; the only link annotation without a named destination is the deliberate whole-file link to the catalogue.
- Pages inspected (Ghostscript, 80 dpi): the international-equity pathway and its checkpoint (pp. 159, 161) and the synthetic-risk-transfer pathway and checkpoint (pp. 109–110).

### 13.4 Remaining limitations

Unchanged from sections 10 and 12.4. The dividend exercise follows MSCI's conventions as read in the selected sections; other providers' conventions (for example S&P Dow Jones Indices, whose site refused automated access) were not checked. The tranche check is one synthetic configuration.
