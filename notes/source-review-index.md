# Source-review index

The reference content is in `compendium/`. Detailed source findings, numerical checks, corrections, input identities and limitations are in [source-review-records.md](source-review-records.md). Entry-level review provenance is keyed by the stable LaTeX label in [entry-evidence.json](entry-evidence.json).

Research protocols and outputs are stored under `artefacts/<topic>/`; reading notes and pathway notes link to the relevant entries. Historical records retain dates and evidence identities. Descriptive filenames and topic names replace numbered editing identifiers. Renaming a record does not renew its verification.

Use `python3 tools/check_compendium.py --check` from the repository root to check entry structure and references. It does not verify source claims or measure learning progress.

## Source integration commits

These commits identify the original integration of each subject. The detailed record contains subsequent corrections.

| Subject | Commit |
|---|---|
| Legacy staging, tooling, map and checker | `3a02a41` |
| `market-making-lob` format pilot | `3a02a41` |
| Glosten–Milgrom and the dealer material | `07a0504` |
| Spread decomposition and inventory models | `79aa634` |
| Volatility and liquidity | `326ad36` |
| Information, market efficiency and price discovery | `80810ee` |
| Strategic trading models | `3780514` |
| Liquidity and market impact | `c7ed121` |
| Market impact models | `2214a1b` |
| Price impact estimation | `3d597b1` |
| Optimal execution problem | `bbaafa5` |
| Execution benchmarks | `5d113ac` |
| Execution algorithms | `3d93967` |
| Transaction cost analysis | `b699ed2` |
| Smart order routing | `4fb411c` |
| High-frequency trading strategies | `60753ff` |
| Reinforcement learning and ML in execution | `6d04e52` |
| Production considerations | `1c3fabc` |
| Equity market microstructure | `580463e` |
| Futures market microstructure | `fb56198` |
| FX market microstructure | `9a9a62e` |
| Options market microstructure | `c035b4f` |
| Fixed-income microstructure | `18eef7f` |
| Securities lending and synthetic shorts | `b56a121` |
| Crypto market microstructure | `9148410` |
| Research and backtest evaluation | `c45e2b5` |
| Risk assessment: model risk, regime change, shocks, contagion, monitoring | `e0451c9` |
| Transaction cost models: components and cost functions | `0224ac7` |
| Portfolio construction models: rules, mean–variance optimisation, signal portfolios | `4e7666d` |
| Risk models: factor exposures, limits and penalties | `cd7b13c` |
| Narang's systematic-investing cluster: overview and diagram, alpha models, execution (three files, chapter closed) | `2642451` |
| Hull's derivatives basics, forwards, futures and hedging, and the time-value file (three files, two chapters closed) | `9fbd551` |
| AFML data cluster: taxonomy, bars and multi-product series, labels, sample weights, fractional differentiation (five files, chapter closed) | `8be60d1` |
| Orders, the limit order book and queues; trade signing and order-flow imbalance; stylised facts, event time and point processes (eight files, one batch) | `d40d4c2` |
| The rest of the orders-and-matching folder: order instructions, matching and trade pricing, dark trading, routing and fragmentation (four files, folder closed) | `4d9d5da` |
| The foundations folder: market functions, motives, skill and luck, intermediaries, venues, sessions, liquidity; regulation, venue competition, U.S. and EU rules, circuit breakers (six files, folder closed) | `063de31` |
| The rest of the legacy microstructure chapter: market making (dealers, specialists, queue value, fees and the speed race, cross-asset arbitrage), information and volatility (price formation across venues, the Flash Crash and its toy model), and the feature- and data-engineering files (eight files, chapter closed) | `ca6986e` |
| The legacy macro chapter: global macro, its record, sizing and practitioners; regimes, indicators, releases and event queries; central banks, the Taylor rule, the policy path and LIBOR's end, curve trades, TIPS, swaps and money markets; sovereign credit and CDS; currencies; equity indices, valuation and the VIX; commodity curves, indices, oil, gas, metals and agriculture (three files, chapter closed, legacy part removed) | `f73498d` |
| Four audit corrections; 15 queue leftovers, 19 older backlog items and six macro empirical stubs (three bounded tests) | `820517a` |
| Eight audit repairs (three empirical tests rerun, v1 kept) and a source-review coverage | `12e634a` |
| Six audit repairs and a source-review coverage (four bounded tests) | `012aa19` |
