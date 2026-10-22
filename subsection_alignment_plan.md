# Subsection alignment plan

Status: complete on 22 October 2026. The compendium changes were implemented on branch
`codex/align-guide-subsections` (based on `dc3f3f0`). The learning guide was
revised at its source on branch `codex/compendium-pathway-coverage` of
`institutional_reading_list` and committed locally as
`8302467bc5acfedba55c7e79b311cfb2154f433c`. This
file records how the compendium's hierarchy came to mirror the guide's specialist pathways.
It is separate from the completed Part and section migration, whose records
([content_migration_plan.md](content_migration_plan.md),
[content_migration_ledger.md](content_migration_ledger.md)) are kept unchanged as historical
evidence. The deferred proposal in `content_development_plan.md` was not executed.

The work ran in three passes. The first replaced each chapter's independently designed
subject groups with the guide's pathways. The second placed every entry under the pathway
whose outcome serves it, made five cross-chapter moves, and left 105 entries of chapter-wide
foundations as unnumbered overview topics and 28 entries at a "nearest" pathway, because no
guide pathway's outcome covered them. The third pass amended the guide instead: five
pathways were added and eleven broadened, so that every one of the 697 entries now sits
under a numbered pathway whose outcome covers it, and the overview and nearest
classifications are gone.

## 1. Hierarchy and authorities

| Guide | Compendium |
| --- | --- |
| Part (`learning_parts`) | Part (`\qfpart`) |
| Overview section (`routes`) | chapter (`<section-key>/section.tex`); brief prose may open the wrapper, but no entries |
| Specialist pathway (`routes[*].specialist_order`, names from `specialist_routes`) | numbered section, `\qfpathway{pathway-key}{Name}` in the wrapper |
| Detailed topic | `\subsection` per topic file when a pathway has several; `\subsubsection` inside a topic |
| Typed entry | unchanged |

Authority: `guide/learning_routes.json`, now the snapshot of guide commit `8302467`
(previously `6c7734e`). Pathway outcomes decide ownership; a pathway prints only when it has
entries of its own.

## 2. Baseline and results

Starting point `ca0fd75`; another session merged `dc3f3f0`, which adds only
`content_development_plan.md`, and the branch was re-pointed there with the working tree
intact. Compendium comparisons are with `dc3f3f0`; the third pass was also compared with a
snapshot of the second pass's working tree taken before it began.

| Measure | Baseline | Pass 1 | Pass 2 | Final |
| --- | ---: | ---: | ---: | ---: |
| Guide pathways (pin) | 222 (`6c7734e`) | 222 | 222 | 227 (`8302467`) |
| Typed entries (labels and types unchanged) | 697 | 697 | 697 | 697 |
| Topic files | 179 | 198 | 212 | 212 |
| Printed pathways (numbered sections) | — | 100 | 103 | 111 |
| Entries in unnumbered overview topics | — | — | 105 | 0 |
| Entries at a nearest pathway | — | — | 28 | 0 |
| Level-1 / subsection / subsubsection bookmarks in chapters | 115 / 105 / 9 | 100 / 136 / 9 | 129 / 123 / 4 | 111 / 144 / 4 |
| Compendium PDF pages | 459 | 458 | 461 | 461 |
| Guide PDF pages | 345 | 345 | 345 | 350 |

By chapter (level-1 headings; *Guide* counts all pathways of the section in the final guide):

| Chapter | Guide pathways | Baseline level-1 headings | Printed pathways |
| --- | ---: | ---: | ---: |
| `financial-mathematics` | 2 | 2 | 2 |
| `probability-statistics` | 2 | 5 | 2 |
| `regression-time-series` | 3 | 4 | 3 |
| `stochastic-processes-calculus` | 1 | 1 | 1 |
| `bayesian-inference` | 1 | 1 | 1 |
| `high-dimensional-statistics` | 1 | 1 | 1 |
| `numerical-optimisation` | 1 | 1 | 1 |
| `asset-pricing` | 5 | 1 | 2 |
| `research-engineering-validation` | 4 | 4 | 3 |
| `professional-ethics` | 2 | 5 | 2 |
| `ml-alternative-data` | 7 | 3 | 4 |
| `rates-credit-mortgages` | 6 | 5 | 6 |
| `government-bond-markets` | 5 | 1 | 1 |
| `financial-statement-analysis` | 5 | 5 | 5 |
| `corporate-finance` | 3 | 6 | 3 |
| `corporate-credit-capital` | 5 | 3 | 2 |
| `securitised-structured-credit` | 5 | 2 | 2 |
| `systematic-equities` | 7 | 3 | 3 |
| `volatility-options` | 7 | 6 | 5 |
| `volatility-trading-premia` | 5 | 1 | 1 |
| `multi-asset-systematic-macro` | 7 | 3 | 5 |
| `currency-markets` | 7 | 3 | 6 |
| `international-equity-markets` | 5 | 2 | 1 |
| `portfolio-construction-risk` | 5 | 6 | 5 |
| `portfolio-risk-financing` | 5 | 5 | 5 |
| `execution-market-making` | 8 | 4 | 7 |
| `execution-trading-costs` | 6 | 8 | 5 |
| `energy-commodities` | 4 | 2 | 2 |
| `physical-commodity-markets` | 7 | 1 | 3 |
| `commodity-investing-premia` | 5 | 2 | 3 |
| `power-gas-environmental` | 7 | 1 | 1 |
| `private-capital-allocator` | 7 | 5 | 4 |
| `real-asset-investor` | 5 | 3 | 3 |
| `private-wealth-management` | 3 | 4 | 3 |
| `digital-assets-prediction-markets` | 6 | 3 | 4 |
| `crypto-spot-markets` | 6 | 1 | 1 |
| `onchain-protocols` | 7 | 1 | 2 |
| `crypto-trading-strategies` | 6 | 1 | 1 |

## 3. Guide revision (commit `8302467`)

Made in `learning_routes.json`, the guide's authority, then regenerated with
`refresh_views.py` and rebuilt as the guide's README prescribes. Parts, overview sections,
existing pathway keys and catalogue keys are unchanged; every new reading reuses an existing
catalogue entry, and no source-verification claim was added.

### 3.1 New pathways

| Section | Pathway | Covers (compendium topics) | Readings (catalogue keys) | In-section prerequisite of |
| --- | --- | --- | --- | --- |
| `rates-credit-mortgages` | `bond-pricing-rate-risk` Bond instruments, pricing, yields and interest-rate risk | rate measures and quotation, bond contracts and issuers, the fixed-income universe, pricing from yields, duration and convexity (5 topics, 19 entries) | `s7-hulloptions`, `s7-fabozzifixed`, `wide-bsv-fi-survey`, `exp-sofr-data` | `curve-term-structure` |
| `volatility-options` | `derivative-valuation-strategies` Forwards, swaps and options: no-arbitrage valuation and option strategies | derivative contracts and markets, forward-commitment valuation, option valuation, option strategies (5 topics, 22 entries) | `s7-hulloptions`, `s7-natenberg` | `option-pricing-models`, `convertible-bonds` |
| `multi-asset-systematic-macro` | `macro-economy-global-macro` Business cycles, growth, capital-market expectations and global macro trading | business cycles and policy, growth, capital-market expectations, global macro (4 topics, 20 entries) | `s7-gliner`, `w3-moench-stein-business-cycle`, `wide-harvey-worst-times`, `s7-drobny` | `macro-regimes-stock-bond`, `macro-nowcasting-signals` |
| `portfolio-construction-risk` | `investment-policy-allocation` Investment policy and strategic asset allocation, with alternatives and derivative overlays | the investment process and IPS, behavioural finance, strategic asset allocation, derivative overlays, hedge funds, alternatives allocation (6 topics, 28 entries) | `s7-ang`, `s16-r09`, `wide-barberis-thaler-survey`, `wide-getmansky-lo-makarov` | — (it builds on `portfolio-construction`, so the section DAG places it last) |
| `execution-market-making` | `market-organisation-liquidity` Market organisation, informed trading and liquidity measurement | markets, traders and venues, trading systems, informed trading, arbitrage and manipulation, spread measurement, volatility and crashes (6 topics, 32 entries) | `alpha-harris`, `s6-hasbrouck`, `alpha-laruelle` | `market-making-lob` |

Each has an outcome, prerequisites, staged readings and a checkpoint that tests the outcome;
each section's `section_goals` maps it.

### 3.2 Broadened pathways

| Pathway (key unchanged; new name) | Added to the outcome | Compendium topics now covered | Reading added |
| --- | --- | --- | --- |
| `backtest-inference` Strategy specification, backtest inference, multiple testing and Sharpe-ratio statistics | specify alpha, risk and cost models, horizon and universe as a testable hypothesis | `quant-strategy-structure` | `s7-narang` |
| `bond-risk-premia` Bond risk premia, rates strategies and fixed-income portfolio management | manage a bond portfolio against an index or mandate, with leverage, taxes and curve positioning | `fixed-income-portfolio-management` (mandates, leverage and taxes, indexing) | `s7-fabozzifixed` |
| `equity-long-short-construction` Equity portfolio construction: mandates, indexing, signal combination and long–short portfolios | choose a mandate and benchmark and build an index portfolio | equity mandates and indexing in `equity-portfolio-management` | `s7-ang` |
| `equity-event-driven` Equity securities, corporate actions, earnings events and merger arbitrage | share classes, shareholder rights, issuance, distributions and trading | `equity-securities-markets` | — |
| `corporate-governance-restructuring` Business models, ownership, corporate governance, mergers and restructuring | business model and ESG exposures | `business-models`, `meth:esg-exposure-evaluation` | — |
| `fx-determination-forecasting` Exchange-rate quotes, real exchange rates, determination and forecasting | read quotes in either direction and compute real exchange rates | `fx-market` | — |
| `price-impact-execution` (name unchanged) | feedback from mechanical hedging such as portfolio insurance | `mech:positive-feedback-hedging` | — |
| `commodity-allocation-inflation` Commodities as investments: sectors, access, diversification and inflation hedging | commodity sectors, participants and forms of access | `commodity-futures-investing` | `physical-geman-commodities-2005` |
| `stablecoin-tokenisation` Distributed ledgers, stablecoins and tokenised bonds | consensus, ledgers and smart contracts | `distributed-ledgers` | `crypto-narayanan` |
| `pe-performance-measurement` Alternative-fund structures, fees and private-market performance measurement | categories of alternatives, access routes, returns before and after fees and waterfalls | `def:alternative-investment-categories` (and the fee entries already there) | `s7-ang` |
| `household-finance-lifecycle` Private clients, household finance and lifecycle investment planning | profile a private client and family, the advice industry and its regulation | `def:wealth-management-industry`, `meth:advising-families` | — |

Nine broadened checkpoints gained a first task that tests the added outcome and
`bond-risk-premia` a final one; `price-impact-execution` keeps its checkpoint and section
goal, since its addition is one sentence of explanation. The other ten section goals gained
the matching clause. Where an added subject cites only sources outside
the catalogue (equity securities, business models, the FX market, private clients), the
pathway was broadened rather than a pathway created without catalogue readings.

### 3.3 Other guide changes

- `specialist_order` of five sections (the five that gained a pathway), in the order the
  section DAGs require (`refresh_views.py` stops otherwise); that order puts
  `investment-policy-allocation` last in its section. `section_goals` of thirteen sections:
  a goal for each new pathway and a clause for broadened ones.
- Prerequisite links: `curve-term-structure` on `bond-pricing-rate-risk`;
  `option-pricing-models` and `convertible-bonds` on `derivative-valuation-strategies`;
  `macro-regimes-stock-bond` and `macro-nowcasting-signals` on `macro-economy-global-macro`;
  `market-making-lob` on `market-organisation-liquidity`. The validator confirms that every
  prerequisite precedes its pathway.
- Learning sequences of nine overview sections now name the new or broadened pathways.
- The pathway count in the guide's `README.md` and `structural_mapping.md` (222 → 227).
  `study_guide_migration_plan.md`, a historical record, is unchanged.
- Generated: `institutional_quantitative_finance_learning_guide.tex` and `.pdf`. The HTML
  notes, JSON export and catalogue are regenerated identically.

## 4. Compendium placement

### 4.1 Former overview and nearest placements

| Material | Before (pass 2) | Now under |
| --- | --- | --- |
| `quant-strategy-structure` | overview | `backtest-inference` |
| `interest-rates`, `bond-instruments-markets`, `fixed-income-universe`, `bond-pricing-yields`, `interest-rate-risk` | overview | `bond-pricing-rate-risk` |
| `def:fixed-income-mandates-return-model`, `meth:bond-leverage-taxation`, `meth:bond-index-exposure-benchmarks` | nearest (`bond-risk-premia`) | `bond-risk-premia` (broadened) |
| `business-models`; `meth:esg-exposure-evaluation` | overview; nearest | `corporate-governance-restructuring` (broadened) |
| `equity-securities-markets` | overview | `equity-event-driven` (broadened) |
| `def:equity-portfolio-roles-mandate`, `def:cap-weighted-factor-indexing`, `meth:index-equity-portfolio-construction` | nearest | `equity-long-short-construction` (broadened) |
| `derivative-contracts`, `derivative-markets-uses`, `forward-commitment-valuation`, `option-valuation`; `option-strategies` | overview; nearest (`option-hedging-smile`) | `derivative-valuation-strategies` |
| `business-cycles-policy`, `economic-growth`, `capital-market-expectations`; `global-macro` | overview; nearest (`cross-asset-style-premia`) | `macro-economy-global-macro` |
| `fx-market` | overview | `fx-determination-forecasting` (broadened) |
| `investment-process-planning`, `behavioural-finance`; `derivative-overlays`, `hedge-fund-strategies`, `alternatives-allocation`; and `strategic-asset-allocation` | overview; nearest; outcome-covered under `portfolio-construction` | `investment-policy-allocation` |
| `market-organisation`, `trading-systems`, `informed-trading`, `arbitrage-anticipation`, `spread-measurement`, `volatility-liquidity-crashes` | overview | `market-organisation-liquidity` |
| `mech:positive-feedback-hedging` | nearest | `price-impact-execution` (broadened) |
| `commodity-futures-investing` | overview | `commodity-allocation-inflation` (broadened) |
| `distributed-ledgers` | overview | `stablecoin-tokenisation` (broadened) |
| `def:alternative-investment-categories` | nearest | `pe-performance-measurement` (broadened) |
| `def:wealth-management-industry`, `meth:advising-families` | nearest | `household-finance-lifecycle` (broadened) |

`strategic-asset-allocation` moved with the investment-policy topics because the new
pathway's outcome is exactly the strategic allocation; `portfolio-construction` keeps
portfolio moments and choice, the construction models, cost models and the factor risk model.

### 4.2 Same-chapter placements (pass 2)

| Entries | From (first pass) | To | Pathway outcome served |
| --- | --- | --- | --- |
| `meth:capm-regression`, `def:factor-model-types` | `asset-pricing-models` (`asset-pricing-theory`) | `factor-model-tests` (`empirical-asset-pricing`) | estimate and test a factor model |
| `mod:arch-conditional-variance` | `time-series-models` (`stationarity-cointegration`) | `volatility-forecasting` (`time-series-volatility`) | build and evaluate volatility models |
| `meth:cross-forward-rates`, `meth:fx-bid-offer-triangular-arbitrage`, `meth:currency-forward-mark-to-market` | `fx-mechanics-parity` (`fx-determination-forecasting`) | `fx-quotes-forwards` (`fx-funding-settlement`) | price FX forwards with market quoting conventions, FX liquidity |
| `meth:carry-trade-uip` | same | `currency-carry` (`fx-premia`) | build currency carry portfolios |
| `def:exchange-rate-regimes-capital-flows` | same | `currency-intervention` (`em-currencies-intervention`) | classify exchange-rate regimes |
| `def:fx-market-real-exchange-rates` | same | `fx-market` (pass 2: chapter overview; now `fx-determination-forecasting`) | read quotes and compute real exchange rates |
| `meth:greeks-delta-gamma-hedging`, `res:delta-hedging-volatility-mismatch`, `meth:transaction-cost-hedging` | `option-valuation` | `option-hedging` (`option-hedging-smile`) | delta and vega hedges, discrete rebalancing, transaction costs |
| `meth:revenue-recognition-analysis`, `meth:expense-recognition-capitalisation` | `income-statement-analysis` (`financial-reporting-statements`) | `revenue-expense-recognition` (`accounting-measurement`) | how revenue recognition and depreciation are measured |
| `meth:intangibles-goodwill-reporting` | `balance-sheet-analysis` | `long-lived-asset-accounting` (`accounting-measurement`) | depreciation and impairment of long-lived assets |
| `meth:forward-rates-expected-returns` | `term-structure-returns` (`curve-term-structure`) | `curve-trades` (`bond-risk-premia`) | bond excess returns and carry signals |
| `data:gsw-treasury-curve` | `interest-rates` | `gsw-treasury-curve` (`curve-term-structure`) | build a zero curve |
| `mod:duration-convexity`, `conv:us-rate-quotation` | `interest-rates` (`curve-term-structure`) | `interest-rates` (pass 2: chapter overview; now `bond-pricing-rate-risk`) | quotation conventions and duration |
| `def:electronic-trading-environment` | `trade-strategy-governance` (`price-impact-execution`) | `electronic-trading` (`market-structure-execution-quality`) | how market structure affects execution quality |
| `meth:trade-execution-evaluation-governance` | same | `execution-quality` (`market-structure-execution-quality`) | execution quality |
| `meth:commodity-futures-return-components` | `commodity-futures-investing` | `commodity-return-components` (`commodity-premia`) | separate spot, roll and risk premia; normal backwardation |
| 22 entries of four subsubsections of `market-making-models` | `market-making-lob` | four files (pass 2: chapter overview; now `market-organisation-liquidity`) | informed trading, arbitrage, spread measurement, volatility |

`meth:financial-instruments-liabilities` stays with the balance sheet in
`financial-reporting-statements`: the `accounting-measurement` outcome lists revenue,
inventories, long-lived assets, leases, employee benefits and income taxes, not financial
instruments, and the statements outcome covers preparing and interpreting the balance sheet.

### 4.3 Cross-chapter moves (pass 2)

| Material | From | To | Outcome that decides it | Link kept from the former context |
| --- | --- | --- | --- | --- |
| `meth:convertible-bond-valuation` | `rates-credit-mortgages` (`rate-derivatives`) | `volatility-options` / `convertible-bonds` | combine default, equity optionality and conversion terms | introduction of `embedded-option-bonds` |
| `numerical-methods` (finite differences, least-squares Monte Carlo, Monte Carlo Greeks; 3 entries, file whole) | `volatility-options` | `numerical-optimisation` / `numerical-methods-optimisation`, after Monte Carlo simulation | choose and validate a numerical method (Monte Carlo, PDE) with error bars and sensitivities | introduction of `option-valuation` |
| `meth:cross-currency-basis-swaps` | `volatility-options` (forward commitments) | `currency-markets` / `fx-cip-dollar-funding`, with `ev:cip-deviations` in `cross-currency-basis` | explain the cross-currency basis and price synthetic dollar funding | introduction of `forward-commitment-valuation` |
| `institutional-portfolios` (5 entries, file whole) | `portfolio-construction-risk` (`portfolio-construction`) | `portfolio-risk-financing` / `alm-liquidity` | compare DB plans, insurers, endowments and sovereign funds | introduction of `investment-process-planning` |
| `meth:liability-matching-ladders`, `meth:immunisation-liabilities` | `rates-credit-mortgages` (`bond-risk-premia`) | `portfolio-risk-financing` / `alm-liquidity` (`liability-matching`) | choose a liability hedge that remains fundable | introduction of `fixed-income-portfolio-management` |
| `firms-market-structure` (3 entries, file whole) | `multi-asset-systematic-macro` | `systematic-equities` / `equity-events-fundamentals`, after industry analysis | value a company from its competitive position; the industry analysis there already uses concentration ratios and the HHI that these entries define | none existed; no entry outside the file linked to it |

Not moved: `def:inside-information` and `res:insider-trading-deterrence` (listed by the
professional-ethics note) stay with informed trading; `mod:liquidity-spirals` stays in
`funding-crowding` and is cross-referenced from `crypto-leverage-liquidations`;
`execution-control` stays the optimal-execution benchmark in `price-impact-execution` and is
cross-referenced from `reinforcement-learning-trading`.

Coverage records: `topic:institutional-portfolios` and `topic:firms-market-structure`, whose
entries all moved, now name their new chapters in `notes/coverage/objectives.json` and the
roadmap; four topics with one moved entry keep their owner and are listed in the roadmap's
note on topics with entries in other chapters. No objective, coverage value, next action or
evidence changed.

### 4.4 Remaining exceptions

None. Every entry's printed place is its canonical home, under a numbered pathway whose
outcome covers it (Appendix B). Open questions for a maintainer, outside this structural
pass: `fx-funding-settlement`, `empirical-asset-pricing` and `convertible-bonds` print one
to three entries each, and many guide pathways still have no compendium entries (116 of
227); both are content work.

## 5. Changes

- Guide: section 3; compendium `guide/` replaced by `git archive 8302467`. With a temporary
  index, `git write-tree --prefix=guide/` gives `6e667d8f0b2a9a68f1cb191199de51971cc7134e`,
  equal to the tree of commit `8302467`. The pin is recorded in `README.md`.
- `compendium/house.tex`: `\qfpathway{key}{Name}` only; the overview commands added in pass
  2 are removed.
