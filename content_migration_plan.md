# Content migration plan

Status: complete. Stages M0–M5 were executed on 22 October 2026, followed the same
day by a closeout of three audit findings (section 8.5); the compendium changes are
staged and uncommitted for review. Section 8 records the commands and results and
section 9 the remaining content gaps. The complete disposition ledger is
[content_migration_ledger.md](content_migration_ledger.md).

Prepared: 22 October 2026. Owner: repository maintainer. Audience: the maintainer and
the implementer reorganising the compendium.

The documentation cleanup was committed as `0c5394d` before this file was created.
The structural audit describes the compendium at `80b0fc5`; that structure and its
697 typed entries are unchanged by the cleanup.

## 1. Outcome and scope

Organise the compendium into the eight Parts and 49 sections of the learning guide,
in the guide's order. The guide itself was revised first (commit `6c7734e`, see
section 1.1): it now has the target structure, with the former combined
quantitative-methods overview divided into seven sections, the empirical/causal
overview divided into two, and professional ethics, financial statement analysis,
corporate finance and private wealth management as guide sections. The compendium
therefore mirrors `learning_parts[*].routes` directly. Within each section, group
related material into subsections and use subsubsections where a substantial
subject needs a further division.

Section counts by Part are 7, 5, 13, 4, 7, 4, 6 and 3. A section appears in the
compiled reference only when it has substantive content; a Part prints only when
one of its sections does. The complete declared structure and outstanding subject
gaps remain visible in the declaration, the overview notes and the ledger.

This is a structural migration of existing material. It includes headings, input
order, canonical ownership, navigation, coverage ownership, and the checkers needed
to preserve the structure. New explanations, source research, numerical changes and
completion of unwritten pathways are separate work.

### 1.1 Authorities and invariants

- [Learning routes](guide/learning_routes.json) define the Parts, their sections and
  their order through `learning_parts[*].routes`. The compendium declaration must
  equal them: Part keys, titles and order, and each Part's sections in order. Do
  not derive presentation order from the top-level `routes` array: its storage order
  differs. Do not collapse the structure back to the earlier 7 Parts or 38 sections
  for alignment checks.
- Each route's `section_goals`, `specialist_order` and `prerequisite_routes` inform
  subsection grouping and dependencies. Every one of the guide's 222 specialist
  pathways has a mapped destination or an explicit content gap in the ledger; a
  pathway need not be a separate heading, and a new guide pathway does not authorise
  a new compendium explanation.
- The guide is pinned at `6c7734ed49f1c242908b86a57c4f5d1f0e349ec0` (22 October 2026,
  "Reorganise the learning guide into eight parts and 49 sections"), as recorded in
  [README.md](README.md). Route-file `as_of` 2026-10-22, schema version 3; SHA-256
  `f0b682b38ac871567a98b74249e81209d11609c8a5d7743a710b1c6f83cb74d3`. It has 8 Parts,
  49 overview sections, 222 specialist pathways (all 203 earlier pathway IDs
  preserved, 19 added) and 3,956 catalogue entries.
- Historical baseline: when this plan was drafted the pin was
  `343d145909ba5384202b50604bf5ebe7e5b6ed86`, with route-file edition 14 October 2026
  and SHA-256 `a2aeb67ca658ddf617e803d5bdd8c5030faa2e6d606762765d827503793d1268`
  (7 Parts, 38 overview sections, 203 pathways, 3,893 catalogue entries). Notes and
  review records dated before 22 October 2026 refer to that edition.
- The guide's `retired_overviews` keep the identities of the two divided overviews,
  `common-toolkit` and `empirical-causal-research`, with their successor sections.
  They are compatibility navigation only, never compendium sections.
- The compendium master remains the single declaration of its structure, checked
  against the pinned guide. There is no second independently maintained ordering or
  guide-origin registry. The coverage roadmap describes navigation and
  prerequisites, not a competing declaration.
- Preserve all 697 typed entry labels, their types, citations, source locators,
  assumptions, mathematical content and evidence associations. Chapter and printed
  entry numbers may change; stable labels and links must continue to resolve.
- Preserve the 40 section keys shared with the earlier structure, including legacy
  names such as `rates-credit-mortgages` and `digital-assets-prediction-markets`.
  `common-toolkit` is no longer a compiled section key; entry labels are unchanged.
- Each entry has one canonical compiled home. Applications and specialist pathway
  notes may link to it from multiple places; do not duplicate the entry text.
- A move does not establish new source verification, coverage, study or mastery.
  Preserve existing evidence dates and the distinctions between these states.

## 2. Audit baseline

Historical: the state at `80b0fc5`/`0c5394d` with the guide at `343d145`, before
either migration. The counts were re-parsed from the checkout before editing and
reconciled exactly (ledger section 1).

| Measure | Observed state |
| --- | --- |
| Learning guide | 7 Parts, 38 overview sections, 203 specialist pathways |
| Compendium declaration | 42 keys: all 38 guide keys in order, plus 4 additions |
| Compiled subject wrappers | 28 present; 14 declared keys without wrappers |
| Topic source files | 169 |
| Main-content heading levels | 178 `\section` headings; no `\subsection` or `\subsubsection` headings |
| Part divisions | None |
| Typed entries | 697 |
| Pathway notes | 72; 11 populated sections lack their matching overview note |
| Objective coverage registry | 449 objectives in 108 topics |
| External-outline crosswalk | 1,030 items in 203 modules |

Both structural checkers passed. The objective and outline counts describe that
registry, not coverage of the guide's specialist pathways (203 then, 222 now). A populated wrapper
also does not imply that all of its guide subjects are covered.

### 2.1 Findings and remedies

| Finding | Evidence | Remedy |
| --- | --- | --- |
| Part hierarchy is absent | [Master declaration](compendium/compendium.tex) is one flat list | Declare and render the guide's eight Parts (done: `\qfpart`) |
| Two overview titles conceal distinct subjects | `common-toolkit` combines mathematical, statistical and numerical disciplines; `empirical-causal-research` combines pricing tests with causal designs | Resolved by the guide's own division into nine sections; the compendium follows it |
| Large chapters lack grouping | Portfolio construction has 85 entries; microstructure 72; execution 59; financial statements 56 | Group by subject and introduce meaningful lower-level headings |
| Some applications precede their foundations | [ML](compendium/ml-alternative-data/section.tex) introduces specialised data transforms and execution control before learning methods; [macro](compendium/multi-asset-systematic-macro/section.tex) starts with strategies before economic foundations | Reorder introductions and general concepts before applications |
| Topic ownership diverges from the guide | xVA under corporate credit; general estimation under portfolio risk; AMMs and lending in the crypto overview | Perform the explicit relocations in section 5 |
| Additional sections interrupt learning dependencies | Financial statements and corporate finance follow corporate credit; private wealth interrupts financing and execution | Done, following the guide's order |
| Missing wrappers hide existing relevant content | Empirical asset pricing, on-chain protocols, crypto spot and crypto strategies lack wrappers | Populate those homes from existing entries where the mapping supports it |
| Existing checks permit future drift | [Section loader](tools/check_compendium.py) validates the compendium declaration against itself | Done: direct guide comparison, overview, bridge, heading-level and single-inclusion checks |

The 11 populated sections without their matching `notes/pathways/<key>.md` overview
are `research-engineering-validation`, `ml-alternative-data`,
`government-bond-markets`, `corporate-credit-capital`, `volatility-trading-premia`,
`portfolio-risk-financing`, `energy-commodities`, `physical-commodity-markets`,
`commodity-investing-premia`, `power-gas-environmental`, and
`digital-assets-prediction-markets`. Existing specialist notes remain useful; they
do not replace the section overview required by the compendium conventions.

## 3. Hierarchy and navigation conventions

### 3.1 Reader-facing levels

