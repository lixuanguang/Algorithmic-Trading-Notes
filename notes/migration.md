# Compendium migration record

The working record for moving the notes written before the study method into the guide's typed entries. The plan, with its type mapping and order, is in [compendium/README.md](../compendium/README.md). This file holds the conventions, the current status, an index of the slices and the map of legacy files to pathways; each slice's full record (sources, findings, checks, dispositions, counts, build) is in [migration-slices.md](migration-slices.md). Check the map and progress with `python3 tools/migration_status.py` (add `--check` to fail on any problem).

## Four kinds of progress, kept apart

| Kind | What it means | Where it is recorded | Set by |
|---|---|---|---|
| Migration progress | A legacy block has a disposition: rewritten as an entry, merged into one, stubbed in a backlog, or deleted | Each slice's dispositions in [migration-slices.md](migration-slices.md); counts in this file's status and index, and `tools/migration_status.py` | The migration |
| Source verification | An entry's claims have been compared with the passages at their locators | Each entry's *Status: Verification*, and the *Checks and their limits* of each slice in [migration-slices.md](migration-slices.md) | Whoever reads the passage |
| Learner mastery | A pathway's checkpoint passed from your own notes, readings closed | `notes/log.md`, *Mastered* | You only |
| Pathway consolidation | Everything the pathway relies on is in checked entries and its backlog is empty | `notes/log.md`, *Consolidated* | You, after review |

Migrating a block and compiling the result advances only the first. An entry written during migration starts as a draft whose verification says exactly what was compared; no migration step sets a mastery or consolidation date.

## Conventions

- **Legacy staging.** Old chapters live in `compendium/legacy/<section-key>/` and compile, through `compendium/legacy/part.tex`, as the final part *Notes awaiting migration*. This is a temporary convention of this repository, not part of the guide's layout. Their chapter labels carry a `legacy:` prefix so that they never collide with the canonical chapter label (`\label{<section-key>}`) when that chapter appears. Their block, figure and remark labels are unchanged.
- **Canonical homes.** Migrated entries go in `compendium/<section-key>/`, in the section where the guide first needs the concept. Other pathways link to that entry rather than restating it.
- **Map.** `% migrate-to: key, key` on the first line of each legacy file with blocks names the pathways its blocks are *candidate* material for. These lists are provisional: drawn from the plan's folder table and narrowed by file name, not from reading every block. A file listing several pathways is shared material; none of those pathways owns its blocks until one is assigned.
- **Assignment.** `% assign: <pathway-key>` on the line before a block assigns that block to one pathway. Only assigned blocks, or blocks in a file with a single candidate, count towards one pathway; the status script lists shared, unassigned blocks separately.
- **Removal.** A block is deleted from a legacy file only when its content is represented in an entry, a backlog stub or an artefact, and the pathways that list the file can find it: the deletion site keeps a `% migrated:` comment naming the destination labels.
- **Derivations.** When an entry keeps only the idea of a proof, the full working goes to `notes/artefacts/<pathway-key>/`, and the entry's *Further reading* names the file.

- **Records.** Each slice appends one section to [migration-slices.md](migration-slices.md) and one row to the index below. A correction to a finished slice is appended as a follow-up; earlier records are left as written.

## Status after slice 26 (15 October 2026)

- **Legacy blocks:** 600 = 530 shared + 41 single-candidate + 29 assigned (867 in the finance chapters at the baseline).
- **Entries:** 98, all *draft* and *partly checked*. **Human review is outstanding** for every entry; the review items of each slice are under its *For review* in [migration-slices.md](migration-slices.md), and the open questions in [log.md](log.md).
- **Legacy chapters emptied:** `execution-trading-costs` (only its 21 unused figures remain).
- **Build:** `latexmk -g -pdf compendium.tex` exits 0; 216 pages; no LaTeX warnings; 0 overfull and 26 underfull boxes, all in the legacy volatility-options and portfolio files; one inherited `page.i` duplicate-destination warning. Tests: 14 pass.