- Wrappers: all 38 open every topic under a `\qfpathway`; 13 changed in pass 3 (11 regrouped,
  2 retitled for renamed pathways).
- Topic files: pass 3 changed only top heading lines, in 28 files: former overview topics
  became `\subsection`s, and files that became, or stopped being, a pathway's only file lost
  or regained their heading. No file was added or removed in pass 3; across all passes
  38 were added and 5 removed relative to `dc3f3f0`.
- `tools/check_compendium.py`: the overview exception is removed. Every `\input` must follow
  a `\qfpathway`; a bare or starred `\section` or an overview command in a wrapper, and
  `\chapter`, `\section`, `\qfpathway` or an overview command in a topic file, are reported.
  Pathway key, name, parent section, relative order, at least one typed entry per pathway,
  duplicate inputs, cycles, reachability and heading levels are still checked.
- Tests: `NumberedPathwaysOnly` (3) replaces the overview tests; `PathwayHierarchy` (8)
  stays; 59 tests in all.
- Navigation: the *Specialist pathways* lists of the 38 section overview notes use the new
  names, add the five new pathways and note the eleven broadened ones with their files; the
  22 compiled-order lists are by numbered pathway. Status, histories, source-review records
  and pathway-note entry lists are unchanged.
- `README.md` and `compendium/README.md`: conventions and the guide pin.

## 6. Preservation evidence

### 6.1 Pass 3, against the working tree before it

- The same 212 topic files and 38 wrappers; all 697 entry blocks byte-identical and in the
  same files; the 28 changed topic files differ only in their first heading line.
- `notes/entry-evidence.json`, `notes/coverage/`, reading notes, artefacts and
  source-review records unchanged.

### 6.2 Cumulative, against `dc3f3f0` (independent script reading `git show`)

- 697 labels and types (convention 4, data 6, definition 178, evidence 18, example 10,
  mechanism 20, method 364, model 46, pitfall 3, result 32, rule 16); one canonical file each.
- 696 entry blocks byte-identical. The one exception, a navigation correction, is in
  `meth:time-series-model-selection`:
  - before: `A defensible sequence (Interpretation, assembling the steps of the entries above):`
  - after: `A defensible sequence (Interpretation, assembling the steps of the entries above and of \hyperref[mod:arch-conditional-variance]{ARCH}):`
- The seven nested figure inputs are unchanged.
- 93 entries changed file (Appendix C); exactly those 93 records of
  `notes/entry-evidence.json` changed, each only in `source`.
- Introductory prose: 43 of the 55 non-entry paragraphs are unchanged. Twelve were reworded
  to describe the new arrangement, keeping their conventions, qualifications and artefact
  pointers: `asset-pricing-models`, `fx-mechanics-parity` (its notation moved to
  `fx-market`), `option-valuation`, `forward-commitment-valuation`, `embedded-option-bonds`,
  `term-structure-returns`, `fixed-income-portfolio-management`,
  `income-statement-analysis`, `balance-sheet-analysis`, `long-lived-asset-accounting`,
  `trade-strategy-governance` and `investment-process-planning`. Thirteen short
  introductions were added to carry a convention, artefact pointer or link to moved entries:
  `factor-model-tests`, `fx-market`, `fx-quotes-forwards`, `currency-carry`,
  `currency-intervention`, `cross-currency-basis`, `option-hedging`, `convertible-bonds`,
  `revenue-expense-recognition`, `curve-trades`, `liability-matching`, `electronic-trading`
  and `execution-quality`. A sentence-level comparison found no qualification of the old
  introductions missing; only each file's description of its contents changed.
- Coverage: objectives in `notes/coverage/objectives.json` are identical; only the owning
  chapter of `topic:institutional-portfolios` and `topic:firms-market-structure` changed (pass
  2), with the matching roadmap lines. No coverage value, next action, mastery state or
  evidence changed.

## 7. Validation

Guide (`institutional_reading_list`, commit `8302467`):

- `refresh_views.py`: "Refreshed 49 overview routes and 227 specialist pathways, 2707
  selected readings, 760 extended notes and 3956 recency records"; its validator passed
  (placement, prerequisite order, section goals, prose references, legacy labels).
- Catalogue built first (`latexmk -pdf`, 561 pages, PDF byte-identical to the committed one;
  its 20 overfull boxes are in the unchanged catalogue source), then the guide: 345 → 350
  pages, one page per new pathway. Guide log: no undefined references, no overfull boxes.
  All 2,465 reading anchors resolve to labels in the catalogue's `.aux`.
- Guide bookmarks: 10 roots, 49 sections, 267 → 272 level-2 entries (five new pathways).
  Inspected: the Rates section page (goals and learning sequence), its section DAG (13.1
  Bond pricing and rate risk feeding 13.2), the 13.1 pathway page, the Option pricing
  section page, and a Portfolio construction pathway page.

Compendium:

- `make check` (exit 0): lock, ruff lint and format, `check_compendium.py --check` (697
  entries, 111 pathways printed, no problems), `check_coverage.py --check` (no problems),
  pytest (59 passed), 127 numerical check scripts, the outline hash check and the PDF build.
- `make pre-commit`: all hooks passed on all files.
- PDF: 461 pages, as after pass 2; every chapter has the same length as in pass 2, because
  former overview topics became subsections in place and no content moved. Against the
  459-page baseline the +2 comes from pass 2: cross-chapter moves
  (`numerical-optimisation` 1 → 3 pages, `portfolio-risk-financing` 11 → 15,
  `systematic-equities` 25 → 27, `currency-markets` 9 → 10, against decreases in
  `volatility-options`, `multi-asset-systematic-macro`, `portfolio-construction-risk` and
  `rates-credit-mortgages`) and the 13 added introductions. The contents are the same length
  as the baseline's. Fonts, sizes and margins are unchanged, and no content was added.
- Log: no overfull boxes and no unresolved references. As at the baseline, it has the
  warning `ignoring duplicate destination with the name 'page.i'` and one underfull box, in
  the introduction of `probability-statistics/statistical-inference.tex` (lines 3--4).
- Bookmarks (PDFKit): 9 roots, 38 chapters, 111 level-1 bookmarks in chapters, all of them
  guide pathways in `specialist_order` without repeats and none unnumbered; 144 subsections
  and 4 subsubsections, each nested under a pathway.
- Pages inspected: contents p. ii (numbered pathways only, including 18.3, 19.1, 21.1, 24.5),
  the opening of *Market microstructure and market making* (26.1 with 26.1.1 Markets,
  traders and venues), and *Investment policy and strategic asset allocation* (24.5 with
  24.5.1 and its introduction).

## 8. Reversal

Compendium: restore `compendium/`, `guide/`, `notes/entry-evidence.json`, `notes/pathways/`,
`notes/coverage/`, `tools/` and `README.md` from `dc3f3f0`, and remove the 38 new topic files
and this file. Guide: delete the local branch `codex/compendium-pathway-coverage` (commit
`8302467`), whose parent is `6c7734e`.

## Appendix A. Implemented hierarchy

By chapter: printed pathways in guide order, with topic files (the subsection heading where
a pathway has several) and entry counts. 111 of the guide's 227 pathways are printed.

**Financial mathematics and return measurement** (`financial-mathematics`)

- `time-value-cash-flows` Time value of money, discounting and cash-flow valuation: `time-value` (3)
- `return-measurement` Return measurement: holding-period, time-weighted and money-weighted returns: `return-measurement` (1)

**Probability and statistical inference** (`probability-statistics`)

- `probability-statistical-inference` Probability, statistical inference and resampling (12):
  - *Descriptive statistics of returns*: `descriptive-statistics` (4)
  - *Probability and distributions in finance*: `probability` (2)
  - *Sampling and statistical inference*: `statistical-inference` (4)
  - *Historical simulation and resampling*: `resampling` (2)
- `heavy-tails-extremes` Heavy tails, extreme values and dependence: `extreme-values` (1)

**Regression and time-series econometrics** (`regression-time-series`)

- `regression-econometrics` Linear regression, GMM and econometric inference (7):
  - *Simple linear regression*: `regression` (3)
  - *Multiple regression*: `multiple-regression` (4)
- `stationarity-cointegration` Stationarity, ARMA and VAR models, unit roots and cointegration: `time-series-models` (6)
- `time-series-volatility` Volatility forecasting, regimes and structural breaks: `volatility-forecasting` (4)

**Stochastic processes and calculus** (`stochastic-processes-calculus`)

- `stochastic-calculus-control` Stochastic calculus and continuous-time control: `stochastic-calculus` (3)

**Bayesian inference and parameter uncertainty** (`bayesian-inference`)

- `bayesian-parameter-uncertainty` Bayesian inference, shrinkage and parameter uncertainty: `bayesian-updating` (1)

**High-dimensional statistics and covariance estimation** (`high-dimensional-statistics`)

- `high-dimensional-estimation` High-dimensional estimation: covariance shrinkage, random matrices and factor models: `covariance-estimation` (2)

**Numerical methods and optimisation** (`numerical-optimisation`)

- `numerical-methods-optimisation` Optimisation and numerical methods for pricing and portfolios (4):
  - *Monte Carlo simulation*: `monte-carlo-simulation` (1)
  - *Numerical option pricing: finite differences, least-squares Monte Carlo and simulated Greeks*: `numerical-methods` (3)

**Asset pricing theory and empirical tests** (`asset-pricing`)

- `asset-pricing-theory` Asset-pricing theory: stochastic discount factors, CAPM and factor pricing: `asset-pricing-models` (5)
- `empirical-asset-pricing` Empirical asset pricing: factor models and tests: `factor-model-tests` (2)

**Research engineering, data provenance and model validation** (`research-engineering-validation`)

- `backtest-inference` Strategy specification, backtest inference, multiple testing and Sharpe-ratio statistics (12):
  - *The structure of a quant strategy and its alpha models*: `quant-strategy-structure` (3)
  - *Strategy research and backtest evaluation*: `backtest-evaluation` (8)
  - *Scenarios, simulation and sensitivity*: `scenario-simulation` (1)
- `point-in-time-data` Point-in-time data, vendor files and bias control: `point-in-time-data` (5)
- `model-governance-controls` Model governance, AI risk and trading controls (9):
  - *Operational controls for automated trading*: `trading-controls` (4)
  - *Sources of strategy risk and their monitoring*: `strategy-risk` (2)
  - *The research and production chain of a strategy*: `strategy-production` (3)

**Professional ethics** (`professional-ethics`)

- `ethics-code-standards` Codes of ethics, professional standards and enforcement (20):
  - *Ethics, trust and decision-making*: `ethics-trust-framework` (2)
  - *The Code, the Standards and their enforcement*: `code-standards-enforcement` (2)
  - *Professionalism and the integrity of capital markets*: `standards-professionalism-markets` (4)
  - *Duties to clients and to employers*: `standards-clients-employers` (4)
  - *Investment analysis, conflicts and responsibilities as a member*: `standards-analysis-conflicts-members` (6)
  - *Evaluating conduct and manager selection*: `conduct-cases` (2)
- `fiduciary-duties-conflicts` Duties to clients, conflicts of interest and asset-manager responsibilities: `asset-manager-code` (2)

**Machine learning and alternative data** (`ml-alternative-data`)

- `statistical-learning-foundations` Statistical learning foundations and time-series validation (18):
  - *The data-science workflow*: `data-science-workflow` (3)
  - *Machine learning methods*: `machine-learning-methods` (3)
  - *Financial data structures: bars, multi-product series and event sampling*: `financial-data-structures` (4)
  - *Labels and sample weights for overlapping financial outcomes*: `labelling-sample-weights` (6)
  - *Fractionally differentiated features*: `fractional-differentiation` (2)
- `financial-ml-evaluation` Financial ML: information timing, uncertainty and portfolio tests: `ml-time-validity` (2)
- `text-llm-agents` Text, language models and agent evaluation: `text-features` (1)
- `alternative-data-sources` Alternative data: sources, information value and market effects: `financial-data-types` (1)

**Rates: yield curves, term premia and derivatives** (`rates-credit-mortgages`)

- `bond-pricing-rate-risk` Bond instruments, pricing, yields and interest-rate risk (19):
  - *Interest rates, discounting and rate risk*: `interest-rates` (4)
  - *Bonds: features, legal terms, markets and issuers*: `bond-instruments-markets` (6)
  - *The fixed-income universe*: `fixed-income-universe` (1)
  - *Bond prices, yields and spreads*: `bond-pricing-yields` (4)
  - *Bond returns and interest-rate risk*: `interest-rate-risk` (4)
- `curve-term-structure` Yield-curve construction and term-structure models (10):
  - *The term structure: curves, forwards, returns and curve risk*: `term-structure-returns` (4)
  - *The Federal Reserve's fitted Treasury curve*: `gsw-treasury-curve` (1)
  - *Arbitrage-free bond valuation and interest-rate trees*: `arbitrage-free-valuation` (5)
- `rate-derivatives` Interest-rate derivatives, volatility and RFR conventions (7):
  - *Swaps, multi-curve valuation and clearing*: `rate-swaps-clearing` (3)
  - *Bonds with embedded options*: `embedded-option-bonds` (4)
- `monetary-policy-curve` Monetary policy, balance-sheet policy and the yield curve (6):
  - *Monetary policy and its interaction with fiscal policy*: `monetary-fiscal-policy` (2)
  - *Central banks, the policy path and the curve*: `monetary-policy-curves` (4)
- `bond-risk-premia` Bond risk premia, rates strategies and fixed-income portfolio management (7):
  - *Forward rates, expected returns and curve trades*: `curve-trades` (2)
  - *Fixed-income portfolio management*: `fixed-income-portfolio-management` (5)
- `rates-inflation` Inflation-linked bonds, real yields and breakevens: `tips-breakevens` (1)

**Government bond markets and sovereign debt** (`government-bond-markets`)

- `sovereign-municipal` Sovereign default, restructuring and local-currency debt: `sovereign-credit` (2)

**Financial statement analysis** (`financial-statement-analysis`)

- `financial-reporting-statements` Financial reporting frameworks and the three financial statements (12):
  - *Reporting framework and information sources*: `financial-reporting-framework` (3)
  - *Income-statement analysis*: `income-statement-analysis` (3)
  - *Balance-sheet analysis*: `balance-sheet-analysis` (2)
  - *Cash-flow analysis*: `cash-flow-analysis` (3)
  - *A reconciled company case*: `company-case` (1)
- `accounting-measurement` Accounting measurement: revenue, inventories, long-lived assets, leases, employee benefits and income taxes (17):
  - *Revenue and expense recognition*: `revenue-expense-recognition` (2)
  - *Inventories*: `inventory-accounting` (3)
  - *Long-lived assets, intangibles and goodwill*: `long-lived-asset-accounting` (3)
  - *Leases and employee compensation*: `leases-employee-compensation` (6)
  - *Income taxes*: `income-tax-accounting` (3)
- `group-international-reporting` Group accounts, intercorporate investments and foreign-currency reporting (5):
  - *Intercorporate investments*: `intercorporate-investments` (2)
  - *Foreign currency in financial statements*: `foreign-currency-reporting` (3)
- `financial-ratio-quality` Financial ratio analysis, earnings quality and misstatement detection (15):
  - *Ratio analysis*: `ratio-analysis` (4)
  - *Financial reporting quality*: `financial-reporting-quality` (7)
  - *Banks and insurers*: `financial-institution-analysis` (4)
- `financial-statement-forecasting` Financial statement forecasting and integrated company analysis (7):
  - *Financial statement modelling*: `financial-statement-modelling` (4)
  - *Integrated analysis*: `integrated-statement-analysis` (3)

**Corporate finance** (`corporate-finance`)

- `capital-budgeting-investment` Capital budgeting, project valuation and working capital (4):
  - *Working capital and liquidity*: `working-capital-liquidity` (2)
  - *Capital investment and allocation*: `capital-investment` (2)
- `capital-structure-payout` Capital structure, cost of capital and payout policy (8):
  - *Capital structure and the cost of capital*: `capital-structure-cost-of-capital` (4)
  - *Payout policy*: `payout-policy` (4)
- `corporate-governance-restructuring` Business models, ownership, corporate governance, mergers and restructuring (8):
  - *Business models*: `business-models` (1)
  - *Corporate issuers, ownership and governance*: `corporate-ownership-governance` (5)
  - *Corporate restructuring*: `corporate-restructuring` (2)

**Corporate credit, hybrids and labelled bonds** (`corporate-credit-capital`)

- `credit-models-default` Credit models, default prediction and credit portfolios: `credit-risk-analysis` (6)
- `corporate-credit-cds` Corporate bonds and credit derivatives (8):
  - *Credit default swaps*: `credit-default-swaps` (4)
  - *Credit portfolio management*: `credit-portfolio-management` (4)

**Securitised and structured credit** (`securitised-structured-credit`)

- `mortgages-abs-clo` Mortgages, ABS and CLO waterfalls: `securitisation` (3)
- `synthetic-risk-transfer` Synthetic risk transfer and credit-linked notes: `default-correlation` (2)

**Systematic equities** (`systematic-equities`)

- `equity-events-fundamentals` Fundamental valuation and accounting signals (35):
  - *Industry and company analysis*: `industry-company-analysis` (2)
  - *Firms and market structure*: `firms-market-structure` (3)
  - *Equity research and forecast models*: `equity-research-reporting` (2)
  - *Equity valuation foundations*: `equity-valuation-foundations` (6)
  - *Dividend discount models*: `dividend-discount-models` (5)
  - *Price and enterprise-value multiples*: `market-multiples` (7)
  - *Free cash flow valuation*: `free-cash-flow-valuation` (4)
  - *Residual income valuation*: `residual-income-valuation` (3)
  - *Private company valuation*: `private-company-valuation` (3)
- `equity-long-short-construction` Equity portfolio construction: mandates, indexing, signal combination and long–short portfolios (9):
  - *Combining alpha signals*: `signal-combination` (2)
  - *Equity portfolio management*: `equity-portfolio-management` (7)
- `equity-event-driven` Equity securities, corporate actions, earnings events and merger arbitrage: `equity-securities-markets` (4)

**Option pricing, volatility models and hedging** (`volatility-options`)

- `derivative-valuation-strategies` Forwards, swaps and options: no-arbitrage valuation and option strategies (22):
  - *Forwards, futures and options, and the cost of carry*: `derivative-contracts` (2)
  - *Derivative markets, types, payoffs and uses*: `derivative-markets-uses` (4)
  - *Pricing and valuing forward commitments*: `forward-commitment-valuation` (7)
  - *Option valuation: value drivers, parity, binomial trees and Black's model*: `option-valuation` (5)
  - *Option strategies*: `option-strategies` (4)
- `option-pricing-models` Stochastic, local and jump volatility models: `option-pricing` (5)
- `convertible-bonds` Convertible bonds and credit-equity hedging: `convertible-bonds` (1)
- `option-hedging-smile` Option hedging: delta, vega, smile dynamics and transaction costs: `option-hedging` (3)
- `exotics-structured-products` Exotic options, autocallables and structured products: `exotic-options` (4)

**Volatility trading, option premia and implied information** (`volatility-trading-premia`)

- `vix-correlation-dividends` VIX, correlation and dividend derivatives: `vix-variance-dividends` (1)

**Multi-asset and systematic macro** (`multi-asset-systematic-macro`)

- `macro-economy-global-macro` Business cycles, growth, capital-market expectations and global macro trading (20):
  - *Business cycles, fiscal policy, trade and geopolitics*: `business-cycles-policy` (6)
  - *Economic growth and its investment implications*: `economic-growth` (4)
  - *Capital market expectations*: `capital-market-expectations` (6)
  - *Global macro: strategy, record, risk and practitioners*: `global-macro` (4)
- `cross-asset-style-premia` Cross-asset style premia: value, momentum, carry and defensive: `equity-index-valuation` (1)
- `macro-announcements-policy` Macro announcements, policy news and announcement premia: `macro-releases` (2)
- `macro-regimes-stock-bond` Macro regimes, inflation and the stock–bond correlation (4):
  - *The economy and asset values*: `macro-asset-valuation` (3)
  - *A regime map of asset responses*: `macro-regimes-data` (1)
- `macro-nowcasting-signals` Nowcasting, real-time macro data and macro trading signals: `macro-indicators` (2)

**Currency markets: exchange rates, premia and hedging** (`currency-markets`)

- `fx-determination-forecasting` Exchange-rate quotes, real exchange rates, determination and forecasting (6):
  - *The foreign exchange market and real exchange rates*: `fx-market` (1)
  - *Parity conditions, fair value and determination*: `fx-mechanics-parity` (3)
  - *Currencies in global macro*: `macro-fx` (2)
- `fx-funding-settlement` FX forwards, options, fixes and settlement: `fx-quotes-forwards` (3)
- `fx-premia` Currency premia: carry, momentum, value and the dollar: `currency-carry` (2)
- `fx-cip-dollar-funding` Covered interest parity, the cross-currency basis and dollar funding: `cross-currency-basis` (2)
- `currency-hedging` Currency hedging for international portfolios: `currency-management` (4)
- `em-currencies-intervention` Emerging-market currencies: regimes, intervention and the global financial cycle: `currency-intervention` (2)

**International and emerging equity markets** (`international-equity-markets`)

- `intl-equity-integration` Equity index construction, international integration, diversification and home bias (3):
  - *Index construction: weights, divisors, returns and index types*: `index-construction` (2)
  - *Equity indices and instruments for macro*: `equity-indices` (1)

**Portfolio construction and risk** (`portfolio-construction-risk`)