| Logical level | Existing book-class mechanism | Purpose |
| --- | --- | --- |
| Part | `\part` | One of the guide's eight Parts |
| Section | `\chapter` in `<key>/section.tex` | One of the guide's 49 overview sections |
| Subsection | `\section` | A coherent subject group |
| Subsubsection | `\subsection` | A substantial division within that group |
| Optional deeper division | `\subsubsection` | Only when a further division materially improves navigation |
| Concept, method or model | Existing typed entry environment | The substantive explanation and evidence |

Keep `extbook` and the existing chapter-based entry counter. The logical use of
"Section" does not require replacing chapters with LaTeX sections or rewriting the
entry numbering system. Use global chapter numbering; section keys, which are the
guide's own, rather than printed numbers provide correspondence with the guide.

Use the printed contents for Parts, Sections and Subsections (`tocdepth` 1). PDF
bookmarks expose Subsubsections and the deeper divisions as well (`bookmarksdepth` 3),
and the back matter starts at the bookmark root. Keep notation in the front matter and sources outside the catalogue in
the back matter. Avoid an empty Part title page when every section in that Part is
unwritten; its intended position remains in the declared roadmap.

### 3.2 Prerequisites and grouping

Use foundational subsections before specialised applications. Follow the guide's
specialist order where subjects retain their original grouping, and preserve the
guide's prerequisite edges; a regrouping may change the order of independent
pathways.
Insert additional foundations ahead of the material they support. Do not turn
source-book chapters or every individual source file into peer headings.

The guide contains branches and shared prerequisites, so a single reading order
cannot remove every forward reference. Link the relevant earlier method or later
application explicitly instead of duplicating it. Examples include restructuring
and equity valuation, foreign-currency reporting and FX mechanics, and ML execution
policies and the later execution benchmarks.

Create further heading depth when it separates several substantial concepts. Do
not create a heading layer solely to hold one typed entry or an unwritten pathway.
Unwritten topics belong in the coverage/navigation record until content exists.

### 3.3 Subject naming

Section titles name the discipline, financial object or analytical task. Avoid
standalone containers such as "toolkit", "foundations", "advanced topics" or
"miscellaneous", and role labels such as "allocator" or "investor" when the
section actually teaches a set of asset classes and methods. Broad Part names can
describe a stage of learning; the sections beneath them must identify its subjects.

For example, use "Private equity, private credit and fund structures" and "Real
estate, infrastructure and natural-resource investments" for the existing private
capital and real-asset sections. Their stable keys need not change. Expand "ML" to
"Machine learning" in the displayed section title.

### 3.4 Retired guide overviews and compatibility

Historical crosswalk. When this plan was drafted the guide had one overview for each
of these blocks and the plan expanded them inside the compendium. The guide has
since made the same division itself, recording the old identities in
`retired_overviews`. The table is kept as migration and compatibility information;
it is no longer an alignment rule, and no expansion metadata or collapse step is
needed.

| Retired guide overview | Successor sections (in guide order) |
| --- | --- |
| `common-toolkit` | `financial-mathematics`, `probability-statistics`, `regression-time-series`, `stochastic-processes-calculus`, `bayesian-inference`, `high-dimensional-statistics`, `numerical-optimisation` |
| `empirical-causal-research` | `asset-pricing`, `causal-inference` |

Compatibility is navigational:

- `notes/pathways/common-toolkit.md` is a bridge that names each successor section
  and keeps the earlier chapter's history; `notes/pathways/empirical-causal-research.md`
  is a bridge for an overview that never had a compendium chapter. The checker
  accepts retired keys as note names, requires each such note to name every
  successor from `retired_overviews`, and rejects a retired key declared as a section.
- The old compiled chapter label `common-toolkit` had no incoming `\ref` or
  `\hyperref` in the compiled sources and no external link to a PDF destination in
  the repository, so it was removed with the wrapper rather than kept as a phantom
  label. Entry labels, which are what notes and coverage records cite, are unchanged.
- Each populated successor section has its own overview note; a bridge does not
  replace it.

Pathway homes within the former quantitative-methods block, now fixed by the guide:

| Guide specialist pathway | Section |
| --- | --- |
| `time-value-cash-flows`, `return-measurement` (new) | `financial-mathematics` |
| `probability-statistical-inference`, `heavy-tails-extremes` (new) | `probability-statistics` |
| `regression-econometrics` (new), `stationarity-cointegration` (new), `time-series-volatility` | `regression-time-series` |
| `stochastic-calculus-control` | `stochastic-processes-calculus` |
| `bayesian-parameter-uncertainty` | `bayesian-inference` |
| `high-dimensional-estimation` | `high-dimensional-statistics` |
| `numerical-methods-optimisation` | `numerical-optimisation` |
| `asset-pricing-theory` (new), `standard-errors-inference`, `empirical-asset-pricing`, `return-predictability`, `event-studies` | `asset-pricing` |
| `causal-research-designs`, `causal-policy-evaluation`, `controlled-experiments` | `causal-inference` |

Robust-inference methods are introduced before the asset-pricing tests that require
them. The causal section links those methods rather than duplicating them. An
abnormal-return event study does not by itself establish a causal effect: the
pricing section owns return estimation and the causal section owns identification
and counterfactual assumptions.

### 3.5 Parts

The compendium's Parts are the guide's, with the same keys and titles. The earlier
draft mapped two compendium Parts onto the guide's first Part (`foundations`); the
guide now has both Parts, so that mapping and its separate boundary check are
unnecessary. The direct comparison already rejects a section in the wrong Part,
including across the Part I/II boundary.

| Part | Key | Sections |
| --- | --- | ---: |
| I — Financial mathematics, statistics and numerical methods | `mathematics-statistics-numerics` | 7 |
| II — Empirical finance, machine learning and research governance | `empirical-finance-research-governance` | 5 |
| III — Public markets and pricing | `public-markets` | 13 |
| IV — Portfolio financing and execution | `portfolio-financing-execution` | 4 |
| V — Energy and commodities | `energy-commodities` | 7 |
| VI — Private capital, real assets and insurance | `private-real-insurance` | 4 |
| VII — Digital assets | `digital-assets` | 6 |
| VIII — Event contracts and prediction markets | `event-contracts` | 3 |

## 4. Target Part / Section / Subsection structure

The tables list the complete target sequence, which is also the guide's. Subsections
read left to right and describe the destination design, not a claim that all of
their content has been written. *Current state* is the state after the migration:
`Populated` sections have a wrapper; `Unpopulated` means the section has no
wrapper, not that no related entry exists elsewhere. The headings actually
implemented for existing material are listed in the ledger (section 3) and follow
these designs where material exists. Earlier drafts marked four sections as
additions outside the guide; all four are now guide sections.

### Part I — Financial mathematics, statistics and numerical methods

| Section key and title | Proposed subsections | Current state |
| --- | --- | --- |
| `financial-mathematics` — Financial mathematics and return measurement | Discounting and compounding; present value and cash-flow additivity; required returns; holding-period, time-weighted and money-weighted returns | Populated |
| `probability-statistics` — Probability and statistical inference | Descriptive statistics; random variables and distributions; conditional moments and dependence; sampling and estimation; hypothesis tests; resampling; heavy tails and extreme values | Populated |
| `regression-time-series` — Regression and time-series econometrics | Linear and multiple regression; diagnostics and misspecification; stationarity and unit roots; autoregression and cointegration; volatility models; forecast evaluation and structural breaks | Populated |
| `stochastic-processes-calculus` — Stochastic processes and calculus | Brownian motion and quadratic variation; stochastic integration and Itô's lemma; stochastic differential equations; changes of measure and pricing equations; continuous-time control | Populated |
| `bayesian-inference` — Bayesian inference and parameter uncertainty | Priors, likelihoods and posterior updating; posterior prediction; hierarchical models and shrinkage; parameter uncertainty in financial decisions | Populated |
| `high-dimensional-statistics` — High-dimensional statistics and covariance estimation | Covariance estimation; random-matrix noise; regularisation and shrinkage; high-dimensional factor estimation | Populated |
| `numerical-optimisation` — Numerical methods and optimisation | Monte Carlo integration and variance reduction; discretisation error; root finding and linear algebra; constrained and convex optimisation | Populated |