## Slices

Blocks are the legacy blocks counted by `migration_status.py` before and after the slice; entries likewise. Follow-ups are the corrections recorded after the slice, each under its own heading in [migration-slices.md](migration-slices.md).

| Slice | Topic | Commit | Blocks | Entries | Follow-ups |
|---|---|---|---|---|---|
| Phase 0 | Legacy staging, tooling, map and checker | `3a02a41` | 879 → 867 (tooling appendix moved out) | 0 | |
| Pilot | `market-making-lob` format pilot | `3a02a41` | 867 → 858 | 0 → 6 | |
| 2 | Glosten–Milgrom and the dealer material | `07a0504` | 858 → 840 | 6 → 12 | |
| 3 | Spread decomposition and inventory models | `79aa634` | 840 → 819 | 12 → 18 | |
| 4 | Volatility and liquidity | `326ad36` | 819 → 805 | 18 → 22 | |
| 5 | Information, market efficiency and price discovery | `80810ee` | 805 → 787 | 22 → 28 | |
| 6 | Strategic trading models | `3780514` | 787 → 757 | 28 → 35 | |
| 7 | Liquidity and market impact | `c7ed121` | 757 → 751 | 35 → 38 | |
| 8 | Market impact models | `2214a1b` | 751 → 741 | 38 → 40 | |
| 9 | Price impact estimation | `3d597b1` | 741 → 733 | 40 → 44 | |
| 10 | Optimal execution problem | `bbaafa5` | 733 → 724 | 44 → 46 | |
| 11 | Execution benchmarks | `5d113ac` | 724 → 721 | 46 → 49 | |
| 12 | Execution algorithms | `3d93967` | 721 → 704 | 49 → 54 | |
| 13 | Transaction cost analysis | `b699ed2` | 704 → 679 | 54 → 60 | |
| 14 | Smart order routing | `4fb411c` | 679 → 664 | 60 → 63 | |
| 15 | High-frequency trading strategies | `60753ff` | 664 → 661 | 63 → 66 | |
| 16 | Reinforcement learning and ML in execution | `6d04e52` | 661 → 657 | 66 → 67 | Corrections to `mod:cartea-jaimungal-execution` (`8aa672a`) |
| 17 | Production considerations | `1c3fabc` | 657 → 646 | 67 → 70 | Clarifications |
| 18 | Equity market microstructure | `580463e` | 646 → 640 | 70 → 71 | ETF and Harris precision |
| 19 | Futures market microstructure | `fb56198` | 640 → 633 | 71 → 75 | Corrections (`bd4ba54`); account classes and second-month settlement |
| 20 | FX market microstructure | `9a9a62e` | 633 → 629 | 75 → 78 | Corrections |
| 21 | Options market microstructure | `c035b4f` | 629 → 625 | 78 → 81 | Corrections |
| 22 | Fixed-income microstructure | `18eef7f` | 625 → 619 | 81 → 84 | Corrections |
| 23 | Securities lending and synthetic shorts | `b56a121` | 619 → 613 | 84 → 88 | Corrections (`74c643e`); lending opening |
| 24 | Crypto market microstructure | `9148410` | 613 → 609 | 88 → 91 | Socialised-loss trigger |
| 25 | Research and backtest evaluation | `c45e2b5` | 609 → 605 | 91 → 95 | Corrections |
| 26 | Risk assessment: model risk, regime change, shocks, contagion, monitoring | this slice's commit | 605 → 600 | 95 → 98 | |

## Next bounded slice