- `portfolio-construction` Portfolio construction, estimation error and risk models (18):
  - *Portfolio return and risk: moments and diversification*: `portfolio-moments` (2)
  - *Portfolio choice: asset classes, risk aversion and efficient portfolios*: `portfolio-choice` (4)
  - *Portfolio construction models: rules and optimisers*: `portfolio-construction-models` (10)
  - *Transaction cost models as inputs to portfolio construction*: `transaction-cost-models` (1)
  - *Risk models: factor exposures and their control*: `risk-models` (1)
- `risk-tail-systemic` Market risk, tail hedging and systemic stress (6):
  - *Risk management framework and governance*: `risk-governance` (2)
  - *Estimating value at risk and expected shortfall*: `var-es-estimation` (1)
  - *Market risk measurement and limits*: `market-risk-measurement` (3)
- `performance-manager-evaluation` Performance attribution and manager evaluation (21):
  - *Performance evaluation*: `performance-evaluation` (3)
  - *Performance attribution, benchmarks and appraisal*: `performance-attribution-appraisal` (7)
  - *Active management: value added, the information ratio and the fundamental law*: `active-management` (3)
  - *Investment manager selection*: `manager-selection` (4)
  - *Performance presentation standards*: `performance-standards` (4)
- `climate-sustainable` Climate risk and sustainable portfolios: `esg-integration` (1)
- `investment-policy-allocation` Investment policy and strategic asset allocation, with alternatives and derivative overlays (28):
  - *Investors, the investment process and investment policy*: `investment-process-planning` (6)
  - *Behavioural finance: biases and market behaviour*: `behavioural-finance` (2)
  - *Strategic asset allocation*: `strategic-asset-allocation` (11)
  - *Derivative overlays for portfolio exposures*: `derivative-overlays` (4)
  - *Hedge funds*: `hedge-fund-strategies` (3)
  - *Allocating to alternative investments*: `alternatives-allocation` (2)

**Funding, collateral and liquidity** (`portfolio-risk-financing`)

- `funding-crowding` Funding liquidity, crowding and arbitrage capital: `crowding-contagion` (3)
- `money-markets-repo-lending` Money markets, repo and securities lending (7):
  - *Money markets and reference rates*: `money-markets` (3)
  - *Securities lending and short selling*: `securities-lending` (4)
- `collateral-xva` Collateral, counterparty risk and xVA: `counterparty-xva` (4)
- `alm-liquidity` Asset-liability management, institutional investment policy and liquidity (7):
  - *Institutional investor portfolios*: `institutional-portfolios` (5)
  - *Cash-flow matching, ladders and immunisation*: `liability-matching` (2)
- `synthetic-equity-cfd-trs` CFDs, total return swaps and synthetic equity financing: `synthetic-shorts` (2)

**Market microstructure and market making** (`execution-market-making`)

- `market-organisation-liquidity` Market organisation, informed trading and liquidity measurement (32):
  - *Markets, traders and venues*: `market-organisation` (9)
  - *Floor and automated trading systems*: `trading-systems` (1)
  - *Informed trading and informative prices*: `informed-trading` (8)
  - *Arbitrageurs, order anticipators and bluffers*: `arbitrage-anticipation` (4)
  - *Measuring and decomposing the spread*: `spread-measurement` (5)
  - *Volatility, liquidity and crashes*: `volatility-liquidity-crashes` (5)
- `market-making-lob` Market making, queues and limit-order-book models (20):
  - *Orders, limit order books and queues*: `order-books` (7)
  - *Inventory and quoting*: `market-making-models` (13)
- `lob-deep-learning` Deep learning on limit-order-book data: `order-flow-imbalance` (1)
- `options-execution` Options market making and execution costs: `options-dealing` (3)
- `market-simulation` Market simulation and counterfactual testing: `order-flow-statistics` (6)
- `fx-dealer-market-making` FX dealing: internalisation, last look and hedging: `fx-dealing` (3)
- `hft-market-design` High-frequency trading, speed and adverse selection: `high-frequency-trading` (7)

**Execution, trading costs and market structure** (`execution-trading-costs`)

- `price-impact-execution` Price impact, optimal execution and TCA (27):
  - *Execution benchmarks and implementation shortfall*: `execution-benchmarks` (3)
  - *Signing trades*: `trade-signing` (1)
  - *Price impact*: `impact-models` (8)
  - *Execution scheduling and block orders*: `execution-scheduling` (2)
  - *Optimal execution as stochastic control: the benchmark for learned policies*: `execution-control` (1)
  - *Execution algorithms, order exposure and portfolio trading*: `execution-algorithms` (6)
  - *Transaction costs and transaction cost analysis*: `transaction-cost-analysis` (3)
  - *Trade strategy, implementation across markets and execution costs*: `trade-strategy-governance` (3)
- `market-structure-execution-quality` Market structure rules, fees and execution quality (21):
  - *The electronic trading environment*: `electronic-trading` (1)
  - *Smart order routing across fragmented venues*: `smart-order-routing` (3)
  - *Dark trading and fragmentation*: `dark-trading-fragmentation` (5)
  - *Best execution, broker conflicts and execution review*: `execution-quality` (3)
  - *Market regulation, venue competition and circuit breakers*: `market-regulation` (6)
  - *Tick size*: `tick-size` (3)
- `otc-fixed-income-trading` Fixed-income and OTC electronic trading: `fixed-income-trading` (3)
- `etf-index-closing-execution` ETFs, index events and closing auctions: `etf-mechanics` (4)
- `futures-execution` Futures execution: matching, rolls and settlement: `futures-execution` (5)

**Commodity futures: storage, curves, hedging and options** (`energy-commodities`)

- `commodity-storage-curves` Theory of storage, convenience yield and inventories: `commodity-curves` (1)
- `commodity-hedging` Commodity hedging: hedge ratios, rolling hedges and corporate risk management: `futures-hedging` (2)

**Physical commodity markets: delivery, price discovery and trading** (`physical-commodity-markets`)

- `metals-storage-delivery` Precious and base metals: storage, lending and delivery: `metals-markets` (1)
- `agricultural-futures-delivery` Agricultural futures, crop balance and delivery: `agricultural-markets` (1)
- `crude-oil-products` Crude oil and refined products: benchmarks, spreads and price reporting: `crude-oil-markets` (1)

**Commodity risk premia and investing: factors, allocation and index products** (`commodity-investing-premia`)

- `commodity-premia` Commodity risk premia: hedging pressure, inventories and the basis: `commodity-return-components` (1)
- `commodity-allocation-inflation` Commodities as investments: sectors, access, diversification and inflation hedging: `commodity-futures-investing` (2)
- `commodity-index-products` Commodity index products: index rules, roll costs, ETFs and flow effects: `commodity-indices` (2)

**Gas and power markets: hubs, storage, networks and market design** (`power-gas-environmental`)

- `gas-hub-pricing` Natural gas markets: hub pricing, oil indexation, market integration and supply shocks: `natural-gas` (1)

**Private equity, private credit and fund structures** (`private-capital-allocator`)

- `pe-performance-measurement` Alternative-fund structures, fees and private-market performance measurement (8):
  - *Alternative investment structures, fees and returns*: `alternative-investment-structures` (3)
  - *Private-market structures, performance and the investment process*: `private-market-programmes` (5)
- `private-equity-vc` Private equity and venture security design: `private-equity-strategies` (4)
- `private-credit-workouts` Private credit and workouts: `private-debt-special-situations` (4)
- `fund-liquidity` Private-fund liquidity and evergreen vehicles: `private-fund-structures` (1)

**Real estate, infrastructure and natural-resource investments** (`real-asset-investor`)

- `property-valuation` Property valuation and listed real estate: `real-estate` (6)
- `infrastructure-regulated-assets` Infrastructure and regulated assets: `infrastructure` (3)
- `natural-resource-rights` Timber, farmland, mineral and water rights: `land-timber-farmland` (1)

**Private wealth management** (`private-wealth-management`)

- `household-finance-lifecycle` Private clients, household finance and lifecycle investment planning (9):
  - *Private clients and the wealth management industry*: `clients-industry` (4)
  - *Wealth and investment planning*: `wealth-planning` (5)
- `tax-aware-wealth-preservation` Taxes, asset location and concentrated positions: `wealth-preservation` (3)
- `wealth-transfer-succession` Estate planning, intergenerational transfers and family-business succession: `wealth-transfer` (3)

**Crypto settlement, venues and derivatives** (`digital-assets-prediction-markets`)

- `stablecoin-tokenisation` Distributed ledgers, stablecoins and tokenised bonds: `distributed-ledgers` (1)
- `crypto-perpetuals` Crypto perpetuals and cross-venue basis: `crypto-venues-perpetuals` (3)
- `stablecoin-pegs-runs` Stablecoin pegs, runs and reserve assets: `stablecoins` (2)
- `crypto-leverage-liquidations` Crypto leverage, liquidations and centralised lenders: `crypto-auto-deleveraging` (1)

**Crypto spot markets: price discovery, market quality, valuation and investors** (`crypto-spot-markets`)

- `crypto-investors-etfs` Crypto investors and access: retail trading, spot ETFs and bank custody: `digital-asset-investing` (1)

**On-chain protocols** (`onchain-protocols`)

- `amm-lending` Automated market makers: pricing, routing and liquidity-provider returns: `amm-lending` (1)
- `defi-lending-liquidations` DeFi lending, liquidations and price oracles: `defi-lending` (1)

**Crypto trading strategies: factors, trend, arbitrage, sentiment and machine learning** (`crypto-trading-strategies`)

- `crypto-arbitrage-carry` Crypto arbitrage and carry: cross-exchange, triangular, funding basis and DeFi yields: `crypto-carry` (1)

## Appendix B. Entry crosswalk

All 697 entries in compiled order. *Pathway* is the entry's canonical home and its printed
place: a numbered pathway whose outcome covers it. *Guide* marks pathways added (*new*) or
broadened (*broadened*) by guide commit `8302467`. *Cross-referenced from* lists other
pathways that cite the entry (pathway-note listings and partial treatments in the overview
notes). Paths are relative to `compendium/`; *File now* is blank when unchanged from
`dc3f3f0`.