Return measurement precedes return statistics; probability and inference precede
econometric, stochastic and Bayesian methods; stochastic calculus precedes the
numerical pricing methods that use it.

Frequentist regularisation and covariance shrinkage belong to high-dimensional
statistics; posterior shrinkage and prior uncertainty belong to Bayesian inference.
General numerical algorithms belong to numerical methods; asset-specific pricing
and portfolio implementations remain in their application sections. These
boundaries keep the new sections from duplicating one another.

### Part II — Empirical finance, machine learning and research governance

| Section key and title | Proposed subsections | Current state |
| --- | --- | --- |
| `asset-pricing` — Asset pricing theory and empirical tests | Systematic risk, CAPM and factor pricing; robust standard errors and identification limits; factor-model estimation and pricing tests; return predictability; abnormal returns and event studies | Populated |
| `causal-inference` — Causal inference and experimental design | Causal estimands and identification; difference-in-differences; synthetic control; regression discontinuity; causal ML and policy evaluation; randomised and switchback experiments; sequential monitoring | Unpopulated |
| `research-engineering-validation` — Research engineering, data provenance and model validation | Strategy anatomy and research specification; backtest inference; point-in-time data; model governance; reproducible research and production lifecycle | Populated |
| `professional-ethics` — Professional ethics | Ethical reasoning; code and enforcement; professional duties; conduct cases; asset-manager responsibilities | Populated |
| `ml-alternative-data` — Machine learning and alternative data | Data types, structures and workflow; learning foundations and validation; return prediction; labels and financial evaluation; deep forecasting; reinforcement learning; text and alternative data | Populated |

Part I supplies the mathematical prerequisites for asset pricing and causal
inference. Professional ethics stays adjacent to research governance. Within
machine learning, distinguish the initial workflow overview from its later use in
model evaluation.

### Part III — Public markets and pricing

| Section key and title | Proposed subsections | Current state |
| --- | --- | --- |
| `rates-credit-mortgages` — Rates: yield curves, term premia and derivatives | Bond and discounting foundations; curves and rate risk; rate derivatives; monetary policy; bond premia and strategies; inflation-linked instruments | Populated |
| `government-bond-markets` — Government bond markets and sovereign debt | Issuance and auctions; market functioning; sovereign credit and restructuring; municipal debt; developed-market conventions | Populated |
| `financial-statement-analysis` — Financial statement analysis | Reporting and the statements; accounting measurement; group and international reporting; analytical ratios and reporting quality; forecasting and integrated cases | Populated |
| `corporate-finance` — Corporate finance | Ownership and business models; working capital; capital investment; capital structure and funding costs; payout; restructuring | Populated |
| `corporate-credit-capital` — Corporate credit, hybrids and labelled bonds | Credit analysis and default models; bonds and CDS; credit portfolios; bank capital; hybrids and preferred shares; labelled bonds | Populated |
| `securitised-structured-credit` — Securitised and structured credit | Structures and recourse; securitisation and waterfalls; default dependence and tranche valuation; risk transfer; workouts | Populated |
| `systematic-equities` — Systematic equities | Securities and fundamental analysis; valuation and accounting signals; factor premia; statistical arbitrage and flows; signal combination and portfolios; corporate events | Populated |
| `volatility-options` — Option pricing, volatility models and hedging | Contract and payoff foundations; forward commitments; option valuation; volatility models and surfaces; hedging and option strategies; numerical pricing; exotics and structured products | Populated |
| `volatility-trading-premia` — Volatility trading, option premia and implied information | Option returns and dealer effects; implied distributions; single-stock options; VIX, variance, correlation and dividends; short-dated options | Populated |
| `multi-asset-systematic-macro` — Multi-asset and systematic macro | Economic foundations; macro data and policy; asset valuation and expectations; cross-asset strategies; regimes, announcements and nowcasting | Populated |
| `currency-markets` — Currency markets: exchange rates, premia and hedging | Quotation and parity; exchange-rate determination; instruments and settlement; currency premia; funding basis; volatility and hedging; emerging currencies | Populated |
| `international-equity-markets` — International and emerging equity markets | Index construction and instruments; integration and diversification; global factors; emerging markets; cross-listings and market access | Populated |
| `global-regional-markets` — Global and regional markets: capital flows, local bonds and market access | Capital flows; local-currency bonds; regional access and settlement | Unpopulated |

Financial statements and corporate finance sit between government bonds and
corporate credit, as in the guide. That introduces issuer analysis before
creditworthiness. Move pricing foundations from
portfolio construction to Part II so cost-of-capital discussions have an earlier
home for their asset-pricing concepts. Keep sector-specific portfolio applications
with their asset class and cross-reference general construction methods.

### Part IV — Portfolio financing and execution

| Section key and title | Proposed subsections | Current state |
| --- | --- | --- |
| `portfolio-construction-risk` — Portfolio construction and risk | Investment process and constraints; portfolio foundations; allocation and construction; risk and overlays; performance and manager evaluation; institutional portfolios | Populated |
| `portfolio-risk-financing` — Funding, collateral and liquidity | Money markets and repo; securities lending; funding liquidity and crowding; collateral and xVA; asset-liability management; synthetic financing | Populated |
| `execution-market-making` — Market microstructure and market making | Markets, trading systems and orders; order flow and dealer models; LOB learning; options and fixed-income dealing; market simulation; FX dealing; HFT and market design | Populated |
| `execution-trading-costs` — Execution, trading costs and market structure | Benchmarks and costs; price impact; optimal execution and scheduling; algorithms and routing; TCA and execution quality; asset-specific execution; regulation and governance | Populated |

General strategic asset allocation belongs in portfolio construction. Macro retains
capital-market expectations as an input to allocation. Introduce money-market
mechanics before funding stress, and benchmark/impact concepts before execution
policies. Preserve distinct treatments of dealer behaviour, portfolio cost inputs
and execution algorithms, linked through their shared concepts.

### Part V — Energy and commodities

| Section key and title | Proposed subsections | Current state |
| --- | --- | --- |
| `energy-commodities` — Commodity futures: storage, curves, hedging and options | Storage and inventories; curve models; hedging; commodity and real options | Populated |
| `commodity-spot-markets` — Commodity spot markets | Benchmarks; spatial arbitrage; price cycles; stabilisation and trade policy; long-run prices | Unpopulated |
| `physical-commodity-markets` — Physical commodity markets | Contract design and delivery; metals; agriculture; oil and products; information and price discovery; freight; trading finance | Populated |
| `commodity-investing-premia` — Commodity risk premia and investing | Economic premia; factor strategies; financialisation; portfolio allocation; indices and investment products | Populated |
| `oil-shocks-macro` — Oil-price shocks, forecasting and the macroeconomy | Shock identification; forecasting; inflation and policy; asset-price transmission | Unpopulated |
| `power-gas-environmental` — Gas and power markets | Gas hubs; storage and LNG; electricity networks; market design; renewables and PPAs; forecasting; short-term flexibility | Populated |
| `environmental-markets` — Environmental markets | Compliance systems; allowance pricing and derivatives; pass-through and leakage; voluntary credits; environmental certificates | Unpopulated |

### Part VI — Private capital, real assets and insurance

| Section key and title | Proposed subsections | Current state |
| --- | --- | --- |
| `private-capital-allocator` — Private equity, private credit and fund structures | Structures and performance; private equity and venture capital; private credit and workouts; receivables and contractual rights; fund liquidity | Populated |
| `real-asset-investor` — Real estate, infrastructure and natural-resource investments | Property; infrastructure; equipment leasing; natural-resource rights; collectibles | Populated |
| `insurance-climate-risk` — Insurance and climate-linked risk | Catastrophe and cyber risk; mortality and longevity; weather derivatives; alternative insurance capital | Unpopulated |
| `private-wealth-management` — Private wealth management | Client circumstances; wealth and investment planning; preservation and concentrated exposures; succession and transfer | Populated |