`compendium/legacy/portfolio-construction-risk/sysinv/txncostmod.tex` (2 blocks: *Transaction Cost Components*, *Types of Transaction Cost Models*), whose map names the section overview `portfolio-construction-risk`. Check its ownership against `execution-trading-costs` and `price-impact-execution`, and its overlap with `def:transaction-costs`, `meth:transaction-cost-analysis` and the impact entries before adding anything; Narang's chapter on transaction cost models in the third edition is the likely source, to be verified. The other `sysinv/` files (`alphamod.tex`, `riskmod.tex`, `portconstmod.tex`, `executionmod.tex`, the overview's method block), the three slice-5 assignments, the fifteen blocks assigned to `hft-market-design`, and the deferred items (the toy-model time term, Lehalle and Laruelle sec. 2.5.3, Ho–Stoll) are unchanged.

## File map

One row per legacy file with blocks; `tools/migration_status.py --check` fails if this table and the files' `% migrate-to:` lines disagree.

<!-- map:begin -->
| Legacy file | Candidate pathways |
|---|---|
| `compendium/legacy/execution-market-making/01_foundations_of_trading_and_market_organization/01_roles_of_financial_markets.tex` | execution-market-making, market-structure-execution-quality |
| `compendium/legacy/execution-market-making/01_foundations_of_trading_and_market_organization/02_market_participants_and_trading_motives.tex` | execution-market-making, market-structure-execution-quality |
| `compendium/legacy/execution-market-making/01_foundations_of_trading_and_market_organization/03_trading_venues_and_market_architecture.tex` | execution-market-making, market-structure-execution-quality |
| `compendium/legacy/execution-market-making/01_foundations_of_trading_and_market_organization/04_auction_and_dealer_market_structures.tex` | execution-market-making, market-structure-execution-quality |
| `compendium/legacy/execution-market-making/01_foundations_of_trading_and_market_organization/05_market_quality_and_efficiency.tex` | execution-market-making, market-structure-execution-quality |
| `compendium/legacy/execution-market-making/01_foundations_of_trading_and_market_organization/06_regulatory_and_structural_evolution.tex` | execution-market-making, market-structure-execution-quality |
| `compendium/legacy/execution-market-making/02_orders_matching_and_limit_order_books/01_order_types_and_instructions.tex` | execution-market-making, market-making-lob, market-structure-execution-quality |
| `compendium/legacy/execution-market-making/02_orders_matching_and_limit_order_books/02_order_lifecycle.tex` | execution-market-making, market-making-lob, market-structure-execution-quality |
| `compendium/legacy/execution-market-making/02_orders_matching_and_limit_order_books/03_limit_order_book_mechanics.tex` | execution-market-making, market-making-lob, market-structure-execution-quality |
| `compendium/legacy/execution-market-making/02_orders_matching_and_limit_order_books/04_matching_algorithms.tex` | execution-market-making, market-making-lob, futures-execution |
| `compendium/legacy/execution-market-making/02_orders_matching_and_limit_order_books/05_queue_dynamics_and_latency.tex` | execution-market-making, market-making-lob |
| `compendium/legacy/execution-market-making/02_orders_matching_and_limit_order_books/06_hidden_liquidity_and_dark_trading.tex` | execution-market-making, market-structure-execution-quality |
| `compendium/legacy/execution-market-making/02_orders_matching_and_limit_order_books/07_cross_venue_routing_and_fragmentation.tex` | execution-market-making, market-structure-execution-quality |
| `compendium/legacy/execution-market-making/03_information_price_formation_and_spreads/02_price_discovery.tex` | execution-market-making, market-making-lob, market-structure-execution-quality, hft-market-design |
| `compendium/legacy/execution-market-making/03_information_price_formation_and_spreads/08_volatility_and_liquidity_interaction.tex` | execution-market-making, market-making-lob, hft-market-design, market-structure-execution-quality |
| `compendium/legacy/execution-market-making/04_order_flow_and_empirical_microstructure/01_trade_classification_and_signed_flow.tex` | price-impact-execution, lob-deep-learning |
| `compendium/legacy/execution-market-making/04_order_flow_and_empirical_microstructure/02_order_flow_imbalance.tex` | market-making-lob, lob-deep-learning, price-impact-execution |
| `compendium/legacy/execution-market-making/04_order_flow_and_empirical_microstructure/03_stylized_facts_of_high_frequency_data.tex` | market-simulation, lob-deep-learning |
| `compendium/legacy/execution-market-making/04_order_flow_and_empirical_microstructure/06_trade_duration_and_event_time.tex` | market-simulation, lob-deep-learning |
| `compendium/legacy/execution-market-making/04_order_flow_and_empirical_microstructure/07_statistical_models_for_order_flow.tex` | market-simulation, market-making-lob |
| `compendium/legacy/execution-market-making/04_order_flow_and_empirical_microstructure/08_feature_engineering_for_microstructure_alpha.tex` | lob-deep-learning |
| `compendium/legacy/execution-market-making/04_order_flow_and_empirical_microstructure/09_microstructure_data_engineering.tex` | lob-deep-learning, market-simulation |
| `compendium/legacy/execution-market-making/05_market_making_and_liquidity_provision/01_economics_of_market_making.tex` | market-making-lob, execution-market-making |
| `compendium/legacy/execution-market-making/05_market_making_and_liquidity_provision/04_optimal_quoting_and_inventory_control.tex` | market-making-lob, execution-market-making |
| `compendium/legacy/execution-market-making/05_market_making_and_liquidity_provision/05_latency_and_queue_competition.tex` | market-making-lob, hft-market-design |
| `compendium/legacy/execution-market-making/05_market_making_and_liquidity_provision/06_cross_asset_and_cross_venue_market_making.tex` | market-making-lob, hft-market-design |
| `compendium/legacy/ml-alternative-data/data/datalabel.tex` | statistical-learning-foundations, financial-ml-evaluation, alternative-data-sources |
| `compendium/legacy/ml-alternative-data/data/datasampleweights.tex` | statistical-learning-foundations, financial-ml-evaluation, alternative-data-sources |
| `compendium/legacy/ml-alternative-data/data/datastruct.tex` | statistical-learning-foundations, financial-ml-evaluation, alternative-data-sources |
| `compendium/legacy/ml-alternative-data/data/fracdifffeat.tex` | statistical-learning-foundations, financial-ml-evaluation, alternative-data-sources |
| `compendium/legacy/ml-alternative-data/data/taxonomy.tex` | statistical-learning-foundations, financial-ml-evaluation, alternative-data-sources |
| `compendium/legacy/multi-asset-systematic-macro/01_regimes.tex` | multi-asset-systematic-macro, macro-regimes-stock-bond |
| `compendium/legacy/multi-asset-systematic-macro/02_transmission_maps.tex` | macro-nowcasting-signals, macro-announcements-policy, monetary-policy-curve, fx-determination-forecasting |
| `compendium/legacy/multi-asset-systematic-macro/03_practitioner_insights.tex` | multi-asset-systematic-macro |
| `compendium/legacy/portfolio-construction-risk/sysinv/alphamod.tex` | portfolio-construction-risk |
| `compendium/legacy/portfolio-construction-risk/sysinv/executionmod.tex` | portfolio-construction-risk |
| `compendium/legacy/portfolio-construction-risk/sysinv/portconstmod.tex` | portfolio-construction |
| `compendium/legacy/portfolio-construction-risk/sysinv/riskmod.tex` | portfolio-construction |
| `compendium/legacy/portfolio-construction-risk/sysinv/sysinvoverview.tex` | portfolio-construction-risk |
| `compendium/legacy/portfolio-construction-risk/sysinv/txncostmod.tex` | portfolio-construction-risk |
| `compendium/legacy/rates-credit-mortgages/01_tvm.tex` | rates-credit-mortgages, performance-manager-evaluation |
| `compendium/legacy/volatility-options/basic.tex` | volatility-options |
| `compendium/legacy/volatility-options/fwdfut.tex` | rates-credit-mortgages, commodity-hedging |
<!-- map:end -->