| Label | Type | Baseline file | File now | Pathway | Guide | Cross-referenced from |
| --- | --- | --- | --- | --- | --- | --- |
| `def:required-return-components` | definition | `financial-mathematics/time-value` |  | `time-value-cash-flows` |  |  |
| `meth:instrument-present-value` | method | `financial-mathematics/time-value` |  | `time-value-cash-flows` |  |  |
| `res:cash-flow-additivity` | result | `financial-mathematics/time-value` |  | `time-value-cash-flows` |  |  |
| `def:return-measures` | definition | `financial-mathematics/return-measurement` |  | `return-measurement` |  | `performance-manager-evaluation` |
| `def:return-sample-statistics` | definition | `probability-statistics/descriptive-statistics` |  | `probability-statistical-inference` |  |  |
| `def:return-shape-statistics` | definition | `probability-statistics/descriptive-statistics` |  | `probability-statistical-inference` |  |  |
| `def:return-dependence` | definition | `probability-statistics/descriptive-statistics` |  | `probability-statistical-inference` |  |  |
| `def:downside-relative-dispersion` | definition | `probability-statistics/descriptive-statistics` |  | `probability-statistical-inference` |  |  |
| `def:conditional-moments` | definition | `probability-statistics/probability` |  | `probability-statistical-inference` |  |  |
| `def:financial-distributions` | definition | `probability-statistics/probability` |  | `probability-statistical-inference` |  |  |
| `meth:confidence-intervals` | method | `probability-statistics/statistical-inference` |  | `probability-statistical-inference` |  |  |
| `meth:hypothesis-testing` | method | `probability-statistics/statistical-inference` |  | `probability-statistical-inference` |  |  |
| `meth:nonparametric-tests` | method | `probability-statistics/statistical-inference` |  | `probability-statistical-inference` |  |  |
| `meth:correlation-independence-tests` | method | `probability-statistics/statistical-inference` |  | `probability-statistical-inference` |  | `standard-errors-inference` |
| `meth:historical-simulation` | method | `probability-statistics/resampling` |  | `probability-statistical-inference` |  |  |
| `meth:bootstrap-resampling` | method | `probability-statistics/resampling` |  | `probability-statistical-inference` |  |  |
| `meth:extreme-value-tail-estimation` | method | `probability-statistics/extreme-values` |  | `heavy-tails-extremes` |  | `risk-tail-systemic` |
| `meth:simple-regression-estimation` | method | `regression-time-series/regression` |  | `regression-econometrics` |  |  |
| `meth:regression-diagnostics-anova` | method | `regression-time-series/regression` |  | `regression-econometrics` |  |  |
| `meth:regression-prediction-functional-form` | method | `regression-time-series/regression` |  | `regression-econometrics` |  |  |
| `meth:multiple-regression-formulation` | method | `regression-time-series/multiple-regression` |  | `regression-econometrics` |  |  |
| `meth:multiple-regression-fit-tests` | method | `regression-time-series/multiple-regression` |  | `regression-econometrics` |  |  |
| `meth:regression-misspecification` | method | `regression-time-series/multiple-regression` |  | `regression-econometrics` |  | `standard-errors-inference` |
| `meth:regression-extensions` | method | `regression-time-series/multiple-regression` |  | `regression-econometrics` |  |  |
| `meth:trend-models` | method | `regression-time-series/time-series-models` |  | `stationarity-cointegration` |  |  |
| `def:stationarity-unit-roots` | definition | `regression-time-series/time-series-models` |  | `stationarity-cointegration` |  |  |
| `meth:autoregressive-forecasting` | method | `regression-time-series/time-series-models` |  | `stationarity-cointegration` |  |  |
| `meth:forecast-accuracy-evaluation` | method | `regression-time-series/time-series-models` |  | `stationarity-cointegration` |  | `return-predictability` |
| `meth:cointegration-testing` | method | `regression-time-series/time-series-models` |  | `stationarity-cointegration` |  | `statistical-arbitrage` |
| `meth:time-series-model-selection` | method | `regression-time-series/time-series-models` |  | `stationarity-cointegration` |  |  |
| `mod:arch-conditional-variance` | model | `regression-time-series/time-series-models` | `regression-time-series/volatility-forecasting` | `time-series-volatility` |  |  |
| `mod:garch-volatility-forecast` | model | `regression-time-series/volatility-forecasting` |  | `time-series-volatility` |  | `portfolio-construction` |
| `meth:volatility-forecast-loss` | method | `regression-time-series/volatility-forecasting` |  | `time-series-volatility` |  |  |
| `meth:structural-break-tests` | method | `regression-time-series/volatility-forecasting` |  | `time-series-volatility` |  |  |
| `def:brownian-motion-quadratic-variation` | definition | `stochastic-processes-calculus/stochastic-calculus` |  | `stochastic-calculus-control` |  |  |
| `res:ito-lemma-geometric-brownian-motion` | result | `stochastic-processes-calculus/stochastic-calculus` |  | `stochastic-calculus-control` |  |  |
| `res:risk-neutral-pricing-feynman-kac` | result | `stochastic-processes-calculus/stochastic-calculus` |  | `stochastic-calculus-control` |  |  |
| `meth:bayesian-updating` | method | `bayesian-inference/bayesian-updating` |  | `bayesian-parameter-uncertainty` |  |  |
| `meth:portfolio-covariance-estimation` | method | `high-dimensional-statistics/covariance-estimation` |  | `high-dimensional-estimation` |  | `portfolio-construction` |
| `ev:correlation-matrix-noise` | evidence | `high-dimensional-statistics/covariance-estimation` |  | `high-dimensional-estimation` |  |  |
| `meth:monte-carlo-simulation` | method | `numerical-optimisation/monte-carlo-simulation` |  | `numerical-methods-optimisation` |  |  |
| `meth:finite-difference-option-pricing` | method | `volatility-options/numerical-methods` | `numerical-optimisation/numerical-methods` | `numerical-methods-optimisation` |  |  |
| `meth:least-squares-monte-carlo` | method | `volatility-options/numerical-methods` | `numerical-optimisation/numerical-methods` | `numerical-methods-optimisation` |  |  |
| `meth:monte-carlo-greeks` | method | `volatility-options/numerical-methods` | `numerical-optimisation/numerical-methods` | `numerical-methods-optimisation` |  |  |
| `mech:systematic-risk-pricing` | mechanism | `asset-pricing/asset-pricing-models` |  | `asset-pricing-theory` |  |  |
| `mod:return-generating-models` | model | `asset-pricing/asset-pricing-models` |  | `asset-pricing-theory` |  | `event-studies` |
| `mod:capm-sml` | model | `asset-pricing/asset-pricing-models` |  | `asset-pricing-theory` |  |  |
| `meth:required-return-on-equity` | method | `asset-pricing/asset-pricing-models` |  | `asset-pricing-theory` |  |  |
| `mod:multifactor-apt` | model | `asset-pricing/asset-pricing-models` |  | `asset-pricing-theory` |  |  |
| `meth:capm-regression` | method | `asset-pricing/asset-pricing-models` | `asset-pricing/factor-model-tests` | `empirical-asset-pricing` |  |  |
| `def:factor-model-types` | definition | `asset-pricing/asset-pricing-models` | `asset-pricing/factor-model-tests` | `empirical-asset-pricing` |  |  |
| `def:quant-strategy-components` | definition | `research-engineering-validation/quant-strategy-structure` |  | `backtest-inference` | broadened |  |
| `def:alpha-model-taxonomy` | definition | `research-engineering-validation/quant-strategy-structure` |  | `backtest-inference` | broadened | `commodity-factor-strategies`, `equity-factor-premia`, `global-equity-factors`, `statistical-arbitrage`, `trend-following` |
| `meth:alpha-strategy-specification` | method | `research-engineering-validation/quant-strategy-structure` |  | `backtest-inference` | broadened | `trend-following` |
| `meth:hypothesis-driven-strategy-research` | method | `research-engineering-validation/backtest-evaluation` |  | `backtest-inference` | broadened |  |
| `meth:backtest-evaluation-diagnostics` | method | `research-engineering-validation/backtest-evaluation` |  | `backtest-inference` | broadened | `return-predictability` |
| `pit:parameter-overfitting` | pitfall | `research-engineering-validation/backtest-evaluation` |  | `backtest-inference` | broadened |  |
| `pit:backtest-cost-short-assumptions` | pitfall | `research-engineering-validation/backtest-evaluation` |  | `backtest-inference` | broadened |  |
| `meth:backtest-design-evaluation` | method | `research-engineering-validation/backtest-evaluation` |  | `backtest-inference` | broadened |  |
| `meth:sharpe-ratio-standard-error` | method | `research-engineering-validation/backtest-evaluation` |  | `backtest-inference` | broadened | `standard-errors-inference` |
| `meth:deflated-sharpe-ratio` | method | `research-engineering-validation/backtest-evaluation` |  | `backtest-inference` | broadened |  |
| `meth:multiple-testing-control` | method | `research-engineering-validation/backtest-evaluation` |  | `backtest-inference` | broadened |  |
| `meth:scenario-simulation-analysis` | method | `research-engineering-validation/scenario-simulation` |  | `backtest-inference` | broadened |  |
| `data:trading-reference-data` | data | `research-engineering-validation/point-in-time-data` |  | `point-in-time-data` |  |  |
| `data:market-data-levels` | data | `research-engineering-validation/point-in-time-data` |  | `point-in-time-data` |  |  |
| `data:derived-market-statistics` | data | `research-engineering-validation/point-in-time-data` |  | `point-in-time-data` |  |  |
| `data:holdings-insider-filing-lags` | data | `research-engineering-validation/point-in-time-data` |  | `point-in-time-data` |  | `equity-trader-signals` |
| `meth:bitemporal-reference-tables` | method | `research-engineering-validation/point-in-time-data` |  | `point-in-time-data` |  |  |
| `meth:automated-trading-operational-controls` | method | `research-engineering-validation/trading-controls` |  | `model-governance-controls` |  |  |
| `rule:mifid-rts6-algorithmic-controls` | rule | `research-engineering-validation/trading-controls` |  | `model-governance-controls` |  |  |
| `mech:order-state-reconciliation` | mechanism | `research-engineering-validation/trading-controls` |  | `model-governance-controls` |  |  |
| `ev:quant-implementation-failures` | evidence | `research-engineering-validation/trading-controls` |  | `model-governance-controls` |  |  |
| `def:quant-strategy-risk-sources` | definition | `research-engineering-validation/strategy-risk` |  | `model-governance-controls` |  |  |
| `meth:quant-strategy-monitoring` | method | `research-engineering-validation/strategy-risk` |  | `model-governance-controls` |  |  |
| `meth:strategy-production-lifecycle` | method | `research-engineering-validation/strategy-production` |  | `model-governance-controls` |  |  |
| `meth:strategy-promotion-criteria` | method | `research-engineering-validation/strategy-production` |  | `model-governance-controls` |  |  |
| `meth:discretionary-override-governance` | method | `research-engineering-validation/strategy-production` |  | `model-governance-controls` |  |  |
| `def:ethics-trust-professions` | definition | `professional-ethics/ethics-trust-framework` |  | `ethics-code-standards` |  |  |
| `meth:ethical-decision-framework` | method | `professional-ethics/ethics-trust-framework` |  | `ethics-code-standards` |  |  |
| `def:professional-conduct-programme` | definition | `professional-ethics/code-standards-enforcement` |  | `ethics-code-standards` |  |  |
| `def:code-of-ethics-standards` | definition | `professional-ethics/code-standards-enforcement` |  | `ethics-code-standards` |  |  |
| `rule:standard-professionalism` | rule | `professional-ethics/standards-professionalism-markets` |  | `ethics-code-standards` |  |  |
| `meth:preventing-professionalism-violations` | method | `professional-ethics/standards-professionalism-markets` |  | `ethics-code-standards` |  |  |
| `rule:standard-market-integrity` | rule | `professional-ethics/standards-professionalism-markets` |  | `ethics-code-standards` |  |  |
| `meth:preventing-market-integrity-violations` | method | `professional-ethics/standards-professionalism-markets` |  | `ethics-code-standards` |  |  |
| `rule:standard-duties-to-clients` | rule | `professional-ethics/standards-clients-employers` |  | `ethics-code-standards` |  |  |
| `meth:preventing-client-duty-violations` | method | `professional-ethics/standards-clients-employers` |  | `ethics-code-standards` |  |  |
| `rule:standard-duties-to-employers` | rule | `professional-ethics/standards-clients-employers` |  | `ethics-code-standards` |  |  |
| `meth:preventing-employer-duty-violations` | method | `professional-ethics/standards-clients-employers` |  | `ethics-code-standards` |  |  |
| `rule:standard-investment-analysis` | rule | `professional-ethics/standards-analysis-conflicts-members` |  | `ethics-code-standards` |  |  |
| `meth:preventing-analysis-violations` | method | `professional-ethics/standards-analysis-conflicts-members` |  | `ethics-code-standards` |  |  |
| `rule:standard-conflicts-of-interest` | rule | `professional-ethics/standards-analysis-conflicts-members` |  | `ethics-code-standards` |  |  |
| `meth:preventing-conflict-violations` | method | `professional-ethics/standards-analysis-conflicts-members` |  | `ethics-code-standards` |  |  |
| `rule:standard-member-responsibilities` | rule | `professional-ethics/standards-analysis-conflicts-members` |  | `ethics-code-standards` |  |  |
| `meth:preventing-member-violations` | method | `professional-ethics/standards-analysis-conflicts-members` |  | `ethics-code-standards` |  |  |
| `meth:evaluating-conduct-cases` | method | `professional-ethics/conduct-cases` |  | `ethics-code-standards` |  |  |
| `meth:standards-in-manager-selection` | method | `professional-ethics/conduct-cases` |  | `ethics-code-standards` |  |  |
| `def:asset-manager-code` | definition | `professional-ethics/asset-manager-code` |  | `fiduciary-duties-conflicts` |  |  |
| `meth:asset-manager-code-compliance` | method | `professional-ethics/asset-manager-code` |  | `fiduciary-duties-conflicts` |  |  |
| `def:financial-data-science-uses` | definition | `ml-alternative-data/data-science-workflow` |  | `statistical-learning-foundations` |  |  |
| `meth:data-analysis-project` | method | `ml-alternative-data/data-science-workflow` |  | `statistical-learning-foundations` |  |  |
| `meth:ml-model-training-evaluation` | method | `ml-alternative-data/data-science-workflow` |  | `statistical-learning-foundations` |  |  |
| `def:learning-methods-overfitting` | definition | `ml-alternative-data/machine-learning-methods` |  | `statistical-learning-foundations` |  |  |
| `meth:supervised-algorithm-selection` | method | `ml-alternative-data/machine-learning-methods` |  | `statistical-learning-foundations` |  |  |
| `meth:unsupervised-algorithm-selection` | method | `ml-alternative-data/machine-learning-methods` |  | `statistical-learning-foundations` |  |  |
| `meth:activity-sampled-bars` | method | `ml-alternative-data/financial-data-structures` |  | `statistical-learning-foundations` |  |  |
| `meth:information-driven-bars` | method | `ml-alternative-data/financial-data-structures` |  | `statistical-learning-foundations` |  |  |
| `meth:etf-trick` | method | `ml-alternative-data/financial-data-structures` |  | `statistical-learning-foundations` |  |  |
| `meth:event-based-sampling` | method | `ml-alternative-data/financial-data-structures` |  | `statistical-learning-foundations` |  |  |
| `meth:triple-barrier-labelling` | method | `ml-alternative-data/labelling-sample-weights` |  | `statistical-learning-foundations` |  |  |
| `meth:meta-labelling` | method | `ml-alternative-data/labelling-sample-weights` |  | `statistical-learning-foundations` |  |  |
| `def:label-concurrency-uniqueness` | definition | `ml-alternative-data/labelling-sample-weights` |  | `statistical-learning-foundations` |  |  |
| `meth:sequential-bootstrap` | method | `ml-alternative-data/labelling-sample-weights` |  | `statistical-learning-foundations` |  |  |
| `meth:sample-weights-attribution-decay` | method | `ml-alternative-data/labelling-sample-weights` |  | `statistical-learning-foundations` |  |  |
| `meth:purged-embargoed-cross-validation` | method | `ml-alternative-data/labelling-sample-weights` |  | `statistical-learning-foundations` |  |  |
| `mod:fractional-differencing-weights` | model | `ml-alternative-data/fractional-differentiation` |  | `statistical-learning-foundations` |  |  |
| `meth:fixed-width-fractional-differencing` | method | `ml-alternative-data/fractional-differentiation` |  | `statistical-learning-foundations` |  |  |
| `pit:label-weight-leakage` | pitfall | `ml-alternative-data/labelling-sample-weights` | `ml-alternative-data/ml-time-validity` | `financial-ml-evaluation` |  |  |
| `meth:time-valid-ml-experiment-record` | method | `ml-alternative-data/labelling-sample-weights` | `ml-alternative-data/ml-time-validity` | `financial-ml-evaluation` |  |  |
| `meth:text-feature-engineering` | method | `ml-alternative-data/data-science-workflow` | `ml-alternative-data/text-features` | `text-llm-agents` |  | `statistical-learning-foundations` |
| `def:financial-data-types` | definition | `ml-alternative-data/financial-data-types` |  | `alternative-data-sources` |  | `equity-trader-signals` |
| `def:interest-rate-measures` | definition | `rates-credit-mortgages/interest-rates` |  | `bond-pricing-rate-risk` | new |  |
| `mod:forward-rates-fra` | model | `rates-credit-mortgages/interest-rates` |  | `bond-pricing-rate-risk` | new |  |
| `mod:duration-convexity` | model | `rates-credit-mortgages/interest-rates` |  | `bond-pricing-rate-risk` | new |  |
| `conv:us-rate-quotation` | convention | `rates-credit-mortgages/interest-rates` |  | `bond-pricing-rate-risk` | new |  |
| `def:bond-features-indenture` | definition | `rates-credit-mortgages/bond-instruments-markets` |  | `bond-pricing-rate-risk` | new |  |
| `def:bond-cash-flow-contingencies` | definition | `rates-credit-mortgages/bond-instruments-markets` |  | `bond-pricing-rate-risk` | new |  |
| `rule:bond-issuance-legal-tax` | rule | `rates-credit-mortgages/bond-instruments-markets` |  | `bond-pricing-rate-risk` | new | `municipal-bonds` |
| `def:bond-market-segments-trading` | definition | `rates-credit-mortgages/bond-instruments-markets` |  | `bond-pricing-rate-risk` | new |  |
| `meth:corporate-funding-ig-hy` | method | `rates-credit-mortgages/bond-instruments-markets` |  | `bond-pricing-rate-risk` | new |  |
| `def:government-agency-supranational-funding` | definition | `rates-credit-mortgages/bond-instruments-markets` |  | `bond-pricing-rate-risk` | new | `municipal-bonds`, `treasury-issuance-demand` |
| `def:fixed-income-universe` | definition | `rates-credit-mortgages/monetary-policy-curves` | `rates-credit-mortgages/fixed-income-universe` | `bond-pricing-rate-risk` | new |  |
| `meth:bond-price-from-yield` | method | `rates-credit-mortgages/bond-pricing-yields` |  | `bond-pricing-rate-risk` | new |  |
| `meth:matrix-pricing` | method | `rates-credit-mortgages/bond-pricing-yields` |  | `bond-pricing-rate-risk` | new |  |
| `def:bond-yield-spread-measures` | definition | `rates-credit-mortgages/bond-pricing-yields` |  | `bond-pricing-rate-risk` | new |  |
| `meth:floating-money-market-yields` | method | `rates-credit-mortgages/bond-pricing-yields` |  | `bond-pricing-rate-risk` | new |  |
| `meth:bond-return-decomposition` | method | `rates-credit-mortgages/interest-rate-risk` |  | `bond-pricing-rate-risk` | new |  |
| `meth:yield-duration-pvbp` | method | `rates-credit-mortgages/interest-rate-risk` |  | `bond-pricing-rate-risk` | new |  |
| `meth:convexity-portfolio-duration` | method | `rates-credit-mortgages/interest-rate-risk` |  | `bond-pricing-rate-risk` | new |  |
| `meth:curve-based-empirical-duration` | method | `rates-credit-mortgages/interest-rate-risk` |  | `bond-pricing-rate-risk` | new |  |
| `meth:spot-par-forward-curves` | method | `rates-credit-mortgages/term-structure-returns` |  | `curve-term-structure` |  |  |
| `def:swap-curve-short-term-spreads` | definition | `rates-credit-mortgages/term-structure-returns` |  | `curve-term-structure` |  |  |
| `res:term-structure-theories` | result | `rates-credit-mortgages/term-structure-returns` |  | `curve-term-structure` |  |  |
| `meth:yield-curve-factor-exposures` | method | `rates-credit-mortgages/term-structure-returns` |  | `curve-term-structure` |  |  |
| `data:gsw-treasury-curve` | data | `rates-credit-mortgages/interest-rates` | `rates-credit-mortgages/gsw-treasury-curve` | `curve-term-structure` |  |  |
| `meth:arbitrage-free-bond-valuation` | method | `rates-credit-mortgages/arbitrage-free-valuation` |  | `curve-term-structure` |  |  |
| `meth:binomial-rate-tree-calibration` | method | `rates-credit-mortgages/arbitrage-free-valuation` |  | `curve-term-structure` |  |  |
| `mod:term-structure-models-simulation` | model | `rates-credit-mortgages/arbitrage-free-valuation` |  | `curve-term-structure` |  |  |
| `mod:affine-short-rate-models` | model | `rates-credit-mortgages/arbitrage-free-valuation` |  | `curve-term-structure` |  |  |
| `mod:hjm-forward-rate-models` | model | `rates-credit-mortgages/arbitrage-free-valuation` |  | `curve-term-structure` |  |  |
| `mod:multi-curve-fra-swap-valuation` | model | `rates-credit-mortgages/interest-rates` | `rates-credit-mortgages/rate-swaps-clearing` | `rate-derivatives` |  |  |
| `mech:otc-clearing-collateral` | mechanism | `rates-credit-mortgages/interest-rates` | `rates-credit-mortgages/rate-swaps-clearing` | `rate-derivatives` |  |  |
| `def:interest-rate-swaps` | definition | `rates-credit-mortgages/monetary-policy-curves` | `rates-credit-mortgages/rate-swaps-clearing` | `rate-derivatives` |  |  |
| `meth:callable-putable-bond-valuation` | method | `rates-credit-mortgages/embedded-option-bonds` |  | `rate-derivatives` |  |  |
| `meth:option-adjusted-spread` | method | `rates-credit-mortgages/embedded-option-bonds` |  | `rate-derivatives` |  |  |
| `meth:embedded-option-effective-duration` | method | `rates-credit-mortgages/embedded-option-bonds` |  | `rate-derivatives` |  |  |
| `meth:capped-floored-floater-valuation` | method | `rates-credit-mortgages/embedded-option-bonds` |  | `rate-derivatives` |  |  |
| `def:monetary-policy-transmission-regimes` | definition | `rates-credit-mortgages/monetary-fiscal-policy` |  | `monetary-policy-curve` |  |  |
| `meth:monetary-fiscal-policy-mix` | method | `rates-credit-mortgages/monetary-fiscal-policy` |  | `monetary-policy-curve` |  |  |
| `def:central-bank-policy-framework` | definition | `rates-credit-mortgages/monetary-policy-curves` |  | `monetary-policy-curve` |  | `event-studies`, `treasury-issuance-demand` |
| `mod:taylor-rule` | model | `rates-credit-mortgages/monetary-policy-curves` |  | `monetary-policy-curve` |  |  |
| `rule:major-central-banks-current` | rule | `rates-credit-mortgages/monetary-policy-curves` |  | `monetary-policy-curve` |  |  |
| `meth:policy-path-ois-futures` | method | `rates-credit-mortgages/monetary-policy-curves` |  | `monetary-policy-curve` |  |  |
| `meth:forward-rates-expected-returns` | method | `rates-credit-mortgages/term-structure-returns` | `rates-credit-mortgages/curve-trades` | `bond-risk-premia` | broadened |  |
| `meth:curve-trades-carry-rolldown` | method | `rates-credit-mortgages/monetary-policy-curves` | `rates-credit-mortgages/curve-trades` | `bond-risk-premia` | broadened | `curve-term-structure` |
| `def:fixed-income-mandates-return-model` | definition | `rates-credit-mortgages/fixed-income-portfolio-management` |  | `bond-risk-premia` | broadened |  |
| `meth:bond-leverage-taxation` | method | `rates-credit-mortgages/fixed-income-portfolio-management` |  | `bond-risk-premia` | broadened | `municipal-bonds` |
| `meth:bond-index-exposure-benchmarks` | method | `rates-credit-mortgages/fixed-income-portfolio-management` |  | `bond-risk-premia` | broadened |  |
| `meth:yield-curve-positioning` | method | `rates-credit-mortgages/fixed-income-portfolio-management` |  | `bond-risk-premia` | broadened |  |
| `meth:curve-strategy-evaluation` | method | `rates-credit-mortgages/fixed-income-portfolio-management` |  | `bond-risk-premia` | broadened |  |
| `def:tips-breakevens` | definition | `rates-credit-mortgages/monetary-policy-curves` | `rates-credit-mortgages/tips-breakevens` | `rates-inflation` |  |  |
| `def:sovereign-credit-defaults` | definition | `government-bond-markets/sovereign-credit` |  | `sovereign-municipal` |  |  |
| `meth:sovereign-credit-analysis` | method | `government-bond-markets/sovereign-credit` |  | `sovereign-municipal` |  | `municipal-bonds` |
| `def:statement-analysis-framework` | definition | `financial-statement-analysis/financial-reporting-framework` |  | `financial-reporting-statements` |  |  |
| `def:filings-disclosures-information-sources` | definition | `financial-statement-analysis/financial-reporting-framework` |  | `financial-reporting-statements` |  |  |
| `def:ifrs-us-gaap-reporting-systems` | definition | `financial-statement-analysis/financial-reporting-framework` |  | `financial-reporting-statements` |  |  |
| `meth:non-recurring-items` | method | `financial-statement-analysis/income-statement-analysis` |  | `financial-reporting-statements` |  |  |
| `meth:earnings-per-share` | method | `financial-statement-analysis/income-statement-analysis` |  | `financial-reporting-statements` |  |  |
| `meth:income-statement-ratios` | method | `financial-statement-analysis/income-statement-analysis` |  | `financial-reporting-statements` |  |  |
| `meth:financial-instruments-liabilities` | method | `financial-statement-analysis/balance-sheet-analysis` |  | `financial-reporting-statements` |  |  |
| `meth:balance-sheet-ratios` | method | `financial-statement-analysis/balance-sheet-analysis` |  | `financial-reporting-statements` |  |  |
| `meth:statement-linked-cash-flows` | method | `financial-statement-analysis/cash-flow-analysis` |  | `financial-reporting-statements` |  |  |
| `meth:cash-flow-interpretation` | method | `financial-statement-analysis/cash-flow-analysis` |  | `financial-reporting-statements` |  |  |
| `meth:free-cash-flow-coverage` | method | `financial-statement-analysis/cash-flow-analysis` |  | `financial-reporting-statements` |  |  |
| `ex:harbour-tools-statements` | example | `financial-statement-analysis/company-case` |  | `financial-reporting-statements` |  |  |
| `meth:revenue-recognition-analysis` | method | `financial-statement-analysis/income-statement-analysis` | `financial-statement-analysis/revenue-expense-recognition` | `accounting-measurement` |  |  |
| `meth:expense-recognition-capitalisation` | method | `financial-statement-analysis/income-statement-analysis` | `financial-statement-analysis/revenue-expense-recognition` | `accounting-measurement` |  |  |
| `meth:inventory-measurement-nrv` | method | `financial-statement-analysis/inventory-accounting` |  | `accounting-measurement` |  |  |
| `meth:inventory-cost-formulas` | method | `financial-statement-analysis/inventory-accounting` |  | `accounting-measurement` |  |  |
| `meth:inventory-disclosure-analysis` | method | `financial-statement-analysis/inventory-accounting` |  | `accounting-measurement` |  |  |
| `meth:intangibles-goodwill-reporting` | method | `financial-statement-analysis/balance-sheet-analysis` | `financial-statement-analysis/long-lived-asset-accounting` | `accounting-measurement` |  |  |
| `meth:intangible-acquisition-routes` | method | `financial-statement-analysis/long-lived-asset-accounting` |  | `accounting-measurement` |  |  |
| `meth:impairment-derecognition` | method | `financial-statement-analysis/long-lived-asset-accounting` |  | `accounting-measurement` |  |  |
| `meth:lease-reporting` | method | `financial-statement-analysis/leases-employee-compensation` |  | `accounting-measurement` |  |  |
| `meth:post-employment-benefit-reporting` | method | `financial-statement-analysis/leases-employee-compensation` |  | `accounting-measurement` |  |  |
| `meth:share-based-compensation-reporting` | method | `financial-statement-analysis/leases-employee-compensation` |  | `accounting-measurement` |  |  |
| `def:long-term-liability-compensation-disclosures` | definition | `financial-statement-analysis/leases-employee-compensation` |  | `accounting-measurement` |  |  |
| `meth:share-based-compensation-modelling` | method | `financial-statement-analysis/leases-employee-compensation` |  | `accounting-measurement` |  |  |
| `meth:post-employment-benefit-modelling` | method | `financial-statement-analysis/leases-employee-compensation` |  | `accounting-measurement` |  |  |
| `def:accounting-taxable-profit-differences` | definition | `financial-statement-analysis/income-tax-accounting` |  | `accounting-measurement` |  |  |
| `meth:deferred-tax-analysis` | method | `financial-statement-analysis/income-tax-accounting` |  | `accounting-measurement` |  |  |
| `meth:tax-rate-measures` | method | `financial-statement-analysis/income-tax-accounting` |  | `accounting-measurement` |  |  |
| `def:intercorporate-investment-classification` | definition | `financial-statement-analysis/intercorporate-investments` |  | `group-international-reporting` |  |  |
| `meth:consolidation-ratio-effects` | method | `financial-statement-analysis/intercorporate-investments` |  | `group-international-reporting` |  |  |
| `def:functional-currency-transactions` | definition | `financial-statement-analysis/foreign-currency-reporting` |  | `group-international-reporting` |  |  |
| `meth:currency-translation-methods` | method | `financial-statement-analysis/foreign-currency-reporting` |  | `group-international-reporting` |  |  |
| `meth:multinational-currency-tax-analysis` | method | `financial-statement-analysis/foreign-currency-reporting` |  | `group-international-reporting` |  |  |
| `meth:financial-ratio-families` | method | `financial-statement-analysis/ratio-analysis` |  | `financial-ratio-quality` |  |  |
| `meth:ratio-based-evaluation` | method | `financial-statement-analysis/ratio-analysis` |  | `financial-ratio-quality` |  |  |
| `meth:return-on-equity-decomposition` | method | `financial-statement-analysis/ratio-analysis` |  | `financial-ratio-quality` |  |  |
| `meth:ratio-based-earnings-forecast` | method | `financial-statement-analysis/ratio-analysis` |  | `financial-ratio-quality` |  |  |
| `def:reporting-results-quality` | definition | `financial-statement-analysis/financial-reporting-quality` |  | `financial-ratio-quality` |  |  |
| `def:reporting-incentives-discipline` | definition | `financial-statement-analysis/financial-reporting-quality` |  | `financial-ratio-quality` |  |  |
| `meth:earnings-management-presentation` | method | `financial-statement-analysis/financial-reporting-quality` |  | `financial-ratio-quality` |  |  |
| `meth:reporting-warning-signs` | method | `financial-statement-analysis/financial-reporting-quality` |  | `financial-ratio-quality` |  |  |
| `meth:report-quality-evaluation` | method | `financial-statement-analysis/financial-reporting-quality` |  | `financial-ratio-quality` |  |  |
| `meth:earnings-quality-persistence` | method | `financial-statement-analysis/financial-reporting-quality` |  | `financial-ratio-quality` |  | `equity-event-driven` |
| `meth:cash-flow-balance-sheet-quality` | method | `financial-statement-analysis/financial-reporting-quality` |  | `financial-ratio-quality` |  |  |
| `def:financial-institution-features` | definition | `financial-statement-analysis/financial-institution-analysis` |  | `financial-ratio-quality` |  | `bank-capital` |
| `meth:bank-camels-analysis` | method | `financial-statement-analysis/financial-institution-analysis` |  | `financial-ratio-quality` |  | `bank-capital` |
| `meth:insurer-analysis` | method | `financial-statement-analysis/financial-institution-analysis` |  | `financial-ratio-quality` |  |  |
| `meth:life-insurer-analysis` | method | `financial-statement-analysis/financial-institution-analysis` |  | `financial-ratio-quality` |  |  |
| `ex:harbour-pro-forma-model` | example | `financial-statement-analysis/financial-statement-modelling` |  | `financial-statement-forecasting` |  |  |
| `meth:forecast-biases-remedies` | method | `financial-statement-analysis/financial-statement-modelling` |  | `financial-statement-forecasting` |  |  |
| `meth:competition-inflation-forecasting` | method | `financial-statement-analysis/financial-statement-modelling` |  | `financial-statement-forecasting` |  |  |
| `meth:forecast-horizon-steady-state` | method | `financial-statement-analysis/financial-statement-modelling` |  | `financial-statement-forecasting` |  |  |
| `ex:integrated-credit-decision` | example | `financial-statement-analysis/integrated-statement-analysis` |  | `financial-statement-forecasting` |  |  |
| `meth:accounting-analysis-adjustments` | method | `financial-statement-analysis/integrated-statement-analysis` |  | `financial-statement-forecasting` |  |  |
| `meth:accounting-change-effects` | method | `financial-statement-analysis/integrated-statement-analysis` |  | `financial-statement-forecasting` |  |  |
| `meth:cash-conversion-cycle` | method | `corporate-finance/working-capital-liquidity` |  | `capital-budgeting-investment` |  |  |
| `meth:working-capital-policy` | method | `corporate-finance/working-capital-liquidity` |  | `capital-budgeting-investment` |  |  |
| `meth:capital-project-evaluation` | method | `corporate-finance/capital-investment` |  | `capital-budgeting-investment` |  |  |
| `meth:capital-allocation-principles` | method | `corporate-finance/capital-investment` |  | `capital-budgeting-investment` |  | `commodity-options-real-options` |
| `meth:wacc-calculation` | method | `corporate-finance/capital-structure-cost-of-capital` |  | `capital-structure-payout` |  |  |
| `mod:capital-structure-theory` | model | `corporate-finance/capital-structure-cost-of-capital` |  | `capital-structure-payout` |  |  |
| `meth:cost-of-debt-equity-estimation` | method | `corporate-finance/capital-structure-cost-of-capital` |  | `capital-structure-payout` |  |  |
| `meth:capital-structure-benchmarking` | method | `corporate-finance/capital-structure-cost-of-capital` |  | `capital-structure-payout` |  |  |
| `meth:distribution-effects` | method | `corporate-finance/payout-policy` |  | `capital-structure-payout` |  |  |
| `meth:dividend-policy-evaluation` | method | `corporate-finance/payout-policy` |  | `capital-structure-payout` |  |  |
| `meth:payout-policy-comparison` | method | `corporate-finance/payout-policy` |  | `capital-structure-payout` |  |  |
| `meth:dividend-sustainability` | method | `corporate-finance/payout-policy` |  | `capital-structure-payout` |  |  |
| `def:business-model-features-types` | definition | `corporate-finance/business-models` |  | `corporate-governance-restructuring` | broadened |  |
| `def:organisational-forms-issuers` | definition | `corporate-finance/corporate-ownership-governance` |  | `corporate-governance-restructuring` | broadened |  |
| `def:stakeholder-claims` | definition | `corporate-finance/corporate-ownership-governance` |  | `corporate-governance-restructuring` | broadened |  |
| `meth:corporate-governance-evaluation` | method | `corporate-finance/corporate-ownership-governance` |  | `corporate-governance-restructuring` | broadened |  |
| `def:global-ownership-structures` | definition | `corporate-finance/corporate-ownership-governance` |  | `corporate-governance-restructuring` | broadened |  |
| `meth:esg-exposure-evaluation` | method | `corporate-finance/corporate-ownership-governance` |  | `corporate-governance-restructuring` | broadened | `climate-sustainable` |
| `meth:restructuring-evaluation` | method | `corporate-finance/corporate-restructuring` |  | `corporate-governance-restructuring` | broadened |  |
| `ex:restructuring-valuation-effects` | example | `corporate-finance/corporate-restructuring` |  | `corporate-governance-restructuring` | broadened |  |
| `def:credit-risk-components` | definition | `corporate-credit-capital/credit-risk-analysis` |  | `credit-models-default` |  | `corporate-credit-cds` |
| `meth:corporate-credit-analysis` | method | `corporate-credit-capital/credit-risk-analysis` |  | `credit-models-default` |  | `corporate-credit-cds` |
| `meth:risky-bond-cva` | method | `corporate-credit-capital/credit-risk-analysis` |  | `credit-models-default` |  | `corporate-credit-cds` |
| `meth:rating-migration-returns` | method | `corporate-credit-capital/credit-risk-analysis` |  | `credit-models-default` |  | `corporate-credit-cds` |
| `mod:structural-reduced-form-credit` | model | `corporate-credit-capital/credit-risk-analysis` |  | `credit-models-default` |  | `corporate-credit-cds` |
| `meth:credit-spread-term-structure` | method | `corporate-credit-capital/credit-risk-analysis` |  | `credit-models-default` |  | `corporate-credit-cds` |
| `mech:cds-contract-credit-events` | mechanism | `corporate-credit-capital/credit-default-swaps` |  | `corporate-credit-cds` |  |  |
| `def:cds-contract-features` | definition | `corporate-credit-capital/credit-default-swaps` |  | `corporate-credit-cds` |  |  |
| `meth:cds-pricing` | method | `corporate-credit-capital/credit-default-swaps` |  | `corporate-credit-cds` |  |  |
| `meth:cds-strategies` | method | `corporate-credit-capital/credit-default-swaps` |  | `corporate-credit-cds` |  |  |
| `meth:credit-spread-portfolio-risk` | method | `corporate-credit-capital/credit-portfolio-management` |  | `corporate-credit-cds` |  |  |
| `meth:credit-selection-positioning` | method | `corporate-credit-capital/credit-portfolio-management` |  | `corporate-credit-cds` |  |  |
| `meth:credit-liquidity-tail-risk` | method | `corporate-credit-capital/credit-portfolio-management` |  | `corporate-credit-cds` |  |  |
| `meth:credit-cds-international-structured` | method | `corporate-credit-capital/credit-portfolio-management` |  | `corporate-credit-cds` |  | `covered-bonds` |
| `def:securitisation-process` | definition | `securitised-structured-credit/securitisation` |  | `mortgages-abs-clo` |  |  |
| `meth:abs-structures-credit-enhancement` | method | `securitised-structured-credit/securitisation` |  | `mortgages-abs-clo` |  | `covered-bonds` |
| `meth:mortgage-securities-prepayment` | method | `securitised-structured-credit/securitisation` |  | `mortgages-abs-clo` |  | `cmbs-workouts` |
| `mod:gaussian-copula-default-correlation` | model | `securitised-structured-credit/default-correlation` |  | `synthetic-risk-transfer` |  |  |
| `meth:tranche-loss-base-correlation` | method | `securitised-structured-credit/default-correlation` |  | `synthetic-risk-transfer` |  |  |
| `meth:industry-analysis` | method | `systematic-equities/industry-company-analysis` |  | `equity-events-fundamentals` |  |  |
| `meth:company-position-analysis` | method | `systematic-equities/industry-company-analysis` |  | `equity-events-fundamentals` |  |  |
| `meth:cost-output-shutdown` | method | `multi-asset-systematic-macro/firms-market-structure` | `systematic-equities/firms-market-structure` | `equity-events-fundamentals` |  |  |
| `def:market-structures-pricing` | definition | `multi-asset-systematic-macro/firms-market-structure` | `systematic-equities/firms-market-structure` | `equity-events-fundamentals` |  |  |
| `meth:market-structure-identification` | method | `multi-asset-systematic-macro/firms-market-structure` | `systematic-equities/firms-market-structure` | `equity-events-fundamentals` |  |  |
| `meth:forecast-model-valuation` | method | `systematic-equities/equity-research-reporting` |  | `equity-events-fundamentals` |  |  |
| `def:research-report-evaluation` | definition | `systematic-equities/equity-research-reporting` |  | `equity-events-fundamentals` |  |  |
| `def:price-value-indicators` | definition | `systematic-equities/equity-valuation-foundations` |  | `equity-events-fundamentals` |  |  |
| `def:valuation-model-families` | definition | `systematic-equities/equity-valuation-foundations` |  | `equity-events-fundamentals` |  |  |
| `meth:present-value-model-inputs` | method | `systematic-equities/equity-valuation-foundations` |  | `equity-events-fundamentals` |  |  |
| `def:intrinsic-value-mispricing` | definition | `systematic-equities/equity-valuation-foundations` |  | `equity-events-fundamentals` |  |  |
| `meth:valuation-approach-choice` | method | `systematic-equities/equity-valuation-foundations` |  | `equity-events-fundamentals` |  |  |
| `meth:valuation-price-judgement` | method | `systematic-equities/equity-valuation-foundations` |  | `equity-events-fundamentals` |  |  |
| `meth:gordon-growth-model` | method | `systematic-equities/dividend-discount-models` |  | `equity-events-fundamentals` |  |  |
| `meth:preferred-stock-valuation` | method | `systematic-equities/dividend-discount-models` |  | `equity-events-fundamentals` |  | `corporate-hybrids-preferred` |
| `meth:pvgo-justified-pe` | method | `systematic-equities/dividend-discount-models` |  | `equity-events-fundamentals` |  |  |
| `meth:multistage-ddm` | method | `systematic-equities/dividend-discount-models` |  | `equity-events-fundamentals` |  |  |
| `meth:sustainable-growth` | method | `systematic-equities/dividend-discount-models` |  | `equity-events-fundamentals` |  |  |
| `meth:multiples-valuation-basics` | method | `systematic-equities/market-multiples` |  | `equity-events-fundamentals` |  |  |
| `meth:peer-group-selection` | method | `systematic-equities/market-multiples` |  | `equity-events-fundamentals` |  |  |
| `meth:justified-multiples` | method | `systematic-equities/market-multiples` |  | `equity-events-fundamentals` |  |  |
| `meth:normalised-earnings` | method | `systematic-equities/market-multiples` |  | `equity-events-fundamentals` |  |  |
| `meth:alternative-multiples` | method | `systematic-equities/market-multiples` |  | `equity-events-fundamentals` |  |  |
| `meth:enterprise-value-multiples` | method | `systematic-equities/market-multiples` |  | `equity-events-fundamentals` |  |  |
| `meth:comparables-evaluation` | method | `systematic-equities/market-multiples` |  | `equity-events-fundamentals` |  |  |
| `meth:fcff-fcfe-derivation` | method | `systematic-equities/free-cash-flow-valuation` |  | `equity-events-fundamentals` |  |  |
| `meth:fcf-forecasting` | method | `systematic-equities/free-cash-flow-valuation` |  | `equity-events-fundamentals` |  |  |
| `meth:fcf-valuation-models` | method | `systematic-equities/free-cash-flow-valuation` |  | `equity-events-fundamentals` |  |  |
| `meth:cash-flow-proxies` | method | `systematic-equities/free-cash-flow-valuation` |  | `equity-events-fundamentals` |  |  |
| `def:residual-income-eva` | definition | `systematic-equities/residual-income-valuation` |  | `equity-events-fundamentals` |  |  |
| `meth:residual-income-valuation` | method | `systematic-equities/residual-income-valuation` |  | `equity-events-fundamentals` |  |  |
| `meth:residual-income-comparison` | method | `systematic-equities/residual-income-valuation` |  | `equity-events-fundamentals` |  |  |
| `meth:private-earnings-normalisation` | method | `systematic-equities/private-company-valuation` |  | `equity-events-fundamentals` |  |  |
| `meth:private-discount-rate` | method | `systematic-equities/private-company-valuation` |  | `equity-events-fundamentals` |  |  |
| `meth:private-company-valuation` | method | `systematic-equities/private-company-valuation` |  | `equity-events-fundamentals` |  |  |
| `meth:alpha-signal-combination` | method | `systematic-equities/signal-combination` |  | `equity-long-short-construction` | broadened |  |
| `meth:forecast-scaling-ic` | method | `systematic-equities/signal-combination` |  | `equity-long-short-construction` | broadened |  |
| `def:equity-portfolio-roles-mandate` | definition | `systematic-equities/equity-portfolio-management` |  | `equity-long-short-construction` | broadened | `equity-event-driven` |
| `def:cap-weighted-factor-indexing` | definition | `systematic-equities/equity-portfolio-management` |  | `equity-long-short-construction` | broadened | `equity-factor-premia` |
| `meth:index-equity-portfolio-construction` | method | `systematic-equities/equity-portfolio-management` |  | `equity-long-short-construction` | broadened | `demand-flows-passive` |
| `def:active-equity-strategies` | definition | `systematic-equities/equity-portfolio-management` |  | `equity-long-short-construction` | broadened | `equity-event-driven`, `statistical-arbitrage` |
| `meth:active-equity-strategy-creation` | method | `systematic-equities/equity-portfolio-management` |  | `equity-long-short-construction` | broadened |  |
| `meth:active-equity-portfolio-construction` | method | `systematic-equities/equity-portfolio-management` |  | `equity-long-short-construction` | broadened |  |
| `meth:equity-portfolio-capacity-structure` | method | `systematic-equities/equity-portfolio-management` |  | `equity-long-short-construction` | broadened |  |
| `def:equity-instruments` | definition | `systematic-equities/equity-securities-markets` |  | `equity-event-driven` | broadened | `corporate-hybrids-preferred` |
| `def:equity-rights-voting` | definition | `systematic-equities/equity-securities-markets` |  | `equity-event-driven` | broadened |  |
| `def:equity-issuance-trading-liquidity` | definition | `systematic-equities/equity-securities-markets` |  | `equity-event-driven` | broadened |  |
| `def:corporate-distribution-mechanics` | definition | `systematic-equities/equity-securities-markets` |  | `equity-event-driven` | broadened |  |
| `def:derivative-contracts` | definition | `volatility-options/derivative-contracts` |  | `derivative-valuation-strategies` | new |  |
| `res:cost-of-carry-forward-price` | result | `volatility-options/derivative-contracts` |  | `derivative-valuation-strategies` | new |  |
| `def:derivative-markets-otc-exchange` | definition | `volatility-options/derivative-markets-uses` |  | `derivative-valuation-strategies` | new |  |
| `def:derivative-types-commitments-contingent` | definition | `volatility-options/derivative-markets-uses` |  | `derivative-valuation-strategies` | new |  |
| `meth:option-payoff-profit` | method | `volatility-options/derivative-markets-uses` |  | `derivative-valuation-strategies` | new |  |
| `def:derivative-uses-risks` | definition | `volatility-options/derivative-markets-uses` |  | `derivative-valuation-strategies` | new |  |
| `meth:arbitrage-replication-carry` | method | `volatility-options/forward-commitment-valuation` |  | `derivative-valuation-strategies` | new |  |
| `meth:forward-price-value-lifecycle` | method | `volatility-options/forward-commitment-valuation` |  | `derivative-valuation-strategies` | new |  |
| `res:forward-futures-price-difference` | result | `volatility-options/forward-commitment-valuation` |  | `derivative-valuation-strategies` | new |  |
| `def:swaps-as-forward-strips` | definition | `volatility-options/forward-commitment-valuation` |  | `derivative-valuation-strategies` | new |  |
| `meth:equity-forward-futures-valuation` | method | `volatility-options/forward-commitment-valuation` |  | `derivative-valuation-strategies` | new |  |
| `meth:rate-bond-forward-valuation` | method | `volatility-options/forward-commitment-valuation` |  | `derivative-valuation-strategies` | new |  |
| `meth:swap-valuation-replication` | method | `volatility-options/forward-commitment-valuation` |  | `derivative-valuation-strategies` | new |  |
| `def:option-value-drivers` | definition | `volatility-options/option-valuation` |  | `derivative-valuation-strategies` | new |  |
| `res:put-call-forward-parity` | result | `volatility-options/option-valuation` |  | `derivative-valuation-strategies` | new |  |
| `meth:one-period-binomial-valuation` | method | `volatility-options/option-valuation` |  | `derivative-valuation-strategies` | new |  |
| `meth:multi-period-binomial-valuation` | method | `volatility-options/option-valuation` |  | `derivative-valuation-strategies` | new |  |
| `meth:black-model-rates-currencies` | method | `volatility-options/option-valuation` |  | `derivative-valuation-strategies` | new |  |
| `meth:option-replication-deltas` | method | `volatility-options/option-strategies` |  | `derivative-valuation-strategies` | new |  |
| `meth:covered-call-protective-put` | method | `volatility-options/option-strategies` |  | `derivative-valuation-strategies` | new |  |
| `meth:option-spreads-volatility-strategies` | method | `volatility-options/option-strategies` |  | `derivative-valuation-strategies` | new |  |
| `ex:option-strategy-selection-case` | example | `volatility-options/option-strategies` |  | `derivative-valuation-strategies` | new |  |
| `mod:black-scholes-merton` | model | `volatility-options/option-pricing` |  | `option-pricing-models` |  |  |
| `def:implied-volatility-surface` | definition | `volatility-options/option-pricing` |  | `option-pricing-models` |  | `option-implied-information` |
| `mod:heston-stochastic-volatility` | model | `volatility-options/option-pricing` |  | `option-pricing-models` |  |  |
| `mod:merton-jump-diffusion` | model | `volatility-options/option-pricing` |  | `option-pricing-models` |  |  |
| `mod:sabr-smile` | model | `volatility-options/option-pricing` |  | `option-pricing-models` |  | `rate-derivatives` |
| `meth:convertible-bond-valuation` | method | `rates-credit-mortgages/embedded-option-bonds` | `volatility-options/convertible-bonds` | `convertible-bonds` |  |  |
| `meth:greeks-delta-gamma-hedging` | method | `volatility-options/option-valuation` | `volatility-options/option-hedging` | `option-hedging-smile` |  |  |
| `res:delta-hedging-volatility-mismatch` | result | `volatility-options/option-valuation` | `volatility-options/option-hedging` | `option-hedging-smile` |  | `option-premia-dealers` |
| `meth:transaction-cost-hedging` | method | `volatility-options/option-valuation` | `volatility-options/option-hedging` | `option-hedging-smile` |  |  |
| `meth:digital-option-valuation` | method | `volatility-options/exotic-options` |  | `exotics-structured-products` |  |  |
| `meth:barrier-option-valuation` | method | `volatility-options/exotic-options` |  | `exotics-structured-products` |  |  |
| `meth:lookback-option-valuation` | method | `volatility-options/exotic-options` |  | `exotics-structured-products` |  |  |
| `meth:asian-option-valuation` | method | `volatility-options/exotic-options` |  | `exotics-structured-products` |  |  |
| `def:vix-variance-dividend-swaps` | definition | `volatility-trading-premia/vix-variance-dividends` |  | `vix-correlation-dividends` |  | `option-premia-dealers` |
| `def:business-credit-cycles` | definition | `multi-asset-systematic-macro/business-cycles-policy` |  | `macro-economy-global-macro` | new |  |
| `meth:business-cycle-indicators` | method | `multi-asset-systematic-macro/business-cycles-policy` |  | `macro-economy-global-macro` | new |  |
| `def:fiscal-policy-tools-stance` | definition | `multi-asset-systematic-macro/business-cycles-policy` |  | `macro-economy-global-macro` | new |  |
| `def:geopolitics-institutions-tools` | definition | `multi-asset-systematic-macro/business-cycles-policy` |  | `macro-economy-global-macro` | new |  |
| `meth:geopolitical-risk-assessment` | method | `multi-asset-systematic-macro/business-cycles-policy` |  | `macro-economy-global-macro` | new |  |
| `meth:trade-benefits-restrictions-blocs` | method | `multi-asset-systematic-macro/business-cycles-policy` |  | `macro-economy-global-macro` | new |  |
| `def:growth-determinants-factors` | definition | `multi-asset-systematic-macro/economic-growth` |  | `macro-economy-global-macro` | new |  |
| `meth:potential-gdp-growth-accounting` | method | `multi-asset-systematic-macro/economic-growth` |  | `macro-economy-global-macro` | new |  |
| `mod:growth-theories-convergence` | model | `multi-asset-systematic-macro/economic-growth` |  | `macro-economy-global-macro` | new |  |
| `def:growth-policies-technology-trade` | definition | `multi-asset-systematic-macro/economic-growth` |  | `macro-economy-global-macro` | new |  |
| `meth:cme-framework-forecasting` | method | `multi-asset-systematic-macro/capital-market-expectations` |  | `macro-economy-global-macro` | new |  |
| `meth:growth-shocks-long-run-expectations` | method | `multi-asset-systematic-macro/capital-market-expectations` |  | `macro-economy-global-macro` | new |  |
| `meth:cycle-policy-curve-expectations` | method | `multi-asset-systematic-macro/capital-market-expectations` |  | `macro-economy-global-macro` | new |  |
| `meth:asset-class-return-forecasts` | method | `multi-asset-systematic-macro/capital-market-expectations` |  | `macro-economy-global-macro` | new | `em-frontier-equities`, `global-equity-factors` |
| `meth:fx-volatility-forecasts` | method | `multi-asset-systematic-macro/capital-market-expectations` |  | `macro-economy-global-macro` | new |  |
| `ex:global-portfolio-macro-rebalancing` | example | `multi-asset-systematic-macro/capital-market-expectations` |  | `macro-economy-global-macro` | new |  |
| `def:global-macro-strategy` | definition | `multi-asset-systematic-macro/global-macro` |  | `macro-economy-global-macro` | new | `trend-following` |
| `ev:global-macro-crisis-performance` | evidence | `multi-asset-systematic-macro/global-macro` |  | `macro-economy-global-macro` | new |  |
| `meth:macro-position-sizing-risk` | method | `multi-asset-systematic-macro/global-macro` |  | `macro-economy-global-macro` | new | `trend-following` |
| `meth:macro-practitioner-frameworks` | method | `multi-asset-systematic-macro/global-macro` |  | `macro-economy-global-macro` | new |  |
| `meth:equity-index-valuation` | method | `multi-asset-systematic-macro/macro-regimes-data` | `multi-asset-systematic-macro/equity-index-valuation` | `cross-asset-style-premia` |  | `global-equity-factors` |
| `data:us-macro-release-calendar` | data | `multi-asset-systematic-macro/macro-regimes-data` | `multi-asset-systematic-macro/macro-releases` | `macro-announcements-policy` |  |  |
| `meth:macro-event-queries` | method | `multi-asset-systematic-macro/macro-regimes-data` | `multi-asset-systematic-macro/macro-releases` | `macro-announcements-policy` |  |  |
| `res:economy-discount-rates-cash-flows` | result | `multi-asset-systematic-macro/macro-asset-valuation` |  | `macro-regimes-stock-bond` |  |  |
| `meth:cycle-rates-breakevens-spreads` | method | `multi-asset-systematic-macro/macro-asset-valuation` |  | `macro-regimes-stock-bond` |  |  |
| `meth:cycle-equities-property` | method | `multi-asset-systematic-macro/macro-asset-valuation` |  | `macro-regimes-stock-bond` |  |  |
| `def:macro-regime-asset-map` | definition | `multi-asset-systematic-macro/macro-regimes-data` |  | `macro-regimes-stock-bond` |  |  |
| `def:macroeconomic-indicators` | definition | `multi-asset-systematic-macro/macro-regimes-data` | `multi-asset-systematic-macro/macro-indicators` | `macro-nowcasting-signals` |  |  |
| `meth:equity-macro-leading-indicators` | method | `multi-asset-systematic-macro/macro-regimes-data` | `multi-asset-systematic-macro/macro-indicators` | `macro-nowcasting-signals` |  |  |
| `def:fx-market-real-exchange-rates` | definition | `currency-markets/fx-mechanics-parity` | `currency-markets/fx-market` | `fx-determination-forecasting` | broadened |  |
| `res:international-parity-conditions` | result | `currency-markets/fx-mechanics-parity` |  | `fx-determination-forecasting` | broadened |  |
| `meth:exchange-rate-forecasting-fair-value` | method | `currency-markets/fx-mechanics-parity` |  | `fx-determination-forecasting` | broadened |  |
| `def:flows-policy-exchange-rates` | definition | `currency-markets/fx-mechanics-parity` |  | `fx-determination-forecasting` | broadened |  |
| `def:us-dollar-dxy-sdr` | definition | `currency-markets/macro-fx` |  | `fx-determination-forecasting` | broadened |  |
| `meth:fx-valuation-signals` | method | `currency-markets/macro-fx` |  | `fx-determination-forecasting` | broadened | `return-predictability` |
| `meth:cross-forward-rates` | method | `currency-markets/fx-mechanics-parity` | `currency-markets/fx-quotes-forwards` | `fx-funding-settlement` |  |  |
| `meth:fx-bid-offer-triangular-arbitrage` | method | `currency-markets/fx-mechanics-parity` | `currency-markets/fx-quotes-forwards` | `fx-funding-settlement` |  |  |
| `meth:currency-forward-mark-to-market` | method | `currency-markets/fx-mechanics-parity` | `currency-markets/fx-quotes-forwards` | `fx-funding-settlement` |  |  |
| `meth:carry-trade-uip` | method | `currency-markets/fx-mechanics-parity` | `currency-markets/currency-carry` | `fx-premia` |  | `fx-volatility-crash-risk` |
| `mod:fx-carry-trade` | model | `currency-markets/macro-fx` | `currency-markets/currency-carry` | `fx-premia` |  | `fx-volatility-crash-risk` |
| `meth:cross-currency-basis-swaps` | method | `volatility-options/forward-commitment-valuation` | `currency-markets/cross-currency-basis` | `fx-cip-dollar-funding` |  |  |
| `ev:cip-deviations` | evidence | `currency-markets/macro-fx` | `currency-markets/cross-currency-basis` | `fx-cip-dollar-funding` |  |  |
| `meth:currency-portfolio-effects` | method | `currency-markets/currency-management` |  | `currency-hedging` |  |  |
| `meth:currency-hedging-programme` | method | `currency-markets/currency-management` |  | `currency-hedging` |  |  |
| `meth:active-currency-strategies` | method | `currency-markets/currency-management` |  | `currency-hedging` |  | `fx-volatility-crash-risk` |
| `meth:currency-hedge-cost-reduction` | method | `currency-markets/currency-management` |  | `currency-hedging` |  | `fx-volatility-crash-risk` |
| `def:exchange-rate-regimes-capital-flows` | definition | `currency-markets/fx-mechanics-parity` | `currency-markets/currency-intervention` | `em-currencies-intervention` |  |  |
| `def:currency-regimes-intervention` | definition | `currency-markets/macro-fx` | `currency-markets/currency-intervention` | `em-currencies-intervention` |  |  |
| `meth:index-value-return-calculation` | method | `international-equity-markets/index-construction` |  | `intl-equity-integration` |  |  |
| `def:equity-fixed-income-index-types` | definition | `international-equity-markets/index-construction` |  | `intl-equity-integration` |  |  |
| `def:equity-indices-derivatives` | definition | `international-equity-markets/equity-indices` |  | `intl-equity-integration` |  | `cross-listing-global-trading` |
| `meth:portfolio-return-moments` | method | `portfolio-construction-risk/portfolio-moments` |  | `portfolio-construction` |  |  |
| `mech:diversification-correlation` | mechanism | `portfolio-construction-risk/portfolio-moments` |  | `portfolio-construction` |  |  |
| `def:asset-class-characteristics` | definition | `portfolio-construction-risk/portfolio-choice` |  | `portfolio-construction` |  |  |
| `def:risk-aversion-utility` | definition | `portfolio-construction-risk/portfolio-choice` |  | `portfolio-construction` |  |  |
| `meth:efficient-frontier` | method | `portfolio-construction-risk/portfolio-choice` |  | `portfolio-construction` |  |  |
| `meth:capital-allocation-line` | method | `portfolio-construction-risk/portfolio-choice` |  | `portfolio-construction` |  |  |
| `meth:rule-based-position-sizing` | method | `portfolio-construction-risk/portfolio-construction-models` |  | `portfolio-construction` |  | `trend-following` |
| `res:kelly-growth-optimal-fraction` | result | `portfolio-construction-risk/portfolio-construction-models` |  | `portfolio-construction` |  |  |
| `meth:equal-risk-contribution` | method | `portfolio-construction-risk/portfolio-construction-models` |  | `portfolio-construction` |  |  |
| `ev:volatility-managed-portfolios` | evidence | `portfolio-construction-risk/portfolio-construction-models` |  | `portfolio-construction` |  | `equity-factor-premia`, `risk-parity-vol-targeting` |
| `meth:resampled-efficiency` | method | `portfolio-construction-risk/portfolio-construction-models` |  | `portfolio-construction` |  |  |
| `mod:mean-variance-portfolio-optimisation` | model | `portfolio-construction-risk/portfolio-construction-models` |  | `portfolio-construction` |  |  |
| `meth:mean-cvar-optimisation` | method | `portfolio-construction-risk/portfolio-construction-models` |  | `portfolio-construction` |  |  |
| `meth:signal-portfolio-allocation` | method | `portfolio-construction-risk/portfolio-construction-models` |  | `portfolio-construction` |  |  |
| `mod:pca-risk-distribution-weights` | model | `portfolio-construction-risk/portfolio-construction-models` |  | `portfolio-construction` |  |  |
| `mod:black-litterman` | model | `portfolio-construction-risk/portfolio-construction-models` |  | `portfolio-construction` |  |  |
| `mod:portfolio-transaction-cost-function` | model | `portfolio-construction-risk/transaction-cost-models` |  | `portfolio-construction` |  |  |
| `mod:factor-risk-model` | model | `portfolio-construction-risk/risk-models` |  | `portfolio-construction` |  |  |
| `def:risk-management-framework` | definition | `portfolio-construction-risk/risk-governance` |  | `risk-tail-systemic` |  |  |
| `meth:risk-identification-modification` | method | `portfolio-construction-risk/risk-governance` |  | `risk-tail-systemic` |  |  |
| `meth:var-es-estimation-methods` | method | `portfolio-construction-risk/risk-models` | `portfolio-construction-risk/var-es-estimation` | `risk-tail-systemic` |  |  |
| `meth:portfolio-var-methods-decomposition` | method | `portfolio-construction-risk/market-risk-measurement` |  | `risk-tail-systemic` |  |  |
| `meth:sensitivity-scenario-risk-measures` | method | `portfolio-construction-risk/market-risk-measurement` |  | `risk-tail-systemic` |  |  |
| `meth:market-risk-limits-capital` | method | `portfolio-construction-risk/market-risk-measurement` |  | `risk-tail-systemic` |  |  |
| `meth:relative-performance-evaluation` | method | `portfolio-construction-risk/performance-evaluation` |  | `performance-manager-evaluation` |  |  |
| `meth:skill-luck-significance-tests` | method | `portfolio-construction-risk/performance-evaluation` |  | `performance-manager-evaluation` |  |  |
| `meth:gips-composite-presentation` | method | `portfolio-construction-risk/performance-evaluation` |  | `performance-manager-evaluation` |  |  |
| `def:performance-evaluation-components` | definition | `portfolio-construction-risk/performance-attribution-appraisal` |  | `performance-manager-evaluation` |  |  |
| `meth:risk-adjusted-performance-measures` | method | `portfolio-construction-risk/performance-attribution-appraisal` |  | `performance-manager-evaluation` |  |  |
| `meth:return-attribution` | method | `portfolio-construction-risk/performance-attribution-appraisal` |  | `performance-manager-evaluation` |  |  |
| `meth:macro-attribution-owner-manager` | method | `portfolio-construction-risk/performance-attribution-appraisal` |  | `performance-manager-evaluation` |  |  |
| `meth:benchmark-selection-quality` | method | `portfolio-construction-risk/performance-attribution-appraisal` |  | `performance-manager-evaluation` |  |  |
| `meth:downside-appraisal-measures` | method | `portfolio-construction-risk/performance-attribution-appraisal` |  | `performance-manager-evaluation` |  |  |
| `meth:manager-skill-evaluation` | method | `portfolio-construction-risk/performance-attribution-appraisal` |  | `performance-manager-evaluation` |  |  |
| `meth:active-return-information-ratio` | method | `portfolio-construction-risk/active-management` |  | `performance-manager-evaluation` |  |  |
| `res:fundamental-law-active-management` | result | `portfolio-construction-risk/active-management` |  | `performance-manager-evaluation` |  |  |
| `meth:active-risk-decomposition` | method | `portfolio-construction-risk/active-management` |  | `performance-manager-evaluation` |  |  |
| `meth:manager-due-diligence` | method | `portfolio-construction-risk/manager-selection` |  | `performance-manager-evaluation` |  |  |
| `meth:manager-philosophy-process-behaviour` | method | `portfolio-construction-risk/manager-selection` |  | `performance-manager-evaluation` |  |  |
| `meth:vehicle-contract-fee-analysis` | method | `portfolio-construction-risk/manager-selection` |  | `performance-manager-evaluation` |  |  |
| `ex:manager-selection-case` | example | `portfolio-construction-risk/manager-selection` |  | `performance-manager-evaluation` |  |  |
| `def:gips-scope-verification` | definition | `portfolio-construction-risk/performance-standards` |  | `performance-manager-evaluation` |  |  |
| `meth:gips-return-calculations` | method | `portfolio-construction-risk/performance-standards` |  | `performance-manager-evaluation` |  |  |
| `meth:gips-composite-membership` | method | `portfolio-construction-risk/performance-standards` |  | `performance-manager-evaluation` |  |  |
| `ex:gips-composite-report` | example | `portfolio-construction-risk/performance-standards` |  | `performance-manager-evaluation` |  |  |
| `meth:institutional-esg-integration` | method | `portfolio-construction-risk/institutional-portfolios` | `portfolio-construction-risk/esg-integration` | `climate-sustainable` |  |  |
| `def:portfolio-management-process` | definition | `portfolio-construction-risk/investment-process-planning` |  | `investment-policy-allocation` | new |  |
| `def:investor-types-needs` | definition | `portfolio-construction-risk/investment-process-planning` |  | `investment-policy-allocation` | new |  |
| `def:asset-management-industry` | definition | `portfolio-construction-risk/investment-process-planning` |  | `investment-policy-allocation` | new |  |
| `meth:investment-policy-statement` | method | `portfolio-construction-risk/investment-process-planning` |  | `investment-policy-allocation` | new |  |
| `meth:asset-class-portfolio-construction` | method | `portfolio-construction-risk/investment-process-planning` |  | `investment-policy-allocation` | new |  |
| `ex:investment-planning-case` | example | `portfolio-construction-risk/investment-process-planning` |  | `investment-policy-allocation` | new |  |
| `def:behavioural-biases` | definition | `portfolio-construction-risk/behavioural-finance` |  | `investment-policy-allocation` | new |  |
| `mech:biases-market-anomalies` | mechanism | `portfolio-construction-risk/behavioural-finance` |  | `investment-policy-allocation` | new | `equity-event-driven`, `equity-factor-premia` |
| `def:investment-governance-allocation` | definition | `portfolio-construction-risk/strategic-asset-allocation` |  | `investment-policy-allocation` | new |  |
| `meth:economic-balance-sheet-allocation` | method | `portfolio-construction-risk/strategic-asset-allocation` |  | `investment-policy-allocation` | new |  |
| `def:allocation-approaches-risk` | definition | `portfolio-construction-risk/strategic-asset-allocation` |  | `investment-policy-allocation` | new |  |
| `meth:asset-class-factor-specification` | method | `portfolio-construction-risk/strategic-asset-allocation` |  | `investment-policy-allocation` | new |  |
| `meth:asset-only-allocation-mvo` | method | `portfolio-construction-risk/strategic-asset-allocation` |  | `investment-policy-allocation` | new |  |
| `meth:allocation-implementation-rebalancing` | method | `portfolio-construction-risk/strategic-asset-allocation` |  | `investment-policy-allocation` | new |  |
| `meth:allocation-robustness-liquidity-risk-budget` | method | `portfolio-construction-risk/strategic-asset-allocation` |  | `investment-policy-allocation` | new |  |
| `meth:liability-relative-allocation` | method | `portfolio-construction-risk/strategic-asset-allocation` |  | `investment-policy-allocation` | new |  |
| `meth:goals-based-allocation-heuristics` | method | `portfolio-construction-risk/strategic-asset-allocation` |  | `investment-policy-allocation` | new |  |
| `meth:allocation-constraints-taxes-revision` | method | `portfolio-construction-risk/strategic-asset-allocation` |  | `investment-policy-allocation` | new |  |
| `meth:tactical-shifts-behavioural-biases` | method | `portfolio-construction-risk/strategic-asset-allocation` |  | `investment-policy-allocation` | new |  |
| `meth:forward-commitment-risk-overlays` | method | `portfolio-construction-risk/derivative-overlays` |  | `investment-policy-allocation` | new |  |
| `meth:volatility-derivative-applications` | method | `portfolio-construction-risk/derivative-overlays` |  | `investment-policy-allocation` | new | `option-premia-dealers` |
| `meth:derivative-overlay-allocation` | method | `portfolio-construction-risk/derivative-overlays` |  | `investment-policy-allocation` | new | `option-implied-information` |
| `ex:endowment-derivative-overlay-case` | example | `portfolio-construction-risk/derivative-overlays` |  | `investment-policy-allocation` | new |  |
| `def:hedge-fund-features` | definition | `portfolio-construction-risk/hedge-fund-strategies` |  | `investment-policy-allocation` | new |  |
| `meth:hedge-fund-strategy-classification` | method | `portfolio-construction-risk/hedge-fund-strategies` |  | `investment-policy-allocation` | new | `equity-event-driven`, `trend-following` |
| `meth:hedge-fund-factor-exposures` | method | `portfolio-construction-risk/hedge-fund-strategies` |  | `investment-policy-allocation` | new |  |
| `def:alternatives-roles-opportunity-set` | definition | `portfolio-construction-risk/alternatives-allocation` |  | `investment-policy-allocation` | new | `trend-following` |
| `meth:alternatives-allocation-approaches` | method | `portfolio-construction-risk/alternatives-allocation` |  | `investment-policy-allocation` | new |  |
| `def:common-investor-contagion` | definition | `portfolio-risk-financing/crowding-contagion` |  | `funding-crowding` |  | `statistical-arbitrage` |
| `mod:margin-liquidity-spiral` | model | `portfolio-risk-financing/crowding-contagion` |  | `funding-crowding` |  |  |
| `mod:liquidity-spirals` | model | `portfolio-risk-financing/crowding-contagion` |  | `funding-crowding` |  | `crypto-leverage-liquidations` |
| `def:money-market-reference-rates` | definition | `portfolio-risk-financing/money-markets` |  | `money-markets-repo-lending` |  |  |
| `ev:money-fund-runs` | evidence | `portfolio-risk-financing/money-markets` |  | `money-markets-repo-lending` |  |  |
| `def:short-term-funding-repo` | definition | `portfolio-risk-financing/money-markets` |  | `money-markets-repo-lending` |  |  |
| `def:street-name-beneficial-ownership` | definition | `portfolio-risk-financing/securities-lending` |  | `money-markets-repo-lending` |  |  |
| `mech:securities-lending-short-sale` | mechanism | `portfolio-risk-financing/securities-lending` |  | `money-markets-repo-lending` |  |  |
| `meth:margin-purchase-leverage` | method | `portfolio-risk-financing/securities-lending` |  | `money-markets-repo-lending` |  |  |
| `def:securities-lending-fee-rebate` | definition | `portfolio-risk-financing/securities-lending` |  | `money-markets-repo-lending` |  |  |
| `def:counterparty-exposure-measures` | definition | `portfolio-risk-financing/counterparty-xva` |  | `collateral-xva` |  | `corporate-credit-cds` |
| `meth:credit-valuation-adjustment` | method | `portfolio-risk-financing/counterparty-xva` |  | `collateral-xva` |  | `corporate-credit-cds` |
| `def:wrong-way-risk` | definition | `portfolio-risk-financing/counterparty-xva` |  | `collateral-xva` |  | `corporate-credit-cds` |
| `rule:counterparty-credit-cva-capital` | rule | `portfolio-risk-financing/counterparty-xva` |  | `collateral-xva` |  | `corporate-credit-cds` |
| `def:institutional-investor-characteristics` | definition | `portfolio-construction-risk/institutional-portfolios` | `portfolio-risk-financing/institutional-portfolios` | `alm-liquidity` |  |  |
| `meth:db-pension-risk` | method | `portfolio-construction-risk/institutional-portfolios` | `portfolio-risk-financing/institutional-portfolios` | `alm-liquidity` |  |  |
| `meth:institutional-ips-portfolios` | method | `portfolio-construction-risk/institutional-portfolios` | `portfolio-risk-financing/institutional-portfolios` | `alm-liquidity` |  |  |
| `meth:swf-risk-case` | method | `portfolio-construction-risk/institutional-portfolios` | `portfolio-risk-financing/institutional-portfolios` | `alm-liquidity` |  | `climate-sustainable` |
| `meth:endowment-liquidity-allocation` | method | `portfolio-construction-risk/institutional-portfolios` | `portfolio-risk-financing/institutional-portfolios` | `alm-liquidity` |  |  |
| `meth:liability-matching-ladders` | method | `rates-credit-mortgages/fixed-income-portfolio-management` | `portfolio-risk-financing/liability-matching` | `alm-liquidity` |  |  |
| `meth:immunisation-liabilities` | method | `rates-credit-mortgages/fixed-income-portfolio-management` | `portfolio-risk-financing/liability-matching` | `alm-liquidity` |  |  |
| `res:synthetic-short-put-call` | result | `portfolio-risk-financing/synthetic-shorts` |  | `synthetic-equity-cfd-trs` |  |  |
| `ev:empty-voting-equity-derivatives` | evidence | `portfolio-risk-financing/synthetic-shorts` |  | `synthetic-equity-cfd-trs` |  |  |
| `def:market-functions` | definition | `execution-market-making/market-organisation` |  | `market-organisation-liquidity` | new |  |
| `def:trader-motives` | definition | `execution-market-making/market-organisation` |  | `market-organisation-liquidity` | new |  |
| `res:zero-sum-skill-luck` | result | `execution-market-making/market-organisation` |  | `market-organisation-liquidity` | new |  |
| `def:market-intermediaries` | definition | `execution-market-making/market-organisation` |  | `market-organisation-liquidity` | new |  |
| `def:dealer-quotes-order-flow` | definition | `execution-market-making/market-organisation` |  | `market-organisation-liquidity` | new |  |
| `def:specialist-obligations-privileges` | definition | `execution-market-making/market-organisation` |  | `market-organisation-liquidity` | new |  |
| `def:market-structures-venues` | definition | `execution-market-making/market-organisation` |  | `market-organisation-liquidity` | new |  |
| `def:trading-sessions-execution-systems` | definition | `execution-market-making/market-organisation` |  | `market-organisation-liquidity` | new |  |
| `def:liquidity-dimensions` | definition | `execution-market-making/market-organisation` |  | `market-organisation-liquidity` | new |  |
| `def:floor-automated-trading-systems` | definition | `execution-market-making/trading-systems` |  | `market-organisation-liquidity` | new |  |
| `def:fundamental-value` | definition | `execution-market-making/market-making-models` | `execution-market-making/informed-trading` | `market-organisation-liquidity` | new |  |
| `res:informed-trading-aggregation` | result | `execution-market-making/market-making-models` | `execution-market-making/informed-trading` | `market-organisation-liquidity` | new |  |
| `def:informed-trader-types` | definition | `execution-market-making/market-making-models` | `execution-market-making/informed-trading` | `market-organisation-liquidity` | new |  |
| `def:winners-curse` | definition | `execution-market-making/market-making-models` | `execution-market-making/informed-trading` | `market-organisation-liquidity` | new |  |
| `def:market-efficiency` | definition | `execution-market-making/market-making-models` | `execution-market-making/informed-trading` | `market-organisation-liquidity` | new |  |
| `def:inside-information` | definition | `execution-market-making/market-making-models` | `execution-market-making/informed-trading` | `market-organisation-liquidity` | new |  |
| `res:insider-trading-deterrence` | result | `execution-market-making/market-making-models` | `execution-market-making/informed-trading` | `market-organisation-liquidity` | new |  |
| `def:price-formation-process` | definition | `execution-market-making/market-making-models` | `execution-market-making/informed-trading` | `market-organisation-liquidity` | new |  |
| `def:arbitrage` | definition | `execution-market-making/market-making-models` | `execution-market-making/arbitrage-anticipation` | `market-organisation-liquidity` | new |  |
| `res:arbitrage-risks` | result | `execution-market-making/market-making-models` | `execution-market-making/arbitrage-anticipation` | `market-organisation-liquidity` | new |  |
| `def:order-anticipation` | definition | `execution-market-making/market-making-models` | `execution-market-making/arbitrage-anticipation` | `market-organisation-liquidity` | new |  |
| `def:bluffing-manipulation` | definition | `execution-market-making/market-making-models` | `execution-market-making/arbitrage-anticipation` | `market-organisation-liquidity` | new |  |
| `def:spread-measures` | definition | `execution-market-making/market-making-models` | `execution-market-making/spread-measurement` | `market-organisation-liquidity` | new |  |
| `res:roll-spread-estimator` | result | `execution-market-making/market-making-models` | `execution-market-making/spread-measurement` | `market-organisation-liquidity` | new |  |
| `res:spread-component-identification` | result | `execution-market-making/market-making-models` | `execution-market-making/spread-measurement` | `market-organisation-liquidity` | new |  |
| `res:spread-determinants` | result | `execution-market-making/market-making-models` | `execution-market-making/spread-measurement` | `market-organisation-liquidity` | new |  |
| `def:outside-spread` | definition | `execution-market-making/market-making-models` | `execution-market-making/spread-measurement` | `market-organisation-liquidity` | new |  |
| `def:volatility-components` | definition | `execution-market-making/market-making-models` | `execution-market-making/volatility-liquidity-crashes` | `market-organisation-liquidity` | new |  |
| `meth:garman-klass-volatility` | method | `execution-market-making/market-making-models` | `execution-market-making/volatility-liquidity-crashes` | `market-organisation-liquidity` | new |  |
| `def:intraday-overnight-returns` | definition | `execution-market-making/market-making-models` | `execution-market-making/volatility-liquidity-crashes` | `market-organisation-liquidity` | new |  |
| `meth:spread-volatility-regression` | method | `execution-market-making/market-making-models` | `execution-market-making/volatility-liquidity-crashes` | `market-organisation-liquidity` | new |  |
| `mech:bubble-crash-dynamics` | mechanism | `execution-market-making/market-making-models` | `execution-market-making/volatility-liquidity-crashes` | `market-organisation-liquidity` | new |  |
| `mech:order-lifecycle` | mechanism | `execution-market-making/order-books` |  | `market-making-lob` |  |  |
| `def:order-instructions` | definition | `execution-market-making/order-books` |  | `market-making-lob` |  |  |
| `def:limit-order-book` | definition | `execution-market-making/order-books` |  | `market-making-lob` |  |  |
| `mech:order-matching-pricing` | mechanism | `execution-market-making/order-books` |  | `market-making-lob` |  |  |
| `res:limit-order-options` | result | `execution-market-making/order-books` |  | `market-making-lob` |  |  |
| `def:queue-imbalance` | definition | `execution-market-making/order-books` |  | `market-making-lob` |  |  |
| `mod:queue-reactive-intensities` | model | `execution-market-making/order-books` |  | `market-making-lob` |  |  |
| `mod:grossman-miller` | model | `execution-market-making/market-making-models` |  | `market-making-lob` |  |  |
| `res:grossman-miller-trading-fees` | result | `execution-market-making/market-making-models` |  | `market-making-lob` |  |  |
| `res:grossman-miller-liquidity-measures` | result | `execution-market-making/market-making-models` |  | `market-making-lob` |  |  |
| `mod:static-limit-order-depth` | model | `execution-market-making/market-making-models` |  | `market-making-lob` |  |  |
| `mod:avellaneda-stoikov` | model | `execution-market-making/market-making-models` |  | `market-making-lob` |  |  |
| `mod:kyle-single-auction` | model | `execution-market-making/market-making-models` |  | `market-making-lob` |  |  |
| `mod:glosten-milgrom` | model | `execution-market-making/market-making-models` |  | `market-making-lob` |  |  |
| `res:glosten-milgrom-half-spreads` | result | `execution-market-making/market-making-models` |  | `market-making-lob` |  |  |
| `res:glosten-milgrom-market-collapse` | result | `execution-market-making/market-making-models` |  | `market-making-lob` |  |  |
| `res:adverse-selection-spread-component` | result | `execution-market-making/market-making-models` |  | `market-making-lob` |  |  |
| `def:dealer-inventory-risk` | definition | `execution-market-making/market-making-models` |  | `market-making-lob` |  |  |
| `meth:dealer-quote-adjustment` | method | `execution-market-making/market-making-models` |  | `market-making-lob` |  |  |
| `mod:inventory-based-quotes` | model | `execution-market-making/market-making-models` |  | `market-making-lob` |  |  |
| `def:order-flow-imbalance` | definition | `execution-market-making/order-books` | `execution-market-making/order-flow-imbalance` | `lob-deep-learning` |  | `forecasting-generative-rl`, `ml-asset-pricing` |
| `res:option-market-maker-spreads` | result | `execution-market-making/options-dealing` |  | `options-execution` |  | `option-premia-dealers` |
| `meth:option-spread-measurement` | method | `execution-market-making/options-dealing` |  | `options-execution` |  |  |
| `mech:options-retail-wholesaler-routing` | mechanism | `execution-market-making/options-dealing` |  | `options-execution` |  | `short-dated-retail-options` |
| `ev:high-frequency-stylised-facts` | evidence | `execution-market-making/order-flow-statistics` |  | `market-simulation` |  |  |
| `meth:realised-variance-signature-plot` | method | `execution-market-making/order-flow-statistics` |  | `market-simulation` |  |  |
| `meth:intraday-deseasonalisation` | method | `execution-market-making/order-flow-statistics` |  | `market-simulation` |  |  |
| `def:market-clocks-durations` | definition | `execution-market-making/order-flow-statistics` |  | `market-simulation` |  |  |
| `def:order-event-point-processes` | definition | `execution-market-making/order-flow-statistics` |  | `market-simulation` |  |  |
| `mod:hawkes-order-flow` | model | `execution-market-making/order-flow-statistics` |  | `market-simulation` |  | `market-making-lob` |
| `def:fx-market-structure` | definition | `execution-market-making/fx-dealing` |  | `fx-dealer-market-making` |  |  |
| `mod:fx-internalisation-horizon` | model | `execution-market-making/fx-dealing` |  | `fx-dealer-market-making` |  |  |
| `mech:fx-last-look` | mechanism | `execution-market-making/fx-dealing` |  | `fx-dealer-market-making` |  |  |
| `def:hft-strategies` | definition | `execution-market-making/high-frequency-trading` |  | `hft-market-design` |  |  |
| `res:latency-arbitrage-arms-race` | result | `execution-market-making/high-frequency-trading` |  | `hft-market-design` |  |  |
| `res:hft-spread-investor-cost` | result | `execution-market-making/high-frequency-trading` |  | `hft-market-design` |  |  |
| `res:queue-position-value` | result | `execution-market-making/high-frequency-trading` |  | `hft-market-design` |  |  |
| `mod:make-take-fee-speed-race` | model | `execution-market-making/high-frequency-trading` |  | `hft-market-design` |  |  |
| `mod:depth-overflow-flash-crash` | model | `execution-market-making/high-frequency-trading` |  | `hft-market-design` |  |  |
| `ev:may-2010-flash-crash` | evidence | `execution-market-making/high-frequency-trading` |  | `hft-market-design` |  |  |
| `def:execution-benchmark` | definition | `execution-trading-costs/execution-benchmarks` |  | `price-impact-execution` | broadened |  |
| `def:implementation-shortfall` | definition | `execution-trading-costs/execution-benchmarks` |  | `price-impact-execution` | broadened |  |
| `meth:algorithm-benchmark-choice` | method | `execution-trading-costs/execution-benchmarks` |  | `price-impact-execution` | broadened |  |
| `meth:trade-sign-classification` | method | `execution-trading-costs/trade-signing` |  | `price-impact-execution` | broadened |  |
| `def:price-impact` | definition | `execution-trading-costs/impact-models` |  | `price-impact-execution` | broadened |  |
| `mod:propagator` | model | `execution-trading-costs/impact-models` |  | `price-impact-execution` | broadened |  |
| `res:no-price-manipulation` | result | `execution-trading-costs/impact-models` |  | `price-impact-execution` | broadened |  |
| `ev:square-root-impact` | evidence | `execution-trading-costs/impact-models` |  | `price-impact-execution` | broadened |  |
| `meth:post-execution-impact-profile` | method | `execution-trading-costs/impact-models` |  | `price-impact-execution` | broadened |  |
| `ev:intraday-impact-profile` | evidence | `execution-trading-costs/impact-models` |  | `price-impact-execution` | broadened |  |
| `meth:almgren-impact-estimation` | method | `execution-trading-costs/impact-models` |  | `price-impact-execution` | broadened |  |
| `meth:order-flow-impact-regression` | method | `execution-trading-costs/impact-models` |  | `price-impact-execution` | broadened |  |
| `mod:almgren-chriss-execution` | model | `execution-trading-costs/execution-scheduling` |  | `price-impact-execution` | broadened |  |
| `def:block-trade` | definition | `execution-trading-costs/execution-scheduling` |  | `price-impact-execution` | broadened |  |
| `mod:cartea-jaimungal-execution` | model | `execution-trading-costs/execution-control` |  | `price-impact-execution` | broadened | `reinforcement-learning-trading` |
| `def:automated-trading-architecture` | definition | `execution-trading-costs/execution-algorithms` |  | `price-impact-execution` | broadened |  |
| `def:trading-envelope` | definition | `execution-trading-costs/execution-algorithms` |  | `price-impact-execution` | broadened |  |
| `meth:execution-decision-support` | method | `execution-trading-costs/execution-algorithms` |  | `price-impact-execution` | broadened |  |
| `def:order-exposure-decisions` | definition | `execution-trading-costs/execution-algorithms` |  | `price-impact-execution` | broadened |  |
| `def:portfolio-trading` | definition | `execution-trading-costs/execution-algorithms` |  | `price-impact-execution` | broadened |  |
| `mech:positive-feedback-hedging` | mechanism | `execution-trading-costs/execution-algorithms` |  | `price-impact-execution` | broadened |  |
| `def:transaction-costs` | definition | `execution-trading-costs/transaction-cost-analysis` |  | `price-impact-execution` | broadened |  |
| `meth:transaction-cost-analysis` | method | `execution-trading-costs/transaction-cost-analysis` |  | `price-impact-execution` | broadened |  |
| `meth:aggressiveness-tradeoff` | method | `execution-trading-costs/transaction-cost-analysis` |  | `price-impact-execution` | broadened |  |
| `meth:execution-cost-measures` | method | `execution-trading-costs/trade-strategy-governance` |  | `price-impact-execution` | broadened |  |
| `meth:trade-strategy-selection` | method | `execution-trading-costs/trade-strategy-governance` |  | `price-impact-execution` | broadened |  |
| `def:trade-implementation-by-market` | definition | `execution-trading-costs/trade-strategy-governance` |  | `price-impact-execution` | broadened | `bond-swap-dealer-market-making` |
| `def:electronic-trading-environment` | definition | `execution-trading-costs/trade-strategy-governance` | `execution-trading-costs/electronic-trading` | `market-structure-execution-quality` |  |  |
| `def:smart-order-routing` | definition | `execution-trading-costs/smart-order-routing` |  | `market-structure-execution-quality` |  |  |
| `res:fee-adjusted-venue-choice` | result | `execution-trading-costs/smart-order-routing` |  | `market-structure-execution-quality` |  |  |
| `meth:passive-order-split` | method | `execution-trading-costs/smart-order-routing` |  | `market-structure-execution-quality` |  |  |
| `def:dark-pools-crossing` | definition | `execution-trading-costs/dark-trading-fragmentation` |  | `market-structure-execution-quality` |  |  |
| `meth:venue-market-share` | method | `execution-trading-costs/dark-trading-fragmentation` |  | `market-structure-execution-quality` |  |  |
| `meth:fragmentation-concentration-metrics` | method | `execution-trading-costs/dark-trading-fragmentation` |  | `market-structure-execution-quality` |  |  |
| `mod:sor-market-share-dynamics` | model | `execution-trading-costs/dark-trading-fragmentation` |  | `market-structure-execution-quality` |  |  |
| `ev:european-fragmentation-evidence` | evidence | `execution-trading-costs/dark-trading-fragmentation` |  | `market-structure-execution-quality` |  |  |
| `def:best-execution` | definition | `execution-trading-costs/execution-quality` |  | `market-structure-execution-quality` |  |  |
| `def:broker-agency-conflicts` | definition | `execution-trading-costs/execution-quality` |  | `market-structure-execution-quality` |  |  |
| `meth:trade-execution-evaluation-governance` | method | `execution-trading-costs/trade-strategy-governance` | `execution-trading-costs/execution-quality` | `market-structure-execution-quality` |  |  |
| `def:market-regulation-design` | definition | `execution-trading-costs/market-regulation` |  | `market-structure-execution-quality` |  |  |
| `mech:venue-competition-fragmentation` | mechanism | `execution-trading-costs/market-regulation` |  | `market-structure-execution-quality` |  |  |
| `rule:us-equity-market-structure` | rule | `execution-trading-costs/market-regulation` |  | `market-structure-execution-quality` |  |  |
| `rule:eu-trading-venue-transparency` | rule | `execution-trading-costs/market-regulation` |  | `market-structure-execution-quality` |  |  |
| `mech:circuit-breakers-trading-halts` | mechanism | `execution-trading-costs/market-regulation` |  | `market-structure-execution-quality` |  |  |
| `rule:spoofing-securities-markets` | rule | `execution-trading-costs/market-regulation` |  | `market-structure-execution-quality` |  |  |
| `def:tick-size` | definition | `execution-trading-costs/tick-size` |  | `market-structure-execution-quality` |  |  |
| `ev:tick-size-market-quality` | evidence | `execution-trading-costs/tick-size` |  | `market-structure-execution-quality` |  |  |
| `mod:harris-discretised-spread` | model | `execution-trading-costs/tick-size` |  | `market-structure-execution-quality` |  |  |
| `def:fixed-income-market-structure` | definition | `execution-trading-costs/fixed-income-trading` |  | `otc-fixed-income-trading` |  | `bond-swap-dealer-market-making`, `municipal-bonds`, `treasury-market-functioning` |
| `rule:us-eu-bond-transparency` | rule | `execution-trading-costs/fixed-income-trading` |  | `otc-fixed-income-trading` |  |  |
| `ev:bond-transparency-trading-costs` | evidence | `execution-trading-costs/fixed-income-trading` |  | `otc-fixed-income-trading` |  |  |
| `mech:etf-creation-redemption` | mechanism | `execution-trading-costs/etf-mechanics` |  | `etf-index-closing-execution` |  |  |
| `meth:etf-trading-tracking-premiums` | method | `execution-trading-costs/etf-mechanics` |  | `etf-index-closing-execution` |  |  |
| `meth:etf-costs-risks-uses` | method | `execution-trading-costs/etf-mechanics` |  | `etf-index-closing-execution` |  |  |
| `ev:index-reconstitution-impact` | evidence | `execution-trading-costs/impact-models` | `execution-trading-costs/etf-mechanics` | `etf-index-closing-execution` |  | `demand-flows-passive`, `price-impact-execution` |
| `conv:cme-globex-trading` | convention | `execution-trading-costs/futures-execution` |  | `futures-execution` |  |  |
| `conv:futures-block-efrp` | convention | `execution-trading-costs/futures-execution` |  | `futures-execution` |  |  |
| `mech:futures-margin-settlement` | mechanism | `execution-trading-costs/futures-execution` |  | `futures-execution` |  |  |
| `ev:index-futures-price-discovery` | evidence | `execution-trading-costs/futures-execution` |  | `futures-execution` |  |  |
| `conv:government-bond-futures` | convention | `execution-trading-costs/futures-execution` |  | `futures-execution` |  | `treasury-market-functioning` |
| `def:contango-backwardation-stocks` | definition | `energy-commodities/commodity-curves` |  | `commodity-storage-curves` |  | `commodity-factor-strategies`, `commodity-information-discovery`, `return-predictability` |
| `def:futures-hedge-basis` | definition | `energy-commodities/futures-hedging` |  | `commodity-hedging` |  |  |
| `mod:minimum-variance-hedge-ratio` | model | `energy-commodities/futures-hedging` |  | `commodity-hedging` |  |  |
| `def:metals-markets` | definition | `physical-commodity-markets/physical-markets` | `physical-commodity-markets/metals-markets` | `metals-storage-delivery` |  |  |
| `def:agricultural-markets` | definition | `physical-commodity-markets/physical-markets` | `physical-commodity-markets/agricultural-markets` | `agricultural-futures-delivery` |  |  |
| `def:crude-oil-markets` | definition | `physical-commodity-markets/physical-markets` | `physical-commodity-markets/crude-oil-markets` | `crude-oil-products` |  |  |
| `meth:commodity-futures-return-components` | method | `commodity-investing-premia/commodity-futures-investing` | `commodity-investing-premia/commodity-return-components` | `commodity-premia` |  | `commodity-factor-strategies`, `commodity-index-products` |
| `def:commodity-features` | definition | `commodity-investing-premia/commodity-futures-investing` |  | `commodity-allocation-inflation` | broadened | `commodity-index-products` |
| `meth:commodity-sectors-participants` | method | `commodity-investing-premia/commodity-futures-investing` |  | `commodity-allocation-inflation` | broadened | `commodity-index-products` |
| `meth:commodity-swaps-index-construction` | method | `commodity-investing-premia/commodity-futures-investing` | `commodity-investing-premia/commodity-indices` | `commodity-index-products` |  |  |
| `def:commodity-indices-risk-return` | definition | `commodity-investing-premia/commodity-indices` |  | `commodity-index-products` |  |  |
| `def:natural-gas-market` | definition | `power-gas-environmental/natural-gas` |  | `gas-hub-pricing` |  |  |
| `def:alternative-investment-categories` | definition | `private-capital-allocator/alternative-investment-structures` |  | `pe-performance-measurement` | broadened |  |
| `def:alternative-fund-terms` | definition | `private-capital-allocator/alternative-investment-structures` |  | `pe-performance-measurement` | broadened |  |
| `meth:alternative-returns-after-fees` | method | `private-capital-allocator/alternative-investment-structures` |  | `pe-performance-measurement` | broadened |  |
| `meth:private-capital-diversification` | method | `private-capital-allocator/private-capital-foundations` | `private-capital-allocator/private-market-programmes` | `pe-performance-measurement` | broadened |  |
| `meth:private-public-market-comparison` | method | `private-capital-allocator/private-market-programmes` |  | `pe-performance-measurement` | broadened |  |
| `meth:private-fund-multiples-pme` | method | `private-capital-allocator/private-market-programmes` |  | `pe-performance-measurement` | broadened |  |
| `meth:gp-alignment-net-returns` | method | `private-capital-allocator/private-market-programmes` |  | `pe-performance-measurement` | broadened |  |
| `meth:private-capital-allocation` | method | `private-capital-allocator/private-equity-strategies` | `private-capital-allocator/private-market-programmes` | `pe-performance-measurement` | broadened |  |
| `def:private-equity-features` | definition | `private-capital-allocator/private-capital-foundations` | `private-capital-allocator/private-equity-strategies` | `private-equity-vc` |  |  |
| `meth:private-deal-process-exits` | method | `private-capital-allocator/private-market-programmes` | `private-capital-allocator/private-equity-strategies` | `private-equity-vc` |  |  |
| `meth:private-equity-strategies` | method | `private-capital-allocator/private-equity-strategies` |  | `private-equity-vc` |  |  |
| `meth:private-equity-valuation` | method | `private-capital-allocator/private-equity-strategies` |  | `private-equity-vc` |  |  |
| `def:private-debt-features` | definition | `private-capital-allocator/private-capital-foundations` | `private-capital-allocator/private-debt-special-situations` | `private-credit-workouts` |  |  |
| `meth:private-debt-financing-structures` | method | `private-capital-allocator/private-debt-special-situations` |  | `private-credit-workouts` |  |  |
| `meth:private-debt-credit-analysis` | method | `private-capital-allocator/private-debt-special-situations` |  | `private-credit-workouts` |  |  |
| `meth:special-situations-distressed` | method | `private-capital-allocator/private-debt-special-situations` |  | `private-credit-workouts` |  |  |
| `meth:private-fund-structures` | method | `private-capital-allocator/private-market-programmes` | `private-capital-allocator/private-fund-structures` | `fund-liquidity` |  |  |
| `def:real-estate-characteristics` | definition | `real-asset-investor/real-estate` |  | `property-valuation` |  |  |
| `meth:real-estate-value-drivers` | method | `real-asset-investor/real-estate` |  | `property-valuation` |  |  |
| `meth:real-estate-valuation-indexes` | method | `real-asset-investor/real-estate` |  | `property-valuation` |  |  |
| `meth:reit-valuation` | method | `real-asset-investor/real-estate` |  | `property-valuation` |  |  |
| `meth:private-real-estate-underwriting` | method | `real-asset-investor/real-estate` |  | `property-valuation` |  |  |
| `meth:real-assets-allocation` | method | `real-asset-investor/real-estate` |  | `property-valuation` |  |  |
| `def:infrastructure-characteristics` | definition | `real-asset-investor/infrastructure` |  | `infrastructure-regulated-assets` |  |  |
| `meth:infrastructure-underwriting` | method | `real-asset-investor/infrastructure` |  | `infrastructure-regulated-assets` |  |  |
| `meth:infrastructure-allocation` | method | `real-asset-investor/infrastructure` |  | `infrastructure-regulated-assets` |  |  |
| `meth:land-timber-farmland` | method | `real-asset-investor/land-timber-farmland` |  | `natural-resource-rights` |  |  |
| `meth:individual-wealth-capital` | method | `private-wealth-management/clients-industry` |  | `household-finance-lifecycle` | broadened |  |
| `meth:private-client-ips` | method | `private-wealth-management/clients-industry` |  | `household-finance-lifecycle` | broadened |  |
| `def:wealth-management-industry` | definition | `private-wealth-management/clients-industry` |  | `household-finance-lifecycle` | broadened |  |
| `meth:advising-families` | method | `private-wealth-management/clients-industry` |  | `household-finance-lifecycle` | broadened |  |
| `meth:goals-based-financial-plan` | method | `private-wealth-management/wealth-planning` |  | `household-finance-lifecycle` | broadened |  |
| `meth:lifetime-exposures` | method | `private-wealth-management/wealth-planning` |  | `household-finance-lifecycle` | broadened |  |
| `meth:private-client-allocation-review` | method | `private-wealth-management/wealth-planning` |  | `household-finance-lifecycle` | broadened |  |
| `meth:retirement-across-jurisdictions` | method | `private-wealth-management/wealth-planning` |  | `household-finance-lifecycle` | broadened |  |
| `meth:human-capital-risks` | method | `private-wealth-management/wealth-preservation` | `private-wealth-management/wealth-planning` | `household-finance-lifecycle` | broadened |  |
| `meth:private-client-tax-inflation` | method | `private-wealth-management/clients-industry` | `private-wealth-management/wealth-preservation` | `tax-aware-wealth-preservation` |  |  |
| `meth:tax-in-planning` | method | `private-wealth-management/wealth-planning` | `private-wealth-management/wealth-preservation` | `tax-aware-wealth-preservation` |  |  |
| `meth:purchasing-power-fx` | method | `private-wealth-management/wealth-preservation` |  | `tax-aware-wealth-preservation` |  |  |
| `meth:residency-citizenship` | method | `private-wealth-management/wealth-transfer` |  | `wealth-transfer-succession` |  |  |
| `meth:complex-client-situations` | method | `private-wealth-management/wealth-transfer` |  | `wealth-transfer-succession` |  |  |
| `meth:wealth-transfer-strategies` | method | `private-wealth-management/wealth-transfer` |  | `wealth-transfer-succession` |  |  |
| `def:distributed-ledger-applications` | definition | `digital-assets-prediction-markets/distributed-ledgers` |  | `stablecoin-tokenisation` | broadened | `crypto-perpetuals`, `staking-restaking` |
| `def:crypto-venue-instrument-structure` | definition | `digital-assets-prediction-markets/crypto-venues-perpetuals` |  | `crypto-perpetuals` |  | `crypto-price-discovery` |
| `mech:perpetual-funding` | mechanism | `digital-assets-prediction-markets/crypto-venues-perpetuals` |  | `crypto-perpetuals` |  |  |
| `def:crypto-trading-risk-layers` | definition | `digital-assets-prediction-markets/crypto-venues-perpetuals` |  | `crypto-perpetuals` |  | `crypto-exchange-failures-regulation` |
| `ev:stablecoin-runs` | evidence | `digital-assets-prediction-markets/stablecoins` |  | `stablecoin-pegs-runs` |  |  |
| `rule:stablecoin-standards` | rule | `digital-assets-prediction-markets/stablecoins` |  | `stablecoin-pegs-runs` |  |  |
| `mech:crypto-auto-deleveraging` | mechanism | `digital-assets-prediction-markets/crypto-venues-perpetuals` | `digital-assets-prediction-markets/crypto-auto-deleveraging` | `crypto-leverage-liquidations` |  |  |
| `meth:digital-asset-investment-analysis` | method | `crypto-spot-markets/digital-asset-investing` |  | `crypto-investors-etfs` |  | `crypto-exchange-failures-regulation`, `crypto-perpetuals`, `crypto-price-discovery`, `crypto-return-dynamics` |
| `def:amm-pool-mechanics` | definition | `onchain-protocols/amm-lending` |  | `amm-lending` |  | `crypto-perpetuals` |
| `mech:defi-lending-liquidation` | mechanism | `onchain-protocols/amm-lending` | `onchain-protocols/defi-lending` | `defi-lending-liquidations` |  |  |
| `ev:crypto-dated-futures-carry` | evidence | `crypto-trading-strategies/crypto-carry` |  | `crypto-arbitrage-carry` |  | `crypto-perpetuals` |