Private wealth closes this Part as a client application of public portfolios,
private assets and insurance. Its current position between financing and
microstructure is removed. Cross-links to the earlier portfolio and ethics sections
provide the common investment and conduct framework.

### Part VII — Digital assets

| Section key and title | Proposed subsections | Current state |
| --- | --- | --- |
| `digital-assets-prediction-markets` — Crypto settlement, venues and derivatives | Ledger and settlement foundations; stablecoins; venues and instruments; perpetuals and options; margin and liquidation risk | Populated |
| `crypto-spot-markets` — Crypto spot markets | Price discovery; market quality; valuation; investors and access vehicles; custody and failures; return dynamics | Populated |
| `onchain-protocols` — On-chain protocols | AMMs; transaction ordering and MEV; staking; lending and liquidation; solver execution; protocol governance; on-chain evidence | Populated |
| `tokenised-fractional-assets` — Fractional and tokenised assets | Fractional ownership mechanics; tokenised securities and funds; tokenised real assets | Unpopulated |
| `crypto-market-making` — Crypto market making | Order-book dealing; venue microstructure; issuer arrangements; DEX liquidity provision; inventory strategies | Unpopulated |
| `crypto-trading-strategies` — Crypto trading strategies | Cross-sectional strategies; trend; statistical arbitrage; ML prediction; arbitrage and carry; sentiment and events | Populated |

Keep digital-asset applications in this Part and link their general methods from
earlier Parts. Basic settlement and instrument mechanics remain in the opening
section. Protocol mechanics, investor analysis and trading evidence gain their own
canonical homes through the entry splits below.

### Part VIII — Event contracts and prediction markets

| Section key and title | Proposed subsections | Current state |
| --- | --- | --- |
| `event-contracts-prediction-markets` — Event contracts and prediction markets | Forecast evidence; price theory and beliefs; wagering markets; decision markets | Unpopulated |
| `event-contract-venues` — Event-contract venues, settlement and regulation | Resolution and settlement; outcome-token identity; market integrity; regulation | Unpopulated |
| `event-contract-trading` — Event-contract trading | Automated market makers; order-book dealing; event derivatives; strategies and sizing | Unpopulated |

### 4.1 Subsubsection examples

These are concrete groupings for the dense existing material, not a requirement to
create empty divisions everywhere.

```text
Part III — Public markets and pricing
  Section — Financial statement analysis
    Subsection — Reporting and the statements
      Subsubsection — Reporting framework
      Subsubsection — Income statement, balance sheet and cash flows
      Subsubsection — Reconciled company case
    Subsection — Accounting measurement
      Subsubsection — Inventories and long-lived assets
      Subsubsection — Leases and employee compensation
      Subsubsection — Income taxes
    Subsection — Group and international reporting
      Subsubsection — Intercorporate investments
      Subsubsection — Foreign-currency reporting
    Subsection — Analytical ratios and reporting quality
      Subsubsection — Ratios and diagnostics
      Subsubsection — Reporting quality
      Subsubsection — Banks and insurers
    Subsection — Forecasting and integrated cases
      Subsubsection — Statement modelling
      Subsubsection — Integrated analysis

Part IV — Portfolio financing and execution
  Section — Portfolio construction and risk
    Subsection — Allocation and construction
      Subsubsection — Strategic allocation and investor constraints
      Subsubsection — Rules, sizing and risk allocation
      Subsubsection — Optimisation and estimation uncertainty
      Subsubsection — Implementation and rebalancing
    Subsection — Performance and manager evaluation
      Subsubsection — Attribution and benchmarks
      Subsubsection — Appraisal and skill
      Subsubsection — Manager selection
      Subsubsection — Performance presentation standards
  Section — Market microstructure and market making
    Subsection — Order flow and dealer models
      Subsubsection — Order-flow statistics
      Subsubsection — Inventory and quoting
      Subsubsection — Information and adverse selection
      Subsubsection — Spread measurement and liquidity stress
```

## 5. Content relocation decisions

All paths in this section are relative to `compendium/`. Retain the original entry
labels. A move must update the source and destination wrappers in the same change.
Leave explanatory cross-links at the former conceptual location when useful, not a
second `\input` of the moved entry.

Implemented as specified, with the differences recorded in section 5.4. The ledger
lists every resulting file and split label.

### 5.1 Whole-file moves

| Current file | Destination section and group | Reason |
| --- | --- | --- |
| `common-toolkit/time-value.tex` | `financial-mathematics`: discounting, present value and cash-flow additivity | Introduce the measurement and valuation language used throughout the reference |
| `common-toolkit/descriptive-statistics.tex` | `probability-statistics`: descriptive statistics | Give statistical descriptions of returns a specific subject home |
| `common-toolkit/statistical-inference.tex` | `probability-statistics`: estimation and hypothesis testing | Keep statistical estimands, assumptions and testing together |
| `common-toolkit/regression.tex` | `regression-time-series`: linear regression | Introduce econometric estimation before its financial applications |
| `common-toolkit/multiple-regression.tex` | `regression-time-series`: multiple regression and diagnostics | Extend the regression sequence coherently |
| `common-toolkit/time-series-models.tex` | `regression-time-series`: time-series econometrics | Follow regression with temporal dependence, forecasting and model selection |
| `common-toolkit/stochastic-calculus.tex` | `stochastic-processes-calculus`: Brownian motion, Itô calculus and changes of measure | Separate continuous-time mathematical models from statistical estimation |
| `portfolio-construction-risk/asset-pricing-models.tex` | `asset-pricing`: pricing foundations and factor-model estimation | Introduce systematic risk, CAPM and factor pricing before issuer valuation and specialist empirical applications |
| `portfolio-construction-risk/quant-strategy-structure.tex` | `research-engineering-validation`: strategy anatomy and research specification | Establish the research object before discussing its evaluation and production lifecycle |
| `multi-asset-systematic-macro/strategic-asset-allocation.tex` | `portfolio-construction-risk`: allocation and construction | General allocation is a portfolio decision; macro supplies expected-return inputs |
| `corporate-credit-capital/counterparty-xva.tex` | `portfolio-risk-financing`: collateral and xVA | Align counterparty exposure and collateral with the guide's financing section; retain risky-bond valuation in credit |
| `ml-alternative-data/execution-control.tex` | `execution-trading-costs`: optimal execution | The existing entry develops a model-based execution benchmark; the ML section should link to it when introducing learned policies |

These destinations retain each source basename. The two figures used by moved files
moved with them (`security-market-line.tikz`, `strategystructure.tikz`); the one
script that reads a moved figure, `asset-pricing-factor-models/asset-pricing-checks.py`,
now reads its new path, and two script docstrings name the new entry files. No
numerical artefact directory was moved.

### 5.2 Entry-level splits