## Appendix C. Entries that changed file

Relative to `dc3f3f0`, across all passes; none changed file in pass 3.

| Entry | From | To | Printed under |
| --- | --- | --- | --- |
| `def:factor-model-types` | `asset-pricing/asset-pricing-models` | `asset-pricing/factor-model-tests` | `empirical-asset-pricing` |
| `meth:capm-regression` | `asset-pricing/asset-pricing-models` | `asset-pricing/factor-model-tests` | `empirical-asset-pricing` |
| `meth:commodity-swaps-index-construction` | `commodity-investing-premia/commodity-futures-investing` | `commodity-investing-premia/commodity-indices` | `commodity-index-products` |
| `meth:commodity-futures-return-components` | `commodity-investing-premia/commodity-futures-investing` | `commodity-investing-premia/commodity-return-components` | `commodity-premia` |
| `ev:cip-deviations` | `currency-markets/macro-fx` | `currency-markets/cross-currency-basis` | `fx-cip-dollar-funding` |
| `meth:cross-currency-basis-swaps` | `volatility-options/forward-commitment-valuation` | `currency-markets/cross-currency-basis` | `fx-cip-dollar-funding` |
| `meth:carry-trade-uip` | `currency-markets/fx-mechanics-parity` | `currency-markets/currency-carry` | `fx-premia` |
| `mod:fx-carry-trade` | `currency-markets/macro-fx` | `currency-markets/currency-carry` | `fx-premia` |
| `def:currency-regimes-intervention` | `currency-markets/macro-fx` | `currency-markets/currency-intervention` | `em-currencies-intervention` |
| `def:exchange-rate-regimes-capital-flows` | `currency-markets/fx-mechanics-parity` | `currency-markets/currency-intervention` | `em-currencies-intervention` |
| `def:fx-market-real-exchange-rates` | `currency-markets/fx-mechanics-parity` | `currency-markets/fx-market` | `fx-determination-forecasting` |
| `meth:cross-forward-rates` | `currency-markets/fx-mechanics-parity` | `currency-markets/fx-quotes-forwards` | `fx-funding-settlement` |
| `meth:currency-forward-mark-to-market` | `currency-markets/fx-mechanics-parity` | `currency-markets/fx-quotes-forwards` | `fx-funding-settlement` |
| `meth:fx-bid-offer-triangular-arbitrage` | `currency-markets/fx-mechanics-parity` | `currency-markets/fx-quotes-forwards` | `fx-funding-settlement` |
| `mech:crypto-auto-deleveraging` | `digital-assets-prediction-markets/crypto-venues-perpetuals` | `digital-assets-prediction-markets/crypto-auto-deleveraging` | `crypto-leverage-liquidations` |
| `def:arbitrage` | `execution-market-making/market-making-models` | `execution-market-making/arbitrage-anticipation` | `market-organisation-liquidity` |
| `def:bluffing-manipulation` | `execution-market-making/market-making-models` | `execution-market-making/arbitrage-anticipation` | `market-organisation-liquidity` |
| `def:order-anticipation` | `execution-market-making/market-making-models` | `execution-market-making/arbitrage-anticipation` | `market-organisation-liquidity` |
| `res:arbitrage-risks` | `execution-market-making/market-making-models` | `execution-market-making/arbitrage-anticipation` | `market-organisation-liquidity` |
| `def:fundamental-value` | `execution-market-making/market-making-models` | `execution-market-making/informed-trading` | `market-organisation-liquidity` |
| `def:informed-trader-types` | `execution-market-making/market-making-models` | `execution-market-making/informed-trading` | `market-organisation-liquidity` |
| `def:inside-information` | `execution-market-making/market-making-models` | `execution-market-making/informed-trading` | `market-organisation-liquidity` |
| `def:market-efficiency` | `execution-market-making/market-making-models` | `execution-market-making/informed-trading` | `market-organisation-liquidity` |
| `def:price-formation-process` | `execution-market-making/market-making-models` | `execution-market-making/informed-trading` | `market-organisation-liquidity` |
| `def:winners-curse` | `execution-market-making/market-making-models` | `execution-market-making/informed-trading` | `market-organisation-liquidity` |
| `res:informed-trading-aggregation` | `execution-market-making/market-making-models` | `execution-market-making/informed-trading` | `market-organisation-liquidity` |
| `res:insider-trading-deterrence` | `execution-market-making/market-making-models` | `execution-market-making/informed-trading` | `market-organisation-liquidity` |
| `def:order-flow-imbalance` | `execution-market-making/order-books` | `execution-market-making/order-flow-imbalance` | `lob-deep-learning` |
| `def:outside-spread` | `execution-market-making/market-making-models` | `execution-market-making/spread-measurement` | `market-organisation-liquidity` |
| `def:spread-measures` | `execution-market-making/market-making-models` | `execution-market-making/spread-measurement` | `market-organisation-liquidity` |
| `res:roll-spread-estimator` | `execution-market-making/market-making-models` | `execution-market-making/spread-measurement` | `market-organisation-liquidity` |
| `res:spread-component-identification` | `execution-market-making/market-making-models` | `execution-market-making/spread-measurement` | `market-organisation-liquidity` |
| `res:spread-determinants` | `execution-market-making/market-making-models` | `execution-market-making/spread-measurement` | `market-organisation-liquidity` |
| `def:intraday-overnight-returns` | `execution-market-making/market-making-models` | `execution-market-making/volatility-liquidity-crashes` | `market-organisation-liquidity` |
| `def:volatility-components` | `execution-market-making/market-making-models` | `execution-market-making/volatility-liquidity-crashes` | `market-organisation-liquidity` |
| `mech:bubble-crash-dynamics` | `execution-market-making/market-making-models` | `execution-market-making/volatility-liquidity-crashes` | `market-organisation-liquidity` |
| `meth:garman-klass-volatility` | `execution-market-making/market-making-models` | `execution-market-making/volatility-liquidity-crashes` | `market-organisation-liquidity` |
| `meth:spread-volatility-regression` | `execution-market-making/market-making-models` | `execution-market-making/volatility-liquidity-crashes` | `market-organisation-liquidity` |
| `def:electronic-trading-environment` | `execution-trading-costs/trade-strategy-governance` | `execution-trading-costs/electronic-trading` | `market-structure-execution-quality` |
| `ev:index-reconstitution-impact` | `execution-trading-costs/impact-models` | `execution-trading-costs/etf-mechanics` | `etf-index-closing-execution` |
| `meth:trade-execution-evaluation-governance` | `execution-trading-costs/trade-strategy-governance` | `execution-trading-costs/execution-quality` | `market-structure-execution-quality` |
| `meth:intangibles-goodwill-reporting` | `financial-statement-analysis/balance-sheet-analysis` | `financial-statement-analysis/long-lived-asset-accounting` | `accounting-measurement` |
| `meth:expense-recognition-capitalisation` | `financial-statement-analysis/income-statement-analysis` | `financial-statement-analysis/revenue-expense-recognition` | `accounting-measurement` |
| `meth:revenue-recognition-analysis` | `financial-statement-analysis/income-statement-analysis` | `financial-statement-analysis/revenue-expense-recognition` | `accounting-measurement` |
| `meth:time-valid-ml-experiment-record` | `ml-alternative-data/labelling-sample-weights` | `ml-alternative-data/ml-time-validity` | `financial-ml-evaluation` |
| `pit:label-weight-leakage` | `ml-alternative-data/labelling-sample-weights` | `ml-alternative-data/ml-time-validity` | `financial-ml-evaluation` |
| `meth:text-feature-engineering` | `ml-alternative-data/data-science-workflow` | `ml-alternative-data/text-features` | `text-llm-agents` |
| `meth:equity-index-valuation` | `multi-asset-systematic-macro/macro-regimes-data` | `multi-asset-systematic-macro/equity-index-valuation` | `cross-asset-style-premia` |
| `def:macroeconomic-indicators` | `multi-asset-systematic-macro/macro-regimes-data` | `multi-asset-systematic-macro/macro-indicators` | `macro-nowcasting-signals` |
| `meth:equity-macro-leading-indicators` | `multi-asset-systematic-macro/macro-regimes-data` | `multi-asset-systematic-macro/macro-indicators` | `macro-nowcasting-signals` |
| `data:us-macro-release-calendar` | `multi-asset-systematic-macro/macro-regimes-data` | `multi-asset-systematic-macro/macro-releases` | `macro-announcements-policy` |
| `meth:macro-event-queries` | `multi-asset-systematic-macro/macro-regimes-data` | `multi-asset-systematic-macro/macro-releases` | `macro-announcements-policy` |
| `meth:finite-difference-option-pricing` | `volatility-options/numerical-methods` | `numerical-optimisation/numerical-methods` | `numerical-methods-optimisation` |
| `meth:least-squares-monte-carlo` | `volatility-options/numerical-methods` | `numerical-optimisation/numerical-methods` | `numerical-methods-optimisation` |
| `meth:monte-carlo-greeks` | `volatility-options/numerical-methods` | `numerical-optimisation/numerical-methods` | `numerical-methods-optimisation` |
| `mech:defi-lending-liquidation` | `onchain-protocols/amm-lending` | `onchain-protocols/defi-lending` | `defi-lending-liquidations` |
| `def:agricultural-markets` | `physical-commodity-markets/physical-markets` | `physical-commodity-markets/agricultural-markets` | `agricultural-futures-delivery` |
| `def:crude-oil-markets` | `physical-commodity-markets/physical-markets` | `physical-commodity-markets/crude-oil-markets` | `crude-oil-products` |
| `def:metals-markets` | `physical-commodity-markets/physical-markets` | `physical-commodity-markets/metals-markets` | `metals-storage-delivery` |
| `meth:institutional-esg-integration` | `portfolio-construction-risk/institutional-portfolios` | `portfolio-construction-risk/esg-integration` | `climate-sustainable` |
| `meth:var-es-estimation-methods` | `portfolio-construction-risk/risk-models` | `portfolio-construction-risk/var-es-estimation` | `risk-tail-systemic` |
| `def:institutional-investor-characteristics` | `portfolio-construction-risk/institutional-portfolios` | `portfolio-risk-financing/institutional-portfolios` | `alm-liquidity` |
| `meth:db-pension-risk` | `portfolio-construction-risk/institutional-portfolios` | `portfolio-risk-financing/institutional-portfolios` | `alm-liquidity` |
| `meth:endowment-liquidity-allocation` | `portfolio-construction-risk/institutional-portfolios` | `portfolio-risk-financing/institutional-portfolios` | `alm-liquidity` |
| `meth:institutional-ips-portfolios` | `portfolio-construction-risk/institutional-portfolios` | `portfolio-risk-financing/institutional-portfolios` | `alm-liquidity` |
| `meth:swf-risk-case` | `portfolio-construction-risk/institutional-portfolios` | `portfolio-risk-financing/institutional-portfolios` | `alm-liquidity` |
| `meth:immunisation-liabilities` | `rates-credit-mortgages/fixed-income-portfolio-management` | `portfolio-risk-financing/liability-matching` | `alm-liquidity` |
| `meth:liability-matching-ladders` | `rates-credit-mortgages/fixed-income-portfolio-management` | `portfolio-risk-financing/liability-matching` | `alm-liquidity` |
| `def:private-debt-features` | `private-capital-allocator/private-capital-foundations` | `private-capital-allocator/private-debt-special-situations` | `private-credit-workouts` |
| `def:private-equity-features` | `private-capital-allocator/private-capital-foundations` | `private-capital-allocator/private-equity-strategies` | `private-equity-vc` |
| `meth:private-deal-process-exits` | `private-capital-allocator/private-market-programmes` | `private-capital-allocator/private-equity-strategies` | `private-equity-vc` |
| `meth:private-fund-structures` | `private-capital-allocator/private-market-programmes` | `private-capital-allocator/private-fund-structures` | `fund-liquidity` |
| `meth:private-capital-allocation` | `private-capital-allocator/private-equity-strategies` | `private-capital-allocator/private-market-programmes` | `pe-performance-measurement` |
| `meth:private-capital-diversification` | `private-capital-allocator/private-capital-foundations` | `private-capital-allocator/private-market-programmes` | `pe-performance-measurement` |
| `meth:human-capital-risks` | `private-wealth-management/wealth-preservation` | `private-wealth-management/wealth-planning` | `household-finance-lifecycle` |
| `meth:private-client-tax-inflation` | `private-wealth-management/clients-industry` | `private-wealth-management/wealth-preservation` | `tax-aware-wealth-preservation` |
| `meth:tax-in-planning` | `private-wealth-management/wealth-planning` | `private-wealth-management/wealth-preservation` | `tax-aware-wealth-preservation` |
| `meth:curve-trades-carry-rolldown` | `rates-credit-mortgages/monetary-policy-curves` | `rates-credit-mortgages/curve-trades` | `bond-risk-premia` |
| `meth:forward-rates-expected-returns` | `rates-credit-mortgages/term-structure-returns` | `rates-credit-mortgages/curve-trades` | `bond-risk-premia` |
| `def:fixed-income-universe` | `rates-credit-mortgages/monetary-policy-curves` | `rates-credit-mortgages/fixed-income-universe` | `bond-pricing-rate-risk` |
| `data:gsw-treasury-curve` | `rates-credit-mortgages/interest-rates` | `rates-credit-mortgages/gsw-treasury-curve` | `curve-term-structure` |
| `def:interest-rate-swaps` | `rates-credit-mortgages/monetary-policy-curves` | `rates-credit-mortgages/rate-swaps-clearing` | `rate-derivatives` |
| `mech:otc-clearing-collateral` | `rates-credit-mortgages/interest-rates` | `rates-credit-mortgages/rate-swaps-clearing` | `rate-derivatives` |
| `mod:multi-curve-fra-swap-valuation` | `rates-credit-mortgages/interest-rates` | `rates-credit-mortgages/rate-swaps-clearing` | `rate-derivatives` |
| `def:tips-breakevens` | `rates-credit-mortgages/monetary-policy-curves` | `rates-credit-mortgages/tips-breakevens` | `rates-inflation` |
| `mod:arch-conditional-variance` | `regression-time-series/time-series-models` | `regression-time-series/volatility-forecasting` | `time-series-volatility` |
| `def:market-structures-pricing` | `multi-asset-systematic-macro/firms-market-structure` | `systematic-equities/firms-market-structure` | `equity-events-fundamentals` |
| `meth:cost-output-shutdown` | `multi-asset-systematic-macro/firms-market-structure` | `systematic-equities/firms-market-structure` | `equity-events-fundamentals` |
| `meth:market-structure-identification` | `multi-asset-systematic-macro/firms-market-structure` | `systematic-equities/firms-market-structure` | `equity-events-fundamentals` |
| `meth:convertible-bond-valuation` | `rates-credit-mortgages/embedded-option-bonds` | `volatility-options/convertible-bonds` | `convertible-bonds` |
| `meth:greeks-delta-gamma-hedging` | `volatility-options/option-valuation` | `volatility-options/option-hedging` | `option-hedging-smile` |
| `meth:transaction-cost-hedging` | `volatility-options/option-valuation` | `volatility-options/option-hedging` | `option-hedging-smile` |
| `res:delta-hedging-volatility-mismatch` | `volatility-options/option-valuation` | `volatility-options/option-hedging` | `option-hedging-smile` |