| Entry label(s) | Current file | Destination |
| --- | --- | --- |
| `def:conditional-moments`, `def:financial-distributions` | `common-toolkit/probability.tex` | `probability-statistics`: conditional moments and distributions |
| `meth:bayesian-updating` | `common-toolkit/probability.tex` | `bayesian-inference`: prior, likelihood, posterior and predictive probability |
| `meth:historical-simulation`, `meth:bootstrap-resampling` | `common-toolkit/simulation-methods.tex` | `probability-statistics`: empirical distributions and resampling |
| `meth:monte-carlo-simulation` | `common-toolkit/simulation-methods.tex` | `numerical-optimisation`: Monte Carlo integration, variance reduction and discretisation error |
| `def:return-measures` | `portfolio-construction-risk/performance-evaluation.tex` | `financial-mathematics`: return measurement, before return statistics; keep relative performance, skill tests and GIPS in portfolio performance |
| `meth:portfolio-covariance-estimation`, `ev:correlation-matrix-noise` | `portfolio-construction-risk/risk-models.tex` | `high-dimensional-statistics`: covariance estimation and random-matrix noise |
| `mod:garch-volatility-forecast`, `meth:volatility-forecast-loss`, `meth:structural-break-tests` | `portfolio-construction-risk/risk-models.tex` | `regression-time-series`: volatility methods, forecast evaluation and structural breaks |
| `meth:extreme-value-tail-estimation` | `portfolio-construction-risk/risk-models.tex` | `probability-statistics`: heavy tails and extreme-value estimation |
| `def:amm-pool-mechanics` | `digital-assets-prediction-markets/crypto-venues-perpetuals.tex` | `onchain-protocols`: AMMs |
| `mech:defi-lending-liquidation` | `digital-assets-prediction-markets/crypto-venues-perpetuals.tex` | `onchain-protocols`: lending and liquidation, after AMM foundations |
| `ev:crypto-dated-futures-carry` | `digital-assets-prediction-markets/crypto-venues-perpetuals.tex` | `crypto-trading-strategies`: arbitrage and carry |
| `mod:liquidity-spirals` | `digital-assets-prediction-markets/crypto-venues-perpetuals.tex` | `portfolio-risk-financing`: funding liquidity and crowding; crypto liquidation topics link to it |
| `meth:digital-asset-investment-analysis` | `digital-assets-prediction-markets/digital-asset-investing.tex` | `crypto-spot-markets`: investors, vehicles and custody |

Keep `mod:factor-risk-model` and `meth:var-es-estimation-methods` in portfolio risk,
linking the relocated estimation methods. Keep `def:distributed-ledger-applications`
in the opening crypto section, before venue mechanics. Stablecoin, perpetual-funding,
venue-risk and auto-deleveraging entries also remain in that opening section.

These moves replace one populated quantitative-methods wrapper with seven
populated subject wrappers and populate asset pricing, on-chain protocols, crypto
spot markets and crypto trading strategies. Causal inference remains declared but
unpopulated until substantive causal-method content is written. Result, verified
against the completed mapping: 38 populated sections and 11 unpopulated, with no new
typed entries. The old quantitative-methods wrapper was removed once all nine of its
inputs had moved; its guide identity survives only as the bridge note.

### 5.3 Within-section ordering and ownership

- Financial mathematics: discounting and cash flows before return measurement.
- Probability and statistics: descriptions and distributions before inference;
  historical simulation and resampling with empirical distributions; tail estimation
  after the general inferential concepts it uses.
- Regression and time-series econometrics: linear and multiple regression before
  stationarity, dynamic models, volatility forecasts and structural-break tests.
- Stochastic processes: Brownian motion before Itô calculus, stochastic differential
  equations and changes of measure; continuous-time control follows those concepts.
- Bayesian inference: posterior updating before hierarchical models and parameter
  uncertainty. Keep frequentist covariance regularisation in high-dimensional
  statistics and link the Bayesian interpretation where supported.
- High-dimensional statistics: covariance estimation and sampling noise before
  shrinkage, regularisation and factor-estimation applications.
- Numerical methods: numerical integration and error assessment before advanced
  pricing algorithms; optimisation methods before their portfolio applications.
- Asset pricing: economic pricing models before estimation; robust inference before
  factor tests, predictability and event studies. Keep general regression methods in
  econometrics and the asset-pricing application here.
- Causal inference: estimands and identification before quasi-experimental designs,
  policy evaluation and controlled experiments. Keep descriptive or predictive
  relations distinct from claims requiring a causal design.
- Research engineering: strategy specification first; group backtest inference,
  data, controls and production material rather than leaving six unrelated headings.
- ML: data types before structures; learning methods before specialist labelling
  and transformations; introduce the workflow early and link later applications.
- Financial statements: statement mechanics before the worked company case;
  measurement and group reporting before integrated analysis; ratios before
  reporting-quality diagnostics and forecasting.
- Equities: foundational analysis and valuation before signal combination and
  portfolio construction. Group the multiple valuation files beneath a common
  valuation subsection with subsubsections for their distinct methods.
- Options: instrument types and payoffs before valuation; valuation before hedging
  and strategies; numerical techniques before advanced exotic applications.
  Preserve distinct entries rather than merging superficially similar treatments.
- Macro: firms, cycles, growth and policy before strategy frameworks; retain macro
  data and capital-market expectations, with strategic allocation moved as above.
- International equities: `index-construction.tex` before `equity-indices.tex`.
- Portfolio construction: investor objectives and constraints first; portfolio
  moments and choice before allocation models; risk and implementation before
  performance assessment and institutional applications.
- Financing: money markets and lending before crowding; collateral and xVA before
  their advanced financing applications.
- Microstructure: market organisation, trading systems and order books first;
  group the nine current headings in `market-making-models.tex` by mechanism.
  Use headings within the file or split it only where that improves ownership.
- Execution: benchmarks and trade measurement before impact estimation; impact
  before scheduling and control; algorithms and routing before TCA applications
  and asset-specific implementation.
- Commodity futures: storage and curve foundations before hedging applications.
  Commodity investing: investment mechanics and premia before index products.
- Private capital and real assets: structures and valuation before allocation
  decisions, while retaining their specialist subject identity.
- Private wealth: preserve the current progression from clients to planning,
  preservation and transfer within its new Part.

### 5.4 Implementation decisions beyond sections 5.1–5.3

- `mod:liquidity-spirals` joins `portfolio-risk-financing/crowding-contagion.tex`
  after `mod:margin-liquidity-spiral`, the other Brunnermeier–Pedersen entry, rather
  than a one-entry file. Both entries stay distinct; the file heading became
  "Crowding, contagion and liquidity spirals".
- The opening crypto section is ordered as the plan's subsections: the
  distributed-ledger entry (`distributed-ledgers.tex`, split from the moved
  `digital-asset-investing.tex`), then the two stablecoin entries
  (`stablecoins.tex`, split from `crypto-venues-perpetuals.tex`), then venues,
  perpetuals and margin risk.
- `execution-market-making/market-making-models.tex` keeps its entry order. Three
  inner groups (inventory and quoting; information and adverse selection; dealer
  quotes, spread measurement and liquidity stress) are subsections, and its nine
  former headings are subsubsections. Splitting the file would not have improved
  ownership.
- Headings: a topic file that forms a group alone keeps its `\section`; files in a
  multi-file group were demoted to `\subsection` under a wrapper `\section`. Four
  headings changed text: the resampling, digital-asset investing, crowding and
  asset-pricing files (the last no longer repeats the chapter title).
- One sentence outside headings changed: the resampling introduction now links
  `meth:monte-carlo-simulation`, which moved to numerical methods.
- Chapter titles are the guide's section names; Part titles are the guide's.
- Entry order changes within sections follow section 5.3: commodity curves before
  futures hedging; commodity investing before index products; index construction
  before equity indices; the financial-statement company case after the three
  statements; ratios before reporting quality; macro foundations before strategy;
  monetary policy before fixed-income portfolio management; options valuation and
  the volatility surface together before option strategies; private wealth after
  insurance.

## 6. Execution stages

Stage records below say what was done; section 8 gives the evidence. The guide had
already been migrated to the target structure, so the first step adopted its
snapshot (section 8). M0 establishes the mapping before implementation. M1-M4 are work stages within one
coherent migration, not a requirement for separate commits. In particular, activate
replacement section keys together with their file moves and overview notes: the
current checker derives source-folder ownership from the declaration, so switching
the declaration alone would make existing content invalid. Keep changes reviewable
and commit coupled changes together. Routine implementation choices within this
scope do not need a new design review.

### M0 — Reconcile the complete inventory

Done. Before moving entries, record a compact disposition ledger covering
every current topic file and all 697 labels (now [content_migration_ledger.md](content_migration_ledger.md)). A whole-file disposition can cover its
labels together; explicitly list the split-file exceptions from section 5.2.
Record source, destination section, subsection, action and affected navigation.
Use the parsed input graph to include figures and nested inputs, not filenames alone.

Map all 222 specialist pathways of the pinned guide to existing material or an
explicit unwritten gap. Preserve the distinction between an existing related entry and a reviewed
complete treatment. Check prerequisite edges when grouping or moving material.
The compendium has no sections outside the guide. Reconcile all nine
current `common-toolkit` topic files through the seven whole-file moves and two
split-file dispositions above; no input should remain assigned to its old wrapper.

Finish: every existing entry has exactly one planned destination; every guide
pathway has a navigation disposition; no new writing is needed to complete the
structural slice. Store this ledger with this plan rather than building a new
coverage service or mandatory metadata platform.

### M1 — Introduce Parts and enforce the guide sequence

Done. Affected files: `compendium/compendium.tex`, `compendium/house.tex`,
`compendium/preamble.tex`, `tools/check_compendium.py`, its tests and the
documentation of the declaration format.

The flat `\qfsections` list was replaced by eight declarations
`\qfpart{part-key}{Title}{section-key, ...}` in the master, which `house.tex` renders
and the checkers parse: one declaration of each section, explicit Part membership,
and the same traversal for rendering and validation. `load_sections` still returns
the flattened order for existing consumers such as the coverage checker. A Part
heading prints when at least one of its sections has a wrapper, even if its first
declared section is unpopulated; empty sections create no chapter page. The checker
validates the declared structure even where content is absent.

Because the guide already has the target structure, the checker compares the
declaration with `learning_parts` directly: Part keys, titles and order; every guide
section declared exactly once, in its Part and in order; no extra section. The
earlier design's guide-origin metadata, removal of four additions and collapse of
expanded blocks were dropped as unnecessary. Note names may be declared sections,
guide specialist keys or retired overview keys; a retired key cannot be a section,
and its bridge note must name every successor. Every populated section needs its
overview note.

Regression tests cover swapped sections and swapped Parts, a section in the wrong
Part (the Part I/II case), a missing or repeated section, a section outside the
guide, a wrong Part title, a retired overview declared as a section and a bridge
missing a successor, a missing overview, an empty leading section in a populated
Part, a repeated `\input`, an input cycle, a skipped heading level and a wrapper
without one chapter heading. The closeout (section 8.5) added tests for a repeat and
a cycle through equivalent paths such as `sec-a/../sec-a/topic`, for an aliased
input that must count once for reachability and headings, and for an unreachable
topic file with only headings or prose.

### M2 — Reorder and group existing chapters

Apply the within-section ordering in section 5.3 and the heading levels in section
3. Put coherent group headings in wrappers or topic files with a clear owner.
Demote former peer headings where they now belong under a common group.

Avoid a blanket search-and-replace of every `\section`: files such as
`market-making-models.tex` contain multiple topics, while others contain one.
Preserve the entry counter, labels, equations and body text. Configure contents
and bookmark depths in the existing typography setup; retain house typography.

Finish: the populated outline has no skipped heading levels (checked) and reads
from foundations to applications. Representative dense chapters were inspected in
the PDF (section 8). Done.

### M3 — Move material and populate its canonical homes

Apply the whole-file and entry-level moves in section 5. Update both wrappers,
figure paths, cross-links and the disposition ledger together. Introduce a new
wrapper only with its first substantive material and its section overview note.

Compare each moved typed entry against its pre-move body. Allow heading, path and
cross-reference changes; flag substantive content differences for separate review.
Migrate the two split quantitative-methods files by entry label and preserve links
to their old guide-overview identities through the navigation bridges in section
3.4. An old input path may disappear; its callers must be updated in the same change.
The input graph must include each entry exactly once: set-based reachability alone
cannot detect a duplicate `\input`, and traversal must handle cycles explicitly.

Finish: all 697 original labels are present exactly once in the compiled source
graph, with the same types and substantive content. Source methods and their
applications cross-reference one another without duplicate explanations. Done.

### M4 — Reconcile navigation, coverage and conventions

Affected files include section and specialist notes in `notes/pathways/`,
`notes/coverage/objectives.json`, `notes/coverage/learning-roadmap.md`,
`notes/coverage/README.md`, `README.md`, and `compendium/README.md`.

Done. Create the 11 missing overviews and the overviews for newly populated sections
(22 notes; the 16 existing overview notes gained the same specialist-pathway lists).
Update active entry links and topic ownership. If a topic intentionally draws on
entries in several sections, retain its coherent topic identity and explain its
owning section rather than duplicating the objective or evidence record.

Rewrite the two combined guide-overview notes as bridges to the specific sections,
using subject-based displayed titles. Update the owning section of existing
quantitative-methods topics and the asset-pricing topic without renaming their
objective or topic IDs. Document the retired overviews and their successor sections
in the existing navigation documentation; the vendored guide is not edited.

Preserve objective IDs, source locators, evidence dates and outline mappings.
Moves alone must not change coverage or mastery claims. Historical review records
retain their historical meaning; distinguish a historical path from an active
navigation link before updating it. Keep research artefacts at their existing
paths unless a specific broken consumer requires a move.

Record the remaining unwritten sections and pathways in the existing navigation
and coverage documentation. Do not print progress diaries or placeholders inside
the reference's substantive chapters.

Finish: readers can navigate from Part to section overview, pathway, entry and
source, and from coverage objectives to the current canonical entry location. Done.

### M5 — Verify and close out

Done. Use the evidence below, record the commands and actual results in section 8,
and update this plan's status only when its acceptance conditions are met.

## 7. Verification and acceptance

### 7.1 Required structural proof

- Eight declared Parts and 49 unique section keys whose Part keys, titles, order and
  membership equal the pinned guide's `learning_parts` directly.
  The two retired overview keys appear only as guide identities and compatibility
  navigation, not as compiled chapters.
- Every current label retains its type and substantive content; 697 typed entries
  remain. Each is included exactly once, with no missing or cyclic input.
- Every populated section has an overview note; all specialist notes remain valid.
- No broken source, figure, pathway, objective or evidence links caused by moves.
- No changed objective coverage, source-review state or mastery claims solely from
  reorganisation. The registry remains 449 objectives in 108 topics and 1,030
  outline items.
- The printed contents and PDF bookmarks reflect the implemented hierarchy.
  Empty sections and wholly empty Parts do not generate content pages.

### 7.2 Proportionate checks

After each coherent structural edit, run the affected checker and focused checker
tests. Run lint and format checks when changing Python tooling. Include regressions
for Part/order drift, a section in the wrong Part, missing or repeated sections,
compatibility bridges, missing overviews, duplicate inclusions and cycles because
these are concrete risks introduced or exposed by the migration.

At final integration, follow the repository's existing validation requirements:

```sh
make source-check
make pdf
```

Before merging, run `make check` and the pre-commit hooks as required by the root
README. The outline hash check needs the ignored local outline copies. If they are
unavailable, record that exact unverified boundary; do not describe it as passed.

Inspect rendered pages containing Part openings, chapter/subsection boundaries,
typed entry titles, lists, tables, equations and figures, plus the contents and
bookmark hierarchy. Review the log for new overfull boxes, duplicate destinations,
undefined references and missing files. Compare against existing warnings rather
than assigning unrelated layout repairs to this migration.

Do not rerun empirical research or download source data for a file move. Preserve
historical evidence, and rerun a numerical example only when its executable inputs,
path dependencies or calculation have changed, or when an existing required gate
runs it. Diagnose a failed check before repeating it or broadening the scope.

### 7.3 Completion boundary

Completion means the populated compendium follows the declared guide-aligned
hierarchy and every existing entry remains usable and traceable. It does not mean
all 222 specialist pathways have been written, verified or mastered. Keep those
remaining content gaps separate from the structural completion decision.

## 8. Progress and evidence

| Item | State | Evidence |
| --- | --- | --- |
| Documentation cleanup before this plan | Complete | Commit `0c5394d`; this file was created afterwards |
| Structural baseline audit | Complete | 697 entries, 28 populated wrappers, 169 topic files, 42 declared keys; both structural checkers reported zero problems |
| Plan creation | Complete | This file records the proposed hierarchy, relocation decisions and validation scope |
| Subject-name and section-split refinement | Complete | Proposed 49-section structure: seven quantitative-methods sections, separate asset-pricing and causal-inference sections, explicit guide mapping and compatibility requirements |
| First-Part split | Complete | Proposed eight-Part structure: 7 mathematical-methods sections in Part I and 5 empirical-research sections in Part II; remaining Parts renumbered; section order and 49-section total preserved |
| Guide migration (separate repository) | Complete | `institutional_reading_list` commit `6c7734e`: the guide adopted the eight-Part, 49-section structure; not modified here |
| Guide snapshot adopted | Complete, 22 October 2026 | Section 8.1 |
| Plan reconciled with the new guide | Complete | Sections 1, 1.1, 3.4, 3.5, 4 and M1 now use direct `learning_parts` alignment; expansion and Part-origin machinery removed; the earlier crosswalk kept as history in section 3.4 |
| M0: complete disposition ledger | Complete | [content_migration_ledger.md](content_migration_ledger.md): reconciled inventory, 179 file rows, 16 split labels, 12 owner changes, 222 pathway rows |
| M1: Part declarations and alignment checks | Complete | `\qfpart` in the master and `house.tex`; `check_compendium.py` direct guide comparison, overview, bridge, heading and single-inclusion checks; 10 new regression tests, replacing one that accepted sections outside the guide (17 to 26 tests in that file; 29 after the closeout) |
| M2: subsection grouping and ordering | Complete | 38 wrappers with group headings; ordering per section 5.3; contents and bookmark depths set |
| M3: content relocation | Complete | 15 whole-file moves (2 figures with them), 16 labels split into 10 new files and one existing file; 75 entries changed file |
| M4: navigation and coverage reconciliation | Complete | 22 new overview notes, specialist lists in all 38, two bridges, 12 topic owners, 75 evidence paths, roadmap, README files |
| M5: final migration verification | Complete | Sections 8.2–8.4 |
| Closeout of the independent audit | Complete | Section 8.5: pathway inventory reconciled with existing entries; input paths resolved before duplicate, cycle, heading and reachability checks; prose-only topic files must be reachable |

Cleanup validation on 22 October 2026: lint and format checks passed; the compendium
and coverage checkers reported zero problems. An AST comparison found no change to
the calculations in the 20 affected Python scripts; changes were documentation,
comments and one printed heading. Objective records were unchanged apart from
removing 449 obsolete scheduling fields. These results validate the cleanup only,
not the migration.

### 8.1 Guide provenance

- Source: `/Users/lxg/Documents/GitHub/institutional_reading_list`, commit
  `6c7734ed49f1c242908b86a57c4f5d1f0e349ec0` (2026-10-22 14:16:49 +0800). Its working
  tree was clean and its `HEAD` was that commit; it was only read.
- Export: `git -C ../institutional_reading_list archive --format=tar 6c7734ed… | tar -x`
  into a scratch directory, then `git rm -r guide`, a copy of the export and
  `git add -f guide`. Only the 16 tracked files of the commit were copied (no `.git`,
  downloads or untracked files); `study_guide_migration_plan.md` is new, and no file
  was removed.
- Verification: the staged blob IDs of all 16 files equal `git ls-tree -r 6c7734ed`,
  and `git write-tree --prefix=guide/` equals the commit's tree,
  `5eb7d1fc744aa1f65029bac0897e666213161014`. Before replacement the vendored copy
  matched `343d145` byte for byte.
- Key comparison by the guide's maintenance procedure: the catalogue grew from 3,893
  to 3,956 entries (63 added, none removed); none of the 64 changed or added
  catalogue keys is cited by the compendium or notes. Pathways: 203 preserved,
  19 added. Overviews: `common-toolkit` and `empirical-causal-research` retired;
  nine sections added; professional ethics, financial statements, corporate finance
  and private wealth became guide sections.
- `README.md` records the new pin and the previous one. The vendored files were not
  edited.

### 8.2 Commands and results (final tree)

| Command | Result |
| --- | --- |
| `make check` (lock, lint, format, both checkers, tests, numerical examples, outline hashes, PDF) | Exit 0 |
| `uv lock --check` | Resolved 36 packages |
| `ruff check`, `ruff format --check` | All checks passed; 157 files already formatted |
| `check_compendium.py --check` | 697 entries; Parts 8, sections declared 7/5/13/4/7/4/6/3, populated 7/4/12/4/4/3/4/0; 0 problems |
| `check_coverage.py --check --verify-outlines` | 449 objectives in 108 topics, all covered as before; 1,030 outline items in 203 modules, 0 unreviewed; local outline hashes verified; 0 problems |
| `pytest` | 45 passed, 3 subtests passed; 48 passed after the closeout (section 8.5) |
| `make examples` | 127 numerical check scripts passed (includes the figure-reading `asset-pricing-checks.py` after its path change) |
| `make pdf` | 459 pages (446 before); 0 overfull boxes; one underfull box and one `page.i` duplicate-destination warning, both present in the pre-migration log; no undefined or multiply defined references, missing files or other duplicate destinations |
| `make pre-commit` | All 12 hooks passed (the end-of-file hook first fixed the final newline of four split-source files) |

No empirical research was rerun and no data were downloaded. Coverage values,
source-review records, evidence review texts and mastery records are unchanged;
only topic owners, evidence `source` paths and navigation changed.

### 8.3 Entry preservation and alignment

- A parsed inventory before and after (labels, types, titles and a hash of each
  entry body) shows the same 697 labels and types. 695 bodies are byte-identical;
  `mod:capm-sml` and `def:quant-strategy-components` differ only in the `\input`
  path of their moved figures.
- The checker's ordered traversal finds every one of the 179 topic files input
  exactly once, no cycle, no missing input and no entry outside the input graph;
  labels are unique. After the closeout it resolves each input path first and also
  requires every non-empty topic file without entries to be reachable; the tree still
  passes.
- The declaration equals `learning_parts` exactly (keys, titles, order and
  membership); no retired key is declared; all 38 populated sections have overview
  notes; both bridges name all their successors; no heading skips a level.

### 8.4 PDF inspection

Inspected from the built PDF (pages rendered with Ghostscript; outline read with
pypdf in a scratch environment): the contents (Parts, chapters and groups; Part VIII
absent because it has no populated section); the bookmark tree (7 Parts at the root,
chapters, groups, subsections, and the market-making subsubsections beneath their
three groups; the back-matter chapter at the root after a fix); the Part I opening;
the first chapter; the opening of *Financial statement analysis* with its new
group and subsection boundary; the regrouped market-making pages with a figure; the
chapter-end page of asset pricing; the relocated security-market-line figure with
the CAPM regression table and equations; the relocated strategy-structure figure;
and the new *Volatility forecasts* boundary after a table. No new layout defect was
found. Typed-entry titles stay with their first field (house rule unchanged).

### 8.5 Closeout of the independent audit

An independent audit confirmed preservation and passing validation and found three
remaining issues. All three were fixed on 22 October 2026 without changing any
compendium source file, entry, citation, source-review record or coverage state.

1. *Pathway inventory.* Gap had meant only that the pathway's own section had no
   matching file. Every Gap row was compared with all 697 entry titles and bodies by
   subject terms, and the candidate entries were read; a shared citation was not
   counted. A new state, Partial, records 42 pathways whose subtopics are partly
   treated by existing entries, with the labels, their files and the subtopics not
   written. The audit's two cases became Partial: `standard-errors-inference`
   (`meth:regression-misspecification`, `meth:sharpe-ratio-standard-error`,
   `meth:correlation-independence-tests`) and `trend-following`
   (`def:alpha-model-taxonomy`, with CTA, sizing and drawdown material in five
   further entries). The same entry also partly treats `equity-factor-premia`,
   `statistical-arbitrage`, `global-equity-factors` and `commodity-factor-strategies`.
   23 of the 71 remaining gaps record a passing mention or a general method that is
   not a treatment. Ledger section 7, 17 section overview notes and section 9 were
   updated together; the totals are Note 55, Related 54, Partial 42, Gap 71.
2. *Input identity.* `tools/check_compendium.py` resolves each `\input` path before
   the duplicate and cycle checks, heading traversal and reachability use it, so
   `sec-a/topic` and `sec-a/../sec-a/topic` are one file; an input resolving outside
   `compendium/` is reported. Tests cover an aliased repeat, an aliased cycle and an
   aliased input counted once for reachability and headings.
3. *Prose-only topic files.* Every non-empty `.tex` file in a section folder must be
   reachable, not only files with typed entries. Front matter (`front/`) and the
   shared files at the top of `compendium/` stay outside the rule, and a file of
   comments or whitespace is not substantive. A test covers an orphan with a heading
   and prose. On the old checker the three new tests fail; on the new one all pass.
   The real tree has no such orphan.

`compendium/README.md` and the checker's docstring describe both rules.

| Command (final tree) | Result |
| --- | --- |
| `make check` | Exit 0: lock (36 packages), ruff check and format (157 files), compendium checker 0 problems, coverage checker 0 problems (449 objectives in 108 topics; 1,030 outline items, 0 unreviewed; local outline hashes verified), 48 tests and 3 subtests passed, 127 numerical check scripts passed; `make pdf` up to date, since no LaTeX source changed in the closeout |
| `make pre-commit` | All 12 hooks passed, no file modified |
| Entry inventory against `0c5394d` | 697 labels and types identical; 695 bodies byte-identical; `mod:capm-sml` and `def:quant-strategy-components` differ only in their figure `\input` paths; 75 entries changed file |
| Guide provenance | Working tree equals the index for `guide/`; `git write-tree --prefix=guide/` is `5eb7d1fc744aa1f65029bac0897e666213161014`, the tree of `6c7734ed…`; `institutional_reading_list` is at that commit with a clean working tree and was only read |

## 9. Remaining content gaps

These are not structural blockers. Writing them is separate work; the migration
created no placeholder chapters or explanations.

- Declared but unpopulated sections (11): `causal-inference`, `global-regional-markets`, `commodity-spot-markets`, `oil-shocks-macro`, `environmental-markets`, `insurance-climate-risk`, `tokenised-fractional-assets`, `crypto-market-making`, `event-contracts-prediction-markets`, `event-contract-venues`, `event-contract-trading`.
  Their Parts print only through their populated sections; Part VIII prints nothing.
- Pathways (222): 55 have a pathway note with entries; 54 have related existing
  material but no note; 42 have a partial treatment, existing
  entries (often in another section) that treat some subtopics while the rest has
  nothing written; and 71 are content gaps. None of the related or partial material
  has been reviewed as a complete treatment. Ledger section 7 lists every pathway with
  its entry labels, files and unwritten subtopics.
- The closeout review of 22 October 2026 replaced the earlier count of 113 gaps. The
  first inventory recorded a gap wherever the pathway's own section had no matching
  file, and so overlooked material elsewhere: for example robust standard errors in
  `meth:regression-misspecification` (`regression-time-series/multiple-regression`)
  for `standard-errors-inference`, and time-series momentum evidence in
  `def:alpha-model-taxonomy` (`research-engineering-validation/quant-strategy-structure`)
  for `trend-following`. Every Gap row was compared with all 697 entry titles and
  bodies by subject terms and the candidate entries were read; a shared citation was
  not counted. 42 rows became Partial. 23 of the 71 remaining gaps carry a recorded
  passing mention or general method that is not a treatment.

Partial treatments within populated sections (34; the subtopics not written are in
the ledger and the section overview notes):

- `asset-pricing`: `standard-errors-inference`, `return-predictability`, `event-studies`
- `ml-alternative-data`: `ml-asset-pricing`, `forecasting-generative-rl`
- `government-bond-markets`: `treasury-market-functioning`, `treasury-issuance-demand`, `municipal-bonds`
- `corporate-credit-capital`: `bank-capital`, `corporate-hybrids-preferred`
- `securitised-structured-credit`: `covered-bonds`, `cmbs-workouts`
- `systematic-equities`: `equity-factor-premia`, `statistical-arbitrage`, `demand-flows-passive`, `equity-trader-signals`, `equity-event-driven`
- `volatility-trading-premia`: `option-premia-dealers`, `option-implied-information`, `short-dated-retail-options`
- `multi-asset-systematic-macro`: `trend-following`
- `currency-markets`: `fx-volatility-crash-risk`
- `international-equity-markets`: `global-equity-factors`, `em-frontier-equities`, `cross-listing-global-trading`
- `portfolio-construction-risk`: `climate-sustainable`
- `execution-market-making`: `bond-swap-dealer-market-making`
- `energy-commodities`: `commodity-options-real-options`
- `physical-commodity-markets`: `commodity-information-discovery`
- `commodity-investing-premia`: `commodity-factor-strategies`
- `crypto-spot-markets`: `crypto-price-discovery`, `crypto-exchange-failures-regulation`, `crypto-return-dynamics`
- `onchain-protocols`: `staking-restaking`

Eight pathways of unpopulated sections also have partial treatments elsewhere:
`em-capital-flows`, `em-local-currency-bonds`, `commodity-spot-benchmarks`,
`longevity-risk`, `fractional-shares-contracts`, `dex-liquidity-provision`,
`prediction-event-derivatives` and `prediction-trading-strategies`.

Gaps within populated sections (35):

- `government-bond-markets`: `dm-sovereign-bonds`
- `corporate-credit-capital`: `sustainable-bonds`
- `securitised-structured-credit`: `sukuk`
- `volatility-options`: `volatility-models`, `learning-pricing-model-risk`
- `volatility-trading-premia`: `equity-option-returns`
- `international-equity-markets`: `china-em-equities`
- `execution-trading-costs`: `retail-cfd-brokers`
- `energy-commodities`: `commodity-curve-models`
- `physical-commodity-markets`: `freight-forward-hedging`, `commodity-trading-finance`
- `commodity-investing-premia`: `commodity-financialisation`
- `power-gas-environmental`: `physical-lng`, `power-ftr`, `power-market-design`, `renewables-ppa-value`, `power-price-forecasting`, `power-short-term-flexibility`
- `private-capital-allocator`: `trade-receivables`, `royalty-rights`, `litigation-finance-claims`
- `real-asset-investor`: `equipment-aircraft-leasing`, `collectibles-valuation`
- `digital-assets-prediction-markets`: `crypto-option-markets`
- `crypto-spot-markets`: `crypto-exchange-market-quality`, `crypto-valuation-adoption`
- `onchain-protocols`: `mev-block-building`, `onchain-solvers-execution`, `protocol-risk-governance`, `crypto-signals`
- `crypto-trading-strategies`: `crypto-cross-section`, `crypto-trend-technical`, `crypto-stat-arb`, `crypto-ml-prediction`, `crypto-sentiment-events`

The other 36 gaps belong to the 11 unpopulated sections.

- The bridge for `empirical-causal-research` records that causal inference has no
  content. The asset-pricing section's own file treats none of
  `standard-errors-inference`, `return-predictability` and `event-studies`; their
  partial treatments sit in Part I, research engineering and rates.
- Pre-existing, outside this migration: the underfull box in
  `probability-statistics/statistical-inference.tex` and the `page.i` duplicate
  destination from the front matter.
